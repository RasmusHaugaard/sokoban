class UnitCost:
    def __init__(self, forward, turn, u_turn, forward_diamond, push):
        self.forward = forward
        self.turn = turn
        self.u_turn = u_turn
        self.forward_diamond = forward_diamond
        self.push = push

    def __str__(self):
        return str((self.forward, self.turn, self.u_turn, self.forward_diamond, self.push))


default_unit_cost = UnitCost(1, 0.5, 1, 1.3, 1.5)
