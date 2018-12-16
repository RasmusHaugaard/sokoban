from ..src.setup import run


class DistanceTest:
    start_pos = None

    def __call__(self, per, s):
        pos = s['p']
        if s['rBoth']:
            if self.start_pos is None:
                self.start_pos = s['p']
            else:
                distance = pos - self.start_pos
                print("distance:", distance)
                self.start_pos = pos
        s['mL'] = 50
        s['mR'] = 50
        return s


run(DistanceTest())
