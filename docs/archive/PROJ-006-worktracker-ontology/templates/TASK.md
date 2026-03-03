# {{TITLE}}

<!--
TEMPLATE: Task (DRAFT)
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 0.1.0
STATUS: DRAFT - Pending review

DESCRIPTION:
  Specific work unit typically completed in hours to a day.
  Universal concept with identical semantics across ADO, SAFe, and JIRA.

EXTENDS: DeliveryItem -> WorkItem
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
id: "{{ID}}"                           # Format: PREFIX-NNN (e.g., TASK-001)
work_type: TASK                        # Immutable discriminator

# === CORE METADATA ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
title: "{{TITLE}}"                     # Required, 1-500 chars
description: |
  {{DESCRIPTION}}

# === CLASSIFICATION ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
classification: BUSINESS               # BUSINESS | ENABLER (default: BUSINESS)

# === LIFECYCLE STATE ===
# Source: ONTOLOGY-v1.md Section 3.4.6 (Task state_machine)
status: BACKLOG                        # See State Machine below
resolution: null                       # Set when status is DONE or REMOVED

# === PRIORITY ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
priority: MEDIUM                       # CRITICAL | HIGH | MEDIUM | LOW

# === PEOPLE ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
assignee: "{{ASSIGNEE}}"               # User responsible
created_by: "{{CREATED_BY}}"           # Auto-set on creation

# === TIMESTAMPS (Auto-managed) ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
created_at: "{{CREATED_AT}}"           # ISO 8601 datetime
updated_at: "{{UPDATED_AT}}"           # ISO 8601 datetime

# === HIERARCHY ===
# Source: ONTOLOGY-v1.md Section 3.4.6 (Task containment)
parent_id: "{{PARENT_ID}}"             # Story, Bug, or Enabler ID

# === TAGS ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
tags:
  - "{{TAG_1}}"
  - "{{TAG_2}}"

# === DELIVERY ITEM PROPERTIES ===
# Source: ONTOLOGY-v1.md Section 3.3.2 (DeliveryItem)
effort: null                           # Story points or effort estimate (0-100)
acceptance_criteria: |
  {{ACCEPTANCE_CRITERIA}}
due_date: null                         # ISO 8601 date

# === TASK-SPECIFIC PROPERTIES ===
# Source: ONTOLOGY-v1.md Section 3.4.6 (Task.specific)
activity: null                         # DEVELOPMENT | TESTING | DOCUMENTATION | DESIGN | DEPLOYMENT | RESEARCH | OTHER
original_estimate: null                # Initial time estimate in hours (min: 0)
remaining_work: null                   # Remaining effort in hours (min: 0)
time_spent: null                       # Actual time logged in hours (min: 0)
```

---

## State Machine

<!-- Source: ONTOLOGY-v1.md Section 3.4.6 (Task.state_machine) -->

**Initial State:** `BACKLOG`

**Valid States:** `BACKLOG`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `REMOVED`

**Note:** Tasks use a simplified state machine - no `READY` or `IN_REVIEW` states.

```
              +-----------+
              |  BACKLOG  |
              +-----+-----+
                    |
        +-----------+-----------+
        |                       |
        v                       v
  +------------+           +---------+
  | IN_PROGRESS|---------->| REMOVED |
  +-----+------+           +---------+
        |
    +---+---+
    |       |
    v       v
+-------+ +------+
|BLOCKED| | DONE |
+---+---+ +--+---+
    |        |
    |        | (Reopen)
    v        v
  +------------+
  | IN_PROGRESS|
  +------------+
```

| From State    | Allowed Transitions                    |
|---------------|----------------------------------------|
| BACKLOG       | IN_PROGRESS, REMOVED                   |
| IN_PROGRESS   | BLOCKED, DONE, REMOVED                 |
| BLOCKED       | IN_PROGRESS, REMOVED                   |
| DONE          | IN_PROGRESS (Reopen)                   |
| REMOVED       | (Terminal - no transitions)            |

---

## Containment Rules

<!-- Source: ONTOLOGY-v1.md Section 3.4.6 (Task.containment) -->

| Rule             | Value                           |
|------------------|---------------------------------|
| Allowed Children | Subtask                         |
| Allowed Parents  | Story, Bug, Enabler             |
| Max Depth        | 1                               |

---

## Invariants

<!-- Source: ONTOLOGY-v1.md Section 3.4.6 (Task.invariants) -->

- **INV-D01:** effort must be non-negative (inherited from DeliveryItem)
- **INV-D02:** acceptance_criteria should be defined before IN_PROGRESS (inherited)
- **INV-T01:** Task can have Story, Bug, or Enabler as parent
- **INV-T02:** remaining_work <= original_estimate when both set
- **INV-T03:** time_spent should be updated when DONE

---

## System Mapping

<!-- Source: ONTOLOGY-v1.md Section 3.4.6 (Task.system_mapping) -->

| System | Mapping                          |
|--------|----------------------------------|
| ADO    | Task                             |
| SAFe   | Task                             |
| JIRA   | Task, Sub-task                   |

---

## Content

### Description

{{DESCRIPTION_CONTENT}}

### Acceptance Criteria

- [ ] {{CRITERION_1}}
- [ ] {{CRITERION_2}}
- [ ] {{CRITERION_3}}

### Implementation Notes

{{IMPLEMENTATION_NOTES}}

### Related Items

- Parent: [{{PARENT_TITLE}}]({{PARENT_LINK}})
- Related: [{{RELATED_ITEM}}]({{RELATED_LINK}})

---

## Time Tracking

| Metric            | Value           |
|-------------------|-----------------|
| Original Estimate | {{ORIGINAL_ESTIMATE}} hours |
| Remaining Work    | {{REMAINING_WORK}} hours    |
| Time Spent        | {{TIME_SPENT}} hours        |

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| {{DATE}}   | Created     | Initial creation               |

---

<!--
JERRY ALIGNMENT:
  existing_type: "WorkType.TASK"
  changes_needed: "None - already exists"

DESIGN RATIONALE:
  Task is universally agreed across all systems. No translation needed.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.1
-->
