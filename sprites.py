#Imports
import pygame as pg
from settings import *
vec = pg.math.Vector2
from os import path

#Player class
class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		#Adding to sprite groups
		self.groups = game.all_sprites, game.player_sprite

		self.type = "p"

		#Sprite init function
		pg.sprite.Sprite.__init__(self, self.groups)

		#Initializing variables
		self.game = game
		
		self.image = pg.image.load(FILEPATH + PLAYER_IMG1).convert_alpha()
		self.dwarf1Left = self.image
		self.dwarf1Right = pg.transform.flip(self.image, True, False)
		self.dwarf2Left = pg.image.load(FILEPATH + PLAYER_IMG2).convert_alpha()
		self.dwarf2Right = pg.transform.flip(self.dwarf2Left,True,False)
		self.dwarf3Left = pg.image.load(FILEPATH + PLAYER_IMG3).convert_alpha()
		self.dwarf3Right = pg.transform.flip(self.dwarf3Left,True,False)
		self.dwarf4Left = pg.image.load(FILEPATH + PLAYER_IMG4).convert_alpha()
		self.dwarf4Right = pg.transform.flip(self.dwarf4Left,True,False)
		
		self.facing = 1
		self.imageDict = {"11":self.dwarf1Right,"12":self.dwarf2Right,"13":self.dwarf3Right, "14":self.dwarf4Right, "-11":self.dwarf1Left,"-12":self.dwarf2Left,"-13":self.dwarf3Left, "-14":self.dwarf4Left}
		self.imgNum = 1
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.pos = vec(x + (self.rect.width/2), y + 20)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)
		self.lastPos = self.pos
		self.onGround = False

	#Animating sprite
	def animate(self):
		if self.game.ticks % 2 == 0:
			self.imgNum +=1
			if self.imgNum == 5:
				self.imgNum = 1
			self.image = self.imageDict[str(self.facing) + str(self.imgNum)]

	#Updating player pos, vel, acc, etc.
	def update(self):

		#Checking onGround
		self.onGround = False
		for platform in self.game.platforms:
			if self.pos.y <= platform.rect.top and (platform.rect.collidepoint((self.rect.bottomright[0], self.rect.bottomright[1] + 1)) or platform.rect.collidepoint((self.rect.bottomleft[0], self.rect.bottomleft[1] + 1))):
				self.onGround = True

		#Saving last position
		self.lastPos = vec(self.pos.x, self.pos.y)

		#Setting acceleration due to gravity
		self.acc = vec(0, PLAYER_GRAV)

		#Canceling acceleration due to gravity if onGround
		if self.onGround:
			self.acc.y = 0
			self.vel.y = 0

		#Setting x acceleration based on user input
		keys = pg.key.get_pressed()
		if keys[pg.K_a] and not self.game.leftWall:
			self.game.rightWall = False
			self.facing = -1
			self.acc.x = -PLAYER_ACC
		if keys[pg.K_d] and not self.game.rightWall:
			self.game.leftWall = False
			self.acc.x = PLAYER_ACC
			self.facing = 1
		
		#Calculating velocity
		self.acc.x += self.vel.x * PLAYER_FRICTION
		self.vel += self.acc
		if(self.vel.y > 0):
			self.vel.y = min(30, self.vel.y)

		#Updating position
		self.pos += self.vel + 0.5 * self.acc

		if self.pos.x < 0:
			self.pos.x = 0

		#Updating player rectangle to match pos
		self.rect.midbottom = self.pos
		
		#Animating player sprite
		if abs(self.vel.x) > 1 and self.onGround:
			self.animate()
		else:
			if abs(self.vel.y) > 0:
				self.image = self.imageDict[str(self.facing) + "2"]
			else:
				self.image = self.imageDict[str(self.facing) + "1"]
		
	#Player jump function
	def jump(self):
		#Run only if the player is on the ground
		if self.onGround:
			#Set upward velocity and such
			self.vel.y = -18
			self.pos.y -= 1
			self.rect.top -= 2
			self.onGround = False

	#Kill the player
	def die(self, cause="You have died from unknown causes."):
		#Kill the sprite
		self.kill()

		#Stop the game
		self.game.playing = False

		#Print cause of death
		print(cause)

		#Displaying game over menu
		self.game.gameOverMenu()

#Green cave creature class
class Enemy1(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h, direction = -1, vel = 5):
		#Adding to sprite groups
		self.groups = game.all_sprites, game.enemy_sprites

		self.type = "0"

		#Sprite init function
		pg.sprite.Sprite.__init__(self, self.groups)

		#Initializing variables
		self.game = game
		self.image = pg.Surface((w, h))
		self.img = pg.image.load(FILEPATH + "enemy.png")
		self.img2 = pg.image.load(FILEPATH + "enemy2.png")
		self.image = self.img
		self.animate = 1
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.width = w
		self.height = h
		self.direction = direction
		self.vel = vel

	#Updating pos, direction, etc.
	def update(self):
		#Animating sprite
		if self.game.ticks % 5 == 0:
			if self.animate == 1:
				self.image = self.img2
				self.animate = 0
			else:
				self.image = self.img
				self.animate = 1

		#Moving enemy
		self.rect.x += self.vel * self.direction

		#Changing direction if necessary
		for tile in self.game.tiles:
			if tile.rect.colliderect(self.rect):
				self.direction *= -1

	#Kill the enemy
	def die(self):
		#Sprite kill
		self.kill()

class Enemy2(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h, direction = -1, vel = 5):
		#Adding to sprite groups
		self.groups = game.all_sprites, game.ghost_sprites

		self.type = "n"

		#Sprite init function
		pg.sprite.Sprite.__init__(self, self.groups)

		#Initializing variables
		self.game = game
		self.direction = 0
		self.directiony = 0
		self.image = pg.Surface((w, h))
		self.img = pg.image.load(FILEPATH + "ghost.png")
		self.img2 = pg.image.load(FILEPATH + "ghost2.png")
		self.image = self.img
		self.animate = 1
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.width = w
		self.height = h
			
		
		self.vel = vel

	#Updating pos, direction, etc.
	def update(self):
		#Animating sprite
		if self.game.ticks % 5 == 0:
			if self.animate == 1:
				self.image = self.img2
				self.animate = 0
			else:
				self.image = self.img
				self.animate = 1

		#Moving enemy
		if(self.game.player.pos.y > self.rect.y):
		        self.directiony = 1
		elif(self.game.player.pos.y < self.rect.y):
		        self.directiony = -1	
		else:
			self.directiony = 0
		if(self.game.player.pos.x > self.rect.x):
		        self.direction = 1
		elif(self.game.player.pos.x < self.rect.x):
		        self.direction = -1	
		else:
			self.direction = 0

		#Changing direction if necessary
						
					
			
		self.rect.x += self.vel * self.direction
		self.rect.y += self.vel * self.directiony	

	#Kill the enemy
	def die(self):
		#Sprite kill
		self.kill()
#--------------------PLEASE CHANGE TO BE LESS JANKY, EVAN--------------------#
class Spike(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		#Adding to sprite groups
		self.groups = game.all_sprites, game.spike_sprites

		self.type = "i"

		#Sprite init function
		pg.sprite.Sprite.__init__(self, self.groups)

		#Initializing variables
		self.game = game
		self.image = pg.Surface((20, 10))
		self.image = pg.image.load(FILEPATH + "spikes.png")
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y+10)
#--------------------PLEASE CHANGE TO BE LESS JANKY, EVAN--------------------#

#Turret class
class Turret(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h, d, vel = 5, delay = int(FPS * 2.5)):
		#Adding to sprite groups
		self.groups = game.all_sprites, game.turret_sprites

		self.type = "t"

		#Sprite init function
		pg.sprite.Sprite.__init__(self, self.groups)

		#Initializing variables
		self.direction = d
		self.game = game
		self.img = pg.image.load(FILEPATH + "turret.png")
		self.img2 = pg.transform.flip(self.img, True, False)
		self.image = pg.Surface((w, h))
		print(d)
		if(d == 1):
		        self.image = self.img
		else:
			self.image = self.img2
		
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.width = w
		self.height = h
		
		self.vel = vel
		self.delay = delay
		self.delay = int(FPS*2.5)

	#Turret update function
	def update(self):
		#Fire projectile
		self.fireProjectile()

	#Function to create new projectiles
	def fireProjectile(self):
		#Make new projectile every time it has reached the delay
		if self.game.ticks % self.delay == 0:
			Projectile(self.game, self)

	#Kill the turret
	def die(self):
		#Sprite kill
		self.kill()

#Turret projectile class
class Projectile(pg.sprite.Sprite):
	def __init__(self, game, parent):
		#Adding to sprite groups
		self.groups = game.all_sprites, game.projectile_sprites

		self.type = None

		#Sprite init function
		pg.sprite.Sprite.__init__(self, self.groups)

		#Initializing variables
		self.game = game
		self.img = pg.image.load(FILEPATH + "projectile.png")
		self.img2 = pg.transform.flip(self.img, True, False)
		self.parent = parent
		self.image = pg.Surface((10, 5))
		if self.parent.direction == 1:
			self.image = self.img
		else:
			self.image = self.img2
		self.rect = self.image.get_rect()
		self.rect.center = self.parent.rect.center
		self.width = 10
		self.height = 5

	#Updating pos, killing if necessary
	def update(self):
		#Moving projectile
		self.rect.x += self.parent.vel * self.parent.direction

		#If it's collided with a tile, kill it
		for tile in self.game.tiles:
			if tile.rect.colliderect(self.rect):
				self.kill()

		#If it's gone off the map, kill it
		if self.rect.left > self.game.map.width or self.rect.right < 0:
			self.kill()

#Tile class
class Tile(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		#Adding to sprite groups
		self.groups = game.all_sprites, game.tiles

		self.type = "s"

		#Sprite init function
		pg.sprite.Sprite.__init__(self, self.groups)

		#Initializing variables
		self.game = game
		self.image = game.tileImage
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

#Platform class, horizontal string of tiles
class Platform(pg.sprite.Sprite):
	def __init__(self, tiles, game):
		#Adding to sprite groups
		self.groups = game.platforms, game.all_sprites

		self.type = None

		#Sprite init function
		pg.sprite.Sprite.__init__(self, self.groups)

		#Initializing variables
		self.game = game
		self.tiles = tiles
		
		leftPos = game.map.width
		rightPos = 0
		topPos = game.map.height
		bottomPos = 0

		#Finding rectangle's sides
		for tile in tiles:
			if tile.rect.left < leftPos:
				leftPos = tile.rect.left
			if tile.rect.right > rightPos:
				rightPos = tile.rect.right
			if tile.rect.top < topPos:
				topPos = tile.rect.top
			if tile.rect.bottom > bottomPos:
				bottomPos = tile.rect.bottom
		self.rect = pg.Rect(leftPos, topPos, rightPos - leftPos, bottomPos - topPos)

		self.image = pg.Surface((self.rect.width, self.rect.height))
		self.image = game.tileImage

#End point (gold) class
class EndPoint(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		#Adding to sprite groups
		self.groups = game.all_sprites, game.endpoint_sprites

		self.type = "e"

		#Sprite init function
		pg.sprite.Sprite.__init__(self, self.groups)

		#Initializing variables
		self.game = game
		self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
		img = pg.image.load(FILEPATH + "goldOre.png")
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
#Button class
class Button(pg.sprite.Sprite):
	def __init__(self, game, x, y, image, hoverImage, function, group):
		#Adding to sprite groups
		self.groups = game.button_sprites, group

		#Sprite init function
		pg.sprite.Sprite.__init__(self, self.groups)

		#Initializing variables
		self.game = game
		self.noHoverImage = image
		self.hoverImage = hoverImage
		self.image = image
		self.x = x
		self.y = y
		self.rect = image.get_rect()
		self.rect.topleft = (x,y)
		self.function = function
		
		

	#Updating image, getting clicked
	def update(self, click):
		#Getting mouse pos
		mousePos = vec(pg.mouse.get_pos())

		#If mouse in button
		if self.rect.collidepoint(mousePos.x, mousePos.y):
			#Changing to hover image
			self.image = self.hoverImage
			#If clicked
			if click:
				#Execute function
				self.function()

		else:
			#Changing to default image
			self.image = self.noHoverImage

	#Draw function
	def draw(self):
		#Blit image to screen
		self.game.screen.blit(self.image, self.rect, special_flags=0)