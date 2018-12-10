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

        onBoth = onL and onR
        onAny = onL or onR

        rL = onL and not self.onL
        rR = onR and not self.onR
        rAny = rL or rR
        rBoth = rAny and onBoth

        fL = not onL and self.onL
        fR = not onR and self.onR
        fAny = fL or fR
        fBoth = self.onL and self.onR and not onBoth

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
