import zmq
import subprocess
from datetime import *

# Prepare context and sockets
port = 5556
context = zmq.Context()
socket = context.socket(zmq.REQ)
# connect socket to destination server
socket.connect("tcp://192.168.1.73:%s" % port)

try:
    print("Successfully connected to server.")

    # start timer
    start_time = datetime.now()
    # send request to server
    socket.send("get_time".encode())
    message = socket.recv(4096)
    # end receiving request
    end_time = datetime.now()

    response = message.decode()
    print("Received reply is: {0}".format(response))

    # time calculation
    offset = (end_time - start_time)/2
    result = datetime.strptime(response, '%Y-%m-%d %H:%M:%S.%f') + offset

    print("Request sent at: {0}".format(start_time))
    print("Reply received at : {0}".format(end_time))
    print("Offset (RTT/2) is {0}".format(offset))

    # for linux system, modify system time
    subprocess.run(["date", "-s", str(result)])
    print("Time is set to: {0}".format(str(result)))
finally:
    print("An exception has occurred, terminate")
    socket.close()
