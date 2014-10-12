# Squelch
# Oracle sqlplus wrapper
import os
import cmd
import readline
from subprocess import Popen, PIPE

# Define intro text
introText = '''===============================================
== Welcome to Squelch
== SQL plus a bit more
==============================================='''

class Squelch(cmd.Cmd):

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.connstring = ''
		self.intro = introText
		self.setPrompt()
		self.initSquelch()

	def emptyline(self):
		pass

	def initSquelch(self):
		# Initialize squelch parameters
		self.sqParms = {}
		self.sqParms['allows'] = {}
		self.sqParms['connections'] = {}
		self.sqParms['spools'] = {}
		self.sqParms['cwd'] = '/home/morten/Kode/Projects/squelch'
		# Set defaults
		self.sqParms['allows']['DROP'] = False
		self.sqParms['allows']['TRUNCATE'] = False
		self.sqParms['allows']['SHUTDOWN'] = False

	def setPrompt(self):
		self.prompt = 'Squelch [' + self.connstring + ']=> '

	def do_ls(self, args):
		os.system('ls ' + args + ' ' + self.sqParms['cwd'])

	def do_tail(self, args):
		os.system('tail ' + args)
		print os.linesep

	def do_head(self, args):
		os.system('head ' + args)

	def do_strace(self, args):
		os.system('strace ' + args)

	def do_pwd(self, args):
		print self.sqParms['cwd']

	def do_cd(self, args):
		if args[:1] == '/':
			self.sqParms['cwd'] = args
		else:
			self.sqParms['cwd'] = self.sqParms['cwd'] + args

	def do_exit(self, args):
		'Exit Squelch'
		return -1

if __name__ == '__main__':
	cmdline = Squelch()
	cmdline.cmdloop()