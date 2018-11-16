class UnitCost:
    def __init__(self, forward, turn, u_turn):
        self.forward = forward
        self.turn = turn
        self.u_turn = u_turn


default_unit_cost = UnitCost(1, 0.9, 1.6)
