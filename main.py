import mraa
import time
import sys
import cv2 as cv
import zmq

# connected pwm0 (pin11) to pwm pin on top servo
# connected pwm1(pin13) to pwm pin on bottom servo
# https://avinton.com/en/academy/install-python2-7-opencv/


# declare all the buttons as gpio
displayButton = mraa.Gpio(16)
terminateButton = mraa.Gpio(18)
upButton = mraa.Gpio(21)
downButton = mraa.Gpio(22)
leftButton = mraa.Gpio(38)
rightButton = mraa.Gpio(40)

# declare the motor pwm pins and set the period
tiltMotor = mraa.Pwm(11)
panMotor = mraa.Pwm(13)
tiltMotor.period_ms(20)
panMotor.period_ms(20)
tiltMotor.enable(True)
panMotor.enable(True)

# set the direction of the buttons
displayButton.dir(mraa.DIR_IN)
terminateButton.dir(mraa.DIR_IN)
upButton.dir(mraa.DIR_IN)
downButton.dir(mraa.DIR_IN)
leftButton.dir(mraa.DIR_IN)
rightButton.dir(mraa.DIR_IN)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:6969')





def angletoPWM(angle):
    # method to convert angle angle to pwm that is readable by the motors
    temp = (0.000556 * angle) + 0.88
    if temp == 0.90088:
        temp = 0.9800
    print('value being sent to motor:')
    print(temp)

    return temp


def testBothMotors():
    # test: have both motors move from min to max value
    for i in range(0, 177):
        print("value of i passed:", i)
        print("converted", angletoPWM(i))
        tiltMotor.write(angletoPWM(i))
        panMotor.write(angletoPWM(i))
        time.sleep(0.1)


def tiltGoToPosition(val):
    # used for bringing the tilt motor from 0 to a position val
    for i in range(0, val):
        print("value of i passed:", i)
        print("converted", angletoPWM(i))
        tiltMotor.write(angletoPWM(i))
        # panMotor.write(angletoPWM(i))
        time.sleep(0.1)


def panGoToPosition(val):
    # used for bringing the pan motor from 0 to a position val
    for i in range(0, val):
        print("value of i passed:", i)
        print("converted", angletoPWM(i))
        # tiltMotor.write(angletoPWM(i))
        panMotor.write(angletoPWM(i))
        time.sleep(0.1)


def getValueOfPin(button):
    # read the current value of a pin
    return button.read()


def testTakeAPic():
    # example code used for a signature. Take a screenshot and save it to a file when space is pressed.
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


def takePicandDisplay():
    cam = cv.VideoCapture(4)
    # cv.namedWindow("CSE398")

    img_counter = 0
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")

    # cv.imshow("test", frame)
    img_name = "opencv_frame_{}.png".format(img_counter)
    cv.imwrite(img_name, frame)
    print("{} written!".format(img_name))

    img_counter += 1

    cv.imshow('testing here', frame)

    cv.waitKey(0)
    cv.destroyAllWindows()


def main():
    # main entry point for the program here

    # global variables to track current position of tilt and pan motors
    currentPWMTILT = 0
    currentPWMPAN = 0

    # change the motor step here (makes slower or faster depending on accuracy)
    motorStep = 5

    # before doing anything, initalize both motors to positions 0
    panMotor.write(angletoPWM(0))
    tiltMotor.write(angletoPWM(0))

    while True:

        # check if there is a received packet
        # if there is a packet received, print it and do something else
        message = socket.recv_string()
        if message():
            # print('Received request', message)
            if message.lower() == 'getimage':
                #     getImage - the Rock Pi takes an image
                #     and sends it to the host computer over the IoT network.
                #     The host computer displays the image on its own output screen.
                pass
            elif message.lower == 'getshapes':
                #   getShapes - the Rock Pi takes an image and detects shapes in the image.
                #   The only shapes the Rock Pi should look for are Circle, Square, and Triangle.
                #   The Rock Pi should send a message back to the host computer with a list of shapes.
                #   The message should be a list of all shapes found.
                #   Each item in the list should include the type of shape (Circle, Square, or Triangle)
                #   and the x, y coordinates of the center of the shape in the image.
                pass
            elif message.lower == 'trackshape':
                #   track shape - the shape field is either Circle, Square, or Triangle.
                #   The Rock pi should "track" or center the listed object to the center of the image.
                #   The tracking algorithm should execute for 10 seconds.  The Rock Pi should then capture
                #   an image and send it to the host.
                pass
            elif message.lower == 'getangles':
                #   getAngles - the Rock Pi should return the current angles the PTU servos are set at.
                pass
            elif message.lower == 'movepanangle':
                #   move pan_angle, tilt_angle - the Rock Pi should move the PTU to the corresponding angle parameters.
                pass
            elif message.lower == 'movetiltangle':
                #   move pan_angle, tilt_angle - the Rock Pi should move the PTU to the corresponding angle parameters.
                pass
            elif message.lower == 'localcontrol':
                #   localControl - the host should give control to the Rock Pi pushbuttons and wait for a message from
                #   the Rock Pi saying it is ready to relinquish local control.  The Rock Pi releases local control
                #   when the sixth pushbutton is pressed.
                pass
            else:
                print('Recieved a bad input!:', message.lower)
                # should never get into this case here.
        time.sleep(1)
        socket.send(b"Completed....subprocess")

        # check what button is being pressed
        if getValueOfPin(displayButton):
            # print('display button pressed!')
            takePicandDisplay()
            time.sleep(0.2)

        elif getValueOfPin(terminateButton):
            print('terminate connection!')
            time.sleep(0.2)

        elif getValueOfPin(upButton):
            # print('move it up!')
            if currentPWMTILT > 177 - motorStep:
                print('OUT OF BOUNDS! GOING UP CURRENT POSITION', currentPWMTILT)
                pass
            else:
                currentPWMTILT += motorStep
            tiltMotor.write(angletoPWM(currentPWMTILT))
            time.sleep(0.2)

        elif getValueOfPin(downButton):
            # print('move it down!')
            if currentPWMTILT < 0 + motorStep:
                print('OUT OF BOUNDS! GOING DOWN CURRENT POSITION', currentPWMTILT)
                pass
            else:
                currentPWMTILT -= motorStep
            # print('current pwm value tilt:', currentPWMTILT)
            tiltMotor.write(angletoPWM(currentPWMTILT))
            time.sleep(0.2)

        elif getValueOfPin(leftButton):
            # print('move it left!')
            if currentPWMPAN < 0 + motorStep:
                print('OUT OF BOUNDS! GOING LEFT CURRENT POSITION', currentPWMPAN)
                pass
            else:
                currentPWMPAN -= motorStep
            # print('current pwm value tilt:', currentPWMTILT)
            panMotor.write(angletoPWM(currentPWMPAN))
            time.sleep(0.2)

        elif getValueOfPin(rightButton):
            # print('move it right!')
            if currentPWMPAN > 177 - motorStep:
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
            # testBothMotors()
            # takeAPic()

if __name__ == '__main__':
    main()
