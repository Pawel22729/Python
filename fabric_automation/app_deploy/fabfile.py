from fabric.api import *
from fabric.contrib.files import exists
import os
import yaml
import subprocess
import time

from yamlLoad import parseYaml
import prepareConf

def setupChown(app,env):
    yamlContent = parseYaml(app)
    deploy = yamlContent['environments'][env]['deployment']
    app_user = yamlContent['deployments'][deploy]['user']
    appDir = app_user
    sudo('chmod +x /export/apps/vc/'+appDir+'/bin/*.sh',user=app_user)

def stopApp(app,env):
#       Variables required by this fabric step
    yamlContent = parseYaml(app)
    deploy = yamlContent['environments'][env]['deployment']
    scripts_path = yamlContent['deployments'][deploy]['scripts_location']
    app_user = yamlContent['deployments'][deploy]['user']
    stop_cmd = yamlContent['deployments'][deploy]['stop_commands'][0]
    process = yamlContent['deployments'][deploy]['processes'][0]
    tries = 5
#       Proper function
    with cd(scripts_path):
	with settings(warn_only=True):
	    with hide('stdout'):
		    check = 'ps -ef | grep "{0}" | grep -v grep'.format(process)
		    if run(check).return_code != 0:
			print 'Application not running...'
		    else:
			sudo(stop_cmd, user=app_user)
			for i in range(tries):
			    run(check)
			    time.sleep(5)
			    if run(check).return_code != 0:
				print 'Application stopped gracefully...'
			        break
			if run(check).return_code == 0:
			    print 'Cant stop application - killing Bitch'
			    sudo('pgrep -f '+process+' | xargs kill -9',user=app_user)

def test():
	with cd('/export/apps/vc/octo/bin'):
	    run('sudo -u octo nohup ./startup.sh')

def startApp(app,env):
#       Variables required by this fabric step
    yamlContent = parseYaml(app)
    deploy = yamlContent['environments'][env]['deployment']
    scripts_path = yamlContent['deployments'][deploy]['scripts_location']
    app_user = yamlContent['deployments'][deploy]['user']
    start_cmd = 'nohup '+yamlContent['deployments'][deploy]['start_commands'][0]
    process = yamlContent['deployments'][deploy]['processes'][0]
    tries = 5
    print start_cmd
#	Proper function
    with cd(scripts_path):
	with settings(warn_only=True):
		with hide('stdout'):
			check = 'ps -ef | grep "{0}" | grep -v grep'.format(process)
			if run(check).return_code == 0:
			    print 'Application already running...'
			else:
			    sudo(start_cmd, user=app_user)
			    for i in range(tries):
				    run(check)
				    time.sleep(5)
				    if run(check).return_code == 0:
					print 'Application started...'
					break
			    if run(check).return_code != 0:
				print 'Application failed to start..'
		

def prepareStruct(app,env):
#       Variables required by this fabric step
    yamlContent = parseYaml(app)
    deploy = yamlContent['environments'][env]['deployment']
    configLocation = yamlContent['deployments'][deploy]['configs_location']
    releaseLocation = yamlContent['deployments'][deploy]['releases_location']
    appDir = app
    app_user = yamlContent['deployments'][deploy]['user']
    appConfDir = yamlContent['deployments'][deploy]['configs_svn_destination']
    absDir = '/export/apps/vc/'
    rootDir = absDir+app 
    tomcatDir = '/export/local/tomcat'
#	Proper function
    if not exists(absDir+app):
	sudo('mkdir -p '+absDir+appDir, user=app_user)
    if not exists(configLocation):
        run('sudo mkdir -p '+configLocation)
    if not exists(releaseLocation):
        run('sudo mkdir -p '+releaseLocation)
    if not exists(rootDir+'/webapps'):
	run('sudo mkdir -p '+rootDir+'/webapps')
    if not exists(rootDir+'/configs'):
	run('sudo mkdir -p '+rootDir+'/configs')
    if not exists(rootDir+'/configs/previous'):
        run('sudo mkdir -p '+rootDir+'/configs/previous')
    if not exists(rootDir+'/configs/working/bin'):
	run('sudo mkdir -p '+rootDir+'/configs/working/bin')
    if not exists(rootDir+'/configs/working/lib'):
        run('sudo mkdir -p '+rootDir+'/configs/working/lib')
    if not exists(rootDir+'/configs/working/conf'):
        run('sudo mkdir -p '+rootDir+'/configs/working/conf')
    if not exists(rootDir+'/configs/working/app-conf'):
        run('sudo mkdir -p '+rootDir+'/configs/working/app-conf')
    if not exists(rootDir+'/releases/working/'):
        run('sudo mkdir -p '+rootDir+'/releases/working/')
    if not exists(rootDir+'/releases/previous/'):
        run('sudo mkdir -p '+rootDir+'/releases/previous/')
    if not exists(rootDir+'/work'):
        run('sudo mkdir -p '+rootDir+'/work')
    if not exists(rootDir+'/temp'):
        run('sudo mkdir -p '+rootDir+'/temp')
    run('sudo chown -R '+app_user+'.'+app_user+' '+rootDir+'/')
    
def resolveUrl(url):
    url_effective = '%{url_effective}'
    url = subprocess.Popen('curl -sL -w "{0}" "{1}" -o /dev/null'.format(url_effective, url),stdout=subprocess.PIPE,shell=True)
    (out,err) = url.communicate()
    return out

def getPackageFromUrl(url):
    url = resolveUrl(url)
    filename = url.split('/')[-1]
    print('Downloading {0}'.format(filename))
    with lcd('/tmp/'):
        local('curl -o {0} {1}'.format(filename, url))
    if exists('/tmp/'+filename):
	print 'File has been downloaded...'

def uploadApp(url,app,env):
#	Variables required by this fabric step
    yamlContent = parseYaml(app)
    deploy = yamlContent['environments'][env]['deployment']
    warName = yamlContent['deployments'][deploy]['releases_links']['warfile']
    filename = url.split('/')[-1]
    if not (filename.endswith('war') or filename.endswith('jar')):
	print 'Wrong war file link !!!'
    else:
	app_user = yamlContent['deployments'][deploy]['user']
        appDir = app
        localFile = '/tmp/'+filename
        scmHome = '/export/home/scm/'
        url = resolveUrl(url)
        getPackageFromUrl(url)
    with settings(warn_only=True):
	    sudo('/bin/rm -rf /export/apps/vc/'+appDir+'/releases/previous/*',user=app_user)
	    sudo('/bin/cp -r /export/apps/vc/'+appDir+'/releases/working/* /export/apps/vc/'+appDir+'/releases/previous/', user=app_user)
	    sudo('/bin/rm -rf /export/apps/vc/'+appDir+'/releases/working/*',user=app_user)
	    sudo('/bin/rm -rf /export/apps/vc/'+appDir+'/webapps/*',user=app_user)

    print 'Uploading...'
    if os.path.exists(localFile):
        put(localFile, '/tmp/')
	sudo('cp /tmp/'+filename+' /export/apps/vc/'+appDir+'/releases/working/',user=app_user)
	if filename.endswith('war'):
	    with cd('/export/apps/vc/'+appDir+'/webapps/'):
                sudo('ln -s /export/apps/vc/'+appDir+'/releases/working/'+filename+' '+warName.split('/')[-1],user=app_user)
	else:
	    with cd('/export/apps/vc/'+appDir+'/lib/'):
                sudo('ln -s /export/apps/vc/'+appDir+'/releases/working/'+filename+' '+warName.split('/')[-1],user=app_user)
	run('rm -rf /tmp/'+filename)
    else:
	print localFile+" doesn't exists"

def cleanAndBack(app,env):
    yamlContent = parseYaml(app)
    deploy = yamlContent['environments'][env]['deployment']
    app_user = yamlContent['deployments'][deploy]['user']
    appDir = yamlContent['deployments'][deploy]['user']
    sudo('/bin/rm -rf /export/apps/vc/'+appDir+'/configs/previous/*',user=app_user)
    sudo('/bin/cp -r /export/apps/vc/'+appDir+'/configs/working/* /export/apps/vc/'+appDir+'/configs/previous/', user=app_user)
    sudo('/bin/rm -rf /export/apps/vc/'+appDir+'/work/*',user=app_user)
    sudo('/bin/rm -rf /export/apps/vc/'+appDir+'/temp/*',user=app_user)
    

def configUpdate(app,env,zip):
    yamlContent = parseYaml(app)
    deploy = yamlContent['environments'][env]['deployment']
    app_user = yamlContent['deployments'][deploy]['user']
    appDir = app
    if zip != 'None':
# If config link - commit first
	getPackageFromUrl(zip)
	filename = '/tmp/'+zip.split('/')[-1]
	if not filename.endswith('zip'):
	    print 'Not a zip file !!!'
	else:
	    local('mv '+filename+' /export/home/scm/tmp/'+appDir+'/'+env+'/app-conf/')
    	    with lcd('/export/home/scm/tmp/'+appDir+'/'+env+'/app-conf/'):
	        local('svn up')
	        local('unzip -q -j -o '+zip.split('/')[-1])
		local('rm -rf *.zip')
	    with lcd('/export/home/scm/tmp/'+appDir+'/'+env):
	            local('svn add --force *')
	            local('svn ci -m "DEPLOYMENT COMMIT FROM CONFIG FILE: '+zip.split('/')[-1]+'"')
		
    path = prepareConf.main(app,env)
    appDir = app

    if os.path.exists(path):
	put(path, '/tmp/')
	sudo('/bin/rm -rf /export/apps/vc/'+appDir+'/configs/working/*',user=app_user)
        sudo('cp /tmp/'+path.split('/')[-1]+' /export/apps/vc/'+appDir+'/configs/working/',user=app_user)
	with cd('/export/apps/vc/'+appDir+'/configs/working/'):
	    sudo('/usr/bin/unzip -q /export/apps/vc/'+appDir+'/configs/working/'+path.split('/')[-1],user=app_user)
	setupChown(app,env)
	run('rm -rf /tmp/tmp*')
	local('sudo rm -rf /tmp/tmp*')

def createLinks(app,env):
    yamlContent = parseYaml(app)
    deploy = yamlContent['environments'][env]['deployment']
    app_user = yamlContent['deployments'][deploy]['user']
    Links = yamlContent['deployments'][deploy]['configs_links']
    appDir = '/export/apps/vc/'+app+'/' 
    with cd(appDir):
	for link in Links:
            sudo('rm -rf '+Links[link],user=app_user)
	    sudo('ln -s '+appDir+'configs/working/'+link+' '+link,user=app_user)
	if not exists('/export/apps/vc/'+app+'/logs'):
	    sudo('ln -s /export/logs/'+app+' logs',user=app_user)


def deployConf(app,env,war,zip):
    print 'STOPPING APP...'
    stopApp(app,env)
    print 'MOVEING OLD CNFIGS...'
    cleanAndBack(app,env)
    print 'UPLOADING APP...'
    uploadApp(war,app,env)
    print 'PREPAREING AND UPLOADING CONFIGS...'
    configUpdate(app,env,zip)
    print 'PREPAREING LINKS...'
    createLinks(app,env)    
    print 'CHOWNIG...'
    setupChown(app,env)
    print 'STARTING APP...'
    startApp(app,env)

def deploy(app,env,war):
    print 'STOPPING APP...'
    stopApp(app,env)
    print 'MOVEING OLD CNFIGS...'
    cleanAndBack(app,env)
    print 'UPLOADING APP...'
    uploadApp(war,app,env)
    print 'CHOWNIG...'
    setupChown(app,env)
    print 'STARTING APP...'
    startApp(app,env)

def confUp(app,env,zip):
    print 'STOPPING APP...'
    stopApp(app,env)
    print 'MOVEING OLD CNFIGS...'
    cleanAndBack(app,env)
    print 'PREPAREING AND UPLOADING CONFIGS...'
    configUpdate(app,env,zip)
    print 'PREPAREING LINKS...'
    createLinks(app,env)
    print 'CHOWNIG...'
    setupChown(app,env)
    print 'STARTING APP...'
    startApp(app,env)

def newServer(app,env,war,zip):
    print 'PREPAREING CATALOG STRUCTURE...'
    prepareStruct(app,env)
    print 'UPLOADING APP...'
    uploadApp(war,app,env)
    print 'PREPAREING LINKS...'
    createLinks(app,env)
    print 'PREPAREING AND UPLOADING CONFIGS...'
    configUpdate(app,env,zip)
    print 'STARTING APP...'
    startApp(app,env)



















