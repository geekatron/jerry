# TASK-119B: Create Extractor-Formatter Integration Tests

<!--
TEMPLATE: Task
VERSION: 2.0.0
SOURCE: TDD/BDD Testing Strategy
CREATED: 2026-01-27
-->

> **Type:** task
> **Status:** DONE
> **Priority:** high
> **Created:** 2026-01-27T00:00:00Z
> **Updated:** 2026-01-28T18:15:00Z
> **Parent:** EN-016
> **Owner:** Claude
> **Effort Points:** 2
> **Blocked By:** TASK-112A (extractor contract tests) ✓, TASK-119A (formatter contract tests) ✓

---

## Summary

Create **integration tests** that validate data flow from ts-extractor to ts-formatter. These tests verify that:
- Extractor output is compatible with formatter input
- Entity counts are preserved during formatting
- Citations remain valid and resolvable in formatted output

---

## Acceptance Criteria

### Definition of Done

- [x] Integration test suite added to `test_data/validation/integration-tests.yaml`
- [x] extractor-to-formatter test suite defined
- [x] Tests verify entity count preservation
- [x] Tests verify citation link validity
- [ ] Tests run successfully with sample data (deferred to execution phase)

### Technical Criteria

| # | Criterion | Source | Verified |
|---|-----------|--------|----------|
| AC-1 | Extractor output compatible with formatter input | Pipeline | [x] INT-EF-001 |
| AC-2 | Entity counts preserved (action_items, decisions, questions) | No data loss | [x] INT-EF-001 |
| AC-3 | Citation links resolve correctly in formatted output | PAT-004 | [x] INT-EF-002 |
| AC-4 | Speaker information preserved in formatted output | Accuracy | [x] INT-EF-003 |

---

## Test Specification

```yaml
# test_data/validation/integration-tests.yaml (extractor-formatter section)

test_suites:
  extractor-to-formatter:
    description: "ts-extractor output compatible with ts-formatter input"
    tests:
      - id: int-003
        name: "All entity types flow to formatter"
        pipeline:
          - agent: ts-extractor
            input: "precalculated/canonical-001.json"
            capture: extractor_output
          - agent: ts-formatter
            input: "${extractor_output}"
            capture: formatter_output
        assertions:
          - type: entity_count_preserved
            entities: ["action_items", "decisions", "questions"]
          - type: citation_links_valid
            description: "All citations resolve in formatted output"

      - id: int-004
        name: "Speaker data preserved in speaker section"
        assertions:
          - type: speaker_count_preserved
            source: "extractor_output.speakers"
            target: "formatter_output/02-speakers.md"

      - id: int-005
        name: "Topic hierarchy preserved"
        assertions:
          - type: topic_structure_preserved
            source: "extractor_output.topics"
            target: "formatter_output/03-topics.md"
```

---

## Deliverables

| Deliverable | Path | Description |
|-------------|------|-------------|
| Integration Tests | `test_data/validation/integration-tests.yaml` | Extractor-formatter integration specification |

---

## Related Items

- **Parent Enabler:** [EN-016](./EN-016-ts-formatter.md)
- **Depends On:** TASK-112A (extractor contract tests), TASK-119A (formatter contract tests)
- **Blocks:** TASK-119C (end-to-end pipeline tests)
- **Strategy:** [TDD/BDD Testing Strategy](../docs/analysis/tdd-bdd-testing-strategy.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-27 | Claude | pending | Task created per TDD/BDD Testing Strategy |
| 2026-01-28 | Claude | **DONE** | Created 6 integration tests (INT-EF-001 to INT-EF-006) in integration-tests.yaml. Tests cover: entity count preservation, citation link resolution (PAT-004), speaker data flow, topic hierarchy preservation, backlink generation (ADR-003/IR-004), and extraction stats in summary. |
