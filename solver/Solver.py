class StateNode:
    current_cost = 0
    total_cost = 0

    def __init__(self, _map, a, d):
        self.map = _map
        self.a = a
        self.d = d

    def hash(self):
        return str([self.a] + self.d)




def solve(heuristic, _map, init_state):
    pass


def mergeLists(openList, children):
    openList.extend(children)

    bubblesort(openList)


def bubblesort(openList):
    i = 1

# Swap the elements to arrange in order
    for iter_num in range(len(openList)-1,0,-1):
        for idx in range(iter_num):
            if (openList[idx].manhatten + (i*openList[idx].depth)) > (openList[idx+1].manhatten + (i*openList[idx+1].depth)):
                temp = openList[idx]
                openList[idx] = openList[idx+1]
                openList[idx+1] = temp


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
            if (np.array_equal(children[-1].map, closedSet[i].map)):
                childExists = 1
                break

        # Test if child is already in openList
        for i in range(len(openList)):
            if (np.array_equal(children[-1].map, openList[i].map)):
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
            if (np.array_equal(children[-1].map, closedSet[i].map)):
                childExists = 1
                break

        # Test if child is already in openList
        for i in range(len(openList)):
            if (np.array_equal(children[-1].map, openList[i].map)):
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
            if (np.array_equal(children[-1].map, closedSet[i].map)):
                childExists = 1
                break

        # Test if child is already in openList
        for i in range(len(openList)):
            if (np.array_equal(children[-1].map, openList[i].map)):
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
            if (np.array_equal(children[-1].map, closedSet[i].map)):
                childExists = 1
                break

        # Test if child is already in openList
        for i in range(len(openList)):
            if (np.array_equal(children[-1].map, openList[i].map)):
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

