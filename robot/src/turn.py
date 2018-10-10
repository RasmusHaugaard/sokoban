INACTIVE = 'INACTIVE'
TURN1 = 'TURN1'
TURN2 = 'TURN2'

TURN1_DISTANCE = 200

class Turn:
    def __init__(self, cb):
        self.state = INACTIVE
        self.cb = cb
        self.turnon = False
        self.direction = 'RIGHT'

    def start(self, direction):
        self.turnon = True
        self.direction = direction

    def next(self, per, state):
        mL, mR = per['mL'], per['mR']
        sL, sR = per['sL'], per['sR']
        gy = per['gy']

        if self.direction == 'LEFT':
            m1n, m2n = 'mL', 'mR'
            m1, m2 = mL, mR
            s1, s2 = sL, sR
        else:
            m1n, m2n = 'mR', 'mL'
            m1, m2 = mR, mL
            s1, s2 = sR, sL

        if self.state == INACTIVE:
            if self.turnon:
                self.turnon = False
                self.state = TURN1
                m2.position = 0
                self.gyroStart = gy.angle
        elif self.state == TURN1:
            # ml.position from 0 to 200 -> 100 to -100
            val = 100 - min(m2.position / TURN1_DISTANCE, 1.0) * 200
            state[m2n] = 100
            state[m1n] = val
            if (abs(gy.angle - self.gyroStart) > 35):
                self.state = TURN2
        elif self.state == TURN2:
            state[m2n] = 100
            state[m1n] = -100
            if (sR.value() < 30):
                self.state = INACTIVE
                self.cb()

        return state


if (__name__ == '__main__'):
    import setup
    from linefollowing import Linefollowing

    def cb():
        print('Done')

    lf = Linefollowing()
    turn = Turn(cb)

    def program(per, state):
        state = lf(per, state)
        state = turn(per, state)
        return state

    setup.run(program)
