import time
import signal

from ..src.MapLoader import parse_map
from ..src.Heuristics import get_heuristic, heuristic_keys
from ..src.AgentStateNodeExpander import AgentStateNodeExpander as NodeExpander
from ..src.Solver import solve
from ..src.UnitCost import default_unit_cost as unit_cost
from ..util.draw import draw_state

WIDTH = 6
MAX_TIME = 150

"""
WIDTH: 6, DIAMONDS: 3
XXXXXX
XM...X
X.J.GX
X.J.GX
X.J.GX
XXXXXX
"""


block_row = ['X' * WIDTH]
start = ['XM' + '.' * (WIDTH - 3) + 'X']
middle = ['X.J' + '.' * (WIDTH - 5) + 'GX']


def handler(signum, frame):
    raise Exception("timeout")


signal.signal(signal.SIGALRM, handler)

heuristic_keys = ['bfs']

durations = {}
active = {}
for key in heuristic_keys:
    active[key] = True
    durations[key] = []

for n in range(1, 100):
    if sum(active.values()) == 0:
        break
    map_str = '\n'.join(block_row + start + middle * n + block_row)
    _map, init_states = parse_map(map_str)
    draw_state(_map, init_states[0])

    for heuristic_key in heuristic_keys:
        if not active[heuristic_key]:
            continue

        print('n: {}, h: {}'.format(n, heuristic_key))
        _map, init_states = parse_map(map_str)
        Heuristic = get_heuristic(heuristic_key)

        start_time = time.process_time()
        try:
            signal.alarm(MAX_TIME)
            solve(_map, init_states, NodeExpander, Heuristic, unit_cost)
            signal.alarm(0)
        except:
            signal.alarm(0)
            active[heuristic_key] = False
            continue

        duration = time.process_time() - start_time
        durations[heuristic_key].append(duration)

f = open('solver/test/timeComplexity/0.txt', 'w')
for key in heuristic_keys:
    entries = [key] + [str(val) for val in durations[key]]
    f.write(','.join(entries) + '\n')
f.close()

"""
possible other map conf
XXXXXXXXXXX
XM........X
X..J.....GX
XG.....J..X
X.......G.X
X.........X
XXXXXXXXXXX
"""
