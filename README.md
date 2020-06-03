# A support service for baremetal testing 
[![Build Status](https://travis-ci.com/frankenmichl/baremetal_support.svg?branch=master)](https://travis-ci.com/frankenmichl/baremetal_support)
[![codecov](https://codecov.io/gh/frankenmichl/baremetal_support/branch/master/graph/badge.svg)](https://codecov.io/gh/frankenmichl/baremetal_support)

## Running

Prior to doing anyting. some preparation is needed: 

```bash
 git clone https://github.com/frankenmichl/baremetal_support.git
 cd baremetal_support
 python3 -m venv venv
 . venv/bin/activate
 make init
```

To get some usage instructions, just run:  
```
# ./baremetal_support.py --help
usage: baremetal_support.py [-h] [-l LISTEN] [-p PORT] [-i INSTANCE]

optional arguments:
  -h, --help            show this help message and exit
  -l LISTEN, --listen LISTEN
                        hostname to listen on - defaults to all
  -p PORT, --port PORT  specify listening port - defaults to 8080
  -i INSTANCE, --instance INSTANCE
                        specify openQA instance - defaults to http://openqa.suse.de
```

You can also use the included systemd service file baremetal_support.service
or retrieve a package from https://build.opensuse.org/project/show/home:MMoese:baremetal_support

## Running the tests

Running the unit tests is easy.
```
make test
```
You get a coverage report, this should show 100% coverage.
If you want to see more information, just run
```
coverage html
```
and open the report in your browser.

## API Documentation
All parameters in this documentation are surrounded by <>.

### Bootscript related API
#### /v1/bootscript/script.ipxe 
- GET
  Returns the bootscript for the host issuing the GET request

#### /v1/bootscript/script.ipxe/<addr> 
- GET
  Return the bootscript for the host with IP address <addr>
- POST
  set the bootscript for the host with IP address <addr>

### Lock related API
#### /v1/host_lock/lock/<addr>
- GET
  take the lock if possible and return a token in the response body.
  If the host is already locked, HTTP status 412 is returned. 
#### /v1/host_lock/lock/<addr>/<token>
- PUT
  token is retrieved when locking, this needs to be passed to the unlock.
  free the lock. If it is not locked, HTTP status 412 signals the error.
#### /v1/host_lock/lock_state/<addr>
- GET
  retrieve the lock status of <addr>. Returned in the body as _locked_ or
  _unlocked_

### Job-ID related API
#### v1/latest_job/<arch>/<distri>/<flavor>/<version>/<test>
- GET
  retrieve the latest jobid from the connected openQA-instance in the request
  body. All variables are mandatory here.
  Example:  
    v1/latest_job/x86_64/sle/Online/15-SP2/create_hdd_minimal_base+sdk 
  On error, HTTP status 404 is returned.

