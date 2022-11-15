from district import District

from block import Block, OverSwitch, Route
from turnout import Turnout, SlipSwitch
from signal import Signal
from button import Button
from handswitch import HandSwitch

from constants import RESTRICTING, MAIN, DIVERGING, SLOW, NORMAL, REVERSE, EMPTY, RegAspects, RegSloAspects, SloAspects

class Cliff (District):
	def __init__(self, name, frame, screen):
		District.__init__(self, name, frame, screen)

	def PerformButtonAction(self, btn):
		bname = btn.GetName()
		if bname in self.osButtons["COSGMW"]:
			osBlk = self.blocks["COSGMW"]
			if osBlk.IsBusy():
				self.ReportBlockBusy("COSGMW")
				return

			btn.Press(refresh=True)
			self.frame.ClearButtonAfter(2, btn)
			self.frame.Request({"nxbutton": { "button": btn.GetName() }})

	def DetermineRoute(self, blocks):
		pass
		s37 = 'N' if self.turnouts["CSw37"].IsNormal() else 'R'
		s39 = 'N' if self.turnouts["CSw39"].IsNormal() else 'R'
		s41 = 'N' if self.turnouts["CSw41"].IsNormal() else 'R'

		for block in blocks:
			bname = block.GetName()
			if bname == "COSGMW":
				if s41 == "R":
					block.SetRoute(self.routes["CRtC11G21"])
				elif s41+s39 == "NN":
					block.SetRoute(self.routes["CRtC11C10"])
				elif s41+s39+s37== "NRR":
					block.SetRoute(self.routes["CRtC11C30"])
				elif s41+s39+s37== "NRN":
					block.SetRoute(self.routes["CRtC11C31"])
				else:
					block.SetRoute(None)

	def DefineBlocks(self, tiles):
		self.blocks = {}
		self.osBlocks = {}

		self.blocks["G21"] = Block(self, self.frame, "G21",
			[
				(tiles["houtline"], self.screen,  (127, 28), False),
				(tiles["houtline"], self.screen,  (128, 28), False),
				(tiles["houtline"], self.screen,  (129, 28), False),
			], True)

		self.blocks["C10"] = Block(self, self.frame, "C10",
			[
				(tiles["horiznc"], self.screen,  (127, 30), False),
				(tiles["horiz"],   self.screen,  (128, 30), False),
				(tiles["horiznc"], self.screen,  (129, 30), False),
				(tiles["horiz"],   self.screen,  (130, 30), False),
				(tiles["horiznc"], self.screen,  (131, 30), False),
				(tiles["horiz"],   self.screen,  (132, 30), False),
				(tiles["horiznc"], self.screen,  (133, 30), False),
				(tiles["horiz"],   self.screen,  (134, 30), False),
				(tiles["horiznc"], self.screen,  (135, 30), False),
				(tiles["horiz"],   self.screen,  (136, 30), False),
				(tiles["horiznc"], self.screen,  (137, 30), False),
				(tiles["horiz"],   self.screen,  (138, 30), False),
				(tiles["horiznc"], self.screen,  (139, 30), False),
				(tiles["horiz"],   self.screen,  (140, 30), False),
				(tiles["horiznc"], self.screen,  (141, 30), False),
				(tiles["horiz"],   self.screen,  (142, 30), False),
				(tiles["horiznc"], self.screen,  (143, 30), False),
				(tiles["horiz"],   self.screen,  (144, 30), False),
			], True)
		self.blocks["C10"].AddTrainLoc(self.screen, (130, 30))

		self.blocks["C30"] = Block(self, self.frame, "C30",
			[
				(tiles["horiznc"], self.screen,  (127, 32), False),
				(tiles["horiz"],   self.screen,  (128, 32), False),
				(tiles["horiznc"], self.screen,  (129, 32), False),
				(tiles["horiz"],   self.screen,  (130, 32), False),
				(tiles["horiznc"], self.screen,  (131, 32), False),
				(tiles["horiz"],   self.screen,  (132, 32), False),
				(tiles["horiznc"], self.screen,  (133, 32), False),
				(tiles["horiz"],   self.screen,  (134, 32), False),
				(tiles["horiznc"], self.screen,  (135, 32), False),
				(tiles["horiz"],   self.screen,  (136, 32), False),
				(tiles["horiznc"], self.screen,  (137, 32), False),
				(tiles["horiz"],   self.screen,  (138, 32), False),
				(tiles["horiznc"], self.screen,  (139, 32), False),
				(tiles["horiz"],   self.screen,  (140, 32), False),
				(tiles["horiznc"], self.screen,  (141, 32), False),
				(tiles["horiznc"], self.screen,  (143, 32), False),
				(tiles["horiz"],   self.screen,  (144, 32), False),
			], True)
		self.blocks["C30"].AddTrainLoc(self.screen, (130, 32))

		self.blocks["C31"] = Block(self, self.frame, "C31",
			[
				(tiles["horiznc"], self.screen,  (127, 34), False),
				(tiles["horiz"],   self.screen,  (128, 34), False),
				(tiles["horiznc"], self.screen,  (129, 34), False),
				(tiles["horiz"],   self.screen,  (130, 34), False),
				(tiles["eobright"], self.screen,  (131, 34), False),
			], True)
		self.blocks["C31"].AddTrainLoc(self.screen, (128, 34))

		self.blocks["COSGMW"] = OverSwitch(self, self.frame, "COSGMW",
			[
				(tiles["eobleft"], self.screen,  (119, 30), False),

				(tiles["diagleft"], self.screen, (121, 29), False),
				(tiles["turnleftleft"], self.screen, (122, 28), False),
				(tiles["horiznc"],  self.screen, (123, 28), False),
				(tiles["horiz"],    self.screen, (124, 28), False),
				(tiles["horiznc"],  self.screen, (125, 28), False),

				(tiles["horiz"],    self.screen, (122, 30), False),
				(tiles["horiznc"],  self.screen, (123, 30), False),
				(tiles["horiz"],    self.screen, (124, 30), False),
				(tiles["horiznc"],  self.screen, (125, 30), False),

				(tiles["diagright"], self.screen, (122, 31), False),

				(tiles["horiz"],    self.screen, (124, 32), False),
				(tiles["horiznc"],  self.screen, (125, 32), False),

				(tiles["diagright"], self.screen, (124, 33), False),
				(tiles["turnrightleft"], self.screen, (125, 34), False),
			], True)


		self.osBlocks["COSGMW"] = [ "C11", "G21", "C10", "C30", "C31" ]

		return self.blocks, self.osBlocks

	def DefineTurnouts(self, tiles, blocks):
		self.turnouts = {}

		toList = [
			[ "CSw3",   "toleftleft",   ["C30"], (142, 32) ],
			[ "CSw37",  "toleftdown",   ["COSGMW"], (123, 32) ],
			[ "CSw39",  "torightright", ["COSGMW"], (121, 30) ],
			[ "CSw41",  "toleftright",  ["COSGMW"], (120, 30) ],
		]

		for tonm, tileSet, blks, pos in toList:
			trnout = Turnout(self, self.frame, tonm, self.screen, tiles[tileSet], pos)
			for blknm in blks:
				blocks[blknm].AddTurnout(trnout)
				trnout.AddBlock(blknm)
			self.turnouts[tonm] = trnout

		self.turnouts["CSw3"].SetDisabled(True)
		self.turnouts["CSw37"].SetRouteControl(True)
		self.turnouts["CSw39"].SetRouteControl(True)
		self.turnouts["CSw41"].SetRouteControl(True)

		return self.turnouts

	def DefineButtons(self, tiles):
		self.buttons = {}
		self.osButtons = {}

		b = Button(self, self.screen, self.frame, "CG21W", (126, 28), tiles)
		self.buttons["CG21W"] = b

		b = Button(self, self.screen, self.frame, "CC10W", (126, 30), tiles)
		self.buttons["CC10W"] = b

		b = Button(self, self.screen, self.frame, "CC30W", (126, 32), tiles)
		self.buttons["CC30W"] = b

		b = Button(self, self.screen, self.frame, "CC31W", (126, 34), tiles)
		self.buttons["CC31W"] = b

		self.osButtons["COSGMW"] = [ "CG21W", "CC10W", "CC30W", "CC31W" ]

		return self.buttons

	def DefineSignals(self, tiles):
		self.signals = {}

		sigList = [
			[ "C4R",  RegSloAspects, True,  "rightlong", (119, 31) ],

			[ "C4LD", RegAspects,    False, "left",      (126, 27) ],
			[ "C4LC", RegAspects,    False, "leftlong",  (126, 29) ],
			[ "C4LB", SloAspects,    False, "left",      (126, 31) ],
			[ "C4LA", SloAspects,    False, "left",      (126, 33) ],
		]
		
		for signm, atype, east, tileSet, pos in sigList:
			self.signals[signm]  = Signal(self, self.screen, self.frame, signm, atype, east, pos, tiles[tileSet])  

		self.routes = {}
		self.osSignals = {}

		# Green Mountain West
		block = self.blocks["COSGMW"]
		self.routes["CRtC11G21"] = Route(self.screen, block, "CRtC11G21", "C11", [ (119, 30), (120, 30), (121, 29), (122, 28), (123, 28), (124, 28), (125, 28) ], "G21", [RESTRICTING, RESTRICTING], ["CSw41"])
		self.routes["CRtC11C10"] = Route(self.screen, block, "CRtC11C10", "C11", [ (119, 30), (120, 30), (121, 30), (122, 30), (123, 30), (124, 30), (125, 30) ], "C10", [MAIN, MAIN], ["CSw39", "CSw41"])
		self.routes["CRtC11C30"] = Route(self.screen, block, "CRtC11C30", "C11", [ (119, 30), (120, 30), (121, 30), (122, 31), (123, 32), (124, 32), (125, 32) ], "C30", [SLOW, SLOW], ["CSw37", "CSw39", "CSw41"])
		self.routes["CRtC11C31"] = Route(self.screen, block, "CRtC11C31", "C11", [ (119, 30), (120, 30), (121, 30), (122, 31), (123, 32), (124, 33), (125, 34) ], "C31", [RESTRICTING, SLOW], ["CSw37", "CSw39", "CSw41"])

		self.signals["C4R"].AddPossibleRoutes("COSGMW", [ "CRtC11G21", "CRtC11C10", "CRtC11C30", "CRtC11C31" ])
		self.signals["C4LD"].AddPossibleRoutes("COSGMW", [ "CRtC11G21" ])
		self.signals["C4LC"].AddPossibleRoutes("COSGMW", [ "CRtC11C10" ])
		self.signals["C4LB"].AddPossibleRoutes("COSGMW", [ "CRtC11C30" ])
		self.signals["C4LA"].AddPossibleRoutes("COSGMW", [ "CRtC11C31" ])

		self.osSignals["COSGMW"] = [ "C4R", "C4LA", "C4LB", "C4LC", "C4LD" ]

		return self.signals

	def DefineHandSwitches(self, tiles):
		self.handswitches = {}

		hs = HandSwitch(self, self.screen, self.frame, self.blocks["C30"], "CSw3.hand", (142, 33), tiles["handup"])
		self.blocks["C30"].AddHandSwitch(hs)
		self.handswitches["CSw3.hand"] = hs

		return self.handswitches

