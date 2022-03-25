import mraa
import time
import sys


testGpio = mraa.Gpio(40)
testGpio.dir(mraa.DIR_OUT)

while True:
    testGpio.write(1)
    print('flipped high')
    time.sleep(2)

    testGpio.write(0)
    print('flipped low')
    time.sleep(3)


