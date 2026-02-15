# TASK-003: Clarify TEMPLATE-FORMAT.md template length criterion

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
> **Parent:** EN-815

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

The current template length criterion in TEMPLATE-FORMAT.md is ambiguous. Clarify that template length is a SHOULD constraint (not MUST) with an explicit exception clause for strategies that require additional depth (e.g., S-014 LLM-as-Judge scoring rubrics, S-012 FMEA systematic enumeration).

### Acceptance Criteria

- [ ] Length criterion updated to SHOULD with exception clause
- [ ] Exception conditions listed (S-014 rubrics, S-012 enumeration)
- [ ] No contradiction with other rules
- [ ] Follows MEDIUM tier vocabulary

### Related Items
- Parent: [EN-815: Documentation & Navigation Fixes](EN-815-documentation-navigation-fixes.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated TEMPLATE-FORMAT.md | file | .context/templates/adversarial/TEMPLATE-FORMAT.md |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Created from EN-815 breakdown. |
