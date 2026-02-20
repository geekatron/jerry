# EPIC-001:DISC-002: Training Data Research Produces Factual Errors

> **Type:** discovery
> **Status:** VALIDATED
> **Priority:** HIGH
> **Impact:** HIGH
> **Created:** 2026-02-19
> **Completed:** 2026-02-19
> **Parent:** EPIC-001
> **Owner:** Claude (orchestrator)
> **Source:** Phase 1 execution, ps-researcher-001 output review

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Core finding: training data alone produces factual errors |
| [Context](#context) | Background on the initial research pipeline |
| [Finding](#finding) | 4 factual errors and 1 misattributed quote |
| [Evidence](#evidence) | Sources and citations |
| [Implications](#implications) | Impact on research methodology and P-022 compliance |
| [Recommendations](#recommendations) | Immediate and long-term actions |
| [Relationships](#relationships) | Related work items |
| [Metadata](#metadata) | Machine-readable metadata |

---

## Summary

ps-researcher-001 initially used only LLM training data for the Shane McConkey persona research, producing 4 factual errors (birthplace, documentary directors, Spatula timeline, Saucer Boy costume) and 1 misattributed quote. Supplemental web research (18 WebSearches, 8 WebFetches, 35 sources) corrected all errors. ANY research agent producing factual claims about real people MUST use WebSearch/WebFetch for primary source verification. Training data alone is insufficient for P-022 compliance.

**Key Findings:**
- Training data produced 4 factual errors and 1 misattributed quote across a 710-line research artifact
- Supplemental web research pipeline (18 WebSearches, 8 WebFetches, 35 sources) corrected all errors
- The correction cycle cost ~2.5x the initial research pipeline in token usage -- avoidable overhead

**Validation:** All errors confirmed via web-sourced primary references (Shane McConkey Foundation, IMDB, Wikipedia, Moonshine Ink, The Inertia, FREESKIER, Goodreads).

---

## Context

### Background

During Phase 1 execution, ps-researcher-001 was launched without explicit instructions to use web search tools. The agent relied entirely on training data, producing a 710-line research artifact with [WIDELY ATTRIBUTED] and [INFERENCE] tags instead of actual citations. The user identified this gap after reviewing the initial Barrier 1 gate artifacts.

### Research Question

Is LLM training data sufficient for producing factual claims about real people in persona research?

### Investigation Approach

1. Reviewed ps-researcher-001 initial output for citation quality
2. Launched supplemental web research pipeline (18 WebSearches, 8 WebFetches)
3. Cross-referenced training data claims against 35 web sources
4. Documented all discrepancies and corrections

---

## Finding

### Factual Errors from Training Data

| Claim | Training Data Said | Reality (Web Verified) | Source |
|-------|-------------------|----------------------|--------|
| Birthplace | San Francisco, CA | Vancouver, BC, Canada | Shane McConkey Foundation, U.S. Ski Hall of Fame |
| Documentary directors | "Steven Rosenbaum" | Rob Bruce, Scott Gaffney, Murray Wais, Steve Winter, David Zieff | IMDB, Matchstick Productions |
| Volant Spatula | "Released 2001" | Concept 1996, prototype Aug 2001, commercial Oct 2002 | Wikipedia (Spatula article) |
| Saucer Boy costume | "Spandex onesie" | Snowblades + snow disc + climbing rope + Jack Daniels + neon 90s apparel | Moonshine Ink, The Inertia, FREESKIER |

### Quote Misattribution

"If you're not having fun, you're doing it wrong" was attributed to McConkey but is actually found attributed to Groucho Marx on Goodreads. No McConkey primary source was identified for this quote.

### Cost Impact

The supplemental pipeline cost ~2.5x the initial research pipeline in token usage. The correction cycle (researcher + creator + 3 critic + scorer + rescore) required 6 additional agent invocations. This overhead is avoidable if the initial prompt includes WebSearch instructions.

---

## Evidence

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Artifact | ps-researcher-001-research.md (initial, training-data-only) | Phase 1 orchestration output | 2026-02-19 |
| E-002 | Artifact | ps-researcher-001-supplemental-research.md (35 web sources, corrections documented) | Phase 1 supplemental pipeline | 2026-02-19 |
| E-003 | Artifact | ps-creator-001-draft.md v0.5.0 changelog (corrections applied) | Phase 1 creator output | 2026-02-19 |
| E-004 | Reference | Goodreads attribution of "If you're not having fun" to Groucho Marx | Goodreads.com | 2026-02-19 |

---

## Implications

### Impact on Project

All future research agents in this workflow MUST include explicit WebSearch/WebFetch instructions. P-022 (no deception) compliance requires verifiable citations for factual claims about real people. ORCHESTRATION_PLAN.md should add a standard instruction template for research agents.

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Future research agents repeat training-data-only pattern | HIGH | Mandate WebSearch in all research agent prompts |
| Factual errors in persona doc undermine authenticity | HIGH | Supplemental pipeline corrected all known errors |
| P-022 non-compliance from unverifiable claims | MEDIUM | Citation requirements enforced in orchestration templates |

---

## Recommendations

### Immediate Actions

1. Update ps-researcher-002 prompt (Phase 2) to mandate WebSearch for all biographical/factual claims
2. Add citation verification to Barrier gate criteria in ORCHESTRATION_PLAN.md

### Long-term Considerations

- Add a standard "Research Agent Citation Requirements" section to the orchestration skill's agent templates
- Consider a dedicated citation-verification agent for pipelines involving real people

---

## Relationships

### Informs

- Phase 2 ps-researcher-002 prompt design (citation requirements)
- ORCHESTRATION_PLAN.md Barrier gate criteria

### Related Discoveries

- DISC-003 Supplemental Citation Pipeline Pattern (the recovery pipeline this discovery triggered)

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-19 | Claude (orchestrator) | Created discovery |

---

## Metadata

```yaml
id: "EPIC-001:DISC-002"
parent_id: "EPIC-001"
work_type: DISCOVERY
title: "Training Data Research Produces Factual Errors"
status: VALIDATED
priority: HIGH
impact: HIGH
created_by: "Claude (orchestrator)"
created_at: "2026-02-19"
updated_at: "2026-02-19"
completed_at: "2026-02-19"
tags: [research-methodology, citation-quality, P-022]
source: "Phase 1 execution, ps-researcher-001 output review"
finding_type: RISK
confidence_level: HIGH
validated: true
```
