import pygame as pg, resource_handler as rh

class Player(pg.sprite.Sprite):
	
	def __init__(self, hp, weapons, position, direction, sounds, surface, room, monsterGroup, inventory):
		pg.sprite.Sprite.init(self)
		self.hp = hp
		self.weapons = weapons
		self.weapon = self.weapons[0]
		self.pos = position
		self.death_sound, self.attack_sound = sounds[0], sounds[1]
		self.direction
		self.image = eval("self.weapon.image_" + self.direction)
		self.sur = surface
		self.room = room
		self.rect = self.image.get_rect()
		self.monsterGroup = monsterGroup
		self.inventory = inventory

	def check_events(self, tilemap, roommap):
		#return-codes: 0 = game quit; 1 = normal move, 2 = collide with wall, 3 = end tile collision
		self.oldPos = self.pos
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return 0
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_LEFT:
					self.pos[0] -= 5
					self.direction = "left"
					self.image = eval("self.weapon.image_" + self.direction)
				elif event.key == pg.K_UP:
					self.pos[1] -= 5
					self.direction = "up"
					self.image = eval("self.weapon.image_" + self.direction)
				elif event.key == pg.K_RIGHT:
					self.pos[0] += 5
					self.direction = "right"
					self.image = eval("self.weapon.image_" + self.direction)
				elif event.key == pg.K_DOWN:
					self.pos[1] += 5
					self.direction = "down"
					self.image = eval("self.weapon.image_" + self.direction)
				elif event.type == pg.MOUSEBUTTONDOWN:
					if event.button == 4:
						self.weapon_change()
					elif event.button = 1:
						self.attack()
		tile_rects = []
		end_tile = None
		for i in tilemap:
			if i[0][0][0] == "pillar.png":
				tile_rects.append(i[0][0][1])
			elif i[0][0][0] == "end.png":
				end_tile = i[0][0][1]
		if self.rect.collidelist(tile_rects):
			self.pos = self.oldPos
			return 2
		if self.rect.colliderect(end_tile):
			self.check_End()
		if self.pos[0] < 100:
			self.change_room(roommap, 0)#right
		elif self.pos[0]+100 > self.room[1]*50+100:
			self.change_room(roommap, 1)#left
		elif self.pos[1] < 100:
			self.change_room(roommap, 2)#up
		elif self.pos[1]+100 > self.room[2]*50+100:
			self.change_room(roommap, 3)#down
		#normal move
		return 1

	def change_room(self, roommap, map_size, entry):
		if entry == 0:#left entry
			self.room = roommap[self.room[0][0]+1+self.room[0][1]*map_size[0]]
			self.pos = (100, self.room[2]*25+100)
			self.direction = "right"
			self.image = eval("self.weapon.image_" + self.direction)
			return self.room
		elif entry == 1:#right entry
			self.room = roommap[self.room[0][0]-1+self.room[0][1]*map_size[0]]
			self.pos = (self.room[1]*50+50, self.room[2]*25+100)
			self.direction = "left"
			self.image = eval("self.weapon.image_" + self.direction)
			return self.room
		elif entry == 2:#bottom entry
			self.room = roommap[self.room[0][1]+1+self.room[0][1]*map_size[1]]
			self.pos = (self.room[1]*50+50, self.room[2]*25+100)
			self.direction = "up"
			self.image = eval("self.weapon.image_" + self.direction)
			return self.room
		elif entry == 3:#top entry
			self.room = roommap[self.room[0][1]-1+self.room[0][1]*map_size[1]]
			self.pos = (self.room[1]*50+50, self.room[2]*25+100)
			self.direction = "down"
			self.image = eval("self.weapon.image_" + self.direction)
			return self.room

	def update(self):
		self.rect.move(pos)

	def attack(self):
		pass

	def weapon_change(self):
		self.idx = self.weapons.index(self.weapon)+1
		if self.idx >= len(self.weapons):
			self.idx = 0
		self.weapon = self.weapons[idx]
		self.image = eval("self.weapon.image_" + self.direction)

	def pick_Up(self):
		pass

if __name__=="__main__":
	import map_generator as mg, weapons, random as r
	pg.init()
	msize = [r.randint(4, 7), r.randint(4, 7)]
	WIDTH = 800
	HEIGHT = 800
	screen = pg.display.set_mode((WIDTH, HEIGHT))
	bg = pg.Surface(screen.get_size())
	bg = bg.convert()
	bg.fill((0,0,0))
	roommap = mg.generate_map(msize)
	roomI = 0
	screen.blit(bg, (0,0))

	tm = mg.generate_tilemap(roomI, roommap, msize)
	mg.draw_room(tm, bg)
	pg.display.flip()
	clock = pg.time.Clock()
	going = 1

	player = Player(100,[knife=weapons.Knife()], [None, None], bg, roomI, None, [])
	player_Group = pg.sprite.RenderUpdate()
	player_Group.add(player)
	#hp, weapons, position, direction, sounds, surface, room, monsterGroup, inventory

	while Going:
		pass