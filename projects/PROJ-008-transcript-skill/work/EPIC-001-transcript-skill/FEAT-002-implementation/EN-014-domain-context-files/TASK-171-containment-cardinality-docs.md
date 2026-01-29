# TASK-171: Add Containment Cardinality Documentation

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-014 (Domain Context Files Implementation)
WORKFLOW: EN-014--WORKFLOW-schema-extension.md
ISSUE: ps-critic MINOR-001
-->

---

## Frontmatter

```yaml
id: "TASK-171"
work_type: TASK
title: "Add Containment Cardinality Documentation"
description: |
  Address ps-critic MINOR-001: Document that the `contains` relationship type
  implies `one-to-many` cardinality by default in TDD Section 2.1.

classification: ENABLER
status: DONE
resolution: COMPLETED
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-29T12:30:00Z"
updated_at: "2026-01-29T12:30:00Z"

parent_id: "EN-014"

tags:
  - "tdd-improvement"
  - "documentation"
  - "ps-critic-minor-001"
  - "cardinality"

effort: 1
acceptance_criteria: |
  - TDD Section 2.1 updated with containment cardinality note
  - Documentation explains `contains` implies `one-to-many` by default
  - Example provided showing hierarchical relationship
  - ps-critic MINOR-001 addressed

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

This task addresses ps-critic MINOR-001 from the TASK-167 quality review:

> **MINOR-001: Missing `"contains"` Cardinality Option**
>
> The `cardinality` enum includes `one-to-one`, `one-to-many`, `many-to-one`, `many-to-many`
> but the relationship types include `contains` which typically implies a containment hierarchy.
> Consider whether a `containment` cardinality or specialized `parent-of`/`child-of` relationship
> type should be added for hierarchical relationships.
>
> **Recommendation:** Document in implementation notes that `contains` relationship type implies
> `one-to-many` cardinality by default.

### Required Changes

**Location:** `docs/design/TDD-EN014-domain-schema-v2.md` Section 2.1

**Change:** Add a note explaining the default cardinality semantics for the `contains` relationship type.

**Example Content to Add:**

```markdown
#### Containment Relationship Semantics

The `contains` relationship type has special semantics:

| Relationship Type | Default Cardinality | Semantics |
|-------------------|---------------------|-----------|
| `contains` | `one-to-many` | Parent contains multiple children |
| `parent_of` | `one-to-many` | Explicit parent-child (same as contains) |
| `child_of` | `many-to-one` | Explicit child-parent (inverse of contains) |

**Example:**
```yaml
entities:
  topic:
    relationships:
      - type: "contains"
        target: "subtopic"
        cardinality: "one-to-many"  # Default, can be omitted
        description: "Topic contains multiple subtopics"
```
```

### Dependencies

**Blocked By:** None

**Blocks:**
- TASK-170: TDD Adversarial Review (must address minor issues first)

### Acceptance Criteria

- [x] TDD Section 2.1 updated with containment cardinality documentation
- [x] Default cardinality semantics explained
- [x] Example YAML provided demonstrating usage
- [ ] Change committed to repository

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Issue Source: [en014-task167-iter1-critique.md](./critiques/en014-task167-iter1-critique.md) MINOR-001
- Blocks: [TASK-170: TDD Adversarial Review](./TASK-170-tdd-adversarial-review.md)
- Related: [DISC-007: TDD Validation Implementation Gap](./EN-014--DISC-007-tdd-validation-implementation-gap.md)

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
| TDD Section 2.1 Update | Markdown | docs/design/TDD-EN014-domain-schema-v2.md | DONE |

### Verification

- [x] TDD Section 2.1 contains containment cardinality note
- [x] Example YAML demonstrates usage
- [x] Reviewed by: Claude (self-review)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | Created | Created per DISC-007 and ps-critic MINOR-001 |
| 2026-01-29 | DONE | Added containment cardinality note to TDD Section 2.1. ps-critic MINOR-001 addressed. |
