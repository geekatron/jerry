# TASK-008: CI/CD Non-Regression Testing Specifications

<!--
TEMPLATE: Task Deliverable
VERSION: 1.0.0
ENABLER: EN-406
AC: AC-9
CREATED: 2026-02-13 (ps-validator-406)
PURPOSE: CI/CD non-regression test specifications for enforcement mechanisms
-->

> **Type:** deliverable
> **Status:** complete
> **Parent:** EN-406-integration-testing-validation
> **AC Mapping:** AC-9 (CI/CD non-regression tests pass)
> **Agent:** ps-validator-406
> **Created:** 2026-02-13

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | CI/CD testing scope and objectives |
| [Existing Pipeline Inventory](#existing-pipeline-inventory) | Current CI/CD pipeline components |
| [Non-Regression Tests](#non-regression-tests) | Tests verifying no pipeline breakage |
| [Enforcement in CI/CD](#enforcement-in-cicd) | How enforcement integrates with CI/CD |
| [Rollback Strategy](#rollback-strategy) | Recovery plan if enforcement breaks CI/CD |
| [Requirements Traceability](#requirements-traceability) | Test-to-requirement mapping |
| [References](#references) | Source documents |

---

## Overview

This document specifies non-regression tests ensuring that enforcement mechanisms do not break existing CI/CD pipelines, development workflows, or tool integrations. NFC-3 (FEAT-005) mandates: "No CI/CD breakage from enforcement mechanisms."

### Objectives

1. Verify enforcement hooks do not interfere with CI/CD pipeline execution.
2. Verify rule files do not cause Claude Code session failures.
3. Verify enforcement does not prevent valid code commits.
4. Verify enforcement does not block valid test execution.
5. Verify enforcement can be disabled/bypassed for CI/CD contexts where appropriate.

### Test Summary

| Category | Test Count | ID Range |
|----------|------------|----------|
| Pipeline Non-Regression | 8 | TC-CICD-001 through TC-CICD-008 |
| Development Workflow | 6 | TC-DEVW-001 through TC-DEVW-006 |
| Tool Integration | 4 | TC-TOOL-001 through TC-TOOL-004 |
| **Total** | **18** | |

---

## Existing Pipeline Inventory

### Current CI/CD Components

| Component | Location | Purpose | Enforcement Impact |
|-----------|----------|---------|-------------------|
| GitHub Actions workflows | `.github/workflows/` | Automated testing | Should not be affected |
| Pre-commit hooks | `.pre-commit-config.yaml` | Code quality gates | Must coexist with enforcement hooks |
| pytest test suite | `tests/` | Automated testing | Must remain runnable |
| ruff linting | `pyproject.toml` | Code style | Must not conflict with rule files |
| mypy type checking | `pyproject.toml` | Type safety | Must not conflict |
| UV dependency management | `pyproject.toml` | Python deps | Must work with enforcement |

### Enforcement Components in CI/CD Context

| Component | CI/CD Behavior | Notes |
|-----------|---------------|-------|
| `.claude/rules/*.md` | Not loaded in CI/CD (Claude Code only) | No CI/CD impact |
| `hooks/user-prompt-submit.py` | Not invoked in CI/CD | Claude Code hook only |
| `hooks/pre-tool-use.py` | Not invoked in CI/CD | Claude Code hook only |
| `scripts/session_start_hook.py` | Not invoked in CI/CD | Claude Code hook only |
| Enforcement engine modules | Importable by tests | Must not break imports |
| `quality-enforcement.md` | Rule file, not code | No CI/CD impact |

---

## Non-Regression Tests

### TC-CICD-001: Test Suite Execution

| Field | Value |
|-------|-------|
| **ID** | TC-CICD-001 |
| **Objective** | Verify complete test suite runs without enforcement-related failures |
| **Steps** | 1. Run `uv run pytest tests/`. 2. Verify all pre-existing tests pass. 3. Verify no new test failures. |
| **Expected Output** | All existing tests pass; no new failures attributable to enforcement |
| **Pass Criteria** | Zero regression failures |
| **Requirements** | NFC-3 |
| **Verification** | Test |

### TC-CICD-002: Linting Non-Regression

| Field | Value |
|-------|-------|
| **ID** | TC-CICD-002 |
| **Objective** | Verify ruff linting passes with enforcement modules |
| **Steps** | 1. Run `uv run ruff check src/`. 2. Verify enforcement engine modules pass linting. |
| **Expected Output** | No new linting errors from enforcement code |
| **Pass Criteria** | Zero new ruff violations |
| **Requirements** | NFC-3 |
| **Verification** | Test |

### TC-CICD-003: Type Checking Non-Regression

| Field | Value |
|-------|-------|
| **ID** | TC-CICD-003 |
| **Objective** | Verify mypy type checking passes with enforcement modules |
| **Steps** | 1. Run `uv run mypy src/`. 2. Verify enforcement engine modules type-check. |
| **Expected Output** | No new type errors from enforcement code |
| **Pass Criteria** | Zero new mypy errors |
| **Requirements** | NFC-3 |
| **Verification** | Test |

### TC-CICD-004: GitHub Actions Workflow

| Field | Value |
|-------|-------|
| **ID** | TC-CICD-004 |
| **Objective** | Verify GitHub Actions workflows run successfully with enforcement in place |
| **Steps** | 1. Push changes including enforcement code. 2. Verify CI pipeline completes. 3. Check for enforcement-related failures. |
| **Expected Output** | CI pipeline passes; no enforcement-related failures |
| **Pass Criteria** | Pipeline green |
| **Requirements** | NFC-3 |
| **Verification** | Test |

### TC-CICD-005: Dependency Installation

| Field | Value |
|-------|-------|
| **ID** | TC-CICD-005 |
| **Objective** | Verify enforcement does not introduce dependency conflicts |
| **Steps** | 1. Run `uv sync`. 2. Verify all dependencies resolve. 3. Check for conflicts. |
| **Expected Output** | Clean dependency resolution |
| **Pass Criteria** | Zero dependency conflicts |
| **Requirements** | NFC-3 |
| **Verification** | Test |

### TC-CICD-006: Build Process

| Field | Value |
|-------|-------|
| **ID** | TC-CICD-006 |
| **Objective** | Verify package builds correctly with enforcement modules |
| **Steps** | 1. Run `uv build` or equivalent. 2. Verify package includes enforcement modules. |
| **Expected Output** | Clean build; enforcement modules included |
| **Pass Criteria** | Build succeeds |
| **Requirements** | NFC-3 |
| **Verification** | Test |

### TC-CICD-007: Pre-Commit Hook Coexistence

| Field | Value |
|-------|-------|
| **ID** | TC-CICD-007 |
| **Objective** | Verify enforcement hooks coexist with pre-commit hooks |
| **Steps** | 1. Verify pre-commit hooks still function. 2. Verify no conflict with Claude Code hooks. |
| **Expected Output** | Both hook systems work independently |
| **Pass Criteria** | No interference between hook systems |
| **Requirements** | NFC-3 |
| **Verification** | Test |

### TC-CICD-008: Architecture Test Non-Regression

| Field | Value |
|-------|-------|
| **ID** | TC-CICD-008 |
| **Objective** | Verify enforcement modules pass architecture tests |
| **Steps** | 1. Run `uv run pytest tests/architecture/`. 2. Verify enforcement modules respect layer boundaries. |
| **Expected Output** | Enforcement modules in `infrastructure/internal/enforcement/` pass boundary checks |
| **Pass Criteria** | Architecture tests pass |
| **Requirements** | NFC-3, REQ-403-080 |
| **Verification** | Test |

---

## Development Workflow Tests

### TC-DEVW-001: Git Commit with Enforcement

| Field | Value |
|-------|-------|
| **ID** | TC-DEVW-001 |
| **Objective** | Verify developers can commit code with enforcement in place |
| **Steps** | 1. Make valid code change. 2. Stage and commit. 3. Verify no enforcement interference. |
| **Expected Output** | Commit succeeds without enforcement blocking |
| **Requirements** | NFC-3 |
| **Verification** | Test |

### TC-DEVW-002: Git Push with Enforcement

| Field | Value |
|-------|-------|
| **ID** | TC-DEVW-002 |
| **Objective** | Verify git push works with enforcement in place |
| **Steps** | 1. Push to remote. 2. Verify no enforcement interference. |
| **Expected Output** | Push succeeds |
| **Requirements** | NFC-3 |
| **Verification** | Test |

### TC-DEVW-003: Branch Operations

| Field | Value |
|-------|-------|
| **ID** | TC-DEVW-003 |
| **Objective** | Verify branch create/switch/merge work with enforcement |
| **Steps** | 1. Create branch. 2. Switch branches. 3. Merge branches. |
| **Expected Output** | All branch operations succeed |
| **Requirements** | NFC-3 |
| **Verification** | Test |

### TC-DEVW-004: File Operations Outside src/

| Field | Value |
|-------|-------|
| **ID** | TC-DEVW-004 |
| **Objective** | Verify enforcement does not interfere with non-source file operations |
| **Steps** | 1. Create/modify files in docs/, tests/, scripts/. 2. Verify no enforcement blocking. |
| **Expected Output** | Non-source files unaffected by enforcement |
| **Requirements** | REQ-403-039, NFC-3 |
| **Verification** | Test |

### TC-DEVW-005: Claude Code Session Stability

| Field | Value |
|-------|-------|
| **ID** | TC-DEVW-005 |
| **Objective** | Verify Claude Code sessions start and operate stably with all enforcement |
| **Steps** | 1. Start Claude Code session. 2. Perform normal development tasks. 3. End session. |
| **Expected Output** | Stable session lifecycle |
| **Requirements** | NFC-3 |
| **Verification** | Test |

### TC-DEVW-006: Enforcement Disable/Bypass

| Field | Value |
|-------|-------|
| **ID** | TC-DEVW-006 |
| **Objective** | Verify enforcement can be disabled if needed (emergency bypass) |
| **Steps** | 1. Document bypass method. 2. Verify bypass works. 3. Verify re-enabling works. |
| **Expected Output** | Documented and tested bypass mechanism |
| **Pass Criteria** | Bypass works; re-enable works; both documented |
| **Requirements** | REQ-403-070 (fail-open philosophy) |
| **Verification** | Test |

---

## Tool Integration Tests

### TC-TOOL-001: UV Tool Chain

| Field | Value |
|-------|-------|
| **ID** | TC-TOOL-001 |
| **Objective** | Verify UV operations work with enforcement |
| **Steps** | 1. `uv sync`. 2. `uv run pytest`. 3. `uv add <package>`. |
| **Expected Output** | All UV operations succeed |
| **Requirements** | NFC-3 |
| **Verification** | Test |

### TC-TOOL-002: IDE Integration

| Field | Value |
|-------|-------|
| **ID** | TC-TOOL-002 |
| **Objective** | Verify enforcement does not interfere with IDE operations |
| **Steps** | 1. Open project in VS Code. 2. Verify Python extension works. 3. Verify linting works in-editor. |
| **Expected Output** | IDE functionality unaffected |
| **Requirements** | NFC-3 |
| **Verification** | Test |

### TC-TOOL-003: Documentation Generation

| Field | Value |
|-------|-------|
| **ID** | TC-TOOL-003 |
| **Objective** | Verify documentation can be generated with enforcement in place |
| **Steps** | 1. Generate any auto-documentation. 2. Verify enforcement modules documented correctly. |
| **Expected Output** | Documentation generates cleanly |
| **Requirements** | NFC-3 |
| **Verification** | Test |

### TC-TOOL-004: Test Coverage Reporting

| Field | Value |
|-------|-------|
| **ID** | TC-TOOL-004 |
| **Objective** | Verify test coverage includes enforcement modules |
| **Steps** | 1. Run `uv run pytest --cov=src`. 2. Verify enforcement modules appear in coverage report. |
| **Expected Output** | Enforcement modules in coverage report; no coverage tool errors |
| **Requirements** | NFC-3 |
| **Verification** | Test |

---

## Rollback Strategy

### If Enforcement Breaks CI/CD

| Step | Action | Owner |
|------|--------|-------|
| 1 | Identify failing pipeline step | Developer |
| 2 | Determine if enforcement-related | Developer |
| 3 | If yes: disable enforcement hooks (rename/remove hook files) | Developer |
| 4 | Verify pipeline recovers | CI/CD |
| 5 | File bug report with enforcement mechanism details | Developer |
| 6 | Fix enforcement code | Enforcement team |
| 7 | Re-enable enforcement | Enforcement team |

### Enforcement Kill Switch

```yaml
# .claude/settings.json - disable hooks
{
  "hooks": {
    "UserPromptSubmit": [],
    "PreToolUse": [],
    "SessionStart": {
      "command": "scripts/session_start_hook.py"
      # Quality context controlled by QUALITY_CONTEXT_AVAILABLE flag
    }
  }
}
```

### Recovery Verification

After re-enabling enforcement:
1. Re-run all TC-CICD tests
2. Re-run all TC-DEVW tests
3. Verify no test regressions
4. Document root cause and fix

---

## Requirements Traceability

| Test ID | Requirements Verified |
|---------|----------------------|
| TC-CICD-001 | NFC-3 |
| TC-CICD-002 | NFC-3 |
| TC-CICD-003 | NFC-3 |
| TC-CICD-004 | NFC-3 |
| TC-CICD-005 | NFC-3 |
| TC-CICD-006 | NFC-3 |
| TC-CICD-007 | NFC-3 |
| TC-CICD-008 | NFC-3, REQ-403-080 |
| TC-DEVW-001 through TC-DEVW-006 | NFC-3 |
| TC-TOOL-001 through TC-TOOL-004 | NFC-3 |

---

## References

| Document | Path | Relevance |
|----------|------|-----------|
| FEAT-005 | `../FEAT-005-enforcement-mechanisms.md` | NFC-3 (No CI/CD breakage) |
| EN-403 TASK-001 | `../EN-403-hook-based-enforcement/TASK-001-hook-requirements.md` | Architecture requirements |
| TASK-001 Integration Test Plan | `TASK-001-integration-test-plan.md` | Master test plan |

---

*Generated by ps-validator-406 | 2026-02-13 | EN-406 AC-9*
