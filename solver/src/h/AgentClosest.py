import numpy as np

from ...util import util
from . import CostCache


def agent_closest(agent_move_cost_cache, goals, cm, diamonds):
    for i, goal in enumerate(goals):
        for j, diamond in enumerate(diamonds):
            move = goal + diamond
            cm[i, j] = agent_move_cost_cache[move]
    g2d = cm.min(axis=0)
    d2g = cm.min(axis=1)
    return max(g2d.sum() - g2d.max(), d2g.sum() - d2g.max())


class AgentClosest:
    meta = ()

    def __init__(self, _map, unit_cost):
        self.goals = util.get_goals(_map)
        self.unit_cost = unit_cost
        self.agent_g2d_move_cost_cache, _ = \
            CostCache.build_agent_g2d_move_cost_cache(_map, unit_cost)
        n = len(self.goals)
        self.cm = np.empty((n, n), np.float)
        self.h_cache = {}

    def __call__(self, state):
        h = self.h_cache.get(state.diamonds, None)
        if h is not None:
            return h, ()
        h = agent_closest(self.agent_g2d_move_cost_cache, self.goals, self.cm, state.diamonds)
        self.h_cache[state.diamonds] = h
        return h, ()


def main():
    from ..MapLoader import load_map
    from ..UnitCost import default_unit_cost

    for map_path in ['test-map1.txt', 'test-map2.txt', 'test-map3.txt', 'test-map4.txt', 'test-map5.txt']:
        _map, init_states = load_map('solver/maps/' + map_path)
        heuristic = AgentClosest(_map, default_unit_cost)
        h, _ = heuristic(init_states[0])
        print(map_path, h)


if __name__ == '__main__':
    main()
