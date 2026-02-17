# TASK-002: Design Adversarial Mode Integration for ps-critic

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
id: "TASK-002"
work_type: TASK
title: "Design adversarial mode integration for ps-critic"
description: |
  Design the adversarial mode architecture for ps-critic. Each of the 10 selected strategies
  becomes a named mode with its own prompt template, evaluation criteria, output format, and
  applicability metadata from EN-303.
classification: ENABLER
status: BACKLOG
resolution: null
priority: CRITICAL
assignee: "ps-architect"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-304"
tags:
  - "epic-002"
  - "feat-004"
effort: null
acceptance_criteria: |
  - Architecture design covers all 10 adversarial modes with distinct definitions
  - Each mode has: name, prompt template structure, evaluation criteria, output format
  - Mode switching mechanism is defined (how to change between modes)
  - Mode composition design supports sequential multi-mode pipelines
  - Fallback behavior for unspecified mode selection is defined
due_date: null
activity: DESIGN
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Design the adversarial mode architecture for ps-critic. Each of the 10 selected strategies becomes a named mode with its own prompt template, evaluation criteria, output format, and applicability metadata (from EN-303). Define mode switching, composition (multiple modes in sequence), and fallback behavior when no mode is explicitly selected.

### Acceptance Criteria

- [ ] Architecture design covers all 10 adversarial modes with distinct definitions
- [ ] Each mode has: name, prompt template structure, evaluation criteria, output format
- [ ] Mode switching mechanism is defined (how to change between modes)
- [ ] Mode composition design supports sequential multi-mode pipelines
- [ ] Fallback behavior for unspecified mode selection is defined

### Implementation Notes

Depends on TASK-001 (requirements). Uses ps-architect agent. Core design work for ps-critic adversarial modes. Feeds into TASK-003 (invocation protocol) and TASK-004 (implementation).

### Related Items

- Parent: [EN-304](../EN-304-problem-solving-skill-enhancement.md)
- Depends on: [TASK-001](./TASK-001-define-ps-skill-requirements.md)
- Feeds into: [TASK-003](./TASK-003-design-invocation-protocol.md), [TASK-004](./TASK-004-implement-ps-critic-spec-updates.md)

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
