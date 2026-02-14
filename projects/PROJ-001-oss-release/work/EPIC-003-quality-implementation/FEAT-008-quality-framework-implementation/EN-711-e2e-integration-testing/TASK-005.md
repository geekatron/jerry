# TASK-005: Create Skill Adversarial Mode Integration Tests

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 0.1.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Summary

```yaml
id: "TASK-005"
work_type: TASK
title: "Create skill adversarial mode integration tests"
description: |
  Write tests that verify the Problem-Solving (PS), NASA-SE (NSE), and Orchestration
  (ORCH) skills correctly activate adversarial mode when triggered and produce
  quality-scored outputs. Validates L4 enforcement integration across all three skills.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-711"
tags:
  - "e2e-testing"
  - "adversarial-mode"
  - "skill-integration"
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Create integration tests for the adversarial mode of all three quality-enforcing skills:

1. **PS (Problem-Solving) adversarial mode** -- Verify that PS skill activates adversarial analysis when quality triggers are detected, producing scored critique outputs
2. **NSE (NASA-SE) adversarial mode** -- Verify that NSE skill activates verification/validation adversarial mode with quality-scored assessments
3. **ORCH (Orchestration) adversarial mode** -- Verify that ORCH skill activates quality gate enforcement at phase transitions, blocking progression on failures
4. **Cross-skill interaction** -- Verify that adversarial outputs from one skill can be consumed by another (e.g., PS critique feeding NSE verification)

### Acceptance Criteria

- [ ] PS adversarial mode integration tests implemented
- [ ] NSE adversarial mode integration tests implemented
- [ ] ORCH adversarial mode integration tests implemented
- [ ] Cross-skill adversarial interaction tests implemented
- [ ] Tests verify quality-scored output format and content
- [ ] All tests pass via `uv run pytest tests/e2e/`

### Implementation Notes

- Reference EN-707 (PS adversarial mode), EN-708 (NSE adversarial mode), EN-709 (ORCH adversarial mode)
- Test adversarial activation triggers (quality keywords, review requests, phase gates)
- Verify output includes quality scores and structured critique
- Consider mock skill invocations if full skill execution is too expensive for E2E

### Related Items

- Parent: [EN-711: E2E Integration Testing](EN-711-e2e-integration-testing.md)
- Depends on: EN-707 (PS adversarial mode), EN-708 (NSE adversarial mode), EN-709 (ORCH adversarial mode)
- Blocks: TASK-007 (adversarial review of test completeness)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Skill adversarial mode tests | Test suite | `tests/e2e/` |

### Verification

- [ ] Acceptance criteria verified
- [ ] All skill adversarial mode tests pass
- [ ] Tests cover activation triggers, output format, and cross-skill interaction
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------------|-------------|--------------------------------|
| 2026-02-14 | Created | Initial creation from EN-711 task decomposition |
