install-editable:
	pip install -e .

test:
	python setup.py test

# release:
# 	python setup.py sdist bdist_wheel
# 	twine upload dist/*
