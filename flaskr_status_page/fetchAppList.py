#!/usr/bin/python

import urllib2
import yaml
import requests
import re
from BeautifulSoup import BeautifulSoup


YAMLS = 'https://subversion01all.vcint.com/scm/trunk/deployments/'
USER = 'scm'
PASS = 'scmISC00l'

def getAppVer(app):
    res = requests.get(YAMLS+app, auth = (USER, PASS), verify=False)
    y = yaml.load(res.text)
    try:
        link = y['versions']['application']['urls'][0]
    except:
        link = "Link not found in yaml file"
    _prd, _agt, _uat, _rest = {}, {}, {}, {}
    for i in y['environments']:
        for j in y['environments'][i]['servers']:
            try:
                version = urllib2.urlopen(link.replace('$server', j), timeout=1).read()
            except:
                version = "NOVERSION"
            if j:
                if 'prd' in j:
                    _prd[j] = version.rstrip()
    return _prd

def stripAll():
    content = requests.get(YAMLS, auth = (USER, PASS), verify=False)
    soup = BeautifulSoup(content.text)
    appList = []
    for i in soup.findAll('li'):
        i = re.sub('<.*?>', '', str(i))
        if i.endswith('yaml'):
            appList.append(i)

    return appList
