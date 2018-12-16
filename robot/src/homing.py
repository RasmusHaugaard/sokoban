TARGET_SPEED_RATIO = 0.8
HOMING_DISTANCE = 60


class Homing:
    def __init__(self):
        self.homing_start_pos = 0

    def restart_homing(self, pos):
        self.homing_start_pos = pos

    def __call__(self, per, s):
        pos = s['p']
        distance = pos - self.homing_start_pos

        mi, ma, mi_key, ma_key = s['mL'], s['mR'], 'mL', 'mR'
        if mi > ma:
            mi, ma, mi_key, ma_key = ma, mi, ma_key, mi_key
        t = min(distance / HOMING_DISTANCE, 1)
        target = ma * TARGET_SPEED_RATIO
        mi = mi + (target - mi) * t
        s[mi_key] = mi

        s['restart_homing'] = self.restart_homing
        return s


if __name__ == '__main__':
    from . import setup
    from .linefollowing import LineFollowing

    lf = LineFollowing()
    homing = Homing()

    def fun(per, state):
        state = lf(per, state)
        return homing(per, state)

    setup.run(fun)
