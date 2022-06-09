SHELL   := /bin/bash
PYTHON  ?= python3

export PYTHONWARNINGS := default

.PHONY: all install test cleanup

all:

install:
	$(PYTHON) -mpip install -e .

test:
	$(PYTHON) nametag --doctest --verbose

cleanup:
	find -name '*~' -delete -print
	rm -fr __pycache__/
	rm -fr build/ dist/ nametag.egg-info/
	rm -fr .coverage htmlcov/

.PHONY: _package _publish

_package:
	$(PYTHON) setup.py sdist bdist_wheel
	twine check dist/*

_publish: cleanup _package
	read -r -p "Are you sure? "; \
	[[ "$$REPLY" == [Yy]* ]] && twine upload dist/*
