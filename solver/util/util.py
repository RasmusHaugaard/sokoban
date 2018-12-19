import gc
import os
import psutil
import numpy as np

from ..src.MapLoader import load_map, GOAL
from ..src.StateNode import StateNode

DIRECTIONS = 0, 1, 2, 3, 4
UP, RIGHT, DOWN, LEFT, ANY = DIRECTIONS
OPPOSITE_DIR = [DOWN, LEFT, UP, RIGHT, ANY]


def move(y, x, d):
    if d == UP:
        return y - 1, x
    elif d == RIGHT:
        return y, x + 1
    elif d == DOWN:
        return y + 1, x
    return y, x - 1


def get_goals(_map):
    return [tuple(goal) for goal in np.argwhere(_map == GOAL)]


def load_solution(path):
    _map, _ = load_map(path)
    with open(path, 'r') as f:
        _, h, _ = [int(v) for v in f.readline().split()]
        for _ in range(h):
            f.readline()
        solution = [StateNode.from_str(line) for line in f.readlines() if ':' in line]
    return _map, solution


def get_memory_usage():  # in MB
    gc.collect()
    return psutil.Process(os.getpid()).memory_info().rss // 10 ** 6


def count_referenced_nodes(open_list):
    visited = set()

    def count(node):
        if node not in visited:
            visited.add(node)
            count.i += 1
    count.i = 0

    for node in open_list:
        count(node)
        while node.parent:
            node = node.parent
            count(node)

    return count.i
