#!/usr/bin/env python

from getJms import getJms
from fetchAppList import stripAll
import threading
apps = stripAll()

#apps = ['risktools', 'cinbox']

def jav():
    for app in apps:
        lista = []
        try:
            obj = getJms(app.replace('.yaml', ''), 'java')
            rest, uat, agt, prd, link = obj.getVer()
            for k,v in prd.iteritems():
                lista.append(k+' : '+v+'\n')
            for a,b in uat.iteritems():
                lista.append(a+' : '+b+'\n')
            for c,d in agt.iteritems():
                lista.append(c+' : '+d+'\n')
            for e,f in rest.iteritems():
                lista.append(e+' : '+f+'\n')

        except:
            pass
        f = open('javaVersionsFiles/'+app.replace('.yaml', ''), 'w')
        f.writelines(lista)
        f.close()

def tom():
    for app in apps:
        lista = []
        try:
            obj = getJms(app.replace('.yaml', ''), 'tomcat')
            rest, uat, agt, prd, link = obj.getVer()
            for k,v in prd.iteritems():
                lista.append(k+' : '+v+'\n')
            for a,b in uat.iteritems():
                lista.append(a+' : '+b+'\n')
            for c,d in agt.iteritems():
                lista.append(c+' : '+d+'\n')
            for e,f in rest.iteritems():
                lista.append(e+' : '+f+'\n')
	except:
            pass

        f = open('tomcatVersionsFiles/'+app.replace('.yaml', ''), 'w')
        f.writelines(lista)
        f.close()

t1 = threading.Thread(target=tom, args=())
t2 = threading.Thread(target=jav, args=())
t1.start()
t2.start()
