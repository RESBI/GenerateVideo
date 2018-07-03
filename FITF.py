import time
import random
import os
from copy import deepcopy as DP

# [[mode, step], [mode, step], .......]
#  tree_1        tree_2        tree_n

boomRate = 50000
emptySteps = 1
spreadRate = 400
growUpRate = 10000

onTree = 0
onEmpty = 1
onFire = 5

Black = "\033[40m"
Red = "\033[41m"
Green = "\033[42m"

def getSet(length, fillWith):
    return [DP(fillWith) for k in range(length)]
           
def getGird(H, W, fillWith):
    a = getSet(W, fillWith)
    return [DP(a) for k in range(H)]

def Draw(Gird):
    print("\033[0;0H")
    for y in range(len(Gird)):
        line = ""
        for x in range(len(Gird[y])):
            a = Gird[y][x][0]
            if a == 0:
                line += "{}  ".format(Green)
            elif a == 1:
                line += "{}  ".format(Black)
            elif a == 5:
                line += "{}  ".format(Red)
        print(line)

def getRandomForest(Gird):
    for y in range(len(Gird)):
        for x in range(len(Gird[y])):
            Gird[y][x][0] = random.choice([onTree, onEmpty, onEmpty])
            Gird[y][x][1] = 0

    return DP(Gird)

def getNewForest(Gird, growUpRate, boomRate, emptySteps):
    newForest = DP(emptyForest)
    for y in range(len(Gird)):
        for x in range(len(Gird[y])):
            
            Mode = Gird[y][x][0]
            Step = Gird[y][x][1]

            a = Gird[((y-1)+len(Gird))%len(Gird)][x]
            b = Gird[y][((x+1)+len(Gird[0]))%len(Gird[0])]
            c = Gird[((y+1)+len(Gird))%len(Gird)][x]
            d = Gird[y][((x-1)+len(Gird[0]))%len(Gird[0])]
            modes = [a[0], b[0], c[0], d[0]]
            steps = [a[1], b[1], c[1], d[1]]
            
            Trees = 0
            for m in modes:
                if m == onTree:
                    Trees += 1
            Trees /= 2
                    
            if (Mode == onFire) and (Step >= emptySteps):
                newForest[y][x][0] = onEmpty
                newForest[y][x][1] = 0
                continue
        
            elif (onFire in modes) and (Mode == onTree):# and (emptySteps in steps):
                newForest[y][x][0] = onFire
                newForest[y][x][1] += 1

            elif Mode == onEmpty:
                newForest[y][x][0] = onEmpty
                if onTree in modes:
                    if random.randint(1, int(spreadRate/Trees)) == 1:
                        newForest[y][x][0] = onTree
                elif random.randint(1, growUpRate) == 1:
                    newForest[y][x][0] = onTree
                    
            elif Mode == onTree:
                newForest[y][x][0] = onTree
                if random.randint(1, boomRate) == 1:
                    newForest[y][x][0] = onFire
                    
    return DP(newForest)


emptyForest = getGird(30, 30, [0, 0])
Forest = getRandomForest(emptyForest)
os.system("clear")
OForest = Forest
while 1:
    if OForest != Forest:
        Draw(Forest)
    Forest = OForest
    OForest = getNewForest(Forest, growUpRate, boomRate, emptySteps)
#print(Forest)
