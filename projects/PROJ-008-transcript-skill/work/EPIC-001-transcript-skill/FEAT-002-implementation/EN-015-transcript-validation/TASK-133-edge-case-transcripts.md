# TASK-133: Create Edge Case Transcripts

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-015 (Transcript Validation & Test Cases)
-->

---

## Frontmatter

```yaml
id: "TASK-133"
work_type: TASK
title: "Create Edge Case Transcripts (malformed, empty, large)"
description: |
  Create test transcripts that exercise error handling and edge cases.
  These validate defensive parsing (PAT-002) and graceful degradation.

classification: ENABLER
status: BACKLOG
resolution: null
priority: MEDIUM
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:00:00Z"
updated_at: "2026-01-26T18:00:00Z"

parent_id: "EN-015"

tags:
  - "validation"
  - "testing"
  - "edge-cases"
  - "error-handling"

effort: 1
acceptance_criteria: |
  - empty.vtt: Valid VTT header, no cues
  - malformed.vtt: Various syntax errors for partial recovery testing
  - large.vtt: Exceeds 35K tokens to test splitting
  - unicode.vtt: Multi-language content with emojis

due_date: null

activity: DOCUMENTATION
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

Create edge case transcripts that test error handling, boundary conditions, and defensive parsing per PAT-002.

### Acceptance Criteria

#### empty.vtt
- [ ] Valid WEBVTT header present
- [ ] No cue content (0 segments)
- [ ] Expected behavior: Parser returns empty array, no errors

#### malformed.vtt
- [ ] Missing end timestamp in one cue
- [ ] Missing start timestamp in one cue
- [ ] End timestamp before start timestamp
- [ ] Random text without cue header
- [ ] Invalid timestamp format
- [ ] Expected behavior: Partial recovery, warnings logged

#### large.vtt
- [ ] Duration: 2 hours (7,200,000 ms)
- [ ] Token count: ~50,000 tokens
- [ ] Segment count: 500+
- [ ] Expected behavior: Formatter splits output per ADR-004

#### unicode.vtt
- [ ] Japanese text with Kanji
- [ ] French text with accents
- [ ] German text with umlauts
- [ ] Emoji characters
- [ ] Right-to-left text (Arabic/Hebrew sample)
- [ ] Expected behavior: All characters preserved, no corruption

### Edge Case Specifications

**empty.vtt:**
```vtt
WEBVTT

```

**malformed.vtt:**
```vtt
WEBVTT

00:00:01.000 --> 00:00:05
Missing end milliseconds

--> 00:00:10.000
Missing start timestamp

00:00:15.000 --> 00:00:10.000
End before start

not-a-timestamp
Random text without cue header

00:00:xx.000 --> 00:00:25.000
Invalid timestamp format

00:00:30.000 --> 00:00:35.000
<v Alice>Valid cue after errors
```

**unicode.vtt:**
```vtt
WEBVTT

00:00:01.000 --> 00:00:05.000
<v Tanaka>日本語のテストです。

00:00:05.000 --> 00:00:10.000
<v François>Bonjour! Comment ça va? 🎉

00:00:10.000 --> 00:00:15.000
<v Müller>Guten Tag! Größe: ß é ü ö

00:00:15.000 --> 00:00:20.000
<v Ahmed>مرحبا بالعالم

00:00:20.000 --> 00:00:25.000
<v Mixed>English 中文 العربية עברית 🎵🎶
```

**large.vtt:** (Specification only - generated programmatically)
- 500+ cues
- Each cue: ~100 tokens average
- Total: ~50,000 tokens
- Realistic meeting content pattern

### Related Items

- Parent: [EN-015: Transcript Validation](./EN-015-transcript-validation.md)
- References: [PAT-002: Defensive Parsing](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md)
- References: [ADR-004: File Splitting Strategy](../../../docs/adrs/ADR-004-file-splitting-strategy.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| empty.vtt | Test Data | test_data/transcripts/edge_cases/empty.vtt |
| malformed.vtt | Test Data | test_data/transcripts/edge_cases/malformed.vtt |
| large.vtt | Test Data | test_data/transcripts/edge_cases/large.vtt |
| unicode.vtt | Test Data | test_data/transcripts/edge_cases/unicode.vtt |

### Verification

- [ ] empty.vtt has valid header, no cues
- [ ] malformed.vtt contains all specified error types
- [ ] large.vtt exceeds 35K tokens
- [ ] unicode.vtt renders correctly in text editor
- [ ] Parser handles each case per specification
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-015 |

