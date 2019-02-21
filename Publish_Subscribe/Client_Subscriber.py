import zmq
import subprocess
import datetime


def main():
    # define server name
    server_name = "192.168.1.73"

    # prepare context and subscriber
    context = zmq.Context()
    # create subscriber socket
    subscriber = context.socket(zmq.SUB)
    # connect subscriber to destination publisher server
    subscriber.connect("tcp://{0}:5563".format(server_name))
    # send message to publisher

    try:
        # start timer
        start_time = datetime.datetime.now()
        # send subscribe message to publisher
        subscriber.setsockopt(zmq.SUBSCRIBE, "get_time".encode())
        # get envelope from server
        [address, contents] = subscriber.recv_multipart()
        # end timer
        end_time = datetime.datetime.now()

        # calculate offset and result server time
        offset = (end_time - start_time) / 2
        result = datetime.datetime.strptime(contents.decode(), '%Y-%m-%d %H:%M:%S.%f') + offset

        # print result
        print("Subscriber starts at: {0}".format(start_time))
        print("Content received at : {0}".format(end_time))
        print("Offset (RTT/2) is {0}".format(offset))

        # optional: modify linux system time
        # please run with sudo permission
        subprocess.run(["date", "-s", str(result)])
        print("Time is set to: {0}".format(str(result)))

        # print("[%s] %s" % (address, contents))
    finally:
        subscriber.close()
        context.term()


if __name__ == "__main__":
    main()
