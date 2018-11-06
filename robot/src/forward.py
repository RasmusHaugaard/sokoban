from linefollowing import LineFollowing
from time import time

INACTIVE = 'INACTIVE'
START = 'START'
ACTIVE = 'ACTIVE'

DEBOUNCE_TIME = 0.5


class Forward:
    keys = 'f'
    state = INACTIVE
    cb = None
    start_time = None
    lf = LineFollowing()

    def start(self, key, cb):
        self.state = START
        self.start_time = time()
        self.cb = cb

    def __call__(self, per, state):
        if self.state == START:
            state = self.lf(per, state)
            if time() - self.start_time > DEBOUNCE_TIME:
                print(time())
                self.state = ACTIVE
        elif self.state == ACTIVE:
            state = self.lf(per, state)
            if state['onBothLines']:
                self.state = INACTIVE
                self.cb()
        return state


if __name__ == '__main__':
    import setup

    forward = Forward()
    forward.start('f', lambda: print('done'))
    setup.run(forward)
