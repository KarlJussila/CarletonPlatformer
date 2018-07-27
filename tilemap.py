#Imports
import pygame as pg
from settings import *

#Map (level) class
class Map:
	def __init__(self,fileName):
		#Retrieving data
		self.data = []
		with open(fileName, 'rt') as f:
			for line in f:
				line.replace("\r", "")
				self.data.append(line)

		#Initializing variables
		self.tileWidth = len(self.data[0])
		self.tileHeight = len(self.data)
		self.width = self.tileWidth * TILE_SIZE
		self.height = self.tileHeight * TILE_SIZE

#Camera (screen) class
class Camera:
	def __init__(self, width, height):
		self.camera = pg.Rect(0, 0, WIDTH, HEIGHT)
		self.width = width
		self.height = height

	#Camera offset function
	def apply(self, entity):
		#Applying camera offset to input sprite
		return entity.rect.move(self.camera.topleft)

	#Updating camera position
	def update(self,target):
		#Moving camera
		x = -target.rect.x + int(WIDTH/2)
		y = -target.rect.y + int(HEIGHT/2)

		#Limit scrolling
		x = min(0, x) #left
		y = min(0, y) #top
		x = max(-(self.width - WIDTH), x) #right
		y = max(-(self.height - HEIGHT), y) #bottom

		#Updating camera rectangle
		self.camera = pg.Rect(x, y, self.width, self.height)