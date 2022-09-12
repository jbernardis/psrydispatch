class Tower:
	def __init__(self, name, frame, screen):
		self.name = name
		self.frame = frame
		self.screen = screen

	def DefineBlocks(self, tiles):
		print("Tower %s does not have an implementation of DefineBlocks" % self.name)

	def DefineTurnouts(self, tiles):
		print("Tower %s does not have an implementation of DefineTurnouts" % self.name)

	def DefineSignals(self, tiles):
		print("Tower %s does not have an implementation of DefineSignals" % self.name)

	def DefineButtons(self, tiles):
		print("Tower %s does not have an implementation of DefineButtons" % self.name)

class Towers:
	def __init__(self):
		self.towers = {}

	def AddTower(self, tower):
		self.towers[tower.name] = tower

	def Initialize(self):
		for t in self.towers.values():
			t.Initialize()

	def Draw(self):
		for t in self.towers.values():
			t.Draw()

	def DefineBlocks(self, tiles):
		blocks = {}
		for t in self.towers.values():
			blocks.update(t.DefineBlocks(tiles))

		return blocks

	def DefineTurnouts(self, tiles, blocks):
		tos = {}
		for t in self.towers.values():
			tos.update(t.DefineTurnouts(tiles, blocks))

		return tos

	def DefineSignals(self, tiles):
		sigs = {}
		for t in self.towers.values():
			sigs.update(t.DefineSignals(tiles))

		return sigs

	def DefineButtons(self, tiles):
		btns = {}
		for t in self.towers.values():
			btns.update(t.DefineButtons(tiles))

		return btns
