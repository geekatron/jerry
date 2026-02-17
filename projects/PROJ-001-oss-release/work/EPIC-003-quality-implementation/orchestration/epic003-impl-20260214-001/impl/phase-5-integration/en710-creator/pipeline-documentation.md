# CI Pipeline Quality Enforcement Documentation

> **Version:** 1.0.0
> **Date:** 2026-02-14
> **Enabler:** EN-710 (CI Pipeline Quality Integration)
> **SSOT:** `.context/rules/quality-enforcement.md`

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Enforcement Architecture Overview](#enforcement-architecture-overview) | 5-layer enforcement model (L1-L5) |
| [CI as L5 Post-Hoc Verification](#ci-as-l5-post-hoc-verification) | How CI implements the L5 enforcement layer |
| [CI Jobs and Quality Roles](#ci-jobs-and-quality-roles) | Each CI job mapped to its quality enforcement function |
| [Pre-Commit Hooks and L3-L5 Bridge](#pre-commit-hooks-and-l3-l5-bridge) | Local pre-commit quality gates |
| [Architecture Boundary Enforcement](#architecture-boundary-enforcement) | Multi-layer architecture validation |
| [Coverage and Quality Thresholds](#coverage-and-quality-thresholds) | Configured thresholds and fail conditions |
| [Interpreting CI Results](#interpreting-ci-results) | How to read CI pass/fail outcomes |
| [Adding New Quality Gates](#adding-new-quality-gates) | How to extend the pipeline |
| [SSOT Traceability Matrix](#ssot-traceability-matrix) | Mapping of HARD rules to enforcement points |

---

## Enforcement Architecture Overview

The Jerry quality framework uses a 5-layer enforcement architecture defined in the SSOT (`.context/rules/quality-enforcement.md`). Each layer operates at a different timing and has different context rot vulnerability.

> **SSOT Reference:** `.context/rules/quality-enforcement.md` -- Enforcement Architecture section

| Layer | Timing | Function | Context Rot | Tokens |
|-------|--------|----------|-------------|--------|
| **L1** | Session start | Behavioral foundation via rules | Vulnerable | ~12,500 |
| **L2** | Every prompt | Re-inject critical rules | Immune | ~600/prompt |
| **L3** | Before tool calls | Deterministic gating (AST) | Immune | 0 |
| **L4** | After tool calls | Output inspection, self-correction | Mixed | 0-1,350 |
| **L5** | Commit/CI | Post-hoc verification | **Immune** | 0 |

**L5 is immune to context rot** because it operates entirely outside the LLM context window. CI runs deterministic scripts (ruff, pyright, pytest, AST analysis) that enforce rules regardless of the LLM's current context state.

**Key insight:** L5 is the last line of defense. If a violation passes through L1 (rules loaded at session start), bypasses L2 (prompt-level re-injection), evades L3 (pre-tool-use gating), and is missed by L4 (post-tool-use inspection), L5 catches it at commit time (pre-commit hooks) or PR time (GitHub Actions CI).

---

## CI as L5 Post-Hoc Verification

The CI pipeline at `.github/workflows/ci.yml` is the primary L5 enforcement mechanism. It runs on all pushes and pull requests, providing a comprehensive post-hoc audit of code quality.

### Trigger Configuration

```yaml
on:
  push:
    branches: ["**"]          # All branches
  pull_request:
    branches: [main, master, "claude/**"]  # PRs to main and claude branches
```

### Concurrency

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true    # Cancel stale runs for same branch
```

This ensures CI resources are not wasted on outdated commits when new pushes arrive on the same branch.

---

## CI Jobs and Quality Roles

The CI pipeline consists of 9 jobs. Each is mapped to its quality enforcement function below.

### Job 1: `lint` -- Lint and Format (L5: Code Style)

| Attribute | Value |
|-----------|-------|
| **HARD Rules Enforced** | H-11 (type hints), H-12 (docstrings), coding-standards.md |
| **Tool** | ruff 0.14.11 |
| **Python** | 3.14 |
| **What It Catches** | Import ordering, unused imports, code style violations, formatting inconsistencies |

**Commands:**
- `ruff check . --config=pyproject.toml` -- Linting (flake8, isort, bugbear, simplify, etc.)
- `ruff format --check . --config=pyproject.toml` -- Formatting (deterministic code formatting)

**Ruff rules configured in pyproject.toml:**
- E, W (pycodestyle), F (Pyflakes), I (isort), B (bugbear), C4 (comprehensions)
- UP (pyupgrade), ARG (unused arguments), SIM (simplify), TCH (type-checking)
- PTH (pathlib), ERA (commented code), PL (pylint), RUF (ruff-specific)

### Job 2: `type-check` -- Type Checking (L5: Type Safety)

| Attribute | Value |
|-----------|-------|
| **HARD Rules Enforced** | H-11 (type hints REQUIRED on public functions) |
| **Tool** | pyright |
| **Scope** | `src/` only |

**Commands:**
- `pyright src/` -- Static type analysis of all source code

Type checking validates that all public function signatures include type annotations and that type usage is consistent throughout the codebase.

### Job 3: `security` -- Security Scanning (L5: Dependency Security)

| Attribute | Value |
|-----------|-------|
| **SSOT Rules** | AE-005 (Security-relevant code = auto-C3) |
| **Tool** | pip-audit (strict mode) |

**Commands:**
- `pip-audit --strict` -- Audits installed dependencies against known vulnerability databases

### Job 4: `plugin-validation` -- Plugin Validation (L5: Plugin Integrity)

| Attribute | Value |
|-----------|-------|
| **What It Validates** | Plugin manifests, session hook standalone execution, hook script syntax |

**Commands:**
- `uv run python scripts/validate_plugin_manifests.py` -- Validates plugin.json, marketplace.json, hooks.json
- `python3 scripts/session_start_hook.py` -- Verifies hook runs without pip install
- Hook script syntax validation via `py_compile`

### Job 5: `cli-integration` -- CLI Integration Tests (L5: Interface Compliance)

| Attribute | Value |
|-----------|-------|
| **What It Validates** | CLI subprocess behavior, `jerry --help`, `jerry --version` |

**Commands:**
- `uv run pytest tests/integration/cli/test_jerry_cli_subprocess.py -v` -- Subprocess CLI tests
- `uv run jerry --help` and `uv run jerry --version` -- Smoke tests

### Job 6: `test-pip` -- Test Suite via pip (L5: Full Quality Gate)

| Attribute | Value |
|-----------|-------|
| **HARD Rules Enforced** | H-07 through H-10 (architecture boundaries), H-20 (BDD), H-21 (coverage) |
| **Matrix** | Python 3.11, 3.12, 3.13, 3.14 |
| **Coverage Threshold** | 80% (`--cov-fail-under=80`) |
| **Excluded Tests** | `not subprocess and not llm` |

This job runs the **entire test suite** including architecture boundary tests in `tests/architecture/`. The architecture tests are NOT excluded -- they are collected and executed as part of the standard pytest run.

**Architecture tests executed:**
- `tests/architecture/test_composition_root.py` (7 tests) -- Composition root and Clean Architecture boundaries
- `tests/architecture/test_check_architecture_boundaries.py` (51 tests) -- AST-based boundary validation script unit tests
- `tests/architecture/test_config_boundaries.py` (11 tests) -- Configuration module boundaries and port-adapter contracts
- `tests/architecture/test_session_hook_architecture.py` (10 tests, 2 skipped for tech debt) -- Session hook isolation

**Total: 79 architecture tests pass, 2 skipped (documented tech debt TD-007).**

### Job 7: `test-uv` -- Test Suite via uv (L5: Full Quality Gate)

| Attribute | Value |
|-----------|-------|
| **HARD Rules Enforced** | Same as test-pip |
| **Matrix** | Python 3.11, 3.12, 3.13, 3.14 |
| **Coverage Threshold** | 80% (`--cov-fail-under=80`) |
| **Excluded Tests** | `not llm` (includes subprocess tests) |

Mirrors `test-pip` but uses uv for dependency resolution. Also runs architecture tests.

### Job 8: `coverage-report` -- Coverage Report (L5: Visibility)

| Attribute | Value |
|-----------|-------|
| **Trigger** | Pull requests only |
| **Depends On** | test-pip, test-uv |

Posts a coverage summary comment on the PR using `MishaKav/pytest-coverage-comment`. Provides visibility into coverage changes per PR.

### Job 9: `version-sync` -- Version Sync Check (L5: Consistency)

| Attribute | Value |
|-----------|-------|
| **What It Validates** | Version consistency across pyproject.toml, plugin.json, marketplace.json, CLAUDE.md |

**Commands:**
- `uv run python scripts/sync_versions.py --check`

### Job 10: `ci-success` -- Final Aggregate Gate (L5: Quality Gate)

| Attribute | Value |
|-----------|-------|
| **Depends On** | ALL 8 preceding jobs |
| **Condition** | `if: always()` (runs even if dependencies fail) |

This is the **aggregate quality gate**. It checks that ALL jobs passed and provides a single pass/fail signal. This job can be used as a branch protection rule in GitHub to prevent merging PRs that fail any quality check.

**Jobs required to pass:**
1. lint
2. type-check
3. security
4. plugin-validation
5. cli-integration
6. test-pip
7. test-uv
8. version-sync

---

## Pre-Commit Hooks and L3-L5 Bridge

The pre-commit configuration at `.pre-commit-config.yaml` provides **local L5 enforcement** that catches violations before they reach the CI pipeline. This is the bridge between L3 (pre-action gating) and L5 (CI).

| Hook | Stage | Enforcement Function |
|------|-------|---------------------|
| trailing-whitespace | pre-commit | File hygiene |
| end-of-file-fixer | pre-commit | File hygiene |
| check-yaml | pre-commit | YAML syntax |
| check-added-large-files | pre-commit | Binary/large file prevention |
| check-merge-conflict | pre-commit | Conflict marker detection |
| detect-private-key | pre-commit | Secret detection |
| ruff (lint) | pre-commit | Code style (mirrors CI `lint` job) |
| ruff-format | pre-commit | Code formatting (mirrors CI `lint` job) |
| **architecture-boundaries** | pre-commit | **AST-based architecture validation** |
| pyright | pre-commit | Type checking (mirrors CI `type-check` job) |
| pytest | pre-commit | Full test suite (mirrors CI `test-*` jobs) |
| validate-plugin-manifests | pre-commit | Plugin validation (mirrors CI `plugin-validation` job) |
| version-sync | pre-commit | Version consistency (mirrors CI `version-sync` job) |
| commitizen | commit-msg | Conventional commit message format |
| pip-audit | pre-push | Security scanning (mirrors CI `security` job) |

**Key observation:** The `architecture-boundaries` pre-commit hook runs `scripts/check_architecture_boundaries.py`, which performs the same AST-based architecture boundary validation that the architecture tests in `tests/architecture/` perform. This provides **redundant enforcement** -- violations are caught both by the pre-commit hook and by the test suite.

---

## Architecture Boundary Enforcement

Architecture boundary enforcement is a critical quality gate that prevents hexagonal architecture violations. It operates at multiple enforcement layers.

### Enforcement Points

| Layer | Mechanism | Script/Test | Timing |
|-------|-----------|-------------|--------|
| L3 | PreToolUse hook (EN-703) | `hooks/pre_tool_use.py` | Before each file write |
| L5 (local) | Pre-commit hook | `scripts/check_architecture_boundaries.py` | On `git commit` |
| L5 (CI) | Architecture tests | `tests/architecture/test_*.py` | On push/PR |
| L5 (CI) | Architecture boundary script | Runs as part of test suite | On push/PR |

### Rules Enforced

Per the SSOT (`.context/rules/architecture-standards.md`):

| Source Layer | Forbidden Imports |
|-------------|-------------------|
| domain | application, infrastructure, interface |
| application | infrastructure, interface |
| infrastructure | interface |
| shared_kernel | infrastructure, interface |

**Exemptions:**
- `bootstrap.py` (composition root) is exempt from all boundary checks
- `TYPE_CHECKING` conditional imports are exempt
- Bounded contexts (session_management, work_tracking, transcript, configuration) follow the same rules within their internal layer structure

### Architecture Test Coverage

| Test File | Tests | Focus |
|-----------|-------|-------|
| `test_composition_root.py` | 7 | Composition root is sole infrastructure wiring point |
| `test_check_architecture_boundaries.py` | 51 | Unit tests for the AST-based boundary validation script |
| `test_config_boundaries.py` | 11 | Domain layer isolation, port-adapter contracts, bootstrap wiring |
| `test_session_hook_architecture.py` | 10 (2 skipped) | Session hook isolation, entry point validation |

**Total: 79 pass, 2 skipped.** The 2 skipped tests are documented tech debt (TD-007: pre-existing infrastructure imports in adapter.py).

---

## Coverage and Quality Thresholds

### CI Coverage Threshold

| Setting | Value | Location |
|---------|-------|----------|
| `--cov-fail-under` | 80 | `.github/workflows/ci.yml` (test-pip, test-uv jobs) |
| Skip coverage escape hatch | `[skip-coverage]` in commit message | For refactoring PRs |

> **Note:** The SSOT specifies H-21 (90% line coverage REQUIRED) in `.context/rules/quality-enforcement.md`. The CI currently enforces 80% as a pragmatic threshold. The gap between 80% (CI) and 90% (SSOT) is intentional -- the SSOT target is aspirational and tracked as part of ongoing quality improvement.

### Pre-Commit Coverage

The pre-commit `pytest` hook runs the full test suite without an explicit `--cov-fail-under` flag, relying on the pyproject.toml/pytest.ini configuration.

---

## Interpreting CI Results

### Pass/Fail Semantics

| Scenario | CI Result | Action |
|----------|-----------|--------|
| All jobs green | `ci-success` passes | PR is mergeable |
| Any job red | `ci-success` fails | Fix the failing job before merge |
| Architecture test fails | `test-pip` or `test-uv` red | Architecture boundary violation -- fix the import |
| Coverage below 80% | `test-pip` or `test-uv` red | Add tests to increase coverage |
| Ruff lint fails | `lint` red | Run `ruff check --fix .` locally |
| Ruff format fails | `lint` red | Run `ruff format .` locally |
| Type check fails | `type-check` red | Fix type annotation issues |
| Security audit fails | `security` red | Investigate vulnerable dependency |
| Version mismatch | `version-sync` red | Run `uv run python scripts/sync_versions.py` to fix |

### Debugging Failures

1. Click the failing job in the GitHub Actions UI
2. Expand the failing step to see the error output
3. For test failures, look at the pytest output for the specific test that failed
4. For architecture violations, the output will show the file, line number, source layer, and target layer
5. For coverage failures, check the `term-missing` report to see which lines need coverage

### Local Reproduction

```bash
# Reproduce lint failures
uv run ruff check . --config=pyproject.toml
uv run ruff format --check . --config=pyproject.toml

# Reproduce type check failures
uv run pyright src/

# Reproduce architecture test failures
uv run pytest tests/architecture/ -v

# Reproduce coverage failures
uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=80

# Reproduce version sync failures
uv run python scripts/sync_versions.py --check

# Run all pre-commit hooks locally
uv run pre-commit run --all-files
```

---

## Adding New Quality Gates

To add a new quality enforcement step to the CI pipeline:

### Step 1: Define the Quality Rule

Document the rule in the SSOT (`.context/rules/quality-enforcement.md`) with a HARD rule ID (H-XX) and the enforcement layer (L5 for CI).

### Step 2: Implement the Check

Create a script in `scripts/` or a test in `tests/architecture/` that validates the rule.

**Script pattern** (for `scripts/`):
```python
#!/usr/bin/env python3
"""Quality gate: {description}. Exit 0 = pass, Exit 1 = fail."""
import sys

def main() -> int:
    # Validation logic here
    violations = check_violations()
    if violations:
        print(f"Found {len(violations)} violations")
        return 1
    print("All checks passed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

**Test pattern** (for `tests/architecture/`):
```python
"""Architecture test: {description}."""
class TestNewQualityGate:
    def test_rule_is_enforced(self) -> None:
        """Verify the quality rule holds."""
        # Validation logic here
        assert violations == []
```

### Step 3: Add to CI Pipeline

Add a new job or step to `.github/workflows/ci.yml`:

```yaml
  new-quality-gate:
    name: New Quality Gate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - name: Run quality gate
        run: uv run python scripts/new_quality_gate.py
```

### Step 4: Add to Aggregate Gate

Add the new job to the `ci-success` job's `needs` list and add a condition check:

```yaml
  ci-success:
    needs: [..., new-quality-gate]
    steps:
      - run: |
          if [[ "${{ needs.new-quality-gate.result }}" != "success" ]]; then
            exit 1
          fi
```

### Step 5: Add to Pre-Commit (Optional)

For local enforcement, add a pre-commit hook in `.pre-commit-config.yaml`:

```yaml
  - repo: local
    hooks:
      - id: new-quality-gate
        name: new quality gate
        entry: uv run python scripts/new_quality_gate.py
        language: system
        types: [python]
        pass_filenames: false
```

---

## SSOT Traceability Matrix

This matrix maps each HARD rule from the SSOT to its L5 enforcement point(s) in the CI pipeline.

| HARD Rule | Description | L5 Enforcement | CI Job |
|-----------|-------------|----------------|--------|
| H-05 | UV only for Python execution | Pre-commit hooks use `uv run` | All uv-based jobs |
| H-06 | UV only for dependencies | `uv sync` in CI | test-uv, cli-integration, plugin-validation |
| H-07 | Domain layer: no external imports | Architecture tests + pre-commit hook | test-pip, test-uv |
| H-08 | Application layer: no infra/interface imports | Architecture tests + pre-commit hook | test-pip, test-uv |
| H-09 | Composition root exclusivity | Architecture tests (test_composition_root.py) | test-pip, test-uv |
| H-10 | One class per file | Ruff linting (partial) | lint |
| H-11 | Type hints REQUIRED on public functions | pyright type checking | type-check |
| H-12 | Docstrings REQUIRED on public functions | Ruff linting (D rules if enabled) | lint |
| H-20 | Test before implement (BDD Red phase) | pytest suite execution | test-pip, test-uv |
| H-21 | 90% line coverage REQUIRED | `--cov-fail-under=80` (CI), 90% aspirational | test-pip, test-uv |

**Rules NOT enforceable at L5:**
| HARD Rule | Reason |
|-----------|--------|
| H-01 (No recursive subagents) | Runtime LLM behavior -- enforced at L1/L2 |
| H-02 (User authority) | Runtime LLM behavior -- enforced at L1/L2 |
| H-03 (No deception) | Runtime LLM behavior -- enforced at L1/L2 |
| H-04 (Active project REQUIRED) | Session-time -- enforced at L1 (session hook) |
| H-13 (Quality threshold >= 0.92) | LLM-as-Judge scoring -- enforced at L2/L4 |
| H-14 (Creator-critic-revision cycle) | LLM workflow -- enforced at L2/L4 |
| H-15 (Self-review before presenting) | LLM behavior -- enforced at L2 |
| H-16 (Steelman before critique) | LLM behavior -- enforced at L2 |
| H-17 (Quality scoring REQUIRED) | LLM workflow -- enforced at L2/L4 |
| H-18 (Constitutional compliance check) | LLM behavior -- enforced at L2 |
| H-19 (Governance escalation per AE rules) | LLM behavior -- enforced at L2 |
| H-22 (Proactive skill invocation) | LLM behavior -- enforced at L1/L2 |
| H-23 (Navigation table REQUIRED) | Markdown content -- potential future L5 gate |
| H-24 (Anchor links REQUIRED) | Markdown content -- potential future L5 gate |

---

## References

| Source | Path |
|--------|------|
| CI Pipeline | `.github/workflows/ci.yml` |
| Quality Enforcement SSOT | `.context/rules/quality-enforcement.md` |
| Architecture Standards | `.context/rules/architecture-standards.md` |
| Pre-Commit Config | `.pre-commit-config.yaml` |
| Architecture Boundary Script | `scripts/check_architecture_boundaries.py` |
| Architecture Tests | `tests/architecture/test_*.py` |
| Testing Standards | `.context/rules/testing-standards.md` |
| Coding Standards | `.context/rules/coding-standards.md` |
