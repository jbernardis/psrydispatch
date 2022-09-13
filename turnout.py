from constants import NORMAL, REVERSE, EMPTY
import traceback

class Turnout:
	def __init__(self, tower, frame, name, screen, tiles, block, pos):
		self.tower = tower
		self.frame = frame
		self.name = name
		self.screen = screen
		self.tiles = tiles
		self.pos = pos
		self.block = block
		self.normal = True
		self.routeControlled = False
		self.pairedTurnout = None

	def Draw(self):
		tostat = NORMAL if self.normal else REVERSE
		blkstat = self.block.GetStatusFromRoute(self.screen, self.pos)
		east = self.block.GetEast()
		bmp = self.tiles.getBmp(tostat, blkstat, east)
		self.frame.DrawTile(self.screen, self.pos, bmp)

	def SetRouteControl(self, flag=True):
		self.routeControlled = flag

	def IsRouteControlled(self):
		return self.routeControlled

	def SetPairedTurnout(self, turnout):
		self.pairedTurnout = turnout

	def Changeable(self):
		return self.block.GetStatus() == EMPTY

	def SetReverse(self, refresh=False):
		if not self.normal:
			return False

		if not self.Changeable():
			# cant change a turnout in busy block
			return False
		
		self.normal = False
		if self.pairedTurnout is not None:
			self.pairedTurnout.SetReverse()
		else:
			self.tower.DetermineRoutes(self.block)

		if refresh:
			self.Draw()
		return True

	def SetNormal(self, refresh=False):
		if self.normal:
			return False

		if not self.Changeable():
			# cant change a turnout in busy block
			return False
		
		self.normal = True
		if self.pairedTurnout is not None:
			self.pairedTurnout.SetNormal()
		else:	
			self.tower.DetermineRoutes(self.block)
		if refresh:
			self.Draw()
		return True

	def Toggle(self, refresh=False):
		if not self.Changeable():
			# cant change a turnout in busy block
			return False
		
		self.normal = not self.normal
		if self.pairedTurnout is not None:
			self.pairedTurnout.SetNormal()
		else:
			self.tower.DetermineRoutes(self.block)
		if refresh:
			self.Draw()

	def GetName(self):
		return self.name

	def GetTower(self):
		return self.tower

	def GetScreen(self):
		return self.screen

	def GetPos(self):
		return self.pos

	def IsNormal(self):
		return self.normal

	def IsReverse(self):
		return not self.normal

