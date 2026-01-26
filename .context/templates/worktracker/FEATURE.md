# {{FEATURE_ID}}: {{FEATURE_TITLE}}

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-01-23 (ps-architect-002)
PURPOSE: Significant deliverable containing Stories and Enablers

DESCRIPTION:
  Feature represents a significant deliverable that provides user value.
  Contains Stories and Enablers. Belongs to an Epic or Capability.

EXTENDS: StrategicItem -> WorkItem
-->

> **Type:** feature
> **Status:** {{STATUS}}
> **Priority:** {{PRIORITY}}
> **Impact:** {{IMPACT}}
> **Created:** {{CREATED_AT}}
> **Due:** {{TARGET_DATE}}
> **Completed:** {{COMPLETED_AT}}
> **Parent:** {{EPIC_ID}}
> **Owner:** {{ASSIGNEE}}
> **Target Sprint:** {{TARGET_SPRINT}}

<!--
STATUS VALUES: pending | in_progress | completed
PRIORITY VALUES: critical | high | medium | low
IMPACT VALUES: critical | high | medium | low
TIMESTAMPS: Use ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
-->

---

## Template Structure

```
+---------------------------------------------------------------------+
|                         FEATURE TEMPLATE                             |
|                    Version 1.0.0 (ONTOLOGY-aligned)                  |
+---------------------------------------------------------------------+
| Header Block (blockquote)                                            |
|   |-- type: "feature"                          [REQUIRED]            |
|   |-- status: pending|in_progress|completed    [REQUIRED]            |
|   |-- priority: critical|high|medium|low       [REQUIRED]            |
|   |-- impact: critical|high|medium|low         [REQUIRED]            |
|   |-- created: ISO-8601                        [REQUIRED]            |
|   |-- due: ISO-8601                            [OPTIONAL]            |
|   |-- completed: ISO-8601                      [OPTIONAL]            |
|   |-- parent: {EPIC_ID}                        [REQUIRED]            |
|   |-- owner: {USER}                            [OPTIONAL]            |
|   +-- target_sprint: string                    [OPTIONAL]            |
+---------------------------------------------------------------------+
| Summary Section                                 [REQUIRED]           |
| Benefit Hypothesis                              [RECOMMENDED]        |
| Acceptance Criteria                             [REQUIRED]           |
| MVP Definition                                  [OPTIONAL]           |
| Children (Stories/Enablers)                     [REQUIRED]           |
| Progress Summary                                [REQUIRED]           |
| Containment Rules                               [REFERENCE]          |
| History                                         [RECOMMENDED]        |
+---------------------------------------------------------------------+

CONTAINMENT:
  allowed_parents: [Epic, Capability]
  allowed_children: [Story, Enabler]
  max_depth: 1
```

---

## Frontmatter

```yaml
# =============================================================================
# FEATURE WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.4 (Feature Entity Schema)
# =============================================================================

# Identity (inherited from WorkItem - Section 2.1)
id: "{{FEATURE_ID}}"                       # Required, immutable - Format: FEAT-NNN
work_type: FEATURE                         # Required, immutable - Discriminator
title: "{{FEATURE_TITLE}}"                 # Required - Max 500 chars

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
completed_at: null                         # Optional - When feature completed (ISO 8601)

# Hierarchy
parent_id: "{{EPIC_ID}}"                   # Required - Epic or Capability ID

# Tags
tags: []                                   # Optional - String array

# =============================================================================
# FEATURE-SPECIFIC PROPERTIES (Section 3.4.4)
# =============================================================================

# Strategic (from StrategicItem)
target_date: null                          # Optional - Target completion date (ISO 8601)
business_outcome: null                     # Optional - Expected outcomes

# Feature-Specific
target_sprint: null                        # Optional - Target sprint/iteration (max 50 chars)
value_area: BUSINESS                       # Optional - BUSINESS | ARCHITECTURAL (default: BUSINESS)
benefit_hypothesis: null                   # Optional - Expected benefits (max 5000 chars)
acceptance_criteria: null                  # Required before completed - Verification criteria (max 10000 chars)
mvp_definition: null                       # Optional - Minimum viable product scope (max 5000 chars)
```

---

## Summary

<!--
REQUIRED: Brief 1-3 sentence description of the Feature.
Should communicate the user value being delivered.
-->

{{FEATURE_SUMMARY}}

**Value Proposition:**
- {{VALUE_1}}
- {{VALUE_2}}

---

## Benefit Hypothesis

<!--
RECOMMENDED: Expected benefits from this feature
Source: ONTOLOGY-v1.md Section 3.4.4 - benefit_hypothesis (max 5000 chars)
Maps to: ADO:Value, SAFe:benefit_hypothesis
-->

**We believe that** {{HYPOTHESIS_STATEMENT}}

**Will result in** {{EXPECTED_BENEFIT}}

**We will know we have succeeded when** {{SUCCESS_METRICS}}

---

## Acceptance Criteria

<!--
REQUIRED before completed status (INV-FE02)
Source: ONTOLOGY-v1.md Section 3.4.4 - acceptance_criteria (max 10000 chars)
Maps to: ADO:AcceptanceCriteria, SAFe:acceptance_criteria
-->

### Definition of Done

- [ ] {{CRITERION_1}}
- [ ] {{CRITERION_2}}
- [ ] {{CRITERION_3}}
- [ ] All Stories completed
- [ ] All acceptance criteria verified

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | {{ACCEPTANCE_CRITERION_1}} | [ ] |
| AC-2 | {{ACCEPTANCE_CRITERION_2}} | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | {{NON_FUNCTIONAL_CRITERION_1}} | [ ] |
| NFC-2 | {{NON_FUNCTIONAL_CRITERION_2}} | [ ] |

---

## MVP Definition

<!--
OPTIONAL: Minimum Viable Product scope
Source: ONTOLOGY-v1.md Section 3.4.4 - mvp_definition (max 5000 chars)
Maps to: SAFe:mvp_definition
-->

### In Scope (MVP)

- {{MVP_ITEM_1}}
- {{MVP_ITEM_2}}

### Out of Scope (Future)

- {{FUTURE_ITEM_1}}
- {{FUTURE_ITEM_2}}

---

## Children (Stories/Enablers)

<!--
REQUIRED: Track all child work items.
Source: ONTOLOGY-v1.md Section 3.4.4 - containment
allowed_children: [Story, Enabler]
max_depth: 1
-->

### Story/Enabler Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| {{CHILD_ID_1}} | Story | {{CHILD_TITLE_1}} | {{CHILD_STATUS_1}} | {{CHILD_PRIORITY_1}} | {{EFFORT_1}} |
| {{CHILD_ID_2}} | Enabler | {{CHILD_TITLE_2}} | {{CHILD_STATUS_2}} | {{CHILD_PRIORITY_2}} | {{EFFORT_2}} |

### Work Item Links

- [{{CHILD_ID_1}}: {{CHILD_TITLE_1}}](./{{CHILD_ID_1}}/{{CHILD_ID_1}}.md)
- [{{CHILD_ID_2}}: {{CHILD_TITLE_2}}](./{{CHILD_ID_2}}/{{CHILD_ID_2}}.md)

---

## Progress Summary

<!--
REQUIRED: Track overall feature progress.
Update regularly as children progress.
-->

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Stories:   [##########..........] 50% (3/6 completed)            |
| Enablers:  [####################] 100% (2/2 completed)           |
| Tasks:     [########............] 40% (12/30 completed)          |
+------------------------------------------------------------------+
| Overall:   [##########..........] 55%                            |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Stories** | {{TOTAL_STORIES}} |
| **Completed Stories** | {{COMPLETED_STORIES}} |
| **Total Enablers** | {{TOTAL_ENABLERS}} |
| **Completed Enablers** | {{COMPLETED_ENABLERS}} |
| **Total Effort (points)** | {{TOTAL_EFFORT}} |
| **Completed Effort** | {{COMPLETED_EFFORT}} |
| **Completion %** | {{COMPLETION_PCT}}% |

### Sprint Tracking

| Sprint | Stories | Status | Notes |
|--------|---------|--------|-------|
| {{SPRINT_1}} | {{STORIES_1}} | {{STATUS_1}} | {{NOTES_1}} |
| {{SPRINT_2}} | {{STORIES_2}} | {{STATUS_2}} | {{NOTES_2}} |

---

## State Machine Reference

<!--
Source: ONTOLOGY-v1.md Section 3.4.4 - state_machine
Simplified to match worktracker conventions.
-->

```
+-------------------------------------------------------------------+
|                   FEATURE STATE MACHINE                            |
+-------------------------------------------------------------------+
|                                                                    |
|   +---------+     +-------------+     +-----------+               |
|   | PENDING |---->| IN_PROGRESS |---->| COMPLETED |               |
|   +---------+     +-------------+     +-----------+               |
|        |               |                   |                       |
|        v               v                   v                       |
|   (Refinement)   (Development)       (Delivered)                  |
|                                                                    |
+-------------------------------------------------------------------+

Allowed Transitions:
- pending -> in_progress: Start development
- in_progress -> completed: All stories delivered
- in_progress -> pending: Deprioritized
- completed -> in_progress: Reopened
```

---

## Containment Rules

<!--
Source: ONTOLOGY-v1.md Section 3.4.4 - containment
-->

| Rule | Value |
|------|-------|
| **Allowed Children** | Story, Enabler |
| **Allowed Parents** | Epic, Capability |
| **Max Depth** | 1 |

### Hierarchy Diagram

```
EPIC-001: {{EPIC_TITLE}}
|
+-- FEAT-001: {{FEATURE_TITLE}} (this feature)
    |
    +-- EN-001: Enabler
    +-- ST-001: Story
    |   +-- TASK-001: Task
    |   +-- TASK-002: Task
    +-- ST-002: Story
```

---

## Invariants

<!--
Source: ONTOLOGY-v1.md Section 3.4.4 - invariants
-->

- **INV-FE01:** Feature can contain Stories or Enablers
- **INV-FE02:** acceptance_criteria should be defined before completed
- Title cannot be empty (inherited)
- Status must be valid for Feature state machine (inherited)
- Parent must be valid parent type if set (inherited)
- Circular hierarchy not allowed (inherited)

---

## Related Items

<!--
RECOMMENDED: Link to related work items and artifacts.
-->

### Hierarchy

- **Parent Epic:** [{{EPIC_ID}}: {{EPIC_TITLE}}](../{{EPIC_ID}}/{{EPIC_ID}}.md)

### Related Features

- [{{RELATED_FEATURE_ID}}]({{RELATED_FEATURE_LINK}}) - {{RELATIONSHIP_DESCRIPTION}}

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
| {{CREATED_AT}} | {{CREATED_BY}} | pending | Feature created |
| {{DATE_2}} | {{AUTHOR_2}} | in_progress | Development started |
| {{DATE_3}} | {{AUTHOR_3}} | completed | All stories delivered |

---

## System Mapping

<!--
Source: ONTOLOGY-v1.md Section 3.4.4 - system_mapping
-->

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Feature |
| **SAFe** | Feature (Program Backlog) |
| **JIRA** | Epic (or custom issue type) |

---

<!--
DESIGN RATIONALE:
Feature retained as distinct level despite JIRA lacking it natively.
JIRA users map Epic-to-Feature or create custom issue type.
Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2, Section 2.3

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
