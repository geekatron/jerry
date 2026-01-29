# TASK-215: Schema Validation Tests

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
CREATED: 2026-01-29 (EN-021 Chunking Strategy)
PURPOSE: Contract tests for index.json and chunk.json schemas
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-215"
work_type: TASK

# === CORE METADATA ===
title: "Schema Validation Tests"
description: |
  Create contract tests that validate generated index.json and chunk-NNN.json
  files against their JSON Schemas. Ensures output compliance with TDD-FEAT-004
  Section 5 specification.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: DONE
resolution: COMPLETED

# === PRIORITY ===
priority: HIGH

# === PEOPLE ===
assignee: "Claude"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-29T20:00:00Z"
updated_at: "2026-01-29T20:00:00Z"

# === HIERARCHY ===
parent_id: "EN-021"

# === TAGS ===
tags:
  - "testing"
  - "contract"
  - "json-schema"
  - "validation"

# === DELIVERY ITEM PROPERTIES ===
effort: 3
acceptance_criteria: |
  AC-1: Contract test file at tests/contract/transcript/test_chunk_schemas.py
  AC-2: Index.json validated against index.schema.json
  AC-3: All chunk files validated against chunk.schema.json
  AC-4: Invalid JSON detected and reported with clear error messages
  AC-5: YAML test specifications at skills/transcript/test_data/validation/chunk-contract-tests.yaml
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: TESTING
original_estimate: 3
remaining_work: 3
time_spent: null
```

---

## State Machine

**Current State:** `DONE`

---

## Description

### Purpose

Contract tests ensure that the chunker output adheres to the formal JSON Schema specifications from TASK-210 and TASK-211. This provides:
- Automated schema compliance verification
- Clear error messages for schema violations
- Regression protection for output format

### Test Strategy

1. **Schema Loading**: Load index.schema.json and chunk.schema.json
2. **Output Validation**: Validate all generated files against schemas
3. **Error Reporting**: Provide actionable error messages for violations

### Test Cases

**Index Contract Tests:**
1. `test_index_validates_against_schema` - Happy path
2. `test_index_required_fields_present` - All required fields exist
3. `test_index_chunk_array_not_empty` - At least one chunk

**Chunk Contract Tests:**
4. `test_chunk_validates_against_schema` - Happy path
5. `test_chunk_segment_range_valid` - Start <= end
6. `test_chunk_navigation_links_valid` - prev/next/index format correct

**Negative Contract Tests:**
7. `test_index_missing_required_field_detected`
8. `test_chunk_invalid_segment_format_detected`

---

## Acceptance Criteria

- [x] AC-1: Contract test file at `tests/contract/transcript/test_chunk_schemas.py` - 17 tests
- [x] AC-2: Index.json validated against index.schema.json - 5 tests (CON-IDX-001..005)
- [x] AC-3: All chunk files validated against chunk.schema.json - 5 tests (CON-CHK-001..005)
- [x] AC-4: Invalid JSON detected and reported with clear error messages - 3 negative tests (CON-NEG-001..003)
- [x] AC-5: YAML test specifications at `skills/transcript/test_data/validation/chunk-contract-tests.yaml` - 16 specs

---

## Related Items

- Parent: [EN-021 Chunking Strategy](./EN-021-chunking-strategy.md)
- Depends On: TASK-210 (Index Schema), TASK-211 (Chunk Schema), TASK-214 (Unit Tests)
- Reference: tests/contract/transcript/test_parser_contracts.py (contract test exemplar)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| test_chunk_schemas.py | pytest Contract | `tests/contract/transcript/test_chunk_schemas.py` |
| chunk-contract-tests.yaml | Test Spec | `skills/transcript/test_data/validation/chunk-contract-tests.yaml` |

### Verification

- [x] All contract tests passing - 17/17 passed
- [x] Schema violations produce clear errors - 3 negative tests demonstrate
- [ ] Reviewed by: Human

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-29 | BACKLOG     | Task created from EN-021       |
| 2026-01-29 | DONE        | 17 contract tests implemented: 5 index, 5 chunk, 3 navigation, 3 negative, 1 integration. All passing. YAML spec created with 16 test cases. |
