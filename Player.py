import pygame as pg, resource_handler as rh, Weapons
import time as t
class Player(pg.sprite.Sprite):
	
	def __init__(self, hp, weapons, position, direction, sounds, surface, room, monsterGroup, inventory, roommap):
		pg.sprite.Sprite.__init__(self)
		self.hp = hp
		self.weapons = weapons
		self.weapon = self.weapons[0]
		self.pos = position
		self.death_sound, self.attack_sound = sounds[0], sounds[1]
		self.direction = direction
		self.image = eval("self.weapon.Pimage_" + self.direction)
		#print("self.image = self.weapon.Pimage_" + self.direction)
		#exec("self.image = self.weapon.Pimage_" + self.direction)
		#self.image = self.weapon.Pimage_right
		self.sur = surface
		self.room = roommap[room]
		#self.rect = eval("self.weapon.Pimage_" + self.direction + "_rect")
		#print(self.rect)
		#print(self.pos)
		self.rect = pg.Rect(200, 200, 50, 50)
		self.monsterGroup = monsterGroup
		self.inventory = inventory
		self.pos_change = [0,0]

	def check_events(self, tilemap, roommap):
		#return-codes: 0 = game quit; 1 = normal move, 2 = collide with wall, 3 = end tile collision
		self.oldPos = self.pos.copy()
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return 0
			elif event.type == pg.KEYDOWN:
				if event.type == pg.MOUSEBUTTONDOWN:
					if event.button == 4:
						return 8
					elif event.button == 1:
						return 9
		keys=pg.key.get_pressed()
		if keys[pg.K_a]:
			self.pos[0] -= 5
			self.pos_change[0] -= 5
			self.direction = "left"
			self.image = eval("self.weapon.Pimage_" + self.direction)
			#self.rect = eval("self.weapon.Pimage_" + self.direction + "_rect")
			#self.rect.move_ip(self.pos)
		elif keys[pg.K_w]:
			self.pos[1] -= 5
			self.pos_change[1] -= 5
			self.direction = "up"
			self.image = eval("self.weapon.Pimage_" + self.direction)
			#self.rect = eval("self.weapon.Pimage_" + self.direction + "_rect")
			#self.rect.move_ip(self.pos)
		elif keys[pg.K_d]:
			self.pos[0] += 5
			self.pos_change[0] += 5
			self.direction = "right"
			self.image = eval("self.weapon.Pimage_" + self.direction)
			#self.rect = eval("self.weapon.Pimage_" + self.direction + "_rect")
			#self.rect.move_ip(self.pos)
		elif keys[pg.K_s]:
			self.pos[1] += 5
			self.pos_change[1] += 5
			self.direction = "down"
			self.image = eval("self.weapon.Pimage_" + self.direction)
			#self.rect = eval("self.weapon.Pimage_" + self.direction + "_rect")
			#self.rect.move_ip(self.pos)
		#print(self.pos)
		self.rect.move_ip(self.pos_change)
		tile_rects = []
		end_tile = None
		for i in tilemap:
			print(i)
			if i[2] == "pillar.png":
				tile_rects.append(i[0][0][1])
			elif i[2] == "end.png":
				end_tile = i[0][0][1]
		#print(tile_rects)
		#print(self.rect.collidelist(tile_rects))
		if self.rect.collidelist(tile_rects) != -1:
			#called
			#print(self.pos, "  1")
			self.pos[0] -= self.pos_change[0]
			self.pos[1] -= self.pos_change[1]
			self.rect.move_ip((-self.pos_change[0], -self.pos_change[1]))
			#print(self.pos_change)
			#print(self.pos, "  2")
			self.pos_change = [0,0]
			return 2
		if end_tile:
			if self.rect.colliderect(end_tile):
				self.check_End()
		if self.pos[0] < 100:
			#print("called")
			self.pos_change = [0,0]
			return 4#left exit
		elif self.pos[0]+100 > self.room[1]*50+150:
			#print("called")
			self.pos_change = [0,0]
			return 5#right exit
		elif self.pos[1] < 100:
			#print("called")
			self.pos_change = [0,0]
			return 6#top exit
		elif self.pos[1]+100 > self.room[2]*50+150:
			#print("called")
			self.pos_change = [0,0]
			return 7#bottom exit
		#normal move
		#print(self.rect)
		self.pos_change = [0,0]
		return 1

	def change_room(self, roommap, map_size, entry, roomI):
		if entry == 0:#right entry
			self.room = roommap[roomI]
			self.pos = [self.room[1]*50+50, self.room[2]*25+100]
			self.rect.update(self.pos, (50,50))
			self.direction = "right"
			self.image = eval("self.weapon.Pimage_" + self.direction)
			#self.rect = eval("self.Pweapon.image_" + self.direction + "_rect")
			return self.room
		elif entry == 1:#left entry
			self.room = roommap[roomI]
			self.pos = [100, self.room[2]*25+100]
			self.rect.update(self.pos, (50,50))
			self.direction = "left"
			self.image = eval("self.weapon.Pimage_" + self.direction)
			#self.rect = eval("self.Pweapon.image_" + self.direction + "_rect")
			return self.room
		elif entry == 2:#bottom entry
			self.room = roommap[roomI]
			self.pos = [self.room[1]*25+50, self.room[2]*50+50]
			self.rect.update(self.pos, (50,50))
			self.direction = "up"
			self.image = eval("self.weapon.Pimage_" + self.direction)
			#self.rect = eval("self.Pweapon.image_" + self.direction + "_rect")
			return self.room
		elif entry == 3:#top entry
			self.room = roommap[roomI]
			self.pos = [self.room[1]*25+50, 100]
			self.rect.update(self.pos, (50,50))
			self.direction = "down"
			self.image = eval("self.weapon.Pimage_" + self.direction)
			#self.rect = eval("self.Pweapon.image_" + self.direction + "_rect")

	def attack(self):
		pass

	def weapon_change(self):
		self.idx = self.weapons.index(self.weapon)+1
		if self.idx >= len(self.weapons):
			self.idx = 0
		self.weapon = self.weapons[idx]
		self.image = eval("self.weapon.Pimage_" + self.direction)
		#self.rect = eval("self.Pweapon.image_" + self.direction + "_rect")

	def pick_Up(self):
		pass

if __name__=="__main__":
	import map_generator as mg, Weapons, random as r
	pg.init()
	msize = [r.randint(4, 7), r.randint(4, 7)]
	WIDTH = 800
	HEIGHT = 800
	screen = pg.display.set_mode((WIDTH, HEIGHT))
	bg = pg.Surface(screen.get_size())
	#bg, bg_rect = rh.load_img("bg.png")
	buffer = pg.Surface(screen.get_size())
	bg.fill((0,0,0))
	roommap = mg.generate_map(msize)
	roomI = 0
	screen.blit(bg, (0,0))
	tm = mg.generate_tilemap(roomI, roommap, msize)
	mg.draw_room(tm, bg, screen, buffer)
	clock = pg.time.Clock()
	going = 1
	knife=Weapons.Knife()
	player = Player(100, [knife], [200, 200], "right", [None, None], bg, roomI, None, [], roommap)
	player_Group = pg.sprite.RenderUpdates()
	player_Group.add(player)
	player_Group.draw(screen)
	pg.display.flip()
	#self, hp, weapons, position, direction, sounds, surface, room, monsterGroup, inventory, roommap

	going = 1
	while going:
		returnValue = player.check_events(tm, roommap)
		#print(returnValue)
		if returnValue == 0:
			going = 0
		elif returnValue == 3:
			if key in player.inventory:
				pass
			else:
				pass
		elif returnValue == 4:
			roomI -= msize[1]
			player.change_room(roommap, msize, 0, roomI)#left
			tm = mg.generate_tilemap(roomI, roommap, msize)
			mg.draw_room(tm, bg, screen, buffer)
		elif returnValue == 5:
			roomI += msize[1]
			player.change_room(roommap, msize, 1, roomI)#right
			tm = mg.generate_tilemap(roomI, roommap, msize)
			mg.draw_room(tm, bg, screen, buffer)
		elif returnValue == 6:
			roomI -= 1
			player.change_room(roommap, msize, 2, roomI)#top
			tm = mg.generate_tilemap(roomI, roommap, msize)
			mg.draw_room(tm, bg, screen, buffer)
		elif returnValue == 7:
			roomI += 1
			player.change_room(roommap, msize, 3, roomI)#bottom
			tm = mg.generate_tilemap(roomI, roommap, msize)
			mg.draw_room(tm, bg, screen, buffer)
		elif returnValue == 8:
			player.weapon_change()
		elif returnValue == 9:
			player.attack()
		print(roomI)
		player_Group.clear(screen, buffer)
		rects = player_Group.draw(screen)
		#print(rects)
		#rects.append(rectan)
		pg.display.update(rects)
		clock.tick(60)

	pg.quit()

