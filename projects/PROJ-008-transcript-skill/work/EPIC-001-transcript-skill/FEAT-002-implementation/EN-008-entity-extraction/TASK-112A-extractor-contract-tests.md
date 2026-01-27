# TASK-112A: Create Extractor Contract Tests

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
> **Effort Points:** 1
> **Blocked By:** TASK-106 (extractor agent alignment)

---

## Summary

Create **contract tests** that validate ts-extractor output matches the **ExtractionReport** schema defined in TDD-ts-extractor.md. Includes validation that all entities have citations per PAT-004.

---

## Acceptance Criteria

### Definition of Done

- [ ] Contract test section added to `test_data/validation/contract-tests.yaml`
- [ ] Tests verify ExtractionReport schema compliance
- [ ] Tests verify all required entity fields present
- [ ] Tests verify citation coverage (PAT-004 anti-hallucination)
- [ ] Tests run successfully against sample output

### Technical Criteria

| # | Criterion | Source | Verified |
|---|-----------|--------|----------|
| AC-1 | Validate ExtractionReport schema compliance | TDD-ts-extractor | [ ] |
| AC-2 | Verify required fields: version, source_transcript_id, speakers, action_items, decisions, questions, topics | TDD-ts-extractor | [ ] |
| AC-3 | Verify all entities have citations | PAT-004 | [ ] |
| AC-4 | Citation paths resolve correctly | PAT-004 | [ ] |

---

## Test Specification

```yaml
# test_data/validation/contract-tests.yaml (extractor section)

contracts:
  ts-extractor-output:
    description: "ts-extractor output matches ExtractionReport schema"
    schema_ref: "schemas/extraction-report.json"
    tests:
      - id: con-ext-001
        name: "Extractor output has required fields"
        assertions:
          - type: json_schema_valid
            schema: "extraction-report.json"
          - type: required_fields
            expected: ["version", "source_transcript_id", "speakers", "action_items", "decisions", "questions", "topics"]

      - id: con-ext-002
        name: "All entities have citations (PAT-004)"
        assertions:
          - type: citation_present
            paths:
              - "$.action_items[*].citation"
              - "$.decisions[*].citation"
              - "$.questions[*].citation"

      - id: con-ext-003
        name: "Citation structure is valid"
        assertions:
          - type: citation_fields
            required: ["segment_id", "timestamp_ms", "text_snippet"]
```

---

## Deliverables

| Deliverable | Path | Description |
|-------------|------|-------------|
| Contract Tests | `test_data/validation/contract-tests.yaml` | Extractor contract test specification |
| JSON Schema | `test_data/schemas/extraction-report.json` | ExtractionReport schema |

---

## Related Items

- **Parent Enabler:** [EN-008](./EN-008-entity-extraction.md)
- **TDD Document:** TDD-ts-extractor.md
- **Pattern:** PAT-004 (Citation-Required)
- **Blocks:** TASK-112B (parser-extractor integration tests)
- **Strategy:** [TDD/BDD Testing Strategy](../docs/analysis/tdd-bdd-testing-strategy.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-27 | Claude | pending | Task created per TDD/BDD Testing Strategy |
