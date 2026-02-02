# {{STORY_ID}}: {{STORY_TITLE}}

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
CREATED: 2026-01-23 (ps-architect-002)
PURPOSE: User story representing a vertical slice of functionality

DESCRIPTION:
  Story represents a vertical slice of user functionality.
  Typically completed within a single sprint. Contains Tasks.

EXTENDS: DeliveryItem -> WorkItem

NOTE: "Story" chosen over "PBI" because: (1) more intuitive for users,
      (2) used by 2/3 systems natively, (3) aligns with Scrum terminology.
      Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2 (Canonical Name Rationale)
-->

> **Type:** story
> **Status:** {{STATUS}}
> **Priority:** {{PRIORITY}}
> **Impact:** {{IMPACT}}
> **Created:** {{CREATED_AT}}
> **Due:** {{DUE_DATE}}
> **Completed:** {{COMPLETED_AT}}
> **Parent:** {{FEATURE_ID}}
> **Owner:** {{ASSIGNEE}}
> **Effort:** {{EFFORT}}

<!--
STATUS VALUES: pending | in_progress | completed
PRIORITY VALUES: critical | high | medium | low
IMPACT VALUES: critical | high | medium | low
TIMESTAMPS: Use ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
EFFORT: Story points (1-13 Fibonacci recommended)
-->

---

## Template Structure

```
+---------------------------------------------------------------------+
|                          STORY TEMPLATE                              |
|                    Version 1.0.0 (ONTOLOGY-aligned)                  |
+---------------------------------------------------------------------+
| Header Block (blockquote)                                            |
|   |-- type: "story"                            [REQUIRED]            |
|   |-- status: pending|in_progress|completed    [REQUIRED]            |
|   |-- priority: critical|high|medium|low       [REQUIRED]            |
|   |-- impact: critical|high|medium|low         [REQUIRED]            |
|   |-- created: ISO-8601                        [REQUIRED]            |
|   |-- due: ISO-8601                            [OPTIONAL]            |
|   |-- completed: ISO-8601                      [OPTIONAL]            |
|   |-- parent: {FEATURE_ID}                     [REQUIRED]            |
|   |-- owner: {USER}                            [OPTIONAL]            |
|   +-- effort: points                           [OPTIONAL]            |
+---------------------------------------------------------------------+
| User Story (As a... I want... So that...)      [RECOMMENDED]         |
| Summary Section                                 [REQUIRED]           |
| Acceptance Criteria                             [REQUIRED]           |
| Children (Tasks)                                [OPTIONAL]           |
| Progress Summary                                [REQUIRED]           |
| Definition of Done                              [REQUIRED]           |
| Containment Rules                               [REFERENCE]          |
| History                                         [RECOMMENDED]        |
+---------------------------------------------------------------------+

CONTAINMENT:
  allowed_parents: [Feature]
  allowed_children: [Task, Subtask]
  max_depth: 2
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | YAML metadata schema for stories |
| [User Story](#user-story) | As a/I want/So that format |
| [Summary](#summary) | Additional context and scope |
| [Acceptance Criteria](#acceptance-criteria) | Gherkin format and checklist |
| [Children (Tasks)](#children-tasks) | Task inventory and tracking |
| [Progress Summary](#progress-summary) | Overall story progress |
| [Estimation](#estimation) | Story points and sprint |
| [Definition of Done](#definition-of-done) | Code quality, documentation, verification |
| [Evidence](#evidence) | Deliverables and verification record |
| [State Machine Reference](#state-machine-reference) | Story status transitions |
| [Containment Rules](#containment-rules) | Parent/child constraints |
| [Invariants](#invariants) | Business rules and constraints |
| [Related Items](#related-items) | Hierarchy and related stories |
| [History](#history) | Status changes and key events |
| [System Mapping](#system-mapping) | ADO, SAFe, JIRA mappings |

---

## Frontmatter

```yaml
# =============================================================================
# STORY WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.5 (Story Entity Schema)
# =============================================================================

# Identity (inherited from WorkItem - Section 2.1)
id: "{{STORY_ID}}"                         # Required, immutable - Format: ST-NNN
work_type: STORY                           # Required, immutable - Discriminator
title: "{{STORY_TITLE}}"                   # Required - Max 500 chars

# Classification
classification: BUSINESS                   # Optional - BUSINESS | ENABLER (default: BUSINESS)

# State (see State Machine below)
status: pending                            # Required - pending | in_progress | completed
resolution: null                           # Optional - Resolution enum (when completed)

# Priority & Impact
priority: medium                           # Optional - critical | high | medium | low
impact: medium                             # Optional - critical | high | medium | low

# People
assignee: null                             # Optional - User reference
created_by: "{{CREATED_BY}}"               # Required, auto-populated

# Timestamps (auto-managed)
created_at: "{{CREATED_AT}}"               # Required, auto, immutable (ISO 8601)
updated_at: "{{UPDATED_AT}}"               # Required, auto (ISO 8601)
completed_at: null                         # Optional - When story completed (ISO 8601)

# Hierarchy
parent_id: "{{FEATURE_ID}}"                # Required - Feature ID (INV-ST01)

# Tags
tags: []                                   # Optional - String array

# =============================================================================
# STORY-SPECIFIC PROPERTIES (Section 3.4.5)
# =============================================================================

# From DeliveryItem
effort: null                               # Optional - Story points (1-13 Fibonacci recommended)
due_date: null                             # Optional - Sprint/iteration deadline (ISO 8601)
acceptance_criteria: null                  # Required before completed (INV-ST03)

# Story-Specific
value_area: BUSINESS                       # Optional - BUSINESS | ARCHITECTURAL (default: BUSINESS)

# User Story Format (optional structured format)
user_role: null                            # "As a <user_role>..." (max 100 chars)
user_goal: null                            # "I want <goal>..." (max 500 chars)
user_benefit: null                         # "So that <benefit>..." (max 500 chars)
```

---

## User Story

<!--
RECOMMENDED: Structured user story format
Source: ONTOLOGY-v1.md Section 3.4.5 - user_role, user_goal, user_benefit
-->

**As a** {{USER_ROLE}}

**I want** {{USER_GOAL}}

**So that** {{USER_BENEFIT}}

---

## Summary

<!--
REQUIRED: Additional context and details beyond the user story.
-->

{{STORY_SUMMARY}}

**Scope:**
- {{SCOPE_ITEM_1}}
- {{SCOPE_ITEM_2}}

---

## Acceptance Criteria

<!--
REQUIRED before completed status (INV-ST03)
Source: ONTOLOGY-v1.md Section 3.4.5 - acceptance_criteria (from DeliveryItem)
Maps to: ADO:AcceptanceCriteria, SAFe:acceptance_criteria
-->

### Given-When-Then (Gherkin)

```gherkin
Feature: {{FEATURE_TITLE}}

  Scenario: {{SCENARIO_NAME}}
    Given {{PRECONDITION}}
    When {{ACTION}}
    Then {{EXPECTED_RESULT}}
```

### Acceptance Checklist

- [ ] {{CRITERION_1}}
- [ ] {{CRITERION_2}}
- [ ] {{CRITERION_3}}

---

## Children (Tasks)

<!--
OPTIONAL: Track child tasks.
Source: ONTOLOGY-v1.md Section 3.4.5 - containment
allowed_children: [Task, Subtask]
max_depth: 2
-->

### Task Inventory

| ID | Title | Status | Remaining | Owner |
|----|-------|--------|-----------|-------|
| {{TASK_ID_1}} | {{TASK_TITLE_1}} | {{TASK_STATUS_1}} | {{REMAINING_1}} hrs | {{OWNER_1}} |
| {{TASK_ID_2}} | {{TASK_TITLE_2}} | {{TASK_STATUS_2}} | {{REMAINING_2}} hrs | {{OWNER_2}} |

### Task Links

- [{{TASK_ID_1}}: {{TASK_TITLE_1}}](./{{TASK_ID_1}}.md)
- [{{TASK_ID_2}}: {{TASK_TITLE_2}}](./{{TASK_ID_2}}.md)

---

## Progress Summary

<!--
REQUIRED: Track overall story progress.
Update regularly as tasks progress.
-->

### Status Overview

```
+------------------------------------------------------------------+
|                    STORY PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Tasks:     [##########..........] 50% (3/6 completed)            |
| Hours:     [########............] 40% (8/20 hrs remaining)       |
+------------------------------------------------------------------+
| Overall:   [#########...........] 45%                            |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | {{TOTAL_TASKS}} |
| **Completed Tasks** | {{COMPLETED_TASKS}} |
| **Original Estimate** | {{ORIGINAL_ESTIMATE}} hrs |
| **Remaining Work** | {{REMAINING_WORK}} hrs |
| **Time Spent** | {{TIME_SPENT}} hrs |
| **Completion %** | {{COMPLETION_PCT}}% |

---

## Estimation

<!--
Source: ONTOLOGY-v1.md Section 3.4.5 - effort
Maps to: ADO:Effort, SAFe:story_points, JIRA:story_points
-->

| Attribute | Value |
|-----------|-------|
| **Story Points** | {{EFFORT}} |
| **T-Shirt Size** | {{TSHIRT_SIZE}} |
| **Sprint** | {{TARGET_SPRINT}} |

> **Note (INV-ST02):** Story effort is typically 1-13 (Fibonacci scale: 1, 2, 3, 5, 8, 13)

---

## Definition of Done

<!--
REQUIRED: Standard checklist for story completion.
-->

### Code Quality

- [ ] Code complete and peer reviewed
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Code coverage meets threshold

### Documentation

- [ ] Documentation updated
- [ ] API documentation current
- [ ] User-facing help updated (if applicable)

### Verification

- [ ] Acceptance criteria verified
- [ ] QA testing complete
- [ ] No critical bugs remaining

---

## Evidence

<!--
COMPLETION EVIDENCE: Verification that this story's acceptance criteria were met.
This is audit trail evidence (proving work was done), not knowledge evidence (research citations).
-->

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| {{DELIVERABLE_1}} | Code | {{DESC_1}} | [{{LINK_TEXT_1}}]({{URL_1}}) |
| {{DELIVERABLE_2}} | Test | {{DESC_2}} | [{{LINK_TEXT_2}}]({{URL_2}}) |
| {{DELIVERABLE_3}} | Documentation | {{DESC_3}} | [{{LINK_TEXT_3}}]({{URL_3}}) |

### Verification Record

| Criterion | Verification Method | Verified By | Date |
|-----------|---------------------|-------------|------|
| {{AC_1}} | {{METHOD_1}} | {{VERIFIER_1}} | {{DATE_1}} |
| {{AC_2}} | {{METHOD_2}} | {{VERIFIER_2}} | {{DATE_2}} |

### Verification Checklist

- [ ] All acceptance criteria verified (see table above)
- [ ] All tasks completed
- [ ] Code review approved
- [ ] Tests passing
- [ ] Documentation updated

---

## State Machine Reference

<!--
Source: ONTOLOGY-v1.md Section 3.4.5 - state_machine
Simplified to match worktracker conventions.
-->

```
+-------------------------------------------------------------------+
|                    STORY STATE MACHINE                             |
+-------------------------------------------------------------------+
|                                                                    |
|   +---------+     +-------------+     +-----------+               |
|   | PENDING |---->| IN_PROGRESS |---->| COMPLETED |               |
|   +---------+     +-------------+     +-----------+               |
|        |               |                   |                       |
|        v               v                   v                       |
|   (Backlog)       (Sprint)           (Done)                       |
|                                                                    |
+-------------------------------------------------------------------+

Allowed Transitions:
- pending -> in_progress: Sprint commitment
- in_progress -> completed: All acceptance criteria met
- in_progress -> pending: Removed from sprint
- completed -> in_progress: Reopened
```

---

## Containment Rules

<!--
Source: ONTOLOGY-v1.md Section 3.4.5 - containment
-->

| Rule | Value |
|------|-------|
| **Allowed Children** | Task, Subtask |
| **Allowed Parents** | Feature |
| **Max Depth** | 2 |

### Hierarchy Diagram

```
FEAT-001: {{FEATURE_TITLE}}
|
+-- ST-001: {{STORY_TITLE}} (this story)
    |
    +-- TASK-001: Task
    |   +-- SUBTASK-001: Subtask
    +-- TASK-002: Task
```

---

## Invariants

<!--
Source: ONTOLOGY-v1.md Section 3.4.5 - invariants
-->

- **INV-ST01:** Story must have Feature as parent
- **INV-ST02:** Story effort is typically 1-13 (Fibonacci)
- **INV-ST03:** acceptance_criteria must be defined before completed
- Title cannot be empty (inherited)
- Status must be valid for Story state machine (inherited)
- Parent must be valid parent type if set (inherited)
- Circular hierarchy not allowed (inherited)

---

## Related Items

<!--
RECOMMENDED: Link to related work items and artifacts.
-->

### Hierarchy

- **Parent Feature:** [{{FEATURE_ID}}: {{FEATURE_TITLE}}](../{{FEATURE_ID}}/{{FEATURE_ID}}.md)

### Related Stories

- [{{RELATED_STORY_ID}}]({{RELATED_STORY_LINK}}) - {{RELATIONSHIP_DESCRIPTION}}

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | {{DEPENDENCY_ID}} | {{DEPENDENCY_DESC}} |
| Blocks | {{BLOCKS_ID}} | {{BLOCKS_DESC}} |

---

## History

<!--
RECOMMENDED: Track status changes and key events.
Use ISO 8601 timestamps.
-->

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| {{CREATED_AT}} | {{CREATED_BY}} | pending | Story created |
| {{DATE_2}} | {{AUTHOR_2}} | in_progress | Sprint commitment |
| {{DATE_3}} | {{AUTHOR_3}} | completed | Acceptance verified |

---

## System Mapping

<!--
Source: ONTOLOGY-v1.md Section 3.4.5 - system_mapping
-->

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (PBI) |
| **SAFe** | Story |
| **JIRA** | Story |

---

<!--
DESIGN RATIONALE:
"Story" chosen over "PBI" because: (1) more intuitive for users,
(2) used by 2/3 systems natively, (3) aligns with Scrum terminology.
Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2 (Canonical Name Rationale)

PATTERN COMPLIANCE:
- P-001: Blockquote Header [COMPLIANT]
- P-002: Summary Section [COMPLIANT]
- P-005: History/Changelog [COMPLIANT]
- P-006: ISO 8601 Timestamps [COMPLIANT]
- P-007: Horizontal Rule Separators [COMPLIANT]
- P-019: Parent Reference [COMPLIANT]
- Children Tracking Section [COMPLIANT]
- Progress Summary Section [COMPLIANT]

WORKTRACKER ALIGNMENT:
- Status values: pending, in_progress, completed (per work-items.md)
- Priority/Impact: critical, high, medium, low (per work-items.md)
-->
