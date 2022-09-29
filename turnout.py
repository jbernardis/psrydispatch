from constants import NORMAL, REVERSE, EMPTY
import traceback

class Turnout:
	def __init__(self, district, frame, name, screen, tiles, block, pos):
		self.district = district
		self.frame = frame
		self.name = name
		self.screen = screen
		self.tiles = tiles
		self.pos = pos
		self.block = block
		self.normal = True
		self.routeControlled = False
		self.pairedTurnout = None
		self.controllingTurnout = None
		self.opposite = False

	def Draw(self, blockstat=None):
		tostat = NORMAL if self.normal else REVERSE
		blkstat = blockstat if blockstat is not None else self.block.GetStatus()
		east = self.block.GetEast()
		bmp = self.tiles.getBmp(tostat, blkstat, east)
		self.frame.DrawTile(self.screen, self.pos, bmp)

	def SetRouteControl(self, flag=True):
		self.routeControlled = flag

	def IsRouteControlled(self):
		return self.routeControlled

	def SetPairedTurnout(self, turnout, opposite=False):
		self.pairedTurnout = turnout
		turnout.SetControlledBy(self, opposite)

	def SetControlledBy(self, turnout, opposite=False):
		self.controllingTurnout = turnout
		self.opposite = opposite

	def GetControlledBy(self):
		if self.controllingTurnout:
			return self.controllingTurnout
		else:
			return self

	def Changeable(self):
		return self.block.GetStatus() == EMPTY

	def IsNormal(self):
		return self.normal

	def IsReverse(self):
		return not self.normal

	def SetReverse(self, refresh=False):
		if not self.normal:
			return False

		if not self.Changeable():
			# cant change a turnout in busy block
			return False
		
		self.normal = False
		if self.pairedTurnout is not None:
			if self.opposite:
				self.pairedTurnout.SetNormal(refresh)
			else:
				self.pairedTurnout.SetReverse(refresh)

		blocks = [ blk for blk in self.district.osTurnouts if self.name in self.district.osTurnouts[blk]]
		self.district.DetermineRoute(blocks)

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
			if self.opposite:
				self.pairedTurnout.SetReverse(refresh)
			else:
				self.pairedTurnout.SetNormal(refresh)
		

		blocks = [ blk for blk in self.district.osTurnouts if self.name in self.district.osTurnouts[blk]]
		self.district.DetermineRoute(blocks)
		if refresh:
			self.Draw()
		return True

	def GetName(self):
		return self.name

	def GetDistrict(self):
		return self.district

	def GetScreen(self):
		return self.screen

	def GetBlock(self):
		return self.block

	def GetPos(self):
		return self.pos

	def IsNormal(self):
		return self.normal

	def IsReverse(self):
		return not self.normal

