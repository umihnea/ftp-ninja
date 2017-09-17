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

def ftpConn():
	host = 'firl.rsmas.miami.edu'
	#host = 'ftp.astral.ro'
	# ftp = ftplib.FTP('69.30.214.178')
	ftp = ftplib.FTP(host)
	ftp.login()
	return ftp

def dbConn():
	conn = sqlite3.connect('files.db')
	return conn

def indexerDB(server, filename, path, conn):
	randomNum = random.randint(1, 32)
	if randomNum == 16:
		conn.commit()
		logging.info("Commited changes into db")
	c = conn.cursor()
	c.execute("INSERT INTO FILES (SERVER, NAME, PATHTO) VALUES (?, ?, ?)",(server, filename, path))

def isFile(ftp, filename):
	ftp.voidcmd('TYPE I')
	try:
		ftp.size(filename)
		return True
	except:
		return False

def crawlFtp(ftp, path, conn):
	lines = []
	try:
		ftp.cwd(str(path))
		ftp.dir(str(path), lines.append)
		results = []
		folders = []
		for line in lines:
			fields = line.split()
			if isFile(ftp, fields[8]) == True:
				indexerDB(ftp.host, fields[8], str(path), conn)
				logging.debug("File " + fields[8])

			else:
				name = fields[8].replace("/", "")
				folders.append(name)
				logging.debug("Folder " + fields[8])

		for folder in folders:
			logging.debug("Entering folder \t" + folder)
			crawlFtp(ftp, Path(path, folder), conn)

	except Exception as e:
		logging.error(e, exc_info=True)

def main():
	path = Path('/')
	conn = dbConn()
	with open('log.log', 'w'):
		pass
	logging.basicConfig(filename='log.log',level=logging.DEBUG, format="%(levelname)s|%(asctime)s|%(message)s")
	logging.info("Starting crawling")
	ftp = ftpConn()
	crawlFtp(ftp, path, conn)
	conn.commit()
	logging.info("Last commit to db")
	logging.info("Job done!")
	ftp.quit()



main()