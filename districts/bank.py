from district import District

from block import Block, OverSwitch, Route
from turnout import Turnout, SlipSwitch
from signal import Signal
from button import Button
from handswitch import HandSwitch

from constants import RESTRICTING, MAIN, DIVERGING, SLOW, NORMAL, REVERSE, EMPTY, SLIPSWITCH, RegAspects, AdvAspects

class Bank (District):
	def __init__(self, name, frame, screen):
		District.__init__(self, name, frame, screen)

	def DetermineRoute(self, blocks):
		s17 = 'N' if self.turnouts["CSw17"].IsNormal() else 'R'
		s23 = 'N' if self.turnouts["CSw23"].IsNormal() else 'R'

		for block in blocks:
			bname = block.GetName()
			if bname == "BOSWW":
				if s23 == "N":
					block.SetRoute(self.routes["BRtB10B11"])
				else:
					block.SetRoute(self.routes["BRtB10B21"])

			elif bname == "BOSWE":
				if s23 == "N":
					block.SetRoute(self.routes["BRtB20B21"])
				else:
					block.SetRoute(None)
			
			elif bname == "BOSE":
				if s17 == "R":
					block.SetRoute(self.routes["BRtB11C13"])
				else:
					block.SetRoute(self.routes["BRtB21C13"])

	def DefineBlocks(self, tiles):
		self.blocks = {}
		self.osBlocks = {}

		self.blocks["B20"] = Block(self, self.frame, "B20",
			[
				(tiles["horiznc"], self.screen,      (45, 13), False),
				(tiles["horiz"],   self.screen,      (46, 13), False),
				(tiles["horiznc"], self.screen,      (47, 13), False),
				(tiles["horiz"],   self.screen,      (48, 13), False),
				(tiles["horiznc"], self.screen,      (49, 13), False),
			], True)
		self.blocks["B20"].AddStoppingBlock([
				(tiles["horiz"],   self.screen,      (50, 13), False),
				(tiles["horiznc"], self.screen,      (51, 13), False),
				(tiles["eobright"],self.screen,      (52, 13), False),
			], True)
		self.blocks["B20"].AddTrainLoc(self.screen, (47, 13))

		self.blocks["B11"] = Block(self, self.frame, "B11",
			[
				(tiles["horiznc"], self.screen,      (61, 11), False),
				(tiles["horiz"],   self.screen,      (62, 11), False),
				(tiles["horiz"],   self.screen,      (64, 11), False),
				(tiles["horiznc"], self.screen,      (65, 11), False),
				(tiles["eobright"],self.screen,      (67, 11), False),
			], False)
		self.blocks["B11"].AddStoppingBlock([
				(tiles["eobleft"], self.screen,      (58, 11), False),
				(tiles["horiznc"], self.screen,      (59, 11), False),
				(tiles["horiz"],   self.screen,      (60, 11), False),
			], False)
		self.blocks["B11"].AddTrainLoc(self.screen, (59, 11))

		self.blocks["B21"] = Block(self, self.frame, "B21",
			[
				(tiles["horiz"],   self.screen,      (60, 13), False),
				(tiles["horiznc"], self.screen,      (61, 13), False),
				(tiles["horiz"],   self.screen,      (62, 13), False),
				(tiles["horiz"],   self.screen,      (64, 13), False),
				(tiles["horiznc"], self.screen,      (65, 13), False),
			], True)
		self.blocks["B21"].AddStoppingBlock([
				(tiles["horiz"],   self.screen,      (66, 13), False),
				(tiles["eobright"],self.screen,      (67, 13), False),
			], True)
		self.blocks["B21"].AddStoppingBlock([
				(tiles["eobleft"], self.screen,      (58, 13), False),
				(tiles["horiznc"], self.screen,      (59, 13), False),
			], False)
		self.blocks["B21"].AddTrainLoc(self.screen, (59, 13))

		self.blocks["BOSWW"] = OverSwitch(self, self.frame, "BOSWW",
			[
				(tiles["eobleft"],  self.screen,     (53, 11), False),
				(tiles["horiznc"],  self.screen,     (55, 11), False),
				(tiles["horiz"],    self.screen,     (56, 11), False),
				(tiles["eobright"], self.screen,     (57, 11), False),
				(tiles["diagright"],self.screen,     (55, 12), False),
				(tiles["eobright"], self.screen,     (57, 13), False),
			], False)

		self.blocks["BOSWE"] = OverSwitch(self, self.frame, "BOSWE",
			[
				(tiles["eobleft"],  self.screen,     (53, 13), False),
				(tiles["horiz"],    self.screen,     (54, 13), False),
				(tiles["horiznc"],  self.screen,     (55, 13), False),
				(tiles["eobright"], self.screen,     (57, 13), False),
			], False)

		self.blocks["BOSE"] = OverSwitch(self, self.frame, "BOSE",
			[
				(tiles["eobleft"],  self.screen,     (68, 11), False),
				(tiles["turnrightright"],self.screen,(69, 11), False),
				(tiles["diagright"],self.screen,     (70, 12), False),
				(tiles["eobleft"],  self.screen,     (68, 13), False),
				(tiles["horiz"],    self.screen,     (69, 13), False),
				(tiles["horiznc"],  self.screen,     (70, 13), False),
				(tiles["eobright"], self.screen,     (72, 13), False),
			], True)

		self.osBlocks["BOSWW"] = [ "B10", "B11", "B21" ]
		self.osBlocks["BOSWE"] = [ "B20", "B21", "B10" ]
		self.osBlocks["BOSE"] = [ "B11", "B21", "C13" ]

		return self.blocks, self.osBlocks

	def DefineTurnouts(self, tiles, blocks):
		self.turnouts = {}

		toList = [
			[ "CSw17",  "torightleft",  ["BOSE"], (71, 13) ],
			[ "CSw19",  "torightright",  ["B21"], (63, 13) ],
			[ "CSw21a", "torightleft",   ["B11"], (66, 11) ],
			[ "CSw21b", "torightleft",   ["B11"], (63, 11) ],
			[ "CSw23",  "torightright",  ["BOSWW", "BOSWE"], (54, 11) ],
			[ "CSw23b", "torightleft",   ["BOSWW", "BOSWE"], (56, 13) ],
		]

		for tonm, tileSet, blks, pos in toList:
			trnout = Turnout(self, self.frame, tonm, self.screen, tiles[tileSet], pos)
			for blknm in blks:
				blocks[blknm].AddTurnout(trnout)
				trnout.AddBlock(blknm)
			self.turnouts[tonm] = trnout

		self.turnouts["CSw23"].SetPairedTurnout(self.turnouts["CSw23b"])

		self.turnouts["CSw19"].SetDisabled(True)
		self.turnouts["CSw21a"].SetDisabled(True)
		self.turnouts["CSw21b"].SetDisabled(True)

		return self.turnouts
		
	def DefineSignals(self, tiles):
		self.signals = {}

		sigList = [
			[ "C18RB",  RegAspects, True,    "right", (68, 12) ],
			[ "C18RA",  RegAspects, True,    "rightlong", (68, 14) ],
			[ "C18L",   RegAspects, False,   "leftlong", (72, 12) ],

			[ "C22R",   RegAspects, True,    "right", (53, 12) ],
			[ "C22L",   RegAspects, False,   "leftlong", (57, 10) ],

			[ "C24R",   RegAspects, True,    "rightlong", (53, 14) ],
			[ "C24L",   RegAspects, False,   "leftlong", (57, 12) ],
		]
		for signm, atype, east, tileSet, pos in sigList:
			self.signals[signm]  = Signal(self, self.screen, self.frame, signm, atype, east, pos, tiles[tileSet])  

		blockSigs = {
			# # which signals govern stopping sections, west and east
			"B11": ("C22L",  None),
			"B20": (None,    "C24R"),
			"B21": ("C24L",  "C18RA"),
		}

		for blknm, siglist in blockSigs.items():
			self.blocks[blknm].SetSignals(siglist)

		self.routes = {}
		self.osSignals = {}

		block = self.blocks["BOSWW"]
		self.routes["BRtB10B11"] = Route(self.screen, block, "BRtB10B11", "B11", [ (53, 11), (54, 11), (55, 11), (56, 11), (57, 11) ], "B10", [RESTRICTING, MAIN], ["CSw23"])
		self.routes["BRtB10B21"] = Route(self.screen, block, "BRtB10B21", "B21", [ (53, 11), (54, 11), (55, 12), (56, 13), (57, 13) ], "B10", [RESTRICTING, DIVERGING], ["CSw23"])

		block=self.blocks["BOSWE"]
		self.routes["BRtB20B21"] = Route(self.screen, block, "BRtB20B21", "B21", [ (53, 13), (54, 13), (55, 13), (56, 13), (57, 13) ], "B20", [MAIN, RESTRICTING], ["CSw23"])

		block=self.blocks["BOSE"]
		self.routes["BRtB11C13"] = Route(self.screen, block, "BRtB11C13", "B11", [ (68, 11), (69, 11), (70, 12), (71, 13), (72, 13) ], "C13", [RESTRICTING, DIVERGING], ["CSW17"])
		self.routes["BRtB21C13"] = Route(self.screen, block, "BRtB21C13", "B21", [ (68, 13), (69, 13), (70, 13), (71, 13), (72, 13) ], "C13", [MAIN, MAIN], ["CSW17"])

		self.signals["C22R"].AddPossibleRoutes("BOSWW", [ "BRtB10B11", "BRtB10B21" ])
		self.signals["C22L"].AddPossibleRoutes("BOSWW", [ "BRtB10B11" ])

		self.signals["C24R"].AddPossibleRoutes("BOSWE", [ "BRtB20B21" ])
		self.signals["C24L"].AddPossibleRoutes("BOSWE", [ "BRtB20B21" ])
		self.signals["C24L"].AddPossibleRoutes("BOSWW", [ "BRtB10B21" ])

		self.signals["C18RB"].AddPossibleRoutes("BOSE", ["BRtB11C13"])
		self.signals["C18RA"].AddPossibleRoutes("BOSE", ["BRtB21C13"])
		self.signals["C18L"].AddPossibleRoutes("BOSE", ["BRtB11C13", "BRtB21C13"])

		self.osSignals["BOSWW"] = [ "C22R", "C22L", "C24L" ]
		self.osSignals["BOSWE"] = [ "C24R", "C24L" ]
		self.osSignals["BOSE"] = [ "C18RB", "C18RA", "C18L" ]

		return self.signals

	def DefineHandSwitches(self, tiles):
		self.handswitches = {}

		hs = HandSwitch(self, self.screen, self.frame, self.blocks["B11"], "CSw21b.hand", (63, 10), tiles["handdown"])
		self.blocks["B11"].AddHandSwitch(hs)
		self.handswitches["CSw21b.hand"] = hs

		hs = HandSwitch(self, self.screen, self.frame, self.blocks["B11"], "CSw21a.hand", (66, 10), tiles["handdown"])
		self.blocks["B11"].AddHandSwitch(hs)
		self.handswitches["CSw21a.hand"] = hs

		hs = HandSwitch(self, self.screen, self.frame, self.blocks["B21"], "CSw19.hand", (63, 14), tiles["handup"])
		self.blocks["B11"].AddHandSwitch(hs)
		self.handswitches["CSw19.hand"] = hs

		return self.handswitches