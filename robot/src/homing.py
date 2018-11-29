from time import time

HOMING_FINAL_TIME = 2


def interp(a, b, t):
    return a + t * (b - a)


class Homing:
    def __init__(self):
        self.enabled = False
        self.homing_start = 0

    def __call__(self, per, state):
        if state.get('enable_homing', False) and not self.enabled:
            self.homing_start = time()
            self.enabled = True
            print('ENABLED HOMING')
        if state.get('disable_homing', False) and self.enabled:
            self.enabled = False
            print('DISABLED HOMING')

        if self.enabled:
            for m in ('mL', 'mR'):
                p = state[m]
                if p < 100:
                    homing_duration = time() - self.homing_start
                    t = min(homing_duration / HOMING_FINAL_TIME, 1)
                    state[m] = interp(p, 90, t)

        return state
