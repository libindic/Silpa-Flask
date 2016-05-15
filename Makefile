travis:
	python setup.py testr --coverage \
		--testr-args="--parallel --concurrency=2"
	flake8 silpa

clean:
	find . -name "*.pyc" -exec rm -vf {} \;
	find -name __pycache__ -delete
	find . -name "*~" -exec rm -vf {} \;

tox:
	tox

flake:
	flake8 silpa
