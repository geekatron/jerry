# TASK-119: Create Test Cases and Validation for ts-formatter

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-016 (ts-formatter Agent Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-119"
work_type: TASK
title: "Create Test Cases and Validation for ts-formatter"
description: |
  Create and execute validation test cases for ts-formatter using
  golden dataset from EN-015. Verify ADR-002/003/004 compliance.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:30:00Z"
updated_at: "2026-01-26T18:30:00Z"

parent_id: "EN-016"

tags:
  - "testing"
  - "ts-formatter"
  - "validation"

effort: 2
acceptance_criteria: |
  - All golden dataset transcripts formatted successfully
  - No file exceeds 35K tokens
  - All forward links resolve to valid anchors
  - Backlinks sections populated correctly
  - Processing time <5s for 1-hour transcript

due_date: null

activity: TESTING
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

Execute comprehensive validation of ts-formatter against the golden dataset from EN-015. This task validates that all formatting requirements are met, including ADR compliance.

### Validation Matrix

| Test ID | Input | Validation | Expected | Status |
|---------|-------|------------|----------|--------|
| FMT-001 | meeting-001 | 8-file packet generated | 8 files | [ ] |
| FMT-002 | meeting-001 | Token limits respected | All <35K | [ ] |
| FMT-003 | meeting-001 | Forward links resolve | 100% valid | [ ] |
| FMT-004 | meeting-001 | Backlinks populated | All files | [ ] |
| FMT-005 | meeting-001 | Index accurate | Navigation works | [ ] |
| FMT-006 | meeting-002 | Large transcript | Split correctly | [ ] |
| FMT-007 | meeting-003 | Edge cases | Handled gracefully | [ ] |
| FMT-008 | All | Processing time | <5s each | [ ] |

### ADR Compliance Verification

| ADR | Requirement | Test Method | Status |
|-----|-------------|-------------|--------|
| ADR-002 | 8-file structure | File count check | [ ] |
| ADR-002 | 35K token limit | Token count per file | [ ] |
| ADR-003 | Anchor naming | Regex validation | [ ] |
| ADR-003 | Backlinks present | Section detection | [ ] |
| ADR-004 | Semantic splitting | Split boundary check | [ ] |
| ADR-004 | Navigation headers | Header validation | [ ] |

### Test Execution Steps

1. **Setup**
   - Load parsed transcripts (from ts-parser output)
   - Load extraction reports (from ts-extractor output)

2. **Execute Formatting**
   - Run ts-formatter on each test input
   - Capture output packet directory

3. **Verify Structure**
   - Check 8-file packet structure
   - Verify file naming convention
   - Check token counts per file

4. **Verify Links**
   - Parse all forward links
   - Validate anchor targets exist
   - Check backlinks sections

5. **Verify Content**
   - Index navigation accuracy
   - Summary content
   - Entity file content

6. **Document Results**
   - Record all metrics
   - Capture any failures

### Packet Structure Verification

```
Expected Structure:
transcript-meeting-20260126-001/
├── 00-index.md        ✓ Navigation hub
├── 01-summary.md      ✓ Executive summary
├── 02-transcript.md   ✓ Full transcript (or split)
├── 03-speakers.md     ✓ Speaker directory
├── 04-action-items.md ✓ Action items
├── 05-decisions.md    ✓ Decisions
├── 06-questions.md    ✓ Questions
├── 07-topics.md       ✓ Topics
└── _anchors.json      ✓ Anchor registry
```

### Acceptance Criteria

- [ ] All 8 files generated for standard input
- [ ] No file exceeds 35K tokens
- [ ] Split files have navigation headers
- [ ] All forward links resolve (0 broken links)
- [ ] All backlinks sections populated
- [ ] Anchor naming follows convention (type-NNN)
- [ ] _anchors.json valid JSON
- [ ] Index navigation works
- [ ] Processing time <5s per 1-hour transcript

### Edge Case Tests

| Test ID | Scenario | Expected Behavior |
|---------|----------|-------------------|
| EDGE-001 | Empty extraction | Empty entity files, minimal packet |
| EDGE-002 | Single speaker | 03-speakers.md has one entry |
| EDGE-003 | No decisions | 05-decisions.md shows "None found" |
| EDGE-004 | Very long transcript | Multiple split files |
| EDGE-005 | Unicode content | Characters preserved in output |
| EDGE-006 | Special characters in names | Anchors sanitized |

### Related Items

- Parent: [EN-016: ts-formatter Agent Implementation](./EN-016-ts-formatter.md)
- Blocked By: [TASK-114](./TASK-114-packet-generator.md), [TASK-115](./TASK-115-token-counter.md), [TASK-116](./TASK-116-file-splitter.md), [TASK-117](./TASK-117-anchor-registry.md), [TASK-118](./TASK-118-backlink-injector.md)
- Depends On: [TASK-131: Golden dataset](../EN-015-transcript-validation/TASK-131-golden-dataset-transcripts.md)
- References: [TASK-136: Formatter tests](../EN-015-transcript-validation/TASK-136-formatter-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Test execution log | Documentation | (in this file) |
| Packet samples | Output | (link to sample packets) |
| Validation metrics | Evidence | (below) |

### Test Results

```
[To be filled during task execution]

Test ID | Input | Expected | Actual | Status
--------|-------|----------|--------|-------
FMT-001 |       |          |        |
FMT-002 |       |          |        |
FMT-003 |       |          |        |
FMT-004 |       |          |        |
FMT-005 |       |          |        |
FMT-006 |       |          |        |
FMT-007 |       |          |        |
FMT-008 |       |          |        |
```

### Token Count Summary

```
[To be filled during task execution]

File | meeting-001 | meeting-002 | meeting-003
-----|-------------|-------------|-------------
00-index.md      |             |             |
01-summary.md    |             |             |
02-transcript.md |             |             |
03-speakers.md   |             |             |
04-action-items.md |           |             |
05-decisions.md  |             |             |
06-questions.md  |             |             |
07-topics.md     |             |             |
```

### Verification

- [ ] All ADR compliance verified
- [ ] All link validation passed
- [ ] Performance targets met
- [ ] No regressions
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-016 |

