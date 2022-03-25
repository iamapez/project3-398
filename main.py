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
            continue

        elif getValueOfPin(terminateButton):
            print('terminate connection!')
            break

        elif getValueOfPin(upButton):
            print('move it up!')
            break

        elif getValueOfPin(downButton):
            print('move it up!')
            break

        elif getValueOfPin(leftButton):
            print('move it left!')
            break

        elif getValueOfPin(rightButton):
            print('move it right!')
            break

        else:
            print('nothing pressed')





if __name__ == '__main__':
    main()
