#!/usr/bin/python

import sys

def getKernel(host):
    with open("kernelCronList", 'r') as f:
	for i in f:
	    if host in i:
	        out = i
    return out.split(':')[1]

#getKernel(sys.argv[1])
