import pygame as pg
import random
from settings import *
from sprites import *
from tilemap import *
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
					elif tile == "t":
						Turret(self, col * TILE_SIZE, row * TILE_SIZE, 20, 20, 1, 5)
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

	def new(self):

		self.ticks = 0

		self.all_sprites = pg.sprite.Group()
		self.tiles = pg.sprite.Group()
		self.platforms = pg.sprite.Group()
		self.player_sprite = pg.sprite.Group()
		self.enemy_sprites = pg.sprite.Group()
		self.turret_sprites = pg.sprite.Group()
		self.projectile_sprites = pg.sprite.Group()

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
		hits = pg.sprite.spritecollide(self.player, self.platforms, False)
		if hits:
			for hit in hits:
				#Up
				if self.player.vel.y < 0:
					if self.player.vel.x < 0:
						#Bottom Collision
						if self.player.lastPos.y + TILE_SIZE > hit.rect.bottom:
							self.player.vel.y = 0
							self.player.pos.y = hit.rect.bottom + TILE_SIZE + 1
						#Right Collision
						else:
							self.player.vel.x = 0
							self.player.pos.x = hit.rect.right + (TILE_SIZE/2) + 1
					elif self.player.vel.x > 0:
						#Bottom Collision
						if self.player.lastPos.y + TILE_SIZE > hit.rect.bottom:
							self.player.vel.y = 0
							self.player.pos.y = hit.rect.bottom + TILE_SIZE + 1
						#Left Collision
						else:
							self.player.vel.x = 0
							self.player.pos.x = hit.rect.left - (TILE_SIZE/2) - 1
					#Bottom Collision
					else:
						self.player.vel.y = 0
						self.player.pos.y = hit.rect.bottom + TILE_SIZE
				#Down
				elif self.player.vel.y > 0:
					if self.player.vel.x < 0:
						#Top Collison
						if self.player.lastPos.y < hit.rect.top:
							self.player.vel.y = 0
							self.player.pos.y = hit.rect.top - 1
							self.player.onGround = True
						#Right Collision
						else:
							self.player.vel. x = 0
							self.player.pos.x = hit.rect.right + (TILE_SIZE/2) + 1
					elif self.player.vel.x > 0:
						#Top Collision
						if self.player.lastPos.y < hit.rect.top:
							self.player.vel.y = 0
							self.player.pos.y = hit.rect.top - 1
							self.player.onGround = True
						#Left Collision
						else:
							self.player.vel.x = 0
							self.player.pos.x = hit.rect.left - (TILE_SIZE/2) - 1
					#Top Collision
					else:
						self.player.vel.y = 0
						self.player.pos.y = hit.rect.top - 1
						self.player.onGround = True
				#On Ground
				else:
					if self.player.vel.x < 0:
						pass
					else:
						pass



		if(self.player.rect.top > self.map.height):
			self.player.die("You have fallen out of the world!")

		for enemy in self.enemy_sprites:
			if enemy.rect.colliderect(self.player.rect):
				if self.player.vel.y > 0:
					if(self.player.lastPos.y < enemy.rect.top):
						enemy.die()
						self.player.vel.y = -12
						break
				self.player.die("You have run into an enemy :/")

		for proj in self.projectile_sprites:
			if proj.rect.colliderect(self.player.rect):
				self.player.die("Oh no, you have been shot.")
				break

		if self.endPoint.rect.colliderect(self.player.rect):
			for sprite in self.all_sprites:
				sprite.kill()
			self.load_data()

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
		self.screen.fill(BACKGROUND_COLOR)

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