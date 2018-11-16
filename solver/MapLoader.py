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
    for i in range(height):
        while len(map_raw[i]) < (width + 1):  # + Null-terminator
            map_raw[i] = map_raw[i] + "X"

    # Replace empty spaces with 'X'
    for i in range(height):
        map_raw[i] = map_raw[i].replace('\n', 'X')
        map_raw[i] = map_raw[i].replace(' ', 'X')

    # Initialize map
    _map = np.chararray((height, width))  # y,x

    diamonds = []
    agent = ()

    for i in range(height):
        for j in range(width):
            v = map_raw[i][j]
            if v == AGENT:
                agent = (j, i)
                v = FLOOR
            elif v == DIAMOND:
                diamonds.append((j, i))
                v = FLOOR
            elif v == DIAMOND_ON_GOAL:
                diamonds.append((j, i))
                v = GOAL
            elif v == AGENT_ON_GOAL:
                agent = (j, i)
                v = GOAL
            _map[j, i] = v

    assert agent is not ()
    assert len(diamonds) == number_diamonds

    return StateNode(_map, agent, diamonds)
