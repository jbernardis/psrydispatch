import wx

class TrackDiagram(wx.Panel):
	def __init__(self, frame, screen, diagramBmp, id):
		wx.Panel.__init__(self, frame, size=(100, 100), pos=(0,0), style=0)
		self.frame = frame
		self.screen = screen
		self.diagramBmp = diagramBmp
		self.id = id

		self.tiles = {}
		self.tx = 0
		self.ty = 0

		self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

		self.bg_bmp = diagramBmp
		w = self.bg_bmp.GetWidth()
		h = self.bg_bmp.GetHeight()

		self.SetSize((w, h))
		self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_MOTION, self.OnMotion)
		self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

	def DrawBackground(self, dc):
		dc.DrawBitmap(self.bg_bmp, 0, 0)

	def OnMotion(self, evt):
		pt = evt.GetPosition()
		self.tx = int(pt.x/16)
		self.ty = int(pt.y/16)
		#print("%d %d" % (self.tx, self.ty))
		#print("%d %d  <=> %d %d" % (self.tx, self.ty, pt.x, pt.y))

	def OnLeftUp(self, evt):
		self.frame.ProcessClick(self.screen, (self.tx, self.ty))

	def DrawTile(self, x, y, bmp):
		self.tiles[(x*16, y*16)] = bmp;
		self.Refresh()

	def OnPaint(self, evt):
		dc = wx.PaintDC(self)
		self.DrawBackground(dc)
		for bx, bmp in self.tiles.items():
			dc.DrawBitmap(bmp, bx[0], bx[1])