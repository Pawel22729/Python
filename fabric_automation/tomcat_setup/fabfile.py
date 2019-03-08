from fabric.api import *
from fabric.contrib.files import exists
import os

def test(app_user):
	sudo('whoami', user=app_user)

def upload_tomcat(package,app_user):
	print 'Checking if file exists on the server...'
	if not exists('/export/local/tomcat-versions/'+package):
	    print 'Uploading...'
            put('/export/home/scm/fabric_conf/tomcat_setup/files/'+package, '/export/home/scm/'+package)
	    sudo('cp /export/home/scm/'+package+' /export/local/tomcat-versions/'+package, user=app_user)
	    run('rm -rf /export/home/scm/'+package)
	else:
	    print 'File is already on the server'

def unpack(package,app_user):
	print 'Unpacking...'
	if exists('/export/local/tomcat-versions/'+package):
	    absPath = tomcatNoExtension = os.path.splitext('/export/local/tomcat-versions/'+package)[0]
	    print absPath
	    if exists(absPath):
	        sudo('rm -rf '+absPath, user=app_user)

	    with cd('/export/local/tomcat-versions/'):
	       sudo('unzip -q '+package, user=app_user)
	       sudo('rm -rf '+package, user=app_user)
	    

def create_link(package,app_user):
	print 'Creating link to uploaded tomcat...'
        tomcatNoExtension = os.path.splitext('/export/local/tomcat-versions/'+package)[0]
	if exists('/export/local/tomcat'):
	    print 'Link exists - recreating...'
	    run('sudo rm -rf /export/local/tomcat')
	with cd('/export/local/'):
	    run('sudo ln -s '+tomcatNoExtension+' /export/local/tomcat')
	    sudo('chmod +x /export/local/tomcat/bin/*.sh',user=app_user)


def deploy(package, app_user):
	upload_tomcat(package,app_user)
	unpack(package,app_user)
	create_link(package,app_user)
