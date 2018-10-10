from linefollowing import Linefollowing
from time import time

INACTIVE = 'INACTIVE'
START = 'START'
ACTIVE = 'ACTIVE'

class Forward:
    keys = 'f'

    def __init__(self, cb):
        self.lf = Linefollowing()
        self.state = INACTIVE
        self.cb = cb

    def start(self):
        self.state = START
        self.starttime = time()

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
    forward = Forward(lambda: print('done'))
    forward.start()
    setup.run(forward)
