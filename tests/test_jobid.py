# Copyright (C) 2020-2021 SUSE LLC
# SPDX-License-Identifier: GPL-3.0

from bottle import Bottle
import bottle
from unittest.mock import patch
import pytest
from pytest import raises
import requests

from baremetal_support.jobid import LatestJob, LatestJobNotFound
from baremetal_support.logging import Logging

logger = Logging("baremetal support", "DEBUG")


def test_exception():
    instance = "http://openqa.opensuse.org"
    try:
        _ = requests.get(instance)
    except Exception:
        pytest.skip("instance unreachable")

    app = Bottle()
    lj = LatestJob(app, logger, instance)

    filter = {}
    filter["arch"] = "MIPS"
    filter["distri"] = "gentoo"
    filter["flavor"] = "hardened"
    filter["version"] = "1.0"
    filter["test"] = "install_gentoo_mips"
    with raises(LatestJobNotFound):
        _ = lj.get_latest_job(filter)


def test_get():
    instance = "http://openqa.opensuse.org"
    try:
        _ = requests.get(instance)
    except Exception:
        pytest.skip("instance unreachable")

    app = Bottle()
    lj = LatestJob(app, logger, instance)
    filter = {}
    filter["arch"] = "x86_64"
    filter["distri"] = "opensuse"
    filter["flavor"] = "DVD"
    filter["version"] = "Tumbleweed"
    filter["test"] = "create_hdd_textmode"

    res = lj.get_latest_job(filter)
    assert res


def test_http_get_latest_job_success():
    app = Bottle()
    lj = LatestJob(app, logger)
    with patch.object(lj, "get_latest_job", return_value={"id": "12345"}):
        res = lj.http_get_latest_job("x86_64", "opensuse", "DVD", "Tumbleweed", "create_hdd_textmode")
        assert res == "12345"
        assert bottle.response.content_type == "text/text; charset=utf-8"


def test_http_get_latest_job_not_found():
    app = Bottle()
    lj = LatestJob(app, logger)
    with patch.object(lj, "get_latest_job", side_effect=LatestJobNotFound("no such job found")):
        lj.http_get_latest_job("x86_64", "opensuse", "DVD", "Tumbleweed", "create_hdd_textmode")
        assert bottle.response.status == "404 Not Found"
