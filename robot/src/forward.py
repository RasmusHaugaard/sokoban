from linefollowing import Linefollowing
from time import time

INACTIVE = 'INACTIVE'
START = 'START'
ACTIVE = 'ACTIVE'


class Forward:
    keys = 'f'

    def __init__(self):
        self.lf = Linefollowing()
        self.state = INACTIVE

    def start(self, key, cb):
        self.state = START
        self.starttime = time()
        self.cb = cb

    def __call__(self, per, state):
        if self.state == START:
            state = self.lf(per, state)
            if (time() - self.starttime > 0.5):
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
