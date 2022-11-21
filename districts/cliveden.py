from district import District

from block import Block, OverSwitch, Route
from turnout import Turnout
from signal import Signal
from handswitch import HandSwitch

from constants import MAIN, DIVERGING, RegAspects


class Cliveden (District):
	def __init__(self, name, frame, screen):
		District.__init__(self, name, frame, screen)

	def DetermineRoute(self, blocks):
		s13 = 'N' if self.turnouts["CSw13"].IsNormal() else 'R'
		s9 = 'N' if self.turnouts["CSw9"].IsNormal() else 'R'

		for block in blocks:
			bname = block.GetName()
			if bname == "COSCLW":
				if s13 == "N":
					block.SetRoute(self.routes["CRtC13C23"])
				else:
					block.SetRoute(self.routes["CRtC13C12"])

			elif bname == "COSCLEW":
				if s9 == "N":
					block.SetRoute(self.routes["CRtC23C22"])
				else:
					block.SetRoute(None)
			
			elif bname == "COSCLEE":
				if s9 == "N":
					block.SetRoute(self.routes["CRtC12C11"])
				else:
					block.SetRoute(self.routes["CRtC23C11"])

	def DefineBlocks(self, tiles):
		self.blocks = {}
		self.osBlocks = {}

		self.blocks["C13"] = Block(self, self.frame, "C13",
			[
				(tiles["horiz"],   self.screen,      (75, 13), False),
				(tiles["horiznc"], self.screen,      (76, 13), False),
				(tiles["horiz"],   self.screen,      (77, 13), False),
				(tiles["horiz"],   self.screen,      (79, 13), False),
			], False)
		self.blocks["C13"].AddStoppingBlock([
				(tiles["horiznc"], self.screen,      (80, 13), False),
				(tiles["eobright"],self.screen,      (81, 13), False),
			], True)
		self.blocks["C13"].AddStoppingBlock([
				(tiles["eobleft"], self.screen,      (73, 13), False),
				(tiles["horiznc"], self.screen,      (74, 13), False),
			], False)
		self.blocks["C13"].AddTrainLoc(self.screen, (75, 13))

		self.blocks["C23"] = Block(self, self.frame, "C23",
			[
				(tiles["horiz"],   self.screen,      (89, 13), False),
				(tiles["horiznc"], self.screen,      (90, 13), False),
				(tiles["horiz"],   self.screen,      (91, 13), False),
				(tiles["horiz"],   self.screen,      (93, 13), False),
				(tiles["eobright"],self.screen,      (94, 13), False),
			], False)
		self.blocks["C23"].AddStoppingBlock([
				(tiles["eobleft"], self.screen,      (87, 13), False),
				(tiles["horiznc"], self.screen,      (88, 13), False),
			], False)
		self.blocks["C23"].AddTrainLoc(self.screen, (90, 13))

		self.blocks["C12"] = Block(self, self.frame, "C12",
			[
				(tiles["horiz"],   self.screen,      (89, 15), False),
				(tiles["horiznc"], self.screen,      (90, 15), False),
				(tiles["horiz"],   self.screen,      (91, 15), False),
				(tiles["horiznc"], self.screen,      (92, 15), False),
				(tiles["horiz"],   self.screen,      (93, 15), False),
				(tiles["eobright"],self.screen,      (94, 15), False),
			], True)
		self.blocks["C12"].AddStoppingBlock([
				(tiles["eobleft"], self.screen,      (87, 15), False),
				(tiles["horiznc"], self.screen,      (88, 15), False),
			], False)
		self.blocks["C12"].AddTrainLoc(self.screen, (90, 15))

		self.blocks["C22"] = Block(self, self.frame, "C22",
			[
				(tiles["eobleft"], self.screen,      (100, 13), False),
				(tiles["horiznc"], self.screen,      (101, 13), False),
				(tiles["horiz"],   self.screen,      (102, 13), False),
				(tiles["horiznc"], self.screen,      (103, 13), False),
				(tiles["horiz"],   self.screen,      (104, 13), False),
				(tiles["eobright"],self.screen,      (105, 13), False),
			], False)
		self.blocks["C22"].AddTrainLoc(self.screen, (102, 13))

		self.blocks["C11"] = Block(self, self.frame, "C11",
			[
				(tiles["eobleft"], self.screen,      (100, 15), False),
				(tiles["horiznc"], self.screen,      (101, 15), False),
				(tiles["horiz"],   self.screen,      (102, 15), False),
				(tiles["horiznc"], self.screen,      (103, 15), False),
				(tiles["horiz"],   self.screen,      (104, 15), False),
				(tiles["horiznc"], self.screen,      (105, 15), False),
				(tiles["horiz"],   self.screen,      (106, 15), False),
				(tiles["horiznc"], self.screen,      (107, 15), False),
				(tiles["horiz"],   self.screen,      (108, 15), False),
				(tiles["horiznc"], self.screen,      (109, 15), False),
				(tiles["horiz"],   self.screen,      (110, 15), False),
				(tiles["turnrightright"],self.screen,(111, 15), False),
				(tiles["diagright"],self.screen,     (112, 16), False),
				(tiles["diagright"],self.screen,     (113, 17), False),
				(tiles["turnleftup"],self.screen,    (114, 18), False),
				(tiles["verticalnc"],self.screen,    (114, 19), True),
				(tiles["vertical"], self.screen,     (114, 20), True),
				(tiles["verticalnc"],self.screen,    (114, 21), True),
				(tiles["vertical"], self.screen,     (114, 22), True),
				(tiles["verticalnc"],self.screen,    (114, 23), True),
				(tiles["vertical"], self.screen,     (114, 24), True),
				(tiles["verticalnc"],self.screen,    (114, 25), True),
				(tiles["vertical"], self.screen,     (114, 26), True),
				(tiles["turnleftdown"],self.screen,  (114, 27), False),
				(tiles["diagright"],self.screen,     (115, 28), False),
				(tiles["diagright"],self.screen,     (116, 29), False),
				(tiles["turnrightleft"],self.screen, (117, 30), False),
				(tiles["eobright"],self.screen,      (118, 30), False),
			], True)
		self.blocks["C11"].AddTrainLoc(self.screen, (102, 15))

		self.blocks["COSCLW"] = OverSwitch(self, self.frame, "COSCLW",
			[
				(tiles["eobleft"], self.screen,      (82, 13), False),
				(tiles["horiznc"], self.screen,      (84, 13), False),
				(tiles["horiz"],   self.screen,      (85, 13), False),
				(tiles["eobright"],self.screen,      (86, 13), False),
				(tiles["diagright"],self.screen,     (84, 14), False),
				(tiles["turnrightleft"],self.screen, (85, 15), False),
				(tiles["eobright"],self.screen,      (86, 15), False),
			], False)

		self.blocks["COSCLEW"] = OverSwitch(self, self.frame, "COSCLEW",
			[
				(tiles["eobleft"], self.screen,      (95, 13), False),
				(tiles["horiznc"], self.screen,      (97, 13), False),
				(tiles["horiz"],   self.screen,      (98, 13), False),
				(tiles["eobright"],self.screen,      (99, 13), False),
			], False)

		self.blocks["COSCLEE"] = OverSwitch(self, self.frame, "COSCLEE",
			[
				(tiles["eobleft"], self.screen,      (95, 15), False),
				(tiles["horiz"],   self.screen,      (96, 15), False),
				(tiles["horiznc"], self.screen,      (97, 15), False),
				(tiles["eobright"],self.screen,      (99, 15), False),
				(tiles["eobleft"], self.screen,      (95, 13), False),
				(tiles["diagright"],self.screen,     (97, 14), False),
			], True)

		self.osBlocks["COSCLW"] = [ "C13", "C23", "C12" ]
		self.osBlocks["COSCLEW"] = [ "C23", "C22" ]
		self.osBlocks["COSCLEE"] = [ "C12", "C11", "C23" ]

		return self.blocks, self.osBlocks

	def DefineTurnouts(self, tiles, blocks):
		self.turnouts = {}

		toList = [
			[ "CSw9",   "torightright",  ["COSCLEW", "COSCLEE"], (96, 13) ],
			[ "CSw9b",  "torightleft",   ["COSCLEW", "COSCLEE"], (98, 15) ],
			[ "CSw11",  "toleftright",   ["C23"], (92, 13) ],
			[ "CSw13" , "torightright",  ["COSCLW"], (83, 13) ],
			[ "CSw15",  "torightleft",   ["C13"], (78, 13) ],
		]

		for tonm, tileSet, blks, pos in toList:
			trnout = Turnout(self, self.frame, tonm, self.screen, tiles[tileSet], pos)
			for blknm in blks:
				blocks[blknm].AddTurnout(trnout)
				trnout.AddBlock(blknm)
			self.turnouts[tonm] = trnout

		self.turnouts["CSw9"].SetPairedTurnout(self.turnouts["CSw9b"])

		self.turnouts["CSw11"].SetDisabled(True)
		self.turnouts["CSw15"].SetDisabled(True)

		return self.turnouts

	def DefineSignals(self, tiles):
		self.signals = {}
	
		sigList = [
			[ "C14R",   RegAspects, True,    "rightlong", (82, 14) ],
			[ "C14LB",  RegAspects, False,   "leftlong", (86, 12) ],
			[ "C14LA",  RegAspects, False,   "leftlong", (86, 14) ],

			[ "C12R",   RegAspects, True,    "rightlong", (95, 16) ],
			[ "C12L",   RegAspects, False,   "leftlong", (99, 14) ],

			[ "C10R",   RegAspects, True,    "rightlong", (95, 14) ],
			[ "C10L",   RegAspects, False,   "leftlong", (99, 12) ],
		]
		for signm, atype, east, tileSet, pos in sigList:
			self.signals[signm]  = Signal(self, self.screen, self.frame, signm, atype, east, pos, tiles[tileSet])  

		self.sigLeverMap = {
			"C10.lvr": [ "COSCLEW", "COSCLEE" ],
			"C12.lvr": [ "COSCLEE" ],
			"C14.lvr": [ "COSCLW" ],
		}

		for sl in self.sigLeverMap:
			self.frame.AddSignalLever(sl, self)

		blockSigs = {
			# # which signals govern stopping sections, west and east
			"C13": ("C18L",  "C14L"),
			"C23": ("C14LB", None),
			"C12": ("C14LA", None),
		}

		for blknm, siglist in blockSigs.items():
			self.blocks[blknm].SetSignals(siglist)

		self.routes = {}
		self.osSignals = {}

		block = self.blocks["COSCLW"]
		self.routes["CRtC13C23"] = Route(self.screen, block, "CRtC13C23", "C23", [ (82, 13), (83, 13), (84, 13), (85, 13), (86, 13) ], "C13", [MAIN, MAIN], ["CSw13"], ["C14R", "C14LB"])
		self.routes["CRtC13C12"] = Route(self.screen, block, "CRtC13C12", "C12", [ (82, 13), (83, 13), (84, 14), (85, 15), (86, 15) ], "C13", [DIVERGING, DIVERGING], ["CSw13"], ["C14R", "C14LA"])

		block=self.blocks["COSCLEW"]
		self.routes["CRtC23C22"] = Route(self.screen, block, "CRtC23C22", "C22", [ (95, 13), (96, 13), (97, 13), (98, 13), (99, 13) ], "C23", [MAIN, MAIN], ["CSw9"], ["C10R", "C10L"])

		block=self.blocks["COSCLEE"]
		self.routes["CRtC12C11"] = Route(self.screen, block, "CRtC12C11", "C12", [ (95, 15), (96, 15), (97, 15), (98, 15), (99, 15) ], "C11", [MAIN, MAIN], ["CSw9"], ["C12R", "C12L"])
		self.routes["CRtC23C11"] = Route(self.screen, block, "CRtC23C11", "C23", [ (95, 13), (96, 13), (97, 14), (98, 15), (99, 15) ], "C11", [DIVERGING, DIVERGING], ["CSw9"], ["C10R", "C12L"])

		self.signals["C14R"].AddPossibleRoutes("COSCLW", [ "CRtC13C23", "CRtC13C12" ])
		self.signals["C14LA"].AddPossibleRoutes("COSCLW", [ "CRtC13C12" ])
		self.signals["C14LB"].AddPossibleRoutes("COSCLW", [ "CRtC13C23" ])

		self.signals["C12R"].AddPossibleRoutes("COSCLEE", [ "CRtC12C11" ])
		self.signals["C12L"].AddPossibleRoutes("COSCLEE", [ "CRtC12C11", "CRtC23C11" ])

		self.signals["C10R"].AddPossibleRoutes("COSCLEW", [ "CRtC23C22" ])
		self.signals["C10R"].AddPossibleRoutes("COSCLEE", [ "CRtC23C11" ])
		self.signals["C10L"].AddPossibleRoutes("COSCLEW", [ "CRtC23C22" ])

		self.osSignals["COSCLW"] =  [ "C14R", "C14LA", "C14LB" ]
		self.osSignals["COSCLEW"] = [ "C10R", "C10L", "C12L" ]
		self.osSignals["COSCLEE"] = [ "C12R", "C12L", "C10R" ]

		return self.signals

	def DefineHandSwitches(self, tiles):
		self.handswitches = {}

		hs = HandSwitch(self, self.screen, self.frame, self.blocks["C23"], "CSw11.hand", (92, 12), tiles["handdown"])
		self.blocks["C23"].AddHandSwitch(hs)
		self.handswitches["CSw11.hand"] = hs

		hs = HandSwitch(self, self.screen, self.frame, self.blocks["C13"], "CSw15.hand", (78, 12), tiles["handdown"])
		self.blocks["C13"].AddHandSwitch(hs)
		self.handswitches["CSw15.hand"] = hs

		return self.handswitches

