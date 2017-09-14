import os
import sys
import time
import json
import ftplib
import random
import logging
import datetime
from pathlib import Path

def isFile(ftp, filename):
	try:
		ftp.size(filename)
		return True
	except:
		return False

def crawlFtp(ftp, path, numFolders, numFiles):
	lines = []
	try:
		ftp.cwd(str(path))
		ftp.dir(str(path), lines.append)
		results = []
		folders = []
		for line in lines:
			fields = line.split()
			if isFile(ftp, fields[8]) == True:
				text = "File "
				text += fields[8]
				print text
				numFiles += 1
			else:
				text = "Folder "
				text += fields[8]
				print text
				folders.append(fields[8])
				numFolders += 1
		for folder in folders:
			print "Entering folder \t" + folder
			crawlFtp(ftp, Path(path, folder), numFolders, numFiles)
	except Exception:
		pass

def main():
	numFolders = 0
	numFiles = 0
	path = Path('/')
	level = 1
	ftp = ftplib.FTP('ftp.astral.ro')
	ftp.login()
	crawlFtp(ftp, path, numFolders, numFiles)
	print "Folders: " + numFolders
	print "Files: " + numFiles
		
	print "Job done!"
	ftp.quit()



main()