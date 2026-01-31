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
status: DONE
resolution: COMPLETED
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T00:00:00Z"
updated_at: "2026-01-30T00:00:00Z"
parent_id: "EN-024"
tags:
  - testing
  - integration
  - validation
effort: 3
acceptance_criteria: |
  - Test: Default invocation generates both formats (mindmaps ON by default)
  - Test: --mindmap-format mermaid generates only Mermaid
  - Test: --mindmap-format ascii generates only ASCII
  - Test: --no-mindmap opt-out flag skips mindmap generation
  - Test: Mindmap failure produces partial result with warning (ADR-006 Section 5.4)
  - Test: ps-critic validates mindmaps when present (ADR-006 Section 5.5)
  - Test: Output to 08-mindmap/ directory (DISC-001)
  - All tests documented in test specification file
activity: TESTING
original_estimate: 3
remaining_work: 0
time_spent: 2
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

## Test Specifications (Per ADR-006)

### TC-001: Default Mindmap Generation (Both Formats)

**Given:** Transcript file `meeting.vtt`
**When:** `/transcript meeting.vtt` (NO FLAG - mindmaps ON by default)
**Then:**
- `08-mindmap/mindmap.mmd` exists
- `08-mindmap/mindmap.ascii.txt` exists
- Both files have valid content
- ts_mindmap_output.overall_status == "complete"

**Reference:** ADR-006 Section 4 (Default Behavior)

### TC-002: Mermaid Only Format

**Given:** Transcript file `meeting.vtt`
**When:** `/transcript meeting.vtt --mindmap-format mermaid`
**Then:**
- `08-mindmap/mindmap.mmd` exists
- `08-mindmap/mindmap.ascii.txt` does NOT exist
- ts_mindmap_output.mermaid.status == "complete"
- ts_mindmap_output.ascii.status == "skipped"

**Reference:** ADR-006 Section 5.1 (Format Parameter)

### TC-003: ASCII Only Format

**Given:** Transcript file `meeting.vtt`
**When:** `/transcript meeting.vtt --mindmap-format ascii`
**Then:**
- `08-mindmap/mindmap.mmd` does NOT exist
- `08-mindmap/mindmap.ascii.txt` exists
- ts_mindmap_output.mermaid.status == "skipped"
- ts_mindmap_output.ascii.status == "complete"

**Reference:** ADR-006 Section 5.1 (Format Parameter)

### TC-004: Opt-Out via --no-mindmap Flag

**Given:** Transcript file `meeting.vtt`
**When:** `/transcript meeting.vtt --no-mindmap` (explicit opt-out)
**Then:**
- `08-mindmap/` directory does NOT exist
- All other packet files (00-07) exist normally
- ts_mindmap_output.overall_status == "skipped"
- No mindmap validation performed by ps-critic

**Reference:** ADR-006 Section 4 (Opt-Out Mechanism)

### TC-005: Mindmap Failure Graceful Degradation

**Given:** Conditions that cause mindmap generation to fail
**When:** `/transcript meeting.vtt` (default, mindmaps enabled)
**Then:**
- Core packet files (00-07) are generated
- Warning message in output indicating failure
- Regeneration instructions provided (see ADR-006 Section 5.4)
- ts_mindmap_output.overall_status == "failed" OR "partial"
- Pipeline completes (does NOT fail entirely)

**Reference:** ADR-006 Section 5.4 (Graceful Degradation)

### TC-006: ps-critic Validates Mindmaps When Present

**Given:** Transcript processed with default (mindmaps enabled)
**When:** ps-critic runs quality review
**Then:**
- MM-001..007 validation criteria checked for Mermaid
- AM-001..005 validation criteria checked for ASCII
- Quality score includes 15% mindmap contribution
- Invalid Mermaid syntax flagged as MM-001 failure

**Reference:** ADR-006 Section 5.5 (ps-critic Integration)

### TC-007: ps-critic Skips Mindmap Validation When Opted Out

**Given:** Transcript processed with `--no-mindmap` flag
**When:** ps-critic runs quality review
**Then:**
- Mindmap validation criteria NOT checked
- Quality score based on 100% core files
- No penalty for missing mindmaps (explicit opt-out)

**Reference:** ADR-006 Section 5.5 (Conditional Validation)

---

## Acceptance Criteria

- [x] TC-001 through TC-007 documented
- [x] Tests can be executed manually
- [x] Test data (sample VTT) identified
- [x] Expected outputs defined
- [x] Test specification file created

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
- **ADR Reference:** [ADR-006: Mindmap Pipeline Integration](../../../../../docs/adrs/ADR-006-mindmap-pipeline-integration.md) - All test cases derived from ADR decisions
- Blocks: [TASK-248: Quality Review](./TASK-248-quality-review.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Test Specification | Test | [skills/transcript/test_data/validation/mindmap-pipeline-tests.yaml](../../../../../skills/transcript/test_data/validation/mindmap-pipeline-tests.yaml) |
| TC-001..TC-007 | Pipeline Tests | All tests documented in mindmap-pipeline-tests.yaml |
| TC-008 | Directory Test | DISC-001 compliance verification |
| TC-009 | State Test | ts_mindmap_output schema validation |

### Verification

- [x] All test cases documented (TC-001..TC-009)
- [x] Tests executable (manual execution per YAML spec)
- [x] Test data identified (meeting-001.vtt golden dataset)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Initial task creation |
| 2026-01-30 | Updated | **ADR-006 ALIGNMENT**: Rewrote all test specifications to align with ADR-006 opt-out behavior. TC-001 now tests default (mindmaps ON), TC-004 tests --no-mindmap opt-out. All paths updated to 08-mindmap/ per DISC-001. Added ADR section references to each test case. |
| 2026-01-30 | **DONE** | **TASK COMPLETE**: Created `skills/transcript/test_data/validation/mindmap-pipeline-tests.yaml` with comprehensive test specifications. **Tests created:** TC-001 (default both formats), TC-002 (Mermaid only), TC-003 (ASCII only), TC-004 (--no-mindmap opt-out), TC-005 (graceful degradation), TC-006 (ps-critic validation), TC-007 (ps-critic skip when opted out), TC-008 (08-mindmap/ directory per DISC-001), TC-009 (state passing validation). **Coverage:** 5 categories (pipeline-default, pipeline-format, pipeline-optout, failure-handling, critic-integration). All tests reference ADR-006 sections. |
