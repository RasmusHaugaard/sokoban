class UnitCost:
    def __init__(self, forward, turn, u_turn, forward_diamond, push):
        self.forward = forward
        self.turn = turn
        self.u_turn = u_turn
        self.forward_diamond = forward_diamond
        self.push = push

    def __str__(self):
        return str((self.forward, self.turn, self.u_turn, self.forward_diamond, self.push))


# default_unit_cost found by testing unit moves separately
default_unit_cost = UnitCost(
    forward=0.94,
    turn=0.37,
    u_turn=0.41 * 2,
    forward_diamond=0.98,
    push=1.05
)


# bfs_unit_cost simulate the traditional, manhattan move cost
bfs_unit_cost = UnitCost(
    forward=1,
    turn=0,
    u_turn=0,
    forward_diamond=1,
    push=0
)
