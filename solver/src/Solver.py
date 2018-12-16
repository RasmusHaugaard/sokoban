import time
import numpy as np

from .OpenList import OpenList
from .MapLoader import GOAL
from ..util.util import get_memory_usage, count_referenced_nodes

inf = float('inf')


def solve(_map, initial_states, NodeExpander, Heuristic, unit_cost, verbose=False, assign_children_to_parent=False):
    _start_time = time.time()
    node_expander = NodeExpander(_map, unit_cost)
    heuristic = Heuristic(_map, unit_cost)
    _search_start_time = time.time()

    open_list = OpenList()
    closed_set = {}

    for state in initial_states:
        state.total_cost, _ = heuristic(state)
    open_list.add_children(initial_states)

    _expanded_nodes_count = 0
    _min_h = inf

    goals = [tuple(pos) for pos in np.argwhere(_map == GOAL)]
    diamonds_solution = tuple(sorted(goals))

    while open_list.h:
        parent = open_list.extract_min()
        if parent.current_cost >= closed_set.get(hash(parent), inf) - 1e-8:
            continue
        closed_set[hash(parent)] = parent.current_cost
        _expanded_nodes_count += 1

        if parent.diamonds == diamonds_solution:
            if verbose:
                end_time = time.time()
                print('')
                print('Memory usage: {} MBs'.format(get_memory_usage()))
                print('Expanded nodes: {}'.format(_expanded_nodes_count))
                print('Open list size: {}'.format(len(open_list.h)))
                print('Nodes referenced: {}'.format(count_referenced_nodes(open_list.h + [parent])))
                print('')
                print('Init time: {:.2f} seconds.'.format(_search_start_time - _start_time))
                print('Search time: {:.2f} seconds.'.format(end_time - _search_start_time))
                print('Total time: {:.2f} seconds.'.format(end_time - _start_time))
            return parent

        children = []
        for child in node_expander(parent):
            if child.current_cost >= closed_set.get(hash(child), inf):
                continue
            h, _ = heuristic(child)
            child.total_cost = child.current_cost + h
            if child.total_cost != inf:
                children.append(child)
                if h < _min_h:
                    _min_h = h

        if assign_children_to_parent:
            parent.children = children

        open_list.add_children(children)

        if verbose and _expanded_nodes_count % 1000 == 0:
            print('-- {} k nodes expanded, min h: {:.2f}   '.format(_expanded_nodes_count // 1000, _min_h), end='\r')

    if verbose: print('')
    return None
