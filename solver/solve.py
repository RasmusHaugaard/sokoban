import os
import sys

from .src.AgentStateNodeExpander import AgentStateNodeExpander as NodeExpander
from .src.Heuristics import get_heuristic
from .src.UnitCost import default_unit_cost as unit_cost
from .src.MapLoader import load_map
from .src.Solver import solve


def main():
    if len(sys.argv) < 3:
        print('need both map and heuristic arguments')
        return
    map_path = sys.argv[1]
    Heuristic = get_heuristic(sys.argv[2])
    _map, initial_states = load_map(map_path)
    node = solve(_map, initial_states, NodeExpander, Heuristic, unit_cost, verbose=True)

    if not node:
        print('Did not find a solution')
        return

    solution = [node]
    while node.parent:
        node = node.parent
        solution.append(node)
    solution.reverse()

    print('Found a solution in {} steps with cost: {}'.format(len(solution) - 1, solution[-1].current_cost))

    solution_dir_path = 'solver/solutions'

    if not os.path.isdir(solution_dir_path):
        os.mkdir(solution_dir_path)
    solution_path = '{}/{}:{}.txt'.format(
        solution_dir_path,
        os.path.basename(map_path).split('.')[0],
        str(unit_cost).replace(' ', '')
    )
    solution_file = open(solution_path, 'w')

    with open(map_path, 'r') as map_file:
        solution_file.writelines(map_file.readlines())

    for node in solution:
        solution_file.write(str(node) + '\n')


if __name__ == '__main__':
    main()
