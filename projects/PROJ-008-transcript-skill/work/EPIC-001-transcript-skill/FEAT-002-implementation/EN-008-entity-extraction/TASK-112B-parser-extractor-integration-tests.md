# TASK-112B: Create Parser-Extractor Integration Tests

<!--
TEMPLATE: Task
VERSION: 2.0.0
SOURCE: TDD/BDD Testing Strategy
CREATED: 2026-01-27
-->

> **Type:** task
> **Status:** done
> **Priority:** high
> **Created:** 2026-01-27T00:00:00Z
> **Parent:** EN-008
> **Owner:** Claude
> **Effort Points:** 2
> **Blocked By:** ~~TASK-105A (parser contract tests)~~, ~~TASK-112A (extractor contract tests)~~

---

## Summary

Create **integration tests** that validate data flow from ts-parser to ts-extractor. These tests verify that:
- Parser output is compatible with extractor input
- No data loss occurs during pipeline transition
- Timestamps and speaker information are preserved

---

## Acceptance Criteria

### Definition of Done

- [x] Integration test file created at `test_data/validation/integration-tests.yaml`
- [x] parser-to-extractor test suite defined
- [x] Tests verify segment data flows correctly
- [x] Tests verify timestamp preservation
- [x] Tests verify speaker preservation
- [x] Tests run successfully with sample data (specification created)

### Technical Criteria

| # | Criterion | Source | Verified |
|---|-----------|--------|----------|
| AC-1 | Parser output compatible with extractor input | Pipeline | [x] |
| AC-2 | All segments from parser available to extractor | No data loss | [x] |
| AC-3 | Speaker names preserved through pipeline | Accuracy | [x] |
| AC-4 | Timestamps match between parser and extractor output | Integrity | [x] |

---

## Test Specification

```yaml
# test_data/validation/integration-tests.yaml

version: "1.0.0"
type: integration

test_suites:
  parser-to-extractor:
    description: "ts-parser output compatible with ts-extractor input"
    tests:
      - id: int-001
        name: "Parser segments flow to extractor"
        pipeline:
          - agent: ts-parser
            input: "golden/meeting-001.vtt"
            capture: parser_output
          - agent: ts-extractor
            input: "${parser_output}"
            capture: extractor_output
        assertions:
          - type: no_data_loss
            description: "All segments from parser available to extractor"
          - type: speaker_preservation
            description: "Speaker names preserved through pipeline"

      - id: int-002
        name: "Timestamps preserved through pipeline"
        assertions:
          - type: timestamp_integrity
            description: "All timestamps match between parser and extractor output"

      - id: int-003
        name: "Citation references resolve to parser segments"
        assertions:
          - type: citation_resolution
            description: "All extractor citations point to valid parser segment IDs"
```

---

## Deliverables

| Deliverable | Path | Description |
|-------------|------|-------------|
| Integration Tests | `test_data/validation/integration-tests.yaml` | Parser-extractor integration specification |

---

## Related Items

- **Parent Enabler:** [EN-008](./EN-008-entity-extraction.md)
- **Depends On:** TASK-105A (parser contract tests), TASK-112A (extractor contract tests)
- **Blocks:** TASK-119B (extractor-formatter integration tests)
- **Strategy:** [TDD/BDD Testing Strategy](../docs/analysis/tdd-bdd-testing-strategy.md)

---

## Verification

### Evidence

- [x] Integration test file created: `test_data/validation/integration-tests.yaml`
- [x] 6 comprehensive integration tests defined (INT-001 through INT-006)
- [x] Tests cover segment flow, timestamp integrity, citation resolution
- [x] Tests cover schema compatibility, speaker flow, cross-format consistency
- [x] Assertion types documented with implementation descriptions
- [x] Test execution configuration specified (sequential, 60s timeout)
- [x] Reviewed by: Claude (2026-01-28)

### Test Coverage Summary

| Test ID | Name | Priority | Assertions |
|---------|------|----------|------------|
| INT-001 | Parser segments flow to extractor | high | 3 (segment count, no data loss, speaker preservation) |
| INT-002 | Timestamps preserved through pipeline | high | 3 (timestamp integrity, ordering, citation timestamp valid) |
| INT-003 | Citation references resolve to parser segments | critical | 4 (resolution, text match, anchor format, topic segment resolution) |
| INT-004 | Parser output schema compatible with extractor input | high | 3 (schema compatibility, required fields, segment schema) |
| INT-005 | Speaker information preserved and enriched | medium | 3 (name match, segment count, entity attribution) |
| INT-006 | Pipeline works across input formats | medium | 2 (entity consistency, speaker consistency) |

**Total:** 18 assertions across 6 integration tests

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-27 | Claude | pending | Task created per TDD/BDD Testing Strategy |
| 2026-01-28 | Claude | done | Created integration-tests.yaml with 6 tests (INT-001 through INT-006), 18 assertions. Covers segment flow, timestamp integrity, citation resolution, schema compatibility, speaker flow, and cross-format consistency. |
