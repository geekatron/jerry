# BUG-006: statusLine command uses python3 which fails on Windows (#113)

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

The `statusLine` command in `.claude/settings.json` (line 25) uses `python3` which does not exist on Windows. Windows Python installations use `python`, `py`, or `py -3` as the executable name. This causes the status line to fail silently on Windows systems.

**Key Details:**
- **File:** `.claude/settings.json` line 25
- **Symptom:** statusLine command fails on Windows due to missing `python3` executable
- **Frequency:** Every session on Windows
- **Workaround:** Manually replace `python3` with `python` or `py -3` in settings

---

## Steps to Reproduce

1. Open `.claude/settings.json`
2. Observe the `statusLine` command references `python3`
3. Run Claude Code on a Windows system
4. Observe the status line fails because `python3` is not a recognized command on Windows

---

## Acceptance Criteria

- [ ] statusLine command works on Windows, macOS, and Linux
- [ ] Python executable resolved using a cross-platform compatible approach (`python`, `py -3`, or detection logic)
- [ ] No regression on macOS/Linux where `python3` is standard

---

## Related Items

### Hierarchy

- **Parent:** PROJ-030-bugs

### Related Items

- **GitHub Issue:** [#113](https://github.com/geekatron/jerry/issues/113)
- **Labels:** bug, portability

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-03-14 | pending | Triaged from GitHub Issue #113 |
