install:
	@echo "Installing dependencies..."
	@pip install --upgrade pip	# Upgrade pip to the latest version
	@pip install -r requirements.txt	# Install Python dependencies
	@echo "Dependencies installed."

lint:
	@echo "Running linters..."
	@pylint **.py	# Run pylint on the project
	@echo "Linting completed."

format:
	@echo "Formatting code..."
	@black .	# Format code using black
	@echo "Code formatted."

test:
	@echo "Running tests..."
	@pytest	# Run tests using pytest
	@echo "Tests completed."

all: install lint format test	# Run all tasks in order