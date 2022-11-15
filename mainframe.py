import wx
import wx.lib.newevent

import os
import json
import inspect

cmdFolder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
import logging

from settings import Settings
from bitmaps import BitMaps
from district import Districts
from trackdiagram import TrackDiagram
from tile import loadTiles
from block import Block
from train import Train

from breaker import BreakerDisplay, BreakerName
from toaster import Toaster, TB_CENTER

from districts.hyde import Hyde
from districts.yard import Yard
from districts.latham import Latham
from districts.dell import Dell
from districts.shore import Shore
from districts.krulish import Krulish
from districts.nassau import Nassau
from districts.bank import Bank
from districts.cliveden import Cliveden
from districts.cliff import Cliff

from constants import HyYdPt, LaKr, NaCl, screensList, EMPTY, OCCUPIED, NORMAL, REVERSE, OVERSWITCH
from listener import Listener
from rrserver import RRServer

from edittraindlg import EditTrainDlg

(DeliveryEvent, EVT_DELIVERY) = wx.lib.newevent.NewEvent() 
(DisconnectEvent, EVT_DISCONNECT) = wx.lib.newevent.NewEvent() 

allowedCommands = [ "settrain", "renametrain" ]

class Node:
	def __init__(self, screen, bitmapName, offset):
		self.screen = screen
		self.bitmap = bitmapName
		self.offset = offset

class MainFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, size=(900, 800), style=wx.DEFAULT_FRAME_STYLE)
		self.sessionid = None
		self.subscribed = False
		logging.info("Display process starting")
		self.settings = Settings(cmdFolder)

		self.title = "PSRY Dispatcher" if self.settings.dispatch else "PSRY Monitor"
		self.ToasterSetup()
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		vsz = wx.BoxSizer(wx.VERTICAL)
		hsz = wx.BoxSizer(wx.HORIZONTAL)
		self.bitmaps = BitMaps(os.path.join(".", "bitmaps"))
		singlePage = self.settings.pages == 1
		self.diagrams = {
			HyYdPt: Node(HyYdPt, self.bitmaps.diagrams.HydeYardPort, 0),
			LaKr:   Node(LaKr,   self.bitmaps.diagrams.LathamKrulish, 2544 if singlePage else 0),
			NaCl:   Node(NaCl,   self.bitmaps.diagrams.NassauCliff, 5088 if singlePage else 0)
		}
		topSpace = 120
		if self.settings.pages == 1:  # set up a single ultra-wide display accross 3 monitors
			dp = TrackDiagram(self, [self.diagrams[sn] for sn in screensList])
			dp.SetPosition((16, 120))
			diagramw, diagramh = dp.GetSize()
			self.panels = {self.diagrams[sn].screen : dp for sn in screensList}  # all 3 screens just point to the same diagram
			totalw = 2560*3

		else:  # set up three separate screens for a single monitor
			self.panels = {}
			for d in [self.diagrams[sn] for sn in screensList]:
				dp = TrackDiagram(self, [d])
				dp.Hide()
				dp.SetPosition((8, 120))
				self.panels[d.screen] = dp

			self.currentScreen = LaKr
			diagramw, diagramh = self.panels[self.currentScreen].GetSize()
			self.panels[self.currentScreen].Show()

			# add buttons to switch from screen to screen
			voffset = topSpace+diagramh+20
			b = wx.Button(self, wx.ID_ANY, "Hyde/Yard/Port", pos=(500, voffset), size=(200, 50))
			self.Bind(wx.EVT_BUTTON, lambda event: self.SwapToScreen(HyYdPt), b)
			b = wx.Button(self, wx.ID_ANY, "Latham/Krulish", pos=(1145, voffset), size=(200, 50))
			self.Bind(wx.EVT_BUTTON, lambda event: self.SwapToScreen(LaKr), b)
			b = wx.Button(self, wx.ID_ANY, "Nassau/Cliff",   pos=(1790, voffset), size=(200, 50))
			self.Bind(wx.EVT_BUTTON, lambda event: self.SwapToScreen(NaCl), b)
			totalw = 2560+20

		if self.settings.showcameras:
			self.DrawCameras()

		self.bSubscribe = wx.Button(self, wx.ID_ANY, "Connect", pos=(100, 10))
		self.Bind(wx.EVT_BUTTON, self.OnSubscribe, self.bSubscribe)

		self.bRefresh = wx.Button(self, wx.ID_ANY, "Refresh", pos=(400, 10))
		self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.bRefresh)
		self.bRefresh.Enable(False)

		self.scrn = wx.TextCtrl(self, wx.ID_ANY, "", size=(80, -1), pos=(100, 50), style=wx.TE_READONLY)
		self.xpos = wx.TextCtrl(self, wx.ID_ANY, "", size=(40, -1), pos=(200, 50), style=wx.TE_READONLY)
		self.ypos = wx.TextCtrl(self, wx.ID_ANY, "", size=(40, -1), pos=(260, 50), style=wx.TE_READONLY)

		h = 1080
		self.breakerDisplay = BreakerDisplay(self, pos=(int(totalw/2-400/2), 50), size=(400, 40))

		self.SetMaxSize((totalw, h))
		self.SetSize((totalw, h))
		self.SetPosition((0, 0))

		wx.CallAfter(self.Initialize)
			
	def DrawCameras(self):
		cams = {}
		cams[LaKr] = [
			[(242, 32), self.bitmaps.cameras.lakr.cam7],
			[(464, 32), self.bitmaps.cameras.lakr.cam8],
			[(768, 32), self.bitmaps.cameras.lakr.cam8],
			[(890, 32), self.bitmaps.cameras.lakr.cam10],
			[(972, 32), self.bitmaps.cameras.lakr.cam12],
			[(1186, 32), self.bitmaps.cameras.lakr.cam3],
			[(1424, 32), self.bitmaps.cameras.lakr.cam4],
			[(1634, 32), self.bitmaps.cameras.lakr.cam13],
			[(1884, 32), self.bitmaps.cameras.lakr.cam14],
			[(2152, 32), self.bitmaps.cameras.lakr.cam15],
			[(2198, 32), self.bitmaps.cameras.lakr.cam16],
			[(2362, 32), self.bitmaps.cameras.lakr.cam9],
			[(2416, 32), self.bitmaps.cameras.lakr.cam10],
		]
		cams[HyYdPt] = [
			[(282, 72), self.bitmaps.cameras.hyydpt.cam15],
			[(838, 72), self.bitmaps.cameras.hyydpt.cam16],
			[(904, 576), self.bitmaps.cameras.hyydpt.cam1],
			[(1712, 10), self.bitmaps.cameras.hyydpt.cam1],
			[(1840, 10), self.bitmaps.cameras.hyydpt.cam2],
			[(1960, 10), self.bitmaps.cameras.hyydpt.cam3],
			[(2090, 10), self.bitmaps.cameras.hyydpt.cam4],
			[(2272, 236), self.bitmaps.cameras.hyydpt.cam5],
			[(2292, 444), self.bitmaps.cameras.hyydpt.cam6],
		]
		cams[NaCl] = [
			[(364, 28), self.bitmaps.cameras.nacl.cam11],
			[(670, 28), self.bitmaps.cameras.nacl.cam12],
			[(918, 28), self.bitmaps.cameras.nacl.cam1],
			[(998, 28), self.bitmaps.cameras.nacl.cam2],
			[(1074, 28), self.bitmaps.cameras.nacl.cam3],
			[(1248, 28), self.bitmaps.cameras.nacl.cam4],
			[(1442, 28), self.bitmaps.cameras.nacl.cam7],
			[(2492, 502), self.bitmaps.cameras.nacl.cam8],
		]

		for screen in cams:
			offset = self.diagrams[screen].offset
			for pos, bmp in cams[screen]:
				self.panels[screen].DrawFixedBitmap(pos[0], pos[1], offset, bmp)

	def UpdatePositionDisplay(self, x, y, scr):
		self.xpos.SetValue("%4d" % x)
		self.ypos.SetValue("%4d" % y)
		self.scrn.SetValue("%s" % scr)

	def ShowTitle(self):
		titleString = self.title
		if self.subscribed and self.sessionid is not None:
			titleString += ("  -  Session ID %d" % self.sessionid)
		self.SetTitle(titleString)

	def Initialize(self):
		self.listener = None
		self.ShowTitle()
		self.Bind(EVT_DELIVERY, self.onDeliveryEvent)
		self.Bind(EVT_DISCONNECT, self.onDisconnectEvent)

		self.tiles, self.totiles, self.sstiles, self.sigtiles, self.misctiles = loadTiles(self.bitmaps)
		self.districts = Districts()
		self.districts.AddDistrict(Yard("Yard", self, HyYdPt))
		self.districts.AddDistrict(Latham("Latham", self, LaKr))
		self.districts.AddDistrict(Dell("Dell", self, LaKr))
		self.districts.AddDistrict(Shore("Shore", self, LaKr))
		self.districts.AddDistrict(Krulish("Krulish", self, LaKr))
		self.districts.AddDistrict(Nassau("Nassau", self, NaCl))
		self.districts.AddDistrict(Bank("Bank", self, NaCl))
		self.districts.AddDistrict(Cliveden("Cliveden", self, NaCl))
		self.districts.AddDistrict(Cliff("Cliff", self, NaCl))
		self.districts.AddDistrict(Hyde("Hyde", self, HyYdPt))

		self.blocks, self.osBlocks = self.districts.DefineBlocks(self.tiles)
		self.turnouts = self.districts.DefineTurnouts(self.totiles, self.blocks)
		self.signals =  self.districts.DefineSignals(self.sigtiles)
		self.buttons =  self.districts.DefineButtons(self.bitmaps.buttons)
		self.handswitches =  self.districts.DefineHandSwitches(self.misctiles)
		self.indicators = self.districts.DefineIndicators()

		self.pendingFleets = {}

		self.resolveObjects()

		self.AddBogusStuff()

		self.rrServer = RRServer()
		self.rrServer.SetServerAddress(self.settings.ipaddr, self.settings.serverport)

		self.trains = {}

		self.districts.Initialize(self.sstiles, self.misctiles)

		# only set up hot spots on the diagram for dispatchr - not for remote display
		if self.settings.dispatch:
			self.turnoutMap = { (t.GetScreen(), t.GetPos()): t for t in self.turnouts.values() if not t.IsRouteControlled() }
			self.buttonMap = { (b.GetScreen(), b.GetPos()): b for b in self.buttons.values() }
			self.signalMap = { (s.GetScreen(), s.GetPos()): s for s in self.signals.values() }
			self.handswitchMap = { (l.GetScreen(), l.GetPos()): l for l in self.handswitches.values() }

		else:
			self.turnoutMap = {}
			self.buttonMap = {}
			self.signalMap = {}
			self.handswitchMap = {}

		# set up hot spots for entering/modifying train/loco ID - displays can do this too
		self.blockMap = self.BuildBlockMap(self.blocks)

		self.buttonsToClear = []

		self.districts.Draw()
		
		self.Bind(wx.EVT_TIMER, self.onTicker)
		self.ticker = wx.Timer(self)
		self.ticker.Start(1000)

		print("finished initialize")

	def IsDispatcher(self):
		return self.settings.dispatch

	def resolveObjects(self):
		for bknm, bk in self.blocks.items():
			sgWest, sgEast = bk.GetSignals()
			if sgWest is not None:
				try:
					self.signals[sgWest].SetGuardBlock(bk)
				except KeyError:
					sgWest = None

			if sgEast is not None:
				try:
					self.signals[sgEast].SetGuardBlock(bk)
				except KeyError:
					sgEast = None
			bk.SetSignals((sgWest, sgEast))

		# invert osBlocks so the we can easily map a block into the OS's it interconnects
		self.blockOSMap = {}
		for osblknm, blklist in self.osBlocks.items():
			for blknm in blklist:
				if blknm in self.blockOSMap:
					self.blockOSMap[blknm].append(self.blocks[osblknm])
				else:
					self.blockOSMap[blknm] = [ self.blocks[osblknm] ]

	def GetOSForBlock(self, blknm):
		if blknm not in self.blockOSMap:
			return []
		else:
			return self.blockOSMap[blknm]

	def AddPendingFleet(self, block, sig):
		self.pendingFleets[block.GetName()] = sig

	def DelPendingFleet(self, block):
		bname = block.GetName()
		if bname not in self.pendingFleets:
			return

		del(self.pendingFleets[bname])

	def DoFleetPending(self, block):
		bname = block.GetName()
		if bname not in self.pendingFleets:
			return

		sig = self.pendingFleets[bname]
		del(self.pendingFleets[bname])

		sig.DoFleeting()		

	def BuildBlockMap(self, bl):
		blkMap = {}
		for b in bl.values():
			tl = b.GetTrainLoc()
			for scrn, pos in tl:
				lkey = (scrn, pos[1])
				if lkey not in blkMap.keys():
					blkMap[lkey] = []
				blkMap[lkey].append((pos[0], b))

		return blkMap
###################################################### TO BE REMOVED 
	def AddBogusStuff(self):
		#this is to add bogus entries for block that we need before we get to their district

		if "P11" in self.blocks:
			print("You can remove bogus entry for block P11")
		else:
			self.blocks["P11"] = Block(self, self, "P11",	[], False)
		if "P21" in self.blocks:
			print("You can remove bogus entry for block P21")
		else:
			self.blocks["P21"] = Block(self, self, "P21",	[], False)
		if "P32" in self.blocks:
			print("You can remove bogus entry for block P32")
		else:
			self.blocks["P32"] = Block(self, self, "P32",	[], False)
		if "P42" in self.blocks:
			print("You can remove bogus entry for block P42")
		else:
			self.blocks["P42"] = Block(self, self, "P42",	[], False)
		if "P50" in self.blocks:
			print("You can remove bogus entry for block P50")
		else:
			self.blocks["P50"] = Block(self, self, "P50",	[], False)

	def DrawOthers(self, block):
		print("Remove this bogus drawothers method from mainframe")

	def DoBlockAction(self, blk, blockend, state):
		print("Remove this bogus doblockaction method from mainframe")

####################################################### END OF TO BE REMOVED
		
	def onTicker(self, _):
		self.ClearExpiredButtons()
		self.breakerDisplay.ticker()

	def ClearExpiredButtons(self):
		collapse = False
		for b in self.buttonsToClear:
			b[0] -= 1
			if b[0] <= 0:
				b[1].Release(refresh=True)
				collapse = True

		if collapse:
			self.buttonsToClear = [x for x in self.buttonsToClear if x[0] > 0]

	def ClearButtonAfter(self, secs, btn):
		self.buttonsToClear.append([secs, btn])

	def ClearButtonNow(self, btn):
		bnm = btn.GetName()
		collapse = False
		for bx in range(len(self.buttonsToClear)):
			if self.buttonsToClear[bx][1].GetName() == bnm:
				self.buttonsToClear[bx][0] = 0
				self.buttonsToClear[bx][1].Release(refresh=True)
				collapse = True

		if collapse:
			self.buttonsToClear = [x for x in self.buttonsToClear if x[0] > 0]

	def ResetButtonExpiry(self, secs, btn):
		bnm = btn.GetName()
		for bx in range(len(self.buttonsToClear)):
			if self.buttonsToClear[bx][1].GetName() == bnm:
				self.buttonsToClear[bx][0] = secs

	def ProcessClick(self, screen, pos):
		logging.debug("click %s %d, %d" % (screen, pos[0], pos[1]))
		try:
			to = self.turnoutMap[(screen, pos)]
		except KeyError:
			to = None

		if to:
			to.GetDistrict().PerformTurnoutAction(to)
			return

		try:
			btn = self.buttonMap[(screen, pos)]
		except KeyError:
			btn = None

		if btn:
			btn.GetDistrict().PerformButtonAction(btn)
			return

		try:
			sig = self.signalMap[(screen, pos)]
		except KeyError:
			sig = None

		if sig:
			sig.GetDistrict().PerformSignalAction(sig)

		try:
			hs = self.handswitchMap[(screen, pos)]
		except KeyError:
			hs = None

		if hs:
			hs.GetDistrict().PerformHandSwitchAction(hs)

		try:
			ln = self.blockMap[(screen, pos[1])]
		except KeyError:
			ln = None

		if ln:
			for col, blk in ln:
				if col <= pos[0] <= col+3:
					break
			else:
				blk = None

			if blk:
				if blk.IsOccupied():
					tr = blk.GetTrain()
					oldName, oldLoco = tr.GetNameAndLoco()
					dlg = EditTrainDlg(self, tr)
					rc = dlg.ShowModal()
					if rc == wx.ID_OK:
						trainid, locoid = dlg.GetResults()
					dlg.Destroy()
					if rc != wx.ID_OK:
						return

					self.Request({"renametrain": { "oldname": oldName, "newname": trainid, "oldloco": oldLoco, "newloco": locoid}})

	def ProcessRightClick(self, screen, pos):
		logging.debug("right click %s %d, %d" % (screen, pos[0], pos[1]))
		try:
			sig = self.signalMap[(screen, pos)]
		except KeyError:
			sig = None

		if sig:
			sig.EnableFleeting()

	def DrawTile(self, screen, pos, bmp):
		offset = self.diagrams[screen].offset
		self.panels[screen].DrawTile(pos[0], pos[1], offset, bmp)

	def DrawText(self, screen, pos, text):
		offset = self.diagrams[screen].offset
		self.panels[screen].DrawText(pos[0], pos[1], offset, text)

	def ClearText(self, screen, pos):
		offset = self.diagrams[screen].offset
		self.panels[screen].ClearText(pos[0], pos[1], offset)

	def DrawTrain(self, screen, pos, trainID, locoID, stopRelay):
		offset = self.diagrams[screen].offset
		self.panels[screen].DrawTrain(pos[0], pos[1], offset, trainID, locoID, stopRelay)

	def ClearTrain(self, screen, pos):
		offset = self.diagrams[screen].offset
		self.panels[screen].ClearTrain(pos[0], pos[1], offset)

	def SwapToScreen(self, screen):
		if screen not in screensList:
			return False
		if screen == self.currentScreen:
			return True
		self.panels[screen].Show()
		self.panels[self.currentScreen].Hide()
		self.currentScreen = screen
		return True

	def GetBlockStatus(self, blknm):
		try:
			blk = self.blocks[blknm]
		except KeyError:
			return EMPTY

		return blk.GetStatus()

	def GetBlockByName(self, blknm):
		try:
			return self.blocks[blknm]
		except:
			return None

	def GetSignalByName(self, signm):
		try:
			return self.signals[signm]
		except:
			return None

	def NewTrain(self):
		tr = Train(None)
		name, loco = tr.GetNameAndLoco()
		self.trains[name] = tr
		return tr

	def ToasterSetup(self):
		self.toaster = Toaster()
		self.toaster.SetPositionByCorner(TB_CENTER)
		self.toaster.SetFont(wx.Font(wx.Font(20, wx.FONTFAMILY_ROMAN, wx.NORMAL, wx.BOLD, faceName="Arial")))
		self.toaster.SetBackgroundColour(wx.Colour(255, 179, 154))
		self.toaster.SetTextColour(wx.Colour(0, 0, 0))

	def Popup(self, message, background=None, text=None):
		self.toaster.Append(message)

	def OnSubscribe(self, _):
		if self.subscribed:
			self.listener.kill()
			self.listener.join()
			self.listener = None
			self.subscribed = False
			self.sessionid = None
			self.bSubscribe.SetLabel("Connect")
			self.bRefresh.Enable(False)
		else:
			self.listener = Listener(self, self.settings.ipaddr, self.settings.socketport)
			if not self.listener.connect():
				logging.error("Unable to establish connection with server")
				self.listener = None
				return

			self.listener.start()
			self.subscribed = True
			self.bSubscribe.SetLabel("Disconnect")
			self.bRefresh.Enable(True)
			if self.settings.dispatch:
				self.SendBlockDirRequests()
				self.SendOSRoutes()
				
		self.breakerDisplay.UpdateDisplay()
		self.ShowTitle()

	def OnRefresh(self, _):
		self.rrServer.SendRequest({"refresh": {"SID": self.sessionid}})

	def raiseDeliveryEvent(self, data): # thread context
		try:
			jdata = json.loads(data)
		except json.decoder.JSONDecodeError:
			logging.warning("Unable to parse (%s)" % data)
			return
		evt = DeliveryEvent(data=jdata)
		wx.QueueEvent(self, evt)

	def onDeliveryEvent(self, evt):
		for cmd, parms in evt.data.items():
			logging.info("Dispatch: %s: %s" % (cmd, parms))
			print("Dispatch: %s: %s" % (cmd, parms))
			if cmd == "turnout":
				for p in parms:
					turnout = p["name"]
					state = p["state"]
					to = self.turnouts[turnout]
					try:
						to = self.turnouts[turnout]
					except KeyError:
						to = None

					if to is not None and state != to.GetStatus():
						district = to.GetDistrict()
						st = REVERSE if state == "R" else NORMAL
						district.DoTurnoutAction(to, st)

			elif cmd == "block":
				for p in parms:
					block = p["name"]
					state = p["state"]
					blk = None
					try:
						blk = self.blocks[block]
						blockend = None
					except KeyError:
						if block.endswith(".E") or block.endswith(".W"):
							blockend = block[-1]
							block = block[:-2]
							try:
								blk = self.blocks[block]
							except KeyError:
								blk = None

					stat = OCCUPIED if state == 1 else EMPTY
					if blk is not None and blk.GetStatus(blockend) != stat:
						district = blk.GetDistrict()
						district.DoBlockAction(blk, blockend, stat)
					
			elif cmd == "signal":
				for p in parms:
					sigName = p["name"]
					aspect = p["aspect"]
					
					try:
						sig = self.signals[sigName]
					except:
						sig = None

					if sig is not None and aspect != sig.GetAspect():
						district = sig.GetDistrict()
						district.DoSignalAction(sig, aspect)
						
			elif cmd == "handswitch":
				for p in parms:
					hsName = p["name"]
					state = p["state"]
					
					try:
						hs = self.handswitches[hsName]
					except:
						hs = None

					if hs is not None and state != hs.GetValue():
						district = hs.GetDistrict()
						district.DoHandSwitchAction(hs, state)
						
			elif cmd == "indicator":
				for p in parms:
					iName = p["name"]
					value = int(p["value"])
					
					try:
						ind = self.indicators[iName]
					except:
						ind = None

					print("indicator %s %d %d" % (iName, value, ind.GetValue()))
					if ind is not None:
						district = ind.GetDistrict()
						district.DoIndicatorAction(ind, value)

			elif cmd == "breaker":
				for p in parms:
					name = p["name"]
					val = p["value"]
					logging.debug("Set Breaker %s to %s" % (name, "TRIPPED" if val != 0 else "CLEAR"))
					if val == 1:
						self.Popup("Breaker: %s" % BreakerName(name))
						self.breakerDisplay.AddBreaker(name)
					else:
						self.breakerDisplay.DelBreaker(name)

					if name in self.indicators:
						ind = self.indicators[name]
						if val != ind.GetValue():
							ind.SetValue(val)

			elif cmd == "settrain":
				for p in parms:
					block = p["block"]
					name = p["name"]
					loco = p["loco"]
					print("set train %s %s %s" % (str(block), str(name), str(loco)))

					try:
						blk = self.blocks[block]
					except:
						logging.warning("unable to identify block (%s)" % block)
						print("unable to identify block (%s)" % block)
						blk = None

					if blk:
						tr = blk.GetTrain()
						if name is None:
							print("train name is none, tr = %s" % str(tr))
							if tr:
								print("calling remove from block")
								tr.RemoveFromBlock(blk)

							print("remove block from all trains in the trainlist")
							delList = []
							for trid, tr in self.trains.items():
								if tr.IsInBlock(blk):
									tr.RemoveFromBlock(blk)
									if tr.IsInNoBlocks():
										delList.append(trid)

							for trid in delList:
								try:
									del(self.trains[trid])
								except:
									logging.warning("can't delete train %s from train list" % trid)

							print("returning")
							return

						if not blk.IsOccupied():
							logging.warning("Set train for block %s, but that block is unoccupied" % block)
							return

						if tr:
							oldName = tr.GetName()
							if oldName and oldName != name:
								if name in self.trains:
									# merge the two trains under the new "name"
									try:
										bl = self.trains[oldName].GetBlockList()
									except:
										bl = {}
									for blk in bl.values():
										self.trains[name].AddToBlock(blk)
								else:
									tr.SetName(name)
									self.trains[name] = tr

								try:
									del(self.trains[oldName])
								except:
									logging.warning("can't delete train %s from train list" % oldName)
						try:
							tr = self.trains[name]
						except:
							tr = Train(name)
							self.trains[name] = tr
						tr.AddToBlock(blk)
						if loco:
							tr.SetLoco(loco)

						blk.SetTrain(tr)
						if tr:
							tr.Draw()
						else:
							blk.DrawTrain()

			elif cmd == "sessionID":
				self.sessionid = int(parms)
				logging.info("connected to railroad server with session ID %d" % self.sessionid)
				self.districts.OnConnect()
				self.ShowTitle()

		
	def raiseDisconnectEvent(self): # thread context
		evt = DisconnectEvent()
		wx.PostEvent(self, evt)

	def Request(self, req):
		command = list(req.keys())[0]
		if self.settings.dispatch or command in allowedCommands:
			if self.subscribed:
				logging.debug(json.dumps(req))
				print("Outgoing request: %s" % json.dumps(req))
				self.rrServer.SendRequest(req)

	def SendBlockDirRequests(self):
		for b in self.blocks.values():
			self.Request({"blockdir": { "block": b.GetName(), "dir": "E" if b.GetEast() else "W"}})
			sbw, sbe = b.GetStoppingSections()
			for sb in [sbw, sbe]:
				if sb:
					self.Request({"blockdir": { "block": sb.GetName(), "dir": "E" if b.GetEast() else "W"}})

	def SendOSRoutes(self):
		for b in self.blocks.values():
			if b.GetBlockType() == OVERSWITCH:
				b.SendRouteRequest()

	def onDisconnectEvent(self, _):
		self.listener = None
		self.subscribed = False
		self.bSubscribe.SetLabel("Connect")
		self.bRefresh.Enable(False)
		logging.info("Server socket closed")

	def SaveTrains(self):
		trDict = {}
		for trid, tr in self.trains.items():
			trDict[trid] = tr.GetBlockNameList()

		print(json.dumps(trDict))

	def SaveLocos(self):
		locoDict = {}
		for trid, tr in self.trains.items():
			loco = tr.GetLoco()
			if loco is not None:
				locoDict[loco] = tr.GetBlockNameList()

		print(json.dumps(locoDict))


	def OnClose(self, evt):
		self.toaster.Close()
		self.SaveTrains()
		self.SaveLocos()
		try:
			self.listener.kill()
			self.listener.join()
		except:
			pass
		self.Destroy()
		logging.info("Display process ending")

