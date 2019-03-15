#!/usr/bin/env python3

from bottle import Bottle, request, route, run, response, template

import socket
from .bootscript import Bootscript, BootscriptNotFound

class Server:
    def __init__(self, host, port):
        self._bootscript = Bootscript()
        self._host = host
        self._port = port
        self._app = Bottle()
        self._route()

    def _route(self):
        # route methods for ipxe bootscript
        self._app.route('/script.ipxe',  method="GET",  callback = self.get_bootscript_for_peer)
        self._app.route('/<addr>/script.ipxe',  method="POST", callback = self.set_bootscript)
        self._app.route('/<addr>/script.ipxe',  method="GET", callback = self.get_bootscript)

    def start(self):
        self._app.run(host=self._host,  port=self._port, debug=True)

    def _to_ip(self, addr):
        """ convert an address/IP to an IP """
        try:
            addr = socket.inet_aton(addr)
        except Exception as e: raise


    def get_bootscript_for_peer(self):
        addr =request.environ.get('REMOTE_ADDR')
        return self.get_bootscript(addr)

    def get_bootscript(self, addr):
        
        try:
            ip = self._to_ip(addr)
            response.content_type = 'text/text; charset=utf-8'
            ret = self._bootscript.get(ip)
            return ret

        except socket.error:
            # invalid address specified
            response.status = 400
        except BootscriptNotFound:
            # no script found for this IP
            response.status = 404
        
    def set_bootscript(self, addr):
        try:
            ip = self._to_ip(addr)
            postdata = request.body.read()
            script = postdata.decode('utf-8')
            self._bootscript.set(ip, script)
            response.status = 200

        except socket.error:
            # invalid address specified
            response.status = 400

    

if __name__ == "__main__":
    server = Server(host='0.0.0.0', port='8080')
    server.start()
