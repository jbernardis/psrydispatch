import wx
import wx.lib.newevent
import os
import json

from bitmaps import BitMaps
from tower import Towers
from hyde import Hyde
from trackdiagram import TrackDiagram
from tile import loadTiles

from constants import HyYdPt, LaKr, NaCl, screensList
from listener import Listener

(DeliveryEvent, EVT_DELIVERY) = wx.lib.newevent.NewEvent() 
(DisconnectEvent, EVT_DISCONNECT) = wx.lib.newevent.NewEvent() 

class Node:
	def __init__(self, name, bitmapName):
		self.name = name
		self.bitmapName = bitmapName
		self.panel = None

useCameraDiagrams = False

class MainFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, size=(900, 800), style=wx.DEFAULT_FRAME_STYLE)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		vsz = wx.BoxSizer(wx.VERTICAL)
		hsz = wx.BoxSizer(wx.HORIZONTAL)
		self.bitmaps = BitMaps(os.path.join(".", "bitmaps"))
		self.diagrams = {
			HyYdPt: Node(HyYdPt, self.bitmaps.diagrams.HydeYardPortCam  if useCameraDiagrams else self.bitmaps.diagrams.HydeYardPort),
			LaKr:   Node(LaKr,   self.bitmaps.diagrams.LathamKrulishCam if useCameraDiagrams else self.bitmaps.diagrams.LathamKrulish),
			NaCl:   Node(NaCl,   self.bitmaps.diagrams.NassauCliffCam   if useCameraDiagrams else self.bitmaps.diagrams.NassauCliff)
		}
		for sn, d in self.diagrams.items():
			dp = TrackDiagram(self, sn, d.bitmapName, d.name)
			dp.Hide()
			dp.SetPosition((20, 20))
			d.panel = dp

		self.currentScreen = LaKr
		w, h = self.diagrams[self.currentScreen].panel.GetSize()
		self.diagrams[self.currentScreen].panel.Show()

		b = wx.Button(self, wx.ID_ANY, "doit", pos=(30, h+30))
		self.Bind(wx.EVT_BUTTON, self.OnDoit, b)
		b = wx.Button(self, wx.ID_ANY, "doit2", pos=(110, h+30))
		self.Bind(wx.EVT_BUTTON, self.OnDoit2, b)
		b = wx.Button(self, wx.ID_ANY, "doit3", pos=(190, h+30))
		self.Bind(wx.EVT_BUTTON, self.OnDoit3, b)

		b = wx.Button(self, wx.ID_ANY, "Hyde/Yard/Port", pos=(500, h+50), size=(200, 50))
		self.Bind(wx.EVT_BUTTON, lambda event: self.SwapToScreen(HyYdPt), b)
		b = wx.Button(self, wx.ID_ANY, "Latham/Krulish", pos=(1145, h+50), size=(200, 50))
		self.Bind(wx.EVT_BUTTON, lambda event: self.SwapToScreen(LaKr), b)
		b = wx.Button(self, wx.ID_ANY, "Nassau/Cliff",   pos=(1790, h+50), size=(200, 50))
		self.Bind(wx.EVT_BUTTON, lambda event: self.SwapToScreen(NaCl), b)

		self.bSubscribe = wx.Button(self, wx.ID_ANY, "Subscribe", pos=(1900, h+30))
		self.Bind(wx.EVT_BUTTON, self.OnSubscribe, self.bSubscribe)

		self.SetSize((w+50, h+200))
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

		self.towers.Initialize()

		self.turnoutMap = { (t.GetScreen(), t.GetPos()): t for t in self.turnouts.values() if not t.IsRouteControlled() }
		print(str(list(self.turnoutMap.keys())))
		self.buttonMap = { (b.GetScreen(), b.GetPos()): b for b in self.buttons.values() }
		print(str(list(self.buttonMap.keys())))
		self.towers.Draw()

	def ProcessClick(self, screen, pos):
		print("Check maps for (%s, (%d, %d)" % (screen, pos[0], pos[1]))
		try:
			to = self.turnoutMap[(screen, pos)]
		except KeyError:
			to = None

		if to:
			print("turnout %s" % to.GetName())
			return

		try:
			btn = self.buttonMap[(screen, pos)]
		except KeyError:
			btn = None

		if btn:
			btn.GetTower().PerformButtonAction(btn)
			return

		print("ignoring click")

	def DrawTile(self, screen, pos, bmp):
		self.diagrams[screen].panel.DrawTile(pos[0], pos[1], bmp)

	def SwapToScreen(self, screen):
		if screen not in screensList:
			return False
		if screen == self.currentScreen:
			return True
		self.diagrams[screen].panel.Show()
		self.diagrams[self.currentScreen].panel.Hide()
		self.currentScreen = screen
		return True

	def OnDoit(self, _):
		for b in self.blocks.values():
			b.Draw()
		#for t in self.turnouts.values():
			#t.Draw(self)
			
	def OnDoit2(self, evt):
		self.blocks["HydeWW"].SetOccupied(refresh=True)
			
	def OnDoit3(self, evt):
		pass

	def OnSubscribe(self, _):
		if self.subscribed:
			self.listener.kill()
			self.listener.join()
			self.listener = None
			self.subscribed = False
			self.bSubscribe.SetLabel("Subscribe")
		else:
			print("tryiong to subscrube")
			ip = "192.168.1.138"
			pt = 9003
			self.listener = Listener(self, ip, pt)
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
			if cmd == "turnout":
				for turnout, state in parms.items():
					print("set turnout (%s) to (%s)" % (turnout, state))
					try:
						to = self.turnouts[turnout]
					except KeyError:
						print("don't know that turnout")
					else:
						if state.lower() == "normal":
							to.SetNormal(refresh=True)

						elif state.lower() == "reverse":
							to.SetReverse(refresh=True)

						else:
							print("don't know that state")

			elif cmd == "block":
				for block, state in parms.items():
					print("set block (%s) to (%s)" % (block, state))
					try:
						blk = self.blocks[block]
					except KeyError:
						print("dont know that block")
					else:
						if state.lower() == "occupied":
							blk.SetOccupied(refresh=True)

						elif state.lower() == "empty":
							blk.SetOccupied(False, refresh=True)
						
						else:
							print("don't know that state")
			else:
				print("some other command")
		
	def raiseDisconnectEvent(self): # thread context
		evt = DisconnectEvent()
		wx.PostEvent(self, evt)
	
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


class App(wx.App):
	def OnInit(self):
		self.frame = MainFrame()
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True

app = App(False)
app.MainLoop()