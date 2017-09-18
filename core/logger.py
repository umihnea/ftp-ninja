from colorama import Fore, Back, Style, init
from random import choice
import datetime


class Logger():

	def __init__(self, log_file):
		init()
		self.color = self.choose_color()
		self.log_file = self.create_file(log_file)

	def file_log(self, message):
		self.log_file.write(message + "\n")

	def log(self, message):
		timestamp = self.get_timestamp()

		self.console_log(self.color, message)
		self.file_log("[" + timestamp + "]: " + message)

	def error(self, message):
		timestamp = self.get_timestamp()

		self.console_log(Fore.RED, "Error encountered on " + timestamp + ". Check log for details.")
		self.file_log("[" + timestamp + "]: ERROR: " + message)

	def console_log(self, color, message):
		print(color + str(message))
	
	@staticmethod
	def choose_color():
		colors = [
			Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW,
			Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE
		];

		return choice(colors)

	@staticmethod
	def create_file(log_file):
		f = open(log_file, "w+")
		return f

	@staticmethod
	def get_timestamp():
		return datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S.%f")

