from district import District

from block import Block, OverSwitch, Route
from turnout import Turnout
from signal import Signal
from button import Button

from constants import HyYdPt, RESTRICTING, MAIN, DIVERGING

class Yard (District):
	def __init__(self, name, frame, screen):
		District.__init__(self, name, frame, screen)

	def DetermineRoute(self, blocks):
		for bname in blocks:
			block = self.frame.GetBlockByName(bname)
			if bname == "OSYCJW":
				s1 = 'N' if self.turnouts["YSw1"].IsNormal() else 'R'
				s3 = 'N' if self.turnouts["YSw3"].IsNormal() else 'R'

				if s3 == "N":
					block.SetRoute(self.routes["YRtY11L10"])
				else:
					if s1 == 'N':
						block.SetRoute(self.routes["YRtY11L20"])
					else:
						block.SetRoute(self.routes["YRtY11P50"])

			elif bname == "OSYCJE":
				s1 = 'N' if self.turnouts["YSw1"].IsNormal() else 'R'
				s3 = 'N' if self.turnouts["YSw3"].IsNormal() else 'R'
				if s3 == "R":
					block.SetRoute(None)
				elif s1 == "N":
					block.SetRoute(self.routes["YRtY21L20"])
				else:
					block.SetRoute(self.routes["YRtY21P50"])

			elif bname == "OSYEEW":
				s7 = 'N' if self.turnouts["YSw7"].IsNormal() else 'R'
				s9 = 'N' if self.turnouts["YSw9"].IsNormal() else 'R'
				s11 = 'N' if self.turnouts["YSw11"].IsNormal() else 'R'
				if s7 == "N" and s9 == "N":
					block.SetRoute(self.routes["YRtY10Y11"])
				elif s7 == 'N' and s9 == 'R' and s11 == 'R':
					block.SetRoute(self.routes["YRtY30Y11"])
				elif s7 == 'N' and s9 == 'R' and s11 == 'N':
					block.SetRoute(self.routes["YRtY87Y11"])
				else:
					block.SetRoute(None)

			elif bname == "OSYEEE":
				s7 = 'N' if self.turnouts["YSw7"].IsNormal() else 'R'
				s9 = 'N' if self.turnouts["YSw9"].IsNormal() else 'R'
				s11 = 'N' if self.turnouts["YSw11"].IsNormal() else 'R'
				if s7 == 'N':
					block.SetRoute(self.routes["YRtY20Y21"])
				elif s7 == 'R' and s9 == 'R' and s11 == 'R':
					block.SetRoute(self.routes["YRtY30Y21"])
				elif s7 == 'R' and s9 == 'R' and s11 == 'N':
					block.SetRoute(self.routes["YRtY87Y21"])
				elif s7 == 'R' and s9 == 'N':
					block.SetRoute(self.routes["YRtY10Y21"])
				else:
					block.SetRoute(None)

	def PerformButtonAction(self, btn):
		bname = btn.GetName()

	def DefineBlocks(self, tiles):
		self.blocks = {}
		self.osBlocks = {}

		self.blocks["Y10"] = Block(self, self.frame, "Y10",
			[
				(tiles["eobleft"],  self.screen, (107, 11), False),
				(tiles["horiznc"],  self.screen, (108, 11), False),
				(tiles["horiz"],    self.screen, (109, 11), False),
				(tiles["horiznc"],  self.screen, (110, 11), False),
				(tiles["horiz"],    self.screen, (111, 11), False),
				(tiles["horiznc"],  self.screen, (112, 11), False),
				(tiles["eobright"], self.screen, (113, 11), False),
			], False)

		self.blocks["Y11"] = Block(self, self.frame, "Y11",
			[
				(tiles["eobleft"],  self.screen, (122, 11), False),
				(tiles["horiznc"],  self.screen, (123, 11), False),
				(tiles["horiz"],    self.screen, (124, 11), False),
				(tiles["horiznc"],  self.screen, (125, 11), False),
				(tiles["horiz"],    self.screen, (126, 11), False),
				(tiles["horiznc"],  self.screen, (127, 11), False),
				(tiles["eobright"], self.screen, (128, 11), False),
			], False)

		self.blocks["Y20"] = Block(self, self.frame, "Y10",
			[
				(tiles["eobleft"],  self.screen, (107, 13), False),
				(tiles["horiznc"],  self.screen, (108, 13), False),
				(tiles["horiz"],    self.screen, (109, 13), False),
				(tiles["horiznc"],  self.screen, (110, 13), False),
				(tiles["horiz"],    self.screen, (111, 13), False),
				(tiles["horiznc"],  self.screen, (112, 13), False),
				(tiles["eobright"], self.screen, (113, 13), False),
			], True)

		self.blocks["Y21"] = Block(self, self.frame, "Y21",
			[
				(tiles["eobleft"],  self.screen, (122, 13), False),
				(tiles["horiznc"],  self.screen, (123, 13), False),
				(tiles["horiz"],    self.screen, (124, 13), False),
				(tiles["horiznc"],  self.screen, (125, 13), False),
				(tiles["horiz"],    self.screen, (126, 13), False),
				(tiles["horiznc"],  self.screen, (127, 13), False),
				(tiles["eobright"], self.screen, (128, 13), False),
			], True)

		self.blocks["Y30"] = Block(self, self.frame, "Y30",
			[
				(tiles["eobright"],       self.screen, (111, 7), False),
				(tiles["turnrightleft"],  self.screen, (110, 7), False),
				(tiles["diagright"],      self.screen, (109, 6), False),
				(tiles["diagright"],      self.screen, (108, 5), False),
				(tiles["diagright"],      self.screen, (107, 4), False),
				(tiles["turnrightright"], self.screen, (106, 3), False),
				(tiles["horiz"],          self.screen, (83, 3), False),
				(tiles["horiznc"],        self.screen, (84, 3), False),
				(tiles["horiz"],          self.screen, (85, 3), False),
				(tiles["horiznc"],        self.screen, (86, 3), False),
				(tiles["horiz"],          self.screen, (87, 3), False),
				(tiles["horiznc"],        self.screen, (88, 3), False),
				(tiles["horiz"],          self.screen, (89, 3), False),
				(tiles["horiznc"],        self.screen, (90, 3), False),
				(tiles["horiz"],          self.screen, (91, 3), False),
				(tiles["horiznc"],        self.screen, (92, 3), False),
				(tiles["horiz"],          self.screen, (93, 3), False),
				(tiles["horiznc"],        self.screen, (94, 3), False),
				(tiles["horiz"],          self.screen, (95, 3), False),
				(tiles["horiznc"],        self.screen, (96, 3), False),
				(tiles["horiz"],          self.screen, (97, 3), False),
				(tiles["horiznc"],        self.screen, (98, 3), False),
				(tiles["horiz"],          self.screen, (99, 3), False),
				(tiles["horiznc"],        self.screen, (100, 3), False),
				(tiles["horiz"],          self.screen, (101, 3), False),
				(tiles["horiznc"],        self.screen, (102, 3), False),
				(tiles["horiz"],          self.screen, (103, 3), False),
				(tiles["horiznc"],        self.screen, (104, 3), False),
				(tiles["horiz"],          self.screen, (105, 3), False),
				(tiles["turnleftleft"],   self.screen, (82, 3), False),
				(tiles["turnrightup"],    self.screen, (81, 4), False),
				(tiles["vertical"],       self.screen, (81, 5), False),
				(tiles["verticalnc"],     self.screen, (81, 6), False),
				(tiles["vertical"],       self.screen, (81, 7), False),
				(tiles["verticalnc"],     self.screen, (81, 8), False),
				(tiles["vertical"],       self.screen, (81, 9), False),
				(tiles["verticalnc"],     self.screen, (81, 10), False),
				(tiles["vertical"],       self.screen, (81, 11), False),
				(tiles["turnleftdown"],   self.screen, (81, 12), False),
				(tiles["turnrightleft"],  self.screen, (82, 13), False),
				(tiles["eobright"],       self.screen, (83, 13), False),
			], False)

		self.blocks["Y87"] = Block(self, self.frame, "Y87",
			[
				(tiles["eobleft"],        self.screen, (56, 30), False),
				(tiles["horiz"],          self.screen, (57, 30), False),
				(tiles["horiznc"],        self.screen, (58, 30), False),
				(tiles["horiz"],          self.screen, (59, 30), False),
				(tiles["horiznc"],        self.screen, (60, 30), False),
				(tiles["horiz"],          self.screen, (61, 30), False),
				(tiles["horiznc"],        self.screen, (62, 30), False),
				(tiles["horiz"],          self.screen, (63, 30), False),
				(tiles["horiznc"],        self.screen, (64, 30), False),
				(tiles["houtline"],       self.screen, (110, 9), False),
				(tiles["houtline"],       self.screen, (111, 9), False),
				(tiles["houtline"],       self.screen, (112, 9), False),
			], False)

		self.blocks["OSYEEW"] = OverSwitch(self, self.frame, "OSYEEW", 
			[
				(tiles["eobleft"],        self.screen, (112, 7), False),
				(tiles["turnrightright"], self.screen, (113, 7), False),
				(tiles["diagright"],      self.screen, (114, 8), False),
				(tiles["diagright"],      self.screen, (116, 10), False),
				(tiles["eobleft"],        self.screen, (113, 9), False),
				(tiles["horiz"],          self.screen, (114, 9), False),
				(tiles["eobleft"],        self.screen, (114, 11), False),
				(tiles["horiz"],          self.screen, (115, 11), False),
				(tiles["horiznc"],        self.screen, (116, 11), False),
				(tiles["horiz"],          self.screen, (119, 11), False),
				(tiles["horiznc"],        self.screen, (120, 11), False),
				(tiles["eobright"],       self.screen, (121, 11), False),
			],
			False)

		self.blocks["OSYEEE"] = OverSwitch(self, self.frame, "OSYEEE", 
			[
				(tiles["eobleft"],        self.screen, (112, 7), False),
				(tiles["turnrightright"], self.screen, (113, 7), False),
				(tiles["diagright"],      self.screen, (114, 8), False),
				(tiles["diagright"],      self.screen, (116, 10), False),
				(tiles["eobleft"],        self.screen, (113, 9), False),
				(tiles["horiz"],          self.screen, (114, 9), False),
				(tiles["eobleft"],        self.screen, (114, 11), False),
				(tiles["horiz"],          self.screen, (115, 11), False),
				(tiles["horiznc"],        self.screen, (116, 11), False),
				(tiles["diagright"],      self.screen, (119, 12), False),
				(tiles["eobleft"],        self.screen, (114, 13), False),
				(tiles["horiz"],          self.screen, (115, 13), False),
				(tiles["horiznc"],        self.screen, (116, 13), False),
				(tiles["horiz"],          self.screen, (117, 13), False),
				(tiles["horiznc"],        self.screen, (118, 13), False),
				(tiles["horiz"],          self.screen, (119, 13), False),
				(tiles["eobright"],       self.screen, (121, 13), False),				
			],
			True)

		self.blocks["OSYCJE"] = OverSwitch(self, self.frame, "OSYCJE", 
			[
				(tiles["eobleft"],  self.screen, (129, 13), False),
				(tiles["horiznc"],  self.screen, (130, 13), False),
				(tiles["horiznc"],  self.screen, (131, 13), False),
				(tiles["horiz"],    self.screen, (134, 13), False),
				(tiles["horiznc"],  self.screen, (135, 13), False),
				(tiles["eobright"], self.screen, (136, 13), False),
				(tiles["diagright"], self.screen, (134, 14), False),
				(tiles["turnrightleft"], self.screen, (135, 15), True),
				(tiles["eobright"], self.screen, (136, 15), False),
			], 
			True)

		self.blocks["OSYCJW"] = OverSwitch(self, self.frame, "OSYCJW", 
			[
				(tiles["eobleft"],  self.screen, (129, 11), False),
				(tiles["horiznc"],  self.screen, (131, 11), False),
				(tiles["horiz"],    self.screen, (132, 11), False),
				(tiles["horiznc"],  self.screen, (133, 11), False),
				(tiles["horiz"],    self.screen, (134, 11), False),
				(tiles["horiznc"],  self.screen, (135, 11), False),
				(tiles["eobright"], self.screen, (136, 11), False),
				(tiles["diagright"],self.screen, (131, 12), False),
				(tiles["horiz"],    self.screen, (134, 13), False),
				(tiles["horiznc"],  self.screen, (135, 13), False),
				(tiles["eobright"], self.screen, (136, 13), False),
				(tiles["diagright"], self.screen, (134, 14), False),
				(tiles["turnrightleft"], self.screen, (135, 15), True),
				(tiles["eobright"], self.screen, (136, 15), False),
			], 
			False)

		self.osBlocks["OSYCJW"] = [ "Y11", "L10", "L20", "P50" ]
		self.osBlocks["OSYCJE"] = [ "Y21", "L20", "P50" ]
		self.osBlocks["OSYEEW"] = [ "Y11", "Y10", "Y87", "Y30" ]
		self.osBlocks["OSYEEE"] = [ "Y21", "Y20", "Y10", "Y87", "Y30" ]

		return self.blocks

	def DefineTurnouts(self, tiles, blocks):
		self.turnouts = {}

		toList = [
			[ "YSw1",  "torightright",   "OSYCJE", (133, 13) ],
			[ "YSw3",  "torightright",   "OSYCJW", (130, 11) ],
			[ "YSw3b",  "torightleft",   "OSYCJE", (132, 13) ],

			[ "YSw7",  "torightleft",    "OSYEEW", (120, 13) ],
			[ "YSw7b", "torightright",   "OSYEEW", (118, 11) ],
			[ "YSw9",  "torightleft",    "OSYEEW", (117, 11) ],
			[ "YSw11", "toleftupinv",    "OSYEEW", (115, 9) ]

		]

		for tonm, tileSet, blknm, pos in toList:
			trnout = Turnout(self, self.frame, tonm, self.screen, tiles[tileSet], blocks[blknm], pos)
			blocks[blknm].AddTurnout(trnout)
			self.turnouts[tonm] = trnout
		
		self.turnouts["YSw3"].SetPairedTurnout(self.turnouts["YSw3b"])
		self.turnouts["YSw7"].SetPairedTurnout(self.turnouts["YSw7b"])

		self.osTurnouts = {}
		self.osTurnouts["OSYCJW"] = [ "YSw1", "YSw3" ]
		self.osTurnouts["OSYCJE"] = [ "YSw1", "YSw3b" ]
		self.osTurnouts["OSYEEW"] = [ "YSw7b", "YSw9", "YSw11" ]
		self.osTurnouts["OSYEEE"] = [ "YSw7", "YSw9", "YSw11" ]
		
		return self.turnouts

	def DefineSignals(self, tiles):
		self.signals = {}

		sigList = [
			[ "Y2L",  True,    "right", (129, 12) ],
			[ "Y2R",  False,   "left",  (136, 10) ],
			[ "Y4L",  True,    "right", (129, 14) ],
			[ "Y4RA", False,   "left",  (136, 14) ],
			[ "Y4RB", False,   "left",  (136, 12) ],

			[ "Y8LA", True,    "right", (114, 12) ],
			[ "Y8LB", True,    "right", (113, 10) ],
			[ "Y8LC", True,    "right", (112, 8)  ],
			[ "Y8R",  False,   "left",  (121, 10) ],
			[ "Y10L", True,    "right", (114, 14) ],
			[ "Y10R", False,   "left",  (121, 12) ],
		]
		for signm, east, tileSet, pos in sigList:
			self.signals[signm]  = Signal(self, self.screen, self.frame, signm, east, pos, tiles[tileSet])  

		self.routes = {}
		self.osSignals = {}

		# cornell junction
		block = self.blocks["OSYCJW"]
		self.routes["YRtY11L10"] = Route(self.screen, block, "YRtY11L10", "L10", [ (129, 11), (130, 11), (131, 11), (132, 11), (133, 11), (134, 11), (135, 11), (136, 11) ], "Y11", [RESTRICTING, MAIN])
		self.routes["YRtY11L20"] = Route(self.screen, block, "YRtY11L20", "L20", [ (129, 11), (130, 11), (131, 12), (132, 13), (133, 13), (134, 13), (135, 13), (136, 13) ], "Y11", [RESTRICTING, RESTRICTING])
		self.routes["YRtY11P50"] = Route(self.screen, block, "YRtY11P50", "P50", [ (129, 11), (130, 11), (131, 12), (132, 13), (133, 13), (134, 14), (135, 15), (136, 15) ], "Y11", [RESTRICTING, DIVERGING])

		block = self.blocks["OSYCJE"]
		self.routes["YRtY21L20"] = Route(self.screen, block, "YRtY21L20", "Y21", [ (129, 13), (130, 13), (131, 13), (132, 13), (133, 13), (134, 13), (135, 13), (136, 13) ], "L20", [MAIN, RESTRICTING])
		self.routes["YRtY21P50"] = Route(self.screen, block, "YRtY21P50", "Y21", [ (129, 13), (130, 13), (131, 13), (132, 13), (133, 13), (134, 14), (135, 15), (136, 15) ], "P50", [DIVERGING, RESTRICTING])

		self.signals["Y2L"].AddPossibleRoutes("OSYCJW", [ "YRtY11L10", "YRtY11L20", "YRtY11P50" ])
		self.signals["Y2R"].AddPossibleRoutes("OSYCJW", [ "YRtY11L10" ])

		self.signals["Y4L"].AddPossibleRoutes("OSYCJE", [ "YRtY21L20", "YRtY21P50" ])
		self.signals["Y4RB"].AddPossibleRoutes("OSYCJE", [ "YRtY21L20" ])
		self.signals["Y4RB"].AddPossibleRoutes("OSYCJW", [ "YRtY11L20" ])
		self.signals["Y4RA"].AddPossibleRoutes("OSYCJE", [ "YRtY21P50" ])
		self.signals["Y4RA"].AddPossibleRoutes("OSYCJW", [ "YRtY11P50" ])

		self.osSignals["OSYCJW"] = [ "Y2L", "Y2R", "Y4RA", "Y4RB" ]
		self.osSignals["OSYCJE"] = [ "Y2L", "Y4L", "Y4RA", "Y4RB" ]

		# east end junction
		block = self.blocks["OSYEEW"] 
		self.routes["YRtY10Y11"] = Route(self.screen, block, "YRtY10Y11", "Y11", [ (114, 11), (115, 11), (116, 11), (117, 11), (118, 11), (119, 11), (120, 11), (121, 11) ], "Y10", [RESTRICTING, MAIN])
		self.routes["YRtY30Y11"] = Route(self.screen, block, "YRtY30Y11", "Y11", [ (112, 7), (113, 7), (114, 8), (115, 9), (116, 10), (117, 11), (118, 11), (119, 11), (120, 11), (121, 11) ], "Y30", [RESTRICTING, DIVERGING])
		self.routes["YRtY87Y11"] = Route(self.screen, block, "YRtY87Y11", "Y11", [ (113, 9), (114, 9), (115, 9), (116, 10), (117, 11), (118, 11), (119, 11), (120, 11), (121, 11) ], "Y87", [RESTRICTING, RESTRICTING])

		block = self.blocks["OSYEEE"]
		self.routes["YRtY20Y21"] = Route(self.screen, block, "YRtY20Y21", "Y20", [ (114, 13), (115, 13), (116, 13), (117, 13), (118, 13), (119, 13), (120, 13), (121, 13) ], "Y21", [MAIN, RESTRICTING])
		self.routes["YRtY30Y21"] = Route(self.screen, block, "YRtY30Y21", "Y30", [ (112, 7), (113, 7), (114, 8), (115, 9), (116, 10), (117, 11), (118, 11), (119, 12), (120, 13), (121, 13) ], "Y21", [RESTRICTING, RESTRICTING])
		self.routes["YRtY87Y21"] = Route(self.screen, block, "YRtY87Y21", "Y87", [ (113, 9), (114, 9), (115, 9), (116, 10), (117, 11), (118, 11), (119, 12), (120, 13), (121, 13) ], "Y21", [RESTRICTING, RESTRICTING])
		self.routes["YRtY10Y21"] = Route(self.screen, block, "YRtY10Y21", "Y10", [ (114, 11), (115, 11), (116, 11), (117, 11), (118, 11), (119, 12), (120, 13), (121, 13) ], "Y21", [RESTRICTING, RESTRICTING])

		self.signals["Y8LA"].AddPossibleRoutes("OSYEEW", ["YRtY10Y11"])
		self.signals["Y8LA"].AddPossibleRoutes("OSYEEE", ["YRtY10Y21"])
		self.signals["Y8LB"].AddPossibleRoutes("OSYEEW", ["YRtY87Y11"])
		self.signals["Y8LB"].AddPossibleRoutes("OSYEEE", ["YRtY87Y21"])
		self.signals["Y8LC"].AddPossibleRoutes("OSYEEW", ["YRtY30Y11"])
		self.signals["Y8LC"].AddPossibleRoutes("OSYEEE", ["YRtY30Y21"])
		self.signals["Y8R"].AddPossibleRoutes("OSYEEW", ["YRtY10Y11", "YRtY87Y11", "YRtY30Y11"])
		self.signals["Y10L"].AddPossibleRoutes("OSYEEE", ["YRtY20Y21"])
		self.signals["Y10R"].AddPossibleRoutes("OSYEEE", ["YRtY20Y21", "YRtY10Y21", "YRtY87Y21", "YRtY30Y21"])

		self.osSignals["OSYEEW"] = [ "Y8LA", "Y8LB", "Y8LC", "Y8R" ]
		self.osSignals["OSYEEE"] = [ "Y8LA", "Y8LB", "Y8LC", "Y10L", "Y10R" ]

		return self.signals

	def DefineButtons(self, tiles):
		self.buttons = {}
		self.osButtons = {}


		return self.buttons