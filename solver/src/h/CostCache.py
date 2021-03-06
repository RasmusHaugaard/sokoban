"""
Caches the cost of going from any robot state to any
other robot state assuming no diamonds on the map using
custom weights for unit moves: (forward, turn, u turn)

The 'any' direction might be used to give an underestimated cost
of moving a diamond from any position to any other
"""

import numpy as np
import math
from itertools import chain

from ..MapLoader import WALL
from ...util.util import move, DIRECTIONS, OPPOSITE_DIR

UP, RIGHT, DOWN, LEFT, ANY = DIRECTIONS
inf = float('inf')


def is_available(_map, y, x):
    """checks for out of bounds or walls"""
    h, w = _map.shape[:2]
    if y < 0 or h <= y or x < 0 or w <= x:
        return False
    return _map[y, x] != WALL


def init_agent_weight_matrix(_map, unit_costs):
    """
    Initializes a weight matrix with unit agent moves (forward, turn, u turn)
    based on the map and unit costs
    """
    rot_cost = [0, unit_costs.turn, unit_costs.u_turn, unit_costs.turn]

    h, w = _map.shape

    # we want to describe the cost from going from any pos and
    # orientation (h * w * 4) = n, to any other pos/orientation
    # n by n matrix to describe the cost
    cost = np.empty((h, w, 4, h, w, 4), dtype=np.float)

    # start by filling the matrix with infinity (not feasible to go anywhere)
    cost.fill(inf)

    # fill in unit costs: forward, turn (l+r) and u turn
    for y in range(h):
        for x in range(w):
            if not is_available(_map, y, x):
                continue
            for start_dir in (UP, RIGHT, DOWN, LEFT):
                # add rotation costs in this position
                for end_dir in (UP, RIGHT, DOWN, LEFT):
                    c = rot_cost[abs(end_dir - start_dir)]
                    cost[y, x, start_dir, y, x, end_dir] = c

                # add the cost of moving forward from start dir
                # check for out of bounds or walls
                yy, xx = move(y, x, start_dir)
                if not is_available(_map, yy, xx):
                    continue

                cost[y, x, start_dir, yy, xx, start_dir] = unit_costs.forward

    return cost


def init_diamond_weight_matrix(_map, unit_costs):
    """
    Assumes a diamond has an attack side: (UP, RIGHT, DOWN or LEFT),
    in which direction it can be pushed immediately, if there's no wall there.
    The attack side can be changed, which costs the minimum robot cost to move to that side.

    Initializes a weight matrix based on the map and unit costs
    """
    uc = unit_costs
    rot_cost = [
        0,
        uc.push + uc.turn + uc.forward - uc.forward_diamond,
        uc.push + uc.turn + uc.forward - uc.forward_diamond,
        uc.push + uc.turn + uc.forward - uc.forward_diamond
    ]

    h, w = _map.shape

    # we want to describe the cost from going from any pos and
    # orientation (h * w * 4) = n, to any other pos/orientation
    # n by n matrix to describe the cost
    cost = np.empty((h, w, 4, h, w, 4), dtype=np.float)

    # start by filling the matrix with infinity (not feasible to go anywhere)
    cost.fill(inf)

    def attack_side_exists(y, x, direction):
        return is_available(_map, *move(y, x, OPPOSITE_DIR[direction]))

    # fill in unit costs
    for y in range(h):
        for x in range(w):
            if not is_available(_map, y, x):
                continue
            for start_dir in (UP, RIGHT, DOWN, LEFT):
                if not attack_side_exists(y, x, start_dir):
                    continue

                # add rotation costs in this position
                for end_dir in (UP, RIGHT, DOWN, LEFT):
                    if not attack_side_exists(y, x, end_dir):
                        continue
                    c = rot_cost[abs(end_dir - start_dir)]
                    cost[y, x, start_dir, y, x, end_dir] = c

                # add the cost of moving forward from start dir
                yy, xx = move(y, x, start_dir)
                if not is_available(_map, yy, xx):
                    continue
                cost[y, x, start_dir, yy, xx, start_dir] = uc.forward_diamond

    return cost


def floyd_warshall_inplace(cost):
    """
    Standard floyd warshall implementation
    Updates cost and _next inplace
    """
    n = int(math.sqrt(cost.size))
    cost = cost.reshape((n, n))
    # allow use of all vertices, k, as pivots when going
    # from one vertex, i, to another vertex, j
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if cost[i, j] > cost[i, k] + cost[k, j]:
                    # If it is faster to go from i to j through k, update the cost
                    cost[i, j] = cost[i, k] + cost[k, j]


def floyd_warshall_inplace_fast(cost):
    """
    Faster Floyd Warshall implementation, especially with sparse edges
    """
    n = int(math.sqrt(cost.size))
    cost = cost.reshape((n, n))
    for k in range(n):  # for each pivot node k
        K = cost[k]

        # only go through start- and end nodes
        # that might benefit from using k as pivot node
        _i = []
        _j = []
        for idx in chain(range(k), range(k + 1, n)):  # i -> i -> j == i -> j -> j == i -> j
            # if i -> k is inf, then i -> k -> j >= i -> j
            if cost[idx][k] != inf:
                _i += [(idx, cost[idx][k])]
            # if k -> j is inf, then i -> k -> j >= i -> j
            if K[idx] != inf:
                _j += [(idx, K[idx])]

        # Floyd Warshall, but with less iterations
        for i, c_ik in _i:
            I = cost[i]  # pre-index the start-node
            for j, c_kj in _j:
                if c_ik + c_kj < I[j]:
                    I[j] = c_ik + c_kj


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


def build_diamond_move_cost_cache(_map, unit_cost, fast=True):
    cost = init_diamond_weight_matrix(_map, unit_cost)
    if fast:
        floyd_warshall_inplace_fast(cost)
    else:
        floyd_warshall_inplace(cost)
    # only return any to any dir
    cost = expand_with_any_dir(cost)[:, :, 4, :, :, 4]
    # last interaction with the diamond is not a forward_diamond, but a push
    cost[cost > 0] += unit_cost.push - unit_cost.forward_diamond
    return cost


def build_agent_move_cost_cache(_map, unit_cost):
    cost = init_agent_weight_matrix(_map, unit_cost)
    floyd_warshall_inplace_fast(cost)
    return expand_with_any_dir(cost)


def build_agent_g2d_move_cost_cache(_map, unit_cost):
    orig_cost = build_agent_move_cost_cache(_map, unit_cost)

    cost = np.copy(orig_cost[:, :, 4, :, :, 4])
    min_cost = unit_cost.turn + unit_cost.forward
    zeros = cost == 0
    cost -= unit_cost.forward
    cost[cost < min_cost] = min_cost
    cost[zeros] = 0

    return cost, orig_cost


def test():
    from ..UnitCost import default_unit_cost as uc

    _map = np.array([
        [b'X', b'X', b'X'],
        [b'X', b'.', b'X'],
        [b'.', b'.', b'.'],
        [b'X', b'.', b'X'],
        [b'X', b'X', b'X']
    ])

    # agent weight matrix
    cost = init_agent_weight_matrix(_map, uc)
    assert cost[(2, 1, UP) + (2, 1, UP)] == 0
    assert cost[(2, 1, UP) + (2, 1, RIGHT)] == uc.turn
    assert cost[(2, 1, UP) + (2, 1, LEFT)] == uc.turn
    assert cost[(2, 1, UP) + (2, 1, DOWN)] == uc.u_turn
    assert cost[(2, 1, UP) + (1, 1, UP)] == uc.forward

    floyd_warshall_inplace(cost)
    assert cost[2, 0, RIGHT, 2, 2, RIGHT] == uc.forward * 2

    e = (2, 0, LEFT)
    f = (1, 1, RIGHT)
    assert cost[e + f] == uc.u_turn + uc.forward + uc.turn + uc.forward + uc.turn

    _cost = expand_with_any_dir(cost)
    assert _cost[(2, 0, ANY) + (1, 1, ANY)] == uc.forward + uc.turn + uc.forward

    # diamond weight matrix
    cost = init_diamond_weight_matrix(_map, uc)
    floyd_warshall_inplace(cost)
    _cost = expand_with_any_dir(cost)
    assert _cost[(2, 1, ANY) + (1, 1, ANY)] == uc.forward
    assert _cost[(1, 1, ANY) + (2, 1, ANY)] == inf

    print('Tests succeeded')


if __name__ == '__main__':
    test()
