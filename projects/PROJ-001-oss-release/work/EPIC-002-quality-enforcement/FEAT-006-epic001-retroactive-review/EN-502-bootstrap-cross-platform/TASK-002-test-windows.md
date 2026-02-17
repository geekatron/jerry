# TASK-002: Test on Windows (WSL/native)

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

Test bootstrap_context.py and all EPIC-001 scripts on Windows. Test both WSL (Windows Subsystem for Linux) and native Windows (PowerShell/cmd) environments where applicable.

Test scenarios:
1. Bootstrap context initialization on Windows
2. Path handling with Windows backslash separators
3. Symlink creation (if applicable -- Windows requires special permissions)
4. Shell detection (PowerShell, cmd, WSL bash)
5. CLI command execution
6. File permission handling (Windows ACLs vs Unix permissions)
7. Environment variable access

### Acceptance Criteria

- [ ] Bootstrap context tested on Windows (WSL or native)
- [ ] All platform-specific code paths from TASK-001 tested
- [ ] Test results documented with pass/fail per scenario
- [ ] All failures logged with reproduction steps

### Implementation Notes

If native Windows testing is not available, WSL testing provides partial coverage. Document which scenarios were tested on WSL vs native Windows and any gaps in coverage.

### Related Items

- Parent: [EN-502: Bootstrap Cross-Platform Validation](EN-502-bootstrap-cross-platform.md)
- Depends on: TASK-001 (audit identifies code paths to test)
- Parallel with: TASK-003

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Windows test results | Document | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] All identified code paths tested
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Windows testing phase for EN-502 cross-platform validation. |
