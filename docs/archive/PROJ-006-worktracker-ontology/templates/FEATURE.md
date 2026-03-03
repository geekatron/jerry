# {{FEATURE_ID}}: {{FEATURE_TITLE}}

<!--
TEMPLATE: Feature
VERSION: DRAFT v0.1
SOURCE: ONTOLOGY-v1.md Section 3.4.4
GENERATED: Phase 5, WI-002 - Generate Work Item Templates
-->

---

## Frontmatter

```yaml
# =============================================================================
# FEATURE WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.4 (Feature Entity Schema)
# =============================================================================

# Identity (inherited from WorkItem - Section 2.1)
id: "{{FEATURE_ID}}"                     # Required, immutable - Format: system:key
work_type: FEATURE                       # Required, immutable - Discriminator
title: "{{FEATURE_TITLE}}"               # Required - Max 500 chars

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
parent_id: "{{EPIC_ID}}"                 # Required - Epic or Capability ID

# Tags
tags: []                                 # Optional - String array

# =============================================================================
# FEATURE-SPECIFIC PROPERTIES (Section 3.4.4)
# =============================================================================

# Strategic (from StrategicItem)
target_date: null                        # Optional - Target completion date
business_outcome: null                   # Optional - Expected outcomes

# Feature-Specific
target_sprint: null                      # Optional - Target sprint/iteration (max 50 chars)
value_area: BUSINESS                     # Optional - BUSINESS | ARCHITECTURAL (default: BUSINESS)
```

---

## Description

<!-- Required: Provide a clear, concise description of the Feature -->

{{DESCRIPTION}}

---

## Benefit Hypothesis

<!-- Optional: Expected benefits from this feature -->
<!-- Source: ONTOLOGY-v1.md Section 3.4.4 - benefit_hypothesis (max 5000 chars) -->
<!-- Maps to: ADO:Value, SAFe:benefit_hypothesis -->

**We believe that** {{HYPOTHESIS_STATEMENT}}

**Will result in** {{EXPECTED_BENEFIT}}

**We will know we have succeeded when** {{SUCCESS_METRICS}}

---

## Acceptance Criteria

<!-- Required before DONE status (INV-FE02) -->
<!-- Source: ONTOLOGY-v1.md Section 3.4.4 - acceptance_criteria (max 10000 chars) -->
<!-- Maps to: ADO:AcceptanceCriteria, SAFe:acceptance_criteria -->

### Definition of Done

- [ ] {{CRITERION_1}}
- [ ] {{CRITERION_2}}
- [ ] {{CRITERION_3}}

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | {{ACCEPTANCE_CRITERION}} | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | {{NON_FUNCTIONAL_CRITERION}} | [ ] |

---

## MVP Definition

<!-- Optional: Minimum Viable Product scope -->
<!-- Source: ONTOLOGY-v1.md Section 3.4.4 - mvp_definition (max 5000 chars) -->
<!-- Maps to: SAFe:mvp_definition -->

### In Scope (MVP)

- {{MVP_ITEM_1}}
- {{MVP_ITEM_2}}

### Out of Scope (Future)

- {{FUTURE_ITEM_1}}
- {{FUTURE_ITEM_2}}

---

## Children (Contained Work Items)

<!-- Source: ONTOLOGY-v1.md Section 3.4.4 - containment -->
<!-- allowed_children: [Story, Enabler] -->
<!-- max_depth: 1 -->

| ID | Type | Title | Status | Effort |
|----|------|-------|--------|--------|
| {{CHILD_ID}} | Story | {{CHILD_TITLE}} | {{CHILD_STATUS}} | {{CHILD_EFFORT}} |

---

## State Machine Reference

<!-- Source: ONTOLOGY-v1.md Section 3.4.4 - state_machine -->

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
│  Note: IN_REVIEW is available for Features (not all entities)            │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

From BACKLOG:     → READY, REMOVED
From READY:       → IN_PROGRESS, BACKLOG, REMOVED
From IN_PROGRESS: → IN_REVIEW, DONE, BLOCKED, REMOVED
From BLOCKED:     → IN_PROGRESS, REMOVED
From IN_REVIEW:   → DONE, IN_PROGRESS
From DONE:        → IN_PROGRESS (reopen)
From REMOVED:     → (terminal)
```

---

## Containment Rules

<!-- Source: ONTOLOGY-v1.md Section 3.4.4 - containment -->

| Rule | Value |
|------|-------|
| **Allowed Children** | Story, Enabler |
| **Allowed Parents** | Epic, Capability |
| **Max Depth** | 1 |

---

## Invariants

<!-- Source: ONTOLOGY-v1.md Section 3.4.4 - invariants -->

- INV-FE01: Feature can contain Stories or Enablers
- INV-FE02: acceptance_criteria should be defined before DONE
- Title cannot be empty (inherited)
- Status must be valid for Feature state machine (inherited)
- Parent must be valid parent type if set (inherited)
- Circular hierarchy not allowed (inherited)

---

## System Mapping

<!-- Source: ONTOLOGY-v1.md Section 3.4.4 - system_mapping -->

| System | Maps To |
|--------|---------|
| **Azure DevOps** | Feature |
| **SAFe** | Feature (Program Backlog) |
| **JIRA** | Epic (or custom issue type) |

---

## Changelog

| Date | Author | Change |
|------|--------|--------|
| {{CREATED_AT}} | {{CREATED_BY}} | Created |

---

<!--
DESIGN RATIONALE (from ONTOLOGY-v1.md):
Feature retained as distinct level despite JIRA lacking it natively.
JIRA users map Epic-to-Feature or create custom issue type.
Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2, Section 2.3
-->
