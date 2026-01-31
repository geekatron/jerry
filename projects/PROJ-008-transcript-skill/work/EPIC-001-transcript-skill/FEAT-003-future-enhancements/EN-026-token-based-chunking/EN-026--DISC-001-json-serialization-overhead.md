# EN-026:DISC-001: JSON Serialization Overhead in Token-Based Chunking

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-01-30
PURPOSE: Document the ~22% JSON serialization overhead discovered during live verification
-->

> **Type:** discovery
> **Status:** VALIDATED
> **Priority:** MEDIUM
> **Impact:** MEDIUM
> **Created:** 2026-01-30T18:30:00Z
> **Completed:** 2026-01-30T18:45:00Z
> **Parent:** EN-026
> **Owner:** Claude
> **Source:** Live verification of token-based chunking

---

## Frontmatter

```yaml
id: "EN-026:DISC-001"
work_type: DISCOVERY
title: "JSON Serialization Overhead in Token-Based Chunking"
classification: TECHNICAL
status: VALIDATED
resolution: DOCUMENTED
priority: MEDIUM
impact: MEDIUM
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-30T18:30:00Z"
updated_at: "2026-01-30T18:45:00Z"
completed_at: "2026-01-30T18:45:00Z"
parent_id: "EN-026"
tags: ["json", "serialization", "overhead", "tokens", "chunking", "discovery"]
finding_type: CONSTRAINT
confidence_level: HIGH
source: "Live verification with internal-sample VTT"
research_method: "Empirical measurement"
validated: true
validation_date: "2026-01-30T18:45:00Z"
validated_by: "Claude + User"
```

---

## Summary

**Token-based chunking produces chunks ~22% larger than the target token count due to JSON serialization overhead.**

During live verification of EN-026 token-based chunking, chunks targeting 18,000 tokens consistently measured ~22,000 tokens after JSON serialization. This represents a **22% overhead** from chunk metadata, JSON structure, and pretty-printing.

**Key Findings:**
- Target tokens (raw segment text): 18,000
- Actual tokens (serialized JSON): ~22,000
- Overhead: ~4,000 tokens (~22%)
- All chunks still safely under 25,000 token limit (12% margin remaining)

**Validation:** Verified via tiktoken measurement of live output files.

---

## Context

### Background

EN-026 implemented token-based chunking to fix BUG-001 (chunks exceeding Claude Code's 25K token Read limit). The implementation targets 18,000 tokens per chunk with a 25% safety margin below the 25K limit.

During implementation, the TokenCounter service counts tokens in the **raw segment text** before JSON serialization. However, the final chunk files include additional JSON overhead.

### Research Question

**How much token overhead does JSON serialization add to chunks, and does this impact the safety margin?**

### Investigation Approach

1. Run token-based chunking on a real VTT file (internal-sample meeting, ~38 minutes)
2. Measure actual token counts of generated chunk files using tiktoken
3. Calculate the overhead ratio
4. Determine if the overhead impacts Claude Code Read tool compatibility

---

## Finding

### Measured Token Counts

Live verification with `internal-sample` VTT file (710 segments, 2,263,888ms duration):

| Chunk | Target Tokens | Actual Tokens | Segments | Overhead |
|-------|---------------|---------------|----------|----------|
| chunk-001.json | 18,000 | **21,949** | 229 | +22.0% |
| chunk-002.json | 18,000 | **21,862** | 224 | +21.5% |
| chunk-003.json | 18,000 | **22,024** | 229 | +22.4% |
| chunk-004.json | (partial) | **2,839** | 28 | N/A |

**Average Overhead:** ~22% (~4,000 tokens per chunk)

### Sources of JSON Overhead

```
┌─────────────────────────────────────────────────────────────────────┐
│                     JSON OVERHEAD BREAKDOWN                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. CHUNK METADATA (~200-300 tokens per chunk)                      │
│     ┌──────────────────────────────────────────────────────────┐    │
│     │ {                                                         │    │
│     │   "chunk_id": "chunk-001",                               │    │
│     │   "schema_version": "1.0",                               │    │
│     │   "segment_range": [1, 229],                             │    │
│     │   "timestamp_range": {"start_ms": ..., "end_ms": ...},   │    │
│     │   "navigation": {"previous": ..., "next": ..., "index":} │    │
│     │   ...                                                     │    │
│     └──────────────────────────────────────────────────────────┘    │
│                                                                      │
│  2. PER-SEGMENT OVERHEAD (~15 tokens per segment)                   │
│     ┌──────────────────────────────────────────────────────────┐    │
│     │ {                           ← Opening brace (1 token)     │    │
│     │   "id": "123",              ← Key "id" + quotes (3-4)     │    │
│     │   "start_ms": 12345,        ← Key "start_ms" (3-4)        │    │
│     │   "end_ms": 12567,          ← Key "end_ms" (3-4)          │    │
│     │   "speaker": "Adam Nowak",  ← Key "speaker" (3-4)         │    │
│     │   "text": "...",            ← Key "text" (2-3)            │    │
│     │   "raw_text": "..."         ← Key "raw_text" (3-4)        │    │
│     │ },                          ← Closing brace + comma (1-2)  │    │
│     └──────────────────────────────────────────────────────────┘    │
│     ~15 tokens overhead × 229 segments = ~3,435 tokens              │
│                                                                      │
│  3. PRETTY-PRINTING OVERHEAD (~500-800 tokens)                      │
│     - 2-space indentation per line                                  │
│     - Newlines between elements                                     │
│     - Whitespace for readability                                    │
│                                                                      │
│  TOTAL ESTIMATED OVERHEAD: ~4,000 tokens (~22%)                     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Overhead Calculation

```
Raw segment text target:     18,000 tokens
Per-segment JSON overhead:   229 segments × ~15 tokens = ~3,435 tokens
Chunk metadata overhead:     ~300 tokens
Pretty-printing overhead:    ~700 tokens
                            ─────────────
Total estimated overhead:    ~4,435 tokens
Actual measured overhead:    ~3,949 tokens (21,949 - 18,000)

Overhead percentage:         3,949 / 18,000 = 21.9% ≈ 22%
```

### Safety Margin Analysis

```
┌────────────────────────────────────────────────────────────────────┐
│                    TOKEN BUDGET ANALYSIS                           │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Claude Code Read Limit:    25,000 tokens   │████████████████████│ │
│  Actual Chunk Size:         22,000 tokens   │████████████████░░░░│ │
│  Target (before overhead):  18,000 tokens   │█████████████░░░░░░░│ │
│                                                                     │
│  Remaining Safety Margin:   3,000 tokens (12%)                     │
│  Original Design Margin:    7,000 tokens (28%)                     │
│  Consumed by Overhead:      4,000 tokens (16%)                     │
│                                                                     │
│  STATUS: SAFE - All chunks under limit with 12% margin             │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### Validation

Validation performed via live execution and independent token measurement:

```bash
# Command used for live verification
uv run jerry transcript parse "/path/to/meeting.vtt" --output-dir "/path/to/output/"

# Token counting verification (tiktoken p50k_base)
# Measured each chunk file independently
```

**Validation Results:**
- All 4 chunks under 25K limit
- Largest chunk: 22,024 tokens (12% margin)
- No Read tool failures
- ts-extractor agent can process all chunks

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Measurement | chunk-001.json: 21,949 tokens | Live verification output | 2026-01-30 |
| E-002 | Measurement | chunk-002.json: 21,862 tokens | Live verification output | 2026-01-30 |
| E-003 | Measurement | chunk-003.json: 22,024 tokens | Live verification output | 2026-01-30 |
| E-004 | Measurement | chunk-004.json: 2,839 tokens | Live verification output | 2026-01-30 |
| E-005 | Configuration | target_tokens: 18,000 | index.json | 2026-01-30 |

### Reference Material

- **Source:** EN-026 Token-Based Chunking Enabler
- **Path:** `EN-026-token-based-chunking.md`
- **Relevance:** Parent enabler documenting the implementation

---

## Implications

### Impact on Project

The JSON overhead is **acceptable** - all chunks remain safely under the 25K limit with 12% margin. However, this discovery documents an important constraint for future reference.

### Design Decisions Affected

- **Decision:** Target token value selection
  - **Impact:** Current 18,000 target produces ~22,000 actual (12% margin remaining)
  - **Rationale:** Sufficient margin for safety; no change needed

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Unusual segment content with higher JSON overhead | Low | 12% remaining margin absorbs variation |
| Future schema changes increasing metadata | Low | Document overhead in schema design |

### Opportunities Created

- **DEFERRED:** If tighter token budget needed, could reduce target to 14,000-15,000 tokens
- **DEFERRED:** Could implement compact JSON serialization (minified) for 10-15% reduction

---

## Relationships

### Creates

None - this is an informational discovery documenting a constraint.

### Informs

- [EN-026: Token-Based Chunking](./EN-026-token-based-chunking.md) - Parent enabler
- Future work on schema optimization

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-026-token-based-chunking.md](./EN-026-token-based-chunking.md) | Parent enabler |
| Bug Fixed | [BUG-001](../../FEAT-004-hybrid-infrastructure/EN-021-chunking-strategy/BUG-001-chunk-token-overflow.md) | Token overflow bug |
| Service | `src/transcript/application/services/token_counter.py` | TokenCounter implementation |
| Service | `src/transcript/application/services/chunker.py` | TranscriptChunker implementation |

---

## Recommendations

### Immediate Actions

1. **No action required** - Current implementation is safe and functional
2. **Document in SKILL.md** - Note that chunk files are ~22% larger than target_tokens

### Long-term Considerations

- **If budget becomes tighter:** Reduce target_tokens to 14,000-15,000 to hit ~18K actual
- **If overhead reduction needed:** Implement minified JSON option (remove pretty-printing)
- **Schema changes:** Factor in ~15 tokens per segment overhead when modifying segment schema

---

## Open Questions

### Questions for Follow-up

1. **Q:** Should we adjust the default target_tokens to account for overhead?
   - **Investigation Method:** User feedback on chunk sizes
   - **Priority:** LOW - Current setting works well
   - **Decision:** DEFERRED - 12% margin is sufficient

2. **Q:** Should we offer minified JSON output option?
   - **Investigation Method:** Measure size reduction from minification
   - **Priority:** LOW - Only if token budget becomes critical
   - **Decision:** DEFERRED - Not needed currently

---

## Technical Details

### Overhead Breakdown by Component

| Component | Estimated Tokens | % of Overhead |
|-----------|------------------|---------------|
| Per-segment keys + structure | ~3,435 | 77% |
| Pretty-printing whitespace | ~700 | 16% |
| Chunk metadata | ~300 | 7% |
| **Total** | **~4,435** | **100%** |

### Comparison: Before vs After Token-Based Chunking

| Metric | Segment-Based (Before) | Token-Based (After) | Improvement |
|--------|------------------------|---------------------|-------------|
| Max chunk size | 49,377 tokens | 22,024 tokens | **55% reduction** |
| Read tool compatible | No (fails) | Yes (passes) | **Fixed** |
| Safety margin | -97% (over limit) | +12% (under limit) | **109% improvement** |
| Chunks for test file | 2 | 4 | More granular |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-30 | Claude | Created discovery documenting JSON serialization overhead |

---

## Metadata

```yaml
id: "EN-026:DISC-001"
parent_id: "EN-026"
work_type: DISCOVERY
title: "JSON Serialization Overhead in Token-Based Chunking"
status: VALIDATED
priority: MEDIUM
impact: MEDIUM
created_by: "Claude"
created_at: "2026-01-30T18:30:00Z"
updated_at: "2026-01-30T18:45:00Z"
completed_at: "2026-01-30T18:45:00Z"
tags: ["json", "serialization", "overhead", "tokens", "chunking"]
source: "Live verification"
finding_type: CONSTRAINT
confidence_level: HIGH
validated: true
```
