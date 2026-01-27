# TASK-107: Implement/Verify SpeakerIdentifier (PAT-003)

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-008 (ts-extractor Agent Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-107"
work_type: TASK
title: "Implement/Verify SpeakerIdentifier (PAT-003)"
description: |
  Implement and verify the SpeakerIdentifier component using the 4-pattern
  speaker detection chain per TDD-ts-extractor.md Section 3.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:30:00Z"
updated_at: "2026-01-26T18:30:00Z"

parent_id: "EN-008"

tags:
  - "implementation"
  - "ts-extractor"
  - "speaker-identification"
  - "PAT-003"

effort: 2
acceptance_criteria: |
  - 4-pattern chain implemented in priority order
  - Confidence scores assigned per pattern
  - Fallback to "Unknown Speaker" when all patterns fail
  - >90% speaker attribution accuracy target

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

Implement and verify the SpeakerIdentifier component that applies a 4-pattern detection chain to identify speakers in transcript segments. The implementation must follow PAT-003 from TDD-ts-extractor.md.

### PAT-003: 4-Pattern Speaker Detection Chain

| Priority | Pattern | Confidence | Example |
|----------|---------|------------|---------|
| 1 | VTT Voice Tags | 0.95 | `<v Alice>Hello` |
| 2 | Prefix Pattern | 0.90 | `Alice: Hello` or `ALICE: Hello` |
| 3 | Bracket Pattern | 0.85 | `[Alice] Hello` |
| 4 | Contextual Resolution | 0.60 | "...said Alice" or continuation |

### Algorithm Flow

```
                    ┌─────────────────┐
                    │ Input Segment   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Pattern 1: VTT  │──Yes──► Return (speaker, 0.95)
                    │ Voice Tags      │
                    └────────┬────────┘
                             │ No
                             ▼
                    ┌─────────────────┐
                    │ Pattern 2:      │──Yes──► Return (speaker, 0.90)
                    │ Prefix Pattern  │
                    └────────┬────────┘
                             │ No
                             ▼
                    ┌─────────────────┐
                    │ Pattern 3:      │──Yes──► Return (speaker, 0.85)
                    │ Bracket Pattern │
                    └────────┬────────┘
                             │ No
                             ▼
                    ┌─────────────────┐
                    │ Pattern 4:      │──Yes──► Return (speaker, 0.60)
                    │ Contextual      │
                    └────────┬────────┘
                             │ No
                             ▼
                    ┌─────────────────┐
                    │ Return          │
                    │ ("Unknown", 0.0)│
                    └─────────────────┘
```

### Acceptance Criteria

- [ ] Pattern 1: VTT `<v Speaker>` tags extracted correctly
- [ ] Pattern 2: `Name:` and `NAME:` prefix patterns detected
- [ ] Pattern 3: `[Name]` bracket patterns detected
- [ ] Pattern 4: Contextual hints (previous speaker, quoted attribution)
- [ ] Confidence scores assigned per pattern level
- [ ] Chain stops at first successful match
- [ ] "Unknown Speaker" returned with confidence 0.0 when all patterns fail
- [ ] SpeakerMap aggregates results across all segments
- [ ] >90% accuracy on golden dataset (from EN-015)

### Test Cases (from EN-015)

Reference test scenarios:
- VTT with `<v Alice>` tags → Alice (0.95)
- SRT with `Alice:` prefix → Alice (0.90)
- Plain with `[Alice]` → Alice (0.85)
- Mixed patterns in same transcript
- Missing voice tags (fallback chain)
- Unknown speakers (graceful degradation)

### Related Items

- Parent: [EN-008: ts-extractor Agent Implementation](./EN-008-entity-extraction.md)
- Blocked By: [TASK-106: Agent alignment](./TASK-106-extractor-agent-alignment.md)
- References: [TDD-ts-extractor.md Section 3](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-extractor.md)
- Validated By: [TASK-135: Extractor tests](../EN-015-transcript-validation/TASK-135-extractor-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-extractor.md SpeakerIdentifier section | Agent | skills/transcript/agents/ts-extractor.md |
| Speaker identification test results | Test Evidence | (link to test output) |

### Verification

- [ ] All 4 patterns implemented
- [ ] Confidence scores match TDD specification
- [ ] Fallback behavior works correctly
- [ ] >90% accuracy on test data
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-008 |

