# TASK-116: Implement/Verify FileSplitter (ADR-004)

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-016 (ts-formatter Agent Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-116"
work_type: TASK
title: "Implement/Verify FileSplitter (ADR-004)"
description: |
  Implement and verify the FileSplitter component that splits large
  files at semantic boundaries per ADR-004.

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
  - "file-splitting"
  - "ADR-004"

effort: 2
acceptance_criteria: |
  - Semantic boundary splitting at ## headings
  - Split files maintain navigation context
  - Previous/next links between split parts
  - No orphaned anchors across splits

due_date: null

activity: DEVELOPMENT
original_estimate: 4
remaining_work: 4
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Content

### Description

Implement and verify the FileSplitter component that splits files exceeding the token limit at semantic boundaries (## headings) per ADR-004. This ensures large transcripts remain navigable.

### Semantic Boundary Splitting (ADR-004)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      SEMANTIC BOUNDARY SPLITTING                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ALGORITHM:                                                                  │
│                                                                              │
│  1. Monitor token count while building file                                  │
│  2. When approaching SOFT_LIMIT (31,500):                                    │
│     - Find next ## heading boundary                                          │
│     - Split BEFORE that heading                                              │
│  3. If HARD_LIMIT reached without ## heading:                                │
│     - Split at paragraph boundary                                            │
│     - Or at sentence boundary as last resort                                 │
│                                                                              │
│                                                                              │
│  EXAMPLE SPLIT:                                                              │
│  ──────────────                                                              │
│                                                                              │
│  BEFORE (02-transcript.md - 45K tokens):                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ # Transcript                                                         │    │
│  │                                                                       │    │
│  │ ## 00:00:00 - 00:15:00                                               │    │
│  │ [content ~15K tokens]                                                │    │
│  │                                                                       │    │
│  │ ## 00:15:00 - 00:30:00                                               │    │
│  │ [content ~15K tokens]                                                │    │
│  │                                                                       │    │
│  │ ## 00:30:00 - 00:45:00                                               │    │
│  │ [content ~15K tokens]                                                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  AFTER:                                                                      │
│  ┌──────────────────────┐  ┌──────────────────────┐                         │
│  │ 02-transcript-01.md  │  │ 02-transcript-02.md  │                         │
│  │ ~30K tokens          │  │ ~15K tokens          │                         │
│  │                      │  │                      │                         │
│  │ [Navigation header]  │  │ [Navigation header]  │                         │
│  │ Part 1 of 2          │  │ Part 2 of 2          │                         │
│  │ Next: -02.md         │  │ Prev: -01.md         │                         │
│  │                      │  │                      │                         │
│  │ ## 00:00:00-00:15:00 │  │ ## 00:30:00-00:45:00 │                         │
│  │ ## 00:15:00-00:30:00 │  │                      │                         │
│  └──────────────────────┘  └──────────────────────┘                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Split File Naming

```
Original: 02-transcript.md

Split into:
- 02-transcript-01.md (Part 1)
- 02-transcript-02.md (Part 2)
- 02-transcript-03.md (Part 3, if needed)
```

### Navigation Header Template

```markdown
---
part: 1
total_parts: 2
previous: null
next: 02-transcript-02.md
---

# Transcript (Part 1 of 2)

> This file is part of a multi-part transcript. Use the navigation below.
>
> **Navigation:** [Next Part →](02-transcript-02.md)

---
```

### Interface

```python
class FileSplitter:
    def should_split(self, content: str, token_count: int) -> bool:
        """Check if file needs splitting."""
        return token_count >= TokenCounter.SOFT_LIMIT

    def find_split_point(self, content: str, soft_limit: int) -> int:
        """Find semantic boundary before soft limit."""
        # Look for ## heading
        # Fall back to paragraph
        # Fall back to sentence
        ...

    def split_file(
        self,
        content: str,
        base_name: str,
        token_counter: TokenCounter
    ) -> List[SplitFile]:
        """Split file into multiple parts."""
        ...
```

### Anchor Handling

When a file is split, anchors must be updated:

1. **Anchor relocation:** Anchors move to their new file
2. **Index update:** 00-index.md references correct file for each anchor
3. **Cross-references:** Links between split files use relative paths
4. **AnchorRegistry update:** Registry reflects final anchor locations

### Acceptance Criteria

- [ ] Files exceeding soft limit trigger split evaluation
- [ ] Split occurs at ## heading boundary
- [ ] Fallback to paragraph/sentence if no heading
- [ ] Split files have navigation headers
- [ ] Previous/Next links between parts
- [ ] Part numbering (Part N of M) in headers
- [ ] Anchors relocated correctly
- [ ] No split file exceeds hard limit
- [ ] 00-index.md updated with split file references

### Test Cases (from EN-015)

Reference test scenarios:
- Small file (no split needed)
- File at 32K tokens (split at soft limit)
- File with clean ## boundaries
- File without ## headings (paragraph split)
- Very long file (multiple splits)

### Related Items

- Parent: [EN-016: ts-formatter Agent Implementation](./EN-016-ts-formatter.md)
- Blocked By: [TASK-115: TokenCounter](./TASK-115-token-counter.md)
- References: [TDD-ts-formatter.md Section 3](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-formatter.md)
- References: [ADR-004: File Splitting Strategy](../../FEAT-001-analysis-design/EN-004-architecture-decisions/docs/adrs/adr-004.md)
- Validated By: [TASK-136: Formatter tests](../EN-015-transcript-validation/TASK-136-formatter-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-formatter.md FileSplitter section | Agent | skills/transcript/agents/ts-formatter.md |
| File splitting test results | Test Evidence | (link to test output) |

### Verification

- [ ] Semantic boundary detection works
- [ ] Navigation headers included
- [ ] Anchors handled correctly
- [ ] No file exceeds hard limit
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-016 |

