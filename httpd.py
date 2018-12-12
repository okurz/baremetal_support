#!/usr/bin/env python3

from bottle import Bottle, request, route, run, response, template
import json 

autoinst = {}
bootscript = {}

class Server:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._app = Bottle()
        self._route()

    def _route(self):
        # route methods for autoinst.xml
        self._app.route('/autoinst.xml', METHOD="GET",  callback = self.get_autoinst)
        self._app.route('/autoinst.xml', METHOD="POST", callback = self.set_autoinst)

        # route methods for ipxe bootscript
        self._app.route('/script.ipxe',  METHOD="GET",  callback = self.get_bootscript)
        self._app.route('/script.ipxe',  METHOD="POST", callback = self.set_bootscript)

        # these should be removed.. 
        self._app.route('/setversion',   METHOD="POST", callback = self.set_version)


    def start(self):
        self._app.run(host=self._host,  port=self._port, debug=True)


    def get_bootscript(self, ip='none'):
        if (ip == 'none'):
            ip = request.environ.get('REMOTE_ADDR')
        return bootscript[ip]
        
    def set_bootscript(self):
        ip = request.json['ip']
        bootscript[ip] = request.json['bootscript']



    def get_autoinst(self):
        ip = request.environ.get('REMOTE_ADDR')
        return autoyast[ip]

    def set_autoinst(self):
        ip = request.json['ip']
        autoinst[ip] = request.json['autoinst']

    # this is an ugly hack to easily create configurations for 12.x or 15.x
    def set_version(self):
        ip = request.json['ip']
        version = request.json['version']
    
        kern = "tftp://10.162.0.1/mounts/dist/install/SLP/" + version 
        kern = kern +"-Installer-TEST/x86_64/DVD1/boot/x86_64/loader/linux"
        inst = "install=nfs://10.160.0.100/dist/install/SLP/SLE-15-SP1-Installer-TEST/x86_64/DVD1"
        auto = "autoyast=http://" + self._host + " /autoinst.xml"

        kernel = "kernel " + kern + " " + inst + " " + auto
        initrd = "initrd tftp://10.162.0.1/mounts/dist/install/SLP/" + version 
        initrd = initrd +"-Installer-TEST/x86_64/DVD1/boot/x86_64/loader/initrd"

        bootscript[ip] = kernel + "\n" + initrd
        response.headers['Content-Type'] = 'application/json'
        return json.dumps(request.json)


if __name__ == "__main__":
    server = Server(host='localhost', port='8080')
    server.start()
