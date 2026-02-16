# TASK-001: Audit platform-specific code

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** RESEARCH
> **Created:** 2026-02-16
> **Parent:** EN-502

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Description, acceptance criteria, implementation notes |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Content

### Description

Audit all EPIC-001 scripts and code for platform-specific behavior. Focus on:
- `bootstrap_context.py` -- path handling, symlinks, file permissions, shell detection
- CLI scripts -- any OS-dependent logic
- Hook scripts -- shell-specific syntax, path separators
- Configuration files -- hardcoded paths, OS assumptions

For each platform-specific code path, document:
- File and line number
- What OS assumption is made
- Expected behavior on Windows
- Expected behavior on Linux
- Risk level (critical/high/medium/low)

### Acceptance Criteria

- [ ] All EPIC-001 scripts audited for platform-specific code
- [ ] Platform-specific code paths cataloged with risk levels
- [ ] Test plan for Windows and Linux identified
- [ ] Audit report persisted as deliverable

### Implementation Notes

Use `pathlib` usage as a positive indicator (cross-platform). Look for `os.path.join`, string path concatenation, hardcoded `/` separators, `subprocess` calls with shell=True, and symlink operations as potential issues.

### Related Items

- Parent: [EN-502: Bootstrap Cross-Platform Validation](EN-502-bootstrap-cross-platform.md)
- Informs: TASK-002, TASK-003

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Platform-specific code audit report | Document | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] All scripts audited
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Platform audit phase for EN-502 cross-platform validation. |
