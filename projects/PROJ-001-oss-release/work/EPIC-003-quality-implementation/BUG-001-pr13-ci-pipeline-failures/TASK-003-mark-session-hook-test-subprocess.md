# TASK-003: Mark session start hook integration test with subprocess marker

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

Add `@pytest.mark.subprocess` decorator to 1 test in `tests/integration/test_session_start_hook_integration.py` that invokes `uv run` via subprocess. This test fails in pip-only CI jobs because `uv` is not installed.

---

## Acceptance Criteria

- [ ] Test calling `uv run` in `test_session_start_hook_integration.py` has `@pytest.mark.subprocess`
- [ ] Test still passes locally with `uv run pytest tests/integration/test_session_start_hook_integration.py`

---

## Implementation Notes

**File:** `tests/integration/test_session_start_hook_integration.py`

Locate the test function(s) that invoke `uv run` via subprocess. Add `@pytest.mark.subprocess`.

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
