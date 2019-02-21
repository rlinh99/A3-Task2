import zmq
from datetime import *

# Prepare context and sockets
port = 5556

context = zmq.Context()
# Create zmq replier
socket = context.socket(zmq.REP)

#bind replier to a port
socket.bind("tcp://*:%s" % port)
print("ZeroMQ Server is up")

while True:
    # recove request from Client
    message = socket.recv()
    print("Received request from Client")

    request = message.decode()
    print("Received request: {}".format(request))

    # check request's name.
    if request == "get_time":
        socket.send(str(datetime.now()).encode())
