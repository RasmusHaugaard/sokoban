import time


class Gyro:
    angle = 0
    last_time = None
    start_value = None
    last_val = None

    def get_val(self, gy):
        try:
            val = gy.value()
        except OSError:
            val = self.last_val
            print('OS LIGHT SENSOR ERROR')
        self.last_val = val
        return val

    def init(self, gy):
        gy.mode = 'GYRO-FAS'
        time.sleep(0.1)
        self.start_value = self.get_val(gy)
        self.last_time = time.time()

    def __call__(self, per, state):
        gy = per['gy']

        v = self.get_val(gy) - self.start_value
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        self.angle += dt * v
        state['angle'] = self.angle

        return state
