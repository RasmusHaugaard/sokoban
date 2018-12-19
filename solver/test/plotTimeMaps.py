from glob import glob
import numpy as np

file_paths = glob('solver/test/timeMaps/*.txt')

des_map_names = ['2015-competition-map', '2017-competition-map', '2018-competition-map']
des_heu_names = ['d_closest', 'closest', 'min_match_d2g', 'min_match', 'min_match+']
durs = [[[] for _ in range(len(des_map_names))] for _ in range(len(des_heu_names))]

for k, file_path in enumerate(file_paths):
    f = open(file_path, 'r')
    map_names = f.readline().replace('\n', '')
    map_names = map_names.split(',')[1:]
    for line in f.readlines():
        line = line.replace('\n', '')
        entries = line.split(',')
        heu_name, durations = entries[0], entries[1:]
        assert len(durations) == 3
        if heu_name not in des_heu_names:
            continue
        h_i = des_heu_names.index(heu_name)
        for i, val in enumerate(durations):
            map_name = map_names[i]
            if map_name not in des_map_names:
                continue
            m_i = des_map_names.index(map_name)
            durs[h_i][m_i].append(float(val))


for h_i in range(len(des_heu_names)):
    h_name = des_heu_names[h_i]
    for m_i in range(len(des_map_names)):
        m_name = des_map_names[m_i]
        vals = durs[h_i][m_i]
        print('{}, {}, mean: {:.1f}, std: {:.1f}'.format(h_name, m_name, np.mean(vals), np.std(vals)))
