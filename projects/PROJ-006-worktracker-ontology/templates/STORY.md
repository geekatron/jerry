# {{STORY_ID}}: {{STORY_TITLE}}

<!--
TEMPLATE: Story
VERSION: DRAFT v0.1
SOURCE: ONTOLOGY-v1.md Section 3.4.5
GENERATED: Phase 5, WI-002 - Generate Work Item Templates
-->

---

## Frontmatter

```yaml
# =============================================================================
# STORY WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.5 (Story Entity Schema)
# =============================================================================

# Identity (inherited from WorkItem - Section 2.1)
id: "{{STORY_ID}}"                       # Required, immutable - Format: system:key
work_type: STORY                         # Required, immutable - Discriminator
title: "{{STORY_TITLE}}"                 # Required - Max 500 chars

# Classification
classification: BUSINESS                 # Optional - BUSINESS | ENABLER (default: BUSINESS)

# State (see State Machine below)
status: BACKLOG                          # Required - WorkItemStatus enum
resolution: null                         # Optional - Resolution enum (when DONE/REMOVED)

# Priority
priority: MEDIUM                         # Optional - CRITICAL | HIGH | MEDIUM | LOW

# People
assignee: null                           # Optional - User reference
created_by: "{{CREATED_BY}}"             # Required, auto-populated

# Timestamps (auto-managed)
created_at: "{{CREATED_AT}}"             # Required, auto, immutable
updated_at: "{{UPDATED_AT}}"             # Required, auto

# Hierarchy
parent_id: "{{FEATURE_ID}}"              # Required - Feature ID (INV-ST01)

# Tags
tags: []                                 # Optional - String array

# =============================================================================
# STORY-SPECIFIC PROPERTIES (Section 3.4.5)
# =============================================================================

# From DeliveryItem
effort: null                             # Optional - Story points (1-13 Fibonacci recommended)
due_date: null                           # Optional - Sprint/iteration deadline

# Story-Specific
value_area: BUSINESS                     # Optional - BUSINESS | ARCHITECTURAL (default: BUSINESS)

# User Story Format (optional structured format)
user_role: null                          # "As a <user_role>..." (max 100 chars)
user_goal: null                          # "I want <goal>..." (max 500 chars)
user_benefit: null                       # "So that <benefit>..." (max 500 chars)
```

---

## User Story

<!-- Optional: Structured user story format -->
<!-- Source: ONTOLOGY-v1.md Section 3.4.5 - user_role, user_goal, user_benefit -->

**As a** {{USER_ROLE}}

**I want** {{USER_GOAL}}

**So that** {{USER_BENEFIT}}

---

## Description

<!-- Required: Provide additional context and details -->

{{DESCRIPTION}}

---

## Acceptance Criteria

<!-- Required before DONE status (INV-ST03) -->
<!-- Source: ONTOLOGY-v1.md Section 3.4.5 - acceptance_criteria (from DeliveryItem) -->
<!-- Maps to: ADO:AcceptanceCriteria, SAFe:acceptance_criteria -->

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

### Definition of Done

- [ ] Code complete and peer reviewed
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] Acceptance criteria verified

---

## Estimation

<!-- Source: ONTOLOGY-v1.md Section 3.4.5 - effort -->
<!-- Maps to: ADO:Effort, SAFe:story_points, JIRA:story_points -->

| Attribute | Value |
|-----------|-------|
| **Story Points** | {{EFFORT}} |
| **T-Shirt Size** | {{TSHIRT_SIZE}} |
| **Sprint** | {{TARGET_SPRINT}} |

> **Note (INV-ST02):** Story effort is typically 1-13 (Fibonacci scale: 1, 2, 3, 5, 8, 13)

---

## Children (Contained Work Items)

<!-- Source: ONTOLOGY-v1.md Section 3.4.5 - containment -->
<!-- allowed_children: [Task, Subtask] -->
<!-- max_depth: 2 -->

| ID | Type | Title | Status | Remaining |
|----|------|-------|--------|-----------|
| {{CHILD_ID}} | Task | {{CHILD_TITLE}} | {{CHILD_STATUS}} | {{REMAINING_WORK}} |

---

## State Machine Reference

<!-- Source: ONTOLOGY-v1.md Section 3.4.5 - state_machine -->

```
Initial State: BACKLOG
Valid States: [BACKLOG, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, DONE, REMOVED]

Transitions:
┌───────────────────────────────────────────────────────────────────────────┐
│                                                                           │
│  BACKLOG ─────► READY ─────► IN_PROGRESS ────► IN_REVIEW ────► DONE      │
│     │             │              │    │            │             │        │
│     │             │              │    └──► BLOCKED─┘             │        │
│     │             │              │              │                 │        │
│     ▼             ▼              ▼              ▼                 ▼        │
│  REMOVED ◄────────────────────────────────────────◄──────────────┘        │
│                                                                           │
│  Stories have full state machine with BLOCKED and IN_REVIEW states       │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

From BACKLOG:     → READY, REMOVED
From READY:       → IN_PROGRESS, BACKLOG, REMOVED
From IN_PROGRESS: → BLOCKED, IN_REVIEW, DONE, REMOVED
From BLOCKED:     → IN_PROGRESS, REMOVED
From IN_REVIEW:   → DONE, IN_PROGRESS
From DONE:        → IN_PROGRESS (reopen)
From REMOVED:     → (terminal)
```

---

## Containment Rules

<!-- Source: ONTOLOGY-v1.md Section 3.4.5 - containment -->

| Rule | Value |
|------|-------|
| **Allowed Children** | Task, Subtask |
| **Allowed Parents** | Feature |
| **Max Depth** | 2 |

---

## Invariants

<!-- Source: ONTOLOGY-v1.md Section 3.4.5 - invariants -->

- INV-ST01: Story must have Feature as parent
- INV-ST02: Story effort is typically 1-13 (Fibonacci)
- INV-ST03: acceptance_criteria must be defined before DONE
- Title cannot be empty (inherited)
- Status must be valid for Story state machine (inherited)
- Parent must be valid parent type if set (inherited)
- Circular hierarchy not allowed (inherited)

---

## System Mapping

<!-- Source: ONTOLOGY-v1.md Section 3.4.5 - system_mapping -->

| System | Maps To |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (PBI) |
| **SAFe** | Story |
| **JIRA** | Story |

---

## Changelog

| Date | Author | Change |
|------|--------|--------|
| {{CREATED_AT}} | {{CREATED_BY}} | Created |

---

<!--
DESIGN RATIONALE (from ONTOLOGY-v1.md):
"Story" chosen over "PBI" because: (1) more intuitive for users,
(2) used by 2/3 systems natively, (3) aligns with Scrum terminology.
Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2 (Canonical Name Rationale)
-->
