from OpenList import OpenList
from MapLoader import GOAL, load_map
from time import time

inf = float('inf')


def is_solution(_map, state):
    for diamond in state.diamonds:
        if _map[diamond] != GOAL:
            return False
    return True


def solve(_map, initial_states, NodeExpander, Heuristic, unit_cost):
    _start_time = time()

    print('initializing node expander', NodeExpander)
    node_expander = NodeExpander(_map, unit_cost)
    _exp_time = time()
    print('Node expander initialized in {} seconds'.format(_exp_time - _start_time))

    print('initializing heuristic', Heuristic)
    heuristic = Heuristic(_map, unit_cost)
    _heu_time = time()
    print('Heuristic initialized in {} seconds'.format(_heu_time - _exp_time))

    closed_set = set()
    for state in initial_states:
        state.total_cost = heuristic(state)

    open_list = OpenList()
    open_list.add_children(initial_states)

    _extracted_nodes_count = 0
    _extracted_nodes_in_closed_set = 0
    _child_nodes_count = 0
    _child_nodes_in_closed_set = 0
    _min_h = inf

    while open_list.h:
        parent = open_list.extract_min()
        _extracted_nodes_count += 1
        if hash(parent) in closed_set:
            _extracted_nodes_in_closed_set += 1
            continue
        closed_set.add(hash(parent))

        if is_solution(_map, parent):
            print('')
            print('Solution found in {} seconds'.format(time() - _heu_time))
            print('Total time: {} seconds'.format(time() - _start_time))
            expanded_nodes_count = _extracted_nodes_count - _extracted_nodes_in_closed_set
            cache_ratio = _extracted_nodes_in_closed_set / _extracted_nodes_count
            print('Expanded nodes: {}, Cache Ratio: {:.2f}'
                  .format(expanded_nodes_count, cache_ratio))

            appended_child_nodes_count = _child_nodes_count - _child_nodes_in_closed_set
            cache_ratio = _child_nodes_in_closed_set / _child_nodes_count
            print('Appended nodes: {}, Cache Ratio: {:.2f}'
                  .format(appended_child_nodes_count, cache_ratio))
            return parent

        children = []
        for child in node_expander(parent):
            _child_nodes_count += 1
            if hash(child) in closed_set:
                _child_nodes_in_closed_set += 1
                continue
            h = heuristic(child)
            child.total_cost = child.current_cost + h
            if child.total_cost != inf:
                children.append(child)
                if h < _min_h:
                    _min_h = h

        open_list.add_children(children)

        expanded_nodes_count = _extracted_nodes_count - _extracted_nodes_in_closed_set
        if expanded_nodes_count % 1000 == 0:
            print(' {} k nodes expanded, min h: {:.2f}   '.format(expanded_nodes_count // 1000, _min_h), end='\r')
    print('')
    return None


def main():
    import sys
    from AgentStateNodeExpander import AgentStateNodeExpander as NodeExpander
    from MinMatchingHeuristic import MinMatchingHeuristic as Heuristic
    from UnitCost import default_unit_cost
    import os

    if len(sys.argv) < 2:
        print('no map file argument given')
        return
    map_path = sys.argv[1]
    _map, initial_states = load_map(map_path)
    node = solve(_map, initial_states, NodeExpander, Heuristic, default_unit_cost)

    if not node:
        print('Did not find a solution')
        return

    solution = [node]
    while node.parent:
        node = node.parent
        solution.append(node)
    solution.reverse()

    print('Found a solution in {} steps with cost: {}'.format(len(solution) - 1, solution[-1].current_cost))

    if not os.path.isdir('solutions'):
        os.mkdir('solutions')
    solution_path = 'solutions/{}:{}.txt'.format(
        map_path.split('.')[0],
        str(default_unit_cost).replace(' ', '')
    )
    solution_file = open(solution_path, 'w')

    with open(map_path, 'r') as map_file:
        solution_file.writelines(map_file.readlines())

    for node in solution:
        solution_file.write(str(node) + '\n')


if __name__ == '__main__':
    main()
