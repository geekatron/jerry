# Quality Gate 1 -- Iteration 1

> Full strategy application: S-010, S-003, S-007, S-002, S-014
> Deliverable: `library-recommendation.md` (Phase 3 synthesis)
> Date: 2026-02-19

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scores](#scores) | Dimension-level scoring with S-014 LLM-as-Judge |
| [Verdict](#verdict) | PASS / REVISE / REJECTED determination |
| [Findings](#findings) | Strategy-by-strategy findings |
| [Revisions Required](#revisions-required) | Specific changes to address in revision |

---

## Scores

| Dimension | Weight | Score (1-5) | Weighted | Notes |
|-----------|--------|-------------|----------|-------|
| Completeness | 0.20 | 4 | 0.80 | All required sections present. Missing: sensitivity analysis, Phase 2 uncertainty resolution map, version pinning guidance. |
| Internal Consistency | 0.20 | 3 | 0.60 | Phase 2 exec summary says composite 4.25 but table shows 4.20 -- not acknowledged. Phase 2 exec summary says ~350 LOC but table shows ~470 -- not acknowledged. "AST-equality" vs "HTML-equality" used interchangeably without clarification. |
| Methodological Rigor | 0.20 | 3 | 0.60 | No sensitivity analysis on recommendation robustness. No explicit steelman for #2 (H-16 spirit). Semantic equivalence vs byte-for-byte preservation distinction not analyzed. |
| Evidence Quality | 0.15 | 4 | 0.60 | Two traceability tables with 24 claims mapped. Minor: "formally validated" paraphrases Phase 1's "validates that rendered HTML is consistent." LOC discrepancy selective. |
| Actionability | 0.15 | 4 | 0.60 | Clear recommendation, extension roadmap, SPIKE-002 handoff. Missing: version pinning guidance, day-1 setup instructions, complete fallback escalation chain. |
| Traceability | 0.10 | 4 | 0.40 | Comprehensive traceability tables. Minor: Phase 2 LOC discrepancy not traced. Some Phase 1 refs use "Observation N" rather than searchable headings. |
| **COMPOSITE** | **1.00** | -- | **0.72** | -- |

## Verdict: REJECTED (0.72 < 0.85)

Internal Consistency and Methodological Rigor are the primary weakness areas, dragging the composite below threshold. Both scored 3/5 due to substantive issues, not cosmetic ones.

---

## Findings

### S-010 (Self-Refine): Gaps Identified

1. **Composite score discrepancy with Phase 2 executive summary.** Phase 2 exec summary (line 21) states composite as 4.25; Phase 2 detailed table (line 54) shows 4.20. Phase 3 uses 4.20 without acknowledging the discrepancy.

2. **Extension LOC discrepancy with Phase 2 executive summary.** Phase 2 exec summary (line 23) states "~350 LOC, low complexity" for markdown-it-py; Phase 2 detailed table (line 292) shows ~470 LOC. Phase 3 uses ~470 without noting this.

3. **Missing sensitivity analysis.** The recommendation's robustness is untested. If Roundtrip Fidelity weight changes from 0.20 to 0.15, or if mistletoe's roundtrip score is raised from 4 to 4.5 (acknowledging that Jerry can build diff-based validation), does the ranking change?

4. **Imprecise validation terminology.** "AST-equality verification" and "HTML-equality" are used interchangeably (lines 24, 52, 97, 99) without explaining that they describe the same mechanism: comparing rendered HTML of input vs rendered HTML of output.

5. **Phase 2 uncertainties not explicitly resolved.** Phase 2 (lines 496-500) lists 4 uncertainties for Phase 3. Phase 3 addresses them implicitly but does not include an explicit resolution table.

6. **Incomplete fallback escalation chain.** Document discusses mistletoe fallback and hybrid approach but does not address what happens if mistletoe's MarkdownRenderer also fails roundtrip requirements.

7. **No version pinning guidance.** Decision record specifies versions but no guidance on pinning strategy or `pyproject.toml` configuration.

### S-003 (Steelman): Strongest Case FOR Mistletoe

The steelman for mistletoe is strong enough to warrant explicit acknowledgment:

- **True tree AST is genuinely superior for tree-walking operations.** Jerry's core operations (blockquote traversal, parent-child identification) are more ergonomic with mistletoe's native tree than with markdown-it-py's flat tokens + SyntaxTreeNode conversion.
- **Single dependency reduces supply chain risk.** mdformat has only 15 contributors vs markdown-it-py's 34, suggesting a smaller maintenance base within Executable Books.
- **"Validated roundtrip" may be less decisive than claimed.** mdformat validates semantic equivalence (HTML output consistency), not byte-for-byte source preservation. Jerry could build a diff-based validation layer on top of mistletoe's MarkdownRenderer that directly validates what Jerry actually needs: unmodified source lines are preserved.
- **mistletoe's MarkdownRenderer was designed for parse-modify-render.** mdformat was designed as a formatter. Jerry is repurposing a formatter as a preservation engine.

**Steelman verdict:** Does not change the recommendation (markdown-it-py + mdformat's ecosystem and institutional backing still win), but the steelman arguments should be explicitly addressed in the deliverable to demonstrate balanced analysis.

### S-007 (Constitutional AI Critique)

- **H-23 (nav table):** PASS. Present at lines 8-16.
- **H-24 (anchor links):** PASS. All navigation entries use anchor links.
- **P-022 (no deception):** PASS. Uncertainties explicitly flagged. Confidence stated with evidence.
- **Citations:** PASS. Traceability tables present.
- **Persistence:** PASS. Persisted to repository filesystem.

**Constitutional compliance: PASS.** No violations.

### S-002 (Devil's Advocate): Arguments AGAINST the Recommendation

1. **Semantic equivalence is not byte-for-byte preservation.** mdformat's HTML-equality check proves that formatting changes do not alter document meaning. It does NOT prove that unmodified markdown source lines are preserved byte-for-byte. mdformat could pass its check while normalizing table alignment, heading whitespace, or list indentation in sections Jerry did not modify. The deliverable treats "validated roundtrip" as a byte-for-byte guarantee, which it is not.

2. **Two-library dependency risk dismissed too quickly.** "Both MIT, same organization" is a snapshot. mdformat's 15 contributors vs markdown-it-py's 34 suggests differential maintenance depth. The risk is not that both libraries fail, but that one (mdformat) stagnates while the other continues.

3. **Diff-based validation is a viable alternative.** Jerry could implement a simpler strategy with ANY library: parse, modify, render, then diff output against original source and reject changes outside the intended modification zone. This "diff-based validation" approach provides stronger guarantees for Jerry's specific need (preserve unmodified lines) than mdformat's HTML-equality check (preserve semantic meaning). Under this approach, the roundtrip dimension becomes less differentiating.

**Devil's advocate verdict:** The semantic-equivalence-vs-byte-preservation distinction is a genuine analytical gap. The diff-based validation alternative is a legitimate counter-argument that weakens the "validated roundtrip is decisive" claim. Both should be addressed in the revision.

---

## Revisions Required

### Priority 1 (Internal Consistency -- must fix)

- [ ] Add a note acknowledging the Phase 2 composite score discrepancy (4.25 in exec summary vs 4.20 in table) and state which is authoritative.
- [ ] Add a note acknowledging the Phase 2 LOC discrepancy (350 in exec summary vs 470 in table) and state which is authoritative.
- [ ] Clarify mdformat's validation mechanism: state precisely that "AST-equality verification" means comparing rendered HTML of input vs rendered HTML of output. Use consistent terminology throughout.

### Priority 2 (Methodological Rigor -- must fix)

- [ ] Add a sensitivity analysis section testing the recommendation's robustness under altered weights or scores.
- [ ] Add an explicit steelman for mistletoe (per H-16 spirit) and explicitly address the steelman arguments.
- [ ] Address the semantic-equivalence-vs-byte-preservation distinction: explain why semantic equivalence is sufficient for Jerry, OR acknowledge that additional diff-based validation may be needed.

### Priority 3 (Completeness -- should fix)

- [ ] Add explicit Phase 2 uncertainty resolution table mapping each Phase 2 uncertainty to its Phase 3 resolution.
- [ ] Add version pinning guidance (recommended `pyproject.toml` configuration).
- [ ] Add fallback escalation to the hybrid approach if mistletoe also fails.

### Priority 4 (Actionability -- should fix)

- [ ] Add day-1 getting-started instruction (`uv add markdown-it-py mdformat`).
