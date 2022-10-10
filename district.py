from constants import OCCUPIED, EMPTY, NORMAL, REVERSE, GREEN, OVERSWITCH, RED, STOP

class District:
	def __init__(self, name, frame, screen):
		self.name = name
		self.frame = frame
		self.screen = screen

	def Initialize(self, sstiles, misctiles):
		self.sstiles = sstiles
		self.misctiles = misctiles

		for t in self.turnouts.values():
			t.initialize()

		blist = [b.GetName() for b in self.blocks.values() if b.GetBlockType() == OVERSWITCH]
		self.DetermineRoute(blist)

	def Draw(self):
		for b in self.blocks.values():
			b.Draw()
			b.DrawTurnouts()
		for b in self.buttons.values():
			b.Draw()
		for s in self.signals.values():
			s.Draw()

	def DrawOthers(self, block):
		pass

	def DetermineRoute(self, blocks):
		print("District %s does not have an implementation of DetermineRoute" % self.name)

	#  Perform... routines handle the user clicking on track diagram components.  This includes, switches, signals, and buttons
	# in most cases, this does not actually make any changed to the display, but instead sends requests to the dispatch server
	def PerformButtonAction(self, btn):
		print("District %s does not have an implementation of PerformButtonAction" % self.name)

	def MatrixTurnoutRequest(self, tolist):
		for toname, state in tolist:
			if (state == "R" and self.turnouts[toname].IsNormal()) or \
					(state == "N" and self.turnouts[toname].IsReverse()):
				self.frame.Request({"turnout": {"name": toname, "status": state}})

	def PerformTurnoutAction(self, turnout):
		blocks = [ blk for blk in self.osTurnouts if turnout.name in self.osTurnouts[blk]]
		print(str(blocks))
		for bname in blocks:
			print("looking at block (%s)" % bname)
			blk = self.frame.GetBlockByName(bname)
			if blk.IsBusy():
				self.reportBlockBusy(bname)
				return
		print("past block loop")

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

		if osblk.AreLocksSet():
			self.frame.Popup("OS Block %s is locked" % osblknm)
			return

		# this is a valid signal for the current route	
		if color == GREEN:	
			if osblk.IsBusy():
				self.frame.Popup("OS Block %s is busy" % osblk.GetName())
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
				self.frame.Popup("OS Exit Block %s is busy" % exitBlk.GetName())
				return

			if exitBlk.AreLocksSet():
				self.frame.Popup("OS Exit Block %s is locked" % exitBlk.GetName())
				return

		else: # color == RED
			esig = osblk.GetEntrySignal()	
			if esig is not None and esig.GetName() != signm:
				self.frame.Popup("Signal %s is not for route %s" % (signm, rt.GetDescription()))
				return
			aspect = STOP

		# better logic here to determine signal aspect - no need to send color

		self.frame.Request({"signal": { "name": signm, "aspect": aspect }})

	def PerformLockAction(self, lk):
		if not lk.GetValue():
			# currently unlocked - trying to lock
	
			if lk.IsBlockBusy():
				self.frame.Popup("Block %s is busy" % lk.GetBlock().GetName())
				return

			stat = 1
		else:
			stat = 0
			
		self.frame.Request({"lock": { "name": lk.GetName(), "status": stat }})

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

	def DoSignalAction(self, sig, aspect):
		signm = sig.GetName()
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

		# all checking was done on the sending side, so this is a valid request - just do it
		osblock.SetEast(sig.GetEast())
		sig.SetAspect(aspect, refresh=True)
		osblock.SetEntrySignal(sig)
		osblock.SetCleared(aspect != STOP, refresh=True)

		# now see if it should be propagated to the exit block
		if osblock.IsBusy() and aspect == STOP:
			return

		exitBlkNm = rt.GetExitBlock()
		exitBlk = self.frame.GetBlockByName(exitBlkNm)
		if exitBlk.IsOccupied():
			return

		if self.CrossingEastWestBoundary(osblock, exitBlk):
			nd = not sig.GetEast()
		else:
			nd = sig.GetEast()
		exitBlk.SetEast(nd)
		exitBlk.SetCleared(aspect!=STOP, refresh=True)

	def DoLockAction(self, lk, stat):
		lk.SetValue(stat!=0, refresh=True)

	def CrossingEastWestBoundary(self, blk1, blk2):
		return False
					
	def DefineBlocks(self, tiles):
		print("District %s does not have an implementation of DefineBlocks" % self.name)
		self.blocks = {}
		return({})

	def DefineTurnouts(self, tiles):
		print("District %s does not have an implementation of DefineTurnouts" % self.name)
		self.turnouts = {}
		return({})

	def DefineSignals(self, tiles):
		print("District %s does not have an implementation of DefineSignals" % self.name)
		self.signals = {}
		return({})

	def DefineButtons(self, tiles):
		print("District %s does not have an implementation of DefineButtons" % self.name)
		self.buttons = {}
		return({})

	def DefineLocks(self, tiles):
		print("District %s does not have an implementation of DefineLocks" % self.name)
		self.locks = {}
		return({})

	def reportBlockBusy(self, blknm):
		self.frame.Popup("Block %s is busy" % blknm)


class Districts:
	def __init__(self):
		self.districts = {}

	def AddDistrict(self, district):
		self.districts[district.name] = district

	def Initialize(self, sstiles, misctiles):
		for t in self.districts.values():
			t.Initialize(sstiles, misctiles)

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

	def DefineLocks(self, tiles):
		locks = {}
		for t in self.districts.values():
			locks.update(t.DefineLocks(tiles))

		return locks
