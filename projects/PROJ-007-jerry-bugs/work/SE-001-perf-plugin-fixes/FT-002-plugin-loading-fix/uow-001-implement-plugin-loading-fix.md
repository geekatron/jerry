# UoW-001: Implement Plugin Loading Fix

> **Unit of Work ID:** UoW-001
> **Feature:** FT-002-plugin-loading-fix
> **Project:** PROJ-007-jerry-bugs
> **Status:** BLOCKED
> **Blocked By:** EN-003 (Validate Solution)
> **Target Version:** v0.2.0
> **Created:** 2026-01-14
> **Last Updated:** 2026-01-14

---

## Objective

Fix the plugin loading issue (BUG-002) by removing PEP 723 inline metadata from `session_start.py`, enabling proper `uv run` execution that respects the project's `pyproject.toml` and PYTHONPATH.

---

## Solution

Remove PEP 723 inline script metadata that causes `uv` to create an isolated environment:

```python
# REMOVE these lines from session_start.py:
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
```

**Why this works:**
- Without PEP 723 metadata, `uv run` treats the script as part of the project
- Uses `pyproject.toml` for dependency resolution instead of inline `dependencies = []`
- PYTHONPATH is respected, allowing `from src.infrastructure.*` imports

---

## TDD/BDD Methodology

This implementation follows the **Red/Green/Refactor** cycle as defined in `.claude/rules/testing-standards.md`.

---

## Tasks

### Phase 1: RED (Write Failing Tests First)

| ID | Description | Status | Test Type | Notes |
|----|-------------|--------|-----------|-------|
| T-001 | Write integration test: hook execution from arbitrary directory | PENDING | Integration | Simulates hook running from non-repo directory |
| T-002 | Write contract test: hook output format compliance | PENDING | Contract | Validates `<project-context>` or `<project-required>` output |
| T-003 | Write E2E test: plugin loading workflow (subprocess) | PENDING | E2E | Tests full `uv run` invocation |

**Test Scenarios (per testing-standards.md):**
- Happy Path (60%): Hook executes successfully, returns valid output
- Negative Cases (30%): Invalid JERRY_PROJECT, missing project directory
- Edge Cases (10%): Unicode paths, spaces in paths, symlinks

### Phase 2: GREEN (Minimal Code to Pass)

| ID | Description | Status | Notes |
|----|-------------|--------|-------|
| T-004 | Remove PEP 723 inline metadata from session_start.py | PENDING | Lines 36-39 |
| T-005 | Verify all new tests pass | PENDING | Run `pytest tests/integration/` |

### Phase 3: REFACTOR (Improve Without Changing Behavior)

| ID | Description | Status | Notes |
|----|-------------|--------|-------|
| T-006 | Update session_start.py module docstring | PENDING | Document why PEP 723 was removed |
| T-007 | Correct ADR-PROJ007-002 with validated solution | PENDING | Update proposed solution section |

### Phase 4: Quality Gates

| ID | Description | Status | Notes |
|----|-------------|--------|-------|
| T-008 | Run full test suite - verify no regressions | PENDING | `pytest --cov=src` |
| T-009 | Run linting and type checking | PENDING | `ruff check` and `pyright` |
| T-010 | Run CI pipeline validation locally | PENDING | Verify all CI checks pass |
| T-011 | Version bump to 0.2.0 in pyproject.toml | PENDING | Update version string |
| T-012 | User verification gate | PENDING | Manual `claude --plugin-dir` test |

---

## Acceptance Criteria

| ID | Criterion | Verification Method |
|----|-----------|---------------------|
| AC-001 | SessionStart hook executes successfully | Integration test passes |
| AC-002 | Hook works from any working directory | E2E test from /tmp passes |
| AC-003 | Output matches contract format | Contract test passes |
| AC-004 | No test regressions | Full suite passes with ≥80% coverage |
| AC-005 | CI pipeline passes | All CI jobs green |
| AC-006 | User can run `claude --plugin-dir` | Manual verification by user |

---

## Test Coverage Requirements

Per `.claude/rules/testing-standards.md`:

| Category | Target % | This UoW |
|----------|----------|----------|
| Unit | 60% | N/A (no domain changes) |
| Integration | 15% | T-001 (hook execution) |
| Contract | 5% | T-002 (output format) |
| E2E | 5% | T-003 (plugin workflow) |
| Architecture | 5% | N/A (no layer changes) |

---

## Dependencies

| Type | ID | Description | Status |
|------|-----|-------------|--------|
| BLOCKED_BY | EN-003 | Solution validation must pass first | IN PROGRESS |
| REFERENCES | disc-001 | uv portability requirement | OPEN |
| RESOLVES | BUG-002 | Plugin not loading | PENDING |
| ADDRESSES | TD-002 | Partially (tests validate hook env) | DOCUMENTED |

---

## Files to Modify

| File | Change |
|------|--------|
| `src/interface/cli/session_start.py` | Remove PEP 723 metadata (lines 36-39) |
| `pyproject.toml` | Version bump to 0.2.0 |
| `projects/PROJ-007-jerry-bugs/decisions/ADR-PROJ007-002-*.md` | Correct solution |

## Files to Create

| File | Purpose |
|------|---------|
| `tests/integration/cli/test_hook_execution.py` | Integration tests for hook |
| `tests/contract/test_hook_output.py` | Contract tests for output format |
| `tests/e2e/test_plugin_loading.py` | E2E tests for plugin workflow |

---

## Related Artifacts

| Type | Reference |
|------|-----------|
| Bug | BUG-002 (Plugin not loading) |
| Discovery | disc-001, disc-002, disc-003 |
| Enabler | EN-003 (Solution validation) |
| Tech Debt | TD-002 (CI test gap) |
| ADR | ADR-PROJ007-002 |
| PROJ-005 ADR | PROJ-005-e-010-adr-uv-session-start.md |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | UoW-001 created with TDD/BDD tasks | Claude |
