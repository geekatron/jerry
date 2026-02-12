# TASK-004: Add Context Optimization Rationale

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | Task metadata |
| [Content](#content) | Description, target structure, acceptance criteria |
| [Time Tracking](#time-tracking) | Effort metrics |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-004"
work_type: TASK
title: "Add Context Optimization Rationale"
description: |
  Add documentation explaining the rationale for the CLAUDE.md
  optimization to docs/design/.

classification: ENABLER
status: BACKLOG
resolution: null
priority: LOW
assignee: null
created_by: "Claude"
created_at: "2026-02-01T00:00:00Z"
updated_at: "2026-02-01T00:00:00Z"
parent_id: "EN-205"
tags:
  - enabler
  - documentation
  - design

effort: 0.5
acceptance_criteria: |
  - Rationale document created
  - Context rot research cited
  - Before/after metrics documented
  - Clear for future maintainers
due_date: null

activity: DOCUMENTATION
original_estimate: 0.5
remaining_work: 0.5
time_spent: null
```

---

## Content

### Description

Create a design document explaining the rationale behind the CLAUDE.md optimization, including research references and metrics.

### Target Structure

```markdown
# Context Optimization Rationale

## Problem

Context rot degrades LLM performance as context window fills...

## Research

Based on Chroma Research (https://research.trychroma.com/context-rot):
- 75% utilization is optimal
- Performance degrades at 90%+
- Selective context > maximum context

## Solution

Tiered Hybrid Loading Strategy:
- Tier 1: Essential identity (always)
- Tier 2: Standards (auto)
- Tier 3: Skills (on-demand)
- Tier 4: Reference (explicit)

## Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Lines | 914 | 75 | 92% |
| Tokens | ~10,000 | ~3,500 | 65% |
| Session utilization | ~50% | ~17% | 66% |

## References

- Chroma Context Rot Research
- ADR-OSS-001
- PLAN-CLAUDE-MD-OPTIMIZATION.md
```

### Acceptance Criteria

- [ ] Document created at docs/design/
- [ ] Context rot research cited
- [ ] Before/after metrics included
- [ ] Clear for future maintainers

### Related Items

- Parent: [EN-205: Documentation Update](./EN-205-documentation-update.md)
- Target: docs/design/CONTEXT-OPTIMIZATION-RATIONALE.md

---

## Time Tracking

| Metric | Value |
|---------|-------|
| Original Estimate | 0.5 hours |
| Remaining Work | 0.5 hours |
| Time Spent | 0 hours |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-01 | Created | Initial creation |
