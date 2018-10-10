from linefollowing import Linefollowing
from time import time

CENTERING_DISTANCE = 225

INACTIVE = 'INACTIVE'
START = 'START'
CENTERING = 'CENTERING'
WAIT = 'WAIT'

class Center:
    keys = 'c'

    def __init__(self):
        self.state = INACTIVE
        self.lf = Linefollowing()

    def start(self, key, cb):
        self.state = START
        self.cb = cb

    def __call__(self, per, state):
        m = per['mL']

        if self.state == START:
            m.position = 0
            self.state = CENTERING
        elif self.state == CENTERING:
            state = self.lf(per, state)
            if (m.position > CENTERING_DISTANCE):
                self.state = WAIT
                self.waitstart = time()
        elif self.state == WAIT:
            state['mL'] = 0
            state['mR'] = 0
            if time() - self.waitstart > 0.1:
                self.state = INACTIVE
                self.cb()

        return state
