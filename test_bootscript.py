import pytest
from .bootscript import Bootscript, BootscriptNotFound


def test_bootscript_set():
    """ test if the key is present after setting the value"""
    bs = Bootscript()
    bs.set("10.0.0.1", "foo")
    assert "10.0.0.1" in bs.bootscript


def test_bootscript_get():
    """ retrieve value after setting it """
    bs = Bootscript()
    bs.set("10.0.0.1", "foo")
    assert bs.get("10.0.0.1") == "foo"


def test_bootscript_overwrite():
    """ overwrite a value and make sure it can be read """
    bs = Bootscript()
    bs.set("10.0.0.1", "foo")
    assert bs.get("10.0.0.1") == "foo"
    bs.set("10.0.0.1", "bar")
    assert bs.get("10.0.0.1") == "bar"


def test_new_bootscript():
    """ ensure a new object does not contain entries """
    bs = Bootscript()
    assert len(bs.bootscript) == 0


def test_exception():
    """ ensure the proper BootscriptNotFound is raised """
    bs = Bootscript()
    with pytest.raises(BootscriptNotFound):
        inval = bs.get("10.0.0.1")
