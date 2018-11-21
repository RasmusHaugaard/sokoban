class StateNode:
    total_cost = None

    def __init__(self, parent, agent, diamonds, current_cost, pushing=False):
        self.parent = parent
        self.agent = agent
        self.diamonds = tuple(sorted(diamonds))
        self.current_cost = current_cost
        self.pushing = pushing

    def __hash__(self):
        return hash(self.agent + self.diamonds)

    def __str__(self):
        return str(self.agent) + ": " + str(self.diamonds)

    def __lt__(self, other):
        return self.total_cost < other.total_cost

    def __gt__(self, other):
        return self.total_cost > other.total_cost

    @staticmethod
    def from_str(text):
        agent, diamonds = text.split(':')
        agent = tuple([int(x) for x in agent[1:-1].split(',')])
        diamonds = diamonds[3:-2].replace('(', '').split('),')
        diamonds = [diamond.split(',') for diamond in diamonds]
        diamonds = [(int(diamond[0]), int(diamond[1].replace(')', ''))) for diamond in diamonds]
        return StateNode(None, agent, diamonds, None)


if __name__ == '__main__':
    node = StateNode(None, (3, 3, 0), ((1, 1), (1, 0), (0, 1), (2, 1)), None)
    assert hash(node) == hash((3, 3, 0, (0, 1), (1, 0), (1, 1), (2, 1))), hash(node)
    assert hash(StateNode.from_str(str(node))) == hash(node)
    print('Test succeeded')
