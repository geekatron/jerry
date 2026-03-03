# Quality Score Report: PROJ-014 Medium Article (Iteration 4)

## L0 Executive Summary

**Score:** 0.946/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.92)
**One-line assessment:** All four i4 fixes are confirmed applied and genuine — McNemar rationale, Barreto & Jana title, 6-of-9 arithmetic explicit + Ferraz venue harmonized, "established by peer-reviewed research" — lifting the composite from 0.937 to 0.946, but the 0.95 publication threshold is not yet reached; the remaining gap is distributed across Evidence Quality (0.94) and Traceability (0.92), both improvable with single targeted additions.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/proj-014-completion-20260301-001/articles/medium-negative-prompting.md`
- **Deliverable Type:** Other (Medium publication article, external audience)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-01T00:00:00Z
- **Custom threshold:** 0.95 (per task specification; publication artifact, C4)
- **Prior Score (i3):** 0.937 REVISE
- **Prior Score (i2):** 0.913 REVISE
- **Prior Score (i1):** 0.876 REVISE
- **Iteration:** 4
- **Strategy Findings Incorporated:** No (standalone scoring)

---

## I4 Fix Verification

All four fixes specified in the task brief are verified against the article text.

| Fix | Target | i4 Status | Evidence |
|-----|--------|-----------|----------|
| 1. McNemar rationale sentence | Explain why matched pairs require McNemar rather than independent-group tests | **CONFIRMED FIXED** | Line 60-61: "McNemar's test is designed for matched-pair designs, where each pair controls for constraint-specific difficulty -- an independent-group test like chi-square would misattribute within-pair variation to the framing condition." Rationale names the alternative test (chi-square), explains the design property (matched pairs control for constraint difficulty), and names the error avoided (misattributing within-pair variation). Complete and accurate. |
| 2. Barreto & Jana full paper title | Full paper title in footnote citation | **CONFIRMED FIXED** | Footnote (line 137): "Barreto & Jana, 'This is not a Disimprovement: Improving Negation Reasoning in Large Language Models via Prompt Engineering,' EMNLP 2025 Findings ([ACL Anthology](https://aclanthology.org/2025.findings-emnlp.761))." Full title present, venue present, URL present. |
| 3a. 6-of-9 arithmetic explicit | "6 of 9 violations" with percentage stated | **CONFIRMED FIXED** | Line 68: "two-thirds (6 of 9, 67%) landed on a single constraint type: behavioral timing rules." Fraction, count, and percentage all explicit. The arithmetic path "7 C1 + 2 C2 = 9 total" is now deducible without reader inference for the behavioral-timing subset. |
| 3b. Ferraz venue harmonized | "EMNLP 2024 Findings" in both body and footnote | **CONFIRMED FIXED** | Body (line 38): "Ferraz et al.'s 'LLM Self-Correction with DeCRIM' (EMNLP 2024 Findings, [arXiv:2410.06458]...)." Footnote (line 137): "Ferraz et al., 'LLM Self-Correction with DeCRIM,' EMNLP 2024 Findings ([arXiv:2410.06458]...)." Venue designation now consistent in both locations. |
| 4. "settled science" → "established by peer-reviewed research" | More precise characterization for T1+T3 evidence base | **CONFIRMED FIXED** | Line 38: "That much is established by peer-reviewed research." The i3 characterization "That much is settled science" is gone; the replacement is more precise and durable against reviewer challenge. |

**Placement check — McNemar rationale (Fix 1):** The rationale sentence appears immediately after the p-value statement ("p = 0.016") and Bonferroni qualifier. This is the optimal placement — the reader encounters the justification at the exact moment of the statistical claim. The sentence is self-contained and does not require the reader to hold prior context.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.946 |
| **Threshold** | 0.95 (publication artifact, C4) |
| **Verdict** | REVISE |
| **Delta from i3** | +0.009 (0.937 → 0.946) |
| **Delta from i1** | +0.070 (0.876 → 0.946) |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | i3 Score | i4 Score | i4 Weighted | Delta | Evidence Summary |
|-----------|--------|----------|----------|-------------|-------|-----------------|
| Completeness | 0.20 | 0.95 | 0.95 | 0.190 | 0.00 | No new changes; all i3 elements intact |
| Internal Consistency | 0.20 | 0.95 | 0.95 | 0.190 | 0.00 | 6-of-9 arithmetic explicit and Ferraz venue harmonized, but both were minor/cosmetic; uncertain increment resolved downward |
| Methodological Rigor | 0.20 | 0.93 | 0.95 | 0.190 | +0.02 | McNemar rationale sentence added (lines 60-61) — the binding i3 gap is closed |
| Evidence Quality | 0.15 | 0.93 | 0.94 | 0.141 | +0.01 | "established by peer-reviewed research" replaces "settled science" — precision fix on borderline characterization |
| Actionability | 0.15 | 0.95 | 0.95 | 0.143 | 0.00 | Unchanged; five concrete, data-grounded, code-backed actions |
| Traceability | 0.10 | 0.88 | 0.92 | 0.092 | +0.04 | Barreto & Jana title added; Ferraz venue consistent — both i3 Traceability gaps closed |
| **TOTAL** | **1.00** | **0.937** | | **0.946** | **+0.009** | |

**Composite arithmetic verification (H-15):** 0.190 + 0.190 + 0.190 + 0.141 + 0.143 + 0.092 = **0.946**

---

## Detailed Dimension Analysis

### Completeness (0.95/1.00)

**Evidence:**

No new changes in this dimension from i3. All completeness elements remain intact and verified:
- Problem framing (compliance degradation, production context): present
- Research overview (six weeks, six phases, 75 sources): present
- Experimental design (90 matched pairs, 270 invocations, three models, 10 constraints, three conditions, blind scoring): present and accurate
- Primary results (100% C3 compliance, 7.8% C1 violation rate with 95% CI, p = 0.016 with marginal Bonferroni qualifier): all present
- CI surfaced in Results paragraph (line 58): present (i3 fix, still intact)
- NPT-013 three-component explanation: present
- Five actionable steps with before/after code example: present
- Caveats (effect size, single-session, test scope, mechanistic gap): all present
- Conclusion ("Structure Beats Polarity" analytical beat): present

**Gaps:**

Same minor gap as i3: the CI lower bound (2.3%) is disclosed but the article does not flag symmetrically that the true effect may also be smaller. One-directional CI framing ("the true effect may be larger") is acceptable at the article genre.

**Improvement Path:**

At 0.95, the remaining gap is a symmetric framing refinement in the Caveats section. Addressing it would target 0.96, but this is a minor polish item and not required for the 0.95 publication threshold.

---

### Internal Consistency (0.95/1.00)

**Evidence:**

Two i4 improvements were applied to this dimension:

**Fix 3a (6-of-9 arithmetic):** Line 68 now reads "two-thirds (6 of 9, 67%) landed on a single constraint type: behavioral timing rules." The i3 gap was that the reader had to infer the "6 of 9" subset from "7 C1 + 2 C2 = 9 total" and separately infer which landed on behavioral-timing. The fix makes the count and fraction explicit. No arithmetic path is left to inference for this claim.

**Fix 3b (Ferraz venue):** The "Findings" designation is now present in both body (line 38: "EMNLP 2024 Findings") and footnote (line 137: "EMNLP 2024 Findings"). The i3 venue inconsistency is closed.

All i1 and i2 factual corrections remain intact:
- Pair count: "90 matched pairs" consistent (lines 44, 56, 58, 68)
- Test name: "McNemar's exact test on matched pairs" at line 60 and footnote; zero Fisher's instances
- Bonferroni qualifier: "marginally (p = 0.016 vs. adjusted alpha = 0.0167)" — both values present

Model-level improvement figures (Haiku 10pp, Sonnet 6.7pp, Opus 6.7pp) remain internally consistent with source compliance matrix.

**Scoring rationale — why 0.95 rather than 0.96:**

Both fixes addressed gaps rated as "minor" and "cosmetic" in the i3 report. The dimension was already at 0.95 with no material contradictions. The rubric for 0.9+ is "No contradictions, all claims aligned" — the article was already meeting this criterion at 0.95. Moving to 0.96 requires evidence of meaningful improvement beyond cosmetic polish. Per the S-014 leniency bias rule (uncertain score increments resolved downward), the score is held at 0.95. The fixes are acknowledged as real improvements but insufficient to cross the 0.95-to-0.96 boundary.

**Gaps:**

No material internal consistency gaps remain. The article is clean across all statistical figures.

**Improvement Path:**

At 0.95, the dimension is at the top of the "most claims aligned" band. No actionable gaps remain for this iteration.

---

### Methodological Rigor (0.95/1.00)

**Evidence:**

Fix 1 is applied correctly and completely. Line 60-61:

> "McNemar's test is designed for matched-pair designs, where each pair controls for constraint-specific difficulty -- an independent-group test like chi-square would misattribute within-pair variation to the framing condition."

This sentence does three things:
1. Names the design property that mandates McNemar (matched-pair structure)
2. Names what the pairs control for (constraint-specific difficulty)
3. Names the alternative test (chi-square) and the specific error it would introduce (misattributing within-pair variation)

This is precisely what a statistical reviewer would need to see. The rationale is complete, technically accurate, and appropriately brief for the article genre. The i3 binding gap is closed.

The remaining methodology elements from i3 remain intact:
- Three framing conditions with concrete examples (lines 48-51): present
- Adversarial pressure scenario design described (line 44): present
- Blind scoring with separate model instance (line 52): present
- Inter-rater reliability: 10% double-scoring, 92.6% agreement, Gwet's AC1 = 0.920 (footnote): present
- Effect size below pre-specified threshold explicitly acknowledged (line 119): present
- Contingency pathway in plain language (line 119): present
- CI in Results paragraph (line 58): present

**Gap (Low severity, unchanged from i3):**

The power analysis (80% power to detect pi_d >= 0.10) remains absent from the article. The Caveats section acknowledges the effect fell below the pre-specified threshold but does not explain the sample size rationale. This is acceptable at the Medium article genre; a methodological appendix would be the appropriate venue.

**Scoring rationale — why 0.95 and not 0.94 or 0.96:**

The i3 report identified the McNemar rationale as the binding gap for this dimension and projected it would move the score from 0.93 to 0.95. That projection is now confirmed. The remaining gap (power analysis) is rated Low severity at the genre level. The rubric for 0.9+ is "Rigorous methodology, well-structured." With the McNemar rationale in place, the article now meets this criterion. 0.95 is the correct landing point: the methodology is rigorous and well-documented for the format, with one low-severity genre-appropriate omission. This is not leniency — it is calibrated recognition that the binding gap was specifically identified and specifically fixed.

**Improvement Path:**

To reach 0.97: Add a parenthetical in Caveats explaining sample size rationale: "The 90-pair design was sized to detect a minimum 10% difference (pi_d >= 0.10) with 80% power at alpha = 0.05." This is optional polish; the article reads as rigorous without it.

---

### Evidence Quality (0.94/1.00)

**Evidence:**

Fix 4 is applied. Line 38 now reads "That much is established by peer-reviewed research" in place of i3's "That much is settled science." The replacement is more precise for a T1+T3 evidence base — "established by peer-reviewed research" accurately represents the state of the literature without overstating consensus ("settled" implies T1 unanimity; T1+T3 warrants the more measured "established").

The i3 evidence qualification fixes remain intact:
- "One plausible explanation for the effect we observed: LLMs process instructions as weighted priorities...We have not isolated this mechanism experimentally, but the pattern is consistent across our data." (Line 84): Both qualifications present.

The two Geng and Ferraz citations remain accurately characterized:
- Geng et al.: "standalone prohibitions fail within instruction hierarchies" — accurate characterization of A-20 (AAAI 2026).
- Ferraz et al.: "structured constraint decomposition improves compliance by 7-8% over bare prohibitions" — accurate characterization of A-15 (EMNLP 2024) DeCRIM result.

**Scoring rationale — why 0.94 and not 0.93 or 0.95:**

The "settled science" characterization was identified in i3 as a precision gap warranting a +0.01 weighted score increase (the improvement path table projected 0.93 → 0.94 for this fix). That fix is now applied. 0.94 reflects the closure of this specific minor gap. A score of 0.95 would require that all claims be supported by credible evidence at the 0.9+ rubric standard ("All claims with credible citations"). The article still has the "LLMs process as weighted priorities" hypothesis, which is correctly qualified but inherently mechanistic speculation. This is the appropriate genre-level constraint on the score. 0.94 is the honest landing point.

**Gaps:**

No new gaps introduced. The Barreto & Jana paper (A-23) is correctly limited to footnote mention — the article accurately does not use the +25.14% negation reasoning accuracy figure as behavioral compliance evidence (consistent with KF-007 in final-synthesis).

**Improvement Path:**

To reach 0.95: The mechanistic hypothesis ("One plausible explanation...LLMs process instructions as weighted priorities") is inherently unverifiable at current experimental scope. No single-sentence fix closes this gap. Future work section or a comparative mechanism study would be required. This is not a revision target for this article.

---

### Actionability (0.95/1.00)

**Evidence:**

Unchanged from i3. The actionability section remains the strongest dimension:

1. Audit for blunt prohibitions: search terms specified ("don't," "never," "must not"), characterization accurate
2. Convert to NPT-013: complete before/after code example with all three components correctly represented
3. Prioritize behavioral-timing constraints: grounded in data (56% violation rate for the most vulnerable constraint type)
4. Extra attention to smaller models: grounded in per-model data (Haiku 10pp vs. Sonnet/Opus 6.7pp), practical routing implication stated
5. Consequence specificity: good/bad example present, specificity rationale explained

Action ordering is correct and matches PROJ-014's own priority structure.

**Gaps:**

Same scope limitation as i3: no guidance on constraint batching order within a system prompt audit. Appropriate for an 8-minute article.

**Improvement Path:**

At 0.95, no material actionability gaps remain for this article format.

---

### Traceability (0.92/1.00)

**Evidence:**

Both remaining i3 traceability gaps are now closed:

**Gap 1 (Barreto & Jana title) — CLOSED:** The footnote now reads: "Barreto & Jana, 'This is not a Disimprovement: Improving Negation Reasoning in Large Language Models via Prompt Engineering,' EMNLP 2025 Findings ([ACL Anthology](https://aclanthology.org/2025.findings-emnlp.761))." Full title, venue with track designation, and URL — all three citation components present. The Barreto & Jana citation is now at the same completeness level as the Geng and Ferraz citations.

**Gap 2 (Ferraz venue inconsistency) — CLOSED:** "EMNLP 2024 Findings" appears in both the body (line 38) and the footnote (line 137). The cosmetic inconsistency from i3 is eliminated.

All previously closed traceability items remain intact:
- Geng et al. full title ("Control Illusion...") + arXiv URL: inline body (line 38) and footnote (line 137)
- Ferraz et al. full title ("LLM Self-Correction with DeCRIM") + arXiv URL: inline body (line 38) and footnote (line 137)
- GitHub URL for experimental artifacts: footnote (line 137)

**Scoring rationale — why 0.92 and not 0.90 or 0.94:**

The i3 improvement path stated "To reach 0.92: Add Barreto & Jana paper title + harmonize Ferraz venue." Both are done. The 0.92 landing point is the direct implementation of the i3 projection. The score of 0.92 reflects "most items traceable" at the 0.9+ rubric band — all three primary academic sources now have full citation chains (title + venue + URL). The article does not reach 0.94+ because: (a) Barreto & Jana appears only in the footnote, not inline in the body (the paper is correctly not cited inline as its finding is negation accuracy, not behavioral compliance); (b) the GitHub URL is footnote-only. For a Medium article, footnote-level traceability for supporting sources is appropriate and meets the "most items traceable" standard. A 0.94 score would require full inline traceability for all sources — appropriate for a technical paper, not an 8-minute general-audience article.

**Gaps:**

No remaining gaps rise above Low severity. The citation chain for the three primary sources is now complete.

**Improvement Path:**

To reach 0.94 at Medium article norms: No further improvement is realistically achievable at this format. A general-audience article with three fully cited academic sources (title + venue + URL, all resolvable) meets the traceability standard for the genre.

---

## I3 Gap Closure Summary

| i3 Gap | Priority | i4 Fix Applied | Closure Status | Score Impact |
|--------|----------|---------------|----------------|-------------|
| Methodological Rigor: McNemar rationale absent (binding gap) | P1 | "McNemar's test is designed for matched-pair designs..." sentence added at line 60-61 | **CLOSED** | +0.02 on MR score (0.93 → 0.95) |
| Traceability: Barreto & Jana title absent from footnote | P2 | Full paper title added to footnote citation | **CLOSED** | Part of +0.04 on Traceability (0.88 → 0.92) |
| Internal Consistency: Ferraz venue inconsistent | P3 | "EMNLP 2024 Findings" now in both body and footnote | **CLOSED** | Minor; uncertain increment resolved downward, IC held at 0.95 |
| Internal Consistency: 6-of-9 arithmetic implicit | P3 | "two-thirds (6 of 9, 67%)" explicit at line 68 | **CLOSED** | Minor; uncertain increment resolved downward, IC held at 0.95 |
| Evidence Quality: "settled science" imprecise | P4 | "established by peer-reviewed research" | **CLOSED** | +0.01 on EQ score (0.93 → 0.94) |

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.94 | 0.96 | The mechanistic hypothesis ("One plausible explanation...LLMs process instructions as weighted priorities") cannot be elevated to 0.95+ without experimental evidence. However, adding a brief forward pointer — "this is a question for mechanistic interpretability research" — would signal intellectual honesty about the gap. Low-leverage given the existing qualification. |
| 2 | Traceability | 0.92 | 0.94 | Footnote-only placement of Barreto & Jana is appropriate given the paper's subject (negation accuracy, not behavioral compliance). No practical improvement available within this article's scope without misrepresenting what A-23 contributes. |
| 3 | Completeness | 0.95 | 0.96 | Add symmetric CI framing: "the CI also extends down to 2.3 percentage points, suggesting the true effect may be smaller than observed." Optional polish. |
| 4 | Methodological Rigor | 0.95 | 0.97 | Add power analysis rationale parenthetical in Caveats: "The 90-pair design was powered at 80% to detect pi_d >= 0.10 at alpha = 0.05." Optional for the article genre. |

**Key observation:** The remaining gaps across all four dimensions are at or near the genre-appropriate ceiling for an 8-minute general-audience Medium article. The gap between 0.946 and 0.950 is not a deficiency in the article's substance — it reflects the inherent ceiling of traceability and evidence quality norms at the Medium format level. The path to 0.950 requires approximately +0.004 weighted improvement across two or three dimensions from genuinely marginal items.

---

## Composite Score Pathway to 0.950

| Fix Available | Dimension | Current | Projected | Weighted Impact | Feasibility |
|---------------|-----------|---------|-----------|----------------|-------------|
| Symmetric CI framing | Completeness | 0.95 | 0.96 | +0.002 | High (one sentence in Caveats) |
| Power analysis note | Methodological Rigor | 0.95 | 0.96 | +0.002 | High (one sentence in Caveats) |
| Mechanistic forward pointer | Evidence Quality | 0.94 | 0.95 | +0.002 | Medium (one phrase in Why Three Components Work section) |
| Traceability ceiling | Traceability | 0.92 | 0.92 | 0.000 | Genre ceiling reached |
| **Projected composite** | | **0.946** | **~0.952** | **+0.006** | If all three applied |

**Note on projections:** Projected scores are upper bounds under conservative S-014 leniency bias counteraction. Any single fix applied alone reaches ~0.948. All three together project ~0.952. Given the proximity to the 0.950 threshold, the recommendation is to apply all three simultaneously in i5.

---

## Iteration Score Progression

| Iteration | Score | Delta | Verdict | Binding Constraint | Key Changes |
|-----------|-------|-------|---------|-------------------|-------------|
| i1 | 0.876 | baseline | REVISE | Internal Consistency (three mechanical errors) | Baseline article |
| i2 | 0.913 | +0.037 | REVISE | Evidence Quality (0.88) | Three errors fixed; voice compliance |
| i3 | 0.937 | +0.024 | REVISE | Methodological Rigor (0.93) | Evidence qualified; citations added; CI in Results |
| i4 | 0.946 | +0.009 | REVISE | Traceability (0.92) | McNemar rationale; Barreto title; 6-of-9 explicit; venue harmonized; "established by peer-reviewed research" |

**Diminishing returns pattern:** Deltas are converging: +0.037, +0.024, +0.009. This is expected as the article approaches genre ceiling. The remaining 0.004 gap to 0.950 is addressable but requires targeting genuinely marginal improvements.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented with specific line references and direct quotation for each fix
- [x] Uncertain score increments resolved downward: Internal Consistency held at 0.95 despite two closed gaps (both rated minor/cosmetic in i3); Traceability scored at 0.92 per i3 projection rather than 0.94 (genre ceiling reasoning applied)
- [x] No dimension scored above 0.95 without exceptional evidence (Completeness and Actionability at 0.95 — established in i3 with full evidence; Methodological Rigor at 0.95 — justified by closure of the specific binding gap identified in i3)
- [x] Composite verified by arithmetic: 0.190 + 0.190 + 0.190 + 0.141 + 0.143 + 0.092 = 0.946
- [x] Verdict cross-checked: 0.946 falls below the 0.95 custom threshold; REVISE verdict is correct
- [x] i4 fixes verified individually with direct text evidence before scoring
- [x] i3 projected composite (~0.950) vs. actual i4 result (0.946): discrepancy explained by Internal Consistency resolved downward (projection assumed +0.002; actual 0.000) and Traceability landing at 0.92 rather than projected 0.90 (+0.002 offset). Net effect: approximately cancels, with actual result 0.004 below projection — consistent with conservative S-014 leniency bias counteraction
- [x] Diminishing-returns calibration applied: +0.009 delta at i4 is consistent with the convergence pattern from i1-i3 (+0.037, +0.024)
- [x] McNemar rationale sentence scored as fixing the binding Methodological Rigor gap (which it directly and specifically addresses per the i3 improvement path)

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.946
threshold: 0.95
weakest_dimension: Traceability
weakest_score: 0.92
binding_constraint_dimension: None (previous binding constraint Methodological Rigor is now resolved)
binding_constraint_score: N/A
critical_findings_count: 0
publication_blocking_count: 0
iteration: 4
delta_from_i3: +0.009
delta_from_i1: +0.070
i4_fixes_confirmed:
  - mcnemar_rationale: CLOSED (lines 60-61, complete rationale with alternative test named)
  - barreto_jana_title: CLOSED (footnote line 137, full title present)
  - 6_of_9_arithmetic: CLOSED (line 68, fraction + count + percentage explicit)
  - ferraz_venue_harmonized: CLOSED (body and footnote both read "EMNLP 2024 Findings")
  - settled_science_replaced: CLOSED (line 38, "established by peer-reviewed research")
open_gaps:
  - Symmetric CI framing missing (Completeness, Low severity): current one-directional framing "true effect may be larger" does not mention "also may be smaller"
  - Power analysis rationale absent (Methodological Rigor, Low severity): sample size rationale not stated
  - Mechanistic hypothesis unresolved (Evidence Quality, Low severity): inherently unverifiable; requires mechanistic study
  - Traceability at genre ceiling (0.92): Barreto & Jana footnote-only is appropriate; no practical improvement available
gap_to_threshold: 0.004
improvement_recommendations:
  - "Add symmetric CI framing in Caveats (Completeness): 'the CI also extends down to 2.3 percentage points, suggesting the true effect may also be smaller than observed.' (+0.002 weighted)"
  - "Add power analysis note in Caveats (Methodological Rigor): 'The 90-pair design was powered at 80% to detect pi_d >= 0.10 at alpha = 0.05.' (+0.002 weighted)"
  - "Add mechanistic forward pointer (Evidence Quality): 'isolating which component drives the effect is a question for mechanistic interpretability research.' (+0.002 weighted)"
path_to_pass:
  - "All three i5 fixes applied: projected ~0.952 (above 0.950 threshold)"
  - "Any two applied: ~0.950 (marginally at threshold; uncertain; all three recommended)"
  - "Single fix alone: ~0.948 (insufficient)"
  - "Note: projections are conservative upper bounds per S-014 leniency counteraction"
```

---

*Scored by: adv-scorer (S-014 LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Source research verified: `orchestration/neg-prompting-20260227-001/phase-6/final-synthesis.md`*
*Prior gates: `adversary-gates/task-027-gate.md` (i1), `adversary-gates/task-027-gate-i2.md` (i2), `adversary-gates/task-027-gate-i3.md` (i3)*
*Date: 2026-03-01*
