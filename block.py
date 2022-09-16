from turnout import Turnout
from constants import EMPTY, OCCUPIED, CLEARED, BLOCK, OVERSWITCH, RED

class Route:
	def __init__(self, screen, osblk, name, blkin, pos, blkout):
		self.screen = screen
		self.name = name
		self.osblk = osblk
		self.blkin = blkin
		self.pos = [x for x in pos]
		self.blkout = blkout

	def GetName(self):
		return self.name

	def Contains(self, screen, pos):
		if screen != self.screen:
			return False
		return pos in self.pos

	def GetStatus(self):
		return self.osblk.GetStatus()

	def GetExitBlock(self):
		if self.osblk.IsReversed():
			return self.blkin
		else:
			return self.blkout

	def rprint(self):
		print("%s: (%s) %s => %s => %s" % (self.name, self.osblk.GetName(), self.blkin, str(self.pos), self.blkout))


class Block:
	def __init__(self, tower, frame, name, tiles, east=True):
		self.tower = tower
		self.frame = frame
		self.name = name
		self.type = BLOCK
		self.tiles = tiles # [Tile, screen, coordinates, reverseindication]
		self.east = east
		self.defaultEast = east
		self.occupied = False
		self.cleared = False
		self.determineStatus()

	def Reset(self):
		self.east = self.defaultEast

	def determineStatus(self):
		self.status = OCCUPIED if self.occupied else CLEARED if self.cleared else EMPTY

	def GetBlockType(self):
		return self.type

	def GetName(self):
		return self.name

	def GetTower(self):
		return self.tower

	def GetStatus(self):
		self.determineStatus()
		return self.status

	def GetEast(self):
		return self.east

	def SetEast(self, east):
		self.east = east

	def IsReversed(self):
		return self.east != self.defaultEast

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
		if self.occupied:
			self.cleared = False

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
		self.route = None
		self.rtName = ""
		self.entrySignal = None

	def SetRoute(self, route):
		self.route = route
		self.rtName = self.route.GetName()
		route.rprint()
		self.Draw()

	def GetRoute(self):
		return self.route

	def GetRouteName(self):
		return self.rtName

	def SetEntrySignal(self, sig):
		self.entrySignal = sig

	def HasRoute(self, rtName):
		return rtName == self.rtName

	def AddTurnout(self, turnout):
		self.turnouts.append(turnout)

	def SetOccupied(self, occupied=True, refresh=False):
		Block.SetOccupied(self, occupied, refresh)
		if occupied:
			if self.entrySignal is not None:
				self.entrySignal.SetAspect(RED, refresh=True)
				self.entrySignal = None

	def Draw(self):
		for t, screen, pos, revflag in self.tiles:
			if self.route is None:
				stat = EMPTY
			elif self.route.Contains(screen, pos):
				stat = self.status
			else:
				stat = EMPTY
			bmp = t.getBmp(stat, self.east, revflag)
			self.frame.DrawTile(screen, pos, bmp)

		for t in self.turnouts:
			if self.route is None:
				stat = EMPTY
			elif self.route.Contains(t.GetScreen(), t.GetPos()):
				stat = self.status
			else:
				stat = EMPTY
			
			t.Draw(blockstat = stat)





