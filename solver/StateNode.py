class StateNode:
    total_cost = None

    def __init__(self, parent, agent, diamonds, current_cost):
        self.parent = parent
        self.agent = agent
        self.diamonds = tuple(sorted(diamonds))
        self.current_cost = current_cost

    def __hash__(self):
        return hash(self.agent + self.diamonds)

    def __str__(self):
        return str(self.agent) + ": " + str(self.diamonds)

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def __gt__(self, other):
        return self.total_cost > other.total_cost


if __name__ == '__main__':
    node = StateNode(None, (3, 3, 0), ((1, 1), (1, 0), (0, 1), (2, 1)), 0)
    assert hash(node) == hash((3, 3, 0, (0, 1), (1, 0), (1, 1), (2, 1))), hash(node)
    print('Test succeeded')
