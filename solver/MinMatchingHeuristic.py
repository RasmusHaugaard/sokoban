import numpy as np
from MapLoader import GOAL
import CostCache

ANY = CostCache.ANY


class MinMatchingHeuristic:
    def __init__(self, _map, unit_cost):
        self.map = _map
        self.goals = [tuple(goal) for goal in np.argwhere(_map == GOAL)]
        cost, _next = CostCache.init_diamond_weight_matrix(_map, unit_cost)
        CostCache.floyd_warshall_inplace(cost, _next)
        self.diamond_move_cost = CostCache.expand_with_any_dir(cost)

    def __call__(self, state):
        h = 0
        diamonds = state.diamonds
        for diamond in diamonds:
            dist = []
            for goal in self.goals:
                # the move is from the diamond position with any
                # attack side to the goal with any attack side
                move = diamond + (ANY,) + goal + (ANY,)
                dist.append(self.diamond_move_cost[move])
            h += min(dist)
        return h


def main():
    from MapLoader import load_map
    from UnitCost import default_unit_cost

    for map_path in ['test-map1.txt', 'test-map2.txt']:
        _map, init_state = load_map(map_path)
        min_matching_heuristic = MinMatchingHeuristic(_map, default_unit_cost)
        h = min_matching_heuristic(init_state)
        print(map_path, h)


if __name__ == '__main__':
    main()
