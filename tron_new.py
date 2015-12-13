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
		debug(str(self.map[x][y]))
		if self.valid(x,y) and self.map[x][y] == "x":
			return True
		else:
			return False
			
class Position:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def set(self,x,y):
		self.x = x
		self.y = y
		
	def set_left(self):
		self.x = self.x-1
		
	def set_right(self):
		self.x = self.x+1
		
	def set_up(self):
		self.y = self.y-1
		
	def set_down(self):
		self.y = self.y+1
		
	def __str__(self):
		return str(self.x) + "," + str(self.y)

class Direction:
	
	def __init__(self, label):
		self.label = label
		self.score = -1
	
	def valid(self, map, pos):
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
				
	def __lt__(self, other_dir):
		return self.score < other_dir.score
	
	def __str__(self):
		return self.label
		
		
class Player:

	def __init__(self):
		self.pos = Position(0,0)
		self.id = 0
			
	def set_pos(self, pos):
		self.pos.x = pos.x
		self.pos.y = pos.y
		
	def get_pos(self):
		return self.pos
	
	def set_id(seld, id):
		self.id = id
	
	def dump_position(self):
		debug(self.pos)
		
	def get_actions(self):
		#Here we build the actions we can do depending on the current situation
		return "LEFT"
	
def compute_dist(map, me, dir):
	dist = 0
	if dir.label == "LEFT":
		for i in xrange(me.get_pos().x-1, -1, -1):
			debug(i)
			if map.free(i, me.get_pos().y):
				dist +=1
			else:
				break
	elif dir.label == "RIGHT":
		for i in xrange(me.get_pos().x+1, 30):
			debug(i)
			if map.free(i, me.get_pos().y):
				dist +=1
			else:
				break
	elif dir.label == "UP":
		for i in xrange(me.get_pos().y-1, -1, -1):
			debug(i)
			if map.free(me.get_pos().x, i):
				dist +=1
			else:
				break
	elif dir.label == "DOWN":
		for i in xrange(me.get_pos().y+1, 20):
			debug(i)
			if map.free(me.get_pos().x, i):
				dist +=1
			else:
				break
	return dist
	
	
order = 2
def eval_dirs(map, me, dirs):
	debug("Eval dirs")
	valid_dirs = []
	for dir in dirs:
		if dir.valid(map, me.get_pos()):
			valid_dirs.append(dir)
	current_pos = Position(me.get_pos().x, me.get_pos().y)
	for dir1 in valid_dirs:
		me.set_pos(current_pos)
		eval_dist(map, me, dir1)
	
	return max(valid_dirs).label

def eval_dist(map, me, dir):
	debug(dir) 
	dist = compute_dist(map, me, dir)
	debug(dist)
	dir.score = dist

def eval_safe_dir(map, me, dir):
	debug("Evaluating dir " + str(dir))
	
	#First we set the new position depending on the dir
	if dir.label == "LEFT":
		me.get_pos().set_left()
	elif dir.label == "RIGHT":
		me.get_pos().set_right()
	elif dir.label == "UP":
		me.get_pos().set_up()
	elif dir.label == "DOWN":
		me.get_pos().set_down()

	#We are now at the next position, we return the number of possible directions
	valid_dirs = []
	for dir1 in directions:
		if dir1.valid(map, me.get_pos()):
			valid_dirs.append(dir1)

	dir.score=len(valid_dirs)
	
#Objects initialisation
map = Map(30,20)	
me = Player()




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
        
		#We keep our position, might be useful :D
		if i==p:
			me.set_pos(pos)
			me.dump_position()
	#displayMap(map)
	
	#Reset the directions
	right = Direction("RIGHT")
	left = Direction("LEFT")
	up = Direction("UP")
	down = Direction("DOWN")
	directions = [up , down, right, left]

	print eval_dirs(map, me, directions)

	
