#Imports
import pygame as pg
import sys

#Main input processing
def processInput(game):
	#Loop through events
	for event in pg.event.get():
		#Close window event
		if event.type == pg.QUIT:
			if game.playing:
				#Close game
				pg.display.quit()
				pg.quit()
				sys.exit()
			game.running = False
		#Player jump when spacebar is pressed
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_SPACE:
				game.player.jump()

#Menu input processing
def menuInput(game):
	#Loop through events
	for event in pg.event.get():
		#Close window event
		if event.type == pg.QUIT:
			#Close game
			pg.display.quit()
			pg.quit()
			sys.exit()
			game.running = False
		#Returning mouse clicks
		if event.type == pg.MOUSEBUTTONDOWN:
			return True