# Squelch tail process
import threading
from subprocess import Popen, PIPE

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

	def run(self):
		if host:
			tailCommand = ['ssh', '-t', host, 'tail', '-f', self.filepath]
		else:
			tailCommand = ['tail', '-f', self.filepath]
		self.P = Popen(tailCommand, stdin=PIPE, stdout=PIPE)
		while not self.stoprequest:
			# Read from stdin continuesly and print
			pass

	def join(self):
		self.stoprequest.set()
		super(squelchTailer, self).join(timeout)