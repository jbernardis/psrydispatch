from tower import Tower
from block import Block, OverSwitch, Route
from turnout import Turnout
from signal import Signal
from button import Button

from constants import HyYdPt, LaKr, NaCl, BLOCK, OVERSWITCH, NORMAL, REVERSE, RED, GREEN

class Hyde (Tower):
	def __init__(self, name, frame, screen):
		Tower.__init__(self, name, frame, screen)

	def Initialize(self):
		for b in self.blocks.values():
			if b.GetBlockType() == OVERSWITCH:
				self.DetermineRoutes(b)

	def Draw(self):
		for b in self.blocks.values():
			b.Draw()
		for b in self.buttons.values():
			b.Draw()
		for s in self.signals.values():
			s.Draw()

	def DetermineRoutes(self, block):
		print("in determine routes")
		bname = block.name
		if bname == "HydeWW":
			s1 = 'N' if self.turnouts["HSw1"].IsNormal() else 'R'
			s3 = 'N' if self.turnouts["HSw3"].IsNormal() else 'R'
			s5 = 'N' if self.turnouts["HSw5"].IsNormal() else 'R'
			s7 = 'N' if self.turnouts["HSw7"].IsNormal() else 'R'

			routes = []
			if s1 + s3 == "NN":
				routes.append(Route(self.screen, "HWW1", "H11", [ (21, 13), (22, 13), (23, 13), (24, 13), (25, 13), (26, 13), (27, 13), (28, 13), (29, 13), (30, 13), (31, 13) ], "H12"))
			elif s1 + s3 == "NR":
				routes.append(Route(self.screen, "HWW2", "H11", [ (21, 13), (22, 13), (23, 13), (24, 13), (25, 13), (26, 12), (27, 11), (28, 11), (29, 11), (30, 11), (31, 11)], "H34"))
			elif s1 + s5 == "RR":
				routes.append(Route(self.screen, "HWW3", "H11", [ (21, 13), (22, 13), (23, 12), (24, 11), (25, 10), (26, 9), (27, 9), (28, 9), (29, 9), (30, 9), (31, 9) ], "H33"))
			elif s1 + s5 + s7 == "RNN":
				routes.append(Route(self.screen, "HWW4", "H11", [ (21, 13), (22, 13), (23, 12), (24, 11), (25, 10), (26, 9), (27, 8), (28, 7), (29, 7), (30, 7), (31, 7) ], "H32"))
			elif s1 + s5 + s7 == "RNR":
				routes.append(Route(self.screen, "HWW5", "H11", [ (21, 13), (22, 13), (23, 12), (24, 11), (25, 10), (26, 9), (27, 8), (28, 7), (29, 6), (30, 5), (31, 5) ], "H31"))
			
			if s7 == "N":
				routes.append(Route(self.screen, "HWW6", "H30", [ (30, 5), (31, 5) ], "H31"))

			print("routes:")
			for r in routes:
				r.rprint()
			block.SetRoutes(routes)

	def PerformButtonAction(self, btn):
		bname = btn.GetName()
		if bname in self.osButtons["HydeWW"]:
			print("status on HydeWW is %d" % self.blocks["HydeWW"].GetStatus())
			osBlk = self.blocks["HydeWW"]
			if osBlk.IsBusy():
				print("block busy")
				return

			btn.Press(refresh=True)
			self.frame.ClearButtonAfter(2, btn)
			if bname == "HWWB1":
				self.frame.Request({"turnout": [ ["HSw7", REVERSE] ]})
			elif bname == "HWWB2":
				self.frame.Request({"turnout": [ ["HSw7", NORMAL], ["HSw5", NORMAL], ["HSw1", REVERSE] ]})
			elif bname == "HWWB3":
				self.frame.Request({"turnout": [ ["HSw7", REVERSE], ["HSw5", NORMAL], ["HSw1", REVERSE] ]})
			elif bname == "HWWB4":
				self.frame.Request({"turnout": [ ["HSw5", REVERSE], ["HSw1", REVERSE] ]})
			elif bname == "HWWB5":
				self.frame.Request({"turnout": [ ["HSw3", REVERSE], ["HSw1", NORMAL] ]})
			elif bname == "HWWB6":
				self.frame.Request({"turnout": [ ["HSw3", NORMAL], ["HSw1", NORMAL] ]})

	def PerformSignalAction(self, sig):
		aspect = sig.GetAspect()
		#sig.SetAspect(1-aspect, refresh=True)
		color = GREEN if aspect == 0 else RED # the color we are trying to change to
		signm = sig.GetName()
		if signm  in self.osSignals["HydeWW"]:
			osBlk = self.blocks["HydeWW"]
			if signm == "H8L":
				if osBlk.HasRoute("HWW5"):
					print("forward through OS to block H11")
					self.frame.Request({"signal": ["H8L", color, "H11"]})
				elif osBlk.HasRoute("HWW6"):
					print("forward through OS to block H30")
					self.frame.Request({"signal": ["H8L", color, "H30"]})
				else:
					print("ignore signal request")
			elif signm == "H6LA":
				if osBlk.HasRoute("HWW4"):
					self.frame.Request({"signal": ["H6LA", color, "H11"]})
					print("forward though OS to block H11")
				else:
					print("ignore signal request")
			elif signm == "H6LB":
				if osBlk.HasRoute("HWW3"):
					print("forward though OS to block H11")
					self.frame.Request({"signal": ["H6LB", color, "H11"]})
				else:
					print("ignore signal request")
			elif signm == "H6LC":
				if osBlk.HasRoute("HWW2"):
					self.frame.Request({"signal": ["H6LC", color, "H11"]})
					print("forward though OS to block H11")
				else:
					print("ignore signal request")
			elif signm == "H6LD":
				if osBlk.HasRoute("HWW1"):
					self.frame.Request({"signal": ["H6LD", color, "H11"]})
					print("forward though OS to block H11")
				else:
					print("ignore signal request")

	def DoSwitchAction(self, turnout, state):
		print("do switch action %s: %d" % (turnout.GetName(), state))
		if state == NORMAL:
			turnout.SetNormal(refresh=True)
		else:
			turnout.SetReverse(refresh=True)

	def DoSignalAction(self, sig, state, block):
		sig.SetAspect(state, refresh=True)
		sigName = sig.GetName()
		if block is not None:
			block.SetCleared(state==GREEN, refresh=True)

			for osName, signals in self.osSignals.items():
				if sigName in signals:
					self.blocks[osName].Draw()

	def DefineBlocks(self, tiles):
		self.blocks = {}

		self.blocks["H12"] = Block(self, self.frame, "H12",
			[
				(tiles["horiz"], self.screen, (33,13), False),
				(tiles["horiznc"], self.screen, (34,13), False),
				(tiles["horiz"], self.screen, (35,13), False),
				(tiles["horiznc"], self.screen, (36,13), False),
				(tiles["horiz"], self.screen, (37,13), False),
				(tiles["horiznc"], self.screen, (38,13), False),
				(tiles["horiz"], self.screen, (39,13), False),
				(tiles["horiznc"], self.screen, (40,13), False),
			], False)

		self.blocks["H11"] = Block(self, self.frame, "H11",
			[
				(tiles["horiz"], self.screen, (13,13), False),
				(tiles["horiznc"], self.screen, (14,13), False),
				(tiles["horiz"], self.screen, (15,13), False),
				(tiles["horiznc"], self.screen, (16,13), False),
				(tiles["horiz"], self.screen, (17,13), False),
				(tiles["horiznc"], self.screen, (18,13), False),
				(tiles["horiz"], self.screen, (19,13), False),
				(tiles["horiznc"], self.screen, (20,13), False),

				(tiles["eobleft"], LaKr, (123,11), False),
				(tiles["horiz"], LaKr, (124,11), False),
				(tiles["horiznc"], LaKr, (125,11), False),
				(tiles["horiz"], LaKr, (126,11), False),
				(tiles["horiznc"], LaKr, (127,11), False),
			], False)

		self.blocks["H30"] = Block(self, self.frame, "H30",
			[
				(tiles["horiznc"], self.screen, (13, 11), False),
				(tiles["horiz"], self.screen, (14, 11), False),
				(tiles["horiznc"], self.screen, (15, 11), False),
				(tiles["horiz"], self.screen, (16, 11), False),
				(tiles["horiznc"], self.screen, (17, 11), False),
				(tiles["horiz"], self.screen, (18, 11), False),
				(tiles["turnleftright"], self.screen, (19, 11), False),
				(tiles["diagleft"], self.screen, (20, 10), False),
				(tiles["diagleft"], self.screen, (21, 9), False),
				(tiles["diagleft"], self.screen, (22, 8), False),
				(tiles["diagleft"], self.screen, (23, 7), False),
				(tiles["diagleft"], self.screen, (24, 6), False),
				(tiles["turnleftleft"], self.screen, (25, 5), True),
				(tiles["horiz"], self.screen, (26, 5), False),
				(tiles["horiz"], self.screen, (28, 5), False),
				(tiles["horiznc"], self.screen, (29, 5), False),

				(tiles["eobleft"], LaKr, (106, 9), False),
				(tiles["horiznc"], LaKr, (107, 9), False),
				(tiles["horiz"], LaKr, (108, 9), False),
				(tiles["horiznc"], LaKr, (109, 9), False),
				(tiles["horiz"], LaKr, (110, 9), False),
				(tiles["horiznc"], LaKr, (111, 9), False),
				(tiles["horiz"], LaKr, (112, 9), False),
				(tiles["horiznc"], LaKr, (113, 9), False),
				(tiles["horiz"], LaKr, (114, 9), False),
				(tiles["horiznc"], LaKr, (115, 9), False),
				(tiles["horiz"], LaKr, (116, 9), False),
				(tiles["horiznc"], LaKr, (117, 9), False),
				(tiles["horiz"], LaKr, (118, 9), False),
				(tiles["horiznc"], LaKr, (119, 9), False),
				(tiles["horiz"], LaKr, (120, 9), False),
				(tiles["horiznc"], LaKr, (121, 9), False),
				(tiles["horiz"], LaKr, (122, 9), False),
				(tiles["horiznc"], LaKr, (123, 9), False),
				(tiles["horiz"], LaKr, (124, 9), False),
				(tiles["horiznc"], LaKr, (125, 9), False),
				(tiles["horiz"], LaKr, (126, 9), False),
				(tiles["horiznc"], LaKr, (127, 9), False),
			],
			False)

		self.blocks["H31"] = Block(self, self.frame, "H31",
			[
				(tiles["horiz"], self.screen, (33,5), False),
				(tiles["horiznc"], self.screen, (34,5), False),
				(tiles["horiz"], self.screen, (35,5), False),
				(tiles["horiznc"], self.screen, (36,5), False),
				(tiles["horiz"], self.screen, (37,5), False),
				(tiles["horiznc"], self.screen, (38,5), False),
				(tiles["horiz"], self.screen, (39,5), False),
				(tiles["horiznc"], self.screen, (40,5), False),
			], False)

		self.blocks["H32"] = Block(self, self.frame, "H32",
			[
				(tiles["horiz"], self.screen, (33,7), False),
				(tiles["horiznc"], self.screen, (34,7), False),
				(tiles["horiz"], self.screen, (35,7), False),
				(tiles["horiznc"], self.screen, (36,7), False),
				(tiles["horiz"], self.screen, (37,7), False),
				(tiles["horiznc"], self.screen, (38,7), False),
				(tiles["horiz"], self.screen, (39,7), False),
				(tiles["horiznc"], self.screen, (40,7), False),
			], False)

		self.blocks["H33"] = Block(self, self.frame, "H33",
			[
				(tiles["horiz"], self.screen, (33,9), False),
				(tiles["horiznc"], self.screen, (34,9), False),
				(tiles["horiz"], self.screen, (35,9), False),
				(tiles["horiznc"], self.screen, (36,9), False),
				(tiles["horiz"], self.screen, (37,9), False),
				(tiles["horiznc"], self.screen, (38,9), False),
				(tiles["horiz"], self.screen, (39,9), False),
				(tiles["horiznc"], self.screen, (40,9), False),
			], False)

		self.blocks["H34"] = Block(self, self.frame, "H34",
			[
				(tiles["horiz"], self.screen, (33,11), False),
				(tiles["horiznc"], self.screen, (34,11), False),
				(tiles["horiz"], self.screen, (35,11), False),
				(tiles["horiznc"], self.screen, (36,11), False),
				(tiles["horiz"], self.screen, (37,11), False),
				(tiles["horiznc"], self.screen, (38,11), False),
				(tiles["horiz"], self.screen, (39,11), False),
				(tiles["horiznc"], self.screen, (40,11), False),
			], False)

		self.blocks["HydeWW"] = OverSwitch(self, self.frame, "HydeWW", 
			[
				(tiles["diagleft"], self.screen, (29, 6), False),
				(tiles["diagleft"], self.screen, (27, 8), False),
				(tiles["diagleft"], self.screen, (25, 10), False),
				(tiles["diagleft"], self.screen, (24, 11), False),
				(tiles["diagleft"], self.screen, (23, 12), False),
				(tiles["eobleft"], self.screen, (21, 13), False),
				(tiles["horiznc"], self.screen, (23, 13), False),
				(tiles["horiz"], self.screen, (24, 13), False),
				(tiles["horiz"], self.screen, (31, 5), False),

				(tiles["horiznc"], self.screen, (29, 7), False),
				(tiles["horiz"], self.screen, (30, 7), False),
				(tiles["horiznc"], self.screen, (31, 7), False),

				(tiles["horiznc"], self.screen, (27, 9), False),
				(tiles["horiz"], self.screen, (28, 9), False),
				(tiles["horiznc"], self.screen, (29, 9), False),
				(tiles["horiz"], self.screen, (30, 9), False),
				(tiles["horiznc"], self.screen, (31, 9), False),

				(tiles["diagleft"], self.screen, (26, 12), False),
				(tiles["turnleftleft"], self.screen, (27, 11), True),
				(tiles["horiz"], self.screen, (28, 11), False),
				(tiles["horiznc"], self.screen, (29, 11), False),
				(tiles["horiz"], self.screen, (30, 11), False),
				(tiles["horiznc"], self.screen, (31, 11), False),

				(tiles["horiz"], self.screen, (26, 13), False),
				(tiles["horiznc"], self.screen, (27, 13), False),
				(tiles["horiz"], self.screen, (28, 13), False),
				(tiles["horiznc"], self.screen, (29, 13), False),
				(tiles["horiz"], self.screen, (30, 13), False),
				(tiles["horiznc"], self.screen, (31, 13), False),
			], 
			False)

		return self.blocks

	def DefineTurnouts(self, tiles, blocks):
		self.turnouts = {}

		toList = [
			[ "HSw7b", "toleftleft",    "HydeWW", (30, 5) ],
			[ "HSw7",  "torightupinv",  "HydeWW", (28, 7) ],
			[ "HSw5",  "torightup",     "HydeWW", (26, 9) ],
			[ "HSw3",  "toleftright",   "HydeWW", (25, 13) ],
			[ "HSw1",  "toleftright",   "HydeWW", (22, 13) ]
		]

		for tonm, tileSet, blknm, pos in toList:
			trnout = Turnout(self, self.frame, tonm, self.screen, tiles[tileSet], blocks[blknm], pos)
			blocks[blknm].AddTurnout(trnout)
			self.turnouts[tonm] = trnout
		
		for tonm in [ "HSw1", "HSw3", "HSw5", "HSw7", "HSw7b" ]:
			self.turnouts[tonm].SetRouteControl(True)

		self.turnouts["HSw7"].SetPairedTurnout(self.turnouts["HSw7b"])

		self.osTurnouts = {}
		self.osTurnouts["HydeWW"] = ["HSw1", "HSw3", "HSw5", "HSw7", "HSw7b" ]
		
		return self.turnouts

	
	def DefineSignals(self, tiles):
		self.signals = {}

		sigList = [
			[ "H8L",  "left", (32, 4) ],
			[ "H6LA", "left", (32, 6) ],
			[ "H6LB", "left", (32, 8) ],
			[ "H6LC", "left", (32,10) ],
			[ "H6LD", "left", (32, 12) ]
		]
		for signm, tileSet, pos in sigList:
			sig = Signal(self, self.screen, self.frame, signm, pos, tiles[tileSet])  
			self.signals[signm] = sig         
		self.osSignals = {}
		self.osSignals["HydeWW"] = [ "H8L", "H6LA", "H6LB", "H6LC", "H6LD" ]
		return self.signals

	def DefineButtons(self, tiles):
		self.buttons = {}

		b = Button(self, self.screen, self.frame, "HWWB1", (27, 5), tiles)
		self.buttons["HWWB1"] = b

		b = Button(self, self.screen, self.frame, "HWWB2", (32, 5), tiles)
		self.buttons["HWWB2"] = b

		b = Button(self, self.screen, self.frame, "HWWB3", (32, 7), tiles)
		self.buttons["HWWB3"] = b

		b = Button(self, self.screen, self.frame, "HWWB4", (32, 9), tiles)
		self.buttons["HWWB4"] = b

		b = Button(self, self.screen, self.frame, "HWWB5", (32, 11), tiles)
		self.buttons["HWWB5"] = b

		b = Button(self, self.screen, self.frame, "HWWB6", (32, 13), tiles)
		self.buttons["HWWB6"] = b

		self.osButtons = {}
		self.osButtons["HydeWW"] = [ "HWWB1", "HWWB2", "HWWB3", "HWWB4", "HWWB5", "HWWB6" ]

		return self.buttons