from __future__ import print_function
import requests
import logging
from logging.config import dictConfig
import os
import sys
import xml.dom.minidom, xml.sax.saxutils
from subprocess import Popen, PIPE
from time import sleep
from lookup_watcher_class import LookupWatcher 

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from splunklib.six.moves import range


"""
   Lookup Watcher

   Check the filesystem for lookup files, check the current size
   record stats around last update time, previous update time
   how regularly updated occur
   Store size & stats into a kvstore for usage by admins
"""

#Define the XML scheme for the inputs page
SCHEME = """<scheme>
    <title>Lookup Watcher</title>
    <description>Watch lookup files on the Splunk filesystem and record the size and most recent update stats in a kvstore file</description>
    <use_external_validation>false</use_external_validation>
    <streaming_mode>simple</streaming_mode>
    <endpoint>
        <args>
            <arg name="debugMode">
                <title>debugMode</title>
                <description>turn on DEBUG level logging (defaults to INFO) (true/false)</description>
                <validation>is_bool('debugMode')</validation>
                <required_on_create>false</required_on_create>
            </arg>
        </args>
    </endpoint>
</scheme>
"""

#Get the XML for validation
def get_validation_data():
    val_data = {}

    # read everything from stdin
    val_str = sys.stdin.read()

    # parse the validation XML
    doc = xml.dom.minidom.parseString(val_str)
    root = doc.documentElement

    logger.debug("XML: found items")
    item_node = root.getElementsByTagName("item")[0]
    if item_node:
        logger.debug("XML: found item")

        name = item_node.getAttribute("name")
        val_data["stanza"] = name

        params_node = item_node.getElementsByTagName("param")
        for param in params_node:
            name = param.getAttribute("name")
            logger.debug("Found param %s" % name)
            if name and param.firstChild and \
               param.firstChild.nodeType == param.firstChild.TEXT_NODE:
                val_data[name] = param.firstChild.data

    return val_data

# prints XML error data to be consumed by Splunk
def print_error(s):
    print("<error><message>%s</message></error>" % xml.sax.saxutils.escape(s))

#Run an OS process with a timeout, this way if a command gets "stuck" waiting for input it is killed
def runOSProcess(command, timeout=10):
    p = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    for t in range(timeout):
        sleep(1)
        if p.poll() is not None:
            #return p.communicate()
            (stdoutdata, stderrdata) = p.communicate()
            if p.returncode != 0:
                return stdoutdata, stderrdata, False
            else:
                return stdoutdata, stderrdata, True
    p.kill()
    return "", "timeout after %s seconds" % (timeout), False

#Validate the arguments to the app to ensure this will work...
def validate_arguments():
    #val_data = get_validation_data()
    return

#Print the scheme
def do_scheme():
    print(SCHEME)
    
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

# Script must implement these args: scheme, validate-arguments
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheme":
            do_scheme()
        elif sys.argv[1] == "--validate-arguments":
            validate_arguments()
        else:
            pass
    else:
        vc = LookupWatcher()
        vc.run_script()

    sys.exit(0)
