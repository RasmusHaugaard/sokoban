
class StateNode:
    def __init__(self, agent, diamonds, cost):
        self.agent = agent
        self.diamonds = sorted(diamonds)
        self.current_cost = cost

    def __hash__(self):
        return hash(self.agent + self.diamonds)
