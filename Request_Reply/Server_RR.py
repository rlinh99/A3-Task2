import zmq
from datetime import *

# Prepare ZMQ context and sockets
port = 5556

context = zmq.Context()
# create zmq reply socket
socket = context.socket(zmq.REP)

# bind replier to a port
socket.bind("tcp://*:%s" % port)
print("ZeroMQ Server is up")
try:
    while True:
        # receive request from Client
        message = socket.recv()
        print("Received request from Client")

        # decode request
        request = message.decode()
        print("Received request: {}".format(request))

        # validate request, end response
        if request == "get_time":
            socket.send(str(datetime.now()).encode())
finally:
    socket.close()
    context.term()
