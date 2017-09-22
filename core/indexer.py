import ftplib
from os import path

class FTPDriver(object):
	def __init__(self, host, port=21, path="/"):
		self.ftp = self.connect(host, port, path)
		self.cwd = path

	def cd(self, path):
		self.ftp.cwd(path)
		self.cwd = path

	def cwd(self):
		pwd = self.ftp.pwd()
		# if self.cwd != pwd:
		# 	self.cwd = pwd
		return pwd #self.cwd

	def get_nodes(self, path="/"):
		nodes = []
		nodes = self.ftp.nlst(path)

		return nodes

	def get_files(self, path="./"):
		nodes = []
		files = []

		nodes = self.get_nodes(path)

		for node in nodes:
			path_to_file = path + node
			if self.is_file(path_to_file):
				files.append(node)

		return files

	def get_dirs(self, path="./"):
		nodes = []
		dirs = []

		nodes = self.get_nodes(path)
		for node in nodes:
			path_to_dir = path + node
			if not self.is_file(path_to_dir):
				dirs.append(node)

		return dirs

	@staticmethod
	def connect(host, port, path):
		f = ftplib.FTP()
		f.connect(host, port)
		f.login()
		f.cwd(path)

		return f

	def is_file(self, path):
		"""
		Seriously hacky stuff.
		"""

		self.ftp.voidcmd('TYPE I')

		curr = self.ftp.pwd() # Save the current path
		ret = False

		try:
			self.ftp.cwd(path) # Try moving to this one
		except Exception as e:
			ret = True
		finally:
			if self.ftp.pwd() != curr: # If we moved,
				self.ftp.cwd(curr)     # then move back

		return ret
		