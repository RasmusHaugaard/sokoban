import numpy as np
from MapLoader import GOAL


class ManhattanHeuristic:
    def __init__(self, _map, unit_cost):
        self.map = _map
        self.goals = np.argwhere(_map == GOAL)

    def __call__(self, state):
        diamonds = state.diamonds
        manhattan = 0
        for diamond in diamonds:
            dist = []
            for goal in self.goals:
                dist.append(abs(diamond[0] - goal[0]) + abs(diamond[1] - goal[1]))
            manhattan += min(dist)
        return manhattan


def main():
    from MapLoader import load_map

    for map_path, expected_h in [('test-map1.txt', 5), ('test-map2.txt', 2)]:
        _map, init_state = load_map(map_path)
        manhattan_heuristic = ManhattanHeuristic(_map, init_state)
        h = manhattan_heuristic(init_state)
        assert h == expected_h, 'got {}, expected {}'.format(h, expected_h)

    print('Tests succeeded')


if __name__ == '__main__':
    main()
