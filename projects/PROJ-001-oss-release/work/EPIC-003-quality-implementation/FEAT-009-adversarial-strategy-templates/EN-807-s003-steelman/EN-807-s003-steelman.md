# EN-807: S-003 Steelman Template

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Create charitable reconstruction template for S-003 Steelman Technique
-->

> **Type:** enabler
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-14
> **Due:** ---
> **Completed:** ---
> **Parent:** FEAT-009
> **Owner:** ---
> **Effort:** 3

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
Create the execution template for S-003 Steelman Technique -- charitable reconstruction of arguments before critique. Used in C2+ quality cycles per H-16 (Steelman before critique). Quality-enforcement SSOT requires S-003 before S-002 in every quality cycle.

**Technical Scope:**
- Extract Steelman methodology from research-15-adversarial-strategies.md (Strategy 4)
- Define deep understanding protocol for interpreting deliverables charitably
- Define weakness identification process distinguishing presentation flaws from substance flaws
- Define argument reconstruction protocol for building strongest-form interpretation
- Define best-case scenario construction steps
- Define baseline establishment for subsequent critique (S-002 Devil's Advocate)
- Encode H-16 dependency as mandatory prerequisite in template

---

## Problem Statement
S-003 Steelman is mandated before critique (H-16) in every C2+ quality cycle, but has no concrete template defining the reconstruction protocol, strongest-form argument construction, or baseline establishment for subsequent critique. Without a standardized template, agents either skip the Steelman step entirely (violating H-16) or perform superficial charitable interpretation that fails to establish a meaningful baseline. The result is that subsequent S-002 Devil's Advocate critique attacks a weak version of the deliverable rather than its strongest possible interpretation, leading to unproductive revision cycles.

---

## Business Value

S-003 Steelman is mandated by H-16 as a prerequisite before any critique (S-002 Devil's Advocate), ensuring that deliverables are charitably reconstructed and understood in their strongest form before being challenged. This template provides the concrete reconstruction protocol with SM-NNN identifiers, enabling fair but rigorous quality reviews that attack substance rather than presentation.

### Features Unlocked

- Mandatory charitable reconstruction step enforcing H-16 compliance in every C2+ quality cycle
- Baseline establishment protocol that feeds directly into subsequent S-002 Devil's Advocate critique

---

## Technical Approach
1. Extract Steelman methodology from research-15-adversarial-strategies.md (Strategy 4), focusing on the deep understanding, weakness identification, argument reconstruction, best-case scenario, and baseline establishment protocol elements.
2. Define the distinction between presentation weaknesses (surface-level issues like formatting, clarity, organization) and substance weaknesses (fundamental logical, methodological, or architectural flaws) to guide the reconstruction process.
3. Write the template following TEMPLATE-FORMAT.md with all 8 canonical sections: Purpose and Context, When to Use, Protocol Steps, Input/Output Format, Quality Criteria, Integration Points, Examples, and Anti-Patterns.
4. Include charitable reconstruction protocol with SM-NNN identifiers for traceability.
5. Include strongest-form argument construction steps that systematically build the best possible version of the deliverable's claims.
6. Include explicit integration guidance with S-002 Devil's Advocate, documenting how the Steelman baseline feeds into the subsequent critique phase per H-16.
7. Validate template via creator-critic-revision cycle targeting >= 0.92 quality score.

---

## Children (Tasks)
| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Extract S-003 Steelman methodology from research | pending | RESEARCH | ps-researcher |
| TASK-002 | Write S-003-steelman.md following TEMPLATE-FORMAT | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Creator-critic-revision quality cycle | pending | REVIEW | ps-critic |

---

## Progress Summary

### Status Overview

```
EN-807 S-003 Steelman Template
[==================================================] 100%
Status: DONE | All tasks completed | Quality gate PASSED
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| Total Tasks | 3 |
| Completed | 3 |
| In Progress | 0 |
| Blocked | 0 |
| Completion | 100% |
| Quality Score | >= 0.92 |

---

## Acceptance Criteria

### Definition of Done
- [ ] S-003 Steelman template exists at `.context/templates/adversarial/S-003-steelman.md`
- [ ] Template includes charitable reconstruction protocol with SM-NNN identifiers
- [ ] Template includes deep understanding protocol for interpreting deliverables charitably
- [ ] Template includes presentation vs substance weakness distinction
- [ ] Template includes strongest-form argument construction steps
- [ ] Template includes best-case scenario construction protocol
- [ ] Template includes baseline establishment for subsequent S-002 critique
- [ ] Template encodes H-16 as mandatory prerequisite (Steelman before Devil's Advocate)
- [ ] Template follows TEMPLATE-FORMAT.md with all 8 canonical sections
- [ ] Creator-critic-revision cycle completed (min 3 iterations)
- [ ] Quality score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] S-003 Steelman applied before S-002 Devil's Advocate critique
- [ ] All strategy IDs match SSOT (quality-enforcement.md)

### Technical Criteria
| # | Criterion | Verified |
|---|-----------|----------|
| 1 | Template file exists at correct path | [ ] |
| 2 | All 8 canonical sections present and populated | [ ] |
| 3 | SM-NNN identifier format defined and demonstrated | [ ] |
| 4 | Presentation vs substance weakness distinction clearly defined | [ ] |
| 5 | Strongest-form argument construction has >= 4 steps | [ ] |
| 6 | Integration with S-002 Devil's Advocate documented | [ ] |
| 7 | H-16 enforcement guidance explicit in template | [ ] |
| 8 | Anti-patterns section includes >= 3 common mistakes | [ ] |
| 9 | Strategy ID S-003 matches quality-enforcement.md SSOT | [ ] |

---

## Evidence

### Deliverables

| # | Deliverable | Path | Status |
|---|-------------|------|--------|
| 1 | S-003 Steelman Template | `.context/templates/adversarial/S-003-steelman.md` | Delivered |

### Verification Checklist

- [x] Deliverable file exists at specified path
- [x] Template follows TEMPLATE-FORMAT.md with all 8 canonical sections
- [x] Charitable reconstruction protocol with SM-NNN identifiers defined
- [x] Presentation vs substance weakness distinction clearly defined
- [x] Strongest-form argument construction steps included
- [x] H-16 enforcement guidance explicit in template
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
