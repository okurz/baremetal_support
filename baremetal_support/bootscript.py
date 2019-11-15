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
        self.bootscript.update({ip: script})

    def get(self, ip):
        """ return specific bootscript """
        try:
            return self.bootscript[ip]
        except KeyError:
            raise BootscriptNotFound("no script found for requested ip")

    def _to_ip(self, addr):
        """ convert an address/IP to an IP """
        try:
            addr = socket.inet_aton(addr)
        except Exception as e:
            raise

    def http_get_bootscript_for_peer(self):
        addr = bottle.request.environ.get('REMOTE_ADDR')
        return self.http_get_bootscript(addr)

    def http_get_bootscript(self, addr):
        try:
            ip = self._to_ip(addr)
            bottle.response.content_type = 'text/text; charset=utf-8'
            return self.get(ip)

        except socket.error:
            # invalid address specified
            bottle.response.status = 400
        except BootscriptNotFound:
            # no script found for this IP
            bottle.response.body = 'not found'
            bottle.response.status = '404 Not Found'
            return bottle.response

    def http_set_bootscript(self, addr):
        try:
            ip = self._to_ip(addr)
            postdata = bottle.request.body.read()
            script = postdata.decode('utf-8')
            self.set(ip, script)
            bottle.response.status = 200

        except socket.error:
            # invalid address specified
            bottle.response.status = 400
