# TASK-003: Update relevant agent files with strategy-specific guidance

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
> **Assignee:** ps-architect

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

Update relevant problem-solving agent files (ps-researcher, ps-analyst, ps-synthesizer, ps-reviewer) to add strategy-specific adversarial guidance. Each agent role should receive mappings to its most applicable adversarial strategies and instructions for participating in creator-critic-revision cycles.

---

## Acceptance Criteria

- [ ] ps-researcher agent file updated with applicable adversarial strategies
- [ ] ps-analyst agent file updated with applicable adversarial strategies
- [ ] ps-synthesizer agent file updated with applicable adversarial strategies
- [ ] ps-reviewer agent file updated with applicable adversarial strategies
- [ ] Each agent has clear guidance on its role in creator-critic-revision cycles
- [ ] Strategy mappings are traceable to EPIC-002 EN-304 agent-strategy design
- [ ] Agent files follow markdown navigation standards (NAV-001 through NAV-006)

---

## Implementation Notes

- Reference EPIC-002 EN-304 for agent-strategy mappings
- Agents acting as "creators" need guidance on producing high-quality first drafts
- Agents acting as "critics" need guidance on structured adversarial challenge techniques
- Not all agents need all strategies; map only the most applicable ones per role
- Consider adding a "Strategy Selection" section to each agent file

---

## Related Items

- Parent: [EN-707: Problem-Solving Adversarial Mode](EN-707-problem-solving-adversarial.md)
- Depends on: EN-701 (SSOT for strategy encodings)
- Blocks: TASK-006 (adversarial review)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated ps-researcher agent | Markdown | skills/problem-solving/agents/ps-researcher.md |
| Updated ps-analyst agent | Markdown | skills/problem-solving/agents/ps-analyst.md |
| Updated ps-synthesizer agent | Markdown | skills/problem-solving/agents/ps-synthesizer.md |
| Updated ps-reviewer agent | Markdown | skills/problem-solving/agents/ps-reviewer.md |

### Verification

- [ ] Acceptance criteria verified
- [ ] All updated agent files render correctly
- [ ] Strategy mappings align with EPIC-002 EN-304

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation from EN-707 task decomposition |
