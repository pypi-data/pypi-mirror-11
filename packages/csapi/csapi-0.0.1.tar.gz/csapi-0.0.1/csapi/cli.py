#!/usr/bin/env python

# Author: Will Stevens (CloudOps) - wstevens@cloudops.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Usage:
  cs_api.py [--json=<arg>] [--api_key=<arg> --secret_key=<arg>] [options]
  cs_api.py (-h | --help)

Options:
  -h --help                 Show this screen.
  --json=<arg>              Path to a JSON config file with the same names as the options (without the -- in front).
  --api_key=<arg>           CS Api Key.
  --secret_key=<arg>        CS Secret Key.
  --endpoint=<arg>          CS Endpoint [default: http://127.0.0.1:8080/client/api].
  --poll_interval=<arg>     Interval, in seconds, to check for a result on async jobs [default: 5].
  --logging=<arg>           Boolean to turn on or off logging [default: True].
  --log=<arg>               The log file to be used [default: logs/cs_api.log].
  --clear_log=<arg>         Removes the log each time the API object is created [default: True].
"""

import docopt
import sys
import os
from .csapi import CsApi

class CsApiCli(CsApi):
    def __init__(self, doc_str):

        args = self.load_config(doc_str)

        api_key = args['--api_key']
        secret_key = args['--secret_key']
        endpoint = args['--endpoint']
        poll_interval = float(args['--poll_interval'])
        logging = True if args['--logging'].lower() == 'true' else False
        log = args['--log']
        clear_log = True if args['--clear_log'].lower() == 'true' else False

        super(CsApiCli, self).__init__(
            api_key,
            secret_key,
            endpoint,
            poll_interval,
            logging,
            log,
            clear_log
        )


    def load_config(self, doc_str):
      args = docopt.docopt(doc_str)
   
      is_set = [
          x.split('=')[0] \
          for x in sys.argv[1:] \
          if len(x.split('=')) > 0 and x.split('=')[0].startswith('-')
      ] # set by cmd line
   
      config = None
      if '--json' in args and args['--json']:
          with open(args['--json']) as json_config:
              config = json.load(json_config)
   
      if config:
          for key, value in config.iteritems():
              if '--%s' % (key) not in is_set:
                  args['--%s' % (key)] = value
      return args
