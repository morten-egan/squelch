# Squelch process reader/writer thread.
import os
import time
import threading
import Queue
from subprocess import Popen, PIPE

class squelchProcessThread(threading.Thread):
	"""A squelch process thread. Taken any command, it will process input commands
	and write the output to the main console
	"""

	def __init__(self, command, inputQueue):
		super(squelchProcessThread, self).__init__()
		self.stoprequest = threading.Event()
		self.command = command
		self.inputQueue = inputQueue
		self.P = None

	def spawnProcess(self):
		self.P = Popen(self.command, stdin=PIPE, stdout=PIPE)

	def run(self):
		while not self.stoprequest.isSet():
			try:
				pExec = self.inputQueue.get(True, 0.05)
				self._submitExec(pExec)
			except:
				continue

	def join(self, timeout=None):
		self.stoprequest.set()
		super(squelchProcessThread, self).join(timeout)

	def _submitExec(self, command):
		self.P.stdin.write(command)