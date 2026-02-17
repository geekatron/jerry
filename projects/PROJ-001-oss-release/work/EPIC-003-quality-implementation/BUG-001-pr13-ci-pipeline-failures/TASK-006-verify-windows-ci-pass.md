# TASK-006: Verify Windows CI jobs pass

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
| [Evidence](#evidence) | Verification |
| [History](#history) | Changes |

---

## Description

After applying the `shell: bash` fix to ci.yml, verify that Windows test-uv CI jobs (Python 3.13 and 3.14 on windows-latest) pass without PowerShell syntax errors.

---

## Acceptance Criteria

- [ ] `Test uv (Python 3.13, windows-latest)` job passes
- [ ] `Test uv (Python 3.14, windows-latest)` job passes
- [ ] No `ParserError` in CI logs

---

## Related Items

- Parent: [BUG-001](./BUG-001-pr13-ci-pipeline-failures.md)
- Depends on: TASK-005

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
