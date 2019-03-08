#!/usr/bin/python

from fetchAppList import stripAll
import requests, yaml

YAMLS = 'https://subversion01all.vcint.com/scm/trunk/deployments/'
USER = 'scm'
PASS = 'scmISC00l'

apps = stripAll()

def getServers():
    servers = []
    for app in apps:
        res = requests.get(YAMLS+app, auth = (USER, PASS), verify=False)
	print str(res)
        #try:
        #    y = yaml.load(res.text)
        #except:
        #    pass
        #for env in y['environments']:
        #    print env

getServers()
