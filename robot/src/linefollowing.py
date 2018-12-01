STRAIGHT = 'STRAIGHT'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

THRESHOLD = 50
BASE_SPEED = 90
TURN_SPEED = BASE_SPEED * 0.7

DEBOUNCE_DISTANCE = 1


class LineFollowing:
    def __init__(self):
        self.drive = STRAIGHT
        self.start_pos = None

    def __call__(self, per, s):

        if s['onBoth']:
            self.drive = STRAIGHT
        elif s['fBoth']:
            self.start_pos = s['pL'], s['pR']
        elif self.start_pos is not None:
            pL, pR = s['pL'], s['pR']
            spL, spR = self.start_pos
            abs_dist = (abs(pL-spL) + abs(pR-spR)) / 2
            if abs_dist > DEBOUNCE_DISTANCE:
                self.start_pos = None
        elif s['onL']:
            self.drive = LEFT
        elif s['onR']:
            self.drive = RIGHT

        if self.drive == STRAIGHT:
            s['mL'] = BASE_SPEED
            s['mR'] = BASE_SPEED
        elif self.drive == RIGHT:
            s['mL'] = BASE_SPEED
            s['mR'] = TURN_SPEED
        elif self.drive == LEFT:
            s['mL'] = TURN_SPEED
            s['mR'] = BASE_SPEED

        return s


if __name__ == '__main__':
    import setup

    lf = LineFollowing()
    setup.run(lf)
