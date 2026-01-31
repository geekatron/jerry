# TASK-105A: Create Parser Contract Tests

<!--
TEMPLATE: Task
VERSION: 2.0.0
SOURCE: TDD/BDD Testing Strategy
CREATED: 2026-01-27
-->

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Created:** 2026-01-27T00:00:00Z
> **Updated:** 2026-01-27T23:50:00Z
> **Parent:** EN-007
> **Owner:** Claude
> **Effort Points:** 1
> **Blocked By:** ~~TASK-101~~ (completed)

---

## Summary

Create **contract tests** that validate ts-parser output matches the **CanonicalTranscript** schema defined in TDD-ts-parser.md. Contract tests verify schema compliance before integration testing.

---

## Acceptance Criteria

### Definition of Done

- [ ] Contract test file created at `test_data/validation/contract-tests.yaml`
- [ ] ts-parser section added with schema validation tests
- [ ] Tests verify all required fields present
- [ ] Tests verify segment structure matches schema
- [ ] Tests run successfully against sample output

### Technical Criteria

| # | Criterion | Source | Verified |
|---|-----------|--------|----------|
| AC-1 | Validate CanonicalTranscript schema compliance | TDD-ts-parser | [x] |
| AC-2 | Verify required fields: version, source, metadata, segments | TDD-ts-parser | [x] |
| AC-3 | Verify segment structure: id, speaker, text, start_ms, end_ms | TDD-ts-parser | [x] |
| AC-4 | Tests reference JSON Schema at schemas/canonical-transcript.json | TDD/BDD Strategy | [x] |

---

## Test Specification

```yaml
# test_data/validation/contract-tests.yaml (parser section)

contracts:
  ts-parser-output:
    description: "ts-parser output matches CanonicalTranscript schema"
    schema_ref: "schemas/canonical-transcript.json"
    tests:
      - id: con-par-001
        name: "Parser output has required fields"
        input: "golden/meeting-001.vtt"
        assertions:
          - type: json_schema_valid
            schema: "canonical-transcript.json"
          - type: required_fields
            expected: ["version", "source", "metadata", "segments"]

      - id: con-par-002
        name: "Segment structure is valid"
        assertions:
          - type: array_item_schema
            path: "$.segments"
            schema: "segment.json"

      - id: con-par-003
        name: "Metadata includes format detection"
        assertions:
          - type: field_present
            path: "$.metadata.detected_format"
            values: ["vtt", "srt", "plain"]
```

---

## Deliverables

| Deliverable | Path | Description |
|-------------|------|-------------|
| Contract Tests | `test_data/validation/contract-tests.yaml` | Parser contract test specification |
| JSON Schema | `test_data/schemas/canonical-transcript.json` | CanonicalTranscript schema |
| Segment Schema | `test_data/schemas/segment.json` | Segment sub-schema |

---

## Related Items

- **Parent Enabler:** [EN-007](./EN-007-vtt-parser.md)
- **TDD Document:** TDD-ts-parser.md
- **Blocks:** TASK-112B (parser-extractor integration tests)
- **Strategy:** [TDD/BDD Testing Strategy](../docs/analysis/tdd-bdd-testing-strategy.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-27 | Claude | pending | Task created per TDD/BDD Testing Strategy |
