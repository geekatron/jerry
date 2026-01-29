# Enabler: EN-018 - Split Validation Testing

> **Enabler ID:** EN-018
> **Status:** pending
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

- [ ] Test TokenCounter threshold detection
- [ ] Test FileSplitter semantic boundary detection
- [ ] Test SplitNavigation link generation
- [ ] Test _anchors.json split tracking
- [ ] Execute CON-FMT-007 contract test
- [ ] Document split validation evidence

### Out of Scope

- Creating test transcripts (EN-017)
- Modifying ts-formatter agent
- Testing non-split behavior

---

## Acceptance Criteria

### AC-1: Token Threshold Tests
- [ ] TokenCounter correctly identifies meeting-004 as NO split required
- [ ] TokenCounter correctly identifies meeting-005 as 1 split required
- [ ] TokenCounter correctly identifies meeting-006 as 2-3 splits required

### AC-2: Boundary Detection Tests
- [ ] FileSplitter splits at ## heading boundaries
- [ ] Split points preserve semantic coherence
- [ ] No mid-segment splits occur

### AC-3: Navigation Link Tests
- [ ] Split files contain "Continue in Part X" links
- [ ] Links use correct relative paths
- [ ] Links point to valid anchors

### AC-4: Anchor Tracking Tests
- [ ] _anchors.json tracks entities across split files
- [ ] File references are correct for split content
- [ ] Line numbers are accurate within each split file

### AC-5: CON-FMT-007 Execution
- [ ] Contract test passes for meeting-005 (1 split)
- [ ] Contract test passes for meeting-006 (multi-split)
- [ ] Evidence documented in validation report

---

## Technical Design

### Test Matrix

| Test Case | Transcript | Token Count | Splits | Validation Focus |
|-----------|------------|-------------|--------|------------------|
| SPLIT-001 | meeting-004 | ~25K | 0 | Near-limit behavior |
| SPLIT-002 | meeting-005 | ~45K | 1 | Single split |
| SPLIT-003 | meeting-006 | ~90K | 2-3 | Multi-split |

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
├── 02-transcript-part-1.md      ← Split 1
├── 02-transcript-part-2.md      ← Split 2
├── 02-transcript-part-3.md      ← Split 3 (if needed)
├── 03-speakers.md
├── 04-action-items.md
├── 05-decisions.md
├── 06-questions.md
├── 07-topics.md
└── _anchors.json
```

---

## Tasks

| ID | Task | Status | Depends On |
|----|------|--------|------------|
| [TASK-145](./TASK-145-token-threshold-tests.md) | Token Threshold Validation | pending | EN-017 |
| [TASK-146](./TASK-146-boundary-detection-tests.md) | Semantic Boundary Tests | pending | TASK-145 |
| [TASK-147](./TASK-147-navigation-link-tests.md) | Navigation Link Validation | pending | TASK-146 |
| [TASK-148](./TASK-148-anchor-tracking-tests.md) | Anchor Tracking Tests | pending | TASK-146 |
| [TASK-149](./TASK-149-con-fmt-007-execution.md) | CON-FMT-007 Contract Test | pending | TASK-147, TASK-148 |

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
| [EN-017](../EN-017-large-transcript-dataset/EN-017-large-transcript-dataset.md) | Large transcript dataset | pending |
| [EN-016](../EN-016-ts-formatter/EN-016-ts-formatter.md) | ts-formatter implementation | complete |
| [DEC-004](../FEAT-002--DEC-004-split-testing-enablers.md) | Decision documented | complete |

### Blocks

| Item | Relationship |
|------|--------------|
| GATE-6 | Split validation required for gate |

---

## Quality Gates

### GATE-6 Requirements (Split Validation)

- [ ] All threshold tests pass
- [ ] Boundary detection validated
- [ ] Navigation links verified
- [ ] Anchor tracking confirmed
- [ ] CON-FMT-007 contract test passes

---

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Split logic has bugs | High | Medium | Thorough testing with 3 transcript sizes |
| Anchor tracking fails | High | Low | Explicit verification tests |
| Navigation links break | Medium | Low | Relative path validation |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Decision | [DEC-004](../FEAT-002--DEC-004-split-testing-enablers.md) | Split testing decision |
| Contract Test | [contract-tests.yaml](../../../../../skills/transcript/test_data/validation/contract-tests.yaml) | CON-FMT-007 definition |
| ADR | [ADR-004](../../../../../docs/adrs/ADR-004-file-splitting-strategy.md) | Split strategy |
| Dataset | [EN-017](../EN-017-large-transcript-dataset/EN-017-large-transcript-dataset.md) | Large transcripts |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial enabler created per DEC-004 |
