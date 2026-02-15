# TASK-002: Write S-012-fmea.md

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
Create the S-012 FMEA (Failure Mode and Effects Analysis) execution template at `.context/templates/adversarial/S-012-fmea.md`. The template implements systematic failure mode enumeration with the standard Severity x Occurrence x Detection = RPN (Risk Priority Number) scoring methodology. It must include all 8 canonical sections per TEMPLATE-FORMAT.md. Key protocol elements include failure mode identification (systematic enumeration of how each component can fail), effect analysis (downstream consequences of each failure mode), cause analysis (root causes for each failure mode), and RPN calculation with threshold-based action triggers.

### Acceptance Criteria
- [ ] Template file created at `.context/templates/adversarial/S-012-fmea.md`
- [ ] All 8 canonical sections present and populated with substantive content
- [ ] Failure mode identification protocol defined with FM-NNN identifier format
- [ ] Effect analysis protocol includes severity scoring on 1-10 scale
- [ ] Cause analysis protocol includes occurrence scoring on 1-10 scale
- [ ] Detection analysis protocol includes detection scoring on 1-10 scale (inverse: 10 = hardest to detect)
- [ ] RPN formula defined: Severity x Occurrence x Detection = RPN
- [ ] RPN threshold levels defined (e.g., >= 200 = critical, >= 100 = high, >= 50 = medium)
- [ ] Action trigger protocol defined based on RPN thresholds
- [ ] Integration with S-004 Pre-Mortem documented (pre-mortem findings as FMEA input)
- [ ] Integration with S-013 Inversion documented (inversion findings as FMEA input)
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
| S-012-fmea.md | Strategy template | `.context/templates/adversarial/S-012-fmea.md` |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
