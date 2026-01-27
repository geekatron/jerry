# TASK-115: Implement/Verify TokenCounter (NFR-009)

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-016 (ts-formatter Agent Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-115"
work_type: TASK
title: "Implement/Verify TokenCounter (NFR-009)"
description: |
  Implement and verify the TokenCounter component that counts tokens
  and enforces the 35K token limit per file.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:30:00Z"
updated_at: "2026-01-26T18:30:00Z"

parent_id: "EN-016"

tags:
  - "implementation"
  - "ts-formatter"
  - "token-counting"
  - "NFR-009"

effort: 1
acceptance_criteria: |
  - Token counting implemented with reasonable accuracy
  - Soft limit (31,500) triggers split evaluation
  - Hard limit (35,000) enforced
  - Word-to-token ratio estimation for performance

due_date: null

activity: DEVELOPMENT
original_estimate: 2
remaining_work: 2
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Content

### Description

Implement and verify the TokenCounter component that tracks token counts and enforces the 35K token limit per file. This is critical for ensuring Claude-friendly artifact sizes.

### Token Limits (NFR-009)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           TOKEN LIMITS                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                           HARD LIMIT                                 │    │
│  │                          35,000 tokens                               │    │
│  │                                                                       │    │
│  │  • Maximum tokens per file                                           │    │
│  │  • Force split if exceeded                                           │    │
│  │  • No exceptions                                                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                           SOFT LIMIT                                 │    │
│  │                      31,500 tokens (90%)                             │    │
│  │                                                                       │    │
│  │  • Trigger semantic split evaluation                                 │    │
│  │  • Allows completion of current section                              │    │
│  │  • Buffer for headers/navigation (~3,500 tokens)                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  DECISION FLOW:                                                              │
│                                                                              │
│  tokens < 31,500        → Continue writing                                   │
│  31,500 ≤ tokens < 35K  → Evaluate split at next ## heading                 │
│  tokens ≥ 35,000        → Force split immediately                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Token Counting Methods

#### Method 1: Accurate Count (Preferred)

Use tiktoken or equivalent for accurate Claude tokenization:

```
# Conceptual approach
def count_tokens(content: str) -> int:
    # Use Claude tokenizer for accurate count
    tokens = tokenize(content)
    return len(tokens)
```

#### Method 2: Word Estimation (Fallback)

For performance, use word-to-token ratio estimation:

```
# Estimation: ~1.3 tokens per word for English text
def estimate_tokens(word_count: int) -> int:
    return int(word_count * 1.3)
```

### Interface

```python
class TokenCounter:
    SOFT_LIMIT = 31_500
    HARD_LIMIT = 35_000
    WORD_TOKEN_RATIO = 1.3

    def count_tokens(self, content: str) -> int:
        """Count tokens in content."""
        ...

    def estimate_tokens(self, word_count: int) -> int:
        """Estimate tokens from word count."""
        return int(word_count * self.WORD_TOKEN_RATIO)

    def is_approaching_limit(self, count: int) -> bool:
        """Check if approaching soft limit."""
        return count >= self.SOFT_LIMIT

    def exceeds_limit(self, count: int) -> bool:
        """Check if hard limit exceeded."""
        return count >= self.HARD_LIMIT
```

### Acceptance Criteria

- [ ] Token counting implemented (accurate or estimation)
- [ ] SOFT_LIMIT = 31,500 tokens defined
- [ ] HARD_LIMIT = 35,000 tokens defined
- [ ] `is_approaching_limit()` returns True at 90%
- [ ] `exceeds_limit()` returns True at 100%
- [ ] Word-to-token estimation available (1.3 ratio)
- [ ] Token count accuracy within 10% of actual

### Test Cases (from EN-015)

Reference test scenarios:
- Short content → well under limits
- Content at 30K tokens → below soft limit
- Content at 32K tokens → above soft limit
- Content at 36K tokens → exceeds hard limit
- Word count estimation vs actual comparison

### Related Items

- Parent: [EN-016: ts-formatter Agent Implementation](./EN-016-ts-formatter.md)
- Blocked By: [TASK-113: Agent alignment](./TASK-113-formatter-agent-alignment.md)
- References: [TDD-ts-formatter.md Section 4](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-formatter.md)
- Blocks: [TASK-116: FileSplitter](./TASK-116-file-splitter.md)
- Validated By: [TASK-136: Formatter tests](../EN-015-transcript-validation/TASK-136-formatter-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-formatter.md TokenCounter section | Agent | skills/transcript/agents/ts-formatter.md |
| Token counting test results | Test Evidence | (link to test output) |

### Verification

- [ ] Soft and hard limits enforced correctly
- [ ] Token counting accuracy acceptable
- [ ] Estimation fallback works
- [ ] Integration with FileSplitter verified
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-016 |

