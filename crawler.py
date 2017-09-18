from core.logger import Logger
from core.indexer import Indexer

import click

from collections import deque

@click.command()
@click.option("--host", prompt="Host", help="IP Address of a FTP Server", default="0.0.0.0")
@click.option("--port", prompt="Port", help="FTP Port of the Server", default=2121)
@click.option('--workers', prompt='Workers', help='Number of Workers used for Indexing', default=4)

def main(host, port, workers):
	"""
	ftp-ninja

	Performs a simple tree search to index a FTP server.

	- There are no database wrappers.
	- The Logger always picks a random color.

	Tested on a self-hosted pyftpdlib server and configured for its defaults.
	"""

	lg = Logger("log.log")
	x = Indexer(host, port)
	
	lg.log("Ready.")

	start_nodes = x.get_files()
	bfs_queue = deque([])

	for node in start_nodes:
		if x.is_file(node):
			lg.log(node + " is a file.")
		else:
			lg.log(node + " is a folder.")
			bfs_queue.append(node)

	while len(bfs_queue):
		current = bfs_queue.popleft()
		if x.is_file(current):
			lg.log(current + " is a file.")
		else:
			lg.log(current + " is a folder.")

			nodes = []
			nodes = x.get_files(current)
			for node in nodes:
				bfs_queue.append(current + "/" + node)

	lg.log("Operation successful.")


if __name__ == '__main__':
	main()
