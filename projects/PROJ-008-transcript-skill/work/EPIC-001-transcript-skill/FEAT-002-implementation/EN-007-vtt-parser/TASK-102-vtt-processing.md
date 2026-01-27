# TASK-102: Implement/Verify VTT Processing (FR-001)

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-007 (ts-parser Agent Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-102"
work_type: TASK
title: "Implement/Verify VTT Processing (FR-001)"
description: |
  Verify WebVTT format parsing in ts-parser agent handles all VTT
  features: WEBVTT header, cue timing, voice tags, nested tags.

classification: ENABLER
status: BACKLOG
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

**Current State:** `BACKLOG`

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

### Test Cases (from EN-015)

Reference test cases in parser-tests.yaml:
- `vtt-001`: Parse basic VTT with voice tags
- `vtt-002`: Parse VTT with missing voice tags (fallback)
- `err-002`: Handle malformed VTT with partial recovery

### Related Items

- Parent: [EN-007: ts-parser Agent Implementation](./EN-007-vtt-parser.md)
- Blocked By: [TASK-101: Agent alignment](./TASK-101-parser-agent-alignment.md)
- References: [TDD-ts-parser.md Section 1.1](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md)
- Validated By: [TASK-134: Parser tests](../EN-015-transcript-validation/TASK-134-parser-tests.md)

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

