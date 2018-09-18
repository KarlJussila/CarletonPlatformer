#Imports
import pygame as pg
from settings import *
vec = pg.math.Vector2

def collisions(game):
	hits = pg.sprite.spritecollide(game.player, game.tiles, False)
	
	#Resetting leftWall and rightWall
	if not hits and not game.player.onGround:
		for tile in game.tiles:
			if tile.rect.collidepoint(game.player.pos.x + (game.player.rect.width/2) + 3, game.player.pos.y) or tile.rect.collidepoint(game.player.pos.x + (game.player.rect.width/2) + 3, game.player.pos.y - game.player.rect.height):
				break
			elif tile.rect.collidepoint(game.player.pos.x - (game.player.rect.width/2) - 3, game.player.pos.y) or tile.rect.collidepoint(game.player.pos.x - (game.player.rect.width/2) - 3, game.player.pos.y - game.player.rect.height):
				break
		game.rightWall = False
		game.leftWall = False
	
	#####################################################################
	#--------------------TILE COLLISIONS WITH PLAYER--------------------#
	#####################################################################
	if hits:
		for hit in hits:
			
			#Corner collisions
			if len(hits) > 2:
				top = hits[0]
				bottom = hits[0]
				for h in hits:
					
					if h.rect.y > bottom.rect.y:
						bottom = h
					elif h.rect.y < top.rect.y:
						top = h

				cornerHit = True

				game.player.vel = vec(0,0)
				if game.player.vel.y > 0:
					#Top left
					if game.player.vel.x > 0:
						print("TL")
						game.rightWall = True
						print("rightWall1")
						game.player.pos.x = top.rect.left - (game.player.rect.width/2) - 2
						game.player.pos.y = bottom.rect.top - 2
						game.player.rect.midbottom = game.player.pos
					#Top right
					else:
						print("TR")
						game.leftWall = True
						game.player.pos.x = top.rect.right + (game.player.rect.width/2) + 2
						game.player.pos.y = bottom.rect.top - 2
						game.player.rect.midbottom = game.player.pos
				else:
					#Bottom Left
					if game.player.vel.x > 0:
						print("BL")
						game.rightWall = True
						print("rightWall2")
						game.player.pos.x = bottom.rect.left - (game.player.rect.width/2) - 2
						game.player.pos.y = top.rect.bottom + (game.player.height) + 2
						game.player.rect.midbottom = game.player.pos
						game.player.onGround = True
					#Bottom right
					else:
						print("BR")
						game.leftWall = True
						game.player.pos.x = bottom.rect.right + (game.player.rect.width/2) + 2
						game.player.pos.y = top.rect.bottom + (game.player.rect.height) + 2
						game.player.rect.midbottom = game.player.pos
						game.player.onGround = True
				break

			if game.player.vel.y < 0:
				if game.player.lastPos.y - game.player.rect.height > hit.rect.bottom:
					#Collision is from the bottom
					print("B1")
					nextHit = False
					for tile in game.tiles:
						if tile.rect.collidepoint((hit.rect.centerx, hit.rect.bottom + 1)):
							nextHit = True
					if nextHit:
						continue
					game.player.vel.y = 0
					game.player.pos.y = hit.rect.bottom + game.player.rect.height + 1
					game.player.rect.midbottom = game.player.pos
					break
				else:
					if game.player.vel.x > 0:
						#Collision is from the left
						isPlatform = False
						for tile in game.tiles:
							if tile.rect.collidepoint((hit.rect.left - 1, hit.rect.centery)):
								isPlatform = True
						if isPlatform:
							print("B2")
							game.player.vel.y = 0
							game.player.pos.y = hit.rect.bottom + game.player.rect.height + 1
							game.player.rect.midbottom = game.player.pos
							break
						game.rightWall = True
						print("L1")
						game.player.vel.x = 0
						game.player.pos.x = hit.rect.left - (game.player.rect.width/2) - 2
						game.player.rect.midbottom = game.player.pos
						if game.player.wallClimb:
							game.player.vel.y = 0
							game.player.onWall = True						
						break						
						break
					else:
						#Collision is from the right
						isPlatform = False
						for tile in game.tiles:
							if tile.rect.collidepoint((hit.rect.right + 1, hit.rect.centery)):
								isPlatform = True
						if isPlatform:
							print("B3")
							game.player.vel.y = 0
							game.player.pos.y = hit.rect.bottom + game.player.rect.height + 1
							game.player.rect.midbottom = game.player.pos
							break
						print("R1")
						game.leftWall = True
						game.player.vel.x = 0
						game.player.pos.x = hit.rect.right + (game.player.rect.width/2) + 2
						game.player.rect.midbottom = game.player.pos
						print(game.player.wallClimb)
						if game.player.wallClimb:
							game.player.vel.y = 0
							game.player.onWall = True
							
						break
			elif game.player.vel.y > 0:

				##############################################
				#That one case that just doesn't work
				if hit.rect.collidepoint(game.player.lastPos.x + (game.player.rect.width/2), game.player.lastPos.y + 2) or hit.rect.collidepoint(game.player.lastPos.x - (game.player.rect.width/2), game.player.lastPos.y + 2):
					game.player.vel.y = 0
					game.player.pos.y = hit.rect.top - 1
					game.player.rect.midbottom = game.player.pos
					game.player.onGround = True
					break
				##############################################

				if game.player.lastPos.y < hit.rect.top:
					#Collision is from the top
					nextHit = False
					for tile in game.tiles:
						if tile.rect.collidepoint((hit.rect.centerx, hit.rect.top - 1)):
							nextHit = True
					if nextHit:
						continue
					print("T1")
					game.player.vel.y = 0
					game.player.pos.y = hit.rect.top - 1
					game.player.rect.midbottom = game.player.pos
					game.player.onGround = True
					break
				else:
					if game.player.vel.x > 0:
						#Collision is from the left
						isPlatform = False
						for tile in game.tiles:
							if tile.rect.collidepoint((hit.rect.left - 1, hit.rect.centery)):
								isPlatform = True
						if isPlatform:
							print("T2")
							game.player.vel.y = 0
							game.player.pos.y = hit.rect.top - 1
							game.player.rect.midbottom = game.player.pos
							game.player.onGround = True
							break
						game.rightWall = True
						print("L2")
						game.player.vel.x = 0
						game.player.pos.x = hit.rect.left - (game.player.rect.width/2) - 2
						game.player.rect.midbottom = game.player.pos
						if game.player.wallClimb:
							game.player.vel.y = 0
							game.player.onWall = True						
						break						
						break
					elif game.player.vel.x < 0:
						#Collision is from the right
						isPlatform = False
						for tile in game.tiles:
							if tile.rect.collidepoint((hit.rect.right + 1, hit.rect.centery)):
								isPlatform = True
						if isPlatform:
							print("T3")
							game.player.vel.y = 0
							game.player.pos.y = hit.rect.top - 1
							game.player.rect.midbottom = game.player.pos
							game.player.onGround = True
							break
						game.leftWall = True
						print("L3")
						game.player.vel.x = 0
						game.player.pos.x = hit.rect.right + (game.player.rect.width/2) + 2
						game.player.rect.midbottom = game.player.pos
						if game.player.wallClimb:
							game.player.vel.y = 0
							game.player.onWall = True						
						break
			else:
				
				if game.player.vel.x > 0 and not game.rightWall:
					#Collision is from the left
					game.rightWall = True
					print("L4")
					game.player.vel.x = 0
					game.player.pos.x = hit.rect.left - (game.player.rect.width/2) - 2
					game.player.rect.midbottom = game.player.pos
					break
				elif game.player.vel.x < 0 and not game.leftWall:
					#Collision is from the right
					game.leftWall = True
					print("R2")
					game.player.vel.x = 0
					game.player.pos.x = hit.rect.right + (game.player.rect.width/2) + 2
					game.player.rect.midbottom = game.player.pos
					break
	#####################################################################
	#--------------------TILE COLLISIONS WITH PLAYER--------------------#
	#####################################################################			


	#Player falling out of the world
	if(game.player.rect.top > game.map.height):
		game.player.die("You have fallen out of the world!")

	#Enemy collision with players
	for enemy in game.enemy_sprites:
		if enemy.rect.colliderect(game.player.rect):
			if game.player.vel.y > 0:
				if(game.player.lastPos.y < enemy.rect.top):
					enemy.die()
					game.player.vel.y = -12
					break
			game.player.die("You have run into an enemy :/")

	for ghost in game.ghost_sprites:
		if ghost.rect.colliderect(game.player.rect):
			if game.player.vel.y > 0:
				if(game.player.lastPos.y < ghost.rect.top):
					ghost.die()
					game.player.vel.y = -12
					break
			game.player.die("You have run into an enemy :/")

	for turret in game.turret_sprites:
		if turret.rect.colliderect(game.player.rect):
			if game.player.vel.y > 0:
				if(game.player.lastPos.y < turret.rect.top):
					turret.die()
					game.player.vel.y = -12
					break
			game.player.die("You have run into an enemy :/")

	#Spike collision with players
	for spike in game.spike_sprites:
		if spike.rect.colliderect(game.player.rect):
			game.player.die("You were impaled")

	#Turret projectile collision with player
	for proj in game.projectile_sprites:
		if proj.rect.colliderect(game.player.rect):
			game.player.die("Oh no, you have been shot.")
			break
		c =pg.sprite.spritecollideany(proj, game.projectile_sprites)
		if(proj != c):
			for prj in game.projectile_sprites:
				if(prj == c):
					prj.kill()
			proj.kill()
			
	#Endpoint collision
	if pg.sprite.spritecollideany(game.player, game. endpoint_sprites):
		for sprite in game.all_sprites:
			sprite.kill()
		game.mainMenu()
    