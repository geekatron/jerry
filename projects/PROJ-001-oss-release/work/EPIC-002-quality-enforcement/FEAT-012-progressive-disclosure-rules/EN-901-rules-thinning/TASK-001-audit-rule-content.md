# TASK-001: Audit current rule files -- catalog all content by type

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

Read all 10 `.context/rules/` files. For each file, catalog every section as: enforcement (HARD/MEDIUM/SOFT rule), explanation (rationale/theory), example (code/config), or reference (see-also/citations). Output a content inventory table.

The 10 files to audit:
1. `architecture-standards.md`
2. `coding-standards.md`
3. `testing-standards.md`
4. `quality-enforcement.md`
5. `mandatory-skill-usage.md`
6. `markdown-navigation-standards.md`
7. `project-workflow.md`
8. `python-environment.md`
9. `error-handling-standards.md` (stub)
10. `file-organization.md` (stub)
11. `tool-configuration.md` (stub -- note: 10 files includes the 3 stubs)

For each file, record:
- File name
- Section heading
- Content type classification (enforcement / explanation / example / reference)
- Approximate token count per section
- Total token count per file

### Acceptance Criteria

- [ ] Content inventory table covers all 10 files
- [ ] Every section classified as enforcement, explanation, example, or reference
- [ ] Token count per file measured
- [ ] Inventory output persisted as deliverable

### Implementation Notes

Use token estimation (1 token ~= 4 characters) for approximate counts. Focus on identifying which sections contain HARD/MEDIUM/SOFT enforcement rules versus educational content that can be moved to companion guides.

### Related Items

- Parent: [EN-901: Rules File Thinning](EN-901-rules-thinning.md)
- Informs: TASK-002, TASK-003, TASK-004, TASK-005

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Content inventory table | Document | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] All 10 files audited with section-level classification
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-901 rules thinning audit phase. |
