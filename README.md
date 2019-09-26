# A HTTP server for dynamic iPXE boot control

## Running

Prior to doing anyting. some preparation is needed: 

```bash
 git clone https://github.com/frankenmichl/ipxe_http.git
 cd ipxe_http
 virtualenv virtualenv
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
  take the lock if possible. If the host is already locked, HTTP status 412 is
  returned
- PUT
  free the lock. If it is not locked, HTTP status 412 signals the error.
#### /v1/host_lock/lock_state/<addr>
- GET
  retrieve the lock status of <addr>. Returned in the body as _locked_ or
  _unlocked_
