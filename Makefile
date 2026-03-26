VENV_DIR := .venv
PYTHON    := $(VENV_DIR)/bin/python
PIP       := $(VENV_DIR)/bin/pip

venv:
	@echo "Creating virtual environment in $(VENV_DIR)..."
	@python3 -m venv $(VENV_DIR)
	@$(PIP) install --upgrade pip --quiet
	@$(PIP) install -r requirements.txt --quiet
	@echo "Done. Activate with: source $(VENV_DIR)/bin/activate"

install:
	@echo "Installing dependencies..."
	@pip install --upgrade pip
	@pip install -r requirements.txt
	@echo "Dependencies installed."

lint:
	@echo "Running linters..."
	@pylint run.py game/ tests/
	@echo "Linting completed."

format:
	@echo "Formatting code..."
	@black .
	@echo "Code formatted."

check-format:
	@echo "Checking code formatting..."
	@black --check --diff .
	@echo "Format check completed."

test:
	@echo "Running tests..."
	@pytest tests/
	@echo "Tests completed."

# Local: install, then format in-place, lint, and test.
all: install format lint test

# CI: install, check formatting without modifying, lint, and test.
ci: install check-format lint test
