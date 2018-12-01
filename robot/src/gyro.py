import time


class Gyro:
    angle = 0
    last_time = None
    start_value = None

    def init(self, gy):
        gy.mode = 'GYRO-FAS'
        time.sleep(0.1)
        self.start_value = gy.value()
        self.last_time = time.time()

    def __call__(self, per, state):
        gy = per['gy']

        v = gy.value() - self.start_value
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        self.angle += dt * v
        state['angle'] = self.angle

        return state
