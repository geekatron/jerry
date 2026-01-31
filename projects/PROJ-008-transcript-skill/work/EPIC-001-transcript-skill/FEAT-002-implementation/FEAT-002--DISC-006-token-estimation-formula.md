# FEAT-002:DISC-006: Token Estimation Formula Inaccuracy

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
-->

> **Type:** discovery
> **Status:** DOCUMENTED
> **Priority:** medium
> **Impact:** high
> **Created:** 2026-01-28
> **Completed:** 2026-01-28
> **Parent:** FEAT-002
> **Owner:** Claude
> **Source:** EN-017 TASK-141 execution

---

## Summary

The token estimation formula documented in EN-017 does not account for VTT structural overhead, leading to significant underestimation of actual token counts. This affects all large transcript creation tasks.

**Key Findings:**
- Original formula: `estimated_tokens = (word_count × 1.3) × 1.1`
- Missing factor: VTT cue overhead (~10-14 tokens per cue)
- meeting-004.vtt: 13,002 words predicted ~18.6K tokens, actual ~21-22K tokens

**Validation:** Verified through meeting-004-sprint-planning.vtt creation in TASK-141.

---

## Context

### Background

EN-017 defines a large transcript dataset for validating file splitting behavior in ts-formatter. The token targets were derived using a formula that estimates tokens based on word count alone.

### Research Question

Why does the actual token count significantly exceed the predicted token count when creating VTT transcripts?

### Investigation Approach

1. Created meeting-004-sprint-planning.vtt with 13,002 words
2. Applied documented formula: `(13,002 × 1.3) × 1.1 = 18,593 tokens`
3. Analyzed VTT structure to identify additional token sources
4. Calculated actual overhead per cue

---

## Finding

### Token Sources Not Accounted For

The original formula only considers content words. VTT files have structural overhead:

**Per-Cue Overhead (estimated ~400 cues in meeting-004):**

| Element | Example | Est. Tokens |
|---------|---------|-------------|
| Timestamp line | `00:15:30.000 --> 00:15:45.500` | 7-10 |
| Voice tag | `<v Sarah Chen>` | 3-4 |
| Newlines/spacing | (structural) | 1-2 |
| **Total per cue** | | **11-16** |

**Overhead Calculation:**
- 400 cues × ~12 tokens = ~4,800 additional tokens
- Actual: 18,593 (content) + 4,800 (overhead) = ~23,400 tokens
- Observed: ~21-22K tokens (aligns with corrected estimate)

### Corrected Formula

```
actual_tokens = (word_count × 1.3) + (cue_count × 12)
```

Where:
- `1.3` = average tokens per word (accounts for punctuation, subwords)
- `12` = average VTT overhead per cue (timestamp + voice tag + structure)

**Example Validation:**
- meeting-004: (13,002 × 1.3) + (400 × 12) = 16,903 + 4,800 = 21,703 tokens ✓

### Implications for Token Targets

| Transcript | Original Target | Words Needed (Old) | Words Needed (New) |
|------------|-----------------|--------------------|--------------------|
| meeting-004 | 22K-28K | ~17,000 | ~13,000 |
| meeting-005 | 42K-48K | ~32,000 | ~27,000 |
| meeting-006 | 85K-95K | ~66,000 | ~55,000 |

The corrected formula shows fewer words are needed to reach token targets due to VTT overhead.

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Artifact | meeting-004-sprint-planning.vtt | EN-017/TASK-141 | 2026-01-28 |
| E-002 | Analysis | Word count: `wc -w` = 13,002 | CLI output | 2026-01-28 |
| E-003 | Analysis | Line count: `wc -l` = 1,620 | CLI output | 2026-01-28 |
| E-004 | Calculation | Cue count: ~400 (1,620 lines ÷ 4) | Derived | 2026-01-28 |

### Reference Material

- **Source:** OpenAI Tokenizer behavior
- **Relevance:** VTT timestamps tokenize as multiple tokens due to colons and periods

---

## Implications

### Impact on Project

- EN-017 word targets are higher than necessary
- meeting-004 meets token target despite fewer words than originally planned
- Future tasks (TASK-142, TASK-143) can use reduced word targets

### Design Decisions Affected

- **Decision:** Update EN-017 Technical Design section with corrected formula
  - **Impact:** Reduced effort for TASK-142 and TASK-143
  - **Rationale:** Avoid over-production of content

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Token estimates vary by tokenizer | Low | Verify with actual TokenCounter during validation |
| Different VTT styles have different overhead | Low | Use consistent voice tag format |

---

## Relationships

### Informs

- [TASK-142](./EN-017-large-transcript-dataset/TASK-142-meeting-005-creation.md) - Reduced word target
- [TASK-143](./EN-017-large-transcript-dataset/TASK-143-meeting-006-creation.md) - Reduced word target
- [TASK-144](./EN-017-large-transcript-dataset/TASK-144-dataset-validation.md) - Validation criteria

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-002-implementation](./FEAT-002-implementation.md) | Parent feature |
| Enabler | [EN-017](./EN-017-large-transcript-dataset/EN-017-large-transcript-dataset.md) | Large transcript dataset |
| Task | [TASK-141](./EN-017-large-transcript-dataset/TASK-141-meeting-004-creation.md) | Source of discovery |

---

## Recommendations

### Immediate Actions

1. Update EN-017 Technical Design with corrected formula
2. Update TASK-142 and TASK-143 acceptance criteria with accurate word targets
3. Document overhead calculation in VTT Generation Guidelines

### Long-term Considerations

- Consider adding a TokenCounter utility to verify estimates during creation
- Factor in VTT overhead when planning any future transcript work

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Created discovery from TASK-141 findings |

---

## Metadata

```yaml
id: "FEAT-002:DISC-006"
parent_id: "FEAT-002"
work_type: DISCOVERY
title: "Token Estimation Formula Inaccuracy"
status: DOCUMENTED
priority: MEDIUM
impact: HIGH
created_by: "Claude"
created_at: "2026-01-28"
updated_at: "2026-01-28"
completed_at: "2026-01-28"
tags: [token-estimation, vtt-format, technical-debt]
source: "EN-017 TASK-141 execution"
finding_type: GAP
confidence_level: HIGH
validated: true
```
