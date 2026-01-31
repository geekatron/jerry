# TASK-008: Create SKILL.md Orchestrator

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-008"
work_type: TASK

# === CORE METADATA ===
title: "Create SKILL.md Orchestrator"
description: |
  Create the main SKILL.md entry point that orchestrates all 3 custom agents
  (ts-parser, ts-extractor, ts-formatter) and integrates ps-critic for quality review.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: DONE
resolution: completed
relocation_note: |
  RELOCATED per DISC-004 and DEC-002 (2026-01-26):
  Implementation artifact moved to: skills/transcript/SKILL.md
  This task file documents design intent. Executable implementation now in skills/ folder.

# === PRIORITY ===
priority: HIGH

# === PEOPLE ===
assignee: "ps-architect"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"

# === HIERARCHY ===
parent_id: "EN-005"

# === TAGS ===
tags:
  - "skill"
  - "orchestrator"
  - "phase-2"

# === DELIVERY ITEM PROPERTIES ===
effort: 2
acceptance_criteria: |
  See Acceptance Criteria section below
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DESIGN
original_estimate: 3
remaining_work: 3
time_spent: 0
```

---

## State Machine

**Initial State:** `BACKLOG`

**Valid States:** `BACKLOG`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `REMOVED`

---

## Containment Rules

| Rule             | Value                           |
|------------------|---------------------------------|
| Allowed Children | Subtask                         |
| Allowed Parents  | Enabler                         |
| Max Depth        | 1                               |

---

## Content

### Description

Create the SKILL.md that serves as the entry point for the Transcript Skill. This is the orchestrator that:
1. Receives transcript input from Claude Code
2. Invokes agents in sequence: ts-parser → ts-extractor → ts-formatter
3. Integrates ps-critic for quality gate
4. Handles errors and recovery
5. Maintains P-003 single nesting compliance

**ADR-001 Architecture:**
```
Claude Code (User)
       │
       ▼
  ┌─────────────┐
  │  SKILL.md   │ ◄── Entry point (this task)
  │ Orchestrator│
  └──────┬──────┘
         │
    ┌────┴────┬────────────┐
    ▼         ▼            ▼
┌────────┐ ┌────────┐ ┌────────┐
│ts-parser│ │ts-extractor│ │ts-formatter│
└────────┘ └────────┘ └────────┘
         │
    ┌────┴────┐
    ▼
┌────────┐
│ps-critic│ ◄── Quality review
└────────┘
```

### Acceptance Criteria

- [x] **AC-001:** Follows Jerry SKILL.md conventions (see problem-solving skill)
- [x] **AC-002:** Invokes all 3 custom agents in correct sequence
- [x] **AC-003:** Integrates ps-critic for quality gate (>= 0.90)
- [x] **AC-004:** Maintains P-003 single nesting (orchestrator → workers only)
- [x] **AC-005:** Error handling and recovery documented
- [x] **AC-006:** Input validation for transcript formats
- [x] **AC-007:** Output path configuration
- [x] **AC-008:** L0/L1/L2 documentation for skill usage
- [x] **AC-009:** File created at `SKILL.md` → RELOCATED to `skills/transcript/SKILL.md`
- [x] **AC-010:** Agent flow documented with ASCII diagram

### Dependencies

| Type | Item | Status |
|------|------|--------|
| Blocked By | TASK-005 ts-parser AGENT.md | PENDING |
| Blocked By | TASK-006 ts-extractor AGENT.md | PENDING |
| Blocked By | TASK-007 ts-formatter AGENT.md | PENDING |
| Enables | TASK-009 PLAYBOOK | Requires skill definition |
| Enables | TASK-010 RUNBOOK | Requires skill definition |

### Implementation Notes

**Skill Interface:**
```markdown
# Transcript Skill

> Version: 1.0.0
> Type: Skill
> Constitutional Compliance: P-002, P-003, P-020

## Activation

Activate when user says:
- "analyze transcript"
- "process meeting notes"
- "/transcript <file>"

## Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| input_file | string | Yes | Path to transcript file |
| output_dir | string | No | Output directory (default: ./transcript-output/) |
| format | string | No | Force format (VTT, SRT, TXT) |

## Workflow

1. **Parse** - ts-parser extracts canonical JSON
2. **Extract** - ts-extractor identifies entities
3. **Format** - ts-formatter generates packet
4. **Review** - ps-critic validates quality
```

**P-003 Compliance:**
```
MAIN CONTEXT (Claude Code)
    │
    └──► SKILL.md Orchestrator
            │
            ├──► ts-parser (worker)
            ├──► ts-extractor (worker)
            ├──► ts-formatter (worker)
            └──► ps-critic (worker)

Each is a WORKER. None spawn other agents.
```

### Related Items

- Parent: [EN-005 Design Documentation](./EN-005-design-documentation.md)
- Depends On: [TASK-005 ts-parser AGENT.md](./TASK-005-agent-ts-parser.md)
- Depends On: [TASK-006 ts-extractor AGENT.md](./TASK-006-agent-ts-extractor.md)
- Depends On: [TASK-007 ts-formatter AGENT.md](./TASK-007-agent-ts-formatter.md)
- Reference: [ADR-001 Agent Architecture](../../docs/adrs/ADR-001-agent-architecture.md)

---

## Time Tracking

| Metric            | Value           |
|-------------------|-----------------|
| Original Estimate | 3 hours         |
| Remaining Work    | 3 hours         |
| Time Spent        | 0 hours         |

---

## Evidence

### Deliverables

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| SKILL.md | Skill Definition | ~~SKILL.md~~ → **skills/transcript/SKILL.md** | RELOCATED |

### Verification

- [x] Acceptance criteria verified
- [x] P-003 compliance validated
- [x] Agent flow tested
- [x] Reviewed by: ps-critic (Quality Score: 0.93)

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Initial task creation          |
| 2026-01-26 | DONE        | SKILL.md orchestrator created   |
| 2026-01-26 | RELOCATED   | Moved to skills/transcript/SKILL.md per DISC-004, DEC-002 |

---

*Task ID: TASK-008*
*Workflow ID: en005-tdd-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-003 (single nesting), P-004 (provenance)*
