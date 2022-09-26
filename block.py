from turnout import Turnout
from constants import EMPTY, OCCUPIED, CLEARED, BLOCK, OVERSWITCH, STOPPINGBLOCK, RED

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

	def GetDescription(self):
		return "%s <=> %s" % (self.blkin, self.blkout)

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
	def __init__(self, district, frame, name, tiles, east=True):
		self.district = district
		self.frame = frame
		self.name = name
		self.type = BLOCK
		self.tiles = tiles # [Tile, screen, coordinates, reverseindication]
		self.east = east
		self.defaultEast = east
		self.occupied = False
		self.cleared = False
		self.train = None
		self.trainLoc = []
		self.sbEast = None
		self.sbWest = None
		self.determineStatus()

	def SetTrain(self, train):
		self.train = train

	def AddStoppingBlock(self, tiles, eastend=False):
		if eastend:
			self.sbEast = StoppingBlock(self, tiles, eastend)
		else:
			self.sbWest = StoppingBlock(self, tiles, eastend)
		self.determineStatus()

	def AddTrainLoc(self, screen, loc):
		self.trainLoc.append([screen, loc])

	def DrawTrain(self):
		if self.train is None:
			return

		if self.occupied:
			for screen, loc in self.trainLoc:
				self.frame.DrawText(screen, loc, self.train.GetName())

	def Reset(self):
		self.east = self.defaultEast

	def determineStatus(self):
		self.status = OCCUPIED if self.occupied else CLEARED if self.cleared else EMPTY

	def GetBlockType(self):
		return self.type

	def GetName(self):
		return self.name

	def GetDistrict(self):
		return self.district

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
		if self.cleared or self.occupied:
			return True
		for b in [self.sbEast, self.sbWest]:
			if b and b.IsBusy():
				return True
		return False

	def IsCleared(self):
		return self.cleared

	def IsOccupied(self):
		return self.occupied

	def Draw(self):
		for t, screen, pos, revflag in self.tiles:
			bmp = t.getBmp(self.status, self.east, revflag)
			self.frame.DrawTile(screen, pos, bmp)

	def SetOccupied(self, occupied=True, blockend=None, refresh=False):
		if blockend  in ["E", "W"]:
			b = self.sbEast if blockend == "E" else self.sbWest
			b.SetOccupied(occupied, None, refresh)
			return

		if self.occupied == occupied:
			# already in the requested state
			return

		self.occupied = occupied
		if self.occupied:
			self.cleared = False

		self.determineStatus()
		if self.status == EMPTY:
			self.Reset()

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

		for b in [self.sbEast, self.sbWest]:
			if b is not None:
				b.SetCleared(cleared, refresh)

class StoppingBlock (Block):
	def __init__(self, block, tiles, eastend):
		self.block = block
		self.tiles = tiles
		self.eastend = eastend
		self.type = STOPPINGBLOCK
		self.frame = self.block.frame
		self.occupied = False
		self.cleared = False
		self.determineStatus()

	def Draw(self):
		self.east = self.block.east
		Block.Draw(self)

	def determineStatus(self):
		self.status = OCCUPIED if self.occupied else CLEARED if self.cleared else EMPTY

	def getStatus(self):
		return self.status

	def Reset(self):
		pass

	def GetEast(self):
		return self.block.east

	def IsReversed(self):
		return self.block.east != self.block.defaultEast

	def IsBusy(self):
		return self.cleared or self.occupied

	def GetDistrict(self):
		return None

	def GetName(self):
		return self.block.GetName() + "." + "E" if self.eastend else "W"

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
	def __init__(self, district, frame, name, tiles, east=True):
		Block.__init__(self, district, frame, name, tiles, east)
		self.type = OVERSWITCH
		self.turnouts = []
		self.route = None
		self.rtName = ""
		self.entrySignal = None

	def SetRoute(self, route):
		self.route = route
		self.rtName = self.route.GetName()
		#route.rprint()
		self.Draw()

	def GetRoute(self):
		return self.route

	def GetRouteName(self):
		return self.rtName

	def SetEntrySignal(self, sig):
		self.entrySignal = sig

	def GetEntrySignal(self):
		return self.entrySignal

	def HasRoute(self, rtName):
		return rtName == self.rtName

	def AddTurnout(self, turnout):
		self.turnouts.append(turnout)

	def SetOccupied(self, occupied=True, blockend=None, refresh=False):
		Block.SetOccupied(self, occupied, blockend, refresh)
		if occupied:
			if self.entrySignal is not None:
				signm = self.entrySignal.GetName()
				self.frame.Request({"signal": { "name": signm, "state": RED }})
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





