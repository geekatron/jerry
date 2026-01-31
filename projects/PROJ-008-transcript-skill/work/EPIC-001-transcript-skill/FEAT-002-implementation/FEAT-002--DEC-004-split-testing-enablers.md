# Decision: DEC-004 - Create Split Testing Enablers

> **Decision ID:** FEAT-002--DEC-004
> **Status:** ACCEPTED
> **Date:** 2026-01-28
> **Decision Makers:** User, Claude
> **Feature:** FEAT-002-implementation
> **Related Enablers:** EN-016, EN-017, EN-018

---

## Summary

Create two new enablers (EN-017, EN-018) to address the gap identified in EN-016 GATE-5 quality reviews where CON-FMT-007 (Split Navigation) could not be tested because the current golden dataset (meeting-001.vtt) is too small to trigger file splitting.

---

## Context

### Problem Statement

During EN-016 GATE-5 quality reviews (ps-critic scored 0.94, nse-qa scored 0.90), both reviewers identified a critical gap:

> **CON-FMT-007 (Split Navigation)** - The contract test for file splitting behavior cannot be validated because the existing golden dataset `meeting-001.vtt` (~8 minutes, ~1,588 tokens maximum) is significantly below the token thresholds that trigger splitting.

**Token Thresholds (from ADR-004):**
- **Soft Limit:** 31,500 tokens - triggers split at semantic boundaries (## headings)
- **Hard Limit:** 35,000 tokens - forces split regardless of boundary

### Current Golden Dataset

| File | Duration | Est. Tokens | Splits? |
|------|----------|-------------|---------|
| meeting-001.vtt | ~8 min | ~1,588 | NO |

### Gap Analysis

Without transcripts that exceed token limits, we cannot validate:
1. TokenCounter correctly identifies when splitting is needed
2. FileSplitter splits at semantic boundaries (## headings)
3. SplitNavigation links are correctly generated
4. _anchors.json correctly tracks split file locations
5. Index files correctly reference split parts

---

## Decision

**Create TWO enablers with sequential dependency:**

### EN-017: Large Transcript Dataset
Create 3 synthetic transcripts of varying sizes with different topics to comprehensively test split behavior and different context domains.

| Transcript | Duration | Est. Words | Est. Tokens | Expected Splits |
|------------|----------|------------|-------------|-----------------|
| meeting-004.vtt | ~45 min | ~8,000 | ~25K | 0 (near soft limit) |
| meeting-005.vtt | ~90 min | ~15,000 | ~45K | 1 split |
| meeting-006.vtt | ~3 hrs | ~30,000 | ~90K | 2-3 splits |

**Token Estimation Formula:** `(word_count × 1.3) × 1.1`

**Topic Variation (for context testing):**
- meeting-004: Engineering sprint planning (technical context)
- meeting-005: Product roadmap review (business context)
- meeting-006: Quarterly all-hands (mixed context)

### EN-018: Split Validation Testing
Validate split behavior using the large transcripts from EN-017:
1. Verify TokenCounter thresholds
2. Verify FileSplitter semantic boundary detection
3. Verify SplitNavigation link generation
4. Verify _anchors.json split tracking
5. Verify Index file split references
6. Execute contract test CON-FMT-007

---

## Rationale

### Why TWO Enablers?

| Approach | Pros | Cons |
|----------|------|------|
| Single enabler | Fewer artifacts | Mixes concerns, harder to isolate failures |
| **Two enablers** | **Separation of concerns, clear dependencies, reusable dataset** | **More artifacts** |

**Decision:** Two enablers provides cleaner separation - EN-017 is reusable infrastructure that can benefit future testing, EN-018 is specific validation focused on split behavior.

### Why 3 Transcripts?

1. **meeting-004 (~25K tokens):** Tests behavior NEAR soft limit without triggering split - important edge case
2. **meeting-005 (~45K tokens):** Tests single split scenario - the most common case
3. **meeting-006 (~90K tokens):** Tests multiple splits - validates split chaining and navigation

### Why Different Topics?

Different topics enable testing of context injection with varied domains:
- Technical terminology (engineering sprint)
- Business terminology (product roadmap)
- Mixed audience (all-hands meeting)

This provides better coverage for ts-extractor entity recognition and ts-formatter context handling.

---

## Alternatives Considered

### Alternative A: Extend meeting-001.vtt

**Rejected.** Would create an unrealistically long 8-minute meeting with 35K+ tokens of content, violating realistic transcript characteristics.

### Alternative B: Single Large Transcript

**Rejected.** Would not test edge cases (near-limit, single split vs multiple splits).

### Alternative C: External/Real Transcripts

**Rejected.** Privacy concerns, inconsistent format, harder to control test conditions.

---

## Dependencies

```
EN-016 ts-formatter (GATE-5 passed)
    │
    ▼
EN-017 Large Transcript Dataset (GATE-6)
    │
    ▼
EN-018 Split Validation Testing (GATE-6)
    │
    ▼
GATE-6: Integration & Validation Review
```

### Dependency Details

| Enabler | Depends On | Blocks |
|---------|------------|--------|
| EN-017 | EN-016 (GATE-5 passed) | EN-018 |
| EN-018 | EN-017 | GATE-6 |

---

## Implementation Impact

### Files Created

**EN-017:**
- `EN-017-large-transcript-dataset/EN-017-large-transcript-dataset.md`
- `EN-017-large-transcript-dataset/TASK-140-dataset-design.md`
- `EN-017-large-transcript-dataset/TASK-141-meeting-004-creation.md`
- `EN-017-large-transcript-dataset/TASK-142-meeting-005-creation.md`
- `EN-017-large-transcript-dataset/TASK-143-meeting-006-creation.md`
- `EN-017-large-transcript-dataset/TASK-144-dataset-validation.md`

**EN-018:**
- `EN-018-split-validation/EN-018-split-validation.md`
- `EN-018-split-validation/TASK-145-token-threshold-tests.md`
- `EN-018-split-validation/TASK-146-boundary-detection-tests.md`
- `EN-018-split-validation/TASK-147-navigation-link-tests.md`
- `EN-018-split-validation/TASK-148-anchor-tracking-tests.md`
- `EN-018-split-validation/TASK-149-con-fmt-007-execution.md`

**Test Data:**
- `skills/transcript/test_data/input/meeting-004-sprint-planning.vtt`
- `skills/transcript/test_data/input/meeting-005-roadmap-review.vtt`
- `skills/transcript/test_data/input/meeting-006-all-hands.vtt`

### ORCHESTRATION.yaml Updates

```yaml
enablers:
  EN-017:
    name: "Large Transcript Dataset"
    status: pending
    tasks_total: 5
    tasks_complete: 0
    depends_on: [EN-016]
    blocks: [EN-018]
    gate: GATE-6

  EN-018:
    name: "Split Validation Testing"
    status: pending
    tasks_total: 5
    tasks_complete: 0
    depends_on: [EN-017]
    blocks: [GATE-6]
    gate: GATE-6
```

---

## Evidence and Citations

### Quality Review Gap Identification

**ps-critic (0.94):**
> "CON-FMT-007 not validated because sample packet small (~1,588 tokens, well below 31.5K soft limit)"

**nse-qa (0.90):**
> "NPR 7123.1D Process 14 (Verification): Contract test CON-FMT-007 (Split Navigation) cannot be verified with current test data"

### Token Threshold Source

**ADR-004 (File Splitting Strategy):**
- Soft limit: 31,500 tokens (split at semantic boundary)
- Hard limit: 35,000 tokens (force split)
- Semantic boundary: `## Heading` (Markdown H2)

### Token Estimation Formula

Standard industry approximation:
- 1 word ≈ 1.3 tokens (average)
- 10% buffer for formatting and special characters
- Formula: `(word_count × 1.3) × 1.1`

---

## Acceptance Criteria

- [ ] EN-017 creates 3 transcripts of specified sizes
- [ ] EN-018 validates all 5 split-related behaviors
- [ ] CON-FMT-007 contract test passes
- [ ] GATE-6 includes split validation evidence

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial decision document created |

---

## Related Documents

- [EN-016-ts-formatter.md](./EN-016-ts-formatter/EN-016-ts-formatter.md)
- [ADR-004 File Splitting Strategy](../../../../docs/adrs/ADR-004-file-splitting-strategy.md)
- [contract-tests.yaml](../../../../skills/transcript/test_data/validation/contract-tests.yaml)
- [ORCHESTRATION.yaml](./ORCHESTRATION.yaml)
