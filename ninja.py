import multiprocessing as mp
from core.logger import Logger
from core.indexer import FTPDriver
import os
import pickle
import click

class Consumer(mp.Process):
	
	def __init__(self, task_queue, quit_event):
		mp.Process.__init__(self)
		self.task_queue = task_queue
		self.quit_event = quit_event
		self.logger = Logger()

	def run(self):
		proc_name = self.name
		while not self.quit_event.is_set():
			current_task = self.task_queue.get()

			results = current_task.run()

			self.task_queue.task_done()

			for each in results:
				self.task_queue.put(each)
				self.logger.log(proc_name + ": Path " + each.path + " is a directory.")
			
		if self.quit_event.is_set():
			die()

		return

	def die(self):
		self.logger.log(self.name + " commited seppuku.")
		try:
			self.terminate()
		except Exception as e:
			self.logger.error(e)
		return

class Task(object):
	def __init__(self, host, port, path):
		self.host = host
		self.port = port
		self.path = path

	def run(self):
		ftp = FTPDriver(self.host,self.port, self.path)

		dirs = []
		dirs = ftp.get_dirs()

		tasks = []

		for each in dirs:
			T = Task(self.host, self.port, os.path.join(self.path, each))
			tasks.append(T)

		return tasks

def main():
	"""
	ftp-ninja

	"""
	host = "0.0.0.0"
	port = 21
	consumer_count = mp.cpu_count() * 2

	quit_event = mp.Event() # Define a quit event

	tasks = mp.JoinableQueue() # Define the task queue

	consumers = [ # Define consumers
		Consumer(tasks, quit_event)
		for i in xrange(consumer_count)
	]

	for each in consumers:
		each.start()

	print("Started consumers.")

	T = Task(host, port, "/") # Add tasks into the queue
	# pickle.dumps(T)
	tasks.put(T)

	print("Populated task queue.")

	try:
		tasks.join() # Wait for all of the tasks to finish
	except KeyboardInterrupt as e:
		print("\nHalted.")
		quit_event.set()
	except Exception as e:
		quit_event.set()
	# finally:
	# 	tasks.join()

if __name__ == '__main__':
	main()
