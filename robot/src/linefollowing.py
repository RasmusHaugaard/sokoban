STRAIGHT = 'STRAIGHT'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

BASE_SPEED = 100
TURN_SPEED = BASE_SPEED * 0.6

DEBOUNCE_DISTANCE = 1  # cm


class LineFollowing:
    def __init__(self):
        self.drive = STRAIGHT
        self.debounce_start_pos = None
        self.start_pos_L = 0
        self.start_pos_R = 0

    def __call__(self, per, s):
        if s['rL']:
            self.start_pos_L = s['pL']
        if s['rR']:
            self.start_pos_R = s['pR']

        if s['onBoth']:
            self.drive = STRAIGHT
        elif s['fBoth'] and self.debounce_start_pos is None:
            self.drive = STRAIGHT
            self.debounce_start_pos = s['pL'], s['pR']
            self.dL = s['pL'] - self.start_pos_L
            self.dR = s['pR'] - self.start_pos_R
            if self.dL > 3 and self.dL > self.dR:
                self.debounce_direction = LEFT
            elif self.dR > 3:
                self.debounce_direction = RIGHT
            elif s['onL']:
                self.debounce_direction = RIGHT
            elif s['onR']:
                self.debounce_direction = LEFT
            else:
                self.debounce_direction = STRAIGHT
        elif self.debounce_start_pos is not None:
            pL, pR = s['pL'], s['pR']
            spL, spR = self.debounce_start_pos
            abs_dist = (abs(pL-spL) + abs(pR-spR)) / 2
            if abs_dist > DEBOUNCE_DISTANCE:
                # we just exited the debounce period
                if s['onL']:
                    self.drive = LEFT
                elif s['onR']:
                    self.drive = RIGHT
                else:
                    self.drive = self.debounce_direction
                    print('dL: {}, dR: {}, direction: {}'.format(self.dL, self.dR, self.debounce_direction))
                self.debounce_start_pos = None
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
    from . import setup

    lf = LineFollowing()
    setup.run(lf)
