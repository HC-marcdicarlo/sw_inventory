#!/usr/bin/python
#sync spacewalk repos and clean up old and orphaned packages
#repo names can be found in ./repos
#options can be found in ./options.py

import xmlrpclib
import httplib
import datetime
import ConfigParser
import optparse
import sys
import os

from options import *
from subprocess import *
from optparse import OptionParser

#open session with spacewalk api
spacewalk = xmlrpclib.Server("https://%s/rpc/api" % spaceserver, verbose=0)
api_token = spacewalk.auth.login(spw_user, spw_pass)

#get the list of systems
systems = spacewalk.system.listSystems(api_token)

#iterate through system list and print name
for system in systems:
    print system['name']

#logout of api
spacewalk.auth.logout(api_token)

