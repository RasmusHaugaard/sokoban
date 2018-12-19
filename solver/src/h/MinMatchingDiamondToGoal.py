import numpy as np
from scipy.optimize import linear_sum_assignment

from ...util import util
from . import CostCache

ANY = CostCache.ANY
inf = float('inf')
fake_inf = 1e100


def min_matching_diamond_to_goal(diamond_move_cost_cache, goals, unit_cost, cm, diamonds):
    for i, diamond in enumerate(diamonds):
        for j, goal in enumerate(goals):
            move = diamond + goal
            cm[i, j] = min(fake_inf, diamond_move_cost_cache[move])
    costs = cm[linear_sum_assignment(cm)]
    h = costs.sum()

    # fake_inf is used, scipy linear-sum-assignment can't handle the float('inf')
    if h >= fake_inf:
        h = inf

    # fix: state node explorer does not add the last push cost
    if h > 0:
        h -= unit_cost.push

    return h


class MinMatchingDiamondToGoal:
    def __init__(self, _map, unit_cost):
        self.goals = util.get_goals(_map)
        self.unit_cost = unit_cost
        self.diamond_move_cost_cache = \
            CostCache.build_diamond_move_cost_cache(_map, unit_cost)
        n = len(self.goals)
        self.cm = np.empty((n, n), np.float)
        self.h = {}

    def __call__(self, state):
        h = self.h.get(state.diamonds, None)
        if h is not None:
            return h, ()
        h = min_matching_diamond_to_goal(self.diamond_move_cost_cache, self.goals, self.unit_cost, self.cm, state.diamonds)
        self.h[state.diamonds] = h
        return h, ()


def main():
    from ..MapLoader import load_map
    from ..UnitCost import default_unit_cost

    for map_path in ['test-map1.txt', 'test-map2.txt', 'test-map3.txt', 'test-map4.txt', 'test-map5.txt']:
        _map, init_states = load_map('solver/maps/' + map_path)
        heuristic = MinMatchingDiamondToGoal(_map, default_unit_cost)
        h, _ = heuristic(init_states[0])
        print(map_path, h)


if __name__ == '__main__':
    main()
