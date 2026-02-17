# TASK-004: Strip testing-standards.md to enforcement skeleton

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

Remove all code examples, verbose explanations from `testing-standards.md`. Keep: H-20, H-21, test pyramid table, BDD summary, test naming format, coverage configuration, tool configuration refs. Add companion reference section.

Specific content to preserve:
- HARD Rules table (H-20, H-21) with consequences
- Test Pyramid Distribution table (unit 60%, integration 15%, etc.)
- BDD Red/Green/Refactor summary (compressed to 3-line format)
- Test naming format: `test_{scenario}_when_{condition}_then_{expected}`
- Test File Location table
- Coverage Configuration rules (branch >= 85%, exclusions)
- Mocking Guidelines (compressed to key rules)
- Tool Configuration summary (pytest markers, mypy strict, ruff rules)

Specific content to remove:
- Extended BDD explanations
- Scenario distribution prose
- AAA pattern explanation (move to companion guide)
- SOFT Guidance extended explanations

Content to add:
- "Detailed Guidance" section with references to `.context/guides/testing-guide.md`

### Acceptance Criteria

- [ ] H-20, H-21 present with consequences
- [ ] Test pyramid table preserved
- [ ] Companion reference section added
- [ ] File < 1.5K tokens

### Implementation Notes

The BDD cycle is critical for enforcement (H-20 depends on it), so keep a compressed summary. The full explanation with examples belongs in the companion guide.

### Related Items

- Parent: [EN-901: Rules File Thinning](EN-901-rules-thinning.md)
- Depends on: TASK-001 (content inventory informs what to keep/remove)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Thinned testing-standards.md | Code change | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] git diff confirms no enforcement content removed
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-901 rules thinning. |
