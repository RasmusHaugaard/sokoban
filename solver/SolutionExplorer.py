from draw import draw_state
from MapLoader import load_map
from StateNode import StateNode
import getch
import sys


def load_solution(path):
    _map, _ = load_map(path)
    with open(path, 'r') as f:
        _, h, _ = [int(v) for v in f.readline().split()]
        for _ in range(h):
            f.readline()
        solution = [StateNode.from_str(line) for line in f.readlines() if ':' in line]
    return _map, solution


def main():
    if len(sys.argv) < 2:
        print('no solution file argument given')
        return
    _map, solution = load_solution(sys.argv[1])

    i = 0
    while True:
        print('\nMove:', i)
        draw_state(_map, solution[i])
        if getch.getch() == '\033':
            getch.getch()
            v = getch.getch()
            if v == 'A' or v == 'D':  # UP or LEFT
                i = max(0, i - 1)
            elif v == 'B' or v == 'C':  # DOWN or RIGHT
                i = min(i + 1, len(solution) - 1)


if __name__ == '__main__':
    main()
