import pygame as pg
import sys

def processInput(game):
	for event in pg.event.get():
		if event.type == pg.QUIT:
			if game.playing:
				pg.display.quit()
				pg.quit()
				sys.exit()
			game.running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_SPACE:
				game.player.jump()

def menuInput(game):
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.display.quit()
			pg.quit()
			sys.exit()
			game.running = False
		if event.type == pg.MOUSEBUTTONDOWN:
			return True