# TASK-263: Update index.json Schema (target_tokens field)

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
id: "TASK-263"
work_type: TASK
title: "Update index.json Schema (target_tokens field)"
description: |
  Add target_tokens field to index.json schema to document the chunking strategy used.
classification: ENABLER
status: BACKLOG
resolution: null
priority: MEDIUM
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-30T09:15:00Z"
updated_at: "2026-01-30T09:15:00Z"
parent_id: "EN-026"
tags: ["schema", "json", "index"]
effort: 1
acceptance_criteria: |
  - index.schema.json updated with target_tokens field
  - index.json generation includes target_tokens when token-based
  - Backward compatible (target_tokens is optional)
  - Contract tests validate new field
due_date: null
activity: DESIGN
original_estimate: 1
remaining_work: 1
time_spent: null
```

---

## Description

Update the `index.json` schema and generation to include the `target_tokens` field. This provides transparency about which chunking strategy was used.

**Note:** This task does not require TDD per DEC-001 (D-002). Contract tests in TASK-266 validate the schema.

---

## Acceptance Criteria

### Schema Changes

- [ ] `skills/transcript/test_data/schemas/index.schema.json` updated
- [ ] New field: `target_tokens` (integer, optional)
- [ ] Field added alongside existing `chunk_size`

### Generation Changes

- [ ] `_create_index_data()` in chunker.py includes `target_tokens` when token-based chunking used
- [ ] Field omitted when segment-based chunking used (backward compat)

### Example Output

```json
{
  "schema_version": "1.0",
  "total_segments": 710,
  "total_chunks": 4,
  "chunk_size": 500,
  "target_tokens": 18000,
  "...": "..."
}
```

---

## Implementation Notes

### Schema Addition

```json
{
  "properties": {
    "target_tokens": {
      "type": "integer",
      "minimum": 1000,
      "maximum": 100000,
      "description": "Target tokens per chunk when token-based chunking is used"
    }
  }
}
```

### Code Change

```python
def _create_index_data(self, ...) -> dict[str, Any]:
    index_data = {
        # existing fields...
        "chunk_size": self._chunk_size,
    }
    if self._target_tokens is not None:
        index_data["target_tokens"] = self._target_tokens
    return index_data
```

---

## Related Items

- Parent: [EN-026: Token-Based Chunking](./EN-026-token-based-chunking.md)
- Depends on: [TASK-262: Refactor TranscriptChunker](./TASK-262-refactor-chunker.md)
- Validated by: [TASK-266: Contract tests](./TASK-266-contract-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| index.schema.json | Schema | `skills/transcript/test_data/schemas/index.schema.json` |

### Verification

- [ ] Schema validates with new field
- [ ] Schema validates without new field (backward compat)
- [ ] Generated index.json includes target_tokens when appropriate

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation |
