from .src.setup import run


class OnLinesDistanceTest:
    start_pos = None
    stop = False

    def __call__(self, per, s):
        pos = s['p']
        if s['rR']:
            self.start_pos = pos
        if s['fR']:
            print('distance:', pos - self.start_pos)
            self.stop = True
        if not self.stop:
            s['mL'] = s['mR'] = 100
        return s


run(OnLinesDistanceTest())
