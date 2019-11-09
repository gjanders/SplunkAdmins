from __future__ import absolute_import, division, print_function, unicode_literals
import requests
import xml.etree.ElementTree as ET
import logging
from logging.config import dictConfig
import json
import os
import sys
import glob
import xml.dom.minidom
from time import sleep
from subprocess import Popen, PIPE
import platform

"""
   Lookup Watcher

   Check the filesystem for lookup files, check the current size
   record stats around last update time, previous update time
   how regularly updated occur
   Store size & stats into a kvstore for usage by admins
"""

splunkLogsDir = os.environ['SPLUNK_HOME'] + "/var/log/splunk"
#Setup the logging
logging_config = dict(
    version = 1,
    formatters = {
        'f': {'format':
              '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
        },
    handlers = {
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.WARN},
        'file': {'class' : 'logging.handlers.RotatingFileHandler',
              'filename' : splunkLogsDir + '/lookup_watcher.log',
              'formatter': 'f',
              'maxBytes' :  2097152,
              'level': logging.DEBUG,
              'backupCount' : 5 }
        },        
    root = {
        'handlers': ['h','file'],
        'level': logging.DEBUG,
        },
)

dictConfig(logging_config)

logger = logging.getLogger()
logging.getLogger().setLevel(logging.INFO)


class LookupWatcher:

    # read XML configuration passed from splunkd
    def get_config(self):
        config = {}

        try:
            # read everything from stdin
            config_str = sys.stdin.read()

            # parse the config XML
            doc = xml.dom.minidom.parseString(config_str)
            root = doc.documentElement
            session_key = root.getElementsByTagName("session_key")[0].firstChild.data
            #Grab the session key in case we need it
            config['session_key'] = session_key
            config['checkpoint_dir'] = root.getElementsByTagName("checkpoint_dir")[0].firstChild.data
            conf_node = root.getElementsByTagName("configuration")[0]
            if conf_node:
                logger.debug("XML: found configuration")
                stanza = conf_node.getElementsByTagName("stanza")[0]
                if stanza:
                    stanza_name = stanza.getAttribute("name")
                    if stanza_name:
                        logger.debug("XML: found stanza " + stanza_name)
                        config["name"] = stanza_name
                        shortName = stanza_name.replace("splunkversioncontrol_backup://", "")

                        params = stanza.getElementsByTagName("param")
                        for param in params:
                            param_name = param.getAttribute("name")
                            logger.debug("i=\"%s\" XML: found param=\"%s\"" % (shortName, param_name))
                            if param_name and param.firstChild and \
                               param.firstChild.nodeType == param.firstChild.TEXT_NODE:
                                data = param.firstChild.data
                                config[param_name] = data
                                logger.debug("i=\"%s\" XML: \"%s\"=\"%s\"" % (shortName, param_name, data))

            if not config:
                raise Exception("Invalid configuration received from Splunk.")
        except Exception as e:
            raise Exception("Error getting Splunk configuration via STDIN: %s" % str(e))

        return config

    """

     Helper/utility functions
    
    """
    #helper function as per https://stackoverflow.com/questions/31433989/return-copy-of-dictionary-excluding-specified-keys
    def without_keys(self, d, keys):
        return {x: d[x] for x in d if x not in keys}

    ###########################
    #
    # Main logic section
    #
    ##########################    
    def run_script(self):
        config = self.get_config()
        #If we want debugMode, keep the debug logging, otherwise leave this at INFO level
        if 'debugMode' in config:
            debugMode = config['debugMode'].lower()
            if debugMode == "true" or debugMode == "t":
                logging.getLogger().setLevel(logging.DEBUG)

        logger.info("LookupWatcher begin run")
        headers={'Authorization': 'Splunk %s' % config['session_key']}

        #Verify=false is hardcoded to workaround local SSL issues
        url = 'https://localhost:8089/services/shcluster/captain/info?output_mode=json'
        res = requests.get(url, headers=headers, verify=False)
        if (res.status_code == 503):
            logger.debug("Non-shcluster / standalone instance, safe to run on this node")
        elif (res.status_code != requests.codes.ok):
            logger.fatal("unable to determine if this is a search head cluster or not, this is a bug, URL=%s statuscode=%s reason=%s, response=\"%s\"" % (url, res.status_code, res.reason, res.text))
            print("Fatal error, unable to determine if this is a search head cluster or not, refer to the logs")
            sys.exit(-1)
        elif (res.status_code == 200):
            #We're in a search head cluster, but are we the captain?
            json_dict = json.loads(res.text)
            if json_dict['origin'] != "https://localhost:8089/services/shcluster/captain/info":
                logger.info("Not on the captain, exiting now")
                return
            else:
                logger.info("On the captain node, running")
        
        #At this point we are either on the captain or a standalone server so safe to continue
        splunk_home = os.environ['SPLUNK_HOME']
        ostype = platform.system()
        #Find the lookup directories
        app_lookup_dirlist = glob.iglob(splunk_home + '/etc/apps/**/lookups')
        for lookup_dir in app_lookup_dirlist:
            logger.debug("Working with directory=%s" % (lookup_dir))
            files = [f for f in os.listdir(lookup_dir) if os.path.isfile(lookup_dir + '/' + f)]
            for afile in files:
                mtime = os.path.getmtime(lookup_dir + '/' + afile)
                size = os.path.getsize(lookup_dir + '/' + afile)
                #minor tweak to reduce the amount of information logged
                if ostype == "Windows":
                    lookup_loc = lookup_dir[lookup_dir.find("/apps\\") + 1:]
                else:
                    lookup_loc = lookup_dir[lookup_dir.find("/apps/") + 1:]
                logger.debug('dir=%s file=%s mtime=%s size=%s lookup_loc=%s' % (lookup_dir, afile, mtime, size, lookup_loc))
                if ostype == "Windows":
                    print('lookup=%s\\%s mtime=%s size=%s' % (lookup_loc, afile, mtime, size))
                else:
                    print('lookup=%s/%s mtime=%s size=%s' % (lookup_loc, afile, mtime, size))

        user_lookup_dirlist = glob.iglob(splunk_home + '/etc/users/**/**/lookups')
        for lookup_dir in user_lookup_dirlist:
            logger.debug("Working with directory=%s" % (lookup_dir))
            files = [f for f in os.listdir(lookup_dir) if os.path.isfile(lookup_dir + '/' + f)]
            for afile in files:
                mtime = os.path.getmtime(lookup_dir + '/' + afile)
                size = os.path.getsize(lookup_dir + '/' + afile)
                #minor tweak to reduce the amount of information logged
                if ostype == "Windows":
                    lookup_loc = lookup_dir[lookup_dir.find("/users\\") + 1:]
                else:
                    lookup_loc = lookup_dir[lookup_dir.find("/users/") + 1:]                   
                logger.debug('dir=%s file=%s mtime=%s size=%s lookup_loc=%s' % (lookup_dir, afile, mtime, size, lookup_loc))
                if ostype == "Windows":
                    print('lookup=%s\\%s mtime=%s size=%s' % (lookup_loc, afile, mtime, size))
                else:
                    print('lookup=%s/%s mtime=%s size=%s' % (lookup_loc, afile, mtime, size))

        logger.info("LookupWatcher end run")

