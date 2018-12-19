import numpy as np

from ...util import util
from . import CostCache
from .DiamondClosest import diamond_closest
from .AgentClosest import agent_closest


class Closest:
    meta = ('diamond_closest', 'agent_closest')

    def __init__(self, _map, unit_cost):
        self.goals = util.get_goals(_map)
        self.unit_cost = unit_cost
        self.diamond_move_cost_cache = \
            CostCache.build_diamond_move_cost_cache(_map, unit_cost)
        self.agent_move_cost_cache, _ = \
            CostCache.build_agent_g2d_move_cost_cache(_map, unit_cost)
        n = len(self.goals)
        self.cm = np.empty((n, n), np.float)
        self.h_cache = {}

    def __call__(self, state):
        h, meta = self.h_cache.get(state.diamonds, (None, ()))
        if h is not None:
            return h, meta
        d = diamond_closest(self.diamond_move_cost_cache, self.goals, self.unit_cost, self.cm, state.diamonds)
        a = agent_closest(self.agent_move_cost_cache, self.goals, self.cm, state.diamonds)
        h = d + a
        meta = (d, a)
        self.h_cache[state.diamonds] = h, meta
        return h, meta


def main():
    from ..MapLoader import load_map
    from ..UnitCost import default_unit_cost

    for map_path in ['test-map1.txt', 'test-map2.txt', 'test-map3.txt']:
        _map, init_states = load_map('solver/maps/' + map_path)
        heuristic = Closest(_map, default_unit_cost)
        h, _ = heuristic(init_states[0])
        print(map_path, h)


if __name__ == '__main__':
    main()
