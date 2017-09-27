from core.consumer import Consumer
from core.task import Task

import multiprocessing as mp
import os
import pickle
import click

def main():

	host = "0.0.0.0"
	port = 2121
	consumer_count = mp.cpu_count() * 2

	tasks = mp.JoinableQueue() # Defines the task queue

	consumers = [ # Populates consumer pool
		Consumer(tasks)
		for i in xrange(consumer_count)
	]

	for each in consumers:
		each.start()

	print("Started consumers.")

	T = Task(host, port, "/") # Populates queue w/ Task objects
	tasks.put(T)

	print("Populated task queue.")

	tasks.join() # Waits for all to finish

if __name__ == '__main__':
	main()
