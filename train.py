class train:
	def __init__(self, name, frame):
		self.name = name
		self.frame = frame
		self.loco = None
		self.blocks = []

	def SetLoco(self, loco):
		self.loco = loco

	def GetName(self):
		return self.name

	def GetLoco(self):
		return self.loco

	def AddToBlock(self, blknm, refresh=False):
		if blknm in self.blocks:
			return

		self.blocks.append(blknm)
		if refresh:
			self.Draw()

	def RemoveFromBlock(self, blknm, refresh=False):
		if not blknm in self.blocks:
			return

		self.blocks = [x for x in self.blocks if x != blknm]
		if refresh:
			self.Draw()

	def Draw(self):
		for b in self.blocks:
			blk = self.frame.blocks[b]
			blk.DrawTrain()
