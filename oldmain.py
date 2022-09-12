import wx
import wx.lib.newevent
import json
import pprint

from tile import loadTiles
from block import defineBlocks
from turnout import defineTurnouts
from signal import defineSignals
from trackdiagram import TrackDiagram
from listener import Listener

DEVELOPMODE=True

(DeliveryEvent, EVT_DELIVERY) = wx.lib.newevent.NewEvent() 
(DisconnectEvent, EVT_DISCONNECT) = wx.lib.newevent.NewEvent() 

class MainFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, size=(900, 800), style=wx.DEFAULT_FRAME_STYLE)
		self.Bind(wx.EVT_CLOSE, self.onClose)

		self.listener = None
		self.subscribed = False

		self.diagram = TrackDiagram(self, 160, 54, 0)

		vsz = wx.BoxSizer(wx.VERTICAL)
		hsz = wx.BoxSizer(wx.HORIZONTAL)

		btnszr = wx.BoxSizer(wx.HORIZONTAL)
		b = wx.Button(self, wx.ID_ANY, "doit")
		self.Bind(wx.EVT_BUTTON, self.onDoit, b)
		btnszr.Add(b)
		b = wx.Button(self, wx.ID_ANY, "doit2")
		self.Bind(wx.EVT_BUTTON, self.onDoit2, b)
		btnszr.Add(b)
		self.bSubscribe = wx.Button(self, wx.ID_ANY, "Subscribe")
		self.Bind(wx.EVT_BUTTON, self.onSubscribe, self.bSubscribe)
		btnszr.Add(self.bSubscribe)

		vsz.AddSpacer(20)
		vsz.Add(self.diagram)
		vsz.AddSpacer(20)
		vsz.Add(btnszr)
		vsz.AddSpacer(20)

		hsz.AddSpacer(20)
		hsz.Add(vsz)
		hsz.AddSpacer(20)

		self.SetSizer(hsz)
		self.Layout()
		self.Fit()
		self.Bind(EVT_DELIVERY, self.onDeliveryEvent)
		self.Bind(EVT_DISCONNECT, self.onDisconnectEvent)
		wx.CallAfter(self.initialize)

	def initialize(self):
		self.tiles, self.totiles, self.sigtiles = loadTiles()
		self.blocks = defineBlocks(self.tiles)
		self.turnouts = defineTurnouts(self.totiles, self.blocks)
		self.signals = defineSignals(self.sigtiles)


	def onDoit(self, _):
		for b in self.blocks.values():
			b.draw(self.diagram)
		for t in self.turnouts.values():
			t.draw(self.diagram)
		for s in self.signals.values():
			s.draw(self.diagram)
			
	def onDoit2(self, evt):
		self.diagram.clear()
			
	def onClose(self, _):
		try:
			self.listener.kill()
			self.listener.join()
		except:
			pass
		self.Hide()
		self.Destroy()

	def onSubscribe(self, _):
		if self.subscribed:
			self.listener.kill()
			self.listener.join()
			self.listener = None
			self.subscribed = False
			self.bSubscribe.SetLabel("Subscribe")
		else:
			ip = "192.168.1.138"
			pt = 9003
			self.listener = Listener(self, ip, pt)
			if not self.listener.connect():
				print("Unable to estanlish connection with server")
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
		pprint.pprint(evt.data)
		for cmd, parms in evt.data.items():
			if cmd == "turnout":
				print("turnout command")
				for turnout, state in parms.items():
					print("set turnout (%s) to (%s)" % (turnout, state))
					try:
						to = self.turnouts[turnout]
					except KeyError:
						print("don't know that turnout")
					else:
						if state.lower() == "normal":
							if not to.normal:
								to.setNormal()
								to.draw(self.diagram, True)

						elif state.lower() == "reverse":
							if to.normal:
								to.setReverse()
								to.draw(self.diagram, True)

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
	
class App(wx.App):
	def OnInit(self):
		self.frame = MainFrame()
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True

import sys

if not DEVELOPMODE:
	ofp = open("tracker.out", "w")
	efp = open("tracker.err", "w")
	sys.stdout = ofp
	sys.stderr = efp

app = App(False)
app.MainLoop()

if not DEVELOPMODE:
    ofp.close()
    efp.close()
