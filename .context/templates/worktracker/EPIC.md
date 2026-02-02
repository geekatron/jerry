# {{EPIC_ID}}: {{EPIC_TITLE}}

<!--
TEMPLATE: Epic
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.2
CREATED: 2026-01-23 (ps-architect-002)
PURPOSE: Large initiative containing Features or Capabilities

DESCRIPTION:
  Epic is a large initiative that contains Features or Capabilities.
  Universal across all systems. Top-level container in most hierarchies.

EXTENDS: StrategicItem -> WorkItem
-->

> **Type:** epic
> **Status:** {{STATUS}}
> **Priority:** {{PRIORITY}}
> **Impact:** {{IMPACT}}
> **Created:** {{CREATED_AT}}
> **Due:** {{TARGET_DATE}}
> **Completed:** {{COMPLETED_AT}}
> **Parent:** {{PARENT_ID}}
> **Owner:** {{ASSIGNEE}}
> **Target Quarter:** {{TARGET_QUARTER}}

<!--
STATUS VALUES: pending | in_progress | completed
PRIORITY VALUES: critical | high | medium | low
IMPACT VALUES: critical | high | medium | low
TIMESTAMPS: Use ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
TARGET_QUARTER: Format FY##-Q# (e.g., FY26-Q1)
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Template Structure](#template-structure) | Visual structure reference for epic |
| [Frontmatter](#frontmatter) | YAML metadata schema for epics |
| [Summary](#summary) | Brief description and key objectives |
| [Business Outcome Hypothesis](#business-outcome-hypothesis) | Expected business outcomes (SAFe pattern) |
| [Lean Business Case](#lean-business-case) | Economic justification (SAFe pattern) |
| [Children (Features/Capabilities)](#children-featurescapabilities) | Feature inventory and tracking |
| [Progress Summary](#progress-summary) | Overall epic progress |
| [State Machine Reference](#state-machine-reference) | Epic status transitions |
| [Containment Rules](#containment-rules) | Parent/child constraints |
| [Invariants](#invariants) | Business rules and constraints |
| [Related Items](#related-items) | Hierarchy and related epics |
| [History](#history) | Status changes and key events |
| [System Mapping](#system-mapping) | ADO, SAFe, JIRA mappings |

---

## Template Structure

```
+---------------------------------------------------------------------+
|                          EPIC TEMPLATE                               |
|                    Version 1.0.0 (ONTOLOGY-aligned)                  |
+---------------------------------------------------------------------+
| Header Block (blockquote)                                            |
|   |-- type: "epic"                             [REQUIRED]            |
|   |-- status: pending|in_progress|completed    [REQUIRED]            |
|   |-- priority: critical|high|medium|low       [REQUIRED]            |
|   |-- impact: critical|high|medium|low         [REQUIRED]            |
|   |-- created: ISO-8601                        [REQUIRED]            |
|   |-- due: ISO-8601                            [OPTIONAL]            |
|   |-- completed: ISO-8601                      [OPTIONAL]            |
|   |-- parent: {ID}                             [OPTIONAL - top-level]|
|   |-- owner: {USER}                            [OPTIONAL]            |
|   +-- target_quarter: FY##-Q#                  [OPTIONAL]            |
+---------------------------------------------------------------------+
| Summary Section                                 [REQUIRED]           |
| Business Outcome Hypothesis                     [RECOMMENDED]        |
| Lean Business Case                              [OPTIONAL]           |
| Children (Features/Capabilities)                [REQUIRED]           |
| Progress Summary                                [REQUIRED]           |
| Containment Rules                               [REFERENCE]          |
| History                                         [RECOMMENDED]        |
+---------------------------------------------------------------------+

CONTAINMENT:
  allowed_parents: [Initiative] or (top-level)
  allowed_children: [Capability, Feature]
  max_depth: 2 (via Features)
```

---

## Frontmatter

```yaml
# =============================================================================
# EPIC WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.2 (Epic Entity Schema)
# =============================================================================

# Identity (inherited from WorkItem - Section 2.1)
id: "{{EPIC_ID}}"                          # Required, immutable - Format: EPIC-NNN
work_type: EPIC                            # Required, immutable - Discriminator
title: "{{EPIC_TITLE}}"                    # Required - Max 500 chars

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
completed_at: null                         # Optional - When epic completed (ISO 8601)

# Hierarchy
parent_id: null                            # Optional - Initiative ID (or top-level)

# Tags
tags: []                                   # Optional - String array

# =============================================================================
# EPIC-SPECIFIC PROPERTIES (Section 3.4.2)
# =============================================================================

# Target Quarter
target_quarter: null                       # Optional - Pattern: ^FY[0-9]{2}-Q[1-4]$ (e.g., FY26-Q2)

# Strategic (from StrategicItem)
target_date: null                          # Optional - Target completion date (ISO 8601)
business_outcome: null                     # Optional - Expected outcomes (from StrategicItem)

# SAFe WSJF Properties (Optional - for SAFe teams)
wsjf_score: null                           # Calculated: cost_of_delay / job_size
cost_of_delay: null                        # Sum of: business_value + time_criticality + risk_reduction
job_size: null                             # Implementation size (1-13 Fibonacci, min: 1)

# Lean Business Case (Optional - for SAFe teams)
lean_business_case:
  problem: null
  solution: null
  cost: null
  benefit: null
  risk: null
```

---

## Summary

<!--
REQUIRED: Brief 1-3 sentence description of the Epic.
Should communicate the business value and scope.
-->

{{EPIC_SUMMARY}}

**Key Objectives:**
- {{OBJECTIVE_1}}
- {{OBJECTIVE_2}}
- {{OBJECTIVE_3}}

---

## Business Outcome Hypothesis

<!--
RECOMMENDED: Expected business outcomes (SAFe pattern)
Source: ONTOLOGY-v1.md Section 3.4.2 - business_outcome
-->

**We believe that** {{HYPOTHESIS_STATEMENT}}

**Will result in** {{EXPECTED_OUTCOME}}

**We will know we have succeeded when** {{SUCCESS_CRITERIA}}

---

## Lean Business Case

<!--
OPTIONAL: Economic justification (SAFe pattern)
Source: ONTOLOGY-v1.md Section 3.4.2 - lean_business_case
-->

| Aspect | Description |
|--------|-------------|
| **Problem** | {{PROBLEM_STATEMENT}} |
| **Solution** | {{SOLUTION_STATEMENT}} |
| **Cost** | {{ESTIMATED_COST}} |
| **Benefit** | {{ESTIMATED_BENEFIT}} |
| **Risk** | {{RISK_ASSESSMENT}} |

---

## Children (Features/Capabilities)

<!--
REQUIRED: Track all child work items.
Source: ONTOLOGY-v1.md Section 3.4.2 - containment
allowed_children: [Capability, Feature]
max_depth: 2
-->

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| {{FEAT_ID_1}} | {{FEAT_TITLE_1}} | {{FEAT_STATUS_1}} | {{FEAT_PRIORITY_1}} | {{FEAT_PROGRESS_1}} |
| {{FEAT_ID_2}} | {{FEAT_TITLE_2}} | {{FEAT_STATUS_2}} | {{FEAT_PRIORITY_2}} | {{FEAT_PROGRESS_2}} |

### Feature Links

- [{{FEAT_ID_1}}: {{FEAT_TITLE_1}}](./work/{{EPIC_ID}}/{{FEAT_ID_1}}/{{FEAT_ID_1}}.md)
- [{{FEAT_ID_2}}: {{FEAT_TITLE_2}}](./work/{{EPIC_ID}}/{{FEAT_ID_2}}/{{FEAT_ID_2}}.md)

---

## Progress Summary

<!--
REQUIRED: Track overall epic progress.
Update regularly as children progress.
-->

### Status Overview

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [##########..........] 50% (2/4 completed)            |
| Stories:   [########............] 40% (8/20 completed)           |
| Tasks:     [######..............] 30% (15/50 completed)          |
+------------------------------------------------------------------+
| Overall:   [########............] 40%                            |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Features** | {{TOTAL_FEATURES}} |
| **Completed Features** | {{COMPLETED_FEATURES}} |
| **In Progress Features** | {{IN_PROGRESS_FEATURES}} |
| **Pending Features** | {{PENDING_FEATURES}} |
| **Feature Completion %** | {{FEATURE_COMPLETION_PCT}}% |

### Milestone Tracking

| Milestone | Target Date | Status | Notes |
|-----------|-------------|--------|-------|
| {{MILESTONE_1}} | {{DATE_1}} | {{STATUS_1}} | {{NOTES_1}} |
| {{MILESTONE_2}} | {{DATE_2}} | {{STATUS_2}} | {{NOTES_2}} |

---

## State Machine Reference

<!--
Source: ONTOLOGY-v1.md Section 3.4.2 - state_machine
Simplified to match worktracker conventions.
-->

```
+-------------------------------------------------------------------+
|                     EPIC STATE MACHINE                             |
+-------------------------------------------------------------------+
|                                                                    |
|   +---------+     +-------------+     +-----------+               |
|   | PENDING |---->| IN_PROGRESS |---->| COMPLETED |               |
|   +---------+     +-------------+     +-----------+               |
|        |               |                   |                       |
|        v               v                   v                       |
|   (Planning)      (Executing)        (Delivered)                  |
|                                                                    |
+-------------------------------------------------------------------+

Allowed Transitions:
- pending -> in_progress: Start execution
- in_progress -> completed: All features delivered
- in_progress -> pending: Deprioritized
- completed -> in_progress: Reopened
```

---

## Containment Rules

<!--
Source: ONTOLOGY-v1.md Section 3.4.2 - containment
-->

| Rule | Value |
|------|-------|
| **Allowed Children** | Capability, Feature |
| **Allowed Parents** | Initiative (or top-level if no Initiative) |
| **Max Depth** | 2 (via Features containing Stories) |

### Hierarchy Diagram

```
EPIC-001: {{EPIC_TITLE}}
|
+-- FEAT-001: {{FEATURE_1}}
|   +-- EN-001: Enabler
|   +-- ST-001: Story
|   +-- ST-002: Story
|
+-- FEAT-002: {{FEATURE_2}}
    +-- ST-003: Story
    +-- ST-004: Story
```

---

## Invariants

<!--
Source: ONTOLOGY-v1.md Section 3.4.2 - invariants
-->

- **INV-E01:** Epic can contain Capabilities or Features (not mixed)
- **INV-E02:** wsjf_score = cost_of_delay / job_size (when both set)
- **INV-E03:** job_size must be > 0 if set
- Title cannot be empty (inherited)
- Status must be valid for Epic state machine (inherited)
- Parent must be valid parent type if set (inherited)
- Circular hierarchy not allowed (inherited)

---

## Related Items

<!--
RECOMMENDED: Link to related work items and artifacts.
-->

### Hierarchy

- **Parent:** [{{PARENT_TITLE}}]({{PARENT_LINK}}) (if applicable)

### Related Epics

- [{{RELATED_EPIC_ID}}]({{RELATED_EPIC_LINK}}) - {{RELATIONSHIP_DESCRIPTION}}

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
| {{CREATED_AT}} | {{CREATED_BY}} | pending | Epic created |
| {{DATE_2}} | {{AUTHOR_2}} | in_progress | Execution started |
| {{DATE_3}} | {{AUTHOR_3}} | completed | All features delivered |

---

## System Mapping

<!--
Source: ONTOLOGY-v1.md Section 3.4.2 - system_mapping
-->

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Epic |
| **SAFe** | Epic (Portfolio Backlog) |
| **JIRA** | Epic |

---

<!--
DESIGN RATIONALE:
Epic is universal across all systems. The additional WSJF properties
support SAFe's economic prioritization model but are optional for
teams not using SAFe.
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
