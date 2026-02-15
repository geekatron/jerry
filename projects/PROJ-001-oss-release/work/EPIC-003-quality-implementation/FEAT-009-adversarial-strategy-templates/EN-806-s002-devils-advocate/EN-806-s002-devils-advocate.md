# EN-806: S-002 Devil's Advocate Template

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Create structured dissent template for S-002 Devil's Advocate strategy
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
> **Effort:** 3

---

## Document Sections
| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary
Create the execution template for S-002 Devil's Advocate -- structured dissent strategy for challenging proposals. Used in C2+ quality cycles. Includes strongest counterargument protocol and bias detection.

**Technical Scope:**
- Extract Devil's Advocate methodology from research-15-adversarial-strategies.md (Strategy 3)
- Define counter-argument construction protocol with DA-NNN identifiers
- Define assumption extraction checklist for systematic challenge
- Define structured presentation format for dissent findings
- Define response requirement format ensuring actionable outcomes
- Integrate with S-003 Steelman (H-16: Steelman before critique)

---

## Problem Statement
S-002 Devil's Advocate is used in every C2+ quality cycle (see quality-enforcement.md Strategy Catalog) but has no concrete execution template defining the structured dissent protocol, counter-argument construction, or response requirement format. Without a standardized template, agents apply the strategy inconsistently, leading to shallow critiques that miss genuine weaknesses or overly aggressive critiques that waste revision cycles. The quality-enforcement SSOT mandates S-003 Steelman before S-002 Devil's Advocate (H-16), but without a template that encodes this dependency, agents may skip or reorder the protocol.

---

## Technical Approach
1. Extract Devil's Advocate methodology from research-15-adversarial-strategies.md (Strategy 3), capturing the core structured dissent protocol, role assignment mechanics, and counter-argument construction steps.
2. Adapt the methodology for Jerry's quality review context, including integration with the creator-critic-revision cycle and the H-16 requirement that S-003 Steelman must precede S-002.
3. Write the template following TEMPLATE-FORMAT.md with all 8 canonical sections: Purpose and Context, When to Use, Protocol Steps, Input/Output Format, Quality Criteria, Integration Points, Examples, and Anti-Patterns.
4. Include counter-argument construction protocol with DA-NNN identifiers for traceability.
5. Include assumption extraction checklist and structured presentation format.
6. Validate template via creator-critic-revision cycle targeting >= 0.92 quality score.

---

## Children (Tasks)
| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Extract S-002 Devil's Advocate methodology from research | pending | RESEARCH | ps-researcher |
| TASK-002 | Write S-002-devils-advocate.md following TEMPLATE-FORMAT | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Creator-critic-revision quality cycle | pending | REVIEW | ps-critic |

---

## Acceptance Criteria

### Definition of Done
- [ ] S-002 Devil's Advocate template exists at `.context/templates/adversarial/S-002-devils-advocate.md`
- [ ] Template includes counter-argument construction protocol with DA-NNN identifiers
- [ ] Template includes assumption extraction checklist
- [ ] Template includes structured presentation format for dissent findings
- [ ] Template includes response requirement format
- [ ] Template encodes H-16 dependency (S-003 Steelman must precede S-002)
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
| 3 | DA-NNN identifier format defined and demonstrated | [ ] |
| 4 | Assumption extraction checklist has >= 5 categories | [ ] |
| 5 | Integration with S-003 Steelman documented | [ ] |
| 6 | Anti-patterns section includes >= 3 common mistakes | [ ] |
| 7 | Strategy ID S-002 matches quality-enforcement.md SSOT | [ ] |

---

## Related Items

### Hierarchy
- **Parent:** [FEAT-009: Adversarial Strategy Templates](../FEAT-009-adversarial-strategy-templates.md)

---

## History
| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created. |
