import zmq
import subprocess
import datetime


def main():
    # Prepare context and publisher
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5563")
    subscriber.setsockopt(zmq.SUBSCRIBE, "get_time".encode())

    try:
        # Read envelope with address
        start_time = datetime.datetime.now()
        [address, contents] = subscriber.recv_multipart()
        end_time = datetime.datetime.now()

        offset = (end_time - start_time) / 2
        result = datetime.datetime.strptime(contents.decode(), '%Y-%m-%d %H:%M:%S.%f') + offset

        print("Subscriber starts at: {0}".format(start_time))
        print("Content received at : {0}".format(end_time))
        print("Offset (RTT/2) is {0}".format(offset))

        subprocess.run(["date", "-s", str(result)])
        print("Time is set to: {0}".format(str(result)))

        # print("[%s] %s" % (address, contents))
    finally:
        subscriber.close()
        context.term()


if __name__ == "__main__":
    main()
