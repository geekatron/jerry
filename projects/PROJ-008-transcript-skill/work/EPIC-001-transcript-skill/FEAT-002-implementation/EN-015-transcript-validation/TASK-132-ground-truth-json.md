# TASK-132: Create Ground Truth JSON for Golden Dataset

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-015 (Transcript Validation & Test Cases)
-->

---

## Frontmatter

```yaml
id: "TASK-132"
work_type: TASK
title: "Create Ground Truth JSON for Golden Dataset"
description: |
  Create expected extraction results JSON files for each golden dataset transcript.
  These files define the exact entities, timestamps, and relationships that should
  be extracted, enabling precision/recall measurement.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:00:00Z"
updated_at: "2026-01-26T18:00:00Z"

parent_id: "EN-015"

tags:
  - "validation"
  - "testing"
  - "ground-truth"

effort: 2
acceptance_criteria: |
  - Ground truth JSON created for each golden dataset transcript
  - All entities tagged with unique IDs
  - Timestamp references accurate to source transcript
  - Assignees and speakers properly attributed
  - JSON schema validated

due_date: null

activity: DOCUMENTATION
original_estimate: 4
remaining_work: 4
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Content

### Description

Create JSON files that define the expected extraction results for each golden dataset transcript. These serve as ground truth for measuring extraction accuracy (precision, recall, F1).

### Ground Truth Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["metadata", "speakers", "entities"],
  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "transcript_id": { "type": "string" },
        "format": { "enum": ["vtt", "srt", "txt"] },
        "duration_ms": { "type": "integer" },
        "created_at": { "type": "string", "format": "date-time" }
      }
    },
    "speakers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "name": { "type": "string" },
          "speaking_time_ms": { "type": "integer" }
        }
      }
    },
    "entities": {
      "type": "object",
      "properties": {
        "action_items": { "type": "array" },
        "decisions": { "type": "array" },
        "questions": { "type": "array" },
        "topics": { "type": "array" }
      }
    }
  }
}
```

### Acceptance Criteria

- [ ] `meeting-001.expected.json` created with all entities
- [ ] `meeting-002.expected.json` created with all entities
- [ ] `meeting-003.expected.json` created with edge case entities
- [ ] All action items have:
  - [ ] Unique ID (act-XXX)
  - [ ] Description text
  - [ ] Assignee (if stated)
  - [ ] Due date (if stated)
  - [ ] Source timestamp range
  - [ ] Exact source text (for citation verification)
- [ ] All decisions have:
  - [ ] Unique ID (dec-XXX)
  - [ ] Description text
  - [ ] Decided by (person or consensus)
  - [ ] Source timestamp range
  - [ ] Exact source text
- [ ] All questions have:
  - [ ] Unique ID (que-XXX)
  - [ ] Question text
  - [ ] Asked by
  - [ ] Answered (true/false)
  - [ ] Source timestamp range
- [ ] JSON validates against schema

### Example Ground Truth (meeting-001)

```json
{
  "metadata": {
    "transcript_id": "meeting-001",
    "format": "vtt",
    "duration_ms": 900000,
    "created_at": "2026-01-26T00:00:00Z"
  },
  "speakers": [
    { "id": "spk-001", "name": "Alice", "speaking_time_ms": 240000 },
    { "id": "spk-002", "name": "Bob", "speaking_time_ms": 180000 },
    { "id": "spk-003", "name": "Carol", "speaking_time_ms": 240000 },
    { "id": "spk-004", "name": "Dave", "speaking_time_ms": 240000 }
  ],
  "entities": {
    "action_items": [
      {
        "id": "act-001",
        "description": "Bob will send the report by Friday",
        "assignee": "Bob",
        "due_date": "Friday",
        "source_start_ms": 120000,
        "source_end_ms": 125000,
        "exact_text": "I'll send the report by Friday.",
        "confidence_tier": "high"
      }
    ],
    "decisions": [
      {
        "id": "dec-001",
        "description": "Use React for the frontend",
        "decided_by": "Alice",
        "source_start_ms": 300000,
        "source_end_ms": 310000,
        "exact_text": "Let's go with React for the frontend.",
        "rationale": "Team familiarity"
      }
    ],
    "questions": [
      {
        "id": "que-001",
        "text": "How are we handling authentication?",
        "asked_by": "Dave",
        "answered": true,
        "answer_summary": "Using OAuth2 with existing provider",
        "source_start_ms": 450000,
        "source_end_ms": 455000
      }
    ],
    "topics": [
      {
        "id": "top-001",
        "name": "Sprint Progress",
        "start_ms": 30000,
        "end_ms": 300000,
        "confidence": 0.95
      }
    ]
  }
}
```

### Related Items

- Parent: [EN-015: Transcript Validation](./EN-015-transcript-validation.md)
- Blocked By: [TASK-131: Create golden dataset transcripts](./TASK-131-golden-dataset-transcripts.md)
- Blocks: [TASK-135: Create extractor test specification](./TASK-135-extractor-tests.md)
- References: [TDD-ts-extractor.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-extractor.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| meeting-001.expected.json | Test Data | test_data/transcripts/golden/meeting-001.expected.json |
| meeting-002.expected.json | Test Data | test_data/transcripts/golden/meeting-002.expected.json |
| meeting-003.expected.json | Test Data | test_data/transcripts/golden/meeting-003.expected.json |
| ground-truth-schema.json | Schema | test_data/validation/schemas/ground-truth-schema.json |

### Verification

- [ ] JSON validates against schema
- [ ] Entity counts match EN-015 specifications
- [ ] All timestamps are within transcript duration
- [ ] All source text references exist in transcript
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-015 |

