# TASK-266: Contract Tests for Updated Schema

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
id: "TASK-266"
work_type: TASK
title: "Contract Tests for Updated Schema"
description: |
  Contract tests validating index.json schema with new target_tokens field.
  Ensures backward compatibility and forward compatibility.
classification: ENABLER
status: BACKLOG
resolution: null
priority: MEDIUM
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-30T09:15:00Z"
updated_at: "2026-01-30T09:15:00Z"
parent_id: "EN-026"
tags: ["testing", "contract-tests", "schema"]
effort: 1
acceptance_criteria: |
  - Schema validation tests for index.json with target_tokens
  - Schema validation tests for index.json without target_tokens (backward compat)
  - Chunk schema unchanged (no contract break)
due_date: null
activity: TESTING
original_estimate: 1
remaining_work: 1
time_spent: null
```

---

## Description

Create contract tests to validate the updated index.json schema. These tests ensure:
1. New `target_tokens` field validates correctly
2. Old index.json files (without `target_tokens`) still validate (backward compat)
3. Chunk schema remains unchanged

---

## Acceptance Criteria

### Schema Validation

- [ ] index.json with `target_tokens` validates against schema
- [ ] index.json without `target_tokens` validates against schema
- [ ] Invalid `target_tokens` values rejected (e.g., negative, string)
- [ ] chunk.json schema unchanged

### Test Scenarios

| Test | Description | Expected |
|------|-------------|----------|
| `test_index_with_target_tokens_valid` | Schema accepts new field | Pass |
| `test_index_without_target_tokens_valid` | Schema accepts old format | Pass |
| `test_index_invalid_target_tokens_type` | String value rejected | Fail validation |
| `test_index_negative_target_tokens` | Negative rejected | Fail validation |
| `test_chunk_schema_unchanged` | No changes to chunk.json | Pass |

---

## Implementation Notes

### Test Location

Extend existing contract tests:
```
tests/unit/transcript/application/services/test_chunker_schemas.py
```

Or add to existing schema validation tests if they exist.

### Schema Validation

```python
import jsonschema

def test_index_with_target_tokens_valid():
    schema = load_schema("index.schema.json")
    data = {
        "schema_version": "1.0",
        "total_segments": 710,
        "total_chunks": 4,
        "chunk_size": 500,
        "target_tokens": 18000,  # NEW FIELD
        # ... other required fields
    }
    jsonschema.validate(data, schema)  # Should not raise
```

---

## Related Items

- Parent: [EN-026: Token-Based Chunking](./EN-026-token-based-chunking.md)
- Depends on: [TASK-263: Update index.json schema](./TASK-263-update-index-schema.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Schema contract tests | Tests | `tests/.../test_chunker_schemas.py` |

### Verification

- [ ] All contract tests pass
- [ ] Backward compatibility verified
- [ ] Forward compatibility verified

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation |
