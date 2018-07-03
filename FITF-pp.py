import time
import random
import os
import pp
#from copy import deepcopy as dp
import copy
from PIL import Image as img

ppservers = ("192.168.0.104:12337", "192.168.0.102:12337", "192.168.0.100:12337",)
job_server = pp.Server(4, ppservers=ppservers,secret="1222",)#secret="xx")

# [[mode, step], [mode, step], .......]
#  tree_1        tree_2        tree_n

boomRate = 1000000
emptySteps = 1
spreadRate = 200
growUpRate = 100000

onTree = 0
onEmpty = 1
onFire = 5

Black = "\033[40m"
Red = "\033[41m"
Green = "\033[42m"

H = 800
W = 1280

def getPart(area, Parts):
    aa = []
    for l in range(0, area, int(area/Parts)):
        a = l
        b = l + int(area/Parts)
        if b - area >= 0:
            b = area
        aa += [[a,b]]
    return aa

def getSet(length, fillWith):
    return [copy.deepcopy(fillWith) for k in range(length)]
           
def getGird(H, W, fillWith):
    a = getSet(W, fillWith)
    return [copy.deepcopy(a) for k in range(H)]

def Draw(Gird, num):
    temp = img.new("RGB", (W, H), (0, 0, 0))
    for y in range(len(Gird)):
        for x in range(len(Gird[y])):
            a = Gird[y][x][0]
            if a == 0:
                temp.putpixel([x, y],(0, 255, 0))
                #line += "{}  ".format(Green)
            elif a == 1:
                temp.putpixel([x, y],(0, 0, 0))
                #line += "{}  ".format(Black)
            elif a == 5:
                temp.putpixel([x, y],(255, 0, 0))
                #line += "{}  ".format(Red)
    temp.save("pics/{}.jpg".format(num))
    
def getRandomForest(Gird):
    for y in range(len(Gird)):
        for x in range(len(Gird[y])):
            if random.random() >= 0.7:
                Gird[y][x][0] = onTree
            else:
                Gird[y][x][0] = onEmpty
                
            Gird[y][x][1] = 0

    return copy.deepcopy(Gird)

def getNewForest(Gird, part, growUpRate, boomRate, emptySteps, spreadRate, onTree, onFire, onEmpty):
    newForest = getGird(part[1] - part[0], len(Gird[0]), [0, 0])
    for dy in range(part[1]- part[0]):
        for x in range(len(Gird[dy])):
            y = dy + part[0]
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
                newForest[dy][x][0] = onEmpty
                newForest[dy][x][1] = 0
                continue
        
            elif (onFire in modes) and (Mode == onTree):# and (emptySteps in steps):
                newForest[dy][x][0] = onFire
                newForest[dy][x][1] += 1

            elif Mode == onEmpty:
                newForest[dy][x][0] = onEmpty
                if onTree in modes:
                    if random.randint(1, int(spreadRate/Trees)) <= 1:
                        newForest[dy][x][0] = onTree
                elif random.randint(1, growUpRate) <= 1:
                    newForest[dy][x][0] = onTree
                    
            elif Mode == onTree:
                newForest[dy][x][0] = onTree
                if random.randint(1, boomRate) <= 1:
                    newForest[dy][x][0] = onFire
                    
    return newForest

def Out(mode,types,end="\n"):
    modes = ["Ok","Wr","Er","Nt"]
    colos = ["92","93","95","91"]
    if mode in modes:
        for cou in range(len(modes)):
            if mode == modes[cou]:
                print("\033[1;"+colos[cou]+"m"+str(types),end=end)
                break
    else:
        Out("Er","No this mode: "+mode)


emptyForest = getGird(H, W, [0, 0])
Forest = getRandomForest(emptyForest)
os.system("clear")
OForest = Forest
parts = 8
pics = 0

while 1:
    pics += 1
    Out("Ok", "Drawing...")
    Draw(Forest, pics)
    os.system("clear")
    
    Out("Ok", "Now is the {} rool.".format(pics))
    a = time.time()    
    Parts = getPart(H, parts)
    OForest = Forest
    Forest = []#0 for m in range(parts)]
    Out("Wr", "Caculating next forest...")
    jobs = [(job_server.submit(getNewForest, (OForest, Parts[i], growUpRate, boomRate, emptySteps, spreadRate, onTree, onFire, onEmpty,), (getGird, getSet,), ("random", "copy",)), i) for i in range(len(Parts))]
    for job, k in jobs:
        Forest += job()
    Out("Ok", "Done.")
    Out("Wr", "{} pic/sec".format(1/(time.time()-a)))
    #print(Forest)
#print(Forest)
