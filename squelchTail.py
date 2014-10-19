# Squelch tail process
import threading
from subprocess import Popen, PIPE
import sys
import os

class squelchTailer(threading.Thread):
	"""Simple wrapper for tail, so you can tail files outside of main process
	And also tail remote files via ssh access
	"""

	def __init__(self, filepath, host=False):
		super(squelchTailer, self).__init__()
		self.filepath = filepath
		self.host = host
		self.stoprequest = threading.Event()
		self.P = None
		self.daemon = True

	def run(self):
		if self.host:
			tailCommand = ['ssh', '-t', self.host, 'tail', '-f', self.filepath]
		else:
			tailCommand = ['tail', '-f', self.filepath]
		self.P = Popen(tailCommand, stdin=PIPE, stdout=PIPE)
		for line in iter(self.P.stdout.readline, ''):
			if line != '':
				print self.OKBLUE + self.filepath + '-> ' + self.ENDC + line.rstrip(os.linesep)

	def join(self, timeout=None):
		self.P.kill()
		self.stoprequest.set()
		super(squelchTailer, self).join(timeout)