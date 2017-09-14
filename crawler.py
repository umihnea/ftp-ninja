import os
import sys
import time
import json
import ftplib
import random
import logging
import datetime
from pathlib import Path
import click

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

				logging.debug(text)

				numFiles += 1
			else:
				text = "Folder "
				text += fields[8]

				logging.debug(text)

				folders.append(fields[8])
				numFolders += 1
		for folder in folders:

			logging.debug("Entering folder \t" + folder)

			crawlFtp(ftp, Path(path, folder), numFolders, numFiles)
	except Exception:
		pass

#@click.command()
#@click.option('--host', help='Host to index.')
def main():
	logging.basicConfig(filename='log.log',level=logging.DEBUG, format="%(levelname)s|%(asctime)s|%(message)s")
	# logging.basicConfig(filename='log.log', filemode='w', format="%(levelname)s|%(asctime)s|%(message)s")

	logging.info("Starting crawling")

	numFolders = 0
	numFiles = 0
	path = Path('/')
	level = 1
	ftp = ftplib.FTP('ftp.astral.ro')
	ftp.login()

	crawlFtp(ftp, path, numFolders, numFiles)

	logging.info("Folders: " + str(numFolders))
	logging.info("Files: " + str(numFiles))
		
	logging.info("Job done!")
	ftp.quit()



main()