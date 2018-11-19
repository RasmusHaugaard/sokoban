from OpenList import OpenList
from MapLoader import GOAL, load_map

inf = float('inf')


def is_solution(_map, state):
    for diamond in state.diamonds:
        if _map[diamond] != GOAL:
            return False
    return True


def solve(_map, initial_states, NodeExpander, Heuristic, unit_cost):
    print('initializing node expander', NodeExpander)
    node_expander = NodeExpander(_map, unit_cost)
    print('initializing heuristic', Heuristic)
    heuristic = Heuristic(_map, unit_cost)
    print('initialization done')

    closed_set = set()
    for state in initial_states:
        state.total_cost = heuristic(state)

    open_list = OpenList()
    open_list.add_children(initial_states)

    i = 0
    while open_list.h:
        parent = open_list.extract_min()
        if is_solution(_map, parent):
            return parent
        closed_set.add(hash(parent))

        children = []
        for child in node_expander(parent):
            if hash(child) in closed_set:
                continue
            child.total_cost = child.current_cost + heuristic(child)
            if child.total_cost != inf:
                children.append(child)

        open_list.add_children(children)

        i += 1
        if i % 1000 == 0:
            print(i // 1000, 'k nodes expanded')
    return None


def main():
    import sys
    from AgentStateNodeExpander import AgentStateNodeExpander as NodeExpander
    from ClosestHeuristic import ClosestHeuristic as Heuristic
    from UnitCost import default_unit_cost
    from time import time

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

    map_file = open(map_path, 'r')
    solution_path = 'solution/{}:{}.txt'.format(map_path.split('.')[0], int(time()))
    solution_file = open(solution_path, 'w')
    solution_file.writelines(map_file.readlines())

    for node in solution:
        solution_file.write(str(node) + '\n')


if __name__ == '__main__':
    main()
