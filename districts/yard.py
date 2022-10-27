from district import District

from block import Block, OverSwitch, Route
from turnout import Turnout, SlipSwitch
from signal import Signal
from button import Button
from indicator import Indicator

from constants import HyYdPt, RESTRICTING, MAIN, DIVERGING, SLOW, NORMAL, REVERSE, EMPTY, SLIPSWITCH, RegAspects, AdvAspects, RegSloAspects

CJBlocks = ["YOSCJE", "YOSCJW"]
EEBlocks = ["YOSEJE", "YOSEJW"]

class Yard (District):
	def __init__(self, name, frame, screen):
		District.__init__(self, name, frame, screen)
		self.sw17 = None
		self.sw21 = None

	def Draw(self):
		District.Draw(self)
		self.drawCrossover()

	def DrawOthers(self, block):
		if block.GetName() in ["YOSKL1", "YOSKL2", "YOSKL3"]:
			self.drawCrossover()

	def drawCrossover(self):
		s17 = NORMAL if self.sw17.IsNormal() else REVERSE
		s21 = NORMAL if self.sw21.IsNormal() else REVERSE

		if s17 == REVERSE:
			blkstat = self.sw17.GetBlockStatus()
		elif s21 == REVERSE:
			blkstat = self.sw21.GetBlockStatus()
		else:
			blkstat = EMPTY

		bmp = "diagright" if s17 == REVERSE else "diagleft" if s21 == REVERSE else "cross"
		bmp = self.misctiles["crossover"].getBmp(blkstat, bmp)
		self.frame.DrawTile(self.screen, (104, 12), bmp)

	def DoTurnoutAction(self, turnout, state):
		tn = turnout.GetName()
		if turnout.GetType() == SLIPSWITCH:
			if tn == "YSw19":
				bstat = NORMAL if self.turnouts["YSw17"].IsNormal() else REVERSE
				turnout.SetStatus([state, bstat])
				turnout.Draw()

		else:
			District.DoTurnoutAction(self, turnout, state)

		if tn in [ "YSw17", "YSw19", "YSw21" ]:
			self.drawCrossover()
			if tn == "YSw17":
				trnout = self.turnouts["YSw19"]
				trnout.UpdateStatus()
				trnout.Draw()

	def DetermineRoute(self, blocks):
		s1 = 'N' if self.turnouts["YSw1"].IsNormal() else 'R'
		s3 = 'N' if self.turnouts["YSw3"].IsNormal() else 'R'
		s7 = 'N' if self.turnouts["YSw7"].IsNormal() else 'R'
		s9 = 'N' if self.turnouts["YSw9"].IsNormal() else 'R'
		s11 = 'N' if self.turnouts["YSw11"].IsNormal() else 'R'
		s17 = 'N' if self.turnouts["YSw17"].IsNormal() else 'R'
		s19 = 'N' if self.turnouts["YSw19"].IsNormal() else 'R'
		s21 = 'N' if self.turnouts["YSw21"].IsNormal() else 'R'
		s23 = 'N' if self.turnouts["YSw23"].IsNormal() else 'R'
		s25 = 'N' if self.turnouts["YSw25"].IsNormal() else 'R'
		s27 = 'N' if self.turnouts["YSw27"].IsNormal() else 'R'
		s29 = 'N' if self.turnouts["YSw29"].IsNormal() else 'R'
		s113 = 'N' if self.turnouts["YSw113"].IsNormal() else 'R'
		s115 = 'N' if self.turnouts["YSw115"].IsNormal() else 'R'
		s116 = 'N' if self.turnouts["YSw116"].IsNormal() else 'R'
		s131 = 'N' if self.turnouts["YSw131"].IsNormal() else 'R'
		s132 = 'N' if self.turnouts["YSw132"].IsNormal() else 'R'
		s134 = 'N' if self.turnouts["YSw134"].IsNormal() else 'R'
		self.turnouts["YSw17"].SetLock("YSw21", s21=='R', refresh=True)
		self.turnouts["YSw21"].SetLock("YSw17", s17=='R', refresh=True)
		self.turnouts["YSw21b"].SetLock("YSw17", s17=='R', refresh=True)

		for block in blocks:
			bname = block.GetName()
			if bname == "YOSCJW":
				if s3 == "N":
					block.SetRoute(self.routes["YRtY11L10"])
				else:
					if s1 == 'N':
						block.SetRoute(self.routes["YRtY11L20"])
					else:
						block.SetRoute(self.routes["YRtY11P50"])

			elif bname == "YOSCJE":
				if s3 == "R":
					block.SetRoute(None)
				elif s1 == "N":
					block.SetRoute(self.routes["YRtY21L20"])
				else:
					block.SetRoute(self.routes["YRtY21P50"])

			elif bname == "YOSEJW":
				if s7 == "N" and s9 == "N":
					block.SetRoute(self.routes["YRtY10Y11"])
				elif s7 == 'N' and s9 == 'R' and s11 == 'R':
					block.SetRoute(self.routes["YRtY30Y11"])
				elif s7 == 'N' and s9 == 'R' and s11 == 'N':
					block.SetRoute(self.routes["YRtY87Y11"])
				else:
					block.SetRoute(None)

			elif bname == "YOSEJE":
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

			elif bname == "YOSKL1":
				if s17+s21+s23+s25+s27 == "NNNNN":
					block.SetRoute(self.routes["YRtY20Y51"])
				elif s17+s21+s23+s25 == "NNNR":
					block.SetRoute(self.routes["YRtY20Y50"]) 
				elif s17+s21+s23+s25+s27 == "NNNNR":
					block.SetRoute(self.routes["YRtY20Y70"])
				elif s17+s19+s21+s23+s29 == "NRNRN":
					block.SetRoute(self.routes["YRtY20Y52"])
				elif s17+s19+s21+s23+s29 == "NRNRR":
					block.SetRoute(self.routes["YRtY20Y53"])
				else:
					block.SetRoute(None)

			elif bname == "YOSKL2":
				if s17+s19+s21+s29 == "NNNN":
					block.SetRoute(self.routes["YRtY10Y52"])
				elif s17+s21+s23+s25 == "NRNR":
					block.SetRoute(self.routes["YRtY10Y50"])
				elif s17+s21+s23+s25+s27 == "NRNNN":
					block.SetRoute(self.routes["YRtY10Y51"])
				elif s17+s21+s23+s25+s27 == "NRNNR":
					block.SetRoute(self.routes["YRtY10Y70"])
				elif s17+s19+s21+s29 == "NNNR":
					block.SetRoute(self.routes["YRtY10Y53"])
				else:
					block.SetRoute(None)

			elif bname == "YOSKL3":
				if s17+s19+s21 == "NRN":
					block.SetRoute(self.routes["YRtY10Y60"])
				elif s17+s19+s21 == "RRN":
					block.SetRoute(self.routes["YRtY20Y60"])
				else:
					block.SetRoute(None)

			elif bname == "YOSKL4":
				s33 = 'N' if self.turnouts["YSw33"].IsNormal() else 'R'
				if s33 == "N":
					block.SetRoute(self.routes["YRtY30Y51"])
				else:
					block.SetRoute(self.routes["YRtY30Y50"])

			elif bname == "YOSWYW":
				if s113+s115 == "NN":
					block.SetRoute(self.routes["YRtY70Y81"])
				elif s113+s115+s116 == "NRR":
					block.SetRoute(self.routes["YRtY70Y82"])
				elif s113+s115+s116 == "NRN":
					block.SetRoute(self.routes["YRtY70Y83"])
				elif s113 == "R":
					block.SetRoute(self.routes["YRtY70Y84"])
				else:
					block.SetRoute(None)

			elif bname == "YOSWYE":
				if s134+s132 == "NN":
					block.SetRoute(self.routes["YRtY87Y81"])
				elif s134+s132+s131 == "NRR":
					block.SetRoute(self.routes["YRtY87Y82"])
				elif s134+s132+s131 == "NRN":
					block.SetRoute(self.routes["YRtY87Y83"])
				elif s134 == "R":
					block.SetRoute(self.routes["YRtY87Y84"])
				else:
					block.SetRoute(None)

	def CrossingEastWestBoundary(self, blk1, blk2):
		if blk1.GetName() == "YOSKL4" and blk2.GetName() == "Y30":
			return True
		if blk1.GetName() == "YOSKL1" and blk2.GetName() == "Y70":
			return True
		if blk1.GetName() == "YOSKL2" and blk2.GetName() == "Y70":
			return True

		return False

	def PerformButtonAction(self, btn):
		bname = btn.GetName()
		if bname in self.osButtons["YOSWYW"]:
			osBlk = self.blocks["YOSWYW"]
			if osBlk.IsBusy():
				self.ReportBlockBusy("YOSWYW")
				return

			btn.Press(refresh=True)
			self.frame.ClearButtonAfter(2, btn)
			if bname == "YWWB1":   # Y81
				self.MatrixTurnoutRequest([["YSw113", "N"], ["YSw115", "N"]])
			elif bname == "YWWB2":   # Y82
				self.MatrixTurnoutRequest([["YSw113", "N"], ["YSw115", "R"], ["YSw116", "R"]])
			elif bname == "YWWB3":   # Y83
				self.MatrixTurnoutRequest([["YSw113", "N"], ["YSw115", "R"], ["YSw116", "N"]])
			elif bname == "YWWB4":   # Y84
				self.MatrixTurnoutRequest([["YSw113", "R"]])

		elif bname in self.osButtons["YOSWYE"]:
			osBlk = self.blocks["YOSWYE"]
			if osBlk.IsBusy():
				self.ReportBlockBusy("YOSWYE")
				return

			btn.Press(refresh=True)
			self.frame.ClearButtonAfter(2, btn)
			if bname == "YWEB1":   # Y81
				self.MatrixTurnoutRequest([["YSw134", "N"], ["YSw132", "N"]])
			elif bname == "YWEB2":   # Y82
				self.MatrixTurnoutRequest([["YSw134", "N"], ["YSw132", "R"], ["YSw131", "R"]])
			elif bname == "YWEB3":   # Y83
				self.MatrixTurnoutRequest([["YSw134", "N"], ["YSw132", "R"], ["YSw131", "N"]])
			elif bname == "YWEB4":   # Y84
				self.MatrixTurnoutRequest([["YSw134", "R"]])

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
		self.blocks["Y10"].AddTrainLoc(self.screen, (108, 11))

		self.blocks["Y11"] = Block(self, self.frame, "Y11",
			[
				(tiles["horiz"],    self.screen, (124, 11), False),
				(tiles["horiznc"],  self.screen, (125, 11), False),
				(tiles["horiz"],    self.screen, (126, 11), False),
				(tiles["horiznc"],  self.screen, (127, 11), False),
				(tiles["eobright"], self.screen, (128, 11), False),
			], False)
		self.blocks["Y11"].AddTrainLoc(self.screen, (123, 11))
		self.blocks["Y11"].AddStoppingBlock([
				(tiles["eobleft"],  self.screen, (122, 11), False),
				(tiles["horiznc"],  self.screen, (123, 11), False),
			], False)

		self.blocks["Y20"] = Block(self, self.frame, "Y20",
			[
				(tiles["eobleft"],  self.screen, (107, 13), False),
				(tiles["horiznc"],  self.screen, (108, 13), False),
				(tiles["horiz"],    self.screen, (109, 13), False),
				(tiles["horiznc"],  self.screen, (110, 13), False),
				(tiles["horiz"],    self.screen, (111, 13), False),
			], True)
		self.blocks["Y20"].AddTrainLoc(self.screen, (108, 13))
		self.blocks["Y20"].AddStoppingBlock([
				(tiles["horiznc"],  self.screen, (112, 13), False),
				(tiles["eobright"], self.screen, (113, 13), False),
			], True)

		self.blocks["Y21"] = Block(self, self.frame, "Y21",
			[
				(tiles["horiz"],    self.screen, (124, 13), False),
				(tiles["horiznc"],  self.screen, (125, 13), False),
				(tiles["horiz"],    self.screen, (126, 13), False),
			], True)
		self.blocks["Y21"].AddTrainLoc(self.screen, (123, 13))
		self.blocks["Y21"].AddStoppingBlock([
				(tiles["eobleft"],  self.screen, (122, 13), False),
				(tiles["horiznc"],  self.screen, (123, 13), False),
			], False)
		self.blocks["Y21"].AddStoppingBlock([
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
		self.blocks["Y30"].AddTrainLoc(self.screen, (85, 3))

		self.blocks["Y50"] = Block(self, self.frame, "Y50",
			[
				(tiles["eobleft"],        self.screen, (89, 15), False),
				(tiles["horiz"],          self.screen, (90, 15), False),
				(tiles["horiznc"],        self.screen, (91, 15), False),
				(tiles["horiz"],          self.screen, (92, 15), False),
				(tiles["horiznc"],        self.screen, (93, 15), False),
				(tiles["horiz"],          self.screen, (94, 15), False),
				(tiles["eobright"],       self.screen, (95, 15), False),
			], True)
		self.blocks["Y50"].AddTrainLoc(self.screen, (90, 15))

		self.blocks["Y51"] = Block(self, self.frame, "Y51",
			[
				(tiles["eobleft"],        self.screen, (89, 13), False),
				(tiles["horiz"],          self.screen, (90, 13), False),
				(tiles["horiznc"],        self.screen, (91, 13), False),
				(tiles["horiz"],          self.screen, (92, 13), False),
				(tiles["horiznc"],        self.screen, (93, 13), False),
				(tiles["horiz"],          self.screen, (94, 13), False),
				(tiles["eobright"],       self.screen, (95, 13), False),
			], True)
		self.blocks["Y51"].AddTrainLoc(self.screen, (90, 13))

		self.blocks["Y52"] = Block(self, self.frame, "Y52",
			[
				(tiles["eobleft"],        self.screen, (85, 9), False),
				(tiles["horiz"],          self.screen, (86, 9), False),
				(tiles["horiznc"],        self.screen, (87, 9), False),
				(tiles["horiz"],          self.screen, (88, 9), False),
				(tiles["horiznc"],        self.screen, (89, 9), False),
				(tiles["horiz"],          self.screen, (90, 9), False),
				(tiles["horiznc"],        self.screen, (91, 9), False),
				(tiles["horiz"],          self.screen, (92, 9), False),
				(tiles["horiznc"],        self.screen, (93, 9), False),
				(tiles["eobright"],       self.screen, (94, 9), False),
			], True)
		self.blocks["Y52"].AddTrainLoc(self.screen, (86, 9))

		self.blocks["Y53"] = Block(self, self.frame, "Y53",
			[
				(tiles["eobleft"],        self.screen, (85, 7), False),
				(tiles["horiz"],          self.screen, (86, 7), False),
				(tiles["horiznc"],        self.screen, (87, 7), False),
				(tiles["horiz"],          self.screen, (88, 7), False),
				(tiles["horiznc"],        self.screen, (89, 7), False),
				(tiles["horiz"],          self.screen, (90, 7), False),
				(tiles["horiznc"],        self.screen, (91, 7), False),
				(tiles["horiz"],          self.screen, (92, 7), False),
				(tiles["horiznc"],        self.screen, (93, 7), False),
				(tiles["eobright"],       self.screen, (94, 7), False),
			], True)
		self.blocks["Y53"].AddTrainLoc(self.screen, (86, 7))

		self.blocks["Y60"] = Block(self, self.frame, "Y60",
			[
				(tiles["houtline"],       self.screen, (93, 5), False),
				(tiles["houtline"],       self.screen, (94, 5), False),
			], True)

		self.blocks["Y70"] = Block(self, self.frame, "Y70",
			[
				(tiles["houtline"],       self.screen, (93, 11), False),
				(tiles["houtline"],       self.screen, (94, 11), False),
				(tiles["houtline"],       self.screen, (95, 11), False),
				(tiles["horiznc"],        self.screen, (13, 30), False),
				(tiles["horiz"],          self.screen, (14, 30), False),
				(tiles["horiznc"],        self.screen, (15, 30), False),
				(tiles["horiz"],          self.screen, (16, 30), False),
				(tiles["horiznc"],        self.screen, (17, 30), False),
				(tiles["horiz"],          self.screen, (18, 30), False),
				(tiles["horiznc"],        self.screen, (19, 30), False),
				(tiles["eobright"],       self.screen, (20, 30), False),
			], False)
		self.blocks["Y70"].AddTrainLoc(self.screen, (14, 30))

		self.blocks["Y81"] = Block(self, self.frame, "Y81",
			[
				(tiles["horiznc"],        self.screen, (33, 30), False),
				(tiles["horiz"],          self.screen, (34, 30), False),
				(tiles["horiznc"],        self.screen, (35, 30), False),
				(tiles["horiz"],          self.screen, (36, 30), False),
				(tiles["horiznc"],        self.screen, (37, 30), False),
				(tiles["horiz"],          self.screen, (38, 30), False),
				(tiles["horiznc"],        self.screen, (39, 30), False),
				(tiles["horiz"],          self.screen, (40, 30), False),
				(tiles["horiznc"],        self.screen, (41, 30), False),
				(tiles["horiz"],          self.screen, (42, 30), False),
				(tiles["horiznc"],        self.screen, (43, 30), False),
				(tiles["horiz"],          self.screen, (44, 30), False),
			], False)
		self.blocks["Y81"].AddTrainLoc(self.screen, (34, 30))

		self.blocks["Y82"] = Block(self, self.frame, "Y82",
			[
				(tiles["horiznc"],        self.screen, (33, 32), False),
				(tiles["horiz"],          self.screen, (34, 32), False),
				(tiles["horiznc"],        self.screen, (35, 32), False),
				(tiles["horiz"],          self.screen, (36, 32), False),
				(tiles["horiznc"],        self.screen, (37, 32), False),
				(tiles["horiz"],          self.screen, (38, 32), False),
				(tiles["horiznc"],        self.screen, (39, 32), False),
				(tiles["horiz"],          self.screen, (40, 32), False),
				(tiles["horiznc"],        self.screen, (41, 32), False),
				(tiles["horiz"],          self.screen, (42, 32), False),
				(tiles["horiznc"],        self.screen, (43, 32), False),
				(tiles["horiz"],          self.screen, (44, 32), False),
			], False)
		self.blocks["Y82"].AddTrainLoc(self.screen, (34, 32))

		self.blocks["Y83"] = Block(self, self.frame, "Y83",
			[
				(tiles["horiznc"],        self.screen, (33, 34), False),
				(tiles["horiz"],          self.screen, (34, 34), False),
				(tiles["horiznc"],        self.screen, (35, 34), False),
				(tiles["horiz"],          self.screen, (36, 34), False),
				(tiles["horiznc"],        self.screen, (37, 34), False),
				(tiles["horiz"],          self.screen, (38, 34), False),
				(tiles["horiznc"],        self.screen, (39, 34), False),
				(tiles["horiz"],          self.screen, (40, 34), False),
				(tiles["horiznc"],        self.screen, (41, 34), False),
				(tiles["horiz"],          self.screen, (42, 34), False),
				(tiles["horiznc"],        self.screen, (43, 34), False),
				(tiles["horiz"],          self.screen, (44, 34), False),
			], False)
		self.blocks["Y83"].AddTrainLoc(self.screen, (34, 34))

		self.blocks["Y84"] = Block(self, self.frame, "Y84",
			[
				(tiles["horiznc"],        self.screen, (33, 36), False),
				(tiles["horiz"],          self.screen, (34, 36), False),
				(tiles["horiznc"],        self.screen, (35, 36), False),
				(tiles["horiz"],          self.screen, (36, 36), False),
				(tiles["horiznc"],        self.screen, (37, 36), False),
				(tiles["horiz"],          self.screen, (38, 36), False),
				(tiles["horiznc"],        self.screen, (39, 36), False),
				(tiles["horiz"],          self.screen, (40, 36), False),
				(tiles["horiznc"],        self.screen, (41, 36), False),
				(tiles["horiz"],          self.screen, (42, 36), False),
				(tiles["horiznc"],        self.screen, (43, 36), False),
				(tiles["horiz"],          self.screen, (44, 36), False),
			], False)
		self.blocks["Y84"].AddTrainLoc(self.screen, (34, 36))

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
		self.blocks["Y87"].AddTrainLoc(self.screen, (57, 30))

		self.blocks["YOSEJW"] = OverSwitch(self, self.frame, "YOSEJW", 
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

		self.blocks["YOSEJE"] = OverSwitch(self, self.frame, "YOSEJE", 
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

		self.blocks["YOSCJE"] = OverSwitch(self, self.frame, "YOSCJE", 
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

		self.blocks["YOSCJW"] = OverSwitch(self, self.frame, "YOSCJW", 
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

		self.blocks["YOSKL2"] = OverSwitch(self, self.frame, "YOSKL2", 
			[
				(tiles["horiznc"],       self.screen, (104, 11), False),
				(tiles["eobright"],      self.screen, (106, 11), False),
				(tiles["eobleft"],       self.screen, (95, 7), False),
				(tiles["turnrightright"],self.screen, (96, 7), False),
				(tiles["diagright"],     self.screen, (97, 8), False),
				(tiles["diagright"],     self.screen, (99, 10), False),
				(tiles["horiz"],         self.screen, (101, 11), False),
				(tiles["horiznc"],       self.screen, (102, 11), False),
				(tiles["eobleft"],       self.screen, (95, 9), False),
				(tiles["horiz"],         self.screen, (96, 9), False),
				(tiles["horiznc"],       self.screen, (97, 9), False),
				(tiles["eobleft"],       self.screen, (96, 11), False),
				(tiles["turnrightright"],self.screen, (97, 11), False),
				(tiles["diagright"],     self.screen, (98, 12), False),
				(tiles["horiznc"],       self.screen, (101, 13), False),
				(tiles["eobleft"],       self.screen, (96, 13), False),
				(tiles["horiz"],         self.screen, (97, 13), False),
				(tiles["horiznc"],       self.screen, (98, 13), False),
				(tiles["eobleft"],       self.screen, (96, 15), False),
				(tiles["horiz"],         self.screen, (97, 15), False),
				(tiles["turnleftright"], self.screen, (98, 15), False),
				(tiles["diagleft"],      self.screen, (99, 14), False),
			],
			False)

		self.blocks["YOSKL3"] = OverSwitch(self, self.frame, "YOSKL3", 
			[
				(tiles["eobleft"],       self.screen, (95, 5), False),
				(tiles["horiz"],         self.screen, (96, 5), False),
				(tiles["turnrightright"],self.screen, (97, 5), False),
				(tiles["diagright"],     self.screen, (98, 6), False),
				(tiles["diagright"],     self.screen, (99, 7), False),
				(tiles["diagright"],     self.screen, (100, 8), False),
				(tiles["diagright"],     self.screen, (101, 9), False),
				(tiles["diagright"],     self.screen, (102, 10), False),
				(tiles["horiznc"],       self.screen, (104, 11), False),
				(tiles["eobright"],      self.screen, (106, 11), False),
				(tiles["eobright"],      self.screen, (106, 13), False),
			],
			False)

		self.blocks["YOSKL1"] = OverSwitch(self, self.frame, "YOSKL1", 
			[
				(tiles["horiznc"],       self.screen, (104, 13), False),
				(tiles["eobright"],      self.screen, (106, 13), False),
				(tiles["eobleft"],       self.screen, (95, 7), False),
				(tiles["turnrightright"],self.screen, (96, 7), False),
				(tiles["diagright"],     self.screen, (97, 8), False),
				(tiles["diagright"],     self.screen, (99, 10), False),
				(tiles["diagright"],     self.screen, (101, 12), False),
				(tiles["horiznc"],       self.screen, (102, 11), False),
				(tiles["eobleft"],       self.screen, (95, 9), False),
				(tiles["horiz"],         self.screen, (96, 9), False),
				(tiles["horiznc"],       self.screen, (97, 9), False),
				(tiles["eobleft"],       self.screen, (96, 11), False),
				(tiles["turnrightright"],self.screen, (97, 11), False),
				(tiles["diagright"],     self.screen, (98, 12), False),
				(tiles["horiznc"],       self.screen, (101, 13), False),
				(tiles["eobleft"],       self.screen, (96, 13), False),
				(tiles["horiz"],         self.screen, (97, 13), False),
				(tiles["horiznc"],       self.screen, (98, 13), False),
				(tiles["eobleft"],       self.screen, (96, 15), False),
				(tiles["horiz"],         self.screen, (97, 15), False),
				(tiles["turnleftright"], self.screen, (98, 15), False),
				(tiles["diagleft"],      self.screen, (99, 14), False),
			],
			True)

		self.blocks["YOSKL4"] = OverSwitch(self, self.frame, "YOSKL4", 
			[
				(tiles["eobleft"],       self.screen, (84, 13), False),
				(tiles["horiznc"],       self.screen, (86, 13), False),
				(tiles["horiz"],         self.screen, (87, 13), False),
				(tiles["eobright"],      self.screen, (88, 13), False),
				(tiles["diagright"],      self.screen, (86, 14), False),
				(tiles["turnrightleft"], self.screen, (87, 15), False),
				(tiles["eobright"],      self.screen, (88, 15), False),
			],
			True)

		self.blocks["YOSWYE"] = OverSwitch(self, self.frame, "YOSWYE", 
			[
				(tiles["horiznc"],       self.screen, (46, 30), False),
				(tiles["horiz"],         self.screen, (47, 30), False),
				(tiles["horiznc"],       self.screen, (48, 30), False),
				(tiles["horiz"],         self.screen, (49, 30), False),
				(tiles["horiznc"],       self.screen, (50, 30), False),
				(tiles["horiz"],         self.screen, (52, 30), False),
				(tiles["horiznc"],       self.screen, (53, 30), False),
				(tiles["eobright"],      self.screen, (55, 30), False),
				(tiles["horiznc"],       self.screen, (46, 32), False),
				(tiles["horiz"],         self.screen, (47, 32), False),
				(tiles["horiznc"],       self.screen, (48, 32), False),
				(tiles["diagleft"],      self.screen, (50, 31), False),
				(tiles["diagleft"],      self.screen, (48, 33), False),
				(tiles["diagleft"],      self.screen, (53, 31), False),
				(tiles["diagleft"],      self.screen, (52, 32), False),
				(tiles["diagleft"],      self.screen, (51, 33), False),
				(tiles["diagleft"],      self.screen, (50, 34), False),
				(tiles["diagleft"],      self.screen, (49, 35), False),
				(tiles["turnleftright"], self.screen, (47, 34), False),
				(tiles["turnleftright"], self.screen, (48, 36), False),
				(tiles["horiz"],         self.screen, (46, 34), False),
				(tiles["horiz"],         self.screen, (46, 36), False),
				(tiles["horiznc"],       self.screen, (47, 36), False),
			],
			True)

		self.blocks["YOSWYW"] = OverSwitch(self, self.frame, "YOSWYW", 
			[
				(tiles["eobleft"],       self.screen, (21, 30), False),
				(tiles["horiznc"],       self.screen, (23, 30), False),
				(tiles["horiz"],         self.screen, (24, 30), False),
				(tiles["horiznc"],       self.screen, (26, 30), False),
				(tiles["horiz"],         self.screen, (27, 30), False),
				(tiles["horiznc"],       self.screen, (28, 30), False),
				(tiles["horiz"],         self.screen, (29, 30), False),
				(tiles["horiznc"],       self.screen, (30, 30), False),
				(tiles["horiz"],         self.screen, (31, 30), False),
				(tiles["diagright"],     self.screen, (23, 31), False),
				(tiles["diagright"],     self.screen, (24, 32), False),
				(tiles["diagright"],     self.screen, (25, 33), False),
				(tiles["diagright"],     self.screen, (26, 34), False),
				(tiles["diagright"],     self.screen, (27, 35), False),
				(tiles["turnrightleft"], self.screen, (28, 36), False),
				(tiles["horiznc"],       self.screen, (29, 36), False),
				(tiles["horiz"],         self.screen, (30, 36), False),
				(tiles["horiznc"],       self.screen, (31, 36), False),
				(tiles["diagright"],     self.screen, (26, 31), False),
				(tiles["horiznc"],       self.screen, (28, 32), False),
				(tiles["horiz"],         self.screen, (29, 32), False),
				(tiles["horiznc"],       self.screen, (30, 32), False),
				(tiles["horiz"],         self.screen, (31, 32), False),
				(tiles["diagright"],     self.screen, (28, 33), False),
				(tiles["turnrightleft"], self.screen, (29, 34), False),
				(tiles["horiznc"],       self.screen, (30, 34), False),
				(tiles["horiz"],         self.screen, (31, 34), False),
			],
			False)
			
		self.osBlocks["YOSCJW"] = [ "Y11", "L10", "L20", "P50" ]
		self.osBlocks["YOSCJE"] = [ "Y21", "L20", "P50" ]
		self.osBlocks["YOSEJW"] = [ "Y11", "Y10", "Y87", "Y30" ]
		self.osBlocks["YOSEJE"] = [ "Y21", "Y20", "Y10", "Y87", "Y30" ]
		self.osBlocks["YOSKL2"] = [ "Y10", "Y70", "Y53", "Y52", "Y51", "Y50" ]
		self.osBlocks["YOSKL1"] = [ "Y20", "Y70", "Y53", "Y52", "Y51", "Y50" ]
		self.osBlocks["YOSKL3"] = [ "Y10", "Y20", "Y60" ]
		self.osBlocks["YOSKL4"] = [ "Y30", "Y50", "Y51" ]
		self.osBlocks["YOSWYW"] = [ "Y70", "Y81", "Y82", "Y83", "Y84" ]
		self.osBlocks["YOSWYE"] = [ "Y81", "Y82", "Y83", "Y84", "Y87" ]

		return self.blocks, self.osBlocks

	def DefineTurnouts(self, tiles, blocks):
		self.turnouts = {}

		toList = [
			[ "YSw1",  "torightright",   CJBlocks, (133, 13) ],
			[ "YSw3",  "torightright",   CJBlocks, (130, 11) ],
			[ "YSw3b",  "torightleft",   CJBlocks, (132, 13) ],

			[ "YSw7",  "torightleft",    EEBlocks, (120, 13) ],
			[ "YSw7b", "torightright",   EEBlocks, (118, 11) ],
			[ "YSw9",  "torightleft",    EEBlocks, (117, 11) ],
			[ "YSw11", "toleftupinv",    EEBlocks, (115, 9) ],

			[ "YSw17", "torightleft",    ["YOSKL1", "YOSKL2", "YOSKL3"], (105, 13) ],
			[ "YSw21", "toleftleft",     ["YOSKL1", "YOSKL2", "YOSKL3"], (105, 11) ],
			[ "YSw21b","toleftright",    ["YOSKL1", "YOSKL2"], (103, 13) ],
			[ "YSw23", "torightleft",    ["YOSKL1", "YOSKL2"], (102, 13) ],
			[ "YSw23b","toleftdowninv",  ["YOSKL1", "YOSKL2"], (100, 11) ],
			[ "YSw25", "toleftleft",     ["YOSKL1", "YOSKL2"], (100, 13) ],
			[ "YSw27", "torightleft",    ["YOSKL1", "YOSKL2"], (99, 13) ],
			[ "YSw29", "toleftupinv",    ["YOSKL1", "YOSKL2"], (98, 9) ],

			[ "YSw33", "torightright",   ["YOSKL4"], (85, 13) ],

			[ "YSw113", "torightright",  ["YOSWYW"], (22, 30) ],
			[ "YSw115", "torightright",  ["YOSWYW"], (25, 30) ],
			[ "YSw116", "toleftdown",    ["YOSWYW"], (27, 32) ],
			[ "YSw131", "torightdown",   ["YOSWYE"], (49, 32) ],
			[ "YSw132", "toleftleft",    ["YOSWYE"], (51, 30) ],
			[ "YSw134", "toleftleft",    ["YOSWYE"], (54, 30) ],
		]

		for tonm, tileSet, blks, pos in toList:
			trnout = Turnout(self, self.frame, tonm, self.screen, tiles[tileSet], pos)
			for blknm in blks:
				blocks[blknm].AddTurnout(trnout)
				trnout.AddBlock(blknm)
			self.turnouts[tonm] = trnout

		for t in [ "YSw113", "YSw115", "YSw116", "YSw131", "YSw132", "YSw134" ]:
			self.turnouts[t].SetRouteControl(True)

		trnout = SlipSwitch(self, self.frame, "YSw19", self.screen, tiles["ssleft"], (103, 11))
		blocks["YOSKL2"].AddTurnout(trnout)
		blocks["YOSKL1"].AddTurnout(trnout)
		blocks["YOSKL3"].AddTurnout(trnout)
		trnout.AddBlock("YOSKL1")
		trnout.AddBlock("YOSKL2")
		trnout.AddBlock("YOSKL3")
		trnout.SetControllers(None, self.turnouts["YSw17"])
		self.turnouts["YSw19"] = trnout
		
		self.turnouts["YSw3"].SetPairedTurnout(self.turnouts["YSw3b"])
		self.turnouts["YSw7"].SetPairedTurnout(self.turnouts["YSw7b"])
		self.turnouts["YSw21"].SetPairedTurnout(self.turnouts["YSw21b"])
		self.turnouts["YSw23"].SetPairedTurnout(self.turnouts["YSw23b"])

		# preserve these values so we can efficiently draw the slip switch and crossover when necessary
		self.sw17 = self.turnouts["YSw17"]
		self.sw21 = self.turnouts["YSw21"]

		return self.turnouts

	def DefineSignals(self, tiles):
		self.signals = {}

		sigList = [
			[ "Y2L",  RegAspects, True,    "right", (129, 12) ],
			[ "Y2R",  RegAspects, False,   "leftlong",  (136, 10) ],
			[ "Y4L",  RegAspects, True,    "rightlong", (129, 14) ],
			[ "Y4RA", RegAspects, False,   "leftlong",  (136, 14) ],
			[ "Y4RB", RegAspects, False,   "left",  (136, 12) ],

			[ "Y8LA", RegAspects, True,    "right", (114, 12) ],
			[ "Y8LB", RegAspects, True,    "right", (113, 10) ],
			[ "Y8LC", RegAspects, True,    "right", (112, 8)  ],
			[ "Y8R",  RegAspects, False,   "leftlong",  (121, 10) ],
			[ "Y10L", AdvAspects, True,    "rightlong", (114, 14) ],
			[ "Y10R", RegAspects, False,   "left",  (121, 12) ],

			[ "Y22L",  RegAspects, True,   "right", (95, 6) ],
			[ "Y22R",  RegSloAspects, False,  "leftlong",  (106, 10) ],
			[ "Y24LA", RegAspects, True,   "right", (95, 10) ],
			[ "Y24LB", RegAspects, True,   "right", (95, 8) ],
			[ "Y26LA", RegAspects, True,   "right", (96, 16) ],
			[ "Y26LB", RegAspects, True,   "right", (96, 14) ],
			[ "Y26LC", RegAspects, True,   "right", (96, 12) ],
			[ "Y26R",  RegAspects, False,  "left",  (106, 12)],

			[ "Y34L",  RegAspects, True,   "rightlong", (84, 14) ],
			[ "Y34RA", RegAspects, False,  "left",  (88, 14) ],
			[ "Y34RB", RegAspects, False,  "left",  (88, 12) ],

			[ "Y40LA", RegAspects, False,  "left",  (32, 29) ],
			[ "Y40LB", RegAspects, False,  "left",  (32, 31) ],
			[ "Y40LC", RegAspects, False,  "left",  (32, 33) ],
			[ "Y40LD", RegAspects, False,  "left",  (32, 35) ],
			[ "Y40R",  RegAspects, True,   "right", (21, 31) ],

			[ "Y42L",  RegAspects, False,  "left",  (55, 29) ],
			[ "Y42RA", RegAspects, True,   "right", (45, 31) ],
			[ "Y42RB", RegAspects, True,   "right", (45, 33) ],
			[ "Y42RC", RegAspects, True,   "right", (45, 35) ],
			[ "Y42RD", RegAspects, True,   "right", (45, 37) ],
		]
		for signm, atype, east, tileSet, pos in sigList:
			self.signals[signm]  = Signal(self, self.screen, self.frame, signm, atype, east, pos, tiles[tileSet])  

		blockSigs = {
			# which signals govern stopping sections, west and east
			"Y11": ("Y8R",  None),
			"Y20": (None, "Y10L"),
			"Y21": ("Y10R", "Y4L"),
		}

		for blknm, siglist in blockSigs.items():
			self.blocks[blknm].SetSignals(siglist)


		self.routes = {}
		self.osSignals = {}

		# cornell junction
		block = self.blocks["YOSCJW"]
		self.routes["YRtY11L10"] = Route(self.screen, block, "YRtY11L10", "L10", [ (129, 11), (130, 11), (131, 11), (132, 11), (133, 11), (134, 11), (135, 11), (136, 11) ], "Y11", [RESTRICTING, MAIN], ["YSw3"])
		self.routes["YRtY11L20"] = Route(self.screen, block, "YRtY11L20", "L20", [ (129, 11), (130, 11), (131, 12), (132, 13), (133, 13), (134, 13), (135, 13), (136, 13) ], "Y11", [RESTRICTING, RESTRICTING], ["YSw1", "YSw3"])
		self.routes["YRtY11P50"] = Route(self.screen, block, "YRtY11P50", "P50", [ (129, 11), (130, 11), (131, 12), (132, 13), (133, 13), (134, 14), (135, 15), (136, 15) ], "Y11", [RESTRICTING, DIVERGING], ["YSw1", "YSw3"])

		block = self.blocks["YOSCJE"]
		self.routes["YRtY21L20"] = Route(self.screen, block, "YRtY21L20", "Y21", [ (129, 13), (130, 13), (131, 13), (132, 13), (133, 13), (134, 13), (135, 13), (136, 13) ], "L20", [MAIN, RESTRICTING], ["YSw1", "YSw3"])
		self.routes["YRtY21P50"] = Route(self.screen, block, "YRtY21P50", "Y21", [ (129, 13), (130, 13), (131, 13), (132, 13), (133, 13), (134, 14), (135, 15), (136, 15) ], "P50", [DIVERGING, RESTRICTING], ["YSw1", "YSw3"])

		self.signals["Y2L"].AddPossibleRoutes("YOSCJW", [ "YRtY11L10", "YRtY11L20", "YRtY11P50" ])
		self.signals["Y2R"].AddPossibleRoutes("YOSCJW", [ "YRtY11L10" ])

		self.signals["Y4L"].AddPossibleRoutes("YOSCJE", [ "YRtY21L20", "YRtY21P50" ])
		self.signals["Y4RB"].AddPossibleRoutes("YOSCJE", [ "YRtY21L20" ])
		self.signals["Y4RB"].AddPossibleRoutes("YOSCJW", [ "YRtY11L20" ])
		self.signals["Y4RA"].AddPossibleRoutes("YOSCJE", [ "YRtY21P50" ])
		self.signals["Y4RA"].AddPossibleRoutes("YOSCJW", [ "YRtY11P50" ])

		self.osSignals["YOSCJW"] = [ "Y2L", "Y2R", "Y4RA", "Y4RB" ]
		self.osSignals["YOSCJE"] = [ "Y2L", "Y4L", "Y4RA", "Y4RB" ]

		# east end junction
		block = self.blocks["YOSEJW"] 
		self.routes["YRtY10Y11"] = Route(self.screen, block, "YRtY10Y11", "Y11", [ (114, 11), (115, 11), (116, 11), (117, 11), (118, 11), (119, 11), (120, 11), (121, 11) ], "Y10", [RESTRICTING, MAIN], ["YSw7", "YSw9"])
		self.routes["YRtY30Y11"] = Route(self.screen, block, "YRtY30Y11", "Y11", [ (112, 7), (113, 7), (114, 8), (115, 9), (116, 10), (117, 11), (118, 11), (119, 11), (120, 11), (121, 11) ], "Y30", [RESTRICTING, DIVERGING], ["YSw7", "YSw9", "YSw11"])
		self.routes["YRtY87Y11"] = Route(self.screen, block, "YRtY87Y11", "Y11", [ (113, 9), (114, 9), (115, 9), (116, 10), (117, 11), (118, 11), (119, 11), (120, 11), (121, 11) ], "Y87", [RESTRICTING, RESTRICTING], ["YSw7", "YSw9", "YSw11"])

		block = self.blocks["YOSEJE"]
		self.routes["YRtY20Y21"] = Route(self.screen, block, "YRtY20Y21", "Y20", [ (114, 13), (115, 13), (116, 13), (117, 13), (118, 13), (119, 13), (120, 13), (121, 13) ], "Y21", [MAIN, RESTRICTING], ["YSw7"])
		self.routes["YRtY30Y21"] = Route(self.screen, block, "YRtY30Y21", "Y30", [ (112, 7), (113, 7), (114, 8), (115, 9), (116, 10), (117, 11), (118, 11), (119, 12), (120, 13), (121, 13) ], "Y21", [RESTRICTING, RESTRICTING], ["YSw7", "YSw9", "YSw11"])
		self.routes["YRtY87Y21"] = Route(self.screen, block, "YRtY87Y21", "Y87", [ (113, 9), (114, 9), (115, 9), (116, 10), (117, 11), (118, 11), (119, 12), (120, 13), (121, 13) ], "Y21", [RESTRICTING, RESTRICTING], ["YSw7", "YSw9", "YSw11"])
		self.routes["YRtY10Y21"] = Route(self.screen, block, "YRtY10Y21", "Y10", [ (114, 11), (115, 11), (116, 11), (117, 11), (118, 11), (119, 12), (120, 13), (121, 13) ], "Y21", [RESTRICTING, RESTRICTING], ["YSw7", "YSw9"])

		self.signals["Y8LA"].AddPossibleRoutes("YOSEJW", ["YRtY10Y11"])
		self.signals["Y8LA"].AddPossibleRoutes("YOSEJE", ["YRtY10Y21"])
		self.signals["Y8LB"].AddPossibleRoutes("YOSEJW", ["YRtY87Y11"])
		self.signals["Y8LB"].AddPossibleRoutes("YOSEJE", ["YRtY87Y21"])
		self.signals["Y8LC"].AddPossibleRoutes("YOSEJW", ["YRtY30Y11"])
		self.signals["Y8LC"].AddPossibleRoutes("YOSEJE", ["YRtY30Y21"])
		self.signals["Y8R"].AddPossibleRoutes("YOSEJW", ["YRtY10Y11", "YRtY87Y11", "YRtY30Y11"])
		self.signals["Y10L"].AddPossibleRoutes("YOSEJE", ["YRtY20Y21"])
		self.signals["Y10R"].AddPossibleRoutes("YOSEJE", ["YRtY20Y21", "YRtY10Y21", "YRtY87Y21", "YRtY30Y21"])

		self.osSignals["YOSEJW"] = [ "Y8LA", "Y8LB", "Y8LC", "Y8R" ]
		self.osSignals["YOSEJE"] = [ "Y8LA", "Y8LB", "Y8LC", "Y10L", "Y10R" ]

		# Kale interlocking
		block = self.blocks["YOSKL1"]
		self.routes["YRtY20Y51"] = Route(self.screen, block, "YRtY20Y51", "Y51", [ (96, 13), (97, 13), (98, 13), (99, 13), (100, 13), (101, 13), (102, 13), (103, 13), (104, 13), (105, 13), (106, 13) ], "Y20", [RESTRICTING, RESTRICTING], ["YSw17", "YSw21", "YSw23", "YSw25", "YSw27"])
		self.routes["YRtY20Y50"] = Route(self.screen, block, "YRtY20Y50", "Y50", [ (96, 15), (97, 15), (98, 15), (99, 14), (100, 13), (101, 13), (102, 13), (103, 13), (104, 13), (105, 13), (106, 13) ], "Y20", [RESTRICTING, RESTRICTING], ["YSw17", "YSw21", "YSw23", "YSw25"])
		self.routes["YRtY20Y70"] = Route(self.screen, block, "YRtY20Y70", "Y70", [ (96, 11), (97, 11), (98, 12), (99, 13), (100, 13), (101, 13), (102, 13), (103, 13), (104, 13), (105, 13), (106, 13) ], "Y20", [RESTRICTING, DIVERGING], ["YSw17", "YSw21", "YSw23", "YSw25", "YSw27"])
		self.routes["YRtY20Y52"] = Route(self.screen, block, "YRtY20Y52", "Y52", [ (95, 9), (96, 9), (97, 9), (98, 9), (99, 10), (100, 11), (101, 12), (102, 13), (103, 13), (104, 13), (105, 13), (106, 13) ], "Y20", [RESTRICTING, RESTRICTING], ["YSw17", "YSw19", "YSw21", "YSw23", "YSw29"])
		self.routes["YRtY20Y53"] = Route(self.screen, block, "YRtY20Y53", "Y53", [ (95, 7), (96, 7), (97, 8), (98, 9), (99, 10), (100, 11), (101, 12), (102, 13), (103, 13), (104, 13), (105, 13), (106, 13) ], "Y20", [RESTRICTING, RESTRICTING], ["YSw17", "YSw19", "YSw21", "YSw23", "YSw29"])
		
		block = self.blocks["YOSKL3"]
		self.routes["YRtY20Y60"] = Route(self.screen, block, "YRtY20Y60", "Y20", [ (95, 5), (96, 5), (97, 5), (98, 6), (99, 7), (100, 8), (101, 9), (102, 10), (103, 11), (104, 12), (105, 13), (106, 13) ], "Y60", [RESTRICTING, RESTRICTING], ["YSw17", "YSw19", "YSw21"])

		block = self.blocks["YOSKL2"]
		self.routes["YRtY10Y52"] = Route(self.screen, block, "YRtY10Y52", "Y10", [ (95, 9), (96, 9), (97, 9), (98, 9), (99, 10), (100, 11), (101, 11), (102, 11), (103, 11), (104, 11), (105, 11), (106, 11) ], "Y52", [RESTRICTING, SLOW], ["YSw17", "YSw19", "YSw21", "YSw29"])
		self.routes["YRtY10Y50"] = Route(self.screen, block, "YRtY10Y50", "Y10", [ (96, 15), (97, 15), (98, 15), (99, 14), (100, 13), (101, 13), (102, 13), (103, 13), (104, 12), (105, 11), (106, 11) ], "Y50", [RESTRICTING, SLOW], ["YSw17", "YSw21", "YSw23", "YSw25"])
		self.routes["YRtY10Y51"] = Route(self.screen, block, "YRtY10Y51", "Y10", [ (96, 13), (97, 13), (98, 13), (99, 13), (100, 13), (101, 13), (102, 13), (103, 13), (104, 12), (105, 11), (106, 11) ], "Y51", [RESTRICTING, RESTRICTING], ["YSw17", "YSw21", "YSw23", "YSw25", "YSw27"])
		self.routes["YRtY10Y70"] = Route(self.screen, block, "YRtY10Y70", "Y10", [ (96, 11), (97, 11), (98, 12), (99, 13), (100, 13), (101, 13), (102, 13), (103, 13), (104, 12), (105, 11), (106, 11) ], "Y70", [RESTRICTING, RESTRICTING], ["YSw17", "YSw21", "YSw23", "YSw25", "YSw27"])
		self.routes["YRtY10Y53"] = Route(self.screen, block, "YRtY10Y53", "Y10", [ (95, 7), (96, 7), (97, 8), (98, 9), (99, 10), (100, 11), (101, 11), (102, 11), (103, 11), (104, 11), (105, 11), (106, 11) ], "Y53", [RESTRICTING, SLOW], ["YSw17", "YSw19", "YSw21", "YSw29"])

		block = self.blocks["YOSKL3"]
		self.routes["YRtY10Y60"] = Route(self.screen, block, "YRtY10Y60", "Y10", [ (95, 5), (96, 5), (97, 5), (98, 6), (99, 7), (100, 8), (101, 9), (102, 10), (103, 11), (104, 11), (105, 11), (106, 11) ], "Y60", [RESTRICTING, RESTRICTING], ["YSw17", "YSw19", "YSw21"])

		self.signals["Y22R"].AddPossibleRoutes("YOSKL2", [ "YRtY10Y50", "YRtY10Y51", "YRtY10Y52", "YRtY10Y53", "YRtY10Y70" ])
		self.signals["Y22R"].AddPossibleRoutes("YOSKL3", [ "YRtY10Y60" ])
		self.signals["Y26R"].AddPossibleRoutes("YOSKL1", [ "YRtY20Y50", "YRtY20Y51", "YRtY20Y52", "YRtY20Y53", "YRtY20Y70" ])
		self.signals["Y26R"].AddPossibleRoutes("YOSKL3", [ "YRtY20Y60" ])
		self.signals["Y22L"].AddPossibleRoutes("YOSKL3", [ "YRtY10Y60", "YRtY20Y60" ])
		self.signals["Y24LA"].AddPossibleRoutes("YOSKL2", [ "YRtY10Y52" ])
		self.signals["Y24LA"].AddPossibleRoutes("YOSKL1", [ "YRtY20Y52" ])
		self.signals["Y24LB"].AddPossibleRoutes("YOSKL2", [ "YRtY10Y53" ])
		self.signals["Y24LB"].AddPossibleRoutes("YOSKL1", [ "YRtY20Y53" ])
		self.signals["Y26LA"].AddPossibleRoutes("YOSKL2", [ "YRtY10Y50" ])
		self.signals["Y26LA"].AddPossibleRoutes("YOSKL1", [ "YRtY20Y50" ])
		self.signals["Y26LB"].AddPossibleRoutes("YOSKL2", [ "YRtY10Y51" ])
		self.signals["Y26LB"].AddPossibleRoutes("YOSKL1", [ "YRtY20Y51" ])
		self.signals["Y26LC"].AddPossibleRoutes("YOSKL2", [ "YRtY10Y70" ])
		self.signals["Y26LC"].AddPossibleRoutes("YOSKL1", [ "YRtY20Y70" ])

		self.osSignals["YOSKL2"] = [ "Y22R", "Y24LA", "Y24LB", "Y26LA", "Y26LB", "Y26LC" ]
		self.osSignals["YOSKL1"] = [ "Y26R", "Y24LA", "Y24LB", "Y26LA", "Y26LB", "Y26LC" ]
		self.osSignals["YOSKL3"] = [ "Y22L", "Y22R", "Y26R" ]

		# Kale west end
		block = self.blocks["YOSKL4"]
		self.routes["YRtY30Y51"] = Route(self.screen, block, "YRtY30Y51", "Y30", [ (84, 13), (85, 13), (86, 13), (87, 13), (88, 13) ], "Y51", [SLOW, RESTRICTING], ["YSw33"])
		self.routes["YRtY30Y50"] = Route(self.screen, block, "YRtY30Y50", "Y30", [ (84, 13), (85, 13), (86, 14), (87, 15), (88, 15) ], "Y50", [SLOW, RESTRICTING], ["YSw33"])

		self.signals["Y34L"].AddPossibleRoutes("YOSKL4", [ "YRtY30Y51", "YRtY30Y50" ])
		self.signals["Y34RA"].AddPossibleRoutes("YOSKL4", [ "YRtY30Y50" ])
		self.signals["Y34RB"].AddPossibleRoutes("YOSKL4", [ "YRtY30Y51" ])

		self.osSignals["YOSKL4"] = [ "Y34L", "Y34RA", "Y34RB" ]

		# Waterman yard
		block = self.blocks["YOSWYW"]
		self.routes["YRtY70Y81"] = Route(self.screen, block, "YRtY70Y81", "Y81", [ (21, 30), (22, 30), (23, 30), (24, 30), (25, 30), (26, 30), (27, 30), (28, 30), (29, 30), (30, 30), (31, 30) ], "Y70", [RESTRICTING, DIVERGING], ["YSw113", "YSw115"])
		self.routes["YRtY70Y82"] = Route(self.screen, block, "YRtY70Y82", "Y82", [ (21, 30), (22, 30), (23, 30), (24, 30), (25, 30), (26, 31), (27, 32), (28, 32), (29, 32), (30, 32), (31, 32) ], "Y70", [RESTRICTING, DIVERGING], ["YSw113", "YSw115", "YSw116"])
		self.routes["YRtY70Y83"] = Route(self.screen, block, "YRtY70Y83", "Y83", [ (21, 30), (22, 30), (23, 30), (24, 30), (25, 30), (26, 31), (27, 32), (28, 33), (29, 34), (30, 34), (31, 34) ], "Y70", [RESTRICTING, DIVERGING], ["YSw113", "YSw115", "YSw116"])
		self.routes["YRtY70Y84"] = Route(self.screen, block, "YRtY70Y84", "Y84", [ (21, 30), (22, 30), (23, 31), (24, 32), (25, 33), (26, 34), (27, 35), (28, 36), (29, 36), (30, 36), (31, 36) ], "Y70", [RESTRICTING, DIVERGING], ["YSw113"])

		block = self.blocks["YOSWYE"]
		self.routes["YRtY87Y81"] = Route(self.screen, block, "YRtY87Y81", "Y81", [ (46, 30), (47, 30), (48, 30), (49, 30), (50, 30), (51, 30), (52, 30), (53, 30), (54, 30), (55, 30) ], "Y87", [RESTRICTING, RESTRICTING], ["YSw134", "YSw132"])
		self.routes["YRtY87Y82"] = Route(self.screen, block, "YRtY87Y82", "Y82", [ (46, 32), (47, 32), (48, 32), (49, 32), (50, 31), (51, 30), (52, 30), (53, 30), (54, 30), (55, 30) ], "Y87", [RESTRICTING, RESTRICTING], ["YSw134", "YSw132", "YSw131"])
		self.routes["YRtY87Y83"] = Route(self.screen, block, "YRtY87Y83", "Y83", [ (46, 34), (47, 34), (48, 33), (49, 32), (50, 31), (51, 30), (52, 30), (53, 30), (54, 30), (55, 30) ], "Y87", [RESTRICTING, RESTRICTING], ["YSw134", "YSw132", "YSw131"])
		self.routes["YRtY87Y84"] = Route(self.screen, block, "YRtY87Y84", "Y84", [ (46, 36), (47, 36), (48, 36), (49, 35), (50, 34), (51, 33), (52, 32), (53, 31), (54, 30), (55, 30) ], "Y87", [RESTRICTING, RESTRICTING], ["YSw134"])

		self.signals["Y40R"].AddPossibleRoutes("YOSWYW", [ "YRtY70Y81", "YRtY70Y82", "YRtY70Y83", "YRtY70Y84" ])
		self.signals["Y40LA"].AddPossibleRoutes("YOSWYW", [ "YRtY70Y81" ])
		self.signals["Y40LB"].AddPossibleRoutes("YOSWYW", [ "YRtY70Y82" ])
		self.signals["Y40LC"].AddPossibleRoutes("YOSWYW", [ "YRtY70Y83" ])
		self.signals["Y40LD"].AddPossibleRoutes("YOSWYW", [ "YRtY70Y84" ])
		self.signals["Y42L"].AddPossibleRoutes("YOSWYE", [ "YRtY87Y81", "YRtY87Y82", "YRtY87Y83", "YRtY87Y84" ])
		self.signals["Y42RA"].AddPossibleRoutes("YOSWYE", [ "YRtY87Y81" ])
		self.signals["Y42RB"].AddPossibleRoutes("YOSWYE", [ "YRtY87Y82" ])
		self.signals["Y42RC"].AddPossibleRoutes("YOSWYE", [ "YRtY87Y83" ])
		self.signals["Y42RD"].AddPossibleRoutes("YOSWYE", [ "YRtY87Y84" ])

		self.osSignals["YOSWYW"] = [ "Y40R", "Y40LA", "Y40LB", "Y40LC", "Y40LD" ]
		self.osSignals["YOSWYE"] = [ "Y42L", "Y42RA", "Y42RB", "Y42RC", "Y42RD" ]

		return self.signals

	def DefineButtons(self, tiles):
		self.buttons = {}
		self.osButtons = {}

		b = Button(self, self.screen, self.frame, "YWWB1", (32, 30), tiles)
		self.buttons["YWWB1"] = b

		b = Button(self, self.screen, self.frame, "YWWB2", (32, 32), tiles)
		self.buttons["YWWB2"] = b

		b = Button(self, self.screen, self.frame, "YWWB3", (32, 34), tiles)
		self.buttons["YWWB3"] = b

		b = Button(self, self.screen, self.frame, "YWWB4", (32, 36), tiles)
		self.buttons["YWWB4"] = b

		self.osButtons["YOSWYW"] = [ "YWWB1", "YWWB2", "YWWB3", "YWWB4" ]

		b = Button(self, self.screen, self.frame, "YWEB1", (45, 30), tiles)
		self.buttons["YWEB1"] = b

		b = Button(self, self.screen, self.frame, "YWEB2", (45, 32), tiles)
		self.buttons["YWEB2"] = b

		b = Button(self, self.screen, self.frame, "YWEB3", (45, 34), tiles)
		self.buttons["YWEB3"] = b

		b = Button(self, self.screen, self.frame, "YWEB4", (45, 36), tiles)
		self.buttons["YWEB4"] = b

		self.osButtons["YOSWYE"] = [ "YWEB1", "YWEB2", "YWEB3", "YWEB4" ]

		return self.buttons

	def DefineIndicators(self):
		self.indicators = {}
		indNames = [ "CBKale", "CBEastEnd", "CBCornellJct", "CBEngineYard", "CBWaterman" ]
		for ind in indNames:
			self.indicators[ind] = Indicator(self.frame, self, ind)

		return self.indicators
