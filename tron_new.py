import sys
import math
import random

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


#Map definition
map = [["x" for x in range(20)] for x in range(30)]

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
    
        map[x0][y0]=i
        map[x1][y1]=i
        
        if x0 == -1:
            for x in xrange(30):
                for y in xrange(20):
                    if map[x][y] == i:
                        map[x][y] = "x"
        if i==p:
            my_x = x1
            my_y = y1
    
    displayMap(map)
	
	print toto
    
