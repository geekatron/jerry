# Enabler: EN-017 - Large Transcript Dataset

> **Enabler ID:** EN-017
> **Status:** pending
> **Priority:** high
> **Feature:** [FEAT-002-implementation](../FEAT-002-implementation.md)
> **Gate:** GATE-6
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Create a golden dataset of 3 large synthetic transcripts of varying sizes to enable comprehensive testing of file splitting behavior in ts-formatter. This dataset addresses the gap identified in EN-016 GATE-5 quality reviews where CON-FMT-007 (Split Navigation) could not be tested.

---

## Motivation

### Problem Statement

The current golden dataset (`meeting-001.vtt`, ~8 minutes, ~1,588 tokens) is significantly below the token thresholds that trigger file splitting:
- **Soft Limit:** 31,500 tokens
- **Hard Limit:** 35,000 tokens

Without transcripts exceeding these limits, we cannot validate split behavior.

### Business Value

- Enables comprehensive validation of file splitting logic
- Provides reusable test infrastructure for future testing
- Ensures ts-formatter handles large transcripts correctly
- Validates ADR-004 (File Splitting Strategy) implementation

---

## Scope

### In Scope

- [ ] Design dataset with token targets and topic variation
- [ ] Create meeting-004-sprint-planning.vtt (~45 min, ~25K tokens)
- [ ] Create meeting-005-roadmap-review.vtt (~90 min, ~45K tokens)
- [ ] Create meeting-006-all-hands.vtt (~3 hrs, ~90K tokens)
- [ ] Validate all transcripts meet W3C WebVTT specification
- [ ] Document token counts and expected split behavior

### Out of Scope

- Actual validation/testing of split behavior (EN-018)
- Modifications to ts-formatter agent
- Changes to existing golden dataset

---

## Acceptance Criteria

### AC-1: Dataset Design Complete
- [ ] Token targets documented for each transcript
- [ ] Topic domains defined with rationale
- [ ] Speaker roster defined for each transcript
- [ ] Expected entity counts estimated

### AC-2: meeting-004.vtt Created (~25K tokens)
- [ ] Duration ~45 minutes
- [ ] Token count between 22K-28K (near soft limit)
- [ ] Topic: Engineering sprint planning
- [ ] Valid W3C WebVTT format
- [ ] Contains realistic entity distribution

### AC-3: meeting-005.vtt Created (~45K tokens)
- [ ] Duration ~90 minutes
- [ ] Token count between 42K-48K (triggers 1 split)
- [ ] Topic: Product roadmap review
- [ ] Valid W3C WebVTT format
- [ ] Contains realistic entity distribution

### AC-4: meeting-006.vtt Created (~90K tokens)
- [ ] Duration ~3 hours
- [ ] Token count between 85K-95K (triggers 2-3 splits)
- [ ] Topic: Quarterly all-hands meeting
- [ ] Valid W3C WebVTT format
- [ ] Contains realistic entity distribution

### AC-5: Dataset Validated
- [ ] All transcripts pass ts-parser validation
- [ ] Token counts verified with TokenCounter
- [ ] Expected splits documented
- [ ] Test data README updated

---

## Technical Design

### Token Estimation Formula

```
estimated_tokens = (word_count × 1.3) × 1.1
```

Where:
- 1.3 = average tokens per word
- 1.1 = 10% buffer for formatting

### Transcript Specifications

| ID | File | Duration | Words | Est. Tokens | Topic | Splits |
|----|------|----------|-------|-------------|-------|--------|
| 004 | meeting-004-sprint-planning.vtt | ~45 min | ~8,000 | ~25K | Engineering | 0 |
| 005 | meeting-005-roadmap-review.vtt | ~90 min | ~15,000 | ~45K | Product | 1 |
| 006 | meeting-006-all-hands.vtt | ~180 min | ~30,000 | ~90K | Mixed | 2-3 |

### Speaker Rosters

**meeting-004 (Sprint Planning):**
- Scrum Master (facilitator)
- 4 Engineers (dev team)
- Product Owner

**meeting-005 (Roadmap Review):**
- VP Product (facilitator)
- 3 Product Managers
- 2 Engineering Leads
- 1 Designer

**meeting-006 (All-Hands):**
- CEO (facilitator)
- CTO (presenter)
- VP Engineering (presenter)
- VP Product (presenter)
- 5+ audience members (questions)

### Expected Entity Distribution

| Entity Type | meeting-004 | meeting-005 | meeting-006 |
|-------------|-------------|-------------|-------------|
| Speakers | 6 | 7 | 9+ |
| Topics | 3-4 | 4-5 | 6-8 |
| Action Items | 8-12 | 10-15 | 15-20 |
| Decisions | 2-3 | 4-6 | 5-8 |
| Questions | 5-8 | 8-12 | 12-18 |

### File Location

```
skills/transcript/test_data/input/
├── meeting-001.vtt                    # Existing (~8 min)
├── meeting-002.vtt                    # Existing
├── meeting-003-plain.txt              # Existing
├── meeting-004-sprint-planning.vtt    # NEW (~45 min)
├── meeting-005-roadmap-review.vtt     # NEW (~90 min)
└── meeting-006-all-hands.vtt          # NEW (~3 hrs)
```

---

## Tasks

| ID | Task | Status | Depends On |
|----|------|--------|------------|
| [TASK-140](./TASK-140-dataset-design.md) | Dataset Design & Planning | pending | - |
| [TASK-141](./TASK-141-meeting-004-creation.md) | Create meeting-004-sprint-planning.vtt | pending | TASK-140 |
| [TASK-142](./TASK-142-meeting-005-creation.md) | Create meeting-005-roadmap-review.vtt | pending | TASK-140 |
| [TASK-143](./TASK-143-meeting-006-creation.md) | Create meeting-006-all-hands.vtt | pending | TASK-140 |
| [TASK-144](./TASK-144-dataset-validation.md) | Validate Dataset & Update Documentation | pending | TASK-141, TASK-142, TASK-143 |

### Task Dependency Graph

```
TASK-140 (Design)
    │
    ├──► TASK-141 (meeting-004)
    │
    ├──► TASK-142 (meeting-005)
    │
    └──► TASK-143 (meeting-006)
              │
              ▼
        TASK-144 (Validation)
              │
              ▼
           EN-018
```

---

## Dependencies

### Depends On

| Item | Relationship | Status |
|------|--------------|--------|
| [EN-016](../EN-016-ts-formatter/EN-016-ts-formatter.md) | GATE-5 passed | complete |
| [DEC-004](../FEAT-002--DEC-004-split-testing-enablers.md) | Decision documented | complete |
| [ADR-004](../../../../../docs/adrs/ADR-004-file-splitting-strategy.md) | Token limits defined | complete |

### Blocks

| Item | Relationship |
|------|--------------|
| [EN-018](../EN-018-split-validation/EN-018-split-validation.md) | Cannot validate without dataset |
| GATE-6 | Transitively blocked |

---

## Quality Gates

### GATE-6 Requirements

- [ ] All 3 transcripts created and validated
- [ ] Token counts verified
- [ ] W3C WebVTT compliance verified
- [ ] ts-parser successfully parses all transcripts
- [ ] Expected split counts documented

---

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Token estimates inaccurate | Medium | Low | Verify with TokenCounter during creation |
| Transcripts unrealistic | Low | Low | Use realistic entity distributions |
| WebVTT format errors | Medium | Low | Validate with ts-parser during creation |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Decision | [DEC-004](../FEAT-002--DEC-004-split-testing-enablers.md) | Decision to create split testing enablers |
| ADR | [ADR-004](../../../../../docs/adrs/ADR-004-file-splitting-strategy.md) | File splitting strategy |
| Orchestration | [ORCHESTRATION.yaml](../ORCHESTRATION.yaml) | Execution tracking |
| Test Data | `skills/transcript/test_data/input/` | Golden dataset location |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial enabler created per DEC-004 |
