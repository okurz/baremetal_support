#!/usr/bin/env python3

from bottle import Bottle, request, route, run, response, template

bootscript = {}

class Server:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._app = Bottle()
        self._route()

    def _route(self):
        # route methods for ipxe bootscript
        self._app.route('/script.ipxe',  method="GET",  callback = self.get_bootscript)
        self._app.route('/<ip>/script.ipxe',  method="POST", callback = self.set_bootscript)


    def start(self):
        self._app.run(host=self._host,  port=self._port, debug=True)


    def get_bootscript(self):
        ip = request.environ.get('REMOTE_ADDR')
        print("Serving for " + ip)
        if ip in bootscript:
            resp = bootscript[ip]
            response.content_type = 'text/text; charset=utf-8'
            return resp
        else:
            response.status = 404
        
    def set_bootscript(self, ip):
        postdata = request.body.read()
        script = postdata.decode('utf-8')
        
        bootscript.update({ip: script})
    

if __name__ == "__main__":
    server = Server(host='0.0.0.0', port='8080')
    server.start()
