# Quality Score Report: PROJ-014 Medium Article (Iteration 5 — FINAL)

## L0 Executive Summary

**Score:** 0.952/1.00 | **Verdict:** PASS | **Weakest Dimension:** Traceability (0.92)
**One-line assessment:** All three i5 fixes are confirmed applied and genuine — symmetric CI framing, power analysis note, and mechanistic forward pointer — lifting the composite from 0.946 to 0.952, clearing the 0.95 publication threshold; the article is approved for publication.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/proj-014-completion-20260301-001/articles/medium-negative-prompting.md`
- **Deliverable Type:** Other (Medium publication article, external audience)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-01T00:00:00Z
- **Custom threshold:** 0.95 (per task specification; publication artifact, C4)
- **Prior Score (i4):** 0.946 REVISE
- **Prior Score (i3):** 0.937 REVISE
- **Prior Score (i2):** 0.913 REVISE
- **Prior Score (i1):** 0.876 REVISE
- **Iteration:** 5 (FINAL — FA-03 max 5)
- **Strategy Findings Incorporated:** No (standalone scoring)

---

## I5 Fix Verification

All three fixes specified in the i4 gate report improvement pathway are verified against the article text.

| Fix | Target | i5 Status | Evidence |
|-----|--------|-----------|----------|
| 1. Symmetric CI framing | Caveats: add "though it may also be as small as 2.3 percentage points" | **CONFIRMED FIXED** | Line 119: "The 95% confidence interval (2.3% to 13.3%) does overlap with 10%, so the true effect may be larger than what we observed, though it may also be as small as 2.3 percentage points." The symmetric framing is present and appended correctly after the one-directional "may be larger" clause. Both directions (larger and smaller) are now explicitly stated. |
| 2. Power analysis note | Caveats: state that 90-pair sample was sized for 10-pp detection at 80% power | **CONFIRMED FIXED** | Line 119: "Our sample of 90 matched pairs was sized to detect a 10-percentage-point difference with 80% power, and we proceeded under a pre-registered contingency pathway..." The power analysis rationale appears in the correct location (Caveats, immediately adjacent to the effect-size discussion). Both the sample size (90) and power (80%) and target effect (10 pp) are present. |
| 3. Mechanistic forward pointer | "Why Three Components Work" section: forward pointer that isolating component contributions is future work | **CONFIRMED FIXED** | Line 84: "We have not isolated this mechanism experimentally, but the pattern is consistent across our data. Isolating which of the three components contributes most to the effect is a question for future work." The forward pointer is correctly placed after the mechanistic hypothesis qualifier. It is concise, accurate, and signals intellectual honesty without requiring any new claims. |

**Placement quality assessment:**

- **Fix 1 (symmetric CI):** The "though it may also be as small as 2.3 percentage points" clause is appended at the end of the existing CI sentence, immediately after the "may be larger" clause. The reader encounters both directions of uncertainty in a single sentence. Correct placement.
- **Fix 2 (power analysis):** The power note is integrated into the Caveats effect-size paragraph, appearing before the Bonferroni/contingency discussion. The reader sees the sample size rationale at exactly the moment they are evaluating the effect-size claim. Correct placement.
- **Fix 3 (forward pointer):** Placed within the "Why Three Components Work" section immediately after the mechanistic hypothesis ("We have not isolated this mechanism experimentally, but the pattern is consistent across our data."). The forward pointer explicitly names "future work" as the resolution path. This is the correct framing: it does not oversell the hypothesis and does not create an unfulfilled promise.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.952 |
| **Threshold** | 0.95 (publication artifact, C4) |
| **Verdict** | **PASS** |
| **Delta from i4** | +0.006 (0.946 → 0.952) |
| **Delta from i1** | +0.076 (0.876 → 0.952) |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | i4 Score | i5 Score | i5 Weighted | Delta | Evidence Summary |
|-----------|--------|----------|----------|-------------|-------|-----------------|
| Completeness | 0.20 | 0.95 | 0.96 | 0.192 | +0.01 | Symmetric CI framing closes the one-directional CI presentation gap from i4 |
| Internal Consistency | 0.20 | 0.95 | 0.95 | 0.190 | 0.00 | No changes; article remains internally consistent; no new contradictions introduced |
| Methodological Rigor | 0.20 | 0.95 | 0.96 | 0.192 | +0.01 | Power analysis note added in Caveats — completes the sample-size rationale chain |
| Evidence Quality | 0.15 | 0.94 | 0.95 | 0.143 | +0.01 | Mechanistic forward pointer added — closes the "unresolvable hypothesis" presentation gap |
| Actionability | 0.15 | 0.95 | 0.95 | 0.143 | 0.00 | Unchanged; five concrete, data-grounded, code-backed actions remain intact |
| Traceability | 0.10 | 0.92 | 0.92 | 0.092 | 0.00 | Genre ceiling; no new traceability changes; all three primary citations complete |
| **TOTAL** | **1.00** | **0.946** | | **0.952** | **+0.006** | |

**Composite arithmetic verification (H-15):** 0.192 + 0.190 + 0.192 + 0.143 + 0.143 + 0.092 = **0.952**

---

## Detailed Dimension Analysis

### Completeness (0.96/1.00)

**Evidence:**

The i4 report identified a single remaining Completeness gap: one-directional CI framing in the Caveats section. The original text read: "the true effect may be larger than what we observed." This suggested the CI only warranted optimism about effect size, omitting the equally valid possibility that the true effect is near the lower CI bound.

Fix 1 closes this gap. Line 119 now reads:

> "The 95% confidence interval (2.3% to 13.3%) does overlap with 10%, so the true effect may be larger than what we observed, though it may also be as small as 2.3 percentage points."

Both directions of CI uncertainty are now present. A reader can accurately understand that: (a) the true effect may be as large as 13.3 percentage points, and (b) the true effect may be as small as 2.3 percentage points. The fix is symmetric and accurate.

All pre-existing Completeness elements remain intact from i4:
- Problem framing (compliance degradation, production context): present
- Research overview (six weeks, six phases, 75 sources): present
- Experimental design (90 matched pairs, 270 invocations, three models, 10 constraints, three conditions, blind scoring): present
- Primary results (100% C3 compliance, 7.8% C1 violation rate with 95% CI, p = 0.016 with Bonferroni qualifier): present
- NPT-013 three-component explanation with component-level rationale: present
- Five actionable steps with before/after code example: present
- Caveats (effect size, single-session, test scope, mechanistic gap): all present
- Conclusion ("Structure Beats Polarity" analytical beat): present

**Gaps:**

No material gaps remain at the Medium article genre level. The CI presentation is now complete and symmetric.

**Improvement Path:**

At 0.96, the remaining gap is genre-level ceiling. No actionable completeness gaps remain.

**Scoring rationale — why 0.96 and not 0.95 or 0.97:**

The i4 report projected Completeness improvement from 0.95 to 0.96 with the symmetric CI fix ("High feasibility, one sentence in Caveats"). The fix is applied exactly as projected. 0.96 reflects this specific closure. A score of 0.97 would require material new information not present (e.g., an extended discussion of multi-turn degradation scenarios, which would exceed the article format). Per S-014 leniency rules, the uncertain increment above 0.96 is resolved downward. 0.96 is the correct landing point.

---

### Internal Consistency (0.95/1.00)

**Evidence:**

No new changes applied in i5 that affect this dimension. The three i5 fixes each target specific gaps in other dimensions (Completeness, Methodological Rigor, Evidence Quality) without introducing any new claims or data points that could conflict with existing content.

All i4 internal consistency elements remain intact:
- Pair count: "90 matched pairs" consistent in lines 44, 56, 58, 68, and now line 119 (power note) — five occurrences, all consistent
- Test name: "McNemar's exact test on matched pairs" in line 60 and footnote — zero Fisher's or chi-square instances used incorrectly
- Bonferroni qualifier: "marginally (p = 0.016 vs. adjusted alpha = 0.0167)" — both values present and arithmetically correct
- 6-of-9 arithmetic: "two-thirds (6 of 9, 67%)" explicit at line 68 — closed in i4, intact in i5
- Ferraz venue: "EMNLP 2024 Findings" in both body (line 38) and footnote — consistent, intact from i4

The power analysis note introduced in Fix 2 (line 119: "90 matched pairs...sized to detect a 10-percentage-point difference with 80% power") is consistent with the pre-specified threshold already stated ("Our pre-specified minimum effect size threshold was 10%"). No contradiction introduced.

**Gaps:**

No material internal consistency gaps remain. The article is arithmetically clean across all statistical figures.

**Improvement Path:**

At 0.95, no actionable internal consistency gaps remain. A 0.96+ score would require essentially no minor inconsistencies of any kind, which this article achieves on all statistical claims. The 0.95 ceiling reflects a residual minor gap: the "LLMs process instructions as weighted priorities" mechanistic claim is framed as "one plausible explanation" but is not formally marked as hypothesis-level reasoning in the article's structure. This is a presentation convention gap, not a contradiction. Resolving it to 0.96 would require restructuring the paragraph, which is not warranted for this format.

---

### Methodological Rigor (0.96/1.00)

**Evidence:**

Fix 2 is applied correctly and completely. Line 119 now includes:

> "Our sample of 90 matched pairs was sized to detect a 10-percentage-point difference with 80% power, and we proceeded under a pre-registered contingency pathway that treats the format choice as convention-aligned rather than effectiveness-mandated."

This sentence does three things:
1. States the sample size (90 matched pairs) — consistent with the design description at line 44
2. States the detection target (10-percentage-point difference) — consistent with the "pre-specified minimum effect size threshold was 10%" already present in i4
3. States the power level (80%) — previously absent; now present

The power analysis rationale is now in the Caveats section where it belongs: immediately adjacent to the effect-size discussion, allowing the reader to understand simultaneously (a) what the effect size was, (b) what the design was powered to detect, and (c) how the contingency pathway operated.

All i4 methodology elements remain intact:
- Three framing conditions with concrete examples (lines 48-51): present
- Adversarial pressure scenario design (line 44): present
- Blind scoring with separate model instance (line 52): present
- McNemar's exact test rationale (lines 60-61, closed in i4): present
- Inter-rater reliability: 10% double-scoring, 92.6% agreement, Gwet's AC1 = 0.920 (footnote): present
- Effect size below pre-specified threshold acknowledged (line 119): present
- Contingency pathway in plain language (line 119): present
- CI in Results paragraph (line 58): present

**Gaps:**

No material methodological rigor gaps remain at the Medium article genre level. The power analysis note completes the sample size rationale chain.

**Scoring rationale — why 0.96 and not 0.95 or 0.97:**

The i4 improvement path stated "To reach 0.97: Add parenthetical in Caveats explaining sample size rationale." The fix applied is equivalent in content but more naturally integrated (a sentence rather than a parenthetical). This achieves approximately the projected improvement but not the full 0.97, because: (a) the sentence is correctly included but the alpha level (0.05) is not stated alongside the power and target; (b) the McNemar design justification was the binding gap resolved in i4, and this fix addresses the secondary gap. Per S-014 leniency rules, 0.96 is the correct landing: genuinely improved by the power note addition, but not at the 0.97 level which would require complete statistical reporting including alpha. A score of 0.96 is defensible because the rubric for 0.9+ is "Rigorous methodology, well-structured" — the article now documents all key design parameters: sample size, test, power, detection target, and contingency pathway.

---

### Evidence Quality (0.95/1.00)

**Evidence:**

Fix 3 is applied correctly. Line 84 now reads:

> "We have not isolated this mechanism experimentally, but the pattern is consistent across our data. Isolating which of the three components contributes most to the effect is a question for future work."

Before the fix, the mechanistic hypothesis ended with "the pattern is consistent across our data" — a correct qualification but one that left the reader without a resolution path for the inherently unverifiable claim. The forward pointer now explicitly names future work as the venue for resolution.

This is precisely the i4-recommended fix: "Adding a brief forward pointer — 'this is a question for mechanistic interpretability research' — would signal intellectual honesty about the gap." The actual text uses "a question for future work" rather than "mechanistic interpretability research" — this is a marginally less specific formulation, but it is more accurate (the needed work is not exclusively interpretability; it could also be ablation studies on NPT-013 components). The forward pointer is present and functionally complete.

Evidence quality elements from i4 remain intact:
- "established by peer-reviewed research" (closed i4, line 38): intact
- "One plausible explanation...We have not isolated this mechanism experimentally" (line 84): intact
- Geng et al. and Ferraz et al. accurately characterized (line 38): intact
- A-23 (Barreto & Jana) correctly limited to footnote (not used as behavioral compliance evidence): intact

**Scoring rationale — why 0.95 and not 0.94 or 0.96:**

The i4 report projected Evidence Quality improvement from 0.94 to 0.95 with the mechanistic forward pointer ("Medium feasibility, one phrase in Why Three Components Work section"). The fix is applied, achieving the projected improvement. At 0.95, the article meets the rubric criterion "Most claims supported" and crosses into "All claims with credible citations" territory for its primary empirical claims. The residual ceiling: the forward pointer uses "future work" rather than naming a specific research approach, which is a minor specificity gap. A score of 0.96 would require essentially complete evidence qualification with specific resolution paths — reasonable for a technical paper but not for an 8-minute Medium article. 0.95 is the correct landing point.

**Gaps:**

No actionable Evidence Quality gaps remain at the Medium article genre level.

---

### Actionability (0.95/1.00)

**Evidence:**

Unchanged from i4. The five-step actionability section remains the strongest dimension of the article and no i5 changes affect it:

1. Audit for blunt prohibitions: search terms specified ("don't," "never," "must not"), low-hanging fruit characterization accurate
2. Convert to NPT-013: complete before/after code example with all three components correctly represented and labeled
3. Prioritize behavioral-timing constraints: grounded in data (56% violation rate for the most vulnerable constraint type cited at line 68)
4. Extra attention to smaller models: grounded in per-model data (Haiku 10pp vs. Sonnet/Opus 6.7pp at line 74), practical routing implication stated
5. Consequence specificity: specific/vague example present, specificity rationale explained with concrete contrast

Action ordering is correct and matches PROJ-014's priority structure (timing constraints first, then model tier, then specificity).

**Gaps:**

Same scope limitation as i4: no guidance on constraint batching order within a system prompt audit. Appropriate for an 8-minute article.

**Improvement Path:**

At 0.95, no material actionability gaps remain for this article format. A 0.96 score would require adding guidance that would extend the article beyond its intended length.

---

### Traceability (0.92/1.00)

**Evidence:**

No i5 changes affect the traceability dimension. All three i5 fixes (symmetric CI framing, power analysis note, mechanistic forward pointer) add framing or editorial commentary rather than new claims requiring citation. No new sources are introduced. No existing citation chains are altered.

All i4 traceability elements remain intact:
- Geng et al. full title ("Control Illusion: The Failure of Instruction Hierarchies in Large Language Models") + AAAI 2026 + arXiv URL: inline body (line 38) and footnote (line 137) — complete
- Ferraz et al. full title ("LLM Self-Correction with DeCRIM") + "EMNLP 2024 Findings" + arXiv URL: inline body (line 38) and footnote (line 137) — complete and consistent
- Barreto & Jana full title ("This is not a Disimprovement: Improving Negation Reasoning in Large Language Models via Prompt Engineering") + "EMNLP 2025 Findings" + ACL Anthology URL: footnote (line 137) — complete
- GitHub URL for experimental artifacts: footnote (line 137)
- Methodology details: blind scoring, 10% double-scoring, 92.6% agreement, Gwet's AC1 = 0.920 in footnote

**Scoring rationale — why 0.92 held and not increased:**

The i4 report concluded that 0.92 is the genre ceiling for this article: "A general-audience article with three fully cited academic sources (title + venue + URL, all resolvable) meets the traceability standard for the genre." No i5 fixes address traceability, so no increment is warranted. The 0.92 score reflects "most items traceable" at the 0.9+ rubric band — all three primary academic sources have full citation chains, and the GitHub artifact link provides further traceability. The dimension is at its genre ceiling; no further improvement is achievable within this article format.

**Gaps:**

No new gaps. No gaps closed. Traceability is at genre ceiling.

**Improvement Path:**

None available within this article format. A 0.94+ score would require full inline traceability for all sources — appropriate for a technical paper, not an 8-minute general-audience article.

---

## I4 Gap Closure Summary (i5 perspective)

| i4 Gap | Priority | i5 Fix Applied | Closure Status | Score Impact |
|--------|----------|---------------|----------------|-------------|
| Completeness: one-directional CI framing | P1 | "though it may also be as small as 2.3 percentage points" appended (line 119) | **CLOSED** | +0.01 on Completeness (0.95 → 0.96); +0.002 weighted |
| Methodological Rigor: power analysis absent | P2 | "Our sample of 90 matched pairs was sized to detect a 10-percentage-point difference with 80% power" added (line 119) | **CLOSED** | +0.01 on MR (0.95 → 0.96); +0.002 weighted |
| Evidence Quality: mechanistic hypothesis unresolved | P3 | "Isolating which of the three components contributes most to the effect is a question for future work." added (line 84) | **CLOSED** | +0.01 on EQ (0.94 → 0.95); +0.002 weighted (after 0.15 weight rounding: 0.001 visible) |
| Traceability: genre ceiling | N/A | No fix targeted | NOT APPLICABLE — genre ceiling confirmed | 0.00 |

**Net composite improvement:** +0.006 (0.946 → 0.952). The i4 projection was "all three applied: projected ~0.952" — actual result matches projection exactly. This confirms the i4 scoring was well-calibrated.

---

## Improvement Recommendations (Priority Ordered)

This is iteration 5 (FINAL — FA-03 max). The article has cleared the 0.95 threshold. The following residual gaps are documented for completeness but do not block publication.

| Priority | Dimension | Current | Gap | Note |
|----------|-----------|---------|-----|------|
| 1 | Traceability | 0.92 | Genre ceiling | Three fully cited academic sources at title+venue+URL completeness. No practical improvement available within Medium format. |
| 2 | Internal Consistency | 0.95 | Presentation convention | Mechanistic hypothesis framing could be structurally separated from empirical claims. Not a contradiction; not a revision target. |
| 3 | Methodological Rigor | 0.96 | Alpha not stated | Power note does not include alpha = 0.05. Appropriate for genre; minor completeness gap only. |

**Publication verdict: APPROVED.** No dimension is below 0.92. The composite of 0.952 clears the 0.95 custom threshold. All three i5 fixes are confirmed applied.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented with specific line references and direct quotation for each i5 fix
- [x] Uncertain score increments resolved downward: Internal Consistency held at 0.95 (no i5 changes; no increment warranted); Traceability held at 0.92 (genre ceiling confirmed; no i5 changes)
- [x] Actionability held at 0.95 (no i5 changes; no increment warranted)
- [x] No dimension scored above 0.96 (Completeness and Methodological Rigor at 0.96 — justified by specific single-gap closures per i4 projection; not leniency)
- [x] Evidence Quality moved from 0.94 to 0.95 — the forward pointer is present and functional; 0.95 is the i4-projected landing; uncertain increment to 0.96 resolved downward
- [x] Composite verified by arithmetic: 0.192 + 0.190 + 0.192 + 0.143 + 0.143 + 0.092 = 0.952
- [x] Verdict cross-checked: 0.952 exceeds the 0.95 custom threshold; PASS verdict is correct
- [x] i5 fixes verified individually with direct text evidence before scoring
- [x] i4 projected composite (~0.952) vs. actual i5 result (0.952): projection confirmed exactly — consistent with well-calibrated i4 scoring
- [x] Diminishing-returns calibration applied: +0.006 delta at i5 is consistent with the convergence pattern from i1-i4 (+0.037, +0.024, +0.009, +0.006)
- [x] "Future work" forward pointer (Fix 3) evaluated as functionally equivalent to i4-recommended "mechanistic interpretability research" phrasing; marginally less specific but more accurate — scored at 0.95 rather than 0.96, per leniency counteraction

---

## Iteration Score Progression

| Iteration | Score | Delta | Verdict | Binding Constraint | Key Changes |
|-----------|-------|-------|---------|-------------------|-------------|
| i1 | 0.876 | baseline | REVISE | Internal Consistency (three mechanical errors) | Baseline article |
| i2 | 0.913 | +0.037 | REVISE | Evidence Quality (0.88) | Three errors fixed; voice compliance |
| i3 | 0.937 | +0.024 | REVISE | Methodological Rigor (0.93) | Evidence qualified; citations added; CI in Results |
| i4 | 0.946 | +0.009 | REVISE | Traceability (0.92) / gap to threshold | McNemar rationale; Barreto title; 6-of-9 explicit; venue harmonized; "established by peer-reviewed research" |
| **i5** | **0.952** | **+0.006** | **PASS** | **None — threshold cleared** | **Symmetric CI framing; power analysis note; mechanistic forward pointer** |

**Diminishing-returns pattern:** Deltas: +0.037, +0.024, +0.009, +0.006. Convergence is as expected — each iteration addressed progressively more marginal gaps. The 0.952 terminal score reflects a genuinely polished article that has exhausted all material improvements available within the Medium format constraints.

**Total improvement across 5 iterations:** +0.076 (0.876 → 0.952). The article improved substantively across every phase: mechanical accuracy (i2), evidence qualification and citation completeness (i3), statistical justification (i4), and framing precision (i5).

---

## Session Context Handoff

```yaml
verdict: PASS
composite_score: 0.952
threshold: 0.95
weakest_dimension: Traceability
weakest_score: 0.92
binding_constraint_dimension: None — threshold cleared
binding_constraint_score: N/A
critical_findings_count: 0
publication_blocking_count: 0
iteration: 5
final_iteration: true
fa_03_max_reached: false  # threshold cleared before max; PASS at i5
delta_from_i4: +0.006
delta_from_i1: +0.076
i5_fixes_confirmed:
  - symmetric_ci_framing: CLOSED (line 119, "though it may also be as small as 2.3 percentage points")
  - power_analysis_note: CLOSED (line 119, "90 matched pairs...sized to detect a 10-percentage-point difference with 80% power")
  - mechanistic_forward_pointer: CLOSED (line 84, "Isolating which of the three components contributes most to the effect is a question for future work.")
open_gaps:
  - Traceability at genre ceiling (0.92): no practical improvement available; acceptable for publication
  - Methodological Rigor: alpha not stated in power note (0.05 omitted); minor; not a revision target
  - Internal Consistency: mechanistic claim presentation convention; not a contradiction; not a revision target
publication_status: APPROVED
next_action: Proceed to publication — no further revision required
improvement_recommendations: []  # empty; PASS verdict, no blocking items
```

---

*Scored by: adv-scorer (S-014 LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Source research verified: `orchestration/neg-prompting-20260227-001/phase-6/final-synthesis.md`*
*Prior gates: `adversary-gates/task-027-gate.md` (i1), `adversary-gates/task-027-gate-i2.md` (i2), `adversary-gates/task-027-gate-i3.md` (i3), `adversary-gates/task-027-gate-i4.md` (i4)*
*Date: 2026-03-01*
