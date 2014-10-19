# Squelch
# Oracle sqlplus wrapper
import os
import cmd
import readline
from subprocess import Popen, PIPE
import Queue
import squelchProcessThread
import squelchTail
import sys
import orahelper

# Define intro text
introText = '''

 _______  _______           _______  _        _______          
(  ____ \(  ___  )|\     /|(  ____ \( \      (  ____ \|\     /|
| (    \/| (   ) || )   ( || (    \/| (      | (    \/| )   ( |
| (_____ | |   | || |   | || (__    | |      | |      | (___) |
(_____  )| |   | || |   | ||  __)   | |      | |      |  ___  |
      ) || | /\| || |   | || (      | |      | |      | (   ) |
/\____) || (_\ \ || (___) || (____/\| (____/\| (____/\| )   ( |
\_______)(____\/_)(_______)(_______/(_______/(_______/|/     \|
                                                               
                 Because sql++ was already taken!
'''

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
		self.sqParms['keepConnections'] = True
		self.sqParms['dblist_tns'] = []
		self.sqParms['dblist_oratab'] = []
		self.sqParms['dblist_process'] = []
		# Set defaults
		self.sqParms['allows']['DROP'] = False
		self.sqParms['allows']['TRUNCATE'] = False
		self.sqParms['allows']['SHUTDOWN'] = False
		# Run preparation and init functions
		self.oraPrepare()

	def setPrompt(self):
		self.prompt = 'Squelch [' + self.sqParms['cwd'] + '][' + self.connstring + ']> '

	def writeEmpty(self):
		print ''

	def oraPrepare(self):
		self.sqParms['dblist_tns'] = orahelper.getTNSList('/home/morten/tns/tnsnames.ora')
		self.sqParms['dblist_oratab'] = orahelper.getOratabList('/home/morten/tns/oratab')
		self.sqParms['dblist_process'] = orahelper.getOraRunningList()

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
		print ''

	def do_tails(self, args):
		for tailer in self.sqParms['tailers']:
			print tailer['name']

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

	def complete_ldb(self, text, line, begidx, endidx):
		return [i for i in self.sqParms['tnslist'] if i.startswith(text)]

	def do_ldb(self, args):
		try:
			for database in self.sqParms['dblist_tns']:
				print database
		except:
			pass
		try:
			for database in self.sqParms['dblist_oratab']:
				print database
		except:
			pass
		try:
			for database in self.sqParms['dblist_process']:
				print database
		except:
			pass

	def do_sqlplus(self, args):
		connectionObject = {}
		connectionObject['inputQueue'] = Queue.Queue()
		connectionObject['outputQueue'] = Queue.Queue()
		connectionObject['squelchPlus'] = squelchProcessThread.squelchProcessThread(args, connectionObject['inputQueue'], connectionObject['outputQueue'])
		# Start the sqlplus process and Squelch controller thread
		# connectionObject['squelchPlus'].start()
		# Add to connection list
		self.sqParms['connections']['DBNAME'] = connectionObject

	def do_exit(self, args):
		'Exit Squelch'
		# Clean up tailers
		for tailer in self.sqParms['tailers']:
			tailer['tailThread'].join()
		return -1

if __name__ == '__main__':
	os.system('clear')
	cmdline = Squelch()
	cmdline.cmdloop()