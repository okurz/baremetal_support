import pytest
import socket
import requests

import signal
import pytest_cov.embed

from multiprocessing import Process
from time import sleep

from ipxe_http.server import Server



hostname = 'localhost'
port = '1234'

url = 'http://' + hostname + ':' + port + '/'
use_ip = '10.0.0.1'

url_bootscript = url + use_ip + '/script.ipxe'
url_get = url + 'script.ipxe'


def cleanup(*_):
    pytest_cov.embed.cleanup()
    sys.exit(1)

signal.signal(signal.SIGTERM, cleanup)

def server_task(arg):
    arg.start()

def start_server():
    server = Server(hostname, port)
    assert isinstance(server,Server) == True
    p = Process(target=server_task, args=(server, ))
    p.start()
    sleep(1)
    return p

def stop_server(p):
    p.terminate()
    sleep(1)

def test_name_to_ip_exception():
    server = Server(hostname, port)
    with pytest.raises(socket.error):
        inval = server._to_ip("foobar")

def test_set_and_get_bootscript():
    my_bootscript = "this is my bootscript"
    p = start_server()

    print("POST: " +url_bootscript)
    r1 = requests.post(url_bootscript, data=my_bootscript)
    assert r1.status_code == 200
    r2 = requests.get(url_bootscript)
    assert r2.status_code == 200
    assert r2.text == my_bootscript

    stop_server(p)



def test_get_bootscript_status_codes():
    p = start_server()

    err_url = url + 'foobar/script.ipxe' 

    r1 = requests.post(err_url, data='illegal')
    assert r1.status_code == 400

    r2 = requests.get(err_url)
    assert r2.status_code == 400

    err_url = url + '10.10.10.10/script.ipxe'
    r3  = requests.get(err_url)
    assert r3.status_code == 404

    stop_server(p)


def test_get_script_for_localhost():
    text = "data foo bar"
    p = start_server()

    url1 = url + 'script.ipxe' 
    r1 = requests.get(url1)
    assert r1.status_code == 404

    url2 = url_bootscript = url + '127.0.0.1' + '/script.ipxe'
    r2 = requests.post(url2, data='foo bar baz')
    assert r2.status_code == 200

    r1 = requests.get(url1)
    assert r1.status_code == 200

    stop_server(p)

