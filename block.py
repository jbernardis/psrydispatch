from turnout import Turnout
from constants import EMPTY, OCCUPIED, CLEARED, BLOCK, OVERSWITCH, STOPPINGBLOCK, RED

class Route:
	def __init__(self, screen, osblk, name, blkin, pos, blkout, rtype):
		self.screen = screen
		self.name = name
		self.osblk = osblk
		self.blkin = blkin
		self.pos = [x for x in pos]
		self.blkout = blkout
		self.rtype = [x for x in rtype]

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

	def GetRouteType(self, reverse=False):
		if self.osblk.east:
			return self.rtype[1] if reverse else self.rtype[0]
		else:
			return self.rtype[0] if reverse else self.rtype[1]

	def GetExitBlock(self, reverse=False):
		if self.osblk.IsReversed():
			return self.blkout if reverse else self.blkin
		else:
			return self.blkin if reverse else self.blkout

	def GetEntryBlock(self, reverse=False):
		if self.osblk.IsReversed():
			return self.blkin if reverse else self.blkout
		else:
			return self.blkout if reverse else self.blkin

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
		self.turnouts = []
		self.locks = []
		self.train = None
		self.trainLoc = []
		self.blkEast = None
		self.blkWest = None
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

	def GetTrain(self):
		return self.train

	def GetTrainLoc(self):
		return self.trainLoc

	def AddLock(self, lk):
		self.locks.append(lk)

	def AreLocksSet(self):
		for lk in self.locks:
			if lk.GetValue():
				return True
		return False

	def DrawTrain(self):
		if len(self.trainLoc) == 0:
			return

		if self.train is None:
			trainID = "???"
		else:
			trainID = self.train.GetIDString()

		for screen, loc in self.trainLoc:
			if self.occupied:
				self.frame.DrawText(screen, loc, trainID)
			else:
				self.frame.ClearText(screen, loc)

	def DrawTurnouts(self):
		pass

	def Reset(self):
		self.east = self.defaultEast

	def SetNextBlockEast(self, blk):
		#print("Block %s: next east block is %s" % (self.GetName(), blk.GetName()))
		self.blkEast = blk

	def SetNextBlockWest(self, blk):
		#print("Block %s: next west block is %s" % (self.GetName(), blk.GetName()))
		self.blkWest = blk

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
		for b in [self.sbEast, self.sbWest]:
			if b is not None:
				b.Draw()
		for t in self.turnouts:
			t.Draw(self.status, self.east)

		self.district.DrawOthers(self)
		self.DrawTrain()

	def AddTurnout(self, turnout):
		self.turnouts.append(turnout)

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
			self.SetTrain(self.IdentifyTrain())
		else:
			for b in [self.sbEast, self.sbWest]:
				if b is not None:
					b.SetCleared(False, refresh)
			self.SetTrain(None)

		self.determineStatus()
		if self.status == EMPTY:
			self.Reset()

		if refresh:
			self.Draw()

	def IdentifyTrain(self):
		if self.east:
			if self.blkWest:
				return self.blkWest.GetTrain()
			else:
				return None
		else:
			if self.blkEast:
				return self.blkEast.GetTrain()
			else:
				return None

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
		for t, screen, pos, revflag in self.tiles:
			bmp = t.getBmp(self.status, self.east, revflag)
			self.frame.DrawTile(screen, pos, bmp)

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
		self.route = None
		self.rtName = ""
		self.entrySignal = None

	def SetRoute(self, route):
		self.route = route
		if route is None:
			self.rtName = "<None>"
			return

		self.route.rprint()
			
		self.rtName = self.route.GetName()
		entryBlkName = self.route.GetEntryBlock()
		entryBlk = self.frame.GetBlockByName(entryBlkName)
		exitBlkName = self.route.GetExitBlock()
		exitBlk = self.frame.GetBlockByName(exitBlkName)

		if not entryBlk:
			print("could not determine entry block for %s/%s from name %s" % (self.name, self.rtName, entryBlkName))
		if not exitBlk:
			print("could not determine exit block for %s/%s from name %s" % (self.name, self.rtName, exitBlkName))
		if self.east:
			if entryBlk:
				entryBlk.SetNextBlockEast(self)
			self.SetNextBlockWest(entryBlk)
			if exitBlk:
				exitBlk.SetNextBlockWest(self)
			self.SetNextBlockEast(exitBlk)
		else:
			if entryBlk:
				entryBlk.SetNextBlockWest(self)
			self.SetNextBlockEast(entryBlk)
			if exitBlk:
				exitBlk.SetNextBlockEast(self)
			self.SetNextBlockWest(exitBlk)
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

	def SetOccupied(self, occupied=True, blockend=None, refresh=False):
		Block.SetOccupied(self, occupied, blockend, refresh)
		if occupied:
			if self.entrySignal is not None:
				signm = self.entrySignal.GetName()
				self.frame.Request({"signal": { "name": signm, "aspect": RED }})
				self.entrySignal = None

	def GetTileInRoute(self, screen, pos):
		if self.route is None:
			return True, EMPTY
		elif self.route.Contains(screen, pos):
			return True, self.status
		
		return False, EMPTY

	def Draw(self):
		for t, screen, pos, revflag in self.tiles:
			draw, stat = self.GetTileInRoute(screen, pos)
			if draw:
				bmp = t.getBmp(stat, self.east, revflag)
				self.frame.DrawTile(screen, pos, bmp)

		for t in self.turnouts:
			draw, stat = self.GetTileInRoute(t.GetScreen(), t.GetPos())
			if draw:
				t.Draw(stat, self.east)

		self.district.DrawOthers(self)

	def DrawTurnouts(self):
		for t in self.turnouts:
			t.Draw(EMPTY, self.east)
