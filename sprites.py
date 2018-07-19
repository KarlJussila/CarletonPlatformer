import pygame as pg
from settings import *
vec = pg.math.Vector2
from os import path

class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites, game.player_sprite
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((20,20))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.pos = vec(x + (self.rect.width/2), y + 20)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)
		self.lastPos = self.pos
		self.onGround = False

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
		if keys[pg.K_a]:
			self.acc.x = -PLAYER_ACC
		if keys[pg.K_d]:
			self.acc.x = PLAYER_ACC

		self.acc.x += self.vel.x * PLAYER_FRICTION
		self.vel += self.acc
		if(self.vel.y > 0):
			self.vel.y = min(30, self.vel.y)
		self.pos += self.vel + 0.5 * self.acc

		if self.pos.x < 0:
			self.pos.x = 0

		self.rect.midbottom = self.pos


	def jump(self):
		if self.onGround:
			self.vel.y = -18
			self.pos.y -= 1
			self.rect.top -= 2
			self.onGround = False

	def die(self, cause="You have died from unknown causes."):
		self.game.playing = False
		print(cause)


class Enemy1(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h, direction = -1, vel = 5):
		self.groups = game.all_sprites, game.enemy_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((w, h))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.width = w
		self.height = h
		self.direction = direction
		self.vel = vel

	def update(self):
		self.rect.x += self.vel * self.direction
		for tile in self.game.tiles:
			if tile.rect.colliderect(self.rect):
				self.direction *= -1

	def die(self):
		self.kill()

class Turret(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h, direction = 1, vel = 5, delay = int(FPS * 2.5)):
		self.groups = game.all_sprites, game.enemy_sprites, game.turret_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((w, h))
		self.image.fill(BLUE)
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.width = w
		self.height = h
		self.direction = direction
		self.vel = vel
		self.delay = delay

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
		self.parent = parent
		self.image = pg.Surface((10, 5))
		self.image.fill(YELLOW)
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
		self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
		self.image.fill((110,110,110))
		#self.image = game.tileImage
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Platform(pg.sprite.Sprite):
	def __init__(self, tiles, game):
		self.groups = game.platforms, game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.tiles = tiles
		
		leftPos = WIDTH
		rightPos = 0
		topPos = HEIGHT
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
		self.image.fill((255,0,0))


class EndPoint(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
		self.image.fill((150,0,150))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y