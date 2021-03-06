from .center import CENTERING_DISTANCE

OVERSHOOT_PER_SPEED = 0.15

INACTIVE = 'INACTIVE'
START = 'START'
FORWARD = 'FORWARD'
BACK = 'BACK'

PUSH_DISTANCE = 26.6


class Push:
    keys = ['p', 'P']
    state = INACTIVE
    key = None
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
        if self.state is FORWARD:
            distance = pos - self.start_pos
            if distance > PUSH_DISTANCE - OVERSHOOT_PER_SPEED * speed:
                if self.key == 'P':
                    self.state = INACTIVE
                    self.cb()
                self.state = BACK
        if self.state is BACK:
            state['mL'] = state['mR'] = -100
            if abs(pos - self.start_pos) < CENTERING_DISTANCE + OVERSHOOT_PER_SPEED * 0.65 * speed:
                self.state = INACTIVE
                self.cb()

        return state


if __name__ == '__main__':
    from . import setup
    from .stateMachines import Path, LineFollowing, Forward

    p = Path('fp', [LineFollowing(), Forward(), Push()])
    setup.run(p)
