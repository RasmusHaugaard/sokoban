INACTIVE = 'INACTIVE'
START = 'START'
TURN_STAGE = 'TURN'
TURN_END_STAGE = 'TURN_END'

ANGLE_THRESHOLD = 40
HIGH_SPEED = 100
LOW_SPEED = 40


class Turn:
    keys = ['l', 'r']
    state = INACTIVE
    start_angle = None
    direction = None
    threshold = 0
    cb = None

    def start(self, key, cb):
        self.direction = key
        self.cb = cb
        self.state = START

    def __call__(self, per, state):
        if self.state is INACTIVE:
            return state

        angle = state['angle']

        if self.direction is 'l':
            m1n, m2n = 'mL', 'mR'
        else:
            m1n, m2n = 'mR', 'mL'

        state[m2n] = HIGH_SPEED
        state[m1n] = -HIGH_SPEED
        if self.state is START:
            self.state = TURN_STAGE
            self.start_angle = angle
        if self.state is TURN_STAGE:
            if abs(angle - self.start_angle) > ANGLE_THRESHOLD:
                self.state = TURN_END_STAGE
        if self.state is TURN_END_STAGE:
            state[m2n] = LOW_SPEED
            state[m1n] = -LOW_SPEED
            if self.direction is 'l' and state['onL']:
                self.state = INACTIVE
                self.cb()
            if self.direction is 'r' and state['onR']:
                self.state = INACTIVE
                self.cb()

        return state


if __name__ == '__main__':
    import setup
    from stateMachines import Path, LineFollowing, Forward, Center
    from testPaths import TestPaths

    p = Path(TestPaths.leftRight, state_machines=[LineFollowing(), Forward(), Center(), Turn()], repeat=True)
    setup.run(p)
