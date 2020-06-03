# Copyright (C) 2019 SUSE LLC
# SPDX-License-Identifier: GPL-3.0
from bottle import Bottle

from .bootscript import Bootscript
from .lock import Host_Lock
from . jobid import LatestJob

if __name__ == "__main__":
    import argparse


class Baremetal_Support:
    def __init__(self, host, port, instance):
        self._host = host
        self._port = port
        self._instance = instance
        self._app = Bottle()

        self._bootscript = Bootscript(self._app)
        self._locks = Host_Lock(self._app)
        self._latest_job = LatestJob(self._app, self._instance)

        self._route()

    def _route(self):
        # route methods for ipxe bootscript
        # unversioned API is deprecated!
        self._app.route('/script.ipxe',
                        method="GET",
                        callback=self._bootscript.http_get_bootscript_for_peer)
        self._app.route('/<addr>/script.ipxe',
                        method="POST",
                        callback=self._bootscript.http_set_bootscript)
        self._app.route('/<addr>/script.ipxe',
                        method="GET",
                        callback=self._bootscript.http_get_bootscript)

        # bootscript API
    def start(self):
        self._app.run(host=self._host, port=self._port, debug=True)
