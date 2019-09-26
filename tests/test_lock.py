from bottle import Bottle
from pytest import raises
import time

from baremetal_support.lock import Host_Lock, HostNotLocked, HostAlreadyLocked


host0 = "10.0.0.1"
host1 = "10.0.0.2"


def test_my_timer():
    app = Bottle()
    locks = Host_Lock(app)

    assert not locks.is_locked(host0)
    locks.lock_host(host0, 6)
    assert locks.is_locked(host0)
    time.sleep(2)
    assert locks.is_locked(host0)
    time.sleep(9)
    print(locks.locks)
    assert not locks.is_locked(host0)


def test_is_locked():
    app = Bottle()
    locks = Host_Lock(app)

    assert not locks.is_locked(host0)
    assert not locks.is_locked(host1)

    locks.lock_host(host0)
    assert locks.is_locked(host0)
    assert locks.locks[host0]
    print(locks.locks[host0])
    assert not locks.is_locked(host1)

    locks.lock_host(host1)
    assert locks.is_locked(host0)
    assert locks.is_locked(host1)

    locks.unlock_host(host0)
    assert not locks.is_locked(host0)
    assert locks.is_locked(host1)

    locks.unlock_host(host1)
    assert not locks.is_locked(host0)
    assert not locks.is_locked(host1)


def test_lock_host():
    app = Bottle()
    locks = Host_Lock(app)
    locks.lock_host(host1)
    assert locks.locks[host1]


def test_unlock_host():
    app = Bottle()
    locks = Host_Lock(app)
    locks.lock_host(host1)
    assert locks.locks[host1]
    locks.unlock_host(host1)
    assert not locks.locks[host1]


def test_lock_already_locked():
    app = Bottle()
    locks = Host_Lock(app)

    assert not locks.is_locked(host0)
    locks.lock_host(host0)
    assert locks.is_locked(host0)

    with raises(HostAlreadyLocked):
        locks.lock_host(host0)

    locks.unlock_host(host0)
    locks.lock_host(host0)

    with raises(HostAlreadyLocked):
        locks.lock_host(host0)


def test_unlock_unlocked():
    app = Bottle()
    locks = Host_Lock(app)

    assert not locks.is_locked(host0)
    with raises(HostNotLocked):
        locks.unlock_host(host0)
