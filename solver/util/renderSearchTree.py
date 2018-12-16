import sys
from graphviz import Digraph

from ..src.MapLoader import load_map
from ..src.AgentStateNodeExpander import AgentStateNodeExpander as NodeExpander
from ..Solver import solve
from ..src.MinMatchingHeuristic import MinMatchingHeuristic as Heuristic
from ..src.UnitCost import default_unit_cost

DIR_NAME = ['U', 'R', 'D', 'L']


def main():
    if len(sys.argv) < 2:
        print('no map file argument given')
        return
    map_path = sys.argv[1]
    map_name = '.'.join(map_path.split('.')[:-1])
    _map, initial_states = load_map(map_path)
    end_node = solve(_map, initial_states, NodeExpander, Heuristic, default_unit_cost, assign_children_to_parent=True)

    if not end_node:
        print('Did not find a solution')
        return

    solution = [end_node]
    node = end_node
    while node.parent:
        node = node.parent
        solution.append(node)
    solution.reverse()

    def get_children(parent):
        return getattr(parent, 'children', [])

    def _expand(parent, fun):
        fun(parent)
        for child in get_children(parent):
            _expand(child, fun)

    def expand(fun):
        for _node in initial_states:
            _expand(_node, fun)

    dot = Digraph()
    dot.node_attr.update(shape='plaintext', fontsize='24', fixedsize='true', height='.4', width='.4')

    def add_index(node):
        node.i = add_index.i
        add_index.i += 1
    add_index.i = 0

    def add_node(node):
        name = DIR_NAME[node.agent[2]]
        if node in solution:
            dot.node(str(node.i), name, shape='circle')
        else:
            dot.node(str(node.i), name)

    def add_edge(parent):
        for child in get_children(parent):
            dot.edge(str(parent.i), str(child.i))

    expand(add_index)
    expand(add_node)
    expand(add_edge)

    dot.format = 'png'
    dot.render('search-tree-{}'.format(map_name), view=True)


if __name__ == '__main__':
    main()
