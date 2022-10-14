from district import District

from block import Block, OverSwitch, Route
from turnout import Turnout, SlipSwitch
from signal import Signal
from button import Button
from handswitch import HandSwitch

from constants import HyYdPt, RESTRICTING, MAIN, DIVERGING, SLOW, NORMAL, REVERSE, EMPTY, SLIPSWITCH

class Latham (District):
	def __init__(self, name, frame, screen):
		District.__init__(self, name, frame, screen)

	def DetermineRoute(self, blocks):
		s1 = 'N' if self.turnouts["LSw1"].IsNormal() else 'R'
		s3 = 'N' if self.turnouts["LSw3"].IsNormal() else 'R'
		s5 = 'N' if self.turnouts["LSw5"].IsNormal() else 'R'
		s7 = 'N' if self.turnouts["LSw7"].IsNormal() else 'R'
		s9 = 'N' if self.turnouts["LSw9"].IsNormal() else 'R'
		s15 = 'N' if self.turnouts["LSw15"].IsNormal() else 'R'
		s17 = 'N' if self.turnouts["LSw17"].IsNormal() else 'R'
		self.turnouts["LSw3"].SetLock("LSw9", s9=='R')
		self.turnouts["LSw9"].SetLock("LSw3", s3=='R')
		self.turnouts["LSw5"].SetLock("LSw7", s7=='R')
		self.turnouts["LSw7"].SetLock("LSw5", s5=='R')
		for bname in blocks:
			block = self.frame.GetBlockByName(bname)
			if bname == "OSLLAW":
				if s5+s7 == "NN":
					block.SetRoute(self.routes["LRtL10L11A"])
				elif s5+s7 == "RR":
					block.SetRoute(self.routes["LRtL10L11B"])
				elif s5+s7+s9 == "RNN":
					block.SetRoute(self.routes["LRtL10L21"])
				elif s5+s7+s9 == "RNR":
					block.SetRoute(self.routes["LRtL10L31"])
				else:
					block.SetRoute(None)

			elif bname == "OSLLAM":
				if s1+s3+s5+s7 == "NNNR":
					block.SetRoute(self.routes["LRtL20L11"])
				elif s1+s3+s5+s7+s9 == "NNNNN":
					block.SetRoute(self.routes["LRtL20L21"])
				elif s1+s3+s5+s7+s9 == "NNNNR":
					block.SetRoute(self.routes["LRtL20L31"])
				elif s1+s3+s5+s7 == "RNNR":
					block.SetRoute(self.routes["LRtP11L11"])
				elif s1+s3+s5+s7+s9 == "RNNNN":
					block.SetRoute(self.routes["LRtP11L21"])
				elif s1+s3+s5+s7+s9 == "RNNNR":
					block.SetRoute(self.routes["LRtP11L31"])
				else:
					block.SetRoute(None)
			
			elif bname == "OSLLAE":
				if s3+s5+s7 == "RNR":
					block.SetRoute(self.routes["LRtP21L11"])
				elif s3+s5+s7+s9 == "RNNN":
					block.SetRoute(self.routes["LRtP21L21"])
				elif s3+s9 == "NN":
					block.SetRoute(self.routes["LRtP21L31A"])
				elif s3+s5+s7+s9 == "RNNR":
					block.SetRoute(self.routes["LRtP21L31B"])
				else:
					block.SetRoute(None)

			elif bname == "OSLCAW":
				if s15 == "N":
					block.SetRoute(self.routes["LRtL11D10"])
				else:
					block.SetRoute(None)

			elif bname == "OSLCAM":
				if s15+s17 == "NN":
					block.SetRoute(self.routes["LRtL21D20"])
				elif s15 == "R":
					block.SetRoute(self.routes["LRtL21D10"])
				else:
					block.SetRoute(None)

			elif bname == "OSLCAE":
				if s17 == "R":
					block.SetRoute(self.routes["LRtL31D20"])
				else:
					block.SetRoute(None)

	def DefineBlocks(self, tiles):
		self.blocks = {}
		self.osBlocks = {}

		self.blocks["L10"] = Block(self, self.frame, "L10",
			[
				(tiles["horiznc"], HyYdPt,      (140, 11), False),
				(tiles["horiz"],   HyYdPt,      (141, 11), False),
				(tiles["horiznc"], HyYdPt,      (142, 11), False),
				(tiles["horiz"],   HyYdPt,      (143, 11), False),
				(tiles["horiznc"], HyYdPt,      (144, 11), False),
				(tiles["horiz"],   HyYdPt,      (145, 11), False),
				(tiles["horiznc"], HyYdPt,      (146, 11), False),
				(tiles["horiz"],   HyYdPt,      (147, 11), False),
				(tiles["horiznc"], HyYdPt,      (148, 11), False),
				(tiles["horiz"],   HyYdPt,      (149, 11), False),
				(tiles["horiznc"], HyYdPt,      (150, 11), False),
				(tiles["horiz"],   HyYdPt,      (151, 11), False),
				(tiles["horiznc"], HyYdPt,      (152, 11), False),
				(tiles["horiz"],   HyYdPt,      (153, 11), False),
				(tiles["horiznc"], HyYdPt,      (154, 11), False),
				(tiles["horiz"],   HyYdPt,      (155, 11), False),
				(tiles["horiznc"], HyYdPt,      (156, 11), False),
				(tiles["horiz"],   HyYdPt,      (157, 11), False),
				(tiles["horiznc"], HyYdPt,      (158, 11), False),
				(tiles["horiznc"], self.screen, (0, 11), False),
				(tiles["horiz"],   self.screen, (1, 11), False),
				(tiles["horiznc"], self.screen, (2, 11), False),
				(tiles["horiz"],   self.screen, (3, 11), False),
				(tiles["horiznc"], self.screen, (4, 11), False),
				(tiles["horiz"],   self.screen, (5, 11), False),
				(tiles["horiznc"], self.screen, (6, 11), False),
				(tiles["eobright"],self.screen, (7, 11), False),
			], False)
		self.blocks["L10"].AddStoppingBlock([
				(tiles["eobleft"], HyYdPt,      (137, 11), False),
				(tiles["horiznc"], HyYdPt,      (138, 11), False),
				(tiles["horiz"],   HyYdPt,      (139, 11), False),
			], False)
		self.blocks["L10"].AddTrainLoc(self.screen, (1, 11))
		self.blocks["L10"].AddTrainLoc(HyYdPt, (141, 11))

		self.blocks["L20"] = Block(self, self.frame, "L20",
			[
				(tiles["eobleft"], HyYdPt,      (137, 13), False),
				(tiles["horiznc"], HyYdPt,      (138, 13), False),
				(tiles["horiz"],   HyYdPt,      (139, 13), False),
				(tiles["horiznc"], HyYdPt,      (140, 13), False),
				(tiles["horiz"],   HyYdPt,      (141, 13), False),
				(tiles["horiznc"], HyYdPt,      (142, 13), False),
				(tiles["horiz"],   HyYdPt,      (143, 13), False),
				(tiles["horiznc"], HyYdPt,      (144, 13), False),
				(tiles["horiz"],   HyYdPt,      (145, 13), False),
				(tiles["horiznc"], HyYdPt,      (146, 13), False),
				(tiles["horiz"],   HyYdPt,      (147, 13), False),
				(tiles["horiznc"], HyYdPt,      (148, 13), False),
				(tiles["horiz"],   HyYdPt,      (149, 13), False),
				(tiles["horiznc"], HyYdPt,      (150, 13), False),
				(tiles["horiz"],   HyYdPt,      (151, 13), False),
				(tiles["horiznc"], HyYdPt,      (152, 13), False),
				(tiles["horiz"],   HyYdPt,      (153, 13), False),
				(tiles["horiznc"], HyYdPt,      (154, 13), False),
				(tiles["horiz"],   HyYdPt,      (155, 13), False),
				(tiles["horiznc"], HyYdPt,      (156, 13), False),
				(tiles["horiz"],   HyYdPt,      (157, 13), False),
				(tiles["horiznc"], HyYdPt,      (158, 13), False),
				(tiles["horiznc"], self.screen, (0, 13), False),
				(tiles["horiz"],   self.screen, (1, 13), False),
				(tiles["horiznc"], self.screen, (2, 13), False),
				(tiles["horiz"],   self.screen, (3, 13), False),
				(tiles["horiznc"], self.screen, (4, 13), False),
			], True)
		self.blocks["L20"].AddStoppingBlock([
				(tiles["horiz"],   self.screen, (5, 13), False),
				(tiles["horiznc"], self.screen, (6, 13), False),
				(tiles["eobright"],self.screen, (7, 13), False),
			], True)
		self.blocks["L20"].AddTrainLoc(self.screen, (1, 13))
		self.blocks["L20"].AddTrainLoc(HyYdPt, (141, 13))

		self.blocks["L11"] = Block(self, self.frame, "L11",
			[
				(tiles["horiznc"],   self.screen, (24, 11), False),
				(tiles["horiz"],     self.screen, (25, 11), False),
				(tiles["horiznc"],   self.screen, (26, 11), False),
				(tiles["horiz"],     self.screen, (27, 11), False),
				(tiles["horiznc"],   self.screen, (28, 11), False),
				(tiles["eobright"],  self.screen, (29, 11), False),
			], False)
		self.blocks["L11"].AddStoppingBlock([
				(tiles["eobleft"],   self.screen, (21, 11), False),
				(tiles["horiznc"],   self.screen, (22, 11), False),
			], False)
		self.blocks["L11"].AddTrainLoc(self.screen, (24, 11))

		self.blocks["L21"] = Block(self, self.frame, "L21",
			[
				(tiles["horiznc"],   self.screen, (24, 13), False),
				(tiles["horiz"],     self.screen, (25, 13), False),
				(tiles["horiznc"],   self.screen, (26, 13), False),
			], False)
		self.blocks["L21"].AddStoppingBlock([
				(tiles["eobleft"],   self.screen, (21, 13), False),
				(tiles["horiznc"],   self.screen, (22, 13), False),
				(tiles["horiz"],     self.screen, (23, 13), False),
			], False)
		self.blocks["L21"].AddStoppingBlock([
				(tiles["horiz"],     self.screen, (27, 13), False),
				(tiles["horiznc"],   self.screen, (28, 13), False),
				(tiles["eobright"],  self.screen, (29, 13), False),
			], True)
		self.blocks["L21"].AddTrainLoc(self.screen, (24, 13))


		self.blocks["L31"] = Block(self, self.frame, "L31",
			[
				(tiles["eobleft"],   self.screen, (21, 15), False),
				(tiles["horiznc"],   self.screen, (22, 15), False),
				(tiles["horiz"],     self.screen, (23, 15), False),
				(tiles["horiznc"],   self.screen, (24, 15), False),
				(tiles["horiz"],     self.screen, (25, 15), False),
				(tiles["horiznc"],   self.screen, (26, 15), False),
			], True)
		self.blocks["L31"].AddStoppingBlock([
				(tiles["horiznc"],   self.screen, (28, 15), False),
				(tiles["eobright"],  self.screen, (29, 15), False),
			], True)
		self.blocks["L31"].AddTrainLoc(self.screen, (22, 15))

		self.blocks["OSLLAW"] = OverSwitch(self, self.frame, "OSLLAW", 
			[
				(tiles["eobleft"],   self.screen, (8, 11), False),
				(tiles["horiznc"],   self.screen, (9, 11), False),
				(tiles["horiz"],     self.screen, (10, 11), False),
				(tiles["horiznc"],   self.screen, (11, 11), False),
				(tiles["horiz"],     self.screen, (12, 11), False),
				(tiles["horiz"],     self.screen, (14, 11), False),
				(tiles["horiznc"],   self.screen, (15, 11), False),
				(tiles["horiz"],     self.screen, (16, 11), False),
				(tiles["horiznc"],   self.screen, (17, 11), False),
				(tiles["horiznc"],   self.screen, (19, 11), False),
				(tiles["eobright"],  self.screen, (20, 11), False),
				(tiles["diagright"], self.screen, (14, 12), False),
				(tiles["diagleft"],  self.screen, (17, 12), False),
				(tiles["horiz"],     self.screen, (18, 13), False),
				(tiles["horiznc"],   self.screen, (19, 13), False),
				(tiles["eobright"],  self.screen, (20, 13), False),
				(tiles["diagright"], self.screen, (18, 14), False),
				(tiles["eobright"],  self.screen, (20, 15), False),
			],
			False)

		self.blocks["OSLLAM"] = OverSwitch(self, self.frame, "OSLLAM", 
			[
				(tiles["eobleft"],   self.screen, (8, 13), False),
				(tiles["horiznc"],   self.screen, (9, 13), False),
				(tiles["horiz"],     self.screen, (10, 13), False),
				(tiles["horiz"],     self.screen, (12, 13), False),
				(tiles["horiznc"],   self.screen, (13, 13), False),
				(tiles["horiz"],     self.screen, (18, 13), False),
				(tiles["horiznc"],   self.screen, (19, 13), False),
				(tiles["eobright"],  self.screen, (20, 13), False),
				(tiles["diagleft"],  self.screen, (17, 12), False),
				(tiles["horiznc"],   self.screen, (19, 11), False),
				(tiles["eobright"],  self.screen, (20, 11), False),
				(tiles["diagright"], self.screen, (18, 14), False),
				(tiles["eobright"],  self.screen, (20, 15), False),
				(tiles["eobleft"],   self.screen, (8, 15), False),
				(tiles["turnleftright"], self.screen, (9, 15), False),
				(tiles["diagleft"],   self.screen, (10, 14), False),
			],
			False)

		self.blocks["OSLLAE"] = OverSwitch(self, self.frame, "OSLLAE", 
			[
				(tiles["eobleft"],   self.screen, (8, 17), False),
				(tiles["horiznc"],   self.screen, (9, 17), False),
				(tiles["turnleftright"], self.screen, (10, 17), False),
				(tiles["diagleft"],   self.screen, (11, 16), False),
				(tiles["horiznc"],   self.screen, (13, 15), False),
				(tiles["horiz"],     self.screen, (14, 15), False),
				(tiles["horiznc"],   self.screen, (15, 15), False),
				(tiles["horiz"],     self.screen, (16, 15), False),
				(tiles["horiznc"],   self.screen, (17, 15), False),
				(tiles["horiz"],     self.screen, (18, 15), False),
				(tiles["eobright"],  self.screen, (20, 15), False),
				(tiles["diagleft"],  self.screen, (13, 14), False),
				(tiles["horiz"],     self.screen, (18, 13), False),
				(tiles["horiznc"],   self.screen, (19, 13), False),
				(tiles["eobright"],  self.screen, (20, 13), False),
				(tiles["diagleft"],  self.screen, (17, 12), False),
				(tiles["horiznc"],   self.screen, (19, 11), False),
				(tiles["eobright"],  self.screen, (20, 11), False),
				(tiles["diagright"], self.screen, (18, 14), False),
				(tiles["eobright"],  self.screen, (20, 15), False),
			],
			True)

		self.blocks["OSLCAW"] = OverSwitch(self, self.frame, "OSLCAW", 
			[
				(tiles["eobleft"],   self.screen, (30, 11), False),
				(tiles["horiznc"],   self.screen, (31, 11), False),
				(tiles["horiz"],     self.screen, (32, 11), False),
				(tiles["horiz"],     self.screen, (34, 11), False),
				(tiles["eobright"],  self.screen, (35, 11), False),
			], 
			False)

		self.blocks["OSLCAM"] = OverSwitch(self, self.frame, "OSLCAM", 
			[
				(tiles["eobleft"],   self.screen, (30, 13), False),
				(tiles["horiz"],     self.screen, (32, 13), False),
				(tiles["horiznc"],   self.screen, (33, 13), False),
				(tiles["eobright"],  self.screen, (35, 13), False),
				(tiles["diagleft"],  self.screen, (32, 12), False),
				(tiles["horiz"],     self.screen, (34, 11), False),
				(tiles["eobright"],  self.screen, (35, 11), False),
			], 
			False)

		self.blocks["OSLCAE"] = OverSwitch(self, self.frame, "OSLCAE", 
			[
				(tiles["eobleft"],   self.screen, (30, 15), False),
				(tiles["horiznc"],   self.screen, (31, 15), False),
				(tiles["turnleftright"], self.screen, (32, 15), False),
				(tiles["diagleft"],  self.screen, (33, 14), False),
				(tiles["eobright"],  self.screen, (35, 13), False),
			], 
			True)

		self.osBlocks["OSLLAW"] = [ "L10", "L11", "L21", "L31" ]
		self.osBlocks["OSLLAM"] = [ "L20", "P11", "L11", "L21", "L31" ]
		self.osBlocks["OSLLAE"] = [ "P21", "L11", "L21", "L31" ]

		self.osBlocks["OSLCAW"] = [ "L11", "D10" ]
		self.osBlocks["OSLCAM"] = [ "L21", "D10", "D20" ]
		self.osBlocks["OSLCAE"] = [ "L31", "D20" ]

		return self.blocks

	def DefineTurnouts(self, tiles, blocks):
		self.turnouts = {}

		toList = [
			[ "LSw1",  "toleftleft",   ["OSLLAM"], (11, 13) ],
			[ "LSw3",  "toleftleft",   ["OSLLAM", "OSLLAE"], (14, 13) ],
			[ "LSw3b", "torightupinv", ["OSLLAM", "OSLLAE"], (12, 15) ],
			[ "LSw5",  "torightright", ["OSLLAW"], (13, 11) ],
			[ "LSw5b", "torightleft",  ["OSLLAW", "OSLLAM", "OSLLAE"], (15, 13) ],
			[ "LSw7",  "toleftleft",   ["OSLLAW", "OSLLAM", "OSLLAE"], (18, 11) ],
			[ "LSw7b", "toleftright",  ["OSLLAW", "OSLLAM", "OSLLAE"], (16, 13) ],
			[ "LSw9",  "torightright", ["OSLLAW", "OSLLAM", "OSLLAE"], (17, 13) ],
			[ "LSw9b", "torightleft",  ["OSLLAW", "OSLLAM", "OSLLAE"], (19, 15) ],

			[ "LSw15",  "toleftleft",  ["OSLCAW", "OSLCAM"], (33, 11) ],
			[ "LSw15b", "toleftright", ["OSLCAM"], (31, 13) ],
			[ "LSw17",  "toleftleft",  ["OSLCAM", "OSLCAE"], (34, 13) ],

			[ "LSw11", "toleftright",  ["L11"], (23, 11) ],
			[ "LSw13", "toleftleft",   ["L31"], (27, 15) ],
		]

		for tonm, tileSet, blks, pos in toList:
			trnout = Turnout(self, self.frame, tonm, self.screen, tiles[tileSet], pos)
			for blknm in blks:
				blocks[blknm].AddTurnout(trnout)
				trnout.AddBlock(blknm)
			self.turnouts[tonm] = trnout

		self.turnouts["LSw3"].SetPairedTurnout(self.turnouts["LSw3b"])
		self.turnouts["LSw5"].SetPairedTurnout(self.turnouts["LSw5b"])
		self.turnouts["LSw7"].SetPairedTurnout(self.turnouts["LSw7b"])
		self.turnouts["LSw9"].SetPairedTurnout(self.turnouts["LSw9b"])
		self.turnouts["LSw15"].SetPairedTurnout(self.turnouts["LSw15b"])

		self.turnouts["LSw11"].SetDisabled(True)
		self.turnouts["LSw13"].SetDisabled(True)

		return self.turnouts

	def DefineSignals(self, tiles):
		self.signals = {}

		sigList = [
			[ "L8R",  True,    "right", (8, 12) ],
			[ "L6RA", True,    "right", (8, 14) ],
			[ "L6RB", True,    "right", (8, 16) ],
			[ "L4R",  True,    "right", (8, 18) ],

			[ "L8L",  False,   "left",  (20, 10) ],
			[ "L6L",  False,   "left",  (20, 12) ],
			[ "L4L",  False,   "left",  (20, 14) ],

			[ "L18R", True,    "right", (30, 12) ],
			[ "L16R", True,    "right", (30, 14) ],
			[ "L14R", True,    "right", (30, 16) ],

			[ "L18L", False,   "left",  (35, 10) ],
			[ "L14L", False,   "left",  (35, 12) ]
		]
		for signm, east, tileSet, pos in sigList:
			self.signals[signm]  = Signal(self, self.screen, self.frame, signm, east, pos, tiles[tileSet])  

		self.routes = {}
		self.osSignals = {}

		# latham OS
		block = self.blocks["OSLLAW"]
		self.routes["LRtL10L11A"] = Route(self.screen, block, "LRtL10L11A", "L11", [ (8, 11), (9, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 11), (15, 11), (16, 11), (17, 11), (18, 11), (19, 11), (20, 11) ], "L10", [RESTRICTING, MAIN], ["LSw5", "LSw7"])
		self.routes["LRtL10L11B"] = Route(self.screen, block, "LRtL10L11B", "L11", [ (8, 11), (9, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 12), (15, 13), (16, 13), (17, 12), (18, 11), (19, 11), (20, 11) ], "L10", [RESTRICTING, RESTRICTING], ["LSw5", "LSw7"])
		self.routes["LRtL10L21"] = Route(self.screen, block, "LRtL10L21", "L21",   [ (8, 11), (9, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 12), (15, 13), (16, 13), (17, 13), (18, 13), (19, 13), (20, 13) ], "L10", [RESTRICTING, DIVERGING], ["LSw5", "LSw7", "LSw9"])
		self.routes["LRtL10L31"] = Route(self.screen, block, "LRtL10L31", "L31",   [ (8, 11), (9, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 12), (15, 13), (16, 13), (17, 13), (18, 14), (19, 15), (20, 15) ], "L10", [RESTRICTING, DIVERGING], ["LSw5", "LSw7", "LSw9"])

		block=self.blocks["OSLLAM"]
		self.routes["LRtL20L11"] = Route(self.screen, block, "LRtL20L11", "L11", [ (8, 13), (9, 13), (10, 13), (11, 13), (12, 13), (13, 13), (14, 13), (15, 13), (16, 13), (17, 12), (18, 11), (19, 11), (20, 11) ], "L20", [RESTRICTING, RESTRICTING], ["LSw1", "LSw3", "LSw5", "LSw7"])
		self.routes["LRtP11L11"] = Route(self.screen, block, "LRtP11L11", "L11", [ (8, 15), (9, 15), (10, 14), (11, 13), (12, 13), (13, 13), (14, 13), (15, 13), (16, 13), (17, 12), (18, 11), (19, 11), (20, 11) ], "P11", [RESTRICTING, DIVERGING], ["LSw1", "LSw3", "LSw5", "LSw7"])
		self.routes["LRtL20L21"] = Route(self.screen, block, "LRtL20L21", "L21", [ (8, 13), (9, 13), (10, 13), (11, 13), (12, 13), (13, 13), (14, 13), (15, 13), (16, 13), (17, 13), (18, 13), (19, 13), (20, 13) ], "L20", [MAIN, RESTRICTING], ["LSw1", "LSw3", "LSw5", "LSw7", "LSw9"])
		self.routes["LRtP11L21"] = Route(self.screen, block, "LRtP11L21", "L21", [ (8, 15), (9, 15), (10, 14), (11, 13), (12, 13), (13, 13), (14, 13), (15, 13), (16, 13), (17, 13), (18, 13), (19, 13), (20, 13) ], "P11", [RESTRICTING, DIVERGING], ["LSw1", "LSw3", "LSw5", "LSw7", "LSw9"])
		self.routes["LRtL20L31"] = Route(self.screen, block, "LRtL20L31", "L31", [ (8, 13), (9, 13), (10, 13), (11, 13), (12, 13), (13, 13), (14, 13), (15, 13), (16, 13), (17, 13), (18, 14), (19, 15), (20, 15) ], "L20", [DIVERGING, RESTRICTING], ["LSw1", "LSw3", "LSw5", "LSw7", "LSw9"])
		self.routes["LRtP11L31"] = Route(self.screen, block, "LRtP11L31", "L31", [ (8, 15), (9, 15), (10, 14), (11, 13), (12, 13), (13, 13), (14, 13), (15, 13), (16, 13), (17, 13), (18, 14), (19, 15), (20, 15) ], "P11", [RESTRICTING, RESTRICTING], ["LSw1", "LSw3", "LSw5", "LSw7", "LSw9"])

		block=self.blocks["OSLLAE"]
		self.routes["LRtP21L11"] = Route(self.screen, block, "LRtP21L11", "P21", [ (8, 17), (9, 17), (10, 17), (11, 16), (12, 15), (13, 14), (14, 13), (15, 13), (16, 13), (17, 12), (18, 11), (19, 11), (20, 11) ], "L11", [RESTRICTING, RESTRICTING], ["LSw3", "LSw5", "LSw7"])
		self.routes["LRtP21L21"] = Route(self.screen, block, "LRtP21L21", "P21", [ (8, 17), (9, 17), (10, 17), (11, 16), (12, 15), (13, 14), (14, 13), (15, 13), (16, 13), (17, 13), (18, 13), (19, 13), (20, 13) ], "L21", [RESTRICTING, RESTRICTING], ["LSw3", "LSw5", "LSw7", "LSw9"])
		self.routes["LRtP21L31A"] = Route(self.screen, block, "LRtP21L31A", "P21", [ (8, 17), (9, 17), (10, 17), (11, 16), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), (18, 15), (19, 15), (20, 15) ], "L31", [MAIN, RESTRICTING], ["LSw3", "LSw9"])
		self.routes["LRtP21L31B"] = Route(self.screen, block, "LRtP21L31B", "P21", [ (8, 17), (9, 17), (10, 17), (11, 16), (12, 15), (13, 14), (14, 13), (15, 13), (16, 13), (17, 13), (18, 14), (19, 15), (20, 15) ], "L31", [RESTRICTING, RESTRICTING], ["LSw3", "LSw5", "LSw7", "LSw9"])

		self.signals["L8R"].AddPossibleRoutes("OSLLAW", [ "LRtL10L11A", "LRtL10L11B", "LRtL10L21", "LRtL10L31" ])
		self.signals["L8L"].AddPossibleRoutes("OSLLAW", [ "LRtL10L11A", "LRtL10L11B" ])
		self.signals["L8L"].AddPossibleRoutes("OSLLAM", [ "LRtL20L11", "LRtP11L11" ])
		self.signals["L8L"].AddPossibleRoutes("OSLLAE", [ "LRtP21L11" ])

		self.signals["L6RA"].AddPossibleRoutes("OSLLAM", [ "LRtL20L11", "LRtL20L21", "LRtL20L31" ])
		self.signals["L6RB"].AddPossibleRoutes("OSLLAM", [ "LRtP11L11", "LRtP11L21", "LRtP11L31" ])
		self.signals["L6L"].AddPossibleRoutes("OSLLAW", [ "LRtL10L21" ])
		self.signals["L6L"].AddPossibleRoutes("OSLLAM", [ "LRtL20L21", "LRtP11L21" ])
		self.signals["L6L"].AddPossibleRoutes("OSLLAE", [ "LRtP21L21" ])

		self.signals["L4R"].AddPossibleRoutes("OSLLAE", [ "LRtP21L11", "LRtP21L21", "LRtP21L31A", "LRtP21L31B" ])
		self.signals["L4L"].AddPossibleRoutes("OSLLAW", [ "LRtL10L31" ])
		self.signals["L4L"].AddPossibleRoutes("OSLLAM", [ "LRtL20L31", "LRtP11L31" ])
		self.signals["L4L"].AddPossibleRoutes("OSLLAE", [ "LRtP21L31A", "LRtP21L31B" ])

		self.osSignals["OSLLAW"] = [ "L8R", "L8L", "L6L", "L4L" ]
		self.osSignals["OSLLAM"] = [ "L6RA", "L6RB", "L8L", "L6L", "L4L" ]
		self.osSignals["OSLLAE"] = [ "L4R", "L8L", "L6L", "L4L" ]

		# Carlton OS
		block=self.blocks["OSLCAW"]
		self.routes["LRtL11D10"] = Route(self.screen, block, "LRtL11D10", "D10", [(30, 11), (31, 11), (32, 11), (33, 11), (34, 11), (35, 11)], "L11", [RESTRICTING, MAIN], ["LSw15"])

		block=self.blocks["OSLCAM"]
		self.routes["LRtL21D10"] = Route(self.screen, block, "LRtL21D10", "D10", [(30, 13), (31, 13), (32, 12), (33, 11), (34, 11), (35, 11)], "L21", [RESTRICTING, DIVERGING], ["LSw15"])
		self.routes["LRtL21D20"] = Route(self.screen, block, "LRtL21D20", "D20", [(30, 13), (31, 13), (32, 13), (33, 13), (34, 13), (35, 13)], "L21", [MAIN, RESTRICTING], ["LSw15", "LSw17"])

		block=self.blocks["OSLCAE"]
		self.routes["LRtL31D20"] = Route(self.screen, block, "LRtL31D20", "L31", [(30, 15), (31, 15), (32, 15), (33, 14), (34, 13), (35, 13)], "D20", [DIVERGING, RESTRICTING], ["LSw17"])

		self.signals["L18R"].AddPossibleRoutes("OSLCAW", [ "LRtL11D10" ])
		self.signals["L18L"].AddPossibleRoutes("OSLCAW", [ "LRtL11D10" ])
		self.signals["L18L"].AddPossibleRoutes("OSLCAM", [ "LRtL21D10" ])

		self.signals["L16R"].AddPossibleRoutes("OSLCAM", [ "LRtL21D10", "LRtL21D20" ])

		self.signals["L14R"].AddPossibleRoutes("OSLCAE", [ "LRtL31D20" ])
		self.signals["L14L"].AddPossibleRoutes("OSLCAE", [ "LRtL31D20" ])
		self.signals["L14L"].AddPossibleRoutes("OSLCAM", [ "LRtL21D20" ])

		self.osSignals["OSLCAW"] = [ "L18R", "L18L" ]
		self.osSignals["OSLCAM"] = [ "L16R", "L18L", "L14L" ]
		self.osSignals["OSLCAE"] = [ "L14R", "L14L" ]

		return self.signals

	def DefineHandSwitches(self, tiles):
		self.handswitches = {}

		hs = HandSwitch(self, self.screen, self.frame, self.blocks["L11"], "LSw11.hand", (23, 10), tiles["handdown"])
		self.blocks["L11"].AddHandSwitch(hs)
		self.handswitches["LSw11.hand"] = hs

		hs = HandSwitch(self, self.screen, self.frame, self.blocks["L31"], "LSw13.hand", (27, 16), tiles["handup"])
		self.blocks["L31"].AddHandSwitch(hs)
		self.handswitches["LSw13.hand"] = hs
		return self.handswitches

		