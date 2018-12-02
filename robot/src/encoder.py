CM_PER_TICKS = 30 / 617
TICKS_PER_CM = 1 / CM_PER_TICKS


class Encoder:
    def __call__(self, per, s):
        pL = per['mL'].position * CM_PER_TICKS
        pR = per['mR'].position * CM_PER_TICKS
        p = (pL + pR) / 2

        sL = per['mL'].speed * CM_PER_TICKS
        sR = per['mR'].speed * CM_PER_TICKS
        speed = (sL + sR) / 2

        s['pL'], s['pR'], s['p'] = pL, pR, p
        s['speedL'], s['speedR'] = sL, sR
        s['speed'] = speed
        return s
