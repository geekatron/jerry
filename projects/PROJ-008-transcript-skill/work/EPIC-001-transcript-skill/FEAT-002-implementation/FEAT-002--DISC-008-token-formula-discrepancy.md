# FEAT-002:DISC-008: Token Formula Discrepancy Between VTT Input and Markdown Output

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
-->

> **Type:** discovery
> **Status:** DOCUMENTED
> **Priority:** HIGH
> **Impact:** HIGH
> **Created:** 2026-01-28
> **Parent:** FEAT-002
> **Owner:** Claude
> **Source:** EN-018 TASK-145 threshold testing

---

## Summary

**The token formula used for EN-017 dataset design (DISC-006) calculates VTT input tokens, not Markdown output tokens.** The ts-formatter agent uses a different formula for split decisions based on the generated Markdown content. This means:

- **meeting-004** (~18.6K Markdown tokens) will NOT trigger split (was expected to be near-limit at ~23K)
- **meeting-005** (~28.9K Markdown tokens) will NOT trigger split (was expected to trigger 1 split at ~37K)
- **meeting-006** (~63.2K Markdown tokens) WILL trigger split (correctly expected)

**Key Findings:**
- DISC-006 formula: `(words × 1.3) + (cues × 12)` - counts VTT structure overhead
- ts-formatter formula: `words × 1.3 × 1.1` = `words × 1.43` - counts Markdown output tokens
- VTT structure overhead (timestamps, cue markers) is NOT present in Markdown output
- Only meeting-006 currently meets the split testing requirements

**Validation:** Verified against ts-formatter.md lines 202-219

---

## Context

### Background

During EN-018 TASK-145 (Token Threshold Validation), we attempted to validate that the EN-017 golden dataset transcripts would trigger the expected number of file splits when processed by ts-formatter.

EN-017 used the token formula from DISC-006:
```
actual_tokens = (word_count × 1.3) + (cue_count × 12)
```

This formula was derived from VTT file analysis and accounts for:
- Word-to-token ratio (1.3 average)
- VTT cue overhead (timestamps, `-->` markers, voice tags) at ~12 tokens per cue

### Research Question

**Does the DISC-006 token formula correctly predict when ts-formatter will trigger file splitting?**

### Investigation Approach

1. Read ADR-004 (File Splitting Strategy) to understand split thresholds
2. Read ts-formatter.md to understand the agent's token counting algorithm
3. Compare formulas and calculate expected tokens using both methods
4. Determine which transcripts will actually trigger splits

---

## Finding

### Token Formula Comparison

**ts-formatter Token Counting (lines 202-219):**
```
TOKEN COUNTING ALGORITHM:
1. Count words: split on whitespace
2. Estimate tokens: words × 1.3 × 1.1 (10% buffer)
3. Track cumulative tokens during generation
```

This equals: `words × 1.43`

**DISC-006 Formula (VTT input):**
```
actual_tokens = (word_count × 1.3) + (cue_count × 12)
```

**Key Difference:** ts-formatter counts tokens on the **generated Markdown output**, not the VTT input. The Markdown output does not contain VTT structure (timestamps, cue markers), so the cue overhead term is irrelevant.

### Recalculated Token Counts

| Transcript | Words | Cues | DISC-006 (VTT) | ts-formatter (MD) | Split Trigger? |
|------------|-------|------|----------------|-------------------|----------------|
| meeting-004 | 13,030 | 536 | 23,371 | 18,633 | NO (< 31,500) |
| meeting-005 | 20,202 | 899 | 37,051 | 28,889 | NO (< 31,500) |
| meeting-006 | 44,225 | 3,071 | 94,345 | 63,242 | YES (> 31,500) |

**Key Observations:**
1. The cue overhead component in DISC-006 adds significant tokens that don't exist in Markdown output
2. meeting-005 was expected to trigger 1 split at ~37K tokens, but at ~29K Markdown tokens it's below the 31.5K soft limit
3. Only meeting-006 will actually trigger file splitting with the ts-formatter formula

### Why The Discrepancy Matters

The ts-formatter processes:
1. **Input:** Canonical JSON from ts-parser (which came from VTT)
2. **Output:** Markdown files (transcript.md, topics.md, etc.)

The **split decision** is made based on the **Markdown output size**, not the VTT input size. When ts-formatter generates `02-transcript.md`, it formats the content as readable Markdown paragraphs, not as VTT cues with timestamps.

### Validation

**Source:** ts-formatter.md lines 202-219

```
SPLIT DECISION:
tokens < 31,500 (soft limit)  → NO SPLIT
31,500 ≤ tokens < 35,000      → SPLIT at ## heading
tokens ≥ 35,000 (hard limit)  → FORCE SPLIT
```

The formula `words × 1.3 × 1.1` is explicitly defined in the agent.

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Agent Definition | ts-formatter token counting algorithm | ts-formatter.md:202-219 | 2026-01-28 |
| E-002 | Discovery | DISC-006 token formula for VTT | FEAT-002--DISC-006-token-estimation-formula.md | 2026-01-28 |
| E-003 | ADR | File splitting thresholds | ADR-004-file-splitting.md | 2026-01-26 |
| E-004 | Dataset Validation | EN-017 word counts | TASK-144 | 2026-01-28 |

### Reference Material

- **Source:** ts-formatter.md
- **Path:** skills/transcript/agents/ts-formatter.md
- **Lines:** 202-219
- **Relevance:** Defines the actual token counting algorithm used for split decisions

---

## Implications

### Impact on Project

**EN-017 Dataset Validity:**
- meeting-004 and meeting-005 will NOT trigger file splits as originally intended
- Only meeting-006 will exercise the split functionality
- The "near-limit" and "1 split" test scenarios are not covered

**EN-018 Testing Scope:**
- TASK-145 threshold tests need to be updated with correct expectations
- Split boundary testing (TASK-146) can only use meeting-006
- CON-FMT-007 contract test execution will have limited coverage

### Design Decisions Affected

- **Decision:** EN-017 transcript sizing targets
  - **Impact:** Targets were based on incorrect formula
  - **Rationale:** Need to recalculate word counts to trigger splits

### Corrective Work Required

| ID | Work Item | Description |
|----|-----------|-------------|
| EN-019 | Dataset Extension | Extend meeting-004 and meeting-005 to trigger splits |
| TASK-X | meeting-004 extension | Increase to ~22K words for Markdown ~31.5K+ tokens |
| TASK-Y | meeting-005 extension | Increase to ~25K+ words for Markdown ~36K+ tokens |

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Incomplete split testing | HIGH | Proceed with meeting-006, create EN-019 for corrections |
| False confidence in split logic | MEDIUM | Document this gap in test coverage |

---

## Relationships

### Creates

- EN-019 (to be created) - Dataset Extension enabler for corrective work

### Informs

- [EN-018](./EN-018-split-validation/EN-018-split-validation.md) - Split validation scope reduced
- [TASK-145](./EN-018-split-validation/TASK-145-token-threshold-tests.md) - Threshold test expectations updated

### Related Discoveries

- [DISC-006](./FEAT-002--DISC-006-token-estimation-formula.md) - Original token formula (VTT-focused)

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-002](./FEAT-002-implementation.md) | Parent feature |
| ADR | [ADR-004](../../../docs/adrs/ADR-004-file-splitting.md) | File splitting strategy |
| Agent | [ts-formatter](../../../skills/transcript/agents/ts-formatter.md) | Formatter agent definition |

---

## Recommendations

### Immediate Actions

1. **Update TASK-145** with correct token expectations (ts-formatter formula)
2. **Proceed with meeting-006 testing** (only transcript that triggers splits)
3. **Document test coverage gap** in EN-018 for meeting-004/005

### Long-term Considerations

- **Create EN-019** to extend meeting-004 and meeting-005 to proper sizes
- **Consider updating DISC-006** to clarify it applies to VTT input only
- **Add Markdown token formula** to documentation for clarity

---

## Open Questions

### Questions for Follow-up

1. **Q:** Should we update DISC-006 to distinguish VTT vs Markdown tokens?
   - **Investigation Method:** Review DISC-006 and add clarification section
   - **Priority:** LOW (documentation improvement)

2. **Q:** What word counts are needed for meeting-004/005 to trigger splits?
   - **Investigation Method:** Calculate: `31,500 / 1.43 = ~22,028 words` minimum
   - **Priority:** HIGH (for EN-019)

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Created discovery during EN-018 TASK-145 execution |

---

## Metadata

```yaml
id: "FEAT-002:DISC-008"
parent_id: "FEAT-002"
work_type: DISCOVERY
title: "Token Formula Discrepancy Between VTT Input and Markdown Output"
status: DOCUMENTED
priority: HIGH
impact: HIGH
created_by: "Claude"
created_at: "2026-01-28"
updated_at: "2026-01-28"
completed_at: "2026-01-28"
tags: [token-counting, file-splitting, ts-formatter, test-coverage]
source: "EN-018 TASK-145"
finding_type: GAP
confidence_level: HIGH
validated: true
```
