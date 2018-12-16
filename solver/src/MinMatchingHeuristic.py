import numpy as np
from scipy.optimize import linear_sum_assignment

from .MapLoader import GOAL
from . import CostCache

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
        self.cma = np.zeros((n + 1, n + 1), np.float)
        # heuristic cache will be built lazily
        self.h_cache = {}

    def calculate_diamond_state_cost(self, diamonds):
        # Add underestimate of moving diamonds to goals,
        # assuming the agent is in the best possible position before moving each diamond
        # Build a cost matrix and find the lowest goal-assignment by the hungarian method
        for i, diamond in enumerate(diamonds):
            for j, goal in enumerate(self.goals):
                move = diamond + goal
                self.cm[i, j] = min(1e100, self.diamond_move_cost_cache[move])
        costs = self.cm[linear_sum_assignment(self.cm)]
        h = costs.sum()
        dc = h
        if h >= 1e100: return inf, [], 0, 0
        if h == 0: return 0, [], 0, 0
        d = []  # diamonds to be pushed
        for i, c in enumerate(costs):
            if c > 0: d.append(diamonds[i])

        # Add underestimated cost of moving the agent between the diamonds
        for i, goal in enumerate(self.goals):
            for j, diamond in enumerate(diamonds):
                move = goal + (ANY,) + diamond + (ANY,)
                c = self.agent_move_cost_cache[move]
                if c == 0:
                    self.cma[i, j] = 0
                else:
                    self.cma[i, j] = max(
                        c - self.unit_cost.forward,
                        self.unit_cost.turn + self.unit_cost.forward
                    )
        costs = self.cma[linear_sum_assignment(self.cma)]
        ac = costs.sum()
        h += ac

        return h, d, dc, ac

    def __call__(self, state):
        # underestimated cost of moving all diamonds to goals
        # assuming the agent starts at any of the diamonds
        h, d, dc, ac = self.h_cache.get(state.diamonds, (None, [], 0, 0))
        if h is None:
            h, d, dc, ac = self.calculate_diamond_state_cost(state.diamonds)
            self.h_cache[state.diamonds] = (h, d, dc, ac)

        # return if deadlock or done
        if h == inf or h == 0: return h, (0, 0, 0)

        # Fix: cost of pushing the last diamond is not
        # actually added in the node expander
        h -= self.unit_cost.push

        # add cost of moving the agent to the 'closest' diamond not on a goal
        mi = inf
        for diamond in d:
            move = state.agent + diamond + (ANY,)
            c = self.agent_move_cost_cache[move]
            if c < mi: mi = c
        if mi < inf: h += mi

        # return the total heuristic and the components for potential debugging / visualization
        return h, (dc, ac, mi)


def main():
    from .MapLoader import load_map
    from .UnitCost import default_unit_cost

    for map_path in ['test-map1.txt', 'test-map2.txt']:
        _map, init_state = load_map(map_path)
        heuristic = MinMatchingHeuristic(_map, default_unit_cost)
        h = heuristic(init_state)
        print(map_path, h)


if __name__ == '__main__':
    main()
