import numpy as np
from node import Node
from copy import deepcopy
from time import *

openList = []
closedSet = []

nodeID = 0

openList.append(Node(map,r_pos_x_start,r_pos_y_start))

t1 = clock()

for i in range(1000000):
    if (len(openList) == 0):
        print("fail")
        break
    else :
        if (openList[0].goal(number_diamonds) == 0):
            print("success:", i)
            #print(openList[0].map)
            #print("depth:", openList[0].depth)
            #print("action:", openList[0].action)
            #print("parent:", openList[0].parent)
            #print("nodeID:", openList[0].nodeID)
            break
        else :
            children = expandNode(openList, closedSet)
            mergeLists(openList, children)

t2 = clock()



print("closedSet:", len(closedSet))
print("openList:", len(openList))

print("time:", t2-t1, "sec")

#-------------------------------------------------------------------------------

path = []
path.append(openList[0])

while (path[-1].parent != -1):
    for i in range(len(closedSet)):
        if (closedSet[i].nodeID == path[-1].parent):
            #print("parent:", i)
            path.append(closedSet[i])


path.reverse()


print ("-------------------------------------------------")
for i in range(len(path)):
    print(path[i].action)
    #print(path[i].manhatten)
    #print(path[i].map)

#for i in range(len(openList)):
    #print(openList[i].depth)

#bubblesort()

#for i in range(len(openList)):
    #print(openList[i].manhatten)

file.close()




