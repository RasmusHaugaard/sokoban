import time
from glob import glob
import os

from ..src.MapLoader import load_map
from ..src.Heuristics import get_heuristic, heuristic_keys
from ..src.AgentStateNodeExpander import AgentStateNodeExpander as NodeExpander
from ..src.Solver import solve
from ..src.UnitCost import default_unit_cost as unit_cost

map_paths = sorted(glob('solver/evalmaps/201*.txt'))
print(map_paths)

for i in range(10):
    durations = [[] for _ in range(len(heuristic_keys))]

    for map_path in map_paths:
        for j, h_key in enumerate(heuristic_keys):
            print('map: {}, h: {}'.format(map_path, h_key))
            _map, init_states = load_map(map_path)
            Heuristic = get_heuristic(h_key)

            start_time = time.process_time()
            solve(_map, init_states, NodeExpander, Heuristic, unit_cost)
            duration = time.process_time() - start_time

            durations[j].append(str(duration))

    f = open('solver/test/timeMaps/{}.txt'.format(i), 'w')
    map_names = [os.path.basename(path).split('.')[0] for path in map_paths]
    f.write(',' + ','.join(map_names) + '\n')
    for i, h_key in enumerate(heuristic_keys):
        f.write(h_key + ',')
        f.write(','.join(durations[i]) + '\n')
    f.close()
