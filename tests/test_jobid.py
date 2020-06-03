# Copyright (C) 2019 SUSE LLC
# SPDX-License-Identifier: GPL-3.0

from bottle import Bottle
from pytest import raises, skip
import requests

from baremetal_support.jobid import LatestJob, LatestJobNotFound


def test_exception():
    instance = 'http://openqa.opensuse.org'
    try:
        reachable = requests.get(instance)
    except Exception:
        pytest.skip("instance unreachable")
        
    app = Bottle()
    lj = LatestJob(app, instance)

    filter = {}
    filter['arch'] = 'MIPS'
    filter['distri'] = 'gentoo'
    filter['flavor'] = 'hardened'
    filter['version'] = '1.0'
    filter['test'] = 'install_gentoo_mips'
    with raises(LatestJobNotFound):
        res = lj.get_latest_job(filter)

def test_get():
    instance = 'http://openqa.opensuse.org'
    try:
        reachable = requests.get(instance)
    except Exception:
        pytest.skip("instance unreachable")

    app = Bottle()
    lj = LatestJob(app, instance)
    filter = {}
    filter['arch'] = 'x86_64'
    filter['distri'] = 'opensuse'
    filter['flavor'] = 'DVD'
    filter['version'] = 'Tumbleweed'
    filter['test'] = 'create_hdd_textmode'

    res = lj.get_latest_job(filter)
    assert res
