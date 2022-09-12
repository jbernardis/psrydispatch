class Signal:
	def __init__(self, frame, name, pos, tiles):
		self.frame = frame
		self.name = name
		self.tiles = tiles
		self.pos = pos
		self.aspect = 0

	def Draw(self):
		bmp = self.tiles.getBmp(self)
		self.frame.DrawTile(self.pos[0], self.pos[1], bmp)

	def SetAspect(self, aspect):
		if self.aspect == aspect:
			return False
		
		self.aspect = aspect
		return True

