# TASK-003: Update agent files with quality-gate enforcement responsibilities

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

Update orchestration agent files (orch-planner, orch-tracker, orch-synthesizer) to add quality-gate enforcement responsibilities. Define how each agent participates in adversarial review at phase gates and sync barriers, including scoring responsibilities and gate pass/fail decisions.

---

## Acceptance Criteria

- [ ] orch-planner agent file updated with quality-gate planning responsibilities
- [ ] orch-tracker agent file updated with quality-gate tracking and enforcement responsibilities
- [ ] orch-synthesizer agent file updated with quality-gate synthesis responsibilities
- [ ] Each agent has clear guidance on its role in phase gate enforcement
- [ ] Scoring responsibilities and gate pass/fail decision authority defined
- [ ] Agent files follow markdown navigation standards (NAV-001 through NAV-006)

---

## Implementation Notes

- Reference EPIC-002 EN-307 for orchestration agent quality-gate design
- orch-planner: plans which phases require adversarial review, selects strategies
- orch-tracker: monitors quality scores, enforces gate pass/fail, escalates failures
- orch-synthesizer: synthesizes cross-worker feedback incorporating adversarial findings
- Define clear separation of responsibilities to avoid confusion between agents

---

## Related Items

- Parent: [EN-709: Orchestration Adversarial Mode](EN-709-orchestration-adversarial.md)
- Depends on: EN-701 (SSOT for quality thresholds)
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
| Updated orch-planner agent | Markdown | skills/orchestration/agents/orch-planner.md |
| Updated orch-tracker agent | Markdown | skills/orchestration/agents/orch-tracker.md |
| Updated orch-synthesizer agent | Markdown | skills/orchestration/agents/orch-synthesizer.md |

### Verification

- [ ] Acceptance criteria verified
- [ ] All updated agent files render correctly
- [ ] Quality-gate responsibilities are clearly delineated between agents

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation from EN-709 task decomposition |
