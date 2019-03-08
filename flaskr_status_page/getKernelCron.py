#!/usr/bin/python
import xmlrpclib
import sys

SAT_URL = "https://rhsatellite01all.vcint.com/rpc/api"
SAT_USER = "automation"
SAT_PASS = "unix@ops"

client = xmlrpclib.Server(SAT_URL, verbose=0)
key = client.auth.login(SAT_USER, SAT_PASS)
list = client.system.listUserSystems(key)
#client.auth.logout(key)
with open('kernelCronList', 'w') as f:
    for i in list:
	out = i.get('name')+'|'+client.system.getRunningKernel(key,i.get('id'))+'\n'
	f.write(out)
    f.close()    
