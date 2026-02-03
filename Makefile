#!/usr/bin/env python3
# File: Makefile
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/21 17:49:10
# Updated: 2026/01/20 16:09:10

PYTHON := python3
VENV := venv
PYTHON_VENV := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip

SRC := a_maze_ing.py
CONFIG := config.txt

run:
	$(PYTHON_VENV) $(SRC) $(CONFIG)

default:
	$(PYTHON_VENV) $(SRC)

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	unzip mlx-2.2-py3-ubuntu-any.whl -d venv/lib/python3.10/site-packages/

debug:
	$(PYTHON_VENV) -m pdb $(MAIN)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

lint:
	$(PYTHON_VENV) -m flake8 . --exclude $(VENV) ; \
	$(PYTHON_VENV) -m mypy . --exclude $(VENV) \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(PYTHON_VENV) -m flake8 . --exclude $(VENV) ; \
	$(PYTHON_VENV) -m mypy . --strict --exclude $(VENV)

.PHONY: install run debug clean lint lint-strict