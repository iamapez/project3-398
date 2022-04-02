import string

import zmq

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
