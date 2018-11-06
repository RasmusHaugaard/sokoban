from time import time

CENTERING_DISTANCE = 100
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
        m = per['mL']

        if self.state == START:
            m.position = 0
            self.state = CENTERING
        elif self.state == CENTERING:
            if m.position > CENTERING_DISTANCE:
                self.state = WAIT
                self.wait_start = time()
        elif self.state == WAIT:
            state['mL'] = 0
            state['mR'] = 0
            if time() - self.wait_start > PAUSE:
                self.state = INACTIVE
                self.cb()

        return state
