# TASK-264: Unit Tests for Token-Based Chunking

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
id: "TASK-264"
work_type: TASK
title: "Unit Tests for Token-Based Chunking"
description: |
  Comprehensive unit test coverage for token-based chunking logic.
  Part of TDD process - some tests written in RED phase of TASK-261/262.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-30T09:15:00Z"
updated_at: "2026-01-30T09:15:00Z"
parent_id: "EN-026"
tags: ["testing", "unit-tests", "tdd"]
effort: 2
acceptance_criteria: |
  - >=95% code coverage on token_counter.py
  - >=90% code coverage on chunker.py (including new code)
  - All edge cases covered (empty input, single segment, exact boundary)
  - Mocking tests for TokenCounter injection
due_date: null
activity: TESTING
original_estimate: 2
remaining_work: 2
time_spent: null
```

---

## Description

Ensure comprehensive unit test coverage for all token-based chunking functionality. This task consolidates and verifies tests created during TDD phases of TASK-261 and TASK-262.

**Note:** Some tests are written as part of the RED phase in earlier tasks. This task ensures completeness and coverage verification.

---

## Acceptance Criteria

### Coverage Targets

- [ ] `token_counter.py` >= 95% line coverage
- [ ] `chunker.py` >= 90% line coverage (overall, including existing code)
- [ ] All new methods 100% covered

### Required Test Scenarios

#### TokenCounter Tests (test_token_counter.py)

| Test | Description | Status |
|------|-------------|--------|
| `test_count_tokens_empty_string` | Empty string → 0 tokens | [ ] |
| `test_count_tokens_single_word` | "hello" → expected count | [ ] |
| `test_count_tokens_sentence` | Full sentence | [ ] |
| `test_count_tokens_unicode` | Unicode characters | [ ] |
| `test_count_tokens_json_structure` | JSON overhead counted | [ ] |
| `test_count_segment_tokens` | ParsedSegment handling | [ ] |
| `test_encoding_cached` | Same instance reused | [ ] |
| `test_custom_encoding` | Non-default encoding | [ ] |

#### Chunker Token Tests (test_chunker.py)

| Test | Description | Status |
|------|-------------|--------|
| `test_token_based_single_chunk` | Small input → 1 chunk | [ ] |
| `test_token_based_multiple_chunks` | Large input → multiple chunks | [ ] |
| `test_token_based_exact_boundary` | Input exactly at limit | [ ] |
| `test_token_based_empty_input` | Empty segments raises error | [ ] |
| `test_target_tokens_precedence` | target_tokens > chunk_size | [ ] |
| `test_deprecation_warning` | Warning logged appropriately | [ ] |
| `test_token_counter_injection` | Mock used correctly | [ ] |
| `test_backward_compat` | chunk_size alone still works | [ ] |

---

## Implementation Notes

### Running Coverage

```bash
uv run pytest tests/unit/transcript/application/services/test_token_counter.py \
  tests/unit/transcript/application/services/test_chunker.py \
  --cov=src/transcript/application/services \
  --cov-report=term-missing \
  --cov-fail-under=90
```

### Mocking TokenCounter

```python
def test_token_counter_injection():
    mock_counter = Mock(spec=TokenCounter)
    mock_counter.count_segment_tokens.return_value = 100

    chunker = TranscriptChunker(target_tokens=500, token_counter=mock_counter)
    # ...verify mock was called
```

---

## Related Items

- Parent: [EN-026: Token-Based Chunking](./EN-026-token-based-chunking.md)
- Depends on: [TASK-261](./TASK-261-implement-token-counter.md), [TASK-262](./TASK-262-refactor-chunker.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| test_token_counter.py | Tests | `tests/unit/.../test_token_counter.py` |
| test_chunker.py | Tests | `tests/unit/.../test_chunker.py` |
| Coverage report | Report | pytest output |

### Verification

- [ ] All tests pass
- [ ] Coverage >= 90% on chunker.py
- [ ] Coverage >= 95% on token_counter.py

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation |
