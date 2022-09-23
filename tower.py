from constants import OCCUPIED, NORMAL, GREEN, OVERSWITCH, TOGGLE, RED

class Tower:
	def __init__(self, name, frame, screen):
		self.name = name
		self.frame = frame
		self.screen = screen

	def Initialize(self):
		for b in self.blocks.values():
			if b.GetBlockType() == OVERSWITCH:
				self.DetermineRoute(b)

	def Draw(self):
		for b in self.blocks.values():
			b.Draw()
		for b in self.buttons.values():
			b.Draw()
		for s in self.signals.values():
			s.Draw()

	def DetermineRoute(self, block):
		print("Tower %s does not have an implementation of DetermineRoute" % self.name)

	#  Perform... routines handle the user clicking on track diagram components.  This includes, switches, signals, and buttons
	# in most cases, this does not actually make any changed to the display, but instead sends requests to the dispatch server
	def PerformButtonAction(self, btn):
		print("Tower %s does not have an implementation of PerformButtonAction" % self.name)

	def PerformTurnoutAction(self, turnout):
		if turnout.Changeable():
			self.frame.Request({"turnout": { "name": turnout.GetName(), "action": TOGGLE }})

	def PerformSignalAction(self, sig):
		aspect = sig.GetAspect()
		color = GREEN if aspect == 0 else RED # the color we are trying to change to
		signm = sig.GetName()
		for blknm, siglist in self.osSignals.items():
			print("looking at block %s, signals %s" % (blknm, str(siglist)))
			if signm in siglist:
				print("signal in list")
				osblk = self.frame.blocks[blknm]
				osblknm = blknm
				rname = osblk.GetRouteName()
				rt = self.routes[rname]
				if sig.IsPossibleRoute(blknm, rname):
					break
		else:
			self.frame.Popup("Signal %s is not for route %s" % (signm, rt.GetDescription()))
			return

		# this is a valid signal for the current route	
		if color == GREEN:	
			if osblk.IsBusy():
				self.frame.Popup("OS Block %s is occupied" % osblk.GetName())
				print("OS Block is busy")
				return
			exitBlkNm = rt.GetExitBlock()
			exitBlk = self.frame.blocks[exitBlkNm]
			if exitBlk.IsBusy():
				self.frame.Popup("OS Exit Block %s is occupied" % exitBlk.GetName())
				print("exit block is busy")
				return
		else: # color == RED
			esig = osblk.GetEntrySignal()	
			if esig is not None and esig.GetName() != signm:
				self.frame.Popup("Signal %s is not for route %s" % (signm, rt.GetDescription()))
				print("route can only be reset by the entry signal")
				return

		self.frame.Request({"signal": { "name": signm, "state": color }})

	# The Do... routines handle requests that come in from the dispatch server.  The 3 objects of interest for
	# these requests are blocks, signals, and turnouts
	def DoBlockAction(self, blk, blockend, state):
		bname = blk.GetName()
		blk.SetOccupied(occupied = state == OCCUPIED, blockend=blockend, refresh=True)

		for osblknm, blkList in self.osBlocks.items():
			if bname in blkList:
				self.blocks[osblknm].Draw()

	def DoTurnoutAction(self, turnout, state):
		if state == NORMAL:
			turnout.SetNormal(refresh=True)
		else:
			turnout.SetReverse(refresh=True)

	def DoSignalAction(self, sig, state):
		signm = sig.GetName()
		print("do signal action")
		for blknm, siglist in self.osSignals.items():
			if signm in siglist:
				osblock = self.frame.blocks[blknm]
				rname = osblock.GetRouteName()
				rt = self.routes[rname]
				if sig.IsPossibleRoute(blknm, rname):
					print("matching route: %s %s" % (blknm, rname))
					break
		else:
			return

		# all checking was done on the sending side, so this is a valid request - just do it
		sig.SetAspect(state, refresh=True)
		osblock.SetEast(sig.GetEast())
		osblock.SetEntrySignal(sig)
		osblock.SetCleared(state==GREEN, refresh=True)

		# now see if it should be propagated to the exit block
		if osblock.IsBusy() and state == RED:
			print("do not propagate RED past busy OS block")
			return

		exitBlkNm = rt.GetExitBlock()
		exitBlk = self.frame.blocks[exitBlkNm]
		if exitBlk.IsOccupied():
			print("do not propagate to an Occupied block")
			return

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

	def reportBlockBusy(self, blknm):
		self.frame.Popup("Block %s is busy" % blknm)


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
