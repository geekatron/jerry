# {{EPIC_ID}}: {{EPIC_TITLE}}

<!--
TEMPLATE: Epic
VERSION: DRAFT v0.1
SOURCE: ONTOLOGY-v1.md Section 3.4.2
GENERATED: Phase 5, WI-002 - Generate Work Item Templates
-->

---

## Frontmatter

```yaml
# =============================================================================
# EPIC WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.2 (Epic Entity Schema)
# =============================================================================

# Identity (inherited from WorkItem - Section 2.1)
id: "{{EPIC_ID}}"                        # Required, immutable - Format: system:key
work_type: EPIC                          # Required, immutable - Discriminator
title: "{{EPIC_TITLE}}"                  # Required - Max 500 chars

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
parent_id: null                          # Optional - Initiative ID (or top-level)

# Tags
tags: []                                 # Optional - String array

# =============================================================================
# EPIC-SPECIFIC PROPERTIES (Section 3.4.2)
# =============================================================================

# Target Quarter
target_quarter: null                     # Optional - Pattern: ^FY[0-9]{2}-Q[1-4]$ (e.g., FY25-Q2)

# Strategic
target_date: null                        # Optional - Target completion date (from StrategicItem)
business_outcome: null                   # Optional - Expected outcomes (from StrategicItem)

# SAFe WSJF Properties (Optional - for SAFe teams)
wsjf_score: null                         # Calculated: cost_of_delay / job_size
cost_of_delay: null                      # Sum of: business_value + time_criticality + risk_reduction
job_size: null                           # Implementation size (1-13 Fibonacci, min: 1)

# Lean Business Case (Optional - for SAFe teams)
lean_business_case:
  problem: null
  solution: null
  cost: null
  benefit: null
  risk: null
```

---

## Description

<!-- Required: Provide a clear, concise description of the Epic -->

{{DESCRIPTION}}

---

## Business Outcome Hypothesis

<!-- Optional: Expected business outcomes (SAFe pattern) -->
<!-- Source: ONTOLOGY-v1.md Section 3.4.2 - business_outcome -->

**We believe that** {{HYPOTHESIS_STATEMENT}}

**Will result in** {{EXPECTED_OUTCOME}}

**We will know we have succeeded when** {{SUCCESS_CRITERIA}}

---

## Lean Business Case

<!-- Optional: Economic justification (SAFe pattern) -->
<!-- Source: ONTOLOGY-v1.md Section 3.4.2 - lean_business_case -->

| Aspect | Description |
|--------|-------------|
| **Problem** | {{PROBLEM_STATEMENT}} |
| **Solution** | {{SOLUTION_STATEMENT}} |
| **Cost** | {{ESTIMATED_COST}} |
| **Benefit** | {{ESTIMATED_BENEFIT}} |
| **Risk** | {{RISK_ASSESSMENT}} |

---

## Children (Contained Work Items)

<!-- Source: ONTOLOGY-v1.md Section 3.4.2 - containment -->
<!-- allowed_children: [Capability, Feature] -->
<!-- max_depth: 2 -->

| ID | Type | Title | Status |
|----|------|-------|--------|
| {{CHILD_ID}} | Feature | {{CHILD_TITLE}} | {{CHILD_STATUS}} |

---

## State Machine Reference

<!-- Source: ONTOLOGY-v1.md Section 3.4.2 - state_machine -->

```
Initial State: BACKLOG
Valid States: [BACKLOG, READY, IN_PROGRESS, BLOCKED, DONE, REMOVED]

Transitions:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  BACKLOG ─────► READY ─────► IN_PROGRESS ────► DONE            │
│     │             │              │    │          │              │
│     │             │              │    └──► BLOCKED──┘            │
│     │             │              │              │                │
│     ▼             ▼              ▼              │                │
│  REMOVED ◄───────────────────────────◄─────────┘                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

From BACKLOG:    → READY, REMOVED
From READY:      → IN_PROGRESS, BACKLOG, REMOVED
From IN_PROGRESS: → DONE, BLOCKED, REMOVED
From BLOCKED:    → IN_PROGRESS, REMOVED
From DONE:       → IN_PROGRESS (reopen)
From REMOVED:    → (terminal)
```

---

## Containment Rules

<!-- Source: ONTOLOGY-v1.md Section 3.4.2 - containment -->

| Rule | Value |
|------|-------|
| **Allowed Children** | Capability, Feature |
| **Allowed Parents** | Initiative (or top-level if no Initiative) |
| **Max Depth** | 2 (via Feature) |

---

## Invariants

<!-- Source: ONTOLOGY-v1.md Section 3.4.2 - invariants -->

- INV-E01: Epic can contain Capabilities or Features (not mixed)
- INV-E02: wsjf_score = cost_of_delay / job_size (when both set)
- INV-E03: job_size must be > 0 if set
- Title cannot be empty (inherited)
- Status must be valid for Epic state machine (inherited)
- Parent must be valid parent type if set (inherited)
- Circular hierarchy not allowed (inherited)

---

## System Mapping

<!-- Source: ONTOLOGY-v1.md Section 3.4.2 - system_mapping -->

| System | Maps To |
|--------|---------|
| **Azure DevOps** | Epic |
| **SAFe** | Epic (Portfolio Backlog) |
| **JIRA** | Epic |

---

## Changelog

| Date | Author | Change |
|------|--------|--------|
| {{CREATED_AT}} | {{CREATED_BY}} | Created |

---

<!--
DESIGN RATIONALE (from ONTOLOGY-v1.md):
Epic is universal across all systems. The additional WSJF properties
support SAFe's economic prioritization model but are optional for
teams not using SAFe.
Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2 (Canonical Name Rationale)
-->
