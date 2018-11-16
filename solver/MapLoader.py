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
    with open(path, 'r') as file:
        map_info = file.readline()
        map_raw = file.readlines()

    width = int(map_info[0] + map_info[1])
    height = int(map_info[3] + map_info[4])
    number_diamonds = int(map_info[6] + map_info[7])

    print("Width: " + str(width))
    print("Height: " + str(height))
    print("Number of diamonds: " + str(number_diamonds))
    print("-------------------------------------------------")

    # Extend map to rectangular shape
    for y in range(height):
        while len(map_raw[y]) < (width + 1):  # + Null-terminator
            map_raw[y] = map_raw[y] + "X"

    # Replace empty spaces with 'X'
    for y in range(height):
        map_raw[y] = map_raw[y].replace('\n', 'X')
        map_raw[y] = map_raw[y].replace(' ', 'X')

    # Initialize map
    _map = np.chararray((height, width))  # y,x

    diamonds = ()
    agent = ()

    for y in range(height):
        for x in range(width):
            v = map_raw[y][x]
            if v == AGENT:
                agent = (y, x)
                v = FLOOR
            elif v == DIAMOND:
                diamonds += (y, x)
                v = FLOOR
            elif v == DIAMOND_ON_GOAL:
                diamonds += (y, x)
                v = GOAL
            elif v == AGENT_ON_GOAL:
                agent = (y, x)
                v = GOAL
            _map[x, y] = v

    assert agent is not ()
    assert len(diamonds) == number_diamonds

    return _map, StateNode((*agent, 0), diamonds, 0)
