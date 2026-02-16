# TASK-005: Strip remaining rule files to enforcement skeletons

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
> **Parent:** EN-901

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

Thin `mandatory-skill-usage.md`, `markdown-navigation-standards.md`, `project-workflow.md`, `python-environment.md`. Keep enforcement rules (H-22, H-23, H-24, H-04, H-05, H-06) and key tables. Add companion references. Update stub files (`error-handling-standards.md`, `file-organization.md`, `tool-configuration.md`) with guide references.

Files and their HARD rules:
- `mandatory-skill-usage.md`: H-22 (proactive skill invocation) + trigger map + behavior rules
- `markdown-navigation-standards.md`: H-23 (NAV-001), H-24 (NAV-006) + anchor link syntax table
- `project-workflow.md`: H-04 (active project required) + workflow phases table + project structure
- `python-environment.md`: H-05, H-06 (UV only) + command reference table

Stub files to update:
- `error-handling-standards.md`: Add companion guide reference alongside existing redirect
- `file-organization.md`: Add companion guide reference alongside existing redirect
- `tool-configuration.md`: Add companion guide reference alongside existing redirect

### Acceptance Criteria

- [ ] All 6 remaining files thinned (4 substantive + 2 stubs needing update; tool-configuration.md is already a stub)
- [ ] All relevant HARD rules preserved: H-04, H-05, H-06, H-22, H-23, H-24
- [ ] Stub files updated with guide references
- [ ] Each file < 1K tokens

### Implementation Notes

These files are already relatively lean. The main thinning targets are:
- `mandatory-skill-usage.md`: Remove behavior rules prose, keep trigger map table
- `markdown-navigation-standards.md`: Remove table format examples, keep syntax table
- `project-workflow.md`: Remove project resolution extended prose, keep structure
- `python-environment.md`: Remove large file handling section (move to companion guide)

### Related Items

- Parent: [EN-901: Rules File Thinning](EN-901-rules-thinning.md)
- Depends on: TASK-001 (content inventory informs what to keep/remove)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Thinned mandatory-skill-usage.md | Code change | pending |
| Thinned markdown-navigation-standards.md | Code change | pending |
| Thinned project-workflow.md | Code change | pending |
| Thinned python-environment.md | Code change | pending |
| Updated error-handling-standards.md | Code change | pending |
| Updated file-organization.md | Code change | pending |
| Updated tool-configuration.md | Code change | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] git diff confirms no enforcement content removed from any file
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-901 rules thinning. |
