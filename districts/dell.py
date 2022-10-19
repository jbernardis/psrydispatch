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

		# for bname in blocks:
		# 	block = self.frame.GetBlockByName(bname)
		# 	if bname == "LOSLAW":
		# 		if s5+s7 == "NN":
		# 			block.SetRoute(self.routes["LRtL10L11A"])
		# 		elif s5+s7 == "RR":
		# 			block.SetRoute(self.routes["LRtL10L11B"])
		# 		elif s5+s7+s9 == "RNN":
		# 			block.SetRoute(self.routes["LRtL10L21"])
		# 		elif s5+s7+s9 == "RNR":
		# 			block.SetRoute(self.routes["LRtL10L31"])
		# 		else:
		# 			block.SetRoute(None)


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

		self.osBlocks["DOSVJE"] = [ "H13", "H23", "D10", "D20", "D21" ]
		self.osBlocks["DOSVJW"] = [ "H13", "H23", "D10", "D20", "D11" ]
		# self.osBlocks["DOSFOE"] = [ "L10", "L11", "L21", "L31" ]
		# self.osBlocks["DOSFOW"] = [ "P21", "L11", "L21", "L31" ]

		return self.blocks

	def DefineTurnouts(self, tiles, blocks):
		self.turnouts = {}

		toList = [
			[ "DSw1",  "torightleft",  ["DOSVJE", "DOSVJW"], (49, 11) ],
			[ "DSw5",  "toleftleft",   ["DOSVJE", "DOSVJW"], (51, 11) ],
			[ "DSw7",  "torightleft",  ["DOSVJE", "DOSVJW"], (54, 13) ],
			[ "DSw7b", "torightright", ["DOSVJE", "DOSVJW"], (52, 11) ],
			[ "DSw9",  "toleftleft",   ["D21"], (63, 13) ],
		
			[ "DSw11",  "toleftright", [], (67, 13) ],
			[ "DSw11b", "toleftleft",  [], (69, 11) ],
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

		# sigList = [
		# 	[ "L8R",  True,    "right", (8, 12) ],
		# 	[ "L6RA", True,    "right", (8, 14) ],
		# 	[ "L6RB", True,    "right", (8, 16) ],
		# 	[ "L4R",  True,    "right", (8, 18) ],

		# 	[ "L8L",  False,   "left",  (20, 10) ],
		# 	[ "L6L",  False,   "left",  (20, 12) ],
		# 	[ "L4L",  False,   "left",  (20, 14) ],

		# 	[ "L18R", True,    "right", (30, 12) ],
		# 	[ "L16R", True,    "right", (30, 14) ],
		# 	[ "L14R", True,    "right", (30, 16) ],

		# 	[ "L18L", False,   "left",  (35, 10) ],
		# 	[ "L14L", False,   "left",  (35, 12) ]
		# ]
		# for signm, east, tileSet, pos in sigList:
		# 	self.signals[signm]  = Signal(self, self.screen, self.frame, signm, east, pos, tiles[tileSet])  

		self.routes = {}
		self.osSignals = {}

		# # latham OS
		# block = self.blocks["LOSLAW"]
		# self.routes["LRtL10L11A"] = Route(self.screen, block, "LRtL10L11A", "L11", [ (8, 11), (9, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 11), (15, 11), (16, 11), (17, 11), (18, 11), (19, 11), (20, 11) ], "L10", [RESTRICTING, MAIN], ["LSw5", "LSw7"])
		# self.routes["LRtL10L11B"] = Route(self.screen, block, "LRtL10L11B", "L11", [ (8, 11), (9, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 12), (15, 13), (16, 13), (17, 12), (18, 11), (19, 11), (20, 11) ], "L10", [RESTRICTING, RESTRICTING], ["LSw5", "LSw7"])
		# self.routes["LRtL10L21"] = Route(self.screen, block, "LRtL10L21", "L21",   [ (8, 11), (9, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 12), (15, 13), (16, 13), (17, 13), (18, 13), (19, 13), (20, 13) ], "L10", [RESTRICTING, DIVERGING], ["LSw5", "LSw7", "LSw9"])
		# self.routes["LRtL10L31"] = Route(self.screen, block, "LRtL10L31", "L31",   [ (8, 11), (9, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 12), (15, 13), (16, 13), (17, 13), (18, 14), (19, 15), (20, 15) ], "L10", [RESTRICTING, DIVERGING], ["LSw5", "LSw7", "LSw9"])

		# block=self.blocks["LOSLAM"]
		# self.routes["LRtL20L11"] = Route(self.screen, block, "LRtL20L11", "L20", [ (8, 13), (9, 13), (10, 13), (11, 13), (12, 13), (13, 13), (14, 13), (15, 13), (16, 13), (17, 12), (18, 11), (19, 11), (20, 11) ], "L11", [RESTRICTING, RESTRICTING], ["LSw1", "LSw3", "LSw5", "LSw7"])
		# self.routes["LRtP11L11"] = Route(self.screen, block, "LRtP11L11", "P11", [ (8, 15), (9, 15), (10, 14), (11, 13), (12, 13), (13, 13), (14, 13), (15, 13), (16, 13), (17, 12), (18, 11), (19, 11), (20, 11) ], "L11", [RESTRICTING, DIVERGING], ["LSw1", "LSw3", "LSw5", "LSw7"])
		# self.routes["LRtL20L21"] = Route(self.screen, block, "LRtL20L21", "L20", [ (8, 13), (9, 13), (10, 13), (11, 13), (12, 13), (13, 13), (14, 13), (15, 13), (16, 13), (17, 13), (18, 13), (19, 13), (20, 13) ], "L21", [MAIN, RESTRICTING], ["LSw1", "LSw3", "LSw5", "LSw7", "LSw9"])
		# self.routes["LRtP11L21"] = Route(self.screen, block, "LRtP11L21", "P11", [ (8, 15), (9, 15), (10, 14), (11, 13), (12, 13), (13, 13), (14, 13), (15, 13), (16, 13), (17, 13), (18, 13), (19, 13), (20, 13) ], "L21", [RESTRICTING, DIVERGING], ["LSw1", "LSw3", "LSw5", "LSw7", "LSw9"])
		# self.routes["LRtL20L31"] = Route(self.screen, block, "LRtL20L31", "L20", [ (8, 13), (9, 13), (10, 13), (11, 13), (12, 13), (13, 13), (14, 13), (15, 13), (16, 13), (17, 13), (18, 14), (19, 15), (20, 15) ], "L31", [DIVERGING, RESTRICTING], ["LSw1", "LSw3", "LSw5", "LSw7", "LSw9"])
		# self.routes["LRtP11L31"] = Route(self.screen, block, "LRtP11L31", "P11", [ (8, 15), (9, 15), (10, 14), (11, 13), (12, 13), (13, 13), (14, 13), (15, 13), (16, 13), (17, 13), (18, 14), (19, 15), (20, 15) ], "L31", [RESTRICTING, RESTRICTING], ["LSw1", "LSw3", "LSw5", "LSw7", "LSw9"])

		# block=self.blocks["LOSLAE"]
		# self.routes["LRtP21L11"] = Route(self.screen, block, "LRtP21L11", "P21", [ (8, 17), (9, 17), (10, 17), (11, 16), (12, 15), (13, 14), (14, 13), (15, 13), (16, 13), (17, 12), (18, 11), (19, 11), (20, 11) ], "L11", [RESTRICTING, RESTRICTING], ["LSw3", "LSw5", "LSw7"])
		# self.routes["LRtP21L21"] = Route(self.screen, block, "LRtP21L21", "P21", [ (8, 17), (9, 17), (10, 17), (11, 16), (12, 15), (13, 14), (14, 13), (15, 13), (16, 13), (17, 13), (18, 13), (19, 13), (20, 13) ], "L21", [RESTRICTING, RESTRICTING], ["LSw3", "LSw5", "LSw7", "LSw9"])
		# self.routes["LRtP21L31A"] = Route(self.screen, block, "LRtP21L31A", "P21", [ (8, 17), (9, 17), (10, 17), (11, 16), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), (18, 15), (19, 15), (20, 15) ], "L31", [MAIN, RESTRICTING], ["LSw3", "LSw9"])
		# self.routes["LRtP21L31B"] = Route(self.screen, block, "LRtP21L31B", "P21", [ (8, 17), (9, 17), (10, 17), (11, 16), (12, 15), (13, 14), (14, 13), (15, 13), (16, 13), (17, 13), (18, 14), (19, 15), (20, 15) ], "L31", [RESTRICTING, RESTRICTING], ["LSw3", "LSw5", "LSw7", "LSw9"])

		# self.signals["L8R"].AddPossibleRoutes("LOSLAW", [ "LRtL10L11A", "LRtL10L11B", "LRtL10L21", "LRtL10L31" ])
		# self.signals["L8L"].AddPossibleRoutes("LOSLAW", [ "LRtL10L11A", "LRtL10L11B" ])
		# self.signals["L8L"].AddPossibleRoutes("LOSLAM", [ "LRtL20L11", "LRtP11L11" ])
		# self.signals["L8L"].AddPossibleRoutes("LOSLAE", [ "LRtP21L11" ])

		# self.signals["L6RA"].AddPossibleRoutes("LOSLAM", [ "LRtL20L11", "LRtL20L21", "LRtL20L31" ])
		# self.signals["L6RB"].AddPossibleRoutes("LOSLAM", [ "LRtP11L11", "LRtP11L21", "LRtP11L31" ])
		# self.signals["L6L"].AddPossibleRoutes("LOSLAW", [ "LRtL10L21" ])
		# self.signals["L6L"].AddPossibleRoutes("LOSLAM", [ "LRtL20L21", "LRtP11L21" ])
		# self.signals["L6L"].AddPossibleRoutes("LOSLAE", [ "LRtP21L21" ])

		# self.signals["L4R"].AddPossibleRoutes("LOSLAE", [ "LRtP21L11", "LRtP21L21", "LRtP21L31A", "LRtP21L31B" ])
		# self.signals["L4L"].AddPossibleRoutes("LOSLAW", [ "LRtL10L31" ])
		# self.signals["L4L"].AddPossibleRoutes("LOSLAM", [ "LRtL20L31", "LRtP11L31" ])
		# self.signals["L4L"].AddPossibleRoutes("LOSLAE", [ "LRtP21L31A", "LRtP21L31B" ])

		# self.osSignals["LOSLAW"] = [ "L8R", "L8L", "L6L", "L4L" ]
		# self.osSignals["LOSLAM"] = [ "L6RA", "L6RB", "L8L", "L6L", "L4L" ]
		# self.osSignals["LOSLAE"] = [ "L4R", "L8L", "L6L", "L4L" ]

		# # Carlton OS
		# block=self.blocks["LOSCAW"]
		# self.routes["LRtL11D10"] = Route(self.screen, block, "LRtL11D10", "D10", [(30, 11), (31, 11), (32, 11), (33, 11), (34, 11), (35, 11)], "L11", [RESTRICTING, MAIN], ["LSw15"])

		# block=self.blocks["LOSCAM"]
		# self.routes["LRtL21D10"] = Route(self.screen, block, "LRtL21D10", "L21", [(30, 13), (31, 13), (32, 12), (33, 11), (34, 11), (35, 11)], "D10", [RESTRICTING, DIVERGING], ["LSw15"])
		# self.routes["LRtL21D20"] = Route(self.screen, block, "LRtL21D20", "L21", [(30, 13), (31, 13), (32, 13), (33, 13), (34, 13), (35, 13)], "D20", [MAIN, RESTRICTING], ["LSw15", "LSw17"])

		# block=self.blocks["LOSCAE"]
		# self.routes["LRtL31D20"] = Route(self.screen, block, "LRtL31D20", "L31", [(30, 15), (31, 15), (32, 15), (33, 14), (34, 13), (35, 13)], "D20", [DIVERGING, RESTRICTING], ["LSw17"])

		# self.signals["L18R"].AddPossibleRoutes("LOSCAW", [ "LRtL11D10" ])
		# self.signals["L18L"].AddPossibleRoutes("LOSCAW", [ "LRtL11D10" ])
		# self.signals["L18L"].AddPossibleRoutes("LOSCAM", [ "LRtL21D10" ])

		# self.signals["L16R"].AddPossibleRoutes("LOSCAM", [ "LRtL21D10", "LRtL21D20" ])

		# self.signals["L14R"].AddPossibleRoutes("LOSCAE", [ "LRtL31D20" ])
		# self.signals["L14L"].AddPossibleRoutes("LOSCAE", [ "LRtL31D20" ])
		# self.signals["L14L"].AddPossibleRoutes("LOSCAM", [ "LRtL21D20" ])

		# self.osSignals["LOSCAW"] = [ "L18R", "L18L" ]
		# self.osSignals["LOSCAM"] = [ "L16R", "L18L", "L14L" ]
		# self.osSignals["LOSCAE"] = [ "L14R", "L14L" ]

		return self.signals

	def DefineHandSwitches(self, tiles):
		self.handswitches = {}

		hs = HandSwitch(self, self.screen, self.frame, self.blocks["D21"], "DSw9.hand", (63, 14), tiles["handup"])
		self.blocks["D21"].AddHandSwitch(hs)
		self.handswitches["DSw9.hand"] = hs
		return self.handswitches

		