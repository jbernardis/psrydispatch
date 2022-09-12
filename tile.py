import os

from bitmaps import BitMaps
from constants import EMPTY, OCCUPIED, CLEARED, NORMAL, REVERSE

class Tile:
	def __init__(self, name, bmps):
		self.name = name
		self.bmps = bmps

	def getBmp(self, status, east, revflag):
		if status == OCCUPIED:
			return self.bmps["red"]

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

class TurnoutTile:
	def __init__(self, name, nbmps, rbmps):
		self.name = name
		self.nbmps = nbmps
		self.rbmps = rbmps

	def getBmp(self, tostat, blkstat, east):
		if tostat == NORMAL:
			bmps = self.nbmps
		else:
			bmps = self.rbmps

		if blkstat == OCCUPIED:
			return bmps["red"]

		if blkstat == CLEARED:
			if east:
				k = "green-right"
			else:
				k = "green-left"
			try:
				bmp = bmps[k]
			except KeyError:
				bmp = bmps["green"]
			return bmp

		return bmps["white"]


class SignalTile:
	def __init__(self, name, bmps):
		self.name = name
		self.bmps = bmps

	def getBmp(self, sig):
		if sig.aspect == 0:
			return self.bmps["red"]
		elif sig.aspect == 1:
			return self.bmps["green"]


def loadTiles(bitmaps):
	b = bitmaps.track

	tiles = {}
	tiles["horiz"] = Tile("horiz", {
		"white": b.straight.normal,
		"green": b.straight.routed,
		"green-right": b.straight.rightrouted,
		"green-left": b.straight.leftrouted,
		"red": b.straight.occupied})
	tiles["horiznc"] = Tile("horiz", {
		"white": b.straight.normal,
		"green": b.straight.routed,
		"red": b.straight.occupied})
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

	turnouts = {}
	turnouts["torightleft"] = TurnoutTile("torightleft", 
		{
			"white": b.torightleft.normal.normal,
			"green": b.torightleft.normal.routed,
			"red": b.torightleft.normal.occupied
		},
		{
			"white": b.torightleft.reversed.normal,
			"green": b.torightleft.reversed.routed,
			"red": b.torightleft.reversed.occupied
		}
	)

	turnouts["torightright"] = TurnoutTile("torightright", 
		{
			"white": b.torightright.normal.normal,
			"green": b.torightright.normal.routed,
			"red": b.torightright.normal.occupied
		},
		{
			"white": b.torightright.reversed.normal,
			"green": b.torightright.reversed.routed,
			"red": b.torightright.reversed.occupied
		}
	)

	turnouts["torightup"] = TurnoutTile("torightup", 
		{
			"white": b.torightup.normal.normal,
			"green": b.torightup.normal.routed,
			"red": b.torightup.normal.occupied
		},
		{
			"white": b.torightup.reversed.normal,
			"green": b.torightup.reversed.routed,
			"red": b.torightup.reversed.occupied
		}
	)

	turnouts["toleftleft"] = TurnoutTile("toleftleft", 
		{
			"white": b.toleftleft.normal.normal,
			"green": b.toleftleft.normal.routed,
			"red": b.toleftleft.normal.occupied
		},
		{
			"white": b.toleftleft.reversed.normal,
			"green": b.toleftleft.reversed.routed,
			"red": b.toleftleft.reversed.occupied
		}
	)

	turnouts["toleftleftinv"] = TurnoutTile("toleftleftinv", 
		{
			"white": b.toleftleft.reversed.normal,
			"green": b.toleftleft.reversed.routed,
			"red": b.toleftleft.reversed.occupied
		},
		{
			"white": b.toleftleft.normal.normal,
			"green": b.toleftleft.normal.routed,
			"red": b.toleftleft.normal.occupied
		}
	)
	
	turnouts["toleftright"] = TurnoutTile("toleftright", 
		{
			"white": b.toleftright.normal.normal,
			"green": b.toleftright.normal.routed,
			"red": b.toleftright.normal.occupied
		},
		{
			"white": b.toleftright.reversed.normal,
			"green": b.toleftright.reversed.routed,
			"red": b.toleftright.reversed.occupied
		}
	)

	b = bitmaps.signals
	signals = {}
	signals["left"] = SignalTile("C11", 
		{
			"green": b.east.green,
			"red": b.east.red
		})
	signals["right"] = SignalTile("C12", 
		{
			"green": b.west.green,
			"red": b.west.red
		})

	return tiles, turnouts, signals
