# TASK-103: Implement/Verify SRT Processing (FR-002)

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-007 (ts-parser Agent Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-103"
work_type: TASK
title: "Implement/Verify SRT Processing (FR-002)"
description: |
  Verify SubRip (SRT) format parsing in ts-parser agent handles
  sequence numbers, both comma and period timestamps, speaker prefixes.

classification: ENABLER
status: COMPLETED
resolution: VERIFIED
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:30:00Z"
updated_at: "2026-01-27T22:00:00Z"

parent_id: "EN-007"

tags:
  - "implementation"
  - "ts-parser"
  - "srt"
  - "FR-002"

effort: 1
acceptance_criteria: |
  - Sequence number parsing works
  - Both comma (,) and period (.) timestamp separators supported
  - Speaker prefix patterns ([Name], Name:) extracted
  - Multi-line cue content handled
  - Output matches canonical schema

due_date: null

activity: DEVELOPMENT
original_estimate: 2
remaining_work: 2
time_spent: 0
```

---

## State Machine

**Current State:** `COMPLETED`

---

## Content

### Description

Implement and verify SubRip (SRT) format processing in the ts-parser agent per TDD-ts-parser.md Section 1.2.

### FR-002 Requirements (from TDD)

| Req ID | Description | Priority |
|--------|-------------|----------|
| FR-002.1 | Parse sequence numbers | Must |
| FR-002.2 | Support comma timestamps (HH:MM:SS,mmm) | Must |
| FR-002.3 | Support period timestamps (HH:MM:SS.mmm) | Must |
| FR-002.4 | Extract speaker from `[Name]` prefix | Should |
| FR-002.5 | Extract speaker from `Name:` prefix | Should |
| FR-002.6 | Handle multi-line cue content | Must |

### SRT Format Reference

**Comma timestamps (standard):**
```srt
1
00:00:00,000 --> 00:00:05,000
[Alice] Good morning everyone.

2
00:00:05,000 --> 00:00:10,000
Bob: Hi Alice! Ready for the meeting?
```

**Period timestamps (Otter.ai export):**
```srt
1
00:00:00.000 --> 00:00:05.000
[Alice] Good morning everyone.
```

### Acceptance Criteria

- [x] Sequence numbers parsed and used for ordering
- [x] Comma timestamps (00:00:00,000) parsed correctly
- [x] Period timestamps (00:00:00.000) parsed correctly
- [x] `[Speaker]` prefix extracts speaker name
- [x] `Speaker:` prefix extracts speaker name
- [x] Multi-line content joined correctly
- [x] Output matches canonical schema (TDD Section 3)

### Test Cases (from EN-015)

Reference test cases in parser-tests.yaml:
- `srt-001`: Parse SRT with comma timestamps (Zoom)
- `srt-002`: Parse SRT with period timestamps (Otter.ai)

### Related Items

- Parent: [EN-007: ts-parser Agent Implementation](./EN-007-vtt-parser.md)
- Blocked By: [TASK-101: Agent alignment](./TASK-101-parser-agent-alignment.md)
- References: [TDD-ts-parser.md Section 1.2](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md)
- Validated By: [TASK-134: Parser tests](../EN-015-transcript-validation/TASK-134-parser-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-parser.md SRT section | Agent | skills/transcript/agents/ts-parser.md |
| SRT test data (3 files) | Test Input | skills/transcript/test_data/transcripts/real/sample-meeting-zoom.srt |
|  |  | skills/transcript/test_data/transcripts/edge_cases/srt_period_timestamps.srt |
|  |  | skills/transcript/test_data/transcripts/edge_cases/srt_mixed_speakers.srt |
| Expected outputs (3 files) | Golden Data | skills/transcript/test_data/expected/sample-meeting-zoom.expected.json |
|  |  | skills/transcript/test_data/expected/srt_period_timestamps.expected.json |
|  |  | skills/transcript/test_data/expected/srt_mixed_speakers.expected.json |
| Verification Results | Test Evidence | verification/TASK-103-srt-verification-results.md |

### Verification

- [x] All FR-002.x requirements implemented
- [x] Both timestamp formats (comma/period) work
- [x] Speaker extraction patterns work (colon, bracket, ALL CAPS, null fallback)
- [x] Reviewed by: Claude (2026-01-27)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-007 |
| 2026-01-27 | IN_PROGRESS | Test data created (3 SRT files, 3 expected JSON) |
| 2026-01-27 | COMPLETED | All 3 test cases verified - srt-001, srt-002, srt-003 pass |

