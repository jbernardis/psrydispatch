import logging
import json

from constants import RegAspects, RegSloAspects, AdvAspects, SloAspects, \
	MAIN, SLOW, DIVERGING, RESTRICTING, \
	CLEARED, OCCUPIED, STOP, NORMAL, OVERSWITCH


class District:
	def __init__(self, name, frame, screen):
		self.sigLeverMap = None
		self.routes = None
		self.osSignals = None
		self.handswitches = None
		self.buttons = None
		self.osButtons = None
		self.signals = None
		self.indicators = None
		self.turnouts = None
		self.osBlocks = None
		self.blocks = None
		self.misctiles = None
		self.sstiles = None
		self.name = name
		self.frame = frame
		self.screen = screen
		self.eastGroup = {}
		self.westGroup = {}
		self.eastButton = {}
		self.westButton = {}
		logging.info("Creating district %s" % name)

	def Initialize(self, sstiles, misctiles):
		self.sstiles = sstiles
		self.misctiles = misctiles

		blist = [self.frame.GetBlockByName(n) for n in self.osBlocks.keys()]
		self.DetermineRoute(blist)

	def OnConnect(self):
		pass

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

	#  Perform... routines handle the user clicking on track diagram components.  This includes, switches, signals,
	#  and buttons
	#  in most cases, this does not actually make any changed to the display, but instead sends
	#  requests to the dispatch server
	def PerformButtonAction(self, btn):
		pass

	def DoEntryExitButtons(self, btn, groupName):
		bname = btn.GetName()
		if self.westButton[groupName] and not self.westButton[groupName].IsPressed():
			self.westButton[groupName] = None
		if self.eastButton[groupName] and not self.eastButton[groupName].IsPressed():
			self.eastButton[groupName] = None

		if bname in self.westGroup[groupName]:
			if self.westButton[groupName]:
				self.frame.ClearButtonNow(self.westButton[groupName])

			btn.Press(refresh=True)
			self.westButton[groupName] = btn
			self.frame.ClearButtonAfter(5, btn)

		if bname in self.eastGroup[groupName]:
			if self.eastButton[groupName]:
				self.frame.ClearButtonNow(self.eastButton[groupName])

			btn.Press(refresh=True)
			self.eastButton[groupName] = btn
			self.frame.ClearButtonAfter(5, btn)

		wButton = self.westButton[groupName]
		eButton = self.eastButton[groupName]
		if wButton and eButton:
			self.frame.ResetButtonExpiry(2, wButton)
			self.frame.ResetButtonExpiry(2, eButton)
			try:
				toList = self.NXMap[wButton.GetName()][eButton.GetName()]
			except KeyError:
				toList = None

			if toList is None or self.anyTurnoutLocked(toList):
				wButton.Invalidate(refresh=True)
				eButton.Invalidate(refresh=True)
				self.frame.Popup("No available route")

			else:
				wButton.Acknowledge(refresh=True)
				eButton.Acknowledge(refresh=True)
				self.MatrixTurnoutRequest(toList)
				# self.frame.Request({"nxbutton": { "entry": wButton.GetName(),  "exit": eButton.GetName()}})

			self.westButton[groupName] = None
			self.eastButton[groupName] = None


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
			self.frame.Request({"turnout": {"name": turnout.GetName(), "status": "R"}})
		else:
			self.frame.Request({"turnout": {"name": turnout.GetName(), "status": "N"}})

	def FindRoute(self, sig):
		signm = sig.GetName()
		print("find route for signal %s" % signm)
		print("possible routes: %s" % json.dumps(sig.possibleRoutes))
		for blknm, siglist in self.osSignals.items():
			print("block, sigs = %s %s" % (blknm, str(siglist)))
			if signm in siglist:
				osblk = self.frame.blocks[blknm]
				osblknm = blknm
				rname = osblk.GetRouteName()
				print("os: %s route: %s" % (osblknm, str(rname)))
				if osblk.route is None:
					continue

				rt = self.routes[rname]
				if sig.IsPossibleRoute(blknm, rname):
					print("good route")
					return rt, osblk
				print("not a possible route")

		print("no route found")
		return None, None

	def PerformSignalAction(self, sig):
		print("PSA %s %s" % (sig.GetName(), sig.GetAspect()))
		currentMovement = sig.GetAspect() != 0  # does the CURRENT signal status allow movement
		signm = sig.GetName()
		rt, osblk = self.FindRoute(sig)

		if rt is None:
			self.frame.Popup("No available route")
			return

		# osblknm = osblk.GetName()
		if osblk.AreHandSwitchesSet():
			self.frame.Popup("Block is locked")
			return

		# this is a valid signal for the current route	
		if not currentMovement:  # we are trying to change the signal to allow movement
			aspect = self.CalculateAspect(sig, osblk, rt)

		else:  # we are trying to change the signal to stop the train
			esig = osblk.GetEntrySignal()
			if esig is not None and esig.GetName() != signm:
				self.frame.Popup("Incorrect signal for current route")
				return
			aspect = 0

		self.frame.Request({"signal": {"name": signm, "aspect": aspect}})

	def CalculateAspect(self, sig, osblk, rt):
		print("trying to move train")
		if osblk.IsBusy():
			self.frame.Popup("Block is busy")
			return None

		sigE = sig.GetEast()
		print("OS Reverse check: %s %s" % (sigE, osblk.GetEast()))
		if sigE != osblk.GetEast():
			print("reversing OS")
			# the block will need to be reversed, but it's premature
			# to do so now - so force return values as if reversed
			doReverseExit = True
		else:
			doReverseExit = False

		exitBlkNm = rt.GetExitBlock(reverse=doReverseExit)
		print("exit block = %s" % exitBlkNm)
		rType = rt.GetRouteType(reverse=doReverseExit)
		print("Route type: %d" % rType)

		exitBlk = self.frame.blocks[exitBlkNm]
		if exitBlk.IsOccupied():
			self.frame.Popup("Block is busy")
			return None

		if exitBlk.IsCleared() and sigE != exitBlk.GetEast():
			self.frame.Popup("Block is cleared in opposite direction")
			return None

		if exitBlk.AreHandSwitchesSet():
			self.frame.Popup("Block is locked")
			return None

		nb = exitBlk.NextBlock(reverse=doReverseExit)
		if nb:
			print("next block: %s" % nb.GetName())
			nbStatus = nb.GetStatus()
			nbRType = nb.GetRouteType()
			# try to go one more block, skipping past an OS block

			print("%s %s" % (sigE, nb.GetEast()))
			if sigE != nb.GetEast():
				# the block will need to be reversed, but it's premature
				# to do so now - so force return values as if reversed
				print("reversing")
				doReverseNext = True
			else:
				doReverseNext = False

			nxbNm = nb.GetExitBlock(reverse=doReverseNext)
			if nxbNm is None:
				nnb = None
			else:
				nxb = self.frame.blocks[nxbNm]
				if nxb:
					nnb = nxb.NextBlock(reverse=doReverseNext)
				else:
					nnb = None

			if nnb:
				nnbClear = nnb.GetStatus() == CLEARED
			else:
				nnbClear = False
		else:
			nbStatus = None
			nbRType = None
			nnbClear = False

		print("calling get aspect %d %d %s %s %s" % (
			sig.GetAspectType(), rType, str(nbStatus), str(nbRType), str(nnbClear)))
		aspect = self.GetAspect(sig.GetAspectType(), rType, nbStatus, nbRType, nnbClear)

		self.CheckBlockSignals(sig, aspect, exitBlk, doReverseExit, rType, nbStatus, nbRType, nnbClear)

		return aspect

	def anyTurnoutLocked(self, toList):
		rv = False
		for toname, stat in toList:
			turnout = self.turnouts[toname]
			tostat = "N" if turnout.IsNormal() else "R"
			print("check turnout %s %s %s" % (toname, tostat, stat))
			if turnout.IsLocked() and tostat != stat:
				print("it;s OK")
				rv = True

		return rv

	def CheckBlockSignals(self, sig, aspect, blk, rev, rType, nbStatus, nbRType, nnbClear):
		pass

	def GetAspect(self, atype, rtype, nbstatus, nbrtype, nnbclear):
		if atype == RegAspects:
			if rtype == MAIN and nbstatus == CLEARED and nbrtype == MAIN:
				return 0b011  # Clear

			elif rtype == MAIN and nbstatus == CLEARED and nbrtype == DIVERGING:
				return 0b010  # Approach Medium

			elif rtype == DIVERGING and nbstatus == CLEARED and nbrtype == MAIN:
				return 0b111  # Medium Clear

			elif rtype in [MAIN, DIVERGING] and nbstatus == CLEARED and nbrtype == SLOW:
				return 0b110  # Approach Slow

			elif rtype == MAIN and (nbstatus != CLEARED or nbrtype == RESTRICTING):
				return 0b001  # Approach

			elif rtype == DIVERGING and (nbstatus != CLEARED or nbrtype != MAIN):
				return 0b101  # Medium Approach

			elif rtype in [RESTRICTING, SLOW]:
				return 0b100  # Restricting

			else:
				return 0  # Stop

		elif atype == RegSloAspects:
			if rtype == MAIN and nbstatus == CLEARED:
				return 0b011  # Clear

			elif rtype == SLOW and nbstatus == CLEARED:
				return 0b111  # Slow clear

			elif rtype == MAIN:
				return 0b001  # Approach

			elif rtype == SLOW:
				return 0b101  # Slow Approach

			elif rtype == RESTRICTING:
				return 0b100  # Restricting

			else:
				return 0  # Stop

		elif atype == AdvAspects:
			if rtype == MAIN and nbstatus == CLEARED and nbrtype == MAIN and nnbclear:
				return 0b011  # Clear

			elif rtype == MAIN and nbstatus == CLEARED and nbrtype == DIVERGING:
				return 0b010  # Approach Medium

			elif rtype == DIVERGING and nbstatus == CLEARED and nbrtype == MAIN:
				return 0b111  # Clear

			elif rtype == MAIN and nbstatus == CLEARED and nbrtype == MAIN and not nnbclear:
				return 0b110  # Advance Approach

			elif rtype == MAIN and (nbstatus != CLEARED or nbrtype == RESTRICTING):
				return 0b001  # Approach

			elif rtype == DIVERGING and (nbstatus != CLEARED or nbrtype != MAIN):
				return 0b101  # Medium Approach

			elif rtype == RESTRICTING:
				return 0b100  # Restricting

			else:
				return 0  # Stop

		elif atype == SloAspects:
			if nbstatus == CLEARED and rtype in [SLOW, DIVERGING]:
				return 0b01  # Slow Clear

			elif nbstatus != CLEARED and rtype == SLOW:
				return 0b11  # Slow Approach

			elif rtype == RESTRICTING:
				return 0b10  # Restricting

			else:
				return 0  # Stop

		else:
			return 0

	def GetBlockAspect(self, atype, rtype, nbstatus, nbrtype, nnbclear):
		if atype == RegAspects:
			if nbstatus == CLEARED and nbrtype == MAIN:
				return 0b011  # clear
			elif nbstatus == CLEARED and nbrtype == DIVERGING:
				return 0b010  # approach medium
			elif nbstatus == CLEARED and nbrtype == SLOW:
				return 0b110  # appproach slow
			elif nbstatus != CLEARED:
				return 0b001  # approach
			else:
				return 0b000  # stop

		elif atype == AdvAspects:
			if nbstatus == CLEARED and nbrtype == MAIN and nnbclear:
				return 0b011  # clear
			elif nbstatus == CLEARED and nbrtype == MAIN and nnbclear:
				return 0b110  # advance approach
			elif nbstatus == CLEARED and nbrtype == DIVERGING:
				return 0b010  # approach medium
			elif nbstatus != CLEARED:
				return 0b001  # approach
			else:
				return 0b000  # stop

		return 0b000  # stop as default

	def PerformHandSwitchAction(self, hs):
		if not hs.GetValue():
			# currently unlocked - trying to lock

			if hs.IsBlockCleared():
				self.frame.Popup("Block is cleared")
				return

			stat = 1
		else:
			stat = 0

		self.frame.Request({"handswitch": {"name": hs.GetName(), "status": stat}})

	# The Do... routines handle requests that come in from the dispatch server.  The 3 objects of interest for
	# these requests are blocks, signals, and turnouts
	def DoBlockAction(self, blk, blockend, state):
		bname = blk.GetName()
		blk.SetOccupied(occupied=state == OCCUPIED, blockend=blockend, refresh=True)

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
			# no change necessary
			return

		for blknm, siglist in self.osSignals.items():
			if signm in siglist:
				osblock = self.frame.blocks[blknm]
				rname = osblock.GetRouteName()
				if osblock.route is None:
					continue
				# rt = self.routes[rname]
				if sig.IsPossibleRoute(blknm, rname):
					break
		else:
			return

		# all checking was done on the sending side, so this is a valid request - just do it
		if aspect != STOP:
			osblock.SetEast(sig.GetEast())

		exitBlkNm = osblock.GetExitBlock()
		sig.SetAspect(aspect, refresh=True)
		osblock.SetEntrySignal(sig)
		osblock.SetCleared(aspect != STOP, refresh=True)

		if osblock.IsBusy() and aspect == STOP:
			return

		exitBlk = self.frame.GetBlockByName(exitBlkNm)
		# if exitBlk.IsOccupied():
		# 	return

		if self.CrossingEastWestBoundary(osblock, exitBlk):
			nd = not sig.GetEast()
		else:
			nd = sig.GetEast()

		if aspect != STOP:
			exitBlk.SetEast(nd)

		exitBlk.SetCleared(aspect != STOP, refresh=True)

		self.LockTurnoutsForSignal(osblock.GetName(), sig, aspect != STOP)

		if exitBlk.GetBlockType() == OVERSWITCH:
			rt = exitBlk.GetRoute()
			if rt:
				tolist = rt.GetTurnouts()
				self.LockTurnouts(signm, tolist, aspect != STOP)

	def DoSwitchLeverAction(self, signame, state):
		print("in Common DSLA for signal %s state %s" % (signame, state))
		sigPrefix = signame.split(".")[0]
		print("signal prefix = (%s)" % sigPrefix)
		osblknms = self.sigLeverMap[signame]
		signm = None

		for osblknm in osblknms:
			print(osblknm)
			osblk = self.frame.blocks[osblknm]
			route = osblk.GetRoute()
			if route:
				sigs = route.GetSignals()
				if state == "L":
					if sigs[1].startswith(sigPrefix+state):
						signm = sigs[1]
						movement = True   # trying to set to non-stopping aspect
						print("matching L signal %s" % signm)
						break
				elif state == 'R':
					if sigs[0].startswith(sigPrefix+state):
						signm = sigs[0]
						movement = True   # trying to set to non-stopping aspect
						print("matching R signal %s" % signm)
						break
				elif state == "N":
					print("figure out which of %s and %s matches the lever name and is non zero aspect" % (sigs[0], sigs[1]))
					if sigs[0].startswith(sigPrefix+"R"):
						print("%s is a candidate" % sigs[0])
						sig = self.frame.signals[sigs[0]]
						if sig and sig.GetAspect() != 0:
							print("This is the signal")
							signm = sigs[0]
							movement = False
							break
					if sigs[1].startswith(sigPrefix+"L"):
						print("%s is a candidate" % sigs[0])
						sig = self.frame.signals[sigs[1]]
						if sig and sig.GetAspect() != 0:
							print("This is the signal")
							signm = sigs[1]
							movement = False
							break


		if signm is None:
			print("didn't find a matching signal")
			return

		print("found signal (%s)" % signm)
		sig = self.frame.signals[signm]
		if not sig:
			print("could not interprest signal name")
			return

		if movement:
			aspect = self.CalculateAspect(sig, osblk, route)
			if aspect is None:
				print("Unable to find appropriate signal")
				return

			print("aspect is %d" % aspect)
		else:
			aspect = 0
			print("aspect is 0")

		self.frame.Request({"signal": {"name": signm, "aspect": aspect}})


	def LockTurnoutsForSignal(self, osblknm, sig, flag):
		signm = sig.GetName()
		if osblknm in sig.possibleRoutes:
			osblk = self.blocks[osblknm]
			rt = osblk.GetRoute()
			if rt:
				tolist = rt.GetTurnouts()
				self.LockTurnouts(signm, tolist, flag)

	def LockTurnouts(self, locker, tolist, flag):
		for t in tolist:
			to = self.frame.turnouts[t]
			to.SetLock(locker, flag, refresh=True)
			tp = to.GetPaired()
			if tp:
				tp.SetLock(locker, flag, refresh=True)

	def DoHandSwitchAction(self, hs, stat):
		hs.SetValue(stat != 0, refresh=True)

	def DoIndicatorAction(self, ind, value):
		pass

	def CrossingEastWestBoundary(self, blk1, blk2):
		return False

	def DefineBlocks(self, tiles):
		self.blocks = {}
		self.osBlocks = {}
		return {}, {}

	def DefineTurnouts(self, tiles, blocks):
		self.turnouts = {}
		return {}

	def DefineIndicators(self):
		self.indicators = {}
		return {}

	def DefineSignals(self, tiles):
		self.signals = {}
		return {}

	def DefineButtons(self, tiles):
		self.buttons = {}
		return {}

	def DefineHandSwitches(self, tiles):
		self.handswitches = {}
		return {}

	def ReportBlockBusy(self, blknm):
		self.frame.Popup("Block is busy")

	def ReportOSBusy(self):
		self.frame.Popup("Block is busy")

	def ReportTurnoutLocked(self, tonm):
		self.frame.Popup("Turnout is locked")


class Districts:
	def __init__(self):
		self.districts = {}

	def AddDistrict(self, district):
		self.districts[district.name] = district

	def Initialize(self, sstiles, misctiles):
		for t in self.districts.values():
			t.Initialize(sstiles, misctiles)

	def OnConnect(self):
		for t in self.districts.values():
			t.OnConnect()

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
