from tower import Tower
from block import Block, OverSwitch
from turnout import Turnout
from button import Button

from constants import HyYdPt, LaKr, NaCl, BLOCK, OVERSWITCH

class Hyde (Tower):
	def __init__(self, name, frame, screen):
		Tower.__init__(self, name, frame, screen)

	def Initialize(self):
		for b in self.blocks.values():
			print("block: %s" % b.GetName())
			if b.GetBlockType() == OVERSWITCH:
				self.DetermineRoute(b)

	def Draw(self):
		for b in self.blocks.values():
			b.Draw()
		for b in self.buttons.values():
			b.Draw()

	def DetermineRoute(self, block):
		bname = block.name
		if bname == "HydeWW":
			s1 = 'N' if self.turnouts["HSw1"].IsNormal() else 'R'
			s3 = 'N' if self.turnouts["HSw3"].IsNormal() else 'R'
			s5 = 'N' if self.turnouts["HSw5"].IsNormal() else 'R'
			s7 = 'N' if self.turnouts["HSw7"].IsNormal() else 'R'

			if s1 + s3 == "NN":
				route = [ (21, 13), (22, 13), (23, 13), (24, 13), (25, 13) ]
			elif s1 + s3 == "NR":
				route = [ (21, 13), (22, 13), (23, 13), (24, 13), (25, 13) ]
			elif s1 + s5 == "RR":
				route = [ (21, 13), (22, 13), (23, 12), (24, 11), (25, 10), (26, 9) ]
			elif s1 + s5 + s7 == "RNR":
				route = [ (21, 13), (22, 13), (23, 12), (24, 11), (25, 10), (26, 9), (27, 8), (28, 7) ]
			elif s1 + s5 + s7 == "RNN":
				route = [ (21, 13), (22, 13), (23, 12), (24, 11), (25, 10), (26, 9), (27, 8), (28, 7), (29, 6), (30, 5) ]
			else:
				route = []
			block.SetRoute(route)

	def PerformButtonAction(self, btn):
		bname = btn.GetName()
		if self.blocks["HydeWW"].IsBusy():
			# take no action unless the block is empty and not cleared
			print("block busy")
			return

		if bname == "HB1":
			self.turnouts["HSw7"].SetReverse()
		elif bname == "HB2":
			self.turnouts["HSw7"].SetNormal()
			self.turnouts["HSw5"].SetNormal()
			self.turnouts["HSw1"].SetReverse()
		elif bname == "HB3":
			self.turnouts["HSw7"].SetReverse()
			self.turnouts["HSw5"].SetNormal()
			self.turnouts["HSw1"].SetReverse()
		elif bname == "HB4":
			self.turnouts["HSw5"].SetReverse()
			self.turnouts["HSw1"].SetReverse()
		elif bname == "HB5":
			self.turnouts["HSw3"].SetReverse()
			self.turnouts["HSw1"].SetNormal()
		elif bname == "HB6":
			self.turnouts["HSw3"].SetNormal()
			self.turnouts["HSw1"].SetNormal()

	def DefineBlocks(self, tiles):
		self.blocks = {}
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
				(tiles["horiznc"], self.screen, (27, 5), False),
				(tiles["horiz"], self.screen, (28, 5), False),
				(tiles["horiznc"], self.screen, (29, 5), False),
			],
			True)

		self.blocks["HydeWW"] = OverSwitch(self, self.frame, "HydeWW", 
			[
				(tiles["diagleft"], self.screen, (29, 6), False),
				(tiles["diagleft"], self.screen, (27, 8), False),
				(tiles["diagleft"], self.screen, (25, 10), False),
				(tiles["diagleft"], self.screen, (24, 11), False),
				(tiles["diagleft"], self.screen, (23, 12), False),
				(tiles["eobleft"], self.screen, (21, 13), False),
				(tiles["horiz"], self.screen, (23, 13), False),
				(tiles["horiz"], self.screen, (24, 13), False),
				(tiles["horiz"], self.screen, (31, 5), False),

				(tiles["horiz"], self.screen, (29, 7), False),
				(tiles["horiz"], self.screen, (30, 7), False),
				(tiles["horiz"], self.screen, (31, 7), False),

				(tiles["horiz"], self.screen, (27, 9), False),
				(tiles["horiz"], self.screen, (28, 9), False),
				(tiles["horiz"], self.screen, (29, 9), False),
				(tiles["horiz"], self.screen, (30, 9), False),
				(tiles["horiz"], self.screen, (31, 9), False),

				(tiles["diagleft"], self.screen, (26, 12), False),
				(tiles["turnleftleft"], self.screen, (27, 11), True),
				(tiles["horiz"], self.screen, (28, 11), False),
				(tiles["horiz"], self.screen, (29, 11), False),
				(tiles["horiz"], self.screen, (30, 11), False),
				(tiles["horiz"], self.screen, (31, 11), False),

				(tiles["horiz"], self.screen, (26, 13), False),
				(tiles["horiz"], self.screen, (27, 13), False),
				(tiles["horiz"], self.screen, (28, 13), False),
				(tiles["horiz"], self.screen, (29, 13), False),
				(tiles["horiz"], self.screen, (30, 13), False),
				(tiles["horiz"], self.screen, (31, 13), False),
			], 
			False)

		return self.blocks

	def DefineTurnouts(self, tiles, blocks):
		self.turnouts = {}

		toList = [
			[ "HSw7b", "toleftleftinv", "HydeWW", (30, 5) ],
			[ "HSw7",  "torightup",     "HydeWW", (28, 7) ],
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
		
		return self.turnouts

	
	def DefineSignals(self, tiles):
		self.signals = {}

		#sigs["HSw7"] = Signal("HSw7", (30, 5), tiles["right"])
		#sigs["C12"] = Signal("C12", (39, 19), tiles["right"], "12", (0, -1))

		return self.signals

	def DefineButtons(self, tiles):
		self.buttons = {}
		print("Hyde Buttons")

		b = Button(self, self.screen, self.frame, "HB1", (27, 5), tiles)
		self.buttons["HB1"] = b

		b = Button(self, self.screen, self.frame, "HB2", (32, 5), tiles)
		self.buttons["HB2"] = b

		b = Button(self, self.screen, self.frame, "HB3", (32, 7), tiles)
		self.buttons["HB3"] = b

		b = Button(self, self.screen, self.frame, "HB4", (32, 9), tiles)
		self.buttons["HB4"] = b

		b = Button(self, self.screen, self.frame, "HB5", (32, 11), tiles)
		self.buttons["HB5"] = b

		b = Button(self, self.screen, self.frame, "HB6", (32, 13), tiles)
		self.buttons["HB6"] = b

		return self.buttons