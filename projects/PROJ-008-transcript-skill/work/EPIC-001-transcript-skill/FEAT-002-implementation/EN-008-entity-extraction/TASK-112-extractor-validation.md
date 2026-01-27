# TASK-112: Create Test Cases and Validation for ts-extractor

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-008 (ts-extractor Agent Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-112"
work_type: TASK
title: "Create Test Cases and Validation for ts-extractor"
description: |
  Create and execute validation test cases for ts-extractor using
  golden dataset transcripts from EN-015. Verify all FR requirements.

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
  - "testing"
  - "ts-extractor"
  - "validation"

effort: 2
acceptance_criteria: |
  - All golden dataset transcripts processed successfully
  - Precision ≥85% for all entity types
  - Recall ≥80% for all entity types
  - All edge cases handled per error matrix
  - Test results documented

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

Execute comprehensive validation of ts-extractor against the golden dataset from EN-015. This task validates that all extraction requirements are met with target precision and recall.

### Validation Matrix

| Test ID | Input | Entity Type | Expected Count | Precision Target | Recall Target | Status |
|---------|-------|-------------|----------------|------------------|---------------|--------|
| EXT-001 | meeting-001 | Action Items | 5 | ≥85% | ≥80% | [ ] |
| EXT-002 | meeting-001 | Decisions | 3 | ≥85% | ≥80% | [ ] |
| EXT-003 | meeting-001 | Questions | 2 | ≥85% | ≥80% | [ ] |
| EXT-004 | meeting-001 | Topics | 3 | ≥85% | ≥80% | [ ] |
| EXT-005 | meeting-001 | Speakers | 4 | ≥90% | ≥90% | [ ] |
| EXT-006 | meeting-002 | All types | (varies) | ≥85% | ≥80% | [ ] |
| EXT-007 | meeting-003 | Edge cases | (varies) | ≥80% | ≥75% | [ ] |

### Precision and Recall Calculations

```
                         PRECISION & RECALL
                         ==================

    Precision = True Positives / (True Positives + False Positives)
              = Correct extractions / All extractions

    Recall = True Positives / (True Positives + False Negatives)
           = Correct extractions / All actual entities

    F1 Score = 2 × (Precision × Recall) / (Precision + Recall)


    EXAMPLE:
    ────────
    Ground Truth: 5 action items
    Extracted: 6 entities (5 correct, 1 incorrect)
    Missed: 0

    Precision = 5 / 6 = 83.3%
    Recall = 5 / 5 = 100%
    F1 = 2 × (0.833 × 1.0) / (0.833 + 1.0) = 90.9%
```

### Test Execution Steps

1. **Setup**
   - Load golden dataset transcripts (from EN-015 TASK-131)
   - Load ground truth JSON (from EN-015 TASK-132)

2. **Execute Extraction**
   - Run ts-extractor on each test transcript
   - Capture ExtractionReport output

3. **Compare Results**
   - Match extracted entities to ground truth
   - Calculate True Positives, False Positives, False Negatives
   - Compute precision and recall per entity type

4. **Validate Citations**
   - Verify all citations reference valid segments
   - Check citation text snippets match

5. **Validate Confidence Scores**
   - Check confidence distribution
   - Verify HIGH/MEDIUM/LOW thresholds

6. **Document Results**
   - Record all metrics
   - Capture any failures for investigation

### Acceptance Criteria

- [ ] All golden dataset VTT files processed
- [ ] Action item extraction: Precision ≥85%, Recall ≥80%
- [ ] Decision extraction: Precision ≥85%, Recall ≥80%
- [ ] Question extraction: Precision ≥85%, Recall ≥80%
- [ ] Topic segmentation: Precision ≥85%, Recall ≥80%
- [ ] Speaker identification: ≥90% accuracy
- [ ] All citations valid (0 invalid citations)
- [ ] Processing time <30s for 1-hour transcript
- [ ] Edge cases handled (empty, malformed, unicode)

### Edge Case Tests

| Test ID | Scenario | Expected Behavior |
|---------|----------|-------------------|
| EDGE-001 | Empty transcript | Empty results, no errors |
| EDGE-002 | No extractable entities | Empty arrays, statistics reflect zero |
| EDGE-003 | Single speaker | All entities attributed to one speaker |
| EDGE-004 | Missing voice tags | Fallback speaker detection patterns |
| EDGE-005 | Unicode content | All characters preserved in output |
| EDGE-006 | Very long transcript | Stream processing, within memory limits |

### Related Items

- Parent: [EN-008: ts-extractor Agent Implementation](./EN-008-entity-extraction.md)
- Blocked By: [TASK-111: Confidence scoring](./TASK-111-confidence-scoring.md)
- Depends On: [TASK-131: Golden dataset](../EN-015-transcript-validation/TASK-131-golden-dataset-transcripts.md)
- Depends On: [TASK-132: Ground truth](../EN-015-transcript-validation/TASK-132-ground-truth-json.md)
- References: [TASK-135: Extractor tests](../EN-015-transcript-validation/TASK-135-extractor-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Test execution log | Documentation | (in this file) |
| Precision/Recall metrics | Evidence | (below) |
| Failure analysis | Analysis | (below if any) |

### Test Results

```
[To be filled during task execution]

Test ID | Precision | Recall | F1 Score | Status
--------|-----------|--------|----------|-------
EXT-001 |           |        |          |
EXT-002 |           |        |          |
EXT-003 |           |        |          |
EXT-004 |           |        |          |
EXT-005 |           |        |          |
EXT-006 |           |        |          |
EXT-007 |           |        |          |
```

### Aggregate Metrics

```
[To be filled during task execution]

Entity Type    | Precision | Recall | F1 Score
---------------|-----------|--------|----------
Action Items   |           |        |
Decisions      |           |        |
Questions      |           |        |
Topics         |           |        |
Speakers       |           |        |
OVERALL        |           |        |
```

### Verification

- [ ] All precision targets met (≥85%)
- [ ] All recall targets met (≥80%)
- [ ] Speaker accuracy ≥90%
- [ ] Zero invalid citations
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-008 |

