# TASK-261: Implement TokenCounter Service

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
id: "TASK-261"
work_type: TASK
title: "Implement TokenCounter Service"
description: |
  Create TokenCounter service class using tiktoken p50k_base encoding.
  Follows TDD Red/Green/Refactor methodology.
classification: ENABLER
status: COMPLETED
resolution: DONE
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-30T09:15:00Z"
updated_at: "2026-01-30T09:15:00Z"
parent_id: "EN-026"
tags: ["tdd", "service", "tiktoken", "token-counting"]
effort: 2
acceptance_criteria: |
  - TokenCounter class implemented in src/transcript/application/services/
  - Uses tiktoken p50k_base encoding
  - count_tokens(text: str) -> int method
  - count_segment_tokens(segment: ParsedSegment) -> int method
  - Unit tests in test_token_counter.py (RED first, then GREEN)
  - >=95% code coverage on TokenCounter
due_date: null
activity: DEVELOPMENT
original_estimate: 2
remaining_work: 0
time_spent: 2
```

---

## Description

Implement the `TokenCounter` service class that wraps tiktoken for token counting. This service will be injected into `TranscriptChunker` per DEC-001 (D-004, D-005).

**TDD Approach:**
1. **RED:** Write failing tests first
2. **GREEN:** Implement minimal code to pass tests
3. **REFACTOR:** Clean up while keeping tests green

---

## Acceptance Criteria

### Functional

- [x] `TokenCounter` class in `src/transcript/application/services/token_counter.py`
- [x] Uses `tiktoken.get_encoding("p50k_base")`
- [x] `count_tokens(text: str) -> int` - counts tokens in plain text
- [x] `count_segment_tokens(segment: ParsedSegment) -> int` - counts tokens for a segment including JSON overhead
- [x] Encoding is cached (not re-created per call)

### Testing (TDD)

- [x] Test file: `tests/unit/transcript/application/services/test_token_counter.py`
- [x] Tests written BEFORE implementation (RED phase documented)
- [x] All tests pass after implementation (GREEN phase)
- [x] >=95% code coverage on `token_counter.py` (**100% achieved**)

### Test Cases Required

| Test | Description |
|------|-------------|
| `test_count_tokens_empty_string` | Empty string returns 0 |
| `test_count_tokens_simple_text` | "hello world" returns expected count |
| `test_count_tokens_unicode` | Unicode text tokenizes correctly |
| `test_count_segment_tokens_includes_overhead` | Segment JSON structure adds tokens |
| `test_encoding_is_cached` | Multiple calls use same encoding instance |

---

## Implementation Notes

### Interface

```python
class TokenCounter:
    """Service for counting tokens using tiktoken."""

    def __init__(self, encoding_name: str = "p50k_base") -> None:
        """Initialize with specified encoding."""

    def count_tokens(self, text: str) -> int:
        """Count tokens in plain text."""

    def count_segment_tokens(self, segment: ParsedSegment) -> int:
        """Count tokens for a segment including JSON serialization overhead."""
```

### Location

- Service: `src/transcript/application/services/token_counter.py`
- Tests: `tests/unit/transcript/application/services/test_token_counter.py`

---

## Related Items

- Parent: [EN-026: Token-Based Chunking](./EN-026-token-based-chunking.md)
- Depends on: [TASK-260: Add tiktoken dependency](./TASK-260-add-tiktoken-dependency.md)
- Blocks: [TASK-262: Refactor TranscriptChunker](./TASK-262-refactor-chunker.md)
- Decision: [DEC-001 D-004](./EN-026--DEC-001-implementation-decisions.md) (TokenCounter as separate service)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| token_counter.py | Service | `src/transcript/application/services/token_counter.py` |
| test_token_counter.py | Tests | `tests/unit/transcript/application/services/test_token_counter.py` |

### Verification

- [x] All unit tests pass (20/20 passed)
- [x] Coverage >= 95% (**100% achieved**)
- [x] TDD phases documented in History

**Test Output:**
```
tests/unit/transcript/application/services/test_token_counter.py - 20 passed in 0.25s
Coverage: 100% (19 statements, 0 missed)
```

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation |
| 2026-01-30 | RED | Wrote 20 failing tests before implementation |
| 2026-01-30 | GREEN | Implemented TokenCounter, all 20 tests pass |
| 2026-01-30 | COMPLETED | 100% coverage achieved, TDD complete |
