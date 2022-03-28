import mraa
import time
import sys

displayButton = mraa.Gpio(16)
terminateButton = mraa.Gpio(18)

upButton = mraa.Gpio(21)
downButton = mraa.Gpio(22)
leftButton = mraa.Gpio(38)
rightButton = mraa.Gpio(40)

displayButton.dir(mraa.DIR_IN)
terminateButton.dir(mraa.DIR_IN)
upButton.dir(mraa.DIR_IN)
downButton.dir(mraa.DIR_IN)
leftButton.dir(mraa.DIR_IN)
rightButton.dir(mraa.DIR_IN)


def getValueOfPin(button):
    return button.read()


def main():

    flag = 0

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




if __name__ == '__main__':
    main()
