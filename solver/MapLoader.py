from StateNode import StateNode
import numpy as np

AGENT = b'M'
DIAMOND = b'J'
GOAL = b'G'
DIAMOND_ON_GOAL = b'#'
AGENT_ON_GOAL = b'W'
FLOOR = b'.'
WALL = b'X'


def load_map(path):
    """
    reads the map with the initial state from a file and
    separates the initial state and the map
    """
    with open(path, 'r') as f:
        w, h, number_diamonds = [int(v) for v in f.readline().split()]
        map_raw = [f.readline() for _ in range(h)]

    # Extend map to rectangular shape
    for y in range(h):
        map_raw[y] = (map_raw[y] + 'X' * w)[:w]

    # Initialize map
    _map = np.chararray((h, w))
    for y in range(h):
        for x in range(w):
            _map[y, x] = map_raw[y][x]

    diamonds = []
    agent = ()

    for y in range(h):
        for x in range(w):
            v = _map[y, x]
            new_v = WALL
            if v == GOAL or v == FLOOR:
                new_v = v
            elif v == AGENT:
                agent = (y, x)
                new_v = FLOOR
            elif v == DIAMOND:
                diamonds.append((y, x))
                new_v = FLOOR
            elif v == DIAMOND_ON_GOAL:
                diamonds.append((y, x))
                new_v = GOAL
            elif v == AGENT_ON_GOAL:
                agent = (y, x)
                new_v = GOAL
            _map[y, x] = new_v

    assert agent is not ()
    assert len(diamonds) == number_diamonds, diamonds

    initial_states = []
    for orientation in range(4):
        initial_states.append(StateNode(None, agent + (orientation,), diamonds, 0))

    return _map, initial_states


def main():
    print(*load_map('test-map1.txt'))
    print('')
    print(*load_map('test-map2.txt'))


if __name__ == '__main__':
    main()
