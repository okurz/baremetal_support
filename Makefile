
init:
	pip install -r requirements.txt

test:
	pytest --cov=ipxe_http tests/

.PHONY: init test
