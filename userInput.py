import pygame as pg

def processInput():
	for event in pg.event.get():
		if event.type == pg.QUIT:
			if self.playing:
				pg.display.quit()
				pg.quit()
				sys.exit()
			self.running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_SPACE:
				self.player.jump()