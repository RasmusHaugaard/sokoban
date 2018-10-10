STRAIGHT = 'STRAIGHT'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

THRESHOLD = 30

BASE_SPEED = 100
TURN_SPEED = BASE_SPEED * 0.8

class Linefollowing:
    def __init__(self):
        self.drive = STRAIGHT
        self.both = False

    def __call__(self, per, state):
        mL, mR = per['mL'], per['mR']
        sL, sR = per['sL'], per['sR']

        baseSpeed = BASE_SPEED
        turnSpeed = TURN_SPEED

        onLineLeft = sL.value() < THRESHOLD
        onLineRight = sR.value() < THRESHOLD

        self.both = False
        if onLineLeft and onLineRight:
            self.drive = STRAIGHT
            self.both = True
        elif onLineLeft:
            self.drive = LEFT
        elif onLineRight:
            self.drive = RIGHT
        else:
            None

        if self.drive == STRAIGHT:
            state['mL'] = baseSpeed
            state['mR'] = baseSpeed
        elif self.drive == RIGHT:
            state['mL'] = baseSpeed
            state['mR'] = turnSpeed
        elif self.drive == LEFT:
            state['mL'] = turnSpeed
            state['mR'] = baseSpeed

        state['onBothLines'] = self.both
        return state

if __name__ is '__main__':
    import setup
    linefollowing = Linefollowing()
    setup.run(linefollowing)
