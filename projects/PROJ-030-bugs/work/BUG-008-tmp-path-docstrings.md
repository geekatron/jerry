# BUG-008: Replace /tmp with tempfile.gettempdir() in docstring examples (#119)

> **Type:** bug
> **Status:** pending
> **Priority:** low
> **Impact:** low
> **Severity:** trivial
> **Created:** 2026-03-14
> **Parent:** PROJ-030-bugs
> **Owner:** unassigned

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Steps to Reproduce](#steps-to-reproduce) | Steps to reproduce the issue |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

Several docstrings reference `/tmp` as an example path, which does not exist on Windows. The affected files should use `tempfile.gettempdir()` or a platform-neutral path in their docstring examples.

**Affected Files:**
- `event_sourced_session_repository.py`
- `filesystem_event_store.py`
- `event_sourced_work_item_repository.py`
- `file_store.py`

**Key Details:**
- **Symptom:** Docstring examples reference a Unix-only path
- **Frequency:** N/A (documentation only, no runtime impact)
- **Workaround:** None needed -- docstrings only

---

## Steps to Reproduce

1. Search the codebase for `/tmp` references in docstrings
2. Observe the affected files listed above use `/tmp` in usage examples
3. Note that `/tmp` does not exist on Windows and is misleading for cross-platform documentation

---

## Acceptance Criteria

- [ ] All docstring examples use `tempfile.gettempdir()` or a platform-neutral path instead of `/tmp`
- [ ] Affected files updated: `event_sourced_session_repository.py`, `filesystem_event_store.py`, `event_sourced_work_item_repository.py`, `file_store.py`
- [ ] No runtime behavior changes (documentation-only fix)

---

## Related Items

### Hierarchy

- **Parent:** PROJ-030-bugs

### Related Items

- **GitHub Issue:** [#119](https://github.com/geekatron/jerry/issues/119)
- **Labels:** documentation, portability

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-03-14 | pending | Triaged from GitHub Issue #119 |
