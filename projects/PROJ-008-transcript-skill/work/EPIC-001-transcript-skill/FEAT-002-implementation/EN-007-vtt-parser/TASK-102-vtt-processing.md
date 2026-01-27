# TASK-102: Verify VTT Processing (FR-001)

<!--
TEMPLATE: Task
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-007 (ts-parser Agent Implementation)
REVISED: 2026-01-27 per DISC-002 (test infrastructure now available)
-->

---

## Frontmatter

```yaml
id: "TASK-102"
work_type: TASK
title: "Verify VTT Processing (FR-001)"
description: |
  Verify WebVTT format parsing in ts-parser agent handles all VTT
  features: WEBVTT header, cue timing, voice tags, nested tags.

  REVISED 2026-01-27: This is VERIFICATION only (not implementation).
  Implementation code belongs in FEAT-003. We verify the agent definition
  is complete and test it against real VTT files per DISC-002 test infrastructure.

classification: ENABLER
status: READY
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:30:00Z"
updated_at: "2026-01-26T18:30:00Z"

parent_id: "EN-007"

tags:
  - "implementation"
  - "ts-parser"
  - "vtt"
  - "FR-001"

effort: 2
acceptance_criteria: |
  - VTT header validation works
  - Cue timing parsing (HH:MM:SS.mmm --> HH:MM:SS.mmm)
  - Voice tags (<v Speaker>) extracted correctly
  - Nested/class tags handled (stripped or processed)
  - Segment output matches canonical schema

due_date: null

activity: DEVELOPMENT
original_estimate: 4
remaining_work: 4
time_spent: 0
```

---

## State Machine

**Current State:** `READY`

**State History:**
- 2026-01-26: BACKLOG (created)
- 2026-01-27: READY (DISC-002 resolved, test infrastructure available)

---

## Content

### Description

Implement and verify WebVTT format processing in the ts-parser agent per TDD-ts-parser.md Section 1.1.

### FR-001 Requirements (from TDD)

| Req ID | Description | Priority |
|--------|-------------|----------|
| FR-001.1 | Parse WEBVTT header | Must |
| FR-001.2 | Extract cue timing (start → end) | Must |
| FR-001.3 | Extract voice tags `<v Speaker>` | Must |
| FR-001.4 | Handle nested tags (e.g., `<v Speaker><b>`) | Should |
| FR-001.5 | Strip formatting tags, preserve text | Should |

### VTT Format Reference

```vtt
WEBVTT

00:00:00.000 --> 00:00:05.000
<v Alice>Good morning everyone.

00:00:05.000 --> 00:00:10.000
<v Bob>Hi Alice! <b>Ready</b> for the meeting?
```

### Acceptance Criteria

- [ ] WEBVTT header detected and validated
- [ ] Timestamps parsed correctly (millisecond precision)
- [ ] Voice tags extract speaker name
- [ ] Text content extracted without formatting tags
- [ ] raw_text preserves original content (with tags)
- [ ] Segment IDs generated sequentially (seg-001, seg-002)
- [ ] Output matches canonical schema (TDD Section 3)

### Test Cases (from DISC-002 Minimal Infrastructure + W3C Research)

Reference test cases in `skills/transcript/test_data/validation/parser-tests.yaml` (v1.1.0):

#### Core VTT Tests (5)

| Test ID | Name | Status |
|---------|------|--------|
| `vtt-001` | Parse VTT with voice tags and closing `</v>` tags | READY |
| `vtt-002` | Parse VTT with multi-line cue payloads | READY |
| `vtt-003` | Timestamps normalized to milliseconds | READY |
| `vtt-004` | Speaker names extracted from `<v>` tags | READY |
| `vtt-005` | Output matches canonical JSON schema | READY |

#### Edge Case Tests (9 - from W3C WebVTT Research)

| Test ID | Name | Input File | Status |
|---------|------|------------|--------|
| `vtt-006` | Voice tags without closing `</v>` | `voice_tag_no_close.vtt` | READY |
| `vtt-007` | Voice tags with CSS classes | `voice_tag_with_class.vtt` | READY |
| `vtt-008` | Multiple speakers per cue | `multi_speaker_cue.vtt` | READY |
| `vtt-009` | Nested formatting tags stripped | `nested_formatting.vtt` | READY |
| `vtt-010` | Unicode speaker names and content | `unicode_speakers.vtt` | READY |
| `vtt-011` | HTML entity decoding | `entity_escapes.vtt` | READY |
| `vtt-012` | Timestamp edge cases | `timestamp_edge_cases.vtt` | READY |
| `vtt-013` | Empty/malformed (PAT-002) | `empty_and_malformed.vtt` | READY |
| `vtt-014` | Combined edge cases | `combined_edge_cases.vtt` | READY |

**Test Data Locations:**
- Core Input: `skills/transcript/test_data/transcripts/real/internal-sample-sample.vtt`
- Edge Cases: `skills/transcript/test_data/transcripts/edge_cases/*.vtt`
- Expected: `skills/transcript/test_data/expected/internal-sample-sample.expected.json`
- Spec: `skills/transcript/test_data/validation/parser-tests.yaml` (v1.1.0)

**Research Reference:**
- W3C WebVTT test suite research: `EN-007-vtt-parser/research/webvtt-test-suite-research.md`
- Sources: W3C WebVTT Spec, web-platform-tests/wpt, w3c/webvtt.js, mozilla/vtt.js

**NOTE:** Expected output is PENDING_HUMAN_REVIEW before verification.

### Related Items

- Parent: [EN-007: ts-parser Agent Implementation](./EN-007-vtt-parser.md)
- Blocked By: ~~[TASK-101: Agent alignment](./TASK-101-parser-agent-alignment.md)~~ (DONE)
- References: [TDD-ts-parser.md Section 1.1](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md)
- Test Infrastructure: [DISC-002](./EN-007--DISC-002-test-infrastructure-dependency.md) - Created minimal test infrastructure
- Full Test Suite: [TASK-134: Parser tests](../EN-015-transcript-validation/TASK-134-parser-tests.md) (EN-015 expansion)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-parser.md VTT section | Agent | skills/transcript/agents/ts-parser.md |
| VTT test results | Test Evidence | (link to test output) |

### Verification

- [ ] All FR-001.x requirements implemented
- [ ] Golden dataset VTT files parse correctly
- [ ] Edge case VTT files handled per PAT-002
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-007 |
| 2026-01-27 | READY | DISC-002 resolved: Test infrastructure created in `skills/transcript/test_data/`; task clarified as verification (not implementation); status changed from BACKLOG to READY |
| 2026-01-27 | READY | W3C WebVTT research complete: Added 9 edge case tests (vtt-006 through vtt-014); test infrastructure expanded to 14 total VTT tests; parser-tests.yaml updated to v1.1.0 |

