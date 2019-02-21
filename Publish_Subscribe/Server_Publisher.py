import time
import zmq
import datetime


def main():
    # create zmq context and publisher
    context = zmq.Context()
    # create context as publisher
    publisher = context.socket(zmq.PUB)
    # bind publisher with address
    publisher.bind("tcp://*:5563")

    try:
        while True:
            content = str(datetime.datetime.now()).encode()
            # set the message in the publisher
            publisher.send_multipart([b"get_time", content])

            time.sleep(1)
    finally:
        publisher.close()
        context.term()


if __name__ == "__main__":
    main()
