# TASK-119C: Create End-to-End Pipeline Tests

<!--
TEMPLATE: Task
VERSION: 2.0.0
SOURCE: TDD/BDD Testing Strategy
CREATED: 2026-01-27
-->

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-01-27T00:00:00Z
> **Parent:** EN-016
> **Owner:** Claude
> **Effort Points:** 2
> **Blocked By:** TASK-137 (EN-015 integration tests), TASK-131A (human annotation)

---

## Summary

Create **end-to-end tests** that validate the complete pipeline from VTT input to 8-file packet output. These tests use **human-annotated ground truth** (TASK-131A) to measure precision and recall.

---

## Acceptance Criteria

### Definition of Done

- [ ] E2E test file created at `test_data/validation/e2e-tests.yaml`
- [ ] Happy path tests defined
- [ ] Edge case tests defined (large files, malformed input)
- [ ] Precision/recall assertions using ground truth
- [ ] Tests run successfully with golden dataset

### Technical Criteria

| # | Criterion | Source | Verified |
|---|-----------|--------|----------|
| AC-1 | Complete VTT → 8-file packet workflow tested | Pipeline | [ ] |
| AC-2 | Precision >= 85% for action items | TDD-ts-extractor | [ ] |
| AC-3 | Recall >= 80% for action items | TDD-ts-extractor | [ ] |
| AC-4 | Large file triggers correct splitting | ADR-004 | [ ] |
| AC-5 | Malformed VTT produces partial results (no crash) | PAT-002 | [ ] |

---

## Test Specification

```yaml
# test_data/validation/e2e-tests.yaml

version: "1.0.0"
type: e2e

test_suites:
  happy_path:
    description: "Standard VTT processing workflows"
    tests:
      - id: e2e-001
        name: "Basic meeting VTT to 8-file packet"
        input: "golden/meeting-001.vtt"
        expected_output_structure:
          folder: "${session_id}-transcript-output/"
          files: 8
          index_valid: true
        ground_truth: "golden/meeting-001.expected.json"
        assertions:
          - type: precision
            entity: "action_items"
            minimum: 0.85
          - type: recall
            entity: "action_items"
            minimum: 0.80
          - type: files_created
            count: 8

      - id: e2e-002
        name: "User-provided meeting with ground truth"
        input: "user/meeting-alpha.vtt"
        ground_truth: "user/meeting-alpha.expected.json"
        assertions:
          - type: precision
            entity: "action_items"
            minimum: 0.85
          - type: all_entities_have_citations

  edge_cases:
    description: "Edge case handling"
    tests:
      - id: e2e-003
        name: "Large file triggers splitting"
        input: "edge_cases/large.vtt"
        assertions:
          - type: file_split_triggered
            reason: "token_limit"
          - type: all_splits_under_limit
            max_tokens: 35000

      - id: e2e-004
        name: "Malformed VTT graceful degradation"
        input: "edge_cases/malformed.vtt"
        assertions:
          - type: partial_success
            description: "Valid cues extracted despite errors"
          - type: error_logged
            level: "warning"
          - type: no_crash

      - id: e2e-005
        name: "Unicode content preserved"
        input: "edge_cases/unicode.vtt"
        assertions:
          - type: unicode_preserved
            characters: ["Japanese: 田中", "French: François", "German: Müller"]
```

---

## Precision/Recall Targets

| Entity Type | Precision Target | Recall Target | Source |
|-------------|------------------|---------------|--------|
| Action Item | >= 0.85 | >= 0.80 | TDD-ts-extractor |
| Decision | >= 0.85 | >= 0.75 | TDD-ts-extractor |
| Question | >= 0.80 | >= 0.70 | TDD-ts-extractor |
| Speaker | >= 0.90 | >= 0.95 | PAT-003 |

---

## Deliverables

| Deliverable | Path | Description |
|-------------|------|-------------|
| E2E Tests | `test_data/validation/e2e-tests.yaml` | End-to-end test specification |

---

## Related Items

- **Parent Enabler:** [EN-016](./EN-016-ts-formatter.md)
- **Depends On:** TASK-137 (integration tests), TASK-131A (human annotation)
- **Ground Truth:** `test_data/transcripts/user/*.expected.json`
- **Strategy:** [TDD/BDD Testing Strategy](../docs/analysis/tdd-bdd-testing-strategy.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-27 | Claude | pending | Task created per TDD/BDD Testing Strategy |
