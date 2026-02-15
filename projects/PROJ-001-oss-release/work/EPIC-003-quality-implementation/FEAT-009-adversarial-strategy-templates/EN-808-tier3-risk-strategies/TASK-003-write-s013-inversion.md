# TASK-003: Write S-013-inversion.md

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
Create the S-013 Inversion Technique execution template at `.context/templates/adversarial/S-013-inversion.md`. The template implements the "How could this fail?" protocol based on Charlie Munger's inversion mental model. It must include all 8 canonical sections per TEMPLATE-FORMAT.md. Key protocol elements include goal inversion (restating the desired outcome as its opposite), anti-goal analysis (systematically identifying what would cause the anti-goal), failure path enumeration (mapping concrete paths from current state to failure), and defensive design recommendations (design changes that block identified failure paths).

### Acceptance Criteria
- [ ] Template file created at `.context/templates/adversarial/S-013-inversion.md`
- [ ] All 8 canonical sections present and populated with substantive content
- [ ] Goal inversion protocol defined with INV-NNN identifier format for findings
- [ ] Goal inversion step clearly defined (how to restate desired outcome as opposite)
- [ ] Anti-goal analysis protocol includes systematic enumeration of failure causes
- [ ] Failure path enumeration maps concrete sequences from current state to failure
- [ ] Defensive design recommendations linked to specific failure paths
- [ ] Integration with S-004 Pre-Mortem documented (complementary failure analysis)
- [ ] Integration with S-012 FMEA documented (inversion findings as FMEA input)
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
| S-013-inversion.md | Strategy template | `.context/templates/adversarial/S-013-inversion.md` |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
