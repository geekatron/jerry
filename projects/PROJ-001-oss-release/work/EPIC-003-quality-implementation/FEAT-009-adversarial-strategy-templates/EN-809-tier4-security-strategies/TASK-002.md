# TASK-002: Write S-011-cove.md

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
> **Parent:** EN-809

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

Create the Chain-of-Verification (CoVe) execution template at `.context/templates/adversarial/S-011-cove.md`. This template defines the factual verification protocol for claims and documentation within the Jerry quality framework. CoVe (S-011, composite score 3.75) is a Structured Decomposition strategy used in C3+ quality cycles.

The template must include:
- **Claim extraction**: Protocol for systematically identifying verifiable claims in deliverables (documents, ADRs, synthesis artifacts), including claim categorization (factual, quantitative, referential, causal).
- **Verification plan**: Structured approach to generating verification questions for each extracted claim, with independence requirements ensuring verification does not rely on the original source.
- **Independent verification**: Step-by-step execution protocol with CV-NNN identifiers for each verification item, verification method selection (source lookup, cross-reference, logical derivation, computation), and status tracking.
- **Confidence scoring**: Methodology for assigning confidence levels to verified claims (Verified, Partially Verified, Unverified, Contradicted) with supporting evidence requirements for each level.

### Acceptance Criteria
- [ ] Template file created at `.context/templates/adversarial/S-011-cove.md`
- [ ] Template follows TEMPLATE-FORMAT.md with all 8 canonical sections (Identity, Purpose, Prerequisites, Execution Protocol, Output Format, Scoring Rubric, Examples, Integration)
- [ ] Claim extraction section includes >= 4 claim categories with identification heuristics
- [ ] Verification plan section includes independence requirements and question generation protocol
- [ ] Independent verification section defines CV-NNN identifier format with verification method taxonomy
- [ ] Confidence scoring section includes >= 4 confidence levels with evidence thresholds
- [ ] Integration section maps S-011 to C3+ criticality levels and identifies companion strategies
- [ ] Anti-patterns section includes >= 3 common CoVe mistakes (e.g., circular verification, confirmation bias)
- [ ] Strategy ID S-011 matches quality-enforcement.md SSOT entry (composite score 3.75, family: Structured Decomposition)
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items
- Parent: [EN-809: Tier 4 Security Strategy Templates](EN-809-tier4-security-strategies.md)
- Depends on: EN-801 (TEMPLATE-FORMAT.md must exist)
- Parallel: TASK-001 (S-001 Red Team template)
- Blocks: TASK-003 (quality cycle review)

---

## Evidence
### Deliverables
| Deliverable | Type | Link |
|-------------|------|------|
| S-011 Chain-of-Verification template | Strategy template | `.context/templates/adversarial/S-011-cove.md` |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
