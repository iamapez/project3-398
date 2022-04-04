# import shutil
import shutil
import string
import base64
import zmq
from PIL import Image
import os

context = zmq.Context()

# Socket to talk to server
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


def checkStatus(message):
    if ((message == 'trackshape done!') or (message == 'getimage done!') or (message == 'getangles done!') or (
            message == 'movetiltangle done!') or (message == 'movepanangle done!') or (
            message == 'localcontrol done!')):
        print("Success!!")
    else:
        print("Unsuccessful")


while 1:
    userInput = ''
    userInput = input('What command would you like to use?')
    if userInput.lower() == 'getimage':
        try:
            socket.send(b"getimage")
            message = socket.recv()
            print(message.decode("utf-8"))
            f = open("receivedimage.jpg", 'wb')
            ba = bytearray(base64.b64decode(message))
            f.write(ba)
            f.close()

            im = Image.open(r"receivedimage.jpg")
            im.show()
            print("Got here")
            if im is None:
                # image = cv.imread(image_filename)
                # cv.imshow("Received Image", image)
                os.remove(im)

        except Exception as b:
            print('Error while sending the message!')

    elif userInput.lower() == 'getshapes':
        try:
            socket.send(b"getshapes")
            message = socket.recv()
            print(message.decode("utf-8"))
        except Exception as b:
            print('Error while sending the message!')
    elif userInput.lower() == 'trackshape':
        try:
            socket.send(b"trackshape")
            message = socket.recv()
            print(message.decode("utf-8"))
        except Exception as b:
            print('Error while sending the message!')
    elif userInput.lower() == 'getangles':
        try:
            socket.send(b"getangles")
            message = socket.recv()
            print(message.decode("utf-8"))
        except Exception as b:
            print('Error while sending the message!')
    elif userInput.lower() == 'movepanangle':
        try:
            socket.send(b"movepanangle")
            message = socket.recv()
            print(message.decode("utf-8"))
        except Exception as b:
            print('Error while sending the message!')
    elif userInput.lower() == 'movetiltangle':
        try:
            socket.send(b"movetiltangle")
            message = socket.recv()
            print(message.decode("utf-8"))
        except Exception as b:
            print('Error while sending the message!')
    elif userInput.lower() == 'localcontrol':
        try:
            socket.send(b"localcontrol")
            message = socket.recv()
            print(message.decode("utf-8"))
        except Exception as b:
            print('Error while sending the message!')
    else:
        print('BAD USER INPUT! DID NOT SEND ANYTHING')
