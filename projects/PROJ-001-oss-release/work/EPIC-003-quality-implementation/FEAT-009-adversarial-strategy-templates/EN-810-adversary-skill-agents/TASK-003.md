# TASK-003: Write adv-scorer.md agent

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
> **Parent:** EN-810

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

Create the LLM-as-Judge scoring agent at `skills/adversary/agents/adv-scorer.md`. This agent implements the S-014 rubric as a dedicated scoring engine, applying the 6-dimension quality assessment with strict scoring discipline to counteract leniency bias. It is the final arbiter of whether a deliverable passes the quality gate.

The agent must implement the following scoring methodology:

1. **Dimension-level scoring**: Score each of the 6 dimensions independently on a 0.00-1.00 scale. Each dimension must be evaluated against specific criteria:
   - **Completeness (0.20)**: All required sections present, no gaps in coverage, all acceptance criteria addressable.
   - **Internal Consistency (0.20)**: No contradictions between sections, terminology used consistently, cross-references valid.
   - **Methodological Rigor (0.20)**: Approach is systematic, steps are reproducible, methodology is grounded in established practice.
   - **Evidence Quality (0.15)**: Claims supported by evidence, sources cited, examples concrete and verifiable.
   - **Actionability (0.15)**: Instructions are clear and executable, outputs are well-defined, users can follow without ambiguity.
   - **Traceability (0.10)**: References to source documents present, parent-child relationships documented, change history maintained.

2. **Weighted composite calculation**: Calculate the weighted composite score as the sum of (dimension_score * dimension_weight) across all 6 dimensions. The weights must sum to exactly 1.00.

3. **Threshold comparison**: Compare the weighted composite against the >= 0.92 threshold (H-13). Determine PASS/FAIL status with clear justification.

4. **Improvement recommendations**: For any dimension scoring below 0.90, generate specific, actionable improvement recommendations that the creator can apply in the next revision cycle.

5. **Leniency bias counteraction**: Apply strict rubric interpretation per quality-enforcement.md L2-REINJECT guidance. Scores of 0.95+ require explicit justification. Default to conservative scoring when evidence is ambiguous.

### Acceptance Criteria
- [ ] Agent file created at `skills/adversary/agents/adv-scorer.md`
- [ ] All 6 dimensions defined with evaluation criteria and correct weights
- [ ] Dimension weights sum to exactly 1.00 (0.20+0.20+0.20+0.15+0.15+0.10)
- [ ] Weighted composite calculation formula documented
- [ ] Threshold comparison against >= 0.92 with PASS/FAIL determination
- [ ] Improvement recommendations generated for dimensions scoring < 0.90
- [ ] Leniency bias counteraction measures documented
- [ ] Scoring output format defined (dimension scores, composite, status, recommendations)
- [ ] Calibration guidance included (what 0.70, 0.80, 0.90, 0.95, 1.00 look like)
- [ ] Agent follows markdown navigation standards (H-23, H-24)
- [ ] P-003 compliance: agent does not spawn sub-agents
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items
- Parent: [EN-810: Adversary Skill Agents](EN-810-adversary-skill-agents.md)
- Depends on: quality-enforcement.md (S-014 rubric dimensions and weights)
- Depends on: ADR-EPIC002-001 (LLM-as-Judge scoring methodology)
- Parallel: TASK-001 (adv-selector), TASK-002 (adv-executor)
- Blocks: TASK-004 (quality cycle review)

---

## Evidence
### Deliverables
| Deliverable | Type | Link |
|-------------|------|------|
| adv-scorer agent definition | Agent markdown | `skills/adversary/agents/adv-scorer.md` |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
