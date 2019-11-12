# Copyright (C) 2019 SUSE LLC
# SPDX-License-Identifier: GPL-3.0

from bottle import Bottle
from unittest import TestCase
from pytest import raises

from baremetal_support.bootscript import Bootscript, BootscriptNotFound


def test_set():
    app = Bottle()
    # test if the key is present after setting the value
    bs = Bootscript(app)
    bs.set("10.0.0.1", "foo")
    assert "10.0.0.1" in bs.bootscript

    # overwrite a value and make sure it can be read
    bs = Bootscript(app)
    bs.set("10.0.0.1", "foo")
    assert bs.get("10.0.0.1") == "foo"
    bs.set("10.0.0.1", "bar")
    assert bs.get("10.0.0.1") == "bar"


def test_get():
    app = Bottle()
    # retrieve value after setting it
    bs = Bootscript(app)
    bs.set("10.0.0.1", "foo")
    assert bs.get("10.0.0.1") == "foo"

    with raises(BootscriptNotFound):
        bla = bs.get("20.21.22.23")


def test_extra():
    app = Bottle()
    # ensure a new object does not contain entries
    bs = Bootscript(app)
    assert len(bs.bootscript) == 0

    inval = "fooinval"
    with raises(BootscriptNotFound):
        inval = bs.get("10.0.0.1")
    assert inval == "fooinval"
