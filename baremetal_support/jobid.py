# Copyright (C) 2020 SUSE LLC
# SPDX-License-Identifier: GPL-3.0

import os
import bottle
import socket
from openqa_client.client import OpenQA_Client


class LatestJobNotFound(Exception):
    """Raised when no job is found"""
    pass


class LatestJob:
    def __init__(self, app, instance='http://openqa.suse.de'):
        route = '/v1/latest_job/<arch>/<distri>/<flavor>/<version>/<test>'
        self.bootscript = {}
        self._instance = instance
        self._app = app
        self._app.route(route,
                        method="GET",
                        callback=self.http_get_latest_job)

    def get_latest_job(self, filter):
        try:
            client = OpenQA_Client(server=self._instance)
            result = client.openqa_request('GET', 'jobs', filter)
            jobs = sorted(result['jobs'], key=lambda x: str(x['t_finished']))
            if jobs:
                return ([[job] for job in jobs if job['result']
                        in ['passed', 'softfailed']][-1][0])
            else:
                raise LatestJobNotFound("no such job found")
        except Exception:
            raise LatestJobNotFound("no such job found")

    def http_get_latest_job(self, arch, distri, flavor, version, test):
        filter = {}
        filter['arch'] = arch
        filter['distri'] = distri
        filter['flavor'] = flavor
        filter['version'] = version
        filter['test'] = test

        try:
            job = self.get_latest_job(filter)
            bottle.response.content_type = 'text/text; charset=utf-8'
            result = job['id']
            return str(result)
        except LatestJobNotFound:
            bottle.response.body = 'not found'
            bootle.respons.status = '404 Not Found'
