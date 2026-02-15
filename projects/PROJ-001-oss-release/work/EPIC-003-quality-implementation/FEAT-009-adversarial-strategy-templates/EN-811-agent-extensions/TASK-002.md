# TASK-002: Update ps-reviewer.md with strategy template references

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
> **Parent:** EN-811

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

Add a "Strategy Template References" section to `skills/problem-solving/agents/ps-reviewer.md` that points to the concrete adversarial strategy execution templates in `.context/templates/adversarial/`. The ps-reviewer agent performs quality reviews in the /problem-solving skill and needs direct references to the 3 strategies most relevant to its review role:

- **S-010 Self-Refine** at `.context/templates/adversarial/S-010-self-refine.md` -- Self-review protocol for iterative improvement before external review.
- **S-014 LLM-as-Judge** at `.context/templates/adversarial/S-014-llm-as-judge.md` -- Quality scoring with 6-dimension rubric for formal review assessments.
- **S-003 Steelman** at `.context/templates/adversarial/S-003-steelman.md` -- Strongest interpretation construction to ensure fair review.

The section must include:
- Template path for each strategy
- When to use each strategy in the review workflow
- Instructions to load and follow the Execution Protocol section of each template
- How review findings feed into the creator-critic-revision cycle

### Acceptance Criteria
- [ ] ps-reviewer.md updated with "Strategy Template References" section
- [ ] References for S-010, S-014, S-003 with correct template paths
- [ ] Review workflow integration documented (when to apply each strategy)
- [ ] Instructions to load and follow Execution Protocol section
- [ ] Connection to creator-critic-revision cycle documented
- [ ] Navigation table updated to include new section
- [ ] All strategy IDs match quality-enforcement.md SSOT
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items
- Parent: [EN-811: Agent Extensions](EN-811-agent-extensions.md)
- Depends on: EN-804 (S-010 template must exist)
- Depends on: EN-803 (S-014 template must exist)
- Depends on: EN-807 (S-003 template must exist)

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
| Updated ps-reviewer.md | Agent markdown | `skills/problem-solving/agents/ps-reviewer.md` |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
