# TASK-172: Fix Section Numbering Inconsistency

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-014 (Domain Context Files Implementation)
WORKFLOW: EN-014--WORKFLOW-schema-extension.md
ISSUE: ps-critic MINOR-002
-->

---

## Frontmatter

```yaml
id: "TASK-172"
work_type: TASK
title: "Fix Section Numbering Inconsistency"
description: |
  Address ps-critic MINOR-002: Fix inconsistent section numbering where L0/L1/L2
  sections are numbered 1.4, 1.5, 1.6 but could be better structured.

classification: ENABLER
status: DONE
resolution: COMPLETED
priority: MEDIUM
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-29T12:30:00Z"
updated_at: "2026-01-29T12:30:00Z"

parent_id: "EN-014"

tags:
  - "tdd-improvement"
  - "documentation"
  - "ps-critic-minor-002"
  - "editorial"

effort: 1
acceptance_criteria: |
  - TDD section numbering reviewed for consistency
  - L0/L1/L2 sections properly positioned and numbered
  - Document structure is clear and navigable
  - ps-critic MINOR-002 addressed

due_date: null

activity: DOCUMENTATION
original_estimate: 1
remaining_work: 0
time_spent: 1
```

---

## State Machine

**Current State:** `DONE`

```
BACKLOG → IN_PROGRESS → DONE
              ↓
           BLOCKED
```

---

## Content

### Description

This task addresses ps-critic MINOR-002 from the TASK-167 quality review:

> **MINOR-002: Inconsistent Section Numbering**
>
> L0 Executive Summary is numbered as Section 1.4, L1 as 1.5, L2 as 1.6. However,
> Section 2 jumps directly to Schema Specification. Consider restructuring to have
> L0/L1/L2 as Section 1 subsections (1.1, 1.2, 1.3) with Overview as 1.0 or separate
> the lens documentation into its own top-level section.
>
> **Recommendation:** No action required for this iteration; address in future
> document template updates.

### Analysis

**Current Structure:**
```
1. Overview
   1.1 Purpose
   1.2 Design Principles
   1.3 Traceability Matrix
   1.4 L0: Executive Summary (ELI5)
   1.5 L1: Technical Analysis (Engineer)
   1.6 L2: Strategic Implications (Architect)
2. Schema Specification
   ...
```

**Options:**
1. **Keep Current** - Structure is functional, ps-critic noted "no action required"
2. **Restructure** - Move L0/L1/L2 to their own top-level section

### Recommended Action

Given ps-critic's recommendation that "no action required for this iteration", this task should:
1. Document the current structure rationale
2. Add a note in TDD metadata about future restructuring consideration
3. Mark as addressed with minimal changes

### Dependencies

**Blocked By:** None

**Blocks:**
- TASK-170: TDD Adversarial Review (must address minor issues first)

### Acceptance Criteria

- [ ] Section structure reviewed and documented
- [ ] Rationale for current structure noted in TDD
- [ ] Future improvement noted in TDD metadata if applicable
- [ ] ps-critic MINOR-002 addressed (documented as accepted)

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Issue Source: [en014-task167-iter1-critique.md](./critiques/en014-task167-iter1-critique.md) MINOR-002
- Blocks: [TASK-170: TDD Adversarial Review](./TASK-170-tdd-adversarial-review.md)

---

## Time Tracking

| Metric            | Value    |
|-------------------|----------|
| Original Estimate | 1 hour   |
| Remaining Work    | 1 hour   |
| Time Spent        | 0 hours  |

---

## Evidence

### Deliverables

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| TDD Structure Review | Documentation | docs/design/TDD-EN014-domain-schema-v2.md | DONE |

### Verification

- [ ] Section structure reviewed
- [ ] Decision documented (keep or restructure)
- [ ] Reviewed by: (self-review)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | Created | Created per ps-critic MINOR-002. Note: ps-critic recommended "no action required for this iteration" |
| 2026-01-29 | DONE | Added section numbering rationale note before Section 1.4. ps-critic MINOR-002 addressed by documenting structure rationale. |
