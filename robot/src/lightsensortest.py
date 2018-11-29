from ev3dev.ev3 import ColorSensor
import time

sL = ColorSensor('in1')
sR = ColorSensor('in4')

charcount = 40
mi = 0
ma = 100


def progressbar(val):
    t = (val - mi) / (ma - mi)
    markedcount = round(charcount * t)
    return '#' * markedcount + ' ' * (charcount - markedcount)


def intstr(val):
    return ('   ' + str(val))[-3:]


while True:
    l, r = sL.value(), sR.value()
    print(
        "L:" + intstr(l) + "|" + progressbar(l) + "|, " +
        "R:" + intstr(r) + "|" + progressbar(r) + "|",
        end='\r'
    )
    time.sleep(0.1)
