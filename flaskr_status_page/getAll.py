#!/usr/bin/python

from getHttp import getHttp
from getJms import getJms
from fetchAppList import stripAll

apps = stripAll()

def http():
    lista = []
    for app in apps:
        try:
            obj = getHttp(app.replace('.yaml', ''))
            rest, uat, agt, prd, link = obj.getAppVer()
            for k,v in prd.iteritems():
		lista.append(k+'|'+app.replace('.yaml', '')+'|'+v+'\n')
        except:
	    pass
    f = open('appVersions.txt', 'w')
    f.writelines(lista)
    f.close()

def jav():
    lista = []
    for app in apps:
        try:
            obj = getJms(app.replace('.yaml', ''), 'java')
            rest, uat, agt, prd, link = obj.getVer()
            for k,v in prd.iteritems():
		lista.append(k+'|'+app.replace('.yaml', '')+'|'+v+'\n')
        except:
	    pass

    f = open('javaVersions.txt', 'w')
    f.writelines(lista)
    f.close()

def tom():
    lista = []
    for app in apps:
        try:
            obj = getJms(app.replace('.yaml', ''), 'tomcat')
            rest, uat, agt, prd, link = obj.getVer()
            for k,v in prd.iteritems():
		lista.append(k+'|'+app.replace('.yaml', '')+'|'+v+'\n')
        except:
	    pass

    f = open('tomcatVersions.txt', 'w')
    f.writelines(lista)
    f.close()

http()
jav()
tom()
