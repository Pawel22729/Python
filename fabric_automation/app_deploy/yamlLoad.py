#!/usr/bin/python -u

import sys
import os
import yaml

repoUrl = '/export/home/scm/tmp/deployments/'

def parseYaml(file):
    openStream = open(repoUrl+file+'.yaml','r')
    yamlContent = yaml.load(openStream)
    return yamlContent

