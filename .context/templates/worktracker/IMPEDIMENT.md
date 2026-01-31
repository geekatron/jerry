# IMP-{{NNN}}: {{IMPEDIMENT_TITLE}}

<!--
TEMPLATE: Impediment
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.11 (Impediment Entity)
CREATED: 2026-01-23 (EN-001 Phase 2A)
PURPOSE: Document blockers preventing progress on work items
USAGE: Track and resolve impediments that block one or more work items
EXTENDS: FlowControlItem -> WorkItem

REQUIREMENTS SATISFIED:
- REQ-IMP-001 to REQ-IMP-026 (nse-requirements-001-template-requirements.md)
- REQ-C-001 to REQ-C-013 (common requirements)

CRITICAL INVARIANTS:
- INV-IM01: blocked_items MUST contain at least one item
- INV-IM02: resolution_notes MUST be set when status is DONE
- INV-IM03: Clear BLOCKED status on dependent items when DONE
- INV-IM04: Impediments have NO allowed_parents (standalone entity)
- INV-IM05: Impediments have NO allowed_children
- INV-SM-003: DONE and REMOVED are terminal states (no reopen)
-->

> **Type:** impediment
> **Status:** {{STATUS}}
> **Priority:** {{PRIORITY}}
> **Impact:** {{IMPACT}}
> **Created:** {{CREATED_AT}}
> **Owner:** {{OWNER}}
> **Escalation:** {{ESCALATION_LEVEL}}

---

## Frontmatter

```yaml
# =============================================================================
# IMPEDIMENT WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.11 (Impediment Entity)
# Purpose: Document blockers preventing progress on work items
# =============================================================================

# Identity (inherited from WorkItem)
id: "IMP-{{NNN}}"                          # Required, immutable - Format: IMP-NNN (standalone)
work_type: IMPEDIMENT                      # Required, immutable - Discriminator
title: "{{IMPEDIMENT_TITLE}}"              # Required - Max 500 chars

# Description
description: |                             # Should (REQ-IMP-004) - Richtext description
  {{IMPEDIMENT_DESCRIPTION}}

# State (see State Machine below)
status: BACKLOG                            # Required - BACKLOG | IN_PROGRESS | DONE | REMOVED
# CRITICAL: DONE is terminal (INV-SM-003) - no reopen allowed

# Priority
priority: MEDIUM                           # Should - CRITICAL | HIGH | MEDIUM | LOW

# People
created_by: "{{CREATED_BY}}"               # Should, auto-populated
owner: "{{OWNER}}"                         # Should (REQ-IMP-013) - Person responsible for resolution

# Timestamps (auto-managed)
created_at: "{{CREATED_AT}}"               # Required, auto, immutable (ISO 8601)
updated_at: "{{UPDATED_AT}}"               # Required, auto (ISO 8601)

# Tags
tags: []                                   # Optional - String array

# =============================================================================
# IMPEDIMENT-SPECIFIC PROPERTIES (ONTOLOGY Section 3.4.11)
# =============================================================================

# Blocked Items - CRITICAL INVARIANT INV-IM01
blocked_items:                             # REQUIRED (REQ-IMP-010) - Min 1 item
  - "{{BLOCKED_ITEM_1}}"                   # Work item ID being blocked
  - "{{BLOCKED_ITEM_2}}"

# Impact Assessment
impact: TEAM                               # Should (REQ-IMP-011) - TEAM | PROGRAM | PORTFOLIO

# Resolution (REQ-IMP-012) - CRITICAL: Required when status=DONE (INV-IM02)
resolution_notes: null                     # MUST set when DONE - How impediment was resolved

# Escalation (REQ-IMP-014)
escalation_level: 0                        # 0=none, 1=manager, 2=director, 3=executive

# Duration Tracking (REQ-IMP-015)
time_blocked: null                         # Auto-calculated from status history (duration)

# External Dependencies (REQ-IMP-016)
external_dependency: null                  # Optional - External team/vendor if applicable
```

---

## State Machine

<!--
Source: ONTOLOGY-v1.md Section 3.4.11 (state_machine)
INV-SM-003: Impediment Status Transitions
CRITICAL: DONE is terminal - no reopen allowed (INV-SM-003)
-->

```
            +-----------+
            |  BACKLOG  |  <-- Initial state
            +-----+-----+
                  |
      +-----------+-----------+
      |                       |
      v                       v
+------------+           +---------+
| IN_PROGRESS|---------->| REMOVED |
+-----+------+           +---------+
      |                   (Terminal - INV-SM-003)
      v
  +------+
  | DONE | (Terminal - INV-IM02: resolution_notes REQUIRED)
  +------+
```

| Status | Description | Entry Criteria | Exit Criteria |
|--------|-------------|----------------|---------------|
| `BACKLOG` | Impediment identified | Blocker created, blocked_items set | Resolution work started |
| `IN_PROGRESS` | Actively being resolved | Owner assigned, work begun | Resolved or removed |
| `DONE` | Impediment resolved | resolution_notes set (INV-IM02) | **Terminal (no exit)** |
| `REMOVED` | Impediment cancelled | No longer blocking (cancelled) | **Terminal (no exit)** |

**Allowed Transitions:**
- BACKLOG -> IN_PROGRESS (start working on resolution)
- BACKLOG -> REMOVED (cancelled before work started)
- IN_PROGRESS -> DONE (resolved - requires resolution_notes)
- IN_PROGRESS -> REMOVED (cancelled during resolution)

**Forbidden (INV-SM-003):**
- DONE -> any state (terminal - cannot reopen)
- REMOVED -> any state (terminal - cannot reopen)

---

## Containment Rules

<!--
Source: ONTOLOGY-v1.md Section 3.4.11 (containment)
CRITICAL: Impediments are standalone entities with NO hierarchy.
-->

| Rule | Value | Invariant |
|------|-------|-----------|
| **Allowed Children** | None | INV-IM05: Impediments don't contain work |
| **Allowed Parents** | None | INV-IM04: Standalone entity |
| **Max Depth** | 0 | Leaf node only |
| **Co-Location** | Enabler/Story level folder | REQ-IMP-025 |

**Note:** Impediments can block ANY work item type but do not belong to the work item hierarchy. They are cross-cutting concerns that affect multiple items.

---

## Summary

<!--
Required (REQ-IMP-020): Brief description of the blocker.
Should clearly state what is blocked and the current impact.
-->

{{SUMMARY_STATEMENT}}

**Current Status:** {{STATUS}}
**Items Blocked:** {{BLOCKED_COUNT}}
**Escalation Level:** {{ESCALATION_LEVEL}} ({{ESCALATION_DESCRIPTION}})

---

## Blocked Items

<!--
Required (REQ-IMP-021): List of work items blocked by this impediment.
CRITICAL INVARIANT (INV-IM01): Must contain at least one item.
-->

| Work Item | Type | Impact | Blocked Since | Expected Delay |
|-----------|------|--------|---------------|----------------|
| [{{BLOCKED_ITEM_1}}]({{BLOCKED_ITEM_1_PATH}}) | {{BLOCKED_ITEM_1_TYPE}} | {{IMPACT_1}} | {{BLOCKED_SINCE_1}} | {{EXPECTED_DELAY_1}} |
| [{{BLOCKED_ITEM_2}}]({{BLOCKED_ITEM_2_PATH}}) | {{BLOCKED_ITEM_2_TYPE}} | {{IMPACT_2}} | {{BLOCKED_SINCE_2}} | {{EXPECTED_DELAY_2}} |

**Total Blocked Items:** {{BLOCKED_COUNT}}
**Total Expected Delay:** {{TOTAL_DELAY}}

<!--
INVARIANT CHECK (INV-IM01):
- This table MUST contain at least one row.
- Empty blocked_items array is a validation error.
-->

---

## Impact Assessment

<!--
Should (REQ-IMP-022): Business and technical impact assessment.
-->

### Scope

| Level | Description |
|-------|-------------|
| **Impact Level** | {{IMPACT}} (TEAM / PROGRAM / PORTFOLIO) |
| **Teams Affected** | {{TEAMS_AFFECTED}} |
| **Workstreams Affected** | {{WORKSTREAMS_AFFECTED}} |

### Business Impact

{{BUSINESS_IMPACT_DESCRIPTION}}

**Quantified Impact:**
- Schedule Risk: {{SCHEDULE_RISK}}
- Cost Impact: {{COST_IMPACT}}
- Quality Impact: {{QUALITY_IMPACT}}

### Technical Impact

{{TECHNICAL_IMPACT_DESCRIPTION}}

**Affected Systems:**
- {{SYSTEM_1}}
- {{SYSTEM_2}}

### Duration Estimate

| Scenario | Duration | Likelihood |
|----------|----------|------------|
| Best Case | {{BEST_CASE}} | {{BEST_LIKELIHOOD}} |
| Most Likely | {{LIKELY_CASE}} | {{LIKELY_LIKELIHOOD}} |
| Worst Case | {{WORST_CASE}} | {{WORST_LIKELIHOOD}} |

---

## Root Cause Analysis

<!--
Optional: Understanding why the impediment exists.
-->

### Root Cause

{{ROOT_CAUSE_DESCRIPTION}}

### Contributing Factors

- {{FACTOR_1}}
- {{FACTOR_2}}

### Category

| Root Cause Type | Description |
|-----------------|-------------|
| **Type** | {{ROOT_CAUSE_TYPE}} |
| **Category** | TECHNICAL / RESOURCE / EXTERNAL / DECISION / OTHER |
| **Preventable** | {{WAS_PREVENTABLE}} (Yes/No) |

---

## Resolution

<!--
Required (REQ-IMP-023): Resolution tracking.
-->

### Resolution Status

| Field | Value |
|-------|-------|
| **Proposed Solution** | {{PROPOSED_SOLUTION}} |
| **Assigned To** | {{OWNER}} |
| **Target Resolution Date** | {{TARGET_DATE}} |
| **Actual Resolution Date** | {{ACTUAL_DATE}} |
| **Resolution Approach** | {{RESOLUTION_APPROACH}} |

### Action Items

| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|
| 1 | {{ACTION_1}} | {{OWNER_1}} | {{DUE_1}} | {{STATUS_1}} |
| 2 | {{ACTION_2}} | {{OWNER_2}} | {{DUE_2}} | {{STATUS_2}} |

### Resolution Notes

<!--
CRITICAL INVARIANT (INV-IM02): This section MUST be populated when status=DONE.
Document how the impediment was actually resolved.
-->

{{RESOLUTION_NOTES}}

**Resolution Category:** {{RESOLUTION_CATEGORY}}
- FIXED: Root cause addressed
- WORKAROUND: Temporary solution applied
- ACCEPTED: Risk accepted, work proceeds
- REMOVED: No longer applicable

---

## Escalation History

<!--
Should (REQ-IMP-026): Track escalation timeline.
Escalation levels: 0=none, 1=manager, 2=director, 3=executive
-->

| Date | Level | Escalated To | Reason | Outcome |
|------|-------|--------------|--------|---------|
| {{ESCALATION_DATE_1}} | {{LEVEL_1}} | {{ESCALATED_TO_1}} | {{REASON_1}} | {{OUTCOME_1}} |
| {{ESCALATION_DATE_2}} | {{LEVEL_2}} | {{ESCALATED_TO_2}} | {{REASON_2}} | {{OUTCOME_2}} |

**Escalation Level Guide:**
| Level | Role | When to Escalate |
|-------|------|------------------|
| 0 | None | Standard impediment, team can resolve |
| 1 | Manager | Team needs support, resource constraints |
| 2 | Director | Cross-team coordination, policy issues |
| 3 | Executive | Business-critical, strategic decisions needed |

---

## Related Artifacts

<!--
Required (REQ-C-005): Links to blocked work items and resolution items.
-->

| Type | Path | Description |
|------|------|-------------|
| Blocks | [{{BLOCKED_ITEM_1}}]({{BLOCKED_ITEM_1_PATH}}) | Primary blocked item |
| Blocks | [{{BLOCKED_ITEM_2}}]({{BLOCKED_ITEM_2_PATH}}) | Secondary blocked item |
| Resolution Task | [{{RESOLUTION_TASK}}]({{RESOLUTION_TASK_PATH}}) | Task created to resolve (if applicable) |
| Related Bug | [{{RELATED_BUG}}]({{RELATED_BUG_PATH}}) | Related bug (if applicable) |
| External | {{EXTERNAL_LINK}} | External dependency reference |
| Convention | [docs/conventions/worktracker.md](../../../conventions/worktracker.md) | Worktracker conventions |

---

## Document History

<!--
Should (REQ-IMP-026): Track impediment lifecycle.
-->

| Date | Status | Author | Notes |
|------|--------|--------|-------|
| {{DATE_N}} | {{STATUS_N}} | {{AUTHOR_N}} | {{NOTES_N}} |
| {{CREATED_AT}} | BACKLOG | {{CREATED_BY}} | Impediment identified |

---

## Invariants

<!--
Should (REQ-IMP-019): Document business rules and constraints.
Source: ONTOLOGY-v1.md Section 3.4.11
-->

| Invariant | Rule | Enforcement |
|-----------|------|-------------|
| **INV-IM01** | blocked_items MUST contain at least 1 item | HARD - validation error if empty |
| **INV-IM02** | resolution_notes MUST be set when status=DONE | HARD - cannot transition to DONE without |
| **INV-IM03** | Clear BLOCKED status on dependent items when DONE | SOFT - recommended process |
| **INV-IM04** | Impediments have NO allowed_parents | HARD - standalone entity |
| **INV-IM05** | Impediments have NO allowed_children | HARD - leaf node only |
| **INV-SM-003** | DONE and REMOVED are terminal states | HARD - no reopen allowed |

---

## Metadata

<!--
Required (REQ-IMP-024): Machine-readable metadata for tooling and automation.
Keep in sync with frontmatter above.
-->

```yaml
id: "IMP-{{NNN}}"
work_type: IMPEDIMENT
title: "{{IMPEDIMENT_TITLE}}"
description: "{{IMPEDIMENT_DESCRIPTION}}"
status: {{STATUS}}
priority: {{PRIORITY}}
created_by: "{{CREATED_BY}}"
created_at: "{{CREATED_AT}}"
updated_at: "{{UPDATED_AT}}"
owner: "{{OWNER}}"
blocked_items: [{{BLOCKED_ITEM_1}}, {{BLOCKED_ITEM_2}}]
impact: {{IMPACT}}
escalation_level: {{ESCALATION_LEVEL}}
time_blocked: {{TIME_BLOCKED}}
external_dependency: {{EXTERNAL_DEPENDENCY}}
resolution_notes: {{RESOLUTION_NOTES}}
tags: [{{TAG_1}}, {{TAG_2}}]
```

---

<!--
DESIGN RATIONALE:

This template documents blockers preventing progress on work items. It follows
ONTOLOGY-v1.md Section 3.4.11 (Impediment Entity) exactly and extends
FlowControlItem -> WorkItem.

KEY DESIGN CHOICES:

1. Standalone Entity (INV-IM04, INV-IM05): Impediments exist outside the work
   item hierarchy. They BLOCK work items but do not belong to them. This allows
   a single impediment to affect multiple items across the hierarchy.

2. Terminal DONE State (INV-SM-003, REQ-IMP-006): Once an impediment is DONE,
   it cannot be reopened. If the same issue recurs, create a NEW impediment.
   This preserves the historical record of resolved blockers.

3. Required blocked_items (INV-IM01): An impediment without blocked items is
   meaningless. The array MUST contain at least one work item ID.

4. Required resolution_notes when DONE (INV-IM02): Documenting how an impediment
   was resolved is critical for future reference and similar issues.

5. Escalation Levels: 0-3 scale matches organizational hierarchy for appropriate
   response based on impact scope.

6. Impact Scope (TEAM/PROGRAM/PORTFOLIO): From ONTOLOGY FlowControlItem,
   indicates the blast radius of the impediment.

SYSTEM MAPPING:
- Azure DevOps: Impediment (separate work item type)
- SAFe: Impediment (tracked on Program/Team boards)
- JIRA: Issue with "Impediment" label or linked as Blocker

SOURCES:
- ONTOLOGY-v1.md Section 3.4.11: Impediment entity specification
- ONTOLOGY-v1.md Section 3.3.4: FlowControlItem abstract class
- nse-requirements-001-template-requirements.md: REQ-IMP-001 to REQ-IMP-026
- nse-architecture-001-template-architecture.md: Section 1.3, 5.3

TRACE:
- EN-001: Hierarchical Worktracker Conventions (parent enabler)
- ps-analyst-001-pattern-analysis.md: Section 3.3 IMPEDIMENT Blueprint
-->
