#
#   Request-reply client in Python
#   Connects REQ socket to tcp://localhost:5559
#   Sends "Hello" to server, expects "World" back
#
import zmq
import subprocess
from datetime import *

#  Prepare our context and sockets

port = 5556
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.1.73:%s" % port)

#  Do 10 requests, waiting each time for a response
try:
    print("Successfully connected to server.")
    start_time = datetime.now()
    socket.send("get_time".encode())
    message = socket.recv(4096)
    end_time = datetime.now()

    response = message.decode()
    print("Received reply is: {0}".format(response))

    offset = (end_time - start_time)/2
    result = datetime.strptime(response, '%Y-%m-%d %H:%M:%S.%f') + offset

    print("Request sent at: {0}".format(start_time))
    print("Reply received at : {0}".format(end_time))
    print("Offset (RTT/2) is {0}".format(offset))

    # subprocess.run(["date", "-s", str(result)])
    print("Time is set to: {0}".format(str(result)))
finally:
    print("An exception has occurred, terminate")
    socket.close()
