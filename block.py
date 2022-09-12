from turnout import Turnout
from constants import EMPTY, OCCUPIED, CLEARED, BLOCK, OVERSWITCH

class Block:
	def __init__(self, tower, frame, name, tiles, east=True):
		self.tower = tower
		self.frame = frame
		self.name = name
		self.type = BLOCK
		self.tiles = tiles # [Tile, screen, coordinates, reverseindication]
		self.east = east
		self.occupied = False
		self.cleared = False
		self.determineStatus()
		self.route = []

	def determineStatus(self):
		self.status = OCCUPIED if self.occupied else CLEARED if self.cleared else EMPTY

	def GetBlockType(self):
		return self.type

	def GetName(self):
		return self.name

	def GetStatus(self, pos=None):
		if pos is not None:
			return self.status if pos in self.route else EMPTY
		else:
			return self.status

	def GetEast(self):
		return self.east

	def IsBusy(self):
		return self.cleared or self.occupied

	def Draw(self):
		for t, screen, pos, revflag in self.tiles:
			bmp = t.getBmp(self.status, self.east, revflag)
			self.frame.DrawTile(screen, pos, bmp)

	def SetOccupied(self, occupied=True, refresh=False):
		if self.occupied == occupied:
			# already in the requested state
			return

		self.occupied = occupied
		self.determineStatus()
		if refresh:
			self.Draw()

	def SetCleared(self, cleared=True, refresh=False):
		if cleared and self.occupied:
			# can't mark an occupied block as cleared
			return

		if self.cleared == cleared:
			# already in the desired state
			return

		self.cleared = cleared
		self.determineStatus()
		if refresh:
			self.Draw()

class OverSwitch (Block):
	def __init__(self, tower, frame, name, tiles, east=True):
		Block.__init__(self, tower, frame, name, tiles, east)
		self.type = OVERSWITCH
		self.turnouts = []

	def SetRoute(self, route):
		self.route = [x for x in route]
		print("Block %s set route to %s" % (self.name, str(self.route)))
		self.Draw()

	def AddTurnout(self, turnout):
		self.turnouts.append(turnout)

	def Draw(self):
		for t, screen, pos, revflag in self.tiles:
			if pos in self.route:
				stat = self.status
			else:
				stat = EMPTY
			bmp = t.getBmp(stat, self.east, revflag)
			self.frame.DrawTile(screen, pos, bmp)

		for t in self.turnouts:
			t.Draw()





