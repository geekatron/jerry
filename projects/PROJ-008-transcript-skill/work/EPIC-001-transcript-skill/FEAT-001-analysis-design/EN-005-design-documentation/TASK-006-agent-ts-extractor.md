# TASK-006: Create ts-extractor AGENT.md

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-006"
work_type: TASK

# === CORE METADATA ===
title: "Create ts-extractor AGENT.md"
description: |
  Create the ts-extractor agent definition file following PS_AGENT_TEMPLATE.md.
  This is the most complex agent handling semantic entity extraction.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: DONE
resolution: completed

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
  - "ts-extractor"
  - "phase-2"

# === DELIVERY ITEM PROPERTIES ===
effort: 1
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

Create the ts-extractor agent definition for semantic entity extraction. This is the most complex agent requiring careful prompt engineering for:
- Speaker identification with multi-pattern detection
- Action item extraction with confidence scoring
- Decision recognition
- Question extraction
- Topic segmentation

**Key Design Decisions (from DEC-001-005):**
- Follow PS_AGENT_TEMPLATE.md structure
- Model selection: sonnet (complex NER tasks require reasoning)
- Tiered extraction documented in prompts
- Citation format matches ADR-003

### Acceptance Criteria

- [ ] **AC-001:** Follows PS_AGENT_TEMPLATE.md structure exactly
- [ ] **AC-002:** YAML frontmatter with identity, capabilities, guardrails
- [ ] **AC-003:** Entity extraction prompts for all types (speakers, actions, decisions, questions, topics)
- [ ] **AC-004:** Confidence scoring instructions (0.0-1.0 scale)
- [ ] **AC-005:** Citation format requirements per ADR-003
- [ ] **AC-006:** Quality thresholds defined (0.7 default confidence)
- [ ] **AC-007:** Tiered extraction logic documented (rule → ML → LLM)
- [ ] **AC-008:** Model selection: sonnet (complex NER)
- [ ] **AC-009:** File created at `agents/ts-extractor/AGENT.md`
- [ ] **AC-010:** Sample extraction output validated

### Dependencies

| Type | Item | Status |
|------|------|--------|
| Blocked By | TASK-003 TDD ts-extractor | PENDING |
| Parallel | TASK-005 ts-parser AGENT.md | Can run parallel |
| Parallel | TASK-007 ts-formatter AGENT.md | Can run parallel |
| Enables | TASK-008 SKILL.md | Requires all agents defined |

### Implementation Notes

**Key Prompting Strategies:**
1. **Structured Output:** Use JSON schemas in prompt
2. **Few-Shot Examples:** Include extraction examples
3. **Confidence Calibration:** Instructions for scoring confidence
4. **Citation Requirements:** Mandate source references

**Agent Structure:**
```markdown
# ts-extractor Agent

> Version: 1.0.0
> Role: Entity Extractor
> Constitutional Compliance: P-002, P-003, P-004

## YAML Frontmatter
```yaml
identity:
  name: "ts-extractor"
  version: "1.0.0"
  model: "sonnet"

capabilities:
  - "Speaker identification"
  - "Action item extraction"
  - "Decision recognition"
  - "Question extraction"
  - "Topic segmentation"
  - "Confidence scoring"

guardrails:
  - "P-002: All output persisted"
  - "P-003: No subagents"
  - "P-004: Citation required for all extractions"

quality_thresholds:
  confidence_minimum: 0.7
  precision_target: 0.85
  recall_target: 0.85
```

### Related Items

- Parent: [EN-005 Design Documentation](./EN-005-design-documentation.md)
- Depends On: [TASK-003 TDD ts-extractor](./TASK-003-tdd-ts-extractor.md)
- Reference: [ADR-003 Bidirectional Linking](../../docs/adrs/ADR-003-bidirectional-linking.md)
- Reference: [ADR-005 Agent Implementation](../../docs/adrs/ADR-005-agent-implementation.md)

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
| ts-extractor AGENT.md | Agent Definition | agents/ts-extractor/AGENT.md | PENDING |

### Verification

- [ ] Acceptance criteria verified
- [ ] Template compliance checked
- [ ] Sample extraction output validated
- [ ] Reviewed by: TBD

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-26 | Created     | Initial task creation          |

---

*Task ID: TASK-006*
*Workflow ID: en005-tdd-20260126-001*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance)*
