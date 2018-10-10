from ev3dev.ev3 import LargeMotor
from ev3dev.ev3 import ColorSensor
from ev3dev.ev3 import GyroSensor

from signal import signal, SIGINT
from time import time

def run(fun):
    # Connect two motors and two (different) light sensors
    mL = LargeMotor('outC')
    mR = LargeMotor('outB')

    sL = ColorSensor('in3')
    sR = ColorSensor('in2')
    gy = GyroSensor('in1')

    # Check if the sensors are connected
    assert sL.connected, "Left ColorSensor is not connected"
    assert sR.connected, "Right ColorSensor is not conected"
    assert gy.connected, "Gyro is not connected"

    # Set gyro mode
    gy.mode = 'GYRO-ANG'

    # Set the motor mode
    mL.run_direct()
    mR.run_direct()
    mL.polarity = "inversed"
    mR.polarity = "inversed"

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

    # Endless loop reading sensors and controlling motors.
    lastTime = time()
    lastLog = time()
    dts = 0

    while True:
        now = time()
        deltaTime = now - lastTime;
        lastTime = now;

        state = fun({
            'now': now,
            'deltaTime': deltaTime,
            'mL': mL,
            'mR': mR,
            'sL': sL,
            'sR': sR,
            'gy': gy
        }, {})

        mL.duty_cycle_sp = state.get('mL', 0)
        mR.duty_cycle_sp = state.get('mR', 0)

        dts += 1
        if now - lastLog > 5.0:
            lastLog = now
            print("fps: ", dts / 5.0)
            dts = 0

if __name__ is '__main__':
    print('Some logic here for testing')
