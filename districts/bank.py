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
		pass
		# s1 = 'N' if self.turnouts["LSw1"].IsNormal() else 'R'
		# s3 = 'N' if self.turnouts["LSw3"].IsNormal() else 'R'
		# s5 = 'N' if self.turnouts["LSw5"].IsNormal() else 'R'
		# s7 = 'N' if self.turnouts["LSw7"].IsNormal() else 'R'
		# s9 = 'N' if self.turnouts["LSw9"].IsNormal() else 'R'
		# s15 = 'N' if self.turnouts["LSw15"].IsNormal() else 'R'
		# s17 = 'N' if self.turnouts["LSw17"].IsNormal() else 'R'
		# self.turnouts["LSw3"].SetLock("LSw9", s9=='R', refresh=True)
		# self.turnouts["LSw3b"].SetLock("LSw9", s9=='R', refresh=True)
		# self.turnouts["LSw9"].SetLock("LSw3", s3=='R', refresh=True)
		# self.turnouts["LSw9b"].SetLock("LSw3", s3=='R', refresh=True)
		# self.turnouts["LSw5"].SetLock("LSw7", s7=='R', refresh=True)
		# self.turnouts["LSw5b"].SetLock("LSw7", s7=='R', refresh=True)
		# self.turnouts["LSw7"].SetLock("LSw5", s5=='R', refresh=True)
		# self.turnouts["LSw7b"].SetLock("LSw5", s5=='R', refresh=True)
		# for block in blocks:
		# 	bname = block.GetName()
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

		# 	elif bname == "LOSLAM":
		# 		if s1+s3+s5+s7 == "NNNR":
		# 			block.SetRoute(self.routes["LRtL20L11"])
		# 		elif s1+s3+s5+s7+s9 == "NNNNN":
		# 			block.SetRoute(self.routes["LRtL20L21"])
		# 		elif s1+s3+s5+s7+s9 == "NNNNR":
		# 			block.SetRoute(self.routes["LRtL20L31"])
		# 		elif s1+s3+s5+s7 == "RNNR":
		# 			block.SetRoute(self.routes["LRtP11L11"])
		# 		elif s1+s3+s5+s7+s9 == "RNNNN":
		# 			block.SetRoute(self.routes["LRtP11L21"])
		# 		elif s1+s3+s5+s7+s9 == "RNNNR":
		# 			block.SetRoute(self.routes["LRtP11L31"])
		# 		else:
		# 			block.SetRoute(None)
			
		# 	elif bname == "LOSLAE":
		# 		if s3+s5+s7 == "RNR":
		# 			block.SetRoute(self.routes["LRtP21L11"])
		# 		elif s3+s5+s7+s9 == "RNNN":
		# 			block.SetRoute(self.routes["LRtP21L21"])
		# 		elif s3+s9 == "NN":
		# 			block.SetRoute(self.routes["LRtP21L31A"])
		# 		elif s3+s5+s7+s9 == "RNNR":
		# 			block.SetRoute(self.routes["LRtP21L31B"])
		# 		else:
		# 			block.SetRoute(None)

		# 	elif bname == "LOSCAW":
		# 		if s15 == "N":
		# 			block.SetRoute(self.routes["LRtL11D10"])
		# 		else:
		# 			block.SetRoute(None)

		# 	elif bname == "LOSCAM":
		# 		if s15+s17 == "NN":
		# 			block.SetRoute(self.routes["LRtL21D20"])
		# 		elif s15 == "R":
		# 			block.SetRoute(self.routes["LRtL21D10"])
		# 		else:
		# 			block.SetRoute(None)

		# 	elif bname == "LOSCAE":
		# 		if s17 == "R":
		# 			block.SetRoute(self.routes["LRtL31D20"])
		# 		else:
		# 			block.SetRoute(None)
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
			[ "CSw17",  "torightright",  ["BOSE"], (71, 13) ],
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
			[ "C18LB",  RegAspects, True,    "right", (68, 12) ],
			[ "C18LA",  RegAspects, True,    "rightlong", (68, 14) ],
			[ "C18R",   RegAspects, False,   "leftlong", (72, 12) ],

			[ "C22L",   RegAspects, True,    "right", (53, 12) ],
			[ "C22R",   RegAspects, False,   "leftlong", (57, 10) ],

			[ "C24L",   RegAspects, True,    "rightlong", (53, 14) ],
			[ "C24R",   RegAspects, False,   "leftlong", (57, 12) ],
		]
		for signm, atype, east, tileSet, pos in sigList:
			self.signals[signm]  = Signal(self, self.screen, self.frame, signm, atype, east, pos, tiles[tileSet])  

		blockSigs = {
			# # which signals govern stopping sections, west and east
			"B11": ("C22R",  None),
			"B20": (None,    "C24L"),
			"B21": ("C24R",  "C18LA"),
		}

		for blknm, siglist in blockSigs.items():
			self.blocks[blknm].SetSignals(siglist)

		self.routes = {}
		self.osSignals = {}

		# latham OS
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
