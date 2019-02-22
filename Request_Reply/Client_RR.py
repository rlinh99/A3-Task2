import zmq
import subprocess
from datetime import *

# Prepare ZMQ context and sockets
server_name = "192.168.1.73"
port = 5556
context = zmq.Context()
# create request socket
socket = context.socket(zmq.REQ)
# connect socket to destination server
socket.connect("tcp://{0}:{1}".format(server_name, port))

try:
    print("Successfully connected to server.")

    # start timer
    start_time = datetime.now()
    # send request to server
    socket.send("get_time".encode())
    # receive reply from server
    message = socket.recv(4096)
    # end timer
    end_time = datetime.now()
    # decode reply
    response = message.decode()
    print("Received reply is: {0}".format(response))

    # calculate offset and result server time
    offset = (end_time - start_time) / 2
    result = datetime.strptime(response, '%Y-%m-%d %H:%M:%S.%f') + offset

    # print out result
    print("Request sent at: {0}".format(start_time))
    print("Reply received at : {0}".format(end_time))
    print("Offset (RTT/2) is {0}".format(offset))

    # optional: modify linux system time
    # please run with sudo permission
    subprocess.run(["date", "-s", str(result)])
    print("Time is set to: {0}".format(str(result)))
finally:
    socket.close()
    context.term()
