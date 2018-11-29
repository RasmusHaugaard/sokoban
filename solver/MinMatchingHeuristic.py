import numpy as np
from MapLoader import GOAL
import CostCache
from scipy.optimize import linear_sum_assignment

ANY = CostCache.ANY
inf = float('inf')


class MinMatchingHeuristic:
    def __init__(self, _map, unit_cost):
        self.goals = [tuple(goal) for goal in np.argwhere(_map == GOAL)]
        self.unit_cost = unit_cost

        # init move cost caches
        self.diamond_move_cost_cache = \
            CostCache.build_diamond_move_cost_cache(_map, unit_cost)
        self.agent_move_cost_cache = \
            CostCache.build_agent_move_cost_cache(_map, unit_cost)

        # pre-init cost matrix
        n = len(self.goals)
        self.cm = np.empty((n, n), np.float)

        # heuristic cache will be built lazily
        self.h_cache = {}

    def hungarian(self, diamonds):
        for i, diamond in enumerate(diamonds):
            for j, goal in enumerate(self.goals):
                move = diamond + goal
                self.cm[i, j] = min(1e100, self.diamond_move_cost_cache[move])
        costs = self.cm[linear_sum_assignment(self.cm)]
        h = costs.sum()
        if h >= 1e100: return inf, []
        d = []
        for i, c in enumerate(costs):
            if c > 0: d.append(diamonds[i])
        return h, d

    def __call__(self, state):
        # cost of moving diamonds to goals
        h, d = self.h_cache.get(state.diamonds, (None, []))
        if h is None:
            h, d = self.hungarian(state.diamonds)
            self.h_cache[state.diamonds] = (h, d)

        # if deadlock or done
        if h >= inf or h == 0: return h

        # Fix: cost of pushing the last diamond is not
        # actually added in the node expander
        h -= self.unit_cost.push

        # add cost of at least turning and driving forward once
        # after every diamond to be moved but the last
        h += (self.unit_cost.turn + self.unit_cost.forward) * (len(d) - 1)

        # add cost of moving the agent to the 'closest' diamond not on a goal
        mi = inf
        for diamond in d:
            move = state.agent + diamond + (ANY,)
            c = self.agent_move_cost_cache[move]
            if c < mi: mi = c
        if mi < inf: h += mi

        return h


def main():
    from MapLoader import load_map
    from UnitCost import default_unit_cost

    for map_path in ['test-map1.txt', 'test-map2.txt']:
        _map, init_state = load_map(map_path)
        heuristic = MinMatchingHeuristic(_map, default_unit_cost)
        h = heuristic(init_state)
        print(map_path, h)


if __name__ == '__main__':
    main()
