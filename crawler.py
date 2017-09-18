import os
import sys
import time
import ftplib
import random
import logging
import datetime
from pathlib import Path
import click
import sqlite3
import random
import multiprocessing

#Connection to the ftp host
def ftpConn(host):
	#host = 'firl.rsmas.miami.edu'
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

#Gets a list with all files&folders inside the current path
def crawlFtp(ftp, path, conn, q):
	logging.debug("Entering folder \t\t\t" + str(path))
	#Lines stores all the data from ftp.dir()
	lines = []
	try:
		ftp.cwd(str(path))
		ftp.dir(str(path), lines.append)
		for line in lines:
			fields = line.split()
			#Combining fileds for the files/folders that are using spaces in their name
			name = ' '.join(fields[8:])
			if isFile(ftp, name) == True:
				indexerDB(ftp.host, name, str(path), conn)
				logging.debug("File " + name)
			else:
				name = name.replace("/", "")
				#Folders will be pushed into the queue
				q.put(Path(path, name))
				folders.append(name)
				logging.debug("Folder " + name)
	except Exception as e:
		logging.error(e, exc_info=True)

@click.command()
@click.option('--host', prompt='Host', help='FTP server host ip/address')
@click.option('--path', prompt='Path', default='/', help='Enter the path to index')
@click.option('--workers', prompt='Workers', default=4, help='Enter the number of workers')
def worker(path, host, workers):
	#Clearing log file
	with open('log.log', 'w'):
		pass

	#Initializing log
	logging.basicConfig(filename='log.log',level=logging.DEBUG, format="%(levelname)s|%(asctime)s|%(message)s")
	logging.info("Starting crawling")

	ftp = []
	#Initializing a separate connection for each worker
	for i in range(0, workers):
		ftp.append(ftpConn(host))

	#Connecting to the db
	conn = dbConn()

	#Initializing the pool of processes
	pool = multiprocessing.Pool(processes=workers)

	#Initializing multiprocessing queue for better synchronization
	m = multiprocessing.Manager()
	q = m.Queue()

	#Finding first folders
	crawlFtp(ftp[0], path, conn, q)

	#Start workers for every folder inside queue
	while not q.empty():
		#Defining jobs
		jobs = []
		for i in range(0, workers):
			process = multiprocessing.Process(target=crawlFtp, args=(ftp[i], Path(path, str(q.get())), conn, q))
			jobs.append(process)

		# Starting the processes	
		for j in jobs:
			j.start()

		# Making sure all processes have finished work
		for j in jobs:
			j.join()


	#Last commit to the db
	conn.commit()
	logging.info("Last commit to db")
	logging.info("Job done!")

	#Killing all connections to the ftp server
	for ftpServer in ftp:
		ftpServer.quit()

if __name__ == '__main__':
    worker()
