import multiprocessing
from core.logger import Logger

class Consumer(multiprocessing.Process):
	
	def __init__(self, task_queue): # , result_queue
		multiprocessing.Process.__init__(self)
		self.task_queue = task_queue
		self.logger = Logger(self.name + ".log")

		#self.result_queue = result_queue

	def run(self):
		proc_name = self.name

		while True:
			current_task = self.task_queue.get()

			if current_task is None:
				self.die()
				break
			else:
				self.logger.log(proc_name + ": I just retrieved " + current_task.root + " from the queue.")

			tasks_to_add = current_task.run()

			self.logger.log(current_task.get_message(proc_name))

			self.task_queue.task_done()

			for each in tasks_to_add:
				self.task_queue.put(each)
				self.logger.log(proc_name + ": I just put " + each.root + " in queue.")

		return

	def die(self):
		self.logger.log(self.name + ": I will commit seppuku now.")
		self.task_queue.task_done()
		return


class Task(object):
	def __init__(self, graph, root, visited):
		self.graph = graph
		self.root = root
		self.visited = visited

		self.verb = "Visited"

	def run(self):
		nodes_to_add = []
		graph = self.graph

		if self.root not in graph:
			self.verb = "No nodes found for"
			return []

		if self.root in self.visited:
			self.verb = "Skipped"
			return []

		self.visited.add(self.root)

		for each in graph[self.root]:
			if each not in self.visited:
				nodes_to_add.append(each)

		tasks_to_add = []

		for each in nodes_to_add:
			T = Task(graph, each, self.visited)
			tasks_to_add.append(T)

		return tasks_to_add

	def get_message(self, proc_name):
		message = str(proc_name) + ": " + self.verb + " node " + str(self.root) + "."
		return message


if __name__ == '__main__':
	# Establish communication queues
	tasks = multiprocessing.JoinableQueue()
	#results = multiprocessing.Queue()
	
	# Start consumers
	num_consumers = multiprocessing.cpu_count() * 2
	print 'Creating %d consumers' % num_consumers

	consumers = [
		Consumer(tasks)
		for i in xrange(num_consumers)
	]

	for each in consumers:
		each.start()
	
	# Graph
	graph = {
		'A': ['B', 'C'],
		'B': ['D', 'E'],
		'C': ['F', 'G', 'H'],
		'D': [],
		'E': [],
		'F': ['I', 'J', 'K'],
		'I': ['L', 'M', 'N'],
		'J': [],
		'K': [],
		'L': ['O', 'P', 'Q', 'R'],
		'M': ['S', 'T', 'U', 'V']
	}

	# Enqueue the tree root
	S = set([])

	T = Task(graph, 'A', S)
	tasks.put(T)		

	# Wait for all of the tasks to finish
	tasks.join()