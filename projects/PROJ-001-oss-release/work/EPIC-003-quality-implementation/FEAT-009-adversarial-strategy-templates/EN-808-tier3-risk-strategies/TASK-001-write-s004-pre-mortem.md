# TASK-001: Write S-004-pre-mortem.md

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** DONE
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
> **Agents:** ps-architect
> **Created:** 2026-02-14
> **Parent:** EN-808

---

## Document Sections
| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Time Tracking](#time-tracking) | Effort estimates and actuals |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and dependencies |
| [History](#history) | Change log |

---

## Summary
Create the S-004 Pre-Mortem Analysis execution template at `.context/templates/adversarial/S-004-pre-mortem.md`. The template implements the "Imagine this failed -- why?" protocol derived from Gary Klein's prospective hindsight methodology. It must include all 8 canonical sections per TEMPLATE-FORMAT.md. Key protocol elements include prospective hindsight framing (assume the deliverable has failed), failure cause enumeration (systematic generation of failure scenarios), likelihood assessment (ranking failure causes by probability and severity), and mitigation planning (concrete actions to prevent each identified failure mode).

### Acceptance Criteria
- [ ] Template file created at `.context/templates/adversarial/S-004-pre-mortem.md`
- [ ] All 8 canonical sections present and populated with substantive content
- [ ] Prospective hindsight protocol defined with PM-NNN identifier format for findings
- [ ] Failure cause enumeration protocol includes >= 5 categories (technical, process, resource, scope, external)
- [ ] Likelihood assessment scale defined (e.g., 1-5 probability, 1-5 impact)
- [ ] Mitigation planning steps defined with owner assignment and timeline guidance
- [ ] Integration with S-012 FMEA documented (pre-mortem findings can feed FMEA failure modes)
- [ ] Integration with S-013 Inversion documented (complementary failure analysis approaches)
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items
- Parent: [EN-808: Tier 3 Risk Strategy Templates](EN-808-tier3-risk-strategies.md)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | — |
| Remaining Work | 0 hours |
| Time Spent | — |

---

## Evidence
### Deliverables
| Deliverable | Type | Link |
|-------------|------|------|
| S-004-pre-mortem.md | Strategy template | `.context/templates/adversarial/S-004-pre-mortem.md` |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
