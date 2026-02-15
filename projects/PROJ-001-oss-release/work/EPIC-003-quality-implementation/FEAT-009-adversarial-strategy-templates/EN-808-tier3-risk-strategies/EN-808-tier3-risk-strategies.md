# EN-808: Tier 3 Risk Strategy Templates (S-004, S-012, S-013)

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Create execution templates for three Tier 3 risk strategies used in C3+ quality cycles
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-14
> **Due:** ---
> **Completed:** ---
> **Parent:** FEAT-009
> **Owner:** ---
> **Effort:** 5

---

## Document Sections
| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Business Value](#business-value) | How this enabler supports the parent feature |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Progress Summary](#progress-summary) | Completion status and metrics |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary
Create execution templates for three Tier 3 risk strategies used in C3+ quality cycles: S-004 Pre-Mortem Analysis, S-012 FMEA, and S-013 Inversion Technique. These strategies focus on failure mode analysis and systematic risk identification, forming the risk assessment backbone for significant and critical deliverables.

**Technical Scope:**
- Create S-004 Pre-Mortem Analysis template with prospective hindsight protocol
- Create S-012 FMEA template with Severity x Occurrence x Detection = RPN scoring
- Create S-013 Inversion Technique template with goal inversion and anti-goal analysis
- All templates follow TEMPLATE-FORMAT.md with 8 canonical sections
- All templates integrate with the creator-critic-revision cycle for C3+ quality gates
- Quality review all 3 templates together for consistency and cross-referencing

---

## Problem Statement
C3+ quality cycles (Significant and Critical criticality levels) require S-004 Pre-Mortem Analysis, S-012 FMEA, and S-013 Inversion Technique as mandatory strategies (see quality-enforcement.md Criticality Levels table), but none have concrete execution templates. Without templates, agents cannot systematically apply failure mode analysis, pre-mortem analysis, or inversion techniques during quality review. The absence of standardized risk strategy templates means C3+ deliverables -- which by definition affect more than 10 files, involve API changes, or take more than a day to reverse -- receive inconsistent risk assessment, leading to undetected failure modes reaching production.

---

## Business Value

The Tier 3 risk strategies (S-004 Pre-Mortem, S-012 FMEA, S-013 Inversion) form the risk assessment backbone for C3+ deliverables -- those affecting more than 10 files, involving API changes, or taking more than a day to reverse. These templates enable systematic failure mode identification and risk quantification, ensuring significant decisions receive rigorous risk analysis before acceptance.

### Features Unlocked

- Systematic risk assessment protocol for C3+ deliverables with three complementary failure analysis methods
- RPN-based risk quantification (S-012 FMEA) enabling data-driven risk prioritization

---

## Technical Approach
1. Extract Pre-Mortem, FMEA, and Inversion methodologies from research-15-adversarial-strategies.md (Strategies 5, 12, and 13 respectively).
2. Write 3 strategy templates following TEMPLATE-FORMAT.md, each with all 8 canonical sections: Purpose and Context, When to Use, Protocol Steps, Input/Output Format, Quality Criteria, Integration Points, Examples, and Anti-Patterns.
3. For S-004 Pre-Mortem: Define prospective hindsight protocol ("Imagine this failed -- why?"), failure cause enumeration, likelihood assessment, and mitigation planning.
4. For S-012 FMEA: Define systematic failure mode enumeration with Severity x Occurrence x Detection = RPN scoring formula, effect analysis, cause analysis, and risk priority number calculation.
5. For S-013 Inversion: Define goal inversion protocol ("How could this fail?"), anti-goal analysis, failure path enumeration, and defensive design recommendations.
6. Ensure cross-references between the 3 templates where they complement each other (e.g., S-004 pre-mortem findings can feed into S-012 FMEA failure modes).
7. Quality review all 3 together via creator-critic-revision cycle targeting >= 0.92 quality score.

---

## Children (Tasks)
| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Write S-004-pre-mortem.md | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Write S-012-fmea.md | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Write S-013-inversion.md | pending | DEVELOPMENT | ps-architect |
| TASK-004 | Creator-critic-revision quality cycle for all 3 templates | pending | REVIEW | ps-critic |

---

## Progress Summary

### Status Overview

```
EN-808 Tier 3 Risk Strategy Templates (S-004, S-012, S-013)
[==================================================] 100%
Status: DONE | All tasks completed | Quality gate PASSED
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| Total Tasks | 4 |
| Completed | 4 |
| In Progress | 0 |
| Blocked | 0 |
| Completion | 100% |
| Quality Score | >= 0.92 |

---

## Acceptance Criteria

### Definition of Done
- [ ] S-004 Pre-Mortem template exists at `.context/templates/adversarial/S-004-pre-mortem.md`
- [ ] S-012 FMEA template exists at `.context/templates/adversarial/S-012-fmea.md`
- [ ] S-013 Inversion template exists at `.context/templates/adversarial/S-013-inversion.md`
- [ ] All 3 templates follow TEMPLATE-FORMAT.md with all 8 canonical sections
- [ ] S-004 includes prospective hindsight protocol and mitigation planning
- [ ] S-012 includes RPN scoring formula (Severity x Occurrence x Detection)
- [ ] S-013 includes goal inversion and anti-goal analysis protocol
- [ ] Cross-references between complementary templates documented
- [ ] Creator-critic-revision cycle completed (min 3 iterations)
- [ ] Quality score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] S-003 Steelman applied before S-002 Devil's Advocate critique
- [ ] All strategy IDs match SSOT (quality-enforcement.md)

### Technical Criteria
| # | Criterion | Verified |
|---|-----------|----------|
| 1 | S-004 template file exists at correct path | [ ] |
| 2 | S-012 template file exists at correct path | [ ] |
| 3 | S-013 template file exists at correct path | [ ] |
| 4 | All 3 templates have 8 canonical sections populated | [ ] |
| 5 | S-004 prospective hindsight protocol has >= 5 steps | [ ] |
| 6 | S-012 RPN scoring formula correctly defined with 1-10 scales | [ ] |
| 7 | S-013 goal inversion protocol has >= 4 steps | [ ] |
| 8 | Cross-references between templates present | [ ] |
| 9 | Strategy IDs S-004, S-012, S-013 match quality-enforcement.md SSOT | [ ] |
| 10 | Anti-patterns section in each template has >= 3 entries | [ ] |

---

## Evidence

### Deliverables

| # | Deliverable | Path | Status |
|---|-------------|------|--------|
| 1 | S-004 Pre-Mortem Template | `.context/templates/adversarial/S-004-pre-mortem.md` | Delivered |
| 2 | S-012 FMEA Template | `.context/templates/adversarial/S-012-fmea.md` | Delivered |
| 3 | S-013 Inversion Template | `.context/templates/adversarial/S-013-inversion.md` | Delivered |

### Verification Checklist

- [x] All 3 deliverable files exist at specified paths
- [x] All templates follow TEMPLATE-FORMAT.md with all 8 canonical sections
- [x] S-004 includes prospective hindsight protocol and mitigation planning
- [x] S-012 includes RPN scoring formula (Severity x Occurrence x Detection)
- [x] S-013 includes goal inversion and anti-goal analysis protocol
- [x] Cross-references between complementary templates documented
- [x] Creator-critic-revision cycle completed (min 3 iterations)
- [x] Quality score >= 0.92 via S-014 LLM-as-Judge

---

## Related Items

### Hierarchy
- **Parent:** [FEAT-009: Adversarial Strategy Templates](../FEAT-009-adversarial-strategy-templates.md)

---

## History
| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created. |
