# TASK-005: Create ADR-005 - Agent Implementation Approach

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
id: "TASK-005"                           # Enabler-scoped ID
work_type: TASK                          # Immutable discriminator

# === CORE METADATA ===
title: "Create ADR-005: Agent Implementation Approach"
description: |
  Research and create Architecture Decision Record for the Transcript Skill
  agent implementation approach. Define phased strategy: prompt-based first,
  Python-based if needed, and migration path between phases.

# === CLASSIFICATION ===
classification: ENABLER                  # Architecture enabler work

# === LIFECYCLE STATE ===
status: BACKLOG                          # See State Machine below
resolution: null                         # Set when status is DONE or REMOVED

# === PRIORITY ===
priority: HIGH                           # Critical for implementation strategy

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
  - "implementation-strategy"
  - "prompt-based"
  - "python-based"
  - "transcript-skill"

# === DELIVERY ITEM PROPERTIES ===
effort: 1                                # Story points
acceptance_criteria: |
  - ADR-005 created using docs/knowledge/exemplars/templates/adr.md
  - Phase 1 (prompt-based) approach documented
  - Phase 2 (Python-based) criteria defined
  - Migration path between phases specified
  - Trade-offs between approaches analyzed
due_date: null                           # ISO 8601 date

# === TASK-SPECIFIC PROPERTIES ===
activity: DESIGN                         # Architecture design work
original_estimate: 2                     # Initial time estimate in hours
remaining_work: 2                        # Remaining effort in hours
time_spent: 0                            # Actual time logged in hours
```

---

## State Machine

**Initial State:** `BACKLOG`

**Valid States:** `BACKLOG`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `REMOVED`

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

Create Architecture Decision Record (ADR-005) for the phased agent implementation approach. This ADR defines whether to start with prompt-based agents (YAML/MD) or Python-based agents, and the criteria for transitioning between approaches.

**Key Decisions Required:**
1. **Phase 1 Approach**: What does prompt-based implementation look like?
2. **Phase 2 Triggers**: When should we move to Python-based agents?
3. **Migration Path**: How do we migrate from prompt to Python?
4. **Hybrid Model**: Can we mix both approaches?

**Research Required:**
- Review DEC-006 (Phased agents decision)
- Review EN-002 Technical Standards (Claude Code skill architecture)
- Research existing Jerry agent implementations
- Analyze prompt engineering best practices vs Python tooling

### Acceptance Criteria

- [ ] ADR-005 created in `docs/adrs/ADR-005-agent-implementation.md`
- [ ] Uses template from `docs/knowledge/exemplars/templates/adr.md`
- [ ] Phase 1 (prompt-based) structure documented
- [ ] Phase 2 trigger criteria specified
- [ ] Migration path documented
- [ ] Trade-off analysis between approaches
- [ ] ps-critic review integrated via feedback loop

### Implementation Notes

**Process:**
1. Use @problem-solving skill with ps-researcher agent
2. Review Claude Code skill architecture research (EN-002)
3. Use ps-architect agent to draft ADR with options
4. Use ps-critic agent for feedback loop and revision
5. Persist final ADR to `docs/adrs/ADR-005-agent-implementation.md`

**Key References:**
- DEC-006: Phased agents decision (Prompt-based first, Python later)
- EN-002 Technical Standards: Claude Code skill architecture
- SKILL.yaml specification from research
- Existing Jerry agents (ps-researcher, ps-analyst, etc.)

**Phase 1 Structure (from FEAT-002):**
```yaml
skills/transcript/agents/
├── vtt-parser/
│   ├── AGENT.md           # Agent definition
│   └── prompts/
│       └── parse-vtt.md   # Prompt template
├── entity-extractor/
│   ├── AGENT.md
│   └── prompts/
│       ├── extract-speakers.md
│       ├── extract-topics.md
│       ├── extract-questions.md
│       └── extract-actions.md
└── mindmap-generator/
    ├── AGENT.md
    └── prompts/
        └── generate-mindmap.md
```

**Phase 2 Triggers:**
- Prompt-based approach cannot handle edge cases
- Performance requirements exceed prompt capabilities
- Need for complex state management
- Integration requirements beyond prompt scope

### Related Items

- Parent: [EN-004: Architecture Decision Records](./EN-004-architecture-decisions.md)
- Related: [DEC-006: Phased Agents Decision](../../EPIC-001-transcript-skill.md)
- Related: [EN-002: Technical Standards](../EN-002-technical-standards/EN-002-technical-standards.md)
- Output: [ADR-005: Agent Implementation](../../../../../docs/adrs/ADR-005-agent-implementation.md)
- Depends On: ADR-001 (Agent Architecture)

---

## Time Tracking

| Metric            | Value           |
|-------------------|-----------------|
| Original Estimate | 2 hours         |
| Remaining Work    | 2 hours         |
| Time Spent        | 0 hours         |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ADR-005 | Architecture Decision Record | [ADR-005-agent-implementation.md](../../../../../docs/adrs/ADR-005-agent-implementation.md) |
| Research Artifact | Problem-Solving Output | TBD |

### Verification

- [ ] Acceptance criteria verified
- [ ] ADR follows template structure
- [ ] Phase 1 approach documented
- [ ] Phase 2 triggers specified
- [ ] Migration path defined
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
