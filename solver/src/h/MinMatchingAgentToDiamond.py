import numpy as np
from scipy.optimize import linear_sum_assignment

from ...util import util
from . import CostCache


def min_matching_agent_to_diamond(agent_g2d_move_cost_cache, goals, cm, diamonds):
    for i, goal in enumerate(goals):
        for j, diamond in enumerate(diamonds):
            move = goal + diamond
            cm[i, j] = agent_g2d_move_cost_cache[move]
    return cm[linear_sum_assignment(cm)].sum()


class MinMatchingAgentToDiamond:
    meta = ()

    def __init__(self, _map, unit_cost):
        self.goals = util.get_goals(_map)
        self.unit_cost = unit_cost
        self.agent_g2d_move_cost_cache, _ = \
            CostCache.build_agent_g2d_move_cost_cache(_map, unit_cost)
        n = len(self.goals)
        self.cm = np.zeros((n + 1, n + 1), np.float)
        self.h = {}

    def __call__(self, state):
        h = self.h.get(state.diamonds, None)
        if h is not None:
            return h, ()
        h = min_matching_agent_to_diamond(self.agent_g2d_move_cost_cache, self.goals, self.cm, state.diamonds)
        self.h[state.diamonds] = h
        return h, ()


def main():
    from ..MapLoader import load_map
    from ..UnitCost import default_unit_cost

    for map_path in ['test-map1.txt', 'test-map2.txt', 'test-map3.txt', 'test-map4.txt', 'test-map5.txt']:
        _map, init_states = load_map('solver/maps/' + map_path)
        heuristic = MinMatchingAgentToDiamond(_map, default_unit_cost)
        h, _ = heuristic(init_states[0])
        print(map_path, h)


if __name__ == '__main__':
    main()
