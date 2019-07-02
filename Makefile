setup:
	python3 -m pip install --user --upgrade setuptools wheel
	python3 -m pip install --user zest.releaser[recommended]

	@if [ ! -f ~/.pypirc ]; then \
		echo "~/.pypirc doesn't exist; create one using the instructions at https://zestreleaser.readthedocs.io/en/latest/uploading.html"; \
	fi
	# Commands available under zest.releaser -- prerelease, release, etc. -- are
	# documented at https://zestreleaser.readthedocs.io/en/latest/overview.html

install-editable:
	pip install -e .

test:
	python3 setup.py test
