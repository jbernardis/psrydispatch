from constants import RED

class Signal:
	def __init__(self, district, screen, frame, name, east, pos, tiles):
		self.district = district
		self.screen = screen
		self.frame = frame
		self.name = name
		self.tiles = tiles
		self.pos = pos
		self.aspect = RED
		self.east = east
		self.possibleRoutes = {}
		self.guardBlock = None # block that the signal is guarding exit from

	def AddPossibleRoutes(self, blk, rtList):
		self.possibleRoutes[blk] = rtList

	def IsPossibleRoute(self, blknm, rname):
		if not blknm in self.possibleRoutes:
			return False
		
		return rname in self.possibleRoutes[blknm]
		
	def GetDistrict(self):
		return self.district

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

		if self.guardBlock is not None:
			self.guardBlock.EvaluateStoppingSections()
		return True

	def SetGuardBlock(self, blk):
		self.guardBlock = blk

	def GetGuardBlock(self):
		return self.guardBlock

