# TASK-002: Define Canonical Adversarial Strategy Template Sections and Fields

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

Define the 8 required sections for adversarial strategy templates: Identity, Purpose, Prerequisites, Execution Protocol, Output Format, Scoring Rubric, Examples, and Integration. For each section, specify the required fields, field types, constraints, and usage notes. Ensure the section definitions align with quality-enforcement.md dimensions (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability) and support integration with criticality levels C1-C4.

### Acceptance Criteria

- [ ] Identity section defined: strategy ID, name, composite score, family, source reference
- [ ] Purpose section defined: description, when to use, criticality level applicability
- [ ] Prerequisites section defined: required inputs, context requirements, dependencies
- [ ] Execution Protocol section defined: numbered step-by-step instructions, decision points, iteration rules
- [ ] Output Format section defined: deliverable structure, required fields, format conventions
- [ ] Scoring Rubric section defined: dimension-level criteria aligned with quality-enforcement.md weights
- [ ] Examples section defined: calibration example structure at multiple score levels
- [ ] Integration section defined: quality cycle placement, criticality level mapping, hook integration points
- [ ] Field specifications documented for each section (type, required/optional, constraints)
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items

- Parent: [EN-801: Template Format Standard](EN-801-template-format-standard.md)
- Depends on: TASK-001 (template pattern inventory)
- Blocks: TASK-003 (write TEMPLATE-FORMAT.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Section and field specification document | Design artifact | --- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. Core design task -- defines the structure all strategy templates will follow. |
