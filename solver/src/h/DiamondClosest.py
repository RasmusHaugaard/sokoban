import numpy as np

from ...util import util
from . import CostCache


def diamond_closest(diamond_move_cost_cache, goals, unit_cost, cm, diamonds):
    for i, diamond in enumerate(diamonds):
        for j, goal in enumerate(goals):
            move = diamond + goal
            cm[i, j] = diamond_move_cost_cache[move]

    diamond_to_closest_goal = cm.min(axis=0).sum()
    closest_diamond_to_goal = cm.min(axis=1).sum()
    h = max(diamond_to_closest_goal, closest_diamond_to_goal)

    # fix: state node explorer does not add the last push cost
    if h > 0:
        h -= unit_cost.push

    return h


class DiamondClosest:
    meta = ()

    def __init__(self, _map, unit_cost):
        self.goals = util.get_goals(_map)
        self.unit_cost = unit_cost
        self.diamond_move_cost_cache = \
            CostCache.build_diamond_move_cost_cache(_map, unit_cost)
        n = len(self.goals)
        self.cm = np.empty((n, n), dtype=np.float)
        self.h_cache = {}

    def __call__(self, state):
        h = self.h_cache.get(state.diamonds, None)
        if h is not None:
            return h, ()
        h = diamond_closest(self.diamond_move_cost_cache, self.goals, self.unit_cost, self.cm, state.diamonds)
        self.h_cache[state.diamonds] = h
        return h, ()


def main():
    from ..MapLoader import load_map
    from ..UnitCost import default_unit_cost

    for map_path in ['test-map1.txt', 'test-map2.txt', 'test-map3.txt', 'test-map4.txt', 'test-map5.txt']:
        _map, init_states = load_map('solver/maps/' + map_path)
        heuristic = DiamondClosest(_map, default_unit_cost)
        h, _ = heuristic(init_states[0])
        print(map_path, h)


if __name__ == '__main__':
    main()
