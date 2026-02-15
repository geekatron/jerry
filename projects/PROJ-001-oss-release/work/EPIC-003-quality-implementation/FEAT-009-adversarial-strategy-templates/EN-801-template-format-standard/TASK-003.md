# TASK-003: Write TEMPLATE-FORMAT.md

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
> **Created:** 2026-02-14
> **Parent:** EN-801

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

Create the canonical template format file at `.context/templates/adversarial/TEMPLATE-FORMAT.md` with all 8 sections (Identity, Purpose, Prerequisites, Execution Protocol, Output Format, Scoring Rubric, Examples, Integration), placeholder markers, and usage instructions. The file must follow markdown navigation standards (H-23, H-24) and serve as the authoritative reference for all adversarial strategy template authors.

### Acceptance Criteria

- [ ] File created at `.context/templates/adversarial/TEMPLATE-FORMAT.md`
- [ ] All 8 required sections present with field specifications from TASK-002
- [ ] Placeholder markers clearly documented with usage conventions
- [ ] Usage instructions included for template authors
- [ ] File follows markdown navigation standards (H-23, H-24)
- [ ] Format validated against quality-enforcement.md dimensions and weights
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items

- Parent: [EN-801: Template Format Standard](EN-801-template-format-standard.md)
- Depends on: TASK-002 (section and field specifications)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| `.context/templates/adversarial/TEMPLATE-FORMAT.md` | Template file | --- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. Final deliverable task in EN-801 pipeline -- produces the canonical format file. |
