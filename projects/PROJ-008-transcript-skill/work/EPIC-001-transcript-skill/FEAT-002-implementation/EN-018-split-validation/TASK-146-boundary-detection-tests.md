# Task: TASK-146 - Semantic Boundary Detection Tests

> **Task ID:** TASK-146
> **Status:** pending
> **Priority:** high
> **Enabler:** [EN-018-split-validation](./EN-018-split-validation.md)
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Validate that FileSplitter correctly detects and splits at semantic boundaries (## headings) as specified in ADR-004.

---

## Acceptance Criteria

- [ ] **AC-1:** Splits occur at ## heading boundaries
- [ ] **AC-2:** No splits occur mid-paragraph or mid-segment
- [ ] **AC-3:** Each split file starts with a valid heading
- [ ] **AC-4:** Semantic coherence preserved within each split
- [ ] **AC-5:** Split points documented with line numbers

---

## Technical Specifications

### Semantic Boundary Definition (ADR-004)

```markdown
## Topic Section Header  ← Valid split point

Content continues...

## Next Topic Section    ← Valid split point
```

### Invalid Split Points

- Mid-paragraph
- Mid-segment (speaker turn)
- Mid-sentence
- Within code blocks
- Within lists

### Validation Criteria

| Check | Description |
|-------|-------------|
| BOUND-001 | Split starts at ## heading |
| BOUND-002 | Previous split ends at paragraph break |
| BOUND-003 | No orphaned content |
| BOUND-004 | Topic coherence within split |

---

## Unit of Work

### Step 1: Process meeting-005 (1 split)
- Run ts-formatter on meeting-005
- Examine split point location
- Verify ## heading at split

### Step 2: Process meeting-006 (2-3 splits)
- Run ts-formatter on meeting-006
- Examine all split point locations
- Verify ## headings at each split

### Step 3: Validate Split Content
- Check each split file structure
- Verify no mid-segment breaks
- Confirm topic coherence

### Step 4: Document Boundary Detection
- Record split points with line numbers
- Document heading at each split
- Create evidence summary

---

## Dependencies

### Depends On
- TASK-145 (Token Threshold Tests)

### Blocks
- TASK-147 (Navigation Link Tests)
- TASK-148 (Anchor Tracking Tests)

---

## Verification Evidence

| Criterion | Evidence Required |
|-----------|-------------------|
| AC-1 | Split file headers showing ## |
| AC-2 | Confirmation of no mid-content splits |
| AC-3 | First line of each split file |
| AC-4 | Content review summary |
| AC-5 | Split point line number documentation |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial task created |
