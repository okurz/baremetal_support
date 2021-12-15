#!/usr/bin/python
import argparse

from baremetal_support.baremetal_support import Baremetal_Support
from baremetal_support.logging import Logging



if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    instance = "http://openqa.suse.de"

    parser = argparse.ArgumentParser()

    parser.add_argument("-l", "--listen",
                        help="hostname to listen on - defaults to all")
    parser.add_argument("-p", "--port",
                        type=int,
                        help="specify listening port - defaults to 8080")
    parser.add_argument("-i", "--instance",
                        help="specify openQA instance - defaults to http://openqa.suse.de")
    parser.add_argument("-m", "--loglevel",
                        help="Loglevel to use, one of DEBUG, INFO, WARNING, ERROR, CRITICAL, default is INFO")

    args = parser.parse_args()

    if args.port:
        port = args.port

    if args.listen:
        host = args.listen

    if args.instance:
        instance = args.instance

    if args.loglevel:
        logger = Logging("baremetal support", args.loglevel)
    else:
        logger = Logging("baremetal support", "INFO")

    server = Baremetal_Support(host=host, port=port, logger=logger, instance=instance)
    server.start()
