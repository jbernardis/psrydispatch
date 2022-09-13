class Button:
	def __init__(self, tower, screen, frame, name, pos, tiles):
		self.tower = tower
		self.screen = screen
		self.frame = frame
		self.name = name
		self.pos = pos
		self.tiles = tiles
		self.aspect = 0
		self.pressed = False

	def GetTower(self):
		return self.tower

	def GetScreen(self):
		return self.screen

	def GetPos(self):
		return self.pos

	def GetName(self):
		return self.name

	def Draw(self):
		if self.pressed:
			bmp = self.tiles.dark
		else:
			bmp = self.tiles.light
		self.frame.DrawTile(self.screen, self.pos, bmp)

	def Press(self, refresh=False):
		if self.pressed:
			return False
		
		self.pressed = True
		if refresh:
			self.Draw()

		return True

	def Release(self, refresh=False):
		if not self.pressed:
			return False
		
		self.pressed = False
		if refresh:
			self.Draw()

		return True
