# A support service for baremetal testing 
[![Build Status](https://travis-ci.com/frankenmichl/baremetal_support.svg?branch=master)](https://travis-ci.com/frankenmichl/baremetal_support)
[![codecov](https://codecov.io/gh/frankenmichl/baremetal_support/branch/master/graph/badge.svg)](https://codecov.io/gh/frankenmichl/baremetal_support)

While this is designed to work with openQA, this service has not dependencies
to openQA. However, it may be of limited use without being used with an openQA
instance.

## Running

Prior to doing anyting. some preparation is needed: 

```bash
 git clone https://github.com/frankenmichl/baremetal_support.git
 cd baremetal_support
 python3 -m venv venv
 . venv/bin/activate
 make init
```

To start the server, just run ```pythin server.py```.
Hit C-c to exit.

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
