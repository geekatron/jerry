# TASK-007: Update Orchestration SKILL.md

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | YAML metadata |
| [Content](#content) | Description and acceptance criteria |
| [Time Tracking](#time-tracking) | Effort estimates |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes |

---

## Frontmatter

```yaml
id: "TASK-007"
work_type: TASK
title: "Update orchestration SKILL.md with adversarial patterns"
description: |
  Update the /orchestration SKILL.md to document adversarial loop patterns, automatic
  adversarial cycle generation, quality gate enforcement, and adversarial synthesis capabilities.
classification: ENABLER
status: BACKLOG
resolution: null
priority: CRITICAL
assignee: "ps-architect"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-307"
tags:
  - "epic-002"
  - "feat-004"
effort: null
acceptance_criteria: |
  - SKILL.md documents adversarial loop patterns with workflow diagrams
  - Automatic adversarial cycle generation is documented with examples
  - Quality gate enforcement at sync barriers is documented
  - Adversarial synthesis output format is documented
  - Documentation follows the Triple-Lens format (L0/L1/L2)
due_date: null
activity: DOCUMENTATION
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Update the /orchestration SKILL.md to document adversarial loop patterns, automatic adversarial cycle generation, quality gate enforcement, and adversarial synthesis capabilities. Include workflow diagrams showing the creator->critic->revision pattern and examples of auto-embedded adversarial cycles.

### Acceptance Criteria

- [ ] SKILL.md documents adversarial loop patterns with workflow diagrams
- [ ] Automatic adversarial cycle generation is documented with examples
- [ ] Quality gate enforcement at sync barriers is documented
- [ ] Adversarial synthesis output format is documented
- [ ] Documentation follows the Triple-Lens format (L0/L1/L2)

### Implementation Notes

Depends on TASK-006 (orch-synthesizer spec). Uses ps-architect agent. Can run in parallel with TASK-008 and TASK-009. Feeds into TASK-010 (code review).

### Related Items

- Parent: [EN-307](../EN-307-orchestration-skill-enhancement.md)
- Depends on: [TASK-006](./TASK-006-implement-orch-synthesizer-spec.md)
- Feeds into: [TASK-010](./TASK-010-code-review.md)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | -- |
| Remaining Work | -- |
| Time Spent | -- |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| -- | -- | -- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-12 | Created | Initial creation |
