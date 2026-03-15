# BUG-007: file_repository.py uses hardcoded forward slash instead of pathlib (#117)

> **Type:** bug
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Severity:** minor
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

The `_get_file_path` method in `src/infrastructure/adapters/file_repository.py` constructs file paths using an f-string with a hardcoded `/` separator instead of using `pathlib.Path` or `os.path.join`. This produces incorrect paths on Windows where the path separator is `\`.

**Key Details:**
- **File:** `src/infrastructure/adapters/file_repository.py`
- **Method:** `_get_file_path`
- **Symptom:** Incorrect path construction on Windows
- **Frequency:** Every file repository operation on Windows
- **Workaround:** None

---

## Steps to Reproduce

1. Open `src/infrastructure/adapters/file_repository.py`
2. Locate the `_get_file_path` method
3. Observe f-string path construction using `/` instead of `pathlib.Path` or `os.path.join`
4. Run on Windows -- file operations fail or produce incorrect paths

---

## Acceptance Criteria

- [ ] `_get_file_path` uses `pathlib.Path` or `os.path.join` for path construction
- [ ] All path operations in `file_repository.py` are cross-platform compatible
- [ ] Existing tests pass on both forward-slash and backslash path separators

---

## Related Items

### Hierarchy

- **Parent:** PROJ-030-bugs

### Related Items

- **GitHub Issue:** [#117](https://github.com/geekatron/jerry/issues/117)
- **Labels:** bug, portability

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-03-14 | pending | Triaged from GitHub Issue #117 |
