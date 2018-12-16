import getch
import sys

from .draw import draw_state
from .util import load_solution


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
