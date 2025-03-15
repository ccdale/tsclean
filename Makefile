# Description: Makefile for managing Python projects with Poetry.
# Author: https://github.com/hackersandslackers
# License: MIT
PROJECT_NAME := $(shell basename $CURDIR)
VIRTUAL_ENV := $(CURDIR)/.venv
LOCAL_PYTHON := $(VIRTUAL_ENV)/bin/python3

define HELP
Manage $(PROJECT_NAME). Usage:

make run        - Run $(PROJECT_NAME) locally.
make install    - Create local virtualenv & install dependencies.
make deploy     - Set up project & run locally.
make update     - Update dependencies via Poetry and output resulting `requirements.txt`.
make pipeline   - Run code formatter & linter without making changes
make format     - Run Python code formatter & sort dependencies.
make lint       - Check code formatting with flake8.
make clean      - Remove extraneous compiled files, caches, logs, etc.
make test       - Run tests with pytest.
make cov 	    - Run tests with coverage.

endef
export HELP


.PHONY: run install deploy update pipeline format lint clean help test

all help:
	@echo "$$HELP"

env: $(VIRTUAL_ENV)

$(VIRTUAL_ENV):
	if [ ! -d $(VIRTUAL_ENV) ]; then \
		echo "Creating Python virtual env in \`${VIRTUAL_ENV}\`"; \
		python3 -m venv $(VIRTUAL_ENV); \
	fi
	poetry config virtualenvs.path $(VIRTUAL_ENV)

.PHONY: run
run: env
	  $(LOCAL_PYTHON) -m main

.PHONY: install
install: env
	$(shell . $(VIRTUAL_ENV)/bin/activate)
	$(LOCAL_PYTHON) -m pip install --upgrade pip setuptools wheel && \
	poetry install --with dev --sync
	echo Installed dependencies in \`${VIRTUAL_ENV}\`;

.PHONY: deploy
deploy:
	make install && \
	make run

.PHONY: update
update: env
	$(LOCAL_PYTHON) -m pip install --upgrade pip setuptools wheel && \
	poetry update --with dev && \
	poetry export -f requirements.txt --output requirements.txt --without-hashes && \
	echo Installed dependencies in \`${VIRTUAL_ENV}\`;

.PHONY: pipeline
pipeline: env lint
	$(LOCAL_PYTHON) -m isort --multi-line=3 --check . && \
	$(LOCAL_PYTHON) -m black . --check --quiet

.PHONY: format
format: env
	$(LOCAL_PYTHON) -m isort --multi-line=3 . && \
	$(LOCAL_PYTHON) -m black .

.PHONY: lint
lint: env
	$(LOCAL_PYTHON) -m flake8 . --count \
			--select=E9,F63,F7,F82 \
			--exclude .git,.github,__pycache__,.pytest_cache,.venv,logs,creds,.venv,docs,logs,.reports \
			--show-source \
			--statistics

.PHONY: clean
clean:
	find . -name 'poetry.lock' -delete && \
	find . -name '.coverage' -delete && \
	find . -name '.Pipfile.lock' -delete && \
	find . -wholename '**/*.pyc' -delete && \
	find . -type d -wholename '__pycache__' -exec rm -rf {} + && \
	find . -type d -wholename './.venv' -exec rm -rf {} + && \
	find . -type d -wholename '.pytest_cache' -exec rm -rf {} + && \
	find . -type d -wholename '**/.pytest_cache' -exec rm -rf {} + && \
	find . -type d -wholename './logs/*.log' -exec rm -rf {} + && \
	find . -type d -wholename './.reports/*' -exec rm -rf {} +

.PHONY: test
test: env
	$(LOCAL_PYTHON) -m pytest

.PHONY: cov
cov: env
	$(LOCAL_PYTHON) -m pytest -v --cov=main --cov-report=term-missing --cov-report=html
