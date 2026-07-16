# Copyright (C) 2019-2021 SUSE LLC
# SPDX-License-Identifier: GPL-3.0

from bottle import Bottle
import bottle
import io
from pytest import raises

from baremetal_support.bootscript import Bootscript, BootscriptNotFound
from baremetal_support.logging import Logging

logger = Logging("baremetal support", "DEBUG")


def test_set():
    app = Bottle()
    # test if the key is present after setting the value
    bs = Bootscript(app, logger)
    bs.set("10.0.0.1", "foo")
    assert "10.0.0.1" in bs.bootscript

    # overwrite a value and make sure it can be read
    bs = Bootscript(app, logger)
    bs.set("10.0.0.1", "foo")
    assert bs.get("10.0.0.1") == "foo"
    bs.set("10.0.0.1", "bar")
    assert bs.get("10.0.0.1") == "bar"

    count = 0
    while count < 1000000:
        bs.set("10.0.0.1", "bar")
        bs.set("10.0.0.2", "foobar")
        assert bs.get("10.0.0.1") == "bar"
        assert bs.get("10.0.0.2") == "foobar"
        count = count + 1


def test_get():
    app = Bottle()
    # retrieve value after setting it
    bs = Bootscript(app, logger)
    bs.set("10.0.0.1", "foo")
    assert bs.get("10.0.0.1") == "foo"

    with raises(BootscriptNotFound):
        _ = bs.get("20.21.22.23")


def test_extra():
    app = Bottle()
    # ensure a new object does not contain entries
    bs = Bootscript(app, logger)
    assert len(bs.bootscript) == 0

    inval = "fooinval"
    with raises(BootscriptNotFound):
        inval = bs.get("10.0.0.1")
    assert inval == "fooinval"


def test_http_get_bootscript_for_peer():
    app = Bottle()
    bs = Bootscript(app, logger)
    bs.set("10.0.0.1", "foo")
    bottle.request.environ["REMOTE_ADDR"] = "10.0.0.1"
    res = bs.http_get_bootscript_for_peer()
    assert res == "foo"


def test_http_get_bootscript_invalid_ip():
    app = Bottle()
    bs = Bootscript(app, logger)
    bs.http_get_bootscript("invalid_ip")
    assert "400" in bottle.response.status


def test_http_get_bootscript_not_found():
    app = Bottle()
    bs = Bootscript(app, logger)
    res = bs.http_get_bootscript("10.0.0.2")
    assert "404" in res.status


def test_http_set_bootscript():
    app = Bottle()
    bs = Bootscript(app, logger)
    bottle.request.environ["wsgi.input"] = io.BytesIO(b"my_custom_script")
    bottle.request.environ["CONTENT_LENGTH"] = str(len(b"my_custom_script"))
    bs.http_set_bootscript("10.0.0.3")
    assert bs.get("10.0.0.3") == "my_custom_script"
    assert "200" in bottle.response.status


def test_http_set_bootscript_invalid():
    app = Bottle()
    bs = Bootscript(app, logger)
    bs.http_set_bootscript("invalid_ip")
    assert "400" in bottle.response.status
