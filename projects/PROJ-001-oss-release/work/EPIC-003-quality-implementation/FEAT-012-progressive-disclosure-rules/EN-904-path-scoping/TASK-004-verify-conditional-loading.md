# TASK-004: Verify path-scoped rules load correctly

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** REVIEW
> **Created:** 2026-02-16
> **Parent:** EN-904

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

Test that path-scoped rules load when editing Python files and do NOT load when editing non-Python files. Document verification results.

Verification procedure:
1. Start a Claude Code session editing a `src/**/*.py` file -- verify architecture-standards, coding-standards, and testing-standards all load
2. Start a Claude Code session editing a `tests/**/*.py` file -- verify coding-standards and testing-standards load, check architecture-standards behavior
3. Start a Claude Code session editing a markdown file (e.g., `WORKTRACKER.md`) -- verify none of the 3 scoped files load
4. Document each test result with evidence (e.g., screenshot or session log excerpt)

### Acceptance Criteria

- [ ] Python editing session loads all 3 scoped files
- [ ] Markdown editing session does NOT load scoped files
- [ ] Results documented with evidence
- [ ] Non-scoped rules (quality-enforcement, markdown-navigation, etc.) still load in all sessions

### Implementation Notes

This is a manual verification task. Claude Code does not provide programmatic access to which rules were loaded, so verification must be done by observing Claude's behavior or checking session context. Consider creating a simple prompt that tests Claude's knowledge of specific HARD rules from scoped files.

### Related Items

- Parent: [EN-904: Path Scoping Implementation](EN-904-path-scoping.md)
- Depends on: TASK-001, TASK-002, TASK-003 (all scoping must be done first)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Verification report | Document | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] All 3 load scenarios tested
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-904 path scoping verification. |
