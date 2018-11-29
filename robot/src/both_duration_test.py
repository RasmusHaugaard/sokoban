from time import time

THRESHOLD = 50


class BothDurationTest:
    def __init__(self):
        self.both = False
        self.both_start = 0

    def __call__(self, per, state):
        sL, sR = per['sL'], per['sR']

        on_line_left = sL.value() < THRESHOLD
        on_line_right = sR.value() < THRESHOLD

        both = on_line_left and on_line_right

        if both and not self.both:
            self.both = True
            self.both_start = time()

        if self.both and not both:
            print('Both time:', time() - self.both_start)
            self.both = False

        state['mL'] = state['mR'] = 85

        return state


def main():
    import setup
    from linefollowing import LineFollowing
    test = BothDurationTest()
    lf = LineFollowing()

    def fun(per, state):
        state = test(per, state)
        state = lf(per, state)
        return state

    setup.run(fun)


if __name__ == '__main__':
    main()
