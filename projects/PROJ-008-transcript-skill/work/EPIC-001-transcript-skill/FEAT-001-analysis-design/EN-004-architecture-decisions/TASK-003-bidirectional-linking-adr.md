# TASK-003: Create ADR-003 - Bidirectional Deep Linking

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
id: "TASK-003"                           # Enabler-scoped ID
work_type: TASK                          # Immutable discriminator

# === CORE METADATA ===
title: "Create ADR-003: Bidirectional Deep Linking"
description: |
  Research and create Architecture Decision Record for the Transcript Skill
  bidirectional deep linking strategy. Define link format specification,
  backlinks section structure, and anchor generation rules.

# === CLASSIFICATION ===
classification: ENABLER                  # Architecture enabler work

# === LIFECYCLE STATE ===
status: BACKLOG                          # See State Machine below
resolution: null                         # Set when status is DONE or REMOVED

# === PRIORITY ===
priority: HIGH                           # Critical for traceability

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
  - "deep-linking"
  - "backlinks"
  - "traceability"
  - "transcript-skill"

# === DELIVERY ITEM PROPERTIES ===
effort: 1                                # Story points
acceptance_criteria: |
  - ADR-003 created using docs/knowledge/exemplars/templates/adr.md
  - Link format specification defined
  - Backlinks section structure documented
  - Anchor generation rules specified
  - Cross-artifact navigation patterns documented
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

Create Architecture Decision Record (ADR-003) for bidirectional deep linking between transcript artifacts. This ADR ensures all artifacts maintain traceability back to source material and forward to derived insights.

**Key Decisions Required:**
1. **Link Format**: What format should links use (markdown, wiki-style, custom)?
2. **Anchor Generation**: How are unique anchors generated for linkable elements?
3. **Backlinks Section**: Where and how are backlinks maintained?
4. **Cross-Artifact Links**: How do links work across different artifact files?

**Research Required:**
- Review DEC-004 (Bidirectional linking with backlinks decision)
- Research Obsidian/Roam-style backlinks patterns
- Analyze Zettelkasten linking methodology
- Review GitHub/GitLab linking conventions

### Acceptance Criteria

- [ ] ADR-003 created in `docs/adrs/ADR-003-bidirectional-linking.md`
- [ ] Uses template from `docs/knowledge/exemplars/templates/adr.md`
- [ ] Link format specification documented
- [ ] Anchor ID generation rules defined
- [ ] Backlinks section structure specified
- [ ] Examples provided for all link types
- [ ] ps-critic review integrated via feedback loop

### Implementation Notes

**Process:**
1. Use @problem-solving skill with ps-researcher agent
2. Research existing linking patterns (Obsidian, Roam, Zettelkasten)
3. Use ps-architect agent to draft ADR with options
4. Use ps-critic agent for feedback loop and revision
5. Persist final ADR to `docs/adrs/ADR-003-bidirectional-linking.md`

**Key References:**
- DEC-004: Bidirectional linking with backlinks (EPIC-001 decision)
- Obsidian backlinks documentation
- Zettelkasten method

**Example Link Patterns:**
```markdown
<!-- Forward Link -->
See [Speaker Profile: John Smith](02-speakers/speakers.md#speaker-john-smith)

<!-- Backlinks Section (auto-generated) -->
## Backlinks
- Referenced by: [03-topics/topics.md#topic-001](03-topics/topics.md#topic-001)
- Referenced by: [04-entities/action-items.md#action-001](04-entities/action-items.md#action-001)

<!-- Anchor Definition -->
### Topic 001: Project Planning {#topic-001}
```

### Related Items

- Parent: [EN-004: Architecture Decision Records](./EN-004-architecture-decisions.md)
- Related: [DEC-004: Bidirectional Linking Decision](../../EPIC-001-transcript-skill.md)
- Output: [ADR-003: Bidirectional Linking](../../../../../docs/adrs/ADR-003-bidirectional-linking.md)
- Depends On: ADR-002 (Artifact Structure)

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
| ADR-003 | Architecture Decision Record | [ADR-003-bidirectional-linking.md](../../../../../docs/adrs/ADR-003-bidirectional-linking.md) |
| Research Artifact | Problem-Solving Output | TBD |

### Verification

- [ ] Acceptance criteria verified
- [ ] ADR follows template structure
- [ ] Link format examples provided
- [ ] Backlinks structure documented
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
