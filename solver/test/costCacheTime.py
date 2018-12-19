import time
from glob import glob

from ..src.h.CostCache import build_diamond_move_cost_cache
from ..src.MapLoader import load_map
from ..src.UnitCost import default_unit_cost


map_paths = glob('solver/maps/*-competition-map.txt')


for map_path in map_paths:
    _map, _ = load_map(map_path)
    print(map_path.split('/')[-1])
    for fast in (True, False):
        start_time = time.process_time()
        build_diamond_move_cost_cache(_map, default_unit_cost, fast)
        duration = time.process_time() - start_time
        print('fast: {}, cache built in {} s'.format(fast, duration))
