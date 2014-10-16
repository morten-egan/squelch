# Squelch
# Oracle sqlplus wrapper
import os
import cmd
import readline
from subprocess import Popen, PIPE
import Queue
import squelchProcessThread
import squelchTail

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
		self.sqParms['tailers'] = []
		# Set defaults
		self.sqParms['allows']['DROP'] = False
		self.sqParms['allows']['TRUNCATE'] = False
		self.sqParms['allows']['SHUTDOWN'] = False

	def setPrompt(self):
		self.prompt = 'Squelch [' + self.sqParms['cwd'] + '][' + self.connstring + ']> '

	def createSqlplus(self, user, passw, tns):
		connectionObject = {}
		if tns:
			cstring = user + '/' + passw + '@' + tns
		else:
			cstring = user + '/' + passw
		# Create the actual sqlplus process and get descriptor
		connectionObject['sqlplusprocess'] = Popen(['sqlplus', '-s', cstring], stdin=PIPE, stdout=PIPE)

	# Public commands
	def do_set(self, args):
		splArgs = args.split(' ')

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

	def do_stail(self, args):
		'Squelch tail, which runs in the background. Automatically opens squelch output console'
		argSpl = args.split(' ')
		tailObject = {}
		tailObject['name'] = args
		if len(argSpl) > 1:
			tailObject['tailThread'] = squelchTail.squelchTailer(argSpl[1], argSpl[0])
		else:
			tailObject['tailThread'] = squelchTail.squelchTailer(argSpl[0])
		# Start the tail process
		tailObject['tailThread'].start()
		# Add the tail object to the tailers list
		self.sqParms['tailers'].append(tailObject)

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