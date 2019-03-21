
init:
	pip install -r requirements.txt

test:
	pycodestyle ipxe_http.py
	pycodestyle bootscript.py
	pycodestyle test_ipxe_http.py
	pycodestyle test_bootscript.py
	py.test --cov=ipxe_http .

.PHONY: init test
