# Copyright (C) 2019 SUSE LLC
# SPDX-License-Identifier: GPL-3.0

from bottle import request, response
import uuid
from threading import Lock, Timer


class HostAlreadyLocked(Exception):
    """Raised when a host should be locked but is already locked"""
    pass


class HostNotLocked(Exception):
    """host cannot be unlocked because it is not locked"""


class NotLockOwner(Exception):
    """host is locked by someone else"""


class Host_Lock:
    def __init__(self, app, logger):
        self.locks = {}
        self.timeouts = {}
        self.mutex = Lock()
        self._app = app
        self.log = logger

        self._app.route('/v1/host_lock/lock/<addr>',
                        method="GET",
                        callback=self.http_lock)
        self._app.route('/v1/host_lock/lock/<addr>/<timeout:int>',
                        method="GET",
                        callback=self.http_lock)
        self._app.route('/v1/host_lock/lock/<addr>/<token>',
                        method="PUT",
                        callback=self.http_unlock)
        self._app.route('/v1/host_lock/lock_state/<addr>',
                        method="GET",
                        callback=self.http_lock_state)

    def my_timer(self, host):
        self.log.warn("Timer expired, unlocking " + host)
        self.unlock_host(host, '', True)

    def is_locked(self, host):
        self.mutex.acquire()

        try:
            if self.locks[host] != '':
                ret = True
                self.log.info("Host " + host + " is locked")
            else:
                ret = False
                self.log.info("Host " + host + " is not locked")
        except KeyError:
            self.log.info("Host " + host + " is locked")
            ret = False
        finally:
            self.mutex.release()
        return ret

    def lock_host(self, host, timeout=0):
        self.mutex.acquire()

        token = ''

        if host not in self.locks or self.locks[host] == '':
            token = uuid.uuid4().hex
            self.locks[host] = token
            self.log.info("lock_host: Locking host " + host
                          + " with token " + token)
        else:
            self.mutex.release()
            self.log.info("lock_host: Host " + host + "is already locked")
            raise HostAlreadyLocked("Host is already locked")

        if timeout > 0:
            self.log.info("lock_host: setting lock timeout for " + host
                          + " to " + str(timeout))
            self.timeouts[host] = Timer(timeout, self.my_timer, [host])
            self.timeouts[host].start()

        self.mutex.release()
        return token

    def unlock_host(self, host, token, force=False):
        if not self.is_locked(host):
            self.log.error("unlock_host: Host " + host + " is not locked")
            raise HostNotLocked("Host is not locked")

        self.mutex.acquire()

        if force or self.locks[host] == token:
            self.locks[host] = ''
            self.log.info("unlock_host: unlocking " + host)
            if host in self.timeouts:
                self.timeouts[host].cancel()
                del self.timeouts[host]
                self.log.info("unlock_host: cancelling timer for " + host)
        else:
            self.mutex.release()
            self.log.error("unlock_host: Host " + host + " is already locked")
            raise NotLockOwner("host is locked by another host")

        self.mutex.release()

    def http_lock(self, addr, timeout=0):
        response.content_type = 'text/text; charset=utf-8'
        try:
            token = self.lock_host(addr, timeout)
            response.status = 200
            response.body = token
            return response
        except HostAlreadyLocked:
            response.status = 412

    def http_unlock(self, addr, token):
        response.content_type = 'text/text; charset=utf-8'
        try:
            self.unlock_host(addr, token, False)
            response.body = "ok"
        except HostNotLocked:
            response.status = 412
            response.body = "the host is not locked"
        except NotLockOwner:
            response.status = 403
            response.body = "you are not the owner of the lock"
        return response

    def http_lock_state(self, addr):
        response.content_type = 'text/text; charset=utf-8'
        response.status = 200
        if self.is_locked(addr):
            response.body = "locked"
        else:
            response.body = "unlocked"

        return response
