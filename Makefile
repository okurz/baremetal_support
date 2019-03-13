
init:
	pip install -r requirements.txt

test:
	pytest --cov=ipxe_http ipxe_http 

.PHONY: init test
