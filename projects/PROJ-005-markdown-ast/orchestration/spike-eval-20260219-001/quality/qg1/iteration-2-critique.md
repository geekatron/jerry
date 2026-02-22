# Quality Gate 1 -- Iteration 2

> Focused revision: S-014 re-scoring with targeted improvements
> Deliverable: `library-recommendation.md` (Phase 3 synthesis, v1.1.0 -> v1.2.0)
> Date: 2026-02-20

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scores](#scores) | Dimension-level scoring with S-014 LLM-as-Judge |
| [Verdict](#verdict) | PASS / REVISE / REJECTED determination |
| [Improvements from Iteration 1](#improvements-from-iteration-1) | What changed and its impact |
| [Remaining Gaps](#remaining-gaps) | Issues still below threshold |
| [Revisions Made](#revisions-made) | Specific changes in this iteration |

---

## Scores

| Dimension | Weight | Score (1-5) | Weighted | Iter-1 Score | Delta | Notes |
|-----------|--------|-------------|----------|:------------:|:-----:|-------|
| Completeness | 0.20 | 5 | 1.00 | 4 | +1 | All gaps addressed: sensitivity analysis, Phase 2 uncertainty resolution, version pinning, day-1 setup, fallback escalation chain. |
| Internal Consistency | 0.20 | 4 | 0.80 | 3 | +1 | Phase 2 data discrepancies acknowledged. Validation terminology now consistent ("HTML-equality verification"). Two remnant "AST-equality" uses fixed in iteration 2 revision. Minor: Decision Record "Confidence" field still says "validated roundtrip is a categorical advantage" which is somewhat weakened by the semantic-vs-source analysis -- but the sensitivity analysis shows it is still an advantage, just not as categorical. Acceptable. |
| Methodological Rigor | 0.20 | 4 | 0.80 | 3 | +1 | Sensitivity analysis with 4 tests (all verified correct). Steelman for mistletoe (H-16). Semantic equivalence vs source preservation explicitly analyzed. Minor gap: sensitivity analysis only tests top-3, does not explore scenarios unfavorable to the recommendation (e.g., what if markdown-it-py's Extension API score is reduced). |
| Evidence Quality | 0.15 | 4 | 0.60 | 4 | 0 | Same traceability quality. Phase 2 data note clarifies discrepancy. Traceability table now includes Phase 1 Section column for more precise navigation. |
| Actionability | 0.15 | 5 | 0.75 | 4 | +1 | Version pinning, day-1 setup, complete fallback escalation chain, two mitigation strategies for semantic-vs-source gap. SPIKE-002 has everything needed. |
| Traceability | 0.10 | 4 | 0.40 | 4 | 0 | Improved: Phase 1 traceability table now includes section-level references. Still 4 not 5: Phase 2 traceability table does not include section-level paths (uses "Weighted Composite Scores table" rather than "L1: Feature Matrix > Weighted Composite Scores"). |
| **COMPOSITE** | **1.00** | -- | **0.87** | **0.72** | **+0.15** | -- |

## Verdict: REVISE (0.87 -- within 0.85-0.91 band)

Near threshold. Improvement from REJECTED (0.72) to REVISE (0.87) is substantial. The document is close to meeting the 0.92 quality gate. Remaining gaps are focused: Internal Consistency and Methodological Rigor at 4/5, and Traceability at 4/5.

---

## Improvements from Iteration 1

| Iteration 1 Finding | Resolution | Impact |
|---------------------|------------|--------|
| Phase 2 composite discrepancy (4.25 vs 4.20) unacknowledged | Added Phase 2 data note blockquote in executive summary | Internal Consistency: 3 -> 4 |
| Phase 2 LOC discrepancy (350 vs 470) unacknowledged | Same data note clarifies both discrepancies | Internal Consistency: 3 -> 4 |
| "AST-equality" vs "HTML-equality" used interchangeably | Standardized to "HTML-equality verification" throughout. Fixed 4 of 6 instances in iter-1, remaining 2 fixed in iter-2. | Internal Consistency: 3 -> 4 |
| No sensitivity analysis | Added 4-test sensitivity analysis with verified math | Methodological Rigor: 3 -> 4 |
| No steelman for mistletoe | Added "Steelman for Mistletoe (H-16 Compliance)" section with 4 arguments and resolution | Methodological Rigor: 3 -> 4 |
| Semantic equivalence vs source preservation not analyzed | Added dedicated "Semantic Equivalence vs Source Preservation" section with two mitigation strategies | Methodological Rigor: 3 -> 4 |
| Missing Phase 2 uncertainty resolution | Added "Phase 2 Uncertainty Resolution" section with 4-row table | Completeness: 4 -> 5 |
| Missing version pinning guidance | Added to Decision Record | Actionability: 4 -> 5 |
| Missing day-1 setup instructions | Added `uv add` command to Decision Record | Actionability: 4 -> 5 |
| Incomplete fallback escalation chain | Added 3-step escalation to Decision Record | Actionability: 4 -> 5 |

---

## Remaining Gaps

### Internal Consistency (4/5 -> target 5/5)

1. Decision Record "Confidence" field states "validated roundtrip is a categorical advantage" -- but the Semantic Equivalence vs Source Preservation section nuances this claim (it is a semantic advantage, not necessarily a source-preservation advantage). This is a tension between the Decision Record's concise framing and the detailed analysis. Minor -- the sensitivity analysis shows the advantage holds regardless.

### Methodological Rigor (4/5 -> target 5/5)

1. Sensitivity analysis tests 4 scenarios favorable to the recommendation's robustness. It does not test adversarial scenarios (e.g., what if markdown-it-py's Extension API score is downgraded from 5 to 4 because Jerry's use case is not directly comparable to MyST-Parser's, and simultaneously mistletoe's Roundtrip is raised to 4.5). Adding a "worst case" perturbation would strengthen the analysis.

### Traceability (4/5 -> target 5/5)

1. Phase 2 traceability table references use shorthand ("Weighted Composite Scores table") rather than full section paths. Adding Phase 2 section paths would match the improved Phase 1 traceability format.

---

## Revisions Made

### In iteration 2 revision (v1.1.0 -> v1.2.0):

1. **Fixed 3 remaining "AST-equality" references:**
   - Line 59 (Rank 2 mistletoe): "no AST-equality verification" -> "no HTML-equality verification step comparable to mdformat's"
   - Line 316 (Sensitivity Test 2): "missing AST-equality check" -> "missing HTML-equality verification"
   - Line 395 (Decision Record Fallback): "lack of AST-equality validation" -> "lack of HTML-equality verification"
   - Line 140 (Choose mistletoe scenario): "missing AST-equality check" -> "missing HTML-equality verification"

2. **Enhanced Phase 1 traceability table:** Added "Phase 1 Section" column with full section-level paths (e.g., "L1: Technical Analysis > Library 1 > CommonMark Compliance" instead of just "Phase 1, Library 1: CommonMark Compliance").

3. **Version marker updated** to v1.2.0 with QG1 iteration-2 tag.
