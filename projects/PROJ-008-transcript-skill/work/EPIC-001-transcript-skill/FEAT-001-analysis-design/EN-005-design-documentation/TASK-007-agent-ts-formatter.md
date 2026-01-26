# TASK-007: Create ts-formatter AGENT.md

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-007"
work_type: TASK

# === CORE METADATA ===
title: "Create ts-formatter AGENT.md"
description: |
  Create the ts-formatter agent definition file following PS_AGENT_TEMPLATE.md.
  This agent handles output generation, file splitting, and anchor management.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: DONE
resolution: completed
relocation_note: |
  RELOCATED per DISC-004 and DEC-002 (2026-01-26):
  Implementation artifact moved to: skills/transcript/agents/ts-formatter.md
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
  - "ts-formatter"
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

Create the ts-formatter agent definition for output generation. This agent implements the most ADR decisions:
- ADR-002: Hierarchical packet structure
- ADR-003: Anchor registry and backlinks
- ADR-004: File splitting at semantic boundaries

**Agent Responsibilities:**
- Generate Markdown output in packet structure
- Count tokens and split files at boundaries
- Manage anchor registry
- Generate backlinks sections
- Create navigation index

### Acceptance Criteria

- [ ] **AC-001:** Follows PS_AGENT_TEMPLATE.md structure exactly
- [ ] **AC-002:** Output generation instructions for packet structure
- [ ] **AC-003:** Token counting procedures documented
- [ ] **AC-004:** Split decision logic per ADR-004
- [ ] **AC-005:** Anchor registry management per ADR-003
- [ ] **AC-006:** Backlinks generation template
- [ ] **AC-007:** Model selection: sonnet (formatting quality)
- [ ] **AC-008:** Constitutional compliance: P-002 (file persistence)
- [ ] **AC-009:** File created at `agents/ts-formatter/AGENT.md`
- [ ] **AC-010:** Sample output validated against ADR-002

### Dependencies

| Type | Item | Status |
|------|------|--------|
| Blocked By | TASK-004 TDD ts-formatter | PENDING |
| Parallel | TASK-005 ts-parser AGENT.md | Can run parallel |
| Parallel | TASK-006 ts-extractor AGENT.md | Can run parallel |
| Enables | TASK-008 SKILL.md | Requires all agents defined |

### Implementation Notes

**Key ADR Implementations:**

**ADR-002 Packet Structure:**
```yaml
packet_files:
  - "00-index.md"       # Navigation hub
  - "01-summary.md"     # Executive summary
  - "02-transcript.md"  # Full transcript (may split)
  - "03-speakers.md"    # Speaker directory
  - "04-action-items.md"
  - "05-decisions.md"
  - "06-questions.md"
  - "07-topics.md"
```

**ADR-003 Anchor Format:**
```markdown
<!-- Anchor definition -->
<a id="speaker-001">John Smith</a>

<!-- Backlink reference -->
See [John Smith](#speaker-001)

<!-- Backlinks section -->
## Backlinks

Referenced by:
- [02-transcript.md#line-42](./02-transcript.md#line-42)
- [04-action-items.md#action-003](./04-action-items.md#action-003)
```

**ADR-004 Split Logic:**
```yaml
token_limits:
  hard_limit: 35000
  soft_limit: 31500  # 90% of hard
  warning_threshold: 28000  # 80% of hard

split_strategy:
  boundary: "## heading"
  fallback: "force_split_at_hard_limit"
```

### Related Items

- Parent: [EN-005 Design Documentation](./EN-005-design-documentation.md)
- Depends On: [TASK-004 TDD ts-formatter](./TASK-004-tdd-ts-formatter.md)
- Reference: [ADR-002 Artifact Structure](../../docs/adrs/ADR-002-artifact-structure.md)
- Reference: [ADR-003 Bidirectional Linking](../../docs/adrs/ADR-003-bidirectional-linking.md)
- Reference: [ADR-004 File Splitting](../../docs/adrs/ADR-004-file-splitting.md)

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
| ts-formatter AGENT.md | Agent Definition | ~~agents/ts-formatter/AGENT.md~~ → **skills/transcript/agents/ts-formatter.md** | RELOCATED |

### Verification

- [ ] Acceptance criteria verified
- [ ] Sample output validated
- [ ] ADR compliance verified
- [ ] Reviewed by: TBD

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Initial task creation          |
| 2026-01-26 | DONE        | Agent definition created        |
| 2026-01-26 | RELOCATED   | Moved to skills/transcript/agents/ts-formatter.md per DISC-004, DEC-002 |

---

*Task ID: TASK-007*
*Workflow ID: en005-tdd-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance)*
