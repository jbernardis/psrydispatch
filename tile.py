import os

from bitmaps import BitMaps
from constants import EMPTY, OCCUPIED, CLEARED, NORMAL, REVERSE, RED, GREEN, STOP

class Tile:
	def __init__(self, name, bmps):
		self.name = name
		self.bmps = bmps

	def getBmp(self, status, east, revflag):
		if status == OCCUPIED:
			if east:
				k = "red-left" if revflag else "red-right"
			else:
				k = "red-right" if revflag else "red-left"
			try:
				bmp = self.bmps[k]
			except KeyError:
				bmp = self.bmps["red"]
			return bmp

		if status == CLEARED:
			if east:
				k = "green-left" if revflag else "green-right"
			else:
				k = "green-right" if revflag else "green-left"
			try:
				bmp = self.bmps[k]
			except KeyError:
				bmp = self.bmps["green"]
			return bmp

		return self.bmps["white"]

class MiscTile:
	def __init__(self, name, bmps):
		self.name = name
		self.bmps = bmps

	def getBmp(self, status, tag):
		prefix = ""
		if status == OCCUPIED:
			prefix = "red-"
		elif status == CLEARED:
			prefix = "green-"
		elif status == EMPTY:
			prefix = "white-"

		try:
			bmp = self.bmps[prefix+tag]
		except:
			bmp = self.bmps[tag]
		return bmp


class TurnoutTile:
	def __init__(self, name, nbmps, rbmps):
		self.name = name
		self.nbmps = nbmps
		self.rbmps = rbmps

	def getBmp(self, tostat, blkstat, east, disabled):
		if tostat == NORMAL:
			bmps = self.nbmps
		else:
			bmps = self.rbmps

		if blkstat == OCCUPIED:
			if disabled:
				if "red-dis" in bmps:
					return bmps["red-dis"]
			return bmps["red"]

		if blkstat == CLEARED:
			if disabled:
				if "green-dis" in bmps:
					return bmps["green-dis"]
			return bmps["green"]

		if disabled:
			if "white-dis" in bmps:
				return bmps["white-dis"]
		return bmps["white"]

class SlipSwitchTile:
	def __init__(self, name, nnbmps, nrbmps, rnbmps, rrbmps):
		self.name = name
		self.nnbmps = nnbmps
		self.nrbmps = nrbmps
		self.rnbmps = rnbmps
		self.rrbmps = rrbmps


	def getBmp(self, tostat, blkstat, disabled):
		if tostat == [NORMAL, NORMAL]:
			bmps = self.nnbmps
		elif tostat == [NORMAL, REVERSE]:
			bmps = self.nrbmps
		elif tostat == [REVERSE, NORMAL]:
			bmps = self.rnbmps
		else: # tostat == [REVERSE, REVERSE]
			bmps = self.rrbmps

		if blkstat == OCCUPIED:
			if disabled:
				if "red-dis" in bmps:
					return bmps["red-dis"]
			return bmps["red"]

		if blkstat == CLEARED:
			if disabled:
				if "green-dis" in bmps:
					return bmps["green-dis"]
			return bmps["green"]

		if disabled:
			if "white-dis" in bmps:
				return bmps["white-dis"]
		return bmps["white"]


class SignalTile:
	def __init__(self, name, bmps):
		self.name = name
		self.bmps = bmps

	def getBmp(self, sig):
		if sig.aspect == STOP:
			return self.bmps["red"]
		elif sig.aspect == GREEN:
			return self.bmps["green"]
		else:
			return self.bmps["green"]


def loadTiles(bitmaps):
	b = bitmaps.track

	tiles = {}
	tiles["horiz"] = Tile("horiz", {
		"white": b.straight.normal,
		"green": b.straight.routed,
		"green-right": b.straight.rightrouted,
		"green-left": b.straight.leftrouted,
		"red-right": b.straight.rightoccupied,
		"red-left": b.straight.leftoccupied,
		"red": b.straight.occupied})
	tiles["horiznc"] = Tile("horiz", {
		"white": b.straight.normal,
		"green": b.straight.routed,
		"red": b.straight.occupied})
	tiles["houtline"] = Tile("houtline", {
		"white": b.straightoutline.normal,
		"green": b.straightoutline.routed,
		"red": b.straightoutline.occupied})
	tiles["vertical"] = Tile("vertical", {
		"white": b.vertical.normal,
		"green": b.vertical.routed,
		"green-right": b.vertical.uprouted,
		"green-left": b.vertical.downrouted,
		"red-right": b.vertical.upoccupied,
		"red-left": b.vertical.downoccupied,
		"red": b.vertical.occupied})
	tiles["verticalnc"] = Tile("vertical", {
		"white": b.vertical.normal,
		"green": b.vertical.routed,
		"red": b.vertical.occupied})
	tiles["eobleft"] = Tile("eobleft", {
		"white": b.eobleft.normal,
		"green": b.eobleft.routed,
		"red": b.eobleft.occupied})
	tiles["eobright"] = Tile("eobright", {
		"white": b.eobright.normal,
		"green": b.eobright.routed,
		"red": b.eobright.occupied})
	tiles["diagleft"] = Tile("diagleft", {
		"white": b.diagleft.normal,
		"green": b.diagleft.routed,
		"red": b.diagleft.occupied})
	tiles["diagright"] = Tile("diagright", {
		"white": b.diagright.normal,
		"green": b.diagright.routed,
		"red": b.diagright.occupied})
	tiles["turnleftright"] = Tile("turnleftright", {
		"white": b.turnleftright.normal,
		"green": b.turnleftright.routed,
		"red": b.turnleftright.occupied})
	tiles["turnleftleft"] = Tile("turnleftleft", {
		"white": b.turnleftleft.normal,
		"green": b.turnleftleft.routed,
		"red": b.turnleftleft.occupied})
	tiles["turnrightleft"] = Tile("turnrightleft", {
		"white": b.turnrightleft.normal,
		"green": b.turnrightleft.routed,
		"red": b.turnrightleft.occupied})
	tiles["turnrightright"] = Tile("turnrightright", {
		"white": b.turnrightright.normal,
		"green": b.turnrightright.routed,
		"red": b.turnrightright.occupied})

	tiles["turnrightup"] = Tile("turnrightup", {
		"white": b.turnrightup.normal,
		"green": b.turnrightup.routed,
		"red": b.turnrightup.occupied})

	tiles["turnleftdown"] = Tile("turnleftdown", {
		"white": b.turnleftdown.normal,
		"green": b.turnleftdown.routed,
		"red": b.turnleftdown.occupied})

	turnouts = {}
	turnouts["torightleft"] = TurnoutTile("torightleft", 
		{
			"white": b.torightleft.normal.normal,
			"green": b.torightleft.normal.routed,
			"red": b.torightleft.normal.occupied,
			"white-dis": b.torightleft.normal.normaldis,
			"green-dis": b.torightleft.normal.routeddis,
			"red-dis": b.torightleft.normal.occupieddis
		},
		{
			"white": b.torightleft.reversed.normal,
			"green": b.torightleft.reversed.routed,
			"red": b.torightleft.reversed.occupied,
			"white-dis": b.torightleft.reversed.normaldis,
			"green-dis": b.torightleft.reversed.routeddis,
			"red-dis": b.torightleft.reversed.occupieddis
		}
	)

	turnouts["torightright"] = TurnoutTile("torightright", 
		{
			"white": b.torightright.normal.normal,
			"green": b.torightright.normal.routed,
			"red": b.torightright.normal.occupied,
			"white-dis": b.torightright.normal.normaldis,
			"green-dis": b.torightright.normal.routeddis,
			"red-dis": b.torightright.normal.occupieddis
		},
		{
			"white": b.torightright.reversed.normal,
			"green": b.torightright.reversed.routed,
			"red": b.torightright.reversed.occupied,
			"white-dis": b.torightright.reversed.normaldis,
			"green-dis": b.torightright.reversed.routeddis,
			"red-dis": b.torightright.reversed.occupieddis
		}
	)

	turnouts["torightup"] = TurnoutTile("torightup", 
		{
			"white": b.torightup.normal.normal,
			"green": b.torightup.normal.routed,
			"red": b.torightup.normal.occupied,
			"white-dis": b.torightup.normal.normaldis,
			"green-dis": b.torightup.normal.routeddis,
			"red-dis": b.torightup.normal.occupieddis
		},
		{
			"white": b.torightup.reversed.normal,
			"green": b.torightup.reversed.routed,
			"red": b.torightup.reversed.occupied,
			"white-dis": b.torightup.reversed.normaldis,
			"green-dis": b.torightup.reversed.routeddis,
			"red-dis": b.torightup.reversed.occupieddis
		}
	)

	turnouts["toleftup"] = TurnoutTile("toleftup", 
		{
			"white": b.toleftup.normal.normal,
			"green": b.toleftup.normal.routed,
			"red": b.toleftup.normal.occupied,
			"white-dis": b.toleftup.normal.normaldis,
			"green-dis": b.toleftup.normal.routeddis,
			"red=dis": b.toleftup.normal.occupieddis
		},
		{
			"white": b.toleftup.reversed.normal,
			"green": b.toleftup.reversed.routed,
			"red": b.toleftup.reversed.occupied,
			"white-dis": b.toleftup.reversed.normaldis,
			"green-dis": b.toleftup.reversed.routeddis,
			"red-dis": b.toleftup.reversed.occupieddis
		}
	)

	turnouts["toleftupinv"] = TurnoutTile("toleftup", 
		{
			"white": b.toleftup.reversed.normal,
			"green": b.toleftup.reversed.routed,
			"red": b.toleftup.reversed.occupied,
			"white-dis": b.toleftup.reversed.normaldis,
			"green-dis": b.toleftup.reversed.routeddis,
			"red-dis": b.toleftup.reversed.occupieddis
		},
		{
			"white": b.toleftup.normal.normal,
			"green": b.toleftup.normal.routed,
			"red": b.toleftup.normal.occupied,
			"white-dis": b.toleftup.normal.normaldis,
			"green-dis": b.toleftup.normal.routeddis,
			"red-dis": b.toleftup.normal.occupieddis
		}
	)

	turnouts["torightupinv"] = TurnoutTile("torightup", 
		{
			"white": b.torightup.reversed.normal,
			"green": b.torightup.reversed.routed,
			"red": b.torightup.reversed.occupied,
			"white-dis": b.torightup.reversed.normaldis,
			"green-dis": b.torightup.reversed.routeddis,
			"red-dis": b.torightup.reversed.occupieddis
		},
		{
			"white": b.torightup.normal.normal,
			"green": b.torightup.normal.routed,
			"red": b.torightup.normal.occupied,
			"white-dis": b.torightup.normal.normaldis,
			"green-dis": b.torightup.normal.routeddis,
			"red-dis": b.torightup.normal.occupieddis
		}
	)

	turnouts["torightdown"] = TurnoutTile("torightdown", 
		{
			"white": b.torightdown.normal.normal,
			"green": b.torightdown.normal.routed,
			"red": b.torightdown.normal.occupied,
			"white-dis": b.torightdown.normal.normaldis,
			"green-dis": b.torightdown.normal.routeddis,
			"red-dis": b.torightdown.normal.occupieddis
		},
		{
			"white": b.torightdown.reversed.normal,
			"green": b.torightdown.reversed.routed,
			"red": b.torightdown.reversed.occupied,
			"white-dis": b.torightdown.reversed.normaldis,
			"green-dis": b.torightdown.reversed.routeddis,
			"red-dis": b.torightdown.reversed.occupieddis
		}
	)

	turnouts["toleftleft"] = TurnoutTile("toleftleft", 
		{
			"white": b.toleftleft.normal.normal,
			"green": b.toleftleft.normal.routed,
			"red": b.toleftleft.normal.occupied,
			"white-dis": b.toleftleft.normal.normaldis,
			"green-dis": b.toleftleft.normal.routeddis,
			"red-dis": b.toleftleft.normal.occupieddis
		},
		{
			"white": b.toleftleft.reversed.normal,
			"green": b.toleftleft.reversed.routed,
			"red": b.toleftleft.reversed.occupied,
			"white-dis": b.toleftleft.reversed.normaldis,
			"green-dis": b.toleftleft.reversed.routeddis,
			"red-dis": b.toleftleft.reversed.occupieddis
		}
	)

	turnouts["toleftleftinv"] = TurnoutTile("toleftleftinv", 
		{
			"white": b.toleftleft.reversed.normal,
			"green": b.toleftleft.reversed.routed,
			"red": b.toleftleft.reversed.occupied,
			"white-dis": b.toleftleft.reversed.normaldis,
			"green-dis": b.toleftleft.reversed.routeddis,
			"red-dis": b.toleftleft.reversed.occupieddis
		},
		{
			"white": b.toleftleft.normal.normal,
			"green": b.toleftleft.normal.routed,
			"red": b.toleftleft.normal.occupied,
			"white-dis": b.toleftleft.normal.normaldis,
			"green-dis": b.toleftleft.normal.routeddis,
			"red-dis": b.toleftleft.normal.occupieddis
		}
	)
	
	turnouts["toleftright"] = TurnoutTile("toleftright", 
		{
			"white": b.toleftright.normal.normal,
			"green": b.toleftright.normal.routed,
			"red": b.toleftright.normal.occupied,
			"white-dis": b.toleftright.normal.normaldis,
			"green-dis": b.toleftright.normal.routeddis,
			"red-dis": b.toleftright.normal.occupieddis
		},
		{
			"white": b.toleftright.reversed.normal,
			"green": b.toleftright.reversed.routed,
			"red": b.toleftright.reversed.occupied,
			"white-dis": b.toleftright.reversed.normaldis,
			"green-dis": b.toleftright.reversed.routeddis,
			"red-dis": b.toleftright.reversed.occupieddis
		}
	)
	
	turnouts["toleftdown"] = TurnoutTile("toleftdown", 
		{
			"white": b.toleftdown.normal.normal,
			"green": b.toleftdown.normal.routed,
			"red": b.toleftdown.normal.occupied,
			"white-dis": b.toleftdown.normal.normaldis,
			"green-dis": b.toleftdown.normal.routeddis,
			"red-dis": b.toleftdown.normal.occupieddis
		},
		{
			"white": b.toleftdown.reversed.normal,
			"green": b.toleftdown.reversed.routed,
			"red": b.toleftdown.reversed.occupied,
			"white-dis": b.toleftdown.reversed.normaldis,
			"green-dis": b.toleftdown.reversed.routeddis,
			"red-dis": b.toleftdown.reversed.occupieddis
		}
	)
	
	turnouts["toleftdowninv"] = TurnoutTile("toleftdowninv", 
		{
			"white": b.toleftdown.reversed.normal,
			"green": b.toleftdown.reversed.routed,
			"red": b.toleftdown.reversed.occupied,
			"white-dis": b.toleftdown.reversed.normaldis,
			"green-dis": b.toleftdown.reversed.routeddis,
			"red-dis": b.toleftdown.reversed.occupieddis
		},
		{
			"white": b.toleftdown.normal.normal,
			"green": b.toleftdown.normal.routed,
			"red": b.toleftdown.normal.occupied,
			"white-dis": b.toleftdown.normal.normaldis,
			"green-dis": b.toleftdown.normal.routeddis,
			"red-dis": b.toleftdown.normal.occupieddis
		}
	)

	slipswitches = {}
	turnouts["ssleft"] = SlipSwitchTile("ssleft",
		{ # NN
			"white": b.slipleft.nn.normal,
			"green": b.slipleft.nn.routed,
			"red":   b.slipleft.nn.occupied,
			"white-dis": b.slipleft.nn.normaldis,
			"green-dis": b.slipleft.nn.routeddis,
			"red-dis":   b.slipleft.nn.occupieddis
		},
		{ # NR
			"white": b.slipleft.nr.normal,
			"green": b.slipleft.nr.routed,
			"red":   b.slipleft.nr.occupied,
			"white-dis": b.slipleft.nr.normaldis,
			"green-dis": b.slipleft.nr.routeddis,
			"red-dis":   b.slipleft.nr.occupieddis
		},
		{ # RN
			"white": b.slipleft.rn.normal,
			"green": b.slipleft.rn.routed,
			"red":   b.slipleft.rn.occupied,
			"white-dis": b.slipleft.rn.normaldis,
			"green-dis": b.slipleft.rn.routeddis,
			"red-dis":   b.slipleft.rn.occupieddis
		},
		{ # RR
			"white": b.slipleft.rr.normal,
			"green": b.slipleft.rr.routed,
			"red":   b.slipleft.rr.occupied,
			"white-dis": b.slipleft.rr.normaldis,
			"green-dis": b.slipleft.rr.routeddis,
			"red-dis":   b.slipleft.rr.occupieddis
		}

	)

	bmisc = bitmaps.misc
	misctiles = {}
	misctiles["crossing"] = MiscTile("crossing",
		{
			"white-diagright": b.diagright.normal,
			"green-diagright": b.diagright.routed,
			"red-diagright": b.diagright.occupied,
			"white-diagleft": b.diagleft.normal,
			"green-diagleft": b.diagleft.routed,
			"red-diagleft": b.diagleft.occupied,
			"cross": bmisc.cross
		})
	misctiles["handdown"] = MiscTile("handdown",
		{
			"locked" : bmisc.downlocked,
			"unlocked" : bmisc.downunlocked
		})
	misctiles["handup"] = MiscTile("handup",
		{
			"locked" : bmisc.uplocked,
			"unlocked" : bmisc.upunlocked,
		})


	b = bitmaps.signals
	signals = {}
	signals["left"] = SignalTile("C11", 
		{
			"green": b.left.green,
			"red": b.left.red
		})
	signals["right"] = SignalTile("C12", 
		{
			"green": b.right.green,
			"red": b.right.red
		})

	return tiles, turnouts, slipswitches, signals, misctiles
