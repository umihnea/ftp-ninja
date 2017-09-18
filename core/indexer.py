import ftplib

class Indexer:
	def __init__(self, host, port=21, path="/"):
		self.ftp = self.connect(host, port, path)

	def get_files(self, path="/"):
		files = []
		files = self.ftp.nlst(path)
		return files

	@staticmethod
	def connect(host, port, path):
		f = ftplib.FTP()
		f.connect(host, port)
		f.login()
		f.cwd(path)

		return f

	def is_file(self, filename):
		self.ftp.voidcmd('TYPE I')
		try:
			self.ftp.size(filename)
			return True
		except:
			return False
		