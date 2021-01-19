# Copyright (C) 2019 SUSE LLC
# SPDX-License-Identifier: GPL-3.0

import bottle
import socket


class BootscriptNotFound(Exception):
    """Raised when the address is invalid"""
    pass


class Bootscript:
    def __init__(self, app):
        self.bootscript = {}
        self._app = app
        self._app.route('/v1/bootscript/script.ipxe',
                        method="GET",
                        callback=self.http_get_bootscript_for_peer)
        self._app.route('/v1/bootscript/script.ipxe/<addr>',
                        method="POST",
                        callback=self.http_set_bootscript)
        self._app.route('/v1/bootscript/script.ipxe/<addr>',
                        method="GET",
                        callback=self.http_get_bootscript)

    def set(self, ip, script):
        """ set the bootscript in the dict """
        self.bootscript[ip] = script

    def get(self, ip):
        """ return specific bootscript """
        try:
            return self.bootscript[ip]
        except KeyError:
            raise BootscriptNotFound("no script found for requested ip")

    def _is_ip(self, addr):
        try:
            socket.inet_aton(addr)
            return True
        except socket.error:
            return False

    def http_get_bootscript_for_peer(self):
        addr = bottle.request.environ.get('REMOTE_ADDR')
        return self.http_get_bootscript(addr)

    def http_get_bootscript(self, addr):
        try:
            if self._is_ip(addr):
                bottle.response.content_type = 'text/text; charset=utf-8'
                return self.get(addr)
            else:
                # invalid address specified
                bottle.response.status = 400
        except BootscriptNotFound:
            # no script found for this IP
            bottle.response.body = 'not found'
            bottle.response.status = '404 Not Found'
            return bottle.response

    def http_set_bootscript(self, addr):
        print("GET: " + addr)
        if self._is_ip(addr):
            postdata = bottle.request.body.read()
            script = postdata.decode('utf-8')
            self.set(addr, script)
            bottle.response.status = 200
        else:
            bottle.response.status = 400
