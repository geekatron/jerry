# TASK-004: Verify pip jobs exclude subprocess-marked tests

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
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

Verify that the `test-pip` CI job's pytest invocation (`-m "not subprocess and not llm"`) correctly excludes all newly-marked subprocess tests. Run `uv run pytest --collect-only -m "not subprocess and not llm"` locally to confirm the 11 tests are excluded.

---

## Acceptance Criteria

- [ ] `uv run pytest --collect-only -m "not subprocess and not llm"` does NOT list any of the 11 marked tests
- [ ] `uv run pytest --collect-only -m "subprocess"` lists exactly the 11 marked tests (plus any previously marked)

---

## Implementation Notes

Run collection-only commands to verify marker behavior without executing tests:
```
uv run pytest --collect-only -m "not subprocess and not llm" | grep -c "test_"
uv run pytest --collect-only -m "subprocess" | grep -c "test_"
```

---

## Related Items

- Parent: [BUG-001](./BUG-001-pr13-ci-pipeline-failures.md)
- Depends on: TASK-001, TASK-002, TASK-003

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
