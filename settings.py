import configparser
import os

INIFILE = "psrydisplay.ini"


def parseBoolean(val, defaultVal):
	lval = val.lower()
	
	if lval == 'true' or lval == 't' or lval == 'yes' or lval == 'y':
		return True
	
	if lval == 'false' or lval == 'f' or lval == 'no' or lval == 'n':
		return False
	
	return defaultVal

class Settings:
	def __init__(self, folder):
		self.cmdfolder = folder
		self.inifile = os.path.join(folder, INIFILE)
		self.section = "psrdisplay"	
		
		self.pages = 3
		self.dispatch = True
		self.ipaddr = "192.168.1.138"
		self.serverport = 9000
		self.socketport = 9001
		self.usecameradiagrams = False
		
		self.cfg = configparser.ConfigParser()
		self.cfg.optionxform = str
		if not self.cfg.read(self.inifile):
			print("Settings file %s does not exist.  Using default values" % INIFILE)
			self.save()
			return

		if self.cfg.has_section(self.section):
			for opt, value in self.cfg.items(self.section):
				if opt == 'pages':
					try:
						s = int(value)
					except:
						print("invalid value in ini file for pages: (%s)" % value)
						s = 3

					if s not in [1, 3]:
						print("Invalid values for pages: %d" % s)
						s = 3
					self.pages = s

				elif opt == 'dispatch':
					self.dispatch = parseBoolean(value, False)

				elif opt == 'usecameradiagrams':
					self.usecameradiagrams = parseBoolean(value, False)
						
				elif opt == 'ipaddr':
					self.ipaddr = value
						
				elif opt == 'socketport':
					try:
						s = int(value)
					except:
						print("invalid value in ini file for socket port: (%s)" % value)
						s = 9001
					self.socketport = s
						
				elif opt == 'serverport':
					try:
						s = int(value)
					except:
						print("invalid value in ini file for server port: (%s)" % value)
						s = 9000
					self.serverport = s

		else:
			print("Missing %s section - assuming defaults" % self.section)
	
	def save(self):
		try:
			self.cfg.add_section(self.section)
		except configparser.DuplicateSectionError:
			pass
		
		self.cfg.set(self.section, "pages", str(self.pages))
		self.cfg.set(self.section, "dispatch", str(self.dispatch))
		self.cfg.set(self.section, "usecameradiagrams", str(self.usecameradiagrams))
		self.cfg.set(self.section, "ipaddr", str(self.ipaddr))
		self.cfg.set(self.section, "socketport", str(self.socketport))
		self.cfg.set(self.section, "serverport", str(self.serverport))

		try:		
			cfp = open(self.inifile, 'w')
		except:
			print("Unable to open settings file %s for writing" % self.inifile)
			return
		self.cfg.write(cfp)
		cfp.close()
