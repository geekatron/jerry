# TASK-003: Update /bootstrap SKILL.md with guides exclusion rationale

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** MEDIUM
> **Activity:** DOCUMENTATION
> **Created:** 2026-02-16
> **Parent:** EN-905

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

Update `skills/bootstrap/SKILL.md` to document the three-tier architecture and explain why `.context/guides/` is excluded from bootstrap symlinks. Specific updates:

1. Add a "Progressive Disclosure Architecture" section explaining the three tiers
2. Document that `.context/rules/` and `.context/patterns/` are auto-loaded via symlinks
3. Document that `.context/guides/` is on-demand only and NOT symlinked
4. Add rationale: guides contain educational/explanatory content that would consume session-start token budget if auto-loaded

### Acceptance Criteria

- [ ] SKILL.md documents three-tier architecture (rules, patterns, guides)
- [ ] Exclusion rationale for `.context/guides/` documented
- [ ] Rationale references token budget concern
- [ ] Document passes navigation table requirements (H-23, H-24)

### Implementation Notes

Read the current `skills/bootstrap/SKILL.md` before modifying. Add the three-tier documentation as a new section or enhance an existing section. Ensure the navigation table is updated to include the new section. The three tiers are: (1) rules -- always loaded, enforced; (2) patterns -- always loaded, reference implementations; (3) guides -- on-demand, educational content loaded only when invoked by skill or user request.

### Related Items

- Parent: [EN-905: Bootstrap Exclusion & Validation](EN-905-bootstrap-exclusion.md)
- Related: TASK-001 (depends on audit findings)
- Related: EN-902 (companion guides content)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated skills/bootstrap/SKILL.md | Documentation | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] Three-tier architecture clearly documented
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-905 bootstrap exclusion documentation phase. |
