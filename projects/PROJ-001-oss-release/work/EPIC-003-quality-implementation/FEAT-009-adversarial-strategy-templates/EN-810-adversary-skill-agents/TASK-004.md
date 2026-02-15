# TASK-004: Creator-critic-revision quality cycle for all agents

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** DONE
> **Priority:** HIGH
> **Activity:** REVIEW
> **Agents:** ps-critic
> **Created:** 2026-02-14
> **Parent:** EN-810

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

Apply the creator-critic-revision quality cycle to all 3 adversary skill agent definitions produced by TASK-001 (adv-selector), TASK-002 (adv-executor), and TASK-003 (adv-scorer). This review task ensures all agents meet the >= 0.92 quality threshold per H-13 through a minimum of 3 iterations of the creator-critic-revision cycle per H-14.

The quality cycle for each agent must evaluate:
- **Completeness**: All required sections present, input/output formats fully specified, all criticality mappings or dimensions covered.
- **Internal Consistency**: No contradictions between agents (e.g., adv-selector's strategy sets must match what adv-executor expects to load), terminology consistent across all three agents.
- **Methodological Rigor**: Agent protocols are systematic, reproducible, and grounded in the quality-enforcement.md framework.
- **Cross-agent integration**: The three agents work together as a coherent system. adv-selector's output feeds adv-executor's input, adv-executor's output feeds adv-scorer's input, and adv-scorer's output determines pass/fail for the quality gate.
- **P-003 compliance**: None of the agents spawn sub-agents.

### Acceptance Criteria
- [ ] adv-selector.md reviewed with >= 3 creator-critic-revision iterations
- [ ] adv-executor.md reviewed with >= 3 creator-critic-revision iterations
- [ ] adv-scorer.md reviewed with >= 3 creator-critic-revision iterations
- [ ] Cross-agent consistency verified (selector output -> executor input -> scorer input)
- [ ] S-003 Steelman applied before S-002 Devil's Advocate in each iteration (H-16)
- [ ] S-014 LLM-as-Judge scoring applied with all 6 dimensions and correct weights
- [ ] All three agents achieve weighted composite score >= 0.92
- [ ] P-003 compliance verified across all agents
- [ ] Revision history documenting each iteration's findings and improvements
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items
- Parent: [EN-810: Adversary Skill Agents](EN-810-adversary-skill-agents.md)
- Depends on: TASK-001 (adv-selector must exist)
- Depends on: TASK-002 (adv-executor must exist)
- Depends on: TASK-003 (adv-scorer must exist)

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
| adv-selector quality review report | Review artifact | --- |
| adv-executor quality review report | Review artifact | --- |
| adv-scorer quality review report | Review artifact | --- |
| Cross-agent consistency analysis | Analysis document | --- |
| Iteration history (scores per iteration per agent) | Quality evidence | --- |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
