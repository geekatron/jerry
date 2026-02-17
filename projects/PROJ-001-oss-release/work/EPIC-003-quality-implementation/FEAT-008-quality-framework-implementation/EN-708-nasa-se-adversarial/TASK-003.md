# TASK-003: Update relevant agent files with strategy-specific guidance

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** DONE
> **Priority:** high
> **Activity:** DEVELOPMENT
> **Created:** 2026-02-14
> **Parent:** EN-708
> **Assignee:** ps-architect

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Time Tracking](#time-tracking) | Effort estimates and actuals |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Change log |

---

## Summary

Update relevant NASA-SE agent files (nse-requirements, nse-verification, nse-validation, nse-risk) to add strategy-specific adversarial guidance. Each agent role should receive mappings to its most applicable adversarial strategies and instructions for participating in creator-critic-revision cycles within the SE workflow.

---

## Acceptance Criteria

- [ ] nse-requirements agent file updated with applicable adversarial strategies
- [ ] nse-verification agent file updated with applicable adversarial strategies
- [ ] nse-validation agent file updated with applicable adversarial strategies
- [ ] nse-risk agent file updated with applicable adversarial strategies
- [ ] Each agent has clear guidance on its role in creator-critic-revision cycles
- [ ] Strategy mappings are traceable to EPIC-002 EN-305 agent-strategy design
- [ ] Agent files follow markdown navigation standards (NAV-001 through NAV-006)

---

## Implementation Notes

- Reference EPIC-002 EN-305 for agent-strategy mappings in the NSE context
- Requirements agents benefit from completeness and ambiguity detection strategies
- Verification agents benefit from assumption challenging and boundary testing
- Risk agents benefit from failure mode analysis and stress-testing strategies
- Not all agents need all strategies; map only the most applicable per role

---

## Related Items

- Parent: [EN-708: NASA-SE Adversarial Mode](EN-708-nasa-se-adversarial.md)
- Depends on: EN-701 (SSOT for strategy encodings)
- Blocks: TASK-006 (adversarial review)

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
| Updated nse-requirements agent | Markdown | skills/nasa-se/agents/nse-requirements.md |
| Updated nse-verification agent | Markdown | skills/nasa-se/agents/nse-verification.md |
| Updated nse-validation agent | Markdown | skills/nasa-se/agents/nse-validation.md |
| Updated nse-risk agent | Markdown | skills/nasa-se/agents/nse-risk.md |

### Verification

- [ ] Acceptance criteria verified
- [ ] All updated agent files render correctly
- [ ] Strategy mappings align with EPIC-002 EN-305

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation from EN-708 task decomposition |
