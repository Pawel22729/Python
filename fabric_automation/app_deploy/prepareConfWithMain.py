#!/usr/bin/python -u

import re
import os
import tempfile
import subprocess
import zipfile
import shutil
import argparse

def tmpConfigs(app,envi):
    confDir = '/export/home/scm/tmp/'+app+'/'+envi+''
    tmp = tempfile.mkdtemp()
    subprocess.call('cp -r '+confDir+'/* '+tmp, shell=True)
    return tmp

def listConfigs(tmp):
    configs = []
    for dirpath, dirnames, filenames in os.walk(tmp):
        for f in filenames:
            if '.svn' not in f and '.svn' not in dirpath:
                configs.append(os.path.join(dirpath, f))
    return configs
   

def masterConfigs(app):
    masterFilesDirList = []
    masterRootDir = '/export/home/scm/tmp/masterfiles/'
    for dirpath, dirnames, filenames in os.walk(masterRootDir+app):
	for name in filenames:
	    if '.svn' not in name and '.svn' not in dirpath:
	        masterFilesDirList.append(os.path.join(dirpath,name))
    master = []
    for i in masterFilesDirList:
        f = open(i, 'r')
	for j in f:
	    master.append(j)
    return master

def replacePlaceholder(master, configs):
    replace_regex = re.compile(r'(\$\{\{)(.+?)(\}\})')
    values = {}
    for masterLine in master:
	(k, v) = masterLine.split(':', 1)
	values[k] = v.strip()
    newLines = []
    for configFile in configs:
	f = open(configFile,'r')
	for line in f:
	    for match in replace_regex.finditer(line):
	        try:
		    if match.group(2) in values:
		        line = line.replace(match.group(0), str(values[match.group(2)]))
		except KeyError:
		    raise ConfigsError('ERROR: Missing master value {0}'.format(match.group(2)))
	    newLines.append(line)
	    

        with open(configFile, 'w+') as e:
	    e.writelines(newLines)
    print 'CONGIG PREPARED'
					
def preparePackage(tmpDir):
    os.chdir(tmpDir)
    subprocess.call('pwd', shell=True)
    subprocess.call('zip -r /tmp/'+tmpDir.split('/')[-1]+'.zip ./*', shell=True)
    print 'Zipfile prepared: {0}.zip'.format(tmpDir)
    return tmpDir+'.zip'
    shutil.rmtree(tmpDir)


if __name__ == '__main__':
    try:
	parser = argparse.ArgumentParser(description='Prepare configuration base on placeholders.')
	parser.add_argument('-app', '--application', required=True, help='Application name based on application configuration folder name: http://scm04all/svn/repo/<app>')
	parser.add_argument('-env', '--environment', required=True, help='Environment name: live, test - based on folder name under <app> folder: http://scm04all/svn/repo/<app>/<env> ')
	args = parser.parse_args()

	if args.application and args.environment:
	    config = tmpConfigs(args.application,args.environment)
	    list = listConfigs(config)
	    master = masterConfigs(args.application)
	    replace = replacePlaceholder(master,list)
	    preparePackage(config)
    except KeyboardInterrupt:
	print 'Process interrupted...'
