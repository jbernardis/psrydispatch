from district import District

from block import Block, OverSwitch, Route
from turnout import Turnout, SlipSwitch
from signal import Signal
from button import Button
from handswitch import HandSwitch

from constants import LaKr, RESTRICTING, MAIN, DIVERGING, REVERSE, EMPTY, OCCUPIED, CLEARED, GREEN, RED, STOP

class Shore (District):
	def __init__(self, name, frame, screen):
		District.__init__(self, name, frame, screen)

	def PerformSignalAction(self, sig):
		signm = sig.GetName()
		osblk = self.blocks["SOSHF"]
		if signm not in ["S8L", "S8R"]:
			if signm in ["S12R", "S12LA", "S12LB", "S12LC", "S4R", "S4LA", "S4LB", "S4LC" ]:
				if osblk.IsBusy():
					self.ReportOSBusy()
					return
			District.PerformSignalAction(self, sig)
			return

		aspect = sig.GetAspect()
		signm = sig.GetName()
		color = GREEN if aspect == 0 else RED # the color we are trying to change to
		print("trying to set signal %s to %d" % (signm, aspect))
		if color == GREEN:
			if osblk.IsBusy() or self.blocks["SOSW"].IsBusy() or self.blocks["SOSE"].IsBusy():
				self.ReportOSBusy()
				return
			aspect = RESTRICTING
		else: # color == RED
			esig = osblk.GetEntrySignal()	
			if esig is not None and esig.GetName() != signm:
				self.frame.Popup("Signal %s is not entry signal" % signm)
				return
			aspect = STOP

		self.frame.Request({"signal": { "name": signm, "aspect": aspect }})

	def DoSignalAction(self, sig, aspect):
		signm = sig.GetName()
		if signm not in ["S8L", "S8R"]:
			District.DoSignalAction(self, sig, aspect)
			self.drawCrossing()
			return

		osblk = self.blocks["SOSHF"]
		east = signm == "S8R"
		osblk.SetEast(east)
		osblk.SetRoute(self.routes["SRtF10F11"])
		sig.SetAspect(aspect, refresh=True)
		if aspect == STOP:
			osblk.SetEntrySignal(None)
		else:
			osblk.SetEntrySignal(sig)
		osblk.SetCleared(aspect != STOP, refresh=True)

		if osblk.IsBusy() and aspect == STOP:
			return

		exitBlk = self.frame.GetBlockByName("F11" if east else "F10")
		entryBlk = self.frame.GetBlockByName("F10" if east else "F11")
		if exitBlk.IsOccupied():
			return

		exitBlk.SetEast(east)
		entryBlk.SetEast(east)
		exitBlk.SetCleared(aspect!=STOP, refresh=True)

	def DrawOthers(self, block):
		if block.GetName() in ["SOSHF", "SOSW", "SOSE"]:
			self.drawCrossing()

	def drawCrossing(self):
		osstat = self.blocks["SOSHF"].GetStatus()
		bwstat = self.blocks["SOSW"].GetStatus()
		bestat = self.blocks["SOSE"].GetStatus()

		if osstat == OCCUPIED:
			bmpw = bmpe = "red-cross"
		elif osstat == CLEARED:
			bmpw = bmpe = "green-cross"
		else:
			if bwstat == OCCUPIED:
				bmpw = "red-main"
			elif bwstat == CLEARED:
				bmpw = "green-main"
			else:
				bmpw = "white-main"

			if bestat == OCCUPIED:
				bmpe = "red-main"
			elif bestat == CLEARED:
				bmpe = "green-main"
			else:
				bmpe = "white-main"

		bmp = self.misctiles["crossing"].getBmp("", bmpw)
		self.frame.DrawTile(self.screen, (90, 11), bmp)

		bmp = self.misctiles["crossing"].getBmp("", bmpe)
		self.frame.DrawTile(self.screen, (92, 13), bmp)

	def DetermineRoute(self, blocks):
		pass
		s3 = 'N' if self.turnouts["SSw3"].IsNormal() else 'R'
		s5 = 'N' if self.turnouts["SSw5"].IsNormal() else 'R'
		s7 = 'N' if self.turnouts["SSw7"].IsNormal() else 'R'
		s9 = 'N' if self.turnouts["SSw9"].IsNormal() else 'R'
		s11 = 'N' if self.turnouts["SSw11"].IsNormal() else 'R'
		s13 = 'N' if self.turnouts["SSw13"].IsNormal() else 'R'
		self.turnouts["SSw3"].SetLock("SSw5", s5=='R', refresh=True)
		self.turnouts["SSw3b"].SetLock("SSw5", s5=='R', refresh=True)
		self.turnouts["SSw5"].SetLock("SSw3", s3=='R', refresh=True)
		self.turnouts["SSw5b"].SetLock("SSw3", s3=='R', refresh=True)
		for block in blocks:
			bname = block.GetName()
			if bname == "SOSW":
				if s3+s5+s11 == "NNR":
					block.SetRoute(self.routes["SRtS10S11"])
				elif s3+s5+s11+s13 == "NNNR":
					block.SetRoute(self.routes["SRtS10H30"])
				elif s3+s5+s11+s13 == "NNNN":
					block.SetRoute(self.routes["SRtS10H10"])
				elif s3+s5+s7+s9 == "RNNN":
					block.SetRoute(self.routes["SRtS10H20"])
				elif s3+s5+s7+s9 == "RNNR":
					block.SetRoute(self.routes["SRtS10S21"])
				elif s3+s5+s7 == "RNR":
					block.SetRoute(self.routes["SRtS10P32"])
				else:
					block.SetRoute(None)

			elif bname == "SOSE":
				if s3+s5+s11 == "NRR":
					block.SetRoute(self.routes["SRtS20S11"])
				elif s3+s5+s11+s13 == "NRNR":
					block.SetRoute(self.routes["SRtS20H30"])
				elif s3+s5+s11+s13 == "NRNN":
					block.SetRoute(self.routes["SRtS20H10"])
				elif s3+s5+s7+s9 == "NNNN":
					block.SetRoute(self.routes["SRtS20H20"])
				elif s3+s5+s7+s9 == "NNNR":
					block.SetRoute(self.routes["SRtS20S21"])
				elif s3+s5+s7 == "NNR":
					block.SetRoute(self.routes["SRtS20P32"])
				else:
					block.SetRoute(None)

			elif bname == "SOSHF":
				s8r = self.signals["S8R"].GetAspect()
				s8l = self.signals["S8L"].GetAspect()
				print("signal 8: %d %d" % (s8r, s8l))
				block.SetRoute(self.routes["SRtF10F11"])
				# if s8r != 0 or s8l != 0:
				# 	block.SetRoute(self.routes["SRtF10F11"])
				# else:
				# 	block.SetRoute(None)


	def DefineBlocks(self, tiles):
		self.blocks = {}
		self.osBlocks = {}

		self.blocks["S10"] = Block(self, self.frame, "S10",
			[
				(tiles["horiz"],    self.screen, (74, 11), False),
				(tiles["horiznc"],  self.screen, (75, 11), False),
				(tiles["horiz"],    self.screen, (76, 11), False),
				(tiles["horiz"],    self.screen, (78, 11), False),
				(tiles["horiznc"],  self.screen, (79, 11), False),
			], False)
		self.blocks["S10"].AddStoppingBlock([
				(tiles["eobleft"],  self.screen, (71, 11), False),
				(tiles["horiz"],    self.screen, (72, 11), False),
				(tiles["horiznc"],  self.screen, (73, 11), False),
			], False)
		self.blocks["S10"].AddStoppingBlock([
				(tiles["horiz"],    self.screen, (80, 11), False),
				(tiles["horiznc"],  self.screen, (81, 11), False),
				(tiles["eobright"], self.screen, (82, 11), False),
			], True)
		self.blocks["S10"].AddTrainLoc(self.screen, (73, 11))

		self.blocks["S11"] = Block(self, self.frame, "S11",
			[
				(tiles["horiz"],    self.screen, (109, 7), False),
				(tiles["horiznc"],  self.screen, (110, 7), False),
				(tiles["horiz"],    self.screen, (111, 7), False),
				(tiles["horiznc"],  self.screen, (112, 7), False),
				(tiles["horiz"],    self.screen, (113, 7), False),
				(tiles["horiznc"],  self.screen, (114, 7), False),
				(tiles["horiz"],    self.screen, (115, 7), False),
				(tiles["horiznc"],  self.screen, (116, 7), False),
				(tiles["horiz"],    self.screen, (117, 7), False),
				(tiles["horiznc"],  self.screen, (118, 7), False),
			], False)
		self.blocks["S11"].AddStoppingBlock([
				(tiles["eobleft"],  self.screen, (106, 7), False),
				(tiles["horiz"],    self.screen, (107, 7), False),
				(tiles["horiznc"],  self.screen, (108, 7), False),
			], False)
		self.blocks["S11"].AddStoppingBlock([
				(tiles["horiz"],    self.screen, (119, 7), False),
				(tiles["horiznc"],  self.screen, (120, 7), False),
				(tiles["eobright"], self.screen, (121, 7), False),
			], True)
		self.blocks["S11"].AddTrainLoc(self.screen, (112, 7))

		self.blocks["S20"] = Block(self, self.frame, "S20",
			[
				(tiles["horiz"],    self.screen, (74, 13), False),
				(tiles["horiznc"],  self.screen, (75, 13), False),
				(tiles["horiz"],    self.screen, (76, 13), False),
				(tiles["horiznc"],  self.screen, (77, 13), False),
				(tiles["horiz"],    self.screen, (78, 13), False),
				(tiles["horiznc"],  self.screen, (79, 13), False),
			], True)
		self.blocks["S20"].AddStoppingBlock([
				(tiles["eobleft"],  self.screen, (71, 13), False),
				(tiles["horiz"],    self.screen, (72, 13), False),
				(tiles["horiznc"],  self.screen, (73, 13), False),
			], False)
		self.blocks["S20"].AddStoppingBlock([
				(tiles["horiz"],    self.screen, (80, 13), False),
				(tiles["horiznc"],  self.screen, (81, 13), False),
				(tiles["eobright"], self.screen, (82, 13), False),
			], True)
		self.blocks["S20"].AddTrainLoc(self.screen, (73, 13))

		self.blocks["S21"] = Block(self, self.frame, "S21",
			[
				(tiles["eobleft"],  self.screen, (110, 19), False),
				(tiles["horiz"],    self.screen, (111, 19), False),
				(tiles["horiznc"],  self.screen, (112, 19), False),
				(tiles["horiz"],    self.screen, (113, 19), False),
				(tiles["horiznc"],  self.screen, (114, 19), False),
				(tiles["horiz"],    self.screen, (115, 19), False),
				(tiles["horiznc"],  self.screen, (116, 19), False),
				(tiles["horiz"],    self.screen, (117, 19), False),
				(tiles["horiznc"],  self.screen, (118, 19), False),
				(tiles["horiz"],    self.screen, (119, 19), False),
				(tiles["horiznc"],  self.screen, (120, 19), False),
				(tiles["eobright"], self.screen, (121, 19), False),
			], True)
		self.blocks["S21"].AddTrainLoc(self.screen, (112, 19))

		self.blocks["SOSW"] = OverSwitch(self, self.frame, "SOSW", 
			[
				(tiles["eobleft"],   self.screen, (83, 11), False),
				(tiles["horiznc"],   self.screen, (85, 11), False),
				(tiles["horiz"],     self.screen, (86, 11), False),
				(tiles["horiznc"],   self.screen, (87, 11), False),
				(tiles["horiz"],     self.screen, (88, 11), False),
				(tiles["horiznc"],   self.screen, (91, 11), False),
				(tiles["horiz"],     self.screen, (92, 11), False),
				(tiles["horiznc"],   self.screen, (93, 11), False),
				(tiles["horiz"],     self.screen, (94, 11), False),
				(tiles["horiznc"],   self.screen, (95, 11), False),
				(tiles["horiz"],     self.screen, (96, 11), False),
				(tiles["horiznc"],   self.screen, (97, 11), False),
				(tiles["horiz"],     self.screen, (98, 11), False),
				(tiles["horiz"],     self.screen, (100, 11), False),
				(tiles["horiznc"],   self.screen, (101, 11), False),
				(tiles["horiz"],     self.screen, (102, 11), False),
				(tiles["horiznc"],   self.screen, (103, 11), False),
				(tiles["horiz"],     self.screen, (104, 11), False),
				(tiles["eobright"],  self.screen, (105, 11), False),
				(tiles["diagleft"],  self.screen, (100, 10), False),
				(tiles["diagleft"],  self.screen, (101, 9), False),
				(tiles["diagleft"],  self.screen, (102, 8), False),
				(tiles["turnleftleft"], self.screen, (103, 7), False),
				(tiles["horiz"],     self.screen, (104, 7), False),
				(tiles["eobright"],  self.screen, (105, 7), False),
				(tiles["diagleft"],  self.screen, (103, 10), False),
				(tiles["turnleftleft"], self.screen, (104, 9), False),
				(tiles["eobright"],  self.screen, (105, 9), False),
				(tiles["diagright"], self.screen, (85, 12), False),
				(tiles["horiz"],     self.screen, (88, 13), False),
				(tiles["horiznc"],   self.screen, (89, 13), False),
				(tiles["horiz"],     self.screen, (90, 13), False),
				(tiles["horiznc"],   self.screen, (91, 13), False),
				(tiles["horiznc"],   self.screen, (93, 13), False),
				(tiles["horiz"],     self.screen, (94, 13), False),
				(tiles["horiznc"],   self.screen, (95, 13), False),
				(tiles["horiz"],     self.screen, (96, 13), False),
				(tiles["horiznc"],   self.screen, (97, 13), False),
				(tiles["horiz"],     self.screen, (98, 13), False),
				(tiles["horiz"],     self.screen, (100, 13), False),
				(tiles["horiznc"],   self.screen, (101, 13), False),
				(tiles["horiznc"],   self.screen, (103, 13), False),
				(tiles["horiz"],     self.screen, (104, 13), False),
				(tiles["eobright"],  self.screen, (105, 13), False),
				(tiles["diagright"], self.screen, (100, 14), False),
				(tiles["diagright"], self.screen, (101, 15), False),
				(tiles["diagright"], self.screen, (102, 16), False),
				(tiles["diagright"], self.screen, (103, 17), False),
				(tiles["diagright"], self.screen, (104, 18), False),
				(tiles["diagright"], self.screen, (105, 19), False),
				(tiles["diagright"], self.screen, (106, 20), False),
				(tiles["turnrightleft"], self.screen, (107, 21), False),
				(tiles["horiz"],     self.screen, (108, 21), False),
				(tiles["eobright"],  self.screen, (109, 21), False),
				(tiles["diagright"], self.screen, (103, 14), False),
				(tiles["diagright"], self.screen, (104, 15), False),
				(tiles["diagright"], self.screen, (105, 16), False),
				(tiles["diagright"], self.screen, (106, 17), False),
				(tiles["diagright"], self.screen, (107, 18), False),
				(tiles["turnrightleft"], self.screen, (108, 19), False),
				(tiles["eobright"],  self.screen, (109, 19), False),
			],
			False)

		self.blocks["SOSE"] = OverSwitch(self, self.frame, "SOSE", 
			[
				(tiles["eobleft"],   self.screen, (83, 13), False),
				(tiles["horiz"],     self.screen, (84, 13), False),
				(tiles["horiznc"],   self.screen, (85, 13), False),
				(tiles["diagleft"],  self.screen, (88, 12), False),
				(tiles["horiznc"],   self.screen, (85, 11), False),
				(tiles["horiz"],     self.screen, (86, 11), False),
				(tiles["horiznc"],   self.screen, (87, 11), False),
				(tiles["horiz"],     self.screen, (88, 11), False),
				(tiles["horiznc"],   self.screen, (91, 11), False),
				(tiles["horiz"],     self.screen, (92, 11), False),
				(tiles["horiznc"],   self.screen, (93, 11), False),
				(tiles["horiz"],     self.screen, (94, 11), False),
				(tiles["horiznc"],   self.screen, (95, 11), False),
				(tiles["horiz"],     self.screen, (96, 11), False),
				(tiles["horiznc"],   self.screen, (97, 11), False),
				(tiles["horiz"],     self.screen, (98, 11), False),
				(tiles["horiz"],     self.screen, (100, 11), False),
				(tiles["horiznc"],   self.screen, (101, 11), False),
				(tiles["horiz"],     self.screen, (102, 11), False),
				(tiles["horiznc"],   self.screen, (103, 11), False),
				(tiles["horiz"],     self.screen, (104, 11), False),
				(tiles["eobright"],  self.screen, (105, 11), False),
				(tiles["diagleft"],  self.screen, (100, 10), False),
				(tiles["diagleft"],  self.screen, (101, 9), False),
				(tiles["diagleft"],  self.screen, (102, 8), False),
				(tiles["turnleftleft"], self.screen, (103, 7), False),
				(tiles["horiz"],     self.screen, (104, 7), False),
				(tiles["eobright"],  self.screen, (105, 7), False),
				(tiles["diagleft"],  self.screen, (103, 10), False),
				(tiles["turnleftleft"], self.screen, (104, 9), False),
				(tiles["eobright"],  self.screen, (105, 9), False),
				(tiles["horiz"],     self.screen, (88, 13), False),
				(tiles["horiznc"],   self.screen, (89, 13), False),
				(tiles["horiz"],     self.screen, (90, 13), False),
				(tiles["horiznc"],   self.screen, (91, 13), False),
				(tiles["horiznc"],   self.screen, (93, 13), False),
				(tiles["horiz"],     self.screen, (94, 13), False),
				(tiles["horiznc"],   self.screen, (95, 13), False),
				(tiles["horiz"],     self.screen, (96, 13), False),
				(tiles["horiznc"],   self.screen, (97, 13), False),
				(tiles["horiz"],     self.screen, (98, 13), False),
				(tiles["horiz"],     self.screen, (100, 13), False),
				(tiles["horiznc"],   self.screen, (101, 13), False),
				(tiles["horiznc"],   self.screen, (103, 13), False),
				(tiles["horiz"],     self.screen, (104, 13), False),
				(tiles["eobright"],  self.screen, (105, 13), False),
				(tiles["diagright"], self.screen, (100, 14), False),
				(tiles["diagright"], self.screen, (101, 15), False),
				(tiles["diagright"], self.screen, (102, 16), False),
				(tiles["diagright"], self.screen, (103, 17), False),
				(tiles["diagright"], self.screen, (104, 18), False),
				(tiles["diagright"], self.screen, (105, 19), False),
				(tiles["diagright"], self.screen, (106, 20), False),
				(tiles["turnrightleft"], self.screen, (107, 21), False),
				(tiles["horiz"],     self.screen, (108, 21), False),
				(tiles["eobright"],  self.screen, (109, 21), False),
				(tiles["diagright"], self.screen, (103, 14), False),
				(tiles["diagright"], self.screen, (104, 15), False),
				(tiles["diagright"], self.screen, (105, 16), False),
				(tiles["diagright"], self.screen, (106, 17), False),
				(tiles["diagright"], self.screen, (107, 18), False),
				(tiles["turnrightleft"], self.screen, (108, 19), False),
				(tiles["eobright"],  self.screen, (109, 19), False),
			],
			True)

		self.blocks["F10"] = Block(self, self.frame, "F10",
			[
				(tiles["horiz"],    self.screen, (83, 9), False),
				(tiles["horiznc"],  self.screen, (84, 9), False),
			], True)
		self.blocks["F10"].AddStoppingBlock([
				(tiles["horiz"],    self.screen, (85, 9), False),
				(tiles["eobright"], self.screen, (86, 9), False),
			], True)
		self.blocks["F10"].AddTrainLoc(self.screen, (83, 9))

		self.blocks["F11"] = Block(self, self.frame, "F11",
			[
				(tiles["eobleft"], self.screen, (96, 15), False),
				(tiles["horiz"],    self.screen, (97, 15), False),
				(tiles["horiznc"],  self.screen, (98, 15), False),
				(tiles["horiz"],    self.screen, (99, 15), False),
			], True)
		self.blocks["F11"].AddStoppingBlock([
				(tiles["eobleft"], self.screen, (96, 15), False),
				(tiles["horiz"],    self.screen, (97, 15), False),
		], False)
		self.blocks["F11"].AddTrainLoc(self.screen, (99, 15))

		self.blocks["SOSHF"] = OverSwitch(self, self.frame, "SOSHF", 
			[
				(tiles["eobleft"],       self.screen, (87, 9), False),
				(tiles["turnrightright"],self.screen, (88, 9), False),
				(tiles["diagright"],     self.screen, (89, 10), False),
				(tiles["diagright"],     self.screen, (91, 12), False),
				(tiles["diagright"],     self.screen, (93, 14), False),
				(tiles["turnrightleft"], self.screen, (94, 15), False),
				(tiles["eobright"],      self.screen, (95, 15), False),
			],
			True)

		self.blocks["SOSHJW"] = OverSwitch(self, self.frame, "SOSHJW",
			[
				(tiles["eobleft"],   self.screen, (114, 11), False),
				(tiles["horiznc"],   self.screen, (115, 11), False),
				(tiles["horiz"],     self.screen, (116, 11), False),
				(tiles["horiznc"],   self.screen, (117, 11), False),
				(tiles["horiz"],     self.screen, (118, 11), False),
				(tiles["horiznc"],   self.screen, (119, 11), False),
				(tiles["horiz"],     self.screen, (120, 11), False),
				(tiles["eobright"],  self.screen, (122, 11), False),
			], False)

		self.blocks["SOSHJM"] = OverSwitch(self, self.frame, "SOSHJM",
			[
				(tiles["eobright"],  self.screen, (122, 11), False),
				(tiles["diagleft"],  self.screen, (120, 13), False),
				(tiles["eobleft"],   self.screen, (114, 11), False),
				(tiles["horiznc"],   self.screen, (115, 11), False),
				(tiles["horiz"],     self.screen, (116, 11), False),
				(tiles["horiz"],     self.screen, (120, 13), False),
				(tiles["horiznc"],   self.screen, (121, 13), False),
				(tiles["eobright"],  self.screen, (122, 13), False),
				(tiles["diagright"], self.screen, (119, 14), False),
				(tiles["turnrightleft"], self.screen, (120, 15), False),
				(tiles["horiznc"],   self.screen, (121, 15), False),
				(tiles["eobright"],  self.screen, (122, 15), False),
			], True)

		self.blocks["SOSHJE"] = OverSwitch(self, self.frame, "SOSHJE",
			[
				(tiles["eobright"],  self.screen, (122, 11), False),
				(tiles["diagleft"],  self.screen, (120, 12), False),
				(tiles["horiz"],     self.screen, (120, 13), False),
				(tiles["horiznc"],   self.screen, (121, 13), False),
				(tiles["eobright"],  self.screen, (122, 13), False),
				(tiles["diagright"], self.screen, (119, 14), False),
				(tiles["turnrightleft"], self.screen, (120, 15), False),
				(tiles["horiznc"],   self.screen, (121, 15), False),
				(tiles["eobright"],  self.screen, (122, 15), False),
				(tiles["diagleft"],  self.screen, (116, 14), False),
				(tiles["eobleft"],   self.screen, (114, 15), False),
				(tiles["horiz"],     self.screen, (116, 15), False),
				(tiles["turnrightright"], self.screen, (117, 15), False),
				(tiles["diagright"], self.screen, (118, 16), False),
				(tiles["turnrightleft"], self.screen, (119, 17), False),
				(tiles["eobright"],  self.screen, (120, 17), False),
			], True)

		self.osBlocks["SOSW"] = [ "S10", "S11", "H30", "H10", "H20", "S21", "P32" ]
		self.osBlocks["SOSE"] = [ "S20", "S11", "H30", "H10", "H20", "S21", "P32" ]
		self.osBlocks["SOSHF"] = [ "F10", "F11" ]
		self.osBlocks["SOSHJW"] = [ "H10", "H11" ]
		self.osBlocks["SOSHJM"] = [ "H11", "H20", "H21", "H40" ]
		self.osBlocks["SOSHJE"] = [ "H11", "H21", "H40", "P42", "P43" ]

		return self.blocks, self.osBlocks

	def DefineTurnouts(self, tiles, blocks):
		self.turnouts = {}

		toList = [
			[ "SSw1",  "torightleft",  ["S10"], (77, 11) ],
			[ "SSw3",  "torightright", ["SOSW", "SOSE"], (84, 11) ],
			[ "SSw3b",  "torightleft", ["SOSW", "SOSE"], (86, 13) ],
			[ "SSw5",   "toleftleft",  ["SOSW", "SOSE"], (89, 11) ],
			[ "SSw5b",  "toleftright", ["SOSW", "SOSE"], (87, 13) ],
			[ "SSw7",   "torightright",["SOSW", "SOSE"], (99, 13) ],
			[ "SSw9",   "torightright",["SOSW", "SOSE"], (102, 13) ],
			[ "SSw11",  "toleftright", ["SOSW", "SOSE"], (99, 11) ],
			[ "SSw13",  "toleftright", ["SOSW", "SOSE"], (102, 11) ],

			[ "SSw15",  "toleftleft",  ["SOSHJM", "SOSHJE"], (117, 13) ],
			[ "SSw15b", "toleftright", ["SOSHJM", "SOSHJE"], (115, 15) ],
			[ "SSw17",  "torightright",["SOSHJM", "SOSHJE"], (118, 13) ],
			[ "SSw19",  "toleftright", ["SOSHJW", "SOSHJM", "SOSHJE"], (119, 13) ],
			[ "SSw19b", "toleftleft",  ["SOSHJW", "SOSHJM", "SOSHJE"], (121, 11) ],
		]

		for tonm, tileSet, blks, pos in toList:
			trnout = Turnout(self, self.frame, tonm, self.screen, tiles[tileSet], pos)
			for blknm in blks:
				blocks[blknm].AddTurnout(trnout)
				trnout.AddBlock(blknm)
			self.turnouts[tonm] = trnout

		self.turnouts["SSw3"].SetPairedTurnout(self.turnouts["SSw3b"])
		self.turnouts["SSw5"].SetPairedTurnout(self.turnouts["SSw5b"])
		self.turnouts["SSw15"].SetPairedTurnout(self.turnouts["SSw15b"])
		self.turnouts["SSw19"].SetPairedTurnout(self.turnouts["SSw19b"])

		self.turnouts["SSw1"].SetDisabled(True)

		return self.turnouts

	def DefineSignals(self, tiles):
		self.signals = {}

		sigList = [
			[ "S12R", True,    "right", (83, 12) ],
			[ "S4R",  True,    "right", (83, 14) ],

			[ "S12LA",False,   "left",  (105, 6) ],
			[ "S12LB",False,   "left",  (105, 8) ],
			[ "S12LC",False,   "left",  (105, 10) ],

			[ "S4LA", False,    "left", (105, 12) ],
			[ "S4LB", False,    "left", (109, 18) ],
			[ "S4LC", False,    "left", (109, 20) ],

			[ "S8R",  True,    "right",  (87, 10) ],
			[ "S8L",  False,   "left",  (95, 14) ]
		]
		for signm, east, tileSet, pos in sigList:
			self.signals[signm]  = Signal(self, self.screen, self.frame, signm, east, pos, tiles[tileSet])  

		blockSigs = {
			"S10": ("D12L", "S12R"),
			"S20": ("D10L", "S4R"),
			"S11": ("S12LA", "S11E"),
			"F10": (None, "S8R"),
			"F11": ("S8L", None),
			"S21": ("S4LB", "S21E"),
		}

		for blknm, siglist in blockSigs.items():
			self.blocks[blknm].SetSignals(siglist)

		self.routes = {}
		self.osSignals = {}

		block = self.blocks["SOSW"]
		self.routes["SRtS10S11"] = Route(self.screen, block, "SRtS10S11", "S11", [ (83, 11), (84, 11), (85, 11), (86, 11), (87, 11), (88, 11), (89, 11),
																				(90, 11), (91, 11), (92, 11), (93, 11), (94, 11), (95, 11), (96, 11), (97, 11), (98, 11), (99, 11),
																				(100, 10), (101, 9), (102, 8), (103, 7), (104, 7), (105, 7)  ], "S10", [MAIN, MAIN], ["SSw3", "SSw5", "SSw11"])
		self.routes["SRtS10H30"] = Route(self.screen, block, "SRtS10H30", "H30", [ (83, 11), (84, 11), (85, 11), (86, 11), (87, 11), (88, 11), (89, 11),
																				(90, 11), (91, 11), (92, 11), (93, 11), (94, 11), (95, 11), (96, 11), (97, 11), (98, 11), (99, 11),
																				(100, 11), (101, 11), (102, 11), (103, 10), (104, 9), (105, 9)  ], "S10", [RESTRICTING, RESTRICTING], ["SSw3", "SSw5", "SSw11", "SSw13"])
		self.routes["SRtS10H10"] = Route(self.screen, block, "SRtS10H10", "H10", [ (83, 11), (84, 11), (85, 11), (86, 11), (87, 11), (88, 11), (89, 11),
																				(90, 11), (91, 11), (92, 11), (93, 11), (94, 11), (95, 11), (96, 11), (97, 11), (98, 11), (99, 11),
																				(100, 11), (101, 11), (102, 11), (103, 11), (104, 11), (105, 11)  ], "S10", [RESTRICTING, DIVERGING], ["SSw3", "SSw5", "SSw11", "SSw13"])
		self.routes["SRtS10H20"] = Route(self.screen, block, "SRtS10H20", "H20", [ (83, 11), (84, 11), (85, 12), (86, 13), (87, 13), (88, 13), (89, 13),
																				(90, 13), (91, 13), (92, 13), (93, 13), (94, 13), (95, 13), (96, 13), (97, 13), (98, 13), (99, 13),
																				(100, 13), (101, 13), (102, 13), (103, 13), (104, 13), (105, 13)  ], "S10", [DIVERGING, RESTRICTING], ["SSw3", "SSw5", "SSw7", "SSw9"])
		self.routes["SRtS10S21"] = Route(self.screen, block, "SRtS10S21", "S21", [ (83, 11), (84, 11), (85, 12), (86, 13), (87, 13), (88, 13), (89, 13),
																				(90, 13), (91, 13), (92, 13), (93, 13), (94, 13), (95, 13), (96, 13), (97, 13), (98, 13), (99, 13),
																				(100, 13), (101, 13), (102, 13), (103, 14), (104, 15), (105, 16), (106, 17), (107, 18), (108, 19), (109, 19)  ], "S10", [DIVERGING, RESTRICTING], ["SSw3", "SSw5", "SSw7", "SSw9"])
		self.routes["SRtS10P32"] = Route(self.screen, block, "SRtS10P32", "P32", [ (83, 11), (84, 11), (85, 12), (86, 13), (87, 13), (88, 13), (89, 13),
																				(90, 13), (91, 13), (92, 13), (93, 13), (94, 13), (95, 13), (96, 13), (97, 13), (98, 13), (99, 13),
																				(100, 14), (101, 15), (102, 16), (103, 17), (104, 18), (105, 19), (106, 20), (107, 21), (108, 21), (109, 21)  ], "S10", [DIVERGING, DIVERGING], ["SSw3", "SSw5", "SSw7"])
		
		block = self.blocks["SOSE"]
		self.routes["SRtS20S21"] = Route(self.screen, block, "SRtS20S21", "S20", [ (83, 13), (84, 13), (85, 13), (86, 13), (87, 13), (88, 13), (89, 13),
																				(90, 13), (91, 13), (92, 13), (93, 13), (94, 13), (95, 13), (96, 13), (97, 13), (98, 13), (99, 13),
																				(100, 13), (101, 13), (102, 13), (103, 14), (104, 15), (105, 16), (106, 17), (107, 18), (108, 19), (109, 19)  ], "S21", [MAIN, MAIN], ["SSw3", "SSw5", "SSw7", "SSw9"])
		self.routes["SRtS20S11"] = Route(self.screen, block, "SRtS20S11", "S20", [ (83, 13), (84, 13), (85, 13), (86, 13), (87, 13), (88, 12), (89, 11),
																				(90, 11), (91, 11), (92, 11), (93, 11), (94, 11), (95, 11), (96, 11), (97, 11), (98, 11), (99, 11),
																				(100, 10), (101, 9), (102, 8), (103, 7), (104, 7), (105, 7)  ], "S11", [DIVERGING, DIVERGING], ["SSw3", "SSw5", "SSw11"])
		self.routes["SRtS20H30"] = Route(self.screen, block, "SRtS20H30", "S20", [ (83, 13), (84, 13), (85, 13), (86, 13), (87, 13), (88, 12), (89, 11),
																				(90, 11), (91, 11), (92, 11), (93, 11), (94, 11), (95, 11), (96, 11), (97, 11), (98, 11), (99, 11),
																				(100, 11), (101, 11), (102, 11), (103, 10), (104, 9), (105, 9)  ], "H30", [RESTRICTING, RESTRICTING], ["SSw3", "SSw5", "SSw11", "SSw13"])
		self.routes["SRtS20H10"] = Route(self.screen, block, "SRtS20H10", "S20", [ (83, 13), (84, 13), (85, 13), (86, 13), (87, 13), (88, 12), (89, 11),
																				(90, 11), (91, 11), (92, 11), (93, 11), (94, 11), (95, 11), (96, 11), (97, 11), (98, 11), (99, 11),
																				(100, 11), (101, 11), (102, 11), (103, 11), (104, 11), (105, 11)  ], "H10", [RESTRICTING, DIVERGING], ["SSw3", "SSw5", "SSw11", "SSw13"])
		self.routes["SRtS20H20"] = Route(self.screen, block, "SRtS20H20", "S20", [ (83, 13), (84, 13), (85, 13), (86, 13), (87, 13), (88, 13), (89, 13),
																				(90, 13), (91, 13), (92, 13), (93, 13), (94, 13), (95, 13), (96, 13), (97, 13), (98, 13), (99, 13),
																				(100, 13), (101, 13), (102, 13), (103, 13), (104, 13), (105, 13)  ], "H20", [DIVERGING, RESTRICTING], ["SSw3", "SSw5", "SSw7", "SSw9"])
		self.routes["SRtS20P32"] = Route(self.screen, block, "SRtS20P32", "S20", [ (83, 13), (84, 13), (85, 13), (86, 13), (87, 13), (88, 13), (89, 13),
																				(90, 13), (91, 13), (92, 13), (93, 13), (94, 13), (95, 13), (96, 13), (97, 13), (98, 13), (99, 13),
																				(100, 14), (101, 15), (102, 16), (103, 17), (104, 18), (105, 19), (106, 20), (107, 21), (108, 21), (109, 21)  ], "P32", [DIVERGING, DIVERGING], ["SSw3", "SSw5", "SSw7"])

		block = self.blocks["SOSHF"]
		self.routes["SRtF10F11"] = Route(self.screen, block, "SRtF10F11", "F10", [ (87, 9), (88, 9), (89, 10), (90, 11), (91, 12), (92, 13), (93, 14), (94, 15), (95, 15) ], "F11", [RESTRICTING, RESTRICTING], [])

		self.signals["S12R"].AddPossibleRoutes("SOSW", [ "SRtS10S11", "SRtS10H30", "SRtS10H10", "SRtS10H20", "SRtS10S21", "SRtS10P32"])
		self.signals["S4R"].AddPossibleRoutes("SOSE",  [ "SRtS20S11", "SRtS20H30", "SRtS20H10", "SRtS20H20", "SRtS20S21", "SRtS20P32"])
		self.signals["S12LA"].AddPossibleRoutes("SOSW", [ "SRtS10S11" ]) 
		self.signals["S12LA"].AddPossibleRoutes("SOSE", [ "SRtS20S11" ]) 
		self.signals["S12LB"].AddPossibleRoutes("SOSW", [ "SRtS10H30" ]) 
		self.signals["S12LB"].AddPossibleRoutes("SOSE", [ "SRtS20H30" ]) 
		self.signals["S12LC"].AddPossibleRoutes("SOSW", [ "SRtS10H10" ]) 
		self.signals["S12LC"].AddPossibleRoutes("SOSE", [ "SRtS20H10" ]) 
		self.signals["S4LA"].AddPossibleRoutes("SOSW", [ "SRtS10H20" ]) 
		self.signals["S4LA"].AddPossibleRoutes("SOSE", [ "SRtS20H20" ]) 
		self.signals["S4LB"].AddPossibleRoutes("SOSW", [ "SRtS10S21" ]) 
		self.signals["S4LB"].AddPossibleRoutes("SOSE", [ "SRtS20S21" ]) 
		self.signals["S4LC"].AddPossibleRoutes("SOSW", [ "SRtS10P32" ]) 
		self.signals["S4LC"].AddPossibleRoutes("SOSE", [ "SRtS20P32" ]) 
		self.signals["S8R"].AddPossibleRoutes("SOSHF", [ "SRtF10F11" ]) 
		self.signals["S8L"].AddPossibleRoutes("SOSHF", [ "SRtF10F11" ]) 

		self.osSignals["SOSW"] = [ "S12LA", "S12LB", "S12LC", "S12R", "S4LA", "S4LB", "S4LC", "S4R", "S8L", "S8R" ]
		self.osSignals["SOSE"] = [ "S12LA", "S12LB", "S12LC", "S12R", "S4LA", "S4LB", "S4LC", "S4R", "S8L", "S8R" ]
		self.osSignals["SOSHF"] = [ "S8L", "S8R", "S12R" ]

		return self.signals

	def DefineHandSwitches(self, tiles):
		self.handswitches = {}

		hs = HandSwitch(self, self.screen, self.frame, self.blocks["S10"], "SSw1.hand", (77, 10), tiles["handdown"])
		self.blocks["S10"].AddHandSwitch(hs)
		self.handswitches["SSw1.hand"] = hs

		return self.handswitches

		