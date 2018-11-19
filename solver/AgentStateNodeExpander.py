import numpy as np
from MapLoader import WALL
from StateNode import StateNode
from CostCache import move

UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3


class AgentStateNodeExpander:

    def __init__(self, _map, unit_cost):
        self.moves_cache = self.build_moves_cache(_map, unit_cost)

    @staticmethod
    def build_moves_cache(_map, unit_cost):
        """
        cache all possible agent moves from any pos/orientation with their cost
        """
        move_cost = [
            unit_cost.forward,
            unit_cost.forward + unit_cost.turn,
            unit_cost.forward + unit_cost.u_turn,
            unit_cost.forward + unit_cost.turn
        ]

        h, w = _map.shape

        def is_walkable(y, x):
            if y < 0 or h <= y or x < 0 or w <= x:
                return False
            return _map[y, x] != WALL

        moves_cache = np.empty((h, w, 4), dtype=np.object)
        moves_cache.fill([])
        for y in range(h):
            for x in range(w):
                if not is_walkable(y, x):
                    continue
                for orientation in range(4):
                    moves = []
                    for direction in range(4):
                        cost = move_cost[abs(orientation - direction)]
                        pos = move(y, x, direction)
                        push = move(*pos, direction)
                        if is_walkable(*pos):
                            # the direction will be the orientation after the move
                            if not is_walkable(*push):
                                push = False
                            moves.append((cost, pos, direction, push))
                    moves_cache[y, x, orientation] = moves
        return moves_cache

    def __call__(self, parent):
        children = []
        d = parent.diamonds
        for move_cost, pos, direction, push in self.moves_cache[parent.agent]:
            if pos in d:
                if push and push not in d:
                    i = d.index(pos)
                    d = d[:i] + d[i + 1:] + (push,)
                else:
                    continue
            children.append(
                StateNode(
                    parent=parent,
                    agent=pos + (direction,),
                    diamonds=d,
                    current_cost=parent.current_cost + move_cost,
                )
            )
        return children


def test():
    from UnitCost import default_unit_cost

    _map = np.array([
        [b'X', b'X', b'X'],
        [b'X', b'.', b'X'],
        [b'.', b'.', b'.'],
        [b'X', b'.', b'X'],
        [b'X', b'X', b'X']
    ])

    c = AgentStateNodeExpander.build_moves_cache(_map, default_unit_cost)

    assert len(c[0, 0, UP]) == 0
    assert len(c[0, 0, LEFT]) == 0
    assert len(c[2, 0, UP]) == 1
    assert len(c[2, 1, UP]) == 4
    assert c[2, 0, RIGHT][0] == (default_unit_cost.forward, (2, 1), RIGHT, (2, 2))
    assert c[2, 1, RIGHT][1] == (default_unit_cost.forward, (2, 2), RIGHT, False)

    print('build_moves_cache tests succeeded')


if __name__ == '__main__':
    test()
