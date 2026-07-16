# Copyright (C) 2019-2021 SUSE LLC
# SPDX-License-Identifier: GPL-3.0

from bottle import Bottle
import bottle
from pytest import raises
import time

from baremetal_support.lock import Host_Lock, HostAlreadyLocked, HostNotLocked, NotLockOwner
from baremetal_support.logging import Logging

host0 = "10.0.0.1"
host1 = "10.0.0.2"

logger = Logging("baremetal support", "DEBUG")


def test_my_timer():
    app = Bottle()
    locks = Host_Lock(app, logger)

    assert not locks.is_locked(host0)
    token = locks.lock_host(host0, 6)
    assert locks.is_locked(host0)
    assert token != ""
    time.sleep(2)
    assert locks.is_locked(host0)
    time.sleep(9)
    print(locks.locks)
    assert not locks.is_locked(host0)


def test_is_locked():
    app = Bottle()
    locks = Host_Lock(app, logger)

    assert not locks.is_locked(host0)
    assert not locks.is_locked(host1)

    token = locks.lock_host(host0)
    assert locks.is_locked(host0)
    assert locks.locks[host0]
    print(locks.locks[host0])
    assert not locks.is_locked(host1)

    token2 = locks.lock_host(host1)
    assert locks.is_locked(host0)
    assert locks.is_locked(host1)

    locks.unlock_host(host0, token)
    assert not locks.is_locked(host0)
    assert locks.is_locked(host1)

    locks.unlock_host(host1, token2)
    assert not locks.is_locked(host0)
    assert not locks.is_locked(host1)


def test_lock_host():
    app = Bottle()
    locks = Host_Lock(app, logger)
    locks.lock_host(host1)
    assert locks.locks[host1]


def test_unlock_host():
    app = Bottle()
    locks = Host_Lock(app, logger)
    token = locks.lock_host(host1)
    assert locks.locks[host1]
    locks.unlock_host(host1, token)
    assert not locks.locks[host1]


def test_lock_already_locked():
    app = Bottle()
    locks = Host_Lock(app, logger)

    assert not locks.is_locked(host0)
    token = locks.lock_host(host0)
    assert locks.is_locked(host0)

    with raises(HostAlreadyLocked):
        locks.lock_host(host0)

    locks.unlock_host(host0, token)
    locks.lock_host(host0)

    with raises(HostAlreadyLocked):
        locks.lock_host(host0)


def test_unlock_unlocked():
    app = Bottle()
    locks = Host_Lock(app, logger)

    assert not locks.is_locked(host0)
    with raises(HostNotLocked):
        locks.unlock_host(host0, "")


def test_not_lock_owner():
    app = Bottle()
    locks = Host_Lock(app, logger)
    locks.lock_host(host0)
    with raises(NotLockOwner):
        locks.unlock_host(host0, "wrong_token")


def test_http_lock_success():
    app = Bottle()
    locks = Host_Lock(app, logger)
    res = locks.http_lock(host0)
    assert "200" in res.status
    assert len(res.body) > 0


def test_http_lock_already_locked():
    app = Bottle()
    locks = Host_Lock(app, logger)
    locks.lock_host(host0)
    locks.http_lock(host0)
    assert "412" in bottle.response.status


def test_http_unlock_success():
    app = Bottle()
    locks = Host_Lock(app, logger)
    token = locks.lock_host(host0)
    res = locks.http_unlock(host0, token)
    assert res.body == "ok"


def test_http_unlock_not_locked():
    app = Bottle()
    locks = Host_Lock(app, logger)
    res = locks.http_unlock(host0, "some_token")
    assert "412" in res.status
    assert res.body == "the host is not locked"


def test_http_unlock_not_owner():
    app = Bottle()
    locks = Host_Lock(app, logger)
    locks.lock_host(host0)
    res = locks.http_unlock(host0, "wrong_token")
    assert "403" in res.status
    assert res.body == "you are not the owner of the lock"


def test_http_lock_state():
    app = Bottle()
    locks = Host_Lock(app, logger)
    res = locks.http_lock_state(host0)
    assert res.body == "unlocked"
    locks.lock_host(host0)
    res = locks.http_lock_state(host0)
    assert res.body == "locked"
