# Enabler: EN-019 - Large Transcript Dataset Extension

> **Enabler ID:** EN-019
> **Status:** pending
> **Priority:** high
> **Feature:** [FEAT-002-implementation](../FEAT-002-implementation.md)
> **Gate:** GATE-6
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Extend meeting-004 and meeting-005 transcripts to proper word counts that will trigger file splitting in ts-formatter. This corrective enabler addresses the test coverage gap identified in [DISC-008](../FEAT-002--DISC-008-token-formula-discrepancy.md).

---

## Motivation

### Problem Statement

DISC-008 discovered that the EN-017 dataset was sized using the VTT input token formula (DISC-006), but ts-formatter uses a Markdown output token formula. As a result:

| Transcript | Current Words | Current MD Tokens | Split Trigger? | Issue |
|------------|---------------|-------------------|----------------|-------|
| meeting-004 | 13,030 | 18,633 | NO | 58.2% of soft limit - intended as "near-limit" |
| meeting-005 | 20,202 | 28,889 | NO | 91.7% of soft limit - intended as "1-split" |
| meeting-006 | 44,225 | 63,242 | YES | Working as intended - 2 splits |

Only meeting-006 exercises the split functionality, leaving the "near-limit" and "single-split" scenarios untested.

### Business Value

- **Complete CON-FMT-007 test coverage** - All split scenarios tested
- **Validate split boundary behavior** - Near-limit behavior verified
- **Enable comprehensive regression testing** - Full dataset for future changes
- **Quality assurance** - Mission-critical split logic fully validated

---

## Scope

### In Scope

- [ ] Extend meeting-004 to ~22K+ words (trigger threshold)
- [ ] Extend meeting-005 to ~25K+ words (single split)
- [ ] Validate extended transcripts are syntactically valid VTT
- [ ] Update EN-017 dataset documentation with new sizes
- [ ] Re-run EN-018 validation tests on extended dataset

### Out of Scope

- Creating new transcripts (uses existing EN-017 base)
- Modifying ts-formatter agent
- Changing ADR-004 split thresholds

---

## Technical Design

### Target Word Counts

**ADR-004 Thresholds:**
- Soft Limit: 31,500 tokens
- Hard Limit: 35,000 tokens

**ts-formatter Formula:**
```
md_tokens = word_count × 1.3 × 1.1 = word_count × 1.43
```

**Required Word Counts:**
```
Threshold Target            = Token Target / 1.43
Soft Limit (31,500 tokens)  = 22,028 words minimum
Hard Limit (35,000 tokens)  = 24,476 words minimum
1-Split (36,000+ tokens)    = 25,175 words minimum
```

### Extension Matrix

| Transcript | Current | Target | Extension | Result |
|------------|---------|--------|-----------|--------|
| meeting-004 | 13,030 | 22,500 | +9,470 words | ~32,175 tokens (soft limit test) |
| meeting-005 | 20,202 | 26,000 | +5,798 words | ~37,180 tokens (1-split test) |

### Extension Approach

1. **meeting-004 (Sprint Planning):**
   - Add detailed backlog refinement discussion
   - Include technical deep-dives on implementation approaches
   - Extend Q&A sections with additional dialogue
   - **Caution:** Maintain realistic speaker attribution patterns

2. **meeting-005 (Roadmap Review):**
   - Add quarterly business review discussion
   - Include stakeholder feedback segments
   - Extend strategic planning conversations
   - **Caution:** Preserve multi-speaker dynamics

### Expected Split Structure (After Extension)

**meeting-004 (at ~32K tokens):**
```
transcript-meeting-004/
├── 00-index.md
├── 01-summary.md
├── 02-transcript.md           ← Single file (just above soft limit)
├── 03-speakers.md
├── 04-action-items.md
├── 05-decisions.md
├── 06-questions.md
├── 07-topics.md
└── _anchors.json
```

**meeting-005 (at ~37K tokens):**
```
transcript-meeting-005/
├── 00-index.md
├── 01-summary.md
├── 02-transcript-part-1.md    ← Split 1 (~31.5K tokens)
├── 02-transcript-part-2.md    ← Split 2 (~5.7K tokens)
├── 03-speakers.md
├── 04-action-items.md
├── 05-decisions.md
├── 06-questions.md
├── 07-topics.md
└── _anchors.json
```

---

## Tasks

| ID | Task | Status | Depends On | Effort |
|----|------|--------|------------|--------|
| [TASK-160](./TASK-160-extend-meeting-004.md) | Extend meeting-004 to ~22.5K words | pending | - | 2 SP |
| [TASK-161](./TASK-161-extend-meeting-005.md) | Extend meeting-005 to ~26K words | pending | - | 2 SP |
| [TASK-162](./TASK-162-validate-extended-transcripts.md) | Validate VTT syntax and structure | pending | TASK-160, TASK-161 | 1 SP |
| [TASK-163](./TASK-163-update-dataset-documentation.md) | Update EN-017 documentation | pending | TASK-162 | 1 SP |

### Task Dependency Graph

```
TASK-160 (Extend meeting-004)
    │
    ├──────────────────────────┐
    │                          │
    ▼                          ▼
TASK-162 (Validate)    TASK-161 (Extend meeting-005)
    │                          │
    └──────────┬───────────────┘
               │
               ▼
        TASK-163 (Documentation)
               │
               ▼
            GATE-6
```

---

## Acceptance Criteria

### AC-1: meeting-004 Extension
- [ ] Word count reaches 22,000+ words
- [ ] VTT syntax valid (timestamps, cues, speakers)
- [ ] Content thematically consistent (sprint planning)
- [ ] Speaker attribution realistic

### AC-2: meeting-005 Extension
- [ ] Word count reaches 25,500+ words
- [ ] VTT syntax valid (timestamps, cues, speakers)
- [ ] Content thematically consistent (roadmap review)
- [ ] Speaker attribution realistic

### AC-3: Validation
- [ ] Both extended transcripts parse successfully with ts-parser
- [ ] Token counts within expected ranges
- [ ] No VTT format errors

### AC-4: Documentation
- [ ] EN-017 dataset documentation updated with new sizes
- [ ] DISC-008 marked as resolved
- [ ] Test coverage gap closed

---

## Dependencies

### Depends On

| Item | Relationship | Status |
|------|--------------|--------|
| [DISC-008](../FEAT-002--DISC-008-token-formula-discrepancy.md) | Identified this corrective work | **documented** |
| [EN-017](../EN-017-large-transcript-dataset/EN-017-large-transcript-dataset.md) | Base transcripts to extend | **complete** |
| [EN-018](../EN-018-split-validation/EN-018-split-validation.md) | Split validation tests | **complete** |

### Blocks

| Item | Relationship |
|------|--------------|
| Full CON-FMT-007 Coverage | Enables complete split scenario testing |
| GATE-6 | Contributes to gate readiness |

---

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Extended content unrealistic | Medium | Low | Review speaker dynamics, topic flow |
| VTT parsing errors | High | Low | Validate with ts-parser before use |
| Semantic coherence breaks | Medium | Medium | Extend logically, maintain context |
| Token count calculation drift | Low | Low | Verify with formula after extension |

---

## Quality Gates

### Pre-Extension Checks
- [ ] Current word counts verified via `wc -w`
- [ ] Target word counts calculated correctly
- [ ] Extension approach documented

### Post-Extension Checks
- [ ] Extended VTT files parse without errors
- [ ] Word counts match targets (within 5%)
- [ ] Token calculations within expected ranges
- [ ] ts-parser produces valid canonical JSON

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Discovery | [DISC-008](../FEAT-002--DISC-008-token-formula-discrepancy.md) | Token formula discrepancy |
| Parent Dataset | [EN-017](../EN-017-large-transcript-dataset/EN-017-large-transcript-dataset.md) | Original large transcripts |
| Validation | [EN-018](../EN-018-split-validation/EN-018-split-validation.md) | Split validation tests |
| ADR | [ADR-004](../../../../../docs/adrs/ADR-004-file-splitting.md) | Split strategy |
| Agent | [ts-formatter](../../../../../skills/transcript/agents/ts-formatter.md) | Formatter with split logic |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial enabler created per DISC-008 corrective work |
