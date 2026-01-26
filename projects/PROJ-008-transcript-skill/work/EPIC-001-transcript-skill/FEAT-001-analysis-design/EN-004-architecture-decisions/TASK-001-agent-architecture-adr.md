# TASK-001: Create ADR-001 - Agent Architecture

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
id: "TASK-001"                           # Enabler-scoped ID
work_type: TASK                          # Immutable discriminator

# === CORE METADATA ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
title: "Create ADR-001: Agent Architecture"
description: |
  Research and create Architecture Decision Record for the Transcript Skill
  agent architecture. Define custom agents vs existing Jerry agents, agent
  responsibilities and boundaries, and inter-agent communication patterns.

# === CLASSIFICATION ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
classification: ENABLER                  # Architecture enabler work

# === LIFECYCLE STATE ===
# Source: ONTOLOGY-v1.md Section 3.4.6 (Task state_machine)
status: BACKLOG                          # See State Machine below
resolution: null                         # Set when status is DONE or REMOVED

# === PRIORITY ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
priority: HIGH                           # Critical path for implementation

# === PEOPLE ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
assignee: "ps-architect"                 # Primary agent
created_by: "Claude"                     # Auto-set on creation

# === TIMESTAMPS (Auto-managed) ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
created_at: "2026-01-26T00:00:00Z"       # ISO 8601 datetime
updated_at: "2026-01-26T00:00:00Z"       # ISO 8601 datetime

# === HIERARCHY ===
# Source: ONTOLOGY-v1.md Section 3.4.6 (Task containment)
parent_id: "EN-004"                      # Parent Enabler

# === TAGS ===
# Source: ONTOLOGY-v1.md Section 3.3.1 (WorkItem)
tags:
  - "architecture"
  - "adr"
  - "agent-design"
  - "transcript-skill"

# === DELIVERY ITEM PROPERTIES ===
# Source: ONTOLOGY-v1.md Section 3.3.2 (DeliveryItem)
effort: 2                                # Story points
acceptance_criteria: |
  - ADR-001 created using docs/knowledge/exemplars/templates/adr.md
  - Context section with problem statement
  - At least 3 options considered with pros/cons
  - Decision with rationale
  - Consequences documented
  - References to EN-003 requirements
due_date: null                           # ISO 8601 date

# === TASK-SPECIFIC PROPERTIES ===
# Source: ONTOLOGY-v1.md Section 3.4.6 (Task.specific)
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

Create Architecture Decision Record (ADR-001) for the Transcript Skill agent architecture. This ADR will define the foundational agent structure that all subsequent implementation work will follow.

**Key Decisions Required:**
1. **Custom vs Existing**: Should we create new custom agents or extend existing Jerry agents (ps-researcher, ps-analyst, etc.)?
2. **Agent Boundaries**: What are the clear responsibilities of each agent?
3. **Communication Patterns**: How do agents communicate and share data?
4. **Orchestration Model**: How is the agent workflow orchestrated?

**Research Required:**
- Review EN-001 Market Analysis (competitor agent patterns)
- Review EN-002 Technical Standards (Claude Code skill architecture)
- Review EN-003 Requirements Specification (agent-related requirements)
- Research industry best practices for agent architecture

### Acceptance Criteria

- [ ] ADR-001 created in `docs/adrs/ADR-001-agent-architecture.md`
- [ ] Uses template from `docs/knowledge/exemplars/templates/adr.md`
- [ ] Context section documents the problem and constraints
- [ ] At least 3 options considered with pros/cons analysis
- [ ] Decision section with clear rationale
- [ ] Consequences section (positive, negative, neutral)
- [ ] References to supporting research (EN-001, EN-002, EN-003)
- [ ] ps-critic review integrated via feedback loop

### Implementation Notes

**Process:**
1. Use @problem-solving skill with ps-researcher agent for deep research
2. Use ps-architect agent to synthesize options and draft ADR
3. Use ps-critic agent for feedback loop and revision
4. Persist final ADR to `docs/adrs/ADR-001-agent-architecture.md`

**Key References:**
- EN-001 Market Analysis: Speaker identification, entity extraction patterns
- EN-002 Technical Standards: Claude Code skill architecture (SKILL.yaml, agents/)
- EN-003 Requirements: FR-001 through FR-010, NFR-001 through NFR-007

### Related Items

- Parent: [EN-004: Architecture Decision Records](./EN-004-architecture-decisions.md)
- Related: [EN-003: Requirements Synthesis](../EN-003-requirements-synthesis/EN-003-requirements-synthesis.md)
- Output: [ADR-001: Agent Architecture](../../../../../docs/adrs/ADR-001-agent-architecture.md)

---

## Time Tracking

| Metric            | Value           |
|-------------------|-----------------|
| Original Estimate | 4 hours         |
| Remaining Work    | 4 hours         |
| Time Spent        | 0 hours         |

---

## Evidence

<!--
COMPLETION EVIDENCE: Verification that this task was completed correctly.
Link to deliverables and verify acceptance criteria were met.
This is audit trail evidence (proving work was done), not knowledge evidence (research citations).
-->

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ADR-001 | Architecture Decision Record | [ADR-001-agent-architecture.md](../../../../../docs/adrs/ADR-001-agent-architecture.md) |
| Research Artifact | Problem-Solving Output | TBD |

### Verification

- [ ] Acceptance criteria verified
- [ ] ADR follows template structure
- [ ] All 3+ options documented with pros/cons
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

DESIGN RATIONALE:
  Task is universally agreed across all systems. No translation needed.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.1
-->
