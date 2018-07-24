import pygame as pg
from settings import *

class Map:
	def __init__(self,fileName):
		self.data = []
		with open(fileName, 'rt') as f:
			for line in f:
				self.data.append(line)
				print(line)

		self.tileWidth = len(self.data[0])
		self.tileHeight = len(self.data)
		self.width = self.tileWidth * TILE_SIZE
		self.height = self.tileHeight * TILE_SIZE

class Camera:
	def __init__(self, width, height):
		self.camera = pg.Rect(0, 0, WIDTH, HEIGHT)
		self.width = width
		self.height = height

	def apply(self, entity):
		return entity.rect.move(self.camera.topleft)

	def update(self,target):
		x = -target.rect.x + int(WIDTH/2)
		y = -target.rect.y + int(HEIGHT/2)

		#Limit scrolling
		x = min(0, x) #left
		y = min(0, y) #top

		x = max(-(self.width - WIDTH), x) #right
		y = max(-(self.height - HEIGHT), y) #bottom

		self.camera = pg.Rect(x, y, self.width, self.height)