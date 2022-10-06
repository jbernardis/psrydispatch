class Train:
	def __init__(self, name=None):
		print("creating new train object for train %s" % name)
		self.name = name
		self.loco = None
		self.blocks = {}

	def tstring(self):
		return "%s/%s (%s)" % (self.name, self.loco, str(self.blocks))

	def SetName(self, name):
		self.name = name

	def SetLoco(self, loco):
		self.loco = loco

	def GetName(self):
		return self.name

	def GetLoco(self):
		return self.loco

	def GetNameAndLoco(self):
		return self.name, self.loco

	def GetIDString(self):
		n = self.name if self.name else "???"
		l = self.loco if self.loco else "???"
		return n+"/"+l

	def Draw(self):
		for blk in self.blocks.values():
			print("Drawing train %s in block %s" % (self.name, blk.GetName()))
			blk.DrawTrain()

	def AddToBlock(self, blk):
		bn = blk.GetName()
		if bn in self.blocks:
			print("already have train %s in block %s" % (self.name, bn))
			return

		self.blocks[bn] = blk
		print("train %s added to block %s cound %d" % (self.name, bn, len(self.blocks)))

	def RemoveFromBlock(self, blk):
		bn = blk.GetName()
		if bn not in self.blocks:
			print("no need to remove train from block %s" % (self.name, bn))
			return

		del self.blocks[bn]
		print("train %s removed block %s count %d" % (self.name, bn, len(self.blocks)))
