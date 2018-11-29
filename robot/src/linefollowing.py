from time import time

STRAIGHT = 'STRAIGHT'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

THRESHOLD = 50
BASE_SPEED = 100
TURN_SPEED = BASE_SPEED * 0.6
BOTH_ENTER_DEBOUNCE = 0.08


class LineFollowing:
    def __init__(self):
        self.drive = STRAIGHT
        self.both = False
        self.debounce_start = 0

    def reset(self):
        self.drive = STRAIGHT
        self.both = False
        self.debounce_start = 0

    def __call__(self, per, state):
        sL, sR = per['sL'], per['sR']

        on_line_left = sL.value() < THRESHOLD
        on_line_right = sR.value() < THRESHOLD

        both = on_line_left and on_line_right
        any = on_line_left or on_line_right
        state['onBothLines'] = both
        state['onAnyLine'] = any

        now = time()
        if now - self.debounce_start > BOTH_ENTER_DEBOUNCE:
            if both:
                if not self.both:
                    self.debounce_start = now
                    self.both = True
            else:
                if on_line_left:
                    self.drive = LEFT
                elif on_line_right:
                    self.drive = RIGHT

        if self.drive == STRAIGHT:
            state['mL'] = BASE_SPEED
            state['mR'] = BASE_SPEED
        elif self.drive == RIGHT:
            state['mL'] = BASE_SPEED
            state['mR'] = TURN_SPEED
        elif self.drive == LEFT:
            state['mL'] = TURN_SPEED
            state['mR'] = BASE_SPEED

        state['resetLineFollowing'] = self.reset
        return state


if __name__ == '__main__':
    import setup

    lf = LineFollowing()
    setup.run(lf)
