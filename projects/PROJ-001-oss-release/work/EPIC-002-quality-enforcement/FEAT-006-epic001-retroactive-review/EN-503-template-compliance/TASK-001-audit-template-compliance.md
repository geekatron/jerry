# TASK-001: Audit EPIC-001 entity file template compliance

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** MEDIUM
> **Activity:** RESEARCH
> **Created:** 2026-02-16
> **Parent:** EN-503

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

Audit all EPIC-001 entity files against their respective templates (FEATURE, ENABLER, TASK). For each file, check:

1. **Blockquote frontmatter** -- all required fields present with correct format
2. **Navigation table** -- present per H-23, with anchor links per H-24
3. **Required sections** -- all template-mandated sections present
4. **Section content** -- sections have meaningful content (not just headers)
5. **Hyperlinks** -- parent/child/related item links are valid

Files to audit:
- FEAT-001, FEAT-002, FEAT-003 feature files
- EN-001 through EN-004 (FEAT-001 enablers)
- EN-101 through EN-108 (FEAT-002 enablers)
- EN-201 through EN-207 (FEAT-003 enablers)
- All associated task files

For each file, record: file path, template type, compliance status (compliant/non-compliant), and specific gaps.

### Acceptance Criteria

- [ ] All EPIC-001 entity files audited
- [ ] Compliance status recorded for each file
- [ ] Specific gaps documented per file
- [ ] Audit report persisted as deliverable

### Implementation Notes

Use the current EN-901 and TASK-001 templates as the compliance baseline. Focus on structural compliance first (sections present), then content quality.

### Related Items

- Parent: [EN-503: Template Compliance Review](EN-503-template-compliance.md)
- Informs: TASK-002

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Template compliance audit report | Document | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] All entity files audited
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Audit phase for EN-503 template compliance review. |
