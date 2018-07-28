#Imports
import pygame as pg
import random
from settings import *
from sprites import *
from tilemap import *
from collisionDetection import *
from userInput import *
from os import path
import sys

#Game class - Game object controls all aspects of the game
class Game:
	def __init__(self):

		#Starting game
		self.running = True
		pg.init()
		pg.mixer.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()

		#Initializing variables
		self.font_name = pg.font.match_font(FONT_NAME)
		self.music = pg.mixer.music.load(FILEPATH +"solarspire-jungle.wav")
		self.events = processInput
		self.menuEvents = menuInput
		self.level = "level2.txt"
		self.rightWall = False
		self.leftWall = False

		#Background music
		pg.mixer.music.play(-1, 0.0)

		#Distribution of backgroun images
		self.bkimgs = [pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "stone.png"), pg.image.load(FILEPATH + "coalOre.png"), pg.image.load(FILEPATH + "emeraldOre.png"), pg.image.load(FILEPATH + "ironOre.png") , pg.image.load(FILEPATH + "ironOre.png"), pg.image.load(FILEPATH + "ironOre.png"), pg.image.load(FILEPATH + "ironOre.png"), pg.image.load(FILEPATH + "coalOre.png"), pg.image.load(FILEPATH + "coalOre.png"), pg.image.load(FILEPATH + "coalOre.png")]
		
		#Selecting random background
		self.bkg = [[None for i in range(40)]for j in range(30)]

		for c in self.bkimgs:
			dark = pg.Surface((c.get_width(), c.get_height()), flags=pg.SRCALPHA)
			dark.fill((100, 75, 75, 100))
			c.blit(dark, (0, 0), special_flags=pg.BLEND_RGBA_SUB)			
		for row in range(int(HEIGHT/20)):
			for col in range(int(WIDTH/20)):
				b = random.randint(0, 70)
				self.bkg[row][col] = self.bkimgs[b]
		               
				
	#Level loading function
	def load_data(self, file="level2.txt"):
		
		#Accessing file
		game_folder = path.dirname(__file__)
		assets_folder = path.join(game_folder, 'assets')
		self.tileImage = pg.image.load(path.join(assets_folder, TILE_IMAGE)).convert()

		#Creating map object
		self.map = Map(path.join(game_folder, file))

		#Building objects for map
		self.camera = Camera(self.map.width, self.map.height)
		tileList = []
		for row, tiles in enumerate(self.map.data):
			for col, tile in enumerate(tiles):
				if tile != "." and tile != "\n":
					#Tile (ground)
					if tile == "s":
						newTile = Tile(self, col * TILE_SIZE, row * TILE_SIZE)
						tileList.append(newTile)
					#Right turret
					elif tile == "r":
						Turret(self, col * TILE_SIZE, row * TILE_SIZE, 20, 20, 1, 5, 1)
					#Left turret
					elif tile == "l":
						Turret(self, col * TILE_SIZE, row * TILE_SIZE, 20, 20, -1, 5, -1)	
					#Endpoint (gold)					
					elif tile == "e":
						self.endPoint = EndPoint(self, col * TILE_SIZE, row * TILE_SIZE)
					#Player
					elif tile == "p":
						self.player = Player(self, col * TILE_SIZE, row * TILE_SIZE)
					#Spikes
					elif tile == "i":
						Spike(self, col * TILE_SIZE, row * TILE_SIZE, 20, 10)	
					elif tile == "n":
						Enemy2(self, col * TILE_SIZE, row * TILE_SIZE, 20, 20)					
					#Green cave creature			
					else:
						Enemy1(self, col * TILE_SIZE, row * TILE_SIZE, 20, 20, -1, int(tile))
				else:
					if tileList != []:
						Platform(tileList,self)
						tileList = []
		if tileList != []:
			Platform(tileList,self)

	#Main menu function
	def mainMenu(self):

		self.playing = False

		#Tick loop
		while not self.playing:
			self.clock.tick(FPS)

			#Background fill
			self.screen.fill(BACKGROUND_COLOR)

			#Event handling
			clicked = self.menuEvents(self)
			for button in self.main_menu:
				button.update(clicked)

				#Drawing buttons
				button.draw()

			#Update the display
			pg.display.flip()

	#Creating a new instance of the game, either a level or the menu
	def new(self, level=None):

		#Initializing variables
		self.ticks = 0
		self.level = level

		#Sprite groups
		self.all_sprites = pg.sprite.Group()
		self.tiles = pg.sprite.Group()
		self.platforms = pg.sprite.Group()
		self.player_sprite = pg.sprite.Group()
		self.enemy_sprites = pg.sprite.Group()
		self.turret_sprites = pg.sprite.Group()
		self.projectile_sprites = pg.sprite.Group()
		self.spike_sprites = pg.sprite.Group()
		self.endpoint_sprites = pg.sprite.Group()
		self.button_sprites = pg.sprite.Group()
		self.main_menu = pg.sprite.Group()
		self.game_over_menu = pg.sprite.Group()

		#TEMPORARY BUTTON IMAGES
		buttonImage = pg.Surface((100, 35))
		buttonImage.fill((0,220,0))

		buttonHoverImage = pg.Surface((100, 35))
		buttonHoverImage.fill((0,255,0))
		########################

		#Main menu
		self.level1Button = Button(self, 100, 100, buttonImage, buttonHoverImage, lambda: self.new("level1.txt"), self.main_menu)
		self.level2Button = Button(self, 100, 200, buttonImage, buttonHoverImage, lambda: self.new("level2.txt"), self.main_menu)
		self.level3Button = Button(self, 100, 300, buttonImage, buttonHoverImage, lambda: self.new("level2.txt"), self.main_menu)

		#Game over menu
		self.mainMenuButton = Button(self, 100, 100, buttonImage, buttonHoverImage, self.mainMenu, self.game_over_menu)
		self.restartButton = Button(self, 100, 200, buttonImage, buttonHoverImage, lambda: self.new(self.level), self.game_over_menu)

		#Going to main menu if no level has been selected
		if level == None:
			self.mainMenu()

		#Loading level
		self.load_data(level)

		#Running game
		self.run()

	def run(self):
		self.playing = True
		
		#Tick loop
		while self.playing:
			self.clock.tick(FPS)

			#Event handling
			self.events(self)

			#Updating game
			self.update()

			#Drawing sprites
			self.draw()

	#General update function
	def update(self):
		#Updating player
		self.player.update()

		#Updating enemies
		for enemy in self.enemy_sprites:
			enemy.update()
		for proj in self.projectile_sprites:
			proj.update()

		#Updating camera position
		self.camera.update(self.player)

		#Collision detection
		collisions(self)
		self.player.rect.midbottom = self.player.pos
		
		#Incrementing ticks
		self.ticks += 1

	#Draw function
	def draw(self):
		#Background display
		for row in range(int(HEIGHT/20)):
			for col in range(int(WIDTH/20)):
				self.screen.blit(self.bkg[row][col],(col*20,row*20))
				
		#Displaying all sprites
		for sprite in self.all_sprites:
			cameraRect = self.camera.apply(sprite)    
			self.screen.blit(sprite.image, cameraRect)

		#Update the display
		pg.display.flip()

	#Game over menu
	def gameOverMenu(self):
		self.playing = False

		#Tick loop
		while not self.playing:
			self.clock.tick(FPS)

			#Background fill
			self.screen.fill(BACKGROUND_COLOR)

			#Event handling
			clicked = self.menuEvents(self)
			for button in self.game_over_menu:
				button.update(clicked)

				#Drawing buttons
				button.draw()

			#Updating display
			pg.display.flip()

	#---------DEPRECATED---------#
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
	#---------DEPRECATED---------#

	#Text drawing function
	def drawText(self, text, size, color, x, y):
		font = pg.font.Font(self.font_name, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		self.screen.blit(text_surface, text_rect)

#Creating game
g = Game()

#Main loop
while g.running:
	g.new()
	
#Quitting pygame
pg.quit()