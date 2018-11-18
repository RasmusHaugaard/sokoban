import numpy as np


class SimpleManhattenHeuristic:
    def __init__(self, _map, init_state):
        self.map = _map

    def __call__(self, state):

        self.diamonds = state     
        self.manhatten = 0
        self.buffer = []
        self.goals =  np.transpose(self.map.count(b'G').nonzero())

        print(self.diamonds)
        print(self.goals)

        if (np.size(self.goals) >= 4):
            for i in range(np.shape(self.goals)[0]):
                for j in range(np.shape(self.goals)[1]):
                    self.buffer.append(abs(self.diamonds[i][0] - self.goals[j, 0]) + abs(self.diamonds[i][1] - self.goals[j, 1]))

                self.manhatten += min(self.buffer)
                del self.buffer[:]

        elif (np.size(self.goals) == 2):
            self.manhatten = abs(self.diamonds[0][0] - self.goals[0][0]) + abs(
                self.diamonds[0][1] - self.goals[0][1])


        return self.manhatten
