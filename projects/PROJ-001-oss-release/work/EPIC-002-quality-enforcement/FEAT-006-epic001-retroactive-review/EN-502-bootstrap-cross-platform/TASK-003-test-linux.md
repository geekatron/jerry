# TASK-003: Test on Linux

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** TESTING
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

Test bootstrap_context.py and all EPIC-001 scripts on Linux (Ubuntu/Debian preferred as most common distribution). Verify all functionality matches macOS behavior.

Test scenarios:
1. Bootstrap context initialization on Linux
2. Path handling with Linux path separators
3. Symlink creation and resolution
4. Shell detection (bash, zsh, fish)
5. CLI command execution
6. File permission handling (chmod, ownership)
7. Environment variable access
8. Package manager compatibility (apt-based systems)

### Acceptance Criteria

- [ ] Bootstrap context tested on Linux
- [ ] All platform-specific code paths from TASK-001 tested
- [ ] Test results documented with pass/fail per scenario
- [ ] All failures logged with reproduction steps

### Implementation Notes

Linux is the closest to macOS in terms of POSIX compliance, so fewer issues are expected compared to Windows. Focus testing on distribution-specific differences (package locations, default shells, Python installation paths).

### Related Items

- Parent: [EN-502: Bootstrap Cross-Platform Validation](EN-502-bootstrap-cross-platform.md)
- Depends on: TASK-001 (audit identifies code paths to test)
- Parallel with: TASK-002

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Linux test results | Document | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] All identified code paths tested
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Linux testing phase for EN-502 cross-platform validation. |
