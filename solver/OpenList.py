import heapq


class OpenListBubbleSort:
    list = []

    def add_children(self, children):
        self.list += children
        for iter_num in range(len(self.list) - 1, 0, -1):
            for idx in range(iter_num):
                if self.list[idx].total_cost > self.list[idx + 1].total_cost:
                    temp = self.list[idx]
                    self.list[idx] = self.list[idx + 1]
                    self.list[idx + 1] = temp


class OpenListQuickSort:
    list = []

    def add_children(self, children):
        self.list += children
        self.list.sort(key=lambda state: state.total_cost)


class OpenListInsert:
    list = []

    def add_children(self, children):
        for child in children:
            self.list.insert(
                self.bisect(self.list, child.total_cost),
                child
            )

    @staticmethod
    def bisect(a, v):
        lo = 0
        hi = len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if v < a[mid].total_cost:
                hi = mid
            else:
                lo = mid + 1
        return lo


class TreeNode:
    lo = None
    hi = None

    def __init__(self, state, cost):
        self.state = state
        self.cost = cost


class OpenListInsertTree:
    root = None

    def add_children(self, children):
        for child in children:
            cost = child.total_cost
            new_node = TreeNode(child, cost)
            if self.root is None:
                self.root = new_node
            else:
                node = self.root
                while True:
                    if node.cost > cost:
                        if node.hi is None:
                            node.hi = new_node
                            break
                        node = node.hi
                    else:
                        if node.lo is None:
                            node.lo = new_node
                            break
                        node = node.lo


class OpenListHeap:
    h = []

    def add_children(self, children):
        for child in children:
            heapq.heappush(self.h, (child.total_cost, child))

    def take_head(self):
        return heapq.heappop(self.h)[1]


if __name__ == '__main__':
    from time import time
    from random import random


    class State:
        def __init__(self, cost):
            self.total_cost = cost


    for Open in (OpenListBubbleSort, OpenListQuickSort, OpenListInsert, OpenListInsertTree, OpenListHeap):
        start_time = time()
        open_list = Open()
        count = 0
        while time() - start_time < 1:
            open_list.add_children([
                State(random()),
                State(random()),
                State(random()),
                State(random()),
            ])
            count += 1

        print(Open, ": ", count)

# OUTPUT:
# <class '__main__.OpenListBubbleSort'> :  110
# <class '__main__.OpenListQuickSort'> :  1781
# <class '__main__.OpenListInsert'> :  15993
# <class '__main__.OpenListInsertTree'> :  26381
# <class '__main__.OpenListHeap'> :  112472

# Default OpenList chosen based on tests:
OpenList = OpenListHeap
