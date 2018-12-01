INACTIVE = 'INACTIVE'
START = 'START'
ACTIVE = 'ACTIVE'


class Forward:
    keys = 'f'
    state = INACTIVE
    cb = None

    def start(self, key, cb):
        self.state = ACTIVE
        self.cb = cb

    def __call__(self, per, state):
        if self.state == ACTIVE:
            if state['rBoth']:
                self.state = INACTIVE
                self.cb()
        return state


if __name__ == '__main__':
    import setup
    from stateMachines import LineFollowing, Path

    p = Path('f', [LineFollowing(), Forward()])
    setup.run(p)
