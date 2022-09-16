from constants import RED

class Signal:
	def __init__(self, tower, screen, frame, name, east, pos, tiles):
		self.tower = tower
		self.screen = screen
		self.frame = frame
		self.name = name
		self.tiles = tiles
		self.pos = pos
		self.aspect = RED
		self.east = east

	def GetTower(self):
		return self.tower

	def GetScreen(self):
		return self.screen

	def GetName(self):
		return self.name

	def GetPos(self):
		return self.pos

	def GetEast(self):
		return self.east

	def Draw(self):
		bmp = self.tiles.getBmp(self)
		self.frame.DrawTile(self.screen, self.pos, bmp) 

	def GetAspect(self):
		return self.aspect

	def SetAspect(self, aspect, refresh=False):
		if self.aspect == aspect:
			return False
		
		self.aspect = aspect
		if refresh:
			self.Draw()
		return True

