# TASK-002: Create ADR-002 - Artifact Structure & Token Management

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
id: "TASK-002"                           # Enabler-scoped ID
work_type: TASK                          # Immutable discriminator

# === CORE METADATA ===
title: "Create ADR-002: Artifact Structure & Token Management"
description: |
  Research and create Architecture Decision Record for the Transcript Skill
  artifact structure and token management. Define directory layout, token
  budget per artifact (35K limit), and naming conventions.

# === CLASSIFICATION ===
classification: ENABLER                  # Architecture enabler work

# === LIFECYCLE STATE ===
status: BACKLOG                          # See State Machine below
resolution: null                         # Set when status is DONE or REMOVED

# === PRIORITY ===
priority: HIGH                           # Critical path for implementation

# === PEOPLE ===
assignee: "ps-architect"                 # Primary agent
created_by: "Claude"                     # Auto-set on creation

# === TIMESTAMPS (Auto-managed) ===
created_at: "2026-01-26T00:00:00Z"       # ISO 8601 datetime
updated_at: "2026-01-26T00:00:00Z"       # ISO 8601 datetime

# === HIERARCHY ===
parent_id: "EN-004"                      # Parent Enabler

# === TAGS ===
tags:
  - "architecture"
  - "adr"
  - "token-management"
  - "artifact-structure"
  - "transcript-skill"

# === DELIVERY ITEM PROPERTIES ===
effort: 2                                # Story points
acceptance_criteria: |
  - ADR-002 created using docs/knowledge/exemplars/templates/adr.md
  - Context section with token limit problem statement
  - At least 3 options for artifact structure considered
  - Decision with rationale for 35K token limit
  - Naming conventions documented
  - Directory layout specified
due_date: null                           # ISO 8601 date

# === TASK-SPECIFIC PROPERTIES ===
activity: DESIGN                         # Architecture design work
original_estimate: 4                     # Initial time estimate in hours
remaining_work: 4                        # Remaining effort in hours
time_spent: 0                            # Actual time logged in hours
```

---

## State Machine

<!-- Source: ONTOLOGY-v1.md Section 3.4.6 (Task.state_machine) -->

**Initial State:** `BACKLOG`

**Valid States:** `BACKLOG`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `REMOVED`

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

| Rule             | Value                           |
|------------------|---------------------------------|
| Allowed Children | Subtask                         |
| Allowed Parents  | Story, Bug, Enabler             |
| Max Depth        | 1                               |

---

## Invariants

- **INV-D01:** effort must be non-negative (inherited from DeliveryItem)
- **INV-D02:** acceptance_criteria should be defined before IN_PROGRESS (inherited)
- **INV-T01:** Task can have Story, Bug, or Enabler as parent
- **INV-T02:** remaining_work <= original_estimate when both set
- **INV-T03:** time_spent should be updated when DONE

---

## System Mapping

| System | Mapping                          |
|--------|----------------------------------|
| ADO    | Task                             |
| SAFe   | Task                             |
| JIRA   | Task, Sub-task                   |

---

## Content

### Description

Create Architecture Decision Record (ADR-002) for the Transcript Skill artifact structure and token management. This ADR addresses the critical constraint of keeping artifacts under 35K tokens for Claude context window compatibility.

**Key Decisions Required:**
1. **Directory Structure**: What is the optimal directory layout for transcript output packets?
2. **Token Budgets**: How should the 35K token limit be allocated across different artifact types?
3. **Naming Conventions**: What naming scheme ensures clarity and navigation?
4. **Index/Manifest**: How should the packet be indexed for navigation?

**Research Required:**
- Review EN-003 Requirements (NFR-001: 35K token limit)
- Review Chroma Context Rot research on optimal document sizes
- Research Claude best practices for structured document output
- Analyze competitor patterns (EN-001) for artifact organization

### Acceptance Criteria

- [ ] ADR-002 created in `docs/adrs/ADR-002-artifact-structure.md`
- [ ] Uses template from `docs/knowledge/exemplars/templates/adr.md`
- [ ] Context section documents the token limit constraint
- [ ] At least 3 directory structure options considered
- [ ] Token budget allocation table provided
- [ ] Naming convention specification included
- [ ] Decision section with clear rationale
- [ ] ps-critic review integrated via feedback loop

### Implementation Notes

**Process:**
1. Use @problem-solving skill with ps-researcher agent for deep research
2. Analyze EN-003 NFR-001 (35K token limit requirement)
3. Use ps-architect agent to draft ADR with options
4. Use ps-critic agent for feedback loop and revision
5. Persist final ADR to `docs/adrs/ADR-002-artifact-structure.md`

**Key References:**
- EN-003 Requirements: NFR-001 (35K token budget)
- Chroma Research: Context Rot phenomenon
- DEC-005: Token limit decision (35K per artifact)

**Proposed Directory Structure (from FEAT-002):**
```
{session-id}-transcript-output/
├── 00-index.md                    # Manifest with all links
├── 01-summary.md                  # Executive summary (<5K tokens)
├── 02-speakers/
│   └── speakers.md                # Speaker profiles
├── 03-topics/
│   ├── topics.md                  # Topic index
│   └── topics-detail-001.md       # Split if >35K tokens
├── 04-entities/
│   ├── questions.md
│   ├── action-items.md
│   ├── ideas.md
│   └── decisions.md
├── 05-timeline/
│   └── timeline.md                # Chronological view
├── 06-analysis/
│   └── sentiment.md               # If applicable
├── 07-mindmap/
│   ├── mindmap.mmd                # Mermaid source
│   └── mindmap.ascii.txt          # ASCII rendering
└── 08-workitems/
    └── suggested-tasks.md         # For worktracker integration
```

### Related Items

- Parent: [EN-004: Architecture Decision Records](./EN-004-architecture-decisions.md)
- Related: [EN-003: Requirements Synthesis](../EN-003-requirements-synthesis/EN-003-requirements-synthesis.md)
- Output: [ADR-002: Artifact Structure](../../../../../docs/adrs/ADR-002-artifact-structure.md)
- Depends On: ADR-001 (Agent Architecture)

---

## Time Tracking

| Metric            | Value           |
|-------------------|-----------------|
| Original Estimate | 4 hours         |
| Remaining Work    | 4 hours         |
| Time Spent        | 0 hours         |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ADR-002 | Architecture Decision Record | [ADR-002-artifact-structure.md](../../../../../docs/adrs/ADR-002-artifact-structure.md) |
| Research Artifact | Problem-Solving Output | TBD |

### Verification

- [ ] Acceptance criteria verified
- [ ] ADR follows template structure
- [ ] Token budget allocation documented
- [ ] Directory structure specified
- [ ] ps-critic review completed
- [ ] Reviewed by: Human (GATE-3)

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Initial creation from template |

---

<!--
JERRY ALIGNMENT:
  existing_type: "WorkType.TASK"
  changes_needed: "None - already exists"
-->
