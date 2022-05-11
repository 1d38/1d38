import math, random as r, pgzrun

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
	room = roommap[roomI]
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
			f = Actor("floor", topleft=((rwidth-1)*50, y*50))
			tilemap.append([f, (rwidth-1, y)])
			allcoords.remove((rwidth-1, y))
	if room[4]:
		for x in range((int(rwidth/2)-1), (int(rwidth/2)+2)):
			f = Actor("floor", topleft=(x*50, (rheight-1)*50))
			tilemap.append([f, (x, rheight-1)])
			allcoords.remove((x, rheight-1))
	# checks for top and left exit
	if rooms[roomI-mheight][3] and (roomI-mheight >= 0):
		for y in range((int(rheight/2)-1), (int(rheight/2)+2)):
			f = Actor("floor", topleft=(0, y*50))
			tilemap.append([f, (0, y)])
			allcoords.remove((0, y))
	if rooms[roomI-1][4] and (roomI-1 >= 0):
		for x in range((int(rwidth/2)-1), (int(rwidth/2)+2)):
			f = Actor("floor", topleft=(x*50, 0))
			tilemap.append([f, (x, 0)])
			allcoords.remove((x, 0))
	# creates tilemap
	for x in range(1, rwidth-1):
		for y in range(1, rheight-1):
			f = Actor("floor", topleft=(x*50, y*50))
			tilemap.append([f, (x, y)])
			allcoords.remove((x, y))
	for i in allcoords:
		f = Actor("pillar", topleft=(i[0]*50, i[1]*50))
		tilemap.append([f, (i[0], i[1])])
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
		f = Actor("end", topleft=(x*50, y*50))
		tilemap.append([f, (x, y)])
	return tilemap

if __name__=="__main__":
	pass