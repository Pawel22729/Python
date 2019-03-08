#!/usr/bin/python

import json
from fetchAppList import stripAll, getAppVer

list = stripAll()
resultList = []
for i in list:
    result = "\""+i.strip('.yaml')+"\""+':'+json.dumps(getAppVer(i), indent=2)
    resultList.append(result)

with open('jsonVersion.json', 'w') as f:
    f.write('{"Apps":{')
    f.close()
with open('jsonVersion.json', 'a') as f:
    output = ""
    for i in resultList:
	output = output + i+','
    f.write(output[:-1])
    f.write('}}')
    f.close()
    


