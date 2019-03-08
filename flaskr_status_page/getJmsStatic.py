#!/usr/bin/env python

import yaml
import urllib2
import os
import requests
import re
import subprocess
import socket
import json

class getJmsStatic():
    def __init__(self, app, typ):
        self.app = app
        self.typ = typ

    def getVer(self):
        _prd, _agt, _uat, _rest = {}, {}, {}, {}
	if self.typ == 'java':
	    appFile = open('javaVersionsFiles/'+self.app)
	else:
            appFile = open('tomcatVersionsFiles/'+self.app)

        for line in appFile:
	    if 'prd' in line:
                _prd[line.split(':')[0]] = line.split()[-1]
            elif 'agt' in line:
                _agt[line.split(':')[0]] = line.split()[-1]
            elif 'tst' in line:
                _uat[line.split(':')[0]] = line.split()[-1]
            else:
                _rest[line.split(':')[0]] = line.split()[-1]
	appFile.close()
	link = 'Test'
        return _rest, _uat, _agt, _prd, link
