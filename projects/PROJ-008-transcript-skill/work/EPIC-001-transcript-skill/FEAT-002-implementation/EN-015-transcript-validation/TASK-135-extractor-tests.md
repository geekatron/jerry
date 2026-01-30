# TASK-135: Create Extractor Test Specification

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-015 (Transcript Validation & Test Cases)
-->

---

## Frontmatter

```yaml
id: "TASK-135"
work_type: TASK
title: "Create Extractor Test Specification (extractor-tests.yaml)"
description: |
  Create YAML-based test specification for ts-extractor agent validation.
  Uses ground truth JSON to measure precision, recall, and F1 scores.

classification: ENABLER
status: DONE
resolution: COMPLETED
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:00:00Z"
updated_at: "2026-01-29T15:00:00Z"

parent_id: "EN-015"

tags:
  - "validation"
  - "testing"
  - "ts-extractor"
  - "precision-recall"

effort: 1
acceptance_criteria: |
  - Test suites for each entity type extraction
  - Precision/recall thresholds per EN-015 spec
  - Citation validation tests (PAT-004)
  - Confidence tier tests (PAT-001)
  - Speaker identification tests (PAT-003)

due_date: null

activity: TESTING
original_estimate: 2
remaining_work: 0
time_spent: 2
```

---

## State Machine

**Current State:** `DONE`

---

## Content

### Description

Create a comprehensive YAML test specification for validating the ts-extractor agent. Tests measure extraction accuracy against ground truth using precision/recall metrics.

### Acceptance Criteria

- [x] Action item extraction test suite with precision >= 0.85, recall >= 0.80
- [x] Decision extraction test suite with precision >= 0.85, recall >= 0.75
- [x] Question extraction test suite with precision >= 0.80, recall >= 0.70
- [x] Speaker identification test suite with accuracy >= 0.95
- [x] Topic extraction test suite with precision >= 0.75, recall >= 0.70
- [x] Citation validation test suite (100% coverage)
- [x] Confidence tier validation tests
- [x] All tests reference ground truth JSON

### Precision/Recall Targets (from EN-015)

| Entity Type | Precision | Recall | Source |
|-------------|-----------|--------|--------|
| Action Item | >= 0.85 | >= 0.80 | TDD-ts-extractor |
| Decision | >= 0.85 | >= 0.75 | TDD-ts-extractor |
| Question | >= 0.80 | >= 0.70 | TDD-ts-extractor |
| Speaker | >= 0.90 | >= 0.95 | PAT-003 |
| Topic | >= 0.75 | >= 0.70 | FR-009 |

### Extraction Assertion Types

| Type | Description | Parameters |
|------|-------------|------------|
| precision | Extraction precision | entity, minimum |
| recall | Extraction recall | entity, minimum |
| f1_score | F1 harmonic mean | entity, minimum |
| entity_count | Count of entities | entity, expected |
| field_accuracy | Field-level accuracy | entity, field, minimum |
| citation_coverage | Citation completeness | expected (1.0 = 100%) |
| citation_validity | Citations resolve | expected (bool) |
| confidence_threshold | Minimum confidence | entity, minimum |
| speaker_accuracy | Speaker attribution | minimum |
| speaker_count | Number of speakers | expected |

### Test Suite Structure

```yaml
test_suites:
  action_item_extraction:
    description: "Action item extraction tests"
    ground_truth_required: true
    tests:
      - id: act-001
        name: "Extract action items from meeting-001"
        input: "transcripts/golden/meeting-001.vtt"
        ground_truth: "transcripts/golden/meeting-001.expected.json"
        assertions:
          - type: precision
            entity: "action_item"
            minimum: 0.85
          - type: recall
            entity: "action_item"
            minimum: 0.80
          - type: entity_count
            entity: "action_item"
            expected: 5
        requirements: ["FR-006"]

  citation_validation:
    description: "Anti-hallucination citation tests (PAT-004)"
    tests:
      - id: cite-001
        name: "All extractions have citations"
        input: "transcripts/golden/meeting-001.vtt"
        assertions:
          - type: citation_coverage
            expected: 1.0
          - type: citation_validity
            expected: true
        requirements: ["PAT-004"]
```

### Related Items

- Parent: [EN-015: Transcript Validation](./EN-015-transcript-validation.md)
- Blocked By: [TASK-132: Ground truth JSON](./TASK-132-ground-truth-json.md)
- Tests: [EN-008: ts-extractor Agent](../EN-008-entity-extraction/EN-008-entity-extraction.md)
- **Implements:** [EN-008 TASK-112 Validation Matrix](../EN-008-entity-extraction/TASK-112-extractor-validation.md) (EXT-001..007)
- References: [TDD-ts-extractor.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-extractor.md)
- References: [PAT-001: Tiered Extraction](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-extractor.md)
- References: [PAT-003: Speaker Detection](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-extractor.md)
- References: [PAT-004: Citation Required](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-extractor.md)

> **Note:** This task implements the execution phase of EN-008 TASK-112 validation matrix (EXT-001 through EXT-007).
> The specification phase was completed in EN-008 via TASK-112A (contract tests) and TASK-112B (integration tests).

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| extractor-tests.yaml | Test Spec | test_data/validation/extractor-tests.yaml |

### Verification

- [x] All entity types have test suites (speaker_identification, action_item_extraction, decision_extraction, question_extraction, topic_segmentation)
- [x] Precision/recall thresholds match EN-015 spec (targets section at bottom)
- [x] Ground truth files referenced correctly (meeting-001/002/003.expected.json)
- [x] PAT-004 citation tests included (citation_validation suite: CITE-001..005)
- [x] YAML syntax is valid
- [x] Reviewed by: Claude (2026-01-29)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-015 |
| 2026-01-29 | DONE | Created extractor-tests.yaml with 10 test suites, 50+ assertions |

