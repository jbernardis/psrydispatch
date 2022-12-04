from district import District

from block import Block, OverSwitch, Route
from turnout import Turnout, SlipSwitch
from signal import Signal
from handswitch import HandSwitch

from constants import LaKr, SLIPSWITCH, NORMAL, REVERSE, RESTRICTING, SLOW, , MAIN, DIVERGING, RegAspects, AdvAspects


class Port (District):
	def __init__(self, name, frame, screen):
		District.__init__(self, name, frame, screen)

	def CrossingEastWestBoundary(self, osblk, blk):
		blkNm = blk.GetName()
		osNm = osblk.GetName()
		if blkNm == "P50":
			if osNm in [ "POSPJ1", "POSPJ2" ]:
				return True
		elif blkNm == "P30":
			if osNm == "POSPJ2":
				return True

		return False

	def DoTurnoutAction(self, turnout, state):
		tn = turnout.GetName()
		if tn == "PASw35":
			bstat = NORMAL if self.turnouts["PASw37"].IsNormal() else REVERSE
			turnout.SetStatus([state, bstat])
			turnout.Draw()
			to = self.turnouts["PASw33"]
			sstat = to.GetStatus()
			to.SetStatus([sstat[0], state])
			to.Draw()

		elif tn == "PASw33":
			bstat = NORMAL if self.turnouts["PASw35"].IsNormal() else REVERSE
			turnout.SetStatus([state, bstat])
			turnout.Draw()

		elif tn == "PASw37":
			District.DoTurnoutAction(self, turnout, state)
			to = self.turnouts["PASw35"]
			sstat = to.GetStatus()
			to.SetStatus([sstat[0], state])
			to.Draw()

		else:
			District.DoTurnoutAction(self, turnout, state)

		if tn == "PASw33":
			trnout = self.turnouts["PASw35"]
			trnout.UpdateStatus()
			trnout.Draw()

	def DetermineRoute(self, blocks):
		for block in blocks:
			bname = block.GetName()
			if bname in ["POSCJ1", "POSCJ2", "POSSJ1", "POSSJ2"]:  # Port B
				s1 = 'N' if self.turnouts["PBSw1"].IsNormal() else 'R'
				s3 = 'N' if self.turnouts["PBSw3"].IsNormal() else 'R'
				s11 = 'N' if self.turnouts["PBSw11"].IsNormal() else 'R'
				s13 = 'N' if self.turnouts["PBSw13"].IsNormal() else 'R'
				self.turnouts["PBSw11"].SetLock("PBSw13", s13 == 'R', refresh=True)
				self.turnouts["PBSw11b"].SetLock("PBSw13", s13 == 'R', refresh=True)
				self.turnouts["PBSw13"].SetLock("PBSw11", s11 == 'R', refresh=True)
				self.turnouts["PBSw13b"].SetLock("PBSw11", s11 == 'R', refresh=True)

				self.turnouts["PBSw1"].SetLock("PBSw3", s3 == 'R', refresh=True)
				self.turnouts["PBSw1b"].SetLock("PBSw3", s3 == 'R', refresh=True)
				self.turnouts["PBSw3"].SetLock("PBSw1", s1 == 'R', refresh=True)
				self.turnouts["PBSw3b"].SetLock("PBSw1", s1 == 'R', refresh=True)

				if bname == "POSCJ1":
					if s11+s13 == "NN":
						block.SetRoute(self.routes["PRtP31P32"])
					elif s11+s13 == "RN":
						block.SetRoute(self.routes["PRtP31P42"])
					else:
						block.SetRoute(None)

				elif bname == "POSCJ2":
					if s11+s13 == "NN":
						block.SetRoute(self.routes["PRtP41P42"])
					elif s11+s13 == "NR":
						block.SetRoute(self.routes["PRtP41P32"])
					else:
						block.SetRoute(None)

				elif bname == "POSSJ1":
					if s1+s3 == "NN":
						block.SetRoute(self.routes["PRtP30P31"])
					elif s1+s3 == "NR":
						block.SetRoute(self.routes["PRtP30P41"])
					else:
						block.SetRoute(None)

				elif bname == "POSSJ2":
					if s1+s3 == "NN":
						block.SetRoute(self.routes["PRtP40P41"])
					elif s1+s3 == "RN":
						block.SetRoute(self.routes["PRtP40P31"])
					else:
						block.SetRoute(None)

			elif bname in ["POSPJ1", "POSPJ2"]:  # Port A
				s27 = 'N' if self.turnouts["PASw27"].IsNormal() else 'R'
				s29 = 'N' if self.turnouts["PASw29"].IsNormal() else 'R'
				s31 = 'N' if self.turnouts["PASw31"].IsNormal() else 'R'
				s33 = 'N' if self.turnouts["PASw33"].IsNormal() else 'R'
				s35 = 'N' if self.turnouts["PASw35"].IsNormal() else 'R'
				s37 = 'N' if self.turnouts["PASw37"].IsNormal() else 'R'

				if bname == "POSPJ1":
					if s27+s29+s31+s35+s37 == "NNRNR":
						block.SetRoute(self.routes["PRtV11P50"])
					elif s27+s29+s31+s35+s37 == "RNRNR":
						block.SetRoute(self.routes["PRtP60P50"])
					elif s29+s31+s35+s37 == "RRNR":
						block.SetRoute(self.routes["PRtP61P50"])
					elif s31+s35+s37 == "NNR":
						block.SetRoute(self.routes["PRtP10P50"])
					elif s27+s29+s31+s35+s37 == "NNRNN":
						block.SetRoute(self.routes["PRtV11P11"])
					elif s27+s29+s31+s35+s37 == "RNRNN":
						block.SetRoute(self.routes["PRtP60P11"])
					elif s29+s31+s35+s37 == "RRNN":
						block.SetRoute(self.routes["PRtP61P11"])
					elif s31+s35+s37 == "NNN":
						block.SetRoute(self.routes["PRtP10P11"])
					else:
						block.SetRoute(None)

				elif bname == "POSPJ2":
					if s33+s35+s37 == "NRR":
						block.SetRoute(self.routes["PRtP20P50"])
					elif s33+s35+s37 == "RRR":
						block.SetRoute(self.routes["PRtP30P50"])
					elif s33+s35+s37 == "NRN":
						block.SetRoute(self.routes["PRtP20P11"])
					elif s33+s35+s37 == "RRN":
						block.SetRoute(self.routes["PRtP30P11"])
					elif s33+s35 == "NN":
						block.SetRoute(self.routes["PRtP20P21"])
					elif s33+s35 == "RN":
						block.SetRoute(self.routes["PRtP30P21"])
					else:
						block.SetRoute(None)

			elif bname in ["POSSP1", "POSSP2", "POSSP3", "POSSP4", "POSSP5" ]:  # Southport
				s1 = 'N' if self.turnouts["PASw1"].IsNormal() else 'R'
				s3 = 'N' if self.turnouts["PASw3"].IsNormal() else 'R'
				s5 = 'N' if self.turnouts["PASw5"].IsNormal() else 'R'
				s7 = 'N' if self.turnouts["PASw7"].IsNormal() else 'R'
				s9 = 'N' if self.turnouts["PASw9"].IsNormal() else 'R'
				s11 = 'N' if self.turnouts["PASw11"].IsNormal() else 'R'
				s13 = 'N' if self.turnouts["PASw13"].IsNormal() else 'R'
				s15 = 'N' if self.turnouts["PASw15"].IsNormal() else 'R'
				s17 = 'N' if self.turnouts["PASw17"].IsNormal() else 'R'
				s19 = 'N' if self.turnouts["PASw19"].IsNormal() else 'R'
				s21 = 'N' if self.turnouts["PASw21"].IsNormal() else 'R'
				s23 = 'N' if self.turnouts["PASw23"].IsNormal() else 'R'
				if bname == "POSSP1":
					if s15+s17 == "RN":
						block.SetRoute(self.routes["PRtP7V10"])
					elif s15+s17 == "RR":
						block.SetRoute(self.routes["PRtP7P60"])
					elif s15+s19 == "NN":
						block.SetRoute(self.routes["PRtP7P61"])
					else:
						block.SetRoute(None)

				elif bname == "POSSP2":
					if s7+s15+s19+s21+s23 == "NNRRN":
						block.SetRoute(self.routes["PRtP7P10"])
					elif s7+s19+s21+s23 == "NNRN":
						block.SetRoute(self.routes["PRtP6P10"])
					elif s7+s21+s23 == "NNN":
						block.SetRoute(self.routes["PRtP5P10"])
					elif s5+s7+s23 == "NRN":
						block.SetRoute(self.routes["PRtP4P10"])
					elif s3+s5+s7+s9 == "NRRN":
						block.SetRoute(self.routes["PRtP3P10"])
					elif s1+s3+s5+s7+s9 == "NRRRN":
						block.SetRoute(self.routes["PRtP2P10"])
					elif s1+s3+s5+s7+s9 == "RRRRN":
						block.SetRoute(self.routes["PRtP1P10"])
					else:
						block.SetRoute(None)

				elif bname == "POSSP3":
					if s5+s7+s15+s19+s21+s23 == "NNNRRR":
						block.SetRoute(self.routes["PRtP7P20"])
					elif s5+s7+s19+s21+s23 == "NNNRR":
						block.SetRoute(self.routes["PRtP6P20"])
					elif s5+s7+s21+s23 == "NNNR":
						block.SetRoute(self.routes["PRtP5P20"])
					elif s5+s7+s23 == "NNN":
						block.SetRoute(self.routes["PRtP4P20"])
					elif s3+s5+s7+s9 == "NRNN":
						block.SetRoute(self.routes["PRtP3P20"])
					elif s1+s3+s5+s7+s9 == "NRRNN":
						block.SetRoute(self.routes["PRtP2P20"])
					elif s1+s3+s5+s7+s9 == "RRRNN":
						block.SetRoute(self.routes["PRtP1P20"])
					else:
						block.SetRoute(None)

				elif bname == "POSSP4":
					if s3+s5+s9+s11 == "NNNN":
						block.SetRoute(self.routes["PRtP3P62"])
					elif s3+s5+s9+s11+s13 == "NNNRR":
						block.SetRoute(self.routes["PRtP3P63"])
					elif s3+s5+s9+s11+s13 == "NNNRN":
						block.SetRoute(self.routes["PRtP3P64"])
					elif s1+s3+s5+s9+s11 == "NRNNN":
						block.SetRoute(self.routes["PRtP2P62"])
					elif s1+s3+s5+s9+s11+s13 == "NRNNRR":
						block.SetRoute(self.routes["PRtP2P63"])
					elif s1+s3+s5+s9+s11+s13 == "NRNNRN":
						block.SetRoute(self.routes["PRtP2P64"])
					elif s1+s3+s5+s9+s11 == "RRNNN":
						block.SetRoute(self.routes["PRtP1P62"])
					elif s1+s3+s5+s9+s11+s13 == "RRNNRR":
						block.SetRoute(self.routes["PRtP1P63"])
					elif s1+s3+s5+s9+s11+s13 == "RRNNRN":
						block.SetRoute(self.routes["PRtP1P64"])
					else:
						block.SetRoute(None)

				elif bname == "POSSP5":
					if s3+s9 == "NR":
						block.SetRoute(self.routes["PRtP3P40"])
					elif s1+s3+s9 == "NNN":
						block.SetRoute(self.routes["PRtP2P40"])
					elif s1+s3+s9 == "RNN":
						block.SetRoute(self.routes["PRtP1P40"])
					else:
						block.SetRoute(None)

	def DefineBlocks(self, tiles):
		self.blocks = {}
		self.osBlocks = {}

		self.blocks["V10"] = Block(self, self.frame, "V10",
			[
				(tiles["houtline"],  self.screen, (108, 18), False),
			], True)

		self.blocks["V11"] = Block(self, self.frame, "V11",
			[
				(tiles["houtline"],  self.screen, (112, 18), False),
				(tiles["houtline"],  self.screen, (113, 18), False),
				(tiles["houtline"],  self.screen, (114, 18), False),
			], True)

		self.blocks["P1"] = Block(self, self.frame, "P1",
			[
				(tiles["eobleft"],  self.screen, (93, 32), False),
				(tiles["horiz"],    self.screen, (94, 32), False),
				(tiles["horiznc"],  self.screen, (95, 32), False),
				(tiles["horiz"],    self.screen, (96, 32), False),
				(tiles["horiznc"],  self.screen, (97, 32), False),
				(tiles["horiz"],    self.screen, (98, 32), False),
				(tiles["eobright"],  self.screen, (99, 32), False),
			], True)
		self.blocks["P1"].AddTrainLoc(self.screen, (94, 32))

		self.blocks["P2"] = Block(self, self.frame, "P2",
			[
				(tiles["eobleft"],  self.screen, (89, 30), False),
				(tiles["horiz"],    self.screen, (90, 30), False),
				(tiles["horiznc"],  self.screen, (91, 30), False),
				(tiles["horiz"],    self.screen, (92, 30), False),
				(tiles["horiznc"],  self.screen, (93, 30), False),
				(tiles["horiz"],    self.screen, (94, 30), False),
				(tiles["horiznc"],  self.screen, (95, 30), False),
				(tiles["horiz"],    self.screen, (96, 30), False),
				(tiles["horiznc"],  self.screen, (97, 30), False),
				(tiles["horiz"],    self.screen, (98, 30), False),
				(tiles["eobright"],  self.screen, (99, 30), False),
			], True)
		self.blocks["P2"].AddTrainLoc(self.screen, (90, 30))

		self.blocks["P3"] = Block(self, self.frame, "P3",
			[
				(tiles["eobleft"],  self.screen, (89, 28), False),
				(tiles["horiz"],    self.screen, (90, 28), False),
				(tiles["horiznc"],  self.screen, (91, 28), False),
				(tiles["horiz"],    self.screen, (92, 28), False),
				(tiles["horiznc"],  self.screen, (93, 28), False),
				(tiles["horiz"],    self.screen, (94, 28), False),
				(tiles["horiznc"],  self.screen, (95, 28), False),
				(tiles["horiz"],    self.screen, (96, 28), False),
				(tiles["horiznc"],  self.screen, (97, 28), False),
				(tiles["horiz"],    self.screen, (98, 28), False),
				(tiles["horiznc"],  self.screen, (99, 28), False),
				(tiles["eobright"],  self.screen, (100, 28), False),
			], True)
		self.blocks["P3"].AddTrainLoc(self.screen, (90, 28))

		self.blocks["P4"] = Block(self, self.frame, "P4",
			[
				(tiles["eobleft"],  self.screen, (89, 26), False),
				(tiles["horiz"],    self.screen, (90, 26), False),
				(tiles["horiznc"],  self.screen, (91, 26), False),
				(tiles["horiz"],    self.screen, (92, 26), False),
				(tiles["horiznc"],  self.screen, (93, 26), False),
				(tiles["horiz"],    self.screen, (94, 26), False),
				(tiles["horiznc"],  self.screen, (95, 26), False),
				(tiles["horiz"],    self.screen, (96, 26), False),
				(tiles["horiznc"],  self.screen, (97, 26), False),
				(tiles["horiz"],    self.screen, (98, 26), False),
				(tiles["horiznc"],  self.screen, (99, 26), False),
				(tiles["horiz"],    self.screen, (100, 26), False),
				(tiles["eobright"],  self.screen, (101, 26), False),
			], True)
		self.blocks["P4"].AddTrainLoc(self.screen, (90, 26))

		self.blocks["P5"] = Block(self, self.frame, "P5",
			[
				(tiles["eobleft"],  self.screen, (89, 24), False),
				(tiles["horiz"],    self.screen, (90, 24), False),
				(tiles["horiznc"],  self.screen, (91, 24), False),
				(tiles["horiz"],    self.screen, (92, 24), False),
				(tiles["horiznc"],  self.screen, (93, 24), False),
				(tiles["horiz"],    self.screen, (94, 24), False),
				(tiles["horiznc"],  self.screen, (95, 24), False),
				(tiles["horiz"],    self.screen, (96, 24), False),
				(tiles["horiznc"],  self.screen, (97, 24), False),
				(tiles["horiz"],    self.screen, (98, 24), False),
				(tiles["horiznc"],  self.screen, (99, 24), False),
				(tiles["horiz"],    self.screen, (100, 24), False),
				(tiles["eobright"],  self.screen, (101, 24), False),
			], True)
		self.blocks["P5"].AddTrainLoc(self.screen, (90, 24))

		self.blocks["P6"] = Block(self, self.frame, "P6",
			[
				(tiles["eobleft"],  self.screen, (93, 22), False),
				(tiles["horiz"],    self.screen, (94, 22), False),
				(tiles["horiznc"],  self.screen, (95, 22), False),
				(tiles["horiz"],    self.screen, (96, 22), False),
				(tiles["horiznc"],  self.screen, (97, 22), False),
				(tiles["horiz"],    self.screen, (98, 22), False),
				(tiles["eobright"],  self.screen, (99, 22), False),
			], True)
		self.blocks["P6"].AddTrainLoc(self.screen, (94, 22))

		self.blocks["P7"] = Block(self, self.frame, "P7",
			[
				(tiles["eobleft"],  self.screen, (89, 20), False),
				(tiles["horiz"],    self.screen, (90, 20), False),
				(tiles["horiznc"],  self.screen, (91, 20), False),
				(tiles["horiz"],    self.screen, (92, 20), False),
				(tiles["horiznc"],  self.screen, (93, 20), False),
				(tiles["horiz"],    self.screen, (94, 20), False),
				(tiles["horiznc"],  self.screen, (95, 20), False),
				(tiles["horiz"],    self.screen, (96, 20), False),
				(tiles["eobright"],  self.screen, (97, 20), False),
			], True)
		self.blocks["P7"].AddTrainLoc(self.screen, (90, 20))

		self.blocks["P10"] = Block(self, self.frame, "P10",
			[
				(tiles["horiznc"],  self.screen, (111, 24), False),
				(tiles["horiz"],    self.screen, (112, 24), False),
				(tiles["horiznc"],  self.screen, (113, 24), False),
				(tiles["horiz"],    self.screen, (114, 24), False),
				(tiles["horiznc"],  self.screen, (115, 24), False),
				(tiles["horiz"],    self.screen, (116, 24), False),
			], True)
		self.blocks["P10"].AddTrainLoc(self.screen, (114, 24))
		self.blocks["P10"].AddStoppingBlock([
				(tiles["horiznc"],  self.screen, (117, 24), False),
				(tiles["horiz"],    self.screen, (118, 24), False),
			], True)

		self.blocks["P11"] = Block(self, self.frame, "P11",
			[
				(tiles["eobleft"],  self.screen, (128, 24), False),
				(tiles["horiznc"],  self.screen, (129, 24), False),
				(tiles["horiz"],    self.screen, (130, 24), False),
				(tiles["horiznc"],  self.screen, (131, 24), False),
				(tiles["horiz"],    self.screen, (132, 24), False),
				(tiles["horiznc"],  self.screen, (133, 24), False),
				(tiles["horiz"],    self.screen, (134, 24), False),
				(tiles["horiznc"],  self.screen, (135, 24), False),
				(tiles["horiz"],    self.screen, (136, 24), False),
				(tiles["horiznc"],  self.screen, (137, 24), False),
				(tiles["horiz"],    self.screen, (138, 24), False),
				(tiles["turnleftright"], self.screen, (139, 24), False),
				(tiles["diagleft"], self.screen, (140, 23), False),
				(tiles["diagleft"], self.screen, (141, 22), False),
				(tiles["diagleft"], self.screen, (142, 21), False),
				(tiles["diagleft"], self.screen, (143, 20), False),
				(tiles["diagleft"], self.screen, (144, 19), False),
				(tiles["diagleft"], self.screen, (145, 18), False),
				(tiles["diagleft"], self.screen, (146, 17), False),
				(tiles["diagleft"], self.screen, (147, 16), False),
				(tiles["turnleftleft"], self.screen, (148, 15), False),
				(tiles["horiznc"],  self.screen, (149, 15), False),
				(tiles["horiz"],    self.screen, (150, 15), False),
				(tiles["horiznc"],  self.screen, (151, 15), False),
				(tiles["horiz"],    self.screen, (152, 15), False),
				(tiles["horiznc"],  self.screen, (153, 15), False),
				(tiles["horiz"],    self.screen, (154, 15), False),
				(tiles["horiznc"],  self.screen, (155, 15), False),
				(tiles["horiz"],    self.screen, (156, 15), False),
				(tiles["horiznc"],  self.screen, (157, 15), False),
				(tiles["horiz"],    self.screen, (158, 15), False),
				(tiles["horiz"],    LaKr, (0, 15), False),
				(tiles["horiznc"],  LaKr, (1, 15), False),
				(tiles["horiz"],    LaKr, (2, 15), False),
				(tiles["horiznc"],  LaKr, (3, 15), False),
				(tiles["horiz"],    LaKr, (4, 15), False),
			], True)
		self.blocks["P11"].AddTrainLoc(self.screen, (130, 24))
		self.blocks["P11"].AddTrainLoc(LaKr, (2, 15))
		self.blocks["P11"].AddStoppingBlock([
				(tiles["horiznc"],  LaKr, (5, 15), False),
				(tiles["horiz"],    LaKr, (6, 15), False),
				(tiles["eobright"], LaKr, (7, 15), False),
			], True)
		self.blocks["P11"].AddStoppingBlock([
				(tiles["eobleft"],  self.screen, (128, 24), False),
				(tiles["horiznc"],  self.screen, (129, 24), False),
				(tiles["horiz"],    self.screen, (130, 24), False),
			], False)

		self.blocks["P20"] = Block(self, self.frame, "P20",
			[
				(tiles["horiznc"],  self.screen, (111, 26), False),
				(tiles["horiz"],    self.screen, (112, 26), False),
				(tiles["horiznc"],  self.screen, (113, 26), False),
				(tiles["horiz"],    self.screen, (114, 26), False),
				(tiles["horiznc"],  self.screen, (115, 26), False),
				(tiles["horiz"],    self.screen, (116, 26), False),
			], True)
		self.blocks["P20"].AddTrainLoc(self.screen, (114, 26))
		self.blocks["P20"].AddStoppingBlock([
				(tiles["horiznc"],  self.screen, (117, 26), False),
				(tiles["horiz"],    self.screen, (118, 26), False),
			], True)

		self.blocks["P21"] = Block(self, self.frame, "P21",
			[
				(tiles["eobleft"],  self.screen, (128, 26), False),
				(tiles["horiznc"],  self.screen, (129, 26), False),
				(tiles["horiz"],    self.screen, (130, 26), False),
				(tiles["horiznc"],  self.screen, (131, 26), False),
				(tiles["horiz"],    self.screen, (132, 26), False),
				(tiles["horiznc"],  self.screen, (133, 26), False),
				(tiles["horiz"],    self.screen, (134, 26), False),
				(tiles["horiznc"],  self.screen, (135, 26), False),
				(tiles["horiz"],    self.screen, (136, 26), False),
				(tiles["horiznc"],  self.screen, (137, 26), False),
				(tiles["horiz"],    self.screen, (138, 26), False),
				(tiles["horiznc"],  self.screen, (139, 26), False),
				(tiles["turnleftright"], self.screen, (140, 26), False),
				(tiles["diagleft"], self.screen, (141, 25), False),
				(tiles["diagleft"], self.screen, (142, 24), False),
				(tiles["diagleft"], self.screen, (143, 23), False),
				(tiles["diagleft"], self.screen, (144, 22), False),
				(tiles["diagleft"], self.screen, (145, 21), False),
				(tiles["diagleft"], self.screen, (146, 20), False),
				(tiles["diagleft"], self.screen, (147, 19), False),
				(tiles["diagleft"], self.screen, (148, 18), False),
				(tiles["turnleftleft"], self.screen, (149, 17), False),
				(tiles["horiz"],    self.screen, (150, 17), False),
				(tiles["horiznc"],  self.screen, (151, 17), False),
				(tiles["horiz"],    self.screen, (152, 17), False),
				(tiles["horiznc"],  self.screen, (153, 17), False),
				(tiles["horiz"],    self.screen, (154, 17), False),
				(tiles["horiznc"],  self.screen, (155, 17), False),
				(tiles["horiz"],    self.screen, (156, 17), False),
				(tiles["horiznc"],  self.screen, (157, 17), False),
				(tiles["horiz"],    self.screen, (158, 17), False),
				(tiles["horiz"],    LaKr, (0, 17), False),
				(tiles["horiznc"],  LaKr, (1, 17), False),
				(tiles["horiz"],    LaKr, (2, 17), False),
				(tiles["horiznc"],  LaKr, (3, 17), False),
				(tiles["horiz"],    LaKr, (4, 17), False),
			], True)
		self.blocks["P21"].AddTrainLoc(self.screen, (130, 26))
		self.blocks["P21"].AddTrainLoc(LaKr, (2, 17))
		self.blocks["P21"].AddStoppingBlock([
				(tiles["horiznc"],  LaKr, (5, 17), False),
				(tiles["horiz"],    LaKr, (6, 17), False),
				(tiles["eobright"], LaKr, (7, 17), False),
			], True)

		self.blocks["P30"] = Block(self, self.frame, "P30",
			[
				(tiles["turnrightup"],self.screen, (116, 29), False),
				(tiles["verticalnc"],self.screen, (116, 30), True),
				(tiles["vertical"],  self.screen, (116, 31), True),
				(tiles["turnleftdown"],self.screen, (116, 32), False),
			], False)
		self.blocks["P30"].AddTrainLoc(self.screen, (116, 30))
		self.blocks["P30"].AddStoppingBlock([
				(tiles["eobright"], self.screen, (118, 28), False),
				(tiles["turnleftleft"],self.screen, (117, 28), False),
			], False)
		self.blocks["P30"].AddStoppingBlock([
				(tiles["turnrightleft"],self.screen, (117, 33), False),
				(tiles["eobright"], self.screen, (118, 33), False),
			], True)

		self.blocks["P31"] = Block(self, self.frame, "P31",
			[
				(tiles["horiznc"],  self.screen, (129, 33), False),
				(tiles["horiz"],    self.screen, (130, 33), False),
				(tiles["horiznc"],  self.screen, (131, 33), False),
				(tiles["horiz"],    self.screen, (132, 33), False),
			], False)
		self.blocks["P31"].AddTrainLoc(self.screen, (131, 33))
		self.blocks["P31"].AddStoppingBlock([
				(tiles["eobleft"],  self.screen, (127, 33), False),
				(tiles["horiz"],    self.screen, (128, 33), False),
			], False)
		self.blocks["P31"].AddStoppingBlock([
				(tiles["horiznc"],  self.screen, (133, 33), False),
				(tiles["eobright"], self.screen, (134, 33), False),
			], True)

		self.blocks["P32"] = Block(self, self.frame, "P32",
			[
				(tiles["diagleft"], self.screen, (146, 31), False),
				(tiles["diagleft"], self.screen, (147, 30), False),
				(tiles["turnleftleft"], self.screen, (148, 29), False),
				(tiles["horiznc"],  self.screen, (149, 29), False),
				(tiles["horiz"],    self.screen, (150, 29), False),
				(tiles["horiznc"],  self.screen, (151, 29), False),
				(tiles["horiz"],    self.screen, (152, 29), False),
				(tiles["horiznc"],  self.screen, (153, 29), False),

				(tiles["horiznc"],  LaKr,        (113, 21), True),
				(tiles["horiz"],    LaKr,        (114, 21), True),
				(tiles["horiznc"],  LaKr,        (115, 21), True),
				(tiles["horiz"],    LaKr,        (116, 21), True),
				(tiles["horiznc"],  LaKr,        (117, 21), True),
				(tiles["horiz"],    LaKr,        (118, 21), True),
				(tiles["horiznc"],  LaKr,        (119, 21), True),
			], False)
		self.blocks["P32"].AddTrainLoc(self.screen, (149, 29))
		self.blocks["P32"].AddTrainLoc(LaKr, (113, 21))
		self.blocks["P32"].AddStoppingBlock([
				(tiles["eobleft"],  self.screen, (143, 33), False),
				(tiles["turnleftright"], self.screen, (144, 33), False),
				(tiles["diagleft"], self.screen, (145, 32), False),
			], False)
		self.blocks["P32"].AddStoppingBlock([
				(tiles["eobleft"],  LaKr,        (110, 21), False),
				(tiles["horiznc"],  LaKr,        (111, 21), True),
				(tiles["horiz"],    LaKr,        (112, 21), True),
			], True)

		self.blocks["P40"] = Block(self, self.frame, "P40",
			[
				(tiles["eobleft"],  self.screen, (112, 35), False),
				(tiles["horiznc"],  self.screen, (113, 35), False),
				(tiles["horiz"],    self.screen, (114, 35), False),
				(tiles["horiznc"],  self.screen, (115, 35), False),
				(tiles["horiz"],    self.screen, (116, 35), False),
			], False)
		self.blocks["P40"].AddTrainLoc(self.screen, (113, 35))
		self.blocks["P40"].AddStoppingBlock([
				(tiles["horiznc"],  self.screen, (117, 35), False),
				(tiles["eobright"], self.screen, (118, 35), False),
			], True)

		self.blocks["P41"] = Block(self, self.frame, "P41",
			[
				(tiles["horiz"],    self.screen, (130, 35), False),
				(tiles["horiznc"],  self.screen, (131, 35), False),
				(tiles["horiz"],    self.screen, (132, 35), False),
			], False)
		self.blocks["P41"].AddTrainLoc(self.screen, (131, 35))
		self.blocks["P41"].AddStoppingBlock([
				(tiles["eobleft"],  self.screen, (127, 35), False),
				(tiles["horiz"],    self.screen, (128, 35), False),
			], False)
		self.blocks["P41"].AddStoppingBlock([
				(tiles["horiznc"],  self.screen, (133, 35), False),
				(tiles["eobright"], self.screen, (134, 35), False),
			], True)

		self.blocks["P42"] = Block(self, self.frame, "P42",
			[
				(tiles["horiz"],    self.screen, (146, 35), False),
				(tiles["horiznc"],  self.screen, (147, 35), False),
				(tiles["horiz"],    self.screen, (148, 35), False),
				(tiles["horiz"],    self.screen, (150, 35), False),
				(tiles["horiznc"],  self.screen, (151, 35), False),
				(tiles["horiz"],    self.screen, (152, 35), False),
				(tiles["horiznc"],  self.screen, (153, 35), False),

				(tiles["horiznc"],  LaKr,        (109, 15), False),
				(tiles["horiz"],    LaKr,        (110, 15), False),
			], False)
		self.blocks["P42"].AddTrainLoc(self.screen, (151, 35))
		self.blocks["P42"].AddTrainLoc(LaKr, (109, 15))
		self.blocks["P42"].AddStoppingBlock([
				(tiles["eobleft"],  self.screen, (143, 35), False),
				(tiles["horiz"],    self.screen, (144, 35), False),
			], False)
		self.blocks["P42"].AddStoppingBlock([
				(tiles["horiznc"],  LaKr,        (111, 15), False),
				(tiles["horiz"],    LaKr,        (112, 15), False),
				(tiles["eobright"], LaKr,        (113, 15), False),
			], True)

		self.blocks["P50"] = Block(self, self.frame, "P50",
			[
				(tiles["horiznc"],  self.screen, (131, 22), True),
				(tiles["horiz"],    self.screen, (132, 22), True),
				(tiles["horiznc"],  self.screen, (133, 22), True),
				(tiles["horiz"],    self.screen, (134, 22), True),
				(tiles["horiznc"],  self.screen, (135, 22), True),
				(tiles["horiz"],    self.screen, (136, 22), True),
				(tiles["horiznc"],  self.screen, (137, 22), False),
				(tiles["turnleftright"],self.screen, (138, 22), False),
				(tiles["turnrightdown"],self.screen, (139, 21), False),
				(tiles["vertical"], self.screen, (139, 20), True),
				(tiles["verticalnc"], self.screen, (139, 19), True),
				(tiles["vertical"], self.screen, (139, 18), True),
				(tiles["verticalnc"], self.screen, (139, 17), True),
		], False)
		self.blocks["P50"].AddTrainLoc(self.screen, (131, 22))
		self.blocks["P50"].AddStoppingBlock([
				(tiles["eobleft"],  self.screen, (128, 22), False),
				(tiles["horiznc"],  self.screen, (129, 22), True),
				(tiles["horiz"],    self.screen, (130, 22), True),
			], False)
		self.blocks["P50"].AddStoppingBlock([
				(tiles["turnleftup"], self.screen, (139, 16), False),
				(tiles["turnrightright"], self.screen, (138, 15), False),
				(tiles["horiz"],    self.screen, (137, 15), False),
			], True)

		self.blocks["P60"] = Block(self, self.frame, "P60",
			[
				(tiles["houtline"],  self.screen, (108, 20), False),
				(tiles["houtline"],  self.screen, (109, 20), False),
				(tiles["houtline"],  self.screen, (110, 20), False),
				(tiles["houtline"],  self.screen, (111, 20), False),
				(tiles["houtline"],  self.screen, (112, 20), False),
				(tiles["houtline"],  self.screen, (113, 20), False),
				(tiles["houtline"],  self.screen, (114, 20), False),
				(tiles["houtline"],  self.screen, (115, 20), False),
			], True)

		self.blocks["P61"] = Block(self, self.frame, "P61",
			[
				(tiles["houtline"],  self.screen, (107, 22), False),
				(tiles["houtline"],  self.screen, (108, 22), False),
				(tiles["houtline"],  self.screen, (109, 22), False),
				(tiles["houtline"],  self.screen, (110, 22), False),
				(tiles["houtline"],  self.screen, (111, 22), False),
				(tiles["houtline"],  self.screen, (112, 22), False),
				(tiles["houtline"],  self.screen, (113, 22), False),
				(tiles["houtline"],  self.screen, (114, 22), False),
				(tiles["houtline"],  self.screen, (115, 22), False),
				(tiles["houtline"],  self.screen, (116, 22), False),
				(tiles["houtline"],  self.screen, (117, 22), False),
			], True)

		self.blocks["P62"] = Block(self, self.frame, "P62",
			[
				(tiles["houtline"],  self.screen, (110, 28), False),
				(tiles["houtline"],  self.screen, (111, 28), False),
				(tiles["houtline"],  self.screen, (112, 28), False),
			], True)

		self.blocks["P63"] = Block(self, self.frame, "P63",
			[
				(tiles["houtline"],  self.screen, (112, 30), False),
				(tiles["houtline"],  self.screen, (113, 30), False),
				(tiles["houtline"],  self.screen, (114, 30), False),
			], True)

		self.blocks["P64"] = Block(self, self.frame, "P64",
			[
				(tiles["houtline"],  self.screen, (113, 32), False),
			], True)

		self.blocks["POSCJ1"] = OverSwitch(self, self.frame, "POSCJ1",
			[
				(tiles["eobleft"],  self.screen, (135, 33), False),
				(tiles["horiznc"],  self.screen, (137, 33), False),
				(tiles["horiz"],    self.screen, (138, 33), False),
				(tiles["horiznc"],  self.screen, (139, 33), False),
				(tiles["horiz"],    self.screen, (140, 33), False),
				(tiles["eobright"], self.screen, (142, 33), False),
				(tiles["diagright"],self.screen, (137, 34), False),
				(tiles["horiz"],    self.screen, (140, 35), False),
				(tiles["horiznc"],  self.screen, (141, 35), False),
				(tiles["eobright"], self.screen, (142, 35), False),
			], False)

		self.blocks["POSCJ2"] = OverSwitch(self, self.frame, "POSCJ2",
			[
				(tiles["eobleft"],  self.screen, (135, 35), False),
				(tiles["horiz"],    self.screen, (136, 35), False),
				(tiles["horiznc"],  self.screen, (137, 35), False),
				(tiles["horiz"],    self.screen, (140, 35), False),
				(tiles["horiznc"],  self.screen, (141, 35), False),
				(tiles["eobright"], self.screen, (142, 35), False),
				(tiles["diagleft"], self.screen, (140, 34), False),
				(tiles["eobright"], self.screen, (142, 35), False),
			], False)

		self.blocks["POSSJ1"] = OverSwitch(self, self.frame, "POSSJ1",
			[
				(tiles["eobleft"],  self.screen, (119, 33), False),
				(tiles["horiz"],    self.screen, (120, 33), False),
				(tiles["horiznc"],  self.screen, (121, 33), False),
				(tiles["horiz"],    self.screen, (124, 33), False),
				(tiles["horiznc"],  self.screen, (125, 33), False),
				(tiles["eobright"], self.screen, (126, 33), False),
				(tiles["diagright"], self.screen, (124, 34), False),
				(tiles["eobright"], self.screen, (126, 35), False),
			], False)

		self.blocks["POSSJ2"] = OverSwitch(self, self.frame, "POSSJ2",
			[
				(tiles["eobleft"],  self.screen, (119, 35), False),
				(tiles["horiznc"],  self.screen, (121, 35), False),
				(tiles["horiz"],    self.screen, (122, 35), False),
				(tiles["horiznc"],  self.screen, (123, 35), False),
				(tiles["horiz"],    self.screen, (124, 35), False),
				(tiles["eobright"], self.screen, (126, 35), False),
				(tiles["diagleft"], self.screen, (121, 34), False),
				(tiles["horiz"],    self.screen, (124, 33), False),
				(tiles["horiznc"],  self.screen, (125, 33), False),
				(tiles["eobright"], self.screen, (126, 33), False),
			], False)

		self.blocks["POSPJ1"] = OverSwitch(self, self.frame, "POSPJ1",
			[
				(tiles["eobleft"],    self.screen, (115, 18), False),
				(tiles["turnrightright"], self.screen, (116, 18), False),
				(tiles["diagright"],  self.screen, (117, 19), False),
				(tiles["eobleft"],    self.screen, (116, 20), False),
				(tiles["horiz"],      self.screen, (117, 20), False),
				(tiles["diagright"],  self.screen, (119, 21), False),
				(tiles["eobleft"],    self.screen, (118, 22), False),
				(tiles["horiz"],      self.screen, (119, 22), False),
				(tiles["diagright"],  self.screen, (121, 23), False),
				(tiles["eobleft"],    self.screen, (119, 24), False),
				(tiles["horiznc"],    self.screen, (120, 24), False),
				(tiles["horiz"],      self.screen, (121, 24), False),

				(tiles["horiz"],      self.screen, (123, 24), False),
				(tiles["diagleft"],   self.screen, (125, 23), False),
				(tiles["turnleftleft"],self.screen, (126, 22), False),
				(tiles["eobright"],   self.screen, (127, 22), False),
				(tiles["horiz"],      self.screen, (125, 24), False),
				(tiles["horiznc"],    self.screen, (126, 24), False),
				(tiles["eobright"],   self.screen, (127, 24), False),
			], False)

		self.blocks["POSPJ2"] = OverSwitch(self, self.frame, "POSPJ2",
			[
				(tiles["eobleft"],    self.screen, (119, 26), False),
				(tiles["horiznc"],    self.screen, (120, 26), False),
				(tiles["horiz"],      self.screen, (121, 26), False),
				(tiles["eobleft"],    self.screen, (119, 28), False),
				(tiles["turnleftright"],self.screen, (120, 28), False),
				(tiles["diagleft"],   self.screen, (121, 27), False),
				(tiles["horiz"],      self.screen, (123, 26), False),
				(tiles["horiznc"],    self.screen, (124, 26), False),
				(tiles["horiz"],      self.screen, (125, 26), False),
				(tiles["horiznc"],    self.screen, (126, 26), False),
				(tiles["eobright"],    self.screen, (127, 26), False),

				(tiles["diagleft"],   self.screen, (125, 23), False),
				(tiles["diagleft"],   self.screen, (123, 25), False),
				(tiles["turnleftleft"],self.screen, (126, 22), False),
				(tiles["eobright"],   self.screen, (127, 22), False),
				(tiles["horiz"],      self.screen, (125, 24), False),
				(tiles["horiznc"],    self.screen, (126, 24), False),
				(tiles["eobright"],   self.screen, (127, 24), False),
			], False)

		self.blocks["POSSP1"] = OverSwitch(self, self.frame, "POSSP1",
			[
				(tiles["eobleft"],    self.screen, (98, 20), False),
				(tiles["diagleft"],   self.screen, (100, 19), False),
				(tiles["turnleftleft"],self.screen, (101, 18), False),
				(tiles["horiznc"],    self.screen, (102, 18), False),
				(tiles["horiz"],      self.screen, (102, 18), False),
				(tiles["horiznc"],    self.screen, (103, 18), False),
				(tiles["horiznc"],    self.screen, (105, 18), False),
				(tiles["horiz"],      self.screen, (106, 18), False),
				(tiles["eobright"],   self.screen, (107, 18), False),
				(tiles["diagright"],  self.screen, (105, 19), False),
				(tiles["turnrightleft"],self.screen, (106, 20), False),
				(tiles["eobright"],   self.screen, (107, 20), False),
				(tiles["horiznc"],    self.screen, (101, 20), False),
				(tiles["horiz"],      self.screen, (102, 20), False),
				(tiles["turnrightright"],self.screen, (103, 20), False),
				(tiles["diagright"],  self.screen, (104, 21), False),
				(tiles["turnrightleft"],self.screen, (105, 22), False),
				(tiles["eobright"],   self.screen, (106, 22), False),
			], True)

		self.blocks["POSSP2"] = OverSwitch(self, self.frame, "POSSP2",
			[
				(tiles["eobleft"],    self.screen, (98, 20), False),
				(tiles["diagright"],  self.screen, (101, 21), False),
				(tiles["eobleft"],    self.screen, (100, 22), False),
				(tiles["horiznc"],    self.screen, (101, 22), False),
				(tiles["diagright"],  self.screen, (103, 23), False),
				(tiles["eobleft"],    self.screen, (102, 24), False),
				(tiles["horiznc"],    self.screen, (103, 24), False),

				(tiles["horiznc"],    self.screen, (105, 24), False),
				(tiles["horiz"],      self.screen, (106, 24), False),
				(tiles["horiznc"],    self.screen, (107, 24), False),
				(tiles["horiz"],      self.screen, (108, 24), False),

				(tiles["eobleft"],    self.screen, (102, 26), False),
				(tiles["horiznc"],    self.screen, (103, 26), False),
				(tiles["horiz"],      self.screen, (104, 26), False),
				(tiles["horiznc"],    self.screen, (105, 26), False),
				(tiles["diagleft"],   self.screen, (108, 25), False),

				(tiles["eobleft"],    self.screen, (101, 28), False),
				(tiles["horiz"],      self.screen, (102, 28), False),
				(tiles["horiz"],      self.screen, (104, 28), False),
				(tiles["diagleft"],   self.screen, (106, 27), False),

				(tiles["eobleft"],    self.screen, (100, 30), False),
				(tiles["horiznc"],    self.screen, (101, 30), False),
				(tiles["horiz"],      self.screen, (102, 30), False),

				(tiles["eobleft"],    self.screen, (100, 32), False),
				(tiles["turnleftright"],self.screen, (101, 32), False),
				(tiles["diagleft"],   self.screen, (102, 31), False),

				(tiles["eobright"],   self.screen, (110, 24), False),
			], True)

		self.blocks["POSSP3"] = OverSwitch(self, self.frame, "POSSP3",
			[
				(tiles["eobleft"],    self.screen, (98, 20), False),
				(tiles["diagright"],  self.screen, (101, 21), False),
				(tiles["eobleft"],    self.screen, (100, 22), False),
				(tiles["horiznc"],    self.screen, (101, 22), False),
				(tiles["diagright"],  self.screen, (103, 23), False),
				(tiles["eobleft"],    self.screen, (102, 24), False),
				(tiles["horiznc"],    self.screen, (103, 24), False),
				(tiles["diagright"],  self.screen, (105, 25), False),

				(tiles["eobleft"],    self.screen, (102, 26), False),
				(tiles["horiznc"],    self.screen, (103, 26), False),
				(tiles["horiz"],      self.screen, (104, 26), False),
				(tiles["horiznc"],    self.screen, (105, 26), False),

				(tiles["eobleft"],    self.screen, (101, 28), False),
				(tiles["horiz"],      self.screen, (102, 28), False),
				(tiles["horiz"],      self.screen, (104, 28), False),
				(tiles["diagleft"],   self.screen, (106, 27), False),

				(tiles["eobleft"],    self.screen, (100, 30), False),
				(tiles["horiznc"],    self.screen, (101, 30), False),
				(tiles["horiz"],      self.screen, (102, 30), False),

				(tiles["eobleft"],    self.screen, (100, 32), False),
				(tiles["turnleftright"],self.screen, (101, 32), False),
				(tiles["diagleft"],   self.screen, (102, 31), False),

				(tiles["horiz"],      self.screen, (108, 26), False),
				(tiles["horiznc"],    self.screen, (109, 26), False),
				(tiles["eobright"],   self.screen, (110, 26), False),
			], True)

		self.blocks["POSSP4"] = OverSwitch(self, self.frame, "POSSP4",
			[
				(tiles["eobleft"],    self.screen, (101, 28), False),
				(tiles["horiz"],      self.screen, (102, 28), False),
				(tiles["horiz"],      self.screen, (104, 28), False),

				(tiles["eobleft"],    self.screen, (100, 30), False),
				(tiles["horiznc"],    self.screen, (101, 30), False),
				(tiles["horiz"],      self.screen, (102, 30), False),

				(tiles["eobleft"],    self.screen, (100, 32), False),
				(tiles["turnleftright"],self.screen, (101, 32), False),
				(tiles["diagleft"],   self.screen, (102, 31), False),

				(tiles["horiz"],      self.screen, (106, 28), False),
				(tiles["horiz"],      self.screen, (108, 28), False),
				(tiles["eobright"],   self.screen, (109, 28), False),

				(tiles["diagright"],  self.screen, (108, 29), False),
				(tiles["horiz"],      self.screen, (110, 30), False),
				(tiles["eobright"],   self.screen, (111, 30), False),

				(tiles["diagright"],  self.screen, (110, 31), False),
				(tiles["turnrightleft"],self.screen, (111, 32), False),
				(tiles["eobright"],   self.screen, (112, 32), False),
			], True)

		self.blocks["POSSP5"] = OverSwitch(self, self.frame, "POSSP5",
			[
				(tiles["eobleft"],    self.screen, (101, 28), False),
				(tiles["horiz"],      self.screen, (102, 28), False),

				(tiles["eobleft"],    self.screen, (100, 30), False),
				(tiles["horiznc"],    self.screen, (101, 30), False),
				(tiles["horiz"],      self.screen, (102, 30), False),
				(tiles["horiz"],      self.screen, (104, 30), False),

				(tiles["eobleft"],    self.screen, (100, 32), False),
				(tiles["turnleftright"],self.screen, (101, 32), False),
				(tiles["diagleft"],   self.screen, (102, 31), False),

				(tiles["diagright"],  self.screen, (106, 31), False),
				(tiles["diagright"],  self.screen, (107, 32), False),
				(tiles["diagright"],  self.screen, (108, 33), False),
				(tiles["diagright"],  self.screen, (109, 34), False),
				(tiles["turnrightleft"],self.screen, (110, 35), False),
				(tiles["eobright"],   self.screen, (111, 35), False),
			], True)

		self.osBlocks["POSCJ1"] = [ "P31", "P32", "P42" ]
		self.osBlocks["POSCJ2"] = [ "P41", "P32", "P42" ]
		self.osBlocks["POSSJ1"] = [ "P30", "P31", "P41" ]
		self.osBlocks["POSSJ2"] = [ "P40", "P31", "P41" ]
		self.osBlocks["POSPJ1"] = [ "P50", "P11", "V11", "P60", "P61", "P10" ]
		self.osBlocks["POSPJ2"] = [ "P50", "P11", "P21", "P20", "P30" ]
		self.osBlocks["POSSP1"] = [ "P7", "V10", "P60", "P61"]
		self.osBlocks["POSSP2"] = [ "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P10"]
		self.osBlocks["POSSP3"] = [ "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P20"]
		self.osBlocks["POSSP4"] = [ "P1", "P2", "P3", "P62", "P63", "P64"]
		self.osBlocks["POSSP5"] = [ "P1", "P2", "P3", "P40"]

		return self.blocks, self.osBlocks

	def DefineTurnouts(self, tiles, blocks):
		self.turnouts = {}
		toList = [
			[ "PBSw1",   "toleftleft",   ["POSSJ1", "POSSJ2"], (122, 33) ],
			[ "PBSw1b",  "toleftright",  ["POSSJ1", "POSSJ2"], (120, 35) ],
			[ "PBSw3",   "torightright", ["POSSJ1", "POSSJ2"], (123, 33) ],
			[ "PBSw3b",  "torightleft",  ["POSSJ1", "POSSJ2"], (125, 35) ],
			[ "PBSw11",  "torightright", ["POSCJ1", "POSCJ2"], (136, 33) ],
			[ "PBSw11b", "torightleft",  ["POSCJ1", "POSCJ2"], (138, 35) ],
			[ "PBSw13",  "toleftright",  ["POSCJ1", "POSCJ2"], (139, 35) ],
			[ "PBSw13b", "toleftleft",   ["POSCJ1", "POSCJ2"], (141, 33) ],

			[ "PBSw5",   "torightright", ["P41"], (129, 35) ],
			[ "PBSw15a", "toleftright",  ["P42"], (145, 35) ],
			[ "PBSw15b", "toleftleft",   ["P42"], (149, 35) ],

			[ "PASw27",  "toleftup",     ["POSPJ1"], (118, 20) ],
			[ "PASw29",  "toleftup",     ["POSPJ1"], (120, 22) ],
			[ "PASw31",  "torightleft",  ["POSPJ1"], (122, 24) ],
			[ "PASw37",  "toleftright",  ["POSPJ1", "POSPJ2"], None ],

			[ "PASw3",   "torightright", ["POSSP2", "POSSP3", "POSSP4", "POSSP5"], (103, 28) ],
			[ "PASw7b",  "toleftleft",   ["POSSP2", "POSSP3"], (109, 24) ],
			[ "PASw9",   "toleftup",     ["POSSP2", "POSSP3", "POSSP4", "POSSP5"], (105, 30) ],
			[ "PASw11",  "torightright", ["POSSP4"], (107, 28) ],
			[ "PASw13",  "toleftdown",   ["POSSP4"], (109, 30) ],
			[ "PASw15",  "toleftright",  ["POSSP1", "POSSP2", "POSSP3"], (99, 20) ],
			[ "PASw17",  "torightright", ["POSSP1"], (108, 18) ],
			[ "PASw19",  "torightright", ["POSSP1", "POSSP2", "POSSP3"], (100, 20) ],
			[ "PASw19b", "torightleft",  ["POSSP1", "POSSP2", "POSSP3"], (102, 22) ],
			[ "PASw21",  "toleftup",     ["POSSP2", "POSSP3"], None ],
		]

		for tonm, tileSet, blks, pos in toList:
			trnout = Turnout(self, self.frame, tonm, self.screen, tiles[tileSet], pos)
			for blknm in blks:
				blocks[blknm].AddTurnout(trnout)
				trnout.AddBlock(blknm)
			#  TODO
			# trnout.SetDisabled(True)
			self.turnouts[tonm] = trnout

		trnout = SlipSwitch(self, self.frame, "PASw35", self.screen, tiles["ssright"], (124, 24))
		blocks["POSPJ1"].AddTurnout(trnout)
		blocks["POSPJ2"].AddTurnout(trnout)
		trnout.AddBlock("POSPJ1")
		trnout.AddBlock("POSPJ2")
		trnout.SetControllers(None, self.turnouts["PASw37"])
		#  TODO
		# trnout.SetDisabled(True)
		self.turnouts["PASw35"] = trnout

		trnout = SlipSwitch(self, self.frame, "PASw33", self.screen, tiles["ssright"], (122, 26))
		blocks["POSPJ2"].AddTurnout(trnout)
		trnout.AddBlock("POSPJ2")
		trnout.SetControllers(None, self.turnouts["PASw35"])
		#  TODO
		# trnout.SetDisabled(True)
		self.turnouts["PASw33"] = trnout

		self.turnouts["PBSw1"].SetPairedTurnout(self.turnouts["PBSw1b"])
		self.turnouts["PBSw3"].SetPairedTurnout(self.turnouts["PBSw3b"])
		self.turnouts["PBSw11"].SetPairedTurnout(self.turnouts["PBSw11b"])
		self.turnouts["PBSw13"].SetPairedTurnout(self.turnouts["PBSw13b"])
		self.turnouts["PASw19"].SetPairedTurnout(self.turnouts["PASw19b"])

		trnout = SlipSwitch(self, self.frame, "PASw23", self.screen, tiles["ssleft"], (104, 24))
		for b in ["POSSP2", "POSSP3"]:
			blocks[b].AddTurnout(trnout)
			trnout.AddBlock(b)
		trnout.SetControllers(None, self.turnouts["PASw21"])
		#  TODO
		# trnout.SetDisabled(True)
		self.turnouts["PASw23"] = trnout

		trnout = SlipSwitch(self, self.frame, "PASw7", self.screen, tiles["ssright"], (107, 26))
		for b in ["POSSP2", "POSSP3"]:
			blocks[b].AddTurnout(trnout)
			trnout.AddBlock(b)
		trnout.SetControllers(None, self.turnouts["PASw7b"])
		#  TODO
		# trnout.SetDisabled(True)
		self.turnouts["PASw7"] = trnout

		trnout = SlipSwitch(self, self.frame, "PASw5", self.screen, tiles["ssright"], (105, 28))
		for b in ["POSSP2", "POSSP3", "POSSP4"]:
			blocks[b].AddTurnout(trnout)
			trnout.AddBlock(b)
		trnout.SetControllers(None, self.turnouts["PASw7"])
		#  TODO
		# trnout.SetDisabled(True)
		self.turnouts["PASw5"] = trnout

		trnout = SlipSwitch(self, self.frame, "PASw1", self.screen, tiles["ssright"], (103, 30))
		for b in ["POSSP2", "POSSP3", "POSSP4", "POSSP5"]:
			blocks[b].AddTurnout(trnout)
			trnout.AddBlock(b)
		trnout.SetControllers(None, self.turnouts["PASw5"])
		#  TODO
		# trnout.SetDisabled(True)
		self.turnouts["PASw1"] = trnout

		return self.turnouts

	def DefineSignals(self, tiles):
		self.signals = {}
		sigList = [
			[ "PA32RA", RegAspects, True,    "rightlong", (119, 27) ],
			[ "PA32RB", RegAspects, True,    "rightlong", (119, 29) ],
			[ "PA32L",  RegAspects, False,   "left",      (127, 25) ],

			[ "PA34RA", RegAspects, True,    "right",     (115, 19) ],
			[ "PA34RB", RegAspects, True,    "right",     (116, 21) ],
			[ "PA34RC", RegAspects, True,    "right",     (118, 23) ],
			[ "PA34RD", RegAspects, True,    "rightlong", (119, 25) ],
			[ "PA34LA", RegAspects, False,   "leftlong",  (127, 21) ],
			[ "PA34LB", RegAspects, False,   "leftlong",  (127, 23) ],

			[ "PB2R",   RegAspects, True,    "rightlong", (119, 36) ],
			[ "PB2L",   RegAspects, False,   "leftlong",  (126, 34) ],

			[ "PB4R",   RegAspects, True,    "rightlong", (119, 34) ],
			[ "PB4L",   RegAspects, False,   "leftlong",  (126, 32) ],

			[ "PB14R",  RegAspects, True,    "rightlong", (135, 34) ],
			[ "PB14L",  RegAspects, False,   "leftlong",  (142, 32) ],

			[ "PB12R",  RegAspects, True,    "rightlong", (135, 36) ],
			[ "PB12L",  RegAspects, False,   "leftlong",  (142, 34) ],
		]
		for signm, atype, east, tileSet, pos in sigList:
			sig  = Signal(self, self.screen, self.frame, signm, atype, east, pos, tiles[tileSet])
			#  TODO
			# sig.SetDisabled(True)
			self.signals[signm]  = sig

		blockSigs = {
			# which signals govern stopping sections, west and east
			"P10": (None,     "P34RD"),
			"P11": ("PB34LB", "L6RB"),
			"P20": (None,     "P32RA"),
			"P21": (None,     "L4R"),
			"P31": ("PB4L",   "PB14R"),
			"P41": ("PB2L",   "PB12R"),
			"P32": ("PB14L",  "S4LC"),
			"P42": ("PB12L",  "S16R"),
			"P30": ("P32RB",  "PB4R"),
			"P40": (None,     "PB2R"),
			"P50": ("PB4LA",  "P34LA")
		}

		for blknm, siglist in blockSigs.items():
			self.blocks[blknm].SetSignals(siglist)

		self.routes = {}
		self.osSignals = {}

		# routes for circus junction
		block = self.blocks["POSCJ1"]
		self.routes["PRtP31P32"] = Route(self.screen, block, "PRtP31P32", "P32", [ (135, 33), (136, 33), (137, 33), (138, 33), (139, 33), (140, 33), (141, 33), (142, 33) ], "P31", [MAIN, MAIN], ["PBSw11", "PBSw13"], ["PB14R", "PB14L"])
		self.routes["PRtP31P42"] = Route(self.screen, block, "PRtP31P42", "P42", [ (135, 33), (136, 33), (137, 34), (138, 35), (139, 35), (140, 35), (141, 35), (142, 35) ], "P31", [DIVERGING, DIVERGING], ["PBSw11", "PBSw13"], ["PB14R", "PB12L"])

		block = self.blocks["POSCJ2"]
		self.routes["PRtP41P32"] = Route(self.screen, block, "PRtP41P32", "P32", [ (135, 35), (136, 35), (137, 35), (138, 35), (139, 35), (140, 34), (141, 33), (142, 33) ], "P41", [DIVERGING, DIVERGING], ["PBSw11", "PBSw13"], ["PB12R", "PB14L"])
		self.routes["PRtP41P42"] = Route(self.screen, block, "PRtP41P42", "P42", [ (135, 35), (136, 35), (137, 35), (138, 35), (139, 35), (140, 35), (141, 35), (142, 35) ], "P41", [MAIN, MAIN], ["PBSw11", "PBSw13"], ["PB12R", "PB12L"])

		self.signals["PB14R"].AddPossibleRoutes("POSCJ1", [ "PRtP31P32", "PRtP31P42" ])
		self.signals["PB14L"].AddPossibleRoutes("POSCJ1", [ "PRtP31P32" ])
		self.signals["PB14L"].AddPossibleRoutes("POSCJ2", [ "PRtP41P32" ])
		self.signals["PB12R"].AddPossibleRoutes("POSCJ2", [ "PRtP41P32", "PRtP41P42" ])
		self.signals["PB12L"].AddPossibleRoutes("POSCJ1", [ "PRtP31P42" ])
		self.signals["PB12L"].AddPossibleRoutes("POSCJ2", [ "PRtP41P42" ])

		self.osSignals["POSCJ1"] = [ "PB14R", "PB14L", "PB12L" ]
		self.osSignals["POSCJ2"] = [ "PB12R", "PB12L", "PB14L" ]

		# routes for south junction
		block = self.blocks["POSSJ1"]
		self.routes["PRtP30P31"] = Route(self.screen, block, "PRtP30P31", "P31", [ (119, 33), (120, 33), (121, 33), (122, 33), (123, 33), (124, 33), (125, 33), (126, 33) ], "P30", [DIVERGING, MAIN], ["PBSw1", "PBSw3"], ["PB4R", "PB4L"])
		self.routes["PRtP30P41"] = Route(self.screen, block, "PRtP30P41", "P41", [ (119, 33), (120, 33), (121, 33), (122, 33), (123, 33), (124, 34), (125, 35), (126, 35) ], "P30", [DIVERGING, DIVERGING], ["PBSw1", "PBSw3"], ["PB4R", "PB2L"])

		block = self.blocks["POSSJ2"]
		self.routes["PRtP40P31"] = Route(self.screen, block, "PRtP40P31", "P31", [ (119, 35), (120, 35), (121, 34), (122, 33), (123, 33), (124, 33), (125, 33), (126, 33) ], "P40", [DIVERGING, DIVERGING], ["PBSw1", "PBSw1"], ["PB2R", "PB4L"])
		self.routes["PRtP40P41"] = Route(self.screen, block, "PRtP40P41", "P41", [ (119, 35), (120, 35), (121, 35), (122, 35), (123, 35), (124, 35), (125, 35), (126, 35) ], "P40", [MAIN, MAIN], ["PBSw1", "PBSw3"], ["PB2R", "PB2L"])

		self.signals["PB4R"].AddPossibleRoutes("POSSJ1", [ "PRtP30P31", "PRtP30P41" ])
		self.signals["PB4L"].AddPossibleRoutes("POSSJ1", [ "PRtP30P31" ])
		self.signals["PB4L"].AddPossibleRoutes("POSSJ2", [ "PRtP40P31" ])
		self.signals["PB2R"].AddPossibleRoutes("POSSJ2", [ "PRtP40P31", "PRtP40P41" ])
		self.signals["PB2L"].AddPossibleRoutes("POSSJ1", [ "PRtP30P41" ])
		self.signals["PB2L"].AddPossibleRoutes("POSSJ2", [ "PRtP40P41" ])

		self.osSignals["POSSJ1"] = [ "PB4R", "PB4L", "PB2L" ]
		self.osSignals["POSSJ2"] = [ "PB2R", "PB2L", "PB4L" ]

		# routes for parsons junction
		block = self.blocks["POSPJ1"]
		self.routes["PRtV11P50"] = Route(self.screen, block, "PRtV11P50", "P50",
					[ (115, 18), (116, 18), (117, 19), (118, 20), (119, 21), (120, 22), (121, 23), (122, 24), (123, 24), (124, 24), (125, 23), (126, 22), (127, 22) ],
					"V11", [RESTRICTING, RESTRICTING], ["PASw27", "PASw29", "PASw31", "PASw35", "PASw37"], ["PA34RA", "PA34LA"])
		self.routes["PRtP60P50"] = Route(self.screen, block, "PRtP60P50", "P50",
					[ (116, 20), (117, 20), (118, 20), (119, 21), (120, 22), (121, 23), (122, 24), (123, 24), (124, 24), (125, 23), (126, 22), (127, 22) ],
					"P60", [RESTRICTING, RESTRICTING], ["PASw27", "PASw29", "PASw31", "PASw35", "PASw37"], ["PA34RB", "PA34LA"])
		self.routes["PRtP61P50"] = Route(self.screen, block, "PRtP61P50", "P50",
					[ (118, 22), (119, 22), (120, 22), (121, 23), (122, 24), (123, 24), (124, 24), (125, 23), (126, 22), (127, 22) ],
					"P61", [RESTRICTING, RESTRICTING], ["PASw29", "PASw31", "PASw35", "PASw37"], ["PA34RC", "PA34LA"])
		self.routes["PRtP10P50"] = Route(self.screen, block, "PRtP10P50", "P50",
					[ (119, 24), (120, 24), (121, 24), (122, 24), (123, 24), (124, 24), (125, 23), (126, 22), (127, 22) ],
					"P10", [DIVERGING, DIVERGING], ["PASw31", "PASw35", "PASw37"], ["PA34RD", "PA34LA"])
		self.routes["PRtV11P11"] = Route(self.screen, block, "PRtV11P11", "P11",
					[ (115, 18), (116, 18), (117, 19), (118, 20), (119, 21), (120, 22), (121, 23), (122, 24), (123, 24), (124, 24), (125, 24), (126, 24), (127, 24) ],
					"V11", [RESTRICTING, RESTRICTING], ["PASw27", "PASw29", "PASw31", "PASw35", "PASw37"], ["PA34RA", "PA34LB"])
		self.routes["PRtP60P11"] = Route(self.screen, block, "PRtP60P11", "P11",
					[ (116, 20), (117, 20), (118, 20), (119, 21), (120, 22), (121, 23), (122, 24), (123, 24), (124, 24), (125, 24), (126, 24), (127, 24) ],
					"P60", [RESTRICTING, RESTRICTING], ["PASw27", "PASw29", "PASw31", "PASw35", "PASw37"], ["PA34RB", "PA34LB"])
		self.routes["PRtP61P11"] = Route(self.screen, block, "PRtP61P11", "P11",
					[ (118, 22), (119, 22), (120, 22), (121, 23), (122, 24), (123, 24), (124, 24), (125, 24), (126, 24), (127, 24) ],
					"P61", [RESTRICTING, RESTRICTING], ["PASw29", "PASw31", "PASw35", "PASw37"], ["PA34RC", "PA34LB"])
		self.routes["PRtP10P11"] = Route(self.screen, block, "PRtP10P11", "P11",
					[ (119, 24), (120, 24), (121, 24), (122, 24), (123, 24), (124, 24), (125, 24), (126, 24), (127, 24) ],
					"P10", [RESTRICTING, MAIN], ["PASw31", "PASw35", "PASw37"], ["PA34RD", "PA34LB"])

		block = self.blocks["POSPJ2"]
		self.routes["PRtP20P50"] = Route(self.screen, block, "PRtP20P50", "P50",
					[ (119, 26), (120, 26), (121, 26), (122, 26), (123, 25), (124, 24), (125, 23), (126, 22), (127, 22) ],
					"P20", [DIVERGING, RESTRICTING], ["PASw33", "PASw35", "PASw37"], ["PA32RA", "PA34LA"])
		self.routes["PRtP30P50"] = Route(self.screen, block, "PRtP30P50", "P50",
					[ (119, 28), (120, 28), (121, 27), (122, 26), (123, 25), (124, 24), (125, 23), (126, 22), (127, 22) ],
					"P30", [MAIN, MAIN], ["PASw33", "PASw35", "PASw37"], ["PA32RB", "PA34LA"])
		self.routes["PRtP20P11"] = Route(self.screen, block, "PRtP20P11", "P11",
					[ (119, 26), (120, 26), (121, 26), (122, 26), (123, 25), (124, 24), (125, 24), (126, 24), (127, 24) ],
					"P20", [RESTRICTING, RESTRICTING], ["PASw33", "PASw35", "PASw37"], ["PA32RA", "PA34LB"])
		self.routes["PRtP30P11"] = Route(self.screen, block, "PRtP30P11", "P11",
					[ (119, 28), (120, 28), (121, 27), (122, 26), (123, 25), (124, 24), (125, 24), (126, 24), (127, 24) ],
					"P30", [RESTRICTING, DIVERGING], ["PASw33", "PASw35", "PASw37"], ["PA32RB", "PA34LB"])
		self.routes["PRtP20P21"] = Route(self.screen, block, "PRtP20P21", "P21",
					[ (119, 26), (120, 26), (121, 26), (122, 26), (123, 26), (124, 26), (125, 26), (126, 26), (127, 26) ],
					"P20", [MAIN, RESTRICTING], ["PASw33", "PASw35"], ["PA32RA", "PA32L"])
		self.routes["PRtP30P21"] = Route(self.screen, block, "PRtP30P21", "P21",
					[ (119, 28), (120, 28), (121, 27), (122, 26), (123, 26), (124, 26), (125, 26), (126, 26), (127, 26) ],
					"P30", [DIVERGING, RESTRICTING], ["PASw33", "PASw35"], ["PA32RB", "PA32L"])

		self.signals["PA34RA"].AddPossibleRoutes("POSPJ1", [ "PRtV11P50", "PRtV11P11" ])
		self.signals["PA34RB"].AddPossibleRoutes("POSPJ1", [ "PRtP60P50", "PRtP60P11" ])
		self.signals["PA34RC"].AddPossibleRoutes("POSPJ1", [ "PRtP61P50", "PRtP61P11" ])
		self.signals["PA34RD"].AddPossibleRoutes("POSPJ1", [ "PRtP10P50", "PRtP10P11" ])
		self.signals["PA32RA"].AddPossibleRoutes("POSPJ2", [ "PRtP20P50", "PRtP20P11", "PRtP20P21" ])
		self.signals["PA32RB"].AddPossibleRoutes("POSPJ2", [ "PRtP30P50", "PRtP30P11", "PRtP30P21" ])

		self.signals["PA34LA"].AddPossibleRoutes("POSPJ1", [ "PRtV11P50", "PRtP60P50", "PRtP61P50", "PRtP10P50" ])
		self.signals["PA34LA"].AddPossibleRoutes("POSPJ2", [ "PRtP20P50", "PRtP30P50" ])
		self.signals["PA34LB"].AddPossibleRoutes("POSPJ1", [ "PRtV11P11", "PRtP60P11", "PRtP61P11", "PRtP10P11" ])
		self.signals["PA34LB"].AddPossibleRoutes("POSPJ2", [ "PRtP20P11", "PRtP30P11" ])
		self.signals["PA32L"].AddPossibleRoutes("POSPJ2", [ "PRtP20P21", "PRtP30P21" ])

		self.osSignals["POSPJ1"] = [ "PA34RA", "PA34RB", "PA34RC", "PA34RD", "PA34LA", "PA34LB" ]
		self.osSignals["POSPJ2"] = [ "PA32RA", "PA32RB", "PA32L", "PA34LA", "PA34LB" ]

		# routes for southport
		block = self.blocks["POSSP1"]
		self.routes["PRtP7V10"] = Route(self.screen, block, "PRtP7V10", "P7",
					[ (98, 20), (99, 20), (100, 19), (101, 18), (102, 18), (103, 18), (104, 18), (105, 18), (106, 18), (107, 18) ],
					"V10", [RESTRICTING, RESTRICTING], ["PASw15", "PASw17"], ["PA12R", "PA12LA"])
		self.routes["PRtP7P60"] = Route(self.screen, block, "PRtP7P60", "P7",
					[ (98, 20), (99, 20), (100, 19), (101, 18), (102, 18), (103, 18), (104, 18), (105, 19), (106, 20), (107, 20) ],
					"P60", [RESTRICTING, RESTRICTING], ["PASw15", "PASw17"], ["PA12R", "PA12LB"])
		self.routes["PRtP7P61"] = Route(self.screen, block, "PRtP7P61", "P7",
					[ (98, 20), (99, 20), (100, 20), (101, 20), (102, 20), (103, 20), (104, 21), (105, 22), (106, 22) ],
					"P61", [RESTRICTING, RESTRICTING], ["PASw15", "PASw19"], ["PA12R", "PA12LC"])

		block = self.blocks["POSSP2"]
		self.routes["PRtP7P10"] = Route(self.screen, block, "PRtP7P10", "P7",
					[ (98, 20), (99, 20), (100, 20), (101, 21), (102, 22), (103, 23), (104, 24), (105, 24), (106, 24), (107, 24), (108, 24), (109, 24), (110, 24) ],
					"P10", [SLOW, SLOW], ["PASw7", "PASw15", "PASw19", "PASw21", "PASw23"], ["PA12R", "PA10L"])
		self.routes["PRtP6P10"] = Route(self.screen, block, "PRtP6P10", "P6",
					[ (100, 22), (101, 22), (102, 22), (103, 23), (104, 24), (105, 24), (106, 24), (107, 24), (108, 24), (109, 24), (110, 24) ],
					"P10", [SLOW, RESTRICTING], ["PASw7", "PASw19", "PASw21", "PASw23"], ["PA10RA", "PA10L"])
		self.routes["PRtP5P10"] = Route(self.screen, block, "PRtP5P10", "P5",
					[ (102, 24), (103, 24), (104, 24), (105, 24), (106, 24), (107, 24), (108, 24), (109, 24), (110, 24) ],
					"P10", [SLOW, SLOW], ["PASw7", "PASw21", "PASw23"], ["PA10RB", "PA10L"])
		self.routes["PRtP4P10"] = Route(self.screen, block, "PRtP4P10", "P4",
					[ (102, 26), (103, 26), (104, 26), (105, 26), (106, 26), (107, 26), (108, 25), (109, 24), (110, 24) ],
					"P10", [SLOW, SLOW], ["PASw5", "PASw7", "PASw23"], ["PA8R", "PA10L"])
		self.routes["PRtP3P10"] = Route(self.screen, block, "PRtP3P10", "P3",
					[ (101, 28), (102, 28), (103, 28), (104, 28), (105, 28), (106, 27), (107, 26), (108, 25), (109, 24), (110, 24) ],
					"P10", [SLOW, SLOW], ["PASw3", "PASw5", "PASw7", "PASw9"], ["PA6R", "PA10L"])
		self.routes["PRtP2P10"] = Route(self.screen, block, "PRtP2P10", "P2",
					[ (100, 30), (101, 30), (102, 30), (103, 30), (104, 29), (105, 28), (106, 27), (107, 26), (108, 25), (109, 24), (110, 24) ],
					"P10", [SLOW, SLOW], ["PASw1", "PASw3", "PASw5", "PASw7", "PASw9"], ["PA4RA", "PA10L"])
		self.routes["PRtP1P10"] = Route(self.screen, block, "PRtP1P10", "P1",
					[ (100, 32), (101, 32), (102, 31), (103, 30), (104, 29), (105, 28), (106, 27), (107, 26), (108, 25), (109, 24), (110, 24) ],
					"P10", [SLOW, RESTRICTING], ["PASw1", "PASw3", "PASw5", "PASw7", "PASw9"], ["PA4RB", "PA10L"])

		block = self.blocks["POSSP3"]
		self.routes["PRtP7P20"] = Route(self.screen, block, "PRtP7P20", "P7",
					[ (98, 20), (99, 20), (100, 20), (101, 21), (102, 22), (103, 23), (104, 24), (105, 25), (106, 26), (107, 26), (108, 26), (109, 26), (110, 26) ],
					"P20", [SLOW, RESTRICTING], ["PASw5", "PASw7", "PASw15", "PASw19", "PASw21", "PASw23"], ["PA12R", "PA8L"])
		self.routes["PRtP6P20"] = Route(self.screen, block, "PRtP6P20", "P6",
					[ (100, 22), (101, 22), (102, 22), (103, 23), (104, 24), (105, 25), (106, 26), (107, 26), (108, 26), (109, 26), (110, 26) ],
					"P20", [SLOW, RESTRICTING], ["PASw5", "PASw7", "PASw19", "PASw21", "PASw23"], ["PA10RA", "PA8L"])
		self.routes["PRtP5P20"] = Route(self.screen, block, "PRtP5P20", "P5",
					[ (102, 24), (103, 24), (104, 24), (105, 24), (106, 25), (107, 26), (108, 26), (109, 26), (110, 26) ],
					"P20", [SLOW, RESTRICTING], ["PASw5", "PASw7", "PASw21", "PASw23"], ["PA10RB", "PA8L"])
		self.routes["PRtP4P20"] = Route(self.screen, block, "PRtP4P20", "P4",
					[ (102, 26), (103, 26), (104, 26), (105, 26), (106, 26), (107, 26), (108, 26), (109, 26), (110, 26) ],
					"P20", [SLOW, RESTRICTING], ["PASw5", "PASw7", "PASw23"], ["PA8R", "PA8L"])
		self.routes["PRtP3P20"] = Route(self.screen, block, "PRtP3P20", "P3",
					[ (101, 28), (102, 28), (103, 28), (104, 28), (105, 28), (106, 27), (107, 26), (108, 26), (109, 26), (110, 26) ],
					"P20", [SLOW, RESTRICTING], ["PASw3", "PASw5", "PASw7", "PASw9"], ["PA6R", "PA8L"])
		self.routes["PRtP2P20"] = Route(self.screen, block, "PRtP2P20", "P2",
					[ (100, 30), (101, 30), (102, 30), (103, 30), (104, 29), (105, 28), (106, 27), (107, 26), (108, 26), (109, 26), (110, 26) ],
					"P20", [SLOW, SLOW], ["PASw1", "PASw3", "PASw9"], ["PA4RA", "PA8L"])
		self.routes["PRtP1P20"] = Route(self.screen, block, "PRtP1P20", "P1",
					[ (100, 32), (101, 32), (102, 31), (103, 30), (104, 29), (105, 28), (106, 27), (107, 26), (108, 26), (109, 26), (110, 26) ],
					"P20", [SLOW, RESTRICTING], ["PASw1", "PASw3", "PASw5", "PASw7", "PASw9"], ["PA4RB", "PA8L"])

		block = self.blocks["POSSP4"]
		self.routes["PRtP3P62"] = Route(self.screen, block, "PRtP3P62", "P3",
					[ (101, 28), (102, 28), (103, 28), (104, 28), (105, 28), (106, 28), (107, 28), (108, 28), (109, 28) ],
					"P62", [RESTRICTING, RESTRICTING], ["PASw3", "PASw5", "PASw7", "PASw9", "PASw11"], ["PA6R", "PA6LA"])
		self.routes["PRtP3P63"] = Route(self.screen, block, "PRtP3P63", "P3",
					[ (101, 28), (102, 28), (103, 28), (104, 28), (105, 28), (106, 28), (107, 28), (108, 29), (109, 30), (110, 30), (111, 30) ],
					"P63", [RESTRICTING, RESTRICTING], ["PASw3", "PASw5", "PASw7", "PASw9", "PASw11", "PASw13"], ["PA6R", "PA6LB"])
		self.routes["PRtP3P64"] = Route(self.screen, block, "PRtP3P64", "P3",
					[ (101, 28), (102, 28), (103, 28), (104, 28), (105, 28), (106, 28), (107, 28), (108, 29), (109, 30), (110, 31), (111, 32), (112, 32) ],
					"P64", [RESTRICTING, RESTRICTING], ["PASw3", "PASw5", "PASw7", "PASw9", "PASw11", "PASw13"], ["PA6R", "PA6LC"])
		self.routes["PRtP2P62"] = Route(self.screen, block, "PRtP2P62", "P2",
					[ (100, 30), (101, 30), (102, 30), (103, 30), (104, 29), (105, 28), (106, 28), (107, 28), (108, 28), (109, 28) ],
					"P62", [RESTRICTING, RESTRICTING], ["PASw1", "PASw3", "PASw5", "PASw7", "PASw9", "PASw11"], ["PA4RA", "PA6LA"])
		self.routes["PRtP2P63"] = Route(self.screen, block, "PRtP2P63", "P2",
					[ (100, 30), (101, 30), (102, 30), (103, 30), (104, 29), (105, 28), (106, 28), (107, 28), (108, 29), (109, 30), (110, 30), (111, 30) ],
					"P63", [RESTRICTING, RESTRICTING], ["PASw1", "PASw3", "PASw5", "PASw7", "PASw9", "PASw11", "PASw13"], ["PA4RA", "PA6LB"])
		self.routes["PRtP2P64"] = Route(self.screen, block, "PRtP2P64", "P2",
					[ (100, 30), (101, 30), (102, 30), (103, 30), (104, 29), (105, 28), (106, 28), (107, 28), (108, 29), (109, 30), (110, 31), (111, 32), (112, 32) ],
					"P64", [RESTRICTING, RESTRICTING], ["PASw1", "PASw3", "PASw5", "PASw7", "PASw9", "PASw11", "PASw13"], ["PA4RA", "PA6LC"])
		self.routes["PRtP1P62"] = Route(self.screen, block, "PRtP1P62", "P1",
					[ (100, 32), (101, 32), (102, 31), (103, 30), (104, 29), (105, 28), (106, 28), (107, 28), (108, 28), (109, 28) ],
					"P62", [RESTRICTING, RESTRICTING], ["PASw1", "PASw3", "PASw5", "PASw7", "PASw9", "PASw11"], ["PA4RB", "PA6LA"])
		self.routes["PRtP1P63"] = Route(self.screen, block, "PRtP1P63", "P1",
					[ (100, 32), (101, 32), (102, 31), (103, 30), (104, 29), (105, 28), (106, 28), (107, 28), (108, 29), (109, 30), (110, 30), (111, 30) ],
					"P63", [RESTRICTING, RESTRICTING], ["PASw1", "PASw3", "PASw5", "PASw7", "PASw9", "PASw11", "PASw13"], ["PA4RB", "PA6LB"])
		self.routes["PRtP1P64"] = Route(self.screen, block, "PRtP1P64", "P1",
					[ (100, 32), (101, 32), (102, 31), (103, 30), (104, 29), (105, 28), (106, 28), (107, 28), (108, 29), (109, 30), (110, 31), (111, 32), (112, 32) ],
					"P64", [RESTRICTING, RESTRICTING], ["PASw1", "PASw3", "PASw5", "PASw7", "PASw9", "PASw11", "PASw13"], ["PA4RB", "PA6LC"])

		block = self.blocks["POSSP5"]
		self.routes["PRtP3P40"] = Route(self.screen, block, "PRtP3P40", "P3",
					[ (101, 28), (102, 28), (103, 28), (104, 29), (105, 30), (106, 31), (107, 32), (108, 33), (109, 34), (110, 35), (111,35) ],
					"P40", [SLOW, SLOW], ["PASw3", "PASw9"], ["PA6R", "PA4L"])
		self.routes["PRtP2P40"] = Route(self.screen, block, "PRtP2P40", "P2",
					[ (100, 30), (101, 30), (102, 30), (103, 30), (104, 30), (105, 30), (106, 31), (107, 32), (108, 33), (109, 34), (110, 35), (111, 35) ],
					"P40", [SLOW, SLOW], ["PASw1", "PASw3", "PASw9"], ["PA4RA", "PA4L"])
		self.routes["PRtP1P40"] = Route(self.screen, block, "PRtP1P40", "P1",
					[ (100, 32), (101, 32), (102, 31), (103, 30), (104, 30), (105, 30), (106, 31), (107, 32), (108, 33), (109, 34), (110, 35), (111, 35) ],
					"P40", [SLOW, RESTRICTING], ["PASw1", "PASw3", "PASw9"], ["PA4RB", "PA4L"])

		self.signals["PA12R"].AddPossibleRoutes("POSSP1", [ "PRtP7V10", "PRtP7P60", "PRtP7P61" ])
		self.signals["PA12R"].AddPossibleRoutes("POSSP2", [ "PRtP7P10" ])
		self.signals["PA12R"].AddPossibleRoutes("POSSP3", [ "PRtP7P20" ])
		self.signals["PA12LA"].AddPossibleRoutes("POSSP1", [ "PRtP7V10" ])
		self.signals["PA12LB"].AddPossibleRoutes("POSSP1", [ "PRtP7P60" ])
		self.signals["PA12LC"].AddPossibleRoutes("POSSP1", [ "PRtP7P61" ])

		self.signals["PA10RA"].AddPossibleRoutes("POSSP2", [ "PRtP6P10" ])
		self.signals["PA10RA"].AddPossibleRoutes("POSSP3", [ "PRtP6P20" ])
		self.signals["PA10L"].AddPossibleRoutes("POSSP2", [ "PRtP7P10", "PRtP6P10", "PRtP5P10", "PRtP4P10", "PRtP3P10", "PRtP2P10", "PRtP1P10" ])

		self.signals["PA10RB"].AddPossibleRoutes("POSSP2", [ "PRtP5P10" ])
		self.signals["PA10RB"].AddPossibleRoutes("POSSP3", [ "PRtP5P20" ])

		self.signals["PA8R"].AddPossibleRoutes("POSSP2", [ "PRtP4P10" ])
		self.signals["PA8L"].AddPossibleRoutes("POSSP3", [ "PRtP7P20", "PRtP6P20", "PRtP5P20", "PRtP4P20", "PRtP3P20", "PRtP2P20", "PRtP1P20" ])

		self.signals["PA6R"].AddPossibleRoutes("POSSP2", [ "PRtP3P10" ])
		self.signals["PA6R"].AddPossibleRoutes("POSSP3", [ "PRtP3P20" ])
		self.signals["PA6R"].AddPossibleRoutes("POSSP4", [ "PRtP3P62", "PRtP3P63", "PRtP3P64" ])
		self.signals["PA6R"].AddPossibleRoutes("POSSP5", [ "PRtP3P40" ])
		self.signals["PA6LA"].AddPossibleRoutes("POSSP4", [ "PRtP3P62", "PRtP2P62", "PRtP1P62" ])
		self.signals["PA6LB"].AddPossibleRoutes("POSSP4", [ "PRtP3P63", "PRtP2P63", "PRtP1P63" ])
		self.signals["PA6LC"].AddPossibleRoutes("POSSP4", [ "PRtP3P64", "PRtP2P64", "PRtP1P64" ])

		self.signals["PA4RA"].AddPossibleRoutes("POSSP2", [ "PRtP2P10" ])
		self.signals["PA4RA"].AddPossibleRoutes("POSSP3", [ "PRtP2P20" ])
		self.signals["PA4RA"].AddPossibleRoutes("POSSP4", [ "PRtP2P62", "PRtP2P63", "PRtP2P64" ])
		self.signals["PA4RA"].AddPossibleRoutes("POSSP5", [ "PRtP3P40" ])
		self.signals["PA4RB"].AddPossibleRoutes("POSSP2", [ "PRtP1P10" ])
		self.signals["PA4RB"].AddPossibleRoutes("POSSP3", [ "PRtP1P20" ])
		self.signals["PA4RB"].AddPossibleRoutes("POSSP4", [ "PRtP1P62", "PRtP1P63", "PRtP1P64" ])
		self.signals["PA4RB"].AddPossibleRoutes("POSSP5", [ "PRtP3P40" ])
		self.signals["PA4L"].AddPossibleRoutes("POSSP5", [ "PRtP3P40", "PRtP2P40", "PRtP1P40" ])

		self.osSignals["POSSP1"] = [ "PA12R", "PS12LA", "PA12LB", "PA12LC" ]
		self.osSignals["POSSP2"] = [ "PA12R", "PA10RA", "PA10RB", "PA8R", "PA6R", "PA4RA", "PA4RB", "PA10L" ]
		self.osSignals["POSSP3"] = [ "PA12R", "PA10RA", "PA10RB", "PA8R", "PA6R", "PA4RA", "PA4RB", "PA8L" ]
		self.osSignals["POSSP4"] = [ "PA6R", "PA4RA", "PA4RB", "PA6LA", "PA6LB", "PA6LC" ]
		self.osSignals["POSSP5"] = [ "PA6R", "PA4RA", "PA4RB", "PA4L" ]

		return self.signals

	def DefineHandSwitches(self, tiles):
		self.handswitches = {}

		hs = HandSwitch(self, self.screen, self.frame, self.blocks["P42"], "PBSw15a.hand", (145, 34), tiles["handdown"])
		self.blocks["P42"].AddHandSwitch(hs)
		self.handswitches["PBSw15a.hand"] = hs

		hs = HandSwitch(self, self.screen, self.frame, self.blocks["P42"], "PBSw15b.hand", (149, 36), tiles["handup"])
		self.blocks["P42"].AddHandSwitch(hs)
		self.handswitches["PBSw15b.hand"] = hs

		hs = HandSwitch(self, self.screen, self.frame, self.blocks["P41"], "PBSw5.hand", (129, 36), tiles["handup"])
		self.blocks["P41"].AddHandSwitch(hs)
		self.handswitches["PBSw5.hand"] = hs
		return self.handswitches

