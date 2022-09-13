from turnout import Turnout
from constants import EMPTY, OCCUPIED, CLEARED, BLOCK, OVERSWITCH

class Route:
	def __init__(self, screen, name, blkw, pos, blke):
		self.screen = screen
		self.name = name
		self.blkw = blkw
		self.pos = [x for x in pos]
		self.blke = blke

	def GetName(self):
		return self.name

	def Contains(self, screen, pos):
		if screen != self.screen:
			return False
		return pos in self.pos

	def GetStatus(self, blk, frame):
		return frame.GetBlockStatus(self.blke if blk.east else self.blkw)

	def rprint(self):
		print("%s: %s => %s => %s" % (self.name, self.blkw, str(self.pos), self.blke))


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
		self.routes = []

	def determineStatus(self):
		self.status = OCCUPIED if self.occupied else CLEARED if self.cleared else EMPTY

	def GetBlockType(self):
		return self.type

	def GetName(self):
		return self.name

	def GetStatus(self):
		self.determineStatus()
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

	def SetRoutes(self, routes):
		self.routes = [x for x in routes]
		self.rtNames = [rte.GetName() for rte in self.routes]
		self.Draw()

	def GetRoutes(self):
		return self.routes

	def HasRoute(self, rtName):
		return rtName in self.rtNames

	def AddTurnout(self, turnout):
		self.turnouts.append(turnout)

	def GetStatusFromRoute(self, screen, pos):
		inRoute = None
		for rte in self.routes:
			if rte.Contains(screen, pos):
				inRoute = rte
				break
		if inRoute is None:
			return EMPTY

		return inRoute.GetStatus(self, self.frame)


	def Draw(self):
		self.cleared = False
		self.occupied = False
		for t, screen, pos, revflag in self.tiles:
			stat = self.GetStatusFromRoute(screen, pos)
			if stat == OCCUPIED:
				print("Draw sets occupied")
				self.occupied = True
			elif stat == CLEARED:
				print("draw sets cleared")
				self.cleared = True
			bmp = t.getBmp(stat, self.east, revflag)
			self.frame.DrawTile(screen, pos, bmp)

		for t in self.turnouts:
			t.Draw()





