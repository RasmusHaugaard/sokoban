from time import time
from center import CENTERING_DISTANCE

OVERSHOOT_PER_SPEED = 0.11

INACTIVE = 'INACTIVE'
START = 'START'
FORWARD = 'FORWARD'
WAIT = 'WAIT'
BACK = 'BACK'

PUSH_DISTANCE = 26.6
#BACK_DISTANCE = 18.2
POST_PUSH_WAIT = 0.0


class Push:
    keys = ['p', 'P']
    state = INACTIVE
    wait_start = None
    cb = None

    def start(self, key, cb):
        self.state = START
        self.key = key
        self.cb = cb

    def __call__(self, per, state):
        pos = state['p']
        speed = abs(state['speed'])

        if self.state is START:
            self.start_pos = pos
            self.state = FORWARD
        elif self.state is FORWARD:
            distance = pos - self.start_pos
            if distance > PUSH_DISTANCE - OVERSHOOT_PER_SPEED * speed:
                if self.key == 'P':
                    self.state = INACTIVE
                    self.cb()
                self.state = WAIT
                self.wait_start = time()
        elif self.state is WAIT:
            state['mL'] = state['mR'] = 0
            if time() - self.wait_start > POST_PUSH_WAIT:
                self.state = BACK
        elif self.state is BACK:
            state['mL'] = state['mR'] = -100
            if abs(pos - self.start_pos) < CENTERING_DISTANCE + OVERSHOOT_PER_SPEED * speed:
                self.state = INACTIVE
                self.cb()

        return state


if __name__ == '__main__':
    import setup
    from stateMachines import Path, LineFollowing, Forward

    p = Path('fp', [LineFollowing(), Forward(), Push()])
    setup.run(p)
