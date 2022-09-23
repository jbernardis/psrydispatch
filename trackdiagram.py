import wx

class TrackDiagram(wx.Panel):
	def __init__(self, frame, dlist): #screen, id, diagramBmp, offset):
		wx.Panel.__init__(self, frame, size=(100, 100), pos=(0,0), style=0)
		self.frame = frame
		self.screens = [d.screen for d in dlist]
		self.bgbmps =  [d.bitmap for d in dlist]
		self.offsets = [d.offset for d in dlist]

		self.tiles = {}
		self.text = {}
		self.tx = 0
		self.ty = 0

		self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

		w = 0;
		for b in self.bgbmps:
			w += b.GetWidth()
		h = self.bgbmps[0].GetHeight()  # assume all the same height

		self.SetSize((w, h))
		self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_MOTION, self.OnMotion)
		self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

	def DrawBackground(self, dc):
		for i in range(len(self.bgbmps)):
			dc.DrawBitmap(self.bgbmps[i], self.offsets[i], 0)

	def OnMotion(self, evt):
		pt = evt.GetPosition()
		ntx = int(pt.x/16)
		nty = int(pt.y/16)
		if ntx != self.tx or nty != self.ty:
			self.tx = ntx
			self.ty = nty
			#print("%d %d" % (self.tx, self.ty))
			#print("%d %d  <=> %d %d" % (self.tx, self.ty, pt.x, pt.y))

	def OnLeftUp(self, evt):
		self.frame.ProcessClick(self.screens[0], (self.tx, self.ty))

	def DrawTile(self, x, y, offset, bmp):
		self.tiles[(x*16+offset, y*16)] = bmp;
		self.Refresh()

	def DrawText(self, x, y, offset, text):
		print("adding %s to text strings" % text)
		self.text[(x*16+offset, y*16)] = text;
		self.Refresh()

	def OnPaint(self, evt):
		dc = wx.PaintDC(self)
		dc.SetTextForeground(wx.Colour(255, 0, 0))
		dc.SetTextBackground(wx.Colour(255, 255, 255))
		dc.SetBackgroundMode(wx.BRUSHSTYLE_SOLID)
		self.DrawBackground(dc)
		for bx, bmp in self.tiles.items():
			dc.DrawBitmap(bmp, bx[0], bx[1])
		for bx, txt in self.text.items():
			print("drawing (%s)" % txt)
			dc.DrawText(txt, bx[0], bx[1])