import sys
import math
import random

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

my_x=0
my_y=0
last_action = None
use_thickness = False
actions=[]
action = None   
last_action = None
last_last_action = None
same_dir_weight = 5
use_u_turn = True
use_keep_last_action = False
use_check_danger = False
order = 1


map = [["x" for x in range(20)] for x in range(30)]

def cellDangerIndex(x,y,map,order):
    cIndex = 0
    # print >> sys.stderr, "Cell to check %d %d" % (x,y)
    for i in range(1,order+1):
        if x+i < 30 and map[x+i][y]!="x":
            cIndex+=1
        if x-i > -1 and map[x-i][y]!="x":
            cIndex+=1
        if y+i < 20 and map[x][y+i]!="x":
            cIndex+=1
        if y-i > -1 and map[x][y-i]!="x":
            cIndex+=1
            
        if x+i < 30 and y+i < 20 and map[x+i][y+i]!="x":
            cIndex+=1
        if x-i > -1 and y+i < 20 and map[x-i][y+i]!="x":
            cIndex+=1
        if y-i > -1 and x+i < 30 and map[x+i][y-i]!="x":
            cIndex+=1
        if y-i > -1 and x-i > -1 and map[x-i][y-i]!="x":
            cIndex+=1        
    return cIndex
        
def dirDangerIndex(x,y,map,action,dist,order):
    
    dIndex = 0   
    if action == "LEFT":
        for i in range(x-1,(x-dist-1)%30,-1):
            # print >> sys.stderr, "left %d" % i
            dIndex+=cellDangerIndex(i,y,map,order)
    elif action == "RIGHT":
        for i in range(x+1,(x+dist+1)%30):
            # print >> sys.stderr, "right %d" % i
            dIndex+=cellDangerIndex(i,y,map,order)
    elif action == "UP":
        for i in range(y-1,(y-dist-1)%20,-1):
            # print >> sys.stderr, "up %d" % i
            dIndex+=cellDangerIndex(x,i,map,order)
    elif action == "DOWN":
        for i in range(y+1,(y+dist+1)%20):
            # print >> sys.stderr, "down %d" % i
            dIndex+=cellDangerIndex(x,i,map,order)
    
    return dIndex
    

def displayMap(map):
    for j in xrange(20):
        for i in xrange(30):
            print >> sys.stderr, str(map[i][j]),
        print >> sys.stderr, "\n",

def computedistance(My_x,My_y,map,action):
    return compute(My_x,My_y,map,action,"x")

def compute(My_x,My_y,map,action,avoid):

    distance=0

    if action == "RIGHT":
        for i in xrange(My_x+1,30):
            if map[i][My_y]==avoid:
                distance +=1
            else:
                break

    elif action == "LEFT":
        for i in xrange(My_x-1,-1,-1):
            if map[i][My_y]==avoid:
                distance +=1
            else:
                break

    elif action == "DOWN":
        for i in xrange(My_y+1,20):
            if map[my_x][i]==avoid:
                distance +=1
            else:
                break

    elif action == "UP":
        for i in xrange(My_y-1,-1,-1):
            if map[my_x][i]==avoid:
                distance +=1
            else:
                break

    print >> sys.stderr, "DISTANCE " + str(action) + " " + str(distance)
    return distance

#Best path function
def bestPath(my_x, my_y, map, actions, last_action):

    print >> sys.stderr, "Best path --> " + str(actions)
    bestDir = None
    bestAction=""
    maxDist = 0
    minDangerIndex = 1000
    minThickness = 1000

    if use_thickness:
        for a in actions:
            dist = computedistance(my_x, my_y, map, a)
            next_point_dist = 0
            if a == "UP":
                next_point_dist=computedistance(my_x, (my_y-1)%15, map, a)
            elif a == "DOWN":
                next_point_dist=computedistance(my_x, (my_y+1)%15, map, a)
            elif a == "RIGHT":
                next_point_dist=computedistance((my_x+1)%30, my_y, map, a)
            elif a == "LEFT":
                next_point_dist=computedistance((my_x-1)%30, my_y, map, a)
            if a == last_action:
                dist = dist * same_dir_weight
            dist = dist + next_point_dist    
            if dist >= maxDist:
                bestAction = a
                maxDist = dist

        #Now we add the usage of t he tickness if the distance is 1
        if maxDist == 1:
            for a in actions:
                dist = computedistance(my_x, my_y, map, a)
                print >> sys.stderr, "Distance: " + str(a) + " " + str(dist) + " maxDist " + str(maxDist)
                thickness = computethickness(my_x, my_y, map, a)
                print >> sys.stderr, "Thick: " + str(a) + " " + str(thickness) + " minThick " + str(minThickness)
                if dist == maxDist and thickness < minThickness:
                    bestAction = a
                    minThickness = thickness
                    print >> sys.stderr, str(a) + " chosen"
    
    elif use_check_danger:
        for a in actions:
            dist = computedistance(my_x, my_y, map, a)
            if a == last_action:
                dist = dist * same_dir_weight
            dangerIndex = dirDangerIndex(my_x, my_y, map, a, dist, order)
            print >> sys.stderr, "Danger Index " + a + " " + str(dangerIndex)
            if dist > maxDist:
                bestAction = a
                maxDist = dist
                minDangerIndex = dangerIndex
            elif dist == maxDist and dangerIndex < minDangerIndex:
                bestAction = a
                minDangerIndex = dangerIndex

    
    else:
        for a in actions:
            dist = computedistance(my_x, my_y, map, a)*same_dir_weight
            dangerIndex = dirDangerIndex(my_x, my_y, map, a, dist, order)
            print >> sys.stderr, "Danger Index " + a + " " + str(dangerIndex)
            if dist > maxDist:
                bestAction = a
                maxDist = dist

    return bestAction

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
    
    # displayMap(map)
    
    my_next_x = (my_x+1)
    my_next_y = (my_y+1)
    my_prev_x = (my_x-1)
    my_prev_y = (my_y-1)
    
    print >>  sys.stderr, "My position " + str(my_x) + " " + str(my_y)
    # print >> sys.stderr, "Map surroundings R:" + str(map[my_next_x][my_y]) + " L:" + str(map[my_prev_x][my_y]) + " " + " U:" + str(map[my_x][my_prev_y]) + " D:" + str(map[my_x][my_next_y])

    if my_next_x < 30:
        R = map[my_next_x][my_y]
    else:
        R = None
    
    if my_prev_x > -1:
        L = map[my_prev_x][my_y]
    else:
        L = None
        
    if my_prev_y > -1:
        U = map[my_x][my_prev_y]
    else:
        U = None
        
    if my_next_y < 20:
        D = map[my_x][my_next_y]
    else:
        D = None
        
    if R=="x" and R != None:
        actions.append("RIGHT")

    if L=="x" and L != None:
        actions.append("LEFT")

    if U=="x" and U != None:
        actions.append("UP")

    if D=="x" and D != None:
        actions.append("DOWN")

        
    action_chosen = False
    print >> sys.stderr,  str(actions)
    #Check if we are facing a wall to perform a U turn
    if not(last_last_action in actions) and use_u_turn:
        print >> sys.stderr, "U turn activated"
        if last_last_action == "UP" and "DOWN" in actions:
            action = "DOWN"
            action_chosen = True
        elif last_last_action == "DOWN" and "UP" in actions:
            action = "UP"
            action_chosen = True
        elif last_last_action == "RIGHT" and "LEFT" in actions:
            action = "LEFT"
            action_chosen = True
        elif last_last_action == "LEFT" and "RIGHT" in actions:
            action = "RIGHT"
            action_chosen = True
        
    if not action_chosen:
        if action in actions and use_keep_last_action:
            action = last_action
        else:
            action = bestPath(my_x, my_y, map, actions, last_action)
            if not action:
                print >> sys.stderr, "RANDOM chosen..."
                   

    print >> sys.stderr, "A: %s LA: %s LLA:%s " % (action, last_action, last_last_action)
    print action
    last_last_action = last_action
    last_action = action