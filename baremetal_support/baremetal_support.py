# Copyright (C) 2019-2021 SUSE LLC
# SPDX-License-Identifier: GPL-3.0
from bottle import Bottle

from .bootscript import Bootscript
from .lock import Host_Lock
from . jobid import LatestJob
from .logging import Logging


if __name__ == "__main__":
    import argparse


class Baremetal_Support:
    def __init__(self, host, port, logger, instance):
        self.log = logger
        self._host = host
        self._port = port
        self._instance = instance
        self._app = Bottle()

        self._bootscript = Bootscript(self._app, self.log)
        self._locks = Host_Lock(self._app, self.log)
        self._latest_job = LatestJob(self._app, self.log, self._instance)
        self.log.info("host=" + host + ", Port " + port)
        self.log.info("using openQA instance " + instance)
        self._route()

    def _route(self):
        # route methods for ipxe bootscript
        # unversioned API is deprecated!
        self.log.debug("routing legacy API endpoints")
        self.log.debug("/script.ipxe [GET]")
        self._app.route('/script.ipxe',
                        method="GET",
                        callback=self._bootscript.http_get_bootscript_for_peer)
        self.log.debug("/<addr>/script.ipxe [POST][GET]")
        self._app.route('/<addr>/script.ipxe',
                        method="POST",
                        callback=self._bootscript.http_set_bootscript)
        self._app.route('/<addr>/script.ipxe',
                        method="GET",
                        callback=self._bootscript.http_get_bootscript)

        # bootscript API
    def start(self):
        self.log.info("Starting baremetal support service")
        self._app.run(host=self._host, port=self._port, debug=True)
