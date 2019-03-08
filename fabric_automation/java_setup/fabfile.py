from fabric.api import *
from fabric.contrib.files import exists
import os

def test(app_user):
	sudo('whoami', user=app_user)

def upload_java(package,app_user):
	print 'Checking if file exists on the server...'
	if not exists('/export/local/java-versions/'+package):
	    print 'Uploading...'
            put('/export/home/scm/fabric_conf/java_setup/files/'+package, '/export/home/scm/'+package)
	    run('cp /export/home/scm/'+package+' /export/local/java-versions/'+package)
	    run('rm -rf /export/home/scm/'+package)
	else:
	    print 'File is already on the server'

def unpack(package,app_user):
	print 'Unpacking...'
	if exists('/export/local/java-versions/'+package):
	    absPath = javaNoExtension = os.path.splitext('/export/local/java-versions/'+package)[0]
	    print absPath
	    if exists(absPath):
	        sudo('rm -rf '+absPath, user=app_user)

	    with cd('/export/local/java-versions/'):
	       sudo('unzip -q '+package, user=app_user)
	       sudo ('rm -rf '+package, user=app_user)
	    

def create_link(package,app_user):
	print 'Creating link to uploaded java...'
        javaNoExtension = os.path.splitext('/export/local/java-versions/'+package)[0]
	if exists('/export/local/java'):
	    print 'Link exists - recreating...'
	    run('sudo rm -rf /export/local/java')
	with cd('/export/local/'):
	    run('sudo ln -s '+javaNoExtension+' /export/local/java')
	    sudo('chmod +x /export/local/java/bin/*',user=app_user)


def deploy(package,app_user):
	upload_java(package,app_user)
	unpack(package,app_user)
	create_link(package,app_user)
