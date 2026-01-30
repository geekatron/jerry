# TASK-262: Refactor TranscriptChunker to Token-Based

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
id: "TASK-262"
work_type: TASK
title: "Refactor TranscriptChunker to Token-Based"
description: |
  Refactor TranscriptChunker to support token-based chunking alongside existing
  segment-based chunking. TokenCounter injected via constructor.
classification: ENABLER
status: COMPLETED
resolution: DONE
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-30T09:15:00Z"
updated_at: "2026-01-30T09:15:00Z"
parent_id: "EN-026"
tags: ["tdd", "refactor", "chunker", "token-based"]
effort: 3
acceptance_criteria: |
  - TranscriptChunker accepts target_tokens parameter (default: 18000)
  - TranscriptChunker accepts TokenCounter via constructor injection
  - target_tokens takes precedence over chunk_size when both provided
  - Deprecation warning logged when chunk_size used alone
  - All existing tests still pass (backward compatibility)
  - New token-based tests pass
due_date: null
activity: DEVELOPMENT
original_estimate: 3
remaining_work: 0
time_spent: 3
```

---

## Description

Refactor the `TranscriptChunker` class to support token-based chunking. Per DEC-001:
- D-005: TokenCounter injected via constructor
- D-006: Keep both `chunk_size` and `target_tokens` parameters
- D-007: `target_tokens` takes precedence; deprecation warning for `chunk_size` alone

**TDD Approach:**
1. **RED:** Write failing tests for new behavior first
2. **GREEN:** Implement minimal code to pass tests
3. **REFACTOR:** Clean up while keeping tests green

---

## Acceptance Criteria

### Functional

- [x] Constructor signature: `__init__(chunk_size: int = 500, target_tokens: int | None = None, token_counter: TokenCounter | None = None)`
- [x] When `target_tokens` is provided, use token-based chunking
- [x] When only `chunk_size` is provided, use segment-based chunking (backward compat) + log deprecation warning
- [x] When both provided, `target_tokens` takes precedence
- [x] Default `target_tokens` when used: 18,000
- [x] TokenCounter created internally if not injected (but injectable for testing)

### Backward Compatibility

- [x] All existing tests in `test_chunker.py` still pass (20/20)
- [x] Existing usage `TranscriptChunker(chunk_size=500)` works unchanged
- [x] Deprecation warning logged to guide migration

### Testing (TDD)

- [x] New tests added to `tests/unit/transcript/test_chunker.py`
- [x] Tests written BEFORE implementation (RED phase - 13 tests failed)
- [x] All tests pass after implementation (GREEN phase - 33/33 pass)

### Test Cases Required

| Test | Description |
|------|-------------|
| `test_token_based_chunking_respects_limit` | Chunks don't exceed target_tokens |
| `test_target_tokens_takes_precedence` | When both params, target_tokens wins |
| `test_chunk_size_alone_logs_deprecation` | Deprecation warning when no target_tokens |
| `test_token_counter_injection` | Injected TokenCounter is used |
| `test_default_target_tokens_is_18000` | Default value correct |
| `test_backward_compat_segment_based` | Old behavior still works |

---

## Implementation Notes

### New Constructor Signature

```python
def __init__(
    self,
    chunk_size: int = 500,
    target_tokens: int | None = None,
    token_counter: TokenCounter | None = None,
) -> None:
    """Initialize chunker with segment or token-based strategy.

    Args:
        chunk_size: Segments per chunk (legacy, deprecated if target_tokens not set)
        target_tokens: Target tokens per chunk (recommended, default: 18000)
        token_counter: Injected TokenCounter (created if not provided)
    """
```

### Chunking Logic

```python
def _split_segments(self, segments: list[ParsedSegment]) -> Iterator[list[ParsedSegment]]:
    if self._target_tokens is not None:
        # Token-based chunking
        yield from self._split_by_tokens(segments)
    else:
        # Segment-based chunking (legacy)
        yield from self._split_by_count(segments)
```

---

## Related Items

- Parent: [EN-026: Token-Based Chunking](./EN-026-token-based-chunking.md)
- Depends on: [TASK-261: Implement TokenCounter](./TASK-261-implement-token-counter.md)
- Decision: [DEC-001 D-005, D-006, D-007](./EN-026--DEC-001-implementation-decisions.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| chunker.py (refactored) | Service | `src/transcript/application/services/chunker.py` |
| test_chunker.py (updated) | Tests | `tests/unit/transcript/application/services/test_chunker.py` |

### Verification

- [x] All existing tests pass (backward compat) - 20/20 original tests pass
- [x] All new tests pass - 13 new tests pass
- [x] Deprecation warning appears in logs when appropriate
- [x] TDD phases documented in History

**Test Output:**
```
tests/unit/transcript/test_chunker.py - 33 passed in 0.44s
- Original tests: 20 passed (backward compatibility maintained)
- Token-based tests: 9 passed
- Deprecation tests: 2 passed
- Backward compat tests: 2 passed
```

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation |
| 2026-01-30 | RED | Wrote 13 failing tests for token-based chunking |
| 2026-01-30 | GREEN | Refactored TranscriptChunker, all 33 tests pass |
| 2026-01-30 | COMPLETED | TDD complete, backward compatible |
