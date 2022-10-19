from district import District

from block import Block, OverSwitch, Route
from turnout import Turnout, SlipSwitch
from signal import Signal
from button import Button
from handswitch import HandSwitch

from constants import HyYdPt, LaKr, RESTRICTING, MAIN, DIVERGING, SLOW, NORMAL, REVERSE, EMPTY, SLIPSWITCH

class Dell (District):
	def __init__(self, name, frame, screen):
		District.__init__(self, name, frame, screen)

	def DoTurnoutAction(self, turnout, state):
		tn = turnout.GetName()
		print("dell dta, tn=%s" % tn)
		if turnout.GetType() == SLIPSWITCH:
			if tn == "DSw3":
				bstat = NORMAL if self.turnouts["DSw5"].IsNormal() else REVERSE
				print("set slipswitch status to %d %d" % (state, bstat))
				turnout.SetStatus([state, bstat])
				turnout.Draw()

		else:
			District.DoTurnoutAction(self, turnout, state)

		if tn == "DSw5":
			trnout = self.turnouts["DSw3"]
			trnout.UpdateStatus()
			trnout.Draw()

	def DetermineRoute(self, blocks):
		s1 = 'N' if self.turnouts["DSw1"].IsNormal() else 'R'
		s3 = 'N' if self.turnouts["DSw3"].IsNormal() else 'R'
		s5 = 'N' if self.turnouts["DSw5"].IsNormal() else 'R'
		s7 = 'N' if self.turnouts["DSw7"].IsNormal() else 'R'
		s11 = 'N' if self.turnouts["DSw11"].IsNormal() else 'R'
		self.turnouts["DSw5"].SetLock("DSw7", s7=='R')
		self.turnouts["DSw7"].SetLock("DSw5", s5=='R')

		for bname in blocks:
			block = self.frame.GetBlockByName(bname)
			if bname == "DOSVJE":
				if s1+s5+s7 == "RNR":
					block.SetRoute(self.routes["DRtH13D21"])
				elif s1+s5+s7 == "NNR":
					block.SetRoute(self.routes["DRtD10D21"])
				elif s3+s5+s7 == "NNN":
					block.SetRoute(self.routes["DRtD20D21"])
				elif s3+s5+s7 == "RNN":
					block.SetRoute(self.routes["DRtH23D21"])
				else:
					block.SetRoute(None)

			elif bname == "DOSVJW":
				if s1+s5+s7 == "RNN":
					block.SetRoute(self.routes["DRtH13D11"])
				elif s1+s5+s7 == "NNN":
					block.SetRoute(self.routes["DRtD10D11"])
				elif s3+s5+s7 == "NRN":
					block.SetRoute(self.routes["DRtD20D11"])
				elif s3+s5+s7 == "RRN":
					block.SetRoute(self.routes["DRtH23D11"])
				else:
					block.SetRoute(None)

			elif bname == "DOSFOE":
				if s11 == "N":
					block.SetRoute(self.routes["DRtD21S20"])
				else:
					block.SetRoute(None)

			elif bname == "DOSFOW":
				if s11 == "N":
					block.SetRoute(self.routes["DRtD11S10"])
				else:
					block.SetRoute(self.routes["DRtD21S10"])

	def DefineBlocks(self, tiles):
		self.blocks = {}
		self.osBlocks = {}

		self.blocks["D10"] = Block(self, self.frame, "D10",
			[
				(tiles["horiznc"], self.screen,      (39, 11), False),
				(tiles["horiz"],   self.screen,      (40, 11), False),
				(tiles["horiznc"], self.screen,      (41, 11), False),
				(tiles["horiz"],   self.screen,      (42, 11), False),
				(tiles["horiznc"], self.screen,      (43, 11), False),
				(tiles["horiz"],   self.screen,      (44, 11), False),
				(tiles["eobright"],self.screen,      (45, 11), False),
			], False)
		self.blocks["D10"].AddStoppingBlock([
				(tiles["eobleft"], self.screen,      (36, 11), False),
				(tiles["horiznc"], self.screen,      (37, 11), False),
				(tiles["horiz"],   self.screen,      (38, 11), False),
			], False)
		self.blocks["D10"].AddTrainLoc(self.screen, (38, 11))

		self.blocks["D20"] = Block(self, self.frame, "D20",
			[
				(tiles["eobleft"], self.screen,      (36, 13), False),
				(tiles["horiznc"], self.screen,      (37, 13), False),
				(tiles["horiz"],   self.screen,      (38, 13), False),
				(tiles["horiznc"], self.screen,      (39, 13), False),
				(tiles["horiz"],   self.screen,      (40, 13), False),
				(tiles["horiznc"], self.screen,      (41, 13), False),
				(tiles["horiz"],   self.screen,      (42, 13), False),
			], True)
		self.blocks["D20"].AddStoppingBlock([
				(tiles["horiznc"], self.screen,      (43, 13), False),
				(tiles["horiz"],   self.screen,      (44, 13), False),
				(tiles["eobright"],self.screen,      (45, 13), False),
			], True)
		self.blocks["D20"].AddTrainLoc(self.screen, (38, 13))

		self.blocks["D11"] = Block(self, self.frame, "D11",
			[
				(tiles["horiz"],   self.screen,      (58, 11), False),
				(tiles["horiznc"], self.screen,      (59, 11), False),
				(tiles["horiz"],   self.screen,      (60, 11), False),
				(tiles["horiznc"], self.screen,      (61, 11), False),
				(tiles["horiz"],   self.screen,      (62, 11), False),
				(tiles["horiznc"], self.screen,      (63, 11), False),
			], False)
		self.blocks["D11"].AddStoppingBlock([
				(tiles["horiz"],   self.screen,      (64, 11), False),
				(tiles["eobright"],self.screen,      (65, 11), False),
			], True)
		self.blocks["D11"].AddStoppingBlock([
				(tiles["eobleft"], self.screen,      (56, 11), False),
				(tiles["horiznc"], self.screen,      (57, 11), False),
			], False)
		self.blocks["D11"].AddTrainLoc(self.screen, (58, 11))

		self.blocks["D21"] = Block(self, self.frame, "D21",
			[
				(tiles["horiz"],   self.screen,      (58, 13), False),
				(tiles["horiznc"], self.screen,      (59, 13), False),
				(tiles["horiz"],   self.screen,      (60, 13), False),
				(tiles["horiznc"], self.screen,      (61, 13), False),
				(tiles["horiz"],   self.screen,      (62, 13), False),
			], True)
		self.blocks["D21"].AddStoppingBlock([
				(tiles["eobleft"], self.screen,      (56, 13), False),
				(tiles["horiznc"], self.screen,      (57, 13), False),
			], False)
		self.blocks["D21"].AddStoppingBlock([
				(tiles["horiz"],   self.screen,      (64, 13), False),
				(tiles["eobright"],self.screen,      (65, 13), False),
			], True)
		self.blocks["D21"].AddTrainLoc(self.screen, (58, 13))

		self.blocks["DOSVJW"] = OverSwitch(self, self.frame, "DOSVJW", 
			[
				(tiles["eobleft"],        self.screen, (46, 9), False),
				(tiles["turnrightright"], self.screen, (47, 9), False),
				(tiles["diagright"],      self.screen, (48, 10), False),
				(tiles["eobleft"],        self.screen, (46, 11), False),
				(tiles["horiznc"],        self.screen, (47, 11), False),
				(tiles["horiz"],          self.screen, (48, 11), False),
				(tiles["horiznc"],        self.screen, (50, 11), False),
				(tiles["eobleft"],        self.screen, (46, 13), False),
				(tiles["horiznc"],        self.screen, (47, 13), False),
				(tiles["horiz"],          self.screen, (48, 13), False),
				(tiles["eobleft"],        self.screen, (46, 15), False),
				(tiles["turnleftright"],  self.screen, (47, 15), False),
				(tiles["diagleft"],       self.screen, (48, 14), False),
				(tiles["diagleft"],       self.screen, (50, 12), False),
				(tiles["horiz"],          self.screen, (53, 11), False),
				(tiles["horiznc"],        self.screen, (54, 11), False),
				(tiles["eobright"],       self.screen, (55, 11), False),
			],
			False)

		self.blocks["DOSVJE"] = OverSwitch(self, self.frame, "DOSVJE", 
			[
				(tiles["eobleft"],        self.screen, (46, 9), False),
				(tiles["turnrightright"], self.screen, (47, 9), False),
				(tiles["diagright"],      self.screen, (48, 10), False),
				(tiles["eobleft"],        self.screen, (46, 11), False),
				(tiles["horiznc"],        self.screen, (47, 11), False),
				(tiles["horiz"],          self.screen, (48, 11), False),
				(tiles["horiznc"],        self.screen, (50, 11), False),
				(tiles["eobleft"],        self.screen, (46, 13), False),
				(tiles["horiznc"],        self.screen, (47, 13), False),
				(tiles["horiz"],          self.screen, (48, 13), False),
				(tiles["eobleft"],        self.screen, (46, 15), False),
				(tiles["turnleftright"],  self.screen, (47, 15), False),
				(tiles["diagleft"],       self.screen, (48, 14), False),
				(tiles["diagleft"],       self.screen, (48, 14), False),
				(tiles["horiz"],          self.screen, (50, 13), False),
				(tiles["horiznc"],        self.screen, (51, 13), False),
				(tiles["horiz"],          self.screen, (52, 13), False),
				(tiles["horiznc"],        self.screen, (53, 13), False),
				(tiles["diagright"],      self.screen, (53, 12), False),
				(tiles["eobright"],       self.screen, (55, 13), False),
			],
			True)

		self.blocks["DOSFOE"] = OverSwitch(self, self.frame, "DOSFOE", 
			[
				(tiles["eobleft"],        self.screen, (66, 13), False),
				(tiles["horiz"],          self.screen, (68, 13), False),
				(tiles["horiz"],          self.screen, (69, 13), False),
				(tiles["eobright"],       self.screen, (70, 13), False),
				(tiles["diagleft"],       self.screen, (68, 12), False),
				(tiles["eobright"],       self.screen, (70, 11), False),
			],
			True)

		self.blocks["DOSFOW"] = OverSwitch(self, self.frame, "DOSFOW", 
			[
				(tiles["eobleft"],        self.screen, (66, 13), False),
				(tiles["diagleft"],       self.screen, (68, 12), False),
				(tiles["eobleft"],        self.screen, (66, 11), False),
				(tiles["horiz"],          self.screen, (67, 11), False),
				(tiles["horiz"],          self.screen, (68, 11), False),
				(tiles["eobright"],       self.screen, (70, 11), False),
			],
			False)

		self.osBlocks["DOSVJE"] = [ "H13", "H23", "D10", "D20", "D21" ]
		self.osBlocks["DOSVJW"] = [ "H13", "H23", "D10", "D20", "D11" ]
		self.osBlocks["DOSFOE"] = [ "D21", "S10", "S20" ]
		self.osBlocks["DOSFOW"] = [ "S10", "D11", "D21" ]

		return self.blocks

	def DefineTurnouts(self, tiles, blocks):
		self.turnouts = {}

		toList = [
			[ "DSw1",  "torightleft",  ["DOSVJE", "DOSVJW"], (49, 11) ],
			[ "DSw5",  "toleftleft",   ["DOSVJE", "DOSVJW"], (51, 11) ],
			[ "DSw7",  "torightleft",  ["DOSVJE", "DOSVJW"], (54, 13) ],
			[ "DSw7b", "torightright", ["DOSVJE", "DOSVJW"], (52, 11) ],
			[ "DSw9",  "toleftleft",   ["D21"], (63, 13) ],
		
			[ "DSw11",  "toleftright", ["DOSFOE", "DOSFOW"], (67, 13) ],
			[ "DSw11b", "toleftleft",  ["DOSFOE", "DOSFOW"], (69, 11) ],
		]

		for tonm, tileSet, blks, pos in toList:
			trnout = Turnout(self, self.frame, tonm, self.screen, tiles[tileSet], pos)
			for blknm in blks:
				blocks[blknm].AddTurnout(trnout)
				trnout.AddBlock(blknm)
			self.turnouts[tonm] = trnout

		trnout = SlipSwitch(self, self.frame, "DSw3", self.screen, tiles["ssright"], (49, 13))
		blocks["DOSVJE"].AddTurnout(trnout)
		blocks["DOSVJW"].AddTurnout(trnout)
		trnout.AddBlock("DOSVJE")
		trnout.AddBlock("DOSVJW")
		trnout.SetControllers(None, self.turnouts["DSw5"])
		self.turnouts["DSw3"] = trnout

		self.turnouts["DSw7"].SetPairedTurnout(self.turnouts["DSw7b"])
		self.turnouts["DSw11"].SetPairedTurnout(self.turnouts["DSw11b"])

		self.turnouts["DSw9"].SetDisabled(True)

		return self.turnouts

	def DefineSignals(self, tiles):
		self.signals = {}

		sigList = [
			[ "D6RA",  True,   "right", (46, 10) ],
			[ "D6RB",  True,   "right", (46, 12) ],
			[ "D4RA",  True,   "right", (46, 14) ],
			[ "D4RB",  True,   "right", (46, 16) ],

			[ "D6L",   False,  "left",  (55, 10) ],
			[ "D4L",   False,  "left",  (55, 12) ],

			[ "D12R",  True,   "right", (66, 12) ],
			[ "D10R",  True,   "right", (66, 14) ],

			[ "D12L",  False,  "left",  (70, 10) ],
			[ "D10L",  False,  "left",  (70, 12) ]
		]
		for signm, east, tileSet, pos in sigList:
			self.signals[signm]  = Signal(self, self.screen, self.frame, signm, east, pos, tiles[tileSet])  

		self.routes = {}
		self.osSignals = {}

		# FOSS and Valley Junstion interlockings
		block = self.blocks["DOSVJE"]
		self.routes["DRtH13D21"] = Route(self.screen, block, "DRtH13D21", "H13", [ (46,  9), (47,  9), (48, 10), (49, 11), (50, 11), (51, 11), (52, 11), (53, 12), (54, 13), (55, 13) ], "D21", [RESTRICTING, DIVERGING], ["DSw1", "DSw5", "DSw7"])
		self.routes["DRtD10D21"] = Route(self.screen, block, "DRtD10D21", "D10", [ (46, 11), (47, 11), (48, 11), (49, 11), (50, 11), (51, 11), (52, 11), (53, 12), (54, 13), (55, 13) ], "D21", [RESTRICTING, DIVERGING], ["DSw1", "DSw5", "DSw7"])
		self.routes["DRtD20D21"] = Route(self.screen, block, "DRtD20D21", "D20", [ (46, 13), (47, 13), (48, 13), (49, 13), (50, 13), (51, 13), (52, 13), (53, 13), (54, 13), (55, 13) ], "D21", [MAIN, RESTRICTING],      ["DSw3", "DSw5", "DSw7"])
		self.routes["DRtH23D21"] = Route(self.screen, block, "DRtH23D21", "H23", [ (46, 15), (47, 15), (48, 14), (49, 13), (50, 13), (51, 13), (52, 13), (53, 13), (54, 13), (55, 13) ], "D21", [DIVERGING, RESTRICTING], ["DSw3", "DSw5", "DSw7"])

		block = self.blocks["DOSVJW"]
		self.routes["DRtH13D11"] = Route(self.screen, block, "DRtH13D11", "D11", [ (46,  9), (47,  9), (48, 10), (49, 11), (50, 11), (51, 11), (52, 11), (53, 11), (54, 11), (55, 11) ], "H13", [RESTRICTING, DIVERGING], ["DSw1", "DSw5", "DSw7"])
		self.routes["DRtD10D11"] = Route(self.screen, block, "DRtD10D11", "D11", [ (46, 11), (47, 11), (48, 11), (49, 11), (50, 11), (51, 11), (52, 11), (53, 11), (54, 11), (55, 11) ], "D10", [RESTRICTING, MAIN],      ["DSw1", "DSw5", "DSw7"])
		self.routes["DRtD20D11"] = Route(self.screen, block, "DRtD20D11", "D11", [ (46, 13), (47, 13), (48, 13), (49, 13), (50, 12), (51, 11), (52, 11), (53, 11), (54, 11), (55, 11) ], "D20", [DIVERGING, RESTRICTING], ["DSw3", "DSw5", "DSw7"])
		self.routes["DRtH23D11"] = Route(self.screen, block, "DRtH23D11", "D11", [ (46, 15), (47, 15), (48, 14), (49, 13), (50, 12), (51, 11), (52, 11), (53, 11), (54, 11), (55, 11) ], "H23", [DIVERGING, RESTRICTING], ["DSw3", "DSw5", "DSw7"])

		block = self.blocks["DOSFOE"]
		self.routes["DRtD21S20"] = Route(self.screen, block, "DRtD21S20", "D21", [ (66, 13), (67, 13), (68, 13), (69, 13), (70, 13) ], "S20", [MAIN, MAIN],             ["DSw11"])

		block = self.blocks["DOSFOW"]
		self.routes["DRtD11S10"] = Route(self.screen, block, "DRtD11S10", "S10", [ (66, 11), (67, 11), (68, 11), (69, 11), (70, 11) ], "D11", [MAIN, MAIN],             ["DSw11"])
		self.routes["DRtD21S10"] = Route(self.screen, block, "DRtD21S10", "S10", [ (66, 13), (67, 13), (68, 12), (69, 11), (70, 11) ], "D21", [DIVERGING, DIVERGING],   ["DSw11"])

		self.signals["D4RA"].AddPossibleRoutes("DOSVJE", [ "DRtD20D21" ])
		self.signals["D4RA"].AddPossibleRoutes("DOSVJW", [ "DRtD20D11" ])
		self.signals["D4RB"].AddPossibleRoutes("DOSVJE", [ "DRtH23D21" ])
		self.signals["D4RB"].AddPossibleRoutes("DOSVJW", [ "DRtH23D11" ])
		
		self.signals["D6RA"].AddPossibleRoutes("DOSVJE", [ "DRtH13D21" ])
		self.signals["D6RA"].AddPossibleRoutes("DOSVJW", [ "DRtH13D11" ])
		self.signals["D6RB"].AddPossibleRoutes("DOSVJE", [ "DRtD10D21" ])
		self.signals["D6RB"].AddPossibleRoutes("DOSVJW", [ "DRtD10D11" ])

		self.signals["D4L"].AddPossibleRoutes("DOSVJE", [ "DRtD20D21", "DRtH23D21", "DRtH13D21", "DRtD10D21" ])
		self.signals["D6L"].AddPossibleRoutes("DOSVJW", [ "DRtD20D11", "DRtH23D11", "DRtH13D11", "DRtD10D11" ])

		self.signals["D10R"].AddPossibleRoutes("DOSFOW", ["DRtD21S10"])
		self.signals["D10R"].AddPossibleRoutes("DOSFOE", ["DRtD21S20"])
		self.signals["D12R"].AddPossibleRoutes("DOSFOW", ["DRtD11S10"])

		self.signals["D10L"].AddPossibleRoutes("DOSFOE", [ "DRtD21S20"] )
		self.signals["D12L"].AddPossibleRoutes("DOSFOW", [ "DRtD11S10", "DRtD21S10" ])

		self.osSignals["DOSVJE"] = [ "D4RA", "D4RB", "D4L", "D6RA", "D6RB" ]
		self.osSignals["DOSVJW"] = [ "D4RA", "D4RB", "D6RA", "D6RB", "D6L"  ]
		self.osSignals["DOSFOE"] = [ "D10R", "D10L", "D12L" ]
		self.osSignals["DOSFOW"] = [ "D10R", "D12R", "D12L" ]

		return self.signals

	def DefineHandSwitches(self, tiles):
		self.handswitches = {}

		hs = HandSwitch(self, self.screen, self.frame, self.blocks["D21"], "DSw9.hand", (63, 14), tiles["handup"])
		self.blocks["D21"].AddHandSwitch(hs)
		self.handswitches["DSw9.hand"] = hs
		return self.handswitches

		