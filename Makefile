
init:
	pip install -r requirements.txt

test:
	pycodestyle server.py
	pycodestyle bootscript.py
	pycodestyle tests/*.py
	pytest --cov=ipxe_http .

.PHONY: init test
