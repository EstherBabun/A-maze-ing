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
MAIN := a_maze_ing.py

# flexible config name use make run CONFIG=your_config.txt
CONFIG ?= config.txt

run:
	$(PYTHON_VENV) $(MAIN) $(CONFIG)

# run program without config file (using default settings)
default:
	$(PYTHON_VENV) $(MAIN)

# check user's python3 version and print error if it's < 3.10
install:
	@$(PYTHON) -c 'import sys; v=sys.version_info; print(f"Python {v.major}.{v.minor}"); exit(0 if (v.major, v.minor) >= (3, 10) else 1)' || \
		(echo "Error: Python 3.10+ required" && exit 1)
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	unzip mlx-2.2-py3-ubuntu-any.whl -d venv/lib/python3.10/site-packages/

debug:
	$(PYTHON_VENV) -m pdb $(MAIN) $(CONFIG)

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@echo "✨ cache files removed 🧹"

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
