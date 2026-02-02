# Jerry Framework Makefile
# Primary entry point for development setup and common tasks
#
# First-time setup: make setup
# This MUST be run after cloning or creating a worktree.

.PHONY: setup install sync test lint format check clean help

# Default target - show help
.DEFAULT_GOAL := help

# =============================================================================
# Setup (REQUIRED first step)
# =============================================================================

setup: ## First-time setup: install deps + pre-commit hooks (RUN THIS FIRST)
	@echo "Setting up development environment..."
	uv sync
	uv run pre-commit install
	@echo ""
	@echo "Setup complete! Pre-commit hooks are now active."
	@echo "Tests will run automatically before each commit."

install: setup ## Alias for setup

# =============================================================================
# Dependency Management
# =============================================================================

sync: ## Sync dependencies (without hooks)
	uv sync

# =============================================================================
# Testing
# =============================================================================

test: ## Run full test suite
	uv run pytest --tb=short -q

test-verbose: ## Run tests with verbose output
	uv run pytest -v

test-cov: ## Run tests with coverage report
	uv run pytest --cov=src --cov-report=term-missing --cov-report=html

test-integration: ## Run integration tests only
	uv run pytest tests/integration/ -v

test-contract: ## Run contract tests only
	uv run pytest tests/contract/ -v

test-unit: ## Run unit tests only
	uv run pytest tests/unit/ tests/*/unit/ -v

# =============================================================================
# Code Quality
# =============================================================================

lint: ## Run linters (ruff + pyright)
	uv run ruff check src/ tests/
	uv run pyright src/

format: ## Format code with ruff
	uv run ruff check --fix src/ tests/
	uv run ruff format src/ tests/

check: lint test ## Run all checks (lint + test)

# =============================================================================
# Pre-commit
# =============================================================================

pre-commit: ## Run pre-commit on all files
	uv run pre-commit run --all-files

pre-commit-install: ## Install pre-commit hooks
	uv run pre-commit install

pre-commit-update: ## Update pre-commit hooks
	uv run pre-commit autoupdate

# =============================================================================
# Cleanup
# =============================================================================

clean: ## Remove build artifacts and caches
	rm -rf build/ dist/ *.egg-info/
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
	rm -rf htmlcov/ .coverage coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# =============================================================================
# Help
# =============================================================================

help: ## Show this help message
	@echo "Jerry Framework Development Commands"
	@echo ""
	@echo "FIRST TIME SETUP:"
	@echo "  make setup     - Install dependencies and pre-commit hooks"
	@echo ""
	@echo "AVAILABLE TARGETS:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-18s %s\n", $$1, $$2}'
