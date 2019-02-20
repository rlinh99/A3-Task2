import zmq
from datetime import *
port = 5556
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)
print("ZeroMQ Server is up")

while True:
    message = socket.recv()
    print("Received request from Client")

    request = message.decode()
    print("Received request: {}".format(request))

    if request == "get_time":
        socket.send(str(datetime.now()).encode())
