import wx
import wx.lib.newevent
import wx.lib.agw.toasterbox as TB

import os
import json
import inspect

cmdFolder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))

from settings import Settings
from bitmaps import BitMaps
from district import Districts
from trackdiagram import TrackDiagram
from tile import loadTiles
from block import Block
from train import Train

from districts.hyde import Hyde
from districts.yard import Yard
from districts.latham import Latham

from constants import HyYdPt, LaKr, NaCl, screensList, EMPTY, OCCUPIED, NORMAL, REVERSE
from listener import Listener
from rrserver import RRServer

from edittraindlg import EditTrainDlg

import pprint
(DeliveryEvent, EVT_DELIVERY) = wx.lib.newevent.NewEvent() 
(DisconnectEvent, EVT_DISCONNECT) = wx.lib.newevent.NewEvent() 

class Node:
	def __init__(self, screen, bitmapName, offset):
		self.screen = screen
		self.bitmap = bitmapName
		self.offset = offset

class MainFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, size=(900, 800), style=wx.DEFAULT_FRAME_STYLE)
		self.settings = Settings(cmdFolder)
		self.popupFont = wx.Font(wx.Font(12, wx.FONTFAMILY_ROMAN, wx.NORMAL, wx.BOLD, faceName="Arial"))
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		vsz = wx.BoxSizer(wx.VERTICAL)
		hsz = wx.BoxSizer(wx.HORIZONTAL)
		self.bitmaps = BitMaps(os.path.join(".", "bitmaps"))
		singlePage = self.settings.pages == 1
		cameraDiagrams = self.settings.usecameradiagrams
		self.diagrams = {
			HyYdPt: Node(HyYdPt, self.bitmaps.diagrams.HydeYardPortCam  if cameraDiagrams else self.bitmaps.diagrams.HydeYardPort, 0),
			LaKr:   Node(LaKr,   self.bitmaps.diagrams.LathamKrulishCam if cameraDiagrams else self.bitmaps.diagrams.LathamKrulish, 2544 if singlePage else 0),
			NaCl:   Node(NaCl,   self.bitmaps.diagrams.NassauCliffCam   if cameraDiagrams else self.bitmaps.diagrams.NassauCliff, 5088 if singlePage else 0)
		}
		if self.settings.pages == 1:  # set up a single ultra-wide display accross 3 monitors
			dp = TrackDiagram(self, [self.diagrams[sn] for sn in screensList])
			dp.SetPosition((20, 120))
			w, h = dp.GetSize()
			self.panels = {self.diagrams[sn].screen : dp for sn in screensList}  # all 3 screens just point to the same diagram

		else:  # set up three separate screens for a single monitor
			self.panels = {}
			for d in [self.diagrams[sn] for sn in screensList]:
				dp = TrackDiagram(self, [d])
				dp.Hide()
				dp.SetPosition((20, 120))
				self.panels[d.screen] = dp

			self.currentScreen = LaKr
			w, h = self.panels[self.currentScreen].GetSize()
			self.panels[self.currentScreen].Show()
			h += 120  # add in the amount of vertical space we have reserved at the top of the display

			# add buttons to switch from screen to screen
			b = wx.Button(self, wx.ID_ANY, "Hyde/Yard/Port", pos=(500, h+50), size=(200, 50))
			self.Bind(wx.EVT_BUTTON, lambda event: self.SwapToScreen(HyYdPt), b)
			b = wx.Button(self, wx.ID_ANY, "Latham/Krulish", pos=(1145, h+50), size=(200, 50))
			self.Bind(wx.EVT_BUTTON, lambda event: self.SwapToScreen(LaKr), b)
			b = wx.Button(self, wx.ID_ANY, "Nassau/Cliff",   pos=(1790, h+50), size=(200, 50))
			self.Bind(wx.EVT_BUTTON, lambda event: self.SwapToScreen(NaCl), b)

		self.bSubscribe = wx.Button(self, wx.ID_ANY, "Subscribe", pos=(100, 10))
		self.Bind(wx.EVT_BUTTON, self.OnSubscribe, self.bSubscribe)

		self.xpos = wx.TextCtrl(self, wx.ID_ANY, "", size=(40, -1), pos=(100, 50), style=wx.TE_READONLY)
		self.ypos = wx.TextCtrl(self, wx.ID_ANY, "", size=(40, -1), pos=(160, 50), style=wx.TE_READONLY)


		self.SetMaxSize((w+50, h+200))
		self.SetSize((w+50, h+200))
		w, h = self.GetSize()
		wx.CallAfter(self.Initialize)

	def UpdatePositionDisplay(self, x, y):
		self.xpos.SetValue("%4d" % x)
		self.ypos.SetValue("%4d" % y)

	def Initialize(self):
		self.listener = None
		self.subscribed = False
		self.Bind(EVT_DELIVERY, self.onDeliveryEvent)
		self.Bind(EVT_DISCONNECT, self.onDisconnectEvent)

		self.tiles, self.totiles, self.sstiles, self.sigtiles, self.misctiles = loadTiles(self.bitmaps)
		self.districts = Districts()
		self.districts.AddDistrict(Yard("Yard", self, HyYdPt))
		self.districts.AddDistrict(Latham("Latham", self, LaKr))
		self.districts.AddDistrict(Hyde("Hyde", self, HyYdPt))

		self.blocks =   self.districts.DefineBlocks(self.tiles)
		self.turnouts = self.districts.DefineTurnouts(self.totiles, self.blocks)
		self.signals =  self.districts.DefineSignals(self.sigtiles)
		self.buttons =  self.districts.DefineButtons(self.bitmaps.buttons)
		self.handswitches =  self.districts.DefineHandSwitches(self.misctiles)

		self.AddBogusStuff()
		# print("blocks")
		# print(str(list(self.blocks.keys())))
		# print("turnouts")
		# print(str(list(self.turnouts.keys())))
		# print("signals")
		# print(str(list(self.signals.keys())))
		# print("buttons")
		# print(str(list(self.buttons.keys())))
		# print("locks")
		# print(str(list(self.locks.keys())))

		if not self.districts.Audit():
			print("Audit failed")
			#exit(1)

		self.trains = {}

		self.districts.Initialize(self.sstiles, self.misctiles)

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

		self.blockMap = self.BuildBlockMap(self.blocks)

		self.buttonsToClear = []

		self.districts.Draw()

		# for tr in self.trains:
		# 	tr.Draw()
		
		self.Bind(wx.EVT_TIMER, self.onTicker)
		self.ticker = wx.Timer(self)
		self.ticker.Start(1000)

		self.rrServer = RRServer()
		self.rrServer.SetServerAddress(self.settings.ipaddr, self.settings.serverport)

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

	def AddBogusStuff(self):
		#this is to add bogus entries for block that we need before we get to their district

		if "D10" in self.blocks:
			print("You can remove bogus entry for block D10")
		else:
			self.blocks["D10"] = Block(self, self, "D10",	[], False)
		if "D20" in self.blocks:
			print("You can remove bogus entry for block D20")
		else:
			self.blocks["D20"] = Block(self, self, "D20",	[], False)
		if "P11" in self.blocks:
			print("You can remove bogus entry for block P11")
		else:
			self.blocks["P11"] = Block(self, self, "P11",	[], False)
		if "P21" in self.blocks:
			print("You can remove bogus entry for block P21")
		else:
			self.blocks["P21"] = Block(self, self, "P21",	[], False)
		if "P50" in self.blocks:
			print("You can remove bogus entry for block P50")
		else:
			self.blocks["P50"] = Block(self, self, "P50",	[], False)

	def DrawOthers(self, block):
		print("Remove this bogus drawothers method from mainframe")
		
	def onTicker(self, _):
		collapse = False
		for b in self.buttonsToClear:
			b[0] -= 1
			if b[0] == 0:
				b[1].Release(refresh=True)
				collapse = True

		if collapse:
			self.buttonsToClear = [x for x in self.buttonsToClear if x[0] != 0]

	def ClearButtonAfter(self, secs, btn):
		self.buttonsToClear.append([secs, btn])

	def ProcessClick(self, screen, pos):
		#print("click %s %d, %d" % (screen, pos[0], pos[1]))
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
					dlg = EditTrainDlg(self, tr)
					rc = dlg.ShowModal()
					if rc == wx.ID_OK:
						trainid, locoid = dlg.GetResults()
					dlg.Destroy()
					if rc != wx.ID_OK:
						return

					self.Request({"settrain": { "block": blk.GetName(), "name": trainid, "loco": locoid}})

	def DrawTile(self, screen, pos, bmp):
		offset = self.diagrams[screen].offset
		self.panels[screen].DrawTile(pos[0], pos[1], offset, bmp)

	def DrawText(self, screen, pos, text):
		offset = self.diagrams[screen].offset
		self.panels[screen].DrawText(pos[0], pos[1], offset, text)

	def ClearText(self, screen, pos):
		offset = self.diagrams[screen].offset
		self.panels[screen].ClearText(pos[0], pos[1], offset)

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

	def Popup(self, message):
		tb = TB.ToasterBox(self, TB.TB_SIMPLE, TB.TB_DEFAULT_STYLE, TB.TB_ONTIME,
			scrollType=TB.TB_SCR_TYPE_FADE)

		tb.SetPopupSize((400, 60))
		tb.CenterOnParent(wx.BOTH)
		tb.SetPopupPauseTime(5000)
		tb.SetPopupScrollSpeed(8)
		tb.SetPopupBackgroundColour(wx.Colour(255, 179, 154))
		tb.SetPopupTextColour(wx.Colour(0, 0, 0))
		tb.SetPopupText(message)
		tb.SetPopupTextFont(self.popupFont)
		tb.Play()

	def OnSubscribe(self, _):
		if self.subscribed:
			self.listener.kill()
			self.listener.join()
			self.listener = None
			self.subscribed = False
			self.bSubscribe.SetLabel("Subscribe")
		else:
			self.listener = Listener(self, self.settings.ipaddr, self.settings.socketport)
			if not self.listener.connect():
				print("Unable to establish connection with server")
				self.listener = None
				return

			self.listener.start()
			self.subscribed = True
			self.bSubscribe.SetLabel("Unsubscribe")

	def raiseDeliveryEvent(self, data): # thread context
		try:
			jdata = json.loads(data)
		except json.decoder.JSONDecodeError:
			print("Unable to parse (%s)" % data)
			return
		evt = DeliveryEvent(data=jdata)
		wx.PostEvent(self, evt)

	def onDeliveryEvent(self, evt):
		for cmd, parms in evt.data.items():
			print("Delivery from dispatch: %s: %s" % (cmd, parms))
			if cmd == "turnout":
				for p in parms:
					turnout = p["name"]
					state = p["state"]
					to = self.turnouts[turnout]
					try:
						to = self.turnouts[turnout]
					except KeyError:
						return
					
					district = to.GetDistrict()
					st = REVERSE if state == "R" else NORMAL

					district.DoTurnoutAction(to, st)

			elif cmd == "block":
				for p in parms:
					block = p["name"]
					state = p["state"]
					print("block %s %s" % (block, str(state)))
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
								return

					district = blk.GetDistrict()
					stat = OCCUPIED if state == 1 else EMPTY
					district.DoBlockAction(blk, blockend, stat)
					
			elif cmd == "signal":
				for p in parms:
					sigName = p["name"]
					aspect = p["aspect"]
					
					try:
						sig = self.signals[sigName]
					except:
						return

					district = sig.GetDistrict()
					district.DoSignalAction(sig, aspect)
						
			elif cmd == "handswitch":
				for p in parms:
					hsName = p["name"]
					state = p["state"]
					
					try:
						hs = self.handswitches[hsName]
					except:
						return

					district = hs.GetDistrict()
					district.DoHandSwitchAction(hs, state)

			elif cmd == "settrain":
				for p in parms:
					block = p["block"]
					name = p["name"]
					loco = p["loco"]

					try:
						blk = self.blocks[block]
					except:
						print("unable to identify block (%s)" % block)
						blk = None

					if blk:
						tr = blk.GetTrain()
						if name is None:
							if tr:
								tr.RemoveFromBlock(blk)
							tr = None
						else:
							if tr:
								oldName = tr.GetName()
								if oldName and oldName != name:
									tr.SetName(name)
									self.trains[name] = tr
									try:
										del(self.trains[oldName])
									except:
										print("can't delete train %s from train list" % oldName)
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
		
	def raiseDisconnectEvent(self): # thread context
		evt = DisconnectEvent()
		wx.PostEvent(self, evt)

	def Request(self, req):
		if self.settings.dispatch:
			self.rrServer.SendRequest(req)
	
	def onDisconnectEvent(self, _):
		self.listener = None
		self.subscribed = False
		self.bSubscribe.SetLabel("Subscribe")
		print("Server socket closed")

	def OnClose(self, evt):
		print("Trains:")
		for trid, tr in self.trains.items():
			print("%s: %s" % (trid, tr.tstring()))
		try:
			self.listener.kill()
			self.listener.join()
		except:
			pass
		self.Destroy()
