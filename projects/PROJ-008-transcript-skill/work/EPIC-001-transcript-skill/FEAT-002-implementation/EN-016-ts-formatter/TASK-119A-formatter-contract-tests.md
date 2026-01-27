# TASK-119A: Create Formatter Contract Tests

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
> **Effort Points:** 1
> **Blocked By:** TASK-113 (formatter agent alignment)

---

## Summary

Create **contract tests** that validate ts-formatter output produces the correct **8-file packet structure** per ADR-002. Includes validation that all files stay under the 35K token limit per ADR-004.

---

## Acceptance Criteria

### Definition of Done

- [ ] Contract test section added to `test_data/validation/contract-tests.yaml`
- [ ] Tests verify 8-file packet structure
- [ ] Tests verify all required files present
- [ ] Tests verify token limits respected
- [ ] Tests verify bidirectional links (ADR-003)
- [ ] Tests run successfully against sample output

### Technical Criteria

| # | Criterion | Source | Verified |
|---|-----------|--------|----------|
| AC-1 | 8-file packet contains all required files | ADR-002 | [ ] |
| AC-2 | All files under 35K token limit | ADR-004 | [ ] |
| AC-3 | Index file contains valid links to all sections | ADR-003 | [ ] |
| AC-4 | Backlinks sections present in each file | ADR-003 | [ ] |

---

## Test Specification

```yaml
# test_data/validation/contract-tests.yaml (formatter section)

contracts:
  ts-formatter-output:
    description: "ts-formatter output matches 8-file packet structure"
    tests:
      - id: con-fmt-001
        name: "8-file packet has all required files"
        assertions:
          - type: files_exist
            expected:
              - "00-index.md"
              - "01-summary.md"
              - "02-speakers.md"
              - "03-topics.md"
              - "04-entities.md"
              - "05-timeline.md"
              - "06-insights.md"
              - "07-visualization.md"

      - id: con-fmt-002
        name: "All files under 35K token limit"
        assertions:
          - type: token_count
            max: 35000
            apply_to: "all_files"

      - id: con-fmt-003
        name: "Index file has valid structure"
        assertions:
          - type: index_structure
            required_sections:
              - "Meeting Overview"
              - "Quick Navigation"
              - "File Manifest"

      - id: con-fmt-004
        name: "Backlinks sections present"
        assertions:
          - type: section_present
            section: "Related Sections"
            files: ["01-summary.md", "02-speakers.md", "03-topics.md", "04-entities.md"]
```

---

## Deliverables

| Deliverable | Path | Description |
|-------------|------|-------------|
| Contract Tests | `test_data/validation/contract-tests.yaml` | Formatter contract test specification |

---

## Related Items

- **Parent Enabler:** [EN-016](./EN-016-ts-formatter.md)
- **TDD Document:** TDD-ts-formatter.md
- **ADRs:** ADR-002 (8-file structure), ADR-003 (bidirectional linking), ADR-004 (file splitting)
- **Blocks:** TASK-119B (extractor-formatter integration tests)
- **Strategy:** [TDD/BDD Testing Strategy](../docs/analysis/tdd-bdd-testing-strategy.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-27 | Claude | pending | Task created per TDD/BDD Testing Strategy |
