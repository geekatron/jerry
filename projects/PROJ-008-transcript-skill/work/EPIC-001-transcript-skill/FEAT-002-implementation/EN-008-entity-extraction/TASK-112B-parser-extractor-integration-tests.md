# TASK-112B: Create Parser-Extractor Integration Tests

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
> **Parent:** EN-008
> **Owner:** Claude
> **Effort Points:** 2
> **Blocked By:** TASK-105A (parser contract tests), TASK-112A (extractor contract tests)

---

## Summary

Create **integration tests** that validate data flow from ts-parser to ts-extractor. These tests verify that:
- Parser output is compatible with extractor input
- No data loss occurs during pipeline transition
- Timestamps and speaker information are preserved

---

## Acceptance Criteria

### Definition of Done

- [ ] Integration test file created at `test_data/validation/integration-tests.yaml`
- [ ] parser-to-extractor test suite defined
- [ ] Tests verify segment data flows correctly
- [ ] Tests verify timestamp preservation
- [ ] Tests verify speaker preservation
- [ ] Tests run successfully with sample data

### Technical Criteria

| # | Criterion | Source | Verified |
|---|-----------|--------|----------|
| AC-1 | Parser output compatible with extractor input | Pipeline | [ ] |
| AC-2 | All segments from parser available to extractor | No data loss | [ ] |
| AC-3 | Speaker names preserved through pipeline | Accuracy | [ ] |
| AC-4 | Timestamps match between parser and extractor output | Integrity | [ ] |

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

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-27 | Claude | pending | Task created per TDD/BDD Testing Strategy |
