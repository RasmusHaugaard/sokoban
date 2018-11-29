INACTIVE = 'INACTIVE'
START = 'START'
TURN_STAGE_1 = 'TURN1'
TURN_STAGE_2 = 'TURN2'

LIGHT_THRESHOLD = 30
ANGLE_THRESHOLD = 45
HIGH_SPEED = 100
LOW_SPEED = 40


class Turn:
    keys = ['l', 'r', 'u']
    state = INACTIVE
    start_angle = None
    direction = None
    cb = None

    def start(self, key, cb):
        self.direction = key
        self.cb = cb
        self.state = START

    def __call__(self, per, state):
        if self.state is INACTIVE:
            return state

        sL, sR = per['sL'], per['sR']
        angle = state['angle']

        if self.direction is 'l':
            m1n, m2n = 'mL', 'mR'
            s1, s2 = sL, sR
        else:
            m1n, m2n = 'mR', 'mL'
            s1, s2 = sR, sL

        if self.state is START:
            self.state = TURN_STAGE_1
            self.start_angle = angle
        if self.state is TURN_STAGE_1:
            state[m2n] = HIGH_SPEED
            state[m1n] = -HIGH_SPEED
            threshold = ANGLE_THRESHOLD
            if self.direction == 'u':
                threshold += 90
            if abs(angle - self.start_angle) > threshold:
                self.state = TURN_STAGE_2
        if self.state is TURN_STAGE_2:
            state[m2n] = LOW_SPEED
            state[m1n] = -LOW_SPEED
            if s1.value() < LIGHT_THRESHOLD or s2.value() < LIGHT_THRESHOLD:
                self.state = INACTIVE
                self.cb()

        return state


if __name__ == '__main__':
    import setup
    from stateMachines import Path, LineFollowing, Forward, Center
    from testPaths import TestPaths

    p = Path(TestPaths.leftRight, state_machines=[LineFollowing(), Forward(), Center(), Turn()], repeat=True)
    setup.run(p)
