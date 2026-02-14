# TASK-005: Create strategy selection guidance for PS domain contexts

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Activity:** DEVELOPMENT
> **Created:** 2026-02-14
> **Parent:** EN-707
> **Assignee:** ps-analyst

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Change log |

---

## Summary

Create a decision matrix mapping problem-solving domain contexts (research, root cause analysis, architecture review, synthesis) to recommended adversarial strategies. This guidance helps agents select the most effective strategy for their current context rather than applying strategies arbitrarily.

---

## Acceptance Criteria

- [ ] Decision matrix maps PS contexts to recommended adversarial strategies
- [ ] Contexts covered include: research, root cause analysis, architecture review, synthesis
- [ ] Each context-strategy mapping includes rationale for why the strategy is effective
- [ ] Guidance is traceable to EPIC-002 EN-303 decision tree design
- [ ] Matrix references SSOT (EN-701) for strategy encodings
- [ ] Documentation follows markdown navigation standards

---

## Implementation Notes

- Reference EPIC-002 EN-303 for the decision tree for situational strategy selection
- The matrix should be actionable: given context X, use strategy Y because Z
- Consider a table format for quick lookup by agents
- Include fallback guidance for contexts not explicitly covered
- Strategies should be referenced by their SSOT encoding (e.g., S-001, S-002, etc.)

---

## Related Items

- Parent: [EN-707: Problem-Solving Adversarial Mode](EN-707-problem-solving-adversarial.md)
- Depends on: EN-701 (SSOT for strategy encodings)
- Depends on: EPIC-002 EN-303 (decision tree design)
- Blocks: TASK-006 (adversarial review)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Strategy selection matrix | Markdown | Integrated into SKILL.md or PLAYBOOK.md |

### Verification

- [ ] Acceptance criteria verified
- [ ] All major PS contexts are covered
- [ ] Strategy recommendations align with EPIC-002 EN-303

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation from EN-707 task decomposition |
