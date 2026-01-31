# TASK-004: Create ADR-004 - File Splitting Strategy

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
id: "TASK-004"                           # Enabler-scoped ID
work_type: TASK                          # Immutable discriminator

# === CORE METADATA ===
title: "Create ADR-004: File Splitting Strategy"
description: |
  Research and create Architecture Decision Record for the Transcript Skill
  file splitting strategy. Define when to split large artifacts, naming
  conventions for split files, and cross-reference handling.

# === CLASSIFICATION ===
classification: ENABLER                  # Architecture enabler work

# === LIFECYCLE STATE ===
status: BACKLOG                          # See State Machine below
resolution: null                         # Set when status is DONE or REMOVED

# === PRIORITY ===
priority: MEDIUM                         # Important but not blocking

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
  - "file-splitting"
  - "token-management"
  - "transcript-skill"

# === DELIVERY ITEM PROPERTIES ===
effort: 1                                # Story points
acceptance_criteria: |
  - ADR-004 created using docs/knowledge/exemplars/templates/adr.md
  - Split trigger criteria defined (token count thresholds)
  - Naming convention for split files documented
  - Cross-reference handling specified
  - Index/navigation for split files documented
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

Create Architecture Decision Record (ADR-004) for file splitting strategy when transcript artifacts exceed the 35K token limit. This ADR ensures large artifacts are split in a predictable, navigable manner.

**Key Decisions Required:**
1. **Split Trigger**: At what token count should files be split?
2. **Split Boundary**: How to determine natural split points (by topic, by time, by count)?
3. **Naming Convention**: How are split files named (e.g., `topics-001.md`, `topics-002.md`)?
4. **Navigation**: How do users navigate between split files?
5. **Cross-References**: How are cross-references updated when files split?

**Research Required:**
- Review NFR-001 (35K token limit)
- Research pagination patterns in documentation systems
- Analyze how large knowledge bases handle file splitting
- Review Context Rot research for optimal document sizes

### Acceptance Criteria

- [ ] ADR-004 created in `docs/adrs/ADR-004-file-splitting.md`
- [ ] Uses template from `docs/knowledge/exemplars/templates/adr.md`
- [ ] Split trigger threshold documented (e.g., 30K tokens for 35K limit)
- [ ] Natural split boundary rules defined
- [ ] Naming convention for split files specified
- [ ] Navigation patterns between split files documented
- [ ] ps-critic review integrated via feedback loop

### Implementation Notes

**Process:**
1. Use @problem-solving skill with ps-researcher agent
2. Research file splitting patterns in large documentation systems
3. Use ps-architect agent to draft ADR with options
4. Use ps-critic agent for feedback loop and revision
5. Persist final ADR to `docs/adrs/ADR-004-file-splitting.md`

**Key References:**
- NFR-001: 35K token limit per artifact
- ADR-002: Artifact Structure (dependency)
- ADR-003: Bidirectional Linking (for cross-references)

**Example Splitting Patterns:**
```
# Before Split
topics.md (45K tokens - exceeds limit)

# After Split
topics.md (index, 2K tokens)
├── topics-001.md (28K tokens)
├── topics-002.md (15K tokens)

# topics.md becomes index:
# Topics Index
This document is split into multiple parts:
- [Topics Part 1](topics-001.md) - Topics 1-15
- [Topics Part 2](topics-002.md) - Topics 16-23
```

### Related Items

- Parent: [EN-004: Architecture Decision Records](./EN-004-architecture-decisions.md)
- Output: [ADR-004: File Splitting](../../../../../docs/adrs/ADR-004-file-splitting.md)
- Depends On: ADR-002 (Artifact Structure), ADR-003 (Bidirectional Linking)

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
| ADR-004 | Architecture Decision Record | [ADR-004-file-splitting.md](../../../../../docs/adrs/ADR-004-file-splitting.md) |
| Research Artifact | Problem-Solving Output | TBD |

### Verification

- [ ] Acceptance criteria verified
- [ ] ADR follows template structure
- [ ] Split thresholds documented
- [ ] Navigation patterns specified
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
