INACTIVE = 'INACTIVE'
START = 'START'
ACTIVE = 'ACTIVE'

DEBOUNCE_DISTANCE = 10


class Forward:
    keys = 'f'
    state = INACTIVE
    cb = None

    def start(self, key, cb):
        self.state = START
        self.cb = cb

    def __call__(self, per, s):
        if self.state == START:
            self.start_pos = s['p']
            self.state = ACTIVE
        if self.state == ACTIVE:
            if s['rBoth']:
                if s['p'] - self.start_pos > DEBOUNCE_DISTANCE:
                    self.state = INACTIVE
                    self.cb()
                else:
                    print('NOT READY TO COMPLETE FORWARD YET!')
        return s


if __name__ == '__main__':
    from . import setup
    from .stateMachines import LineFollowing, Path

    p = Path('f', [LineFollowing(), Forward()])
    setup.run(p)
