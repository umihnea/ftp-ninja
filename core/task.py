from core.indexer import FTPDriver
import os

class Task(object):
	"""
	Task objects 

	IMPORTANT: PICKLE
	The way mp.Process communication works, Task objects need to be pickle-able.
	
	Pickle-able objects do not encapsulate other objects.
	i.e. the FTPDriver object is created in run() rather than defined as an object property.
	"""
	def __init__(self, host, port, path):
		self.host = host
		self.port = port
		self.path = path

	def run(self):
		ftp = FTPDriver(self.host, self.port, self.path)

		dirs = []
		dirs = ftp.get_dirs()

		tasks = []

		for each in dirs:
			T = Task(self.host, self.port, os.path.join(self.path, each))
			tasks.append(T)

		return tasks