from time import time
import re


def build_state_machine_key_map(state_machines):
    key_map = {}
    for state_machine in state_machines:
        if hasattr(state_machine, 'keys'):
            keys = state_machine.keys
            if not isinstance(keys, list):
                keys = [keys]
            for key in keys:
                key_map[key] = state_machine
    return key_map


def str_repetition(str):
    # (ex: 'fr3l' -> 'frfrfrl')
    path_elements = re.split('([0-9]+)', str)
    str = ''
    for i in range(len(path_elements) // 2 + 1):
        el = path_elements[i * 2]
        if len(path_elements) > i * 2 + 1:
            str += el * int(path_elements[i * 2 + 1])
        else:
            str += el
    return str


class Path:
    path = ''
    running = False
    previous_step_time = None
    machine_durations = {}

    def __init__(self, path, state_machines,
                 replace={'ll': 'u', 'rr': 'u', 'fr': 'fcr', 'fl': 'fcl'},
                 repeat=False):
        # path example: "ffrfr2"
        self.path = path
        self.state_machines = state_machines
        self.i = -1

        # pattern replacement (ex: 'fr' -> 'fcr')
        for key, val in replace.items():
            self.path = self.path.replace(key, val)

        self.state_machine_key_map = build_state_machine_key_map(state_machines)

        self.path = str_repetition(self.path)

        self.start_time = time()
        self.repeat = repeat
        self.next_step()

    def next_step(self):
        if self.previous_step_time:
            machine = self.state_machine_key_map[self.path[self.i]]
            now = time()
            duration = now - self.previous_step_time
            self.previous_step_time = now
            durations = self.machine_durations.get(tuple(machine.keys), [])
            durations.append(duration)
            self.machine_durations[tuple(machine.keys)] = durations
        else:
            self.previous_step_time = time()
        self.i += 1
        if len(self.path) is self.i:
            print("Done with the path in: " + str(time() - self.start_time) + ' seconds.')
            self.running = False
            for key, durations in self.machine_durations.items():
                print(key, 'average:', sum(durations) / len(durations))
            if self.repeat:
                self.i = -1
                self.next_step()
        else:
            key = self.path[self.i]
            assert (
                key in self.state_machine_key_map,
                "'" + str(key) + "' is used in path but not found in stateMachineKeys"
            )
            self.state_machine_key_map[key].start(key, self.next_step)
            self.running = True

    def __call__(self, per, state):
        for stateMachine in self.state_machines:
            state = stateMachine(per, state)
        if not self.running:
            state['mL'] = state['mR'] = 0
        return state


if __name__ == '__main__':
    class FakeMachine:
        keys = 'F'
        state = False
        cb = None

        def start(self, key, cb):
            self.state = True
            self.cb = cb

        def __call__(self, per, state):
            if self.state is True:
                self.state = False
                self.cb()


    f = FakeMachine()
    p = Path('F2k2k', [f], replace={'k': 'F'})
    assert p.path == 'FFFFF'
    for i in range(6):
        if i < 5:
            assert f.state is True, i
        else:
            assert f.state is False, i
        p({}, {})
    print('Test succeeded')
