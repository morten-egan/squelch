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
		self.initSquelch()
		# Lastly set the prompt and open up for business
		self.setPrompt()

	def emptyline(self):
		pass

	def initSquelch(self):
		# Initialize squelch parameters
		self.sqParms = {}
		self.sqParms['allows'] = {}
		self.sqParms['connections'] = {}
		self.sqParms['spools'] = {}
		self.sqParms['cwd'] = os.path.dirname(os.path.abspath(__file__))
		# Set defaults
		self.sqParms['allows']['DROP'] = False
		self.sqParms['allows']['TRUNCATE'] = False
		self.sqParms['allows']['SHUTDOWN'] = False

	def setPrompt(self):
		self.prompt = 'Squelch [' + self.sqParms['cwd'] + '][' + self.connstring + ']> '

	def do_ls(self, args):
		os.system('ls ' + args + ' ' + self.sqParms['cwd'])

	def do_tail(self, args):
		os.system('tail ' + args)
		print os.linesep

	def do_head(self, args):
		os.system('head ' + args)

	def do_strace(self, args):
		os.system('strace ' + args)

	def do_pstack(self, args):
		os.system('pstack ' + args)

	def do_lsof(self, args):
		os.system('lsof ' + args)

	def do_ps(self, args):
		os.system('ps ' + args)

	def do_vi(self, args):
		os.system('vi ' + args)

	def do_pwd(self, args):
		print self.sqParms['cwd']

	def do_top(self, args):
		os.system('top')

	def complete_cd(self, text, line, begidx, endidx):
		dirlist = [name for name in os.listdir(self.sqParms['cwd']) if os.path.isdir(os.path.join(self.sqParms['cwd'], name))]
		return [i for i in dirlist if i.startswith(text)]

	def do_cd(self, args):
		if args[:1] == '/':
			if args[-1:] == '/':
				self.sqParms['cwd'] = args[:-1]
			else:
				self.sqParms['cwd'] = args
		elif args == '..':
			sls = self.sqParms['cwd'].rfind('/')
			self.sqParms['cwd'] = self.sqParms['cwd'][:sls]
		elif args == '.':
			pass
		elif args[:1] == '$':
			self.sqParms['cwd'] = os.environ[args[1:]]
		else:
			self.sqParms['cwd'] = self.sqParms['cwd'] + '/' + args
		self.setPrompt()

	def do_exit(self, args):
		'Exit Squelch'
		return -1

if __name__ == '__main__':
	cmdline = Squelch()
	cmdline.cmdloop()