import logging

from constants import OCCUPIED, EMPTY, NORMAL, REVERSE, GREEN, OVERSWITCH, RED, STOP

class District:
	def __init__(self, name, frame, screen):
		self.name = name
		self.frame = frame
		self.screen = screen
		logging.info("Creating district %s" % name)

	def Initialize(self, sstiles, misctiles):
		self.sstiles = sstiles
		self.misctiles = misctiles

		blist = [self.frame.GetBlockByName(n) for n in self.osBlocks.keys()]
		self.DetermineRoute(blist)

	def Draw(self):
		for b in self.blocks.values():
			b.Draw()
			b.DrawTurnouts()
		for b in self.buttons.values():
			b.Draw()
		for s in self.signals.values():
			s.Draw()
		for h in self.handswitches.values():
			h.Draw()

	def DrawOthers(self, block):
		pass

	def DetermineRoute(self, blocks):
		pass

	#  Perform... routines handle the user clicking on track diagram components.  This includes, switches, signals, and buttons
	# in most cases, this does not actually make any changed to the display, but instead sends requests to the dispatch server
	def PerformButtonAction(self, btn):
		pass

	def MatrixTurnoutRequest(self, tolist):
		for toname, state in tolist:
			if (state == "R" and self.turnouts[toname].IsNormal()) or \
					(state == "N" and self.turnouts[toname].IsReverse()):
				self.frame.Request({"turnout": {"name": toname, "status": state}})

	def PerformTurnoutAction(self, turnout):
		turnout = turnout.GetControlledBy()
		if turnout.IsLocked():
			self.ReportTurnoutLocked(turnout.GetName())
			return

		if turnout.IsNormal():
			self.frame.Request({"turnout": { "name": turnout.GetName(), "status": "R" }})
		else:
			self.frame.Request({"turnout": { "name": turnout.GetName(), "status": "N" }})

	def FindRoute(self, sig):
		signm = sig.GetName()
		for blknm, siglist in self.osSignals.items():
			if signm in siglist:
				osblk = self.frame.blocks[blknm]
				osblknm = blknm
				rname = osblk.GetRouteName()
				if osblk.route is None:
					continue
				rt = self.routes[rname]
				if sig.IsPossibleRoute(blknm, rname):
					return rt, osblk
		return None, None

	def PerformSignalAction(self, sig):
		aspect = sig.GetAspect()
		signm = sig.GetName()
		color = GREEN if aspect == 0 else RED # the color we are trying to change to
		rt, osblk = self.FindRoute(sig)

		if rt is None:
			self.frame.Popup("No routes found for Signal %s" % (signm))
			return

		osblknm = osblk.GetName()
		if osblk.AreHandSwitchesSet():
			self.frame.Popup("OS Block %s is locked" % osblknm)
			return

		# this is a valid signal for the current route	
		if color == GREEN:	
			if osblk.IsBusy():
				self.frame.Popup("OS Block %s is busy" % osblknm)
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

			if exitBlk.AreHandSwitchesSet():
				self.frame.Popup("OS Exit Block %s is locked" % exitBlk.GetName())
				return

		else: # color == RED
			esig = osblk.GetEntrySignal()	
			if esig is not None and esig.GetName() != signm:
				self.frame.Popup("Signal %s is not for route %s" % (sig.GetName(), rt.GetDescription()))
				return
			aspect = STOP

		# better logic here to determine signal aspect - no need to send color

		self.frame.Request({"signal": { "name": signm, "aspect": aspect }})

	def PerformHandSwitchAction(self, hs):
		if not hs.GetValue():
			# currently unlocked - trying to lock
	
			if hs.IsBlockCleared():
				self.frame.Popup("Block %s has a route cleared through it" % hs.GetBlock().GetName())
				return

			stat = 1
		else:
			stat = 0
			
		self.frame.Request({"handswitch": { "name": hs.GetName(), "status": stat }})

	# The Do... routines handle requests that come in from the dispatch server.  The 3 objects of interest for
	# these requests are blocks, signals, and turnouts
	def DoBlockAction(self, blk, blockend, state):
		bname = blk.GetName()
		blk.SetOccupied(occupied = state == OCCUPIED, blockend=blockend, refresh=True)

		osList = self.frame.GetOSForBlock(bname)
		for osblk in osList:
			osblk.Draw()

	def DoTurnoutAction(self, turnout, state):
		if state == NORMAL:
			turnout.SetNormal(refresh=True)
		else:
			turnout.SetReverse(refresh=True)

	def DoSignalAction(self, sig, aspect):
		signm = sig.GetName()
		if sig.GetAspect() == aspect:
			#no change necessary
			return

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

		self.LockSwitches(osblock.GetName(), sig, aspect!=STOP)


	def LockSwitches(self, osblknm, sig, flag):
		signm = sig.GetName()
		if osblknm in sig.possibleRoutes:
			osblk = self.blocks[osblknm]
			rt = osblk.GetRoute()
			if rt:
				tolist = rt.GetTurnouts()
				for t in tolist:
					to = self.turnouts[t]
					to.SetLock(signm, flag, refresh=True)
					tp = to.GetPaired()
					if tp:
						tp.SetLock(signm, flag, refresh=True)

	def DoHandSwitchAction(self, hs, stat):
		hs.SetValue(stat!=0, refresh=True)

	def CrossingEastWestBoundary(self, blk1, blk2):
		return False
					
	def DefineBlocks(self, tiles):
		self.blocks = {}
		self.osBlocks = {}
		return({}, {})

	def DefineTurnouts(self, tiles):
		self.turnouts = {}
		return({})

	def DefineIndicators(self):
		self.indicators = {}
		return({})

	def DefineSignals(self, tiles):
		self.signals = {}
		return({})

	def DefineButtons(self, tiles):
		self.buttons = {}
		return({})

	def DefineHandSwitches(self, tiles):
		self.handswitches = {}
		return({})

	def ReportBlockBusy(self, blknm):
		self.frame.Popup("Block %s is busy" % blknm)

	def ReportOSBusy(self):
		self.frame.Popup("OS Block is busy")

	def ReportTurnoutLocked(self, tonm):
		self.frame.Popup("Turnout %s is locked" % tonm)

	def Audit(self):
		passedAudit = True
		logging.info("Performing audit for district: %s" % self.name)
		logging.info("Auditing blocks:")
		for blknm, blk in self.blocks.items():
			if blk.GetName() != blknm:
				logging.info("  Block name: %s does not agree with its key: %s" % (blk.GetName(), blknm))
				passedAudit = False
			for t in blk.turnouts:
				tnm = t.GetName()
				if tnm not in self.turnouts:
					logging.info("  Block %s: turnout %s not defined" % (blk.GetName(), tnm))
					passedAudit = False

		logging.info("Auditing OS blocks:")
		for osblknm, blknmlist in self.osBlocks.items():
			if osblknm not in self.frame.blocks:
				logging.info("  OS Block name: %s is not defined" % osblknm)
				passedAudit = False
			for blknm in blknmlist:
				if blknm not in self.frame.blocks:
					logging.info("  Block name %s inside of OSBlock %s is not defined" % (blknm, osblknm))
					passedAudit = False

		logging.info("Auditing Turnouts")
		for tnm, t in self.turnouts.items():
			if tnm != t.GetName():
				logging.info("  Turnout %s, name does not agree with key %s" % (t.GetName(), tnm))
				passedAudit = False
			for blknm in t.blockList:
				if blknm not in self.frame.blocks:
					logging.info("  Block name %s in turnout %s is not defined" % (blknm, tnm))
					passedAudit = False

		logging.info("Auditing Signals")
		for snm, sig in self.signals.items():
			if snm != sig.GetName():
				logging.info("  Signal %s, name does not agree with key %s" % (sig.GetName(), snm))
				passedAudit = False
			for blknm, rtnmlist in sig.possibleRoutes.items():
				if blknm not in self.blocks:
					logging.info("  Possible routes for block %s - block is not defined" % blknm)
					passedAudit = False
				for rtnm in rtnmlist:
					if rtnm not in self.routes:
						logging.info("Route %s for block %s is not defines" % (rtnm, blknm))
						passedAudit = False

		logging.info("Auditing OS Signals")
		for blknm, signmlist in self.osSignals.items():
			if blknm not in self.blocks:
				logging.info("Block %s is not defined" % blknm)
				passedAudit = False
			
			for signm in signmlist:
				if signm not in self.signals:
					logging.info("Block %s, signal %s is not defined" % (blknm, signm))
					passedAudit = False

		logging.info("Auditing Routes")
		for rtnm, rt in self.routes.items():
			if rtnm != rt.GetName():
				logging.info("  Route %s, name does not agree with key %s" % (rt.GetName(), rtnm))
				passedAudit = False
			if rt.blkin not in self.frame.blocks:
				logging.info("Route %s: entry block %s is not defined" % (rt.GetName(), rt.blkin))
				passedAudit = False
			if rt.blkout not in self.frame.blocks:
				logging.info("Route %s: exit block %s is not defined" % (rt.GetName(), rt.blkout))
				passedAudit = False
			for tonm in rt.turnouts:
				if tonm not in self.frame.turnouts:
					logging.info("Route %s, turnout %s not defined" % (rt.GetName(), tonm))
					passedAudit = False

			validPos = [x[2] for x in rt.osblk.tiles]
			toPos = [t.pos for t in self.turnouts.values()]
			validPos.extend(toPos)
			for p in rt.pos:
				if p not in validPos:
					logging.info("Route %s, posiition %d, %d is not in block %s" % (rt.GetName(), p[0], p[1], rt.osblk.GetName()))
					passedAudit = False

		


		return passedAudit

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
		osBlocks = {}
		for t in self.districts.values():
			bl, osbl = t.DefineBlocks(tiles)
			blocks.update(bl)
			osBlocks.update(osbl)

		return blocks, osBlocks

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

	def DefineHandSwitches(self, tiles):
		handswitches = {}
		for t in self.districts.values():
			handswitches.update(t.DefineHandSwitches(tiles))

		return handswitches


	def DefineIndicators(self):
		indicators = {}
		for t in self.districts.values():
			indicators.update(t.DefineIndicators())

		return indicators

	def Audit(self):
		passedAudit = True
		for d in self.districts.values():
			if not d.Audit():
				passedAudit = False

		return passedAudit
