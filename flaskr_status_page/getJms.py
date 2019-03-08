#!/usr/bin/env python

import yaml
import urllib2
import os
import requests
import re
import subprocess
import socket
import json

YAMLS = 'https://subversion01all.vcint.com/scm/trunk/deployments/'
REPO = 'https://subversion01all.vcint.com/scm/trunk/deployments/'
USER = 'scm'
PASS = 'scmISC00l'
JAR = 'java -jar cmdline-jmxclient-0.10.3.jar'

#if 'scm02all' in socket.gethostname():
ENVI = 'prd tst agt'
#elif 'scm01all' in socket.gethostname():

class getJms():
    def __init__(self, app, typ):
        self.app = app
        self.typ = typ

    def getVer(self):
        res = requests.get(YAMLS+self.app+'.yaml', auth = (USER, PASS), verify=False)
        y = yaml.load(res.text)
        link = "Link not found in yaml file"
        try:
            if self.typ == 'tomcat':
                link = y['versions'][self.typ]['jmx'][0]
            elif self.typ == 'java':
                link = y['versions'][self.typ]['jav'][0]

            _prd, _agt, _uat, _rest = {}, {}, {}, {}
            for i in y['environments']:
                for j in y['environments'][i]['servers']:
		    if ('prd' in j) or ('tst' in j) or ('agt' in j):
                        version = subprocess.Popen(JAR+' '+link.replace('$server', j), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        out,err = version.communicate()
                    if 'Exception' in out:
                        out = 'n/a'
                    if j:
                            if 'prd' in j:
                                _prd[j] = out.split()[-1]
                            elif 'agt' in j:
                                _agt[j] = out.split()[-1]
                            elif 'tst' in j:
                                _uat[j] = out.split()[-1]
                            else:
                                _rest[j] = out.split()[-1]

            return _rest, _uat, _agt, _prd, link
        except:
            return '', '', '', '', link

