# TASK-003: Strip coding-standards.md to enforcement skeleton

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

Remove all explanatory prose, code examples from `coding-standards.md`. Keep: H-11, H-12, naming convention table, import grouping rules, git commit format, exception hierarchy table. Add companion reference section.

Specific content to preserve:
- HARD Rules table (H-11, H-12) with consequences
- Naming Conventions table (modules, classes, functions, constants, private, test files)
- Line Length rule
- Import grouping rules (stdlib, third-party, local)
- Git Commits format (conventional commits)
- Exception Hierarchy table (ValidationError through QualityGateError)
- L2-REINJECT comments

Specific content to remove:
- Type Hints extended prose (keep table-form summary)
- Docstrings extended explanation (keep Google-style reference)
- Error Handling extended prose (keep hierarchy table)
- SOFT Guidance explanatory text

Content to add:
- "Detailed Guidance" section with references to `.context/guides/coding-guide.md`

### Acceptance Criteria

- [ ] H-11, H-12 present with consequences
- [ ] Naming table preserved
- [ ] Exception hierarchy table preserved
- [ ] Companion reference section added
- [ ] File < 1.5K tokens

### Implementation Notes

The exception hierarchy table is critical for enforcement -- it defines the error taxonomy. Preserve it even though it could be seen as educational content, because it directly supports coding decisions.

### Related Items

- Parent: [EN-901: Rules File Thinning](EN-901-rules-thinning.md)
- Depends on: TASK-001 (content inventory informs what to keep/remove)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Thinned coding-standards.md | Code change | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] git diff confirms no enforcement content removed
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-901 rules thinning. |
