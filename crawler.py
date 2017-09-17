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
import sqlite3
import random

#Connection to the ftp host
def ftpConn(host):
	host = 'firl.rsmas.miami.edu'
	ftp = ftplib.FTP(host)
	ftp.login()
	return ftp

#Connection to the sqlite3 db
def dbConn():
	conn = sqlite3.connect('files.db')
	return conn

#Inserting into db all files, commiting at random intervals
def indexerDB(server, filename, path, conn):
	randomNum = random.randint(1, 32)
	if randomNum == 16:
		conn.commit()
		logging.info("Commited changes into db")
	c = conn.cursor()
	c.execute("INSERT INTO FILES (SERVER, NAME, PATHTO) VALUES (?, ?, ?)",(server, filename, path))

#Checks if it's a file or a folder by verifying if it has size
def isFile(ftp, filename):
	#TYPE I is only for some ftp servers which don't support ASCII encoding
	ftp.voidcmd('TYPE I')
	try:
		ftp.size(filename)
		return True
	except:
		return False

#Main code here, it's recursive and it crawls all the folders in a path
def crawlFtp(ftp, path, conn):
	#Lines stores all the data from ftp.dir()
	lines = []
	try:
		ftp.cwd(str(path))
		ftp.dir(str(path), lines.append)
		#Folders stores all the folders for the recursive call
		folders = []
		for line in lines:
			fields = line.split()
			#Combining fileds for the files/folders that are using spaces in their name
			name = ' '.join(fields[8:])
			if isFile(ftp, name) == True:
				indexerDB(ftp.host, name, str(path), conn)
				logging.debug("File " + name)
			else:
				name = name.replace("/", "")
				folders.append(name)
				logging.debug("Folder " + name)

		for folder in folders:
			logging.debug("Entering folder \t" + folder)
			crawlFtp(ftp, Path(path, folder), conn)

	except Exception as e:
		logging.error(e, exc_info=True)

@click.command()
@click.option('--host', prompt='Host', help='FTP server host ip/address')
@click.option('--path', prompt='Path', default='/', help='Enter the path to index')
def worker(path, host):
	#Clearing log file
	with open('log.log', 'w'):
		pass

	#Initializing log
	logging.basicConfig(filename='log.log',level=logging.DEBUG, format="%(levelname)s|%(asctime)s|%(message)s")
	logging.info("Starting crawling")

	#Connecting to the ftp server
	ftp = ftpConn(host)

	#Connecting to the db
	conn = dbConn()

	#Initializing crawler
	crawlFtp(ftp, path, conn)

	#Last commit to the db
	conn.commit()
	logging.info("Last commit to db")
	logging.info("Job done!")

	#Killing the connection to the ftp
	ftp.quit()

if __name__ == '__main__':
    worker()