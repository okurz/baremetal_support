
init:
	pip install -r requirements.txt

test:
	pycodestyle baremetal_support/baremetal_support.py
	pycodestyle baremetal_support/bootscript.py
	pycodestyle baremetal_support/lock.py
	pycodestyle baremetal_support/jobid.py
	pycodestyle tests/test_bootscript.py
	pycodestyle tests/test_host_lock.py
	pycodestyle tests/test_bootscript.py
	pycodestyle tests/test_jobid.py
	py.test --cov-report=term --cov=baremetal_support tests/

.PHONY: init test
