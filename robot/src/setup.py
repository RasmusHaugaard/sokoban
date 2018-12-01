from ev3dev.ev3 import LargeMotor
from ev3dev.ev3 import ColorSensor
from ev3dev.ev3 import GyroSensor

from signal import signal, SIGINT
from time import time
from gyro import Gyro
from lightsensors import LightSensors
from encoder import Encoder


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
    mL.run_direct()
    mR.run_direct()
    mL.polarity = "normal"  # "inversed"
    mR.polarity = "normal"  # "inversed"

    # The example doesn't end on its own.
    # Use CTRL-C to exit it (needs command line).
    # This is a generic way to be informed
    # of this event and then take action.
    def signal_handler(sig, frame):
        mL.duty_cycle_sp = 0
        mR.duty_cycle_sp = 0
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
    duty_mL = None
    duty_mR = None
    while True:
        state = {}
        state = light_sensors(per, state)
        state = encoder(per, state)
        state = gyro(per, state)
        state = fun(per, state)

        _duty_mL = state.get('mL', 0)
        if _duty_mL != duty_mL:
            duty_mL = _duty_mL
            mL.duty_cycle_sp = duty_mL
        _duty_mR = state.get('mR', 0)
        if _duty_mR != duty_mR:
            duty_mR = _duty_mR
            mR.duty_cycle_sp = duty_mR

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
