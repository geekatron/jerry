# TASK-002: Update skills/orchestration/PLAYBOOK.md with adversarial cycles at sync barriers

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
> **Parent:** EN-709
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

Update `skills/orchestration/PLAYBOOK.md` to integrate creator-critic-revision cycles at sync barriers. Define quality gate requirements per phase: each phase output must pass adversarial review (>= 0.92) before the pipeline advances. Document how adversarial review interleaves with existing sync barrier and cross-pollination mechanics.

---

## Acceptance Criteria

- [ ] PLAYBOOK.md integrates creator-critic-revision cycles at sync barriers
- [ ] Quality gate requirements defined per phase
- [ ] Phase advancement blocked until adversarial review passes (>= 0.92)
- [ ] Integration with existing sync barrier mechanics documented
- [ ] Integration with cross-pollination mechanics documented
- [ ] Entry and exit criteria for adversarial cycles at sync barriers defined
- [ ] Document follows markdown navigation standards (NAV-001 through NAV-006)

---

## Implementation Notes

- Reference EPIC-002 EN-307 for orchestration PLAYBOOK integration design
- Sync barriers already coordinate worker timing; adversarial review adds quality dimension
- The cycle at sync barriers: workers produce output -> critic reviews -> workers revise -> gate evaluates
- Consider how adversarial review interacts with parallel worker execution
- Pipeline should not advance past a sync barrier until all worker outputs pass quality gate

---

## Related Items

- Parent: [EN-709: Orchestration Adversarial Mode](EN-709-orchestration-adversarial.md)
- Depends on: EN-701 (SSOT for quality thresholds)
- Blocks: TASK-006 (adversarial review)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated PLAYBOOK.md | Markdown | skills/orchestration/PLAYBOOK.md |

### Verification

- [ ] Acceptance criteria verified
- [ ] PLAYBOOK.md renders correctly with navigation table
- [ ] Sync barrier adversarial integration is clearly documented

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation from EN-709 task decomposition |
