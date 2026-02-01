# TASK-002: Verify Context Token Count at Session Start

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
id: "TASK-002"
work_type: TASK
title: "Verify Context Token Count at Session Start"
description: |
  Verify that the context token count at session start meets the
  target of less than 5,000 tokens.

classification: ENABLER
status: BACKLOG
resolution: null
priority: CRITICAL
assignee: null
created_by: "Claude"
created_at: "2026-02-01T00:00:00Z"
updated_at: "2026-02-01T00:00:00Z"
parent_id: "EN-204"
tags:
  - enabler
  - validation
  - tokens

effort: 1
acceptance_criteria: |
  - Token count measured
  - Count is < 5,000 tokens
  - Reduction from ~10,000 verified
  - Results documented
due_date: null

activity: TESTING
original_estimate: 1
remaining_work: 1
time_spent: null
```

---

## Content

### Description

After starting a fresh session, verify the context token count at session start using Claude Code's `/context` command or similar mechanism.

### Dependencies

- TASK-001: Start fresh Claude Code session for baseline

### Test Procedure

1. In fresh session, use `/context` command
2. Record token count displayed
3. Calculate reduction percentage from baseline (~10,000)
4. Document results

### Target Metrics

| Metric | Before | Target | Actual | Pass |
|--------|--------|--------|--------|------|
| Session tokens | ~10,000 | < 5,000 | - | [ ] |
| Context utilization | ~50%+ | < 25% | - | [ ] |
| Reduction % | - | 50%+ | - | [ ] |

### Acceptance Criteria

- [ ] Token count < 5,000
- [ ] Reduction from ~10,000 documented
- [ ] Context utilization < 50%
- [ ] Results recorded in this file

### Contingency

If token count > 5,000:
1. Identify what is contributing to excess
2. Check if additional content can be moved to skills
3. Document findings for remediation

### Related Items

- Parent: [EN-204: Validation & Testing](./EN-204-validation-testing.md)
- Dependencies: TASK-001

---

## Results

### Measurement

| Timestamp | Token Count | Utilization | Notes |
|-----------|-------------|-------------|-------|
| - | - | - | - |

---

## Time Tracking

| Metric | Value |
|---------|-------|
| Original Estimate | 1 hour |
| Remaining Work | 1 hour |
| Time Spent | 0 hours |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
