.PHONY: clean run install debug lint lint-strict all

MAP_FILE = maps/easy/02_simple_fork.txt
VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

# Marker file so Make knows the venv is built and can skip rebuilding it
$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install mypy flake8 typing arcade

install: $(VENV)/bin/activate

# Clean temp files, caches, and the venv itself
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	rm -rf $(VENV)

all: clean install

# Executes main script (builds venv first if missing)
run: $(VENV)/bin/activate
	$(PYTHON) main.py $(MAP_FILE)

# Run main script in debug mode
debug: $(VENV)/bin/activate
	$(PYTHON) -m pdb main.py $(MAP_FILE)

# Static type checking with mypy
lint: $(VENV)/bin/activate
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: $(VENV)/bin/activate
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --strict