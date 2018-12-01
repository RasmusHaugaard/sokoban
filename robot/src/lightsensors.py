THRESHOLD_RATIO = 0.7


class LightSensors:
    def __init__(self):
        self.onL = False
        self.onR = False
        self.deb_onL = False
        self.deb_onR = False
        self.threshold = None

    def init(self, per):
        sL, sR = per['sL'].value(), per['sR'].value()
        mi, ma = min(sL, sR), max(sL, sR)
        self.threshold = ma * THRESHOLD_RATIO
        self.onL = self.deb_onL = sL < self.threshold
        self.onR = self.deb_onR = sL < self.threshold

    def __call__(self, per, state):
        sL, sR = per['sL'].value(), per['sR'].value()

        onL = sL < self.threshold
        onR = sR < self.threshold

        # cur_onL = sL < self.threshold
        # cur_onR = sR < self.threshold
        # if cur_onL == self.deb_onL:
        #     onL = cur_onL
        # else:
        #     onL = self.onL
        # if cur_onR == self.deb_onR:
        #     onR = cur_onR
        # else:
        #     onR = self.onR
        # self.deb_onL = cur_onL
        # self.deb_onR = cur_onR

        onBoth = onL and onR
        onAny = onL or onR

        rL = onL and not self.onL
        rR = onR and not self.onR
        rAny = rL or rR
        rBoth = rAny and onBoth

        fL = not onL and self.onL
        fR = not onR and self.onR
        fAny = fL or fR
        fBoth = fAny and not onAny

        for key, val in [
            ('sL', sL), ('sR', sR),
            ('onL', onL), ('onR', onR),
            ('onAny', onAny), ('onBoth', onBoth),
            ('rL', rL), ('rR', rR), ('rAny', rAny), ('rBoth', rBoth),
            ('fL', fL), ('fR', fR), ('fAny', fAny), ('fBoth', fBoth),
        ]: state[key] = val

        self.onL = onL
        self.onR = onR
        return state
