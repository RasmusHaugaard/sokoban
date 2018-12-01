from time import time

OVERSHOOT_PER_SPEED = 0.18

CENTERING_DISTANCE = 8
PAUSE = 0

INACTIVE = 'INACTIVE'
START = 'START'
CENTERING = 'CENTERING'
WAIT = 'WAIT'


class Center:
    keys = 'c'
    state = INACTIVE
    cb = None
    wait_start = None

    def start(self, key, cb):
        self.state = START
        self.cb = cb

    def __call__(self, per, state):
        p = state['p']
        if self.state == START:
            self.start_pos = p
            self.state = CENTERING
        elif self.state == CENTERING:
            if p - self.start_pos > CENTERING_DISTANCE - OVERSHOOT_PER_SPEED * state['speed']:
                self.state = WAIT
                self.wait_start = time()
        elif self.state == WAIT:
            state['mL'] = state['mR'] = 0
            if time() - self.wait_start > PAUSE:
                self.state = INACTIVE
                self.cb()

        return state
