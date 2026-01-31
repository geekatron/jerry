# Task: TASK-161 - Extend meeting-005 to ~26K Words

> **Task ID:** TASK-161
> **Status:** pending
> **Priority:** high
> **Enabler:** [EN-019-dataset-extension](./EN-019-dataset-extension.md)
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Extend the meeting-005-roadmap-review.vtt transcript from ~20,202 words to ~26,000 words to trigger a single file split in ts-formatter (~37,180 Markdown tokens).

---

## Acceptance Criteria

- [ ] **AC-1:** Word count reaches 25,500+ words (target: 26,000)
- [ ] **AC-2:** VTT syntax remains valid (timestamps, cues, speakers)
- [ ] **AC-3:** Content thematically consistent (roadmap review context)
- [ ] **AC-4:** Multi-speaker dynamics preserved
- [ ] **AC-5:** Extended content parseable by ts-parser

---

## Technical Specifications

### Current State

| Metric | Value |
|--------|-------|
| Current Words | 20,202 |
| Target Words | 26,000 |
| Extension Required | +5,798 words |
| Current MD Tokens | 28,889 (~92% of soft limit) |
| Target MD Tokens | ~37,180 (~118% of soft limit) |

### Formula

```
md_tokens = words × 1.43
37,180 = 26,000 × 1.43
```

### Split Expectation

At ~37,180 tokens, meeting-005 will trigger exactly **1 split**:
- Part 1: ~31,500 tokens (split at ## heading)
- Part 2: ~5,680 tokens (remainder)

This provides the "single split" test scenario not currently covered by the dataset.

---

## Unit of Work

### Step 1: Analyze Existing Content Structure
- Review current roadmap topics
- Identify natural extension points
- Map multi-speaker dynamics

### Step 2: Plan Extension Content
- Add quarterly business review sections
- Include stakeholder feedback discussions
- Extend strategic planning conversations
- Add detailed Q&A rounds

### Step 3: Generate Extended Content
- Add ~5,798 words of thematically consistent content
- Maintain VTT format (timestamps, speaker tags)
- Preserve multi-speaker dynamics (3+ active speakers)

### Step 4: Validate Extension
- Verify word count with `wc -w`
- Parse with ts-parser to confirm valid VTT
- Calculate expected token count and split point

---

## Dependencies

### Depends On
- [EN-017](../EN-017-large-transcript-dataset/EN-017-large-transcript-dataset.md) - Original transcript

### Blocks
- TASK-162 (Validation)

---

## Evidence

| Criterion | Evidence Required | Status |
|-----------|-------------------|--------|
| AC-1 | `wc -w` output showing 25,500+ | pending |
| AC-2 | ts-parser successful parse | pending |
| AC-3 | Content review summary | pending |
| AC-4 | Multi-speaker analysis | pending |
| AC-5 | Canonical JSON output | pending |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial task created per DISC-008 corrective work |
