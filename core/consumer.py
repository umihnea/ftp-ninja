import multiprocessing as mp
from core.logger import Logger

class Consumer(mp.Process):
	"""
	A Consumer builds on a mp.Process task.

	A Consumer object is constructed with a reference to task_queue (a mp.JoinableQueue).
	Python thus manages the <Consumer pool>'s access to the queue.
	"""
	
	def __init__(self, task_queue):
		mp.Process.__init__(self)
		self.task_queue = task_queue
		self.logger = Logger()

	"""
	TODO: implement a killswitch.
	
	The run() function overrides the mp.Process.run(), which is not called explicitly.
	Instead, Consumers are initiated by calling another override, mp.Process.start().

	The loop:
	1. Fetch a Task object from the shared task_queue. (This does not dequeue the Task)
	2. Call the run() on the Task. It should return a list of Task objects.
	3. Dequeue the Task.
	4. Consumer enqueues the returned Tasks to the task_queue.

	"""
	def run(self):

		proc_name = self.name
		while True:
			current_task = self.task_queue.get()

			results = current_task.run()

			self.task_queue.task_done()

			for each in results:
				self.task_queue.put(each)
				self.logger.log(proc_name + ": Path " + each.path + " is a directory.")

		return

	def die(self):
		self.logger.log(self.name + " commited seppuku.")
		try:
			self.terminate()
		except Exception as e:
			self.logger.error(e)
		return