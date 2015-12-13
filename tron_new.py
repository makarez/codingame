import sys
import math
import random

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


#Map definition
def debug(msg):
	print >> sys.stderr, str(msg)

def displayMap(map):
    for j in xrange(map.y_size):
        for i in xrange(map.x_size):
            print >> sys.stderr, str(map.map[i][j]),
        print >> sys.stderr, "\n",

class Map:
	def __init__(self, x_size, y_size):
		self.map = [["x" for x in range(y_size)] for x in range(x_size)]
		self.x_size = x_size
		self.y_size = y_size
	
	def clear_dead_players(self, id):
		for x in xrange(self.x_size):
				for y in xrange(self.y_size):
					if self.map[x][y] == id:
						self.map[x][y] = "x"
		
	def set_player_pos(self, x, y, id):
		self.map[x][y] = id
		
	def valid(self, x, y):
		if x < 0 or x >= self.x_size or y < 0 or y >= self.y_size:
			debug("not valid")
			return False
		else:
			return True
			
	def free(self, x, y):
		
		if self.valid(x,y) and self.map[x][y] == "x":
			debug(self.map[x][y])
			return True
		else:
			return False
			
class Position:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def dump(self):
		debug(str(self.x) + "," + str(self.y))
		
	def set(self,x,y):
		self.x = x
		self.y = y

class Direction:
	
	def __init__(self, label):
		self.label = label
	
	def valid(self, map, pos):
		debug (self.label)
		pos.dump()
		if self.label == "UP":
			if map.free(pos.x, pos.y-1):
				return True
		if self.label == "DOWN":
			if map.free(pos.x, pos.y+1):
				return True
		elif self.label == "LEFT":
			if map.free(pos.x-1, pos.y):
				return True
		elif self.label == "RIGHT":
			if map.free(pos.x+1, pos.y):
				return True

		
		
class Player:

	def __init__(self):
		self.pos = Position(0,0)
		self.id = 0
		
		
	def set_pos(self, pos):
		self.pos = pos
		
	def get_pos(self):
		return self.pos
	
	def set_id(seld, id):
		self.id = id
	
	def dump_position(self):
		self.pos.dump()
		
	def get_actions(self):
		#Here we build the actions we can do depending on the current situation
		return "LEFT"
	

#Objects initialisation
map = Map(30,20)	
me = Player()

right = Direction("RIGHT")
left = Direction("LEFT")
up = Direction("UP")
down = Direction("DOWN")

directions = [up , down, right, left, ]

me.dump_position()
# game loop
while 1:
	# n: total number of players (2 to 4).
	# p: your player number (0 to 3).
	n, p = [int(i) for i in raw_input().split()]
	actions=[]
	for i in xrange(n):
         # x0: starting X coordinate of lightcycle (or -1)
         # y0: starting Y coordinate of lightcycle (or -1)
         # x1: starting X coordinate of lightcycle (can be the same as X0 if you play before this player)
         # y1: starting Y coordinate of lightcycle (can be the same as Y0 if you play before this player)
		x0, y0, x1, y1 = [int(j) for j in raw_input().split()]
    
		pos = Position(x1, y1)
		
		map.set_player_pos(x0, y0 ,i)
		map.set_player_pos(x1, y1 ,i)
		    
		#If a player has disappeared, we clear the map
		if x0 == -1:
			map.clear_dead_players(i)
        
		#We keep our positing, might be useful :D
		if i==p:
			me.set_pos(pos)
			me.dump_position()
	displayMap(map)
	
	for dir in directions:
		if dir.valid(map, me.get_pos()):
			print dir.label
			break
	