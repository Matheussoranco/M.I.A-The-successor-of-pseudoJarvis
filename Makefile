# Makefile for M.I.A - Multimodal Intelligent Assistant
# Provides automation for common development, testing, and deployment tasks

.PHONY: help install install-dev run test test-verbose test-coverage lint format clean docs security uninstall type-check build all-checks

# Default target
help:
	@echo "M.I.A - Multimodal Intelligent Assistant"
	@echo "========================================"
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "Installation:"
	@echo "  make install         - Install M.I.A and core dependencies"
	@echo "  make install-dev     - Install with development dependencies"
	@echo ""
	@echo "Running:"
	@echo "  make run             - Run M.I.A with default settings"
	@echo "  make run-debug       - Run M.I.A in debug mode"
	@echo ""
	@echo "Testing:"
	@echo "  make test            - Run tests"
	@echo "  make test-verbose    - Run tests with verbose output"
	@echo "  make test-coverage   - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint            - Run code linting"
	@echo "  make format          - Format code with black and isort"
	@echo "  make type-check      - Run type checking with mypy"
	@echo "  make security        - Run security checks"
	@echo "  make all-checks      - Run all quality checks"
	@echo ""
	@echo "Build & Deploy:"
	@echo "  make build           - Build package for distribution"
	@echo "  make docs            - Build documentation"
	@echo "  make docker-build    - Build Docker image"
	@echo "  make docker-run      - Run M.I.A in Docker"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean           - Clean cache and build files"
	@echo "  make uninstall       - Uninstall M.I.A"
	@echo "  make check-system    - Check system requirements"
	@echo ""
	@echo "Quick setup: make dev-setup"

# Installation
install:
	@echo "Installing M.I.A core dependencies..."
	pip install -r requirements-core.txt
	pip install -e .

install-dev: install
	@echo "Installing development dependencies..."
	pip install -r requirements.txt
	pip install pre-commit pytest-cov black isort flake8 mypy bandit
	pre-commit install

# Running
run:
	@echo "Starting M.I.A..."
	python main.py

run-debug:
	@echo "Starting M.I.A in debug mode..."
	python main.py --info

# Testing
test:
	@echo "Running tests..."
	python -m pytest tests/ -v --tb=short

test-verbose:
	@echo "Running tests with verbose output..."
	python -m pytest tests/ -v -s --tb=long

test-coverage:
	@echo "Running tests with coverage..."
	python -m pytest tests/ -v --cov=src/mia --cov-report=html --cov-report=term --cov-report=xml

# Code Quality
lint:
	@echo "Running linter..."
	flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203,W503

format:
	@echo "Formatting code..."
	black src/ tests/ --line-length=88
	isort src/ tests/ --profile black --line-length=88

type-check:
	@echo "Running type checker..."
	mypy src/ --ignore-missing-imports

security:
	@echo "Running security checks..."
	bandit -r src/ -f json -o bandit-report.json || true
	@echo "Security report saved to bandit-report.json"

all-checks: lint type-check security test-coverage
	@echo "✅ All quality checks completed!"

# Build & Deploy
build:
	@echo "Building package..."
	python -m build
	twine check dist/*

docs:
	@echo "Building documentation..."
	cd docs && make html

docker-build:
	@echo "Building Docker image..."
	docker build -t mia-assistant .

docker-run:
	@echo "Running M.I.A in Docker..."
	docker run -it --rm -v $(PWD)/.env:/app/.env mia-assistant

# Maintenance
clean:
	@echo "Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/
	rm -f bandit-report.json coverage.xml

uninstall:
	@echo "Uninstalling M.I.A..."
	pip uninstall mia-successor -y

# Quick development setup
dev-setup: install-dev
	@echo "Setting up development environment..."
	@echo ""
	@echo "✅ Development environment ready!"
	@echo "Next steps:"
	@echo "1. Edit config files as needed"
	@echo "2. Run 'make test' to verify installation"
	@echo "3. Run 'make run' to start M.I.A"

# CI/CD simulation
ci: install-dev all-checks
	@echo "✅ CI simulation completed successfully!"

# Check system requirements
check-system:
	@echo "Checking system requirements..."
	python -c "import sys; print(f'Python: {sys.version}')"
	python -c "from mia.utils.optional_deps import check_all_dependencies, get_missing_dependencies; deps = check_all_dependencies(); missing = get_missing_dependencies(); print(f'Available deps: {sum(deps.values())}/{len(deps)}'); print(f'Missing: {missing}') if missing else print('All optional dependencies available!')"
