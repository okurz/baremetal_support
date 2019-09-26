from bottle import Bottle, request, response
from threading import Lock, Timer


class HostAlreadyLocked(Exception):
    """Raised when a host should be locked but is already locked"""
    pass


class HostNotLocked(Exception):
    """host cannot be unlocked because it is not locked"""


class Host_Lock:
    def __init__(self, app):
        self.locks = {}
        self.timeouts = {}
        self.mutex = Lock()
        self._app = app

        self._app.route('/v1/host_lock/lock/<addr>',
                        method="GET",
                        callback=self.http_lock)
        self._app.route('/v1/host_lock/lock/<addr>/<timeout:int>',
                        method="GET",
                        callback=self.http_lock)
        self._app.route('/v1/host_lock/lock/<addr>',
                        method="PUT",
                        callback=self.http_unlock)
        self._app.route('/v1/host_lock/lock_state/<addr>',
                        method="GET",
                        callback=self.http_lock_state)

    def my_timer(self, host):
        self.unlock_host(host)

    def is_locked(self, host):
        self.mutex.acquire()
        try:
            ret = self.locks[host]
        except KeyError:
            ret = False
        finally:
            self.mutex.release()
        return ret

    def lock_host(self, host, timeout=0):
        self.mutex.acquire()

        if host not in self.locks:
            self.locks[host] = True
        elif not self.locks[host]:
            self.locks[host] = True
        else:
            self.mutex.release()
            raise HostAlreadyLocked("Host is already locked")

        if timeout > 0:
            self.timeouts[host] = Timer(timeout, self.my_timer, [host])
            self.timeouts[host].start()

        self.mutex.release()

    def unlock_host(self, host):
        self.mutex.acquire()

        if host in self.locks and self.locks[host]:
            self.locks[host] = False
            if host in self.timeouts:
                self.timeouts[host].cancel()
                del self.timeouts[host]
        else:
            self.mutex.release()
            raise HostNotLocked("Host is not locked")

        self.mutex.release()

    def http_lock(self, addr, timeout=0):
        response.content_type = 'text/text; charset=utf-8'
        try:
            self.lock_host(addr, timeout)
            response.status = 200
            response.body = "ok"
            return response
        except HostAlreadyLocked:
            response.status = 412

    def http_unlock(self, addr):
        response.content_type = 'text/text; charset=utf-8'
        try:
            self.unlock_host(addr)
            response.body = "ok"
        except HostNotLocked:
            response.status = 412
        return response

    def http_lock_state(self, addr):
        response.content_type = 'text/text; charset=utf-8'
        response.status = 200
        if self.is_locked(addr):
            response.body = "locked"
        else:
            response.body = "unlocked"

        return response
