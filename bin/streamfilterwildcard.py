#!/usr/bin/env python
# coding=utf-8
#
# Copyright © 2011-2015 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators
from splunklib import six
import types
import re

#Based on the Splunk SDK for python example http://dev.splunk.com/view/python-sdk/SP-CAAAEU2 countmatches.py, searchcommands_app
#with modifications
@Configuration()
class StreamFilterWildcardCommand(StreamingCommand):
    """ Returns a field with a list of non-overlapping matches to a wildcard pattern in a set of fields.

    ##Syntax

    .. code-block::
        StreamFilterWildcardCommand fieldname=<field> pattern=<field containing wildcard pattern> <field-list>

    ##Description

    Returns the non-overlapping matches to the wildcard pattern contained in the field specified by `pattern`
    The result is stored in the field specified by `fieldname`. If `fieldname` exists, its value
    is replaced. If `fieldname` does not exist, it is created. Event records are otherwise passed through to the next
    pipeline processor unmodified.

    ##Example

    Return the wildcard pattern matches in the `text` field (field named text) of each tweet in tweets.csv and store the result in `word_count`.

    .. code-block::
        | inputlookup tweets | eval pattern="\\w+" | streamfilter fieldname=word_count pattern=pattern text

    """
    fieldname = Option(
        doc='''
        **Syntax:** **fieldname=***<fieldname>*
        **Description:** Name of the field that will hold the match count''',
        require=True, validate=validators.Fieldname())

    pattern = Option(
        doc='''
        **Syntax:** **pattern=***<fieldname>* 
        **Description:** Field name containing the wildcard pattern pattern to match''',
        require=True, validate=validators.Fieldname())

    #Filter the data based on the passed in Wildcard pattern, this function exists so we can handle mutli-value pattern fields
    def thefilter(self, record, pattern):
        values = ""
        for fieldname in self.fieldnames:
            #multivalue fields come through as a list, iterate through the list and run the Wildcard against each entry
            #in the multivalued field
            if not fieldname in record:
                continue            
            if isinstance(record[fieldname], list):
                for aRecord in record[fieldname]:
                    matches = pattern.findall(six.ensure_str(aRecord))
                    for match in matches:
                        values = values + " " + match
            else:
                matches = pattern.findall(six.ensure_str(record[fieldname]))
                for match in matches:
                    values = values + " " + match
        return values

    #Change a wildcard pattern to a Wildcard pattern
    def changeToWildcard(self, pattern):
        pattern = pattern.replace("\"", "")
        pattern = pattern.replace("'", "")
        pattern = pattern.replace("*", ".*")
        if pattern.find(".*") == 0:
            pattern = "[^_].*" + pattern[2:]
        pattern = "(?i)^" + pattern + "$"
        return pattern

    #Streaming command to work with each record
    def stream(self, records):
        self.logger.debug('StreamFilterWildcardCommand: %s', self)  # logs command line
        for record in records:
            values = ""
            pattern = self.pattern
            if pattern not in record:
               self.logger.warn("StreamFilterWildcardCommand: pattern field is %s but cannot find this field" % (pattern), self)
               sys.exit(-1)
            if isinstance(record[pattern], list):
                for aPattern in record[pattern]:
                    pattern = re.compile(self.changeToWildcard(aPattern))
                    values = values + self.thefilter(record, pattern)
            else:
                pattern = re.compile(self.changeToWildcard(record[pattern]))
                values = values + self.thefilter(record, pattern)

            record[self.fieldname] = values
            yield record

dispatch(StreamFilterWildcardCommand, sys.argv, sys.stdin, sys.stdout, __name__)
