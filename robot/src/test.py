#!/usr/bin/python3

import ev3dev.ev3 as ev3
import signal

# Connect two motors and two (different) light sensors
mL = ev3.LargeMotor('outC')
mR = ev3.LargeMotor('outB')

lightSensorLeft = ev3.ColorSensor('in3')
lightSensorRight = ev3.ColorSensor('in2')

# Use constants to later acces motor speeds and sensor thresholds
THRESHOLD_LEFT = 30
THRESHOLD_RIGHT = 30

BASE_SPEED = 30
TURN_SPEED = 10

# Check if the motors are connected
assert lightSensorLeft.connected, "LightSensorLeft(ColorSensor) is not connected"
assert lightSensorRight.connected, "LightSensorRight(ColorSensor) is not conected"

# Set the motor mode
mL.run_direct()
mR.run_direct()

mL.polarity = "normal"
mR.polarity = "normal"

# The example doesn't end on its own.
# Use CTRL-C to exit it (needs command line).
# This is a generic way to be informed
# of this event and then take action.
def signal_handler(sig, frame):
	print('Shutting down gracefully')
	mL.duty_cycle_sp = 0
	mR.duty_cycle_sp = 0

	exit(0)

# Install the signal handler for CTRL+C
signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit')

# Endless loop reading sensors and controlling motors.
while True:
	sensorLeft = lightSensorLeft.value()
	sensorRight = lightSensorRight.value()

	if sensorRight < THRESHOLD_RIGHT:
		mR.duty_cycle_sp = TURN_SPEED
	else:
		mR.duty_cycle_sp = BASE_SPEED


	if sensorLeft < THRESHOLD_LEFT:
		mL.duty_cycle_sp = TURN_SPEED
	else:
		mL.duty_cycle_sp = BASE_SPEED
