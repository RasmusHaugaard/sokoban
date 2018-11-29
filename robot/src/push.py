from time import time

INACTIVE = 'INACTIVE'
START = 'START'
FORWARD = 'FORWARD'
WAIT = 'WAIT'
BACK = 'BACK'

PUSH_DISTANCE = 480
BACK_DISTANCE = 300
POST_PUSH_WAIT = 0.1


def get_pos(per):
    return (per['mL'].position + per['mR'].position) / 2


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
        if self.state is START:
            self.start_pos = get_pos(per)
            self.state = FORWARD
        elif self.state is FORWARD:
            if get_pos(per) - self.start_pos > PUSH_DISTANCE:
                if self.key == 'P':
                    self.state = INACTIVE
                    self.cb()
                self.state = WAIT
                self.wait_start = time()
        elif self.state is WAIT:
            if time() - self.wait_start > POST_PUSH_WAIT:
                self.state = BACK
                self.start_pos = get_pos(per)
        elif self.state is BACK:
            state['mL'] = state['mR'] = -100
            if abs(get_pos(per) - self.start_pos) > BACK_DISTANCE:
                self.state = INACTIVE
                self.cb()

        return state


if __name__ == '__main__':
    import setup
    from stateMachines import Path, LineFollowing, Forward

    p = Path('fp', [LineFollowing(), Forward(), Push()])
    setup.run(p)
