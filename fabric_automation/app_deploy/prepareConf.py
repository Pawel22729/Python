#!/usr/bin/python -u

import re
import os
import tempfile
import subprocess
import zipfile
import shutil
import argparse
import yaml

def configUpdate(app,envi):
    deployments = '/export/home/scm/tmp/deployments/'
    f = open(deployments+app+'.yaml')
    yam = yaml.load(f)
    f.close()
    confDir = '/export/home/scm/'+yam['environments'][envi]['configs_templates']
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
   

def masterConfigs(app,env):
    deployments = '/export/home/scm/tmp/deployments/'
    f = open(deployments+app+'.yaml')
    yam = yaml.load(f)
    f.close()
    masterFiles = yam['environments'][env]['masterfiles']
    masterFilesDirList = []
    masterRootDir = '/export/home/scm/tmp/masterfiles/'
    for name in masterFiles:
	if '.svn' not in name:
	    masterFilesDirList.append(os.path.join(masterRootDir,name))
    master = []
    for i in masterFilesDirList:
        f = open(i, 'r')
	for j in f:
	    if j.rstrip():
	        master.append(j)
    f.close()
    return master

def replacePlaceholder(master, configs):
    replace_regex = re.compile(r'(\$\{\{)(.+?)(\}\})')
    values = {}
    for masterLine in master:
	(k, v) = masterLine.split(':', 1)
	values[k] = v.strip()
    newLines = []
    for configFile in configs:
	print configFile
	f = open(configFile,'r')
	for line in f:
	    for match in replace_regex.finditer(line):
	        try:
		    if match.group(2) in values:
		        line = line.replace(match.group(0), str(values[match.group(2)]))
		except KeyError:
		    raise ConfigsError('ERROR: Missing master value {0}'.format(match.group(2)))
	    newLines.append(line)
	f.close()
    
        with open(configFile, 'w+') as e:
	        e.writelines(newLines)
	    newLines = []
	    e.close()
    print 'CONGIG PREPARED'
					
def preparePackage(tmpDir):
    os.chdir(tmpDir)
    subprocess.call('pwd', shell=True)
    #file = zipfile.zipfile(tmpDir.split('/')[-1]+'.zip', 'w')
    #for dirpath, dirnames, filenames in os.walk(tmpDir):
	#for name in filenames:
	    #if '.svn' not in dirpath and '.svn' not in dirnames and '.svn' not in name:
	    #print name
    	    #file.write(os.oath.join(dirpath,name))
    #fale.close()
    subprocess.call('zip -x *.svn* -q -r /tmp/'+tmpDir.split('/')[-1]+'.zip ./*', shell=True)
    print 'Zipfile prepared: {0}.zip'.format(tmpDir)
    return tmpDir+'.zip'

def main(application, environment):
    """Prepare configuration for application with placeholders"""
    try:
        config = configUpdate(application, environment)
        list = listConfigs(config)
        master = masterConfigs(application, environment)
        replace = replacePlaceholder(master, list)
        path = preparePackage(config)
	return path
    except KeyboardInterrupt:
	print 'Process interrupted...'
