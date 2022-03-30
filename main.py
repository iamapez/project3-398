import mraa
import time
import sys

# connected pwm0 (pin11) to pwm pin on top servo
# connected pwm1(pin13) to pwm pin on bottom servo
# https://avinton.com/en/academy/install-python2-7-opencv/

displayButton = mraa.Gpio(16)
terminateButton = mraa.Gpio(18)
upButton = mraa.Gpio(21)
downButton = mraa.Gpio(22)
leftButton = mraa.Gpio(38)
rightButton = mraa.Gpio(40)

tiltMotor = mraa.Pwm(11)
panMotor = mraa.Pwm(13)
tiltMotor.period_ms(20)
panMotor.period_ms(20)

tiltMotor.enable(True)
panMotor.enable(True)

displayButton.dir(mraa.DIR_IN)
terminateButton.dir(mraa.DIR_IN)
upButton.dir(mraa.DIR_IN)
downButton.dir(mraa.DIR_IN)
leftButton.dir(mraa.DIR_IN)
rightButton.dir(mraa.DIR_IN)


def angletoPWM(angle):
    temp = (0.000556 * angle) + 0.88
    if temp == 0.90088:
        temp = 0.9800

    print('value being sent to motor:')
    print(temp)

    return temp


def getValueOfPin(button):
    return button.read()


def main():
    flag = 0
    value = 0.66
    while True:
        if getValueOfPin(displayButton):
            print('print on the display!')
            time.sleep(0.5)
        elif getValueOfPin(terminateButton):
            print('terminate connection!')
            time.sleep(0.5)
        elif getValueOfPin(upButton):
            print('move it up!')
            time.sleep(0.5)
        elif getValueOfPin(downButton):
            print('move it up!')
            time.sleep(0.5)
        elif getValueOfPin(leftButton):
            print('move it left!')
            time.sleep(0.5)
        elif getValueOfPin(rightButton):
            print('move it right!')
            time.sleep(0.5)
        else:
            print('nothing pressed')
            time.sleep(0.5)

            for i in range(0, 177):
                print("value of i passed:", i)
                print("converted", angletoPWM(i))
                tiltMotor.write(angletoPWM(i))
                panMotor.write(angletoPWM(i))
                time.sleep(0.1)



            # for i in range(0, 177):
            #     print("value of i passed:", i)
            #     print("converted", angletoPWM(i))
            #     panMotor.write(angletoPWM(i))
            #     time.sleep(0.1)





if __name__ == '__main__':
    main()
