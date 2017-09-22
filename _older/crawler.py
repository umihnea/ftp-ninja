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

	"""

	lg = Logger("log.log")
	x = Indexer(host, port)
	
	lg.log("Ready.")

	search_queue = deque([])


	for each in x.get_files():
		lg.log(each + " is a file.")

	for each in x.get_dirs():
		search_queue.append(each)

	while len(search_queue):
		current = search_queue.popleft()
		lg.log(current + " is a directory.")

		for each in x.get_files(current + "/"):
			lg.log(each + " is a file.")

		for each in x.get_dirs(current + "/"):
			search_queue.append(current + "/" + each)

	lg.log("Operation successful.")


if __name__ == '__main__':
	main()
