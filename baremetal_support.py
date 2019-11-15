#/usr/bin/python
import argparse

from baremetal_support.baremetal_support import Baremetal_Support

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080

    parser = argparse.ArgumentParser()

    parser.add_argument("-l", "--listen",
                        help="hostname to listen on - defaults to all")
    parser.add_argument("-p", "--port",
                        type=int,
                        help="specify listening port - defaults to 8080")

    args = parser.parse_args()

    if args.port:
        port = args.port

    if args.listen:
        host = args.listen

    server = Baremetal_Support(host=host, port=port)
    server.start()
