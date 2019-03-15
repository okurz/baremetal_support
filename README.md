# A HTTP server for dynamic iPXE boot control


## Running

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
