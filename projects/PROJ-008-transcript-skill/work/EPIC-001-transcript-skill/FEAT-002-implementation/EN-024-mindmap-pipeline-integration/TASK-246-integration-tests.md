# TASK-246: Integration Tests for Mindmap Pipeline

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "EN-024:TASK-246"
work_type: TASK
title: "Integration Tests for Mindmap Pipeline"
description: |
  Create integration tests to verify mindmap pipeline integration works
  correctly, including parameter handling, format selection, and failure modes.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T00:00:00Z"
updated_at: "2026-01-28T00:00:00Z"
parent_id: "EN-024"
tags:
  - testing
  - integration
  - validation
effort: 3
acceptance_criteria: |
  - Test: --mindmap flag generates both formats
  - Test: --mindmap-format mermaid generates only Mermaid
  - Test: --mindmap-format ascii generates only ASCII
  - Test: Pipeline without --mindmap skips mindmap generation
  - Test: Mindmap failure produces partial result with warning
  - Test: ps-critic validates mindmaps when present
  - All tests documented in test specification file
activity: TESTING
original_estimate: 3
remaining_work: 3
time_spent: 0
```

---

## Description

Create comprehensive integration tests for the mindmap pipeline integration feature.

### Test Categories

1. **Parameter Tests**: Verify flag and format parameter handling
2. **Pipeline Flow Tests**: Verify conditional execution
3. **Output Tests**: Verify correct files generated
4. **Failure Tests**: Verify graceful degradation
5. **Quality Tests**: Verify ps-critic integration

---

## Test Specifications

### TC-001: Default Mindmap Generation (Both Formats)

**Given:** Transcript file `meeting.vtt`
**When:** `/transcript meeting.vtt --mindmap`
**Then:**
- `07-mindmap/mindmap.mmd` exists
- `07-mindmap/mindmap.ascii.txt` exists
- Both files have valid content

### TC-002: Mermaid Only Format

**Given:** Transcript file `meeting.vtt`
**When:** `/transcript meeting.vtt --mindmap --mindmap-format mermaid`
**Then:**
- `07-mindmap/mindmap.mmd` exists
- `07-mindmap/mindmap.ascii.txt` does NOT exist

### TC-003: ASCII Only Format

**Given:** Transcript file `meeting.vtt`
**When:** `/transcript meeting.vtt --mindmap --mindmap-format ascii`
**Then:**
- `07-mindmap/mindmap.mmd` does NOT exist
- `07-mindmap/mindmap.ascii.txt` exists

### TC-004: Pipeline Without Mindmap

**Given:** Transcript file `meeting.vtt`
**When:** `/transcript meeting.vtt` (no --mindmap flag)
**Then:**
- `07-mindmap/` directory does NOT exist
- All other packet files exist normally

### TC-005: Mindmap Failure Graceful Degradation

**Given:** Conditions that cause mindmap generation to fail
**When:** `/transcript meeting.vtt --mindmap`
**Then:**
- Core packet files (00-06) are generated
- Warning message in output
- Regeneration instructions provided
- Pipeline completes (not fails)

### TC-006: ps-critic Validates Mindmaps

**Given:** Transcript processed with `--mindmap`
**When:** ps-critic runs quality review
**Then:**
- Mindmap validation criteria checked
- Quality score includes mindmap contribution
- Invalid Mermaid syntax flagged

### TC-007: ps-critic Skips Mindmap Validation When Not Present

**Given:** Transcript processed without `--mindmap`
**When:** ps-critic runs quality review
**Then:**
- Mindmap validation criteria NOT checked
- Quality score based only on core files

---

## Acceptance Criteria

- [ ] TC-001 through TC-007 documented
- [ ] Tests can be executed manually
- [ ] Test data (sample VTT) identified
- [ ] Expected outputs defined
- [ ] Test specification file created

---

## Implementation Notes

### Test File Location

`skills/transcript/test_data/validation/mindmap-pipeline-tests.yaml`

### Test Data

Use existing test data from:
- `skills/transcript/test_data/transcripts/meeting-001.vtt`
- `skills/transcript/test_data/expected_output/transcript-meeting-001/`

---

## Related Items

- Parent: [EN-024: Mindmap Pipeline Integration](./EN-024-mindmap-pipeline-integration.md)
- Blocked By: [TASK-244: Pipeline Orchestration](./TASK-244-pipeline-orchestration-update.md)
- Blocked By: [TASK-245: ps-critic Update](./TASK-245-ps-critic-mindmap-validation.md)
- Blocks: [TASK-248: Quality Review](./TASK-248-quality-review.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Test Specification | Test | skills/transcript/test_data/validation/mindmap-pipeline-tests.yaml |

### Verification

- [ ] All test cases documented
- [ ] Tests executable
- [ ] Results recorded

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Initial task creation |
