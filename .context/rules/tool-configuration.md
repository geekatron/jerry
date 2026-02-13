# Tool Configuration Standards

> Configuration standards for development tools in Jerry.
> Ensures consistent tooling across the codebase.

**Related Standards**:
- [Coding Standards](coding-standards.md) - Code style rules
- [Testing Standards](testing-standards.md) - Test requirements
- [Pattern Catalog](../patterns/PATTERN-CATALOG.md) - Architecture patterns

---

## Python Environment

### Required Version

```
Python 3.11+
```

### Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate
```

---

## pyproject.toml

### Project Metadata

```toml
[project]
name = "jerry"
version = "0.1.0"
description = "Framework for behavior and workflow guardrails"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.1",
    "pytest-asyncio>=0.23",
    "mypy>=1.8",
    "ruff>=0.2",
]
```

### Build System

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
```

---

## pytest Configuration

### pytest.ini Settings

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    unit: Unit tests (fast, no I/O)
    integration: Integration tests (may use filesystem)
    e2e: End-to-end tests (slow, full stack)
    architecture: Architecture boundary tests
asyncio_mode = auto
```

### pyproject.toml Alternative

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "unit: Unit tests (fast, no I/O)",
    "integration: Integration tests (may use filesystem)",
    "e2e: End-to-end tests (slow, full stack)",
    "architecture: Architecture boundary tests",
]
asyncio_mode = "auto"
```

### Coverage Configuration

```toml
[tool.coverage.run]
source = ["src"]
branch = true
omit = [
    "*/tests/*",
    "*/__init__.py",
    "*/conftest.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "@abstractmethod",
]
fail_under = 90
show_missing = true
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific category
pytest -m unit
pytest -m integration
pytest -m architecture

# Run specific file
pytest tests/unit/domain/test_work_item.py

# Run with verbose output
pytest -vvv

# Stop on first failure
pytest -x
```

---

## mypy Configuration

### pyproject.toml Settings

```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_configs = true
show_error_codes = true
show_column_numbers = true

# Per-module overrides
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = "scripts.*"
disallow_untyped_defs = false
```

### Running mypy

```bash
# Check all source code
mypy src/

# Check specific module
mypy src/domain/

# Check with strict mode
mypy --strict src/
```

---

## Ruff Configuration

### pyproject.toml Settings

```toml
[tool.ruff]
target-version = "py311"
line-length = 100
src = ["src", "tests"]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "ARG",    # flake8-unused-arguments
    "SIM",    # flake8-simplify
    "TCH",    # flake8-type-checking
    "PTH",    # flake8-use-pathlib
    "ERA",    # eradicate (commented code)
    "PL",     # Pylint
    "RUF",    # Ruff-specific
]
ignore = [
    "E501",   # Line too long (handled by formatter)
    "PLR0913", # Too many arguments
    "PLR2004", # Magic value comparison
]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["ARG", "PLR2004"]
"scripts/*" = ["T20"]  # Allow print in scripts

[tool.ruff.lint.isort]
known-first-party = ["src"]
force-single-line = false
lines-after-imports = 2

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
```

### Running Ruff

```bash
# Check for issues
ruff check src/

# Fix auto-fixable issues
ruff check --fix src/

# Format code
ruff format src/

# Check formatting without changing
ruff format --check src/
```

---

## Pre-commit Configuration

### .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.2.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies:
          - types-all

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
```

### Installing Pre-commit

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

---

## Editor Configuration

### .editorconfig

```ini
root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false

[*.{yaml,yml}]
indent_size = 2

[*.json]
indent_size = 2

[Makefile]
indent_style = tab
```

### VS Code Settings

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.analysis.typeCheckingMode": "strict",
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit"
    }
  },
  "ruff.lint.args": ["--config=pyproject.toml"],
  "mypy.runUsingActiveInterpreter": true,
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true
}
```

---

## Makefile

### Common Commands

```makefile
.PHONY: install test lint format check clean

# Install dependencies
install:
	pip install -e ".[dev]"
	pre-commit install

# Run tests
test:
	pytest

# Run tests with coverage
test-cov:
	pytest --cov=src --cov-report=term-missing --cov-report=html

# Run linting
lint:
	ruff check src/ tests/
	mypy src/

# Format code
format:
	ruff check --fix src/ tests/
	ruff format src/ tests/

# Run all checks
check: lint test

# Clean build artifacts
clean:
	rm -rf build/ dist/ *.egg-info/
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
	rm -rf htmlcov/ .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +

# Architecture tests only
test-arch:
	pytest tests/architecture/ -v
```

---

## CI/CD Configuration

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Lint with ruff
        run: ruff check src/ tests/

      - name: Type check with mypy
        run: mypy src/

      - name: Run tests
        run: pytest --cov=src --cov-report=xml --cov-fail-under=90

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
```

---

## Environment Variables

### Development

```bash
# .env.development
JERRY_LOG_LEVEL=DEBUG
JERRY_PROJECTS_DIR=projects
JERRY_DATA_DIR=.jerry/data
```

### Testing

```bash
# .env.test
JERRY_LOG_LEVEL=WARNING
JERRY_PROJECTS_DIR=/tmp/jerry-test/projects
JERRY_DATA_DIR=/tmp/jerry-test/data
```

### Loading Environment

```python
# src/infrastructure/config.py
from pathlib import Path
import os


def load_env(env_file: str = ".env") -> None:
    """Load environment variables from file."""
    env_path = Path(env_file)
    if not env_path.exists():
        return

    with env_path.open() as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())
```

---

## Jerry-Specific Decisions

> **Jerry Decision**: Use Ruff over Black+isort+flake8 for unified tooling.

> **Jerry Decision**: Strict mypy configuration with per-module overrides for tests.

> **Jerry Decision**: pytest markers categorize tests by pyramid level.

> **Jerry Decision**: Coverage threshold of 90% enforced in CI.

---

## References

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [pre-commit Documentation](https://pre-commit.com/)
- [EditorConfig](https://editorconfig.org/)
