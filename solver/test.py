import numpy as np
from node import Node
from copy import deepcopy
from time import *

#-------------------------------------------------------------------------------

def expandNode(openList, closedSet):
    global nodeID
    head = openList[0]
    childExists = 0
    children = []

    if (head.up_test() == 0):
        children.append(deepcopy(head))
        children[-1].up()
        
        # Test if child is already in closedSet
        for i in range(len(closedSet)):
            if (np.array_equal(children[-1].map,closedSet[i].map)):
                childExists = 1
                break

        # Test if child is already in openList
        for i in range(len(openList)):
            if (np.array_equal(children[-1].map,openList[i].map)):
                childExists = 1
                break

        if (childExists == 1):
            del children[-1]      
        else:
            nodeID += 1
            children[-1].setNodeID(nodeID)
            children[-1].setParent(head.nodeID)
            children[-1].setManhatten()
        
        childExists = 0
        



    if (head.down_test() == 0):
        children.append(deepcopy(head))
        children[-1].down()

        # Test if child is already in closedSet
        for i in range(len(closedSet)):
            if (np.array_equal(children[-1].map,closedSet[i].map)):
                childExists = 1
                break

        # Test if child is already in openList
        for i in range(len(openList)):
            if (np.array_equal(children[-1].map,openList[i].map)):
                childExists = 1
                break

        if (childExists == 1):
            del children[-1]      
        else:
            nodeID += 1
            children[-1].setNodeID(nodeID)
            children[-1].setParent(head.nodeID)
            children[-1].setManhatten()
            
        childExists = 0
        

    if (head.right_test() == 0):
        children.append(deepcopy(head))
        children[-1].right()

        # Test if child is already in closedSet
        for i in range(len(closedSet)):
            if (np.array_equal(children[-1].map,closedSet[i].map)):
                childExists = 1
                break

        # Test if child is already in openList
        for i in range(len(openList)):
            if (np.array_equal(children[-1].map,openList[i].map)):
                childExists = 1
                break

        if (childExists == 1):
            del children[-1]      
        else:
            nodeID += 1
            children[-1].setNodeID(nodeID)
            children[-1].setParent(head.nodeID)
            children[-1].setManhatten()

        childExists = 0
        

    if (head.left_test() == 0):
        children.append(deepcopy(head))
        children[-1].left()

        # Test if child is already in closedSet
        for i in range(len(closedSet)):
            if (np.array_equal(children[-1].map,closedSet[i].map)):
                childExists = 1
                break

        # Test if child is already in openList
        for i in range(len(openList)):
            if (np.array_equal(children[-1].map,openList[i].map)):
                childExists = 1
                break

        if (childExists == 1):
            del children[-1]      
        else:
            nodeID += 1
            children[-1].setNodeID(nodeID)
            children[-1].setParent(head.nodeID)
            children[-1].setManhatten()

        childExists = 0
        

    openList.pop(0)
    closedSet.append(head)

    return children


def mergeLists(openList, children):
    openList.extend(children)

    bubblesort(openList)  

#-------------------------------------------------------------------------------


#file = open('2017-competation-map.txt', 'r')
file = open('test-map1.txt', 'r')

map_info = file.readline()
map_raw = file.readlines()

width = int(map_info[0] + map_info[1])
height = int(map_info[3] + map_info[4])
number_diamonds = int(map_info[6] + map_info[7])

r_pos_x_start = 0
r_pos_y_start = 0

print("Width: " + str(width))
print("Height: " + str(height))
print ("Number of diamonds: " + str(number_diamonds))
print ("-------------------------------------------------")

# Extend map to rectangular shape
for i in range(height):
    while len(map_raw[i]) < (width+1): # + Null-terminator
        map_raw[i] = map_raw[i] + "X"

# Replace empty spaces with 'X'
for i in range(height):
    map_raw[i] = map_raw[i].replace('\n', 'X')
    map_raw[i] = map_raw[i].replace(' ', 'X')


# Initialize map
map = np.chararray((height,width))  # y,x

for i in range(height):
    for j in range(width):
        map[i,j] = map_raw[i][j]
        if map[i,j] == b'M':
            r_pos_x_start = j
            r_pos_y_start = i
            

#-------------------------------------------------------------------------------


#def manhatten2():

#    manhatten = 0
#    buffer = []

#    diamond_mask = map.count(b'J')
#    diamonds = np.transpose(np.nonzero(diamond_mask))

#    print(np.size(diamonds))

#    goal_mask = map.count(b'G')
#    goals = np.transpose(np.nonzero(goal_mask))

#    print(diamonds)
#    print(goals)

#    for i in range(np.shape(diamonds)[0]):
#        for j in range(np.shape(diamonds)[1]):
#            buffer.append(abs(diamonds[i,0] - goals[j,0]) + abs(diamonds[i,1] - goals[j,1]))
            
#        manhatten += min(buffer)
#        del buffer[:]
        #print(manhatten)

#    return manhatten

    
#def bubblesort(list):

# Swap the elements to arrange in order
#    for iter_num in range(len(list)-1,0,-1):
#        for idx in range(iter_num):
#            if list[idx]>list[idx+1]:
#                temp = list[idx]
#                list[idx] = list[idx+1]
#                list[idx+1] = temp


#list = [19,2,31,45,6,11,121,27]
#bubblesort(list)
#print(list)

def bubblesort(openList):
    i = 1

# Swap the elements to arrange in order
    for iter_num in range(len(openList)-1,0,-1):
        for idx in range(iter_num):
            #if openList[idx].manhatten > openList[idx+1].manhatten:

                
            if (openList[idx].manhatten + (i*openList[idx].depth)) > (openList[idx+1].manhatten + (i*openList[idx+1].depth)):

                
            #if openList[idx].depth < openList[idx+1].depth:
                temp = openList[idx]
                openList[idx] = openList[idx+1]
                openList[idx+1] = temp



    
    

#-------------------------------------------------------------------------------
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




