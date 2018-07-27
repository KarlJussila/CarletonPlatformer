import pygame as pg
import random
from settings import *
from sprites import *
from tilemap import *
from collisionDetection import *
from userInput import *
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
		self.music = pg.mixer.music.load(FILEPATH +"caveMusic.mp3")
		self.events = processInput
		self.menuEvents = menuInput
		self.level = "level2.txt"
		self.bckimgs = []
		self.rightWall = False
		self.leftWall = False
		self.bkg = [[None for i in range(40)]for j in range(30)]
		#self.bkimgs = [pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "coalOre.png"), pg.image.load(FILEPATH + "coalOre.png"), pg.image.load(FILEPATH + "silverOre.png"), pg.image.load(FILEPATH + "emeraldOre.png"), pg.image.load(FILEPATH + "ironOre.png"), pg.image.load(FILEPATH + "goldOre.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png")]
		pg.mixer.music.play(-1, 0.0)
		#beutiful list
		self.bkimgs = [pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "coalOre.png"), pg.image.load(FILEPATH + "emeraldOre.png"), pg.image.load(FILEPATH + "ironOre.png") , pg.image.load(FILEPATH + "ironOre.png"), pg.image.load(FILEPATH + "ironOre.png"), pg.image.load(FILEPATH + "ironOre.png"), pg.image.load(FILEPATH + "coalOre.png"), pg.image.load(FILEPATH + "coalOre.png"), pg.image.load(FILEPATH + "coalOre.png")]
		
		#self.bkstrs = [FILEPATH + "stone.png",FILEPATH + "stone.png",FILEPATH + "stone.png",FILEPATH + "stone.png",FILEPATH + "coalOre.png",FILEPATH + "coalOre.png",FILEPATH + "silverOre.png",FILEPATH + "emeraldOre.png",FILEPATH + "ironOre.png",FILEPATH + "goldOre.png"]
		for c in self.bkimgs:
			dark = pg.Surface((c.get_width(), c.get_height()), flags=pg.SRCALPHA)
			dark.fill((100, 75, 75, 100))
			c.blit(dark, (0, 0), special_flags=pg.BLEND_RGBA_SUB)			
		for row in range(int(HEIGHT/20)):
			for col in range(int(WIDTH/20)):
				b = random.randint(0, 70)
				self.bkg[row][col] = self.bkimgs[b]
		               

	def load_data(self, file="level2.txt"):
		
		game_folder = path.dirname(__file__)
		assets_folder = path.join(game_folder, 'assets')
		self.tileImage = pg.image.load(path.join(assets_folder, TILE_IMAGE)).convert()
		self.map = Map(path.join(game_folder, file))

		self.camera = Camera(self.map.width, self.map.height)
		tileList = []
		for row, tiles in enumerate(self.map.data):
			for col, tile in enumerate(tiles):
				if tile != "." and tile != "\n":
					if tile == "s":
						newTile = Tile(self, col * TILE_SIZE, row * TILE_SIZE)
						tileList.append(newTile)
						    
					elif tile == "r":
						Turret(self, col * TILE_SIZE, row * TILE_SIZE, 20, 20, 1, 5, 1)
					elif tile == "l":
						Turret(self, col * TILE_SIZE, row * TILE_SIZE, 20, 20, -1, 5, -1)						
					elif tile == "e":
						self.endPoint = EndPoint(self, col * TILE_SIZE, row * TILE_SIZE)
					elif tile == "p":
						self.player = Player(self, col * TILE_SIZE, row * TILE_SIZE)
					elif tile == "i":
						spike(self, col * TILE_SIZE, row * TILE_SIZE, 20, 20, -1,)						
					else:
						Enemy1(self, col * TILE_SIZE, row * TILE_SIZE, 20, 20, -1, int(tile))
				else:
					if tileList != []:
						Platform(tileList,self)
						tileList = []
		if tileList != []:
			Platform(tileList,self)				
	def mainMenu(self):
		self.playing = False
		print("Opened main menu")
		while not self.playing:
			self.clock.tick(FPS)
			self.screen.fill(BACKGROUND_COLOR)
			clicked = self.menuEvents(self)
			for button in self.main_menu:
				button.update(clicked)
				button.draw()
			pg.display.flip()
	def new(self, level=None):

		self.ticks = 0
		self.level = level
		self.all_sprites = pg.sprite.Group()
		self.tiles = pg.sprite.Group()
		self.platforms = pg.sprite.Group()
		self.player_sprite = pg.sprite.Group()
		self.enemy_sprites = pg.sprite.Group()
		self.turret_sprites = pg.sprite.Group()
		self.projectile_sprites = pg.sprite.Group()
		self.endpoint_sprites = pg.sprite.Group()
		self.button_sprites = pg.sprite.Group()
		self.main_menu = pg.sprite.Group()
		self.game_over_menu = pg.sprite.Group()

		buttonImage = pg.Surface((100, 35))
		buttonImage.fill((0,220,0))

		buttonHoverImage = pg.Surface((100, 35))
		buttonHoverImage.fill((0,255,0))

		#Main Menu
		self.level1Button = Button(self, 100, 100, buttonImage, buttonHoverImage, lambda: self.new("level1.txt"), self.main_menu)
		self.level2Button = Button(self, 100, 200, buttonImage, buttonHoverImage, lambda: self.new("level2.txt"), self.main_menu)
		self.level3Button = Button(self, 100, 300, buttonImage, buttonHoverImage, lambda: self.new("level2.txt"), self.main_menu)

		#Game Over
		self.mainMenuButton = Button(self, 100, 100, buttonImage, buttonHoverImage, self.mainMenu, self.game_over_menu)
		self.restartButton = Button(self, 100, 200, buttonImage, buttonHoverImage, lambda: self.new(self.level), self.game_over_menu)

		if level == None:
			self.mainMenu()

		self.load_data(level)

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
		self.player.rect.midbottom = self.player.pos
		
		self.ticks += 1

	def draw(self):
		#Background
		for row in range(int(HEIGHT/20)):
			for col in range(int(WIDTH/20)):
				self.screen.blit(self.bkg[row][col],(col*20,row*20))
				

		for sprite in self.all_sprites:
			cameraRect = self.camera.apply(sprite)    
			self.screen.blit(sprite.image, cameraRect)

		#Update the display
		pg.display.flip()

	def displayMainMenu(self):
		self.screen.fill(BACKGROUND_COLOR)
		self.drawText(TITLE, 48, (50,50,50), WIDTH/2, HEIGHT * 1/4)
		self.drawText("(Press any key to play)", 20, (50,50,50), WIDTH/2, HEIGHT * 2/3)
		pg.display.flip()
		self.waitForKey()

	def gameOverMenu(self):
		self.playing = False
		while not self.playing:
			self.clock.tick(FPS)
			self.screen.fill(BACKGROUND_COLOR)
			clicked = self.menuEvents(self)
			for button in self.game_over_menu:
				button.update(clicked)
				button.draw()
			pg.display.flip()

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
while g.running:
	g.new()
	

pg.quit()