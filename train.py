class Train:
	def __init__(self, name=None):
		self.name = name
		self.loco = None
		self.blocks = []

	def SetName(self, name):
		self.name = name

	def SetLoco(self, loco):
		self.loco = loco

	def GetName(self):
		return self.name

	def GetLoco(self):
		return self.loco

	def GetIDString(self):
		n = self.name if self.name else "???"
		l = self.loco if self.loco else "???"
		return n+"/"+l
