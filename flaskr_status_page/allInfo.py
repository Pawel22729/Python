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
	try:
	    res = requests.get(YAMLS+app, auth = (USER, PASS), verify=False)
	    print res
            y = yaml.load(res.text)
	except:
	    pass
	for env in y['environments']:
	    for server in y['environments'][env]['servers']:
		if server and 'prd' in server:
		    servers.append(server)
    return set(servers)

def combineData(serv):   
    version = open('appVersions.txt').readlines()
    java = open('javaVersions.txt').readlines()
    tomcat = open('tomcatVersions.txt').readlines()
    kernel = open('kernelCronList').readlines()
    
    serverInfo = {}
    out = []
    results = []
    for v in version:
	split = v.split('|')
	if serv in v:
	    out.append(split[1]+' '+split[2])
	    for j in java:
		if split[0]+'|'+split[1] in j:
		    out.append('Java '+j.split('|')[-1])
	    for t in tomcat:
		if split[0]+'|'+split[1] in t:
		    out.append('Tomcat '+t.split('|')[-1])
	    for k in kernel:
		if split[0] in k:
		    out.append('Kernel '+k.split('|')[-1])
    results.append(out)
    serverInfo[serv] = results

    return serverInfo

def make():
    data = []
    for server in getServers():
        result = combineData(server)
	data.append(result)       
    return data

