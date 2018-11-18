from OpenList import OpenList
from MapLoader import GOAL, load_map


def is_solution(_map, state):
    for diamond in state.diamonds:
        if _map[diamond] != GOAL:
            return False
    return True


def solve(_map, initial_state, NodeExpander, Heuristic, unit_cost):

    print('initializing node expander')
    node_expander = NodeExpander(_map, unit_cost)
    print('initializing heuristic')
    heuristic = Heuristic(_map, unit_cost)
    print('initialization done')

    closed_set = set()
    initial_state.total_cost = heuristic(initial_state)
    cached_heuristics = {
        initial_state: initial_state.total_cost
    }

    open_list = OpenList()
    open_list.add_children([initial_state])

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
            h = cached_heuristics.get(child, None)
            if h is None:
                h = heuristic(child)
                cached_heuristics[child] = h
            child.total_cost = child.current_cost + h
            children.append(child)

        open_list.add_children(children)

        i += 1
        if i % 1000 == 0:
            print(i // 1000, 'k nodes expanded')


def main():
    import sys
    from AgentStateNodeExpander import AgentStateNodeExpander as NodeExpander
    from ManhattanHeuristic import ManhattanHeuristic as Heuristic
    from UnitCost import default_unit_cost

    if len(sys.argv) < 2:
        print('no map file argument given')
        return
    path = sys.argv[1]
    _map, initial_state = load_map(path)
    solution = solve(_map, initial_state, NodeExpander, Heuristic, default_unit_cost)
    print(solution)


if __name__ == '__main__':
    main()
