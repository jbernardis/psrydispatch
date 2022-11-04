from district import District

from block import Block, OverSwitch, Route
from turnout import Turnout, SlipSwitch
from signal import Signal
from button import Button
from handswitch import HandSwitch

from constants import LaKr, RegAspects, RESTRICTING, DIVERGING, MAIN

class Nassau (District):
	def __init__(self, name, frame, screen):
		District.__init__(self, name, frame, screen)

	def DetermineRoute(self, blocks):
		pass
		# s1 = 'N' if self.turnouts["KSw1"].IsNormal() else 'R'
		# s3 = 'N' if self.turnouts["KSw3"].IsNormal() else 'R'
		# s5 = 'N' if self.turnouts["KSw5"].IsNormal() else 'R'
		# s7 = 'N' if self.turnouts["KSw7"].IsNormal() else 'R'
		# self.turnouts["KSw3"].SetLock("KSw5", s5=='R', refresh=True)
		# self.turnouts["KSw3b"].SetLock("KSw9", s5=='R', refresh=True)
		# self.turnouts["KSw5"].SetLock("KSw3", s3=='R', refresh=True)
		# self.turnouts["KSw5b"].SetLock("KSw3", s3=='R', refresh=True)

		# for block in blocks:
		# 	bname = block.GetName()
		# 	if bname == "KOSW":
		# 		if s3+s5+s7 == "NNR":
		# 			block.SetRoute(self.routes["KRtN10K10"])
		# 		elif s3+s5+s7 == "NNN":
		# 			block.SetRoute(self.routes["KRtN10N11"])
		# 		elif s3+s5 == "NR":
		# 			block.SetRoute(self.routes["KRtN10N21"])
		# 		else:
		# 			block.SetRoute(None)

		# 	elif bname == "KOSM":
		# 		if s3+s5+s7 == "RNR":
		# 			block.SetRoute(self.routes["KRtN25K10"])
		# 		elif s3+s5+s7 == "RNN":
		# 			block.SetRoute(self.routes["KRtN25N11"])
		# 		elif s1+s3+s5 == "RNN":
		# 			block.SetRoute(self.routes["KRtN25N21"])
		# 		else:
		# 			block.SetRoute(None)
				
		# 	elif bname == "KOSE":
		# 		if s1+s5 == "NN":
		# 			block.SetRoute(self.routes["KRtN20N21"])
		# 		else:
		# 			block.SetRoute(None)

	def DefineBlocks(self, tiles):
		self.blocks = {}
		self.osBlocks = {}

		self.blocks["N21"] = Block(self, self.frame, "N21",
			[
				(tiles["horiz"],   LaKr, (153, 13), False),
				(tiles["horiznc"], LaKr, (154, 13), False),
				(tiles["horiz"],   LaKr, (155, 13), False),
				(tiles["horiznc"], LaKr, (156, 13), False),
				(tiles["horiz"],   LaKr, (157, 13), False),
				(tiles["horiznc"], LaKr, (158, 13), False),
				(tiles["horiznc"], self.screen, (0, 13), False),
				(tiles["horiz"],   self.screen, (1, 13), False),
				(tiles["horiznc"], self.screen, (2, 13), False),
				(tiles["horiz"],   self.screen, (3, 13), False),
				(tiles["horiznc"], self.screen, (4, 13), False),
			], True)
		self.blocks["N21"].AddStoppingBlock([
				(tiles["eobleft"], LaKr, (150, 13), False),
				(tiles["horiz"],   LaKr, (151, 13), False),
				(tiles["horiznc"], LaKr, (152, 13), False),
			], False)
		self.blocks["N21"].AddStoppingBlock([
				(tiles["horiz"],   self.screen, (5, 13), False),
				(tiles["horiznc"], self.screen, (6, 13), False),
				(tiles["horiz"],   self.screen, (7, 13), False),
			], True)
		self.blocks["N21"].AddTrainLoc(LaKr, (154, 13))
		self.blocks["N21"].AddTrainLoc(self.screen, (1, 13))

		self.blocks["N32"] = Block(self, self.frame, "N32",
			[
				(tiles["horiz"],   self.screen, (21, 7), False),
				(tiles["horiznc"], self.screen, (22, 7), False),
				(tiles["horiz"],   self.screen, (23, 7), False),
				(tiles["horiznc"], self.screen, (24, 7), False),
				(tiles["horiz"],   self.screen, (25, 7), False),
				(tiles["horiznc"], self.screen, (26, 7), False),
				(tiles["horiz"],   self.screen, (27, 7), False),
				(tiles["horiznc"], self.screen, (28, 7), False),
			], False)
		self.blocks["N32"].AddTrainLoc(self.screen, (23, 7))

		self.blocks["N31"] = Block(self, self.frame, "N31",
			[
				(tiles["horiz"],   self.screen, (21, 9), False),
				(tiles["horiznc"], self.screen, (22, 9), False),
				(tiles["horiz"],   self.screen, (23, 9), False),
				(tiles["horiznc"], self.screen, (24, 9), False),
				(tiles["horiz"],   self.screen, (25, 9), False),
				(tiles["horiznc"], self.screen, (26, 9), False),
				(tiles["horiz"],   self.screen, (27, 9), False),
				(tiles["horiznc"], self.screen, (28, 9), False),
			], False)
		self.blocks["N31"].AddTrainLoc(self.screen, (23, 9))

		self.blocks["N12"] = Block(self, self.frame, "N12",
			[
				(tiles["horiz"],   self.screen, (21, 11), False),
				(tiles["horiznc"], self.screen, (22, 11), False),
				(tiles["horiz"],   self.screen, (23, 11), False),
				(tiles["horiznc"], self.screen, (24, 11), False),
				(tiles["horiz"],   self.screen, (25, 11), False),
				(tiles["horiznc"], self.screen, (26, 11), False),
				(tiles["horiz"],   self.screen, (27, 11), False),
				(tiles["horiznc"], self.screen, (28, 11), False),
			], False)
		self.blocks["N12"].AddTrainLoc(self.screen, (23, 11))

		self.blocks["N22"] = Block(self, self.frame, "N22",
			[
				(tiles["horiz"],   self.screen, (21, 13), False),
				(tiles["horiznc"], self.screen, (22, 13), False),
				(tiles["horiz"],   self.screen, (23, 13), False),
				(tiles["horiznc"], self.screen, (24, 13), False),
				(tiles["horiz"],   self.screen, (25, 13), False),
				(tiles["horiznc"], self.screen, (26, 13), False),
				(tiles["horiz"],   self.screen, (27, 13), False),
				(tiles["horiznc"], self.screen, (28, 13), False),
			], True)
		self.blocks["N22"].AddTrainLoc(self.screen, (23, 13))

		self.blocks["N41"] = Block(self, self.frame, "N41",
			[
				(tiles["horiz"],   self.screen, (21, 15), False),
				(tiles["horiznc"], self.screen, (22, 15), False),
				(tiles["horiz"],   self.screen, (23, 15), False),
				(tiles["horiznc"], self.screen, (24, 15), False),
				(tiles["horiz"],   self.screen, (25, 15), False),
				(tiles["horiznc"], self.screen, (26, 15), False),
				(tiles["horiz"],   self.screen, (27, 15), False),
				(tiles["horiznc"], self.screen, (28, 15), False),
			], True)
		self.blocks["N41"].AddTrainLoc(self.screen, (23, 15))

		self.blocks["N22"] = Block(self, self.frame, "N22",
			[
				(tiles["horiz"],   self.screen, (21, 17), False),
				(tiles["horiznc"], self.screen, (22, 17), False),
				(tiles["horiz"],   self.screen, (23, 17), False),
				(tiles["horiznc"], self.screen, (24, 17), False),
				(tiles["horiz"],   self.screen, (25, 17), False),
				(tiles["horiznc"], self.screen, (26, 17), False),
				(tiles["horiz"],   self.screen, (27, 17), False),
				(tiles["horiznc"], self.screen, (28, 17), False),
			], True)
		self.blocks["N22"].AddTrainLoc(self.screen, (23, 17))

		self.blocks["W20"] = Block(self, self.frame, "W20",
			[
				(tiles["houtline"],  self.screen, (22, 19), False),
				(tiles["houtline"],  self.screen, (23, 19), False),
				(tiles["houtline"],  self.screen, (24, 19), False),
				(tiles["houtline"],  self.screen, (28, 19), False),
				(tiles["houtline"],  self.screen, (29, 19), False),
				(tiles["houtline"],  self.screen, (30, 19), False),
			], True)

		self.blocks["R10"] = Block(self, self.frame, "R10",
			[
				(tiles["horiznc"],  self.screen, (45, 9), False),
				(tiles["horiz"],    self.screen, (46, 9), False),
				(tiles["horiznc"],  self.screen, (47, 9), False),
				(tiles["horiz"],    self.screen, (48, 9), False),
				(tiles["horiznc"],  self.screen, (49, 9), False),
			], True)

		self.blocks["W10"] = Block(self, self.frame, "W10",
			[
				(tiles["houtline"],  self.screen, (21, 5), False),
				(tiles["houtline"],  self.screen, (22, 5), False),
				(tiles["houtline"],  self.screen, (23, 5), False),
			], False)

		self.blocks["W11"] = Block(self, self.frame, "W11",
			[
				(tiles["houtline"],  self.screen, (29, 5), False),
				(tiles["houtline"],  self.screen, (30, 5), False),
				(tiles["houtline"],  self.screen, (31, 5), False),
			], False)

		self.blocks["T12"] = Block(self, self.frame, "T12",
			[
				(tiles["houtline"],  self.screen, (14, 5), False),
				(tiles["houtline"],  self.screen, (15, 5), False),
			], False)

		self.blocks["N60"] = Block(self, self.frame, "N60",
			[
				(tiles["eobleft"],  self.screen, (4, 6), False),
				(tiles["eobleft"],  self.screen, (4, 7), False),
				(tiles["eobleft"],  self.screen, (4, 8), False),
				(tiles["eobleft"],  self.screen, (4, 9), False),
				(tiles["turnrightright"],  self.screen, (5, 6), False),
				(tiles["turnrightright"],  self.screen, (5, 8), False),
				(tiles["horiznc"],  self.screen, (5, 7), False),
				(tiles["horiznc"],  self.screen, (5, 9), False),
				(tiles["horiznc"],  self.screen, (7, 9), False),
				(tiles["diagright"],self.screen, (7, 8), False),
			], False)

		self.blocks["N60A"] = Block(self, self.frame, "N60A",
			[
				(tiles["houtline"],  self.screen, (1, 6), False),
				(tiles["houtline"],  self.screen, (2, 6), False),
				(tiles["houtline"],  self.screen, (3, 6), False),
			], False)

		self.blocks["N60B"] = Block(self, self.frame, "N60B",
			[
				(tiles["houtline"],  self.screen, (1, 7), False),
				(tiles["houtline"],  self.screen, (2, 7), False),
				(tiles["houtline"],  self.screen, (3, 7), False),
			], False)

		self.blocks["N60C"] = Block(self, self.frame, "N60C",
			[
				(tiles["houtline"],  self.screen, (1, 8), False),
				(tiles["houtline"],  self.screen, (2, 8), False),
				(tiles["houtline"],  self.screen, (3, 8), False),
			], False)

		self.blocks["N60D"] = Block(self, self.frame, "N60D",
			[
				(tiles["houtline"],  self.screen, (1, 9), False),
				(tiles["houtline"],  self.screen, (2, 9), False),
				(tiles["houtline"],  self.screen, (3, 9), False),
			], False)

		self.blocks["NWOSTY"] = OverSwitch(self, self.frame, "NWOSTY", 
			[
				(tiles["horiznc"],   self.screen, (17, 5), False),
				(tiles["horiz"],     self.screen, (18, 5), False),
			], 
			False)

		self.blocks["NWOSCY"] = OverSwitch(self, self.frame, "NWOSCY", 
			[
				(tiles["horiznc"],   self.screen, (11, 9), False),
				(tiles["horiz"],     self.screen, (12, 9), False),
				(tiles["horiznc"],   self.screen, (13, 9), False),
				(tiles["horiz"],     self.screen, (14, 9), False),
				(tiles["diagright"], self.screen, (11, 10), False),
				(tiles["diagright"], self.screen, (13, 12), False),

				(tiles["diagleft"],  self.screen, (16, 8), False),
				(tiles["diagleft"],  self.screen, (18, 6), False),
				(tiles["diagright"], self.screen, (15, 14), False),
				(tiles["diagright"], self.screen, (17, 16), False),
				(tiles["diagright"], self.screen, (19, 18), False),
				(tiles["turnrightright"], self.screen, (20, 19), False),
				(tiles["horiznc"],   self.screen, (18, 7), False),
				(tiles["horiz"],     self.screen, (19, 7), False),
				(tiles["horiznc"],   self.screen, (16, 9), False),
				(tiles["horiz"],     self.screen, (17, 9), False),
				(tiles["horiznc"],   self.screen, (18, 9), False),
				(tiles["horiz"],     self.screen, (19, 9), False),
				(tiles["horiznc"],   self.screen, (14, 11), False),
				(tiles["horiz"],     self.screen, (15, 11), False),
				(tiles["horiznc"],   self.screen, (16, 11), False),
				(tiles["horiz"],     self.screen, (17, 11), False),
				(tiles["horiznc"],   self.screen, (18, 11), False),
				(tiles["horiz"],     self.screen, (19, 11), False),
				(tiles["horiz"],     self.screen, (15, 13), False),
				(tiles["horiznc"],   self.screen, (16, 13), False),
				(tiles["horiz"],     self.screen, (17, 13), False),
				(tiles["horiznc"],   self.screen, (18, 13), False),
				(tiles["horiz"],     self.screen, (19, 13), False),
				(tiles["horiz"],     self.screen, (17, 15), False),
				(tiles["horiznc"],   self.screen, (18, 15), False),
				(tiles["horiz"],     self.screen, (19, 15), False),
				(tiles["horiz"],     self.screen, (19, 17), False),
			], 
			False)

		self.blocks["NWOSW"] = OverSwitch(self, self.frame, "NWOSW", 
			[
				(tiles["horiznc"],   self.screen, (9, 11), False),
				(tiles["horiz"],     self.screen, (10, 11), False),
				(tiles["diagright"], self.screen, (13, 12), False),
				(tiles["diagleft"],  self.screen, (14, 10), False),

				(tiles["diagleft"],  self.screen, (16, 8), False),
				(tiles["diagleft"],  self.screen, (18, 6), False),
				(tiles["diagright"], self.screen, (15, 14), False),
				(tiles["diagright"], self.screen, (17, 16), False),
				(tiles["diagright"], self.screen, (19, 18), False),
				(tiles["turnrightright"], self.screen, (20, 19), False),
				(tiles["horiznc"],   self.screen, (18, 7), False),
				(tiles["horiz"],     self.screen, (19, 7), False),
				(tiles["horiznc"],   self.screen, (16, 9), False),
				(tiles["horiz"],     self.screen, (17, 9), False),
				(tiles["horiznc"],   self.screen, (18, 9), False),
				(tiles["horiz"],     self.screen, (19, 9), False),
				(tiles["horiznc"],   self.screen, (14, 11), False),
				(tiles["horiz"],     self.screen, (15, 11), False),
				(tiles["horiznc"],   self.screen, (16, 11), False),
				(tiles["horiz"],     self.screen, (17, 11), False),
				(tiles["horiznc"],   self.screen, (18, 11), False),
				(tiles["horiz"],     self.screen, (19, 11), False),
				(tiles["horiz"],     self.screen, (15, 13), False),
				(tiles["horiznc"],   self.screen, (16, 13), False),
				(tiles["horiz"],     self.screen, (17, 13), False),
				(tiles["horiznc"],   self.screen, (18, 13), False),
				(tiles["horiz"],     self.screen, (19, 13), False),
				(tiles["horiz"],     self.screen, (17, 15), False),
				(tiles["horiznc"],   self.screen, (18, 15), False),
				(tiles["horiz"],     self.screen, (19, 15), False),
				(tiles["horiz"],     self.screen, (19, 17), False),
			], 
			False)

		self.blocks["NWOSE"] = OverSwitch(self, self.frame, "NWOSE", 
			[
				(tiles["horiznc"],   self.screen, (10, 13), False),
				(tiles["horiz"],     self.screen, (11, 13), False),
				(tiles["horiznc"],   self.screen, (12, 13), False),
				(tiles["horiz"],     self.screen, (13, 13), False),
				(tiles["diagleft"],  self.screen, (14, 12), False),
				(tiles["diagleft"],  self.screen, (14, 10), False),

				(tiles["diagleft"],  self.screen, (16, 8), False),
				(tiles["diagleft"],  self.screen, (18, 6), False),
				(tiles["diagright"], self.screen, (15, 14), False),
				(tiles["diagright"], self.screen, (17, 16), False),
				(tiles["diagright"], self.screen, (19, 18), False),
				(tiles["turnrightright"], self.screen, (20, 19), False),
				(tiles["horiznc"],   self.screen, (18, 7), False),
				(tiles["horiz"],     self.screen, (19, 7), False),
				(tiles["horiznc"],   self.screen, (16, 9), False),
				(tiles["horiz"],     self.screen, (17, 9), False),
				(tiles["horiznc"],   self.screen, (18, 9), False),
				(tiles["horiz"],     self.screen, (19, 9), False),
				(tiles["horiznc"],   self.screen, (14, 11), False),
				(tiles["horiz"],     self.screen, (15, 11), False),
				(tiles["horiznc"],   self.screen, (16, 11), False),
				(tiles["horiz"],     self.screen, (17, 11), False),
				(tiles["horiznc"],   self.screen, (18, 11), False),
				(tiles["horiz"],     self.screen, (19, 11), False),
				(tiles["horiz"],     self.screen, (15, 13), False),
				(tiles["horiznc"],   self.screen, (16, 13), False),
				(tiles["horiz"],     self.screen, (17, 13), False),
				(tiles["horiznc"],   self.screen, (18, 13), False),
				(tiles["horiz"],     self.screen, (19, 13), False),
				(tiles["horiz"],     self.screen, (17, 15), False),
				(tiles["horiznc"],   self.screen, (18, 15), False),
				(tiles["horiz"],     self.screen, (19, 15), False),
				(tiles["horiz"],     self.screen, (19, 17), False),
			], 
			True)

		self.osBlocks["NWOSTY"] = [ "T12", "W10" ]
		self.osBlocks["NWOSCY"] = [ "N60", "W10", "N32", "N31", "N12", "N22", "N41", "N42", "W20" ]
		self.osBlocks["NWOSW"] = [ "N11", "W10", "N32", "N31", "N12", "N22", "N41", "N42", "W20" ]
		self.osBlocks["NWOSE"] = [ "N21", "W10", "N32", "N31", "N12", "N22", "N41", "N42", "W20" ]

		return self.blocks, self.osBlocks

	def DefineTurnouts(self, tiles, blocks):
		self.turnouts = {}
		
		# these turnouts are controlled by entry/exit buttons and NOT by direct clicks
		toList = [
			[ "NSw19",  "toleftleft",    ["NWOSE", "NWOSW"], (11, 11) ],
			[ "NSw19b", "toleftright",   ["NWOSE", "NWOSW"], (9, 13) ],
			[ "NSw21b", "toleftright",   ["NWOSE", "NWOSW", "NWOSCY"], (13, 11) ],
			[ "NSw23",  "torightup",     ["NWOSE", "NWOSW", "NWOSCY" ], (17, 7) ],
			[ "NSw25",  "toleftleft",    ["NWOSE", "NWOSW", "NWOSCY", "NWOSTY"], (19, 5) ],
			[ "NSw27b", "torightright",  ["NWOSE", "NWOSW", "NWOSCY"], (10, 9) ],
			[ "NSw31",  "toleftdown",    ["NWOSE", "NWOSW", "NWOSCY"], (16, 15) ],
			[ "NSw33",  "toleftdown",    ["NWOSE", "NWOSW", "NWOSCY"], (18, 17) ],
		]
		for tonm, tileSet, blks, pos in toList:
			trnout = Turnout(self, self.frame, tonm, self.screen, tiles[tileSet], pos)
			trnout.SetRouteControl(True)
			for blknm in blks:
				blocks[blknm].AddTurnout(trnout)
				trnout.AddBlock(blknm)
			self.turnouts[tonm] = trnout

		# these turnouts are NOT controlled by entry/exit buttons	
		toList = [
			[ "NSw13",  "toleftup",      ["N60"], (6, 7) ],
			[ "NSw15",  "torightleft",   ["N60"], (6, 9) ],
			[ "NSw17",  "torightleft",   ["N60"], (8, 9) ],
		]
		for tonm, tileSet, blks, pos in toList:
			trnout = Turnout(self, self.frame, tonm, self.screen, tiles[tileSet], pos)
			for blknm in blks:
				blocks[blknm].AddTurnout(trnout)
				trnout.AddBlock(blknm)
			self.turnouts[tonm] = trnout

		# self.turnouts["KSw3"].SetPairedTurnout(self.turnouts["KSw3b"])
		# self.turnouts["KSw5"].SetPairedTurnout(self.turnouts["KSw5b"])

		return self.turnouts

	def DefineButtons(self, tiles):
		self.buttons = {}
		self.osButtons = {}
	
		self.buttons["NBWI1"] = Button(self, self.screen, self.frame, "NBWI1", (9, 9), tiles)
		self.buttons["NBWI2"] = Button(self, self.screen, self.frame, "NBWI2", (8, 11), tiles)
		self.buttons["NBWI3"] = Button(self, self.screen, self.frame, "NBWI3", (8, 13), tiles)
		self.buttons["NBWIT"] = Button(self, self.screen, self.frame, "NBWIT", (16, 5), tiles)

		self.buttons["NBWO1"] = Button(self, self.screen, self.frame, "NBWO1", (20, 5), tiles)
		self.buttons["NBWO2"] = Button(self, self.screen, self.frame, "NBWO2", (20, 7), tiles)
		self.buttons["NBWO3"] = Button(self, self.screen, self.frame, "NBWO3", (20, 9), tiles)
		self.buttons["NBWO4"] = Button(self, self.screen, self.frame, "NBWO4", (20, 11), tiles)
		self.buttons["NBWO5"] = Button(self, self.screen, self.frame, "NBWO5", (20, 13), tiles)
		self.buttons["NBWO6"] = Button(self, self.screen, self.frame, "NBWO6", (20, 15), tiles)
		self.buttons["NBWO7"] = Button(self, self.screen, self.frame, "NBWO7", (20, 17), tiles)
		self.buttons["NBWO8"] = Button(self, self.screen, self.frame, "NBWO8", (21, 19), tiles)

		self.buttons["NBEI1"] = Button(self, self.screen, self.frame, "NBEI1", (44, 9), tiles)
		self.buttons["NBEI2"] = Button(self, self.screen, self.frame, "NBEI2", (44, 11), tiles)
		self.buttons["NBEI3"] = Button(self, self.screen, self.frame, "NBEI3", (44, 13), tiles)
		self.buttons["NBWO1"] = Button(self, self.screen, self.frame, "NBWO1", (20, 5), tiles)

		self.buttons["NBEO1"] = Button(self, self.screen, self.frame, "NBEO1", (32, 5), tiles)
		self.buttons["NBEO2"] = Button(self, self.screen, self.frame, "NBEO2", (29, 7), tiles)
		self.buttons["NBEO3"] = Button(self, self.screen, self.frame, "NBEO3", (29, 9), tiles)
		self.buttons["NBEO4"] = Button(self, self.screen, self.frame, "NBEO4", (29, 11), tiles)
		self.buttons["NBEO5"] = Button(self, self.screen, self.frame, "NBEO5", (29, 13), tiles)
		self.buttons["NBEO6"] = Button(self, self.screen, self.frame, "NBEO6", (29, 15), tiles)
		self.buttons["NBEO7"] = Button(self, self.screen, self.frame, "NBEO7", (29, 17), tiles)
		self.buttons["NBEO8"] = Button(self, self.screen, self.frame, "NBEO8", (31, 19), tiles)

		return self.buttons
	
	def DefineSignals(self, tiles):
		self.signals = {}
		self.routes = {}
		self.osSignals = {}
		# sigList = [
		# 	[ "K8R",  RegAspects, True,    "rightlong", (141, 12) ],
		# 	[ "K4R",  RegAspects, True,    "rightlong", (141, 14) ],
		# 	[ "K2R",  RegAspects, True,    "rightlong", (141, 16) ],

		# 	[ "K8LA", RegAspects, False,   "left",  (149, 8) ],
		# 	[ "K8LB", RegAspects, False,   "leftlong", (149, 10) ],
		# 	[ "K2L",  RegAspects, False,   "leftlong", (149, 12) ],

		# 	[ "N20W", RegAspects, False,   "leftlong", (121, 18) ],
		# 	[ "S21E", RegAspects, True,    "rightlong", (122, 20) ],

		# 	[ "N10W", RegAspects, False,   "leftlong", (121, 6) ],
		# 	[ "S11E", RegAspects, True,    "rightlong", (122, 8) ],
		# ]

		# for signm, atype, east, tileSet, pos in sigList:
		# 	self.signals[signm]  = Signal(self, self.screen, self.frame, signm, atype, east, pos, tiles[tileSet])  

		# blockSigs = {
		# 	# # which signals govern stopping sections, west and east
		# 	"N10": ("N10W",  "K8R"),
		# 	"N11": ("K8B",  "N16R"),
		# 	"N20": ("N20W", "K2R"),
		# 	"N21": ("K2L",  "N14R"),
		# 	"N25": ("S16L",  "K4R")
		# }

		# for blknm, siglist in blockSigs.items():
		# 	self.blocks[blknm].SetSignals(siglist)

		# block = self.blocks["KOSW"]
		# self.routes["KRtN10K10"] = Route(self.screen, block, "KRtN10K10", "K10", [ (141, 11), (142, 11), (143, 11), (144, 11), (145, 11), (146, 11), (147, 10), (148, 9), (149, 9) ], "N10", [RESTRICTING, RESTRICTING], ["KSw3", "KSw5", "KSw7"])
		# self.routes["KRtN10N11"] = Route(self.screen, block, "KRtN10N11", "N11", [ (141, 11), (142, 11), (143, 11), (144, 11), (145, 11), (146, 11), (147, 11), (148, 11), (149, 11) ], "N10", [MAIN, MAIN], ["KSw3", "KSw5", "KSw7"])
		# self.routes["KRtN10N21"] = Route(self.screen, block, "KRtN10N21", "N21", [ (141, 11), (142, 11), (143, 11), (144, 11), (145, 11), (146, 12), (147, 13), (148, 13), (149, 13) ], "N10", [DIVERGING, DIVERGING], ["KSw3", "KSw5"])

		# block = self.blocks["KOSM"]
		# self.routes["KRtN25K10"] = Route(self.screen, block, "KRtN25K10", "K10", [ (141, 13), (142, 13), (143, 12), (144, 11), (145, 11), (146, 11), (147, 10), (148, 9), (149, 9) ], "N25", [RESTRICTING, RESTRICTING], ["KSw3", "KSw5", "KSw7"])
		# self.routes["KRtN25N11"] = Route(self.screen, block, "KRtN25N11", "N11", [ (141, 13), (142, 13), (143, 12), (144, 11), (145, 11), (146, 11), (147, 11), (148, 11), (149, 11) ], "N25", [DIVERGING, DIVERGING], ["KSw3", "KSw5", "KSw7"])
		# self.routes["KRtN25N21"] = Route(self.screen, block, "KRtN25N21", "N21", [ (141, 13), (142, 13), (143, 13), (144, 13), (145, 13), (146, 13), (147, 13), (148, 13), (149, 13) ], "N25", [MAIN, MAIN], ["KSw1", "KSw3", "KSw5"])

		# block = self.blocks["KOSE"]
		# self.routes["KRtN20N21"] = Route(self.screen, block, "KRtN20N21", "N20", [ (141, 15), (142, 15), (143, 15), (144, 14), (145, 13), (146, 13), (147, 13), (148, 13), (149, 13) ], "N21", [DIVERGING, DIVERGING], ["KSw1", "KSw5"])

		# block = self.blocks["KOSN10S11"]
		# self.routes["KRtN10S11"] = Route(self.screen, block, "KRtN10S11", "N10", [  ], "S11", [MAIN, MAIN], [])
		# block.SetRoute(self.routes["KRtN10S11"])

		# block = self.blocks["KOSN20S21"]
		# self.routes["KRtN20S21"] = Route(self.screen, block, "KRtN20S21", "S21", [  ], "N20", [MAIN, MAIN], [])
		# block.SetRoute(self.routes["KRtN20S21"])

		# self.signals["K8R"].AddPossibleRoutes("KOSW", [ "KRtN10K10", "KRtN10N11", "KRtN10N21" ])
		# self.signals["K4R"].AddPossibleRoutes("KOSM", [ "KRtN25K10", "KRtN25N11", "KRtN25N21" ])
		# self.signals["K2R"].AddPossibleRoutes("KOSE", [ "KRtN20N21" ])
		# self.signals["K8LA"].AddPossibleRoutes("KOSW", [ "KRtN10K10" ])
		# self.signals["K8LA"].AddPossibleRoutes("KOSM", [ "KRtN25K10" ])
		# self.signals["K8LB"].AddPossibleRoutes("KOSW", [ "KRtN10N11" ])
		# self.signals["K8LB"].AddPossibleRoutes("KOSM", [ "KRtN25N11" ])
		# self.signals["K2L"].AddPossibleRoutes("KOSW", [ "KRtN10N21" ])
		# self.signals["K2L"].AddPossibleRoutes("KOSM", [ "KRtN25N21" ])
		# self.signals["K2L"].AddPossibleRoutes("KOSE", [ "KRtN20N21" ])

		# self.signals["N10W"].AddPossibleRoutes("KOSN10S11", [ "KRtN10S11" ])
		# self.signals["S11E"].AddPossibleRoutes("KOSN10S11", [ "KRtN10S11" ])

		# self.signals["N20W"].AddPossibleRoutes("KOSN20S21", [ "KRtN20S21" ])
		# self.signals["S21E"].AddPossibleRoutes("KOSN20S21", [ "KRtN20S21" ])

		# self.osSignals["KOSW"] = [ "K8R", "K8LA", "K8LB", "K2L" ]
		# self.osSignals["KOSM"] = [ "K4R", "K8LA", "K8LB", "K2L" ]
		# self.osSignals["KOSE"] = [ "K2R", "K2L" ]
		# self.osSignals["KOSN10S11"] = [ "N10W", "S11E" ]
		# self.osSignals["KOSN20S21"] = [ "N20W", "S21E" ]


		return self.signals

	def PerformButtonAction(self, btn):
		District.PerformButtonAction(self, btn)

		print("Nassau: press button %s" % btn.GetName())

