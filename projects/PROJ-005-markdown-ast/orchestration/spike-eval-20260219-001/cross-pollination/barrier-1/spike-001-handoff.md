# Barrier 1: SPIKE-001 to SPIKE-002 Handoff

> **Barrier:** barrier-1 | **Direction:** SPIKE-001 -> SPIKE-002
> **Source:** `library-recommendation.md` v1.3.0 (QG1 PASS at 0.96)
> **Date:** 2026-02-20

## Document Sections

| Section | Purpose |
|---------|---------|
| [Top-Ranked Library](#top-ranked-library) | Recommended stack and rationale |
| [Feature Matrix Summary](#feature-matrix-summary) | Top 3 candidates comparison |
| [Extension Requirements](#extension-requirements) | Known limitations and LOC estimates |
| [Build-from-Scratch Assessment](#build-from-scratch-assessment) | Verdict on custom parser |
| [Critical Risk R-01](#critical-risk-r-01) | mdformat write-back uncertainty |
| [SPIKE-002 Investigation Priorities](#spike-002-investigation-priorities) | 6 prioritized investigation items |

---

## Top-Ranked Library

**Recommendation:** markdown-it-py v4.0.0 + mdformat v1.0.0 (composite score: 4.20/5.00)

**Rationale:**
- Only validated roundtrip fidelity in the Python ecosystem via mdformat's HTML-equality verification (semantic equivalence guarantee)
- Richest extension ecosystem: 20+ plugins in mdit-py-plugins, MyST-Parser v5.0.0 as proof-of-concept for domain-specific markdown dialects
- Institutional maintenance by Executable Books organization (not single-maintainer)
- Full CommonMark v0.31.2 compliance
- Flat token stream with on-demand SyntaxTreeNode tree conversion; position tracking via token.map [start, end] on all block tokens

**Fallback:** mistletoe v1.5.1 (composite: 3.75) -- true tree AST, built-in MarkdownRenderer, but lacks formal roundtrip validation and carries single-maintainer risk.

**Important nuance:** mdformat guarantees semantic equivalence (HTML output consistency), NOT byte-for-byte source preservation. May normalize whitespace, heading styles, or list formatting. Two mitigation strategies identified: (1) adopt mdformat canonical formatting for Jerry corpus, or (2) supplementary diff-based validation (~50 LOC).

---

## Feature Matrix Summary

Top 3 candidates on the 8-dimension weighted scoring framework:

| Dimension (Weight) | markdown-it-py + mdformat | mistletoe | marko |
|---------------------|:------------------------:|:---------:|:-----:|
| AST Quality (0.20) | 4 -- flat tokens + SyntaxTreeNode | 4 -- true tree (native) | 4 -- true tree (uncertain position tracking) |
| Roundtrip Fidelity (0.20) | 5 -- HTML-equality verified | 4 -- design goal, unverified | 3 -- normalizing renderer |
| Extension API (0.15) | 5 -- 20+ plugins, MyST proof | 4 -- subclass-based, fewer examples | 3 -- MarkoExtension, fewest examples |
| Jerry Compatibility (0.15) | 3 -- needs ~470 LOC extensions | 3 -- needs ~520 LOC | 3 -- needs ~500 LOC |
| Maintenance (0.10) | 4 -- Executable Books org | 3 -- single maintainer | 3 -- single maintainer |
| Ergonomics (0.10) | 4 -- rich ecosystem | 4 -- clean tree API | 3 -- normalizing concerns |
| Performance (0.05) | 3 -- adequate for Jerry files | 3 -- adequate | 3 -- adequate |
| License (0.05) | 5 -- MIT | 5 -- MIT | 5 -- MIT |
| **Composite** | **4.20** | **3.75** | **3.40** |

---

## Extension Requirements

~470 LOC across 4 Jerry-specific extensions for the recommended stack:

| Extension | LOC | Complexity | Priority |
|-----------|:---:|:----------:|----------|
| Blockquote Frontmatter Extraction + Write-back | ~220 | Low-Medium | P0 |
| L2-REINJECT Comment Parser + Write-back | ~120 | Low | P0 |
| Navigation Table Query Helpers | ~120 | Low | P1 |
| Jerry Markdown Facade (JerryDocument API) | ~130 | Low | P1 |
| **Total (including ~120 LOC tests)** | **~470** | **Low-Medium** | -- |

**Implementation phasing:**
- Phase A (Days 1-3): Blockquote FM extraction + L2-REINJECT read-only (~150 LOC)
- Phase B (Days 4-5): Write-back validation (~120 LOC)
- Phase C (Week 2): Nav table helpers + Jerry facade (~250 LOC)

---

## Build-from-Scratch Assessment

**Verdict: Do Not Build from Scratch**

| Metric | Library Approach | Build-from-Scratch |
|--------|:---------------:|:-----------------:|
| Implementation LOC | ~470 | 2,380-3,320 |
| Development time | 1-2 weeks | 6-10 weeks |
| CommonMark coverage | 100% (via library) | ~65% (subset) |
| Roundtrip validation | mdformat provides | Must build or accept risk |
| Cost ratio | 1x | 5-7x |

The sole advantage of build-from-scratch (full control) is achievable via the extension API at lower cost. If the library approach fails entirely, the correct next step is a hybrid approach (thin wrapper + custom AST nodes, ~800-1,200 LOC), not a full scratch build.

---

## Critical Risk R-01

**Risk:** mdformat plugin API may be insufficient for blockquote frontmatter write-back.

| Attribute | Value |
|-----------|-------|
| Likelihood | Medium |
| Impact | High |
| Status | UNRESOLVED -- SPIKE-002 must validate |

**Details:** Write-back (reconstructing paragraph token content from modified key-value dict after a frontmatter field change) is the highest-uncertainty interaction in the recommendation. It was not clearly documented in Phase 1 or Phase 2 research. The mdformat plugin API is designed for formatting, not surgical content modification.

**Fallback if R-01 materializes:**
1. String-level substitution with roundtrip diff verification (within markdown-it-py stack)
2. Switch to mistletoe + Jerry-owned diff-based validation (~520 LOC + ~50 LOC)
3. Hybrid approach: markdown-it-py parsing + custom Jerry renderer (~800-1,200 LOC)
4. Full scratch build (last resort, not planned)

---

## SPIKE-002 Investigation Priorities

Ranked by criticality to the Rank 1 recommendation:

**Critical (must resolve before adopting Rank 1):**

1. **Blockquote frontmatter write-back via mdformat plugin API.** Parse a WORKTRACKER entity, modify a frontmatter field (e.g., Status: pending -> in_progress), render back, verify: (a) modified field correct, (b) unmodified content byte-for-byte identical, (c) mdformat HTML-equality verification passes.

2. **Full Jerry dialect roundtrip corpus test.** Run mdformat against all 30-50 active Jerry markdown files. Document any files where normalization alters content. Classify alterations as acceptable (whitespace) or disqualifying (semantic change).

3. **L2-REINJECT roundtrip with special characters.** Verify mdformat preserves quotes, commas, and periods in HTML comment content strings through parse-modify-render.

**Important (validate recommendation assumptions):**

4. **Extension API integration pattern.** Implement minimal JerryDocument facade. Verify SyntaxTreeNode provides sufficient position tracking for distinguishing frontmatter blockquotes from content blockquotes.

5. **Performance at batch scale.** Process 50 Jerry files sequentially; confirm sub-100ms total throughput.

**Contingency (if R-01 materializes):**

6. **Mistletoe fallback proof-of-concept.** Same write-back test with mistletoe MarkdownRenderer. Document roundtrip fidelity. Assess whether Jerry-owned diff-based verification is sufficient.

---

*Handoff artifact for barrier-1. Extracted from QG1-approved SPIKE-001 synthesis (library-recommendation.md v1.3.0, score: 0.96).*
