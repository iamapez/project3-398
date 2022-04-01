import mraa
import time
import sys
import cv2 as cv

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


def testBothMotors():
    for i in range(0, 177):
        print("value of i passed:", i)
        print("converted", angletoPWM(i))
        tiltMotor.write(angletoPWM(i))
        panMotor.write(angletoPWM(i))
        time.sleep(0.1)


def tiltGoToPosition(val):
    for i in range(0, val):
        print("value of i passed:", i)
        print("converted", angletoPWM(i))
        tiltMotor.write(angletoPWM(i))
        # panMotor.write(angletoPWM(i))
        time.sleep(0.1)


def panGoToPosition(val):
    for i in range(0, val):
        print("value of i passed:", i)
        print("converted", angletoPWM(i))
        # tiltMotor.write(angletoPWM(i))
        panMotor.write(angletoPWM(i))
        time.sleep(0.1)


def getValueOfPin(button):
    return button.read()


def testTakeAPic():
    cam = cv.VideoCapture(4)

    cv.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv.imshow("test", frame)

        k = cv.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()
    cv.destroyAllWindows()


def main():
    currentPWMTILT = 0
    currentPWMPAN = 0
    motorStep = 5

    panMotor.write(angletoPWM(0))
    tiltMotor.write(angletoPWM(0))

    while True:
        if getValueOfPin(displayButton):
            print('display button pressed!')
            panMotor.write(angletoPWM(45))
            time.sleep(0.2)
        elif getValueOfPin(terminateButton):
            print('terminate connection!')
            time.sleep(0.2)

        elif getValueOfPin(upButton):
            # print('move it up!')
            if currentPWMTILT > 177-motorStep:
                print('OUT OF BOUNDS! GOING UP CURRENT POSITION', currentPWMTILT)
                pass
            else:
                currentPWMTILT += motorStep

            tiltMotor.write(angletoPWM(currentPWMTILT))
            time.sleep(0.2)
        elif getValueOfPin(downButton):
            # print('move it down!')
            print('OUT OF BOUNDS! GOING DOWN CURRENT POSITION', currentPWMTILT)
            if currentPWMTILT < 0+motorStep:
                pass
            else:
                currentPWMTILT -= motorStep
            # print('current pwm value tilt:', currentPWMTILT)
            tiltMotor.write(angletoPWM(currentPWMTILT))
            time.sleep(0.2)
        elif getValueOfPin(leftButton):
            # print('move it left!')
            print('OUT OF BOUNDS! GOING LEFT CURRENT POSITION', currentPWMPAN)
            if currentPWMPAN < 0+motorStep:
                pass
            else:
                currentPWMPAN -= motorStep
            # print('current pwm value tilt:', currentPWMTILT)
            panMotor.write(angletoPWM(currentPWMPAN))
            time.sleep(0.2)
        elif getValueOfPin(rightButton):
            # print('move it right!')
            if currentPWMPAN > 177-motorStep:
                print('OUT OF BOUNDS! GOING RIGHT CURRENT POSITION', currentPWMPAN)
                pass
            else:
                currentPWMPAN += motorStep
            # print('current pwm value tilt:', currentPWMTILT)
            panMotor.write(angletoPWM(currentPWMPAN))
            time.sleep(0.2)
        else:
            # print('nothing pressed')
            time.sleep(0.2)

            # takeAPic()



if __name__ == '__main__':
    main()
