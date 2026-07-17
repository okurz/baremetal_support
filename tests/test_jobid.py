# Copyright (C) 2020-2021 SUSE LLC
# SPDX-License-Identifier: GPL-3.0

from bottle import Bottle
import bottle
from unittest.mock import patch, MagicMock
from pytest import raises

from baremetal_support.jobid import LatestJob, LatestJobNotFound
from baremetal_support.logging import Logging

logger = Logging("baremetal support", "DEBUG")


def test_exception_mocked():
    app = Bottle()
    lj = LatestJob(app, logger, "http://mock-openqa")

    mock_client_inst = MagicMock()
    mock_client_inst.openqa_request.return_value = {"jobs": []}

    with patch("baremetal_support.jobid.OpenQA_Client", return_value=mock_client_inst):
        with raises(LatestJobNotFound):
            _ = lj.get_latest_job({"arch": "MIPS"})


def test_get_mocked():
    app = Bottle()
    lj = LatestJob(app, logger, "http://mock-openqa")

    mock_client_inst = MagicMock()
    mock_client_inst.openqa_request.return_value = {
        "jobs": [
            {"id": 1, "t_finished": 100, "result": "passed"},
            {"id": 2, "t_finished": 200, "result": "failed"},
            {"id": 3, "t_finished": 300, "result": "softfailed"},
        ]
    }

    with patch("baremetal_support.jobid.OpenQA_Client", return_value=mock_client_inst):
        res = lj.get_latest_job({"arch": "x86_64"})
        assert res["id"] == 3


def test_get_mocked_no_passed_jobs():
    app = Bottle()
    lj = LatestJob(app, logger, "http://mock-openqa")

    mock_client_inst = MagicMock()
    # If all jobs are failed/unpassed, it should raise LatestJobNotFound due to index out of bounds
    mock_client_inst.openqa_request.return_value = {
        "jobs": [
            {"id": 1, "t_finished": 100, "result": "failed"},
        ]
    }

    with patch("baremetal_support.jobid.OpenQA_Client", return_value=mock_client_inst):
        with raises(LatestJobNotFound):
            _ = lj.get_latest_job({"arch": "x86_64"})


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
