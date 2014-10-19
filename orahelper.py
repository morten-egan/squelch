# Squelch oracle helper functions
import re
import os

def getTNSList(tnspath):
	tnsFile = open(tnspath, 'r')
	tnsContent = tnsFile.read()
	# Remove comments and blank lines
	tnsContent = re.sub(r'#[^\n]*\n', '\n', tnsContent)
	tnsContent = re.sub(r'( *\n *)+', '\n', tnsContent.strip())
	# Init list and parms
	databases = []
	dblist = []
	start = 0
	c = 0
	while c < len(tnsContent):
		parens = 0
		c = tnsContent.find('(')
		while c < len(tnsContent):
			if tnsContent[c] == '(':
				parens += 1
			elif tnsContent[c] == ')':
				parens -= 1
			c += 1
			if parens == 0:
				break
		databases.append(tnsContent[start:c].strip())
		tnsContent = tnsContent[c:]
		c = 0
	for database in databases:
		name = re.match(r'(\w+)', database).group(1)
		dblist.append(name)
	return dblist

def getOratabList(oratabpath='/etc/oratab'):
	oratabFile = open(oratabpath, 'r')
	dblist = []
	for line in oratabFile:
		if line[:1] == '#' or line == '':
			pass
		else:
			sl = line.split(':')
			dblist.append(sl[0])
	return dblist

def getOraRunningList():
	pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
	dblist = []
	for pid in pids:
		cmdline = open(os.path.join('/proc', pid, 'cmdline'), 'rb').read()
		if cmdline.find('pmon') > 0:
			lpos = cmdline.rfind('_') + 1
			dblist.append(cmdline[lpos:])
