# TASK-265: Integration Tests with Real VTT Files

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
id: "TASK-265"
work_type: TASK
title: "Integration Tests with Real VTT Files"
description: |
  Integration tests using real VTT files to verify end-to-end token-based chunking.
  Includes the internal-sample VTT that exposed BUG-001.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-30T09:15:00Z"
updated_at: "2026-01-30T09:15:00Z"
parent_id: "EN-026"
tags: ["testing", "integration-tests", "vtt"]
effort: 2
acceptance_criteria: |
  - Integration test with internal-sample VTT (the file that exposed BUG-001)
  - All generated chunks verified under 18,000 tokens
  - No chunk exceeds 25,000 tokens (hard limit)
  - Test with meeting-006 VTT (existing test data)
due_date: null
activity: TESTING
original_estimate: 2
remaining_work: 2
time_spent: null
```

---

## Description

Create integration tests that parse real VTT files end-to-end and verify that token-based chunking produces chunks within the required limits. This validates the fix for BUG-001.

---

## Acceptance Criteria

### Test Files

- [ ] Test with `internal-sample` VTT (710 segments, exposed BUG-001)
- [ ] Test with existing `meeting-006` VTT (3071 segments)
- [ ] All generated chunks verified under 18,000 tokens

### Verification Points

- [ ] No chunk exceeds 25,000 tokens (hard limit)
- [ ] All chunks target ~18,000 tokens (±10% acceptable variance)
- [ ] index.json contains `target_tokens` field
- [ ] Chunk files are valid JSON

### Test Scenarios

| Test | Description | Expected |
|------|-------------|----------|
| `test_k8_vtt_chunks_under_limit` | Parse internal-sample.vtt | All chunks < 18K tokens |
| `test_meeting006_chunks_under_limit` | Parse meeting-006.vtt | All chunks < 18K tokens |
| `test_chunk_count_reasonable` | Verify chunk count makes sense | More chunks than segment-based |
| `test_total_segments_preserved` | Sum of chunk segments = total | No data loss |

---

## Implementation Notes

### Test Location

```
tests/integration/transcript/test_token_chunking_integration.py
```

### Test Structure

```python
import pytest
from pathlib import Path
import tiktoken

class TestTokenChunkingIntegration:
    @pytest.fixture
    def token_counter(self):
        enc = tiktoken.get_encoding("p50k_base")
        return lambda text: len(enc.encode(text))

    def test_k8_vtt_chunks_under_limit(self, tmp_path, token_counter):
        # Parse VTT with token-based chunking
        # Verify each chunk file
        # Assert all under 18000 tokens
        pass
```

### Test Data Location

- internal-sample VTT: Need to copy to test_data or use from Downloads
- meeting-006 VTT: `skills/transcript/test_data/validation/live-output-meeting-006/`

---

## Related Items

- Parent: [EN-026: Token-Based Chunking](./EN-026-token-based-chunking.md)
- Fixes: [BUG-001](../../FEAT-004-hybrid-infrastructure/EN-021-chunking-strategy/BUG-001-chunk-token-overflow.md)
- Depends on: [TASK-262: Refactor TranscriptChunker](./TASK-262-refactor-chunker.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| test_token_chunking_integration.py | Tests | `tests/integration/...` |
| Test VTT file | Test data | `skills/transcript/test_data/...` |

### Verification

- [ ] All integration tests pass
- [ ] BUG-001 reproduction no longer reproduces
- [ ] Token counts verified with tiktoken

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation |
