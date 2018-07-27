import pygame as pg
from settings import *
vec = pg.math.Vector2
from os import path

class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites, game.player_sprite
		pg.sprite.Sprite.__init__(self, self.groups)
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
	def animate(self):
		if self.game.ticks % 2 == 0:
			self.imgNum +=1
			if self.imgNum == 5:
				self.imgNum = 1
			self.image = self.imageDict[str(self.facing) + str(self.imgNum)]
	def update(self):
		self.onGround = False
		for platform in self.game.platforms:
			if self.pos.y <= platform.rect.top and (platform.rect.collidepoint((self.rect.bottomright[0], self.rect.bottomright[1] + 1)) or platform.rect.collidepoint((self.rect.bottomleft[0], self.rect.bottomleft[1] + 1))):
				self.onGround = True

		self.lastPos = vec(self.pos.x, self.pos.y)
		self.acc = vec(0, PLAYER_GRAV)
		if self.onGround:
			self.acc.y = 0
			self.vel.y = 0
		keys = pg.key.get_pressed()
		if keys[pg.K_a] and not self.game.leftWall:
			self.game.rightWall = False
			self.facing = -1
			self.acc.x = -PLAYER_ACC
		if keys[pg.K_d] and not self.game.rightWall:
			self.game.leftWall = False
			self.acc.x = PLAYER_ACC
			self.facing = 1
		
		self.acc.x += self.vel.x * PLAYER_FRICTION
		self.vel += self.acc
		if(self.vel.y > 0):
			self.vel.y = min(30, self.vel.y)
		self.pos += self.vel + 0.5 * self.acc

		if self.pos.x < 0:
			self.pos.x = 0

		self.rect.midbottom = self.pos
		
		
		if abs(self.vel.x) > 1 and self.onGround:
			self.animate()
		else:
			if abs(self.vel.y) > 0:
				self.image = self.imageDict[str(self.facing) + "2"]
			else:
				self.image = self.imageDict[str(self.facing) + "1"]
		
			
	def jump(self):
		if self.onGround:
			self.vel.y = -18
			self.pos.y -= 1
			self.rect.top -= 2
			self.onGround = False

	def die(self, cause="You have died from unknown causes."):
		self.kill()
		self.game.playing = False
		print(cause)
		self.game.gameOverMenu()


class Enemy1(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h, direction = -1, vel = 5):
		self.groups = game.all_sprites, game.enemy_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
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

	def update(self):
		if self.game.ticks %5 == 0:
			if self.animate == 1:
				self.image = self.img2
				self.animate = 0
			else:
				self.image = self.img
				self.animate = 1
				
		self.rect.x += self.vel * self.direction
		for tile in self.game.tiles:
			if tile.rect.colliderect(self.rect):
				self.direction *= -1

	def die(self):
		self.kill()
class spike(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h, direction = -1, vel = 5):
		self.groups = game.all_sprites, game.enemy_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((20, 10))
		self.image = pg.image.load(FILEPATH + "spikes.png")
		self.animate = 1
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y+10)
		self.width = w
		self.height = h
		self.direction = direction
		self.vel = vel

	def update(self):
		pass

	def die(self):
		self.game.player.die()

class Turret(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h, d, vel = 5, delay = int(FPS * 2.5)):
		self.groups = game.all_sprites, game.enemy_sprites, game.turret_sprites
		self.direction = d
		pg.sprite.Sprite.__init__(self, self.groups)
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

	def update(self):
		self.fireProjectile()

	def fireProjectile(self):
		if self.game.ticks % self.delay == 0:
			
			Projectile(self.game, self)

	def die(self):
		self.kill()


class Projectile(pg.sprite.Sprite):
	def __init__(self, game, parent):
		self.groups = game.all_sprites, game.projectile_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
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

	def update(self):
		self.rect.x += self.parent.vel * self.parent.direction
		for tile in self.game.tiles:
			if tile.rect.colliderect(self.rect):
				self.kill()
		if self.rect.left > self.game.map.width:
			self.kill()


class Tile(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites, game.tiles
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.tileImage
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Platform(pg.sprite.Sprite):
	def __init__(self, tiles, game):
		self.groups = game.platforms, game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.tiles = tiles
		
		leftPos = game.map.width
		rightPos = 0
		topPos = game.map.height
		bottomPos = 0
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

		#print(self.rect.width, self.rect.height)
		self.image = pg.Surface((self.rect.width, self.rect.height))
		self.image = game.tileImage


class EndPoint(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		
		
		self.groups = game.all_sprites, game.endpoint_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
		img = pg.image.load(FILEPATH + "goldOre.png")
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
class Button(pg.sprite.Sprite):
	def __init__(self, game, x, y, image, hoverImage, function, group):
		self.groups = game.button_sprites, group
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.noHoverImage = image
		self.hoverImage = hoverImage
		self.image = image
		self.x = x
		self.y = y
		self.rect = image.get_rect()
		self.rect.topleft = (x,y)
		self.function = function


	def update(self, click):
		mousePos = vec(pg.mouse.get_pos())
		mousePressed = pg.mouse.get_pressed()
		if self.rect.collidepoint(mousePos.x, mousePos.y):
			self.image = self.hoverImage
			if click:
				self.function()

		else:
			self.image = self.noHoverImage
	def draw(self):
		self.game.screen.blit(self.image, self.rect)