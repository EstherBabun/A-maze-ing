# File: Makefile
# Author: ebabun <ebabun@student.42belgium.be>
# Author: mmeurer <mmeurer@student.42belgium.be>
# Created: 2026/01/21 17:49:10
# Updated: 2026/01/20 16:09:10

PYTHON := python3
VERSION := $(shell $(PYTHON) -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
VENV := venv
PYTHON_VENV := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
MAIN := a_maze_ing.py

GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m

# flexible config name use make run CONFIG=your_config.txt
CONFIG ?= config.txt

help:
	@echo "Available commands:"
	@echo "  install              Create venv and install dependencies"
	@echo "  run                  Run the program with config.txt"
	@echo "  run CONFIG=file.txt  Run the program with custom config file"
	@echo "  default              Run without config file (default settings)"
	@echo "  build                Build the maze generation package"
	@echo "  debug                Run with debugger"
	@echo "  lint                 Run norm and type checks"
	@echo "  lint-strict          Run strict norm and type checks"
	@echo "  clean                Remove cache files"
	@echo "  clean-build          Remove built package"
	@echo "  fclean               Full clean (remove caches, packages, venv)"
	@echo "  help                 Show this help message" 

install:
	@$(PYTHON) -c 'import sys; v=sys.version_info; print(f"Python {v.major}.{v.minor}"); exit(0 if (v.major, v.minor) >= (3, 10) else 1)' || \
		(echo "Error: Python 3.10+ required" && exit 1)
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	unzip mlx-2.2-py3-ubuntu-any.whl -d venv/lib/python$(VERSION)/site-packages/
	@printf "$(GREEN)Setup successfully completed$(NC) ✨\n"

run:
	$(PYTHON_VENV) $(MAIN) $(CONFIG)

default:
	$(PYTHON_VENV) $(MAIN)

build:
	$(PYTHON_VENV) -m build
	@mv dist/* .
	@rm -rf dist/
	@rm -rf mazegen.egg-info

debug:
	$(PYTHON_VENV) -m pdb $(MAIN) $(CONFIG)

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

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@printf "$(YELLOW)cache files removed$(NC) 🧹\n"

clean-build:
	@rm -f mazegen-*
	@printf "$(YELLOW)Package removed$(NC) 🧹\n"

fclean: clean clean-build
	@rm -rf venv/
	@printf "$(YELLOW)Virtual environement removed$(NC) 🧹\n"
	

.PHONY: help install run default build debug lint lint-strict clean clean-build fclean
