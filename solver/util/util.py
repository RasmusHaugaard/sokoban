import gc
import os
import psutil

from ..src.MapLoader import load_map
from ..src.StateNode import StateNode


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
