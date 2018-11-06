from linefollowing import LineFollowing
from time import time

INACTIVE = 'INACTIVE'
START = 'START'
FORWARD = 'FORWARD'
WAIT = 'WAIT'
BACK = 'BACK'

PUSH_DISTANCE = 480
BACK_DISTANCE = 300

class Push:
    keys = 'p'

    def __init__(self):
        self.state = INACTIVE
        self.lf = LineFollowing()

    def start(self, key, cb):
        self.state = START
        self.cb = cb

    def __call__(self, per, state):
        m = per['mL']

        if self.state is START:
            m.position = 0
            self.state = FORWARD
        elif self.state is FORWARD:
            state = self.lf(per, state)
            if m.position > PUSH_DISTANCE:
                self.state = WAIT
                self.waitstart = time()
        elif self.state is WAIT:
            if time() - self.waitstart > 0.1:
                self.state = BACK
                m.position = 0
        elif self.state is BACK:
            state['mL'] = state['mR'] = -100
            if abs(m.position) > BACK_DISTANCE:
                self.state = INACTIVE
                self.cb()

        return state


if __name__ == '__main__':
    import setup
    from path import Path
    from forward import Forward

    path = Path('fp', [Forward(), Push()])

    setup.run(path)
