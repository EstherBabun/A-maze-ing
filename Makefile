#!/usr/bin/env python3
# File: Makefile
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/21 17:49:10
# Updated: 2026/01/20 16:09:10

PYTHON := python3
VENV := venv
PYTHON_VENV := $(VENV)/bin/python

SRC := a_maze_ing.py
CONFIG := config.txt
AFFICHAGE := maze_renderer.py

venv:
	python3 -m venv venv
	$(PYTHON) install -r requirements.txt

run:
	$(PYTHON) $(SRC) $(CONFIG)

play:
	$(PYTHON) $(AFFICHAGE)

debug:
	$(PYTHON_VENV) -m pdb $(MAIN)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

lint:
	$(PYTHON_VENV) -m flake8 .
	$(PYTHON_VENV) -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(PYTHON_VENV) -m flake8 .
	$(PYTHON_VENV) -m mypy . --strict

.PHONY: install run debug clean lint lint-strict