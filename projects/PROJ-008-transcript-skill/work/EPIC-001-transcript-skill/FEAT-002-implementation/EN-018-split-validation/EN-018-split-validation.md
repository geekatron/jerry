# Enabler: EN-018 - Split Validation Testing

> **Enabler ID:** EN-018
> **Status:** done
> **Priority:** high
> **Feature:** [FEAT-002-implementation](../FEAT-002-implementation.md)
> **Gate:** GATE-6
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Validate file splitting behavior in ts-formatter using the large transcript dataset from EN-017. This enabler specifically tests CON-FMT-007 (Split Navigation) and all related split functionality that could not be validated with the small golden dataset.

---

## Motivation

### Problem Statement

Contract test CON-FMT-007 (Split Navigation) was identified as untestable during EN-016 GATE-5 quality reviews because the existing golden dataset (~1,588 tokens) is far below the split thresholds (31.5K soft, 35K hard).

### Business Value

- Validates ADR-004 (File Splitting Strategy) implementation
- Ensures ts-formatter handles large transcripts correctly
- Completes CON-FMT-007 contract test execution
- Provides confidence for production use with large transcripts

---

## Scope

### In Scope

- [x] Test TokenCounter threshold detection ✓
- [x] Test FileSplitter semantic boundary detection ✓
- [x] Test SplitNavigation link generation ✓
- [x] Test _anchors.json split tracking ✓
- [x] Execute CON-FMT-007 contract test ✓
- [x] Document split validation evidence ✓

### Out of Scope

- Creating test transcripts (EN-017)
- Modifying ts-formatter agent
- Testing non-split behavior

---

## Acceptance Criteria

### AC-1: Token Threshold Tests (CORRECTED per DISC-008)
- [x] TokenCounter correctly identifies meeting-004 as NO split required (~18.6K MD tokens) ✓
- [x] TokenCounter correctly identifies meeting-005 as NO split required (~28.9K MD tokens) ✓
- [x] TokenCounter correctly identifies meeting-006 as 2-split required (~63.2K MD tokens) ✓

**Note:** Original expectations used DISC-006 VTT formula. Corrected to use ts-formatter Markdown formula per [DISC-008](../FEAT-002--DISC-008-token-formula-discrepancy.md).

### AC-2: Boundary Detection Tests
- [x] FileSplitter splits at ## heading boundaries ✓
- [x] Split points preserve semantic coherence ✓
- [x] No mid-segment splits occur ✓

### AC-3: Navigation Link Tests
- [x] Split files contain "Continue in Part X" links ✓
- [x] Links use correct relative paths ✓
- [x] Links point to valid anchors ✓

### AC-4: Anchor Tracking Tests
- [x] _anchors.json tracks entities across split files ✓
- [x] File references are correct for split content ✓
- [x] Line numbers are accurate within each split file ✓

### AC-5: CON-FMT-007 Execution (CORRECTED per DISC-008)
- [x] ~~Contract test passes for meeting-005 (1 split)~~ → meeting-005 does NOT trigger split ✓
- [x] Contract test passes for meeting-006 (2-split) ✓
- [x] Evidence documented in validation report ✓
- [x] Test coverage gap documented (EN-019 required for full coverage) ✓

---

## Technical Design

### Test Matrix (CORRECTED per DISC-008)

| Test Case | Transcript | Words | MD Tokens | Splits | Validation Focus |
|-----------|------------|-------|-----------|--------|------------------|
| SPLIT-001 | meeting-004 | 13,030 | ~18,633 | 0 | Below soft limit (31,500) |
| SPLIT-002 | meeting-005 | 20,202 | ~28,889 | 0 | Below soft limit (31,500) |
| SPLIT-003 | meeting-006 | 44,225 | ~63,242 | 2 | Multi-split, index + 2 parts |

**Token Calculation Formula (ts-formatter, per DISC-008):**
```
md_tokens = word_count × 1.3 × 1.1 = word_count × 1.43
```

**Note:** Original values used DISC-006 VTT formula which includes cue overhead. ts-formatter counts Markdown output tokens, not VTT input. See [DISC-008](../FEAT-002--DISC-008-token-formula-discrepancy.md).

**ADR-004 Thresholds:**
- Soft Limit: 31,500 tokens (triggers split)
- Hard Limit: 35,000 tokens

### Test Artifacts

Each test generates:
1. Split file(s) with navigation links
2. _anchors.json with split tracking
3. Index file with split references
4. Validation report

### Expected Split Structure (meeting-006)

```
transcript-meeting-006/
├── 00-index.md
├── 01-summary.md
├── 02-transcript-part-1.md      ← Split 1 (~31.5K tokens)
├── 02-transcript-part-2.md      ← Split 2 (~31.7K tokens)
├── 03-speakers.md
├── 04-action-items.md
├── 05-decisions.md
├── 06-questions.md
├── 07-topics.md
└── _anchors.json
```

**Note:** meeting-006 at ~63.2K tokens will produce 2 parts (not 3 as originally expected with VTT formula).

---

## Tasks

| ID | Task | Status | Depends On |
|----|------|--------|------------|
| [TASK-145](./TASK-145-token-threshold-tests.md) | Token Threshold Validation | **done** ✓ | EN-017 ✓ |
| [TASK-146](./TASK-146-boundary-detection-tests.md) | Semantic Boundary Tests | **done** ✓ | TASK-145 ✓ |
| [TASK-147](./TASK-147-navigation-link-tests.md) | Navigation Link Validation | **done** ✓ | TASK-146 ✓ |
| [TASK-148](./TASK-148-anchor-tracking-tests.md) | Anchor Tracking Tests | **done** ✓ | TASK-146 ✓ |
| [TASK-149](./TASK-149-con-fmt-007-execution.md) | CON-FMT-007 Contract Test | **done** ✓ | TASK-147 ✓, TASK-148 ✓ |

### Task Dependency Graph

```
EN-017 (Dataset)
    │
    ▼
TASK-145 (Thresholds)
    │
    ▼
TASK-146 (Boundaries)
    │
    ├──► TASK-147 (Navigation)
    │
    └──► TASK-148 (Anchors)
              │
              ▼
        TASK-149 (CON-FMT-007)
              │
              ▼
           GATE-6
```

---

## Dependencies

### Depends On

| Item | Relationship | Status |
|------|--------------|--------|
| [EN-017](../EN-017-large-transcript-dataset/EN-017-large-transcript-dataset.md) | Large transcript dataset | **complete** |
| [EN-016](../EN-016-ts-formatter/EN-016-ts-formatter.md) | ts-formatter implementation | complete |
| [DEC-004](../FEAT-002--DEC-004-split-testing-enablers.md) | Decision documented | complete |
| [ADR-004](../../../../../docs/adrs/ADR-004-file-splitting.md) | Split strategy specification | complete |

### Blocks

| Item | Relationship |
|------|--------------|
| GATE-6 | Split validation required for gate |

---

## Quality Gates

### GATE-6 Requirements (Split Validation)

- [x] All threshold tests pass ✓ (TASK-145)
- [x] Boundary detection validated ✓ (TASK-146)
- [x] Navigation links verified ✓ (TASK-147)
- [x] Anchor tracking confirmed ✓ (TASK-148)
- [x] CON-FMT-007 contract test passes ✓ (TASK-149)

---

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Split logic has bugs | High | Medium | Testing with meeting-006 (~63K tokens) |
| Anchor tracking fails | High | Low | Explicit verification tests |
| Navigation links break | Medium | Low | Relative path validation |
| **Test coverage gap** | Medium | **Realized** | EN-019 will extend meeting-004/005 |

**Test Coverage Gap (DISC-008):** Only meeting-006 triggers splits. meeting-004 and meeting-005 are below the 31.5K soft limit with the correct Markdown formula. EN-019 required to achieve full test coverage.

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Decision | [DEC-004](../FEAT-002--DEC-004-split-testing-enablers.md) | Split testing decision |
| Discovery | [DISC-008](../FEAT-002--DISC-008-token-formula-discrepancy.md) | Token formula discrepancy |
| Contract Test | [contract-tests.yaml](../../../../../skills/transcript/test_data/validation/contract-tests.yaml) | CON-FMT-007 definition |
| ADR | [ADR-004](../../../../../docs/adrs/ADR-004-file-splitting.md) | Split strategy |
| Dataset | [EN-017](../EN-017-large-transcript-dataset/EN-017-large-transcript-dataset.md) | Large transcripts |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial enabler created per DEC-004 |
| 2026-01-28 | Claude | **CORRECTED:** Updated token counts per DISC-008 discovery (VTT→MD formula) |
| 2026-01-28 | Claude | **COMPLETE:** All 5 tasks done, GATE-6 requirements met, CON-FMT-007 verified |
