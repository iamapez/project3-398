import string

import zmq

context = zmq.Context()

#Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://10.144.113.4:6969")

#Do 10 requests, waiting each time for a response
for request in range(10):
    print("Sending request  %s ..." % request)
    socket.send(b"Hello")

    #Get the reply
    message = socket.recv()
    filteredMessage = message.decode("utf-8")
    print("Received reply %s [ %s ]" % (request, filteredMessage))
