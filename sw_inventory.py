#!/usr/bin/python
#options can be found in ./opts.py

import xmlrpclib
import httplib
import datetime
import ConfigParser
import optparse
import sys
import os
import json

from opts import *
from subprocess import *
from optparse import OptionParser

#open session with spacewalk api
spacewalk = xmlrpclib.Server("http://%s/rpc/api" % spaceserver, verbose=0)
api_token = spacewalk.auth.login(spw_user, spw_pass)

parser = OptionParser(usage="%prog [options] --list | --host <hostname> | --profile <profile_name>")
parser.add_option('-o', '--oldlist', dest="oldlist",
                  default=False, action="store_true",
                  help="Old list output")

parser.add_option('-l', '--list', dest="groups",
                  default=False, action="store_true",
                  help="System groups")

parser.add_option('-s', '--host', dest="host",
                  default=False, action="store_true",
                  help="host vars")

(options, args) = parser.parse_args()

def mk_lst(sys_grp_details):
    svr_list = []
    for server in sys_grp_details:
        svr_list.append(server['name'])
    return svr_list

if options.host:
    details = spacewalk.system.getDetails(api_token, 1000010769)
    print details

if options.oldlist:
    #get the list of systems
    systems = spacewalk.system.listSystems(api_token)
    #iterate through system list and print name
    for system in systems:
        print system['name']

if options.groups:
    sys_dict = {}
    #find all system groups
    groups = spacewalk.systemgroup.listAllGroups(api_token)

    for group in groups:
        if group:
            sys_dict[group['name']] = set()
        sys_grp_details = spacewalk.systemgroup.listSystemsMinimal(api_token, group['name'])
        sys_dict[group['name']] = mk_lst(sys_grp_details)

    print json.dumps(sys_dict)

#logout of api
spacewalk.auth.logout(api_token)