from Map import Map
import queue
import copy
import random

# t: list with  n, m cords of target
# s: priot pre move cell
# c: valid move vector egs [1,0]
def h(t, s , c):
    currCell = [s[0]+c[0], s[1]+c[1]]
    return abs(t[0]-currCell[0]) + abs(t[1]-currCell[1])

# return new state node in form of tuple
# (f, g ,[cell],[[m1],[m2],...])
#paramters:
# s: prior state node 
#world: Map object defininig problem space 
#move: 1X2 move vector eg [1,0]
# m: min or max prioty to g values in queue, -1 for max 1 for min
def genStateNode( s, world, move, m):
    moves= copy.copy(s[3])
    moves.append(move)
    g= abs(s[1])+1
    hur= h(world.getT(), s[2],move)
    newCell = (s[2][0]+move[0], s[2][1]+move[1])
    return (g+hur,m*g, newCell,moves)

#world: Map object defining problem space
 # m: min or max prioty to g values in queue, -1 for max 1 for min
def genRoute(world, m):
    visited = 0
    open = queue.PriorityQueue(0)
    closed= set()
    open.put_nowait((0+h(world.getT(), (world.n, world.m), [0,0]),m*0,(world.n, world.m),list()))
    while not(open.empty()):
        n =open.get_nowait()
        if not(n[2] in closed) and world.validCell(n[2]):
            visited+=1
            if world.isTarget(n[2]):
                return (n[3], visited)
            closed.add(n[2])

            open.put( genStateNode(n, world ,[1, 0], m) )
            open.put( genStateNode(n, world ,[0, 1], m) )
            open.put( genStateNode(n, world ,[-1,0], m) )
            open.put( genStateNode(n, world ,[0,-1], m) )
    
    return ([] , visted)

#gennerates nXn world of blocked and unblocked cells
#n: dimension, int
#fName: file name of where to save 
def genWorld(n, fName):
    currFile = open(fName, "+w")
    rows = list()
    
    for i in range(n):
        line = list()
        for j in range(n):
            x = random.randint(0,99)
            if x< 80:
                line.append(' ')
            else:
                line.append('B')
        rows.append(line)

    x = random.randint(0,n-1)
    y = random.randint(0,5)
    rows[x][y]= 'A'
    x = random.randint(0,n-1)
    y = random.randint(0,5)
    rows[x][n-1-y]= 'T'

    for r in rows:
        for char in r:
            currFile.write(char)
        if not(r == rows[len(rows)-1]):
            currFile.write('\n')
        
    currFile.close
# will create n worlds of x dimension
# will save to wolrd sub dirrectory to current 
def genWorlds(n,x):
    filePrefix = "./worlds/world"
    for i in range(n):
        genWorld(x, filePrefix+str(i)+".txt")


 #params:
 # print: t/f turns printing results on/off 
 # m: min or max prioty to g values in queue, -1 for max 1 for min 
 # file representing saved world
 # retuns number of expanded celss 

def reptAStar(p, m, fileName):
    expanded = 0
    w1= Map(fileName)
    while not(w1.isDone() ):
        if p:
            w1.display()
        result = genRoute(w1, m)
        moves = result[0]
        expanded += result[1]
        if len(moves)==0: 
            if p:
                print("No possible path")
            break
        for i in moves:
            if not(w1.move(i[0], i[1])):
                if p:
                    print("whoppies, re calcualtiong! ")
                break
    if p:
        w1.display()
    if w1.isDone():
        if p:
            print("Yay I did it! weeee!")
    del w1
    return expanded


if __name__ == "__main__":
    #load the 50 worlds 
    nWorlds = 50
    worldSize = 101
    make = False
    p = False
    if make: # if you want to re create worlds, over writes old data 
        genWorlds(nWorlds,worldSize)
    
    max = 0
    min = 0
   
    for i in range(nWorlds):
        print("world "+ str(i)+".1")
        max += reptAStar(p, -1, "./worlds/world"+str(i)+".txt")
        print("world "+ str(i)+".2")
        min += reptAStar(p,  1, "./worlds/world"+str(i)+".txt") 
        print("-----")
    print("RPT A*, max g tie break nodes expanded: %d", max)
    print("RPT A*, min g tie break nodes expanded: %d", min)
    #call backwards 
    #call adaptive 

    #print stats 



    

