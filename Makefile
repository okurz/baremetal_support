
init:
	pip install -r requirements.txt

test:
	pycodestyle ipxe_http.py
	pycodestyle bootscript.py
	pycodestyle tests/*.py
	pytest --cov=ipxe_http .

.PHONY: init test
