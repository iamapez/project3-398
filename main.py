import cv2

import mraa
import time
import sys
import cv2 as cv
import zmq
import base64
import os
import shutil

# from PIL import Image


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


class localShape:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y


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


def takePicandDisplayRemote():
    cam = cv.VideoCapture(4)
    # cv.namedWindow("CSE398")

    img_counter = 0
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")

    img_name = "opencv_frame_{}.png".format(img_counter)
    cv.imwrite(img_name, frame)
    print("{} written!".format(img_name))
    img_counter += 1

    f = open(img_name, 'rb')
    bytes = bytearray(f.read())
    strng = base64.b64encode(bytes)
    f.close()

    return strng


def getShapes():
    #   getShapes - the Rock Pi takes an image and detects shapes in the image.
    #   The only shapes the Rock Pi should look for are Circle, Square, and Triangle.
    #   The Rock Pi should send a message back to the host computer with a list of shapes.
    #   The message should be a list of all shapes found.
    #   Each item in the list should include the type of shape (Circle, Square, or Triangle)
    #   and the x, y coordinates of the center of the shape in the image.

    cam = cv.VideoCapture(4)
    # cv.namedWindow("CSE398")

    img_counter = 0
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")

    img_name = "getShapesTempFile.png"
    cv.imwrite(img_name, frame)
    print("{} written!".format(img_name))
    img_counter += 1

    img = cv.imread('img_name')
    gray = cv.cvtColor(img, cv2.COLOR_BGR2GRAY)


def getImage():
    pass


def getShapes():
    # getShapes - the Rock Pi takes an image and detects shapes in the image.
    #   The only shapes the Rock Pi should look for are Circle, Square, and Triangle.
    #   The Rock Pi should send a message back to the host computer with a list of shapes.
    #   The message should be a list of all shapes found.
    #   Each item in the list should include the type of shape (Circle, Square, or Triangle)
    #   and the x, y coordinates of the center of the shape in the image.

    # take image
    # detect shapes
    # add to list of objects, set name, x val, y val
    # return list
    return []

def main():
    # main entry point for the program here
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:6969')

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
        try:
            message = socket.recv()
            # print('type message is:', type(message))
            # print('message recieved', message)
            if message.lower() == 'getimage':
                # get image
                response = takePicandDisplayRemote()
                socket.send(response)
                # print('Called getimage method on server!')
                # socket.send(b'getimage done!')
            elif message.lower() == 'getshapes':
                response = getShapes()      # we get a list of objects of shapes here, (type,x,y)
                socket.send(response)       # might have to clean up response so it can be decoded on client side first
                print('called getshapes method on server!')
                # socket.send(b'getshape done!')
            elif message.lower() == 'trackshape':
                #   track shape - the shape field is either Circle, Square, or Triangle.
                #   The Rock pi should "track" or center the listed object to the center of the image.
                #   The tracking algorithm should execute for 10 seconds.  The Rock Pi should then capture
                #   an image and send it to the host.
                print('called trackshape on server!')
                socket.send(b'trackshape done!')
            elif message.lower() == 'getangles':
                #   getAngles - the Rock Pi should return the current angles the PTU servos are set at.
                print('called getangles method on server!')
                socket.send(b'getangles done!')
            elif message.lower() == 'movepanangle':
                #   move pan_angle, tilt_angle - the Rock Pi should move the PTU to the corresponding angle parameters.
                print('called movepanangle method on server!')
                socket.send(b'movepanangle done!')
            elif message.lower() == 'movetiltangle':
                #   move pan_angle, tilt_angle - the Rock Pi should move the PTU to the corresponding angle parameters.
                print('called movepanangle method on server!')
                socket.send(b'movepanangle done!')
            elif message.lower() == 'localcontrol':
                #   localControl - the host should give control to the Rock Pi pushbuttons and wait for a message from
                #   the Rock Pi saying it is ready to relinquish local control.  The Rock Pi releases local control
                #   when the sixth pushbutton is pressed.
                print('called localcontrol method on server!')
                socket.send(b'localcontrol done!')
            else:
                print('Recieved a bad input!:', message)
                socket.send(b'Recieved a bad input!')
                # should never get into this case here.
            time.sleep(1)

        except zmq.Again as e:
            print('no message yet')

        # check what button is being pressed
        if getValueOfPin(displayButton):
            print('display button pressed!')
            takePicandDisplay()
            time.sleep(0.2)

        elif getValueOfPin(terminateButton):
            print('terminate connection!')
            time.sleep(0.2)

        elif getValueOfPin(upButton):
            print('move it up!')
            if currentPWMTILT > 177 - motorStep:
                print('OUT OF BOUNDS! GOING UP CURRENT POSITION', currentPWMTILT)
                pass
            else:
                currentPWMTILT += motorStep
            tiltMotor.write(angletoPWM(currentPWMTILT))
            time.sleep(0.2)

        elif getValueOfPin(downButton):
            print('move it down!')
            if currentPWMTILT < 0 + motorStep:
                print('OUT OF BOUNDS! GOING DOWN CURRENT POSITION', currentPWMTILT)
                pass
            else:
                currentPWMTILT -= motorStep
            # print('current pwm value tilt:', currentPWMTILT)
            tiltMotor.write(angletoPWM(currentPWMTILT))
            time.sleep(0.2)

        elif getValueOfPin(leftButton):
            print('move it left!')
            if currentPWMPAN < 0 + motorStep:
                print('OUT OF BOUNDS! GOING LEFT CURRENT POSITION', currentPWMPAN)
                pass
            else:
                currentPWMPAN -= motorStep
            # print('current pwm value tilt:', currentPWMTILT)
            panMotor.write(angletoPWM(currentPWMPAN))
            time.sleep(0.2)

        elif getValueOfPin(rightButton):
            print('move it right!')
            if currentPWMPAN > 177 - motorStep:
                print('OUT OF BOUNDS! GOING RIGHT CURRENT POSITION', currentPWMPAN)
                pass
            else:
                currentPWMPAN += motorStep
            # print('current pwm value tilt:', currentPWMTILT)
            panMotor.write(angletoPWM(currentPWMPAN))
            time.sleep(0.2)

        else:
            print('nothing pressed')
            time.sleep(0.2)
            # testBothMotors()
            # takeAPic()


if __name__ == '__main__':
    main()
