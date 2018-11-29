import numpy as np

class CheckGoal:
    def __init__(self, _map, init_state):
        self.goals =  np.transpose(_map.count(b'G').nonzero())
    
    def __call__(self, diamonds):
        for i in range(len(diamonds)):
            for j in range(2):
                if self.goals[i][j] == diamonds[i][j]:
                    pass
                else :
                    print("Goal condition not met")
                    return 1

        print("Goal condition met")
        return 0
