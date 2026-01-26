# EN-008: Entity Extraction Pipeline

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-26T00:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-002
> **Owner:** Claude
> **Target Sprint:** Sprint 3
> **Effort Points:** 13
> **Gate:** GATE-5 (Core Implementation Review)

---

## Summary

Implement the entity extraction pipeline using prompt-based agents to extract structured entities from parsed transcript data. The pipeline extracts speakers, topics, questions, action items, ideas, and decisions with confidence scores and source references.

**Technical Justification:**
- Core value delivery of the transcript skill
- Multiple entity types require specialized extraction logic
- Confidence scoring enables quality filtering
- Deep linking to source enables verification

---

## Benefit Hypothesis

**We believe that** implementing entity extraction as modular prompt-based agents

**Will result in** accurate, verifiable entity extraction with clear provenance

**We will know we have succeeded when:**
- All 6 entity types are extracted correctly
- Confidence scores correlate with accuracy
- Source references link back to specific transcript locations
- Human approval received at GATE-5

---

## Acceptance Criteria

### Definition of Done

- [ ] Speaker profiler agent implemented
- [ ] Topic extractor agent implemented
- [ ] Question detector agent implemented
- [ ] Action item extractor agent implemented
- [ ] Idea extractor agent implemented
- [ ] Decision extractor agent implemented
- [ ] Confidence scoring implemented
- [ ] Source reference linking implemented
- [ ] Integration tests passing
- [ ] ps-critic review passed
- [ ] Human approval at GATE-5

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Extracts speaker profiles with metadata | [ ] |
| AC-2 | Identifies topics with hierarchy (main/sub) | [ ] |
| AC-3 | Detects questions with context | [ ] |
| AC-4 | Extracts action items with assignee if present | [ ] |
| AC-5 | Identifies ideas and suggestions | [ ] |
| AC-6 | Captures decisions and rationale | [ ] |
| AC-7 | All entities have confidence scores [0-1] | [ ] |
| AC-8 | All entities link to source cue IDs | [ ] |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner | Effort | Blocked By |
|----|-------|--------|-------|--------|------------|
| TASK-039 | Create Speaker Profiler Agent | pending | Claude | 2 | EN-007 |
| TASK-040 | Create Topic Extractor Agent | pending | Claude | 2 | EN-007 |
| TASK-041 | Create Question Detector Agent | pending | Claude | 2 | EN-007 |
| TASK-042 | Create Action Item Extractor Agent | pending | Claude | 2 | EN-007 |
| TASK-043 | Create Idea Extractor Agent | pending | Claude | 2 | EN-007 |
| TASK-044 | Create Decision Extractor Agent | pending | Claude | 2 | EN-007 |
| TASK-045 | Implement Confidence Scoring | pending | Claude | 1 | TASK-039..044 |

---

## Entity Schemas

### Speaker Profile

```json
{
  "entity_type": "speaker",
  "id": "speaker-001",
  "name": "John Smith",
  "role": "Meeting Host",
  "speaking_time_seconds": 1245,
  "turn_count": 47,
  "topics_discussed": ["topic-001", "topic-003"],
  "confidence": 0.95,
  "source_cues": ["cue-001", "cue-005", "cue-012"]
}
```

### Topic

```json
{
  "entity_type": "topic",
  "id": "topic-001",
  "name": "Q4 Budget Review",
  "parent_topic_id": null,
  "subtopics": ["topic-002", "topic-003"],
  "time_range": {"start": "00:05:00", "end": "00:25:00"},
  "speakers_involved": ["speaker-001", "speaker-002"],
  "confidence": 0.88,
  "source_cues": ["cue-010", "cue-011", "cue-012"]
}
```

### Action Item

```json
{
  "entity_type": "action_item",
  "id": "action-001",
  "description": "Send updated budget projections to finance team",
  "assignee": "speaker-002",
  "due_date": null,
  "priority": "high",
  "related_topic_id": "topic-001",
  "confidence": 0.92,
  "source_cues": ["cue-045"]
}
```

### Question

```json
{
  "entity_type": "question",
  "id": "question-001",
  "text": "What's our timeline for the Q4 deliverables?",
  "asker_id": "speaker-003",
  "answer_summary": "Targeting end of November",
  "answered_by_id": "speaker-001",
  "confidence": 0.97,
  "source_cues": ["cue-067", "cue-068"]
}
```

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  ENTITY EXTRACTION PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐                                               │
│   │ VTT Parser  │                                               │
│   │  Output     │                                               │
│   └──────┬──────┘                                               │
│          │                                                       │
│          ▼                                                       │
│   ┌──────────────────────────────────────────────────────────┐ │
│   │                   PARALLEL EXTRACTION                     │ │
│   │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │ │
│   │  │ Speaker │ │  Topic  │ │Question │ │ Action  │       │ │
│   │  │Profiler │ │Extractor│ │Detector │ │Extractor│       │ │
│   │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘       │ │
│   │       │           │           │           │             │ │
│   │  ┌────┴────┐ ┌────┴────┐                               │ │
│   │  │  Idea   │ │Decision │                               │ │
│   │  │Extractor│ │Extractor│                               │ │
│   │  └────┬────┘ └────┬────┘                               │ │
│   └───────┼───────────┼─────────────────────────────────────┘ │
│           │           │                                        │
│           └─────┬─────┘                                        │
│                 ▼                                               │
│   ┌──────────────────────┐                                     │
│   │   Entity Merger &    │                                     │
│   │  Deduplication       │                                     │
│   └──────────┬───────────┘                                     │
│              │                                                  │
│              ▼                                                  │
│   ┌──────────────────────┐                                     │
│   │   Confidence         │                                     │
│   │   Scoring            │                                     │
│   └──────────┬───────────┘                                     │
│              │                                                  │
│              ▼                                                  │
│   ┌──────────────────────┐                                     │
│   │  Structured Output   │                                     │
│   │  (JSON per entity)   │                                     │
│   └──────────────────────┘                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002: Implementation](../FEAT-002-implementation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EN-007 | Requires parsed VTT output |
| Depends On | EN-005 | Design documentation required |
| Blocks | EN-009 | Mind map needs entities |
| Blocks | EN-010 | Artifact packaging needs entities |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Enabler created |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (tagged Technical) |
| **SAFe** | Enabler Story |
| **JIRA** | Task |
