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
JAR = 'java -jar /export/home/lasakp/flaskr/cmdline-jmxclient-0.10.3.jar'

#if 'scm02all' in socket.gethostname():
ENVI = 'tst agt int dev trd'    
#elif 'scm01all' in socket.gethostname():
#    ENVI = 'prd'

def getVer(app, type):
    res = requests.get(YAMLS+app+'.yaml', auth = (USER, PASS), verify=False)
    if res.status_code == 200:
	    yam = yaml.load(res.text)
	    data = {}
	    try:
		link = 'Link has not been found in yaml'
		if type == 'urls':
			link = yam['versions']['application']['urls'][0]
		elif type == 'jmx':
			link = yam['versions']['tomcat']['jmx'][0]
		elif type == 'jav':
			link = yam['versions']['java']['jav'][0]
		for i in yam['environments']:
		    for j in yam['environments'][i]['servers']:
			if j[-3:] in ENVI:
			    if type == 'urls':
				try:
			            version = urllib2.urlopen(link.replace('$server', j), timeout=1).read()
			            data[j] = version
				except:
				    data[j] = "Cant find application version"
			    elif type == 'jmx':
				version = subprocess.Popen(JAR+' '+link.replace('$server', j), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                                out,err = version.communicate()
				if not 'Exception' in out:
                                    data[j] = out.split()[-1]
				else:
				    data[j] = "Timeout - Cant connect to JMX port"
			    elif type == 'jav':
				version = subprocess.Popen(JAR+' '+link.replace('$server', j), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                                out,err = version.communicate()
				if not 'Exception' in out:  
                                    data[j] = out.split()[-1]
				else:
				    data[j] = "Timeout - Cant connect to JMX port"
		
	    except:
		print 'Cant find version url in yaml file';
    else:
	data = ""
    return data, link

@app.route('/tomcats')
def get_tomcats():
    res = requests.get(REPO, auth=(USER, PASS), verify=False)
    reg = re.findall('[0-9a-zA-Z-]*.yaml', res.text)
    reg = set(reg)
    list = []
    for i in reg:
        list.append(i.replace('.yaml', ''))
    return render_template('tomcatCheck.html', App_list=list)


@app.route('/versions')
def get_apps():
    res = requests.get(REPO, auth=(USER, PASS), verify=False)
    reg = re.findall('[0-9a-zA-Z-]*.yaml', res.text)
    reg = set(reg)
    list = []
    for i in reg:
	list.append(i.replace('.yaml', ''))
    return render_template('versionCheck.html', App_list=list)

@app.route('/java')
def get_java():
    res = requests.get(REPO, auth=(USER, PASS), verify=False)
    reg = re.findall('[0-9a-zA-Z-]*.yaml', res.text)
    reg = set(reg)
    list = []
    for i in reg:
        list.append(i.replace('.yaml', ''))
    return render_template('javaCheck.html', App_list=list)

@app.route('/tomcatCheck')
def tomcat_status():
    if request.args.get('application'):
	app = request.args.get('application')
	ver, link = getVer(app, 'jmx')
    else:
        ver = ""
        app = ""
    return render_template('showTomcat.html', Versions=ver, Link=link, App=app)	

@app.route('/javaCheck')
def java_status():
    if request.args.get('application'):
        app = request.args.get('application')
        ver, link = getVer(app, 'jav')
    else:
        ver = ""
        app = ""
    return render_template('showJava.html', Versions=ver, Link=link, App=app)

@app.route('/versionCheck')
def status_page():
    if request.args.get('application'):
	app = request.args.get('application')
	ver, link = getVer(app, 'urls')
    else:
	ver = ""
	app = ""
    return render_template('showVersion.html', Versions=json.dumps(ver), Link=link, App=app)

@app.route('/')
def main():
    return render_template('menu.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)

