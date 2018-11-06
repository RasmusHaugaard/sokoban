import time

INACTIVE = 'INACTIVE'
START = 'START'
ACTIVE = 'ACTIVE'

DEBOUNCE_TIME = 0.5


class Forward:
    keys = 'f'
    state = INACTIVE
    cb = None
    start_time = None

    def start(self, key, cb):
        self.state = START
        self.start_time = time.time()
        self.cb = cb

    def __call__(self, per, state):
        if self.state == START:
            if time.time() - self.start_time > DEBOUNCE_TIME:
                self.state = ACTIVE
        elif self.state == ACTIVE:
            if state['onBothLines']:
                self.state = INACTIVE
                self.cb()
        return state


if __name__ == '__main__':
    import setup
    from stateMachines import LineFollowing, Path

    p = Path('f', [LineFollowing(), Forward()])
    setup.run(p)
