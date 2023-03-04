 
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
import cgi
cgitb.enable()
import urllib
import os
import shutil
import sys

print "Content-Type: text/html"
print

form = cgi.FieldStorage()
link = form.getvalue("link")
usun = form.getvalue("usun")
name = form.getvalue("name")
fileName = form.getvalue("fileName")
print "<br>"


if link <= 0:
	print """
	<form>
	Link: <br><input type='text' name='link' method='get'><br>
	File name: <br><input type='text' name='fileName'>
	<br><input type='submit' value='Download...'>
	</form><br>
	"""
	print "Uploaded files:<br>"
	uploaded = os.listdir('/var/www/downloads')
	for i in range(len(uploaded)):
		path = os.path.abspath(uploaded[i])
		print "<form>%s<button name='usun' type='submit' value='%s'>Delete file...</button></form>" % (uploaded[i], uploaded[i])
	if usun > 0:
		if os.path.exists('/var/www/downloads/'+usun):
			os.remove('/var/www/downloads/'+usun)
			print "<script>javascript:location.reload(true);</script>"
			
else:
	print "Downloading...<br>%s" % link
	try:
		link_open = urllib.FancyURLopener()
        	plik = link_open.retrieve(link)

	except Exception as blad:
		print blad

	try:
		location = os.path.abspath('/var/www/downloads/')
		if fileName > 0:
			shutil.move(plik[0], location+"/"+fileName)
			print "<br>File moved to<br>%s" % location+"/"+fileName
		else:
                	shutil.move(plik[0], location)
			print "<br>File moved to<br>%s" % location

	except Exception as blad2:
		print blad2

	else: 
		print "<br>Done!<br>"
		print "<a href='http://plasak.no-ip.org:8080/cgi-bin/upload.cgi'>GO BACK</a>"

