# TASK-001: Mark adversary template E2E tests with subprocess marker

> **Type:** task
> **Status:** BACKLOG
> **Priority:** CRITICAL
> **Created:** 2026-02-16T23:00:00Z
> **Parent:** BUG-001
> **Owner:** Claude
> **Activity:** TESTING
> **Effort:** 1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Description](#description) | What needs to be done |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical details |
| [Evidence](#evidence) | Verification |
| [History](#history) | Changes |

---

## Description

Add `@pytest.mark.subprocess` decorator to 2 tests in `tests/e2e/test_adversary_templates_e2e.py` that invoke `uv run` via subprocess. These tests fail in pip-only CI jobs because `uv` is not installed.

---

## Acceptance Criteria

- [ ] Both tests calling `uv run` in `test_adversary_templates_e2e.py` have `@pytest.mark.subprocess`
- [ ] Tests still pass locally with `uv run pytest tests/e2e/test_adversary_templates_e2e.py`

---

## Implementation Notes

**File:** `tests/e2e/test_adversary_templates_e2e.py`

Identify test functions that use `subprocess.run` or `subprocess.check_output` to call `uv`. Add `@pytest.mark.subprocess` above each such test function.

---

## Related Items

- Parent: [BUG-001](./BUG-001-pr13-ci-pipeline-failures.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| — | — | — |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation |

---
