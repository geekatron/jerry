# TASK-004: Remediate platform issues

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
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

Remediate all platform-specific issues discovered during Windows (TASK-002) and Linux (TASK-003) testing. For each issue:

1. Assess severity (critical/high/medium/low)
2. Implement a cross-platform fix using `pathlib`, platform guards, or conditional logic
3. Verify the fix works on all three platforms (macOS, Windows, Linux)
4. Update documentation with platform-specific notes if needed

### Acceptance Criteria

- [ ] All critical and high severity platform issues fixed
- [ ] All medium severity issues fixed or documented with justification for deferral
- [ ] Fixes verified on macOS (no regressions)
- [ ] Platform-specific documentation updated
- [ ] Remediation log persisted as deliverable

### Implementation Notes

Prefer `pathlib.Path` over string manipulation for path handling. Use `platform.system()` for platform detection. Avoid `os.symlink` on Windows unless absolutely necessary. Consider `shutil` for cross-platform file operations.

### Related Items

- Parent: [EN-502: Bootstrap Cross-Platform Validation](EN-502-bootstrap-cross-platform.md)
- Depends on: TASK-002, TASK-003

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Platform remediation log | Document | pending |
| Cross-platform fixes | Code change | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] All critical/high issues resolved
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Remediation phase for EN-502 cross-platform validation. |
