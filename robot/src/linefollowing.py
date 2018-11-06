STRAIGHT = 'STRAIGHT'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

THRESHOLD = 50
BASE_SPEED = 100
TURN_SPEED = BASE_SPEED * 0.7


class LineFollowing:
    def __init__(self):
        self.drive = STRAIGHT
        self.both = False

    def __call__(self, per, state):
        sL, sR = per['sL'], per['sR']

        on_line_left = sL.value() < THRESHOLD
        on_line_right = sR.value() < THRESHOLD

        self.both = False
        if on_line_left and on_line_right:
            self.drive = STRAIGHT
            self.both = True
        elif on_line_left:
            self.drive = LEFT
        elif on_line_right:
            self.drive = RIGHT
        else:
            pass

        if self.drive == STRAIGHT:
            state['mL'] = BASE_SPEED
            state['mR'] = BASE_SPEED
        elif self.drive == RIGHT:
            state['mL'] = BASE_SPEED
            state['mR'] = TURN_SPEED
        elif self.drive == LEFT:
            state['mL'] = TURN_SPEED
            state['mR'] = BASE_SPEED

        state['onBothLines'] = self.both
        return state


if __name__ == '__main__':
    import setup

    lf = LineFollowing()
    setup.run(lf)
