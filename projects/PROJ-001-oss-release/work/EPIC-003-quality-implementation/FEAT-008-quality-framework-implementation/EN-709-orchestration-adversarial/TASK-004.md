# TASK-004: Enhance cross-pollination with adversarial strategy selection

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
> **Parent:** EN-709
> **Assignee:** ps-analyst

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

Enhance the orchestration cross-pollination mechanism with adversarial strategy selection. When workers exchange artifacts during cross-pollination, the receiving worker should apply adversarial critique before integration. Define which strategies are most effective for cross-pollination contexts and how the critique-integration cycle works.

---

## Acceptance Criteria

- [ ] Cross-pollination enhanced with adversarial critique step before integration
- [ ] Adversarial strategy selection guidance defined for cross-pollination contexts
- [ ] Critique-integration cycle documented (receive artifact -> critique -> integrate/reject)
- [ ] Strategy recommendations mapped to cross-pollination scenario types
- [ ] Integration with existing cross-pollination mechanics preserved
- [ ] Strategy references use SSOT (EN-701) encodings
- [ ] Documentation follows markdown navigation standards

---

## Implementation Notes

- Reference EPIC-002 EN-307 for cross-pollination enhancement design
- Cross-pollination currently shares artifacts between parallel workers; adversarial adds quality filter
- The receiving worker acts as "critic" of the sending worker's artifact
- Not all cross-pollination needs full adversarial review; define when it applies
- Consider lightweight critique for routine cross-pollination, full critique for critical artifacts
- Strategies like "devil's advocate" and "assumption challenging" may be most effective here

---

## Related Items

- Parent: [EN-709: Orchestration Adversarial Mode](EN-709-orchestration-adversarial.md)
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
| Cross-pollination enhancement | Markdown | Integrated into PLAYBOOK.md or SKILL.md |

### Verification

- [ ] Acceptance criteria verified
- [ ] Cross-pollination adversarial integration preserves existing mechanics
- [ ] Strategy selection guidance is actionable for orchestration agents

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation from EN-709 task decomposition |
