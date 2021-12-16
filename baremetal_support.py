#!/usr/bin/python
# Copyright (C) 2019-2021 SUSE LLC
import argparse

from baremetal_support.baremetal_support import Baremetal_Support
from baremetal_support.logging import Logging
import yaml



if __name__ == "__main__":
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
    parser.add_argument("-c", "--config",
                        help="Specify configuration file to use. Will not use a default. "
                        "command line settings override settings in the config file")

    args = parser.parse_args()

    if args.config:
        with open(args.config, "r",) as ymlfile:
            conf = yaml.safe_load(ymlfile)
            cfg = conf["baremetal_support"]
    if args.port:
        port = args.port
    elif cfg["port"]:
        port = cfg["port"]
    else:
        port = 8080

    if args.listen:
        host = args.listen
    elif cfg["listen"]:
        host = cfg["listen"]
    else:
        host = "0.0.0.0"

    if args.instance:
        instance = args.instance
    elif cfg["openqa_instance"]:
        instance = cfg["openqa_instance"]
    else:
        instance = "https://openqa.suse.de"

    if args.loglevel:
        loglevel = args.loglevel
    elif cfg["loglevel"]:
        loglevel = cfg["loglevel"]
    else:
        loglevel = "INFO"
    logger = Logging("baremetal support", "INFO")

    server = Baremetal_Support(host=host, port=port, logger=logger, instance=instance)

    logger.info("Listening on " + host + ":" + str(port))
    logger.info("Connecting to openQA-instance at " + instance)
    logger.info("Log level is " + loglevel)

    server.start()
