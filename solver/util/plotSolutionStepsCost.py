from matplotlib import pyplot as plt
from glob import glob
import os

from .util import load_solution
from ..src.Heuristics import get_heuristic, heuristic_keys
from ..src.UnitCost import default_unit_cost as unit_cost
from .calcSolutionCost import calc_solution_cost


solutions = (
    ('test map 3c', '3c'),
    ('test map 4', '4'),
    ('test map 5', '5'),
    ('2015 comp', '2015'),
    ('2017 comp', '2017'),
    ('2018 comp', '2018'),
)


def main():
    plt.figure(figsize=(6, 4))

    for i, (name, path) in enumerate(solutions):
        plt.subplot(2, 3, i + 1)
        _map, solution = load_solution('solver/evalsolutions/{}.txt'.format(path))
        node_path_costs = calc_solution_cost(solution, unit_cost)
        final_cost = node_path_costs[-1]

        optimal_heuristic = [final_cost - cost for cost in node_path_costs]
        plt.plot(optimal_heuristic, label='optimal heuristic')

        for key in heuristic_keys:
            heuristic = get_heuristic(key)(_map, unit_cost)
            node_heuristics = [heuristic(node) for node in solution]
            heuristic_totals = [h[0] for h in node_heuristics]
            plt.plot(heuristic_totals, label=key)

        plt.title(name)
        plt.legend()

    plt.tight_layout(pad=0)
    plt.savefig('solver/evalsolutions/eval.png', dpi=300)


if __name__ == '__main__':
    main()
