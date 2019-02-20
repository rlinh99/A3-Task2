import time
import zmq
import datetime


def main():
    # Prepare our context and publisher
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:5563")
    try:
        while True:
            content = str(datetime.datetime.now()).encode()
            # Write two messages, each with an envelope and content
            publisher.send_multipart([b"get_time", content])
            publisher.send_multipart([b"B", b"We would like to see this"])
            time.sleep(1)
    finally:
        publisher.close()
        context.term()


if __name__ == "__main__":
    main()
