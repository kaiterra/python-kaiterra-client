install-editable:
	pip install -e .

test:
	kaiterra/tests/test_sensors.py
	kaiterra/tests/online_tests/test_sensors.py

release:
	python setup.py sdist bdist_wheel
	twine upload dist/*
