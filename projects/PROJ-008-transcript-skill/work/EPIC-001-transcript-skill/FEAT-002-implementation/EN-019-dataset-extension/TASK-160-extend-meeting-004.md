# Task: TASK-160 - Extend meeting-004 to ~22.5K Words

> **Task ID:** TASK-160
> **Status:** pending
> **Priority:** high
> **Enabler:** [EN-019-dataset-extension](./EN-019-dataset-extension.md)
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Extend the meeting-004-sprint-planning.vtt transcript from ~13,030 words to ~22,500 words to trigger the ts-formatter soft split threshold (~32,175 Markdown tokens).

---

## Acceptance Criteria

- [ ] **AC-1:** Word count reaches 22,000+ words (target: 22,500)
- [ ] **AC-2:** VTT syntax remains valid (timestamps, cues, speakers)
- [ ] **AC-3:** Content thematically consistent (sprint planning context)
- [ ] **AC-4:** Speaker attribution patterns remain realistic
- [ ] **AC-5:** Extended content parseable by ts-parser

---

## Technical Specifications

### Current State

| Metric | Value |
|--------|-------|
| Current Words | 13,030 |
| Target Words | 22,500 |
| Extension Required | +9,470 words |
| Current MD Tokens | 18,633 (~59% of soft limit) |
| Target MD Tokens | ~32,175 (~102% of soft limit) |

### Formula

```
md_tokens = words × 1.43
32,175 = 22,500 × 1.43
```

### Split Expectation

At ~32,175 tokens, meeting-004 will be **just above the soft limit** (31,500), providing a valuable edge case for split threshold testing. This tests the "near-limit" behavior where splitting may or may not trigger depending on heading positions.

---

## Unit of Work

### Step 1: Analyze Existing Content Structure
- Review current sprint planning topics
- Identify natural extension points
- Map speaker patterns and dynamics

### Step 2: Plan Extension Content
- Add detailed backlog refinement discussions
- Include technical implementation deep-dives
- Extend Q&A and discussion sections
- Add retrospective items from previous sprint

### Step 3: Generate Extended Content
- Add ~9,470 words of thematically consistent content
- Maintain VTT format (timestamps, speaker tags)
- Preserve realistic meeting flow

### Step 4: Validate Extension
- Verify word count with `wc -w`
- Parse with ts-parser to confirm valid VTT
- Calculate expected token count

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
| AC-1 | `wc -w` output showing 22,000+ | pending |
| AC-2 | ts-parser successful parse | pending |
| AC-3 | Content review summary | pending |
| AC-4 | Speaker attribution analysis | pending |
| AC-5 | Canonical JSON output | pending |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial task created per DISC-008 corrective work |
