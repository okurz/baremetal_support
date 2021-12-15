# Copyright (C) 2019 SUSE LLC
# SPDX-License-Identifier: GPL-3.0

import logging
import sys


class Logging:
    def __init__(self, name, level):
        self.logger = logging.getLogger(name)
        self.set_level(level)

        formatter = logging.Formatter(fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s",
                                      datefmt="%Y.%m.%d %H:%M:%S")

        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def set_level(self, level):
        self.debug("Setting loglevel to " + level)
        if level.upper == "DEBUG":
            self.logger.setLevel(logging.DEBUG)
        elif level.upper == "INFO":
            self.logger.setLevel(logging.INFO)
        elif level.upper == "WARN":
            self.logger.setLevel(logging.WARNING)
        elif level.upper == "ERROR":
            self.logger.setLevel(logging.ERROR)
        elif level.upper == "CRITICAL":
            self.logger.setLevel(logging.CRITICAL)
        else:
            self.logger.setLevel(logging.NOTSET)


    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)