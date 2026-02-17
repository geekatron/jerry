# TASK-002: Remediate non-compliant files

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** MEDIUM
> **Activity:** DEVELOPMENT
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

Remediate all non-compliant EPIC-001 entity files identified in TASK-001. For each non-compliant file:

1. Add missing blockquote frontmatter fields
2. Add navigation table per H-23 with anchor links per H-24
3. Add missing template-mandated sections
4. Fix invalid hyperlinks
5. Preserve existing content while adding structural compliance

### Acceptance Criteria

- [ ] All non-compliant files updated to match templates
- [ ] All files have correct blockquote frontmatter
- [ ] All files have navigation tables (H-23) with anchor links (H-24)
- [ ] All template-mandated sections present
- [ ] Existing content preserved during remediation

### Implementation Notes

Work through files systematically by feature (FEAT-001 files, then FEAT-002, then FEAT-003). Use batch operations where possible for common gaps (e.g., adding navigation tables to all files missing them). Be careful not to alter the semantic content of existing sections.

### Related Items

- Parent: [EN-503: Template Compliance Review](EN-503-template-compliance.md)
- Depends on: TASK-001
- Informs: TASK-003

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Remediated entity files | Code change | pending |
| Remediation summary | Document | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] All non-compliant files remediated
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Remediation phase for EN-503 template compliance review. |
