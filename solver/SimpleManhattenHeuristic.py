import numpy as np


class SimpleManhattenHeuristic:
    def __init__(self, map, init_state):
        pass

    def __call__(self, state):
        self.manhatten = 0
        self.buffer = []

        self.diamond_mask = self.map.count(b'J')
        self.diamonds = np.transpose(np.nonzero(self.diamond_mask))

        self.goal_mask = self.map.count(b'G')
        self.goal_mask += self.map.count(b'W')
        self.goals = np.transpose(np.nonzero(self.goal_mask))

        if (np.size(self.diamonds) >= 4):
            for i in range(np.shape(self.diamonds)[0]):
                for j in range(np.shape(self.diamonds)[1]):
                    self.buffer.append(
                        abs(self.diamonds[i, 0] - self.goals[j, 0]) + abs(self.diamonds[i, 1] - self.goals[j, 1]))

                self.manhatten += min(self.buffer)
                del self.buffer[:]

        elif (np.size(self.diamonds) == 2):
            self.manhatten = abs(self.diamonds[0][0] - self.goals[0][0]) + abs(
                self.diamonds[0][1] - self.goals[0][1])
