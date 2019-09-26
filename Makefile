
init:
	pip install -r requirements.txt

test:
	pycodestyle baremetal_support.py
	pycodestyle bootscript.py
	pycodestyle lock.py
	pycodestyle tests/test_bootscript.py
	pycodestyle tests/test_lock.py
	pycodestyle tests/test_bootscript.py
	py.test --cov-report term-missing --cov=baremetal_support tests/

.PHONY: init test
