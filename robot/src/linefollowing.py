STRAIGHT = 'STRAIGHT'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

BASE_SPEED = 100
TURN_SPEED = BASE_SPEED * 0.6
TARGET_TURN_SPEED = BASE_SPEED * 0.9

DEBOUNCE_DISTANCE = 2
HOMING_DISTANCE = 60


class LineFollowing:
    def __init__(self):
        self.drive = STRAIGHT
        self.debounce_start_pos = None
        self.homing_start_pos = 0

    def restart_homing(self, pos):
        self.homing_start_pos = pos

    def __call__(self, per, s):

        if s['onBoth']:
            if not self.drive == STRAIGHT:
                self.drive = STRAIGHT
                print('DRIVE STRAIGHT')
        elif s['fBoth'] and self.debounce_start_pos is None:
            self.drive = STRAIGHT
            self.debounce_start_pos = s['pL'], s['pR']
            print('debounce started', s['p'])
        elif self.debounce_start_pos is not None:
            pL, pR = s['pL'], s['pR']
            spL, spR = self.debounce_start_pos
            abs_dist = (abs(pL-spL) + abs(pR-spR)) / 2
            if abs_dist > DEBOUNCE_DISTANCE:
                self.debounce_start_pos = None
                print('debounce ended', s['p'])
        elif s['onL'] and not self.drive == LEFT:
            self.drive = LEFT
            print('DRIVE LEFT')
        elif s['onR'] and not self.drive == RIGHT:
            self.drive = RIGHT
            print('DRIVE RIGHT')

        if self.drive == STRAIGHT:
            s['mL'] = BASE_SPEED
            s['mR'] = BASE_SPEED
        elif self.drive == RIGHT:
            s['mL'] = BASE_SPEED
            s['mR'] = TURN_SPEED
        elif self.drive == LEFT:
            s['mL'] = TURN_SPEED
            s['mR'] = BASE_SPEED

        pos = s['p']
        distance = pos - self.homing_start_pos

        mi, ma, mi_key, ma_key = s['mL'], s['mR'], 'mL', 'mR'
        if mi > ma:
            mi, ma, mi_key, ma_key = ma, mi, ma_key, mi_key
        t = min(distance / HOMING_DISTANCE, 1)
        target = BASE_SPEED * 0.8
        mi = mi + (target - mi) * t
        s[mi_key] = mi

        s['restart_homing'] = self.restart_homing

        return s


if __name__ == '__main__':
    import setup

    lf = LineFollowing()
    setup.run(lf)
