# TASK-131: Create Golden Dataset Transcripts

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-015 (Transcript Validation & Test Cases)
-->

---

## Frontmatter

```yaml
id: "TASK-131"
work_type: TASK
title: "Create Golden Dataset Transcripts (3 Meetings)"
description: |
  Create three test transcript files with known content for validation testing.
  These serve as ground truth for measuring extraction precision and recall.

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
  - "golden-dataset"

effort: 2
acceptance_criteria: |
  - Three meeting transcripts created in VTT format
  - Meeting-001 available in VTT, SRT, and plain text formats
  - All transcripts have realistic content with known entities
  - Speaker attributions are clear and consistent
  - Timestamps are valid and properly formatted

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

Create three golden dataset transcripts that will serve as ground truth for validating the transcript skill agents. Each transcript has specific characteristics:

| Meeting | Duration | Speakers | Purpose |
|---------|----------|----------|---------|
| meeting-001 | 15 min | 4 | Basic standup with clear entities |
| meeting-002 | 45 min | 6 | Planning session with complex discussions |
| meeting-003 | 20 min | 3→5 | Edge cases (late joins, overlaps) |

### Acceptance Criteria

- [ ] `meeting-001.vtt` created with 4 speakers, 15 minutes
- [ ] `meeting-001.srt` created (same content as VTT)
- [ ] `meeting-001.txt` created (same content, plain format)
- [ ] `meeting-002.vtt` created with 6 speakers, 45 minutes
- [ ] `meeting-003.vtt` created with edge cases (late joins)
- [ ] All timestamps are valid (start < end)
- [ ] All speaker voice tags are properly formatted
- [ ] Content includes entities per EN-015 spec:
  - [ ] meeting-001: 5 action items, 3 decisions, 2 questions
  - [ ] meeting-002: 12 action items, 7 decisions, 5 questions
  - [ ] meeting-003: Edge case scenarios documented

### Implementation Notes

**VTT Format Example:**
```vtt
WEBVTT

00:00:00.000 --> 00:00:05.000
<v Alice>Good morning everyone, let's start our standup.

00:00:05.000 --> 00:00:12.000
<v Bob>I finished the API integration yesterday. Today I'll work on the tests.
```

**SRT Format Example:**
```srt
1
00:00:00,000 --> 00:00:05,000
[Alice] Good morning everyone, let's start our standup.

2
00:00:05,000 --> 00:00:12,000
[Bob] I finished the API integration yesterday. Today I'll work on the tests.
```

**Entity Embedding Guidelines:**
- Action items: Use phrases like "will do", "I'll", "need to", "assigned to"
- Decisions: Use phrases like "we decided", "let's go with", "agreed"
- Questions: Use "?" and phrases like "can we", "how do we", "what about"

### File Locations

```
test_data/transcripts/golden/
├── meeting-001.vtt       # Team standup (VTT)
├── meeting-001.srt       # Team standup (SRT)
├── meeting-001.txt       # Team standup (Plain)
├── meeting-002.vtt       # Planning session
└── meeting-003.vtt       # Edge case meeting
```

### Related Items

- Parent: [EN-015: Transcript Validation](./EN-015-transcript-validation.md)
- Blocks: [TASK-132: Create ground truth JSON](./TASK-132-ground-truth-json.md)
- References: [TDD-ts-parser.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| meeting-001.vtt | Test Data | test_data/transcripts/golden/meeting-001.vtt |
| meeting-001.srt | Test Data | test_data/transcripts/golden/meeting-001.srt |
| meeting-001.txt | Test Data | test_data/transcripts/golden/meeting-001.txt |
| meeting-002.vtt | Test Data | test_data/transcripts/golden/meeting-002.vtt |
| meeting-003.vtt | Test Data | test_data/transcripts/golden/meeting-003.vtt |

### Verification

- [ ] All VTT files parse without errors
- [ ] All SRT files parse without errors
- [ ] Speaker count matches specification
- [ ] Entity count matches specification
- [ ] Timestamps are properly formatted
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-015 |

