"""
Caches the cost of going from any robot state to any
other robot state assuming no diamonds on the map using
custom weights for unit moves: (forward, turn, u turn)

The 'any' direction might be used to give an underestimated cost
of moving a diamond from any position to any other
"""


import numpy as np
from MapLoader import WALL
import math

UP, RIGHT, DOWN, LEFT, ANY = 0, 1, 2, 3, 4
inf = float('inf')


def init_weight_matrix(_map, unit_costs):
    """
    Initializes a weight and _next matrix with unit movements (forward, turn, u turn)
    based on the map and unit costs
    """
    rot_cost = [0, unit_costs.turn, unit_costs.u_turn, unit_costs.turn]

    h, w = _map.shape

    # we want to describe the cost from going from any pos and
    # orientation (h * w * 4) = n, to any other pos/orientation
    # n by n matrix to describe the cost
    cost = np.empty((h, w, 4, h, w, 4), dtype=np.float)
    _next = np.empty((h, w, 4, h, w, 4), dtype=np.object)

    # start by filling the matrix with infinity (not feasible to go anywhere)
    cost.fill(inf)
    _next.fill(None)

    # fill in unit costs: forward, turn (l+r) and u turn
    for y in range(h):
        for x in range(w):
            v = _map[y, x]
            if v == WALL:
                continue
            for start_dir in (UP, RIGHT, DOWN, LEFT):
                # add rotation costs in this position
                for end_dir in (UP, RIGHT, DOWN, LEFT):
                    c = rot_cost[abs(end_dir - start_dir)]
                    cost[y, x, start_dir, y, x, end_dir] = c
                    _next[y, x, start_dir, y, x, end_dir] = (y, x, end_dir)

                # add the cost of moving forward from start dir
                if start_dir == UP:
                    yy, xx = y - 1, x
                elif start_dir == RIGHT:
                    yy, xx = y, x + 1
                elif start_dir == DOWN:
                    yy, xx = y + 1, x
                else:  # LEFT
                    yy, xx = y, x - 1

                # check for out of bounds or walls
                if yy < 0 or h <= yy or xx < 0 or w <= xx:
                    continue
                if _map[yy, xx] == WALL:
                    continue

                cost[y, x, start_dir, yy, xx, start_dir] = unit_costs.forward
                _next[y, x, start_dir, yy, xx, start_dir] = (yy, xx, start_dir)

    return cost, _next


def floyd_warshall_inplace(cost, _next):
    """
    Standard floyd warshall implementation
    Updates cost and _next inplace
    """
    n = int(math.sqrt(cost.size))
    cost = cost.reshape((n, n))
    _next = _next.reshape((n, n))
    # allow use of all vertices, k, as pivots when going
    # from one vertex, i, to another vertex, j
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if cost[i, j] > cost[i, k] + cost[k, j]:
                    # If it is faster to go from i to j through k, update the cost
                    cost[i, j] = cost[i, k] + cost[k, j]
                    # and update the i -> j next node to the i -> k next node
                    _next[i, j] = _next[i, k]


def expand_with_any_dir(cost):
    """
    Expand the cost matrix with the 'any' direction
    """
    h, w, d, hh, ww, dd = cost.shape
    assert h == hh and w == ww and d == dd == 4, (h, w, d, hh, ww, dd)

    m = h * w
    cost = cost.reshape((m, 4, m, 4))
    min_from = np.min(cost, 1, keepdims=True)  # (m, 1, m, 4)
    cost = np.append(cost, min_from, axis=1)  # (m, 5, m, 4)
    min_to = np.min(cost, 3, keepdims=True)  # (m, 5, m, 1)
    cost = np.append(cost, min_to, axis=3)  # (m, 5, m, 5)

    return cost.reshape((h, w, 5, h, w, 5))


def get_path(_next, start, end):  # start/end: (x, y, orientation)
    """
    builds a list of pos/orientations from the _next matrix
    and the start and end state
    """
    path = [start]
    cur = start
    while cur != end:
        cur = _next[cur + end]
        path.append(cur)
    return path


def test():
    from UnitCost import default_unit_cost as uc

    _map = np.array([
        [b'X', b'X', b'X'],
        [b'X', b'.', b'X'],
        [b'.', b'.', b'.'],
        [b'X', b'.', b'X'],
        [b'X', b'X', b'X']
    ])

    cost, _next = init_weight_matrix(_map, uc)
    assert cost[(2, 1, UP) + (2, 1, UP)] == 0
    assert cost[(2, 1, UP) + (1, 1, UP)] == uc.forward

    floyd_warshall_inplace(cost, _next)
    c = (2, 0, RIGHT)
    d = (2, 2, RIGHT)
    assert cost[2, 0, RIGHT, 2, 2, RIGHT] == uc.forward * 2
    assert get_path(_next, c, d) == [c, (2, 1, RIGHT), d]

    e = (2, 0, LEFT)
    f = (1, 1, RIGHT)
    assert cost[e + f] == uc.u_turn + uc.forward + uc.turn + uc.forward + uc.turn
    assert get_path(_next, e, f) == [e, (2, 0, RIGHT), (2, 1, RIGHT), (2, 1, UP), (1, 1, UP), f]

    _cost = expand_with_any_dir(cost)
    assert _cost[(2, 0, ANY) + (1, 1, ANY)] == uc.forward + uc.turn + uc.forward

    print('Tests succeeded')


if __name__ == '__main__':
    test()
