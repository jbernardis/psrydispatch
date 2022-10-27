import wx

class TrackDiagram(wx.Panel):
	def __init__(self, frame, dlist): #screen, id, diagramBmp, offset):
		wx.Panel.__init__(self, frame, size=(100, 100), pos=(0,0), style=0)
		self.frame = frame
		self.screens = [d.screen for d in dlist]
		self.bgbmps =  [d.bitmap for d in dlist]
		self.offsets = [d.offset for d in dlist]
		self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

		self.showPosition = True

		self.tiles = {}
		self.text = {}
		self.bitmaps = {}
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
		self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

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
			if self.showPosition:
				self.frame.UpdatePositionDisplay(self.tx, self.ty)

	def OnLeftUp(self, evt):
		self.frame.ProcessClick(self.screens[0], (self.tx, self.ty))

	def OnRightUp(self, evt):
		self.frame.ProcessRightClick(self.screens[0], (self.tx, self.ty))

	def DrawTile(self, x, y, offset, bmp):
		self.tiles[(x*16+offset, y*16)] = bmp;
		self.Refresh()

	def DrawText(self, x, y, offset, text):
		self.text[(x*16+offset, y*16)] = text;
		self.Refresh()

	def DrawFixedBitmap(self, x, y, offset, bmp):
		self.bitmaps[x+offset, y] = bmp
		self.Refresh()

	def ClearText(self, x, y, offset):
		textKey = (x*16+offset, y*16)
		if textKey not in self.text:
			return
		del(self.text[textKey])
		self.Refresh()

	def OnPaint(self, evt):
		dc = wx.BufferedPaintDC(self)
		dc.SetTextForeground(wx.Colour(255, 0, 0))
		dc.SetTextBackground(wx.Colour(255, 255, 255))
		dc.SetBackgroundMode(wx.BRUSHSTYLE_SOLID)
		self.DrawBackground(dc)
		for bx, bmp in self.tiles.items():
			dc.DrawBitmap(bmp, bx[0], bx[1])
		for bx, bmp in self.bitmaps.items():
			dc.DrawBitmap(bmp, bx[0], bx[1])
		for bx, txt in self.text.items():
			dc.DrawText(txt, bx[0], bx[1])