# TASK-005: Create ts-parser AGENT.md

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-005"
work_type: TASK

# === CORE METADATA ===
title: "Create ts-parser AGENT.md"
description: |
  Create the ts-parser agent definition file following PS_AGENT_TEMPLATE.md.
  This is the prompt-based agent definition for Phase 1 (per ADR-005).

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: DONE
resolution: completed
relocation_note: |
  RELOCATED per DISC-004 and DEC-002 (2026-01-26):
  Implementation artifact moved to: skills/transcript/agents/ts-parser.md
  This task file documents design intent. Executable implementation now in skills/ folder.

# === PRIORITY ===
priority: MEDIUM

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
  - "agent"
  - "ts-parser"
  - "phase-2"

# === DELIVERY ITEM PROPERTIES ===
effort: 1
acceptance_criteria: |
  See Acceptance Criteria section below
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DESIGN
original_estimate: 2
remaining_work: 2
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

Create the ts-parser agent definition following the PS_AGENT_TEMPLATE.md structure. This is a prompt-based agent for Phase 1 implementation per ADR-005.

**Agent Responsibilities:**
- Parse VTT, SRT, TXT transcript formats
- Detect format automatically
- Normalize timestamps to milliseconds
- Output canonical JSON structure
- Handle errors gracefully

**Key Design Decisions (from DEC-001-005):**
- Follow PS_AGENT_TEMPLATE.md structure
- Use XML tags: `<agent>`, `<identity>`, `<capabilities>`, `<processing_instructions>`
- Model selection: haiku (fast parsing, low cost)
- Output persistence to canonical JSON

### Acceptance Criteria

- [x] **AC-001:** Follows PS_AGENT_TEMPLATE.md structure exactly
- [x] **AC-002:** YAML frontmatter with identity, capabilities, guardrails
- [x] **AC-003:** XML tags present: `<agent>`, `<identity>`, `<capabilities>`, `<processing_instructions>`
- [x] **AC-004:** Model selection: haiku (fast parsing)
- [x] **AC-005:** Input validation rules documented
- [x] **AC-006:** Output format specification (canonical JSON)
- [x] **AC-007:** Error handling instructions included
- [x] **AC-008:** Constitutional compliance: P-002 (file persistence), P-003 (no subagents)
- [x] **AC-009:** File created at `agents/ts-parser/AGENT.md` → RELOCATED to `skills/transcript/agents/ts-parser.md`
- [x] **AC-010:** Template compliance verified by review

### Dependencies

| Type | Item | Status |
|------|------|--------|
| Blocked By | TASK-002 TDD ts-parser | PENDING |
| Parallel | TASK-006 ts-extractor AGENT.md | Can run parallel |
| Parallel | TASK-007 ts-formatter AGENT.md | Can run parallel |
| Enables | TASK-008 SKILL.md | Requires all agents defined |

### Implementation Notes

**Template Location:** `skills/problem-solving/agents/PS_AGENT_TEMPLATE.md`

**Agent Structure:**
```markdown
# ts-parser Agent

> Version: 1.0.0
> Role: Transcript Parser
> Constitutional Compliance: P-002, P-003

## YAML Frontmatter
```yaml
identity:
  name: "ts-parser"
  version: "1.0.0"
  model: "haiku"

capabilities:
  - "VTT parsing"
  - "SRT parsing"
  - "TXT parsing"
  - "Format detection"
  - "Timestamp normalization"

guardrails:
  - "P-002: All output persisted to files"
  - "P-003: No recursive subagents"
```

## System Prompt
<agent>
  <identity>ts-parser v1.0.0</identity>
  <capabilities>...</capabilities>
  <processing_instructions>...</processing_instructions>
</agent>
```

### Related Items

- Parent: [EN-005 Design Documentation](./EN-005-design-documentation.md)
- Depends On: [TASK-002 TDD ts-parser](./TASK-002-tdd-ts-parser.md)
- Reference: [ADR-005 Agent Implementation](../../docs/adrs/ADR-005-agent-implementation.md)

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

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| ts-parser AGENT.md | Agent Definition | ~~agents/ts-parser/AGENT.md~~ → **skills/transcript/agents/ts-parser.md** | RELOCATED |

### Verification

- [x] Acceptance criteria verified
- [x] Template compliance checked
- [x] XML structure validated
- [x] Reviewed by: ps-critic (Quality Score: 0.93)

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Initial task creation          |
| 2026-01-26 | DONE        | Agent definition created        |
| 2026-01-26 | RELOCATED   | Moved to skills/transcript/agents/ts-parser.md per DISC-004, DEC-002 |

---

*Task ID: TASK-005*
*Workflow ID: en005-tdd-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance)*
