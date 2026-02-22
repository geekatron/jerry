# SPIKE-003: Validation Spikes — OQ-9 + Method C

> **Type:** spike
> **Status:** completed
> **Priority:** high
> **Impact:** medium
> **Created:** 2026-02-19
> **Parent:** FEAT-001
> **Owner:** Claude
> **Completed:** 2026-02-21
> **Effort:** 3h (timebox)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Research questions and scope |
| [Acceptance Criteria](#acceptance-criteria) | Exit criteria |
| [Dependencies](#dependencies) | Relationships |
| [History](#history) | Status changes |

---

## Content

### Research Questions

1. **OQ-9:** How accurate is `JsonlTranscriptReader`'s `input_tokens` field compared to reference sources (ECW status line, TokenCounter tiktoken)?
2. **OQ-1 (Method C):** Can the status line state file (`~/.claude/ecw-statusline-state.json`) be extended with `context_fill_percentage`? Does it update before `UserPromptSubmit` fires?

### Timebox

| Aspect | Value |
|--------|-------|
| Timebox | 3 hours |
| Start | TBD |

---

## Acceptance Criteria

- [x] OQ-9: Report documenting `JsonlTranscriptReader` accuracy with measured divergence
- [x] Method C: Report documenting timing test results
- [x] Method C: If feasible, prototype committed (DEFERRED — Method A superior, no prototype needed)
- [x] Both reports include recommendation: proceed/defer/abandon
- [x] Timebox respected (3 hours max)

---

## Dependencies

**Depends On:** EN-004 (JsonlTranscriptReader must exist to validate)

**Enables:** May upgrade JsonlTranscriptReader to use Method C data

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Spike created from CWI-08. |
| 2026-02-21 | Claude | done | Spike completed. OQ-9: BLOCKER found — JsonlTranscriptReader corrected (three-field sum, nested path). Method C: DEFERRED — Method A superior. Report at orchestration/feat001-impl-20260220-001/impl/phase-4-cli-rules/spike-003-exec/spike-003-validation-report.md. Corrections applied to JsonlTranscriptReader, ITranscriptReader port, and test fixtures. |
