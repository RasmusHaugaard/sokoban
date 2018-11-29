from time import time

CENTERING_DISTANCE = 55
PAUSE = 0

INACTIVE = 'INACTIVE'
START = 'START'
CENTERING = 'CENTERING'
WAIT = 'WAIT'


def get_pos(per):
    return (per['mL'].position + per['mR'].position) / 2


class Center:
    keys = 'c'
    state = INACTIVE
    cb = None
    wait_start = None

    def start(self, key, cb):
        self.state = START
        self.cb = cb

    def __call__(self, per, state):
        if self.state == START:
            self.start_pos = get_pos(per)
            self.state = CENTERING
        elif self.state == CENTERING:
            if get_pos(per) - self.start_pos > CENTERING_DISTANCE:
                self.state = WAIT
                self.wait_start = time()
        elif self.state == WAIT:
            state['mL'] = 0
            state['mR'] = 0
            if time() - self.wait_start > PAUSE:
                self.state = INACTIVE
                self.cb()

        return state
