from constants import OCCUPIED, NORMAL, REVERSE, GREEN, OVERSWITCH, RED, STOP

class District:
	def __init__(self, name, frame, screen):
		self.name = name
		self.frame = frame
		self.screen = screen

	def Initialize(self, sstiles, generictiles):
		self.sstiles = sstiles
		self.generictiles = generictiles

		for t in self.turnouts.values():
			print("initializing turnout %s" % t.GetName())
			t.initialize()

		blist = [b.GetName() for b in self.blocks.values() if b.GetBlockType() == OVERSWITCH]
		self.DetermineRoute(blist)

	def Draw(self):
		for b in self.blocks.values():
			b.Draw()
		for b in self.buttons.values():
			b.Draw()
		for s in self.signals.values():
			s.Draw()

	def DrawRoute(self, block):
		pass

	def DetermineRoute(self, blocks):
		print("District %s does not have an implementation of DetermineRoute" % self.name)

	#  Perform... routines handle the user clicking on track diagram components.  This includes, switches, signals, and buttons
	# in most cases, this does not actually make any changed to the display, but instead sends requests to the dispatch server
	def PerformButtonAction(self, btn):
		print("District %s does not have an implementation of PerformButtonAction" % self.name)

	def PerformTurnoutAction(self, turnout):
		print(turnout.GetName())
		blocks = [ blk for blk in self.osTurnouts if turnout.name in self.osTurnouts[blk]]
		print(str(blocks))
		for bname in blocks:
			blk = self.frame.GetBlockByName(bname)
			if blk.IsBusy():
				self.reportBlockBusy(bname)
				return

		turnout = turnout.GetControlledBy()
		if turnout.Changeable():
			if turnout.IsNormal():
				self.frame.Request({"turnout": { "name": turnout.GetName(), "status": "R" }})
			else:
				self.frame.Request({"turnout": { "name": turnout.GetName(), "status": "N" }})

	def PerformSignalAction(self, sig):
		aspect = sig.GetAspect()
		color = GREEN if aspect == 0 else RED # the color we are trying to change to
		signm = sig.GetName()
		rt = None
		for blknm, siglist in self.osSignals.items():
			if signm in siglist:
				osblk = self.frame.blocks[blknm]
				osblknm = blknm
				rname = osblk.GetRouteName()
				if osblk.route is None:
					continue
				rt = self.routes[rname]
				if sig.IsPossibleRoute(blknm, rname):
					break

		else:
			if rt is None:
				self.frame.Popup("No routes found for Signal %s" % (signm))
			else:
				self.frame.Popup("Signal %s is not for route %s" % (signm, rt.GetDescription()))
			return

		# this is a valid signal for the current route	
		if color == GREEN:	
			if osblk.IsBusy():
				self.frame.Popup("OS Block %s is occupied" % osblk.GetName())
				return

			sigE = sig.GetEast()
			if sigE != osblk.GetEast():
				# the block will need to be reversed, but it's premature
				# to do so now - so force return values as if reversed
				exitBlkNm = rt.GetExitBlock(reverse=True)
				aspect = rt.GetRouteType(reverse=True)
			else:
				exitBlkNm = rt.GetExitBlock()
				aspect = rt.GetRouteType()

			exitBlk = self.frame.blocks[exitBlkNm]
			if exitBlk.IsBusy():
				self.frame.Popup("OS Exit Block %s is occupied" % exitBlk.GetName())
				return

		else: # color == RED
			esig = osblk.GetEntrySignal()	
			if esig is not None and esig.GetName() != signm:
				self.frame.Popup("Signal %s is not for route %s" % (signm, rt.GetDescription()))
				return
			aspect = STOP

		# better logic here to determine signal aspect - no need to send color

		self.frame.Request({"signal": { "name": signm, "aspect": aspect }})

	# The Do... routines handle requests that come in from the dispatch server.  The 3 objects of interest for
	# these requests are blocks, signals, and turnouts
	def DoBlockAction(self, blk, blockend, state):
		bname = blk.GetName()
		blk.SetOccupied(occupied = state == OCCUPIED, blockend=blockend, refresh=True)

		for osblknm, blkList in self.osBlocks.items():
			if bname in blkList:
				self.blocks[osblknm].Draw()

	def DoTurnoutAction(self, turnout, state):
		print("district do turnout %s" % turnout.GetName())
		if state == NORMAL:
			print("call normal")
			turnout.SetNormal(refresh=True)
		else:
			print("call reverse")
			turnout.SetReverse(refresh=True)

	def DoSignalAction(self, sig, aspect):
		signm = sig.GetName()
		print("do signal %s" % signm)
		for blknm, siglist in self.osSignals.items():
			if signm in siglist:
				osblock = self.frame.blocks[blknm]
				rname = osblock.GetRouteName()
				if osblock.route is None:
					continue
				rt = self.routes[rname]
				if sig.IsPossibleRoute(blknm, rname):
					break
		else:
			return

		print("block route: %s/%s" % (blknm, rname))
		print("calling seteast with value %s" % str(sig.GetEast()))

		# all checking was done on the sending side, so this is a valid request - just do it
		osblock.SetEast(sig.GetEast())
		sig.SetAspect(aspect, refresh=True)
		osblock.SetEntrySignal(sig)
		osblock.SetCleared(aspect != STOP, refresh=True)

		# now see if it should be propagated to the exit block
		if osblock.IsBusy() and aspect == STOP:
			#print("do not propagate RED past busy OS block")
			return

		exitBlkNm = rt.GetExitBlock()
		print("retrieved exit block as %s" % exitBlkNm)
		exitBlk = self.frame.GetBlockByName(exitBlkNm)
		if exitBlk.IsOccupied():
			#print("do not propagate to an Occupied block")
			return

		exitBlk.SetEast(sig.GetEast())
		exitBlk.SetCleared(aspect!=STOP, refresh=True)
					
	def DefineBlocks(self, tiles):
		print("District %s does not have an implementation of DefineBlocks" % self.name)

	def DefineTurnouts(self, tiles):
		print("District %s does not have an implementation of DefineTurnouts" % self.name)

	def DefineSignals(self, tiles):
		print("District %s does not have an implementation of DefineSignals" % self.name)

	def DefineButtons(self, tiles):
		print("District %s does not have an implementation of DefineButtons" % self.name)

	def reportBlockBusy(self, blknm):
		self.frame.Popup("Block %s is busy" % blknm)


class Districts:
	def __init__(self):
		self.districts = {}

	def AddDistrict(self, district):
		self.districts[district.name] = district

	def Initialize(self, sstiles, generictiles):
		for t in self.districts.values():
			t.Initialize(sstiles, generictiles)

	def Draw(self):
		for t in self.districts.values():
			t.Draw()

	def DefineBlocks(self, tiles):
		blocks = {}
		for t in self.districts.values():
			blocks.update(t.DefineBlocks(tiles))

		return blocks

	def DefineTurnouts(self, tiles, blocks):
		tos = {}
		for t in self.districts.values():
			tos.update(t.DefineTurnouts(tiles, blocks))

		return tos

	def DefineSignals(self, tiles):
		sigs = {}
		for t in self.districts.values():
			sigs.update(t.DefineSignals(tiles))

		return sigs

	def DefineButtons(self, tiles):
		btns = {}
		for t in self.districts.values():
			btns.update(t.DefineButtons(tiles))

		return btns
