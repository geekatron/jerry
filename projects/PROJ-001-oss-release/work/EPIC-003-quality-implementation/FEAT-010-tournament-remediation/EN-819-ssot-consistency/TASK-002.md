# TASK-002: Update all templates to reference REVISE band from SSOT

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** pending
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
> **Agents:** ps-architect
> **Created:** 2026-02-15
> **Parent:** EN-819

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and dependencies |
| [History](#history) | Change log |

---

## Summary

Update all 10 strategy templates in .context/templates/adversarial/ to reference the REVISE band from quality-enforcement.md instead of defining it locally. Each template should use a reference like "REVISE band (see quality-enforcement.md)" rather than hardcoding "0.85-0.91".

### Acceptance Criteria
- [ ] All 10 templates updated
- [ ] No local REVISE band definitions remain
- [ ] All references point to quality-enforcement.md
- [ ] References are findable and clear

### Related Items
- Parent: [EN-819: SSOT Consistency & Template Resilience](EN-819-ssot-consistency.md)
- Depends on: TASK-001

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated strategy templates (10 files) | Documentation | --- |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Task created from EN-819 breakdown. |
