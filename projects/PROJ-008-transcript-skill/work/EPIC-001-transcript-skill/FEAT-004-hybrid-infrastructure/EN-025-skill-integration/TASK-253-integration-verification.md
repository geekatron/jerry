# TASK-253: Integration Verification Tests via SKILL.md

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-025 (ts-parser v2.0 + CLI + SKILL.md Integration)
RATIONALE: EN-023 tests use direct Python calls; this task verifies via SKILL.md execution
-->

---

## Frontmatter

```yaml
id: "TASK-253"
work_type: TASK
title: "Integration Verification Tests via SKILL.md Execution"
description: |
  Create integration tests that verify the complete hybrid pipeline works
  end-to-end through SKILL.md orchestration (NOT direct Python calls).
  This addresses the gap where EN-023 tests bypass the orchestration layer.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-29T19:05:00Z"
updated_at: "2026-01-29T19:05:00Z"

parent_id: "EN-025"

tags:
  - "integration-testing"
  - "skill-invocation"
  - "live-test"
  - "verification"

effort: 1
acceptance_criteria: |
  - Live test using /transcript skill produces chunked output
  - index.json + chunks/*.json files created
  - ps-critic quality score >= 0.90
  - No 923KB monolithic canonical-transcript.json
  - Test documented in validation folder

due_date: null

activity: TESTING
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

EN-023 integration tests were marked complete, but they all use **direct Python invocation**:

```python
# From EN-023 tests (NOT what we need)
transcript = vtt_parser.parse("meeting-006.vtt")  # Direct Python call
index_path = chunker.chunk(transcript, output_dir)  # Direct Python call
```

This task creates verification tests that invoke the **actual SKILL.md orchestration**:

```
# What we need
/transcript meeting-006.vtt --output ./validation/live-output-meeting-006/
```

This ensures:
1. ts-parser.md v2.0 orchestration works
2. Format detection routes correctly
3. Python parser is invoked via agent
4. Chunker is invoked in pipeline
5. Complete end-to-end flow validated

### Acceptance Criteria

- [ ] Live test executed via `/transcript` skill invocation
- [ ] Output directory contains: index.json, chunks/*.json
- [ ] Output does NOT contain 923KB monolithic canonical-transcript.json
- [ ] Total segments in chunks equals input segments
- [ ] ps-critic quality score >= 0.90 on output
- [ ] Test results documented in validation folder

### Implementation Notes

**Test Procedure:**

1. **Invoke transcript skill:**
   ```
   /transcript /path/to/meeting-006-all-hands.vtt --output /path/to/validation/live-output-meeting-006/
   ```

2. **Verify output structure:**
   ```
   live-output-meeting-006/
   ├── canonical/
   │   ├── index.json           # Must exist
   │   └── chunks/
   │       ├── chunk-000.json   # Must exist
   │       └── ...
   ├── 00-index.md
   ├── 01-summary.md
   └── ...
   ```

3. **Verify NO monolithic file:**
   - `canonical-transcript.json` should NOT be 923KB
   - If exists, should be small metadata file pointing to chunks

4. **Verify segment count:**
   ```python
   # Sum segments across all chunks
   total_segments = sum(len(chunk["segments"]) for chunk in chunks)
   # Should equal input VTT segment count
   assert total_segments == expected_segment_count
   ```

5. **Run ps-critic:**
   ```
   # Invoke ps-critic on output
   # Verify quality_score >= 0.90
   ```

**Validation Criteria:**

| Check | Expected | Evidence |
|-------|----------|----------|
| index.json exists | Yes | File presence |
| chunks/ directory exists | Yes | Directory presence |
| chunk-000.json exists | Yes | File presence |
| monolithic JSON < 100KB | Yes | File size |
| segment count matches | Yes | Count comparison |
| ps-critic score | >= 0.90 | Quality report |

**Key Difference from EN-023:**

| EN-023 Tests | TASK-253 Tests |
|--------------|----------------|
| Direct Python invocation | SKILL.md orchestration |
| `vtt_parser.parse()` | `/transcript` skill |
| Bypasses ts-parser.md | Uses ts-parser.md v2.0 |
| Unit/integration level | E2E system level |

### Related Items

- Parent: [EN-025: ts-parser v2.0 + CLI + SKILL.md Integration](./EN-025-skill-integration.md)
- Contrast: [EN-023: Integration Testing](../EN-023-integration-testing/EN-023-integration-testing.md) - Uses direct Python calls
- Unblocks: [EN-019: Live Skill Invocation](../../FEAT-002-implementation/EN-019-live-skill-invocation/EN-019-live-skill-invocation.md)
- Unblocks: [TASK-236: Full Pipeline E2E](../EN-023-integration-testing/TASK-236-full-pipeline-e2e.md)
- Test Input: [meeting-006-all-hands.vtt](../../../../../skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt)
- Output Location: [validation/live-output-meeting-006/](../../../../../skills/transcript/test_data/validation/live-output-meeting-006/)

---

## Time Tracking

| Metric            | Value           |
|-------------------|-----------------|
| Original Estimate | 2 hours |
| Remaining Work    | 2 hours    |
| Time Spent        | 0 hours        |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Live test output | Verification | test_data/validation/live-output-meeting-006/ |
| Quality report | Verification | test_data/validation/live-output-meeting-006/quality-review.md |

### Verification

- [ ] index.json exists in output
- [ ] chunks/*.json files exist
- [ ] No 923KB monolithic file
- [ ] Segment count matches input
- [ ] ps-critic score >= 0.90
- [ ] Test documented

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | Created | Initial task creation per EN-025 |
