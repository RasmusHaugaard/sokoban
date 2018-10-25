INACTIVE = 'INACTIVE'
START = 'START'
TURN1 = 'TURN1'
TURN2 = 'TURN2'

class Turn:
    keys = ['l', 'r']

    def __init__(self):
        self.state = INACTIVE
        self.direction = 'r'

    def start(self, key, cb):
        self.direction = key
        self.cb = cb
        self.state = START

    def __call__(self, per, state):
        mL, mR = per['mL'], per['mR']
        sL, sR = per['sL'], per['sR']
        gy = per['gy']

        if self.direction is 'l':
            gyroTresh = 25
            m1n, m2n = 'mL', 'mR'
            m1, m2 = mL, mR
            s1, s2 = sL, sR
        elif self.direction is 'r':
            gyroTresh = 50
            m1n, m2n = 'mR', 'mL'
            m1, m2 = mR, mL
            s1, s2 = sR, sL
        else:
            assert False, "unexpected turn direction: " + str(self.direction)

        if self.state is START:
            self.state = TURN1
            self.gyroStart = gy.angle
        elif self.state is TURN1:
            state[m2n] = 100
            state[m1n] = -100
            print(abs(gy.angle - self.gyroStart))
            if abs(gy.angle - self.gyroStart) > gyroTresh:
                self.state = TURN2
        elif self.state is TURN2:
            state[m2n] = 30
            state[m1n] = -30
            if (s1.value() < 30) or (s2.value() < 30):
                self.state = INACTIVE
                self.cb()

        return state


if __name__ is '__main__':
    import setup
    from forward import Forward
    from center import Center
    from path import Path

    path = Path('frfr', stateMachines=[Forward(), Center(), Turn()])

    setup.run(path)
