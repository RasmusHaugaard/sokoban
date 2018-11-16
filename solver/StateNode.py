class StateNode:
    def __init__(self, agent, diamonds, cost):
        self.agent = agent
        self.diamonds = sorted(diamonds)
        self.current_cost = cost

    def __hash__(self):
        return hash(self.agent + (*self.diamonds,))


if __name__ == '__main__':
    node = StateNode((3, 3, 0), ((1, 1), (1, 0), (0, 1), (2, 1)), 0)
    assert node.__hash__() == hash((3, 3, 0, (0, 1), (1, 0), (1, 1), (2, 1))), node.__hash__()
    print('Test succeeded')
