import pytest
import socket

from .server import Server

def test_server():
    """ ensure the server can be instantiated """
    server = Server("localhost","1234")
    assert isinstance(server,Server) == True

def test_name_to_ip_exception():
    server = Server("localhost","1234")
    with pytest.raises(socket.error):
        inval = server._to_ip("foobar")
