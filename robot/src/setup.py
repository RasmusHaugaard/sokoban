from ev3dev.ev3 import LargeMotor
from ev3dev.ev3 import ColorSensor
from ev3dev.ev3 import GyroSensor

from signal import signal, SIGINT
from time import time
from gyro import Gyro
from lightsensors import LightSensors
from encoder import Encoder, TICKS_PER_CM


def run(fun):
    # Connect two motors and two (different) light sensors
    mL = LargeMotor('outC')
    mR = LargeMotor('outB')

    sL = ColorSensor('in1')
    sR = ColorSensor('in4')
    gy = GyroSensor('in3')

    # Check if the sensors are connected
    assert sL.connected, "Left ColorSensor is not connected"
    assert sR.connected, "Right ColorSensor is not conected"
    assert gy.connected, "Gyro is not connected"

    gyro = Gyro()
    light_sensors = LightSensors()
    encoder = Encoder()

    # Set the motor mode
    mL.polarity = "normal"  # "inversed"
    mR.polarity = "normal"  # "inversed"

    def stop_motors():
        mL.run_direct()
        mR.run_direct()
        mL.duty_cycle_sp = 0
        mR.duty_cycle_sp = 0

    stop_motors()

    # The example doesn't end on its own.
    # Use CTRL-C to exit it (needs command line).
    # This is a generic way to be informed
    # of this event and then take action.
    def signal_handler(sig, frame):
        stop_motors()
        print('Shut down gracefully')
        exit(0)

    # Install the signal handler for CTRL+C
    signal(SIGINT, signal_handler)
    print('Press Ctrl+C to exit')

    per = {
        'mL': mL,
        'mR': mR,
        'sL': sL,
        'sR': sR,
        'gy': gy
    }

    light_sensors.init(per)
    gyro.init(gy)

    # Endless loop reading sensors and controlling motors.
    last_log = time()
    last_now = time()
    max_dt = 0
    dts = 0
    speed_mL = None
    speed_mR = None

    while True:
        state = {}
        state = light_sensors(per, state)
        state = encoder(per, state)
        state = gyro(per, state)
        state = fun(per, state)

        max_speed = 40 * TICKS_PER_CM
        _speed_mL = state.get('mL', 0)
        if _speed_mL != speed_mL:
            speed_mL = _speed_mL
            mL.run_forever(speed_sp=speed_mL/100 * max_speed)
        _speed_mR = state.get('mR', 0)
        if _speed_mR != speed_mR:
            speed_mR = _speed_mR
            mR.run_forever(speed_sp=speed_mR/100 * max_speed)

        dts += 1
        now = time()
        dt = now - last_now
        last_now = now

        if dt > max_dt: max_dt = dt
        if now - last_log > 5.0:
            last_log = now
            print("avg fps: ", dts / 5.0)
            print('min fps: ', 1 / max_dt)
            max_dt = 0
            dts = 0


if __name__ == '__main__':
    print('Some logic here for testing')
