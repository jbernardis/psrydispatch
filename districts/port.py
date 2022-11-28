from district import District

from block import Block, OverSwitch, Route
from turnout import Turnout, SlipSwitch
from signal import Signal
from handswitch import HandSwitch

from constants import LaKr, RESTRICTING, MAIN, DIVERGING, RegAspects, AdvAspects


class Port (District):
	def __init__(self, name, frame, screen):
		District.__init__(self, name, frame, screen)

	def DetermineRoute(self, blocks):
		s11 = 'N' if self.turnouts["PBSw11"].IsNormal() else 'R'
		s13 = 'N' if self.turnouts["PBSw13"].IsNormal() else 'R'
		self.turnouts["PBSw11"].SetLock("PBSw13", s13 == 'R', refresh=True)
		self.turnouts["PBSw11b"].SetLock("PBSw13", s13 == 'R', refresh=True)
		self.turnouts["PBSw13"].SetLock("PBSw11", s11 == 'R', refresh=True)
		self.turnouts["PBSw13b"].SetLock("PBSw11", s11 == 'R', refresh=True)

		for block in blocks:
			bname = block.GetName()
			if bname == "POSCJ1":
				if s11+s13 == "NN":
					block.SetRoute(self.routes["PRtP31P32"])
				elif s11+s13 == "RN":
					block.SetRoute(self.routes["PRtP31P42"])
				else:
					block.SetRoute(None)

			elif bname == "POSCJ2":
				print("11: %s   13: %s" % (s11, s13))
				if s11+s13 == "NN":
					block.SetRoute(self.routes["PRtP41P42"])
				elif s11+s13 == "NR":
					block.SetRoute(self.routes["PRtP41P32"])
				else:
					block.SetRoute(None)

	def DefineBlocks(self, tiles):
		self.blocks = {}
		self.osBlocks = {}
		self.blocks["P31"] = Block(self, self.frame, "P31",
			[
				(tiles["horiznc"],  self.screen, (129, 33), False),
				(tiles["horiz"],    self.screen, (130, 33), False),
				(tiles["horiznc"],  self.screen, (131, 33), False),
				(tiles["horiz"],    self.screen, (132, 33), False),
			], False)
		self.blocks["P31"].AddTrainLoc(self.screen, (131, 33))
		self.blocks["P31"].AddStoppingBlock([
				(tiles["eobleft"],  self.screen, (127, 33), False),
				(tiles["horiz"],    self.screen, (128, 33), False),
			], True)
		self.blocks["P31"].AddStoppingBlock([
				(tiles["horiznc"],  self.screen, (133, 33), False),
				(tiles["eobright"], self.screen, (134, 33), False),
			], False)

		self.blocks["P41"] = Block(self, self.frame, "P41",
			[
				(tiles["horiz"],    self.screen, (130, 35), False),
				(tiles["horiznc"],  self.screen, (131, 35), False),
				(tiles["horiz"],    self.screen, (132, 35), False),
			], False)
		self.blocks["P41"].AddTrainLoc(self.screen, (131, 35))
		self.blocks["P41"].AddStoppingBlock([
				(tiles["eobleft"],  self.screen, (127, 35), False),
				(tiles["horiz"],    self.screen, (128, 35), False),
			], True)
		self.blocks["P41"].AddStoppingBlock([
				(tiles["horiznc"],  self.screen, (133, 35), False),
				(tiles["eobright"], self.screen, (134, 35), False),
			], False)

		self.blocks["P32"] = Block(self, self.frame, "P32",
			[
				(tiles["diagleft"], self.screen, (146, 31), False),
				(tiles["diagleft"], self.screen, (147, 30), False),
				(tiles["turnleftleft"], self.screen, (148, 29), False),
				(tiles["horiznc"],  self.screen, (149, 29), False),
				(tiles["horiz"],    self.screen, (150, 29), False),
				(tiles["horiznc"],  self.screen, (151, 29), False),
				(tiles["horiz"],    self.screen, (152, 29), False),
				(tiles["horiznc"],  self.screen, (153, 29), False),

				(tiles["eobleft"],  LaKr,        (110, 21), False),
				(tiles["horiznc"],  LaKr,        (111, 21), True),
				(tiles["horiz"],    LaKr,        (112, 21), True),
				(tiles["horiznc"],  LaKr,        (113, 21), True),
				(tiles["horiz"],    LaKr,        (114, 21), True),
				(tiles["horiznc"],  LaKr,        (115, 21), True),
				(tiles["horiz"],    LaKr,        (116, 21), True),
			], False)
		self.blocks["P32"].AddTrainLoc(self.screen, (149, 29))
		self.blocks["P32"].AddTrainLoc(LaKr, (113, 21))
		self.blocks["P32"].AddStoppingBlock([
				(tiles["eobleft"],  self.screen, (143, 33), False),
				(tiles["turnleftright"], self.screen, (144, 33), False),
				(tiles["diagleft"], self.screen, (145, 32), False),
			], True)
		self.blocks["P32"].AddStoppingBlock([
				(tiles["horiznc"],  LaKr,        (117, 21), True),
				(tiles["horiz"],    LaKr,        (118, 21), True),
				(tiles["horiznc"],  LaKr,        (119, 21), True),
			], False)

		self.blocks["P42"] = Block(self, self.frame, "P42",
			[
				(tiles["horiznc"],  self.screen, (147, 35), False),
				(tiles["horiz"],    self.screen, (148, 35), False),
				(tiles["horiz"],    self.screen, (150, 35), False),
				(tiles["horiznc"],  self.screen, (151, 35), False),
				(tiles["horiz"],    self.screen, (152, 35), False),
				(tiles["horiznc"],  self.screen, (153, 35), False),

				(tiles["horiznc"],  LaKr,        (109, 15), False),
				(tiles["horiz"],    LaKr,        (110, 15), False),
			], False)
		self.blocks["P42"].AddTrainLoc(self.screen, (151, 35))
		self.blocks["P42"].AddTrainLoc(LaKr, (110, 15))
		self.blocks["P42"].AddStoppingBlock([
				(tiles["eobleft"],  self.screen, (143, 35), False),
				(tiles["horiz"],    self.screen, (144, 35), False),
				(tiles["horiz"],    self.screen, (146, 35), False),
			], True)
		self.blocks["P42"].AddStoppingBlock([
				(tiles["horiznc"],  LaKr,        (111, 15), False),
				(tiles["horiz"],    LaKr,        (112, 15), False),
				(tiles["eobright"], LaKr,        (112, 15), False),
			], False)

		self.blocks["POSCJ1"] = OverSwitch(self, self.frame, "POSCJ1",
			[
				(tiles["eobleft"],  self.screen, (135, 33), False),
				(tiles["horiznc"],  self.screen, (137, 33), False),
				(tiles["horiz"],    self.screen, (138, 33), False),
				(tiles["horiznc"],  self.screen, (139, 33), False),
				(tiles["horiz"],    self.screen, (140, 33), False),
				(tiles["eobright"], self.screen, (142, 33), False),
				(tiles["diagright"],self.screen, (137, 34), False),
				(tiles["horiz"],    self.screen, (140, 35), False),
				(tiles["horiznc"],  self.screen, (141, 35), False),
				(tiles["eobright"], self.screen, (142, 35), False),
			], False)

		self.blocks["POSCJ2"] = OverSwitch(self, self.frame, "POSCJ2",
			[
				(tiles["eobleft"],  self.screen, (135, 35), False),
				(tiles["horiz"],    self.screen, (136, 35), False),
				(tiles["horiznc"],  self.screen, (137, 35), False),
				(tiles["horiz"],    self.screen, (140, 35), False),
				(tiles["horiznc"],  self.screen, (141, 35), False),
				(tiles["eobright"], self.screen, (142, 35), False),
				(tiles["diagleft"], self.screen, (140, 34), False),
				(tiles["eobright"], self.screen, (142, 35), False),
			], False)

		self.osBlocks["POSCJ1"] = [ "P31", "P32", "P42" ]
		self.osBlocks["POSCJ2"] = [ "P41", "P32", "P42" ]

		return self.blocks, self.osBlocks

	def DefineTurnouts(self, tiles, blocks):
		self.turnouts = {}
		toList = [
			[ "PBSw11",  "torightright", ["POSCJ1", "POSCJ2"], (136, 33) ],
			[ "PBSw11b", "torightleft",  ["POSCJ1", "POSCJ2"], (138, 35) ],
			[ "PBSw13",  "toleftright",  ["POSCJ1", "POSCJ2"], (139, 35) ],
			[ "PBSw13b", "toleftleft",   ["POSCJ1", "POSCJ2"], (141, 33) ],

			[ "PBSw5",   "torightright", ["P41"], (129, 35) ],
			[ "PBSw15a", "toleftright",  ["P42"], (145, 35) ],
			[ "PBSw15b", "toleftleft",   ["P42"], (149, 35) ],
		]

		for tonm, tileSet, blks, pos in toList:
			print(str(blks))
			trnout = Turnout(self, self.frame, tonm, self.screen, tiles[tileSet], pos)
			for blknm in blks:
				print("(%s)" % blknm)
				blocks[blknm].AddTurnout(trnout)
				trnout.AddBlock(blknm)
			#  TODO
			# trnout.SetDisabled(True)
			self.turnouts[tonm] = trnout

		self.turnouts["PBSw11"].SetPairedTurnout(self.turnouts["PBSw11b"])
		self.turnouts["PBSw13"].SetPairedTurnout(self.turnouts["PBSw13b"])

		return self.turnouts

	def DefineSignals(self, tiles):
		self.signals = {}
		sigList = [
			[ "PB14R",  RegAspects, True,    "rightlong", (135, 34) ],
			[ "PB12R",  RegAspects, True,    "rightlong", (135, 36) ],

			[ "PB14L",  RegAspects, False,   "leftlong",  (142, 32) ],
			[ "PB12L",  RegAspects, False,   "leftlong",  (142, 34) ],
		]
		for signm, atype, east, tileSet, pos in sigList:
			sig  = Signal(self, self.screen, self.frame, signm, atype, east, pos, tiles[tileSet])
			#  TODO
			# sig.SetDisabled(True)
			self.signals[signm]  = sig

		blockSigs = {
			# which signals govern stopping sections, west and east
			"P31": ("PB4L",  "PB14R"),
			"P41": ("PB2L",  "PB12R"),
			"P32": ("PB14L",  "S4LC"),
			"P42": ("PB12L",  "S16R"),
		}
		# 	"P10": (None,  ""),
		# 	"P11": ("",  ""),
		# 	"P20": (None, ""),
		# 	"P30": ("",  ""),
		# 	"P40": (None,  "")
		# 	"P50": ("",  "")

		for blknm, siglist in blockSigs.items():
			self.blocks[blknm].SetSignals(siglist)

		self.routes = {}
		self.osSignals = {}
		block = self.blocks["POSCJ1"]
		self.routes["PRtP31P32"] = Route(self.screen, block, "PRtP31P32", "P32", [ (135, 33), (136, 33), (137, 33), (138, 33), (139, 33), (140, 33), (141, 33), (142, 33) ], "P31", [MAIN, MAIN], ["PBSw11", "PBSw13"], ["PB14R", "PB14L"])
		self.routes["PRtP31P42"] = Route(self.screen, block, "PRtP31P42", "P42", [ (135, 33), (136, 33), (137, 34), (138, 35), (139, 35), (140, 35), (141, 35), (142, 35) ], "P31", [DIVERGING, DIVERGING], ["PBSw11", "PBSw13"], ["PB14R", "PB12L"])

		block = self.blocks["POSCJ2"]
		self.routes["PRtP41P32"] = Route(self.screen, block, "PRtP41P32", "P32", [ (135, 35), (136, 35), (137, 35), (138, 35), (139, 35), (140, 34), (141, 33), (142, 33) ], "P41", [DIVERGING, DIVERGING], ["PBSw11", "PBSw13"], ["PB12R", "PB14L"])
		self.routes["PRtP41P42"] = Route(self.screen, block, "PRtP41P42", "P42", [ (135, 35), (136, 35), (137, 35), (138, 35), (139, 35), (140, 35), (141, 35), (142, 35) ], "P41", [MAIN, MAIN], ["PBSw11", "PBSw13"], ["PB12R", "PB12L"])

		self.signals["PB14R"].AddPossibleRoutes("POSCJ1", [ "PRtP31P32", "PRtP31P42" ])
		self.signals["PB14L"].AddPossibleRoutes("POSCJ1", [ "PRtP31P32" ])
		self.signals["PB14L"].AddPossibleRoutes("POSCJ2", [ "PRtP41P32" ])
		self.signals["PB12R"].AddPossibleRoutes("POSCJ2", [ "PRtP41P32", "PRtP41P42" ])
		self.signals["PB12L"].AddPossibleRoutes("POSCJ1", [ "PRtP31P42" ])
		self.signals["PB12L"].AddPossibleRoutes("POSCJ2", [ "PRtP41P42" ])

		self.osSignals["POSCJ1"] = [ "PB14R", "PB14L", "PB12L" ]
		self.osSignals["POSCJ2"] = [ "PB12R", "PB12L", "PB14L" ]

		return self.signals

	def DefineHandSwitches(self, tiles):
		self.handswitches = {}

		hs = HandSwitch(self, self.screen, self.frame, self.blocks["P42"], "PBSw15a.hand", (145, 34), tiles["handdown"])
		self.blocks["P42"].AddHandSwitch(hs)
		self.handswitches["PBSw15a.hand"] = hs

		hs = HandSwitch(self, self.screen, self.frame, self.blocks["P42"], "PBSw15b.hand", (149, 36), tiles["handup"])
		self.blocks["P42"].AddHandSwitch(hs)
		self.handswitches["PBSw15b.hand"] = hs

		hs = HandSwitch(self, self.screen, self.frame, self.blocks["P41"], "PBSw5.hand", (129, 36), tiles["handup"])
		self.blocks["P41"].AddHandSwitch(hs)
		self.handswitches["PBSw5.hand"] = hs
		return self.handswitches

