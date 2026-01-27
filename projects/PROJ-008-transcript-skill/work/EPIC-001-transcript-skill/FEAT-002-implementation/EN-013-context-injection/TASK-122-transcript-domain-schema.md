# TASK-122: Create transcript.yaml Domain Schema

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-013 (Context Injection Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-122"
work_type: TASK
title: "Create transcript.yaml Domain Schema"
description: |
  Create the transcript.yaml domain schema file with transcript-specific
  entity definitions (action items, decisions, questions, speakers) per REQ-CI-F-007.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T19:00:00Z"
updated_at: "2026-01-26T19:00:00Z"

parent_id: "EN-013"

tags:
  - "implementation"
  - "context-injection"
  - "domain-schema"
  - "REQ-CI-F-007"

effort: 1
acceptance_criteria: |
  - transcript.yaml created in contexts/ folder
  - Entity definitions for action_item, decision, question, speaker
  - Extraction patterns with confidence thresholds
  - Domain-specific prompt_guidance
  - Validates against JSON Schema

due_date: null

activity: DEVELOPMENT
original_estimate: 2
remaining_work: 2
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Content

### Description

Create the transcript domain schema file (`transcript.yaml`) containing entity definitions specific to meeting transcripts: action items, decisions, questions, and speakers.

### File Location

```
skills/transcript/contexts/transcript.yaml
```

### Schema Structure

```yaml
# Domain Schema for Transcript Analysis
# Implements: REQ-CI-F-001, REQ-CI-F-007
schema_version: "1.0.0"
domain: "transcript"
display_name: "Transcript Analysis"

# Entity definitions (what to extract)
entity_definitions:
  action_item:
    description: "Task or commitment made during conversation"
    attributes:
      - name: "text"
        type: "string"
        required: true
      - name: "assignee"
        type: "string"
      - name: "due_date"
        type: "date"
      - name: "confidence"
        type: "float"
    extraction_patterns:
      - "{{assignee}} will {{text}}"
      - "{{assignee}}, can you {{text}}"
      - "action item: {{text}}"

  decision:
    description: "Decision made during conversation"
    attributes:
      - name: "text"
        type: "string"
        required: true
      - name: "decided_by"
        type: "string"
      - name: "rationale"
        type: "string"
    extraction_patterns:
      - "we've decided to {{text}}"
      - "the decision is {{text}}"
      - "let's go with {{text}}"

  question:
    description: "Question raised during conversation"
    attributes:
      - name: "text"
        type: "string"
        required: true
      - name: "asked_by"
        type: "string"
      - name: "answered"
        type: "boolean"

  speaker:
    description: "Person speaking in the transcript"
    attributes:
      - name: "name"
        type: "string"
        required: true
      - name: "role"
        type: "string"
      - name: "segment_count"
        type: "integer"

# Extraction rules (how to find entities)
extraction_rules:
  - id: "action_items"
    entity_type: "action_item"
    confidence_threshold: 0.7
    priority: 1
  - id: "decisions"
    entity_type: "decision"
    confidence_threshold: 0.8
    priority: 2
  - id: "questions"
    entity_type: "question"
    confidence_threshold: 0.75
    priority: 3

# Expert guidance for agent prompts
prompt_guidance: |
  When analyzing transcripts for entity extraction:

  1. **Action Items**: Look for commitments with specific owners and deadlines.
     Phrases like "will do", "by Friday", "I'll handle" indicate action items.

  2. **Decisions**: Identify explicit decisions with consensus language.
     Phrases like "we've decided", "let's go with", "agreed" indicate decisions.

  3. **Questions**: Track open questions and whether they were answered.
     Mark as answered if a response follows within the transcript.

  4. **Confidence Scoring**:
     - 0.9+ : Explicit indicator present ("action item:", "decision:")
     - 0.7-0.9: Strong implicit signal with context
     - 0.5-0.7: Ambiguous, flag for human review
     - <0.5: Do not extract
```

### Entity Mapping to Requirements

| Entity | Requirement | Description |
|--------|-------------|-------------|
| action_item | FR-006 | Action items with assignee/due date |
| decision | FR-007 | Decisions with rationale |
| question | FR-008 | Questions with answered status |
| speaker | PAT-003 | Speaker identification |

### Acceptance Criteria

- [ ] `contexts/transcript.yaml` file created
- [ ] `schema_version: "1.0.0"` present
- [ ] `domain: "transcript"` set
- [ ] 4 entity_definitions: action_item, decision, question, speaker
- [ ] Each entity has required attributes defined
- [ ] extraction_patterns for action_item and decision
- [ ] extraction_rules with confidence thresholds
- [ ] prompt_guidance with transcript-specific advice
- [ ] Validates against JSON Schema (TASK-124)
- [ ] YAML syntax valid

### Related Items

- Parent: [EN-013: Context Injection Implementation](./EN-013-context-injection.md)
- Blocked By: [TASK-120: SKILL.md context_injection section](./TASK-120-skill-context-injection.md)
- Blocks: [TASK-123: AGENT.md context sections](./TASK-123-agent-context-sections.md)
- References: [SPEC-context-injection.md Section 3.3](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md)
- References: REQ-CI-F-007 (Domain-Specific Extraction Rules)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| transcript.yaml | Implementation | skills/transcript/contexts/transcript.yaml |
| Schema validation result | Evidence | (in this file) |

### Verification

- [ ] File created at correct location
- [ ] All 4 entity types defined
- [ ] YAML syntax validates
- [ ] Schema structure complete
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-013 |
