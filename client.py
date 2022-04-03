import shutil
import string
import base64
import zmq
import cv2 as cv
import os

context = zmq.Context()

#Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://10.144.113.4:6969")


# testing
# #Do 10 requests, waiting each time for a response
# for request in range(10):
#     print("Sending request  %s ..." % request)
#     socket.send(b"Hello")
#
#     #Get the reply
#     message = socket.recv()
#     filteredMessage = message.decode("utf-8")
#     print("Received reply %s [ %s ]" % (request, filteredMessage))

while 1:
    userInput = input('What command would you like to use?')
    if userInput.lower() == 'getimage':
        try:
            socket.send(b"getimage")
            message = socket.recv()
            f = open("receivedimage.jpg", 'wb')
            ba = bytearray(base64.b64decode(message))
            f.write(ba)
            f.close()

            image_dir = os.path.join('path', 'to', 'image')
            image_filename = 'image.jpg'
            full_image_path = os.path.join(image_dir, image_filename)

            image = cv.imread(full_image_path)
            if image is None:
                shutil.copy(full_image_path, image_filename)
                image = cv.imread(image_filename)
                cv.imshow("Received Image", image)
                os.remove(image_filename)
        except Exception as b:
            print('Error while sending the message!')

    elif userInput.lower() == 'getshapes':
        try:
            socket.send(b"getshapes")
        except Exception as b:
            print('Error while sending the message!')
    elif userInput.lower() == 'trackshape':
        try:
            socket.send(b"trackshape")
        except Exception as b:
            print('Error while sending the message!')
    elif userInput.lower() == 'getangles':
        try:
            socket.send(b"getangles")
        except Exception as b:
            print('Error while sending the message!')
    elif userInput.lower() == 'movepanangle':
        try:
            socket.send(b"movepanangle")
        except Exception as b:
            print('Error while sending the message!')
    elif userInput.lower() == 'movetiltangle':
        try:
            socket.send(b"movetiltangle")
        except Exception as b:
            print('Error while sending the message!')
    elif userInput.lower() == 'localcontrol':
        try:
            socket.send(b"localcontrol")
        except Exception as b:
            print('Error while sending the message!')
    else:
        print('BAD USER INPUT! DID NOT SEND ANYTHING')
