import wx
import wx.lib.newevent
import wx.lib.agw.toasterbox as TB

import os
import json
import inspect

cmdFolder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))

from settings import Settings
from bitmaps import BitMaps
from tower import Towers
from hyde import Hyde
from trackdiagram import TrackDiagram
from tile import loadTiles

from constants import HyYdPt, LaKr, NaCl, screensList, EMPTY, OCCUPIED, CLEARED, TOGGLE, NORMAL, REVERSE, RED, GREEN
from listener import Listener
from rrserver import RRServer

(DeliveryEvent, EVT_DELIVERY) = wx.lib.newevent.NewEvent() 
(DisconnectEvent, EVT_DISCONNECT) = wx.lib.newevent.NewEvent() 

class Node:
	def __init__(self, screen, bitmapName, offset):
		self.screen = screen
		self.bitmap = bitmapName
		self.offset = offset

useCameraDiagrams = False

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
		self.diagrams = {
			HyYdPt: Node(HyYdPt, self.bitmaps.diagrams.HydeYardPortCam  if useCameraDiagrams else self.bitmaps.diagrams.HydeYardPort, 0),
			LaKr:   Node(LaKr,   self.bitmaps.diagrams.LathamKrulishCam if useCameraDiagrams else self.bitmaps.diagrams.LathamKrulish, 2544 if singlePage else 0),
			NaCl:   Node(NaCl,   self.bitmaps.diagrams.NassauCliffCam   if useCameraDiagrams else self.bitmaps.diagrams.NassauCliff, 5088 if singlePage else 0)
		}
		if self.settings.pages == 1:  # set up a single ultra-wide display accross 3 monitors
			dp = TrackDiagram(self, [self.diagrams[sn] for sn in screensList])
			dp.SetPosition((20, 20))
			w, h = dp.GetSize()
			self.panels = {self.diagrams[sn].screen : dp for sn in screensList}  # all 3 screens just point to the same diagram

		else:  # set up three separate screens for a single monitor
			self.panels = {}
			for d in [self.diagrams[sn] for sn in screensList]:
				dp = TrackDiagram(self, [d])
				dp.Hide()
				dp.SetPosition((20, 20))
				self.panels[d.screen] = dp

			self.currentScreen = LaKr
			w, h = self.panels[self.currentScreen].GetSize()
			self.panels[self.currentScreen].Show()

			# add buttons to switch from screen to screen
			b = wx.Button(self, wx.ID_ANY, "Hyde/Yard/Port", pos=(500, h+50), size=(200, 50))
			self.Bind(wx.EVT_BUTTON, lambda event: self.SwapToScreen(HyYdPt), b)
			b = wx.Button(self, wx.ID_ANY, "Latham/Krulish", pos=(1145, h+50), size=(200, 50))
			self.Bind(wx.EVT_BUTTON, lambda event: self.SwapToScreen(LaKr), b)
			b = wx.Button(self, wx.ID_ANY, "Nassau/Cliff",   pos=(1790, h+50), size=(200, 50))
			self.Bind(wx.EVT_BUTTON, lambda event: self.SwapToScreen(NaCl), b)

		self.bSubscribe = wx.Button(self, wx.ID_ANY, "Subscribe", pos=(1900, h+30))
		self.Bind(wx.EVT_BUTTON, self.OnSubscribe, self.bSubscribe)

		self.SetMaxSize((w+50, h+200))
		self.SetSize((w+50, h+200))
		w, h = self.GetSize()
		wx.CallAfter(self.Initialize)

	def Initialize(self):
		self.listener = None
		self.subscribed = False
		self.Bind(EVT_DELIVERY, self.onDeliveryEvent)
		self.Bind(EVT_DISCONNECT, self.onDisconnectEvent)

		self.tiles, self.totiles, self.sigtiles = loadTiles(self.bitmaps)
		self.towers = Towers()
		self.towers.AddTower(Hyde("Hyde", self, HyYdPt))

		self.blocks =   self.towers.DefineBlocks(self.tiles)
		self.turnouts = self.towers.DefineTurnouts(self.totiles, self.blocks)
		self.signals =  self.towers.DefineSignals(self.sigtiles)
		self.buttons =  self.towers.DefineButtons(self.bitmaps.buttons)

		self.trains = []

		self.towers.Initialize()

		if self.settings.dispatch:
			self.turnoutMap = { (t.GetScreen(), t.GetPos()): t for t in self.turnouts.values() if not t.IsRouteControlled() }
			self.buttonMap = { (b.GetScreen(), b.GetPos()): b for b in self.buttons.values() }
			self.signalMap = { (s.GetScreen(), s.GetPos()): s for s in self.signals.values() }
		else:
			self.turnoutMap = {}
			self.buttonMap = {}
			self.signalMap = {}

		self.buttonsToClear = []

		self.towers.Draw()

		for tr in self.trains:
			tr.Draw()
		
		self.Bind(wx.EVT_TIMER, self.onTicker)
		self.ticker = wx.Timer(self)
		self.ticker.Start(1000)

		self.rrServer = RRServer()
		self.rrServer.SetServerAddress(self.settings.ipaddr, self.settings.serverport)
		
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
		try:
			to = self.turnoutMap[(screen, pos)]
		except KeyError:
			to = None

		if to:
			to.GetTower().PerformTurnoutAction(to)
			return

		try:
			btn = self.buttonMap[(screen, pos)]
		except KeyError:
			btn = None

		if btn:
			btn.GetTower().PerformButtonAction(btn)
			return

		try:
			sig = self.signalMap[(screen, pos)]
		except KeyError:
			sig = None

		if sig:
			sig.GetTower().PerformSignalAction(sig)

	def DrawTile(self, screen, pos, bmp):
		offset = self.diagrams[screen].offset
		self.panels[screen].DrawTile(pos[0], pos[1], offset, bmp)

	def DrawText(self, screen, pos, text):
		offset = self.diagrams[screen].offset
		self.panels[screen].DrawText(pos[0], pos[1], offset, text)

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
		#tb.SetPopupPosition((500, 500))
		tb.SetPopupPauseTime(5000)
		tb.SetPopupScrollSpeed(8)
		tb.SetPopupBackgroundColour(wx.Colour(255, 179, 154))
		tb.SetPopupTextColour(wx.Colour(0, 0, 0))
		tb.SetPopupText(message)
		tb.SetPopupTextFont(self.popupFont)
		print("POPUP: %s" % message)
		tb.Play()

	def OnSubscribe(self, _):
		if self.subscribed:
			self.listener.kill()
			self.listener.join()
			self.listener = None
			self.subscribed = False
			self.bSubscribe.SetLabel("Subscribe")
		else:
			print("trying to subscribe")
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
		print("got http cmd")
		evt = DeliveryEvent(data=jdata)
		wx.PostEvent(self, evt)

	def onDeliveryEvent(self, evt):
		for cmd, parms in evt.data.items():
			print("%s: %s" % (cmd, parms))
			if cmd == "turnout":
				for turnout, state in parms.items():
					try:
						to = self.turnouts[turnout]
					except KeyError:
						return
					
					tower = to.GetTower()
					st = REVERSE if state == "R" else NORMAL

					tower.DoTurnoutAction(to, st)

			elif cmd == "block":
				for block, state in parms.items():
					print("block command for %s" % block)
					try:
						blk = self.blocks[block]
						blockend = None
					except KeyError:
						if block.endswith(".E") or block.endswith(".W"):
							blockend = block[-1]
							block = block[:-2]
							print("Stopping block %s %s" % (block, blockend))
							try:
								blk = self.blocks[block]
							except KeyError:
								return

					tower = blk.GetTower()
					stat = OCCUPIED if state == 1 else EMPTY
					tower.DoBlockAction(blk, blockend, stat)
						
			elif cmd == "signal":
				sigName = parms[0]
				asp = parms[1]
				
				try:
					sig = self.signals[sigName]
				except:
					return

				aspect = GREEN if asp == 1 else RED

				tower = sig.GetTower()
				tower.DoSignalAction(sig, aspect)

		
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
		try:
			self.listener.kill()
			self.listener.join()
		except:
			pass
		self.Destroy()
