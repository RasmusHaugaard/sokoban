from ev3dev.ev3 import GyroSensor
import time

gy = GyroSensor('in1')

gy.mode = 'GYRO-FAS'
time.sleep(0.1)

def intstr(val):
    return (' ' * 5 + str(val))[-5:]


startvalue = gy.value()
lasttime = time.time()

angle = 0

while True:
    v = gy.value() - startvalue
    now = time.time()
    dt = now - lasttime
    lasttime = now

    angle += dt * v

    print(
        "gyro: " + str(angle) + " " * 10,
        end='\r'
    )
    time.sleep(0.01)
