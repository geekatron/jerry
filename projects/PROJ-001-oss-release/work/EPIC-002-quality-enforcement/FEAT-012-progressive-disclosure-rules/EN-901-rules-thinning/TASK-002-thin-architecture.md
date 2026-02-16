# TASK-002: Strip architecture-standards.md to enforcement skeleton

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

Remove all explanatory prose, code examples, and reference sections from `architecture-standards.md`. Keep only: HARD rules (H-07 through H-10), layer dependency table, directory structure (compressed), naming convention tables, MEDIUM/SOFT guidance tables. Add "Detailed Guidance" section referencing companion guides.

Specific content to preserve:
- HARD Rules table (H-07, H-08, H-09, H-10) with consequences
- Layer Dependencies table (Can Import / MUST NOT Import)
- Directory Structure (compressed to essential layout)
- Naming Conventions tables (ports, adapters, commands, queries, handlers, events)
- CQRS File Naming table
- MEDIUM/SOFT guidance tables

Specific content to remove:
- Explanatory prose around each section
- Pattern Guidance bullet list (move to companion guide)
- Query Verb Selection table (move to companion guide)
- Any extended rationale or commentary

Content to add:
- "Detailed Guidance" section with references to `.context/guides/architecture-guide.md`

### Acceptance Criteria

- [ ] H-07, H-08, H-09, H-10 present with consequences
- [ ] Layer dependency table preserved
- [ ] Companion reference section added
- [ ] File < 2K tokens

### Implementation Notes

Run `git diff` after editing to confirm no enforcement content was accidentally removed. The L2-REINJECT comments must be preserved as they are part of the enforcement architecture.

### Related Items

- Parent: [EN-901: Rules File Thinning](EN-901-rules-thinning.md)
- Depends on: TASK-001 (content inventory informs what to keep/remove)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Thinned architecture-standards.md | Code change | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] git diff confirms no enforcement content removed
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-901 rules thinning. |
