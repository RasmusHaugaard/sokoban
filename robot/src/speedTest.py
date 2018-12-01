from setup import run


class SpeedTest:
    stop = False

    def __call__(self, per, s):
        speed = per['mL'].speed
        if s['fBoth']:
            print(speed)
            self.stop = True
        elif not self.stop:
            s['mL'] = s['mR'] = 25
        return s


run(SpeedTest())
