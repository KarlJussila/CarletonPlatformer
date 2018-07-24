import pygame as pg
import random
from settings import *
from sprites import *
from tilemap import *
from collisionDetection import *
from userInput import processInput
from os import path
import sys


class Game:
	def __init__(self):
		self.running = True
		pg.init()
		pg.mixer.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		self.font_name = pg.font.match_font(FONT_NAME)
		self.events = processInput
		self.bckimgs = []
		self.rightWall = False
		self.leftWall = False
		self.bkg = [[None for i in range(40)]for j in range(30)]
		#self.bkimgs = [pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\coalOre.png"), pg.image.load("assets\\coalOre.png"), pg.image.load("assets\\silverOre.png"), pg.image.load("assets\\emeraldOre.png"), pg.image.load("assets\\ironOre.png"), pg.image.load("assets\\goldOre.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png")]
		#beutiful list
		self.bkimgs = [pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\stone.png"), pg.image.load("assets\\coalOre.png"), pg.image.load("assets\\emeraldOre.png"), pg.image.load("assets\\ironOre.png") , pg.image.load("assets\\ironOre.png"), pg.image.load("assets\\ironOre.png"), pg.image.load("assets\\ironOre.png"), pg.image.load("assets\\coalOre.png"), pg.image.load("assets\\coalOre.png"), pg.image.load("assets\\coalOre.png")]
		
		#self.bkstrs = ["assets\\stone.png","assets\\stone.png","assets\\stone.png","assets\\stone.png","assets\\coalOre.png","assets\\coalOre.png","assets\\silverOre.png","assets\\emeraldOre.png","assets\\ironOre.png","assets\\goldOre.png"]
		for c in self.bkimgs:
			
			dark = pg.Surface((c.get_width(), c.get_height()), flags=pg.SRCALPHA)
			dark.fill((100, 75, 75, 100))
			c.blit(dark, (0, 0), special_flags=pg.BLEND_RGBA_SUB)			
		for row in range(int(HEIGHT/20)):
			for col in range(int(WIDTH/20)):
				b = random.randint(0, 70)
				print(b, col)
				self.bkg[row][col] = self.bkimgs[b]
				
		
		
		               

	def load_data(self, file="level1.txt"):
		game_folder = path.dirname(__file__)
		assets_folder = path.join(game_folder, 'assets')
		self.tileImage = pg.image.load(path.join(assets_folder, TILE_IMAGE)).convert()
		self.map = Map(path.join(game_folder, 'level1.txt'))

		self.camera = Camera(self.map.width, self.map.height)
		tileList = []
		for row, tiles in enumerate(self.map.data):
			for col, tile in enumerate(tiles):
				if tile != "." and tile != "\n":
					if tile == "s":
						newTile = Tile(self, col * TILE_SIZE, row * TILE_SIZE)
						tileList.append(newTile)
						    
					elif tile == "r":
						TurretR(self, col * TILE_SIZE, row * TILE_SIZE, 20, 20, 1, 5)
					elif tile == "l":
						TurretL(self, col * TILE_SIZE, row * TILE_SIZE, 20, 20, 1, 5)						
					elif tile == "e":
						self.endPoint = EndPoint(self, col * TILE_SIZE, row * TILE_SIZE)
					elif tile == "p":
						self.player = Player(self, col * TILE_SIZE, row * TILE_SIZE)
					else:
						Enemy1(self, col * TILE_SIZE, row * TILE_SIZE, 20, 20, -1, int(tile))
				else:
					if tileList != []:
						Platform(tileList,self)
						tileList = []
		if tileList != []:
			Platform(tileList,self)				

	def new(self):

		self.ticks = 0

		self.all_sprites = pg.sprite.Group()
		self.tiles = pg.sprite.Group()
		self.platforms = pg.sprite.Group()
		self.player_sprite = pg.sprite.Group()
		self.enemy_sprites = pg.sprite.Group()
		self.turret_sprites = pg.sprite.Group()
		self.projectile_sprites = pg.sprite.Group()
		self.endpoint_sprites = pg.sprite.Group()

		self.load_data()

		self.all_sprites.add(self.player)
		self.player_sprite.add(self.player)

		self.run()

	def run(self):
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events(self)
			self.update()
			self.draw()

	def update(self):
		self.player.update()
		for enemy in self.enemy_sprites:
			enemy.update()
		for proj in self.projectile_sprites:
			proj.update()
		self.camera.update(self.player)

		#Collision detection
		collisions(self)
		
		self.ticks += 1

	# def events(self):
	# 	for event in pg.event.get():
	# 		if event.type == pg.QUIT:
	# 			if self.playing:
	# 				pg.display.quit()
	# 				pg.quit()
	# 				sys.exit()
	# 			self.running = False
	# 		if event.type == pg.KEYDOWN:
	# 			if event.key == pg.K_SPACE:
	# 				self.player.jump()

	def draw(self):
		#Background
		for row in range(int(HEIGHT/20)):
			for col in range(int(WIDTH/20)):
				 
				self.screen.blit(self.bkg[row][col],(col*20,row*20))
				

		for sprite in self.all_sprites:
			self.screen.blit(sprite.image, self.camera.apply(sprite))

		#Update the display
		pg.display.flip()

	def displayMainMenu(self):
		self.screen.fill(BACKGROUND_COLOR)
		self.drawText(TITLE, 48, (50,50,50), WIDTH/2, HEIGHT * 1/4)
		self.drawText("(Press any key to play)", 20, (50,50,50), WIDTH/2, HEIGHT * 2/3)
		pg.display.flip()
		self.waitForKey()

	def displayGameOverScreen(self):
		if not self.running:
			self.new()
		self.screen.fill(BACKGROUND_COLOR)
		self.drawText("Game Over", 48, (50,50,50), WIDTH/2, HEIGHT * 1/4)
		self.drawText("(Press any key to restart)", 20, (50,50,50), WIDTH/2, HEIGHT * 2/3)
		pg.display.flip()
		self.waitForKey()

	# def displayVictoryScreen(self):
	# 	if not self.running:
	# 		return
	# 	self.screen.fill(BACKGROUND_COLOR)
	# 	self.drawText("Congratulations!", 48, (50,50,50), WIDTH/2, HEIGHT * 1/4)
	# 	self.drawText("(Press any key to restart)", 20, (50,50,50), WIDTH/2, HEIGHT * 2/3)
	# 	pg.display.flip()
	# 	self.waitForKey()

	def waitForKey(self):
		waiting = True
		while waiting:
			self.clock.tick(FPS)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					waiting = False
					self.running = False
				if event.type == pg.KEYDOWN:
					waiting = False


	def drawText(self, text, size, color, x, y):
		font = pg.font.Font(self.font_name, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		self.screen.blit(text_surface, text_rect)

g = Game()
g.displayMainMenu()
while g.running:
	g.new()
	g.displayGameOverScreen()

pg.quit()