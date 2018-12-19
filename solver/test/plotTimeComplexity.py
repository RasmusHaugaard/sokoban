from matplotlib import pyplot as plt
from glob import glob
import numpy as np

file_paths = glob('solver/test/timeComplexity/collection.txt')
print(file_paths)
vals = None

durs = {}

label_names = [
    'bfs',
    'can-closest',
    'closest',
    'min-match-c2g',
    'min-match',
    'min-match+',
]

for k, file_path in enumerate(file_paths):
    f = open(file_path, 'r')
    for line in f.readlines():
        line = line.replace('\n', '')
        entries = line.split(',')
        key, durations = entries[0], entries[1:]

        if key not in durs:
            durs[key] = []

        for i, val in enumerate(durations):
            durs[key].append((i+1, float(val)))


plt.figure(figsize=(4, 2))
heuristic_names = list(durs.keys())
for i, name in enumerate(heuristic_names):
    x = []
    y = []
    for p in durs[name]:
        x.append(p[0])
        y.append(p[1])
    plt.plot(x, y, label=label_names[i])

plt.legend()
plt.tight_layout(pad=0)
plt.show()
