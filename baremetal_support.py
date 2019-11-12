#!/usr/bin/python

# Copyright (C) 2019 SUSE LLC
# SPDX-License-Identifier: GPL-3.0
import argparse
import socket

from bottle import Bottle, request, response

from .bootscript import Bootscript, BootscriptNotFound
from .lock import Host_Lock, HostAlreadyLocked, HostNotLocked


class Baremetal_Support:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._app = Bottle()

        self._bootscript = Bootscript(self._app)
        self._locks = Host_Lock(self._app)

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
