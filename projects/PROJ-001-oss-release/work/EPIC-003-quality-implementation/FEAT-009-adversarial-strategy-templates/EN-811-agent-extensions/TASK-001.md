# TASK-001: Update ps-critic.md with strategy template references

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

Add a "Strategy Template References" section to `skills/problem-solving/agents/ps-critic.md` that points to the concrete adversarial strategy execution templates in `.context/templates/adversarial/`. The ps-critic agent is the primary adversarial reviewer in the /problem-solving skill and needs direct references to the 4 strategies it most commonly applies:

- **S-002 Devil's Advocate** at `.context/templates/adversarial/S-002-devils-advocate.md` -- Structured dissent protocol for challenging proposals and assumptions.
- **S-003 Steelman** at `.context/templates/adversarial/S-003-steelman.md` -- Strongest interpretation construction before critique (H-16 requires S-003 before S-002).
- **S-007 Constitutional AI Critique** at `.context/templates/adversarial/S-007-constitutional-ai.md` -- Constitutional compliance checking against HARD rules.
- **S-014 LLM-as-Judge** at `.context/templates/adversarial/S-014-llm-as-judge.md` -- Quality scoring with 6-dimension rubric.

The section must include:
- Template path for each strategy
- When to use each strategy (criticality-based triggers)
- Execution ordering requirements (S-003 before S-002 per H-16)
- Instructions to load and follow the Execution Protocol section of each template

### Acceptance Criteria
- [ ] ps-critic.md updated with "Strategy Template References" section
- [ ] References for S-002, S-003, S-007, S-014 with correct template paths
- [ ] H-16 ordering documented (S-003 Steelman before S-002 Devil's Advocate)
- [ ] Criticality-based triggers specified (which strategies at which level)
- [ ] Instructions to load and follow Execution Protocol section
- [ ] Navigation table updated to include new section
- [ ] All strategy IDs match quality-enforcement.md SSOT
- [ ] Quality gate: Deliverable reviewed via creator-critic-revision cycle (min 3 iterations)
- [ ] Quality gate: Score >= 0.92 via S-014 LLM-as-Judge rubric
- [ ] Quality gate: S-003 Steelman applied before S-002 Devil's Advocate critique

### Related Items
- Parent: [EN-811: Agent Extensions](EN-811-agent-extensions.md)
- Depends on: EN-806 (S-002 template must exist)
- Depends on: EN-807 (S-003 template must exist)
- Depends on: EN-805 (S-007 template must exist)
- Depends on: EN-803 (S-014 template must exist)

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
| Updated ps-critic.md | Agent markdown | `skills/problem-solving/agents/ps-critic.md` |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History
| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. |
