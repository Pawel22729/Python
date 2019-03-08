#!/usr/bin/env python

from flask import Flask, render_template, url_for, request
app = Flask(__name__)
from getHttp import getHttp
from getJms import getJms
from allInfo import make
from getJmsStatic import getJmsStatic
import requests, re

REPO = 'https://subversion01all.vcint.com/scm/trunk/deployments/'
USER = 'scm'
PASS = 'scmISC00l'

@app.route('/tomcats')
def get_tomcats():
    res = requests.get(REPO, auth=(USER, PASS), verify=False)
    reg = re.findall('[0-9a-zA-Z-]*.yaml', res.text)
    reg = set(reg)
    list = []
    for i in reg:
        list.append(i.replace('.yaml', ''))
    return render_template('appList.html', App_list=list, check='tomcatCheck')


@app.route('/versions')
def get_apps():
    res = requests.get(REPO, auth=(USER, PASS), verify=False)
    reg = re.findall('[0-9a-zA-Z-]*.yaml', res.text)
    reg = set(reg)
    list = []
    for i in reg:
	list.append(i.replace('.yaml', ''))
    return render_template('appList.html', App_list=list, check='versionCheck')

@app.route('/java')
def get_java():
    res = requests.get(REPO, auth=(USER, PASS), verify=False)
    reg = re.findall('[0-9a-zA-Z-]*.yaml', res.text)
    reg = set(reg)
    list = []
    for i in reg:
        list.append(i.replace('.yaml', ''))
    return render_template('appList.html', App_list=list, check='javaCheck')

@app.route('/tomcatCheck')
def tomcat_status():
    if request.args.get('application'):
	app = request.args.get('application')
	# getJms fetch instant, getJmsStatic fetch from cache file
        obj = getJms(app, 'tomcat')
        #obj = getJmsStatic(app, 'tomcat')
        rest, uat, agt, prd, link = obj.getVer()
    else:
        app = ""
    return render_template('show.html', PRD=prd, UAT=uat, AGT=agt, REST=rest, Link=link, App=app)	

@app.route('/javaCheck')
def java_status():
    if request.args.get('application'):
        app = request.args.get('application')
	# getJms fetch instant, getJmsStatic fetch from cache file
	obj = getJms(app, 'java')
        #obj = getJmsStatic(app, 'java')
	rest, uat, agt, prd, link = obj.getVer()
    else:
        app = ""
    return render_template('show.html', PRD=prd, UAT=uat, AGT=agt, REST=rest, Link=link, App=app)

@app.route('/versionCheck')
def status_page():
    if request.args.get('application'):
	app = request.args.get('application')
	obj = getHttp(app)
	rest, uat, agt, prd, link = obj.getAppVer()
    else:
	app = ""
	data = ""
    return render_template('show.html', PRD=prd, UAT=uat, AGT=agt, REST=rest, Link=link, App=app)

@app.route('/json')
def jsonApi():
    data = open('jsonVersion.json').read()
    return render_template('json.html', Data=data)

@app.route('/all')
def all():
    data = make()
    return render_template('all.html', Data=data)

@app.route('/')
def main():
    return render_template('menu.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)

