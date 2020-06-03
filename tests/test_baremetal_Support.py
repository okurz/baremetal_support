# Copyright (C) 2019 SUSE LLC
# SPDX-License-Identifier: GPL-3.0
import sys

import pytest
import requests
import socket

import signal
import pytest_cov.embed

from multiprocessing import Process
from time import sleep

from baremetal_support.baremetal_support import Baremetal_Support


def cleanup(*_):
    pytest_cov.embed.cleanup()
    sys.exit(1)


def server_task(arg):
    arg.start()


def test_baremetal_support():
    hostname = 'localhost'
    port = '23456'
    instance = "http://openqa.opensuse.org"

    url = 'http://' + hostname + ':' + port + '/v1/'
    use_ip = '10.0.0.1'

    url_bootscript = url + 'bootscript/script.ipxe/' + use_ip
    url_localhost = url + 'bootscript/script.ipxe/' + '127.0.0.1'
    url_get = url + 'bootscript/script.ipxe'

    err_url = url + 'bootscript/script.ipxe/foobar'
    err_url2 = url + 'bootscript/script.ipxe/31.32.33.34'

    url_status = url + 'host_lock/lock_state/' + use_ip
    url_lock = url + 'host_lock/lock/' + use_ip
    url_lock_timeout = url + 'host_lock/lock/' + use_ip + '/10'
    url_unlock = url + 'host_lock/lock/' + use_ip

    url_jobid_good = url + 'latest_job/x86_64/opensuse/DVD/Tumbleweed/create_hdd_textmode'
    url_jobid_bad = url + 'latest_job/MIPS/Gentoo/hardened/1.0/install_foobar'

    text = "data foo bar"

    server = Baremetal_Support(hostname, port, instance)
    signal.signal(signal.SIGTERM, cleanup)
    assert isinstance(server, Baremetal_Support)
    p = Process(target=server_task, args=(server,))
    p.start()
    sleep(1)

    with pytest.raises(socket.error):
        inval = server._bootscript._to_ip("foobar")

    # request bootscript api
    r1 = requests.post(err_url, data='illegal')
    assert r1.status_code == 400

    r2 = requests.get(err_url)
    assert r2.status_code == 400

    r3 = requests.get(err_url2)
    assert r3.status_code == 404
    assert r3.text == 'not found'

    r4 = requests.get(url_get)
    assert r4.status_code == 404

    r5 = requests.post(url_bootscript, data="my_bootscript")
    assert r5.status_code == 200

    r6 = requests.get(url_bootscript)
    assert r6.status_code == 200
    assert r6.text == "my_bootscript"

    r7 = requests.post(url_localhost, data=text)
    assert r7.status_code == 200

    r8 = requests.get(url_localhost)
    assert r8.status_code == 200

    # test locking API
    r9 = requests.get(url_status)
    assert r9.status_code == 200
    assert r9.text == 'unlocked'

    r10 = requests.get(url_lock)
    assert r10.status_code == 200
    token = r10.text

    r11 = requests.get(url_status)
    assert r11.status_code == 200
    assert r11.text == 'locked'

    url_unlock2 = url_unlock + '/' + token
    r12 = requests.put(url_unlock2)
    assert r12.status_code == 200
    assert r12.text == 'ok'

    r13 = requests.get(url_status)
    assert r13.status_code == 200
    assert r13.text == 'unlocked'

    print(url_lock_timeout)
    r14 = requests.get(url_lock_timeout)
    assert r14.status_code == 200
    assert r14.text != ''

    r15 = requests.get(url_status)
    assert r15.status_code == 200
    assert r15.text == 'locked'

    sleep(15)

    r16 = requests.get(url_status)
    assert r16.status_code == 200
    assert r16.text == 'unlocked'

    r17 = requests.get(url_lock)
    assert r17.status_code == 200
    token = r17.text

    r18 = requests.get(url_lock)
    assert r18.status_code == 412

    r19 = requests.put(url_unlock + '/0xdeadbeefcafebabe')
    assert r19.status_code == 403

    url_unlock3 = url_unlock + '/' + token
    r20 = requests.put(url_unlock3)
    assert r20.status_code == 200
    assert r20.text == 'ok'

    r21 = requests.get(url_status)
    assert r21.status_code == 200
    assert r21.text == 'unlocked'

    r22 = requests.put(url_unlock3)
    assert r22.status_code == 412

    # tests for jobid.py
    try:
        reachable = requests.get(instance)
        r23 = requests.get(url_jobid_good)
        assert r23.status_code == 200
        assert r23.text != ""

        r24 = requests.get(url_jobid_bad)
        assert r24.status_code != 200
    except Exception:
        pytest.skip("instance unreachable")

    p.terminate()
    p.join()

