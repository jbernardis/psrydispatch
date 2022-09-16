from constants import OCCUPIED, NORMAL, GREEN

class Tower:
	def __init__(self, name, frame, screen):
		self.name = name
		self.frame = frame
		self.screen = screen

	def Initialize(self):
		print("Tower %s does not have an implementation of Initialize" % self.name)

	def Draw(self):
		print("Tower %s does not have an implementation of Draw" % self.name)

	def DetermineRoute(self, block):
		print("Tower %s does not have an implementation of DetermineRoute" % self.name)

	#  Perform... routines handle the user clicking on track diagram components.  This includes, switched, signals, and buttons
	# in most cases, this does not actually make any changed to the display, but instead sends requests to the dispatch server
	def PerformButtonAction(self, btn):
		print("Tower %s does not have an implementation of PerformAction" % self.name)

	def PerformTurnoutAction(self, turnout):
		print("Tower %s does not have an implementation of PerformTurnoutAction" % self.name)

	def PerformSignalAction(self, signal):
		print("Tower %s does not have an implementation of PerformSignalAction" % self.name)

	# The Do... routines handle requests that come in from the dispatch server.  The 3 objects of interest for
	# these requests are blocks, signals, and turnouts
	def DoBlockAction(self, blk, state):
		bname = blk.GetName()
		print("Block occupied: %s %s" % (self.name, bname))
		blk.SetOccupied(occupied = state == OCCUPIED, refresh=True)

		for osblknm, blkList in self.osBlocks.items():
			if bname in blkList:
				print("osblk: %s" % osblknm)
				self.blocks[osblknm].Draw()

	def DoTurnoutAction(self, turnout, state):
		if state == NORMAL:
			turnout.SetNormal(refresh=True)
		else:
			turnout.SetReverse(refresh=True)

	def DoSignalAction(self, sig, state, osblock):
		sig.SetAspect(state, refresh=True)
		sigName = sig.GetName()
		if osblock is not None:
			if state == GREEN:
				osblock.SetEast(sig.GetEast())
				osblock.SetEntrySignal(sig)
			osblock.SetCleared(state==GREEN, refresh=True)
			rte = osblock.GetRoute()
			if rte is not None:
				exitBlkName = rte.GetExitBlock()
				exitBlk = self.frame.GetBlockByName(exitBlkName)
				if exitBlk is not None:
					if state == GREEN:
						exitBlk.SetEast(sig.GetEast())
					exitBlk.SetCleared(state==GREEN, refresh=True)
					
	def DefineBlocks(self, tiles):
		print("Tower %s does not have an implementation of DefineBlocks" % self.name)

	def DefineTurnouts(self, tiles):
		print("Tower %s does not have an implementation of DefineTurnouts" % self.name)

	def DefineSignals(self, tiles):
		print("Tower %s does not have an implementation of DefineSignals" % self.name)

	def DefineButtons(self, tiles):
		print("Tower %s does not have an implementation of DefineButtons" % self.name)

class Towers:
	def __init__(self):
		self.towers = {}

	def AddTower(self, tower):
		self.towers[tower.name] = tower

	def Initialize(self):
		for t in self.towers.values():
			t.Initialize()

	def Draw(self):
		for t in self.towers.values():
			t.Draw()

	def DefineBlocks(self, tiles):
		blocks = {}
		for t in self.towers.values():
			blocks.update(t.DefineBlocks(tiles))

		return blocks

	def DefineTurnouts(self, tiles, blocks):
		tos = {}
		for t in self.towers.values():
			tos.update(t.DefineTurnouts(tiles, blocks))

		return tos

	def DefineSignals(self, tiles):
		sigs = {}
		for t in self.towers.values():
			sigs.update(t.DefineSignals(tiles))

		return sigs

	def DefineButtons(self, tiles):
		btns = {}
		for t in self.towers.values():
			btns.update(t.DefineButtons(tiles))

		return btns
