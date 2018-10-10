from time import time

class Path:
    def __init__(self, path, stateMachines, replace={'fr':'fcr', 'fl':'fcl'}, repeat=False):
        # path example: "ffrfrffrfr"
        self.path = path
        self.i = -1
        for key, val in replace.items():
            self.path = self.path.replace(key, val)

        self.stateMachines = []
        self.stateMachineKeys = {}
        for stateMachine in stateMachines:
            self.stateMachines.append(stateMachine)
            if hasattr(stateMachine, 'keys'):
                keys = stateMachine.keys
                if not isinstance(keys, list): keys = [keys]
                for key in keys:
                    self.stateMachineKeys[key] = stateMachine

        self.starttime = time()
        self.repeat = repeat
        self.nextStep()

    def nextStep(self):
        self.i += 1
        if len(self.path) is self.i:
            print("Done with the path in: " + str(time() - self.starttime) + ' seconds.')
            if self.repeat:
                self.i = -1
                self.nextStep()
        else:
            key = self.path[self.i]
            assert key in self.stateMachineKeys, "'" + str(key) + "' is used in path but not found in stateMachineKeys"
            self.stateMachineKeys[key].start(key, self.nextStep)

    def __call__(self, per, state):
        for stateMachine in self.stateMachines:
            state = stateMachine(per, state)
        return state


if __name__ is '__main__':
    print("todo: test Path class")
