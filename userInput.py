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
		elif event.type == pg.KEYDOWN:
			if event.key == pg.K_SPACE:
				game.player.jump()
			if event.key == pg.K_a:
				game.player.onWall = False
				
				
		else:
			game.player.onWall = False
			game.player.pos.x +=1
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
		elif event.type == pg.MOUSEBUTTONDOWN:
			return True

#Input processing for level editor
def editorInput(game):
	#Loop through events
	for event in pg.event.get():
		#Close window event
		if event.type == pg.QUIT:
			#Close game
			pg.display.quit()
			pg.quit()
			sys.exit()
			game.running = False
		elif event.type == pg.KEYDOWN:
			if event.key == pg.K_t:
				game.editTile = "s"
			elif event.key == pg.K_e:
				game.editTile = "e"
			elif event.key == pg.K_i:
				game.editTile = "i"
			elif event.key == pg.K_n:
				game.editTile = "n"
			elif event.key == pg.K_p:
				game.editTile = "p"
			elif event.key == pg.K_l:
				game.editTile = "l"
			elif event.key == pg.K_r:
				game.editTile = "r"			
			elif event.key == pg.K_PERIOD:
				game.editTile = "."
			elif event.key == pg.K_1:
				game.editTile = "1"
			elif event.key == pg.K_2:
				game.editTile = "2"
			elif event.key == pg.K_3:
				game.editTile = "3"
			elif event.key == pg.K_4:
				game.editTile = "4"
			elif event.key == pg.K_5:
				game.editTile = "5"
			elif event.key == pg.K_6:
				game.editTile = "6"
			elif event.key == pg.K_7:
				game.editTile = "7"
			elif event.key == pg.K_8:
				game.editTile = "8"
			elif event.key == pg.K_9:
				game.editTile = "9"
			elif event.key == pg.K_BACKQUOTE:
				print("Saved")
				game.saveLevel()
		elif event.type == pg.MOUSEBUTTONDOWN:
			return True