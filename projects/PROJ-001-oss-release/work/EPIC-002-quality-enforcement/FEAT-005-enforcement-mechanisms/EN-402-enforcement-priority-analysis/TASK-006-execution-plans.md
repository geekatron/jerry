# TASK-006: Detailed Execution Plans for Top 3 Priority Enforcement Vectors

<!--
DOCUMENT-ID: FEAT-005:EN-402-TASK-006-EXECUTION-PLANS
TEMPLATE: Execution Plan
VERSION: 1.1.0
SOURCE: TASK-004 (Priority Matrix), TASK-005 (Enforcement ADR), TASK-003 (Trade Study), TASK-009 (Revised Catalog)
AGENT: ps-architect (Claude Opus 4.6)
DATE: 2026-02-13
PARENT: EN-402 (Enforcement Priority Analysis & Decision)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
QUALITY-TARGET: >= 0.92
CONSUMERS: TASK-007 (ps-critic adversarial review), EN-403 (Rule Optimization), EN-404 (Structural Enforcement), EN-405 (Process Enforcement)
-->

> **Version:** 1.1.0
> **Agent:** ps-architect (Claude Opus 4.6)
> **Created:** 2026-02-13
> **Inputs:** TASK-004 (top 3 vector profiles), TASK-005 (ADR roadmap), TASK-003 (integration architecture), TASK-009 (catalog)
> **Confidence:** HIGH -- all tasks traceable to existing codebase and established tooling

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Scope, objectives, and cross-vector integration overview |
| [Vector 1: V-038 AST Import Boundary Validation](#vector-1-v-038-ast-import-boundary-validation) | Full execution plan for AST enforcement (WCS 4.92) |
| [Vector 2: V-045 CI Pipeline Enforcement](#vector-2-v-045-ci-pipeline-enforcement) | Full execution plan for CI enforcement (WCS 4.86) |
| [Vector 3: V-044 Pre-commit Hook Validation](#vector-3-v-044-pre-commit-hook-validation) | Full execution plan for pre-commit enforcement (WCS 4.80) |
| [Cross-Vector Integration](#cross-vector-integration) | Defense-in-depth composition, execution order, shared infrastructure |
| [Consolidated Risk Register](#consolidated-risk-register) | All risks across 3 vectors with mitigations |
| [Consolidated Token Budget Impact](#consolidated-token-budget-impact) | Total token cost analysis |
| [References](#references) | All citations |

---

## Executive Summary

This document provides detailed, developer-implementable execution plans for the top 3 priority enforcement vectors identified by TASK-004 and confirmed by the TASK-005 ADR:

| Priority | Vector | Name | WCS | Tier | Layer |
|----------|--------|------|-----|------|-------|
| 1 | V-038 | AST Import Boundary Validation | 4.92 | T1 | L3/L5 |
| 2 | V-045 | CI Pipeline Enforcement | 4.86 | T1 | L5 |
| 3 | V-044 | Pre-commit Hook Validation | 4.80 | T1 | L5 |

All three vectors share critical properties that make them the enforcement foundation:

- **Context rot immunity**: All operate as external processes, unaffected by LLM context degradation
- **Zero token cost**: None consume context window tokens
- **Universal portability**: All work on macOS, Linux, and Windows with Python + Git
- **Deterministic enforcement**: Binary pass/fail results, not probabilistic LLM compliance

Together, these three vectors form a **defense-in-depth stack** covering Layer 3 (pre-action gating) and Layer 5 (post-hoc verification) of the TASK-003 enforcement architecture.

### Estimated Total Effort

| Vector | Effort Range | Primary Deliverables |
|--------|-------------|---------------------|
| V-038 | 2-3 days | AST validator library, boundary rule engine, test suite |
| V-045 | 1-2 days | Enhanced CI workflow with architecture enforcement jobs |
| V-044 | 0.5-1 day | Enhanced pre-commit configuration with AST boundary hooks |
| **Total** | **3.5-6 days** | **Complete L3/L5 enforcement stack** |

---

## Vector 1: V-038 AST Import Boundary Validation

### 1.1 Vector Profile

| Attribute | Value |
|-----------|-------|
| **ID** | V-038 |
| **Name** | AST Import Boundary Validation |
| **WCS** | 4.92 (highest in 62-vector catalog) |
| **Tier** | Tier 1: Implement Immediately |
| **Family** | F5: Structural/Code-Level Enforcement |
| **Enforcement Layer** | L3 (Pre-Action Gating) + L5 (Post-Hoc Verification) |
| **Scores** | CRR=5, EFF=5, PORT=5, TOK=5, BYP=5, COST=4, MAINT=5 |
| **TRL** | 6 -- concept demonstrated in `tests/architecture/test_composition_root.py` |

**What it enforces:** Jerry's hexagonal architecture layer boundaries -- ensuring that domain code never imports from infrastructure, application code never imports from interface, and only the composition root (`src/bootstrap.py`) wires infrastructure adapters. These boundaries are defined in `.claude/rules/architecture-standards.md`.

**Why it is top priority:** It is the only vector that scores 5 on six of seven evaluation dimensions. It is context-rot-immune (external Python process), deterministic (AST analysis is binary), universally portable (Python stdlib `ast` module), zero-token, and survives all four adversary scenarios. Existing test infrastructure reduces implementation cost to approximately one day for the core library.

### 1.2 Implementation Design

#### Technical Approach

The implementation extracts and generalizes the AST import analysis logic currently in `tests/architecture/test_composition_root.py` into a reusable library that can be invoked from three integration points:

1. **Architecture test suite** (existing, enhanced): `tests/architecture/` -- runs via `pytest` during development and CI
2. **Pre-commit hook** (new): Invoked by `.pre-commit-config.yaml` to validate changed files before commit
3. **Standalone CLI** (new): `uv run python -m src.infrastructure.internal.enforcement.ast_boundary_validator` for ad-hoc checks

```
EXECUTION FLOW:

Developer writes code
       │
       ├──► [L5: pre-commit] ──► ast_boundary_validator.validate_file(path)
       │                                    │
       │                              ┌─────┴─────┐
       │                              │ PASS/FAIL  │
       │                              └─────┬─────┘
       │                                    │
       ├──► [L5: pytest] ──► test_layer_boundaries.py ──► ast_boundary_validator
       │
       └──► [L5: CI] ──► GitHub Actions ──► pytest ──► ast_boundary_validator
```

#### Integration Points in Jerry's Architecture

The validator library lives in the infrastructure layer as an internal utility, not a domain concept:

```
src/
├── infrastructure/
│   └── internal/
│       └── enforcement/                  # NEW: Enforcement utilities
│           ├── __init__.py
│           ├── ast_boundary_validator.py # Core AST analysis engine
│           ├── boundary_rules.py         # Boundary rule definitions
│           └── __main__.py               # Standalone CLI entry point
│
tests/
├── architecture/
│   ├── test_composition_root.py          # EXISTING: Enhanced to use new library
│   ├── test_config_boundaries.py         # EXISTING: Enhanced to use new library
│   ├── test_session_hook_architecture.py # EXISTING: Enhanced to use new library
│   ├── test_layer_boundaries.py          # NEW: Comprehensive boundary tests
│   └── conftest.py                       # NEW: Shared fixtures for arch tests
```

**Design decision (v1.1 revision):** The enforcement utilities are placed in `src/infrastructure/internal/enforcement/` to comply with Jerry's hexagonal architecture standards (`.claude/rules/architecture-standards.md`). The `src/infrastructure/internal/` directory is designated for internal utilities including `IFileStore` and `ISerializer` implementations, and enforcement utilities (AST validation, boundary rules) are internal infrastructure concerns that serve the same cross-cutting role. While enforcement utilities are not port adapters, they are infrastructure-layer tools that validate code structure -- a concern that belongs in the infrastructure layer per the dependency rules (infrastructure may import from domain and application; interface imports from all layers). Placing them at `src/enforcement/` (a top-level sibling to `src/domain/`, `src/application/`, etc.) would violate the established 4-layer hexagonal structure where all code resides within one of the canonical layers or `shared_kernel/`.

#### File Locations for New/Modified Code

| File | Action | Purpose |
|------|--------|---------|
| `src/infrastructure/internal/enforcement/__init__.py` | CREATE | Package initialization |
| `src/infrastructure/internal/enforcement/ast_boundary_validator.py` | CREATE | Core AST import extraction and validation |
| `src/infrastructure/internal/enforcement/boundary_rules.py` | CREATE | Declarative boundary rule definitions |
| `src/infrastructure/internal/enforcement/__main__.py` | CREATE | CLI entry point for standalone validation |
| `tests/architecture/test_layer_boundaries.py` | CREATE | Comprehensive boundary enforcement tests |
| `tests/architecture/conftest.py` | CREATE | Shared fixtures (project_root, src_root, etc.) |
| `tests/architecture/test_composition_root.py` | MODIFY | Refactor to use shared AST library |
| `tests/architecture/test_config_boundaries.py` | MODIFY | Refactor to use shared AST library |
| `tests/architecture/test_session_hook_architecture.py` | MODIFY | Refactor to use shared AST library |
| `.pre-commit-config.yaml` | MODIFY | Add AST boundary check hook (V-044 integration) |
| `.github/workflows/ci.yml` | MODIFY | Add architecture enforcement job (V-045 integration) |

#### Dependencies on Existing Code

| Dependency | Location | Nature |
|------------|----------|--------|
| AST extraction functions | `tests/architecture/test_composition_root.py` (lines 18-78) | Refactor and generalize |
| Layer import detection | `tests/architecture/test_config_boundaries.py` (lines 31-75) | Consolidate into shared library |
| Architecture boundary rules | `.claude/rules/architecture-standards.md` (Dependency Rules table) | Encode as data |
| Bounded context structure | `src/session_management/`, `src/work_tracking/`, `src/transcript/`, `src/configuration/` | Dynamic discovery |

### 1.3 Implementation Tasks

#### TASK-038-01: Create AST Boundary Validator Core Library

**Description:** Extract and generalize the AST import extraction logic from the three existing architecture test files into a reusable library at `src/infrastructure/internal/enforcement/ast_boundary_validator.py`.

**Estimated Effort:** 4 hours

**Dependencies:** None (first task)

**Deliverables:**

```python
# src/infrastructure/internal/enforcement/ast_boundary_validator.py

@dataclass(frozen=True)
class ImportViolation:
    """A detected import boundary violation."""
    file_path: Path
    line_number: int
    import_module: str
    source_layer: str
    target_layer: str
    rule_violated: str

class ASTBoundaryValidator:
    """Validates Python import boundaries using AST analysis.

    Uses Python's ast module to extract import statements and
    check them against configurable boundary rules.
    """

    def __init__(self, rules: list[BoundaryRule]) -> None: ...

    def extract_imports(
        self,
        file_path: Path,
        include_local: bool = False,
    ) -> list[ImportInfo]: ...

    def validate_file(self, file_path: Path) -> list[ImportViolation]: ...

    def validate_directory(
        self,
        directory: Path,
        recursive: bool = True,
    ) -> list[ImportViolation]: ...

    def validate_changed_files(
        self,
        file_paths: list[Path],
    ) -> list[ImportViolation]: ...
```

**Acceptance Criteria:**
- [ ] AC-038-01-01: `extract_imports()` returns all module-level imports from a Python file using `ast.parse()`
- [ ] AC-038-01-02: `extract_imports(include_local=True)` also returns imports inside functions/classes
- [ ] AC-038-01-03: `validate_file()` returns an empty list for compliant files and a list of `ImportViolation` for non-compliant files
- [ ] AC-038-01-04: `validate_directory()` recursively validates all `.py` files, excluding `__pycache__` and `__init__.py`
- [ ] AC-038-01-05: Handles `SyntaxError` gracefully (skip file, log warning)
- [ ] AC-038-01-06: Uses only Python stdlib (`ast`, `pathlib`, `dataclasses`)
- [ ] AC-038-01-07: Type hints on all public functions and methods
- [ ] AC-038-01-08: Google-style docstrings on all public functions and methods

#### TASK-038-02: Create Boundary Rule Engine

**Description:** Define a declarative boundary rule system at `src/infrastructure/internal/enforcement/boundary_rules.py` that encodes Jerry's hexagonal architecture constraints as data rather than hardcoded logic.

**Estimated Effort:** 3 hours

**Dependencies:** TASK-038-01

**Deliverables:**

```python
# src/infrastructure/internal/enforcement/boundary_rules.py

@dataclass(frozen=True)
class BoundaryRule:
    """A single import boundary rule."""
    name: str
    source_layer_patterns: list[str]  # e.g., ["src.*.domain", "src.domain"]
    forbidden_target_patterns: list[str]  # e.g., ["src.*.infrastructure"]
    description: str
    severity: str = "error"  # "error" or "warning"

def get_jerry_boundary_rules() -> list[BoundaryRule]:
    """Return Jerry's hexagonal architecture boundary rules.

    Rules encoded from .claude/rules/architecture-standards.md:
    - Domain cannot import application, infrastructure, or interface
    - Application cannot import infrastructure or interface
    - Infrastructure cannot import interface
    - Shared kernel cannot import infrastructure or interface
    """
```

**Acceptance Criteria:**
- [ ] AC-038-02-01: Rules cover all four hexagonal layer boundaries from architecture-standards.md
- [ ] AC-038-02-02: Rules handle bounded context prefixes (`src.session_management.domain`, `src.work_tracking.domain`, etc.)
- [ ] AC-038-02-03: Rules support wildcard patterns for bounded context discovery (e.g., `src.*.domain`)
- [ ] AC-038-02-04: Composition root (`src/bootstrap.py`) is explicitly exempted
- [ ] AC-038-02-05: `shared_kernel` is allowed as an import source for domain layers
- [ ] AC-038-02-06: Dynamic import detection (`importlib`, `__import__`) is flagged as warning
- [ ] AC-038-02-07: Rules are immutable (`@dataclass(frozen=True)`)

#### TASK-038-03: Create Standalone CLI Entry Point

**Description:** Create `src/infrastructure/internal/enforcement/__main__.py` so the validator can be invoked as `uv run python -m src.infrastructure.internal.enforcement` for ad-hoc validation runs.

**Estimated Effort:** 1 hour

**Dependencies:** TASK-038-01, TASK-038-02

**Deliverables:**

```python
# src/infrastructure/internal/enforcement/__main__.py
"""Standalone enforcement validator CLI.

Usage:
    uv run python -m src.infrastructure.internal.enforcement [path...]
    uv run python -m src.infrastructure.internal.enforcement --changed  # git changed files only
"""
```

**Acceptance Criteria:**
- [ ] AC-038-03-01: Exit code 0 when all files pass validation
- [ ] AC-038-03-02: Exit code 1 when violations are found, with human-readable violation report
- [ ] AC-038-03-03: `--changed` flag validates only files changed in git working tree
- [ ] AC-038-03-04: `--json` flag outputs violations as JSON for tooling integration
- [ ] AC-038-03-05: Default path is `src/` if no arguments provided

#### TASK-038-04: Refactor Existing Architecture Tests

**Description:** Refactor the three existing architecture test files to use the new shared `ASTBoundaryValidator` library, eliminating code duplication.

**Estimated Effort:** 2 hours

**Dependencies:** TASK-038-01, TASK-038-02

**Deliverables:**
- Modified `tests/architecture/test_composition_root.py`: Replace inline `get_imports_from_file()` and `has_infrastructure_import()` with `ASTBoundaryValidator`
- Modified `tests/architecture/test_config_boundaries.py`: Replace inline `get_module_imports()` and `has_layer_import()` with `ASTBoundaryValidator`
- Modified `tests/architecture/test_session_hook_architecture.py`: Replace inline `get_imports_from_file()` with shared import
- New `tests/architecture/conftest.py`: Extract shared fixtures (`project_root`, `src_root`, `scripts_root`)

**Acceptance Criteria:**
- [ ] AC-038-04-01: All existing architecture tests pass after refactor (zero behavior change)
- [ ] AC-038-04-02: `get_imports_from_file()` function is defined in exactly one location (the validator library)
- [ ] AC-038-04-03: Shared fixtures (`project_root`, `src_root`) are in `tests/architecture/conftest.py`
- [ ] AC-038-04-04: No test file duplicates AST analysis logic

#### TASK-038-05: Create Comprehensive Layer Boundary Tests

**Description:** Create `tests/architecture/test_layer_boundaries.py` with comprehensive boundary tests covering all bounded contexts and layers.

**Estimated Effort:** 3 hours

**Dependencies:** TASK-038-01, TASK-038-02, TASK-038-04

**Deliverables:**

```python
# tests/architecture/test_layer_boundaries.py

class TestDomainLayerBoundaries:
    """Domain must not import application, infrastructure, or interface."""

    @pytest.mark.parametrize("context", [
        "session_management", "work_tracking", "transcript", "configuration"
    ])
    def test_domain_has_no_infrastructure_imports(self, context): ...
    def test_domain_has_no_application_imports(self, context): ...
    def test_domain_has_no_interface_imports(self, context): ...

class TestApplicationLayerBoundaries:
    """Application must not import infrastructure or interface."""
    ...

class TestSharedKernelBoundaries:
    """Shared kernel must not import infrastructure or interface."""
    ...

class TestCompositionRootExclusivity:
    """Only bootstrap.py may import infrastructure adapters."""
    ...

class TestDynamicImportDetection:
    """Flag importlib/__import__ usage as warnings."""
    ...
```

**Acceptance Criteria:**
- [ ] AC-038-05-01: Tests cover all 4 bounded contexts (session_management, work_tracking, transcript, configuration)
- [ ] AC-038-05-02: Tests cover all 4 layer boundaries from architecture-standards.md
- [ ] AC-038-05-03: Tests use `pytest.mark.parametrize` for bounded context iteration
- [ ] AC-038-05-04: Tests dynamically discover bounded contexts from `src/` directory
- [ ] AC-038-05-05: Tests detect `importlib.import_module()` and `__import__()` calls
- [ ] AC-038-05-06: Tests are marked with `@pytest.mark.architecture`
- [ ] AC-038-05-07: All tests pass on current codebase (no false positives)

#### TASK-038-06: Unit Tests for Validator Library

**Description:** Write unit tests for the AST boundary validator library itself.

**Estimated Effort:** 2 hours

**Dependencies:** TASK-038-01, TASK-038-02

**Deliverables:**
- `tests/unit/enforcement/test_ast_boundary_validator.py`
- `tests/unit/enforcement/test_boundary_rules.py`
- Test fixtures with sample Python files containing valid/invalid imports

**Acceptance Criteria:**
- [ ] AC-038-06-01: Tests for `extract_imports()` with module-level and local imports
- [ ] AC-038-06-02: Tests for `validate_file()` with compliant and violating files
- [ ] AC-038-06-03: Tests for `validate_directory()` with mixed compliance
- [ ] AC-038-06-04: Tests for `SyntaxError` handling (graceful skip)
- [ ] AC-038-06-05: Tests for boundary rule matching with wildcard patterns
- [ ] AC-038-06-06: Tests for composition root exemption
- [ ] AC-038-06-07: Tests for dynamic import detection
- [ ] AC-038-06-08: Coverage >= 90% for `src/infrastructure/internal/enforcement/`

### 1.4 Testing Strategy

| Level | Tests | Location | Focus |
|-------|-------|----------|-------|
| Unit | 15-20 tests | `tests/unit/enforcement/` | Validator logic, rule matching, edge cases |
| Integration | 5-8 tests | `tests/architecture/test_layer_boundaries.py` | Real codebase boundary validation |
| E2E | 2-3 tests | `tests/e2e/test_enforcement_cli.py` | CLI entry point, exit codes, output format |
| Platform | 3 tests | CI matrix (macOS, Linux, Windows) | Cross-platform `ast.parse()` behavior |

### 1.5 Risk Mitigations

| Risk ID | Risk | RPN | Mitigation | Residual |
|---------|------|-----|------------|----------|
| FM-038-02 | Dynamic imports via `importlib`/`__import__` bypass static AST | 98 | Supplementary `grep`-based detection for `importlib.import_module` and `__import__` patterns; flag as warnings | 48 |
| FM-038-04 | New bounded context directories not covered by hardcoded paths | 72 | Use dynamic directory discovery from `src/` root: `[d for d in src.iterdir() if d.is_dir() and (d / 'domain').exists()]` | 24 |
| FM-038-05 | Validation runs only at test time, not at write time | 64 | V-044 pre-commit integration runs validation before commit; V-045 CI runs as ultimate backstop | 16 |
| FM-038-NEW | False positives from TYPE_CHECKING imports | 36 | `extract_imports()` distinguishes `TYPE_CHECKING` conditional imports; these are exempted from boundary checks | 12 |

### 1.6 Platform Portability

| Platform | Notes |
|----------|-------|
| **macOS** | Primary development platform. `ast` module is stdlib. No platform-specific code. |
| **Windows** | `Path` operations use `pathlib` which handles `\` vs `/` automatically. `ast.parse()` handles CRLF line endings. File encoding: specify `encoding='utf-8'` in `open()` calls. |
| **Linux** | CI primary platform (GitHub Actions runners). No platform-specific considerations. |

**Platform-specific code paths:** None. The implementation uses only `ast`, `pathlib`, `dataclasses`, and `sys` -- all platform-agnostic stdlib modules.

### 1.7 Token Budget Impact

**Zero.** V-038 executes as an external Python process. No content is added to the LLM context window. The boundary rules are encoded in Python code (`boundary_rules.py`), not in `.claude/rules/` files.

**Impact on the 25,700 token envelope:** No change. V-038 does not add to or modify the rules files.

---

## Vector 2: V-045 CI Pipeline Enforcement

### 2.1 Vector Profile

| Attribute | Value |
|-----------|-------|
| **ID** | V-045 |
| **Name** | CI Pipeline Enforcement |
| **WCS** | 4.86 (second highest in catalog) |
| **Tier** | Tier 1: Implement Immediately |
| **Family** | F5: Structural/Code-Level Enforcement |
| **Enforcement Layer** | L5 (Post-Hoc Verification) |
| **Scores** | CRR=5, EFF=5, PORT=5, TOK=5, BYP=5, COST=3, MAINT=5 |
| **TRL** | 7 -- Jerry already has a comprehensive CI pipeline at `.github/workflows/ci.yml` |

**What it enforces:** All code quality standards checked deterministically before merge. The CI pipeline is the ultimate backstop that catches any violation that slipped through pre-commit hooks, developer testing, and LLM sessions. It runs linting (ruff), type checking (pyright), security scanning (pip-audit), and the full test suite including architecture tests.

**Why it is top priority:** Near-impossible to bypass (requires admin access to override branch protection). Catches everything that all runtime layers missed. The existing CI pipeline already handles linting, type checking, security, and testing -- the enhancement needed is to add explicit architecture enforcement steps and required status checks.

**Current State Assessment:** Jerry already has a mature CI pipeline at `.github/workflows/ci.yml` with 9 jobs (lint, type-check, security, plugin-validation, cli-integration, test-pip, test-uv, version-sync, ci-success). The architecture tests in `tests/architecture/` already run as part of the `test-pip` and `test-uv` jobs. What is missing:

1. **No dedicated architecture enforcement job** -- architecture tests run as part of the general test suite but are not surfaced as a distinct, required check
2. **No branch protection rules** enforcing CI passage before merge
3. **No explicit enforcement reporting** -- architecture violations are buried in general test output

### 2.2 Implementation Design

#### Technical Approach

The implementation enhances the existing CI pipeline with three changes:

1. **New CI job: `architecture-enforcement`** -- runs architecture tests as a dedicated, visible job
2. **Branch protection configuration** -- documentation and scripts for enabling required status checks
3. **Architecture violation reporting** -- structured output for architecture test failures

```
EXECUTION FLOW:

Developer pushes branch / opens PR
       │
       ├──► [existing] lint job ──────────────► ruff check/format
       ├──► [existing] type-check job ────────► pyright
       ├──► [existing] security job ──────────► pip-audit
       ├──► [existing] test-pip/test-uv jobs ─► pytest (includes arch tests)
       │
       ├──► [NEW] architecture-enforcement job
       │         │
       │         ├──► Layer boundary tests (V-038)
       │         ├──► Composition root exclusivity
       │         ├──► Bounded context isolation
       │         └──► Dynamic import detection
       │
       └──► [existing] ci-success job ────────► Gate (all must pass)
                 │
                 └──► [NEW] includes architecture-enforcement
```

#### Integration Points in Jerry's Architecture

| Component | Location | Change |
|-----------|----------|--------|
| CI workflow | `.github/workflows/ci.yml` | Add `architecture-enforcement` job |
| CI success gate | `.github/workflows/ci.yml` (`ci-success` job) | Add `architecture-enforcement` to `needs` |
| Branch protection | GitHub repository settings | Document required status checks |
| Architecture tests | `tests/architecture/` | Already covered by V-038 tasks |

#### File Locations for New/Modified Code

| File | Action | Purpose |
|------|--------|---------|
| `.github/workflows/ci.yml` | MODIFY | Add architecture-enforcement job; update ci-success gate |
| `docs/governance/BRANCH_PROTECTION.md` | CREATE | Document branch protection configuration |
| `scripts/check_architecture.sh` | CREATE | Wrapper script for architecture test invocation |

#### Dependencies on Existing Code

| Dependency | Location | Nature |
|------------|----------|--------|
| Existing CI pipeline | `.github/workflows/ci.yml` | Extend with new job |
| Architecture tests | `tests/architecture/` | Executed by new CI job |
| AST validator (V-038) | `src/infrastructure/internal/enforcement/` | Tests invoke the validator |
| pytest markers | `pytest.ini` / `pyproject.toml` | `@pytest.mark.architecture` marker |

### 2.3 Implementation Tasks

#### TASK-045-01: Add Architecture Enforcement CI Job

**Description:** Add a dedicated `architecture-enforcement` job to `.github/workflows/ci.yml` that runs architecture-specific tests as a visible, independent check.

**Estimated Effort:** 2 hours

**Dependencies:** V-038 TASK-038-05 (comprehensive boundary tests exist)

**Deliverables:**

```yaml
# Addition to .github/workflows/ci.yml

  # ===========================================================================
  # Architecture Enforcement (V-038 + V-043)
  # ===========================================================================
  architecture-enforcement:
    name: Architecture Boundaries
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"

      - name: Set up Python
        run: uv python install 3.14

      - name: Install dependencies
        run: uv sync --extra dev

      - name: Run architecture boundary tests
        run: |
          uv run pytest tests/architecture/ \
            -v \
            --tb=long \
            --junitxml=architecture-results.xml \
            -m "architecture or not architecture"

      - name: Run standalone boundary validator
        run: |
          uv run python -m src.infrastructure.internal.enforcement --json > boundary-report.json || true
          if [ -f boundary-report.json ]; then
            echo "=== Architecture Boundary Report ==="
            uv run python -c "
            import json
            with open('boundary-report.json') as f:
                report = json.load(f)
            violations = report.get('violations', [])
            if violations:
                print(f'FAIL: {len(violations)} boundary violations found')
                for v in violations:
                    print(f'  {v[\"file_path\"]}:{v[\"line_number\"]} - {v[\"rule_violated\"]}')
                exit(1)
            else:
                print('PASS: No boundary violations detected')
            "
          fi

      - name: Upload architecture results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: architecture-results
          path: |
            architecture-results.xml
            boundary-report.json
```

**Acceptance Criteria:**
- [ ] AC-045-01-01: `architecture-enforcement` job runs on all pushes and PRs
- [ ] AC-045-01-02: Job runs architecture tests from `tests/architecture/` directory
- [ ] AC-045-01-03: Job runs standalone validator and produces structured JSON report
- [ ] AC-045-01-04: Job fails (exit code 1) if any boundary violation is detected
- [ ] AC-045-01-05: Job produces JUnit XML artifact for test result reporting
- [ ] AC-045-01-06: Job execution time is under 2 minutes

#### TASK-045-02: Update CI Success Gate

**Description:** Update the `ci-success` job to include `architecture-enforcement` as a required predecessor.

**Estimated Effort:** 15 minutes

**Dependencies:** TASK-045-01

**Deliverables:**

```yaml
# Modification to ci-success job in .github/workflows/ci.yml

  ci-success:
    name: CI Success
    runs-on: ubuntu-latest
    needs: [lint, type-check, security, plugin-validation, cli-integration,
            test-pip, test-uv, version-sync, architecture-enforcement]  # Added
    if: always()
    steps:
      - name: Check all jobs passed
        run: |
          # ... existing checks ...
          if [[ "${{ needs.architecture-enforcement.result }}" != "success" ]]; then
            echo "Architecture enforcement failed"
            exit 1
          fi
          # ... rest of checks ...
```

**Acceptance Criteria:**
- [ ] AC-045-02-01: `ci-success` job depends on `architecture-enforcement`
- [ ] AC-045-02-02: CI fails if architecture enforcement fails, even if all other jobs pass
- [ ] AC-045-02-03: Architecture enforcement status is displayed in the job summary

#### TASK-045-03: Document Branch Protection Configuration

**Description:** Create documentation for configuring GitHub branch protection rules to require the CI pipeline to pass before merging PRs.

**Estimated Effort:** 1 hour

**Dependencies:** TASK-045-01, TASK-045-02

**Deliverables:**
- `docs/governance/BRANCH_PROTECTION.md` -- step-by-step guide for enabling branch protection

**Acceptance Criteria:**
- [ ] AC-045-03-01: Document covers enabling required status checks for `ci-success` job
- [ ] AC-045-03-02: Document covers requiring PR reviews before merge
- [ ] AC-045-03-03: Document covers disabling force-push to `main`
- [ ] AC-045-03-04: Document includes emergency merge process for admin overrides

#### TASK-045-04: Create Architecture Check Wrapper Script

**Description:** Create a convenience script `scripts/check_architecture.sh` for local invocation of the full architecture enforcement suite, matching the CI job behavior.

**Estimated Effort:** 30 minutes

**Dependencies:** TASK-038-05

**Deliverables:**

```bash
#!/usr/bin/env bash
# scripts/check_architecture.sh
# Runs the full architecture enforcement suite locally.
# Mirrors the CI architecture-enforcement job.

set -euo pipefail

echo "=== Jerry Architecture Enforcement ==="
echo ""

echo "[1/2] Running architecture tests..."
uv run pytest tests/architecture/ -v --tb=long

echo ""
echo "[2/2] Running standalone boundary validator..."
uv run python -m src.infrastructure.internal.enforcement

echo ""
echo "=== All architecture checks passed ==="
```

**Acceptance Criteria:**
- [ ] AC-045-04-01: Script runs architecture tests and standalone validator
- [ ] AC-045-04-02: Script exits with non-zero code on any failure
- [ ] AC-045-04-03: Script is executable (`chmod +x`)
- [ ] AC-045-04-04: Script works on macOS and Linux (uses `/usr/bin/env bash`)

### 2.4 Testing Strategy

| Level | Tests | Location | Focus |
|-------|-------|----------|-------|
| Unit | N/A | -- | CI configuration is declarative YAML, not testable code |
| Integration | 2-3 tests | Manual CI pipeline run | Verify new job executes and gates correctly |
| E2E | 1 test | PR with deliberate violation | Verify CI blocks merge on architecture failure |
| Platform | Implicit | CI matrix (ubuntu-latest) | GitHub Actions standard runner |

**Validation approach:** Because CI configuration is declarative (YAML), testing consists of:
1. Push a branch with the updated CI and verify the `architecture-enforcement` job appears and runs
2. Create a PR with a deliberate architecture violation (e.g., domain file importing infrastructure) and verify CI fails
3. Fix the violation and verify CI passes

### 2.5 Risk Mitigations

| Risk ID | Risk | RPN | Mitigation | Residual |
|---------|------|-----|------------|----------|
| FM-045-01 | CI configured as optional; developers bypass by merging without checks | 36 | Configure `ci-success` as required status check in branch protection rules; document in BRANCH_PROTECTION.md | 12 |
| FM-045-02 | Environment differences between local and CI cause false positives/negatives | 30 | Pin Python version (3.14) and dependency versions in CI; use `uv sync` for reproducible installs | 12 |
| FM-045-04 | Admin override merges code that fails CI | 24 | Document emergency merge process; add post-merge CI run that validates `main` branch; audit trail via PR comments | 12 |
| FM-045-NEW | Architecture enforcement job adds CI runtime; slows feedback | 24 | Architecture tests typically run in under 30 seconds; parallel with other jobs; does not affect critical path | 8 |

### 2.6 Platform Portability

| Platform | Notes |
|----------|-------|
| **macOS** | `scripts/check_architecture.sh` works natively. CI runs on GitHub Actions (Linux). |
| **Windows** | Shell script requires Git Bash or WSL. Provide PowerShell equivalent or document `uv run pytest tests/architecture/ -v` as the Windows alternative. |
| **Linux** | Primary CI execution platform. No platform-specific considerations. |

**Platform-specific code paths:** The CI workflow itself runs on `ubuntu-latest`. The wrapper script uses `/usr/bin/env bash` which works on macOS and Linux. Windows users should invoke pytest directly via `uv run pytest tests/architecture/ -v`.

### 2.7 Token Budget Impact

**Zero.** CI execution happens outside the LLM context window entirely. No content is added to rules or context.

**Impact on the 25,700 token envelope:** No change.

---

## Vector 3: V-044 Pre-commit Hook Validation

### 3.1 Vector Profile

| Attribute | Value |
|-----------|-------|
| **ID** | V-044 |
| **Name** | Pre-commit Hook Validation |
| **WCS** | 4.80 (tied for third highest) |
| **Tier** | Tier 1: Implement Immediately |
| **Family** | F5: Structural/Code-Level Enforcement |
| **Enforcement Layer** | L5 (Post-Hoc Verification) |
| **Scores** | CRR=5, EFF=5, PORT=5, TOK=5, BYP=4, COST=4, MAINT=4 |
| **TRL** | 7 -- Jerry already has a mature `.pre-commit-config.yaml` |

**What it enforces:** Code quality gates before code enters the git repository. Pre-commit hooks provide immediate developer feedback at commit time, catching violations before they reach CI. This includes linting (ruff), type checking (pyright), testing (pytest), and -- with V-038 integration -- architecture boundary validation.

**Why it is top priority:** Provides the fastest feedback loop in the L5 layer. While CI is the ultimate backstop, pre-commit hooks catch violations immediately, saving the developer the round-trip to CI. The `--no-verify` bypass is mitigated by CI (V-045).

**Current State Assessment:** Jerry already has a comprehensive pre-commit configuration with:
- File hygiene hooks (trailing whitespace, EOF, YAML, large files, merge conflicts, private keys)
- Ruff linting and formatting
- Pyright type checking
- Full pytest suite
- Plugin manifest validation
- Version sync validation
- Commitizen conventional commit linting
- pip-audit security scanning (pre-push)

What is missing:
1. **No dedicated AST boundary check hook** -- architecture violations are caught by pytest (which runs as a pre-commit hook) but without targeted error messages
2. **No incremental architecture checking** -- changed-files-only validation for faster feedback

### 3.2 Implementation Design

#### Technical Approach

The implementation adds a dedicated architecture boundary check hook to the existing `.pre-commit-config.yaml`. This hook validates only changed Python files against the boundary rules, providing fast, targeted feedback.

```
EXECUTION FLOW:

Developer runs `git commit`
       │
       ├──► [existing] trailing-whitespace ──► PASS/FAIL
       ├──► [existing] ruff lint + format ──► PASS/FAIL
       ├──► [existing] pyright ─────────────► PASS/FAIL
       │
       ├──► [NEW] architecture-boundaries
       │         │
       │         ├──► Identify changed .py files
       │         ├──► Run AST boundary validator on changed files only
       │         └──► Report violations with file:line format
       │
       ├──► [existing] pytest ──────────────► PASS/FAIL (includes arch tests)
       ├──► [existing] validate-plugin-manifests
       ├──► [existing] version-sync
       └──► [existing] commitizen
```

**Design decision: Why a separate hook instead of relying on pytest?**

The pytest hook already runs architecture tests, but:
1. **Performance:** pytest runs the entire test suite (~80+ tests). A dedicated hook runs only the boundary validator on changed files, completing in under 2 seconds vs. 15+ seconds for the full suite.
2. **Targeted feedback:** The boundary validator produces specific `file:line: violation` messages, matching the format developers expect from linters. pytest produces test assertion failures which require more cognitive effort to parse.
3. **Fail-fast:** The boundary hook runs before pytest, providing earlier feedback if the developer introduced an architecture violation.

#### Integration Points

| Component | Location | Change |
|-----------|----------|--------|
| Pre-commit config | `.pre-commit-config.yaml` | Add `architecture-boundaries` hook |
| AST validator | `src/infrastructure/internal/enforcement/ast_boundary_validator.py` | Consumed by hook |
| CLI entry point | `src/infrastructure/internal/enforcement/__main__.py` | Invoked by hook |

#### File Locations for New/Modified Code

| File | Action | Purpose |
|------|--------|---------|
| `.pre-commit-config.yaml` | MODIFY | Add architecture-boundaries hook |
| `src/infrastructure/internal/enforcement/__main__.py` | USED | Already created in V-038 TASK-038-03 |

### 3.3 Implementation Tasks

#### TASK-044-01: Add Architecture Boundary Pre-commit Hook

**Description:** Add a dedicated architecture boundary check to `.pre-commit-config.yaml` that validates changed Python files against Jerry's hexagonal architecture rules.

**Estimated Effort:** 1 hour

**Dependencies:** V-038 TASK-038-01, TASK-038-02, TASK-038-03 (AST validator library and CLI)

**Deliverables:**

```yaml
# Addition to .pre-commit-config.yaml, after ruff hooks and before pytest

  # =============================================================================
  # Architecture Boundary Enforcement (V-038 + V-044)
  # =============================================================================
  - repo: local
    hooks:
      - id: architecture-boundaries
        name: Architecture boundary check
        entry: uv run python -m src.infrastructure.internal.enforcement
        language: system
        types: [python]
        # Only check files in src/ -- test files are not subject to
        # architecture boundary rules
        files: ^src/
        pass_filenames: true
        stages: [pre-commit]
```

**Acceptance Criteria:**
- [ ] AC-044-01-01: Hook runs on `git commit` for changed Python files in `src/`
- [ ] AC-044-01-02: Hook receives changed file paths as arguments (pass_filenames: true)
- [ ] AC-044-01-03: Hook exits 0 on compliant files, exits 1 on violations
- [ ] AC-044-01-04: Hook runs before pytest (ordering in YAML)
- [ ] AC-044-01-05: Hook only validates files in `src/` (not `tests/`, `scripts/`)
- [ ] AC-044-01-06: Hook completes in under 5 seconds for typical commits (1-10 files)

#### TASK-044-02: Add Changed-Files Mode to Validator CLI

**Description:** Enhance `src/infrastructure/internal/enforcement/__main__.py` to accept file paths as positional arguments, enabling the pre-commit hook to pass only changed files.

**Estimated Effort:** 30 minutes

**Dependencies:** V-038 TASK-038-03

**Deliverables:**

The `__main__.py` already supports path arguments from TASK-038-03. This task ensures it works correctly when invoked with individual file paths (as pre-commit does) rather than directory paths.

**Acceptance Criteria:**
- [ ] AC-044-02-01: `uv run python -m src.infrastructure.internal.enforcement src/domain/foo.py src/app/bar.py` validates only those two files
- [ ] AC-044-02-02: Non-existent file paths are skipped with a warning (not an error)
- [ ] AC-044-02-03: Non-Python files are silently ignored
- [ ] AC-044-02-04: Mixed file and directory arguments are supported

#### TASK-044-03: Performance Validation

**Description:** Measure and validate pre-commit hook performance to ensure the architecture boundary check does not significantly slow down the commit workflow.

**Estimated Effort:** 30 minutes

**Dependencies:** TASK-044-01, TASK-044-02

**Deliverables:**
- Performance benchmark results documented in commit message
- Performance budget: under 5 seconds for 10-file commits

**Acceptance Criteria:**
- [ ] AC-044-03-01: Single file validation completes in under 500ms
- [ ] AC-044-03-02: 10-file validation completes in under 3 seconds
- [ ] AC-044-03-03: Full `src/` directory validation completes in under 10 seconds
- [ ] AC-044-03-04: No measurable impact on `git commit` for non-Python changes

#### TASK-044-04: Update Pre-commit Installation Documentation

**Description:** Update the pre-commit installation documentation to mention the architecture boundary hook and any prerequisites.

**Estimated Effort:** 15 minutes

**Dependencies:** TASK-044-01

**Deliverables:**
- Updated comments in `.pre-commit-config.yaml` header
- Updated `docs/INSTALLATION.md` if needed

**Acceptance Criteria:**
- [ ] AC-044-04-01: Installation instructions mention the architecture boundary hook
- [ ] AC-044-04-02: `uv sync` installs all dependencies needed for the hook
- [ ] AC-044-04-03: `--no-verify` escape hatch is documented with explanation that CI catches violations

### 3.4 Testing Strategy

| Level | Tests | Location | Focus |
|-------|-------|----------|-------|
| Unit | Covered by V-038 | `tests/unit/enforcement/` | Validator logic already tested |
| Integration | 2 tests | Manual | Run `pre-commit run --all-files` and verify hook output |
| E2E | 2 tests | Manual | Commit compliant code (passes); commit violating code (blocked) |
| Platform | 2 tests | macOS + Linux | Verify hook works on both platforms |

**Validation approach:**
1. Run `pre-commit run architecture-boundaries --all-files` and verify all existing code passes
2. Temporarily add an import violation to a domain file, run `git commit`, and verify the hook blocks
3. Measure execution time with `time pre-commit run architecture-boundaries --all-files`

### 3.5 Risk Mitigations

| Risk ID | Risk | RPN | Mitigation | Residual |
|---------|------|-----|------------|----------|
| FM-044-01 | `--no-verify` bypass skips all pre-commit hooks | 63 | CI (V-045) runs all the same checks as a mandatory backup; `--no-verify` is documented as emergency-only in `.pre-commit-config.yaml` header | 21 |
| FM-044-03 | Slow hooks frustrate developers, encouraging `--no-verify` | 36 | Changed-files-only validation keeps execution under 3 seconds; architecture hook runs before full pytest suite | 12 |
| FM-044-04 | Hooks not installed on fresh clones | 60 | `make setup` target runs `uv sync && uv run pre-commit install`; CI catches violations from contributors who skip local hooks | 20 |
| FM-044-NEW | Pre-commit framework version incompatibility | 18 | Pin `pre-commit` version in `pyproject.toml` dev dependencies; annual version review | 6 |

### 3.6 Platform Portability

| Platform | Notes |
|----------|-------|
| **macOS** | Primary development platform. Pre-commit framework works natively. |
| **Windows** | Pre-commit framework works on Windows with Python. The `entry` command uses `uv run python -m src.infrastructure.internal.enforcement` which is platform-agnostic. Git hooks use the shell configured by Git for Windows. |
| **Linux** | CI primary platform. No platform-specific considerations. |

**Platform-specific code paths:** None. The pre-commit hook invokes the Python validator via `uv run python -m src.infrastructure.internal.enforcement`, which is platform-agnostic.

### 3.7 Token Budget Impact

**Zero.** Pre-commit hooks execute as external processes at commit time. No content is added to the LLM context window.

**Impact on the 25,700 token envelope:** No change.

---

## Cross-Vector Integration

### Defense-in-Depth Stack

The three vectors compose into a layered defense-in-depth stack that provides enforcement at two architectural layers:

```
TEMPORAL ENFORCEMENT PIPELINE (for architecture boundary violations)
====================================================================

Time ──────────────────────────────────────────────────────────►

Developer     Pre-commit      CI Pipeline
writes code   (V-044)         (V-045)
    │            │                │
    │   ┌────────┴────────┐      │
    │   │ AST Boundary    │      │
    │   │ Check (V-038)   │      │
    │   │                 │      │
    │   │ Changed files   │      │
    │   │ only -- fast    │      │
    │   └────────┬────────┘      │
    │            │               │
    │   ┌────────┴────────┐      │
    │   │ Full pytest     │      │
    │   │ (includes arch  │      │
    │   │  tests using    │      │
    │   │  V-038 library) │      │
    │   └────────┬────────┘      │
    │            │               │
    │     git commit             │
    │            │               │
    │     git push ──────────────┤
    │                            │
    │                   ┌────────┴────────┐
    │                   │ Architecture    │
    │                   │ Enforcement Job │
    │                   │ (V-038 library  │
    │                   │  + full tests)  │
    │                   └────────┬────────┘
    │                            │
    │                   ┌────────┴────────┐
    │                   │ CI Success Gate │
    │                   │ (must pass to   │
    │                   │  merge PR)      │
    │                   └─────────────────┘
```

### Execution Order and Data Flow

| Step | Timing | Vector | Input | Output | Fallback |
|------|--------|--------|-------|--------|----------|
| 1 | `git commit` | V-044 (pre-commit) | Changed `.py` files in `src/` | PASS/FAIL per file | If bypassed via `--no-verify`, step 3 catches violations |
| 2 | `git commit` | V-044 (pytest in pre-commit) | Full `tests/architecture/` suite | PASS/FAIL per test | If bypassed, step 3 catches violations |
| 3 | `git push` + PR | V-045 (CI) | Full repository checkout | PASS/FAIL per job; blocks merge | Admin override required to bypass |

**Key property:** Each step uses the same underlying V-038 validator library, ensuring consistent enforcement rules across all integration points. A violation detected by pre-commit would also be detected by CI; the difference is feedback latency.

### Shared Infrastructure

| Component | Used By | Location |
|-----------|---------|----------|
| `ASTBoundaryValidator` class | V-044 (pre-commit), V-045 (CI), architecture tests | `src/infrastructure/internal/enforcement/ast_boundary_validator.py` |
| `BoundaryRule` definitions | All three vectors | `src/infrastructure/internal/enforcement/boundary_rules.py` |
| CLI entry point | V-044 (pre-commit hook), V-045 (CI wrapper) | `src/infrastructure/internal/enforcement/__main__.py` |
| Architecture test suite | V-044 (pytest hook), V-045 (CI job) | `tests/architecture/` |

### Implementation Order

The three vectors should be implemented in this sequence:

```
Phase 1: V-038 (AST Validator Library)
    │
    ├── TASK-038-01: Core library
    ├── TASK-038-02: Boundary rules
    ├── TASK-038-03: CLI entry point
    ├── TASK-038-04: Refactor existing tests
    ├── TASK-038-05: Comprehensive boundary tests
    └── TASK-038-06: Unit tests
    │
Phase 2: V-044 (Pre-commit) -- depends on V-038
    │
    ├── TASK-044-01: Pre-commit hook config
    ├── TASK-044-02: Changed-files mode
    ├── TASK-044-03: Performance validation
    └── TASK-044-04: Documentation
    │
Phase 3: V-045 (CI Enhancement) -- depends on V-038
    │
    ├── TASK-045-01: CI architecture job
    ├── TASK-045-02: CI success gate update
    ├── TASK-045-03: Branch protection docs
    └── TASK-045-04: Wrapper script
```

**Note:** V-044 and V-045 are independent of each other and could be implemented in parallel after V-038 is complete. The sequential ordering above is recommended because pre-commit provides the faster developer feedback loop, making it a higher priority for developer experience.

### E2E Defense-in-Depth Integration Testing

The three vectors form a defense-in-depth stack where each layer compensates for the previous layer's bypass scenario. The following E2E test scenarios validate that the stack functions as an integrated defense system, not merely three independent checks:

**Scenario 1: Pre-commit bypass via --no-verify (validates V-045 compensates for V-044 bypass)**

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Introduce a deliberate architecture violation in `src/domain/` (e.g., `from src.infrastructure.adapters import X`) | Violation present in working tree |
| 2 | Commit with `git commit --no-verify -m "test: deliberate violation"` | Commit succeeds (pre-commit bypassed) |
| 3 | Push to remote and open PR | PR created |
| 4 | Observe CI `architecture-enforcement` job | Job FAILS with specific violation message referencing the boundary rule |
| 5 | Verify PR merge is blocked | PR cannot be merged; `ci-success` status check fails |

**Scenario 2: Pre-commit catches violation before CI (validates V-044 provides early feedback)**

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Introduce a deliberate import violation in `src/application/` importing from `src/interface/` | Violation present in staged files |
| 2 | Run `git commit -m "test: deliberate violation"` (without --no-verify) | Commit BLOCKED by `architecture-boundaries` pre-commit hook |
| 3 | Verify error message | Output shows `file:line: violation` format with specific boundary rule |
| 4 | Verify no commit was created | `git log -1` shows previous commit, not the blocked one |

**Scenario 3: New bounded context discovery (validates V-038 dynamic scanning)**

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Create a new bounded context directory `src/new_context/domain/` with a Python file | New directory exists |
| 2 | Add an import violation in the new directory (e.g., importing from `src/infrastructure/`) | Violation present |
| 3 | Run `uv run python -m src.infrastructure.internal.enforcement src/new_context/` | Validator detects the violation WITHOUT any configuration change (dynamic discovery) |
| 4 | Run `git commit` with the violation | Pre-commit hook catches the violation |
| 5 | Push regardless (--no-verify) | CI catches the violation |

**Scenario 4: Clean code passes all layers (validates no false positives in integrated stack)**

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Write a new compliant file in `src/domain/entities/` that imports only from `src/domain/` and stdlib | Compliant code |
| 2 | Run `uv run python -m src.infrastructure.internal.enforcement src/domain/entities/new_file.py` | PASS: no violations |
| 3 | Run `git commit` | Pre-commit hook passes; commit succeeds |
| 4 | Push and open PR | CI `architecture-enforcement` job passes |
| 5 | Merge PR | PR merges successfully |

**Implementation note:** These E2E scenarios should be documented as manual integration test procedures initially. Once the V-038/V-044/V-045 stack is operational, selected scenarios (particularly Scenario 3 and 4) can be automated as CI-level integration tests that run against a test repository or test fixtures.

---

## Consolidated Risk Register

### All Risks Across 3 Vectors

| Risk ID | Vector | Risk Description | RPN | Severity | Mitigation | Residual RPN |
|---------|--------|------------------|-----|----------|------------|-------------|
| FM-038-02 | V-038 | Dynamic imports via `importlib`/`__import__` bypass AST | 98 | MEDIUM | Grep-based detection; flag as warning | 48 |
| FM-044-01 | V-044 | `--no-verify` bypasses all pre-commit hooks | 63 | MEDIUM | CI (V-045) as mandatory backup | 21 |
| FM-044-04 | V-044 | Hooks not installed on fresh clones | 60 | MEDIUM | `make setup`; CI catches violations | 20 |
| FM-038-04 | V-038 | New directories not covered | 72 | MEDIUM | Dynamic directory discovery | 24 |
| FM-038-05 | V-038 | Validation runs only at test time | 64 | MEDIUM | V-044 pre-commit + V-045 CI coverage | 16 |
| FM-038-NEW | V-038 | False positives from TYPE_CHECKING imports | 36 | LOW | Exempt TYPE_CHECKING conditional imports | 12 |
| FM-044-03 | V-044 | Slow hooks encourage `--no-verify` | 36 | LOW | Changed-files-only; under 3 seconds | 12 |
| FM-045-01 | V-045 | CI configured as optional | 36 | LOW | Required status checks in branch protection | 12 |
| FM-045-02 | V-045 | Environment differences cause inconsistencies | 30 | LOW | Pin versions; `uv sync` reproducibility | 12 |
| FM-045-04 | V-045 | Admin override merges failing code | 24 | LOW | Emergency merge docs; post-merge validation | 12 |
| FM-045-NEW | V-045 | Architecture job adds CI runtime | 24 | LOW | Parallel execution; under 2 minutes | 8 |
| FM-044-NEW | V-044 | Pre-commit version incompatibility | 18 | LOW | Pin version; annual review | 6 |

**No HIGH-priority risks (RPN > 200).** All risks are MEDIUM or LOW with effective mitigations.

### Cross-Vector Risk Interaction

The three vectors form a compensating risk network:

- **V-044 bypass (FM-044-01)** is mitigated by **V-045** (CI catches what pre-commit missed)
- **V-045 optional status (FM-045-01)** is mitigated by **branch protection** (administrative control)
- **V-038 dynamic import blind spot (FM-038-02)** is mitigated by **grep-based supplementary detection** across all three integration points

---

## Consolidated Token Budget Impact

| Vector | In-Context Tokens Added | Impact on 25,700 Envelope |
|--------|------------------------|--------------------------|
| V-038 (AST Validator) | 0 | No change |
| V-045 (CI Pipeline) | 0 | No change |
| V-044 (Pre-commit) | 0 | No change |
| **Total** | **0** | **No change** |

All three vectors execute as external processes. They add zero tokens to the LLM context window and have zero impact on the 25,700 token rules envelope. This is a defining property of Family 5 (Structural) enforcement vectors and is the reason they score TOK=5 across the board.

---

## References

### Primary Sources (Direct Input)

| # | Citation | Used For |
|---|----------|----------|
| 1 | TASK-004: Priority Matrix and Composite Scoring v1.0 (EN-402) | Top 3 vector profiles, scoring breakdown, risk references |
| 2 | TASK-005: Enforcement ADR v1.0 (EN-402) | Implementation roadmap phases, architecture decisions, compliance requirements |
| 3 | TASK-003: Architecture Trade Study v1.0 (EN-402) | 5-layer architecture, integration architecture, hexagonal mapping, hook integration points |
| 4 | TASK-009: Revised Unified Enforcement Vector Catalog v1.1 (EN-401) | Authoritative vector descriptions, FMEA references, TRL assessments |

### Jerry Codebase Sources

| # | Citation | Used For |
|---|----------|----------|
| 5 | `tests/architecture/test_composition_root.py` | Existing AST analysis implementation (lines 18-78); refactoring target |
| 6 | `tests/architecture/test_config_boundaries.py` | Existing layer boundary tests; refactoring target |
| 7 | `tests/architecture/test_session_hook_architecture.py` | Existing hook isolation tests; refactoring target |
| 8 | `scripts/pre_tool_use.py` | Existing PreToolUse hook infrastructure; integration pattern reference |
| 9 | `.pre-commit-config.yaml` | Existing pre-commit configuration; enhancement target |
| 10 | `.github/workflows/ci.yml` | Existing CI pipeline; enhancement target |
| 11 | `.claude/rules/architecture-standards.md` | Authoritative boundary rules encoded in V-038 |
| 12 | `src/` directory structure | Dynamic bounded context discovery for V-038 |

### Downstream Consumers

| # | Citation | Relationship |
|---|----------|-------------|
| 13 | TASK-007 (ps-critic adversarial review) | Stress-tests these execution plans for completeness and feasibility |
| 14 | EN-403 (Rule Optimization) | Uses V-038 to validate optimized rules maintain boundary compliance |
| 15 | EN-404 (Structural Enforcement Implementation) | Implements these execution plans; primary consumer |
| 16 | EN-405 (Process Enforcement Implementation) | Uses V-045 CI as enforcement mechanism for process vectors |

---

**DISCLAIMER:** This execution plan is AI-generated based on analysis of Jerry's existing codebase and the EN-402 research program. All implementation tasks require human review and professional engineering judgment. Task effort estimates are approximate and should be validated against actual development velocity.

---

*Agent: ps-architect (Claude Opus 4.6)*
*Date: 2026-02-13*
*Parent: EN-402 Enforcement Priority Analysis & Decision*
*Status: COMPLETE (pending adversarial review, TASK-007)*
*Quality Target: >= 0.92*
*Consumers: TASK-007 (adversarial review), EN-404 (implementation)*
