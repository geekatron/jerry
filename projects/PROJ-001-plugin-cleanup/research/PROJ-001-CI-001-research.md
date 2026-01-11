# CI/CD Best Practices Research

> **Document ID**: PROJ-001-CI-001-research
> **PS ID**: PROJ-001
> **Entry ID**: CI-001.R
> **Date**: 2026-01-10
> **Author**: ps-researcher agent v2.0.0 (Claude Opus 4.5)
> **Topic**: CI/CD Pipeline Implementation Best Practices

---

## L0: Executive Summary (ELI5)

This research investigates best practices for implementing CI/CD pipelines in Python projects, specifically for the Jerry framework. The goal is to prevent regressions through automated testing at two stages: pre-commit (local) and GitHub Actions (remote).

**Key Findings:**

1. **Pre-commit hooks** provide the first line of defense - they catch issues before code is even committed. Industry best practice is to run the full test suite by default, with configuration options for fast-feedback scenarios.

2. **GitHub Actions** serves as a safety net - it validates code in a clean environment, provides PR status checks, and catches issues if someone bypasses local hooks.

3. **Modern Python tooling** has consolidated around **ruff** (linting + formatting) and **pyright** (type checking), replacing older fragmented tools like flake8, black, isort, and mypy.

4. **Coverage reporting** on PRs improves visibility and encourages maintaining test quality.

**Business Impact:** Implementing this CI/CD pipeline will:
- Prevent regressions from reaching the repository
- Provide immediate feedback to developers
- Enable confident refactoring and feature development
- Establish a quality baseline for the project

---

## L1: Technical Analysis (Software Engineer)

### Pre-commit Configuration

**Tool Selection:**

| Tool | Purpose | Why |
|------|---------|-----|
| pre-commit | Hook framework | Industry standard, 230+ code snippets in Context7 |
| ruff | Linting + formatting | 10-100x faster than flake8+black, unified tool |
| pyright | Type checking | Microsoft-backed, faster than mypy |
| pytest | Testing | Already in use, full test suite |

**Recommended `.pre-commit-config.yaml`:**

```yaml
# .pre-commit-config.yaml
# See: https://pre-commit.com

default_install_hook_types: [pre-commit, pre-push]
default_stages: [pre-commit]

repos:
  # Basic file hygiene
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  # Ruff: Fast linting and formatting (replaces flake8, black, isort)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.10
    hooks:
      - id: ruff-check
        args: [--fix, --config=pyproject.toml]
      - id: ruff-format
        args: [--config=pyproject.toml]

  # Type checking (pyright via local hook)
  - repo: local
    hooks:
      - id: pyright
        name: pyright type checking
        entry: .venv/bin/pyright
        language: system
        types: [python]
        pass_filenames: false

  # Full test suite (default: all tests)
  - repo: local
    hooks:
      - id: pytest
        name: pytest (full suite)
        entry: .venv/bin/python -m pytest
        language: system
        types: [python]
        pass_filenames: false
        # CONFIGURABLE: Set to pre-push for faster commits
        stages: [pre-commit]
```

**Configuration Options:**

1. **Full suite on commit** (default, safest):
   - All 1330 tests run before every commit
   - Slower but prevents ALL regressions

2. **Full suite on push** (faster iteration):
   - Change pytest stage from `pre-commit` to `pre-push`
   - Linting/formatting still runs on commit

3. **Fast subset on commit** (power users):
   - Add `args: [-m, "not slow"]` to pytest hook
   - Requires marking slow tests with `@pytest.mark.slow`

### GitHub Actions Workflow

**Recommended `.github/workflows/ci.yml`:**

```yaml
name: CI

on:
  push:
    branches: ["**"]
  pull_request:
    branches: [main, master, claude/*]

permissions:
  contents: read
  pull-requests: write

jobs:
  lint:
    name: Lint & Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.14"
      - name: Install ruff
        run: pip install ruff
      - name: Check linting
        run: ruff check .
      - name: Check formatting
        run: ruff format --check .

  type-check:
    name: Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.14"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pyright
          pip install -e .
      - name: Run pyright
        run: pyright

  test:
    name: Test (Python ${{ matrix.python-version }})
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13", "3.14"]
    steps:
      - uses: actions/checkout@v5
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"
      - name: Run tests with coverage
        run: |
          pytest --cov=src --cov-report=xml --cov-report=html --junitxml=junit.xml
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        if: matrix.python-version == '3.14'
        with:
          files: coverage.xml
          fail_ci_if_error: false
      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results-${{ matrix.python-version }}
          path: junit.xml

  coverage-comment:
    name: Coverage Report
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v5
      - name: Download coverage
        uses: actions/download-artifact@v4
        with:
          name: test-results-3.14
      - name: Pytest Coverage Comment
        uses: MishaKav/pytest-coverage-comment@main
        with:
          pytest-xml-coverage-path: coverage.xml
          junitxml-path: junit.xml
```

### pyproject.toml Configuration

```toml
[tool.ruff]
target-version = "py311"
line-length = 100
src = ["src", "tests"]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "ARG",    # flake8-unused-arguments
    "SIM",    # flake8-simplify
]
ignore = [
    "E501",   # line length (handled by formatter)
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.pyright]
pythonVersion = "3.11"
typeCheckingMode = "basic"
include = ["src"]
exclude = ["**/__pycache__", ".venv"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--import-mode=importlib"
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
]

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

---

## L2: Architectural Implications (Principal Architect)

### Trade-offs Analysis

| Aspect | Pre-commit | GitHub Actions | Recommendation |
|--------|------------|----------------|----------------|
| **Speed** | Slower commits | Async, no wait | Both: layered defense |
| **Bypass** | `--no-verify` possible | Always runs | GHA is safety net |
| **Environment** | Developer machine | Clean Ubuntu | GHA catches env issues |
| **Coverage** | Local only | PR comments | GHA for visibility |
| **Matrix testing** | Single version | Multiple versions | GHA for compatibility |

### Risk Assessment

| Risk | Mitigation |
|------|------------|
| Long commit times | Document fast-mode configuration |
| Hook bypass | GHA required status check |
| Flaky tests | Mark slow tests, run separately |
| False positives | Ruff has good defaults, tune via config |

### Integration with Existing Architecture

**Hexagonal Alignment:**
- Pre-commit: Primary adapter (developer interface)
- GitHub Actions: Secondary adapter (platform interface)
- Both validate the same domain logic (tests)

**Jerry Constitution Compliance:**
- P-REGRESS: Zero regressions via test suite
- P-002: CI config persisted to repository
- P-EVIDENCE: Coverage reports provide evidence

### Future Evolution Path

1. **Phase 1 (Current)**: Pre-commit + GitHub Actions basics
2. **Phase 2**: Add coverage thresholds (`--cov-fail-under=80`)
3. **Phase 3**: Add dependency scanning (Dependabot, Snyk)
4. **Phase 4**: Add performance benchmarks (pytest-benchmark)

---

## References

### Context7 Sources
1. Context7 `/pre-commit/pre-commit.com` - Hook configuration patterns
2. Context7 `/websites/github_en_actions` - Python CI workflow examples
3. Context7 `/astral-sh/ruff` - Pre-commit integration patterns
4. Context7 `/pre-commit/pre-commit-hooks` - Standard hooks

### Web Sources
5. [Effortless Code Quality: Ultimate Pre-Commit Hooks Guide 2025](https://gatlenculp.medium.com/effortless-code-quality-the-ultimate-pre-commit-hooks-guide-for-2025-57ca501d9835) - Modern Python pre-commit practices
6. [Pre-commit vs CI](https://switowski.com/blog/pre-commit-vs-ci/) - Layered approach rationale
7. [A GitHub Actions Setup for Python Projects in 2025](https://ber2.github.io/posts/2025_github_actions_python/) - Modern workflow patterns
8. [Pytest Coverage Comment Action](https://github.com/marketplace/actions/pytest-coverage-comment) - PR coverage reporting

### Official Documentation
9. [pre-commit.com](https://pre-commit.com) - Official pre-commit documentation
10. [GitHub Actions Python Tutorial](https://docs.github.com/en/actions/tutorials/build-and-test-code/python) - Official GHA Python guide
11. [Ruff Documentation](https://docs.astral.sh/ruff/) - Ruff linter/formatter docs

---

## PS Integration

```yaml
researcher_output:
  ps_id: "PROJ-001"
  entry_id: "CI-001.R"
  artifact_path: "projects/PROJ-001-plugin-cleanup/research/PROJ-001-CI-001-research.md"
  summary: "CI/CD pipeline research complete - pre-commit + GitHub Actions recommended"
  sources_count: 11
  confidence: "high"
  next_agent_hint: "ps-analyst for implementation gap analysis"
```

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-10 | Claude Opus 4.5 | Initial research document |
