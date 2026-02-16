# TASK-004: Integration testing with EN-603 selector and EN-605 metrics

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
id: "TASK-004"
work_type: TASK
title: "Integration testing with EN-603 selector and EN-605 metrics"
description: |
  Verify that custom strategies integrate correctly with EN-603
  (automated strategy selector) and EN-605 (effectiveness metrics)
  components. Test registration, discovery, and deregistration
  workflows across components.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "nse-integration"
created_by: "Claude"
created_at: "2026-02-12"
updated_at: "2026-02-13"
parent_id: "EN-604"
tags:
  - "epic-002"
  - "feat-007"
effort: null
acceptance_criteria: |
  - Custom strategies appear in EN-603 selector recommendations after registration
  - Custom strategies are tracked by EN-605 effectiveness metrics after registration
  - Deregistered strategies are properly removed from selector and metrics tracking
  - Integration tests cover registration, discovery, and deregistration workflows
  - Cross-platform compatibility verified (macOS, Windows, Linux)
due_date: null
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Verify that custom strategies integrate correctly with EN-603 (automated strategy selector) and EN-605 (effectiveness metrics) components. Test that registered custom strategies appear in the selector's recommendation pool, that custom strategies are tracked by the effectiveness metrics system after registration, and that deregistered strategies are properly removed from both the selector and metrics tracking.

### Acceptance Criteria

- [ ] Custom strategies appear in EN-603 selector recommendations after registration
- [ ] Custom strategies are tracked by EN-605 effectiveness metrics after registration
- [ ] Deregistered strategies are properly removed from selector and metrics tracking
- [ ] Integration tests cover registration, discovery, and deregistration workflows
- [ ] Cross-platform compatibility verified (macOS, Windows, Linux)

### Implementation Notes

- Requires TASK-003 registration/discovery mechanism to complete
- Integration testing spans multiple enablers (EN-603, EN-604, EN-605)
- Test the full lifecycle: register -> discover -> use in selector -> track metrics -> deregister
- Verify cross-platform file path handling

### Related Items

- Parent: [EN-604: Custom Strategy Creation Tooling](../EN-604-custom-strategy-tooling.md)
- Depends on: [TASK-003](./TASK-003-implement-registration-discovery.md)
- Downstream: [TASK-005](./TASK-005-adversarial-critique-schema.md) (depends on this task)

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
