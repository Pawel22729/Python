#!/usr/bin/env python

from flask import Flask, render_template, url_for, request
app = Flask(__name__)
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
ENVI = 'tst agt int dev trd'
#elif 'scm01all' in socket.gethostname():


class getHttp():
    def __init__(self, app):
        self.app = app

    def getAppVer(self):
        res = requests.get(YAMLS+self.app+'.yaml', auth = (USER, PASS), verify=False)
        y = yaml.load(res.text)
        try:
            link = y['versions']['application']['urls'][0]
        except:
            link = "Link not found in yaml file"
        _prd, _agt, _uat, _rest = {}, {}, {}, {}
        for i in y['environments']:
            for j in y['environments'][i]['servers']:
                try:
                    version = urllib2.urlopen(link.replace('$server', j), timeout=0.3).read()
                except:
                    version = "Can't find application version"
                if j:
                        if 'prd' in j:
                            _prd[j] = version
                        elif 'agt' in j:
                            _agt[j] = version
                        elif 'tst' in j:
                            _uat[j] = version
                        else:
                            _rest[j] = version
        return _rest, _uat, _agt, _prd, link
