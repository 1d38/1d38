import math, random as r, pygame as pg, resource_handler as rh

def generate_map(size): #generates a map with a tupel/list giving the amount of rooms on the x-/y-axis
	mwidth = size[0]
	mheight = size[1]
	fieldcoords = []
	rooms = []
	#defines the exits of the room on the bottom (be) and right (re) side of the room; ensures the existence of an exist
	re = r.randint(0, 1)
	if re:
		be = r.randint(0, 1)
	else:
		be = 1
	# generates the cartesian product of width and height, so every room can be defined
	for x in range(mwidth):
		for y in range(mheight):
			fieldcoords.append((x, y))
	for i in range(len(fieldcoords)):
		#creates rooms with random sizes
		pos = fieldcoords[i]
		if (not pos[0]==(mwidth-1)) and (not pos[1]==(mheight-1)):
			re = r.randint(0, 1)
			if re:
				be = r.randint(0, 1)
			else:
				be = 1
			rooms.append([pos, r.randrange(7, 13, 2), r.randrange(7, 13, 2), re, be])
			#room def = [position, width in tiles, height in tiles, right exit(0=False,1=True), bottom exit(0=False,1=True)]
		elif pos[1] == (mheight-1) and (not pos[0] == (mwidth-1)):
			rooms.append([pos, r.randrange(7, 13, 2), r.randrange(7, 13, 2), 1, 0])
		elif pos[0] == (mwidth-1) and (not pos[1] == (mheight-1)):
			rooms.append([pos, r.randrange(7, 13, 2), r.randrange(7, 13, 2), 0, 1])
		elif pos[0] == (mwidth-1) and pos[1] == (mheight-1):
			rooms.append([pos, r.randrange(7, 13, 2), r.randrange(7, 13, 2), 0, 0])
	# ensures that the room diagonal to the bottom right room has two exits
	rooms[(len(rooms)-1)-(mheight+1)] = [(mwidth-2, mheight-2), r.randrange(7, 13, 2), r.randrange(7, 13, 2), 1, 1]
	return rooms

def generate_tilemap(roomI, rooms, msize): #generates a random tilemap for a room  ONCE during runtime
	mheight = msize[1]
	room = rooms[roomI]
	rwidth = room[1]
	rheight = room[2]
	allcoords = []
	tilemap = []
	for x in range(rwidth):
		for y in range(rheight):
			allcoords.append((x, y))
	# checks for bottom and right exit
	if room[3]:
		for y in range((int(rheight/2)-1), (int(rheight/2)+2)):
			img = [None, None]
			img[0], img[1] = rh.load_img("floor.png")
			img[1].move_ip(((rwidth-1)*50+100, y*50+100))
			f = [img, ((rwidth-1)*50+100, y*50+100)]
			tilemap.append([f, (rwidth-1, y), "floor.png"])
			allcoords.remove((rwidth-1, y))
	if room[4]:
		for x in range((int(rwidth/2)-1), (int(rwidth/2)+2)):
			img = [None, None]
			img[0], img[1] = rh.load_img("floor.png")
			img[1].move_ip((x*50+100, (rheight-1)*50+100))
			f = [img, (x*50+100, (rheight-1)*50+100)]
			tilemap.append([f, (x, rheight-1), "floor.png"])
			allcoords.remove((x, rheight-1))
	# checks for top and left exit
	if rooms[roomI-mheight][3] and (roomI-mheight >= 0):
		for y in range((int(rheight/2)-1), (int(rheight/2)+2)):
			img = [None, None]
			img[0], img[1] = rh.load_img("floor.png")
			img[1].move_ip((100, y*50+100))
			f = [img, (100, y*50+100)]
			tilemap.append([f, (0, y), "floor.png"])
			allcoords.remove((0, y))
	if rooms[roomI-1][4] and (roomI-1 >= 0):
		for x in range((int(rwidth/2)-1), (int(rwidth/2)+2)):
			img = [None, None]
			img[0], img[1] = rh.load_img("floor.png")
			img[1].move_ip((x*50+100, 100))
			f = [img, (x*50+100, 100)]
			tilemap.append([f, (x, 0), "floor.png"])
			allcoords.remove((x, 0))
	# creates tilemap
	for x in range(1, rwidth-1):
		for y in range(1, rheight-1):
			img = [None, None]
			img[0], img[1] = rh.load_img("floor.png")
			img[1].move_ip((x*50+100, y*50+100))
			f = [img, (x*50+100, y*50+100)]
			tilemap.append([f, (x, y), "floor.png"])
			allcoords.remove((x, y))
	for i in allcoords:
		img = [None, None]
		img[0], img[1] = rh.load_img("pillar.png")
		img[1].move_ip((i[0]*50+100, i[1]*50+100))
		f = [img, (i[0]*50+100, i[1]*50+100)]
		tilemap.append([f, (i[0], i[1]), "pillar.png"])
	# if its the bottom right room, a blue square in the middle is added
	if roomI == (len(rooms)-1):
		x = (room[1]-1)/2
		y = (room[2]-1)/2
		for i in tilemap:
			if i[1] == (x, y):
				del i
				break
			else:
				continue
		img = [None, None]
		img[0], img[1] = rh.load_img("end.png")
		img[1].move_ip((x*50+100, y*50+100))
		f = [img, (x*50+100, y*50+100), "end.png"]
		tilemap.append([f, (x, y)])
	return tilemap

#tilecoords:	coords = (tile[0][1][0],tile[0][1][1])

def draw_room(tm, surface, screen, buffer):
	screen.blit(surface, (0,0))
	for i in tm:
		coords = (i[0][1][0],i[0][1][1])
		#print(coords)
		screen.blit(i[0][0][0], coords)
		buffer.blit(i[0][0][0], coords)
	pg.display.flip()


if __name__=="__main__":
	pg.init()
	msize = [r.randint(4, 7), r.randint(4, 7)]
	# ~ msize = ["", 5, 7]
	#print(msize)
	WIDTH = 800
	HEIGHT = 800
	screen = pg.display.set_mode((WIDTH, HEIGHT))
	bg = pg.Surface(screen.get_size())
	bg = bg.convert()
	#bg.fill((0,0,0))
	roommap = generate_map(msize)
	roomI = 0
	screen.blit(bg, (0,0))
	tm = generate_tilemap(roomI, roommap, msize)
	#print(tm)
	#print(len(tm))
	draw_room(tm, bg, screen)
	fg = pg.Surface(screen.get_size(), pg.SRCALPHA)
	#fg.fill((0,0,0))
	#screen.blit(fg, (0,0))
	lol, lol_rect = rh.load_img("easworddown.png")
	fg.blit(lol, (200,200))
	pg.display.flip()
	clock = pg.time.Clock()
	going = 1
	while going:
		roomIn = roomI
		for event in pg.event.get():
			if event.type == pg.QUIT:
				going = False
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_LEFT:
					roomIn -= msize[1]
					if roomIn >= 0 and roommap[roomIn][3]:
						roomI = roomIn
						print(roomI)
						# ~ print(roommap)
					else:
						print("nope")
				elif event.key == pg.K_UP:
					roomIn -= 1
					# ~ print(roommap[roomIn-1])
					# ~ print("roomIN: " + str(roomIn))
					# ~ print(roommap)
					if roomIn >= 0 and roommap[roomIn][4]:
						roomI = roomIn
						print(roomI)
						# ~ print(roommap)
					else:
						print("nope")
				elif event.key == pg.K_RIGHT:
					roomIn += msize[1]
					if roomIn <= len(roommap)-1 and roommap[roomI][3]:
						roomI = roomIn
						print(roomI)
						# ~ print(roommap)
					else:
						print("nope")
				elif event.key == pg.K_DOWN:
					roomIn += 1
					if roomIn <= len(roommap)-1 and roommap[roomI][4]:
						roomI = roomIn
						print(roomI)
						# ~ print(roommap)
					else:
						print("nope")
			draw_room(generate_tilemap(roomI, roommap, msize), bg, screen)
			screen.blit(fg, (0,0))
			lol, lol_rect = rh.load_img("easworddown.png")
			fg.blit(lol, (200,200))
			screen.blit(fg, (0,0), area=(200,200,50,50))
			pg.display.flip()
		clock.tick(60)
	pg.quit()