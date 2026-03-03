# Quality Score Report: PROJ-014 Medium Article (Iteration 3)

## L0 Executive Summary

**Score:** 0.937/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.88)
**One-line assessment:** All three i3 fixes are confirmed applied and genuine — evidence hypothesis qualification, paper titles with URLs, and 95% CI surfaced in Results — lifting the composite from 0.913 to 0.937, but Methodological Rigor (0.93, unchanged) is the binding constraint holding the composite 0.013 below the 0.95 publication threshold; a targeted one-sentence addition about McNemar test selection rationale is the highest-leverage remaining fix.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/proj-014-completion-20260301-001/articles/medium-negative-prompting.md`
- **Deliverable Type:** Other (Medium publication article, external audience)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-01T00:00:00Z
- **Custom threshold:** 0.95 (per task specification; publication artifact, C4)
- **Prior Score (i2):** 0.913 REVISE
- **Prior Score (i1):** 0.876 REVISE
- **Iteration:** 3
- **Strategy Findings Incorporated:** No (standalone scoring)

---

## I3 Fix Verification

All three fixes specified in the task brief are verified against the article text.

| Fix | Target | i3 Status | Evidence |
|-----|--------|-----------|----------|
| 1. Hypothesis qualification | "LLMs process instructions as weighted priorities" qualified as hypothesis, not measured result | **CONFIRMED FIXED** | Line 84: "One plausible explanation for the effect we observed: LLMs process instructions as weighted priorities...We have not isolated this mechanism experimentally, but the pattern is consistent across our data." Both qualifications present. |
| 2. Full paper titles + URLs | Geng et al. AAAI 2026 arXiv title + URL; Ferraz et al. EMNLP 2024 arXiv title + URL; Barreto & Jana ACL URL | **CONFIRMED FIXED** | Line 38 inline: full titles + hyperlinked arXiv IDs for Geng et al. and Ferraz et al. Footnote (line 137): all three sources with URLs including ACL Anthology for Barreto & Jana. |
| 3. 95% CI surfaced in Results | CI alongside primary finding in Results section, not only in Caveats | **CONFIRMED FIXED** | Line 58: "7 failures out of 90 matched pairs (95% CI: 2.3% to 13.3%)" — CI now in primary findings paragraph. Also retained in Caveats at line 119. |

**Author name consistency check (Liu→Geng, Wen→Ferraz):**
- "Geng et al." appears at line 38 (body) and line 137 (footnote) — consistent
- "Ferraz et al." appears at line 38 (body) and line 137 (footnote) — consistent
- No instances of "Liu et al." or "Wen et al." remain in the article — confirmed by search

**Venue consistency check:**
- Body (line 38): Ferraz et al. cited as "EMNLP 2024" without "Findings" qualifier
- Footnote (line 137): Ferraz et al. cited as "EMNLP 2024 Findings"
- Minor inconsistency: "Findings" designation present in footnote but absent from inline body citation. Does not affect verifiability (arXiv URL is present in both locations) but a technical reviewer would note the discrepancy.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.937 |
| **Threshold** | 0.95 (publication artifact, C4) |
| **Verdict** | REVISE |
| **Delta from i2** | +0.024 (0.913 → 0.937) |
| **Delta from i1** | +0.061 (0.876 → 0.937) |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | i2 Score | i3 Score | i3 Weighted | Delta | Evidence Summary |
|-----------|--------|----------|----------|-------------|-------|-----------------|
| Completeness | 0.20 | 0.93 | 0.95 | 0.190 | +0.02 | 95% CI now surfaced in Results paragraph (line 58), not only in Caveats — i2 gap closed |
| Internal Consistency | 0.20 | 0.95 | 0.95 | 0.190 | 0.00 | No new changes; all i1 factual corrections hold; minor "6 out of 9" phrasing gap unchanged |
| Methodological Rigor | 0.20 | 0.93 | 0.93 | 0.186 | 0.00 | No i3 fixes in this dimension; McNemar rationale still unexplained; power analysis still absent |
| Evidence Quality | 0.15 | 0.88 | 0.93 | 0.140 | +0.05 | Inference qualified with "one plausible explanation" and "not isolated experimentally" — i2 gap closed |
| Actionability | 0.15 | 0.95 | 0.95 | 0.143 | 0.00 | Unchanged; five concrete, data-grounded, code-backed actions |
| Traceability | 0.10 | 0.76 | 0.88 | 0.088 | +0.12 | Full paper titles + arXiv URLs inline; ACL URL for Barreto & Jana in footnote; GitHub URL replaces "project repository" |
| **TOTAL** | **1.00** | **0.913** | | **0.937** | **+0.024** | |

**Composite arithmetic verification (H-15):** 0.190 + 0.190 + 0.186 + 0.140 + 0.143 + 0.088 = **0.937**

---

## Detailed Dimension Analysis

### Completeness (0.95/1.00)

**Evidence:**

Fix 3 (95% CI in Results) is fully applied. Line 58 now reads: "7 failures out of 90 matched pairs (95% CI: 2.3% to 13.3%)." The CI appears in the primary findings paragraph alongside the point estimate, and is also retained in the Caveats section at line 119. This is the correct implementation — the reader encounters the uncertainty range at the moment of the primary claim, not only if they read through to caveats.

All other completeness elements from i2 remain intact:
- Problem framing (compliance degradation, production context): present
- Research overview (six weeks, six phases, 75 sources): present
- Experimental design (90 matched pairs, 270 invocations, three models, 10 constraints, three conditions, blind scoring): present and accurate
- Primary results (100% C3 compliance, 7.8% C1 violation rate with CI, p = 0.016 with marginal Bonferroni qualifier): all present
- NPT-013 three-component explanation: present
- Five actionable steps with before/after code example: present
- Caveats (effect size, single-session, test scope, mechanistic gap): all present
- Conclusion ("Structure Beats Polarity" new analytical beat): present

**Gaps:**

The CI lower bound (2.3%) is disclosed but the article does not explicitly flag that 2.3 percentage points is likely below any meaningful practical significance threshold. The sentence "the true effect may be larger than what we observed" in Caveats is accurate but one-directional — it does not mention the possibility of the effect being smaller. This is a minor framing gap acceptable at the article genre.

**Improvement Path:**

To reach 0.96+: The Caveats section could note symmetrically that "the CI also extends down to 2.3 percentage points, suggesting the true effect may be smaller than observed." This is optional refinement, not a blocking gap.

---

### Internal Consistency (0.95/1.00)

**Evidence:**

No new changes in this dimension from i2. All three i1 publication-blocking corrections hold:

1. Pair count: "90 matched pairs" consistent across lines 44, 56, 58; 270 = 90 × 3 confirmed
2. Test name: Zero instances of "Fisher's exact test"; "McNemar's exact test on matched pairs" at line 60 and footnote
3. Bonferroni qualifier: "marginally (p = 0.016 vs. adjusted alpha = 0.0167)" — qualifier and threshold both present

Model-level improvement figures (Haiku 10pp, Sonnet 6.7pp, Opus 6.7pp) remain mathematically consistent with source compliance matrix (3/30, 2/30, 2/30 respectively).

C2 violation rate (2.2% = 2/90) internally consistent with the statement "Zero violations out of 90 matched pairs" for C3.

Author name consistency: Geng et al. and Ferraz et al. consistent across body and footnote. No Liu/Wen instances remaining.

Venue consistency minor gap: Ferraz et al. is "EMNLP 2024" in body (line 38) and "EMNLP 2024 Findings" in footnote (line 137). The "Findings" designation is a publication track identifier — both references point to the same paper via arXiv URL, so there is no confusion about source identity. However, the inconsistency is a mild internal consistency imperfection.

**Gaps:**

The "6 out of 9 across all conditions" arithmetic path still implicit (i2 gap, not fixed): "7 C1 violations + 2 C2 violations = 9 total" is left for the reader to infer. Technically correct but not explicit. Minor, acceptable.

**Improvement Path:**

To reach 0.97+: Make the total violation count explicit ("Of the 9 total violations — 7 in C1, 2 in C2 — 6 landed on behavioral-timing constraints") and harmonize the Ferraz venue designation to "EMNLP 2024 Findings" in both body and footnote.

---

### Methodological Rigor (0.93/1.00)

**Evidence:**

No i3 fixes were applied to this dimension. The score is unchanged from i2 at 0.93.

The methodology description remains accurate and complete at the genre level:
- Three framing conditions with concrete examples (lines 48-51)
- Adversarial pressure scenario design described (line 44)
- Blind scoring: separate model instance, no framing knowledge (line 52)
- Inter-rater reliability: 10% double-scoring, 92.6% agreement, Gwet's AC1 = 0.920 (footnote)
- Effect size below pre-specified threshold explicitly acknowledged (line 119)
- Contingency pathway in plain language (line 119)
- CI disclosed in Results (line 58) — improvement from i2, but primarily credited to Completeness

**Gaps:**

Two i2 gaps remain unchanged:

Gap 1 (Medium): The article does not explain why matched pairs require McNemar rather than independent-group tests. A reader could ask why Fisher's exact test would not be appropriate, or why chi-square would be wrong. The answer (within-pair correlation from the matched design) is non-trivial and protects the test choice from a methodological reviewer's challenge. Its absence is the binding gap preventing a score above 0.93 in this dimension.

Gap 2 (Low): The power analysis (80% power to detect pi_d >= 0.10) is not mentioned anywhere in the article. The Caveats section acknowledges the effect fell below the pre-specified threshold but does not explain the sample size rationale. Acceptable at the genre but notable for a rigorous reviewer.

**Improvement Path:**

To reach 0.95: Add one sentence: "McNemar's test is specifically designed for matched-pair designs, where each pair controls for constraint-specific difficulty — using an independent-group test would misattribute within-pair variation to the framing condition." This is the single highest-leverage methodological rigor fix remaining and was the explicit recommendation in the i2 gate.

---

### Evidence Quality (0.93/1.00)

**Evidence:**

Fix 1 is fully and correctly applied. Line 84: "One plausible explanation for the effect we observed: LLMs process instructions as weighted priorities, and a prohibition with documented downstream impact...signals that this constraint is load-bearing, not decorative. We have not isolated this mechanism experimentally, but the pattern is consistent across our data."

This is a correct implementation — two explicit qualifications:
1. "One plausible explanation" — signals hypothesis status, not measured result
2. "We have not isolated this mechanism experimentally" — explicit experimental limitation

The i2 Evidence Quality gap 1 is fully closed. A rigorous reviewer will not be able to fault this framing.

The i2 Evidence Quality gap 2 (literature scope elision: the article says Geng et al. "showed that standalone prohibitions fail within instruction hierarchies" and Ferraz et al. "found that structured constraint decomposition improves compliance by 7-8%") — this is technically a reasonable characterization of A-20 and A-15. The arXiv IDs and full paper titles are now present, so a reviewer can locate the originals and assess the characterization themselves. This is an acceptable level of scope elision for a general-audience article.

The "settled science" characterization at line 38 ("That much is settled science") applies to the claim that blunt prohibition is the worst constraint form — which is supported by T1+T3 evidence (A-20 AAAI 2026, A-15 EMNLP 2024, A-31 arXiv). The characterization is defensible from the source evidence base, though "established science" would be more precise for a T1+T3 evidence base (pure T1 would warrant "settled"). Borderline acceptable.

**Gaps:**

Gap 1 (Low severity): The Ferraz et al. figure of "7-8% over bare prohibitions" maps to A-15's "+7.3-8% compliance with structured framing vs. blunt negation" in the synthesis. This is accurate. However, the synthesis records A-15 as "Wen et al." — the renamed Ferraz et al. arXiv:2410.06458 paper is cited as "LLM Self-Correction with DeCRIM." DeCRIM (Decomposed Constraint Recovery for Instruction Management) is a specific method. The article characterizes this as "structured constraint decomposition improves compliance by 7-8%" — accurate framing of the DeCRIM result. Acceptable.

Gap 2 (Low severity): The "+25.14% negation reasoning accuracy" from Barreto & Jana (A-23, EMNLP 2025) does not appear anywhere in the article body. Only the ACL URL appears in the footnote. This is acceptable — the article focuses on behavioral compliance (the PROJ-014 experimental outcome), not negation comprehension accuracy, and correctly does not assert this figure as compliance evidence. No gap.

**Improvement Path:**

To reach 0.95: Consider replacing "settled science" with "established by peer-reviewed research" — more precise given the T1+T3 (not exclusively T1) evidence base, and more durable against a reviewer challenging the characterization.

---

### Actionability (0.95/1.00)

**Evidence:**

Unchanged from i2. The actionability section remains the strongest dimension:

1. Audit for blunt prohibitions: search terms specified ("don't," "never," "must not"), characterization accurate ("lowest-hanging fruit" — consistent with NPT-014 being unconditionally the worst formulation)
2. Convert to NPT-013: complete before/after code example with all three components (prohibition, consequence, alternative) correctly represented
3. Prioritize behavioral-timing constraints: grounded in data (56% violation rate for the most vulnerable constraint type); timing rules named specifically
4. Extra attention to smaller models: grounded in per-model data (Haiku 10pp vs. Sonnet/Opus 6.7pp), practical routing implication stated
5. Consequence specificity: good/bad example present, explanation of why specificity matters

Action ordering is correct and matches PROJ-014's own priority structure.

**Gaps:**

No material gaps. The score is held at 0.95 rather than higher because no guidance is given on constraint batching order within a system prompt audit — this is a scope limitation appropriate to an 8-minute article, not a deficiency.

---

### Traceability (0.88/1.00)

**Evidence:**

All four i2 traceability fixes are applied:

**Fix 2a — Paper titles:** Geng et al.'s paper is cited with full title inline at line 38: "Control Illusion: The Failure of Instruction Hierarchies in Large Language Models." Ferraz et al.'s paper is cited with full title inline at line 38: "LLM Self-Correction with DeCRIM." Both are verifiable by a motivated reader using the title alone.

**Fix 2b — arXiv URLs:** Geng et al. hyperlinks to `https://arxiv.org/abs/2502.15851`. Ferraz et al. hyperlinks to `https://arxiv.org/abs/2410.06458`. Both are present inline at line 38, not only in the footnote. The primary academic evidence is now independently verifiable at the point of citation.

**Fix 2c — Barreto & Jana URL:** ACL Anthology URL (`https://aclanthology.org/2025.findings-emnlp.761`) is present in the footnote at line 137. Barreto & Jana is not cited inline in the body — the article does not reference the +25.14% negation accuracy figure, which is appropriate given the distinction between negation comprehension and behavioral compliance (KF-007 from final-synthesis). The footnote citation with URL is adequate.

**Fix 3 — GitHub URL:** The footnote at line 137 replaces "the project repository" with `https://github.com/geekatron/jerry/tree/main/projects/PROJ-014-negative-prompting-research` — a specific, externally reachable URL. An external Medium reader can now access the full experimental artifacts.

**Remaining gaps:**

Gap 1 (Low severity): Barreto & Jana paper title is absent from both body and footnote. The footnote provides author names, venue, and ACL URL but not the paper title. A reader using the URL can locate the title, but the citation is less complete than the Geng and Ferraz citations, which include full titles at point of use.

Gap 2 (Very low): Ferraz et al. venue inconsistency: "EMNLP 2024" in body (line 38), "EMNLP 2024 Findings" in footnote (line 137). Both resolve to the same arXiv URL, so no ambiguity in locating the paper. Cosmetic.

Gap 3 (Very low): The article does not cite the PROJ-014 go-no-go determination document or the TASK-025 A/B testing report. These are internal artifacts, and their absence is expected for a public-facing Medium article — the GitHub URL now allows motivated readers to find them.

**Why 0.88 and not 0.90+:**

The 0.9+ rubric criterion is "Full traceability chain." The primary evidence claims now have full inline traceability (titles + URLs for Geng and Ferraz). The Barreto & Jana paper title gap and the footnote-only placement of the ACL URL prevent a "full traceability chain" designation. The score is 0.88: most items are now traceable, with two residual minor gaps.

**Improvement Path:**

To reach 0.92: Add Barreto & Jana paper title to the footnote citation. Harmonize Ferraz venue to "EMNLP 2024 Findings" in body (or remove "Findings" from footnote). These are mechanical character additions.

---

## I2 Gap Closure Summary

| i2 Gap | Priority | i3 Fix Applied | Closure Status | Score Impact |
|--------|----------|---------------|----------------|-------------|
| Evidence Quality: "LLMs process instructions as weighted priorities" unqualified | P1 | "One plausible explanation...We have not isolated this mechanism experimentally" | CLOSED | +0.05 on EQ score |
| Traceability: No URLs for Geng/Ferraz primary citations | P2 | arXiv URLs inline + footnote | CLOSED | +0.12 on Traceability score |
| Traceability: No paper titles for Geng/Ferraz | P2 | Full titles inline in body | CLOSED | Included in +0.12 |
| Traceability: Barreto & Jana URL absent | P2 | ACL Anthology URL in footnote | CLOSED | Included in +0.12 |
| Traceability: "project repository" not a URL | P3 | GitHub URL in footnote | CLOSED | Included in +0.12 |
| Completeness: 95% CI only in Caveats | P4 | CI in primary Results paragraph (line 58) | CLOSED | +0.02 on Completeness score |
| Methodological Rigor: McNemar rationale unexplained | Not in i3 scope | Not applied | OPEN | 0.00 (binding gap) |
| Internal Consistency: "6 out of 9" arithmetic path implicit | Not in i3 scope | Not applied | OPEN | 0.00 (minor) |

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Methodological Rigor | 0.93 | 0.95 | Add one sentence explaining McNemar test selection: "McNemar's test is designed for matched-pair designs, where each pair controls for constraint-specific difficulty — an independent-group test would misattribute within-pair variation to the framing condition." This single sentence is the highest-leverage remaining fix and directly addresses the gap a statistical reviewer would flag. |
| 2 | Traceability | 0.88 | 0.92 | Add Barreto & Jana paper title to the footnote citation. Current: "Barreto & Jana, EMNLP 2025 Findings ([ACL Anthology](...))" — target: "Barreto & Jana, '[paper title],' EMNLP 2025 Findings ([ACL Anthology](...))" |
| 3 | Internal Consistency | 0.95 | 0.97 | Make the "6 out of 9 across all conditions" arithmetic explicit: "Of the 9 total violations — 7 in C1, 2 in C2 — 6 landed on behavioral-timing constraints." Harmonize Ferraz venue designation: "EMNLP 2024 Findings" in both body and footnote. |
| 4 | Evidence Quality | 0.93 | 0.95 | Replace "That much is settled science" with "That much is established by peer-reviewed research" — more precise given the T1+T3 (not exclusively T1) evidence base. |

---

## Composite Score Pathway to 0.95

| Fix Applied | Dimension | Current | Projected | Weighted Impact |
|-------------|-----------|---------|-----------|----------------|
| P1: McNemar rationale | Methodological Rigor | 0.93 | 0.95 | +0.004 (0.186 → 0.190) |
| P2: Barreto & Jana title | Traceability | 0.88 | 0.90 | +0.002 (0.088 → 0.090) |
| P3: Venue + 6-of-9 | Internal Consistency | 0.95 | 0.96 | +0.002 (0.190 → 0.192) |
| P4: "settled science" | Evidence Quality | 0.93 | 0.94 | +0.002 (0.140 → 0.141) |
| **Projected composite** | | **0.937** | **~0.950** | **+0.010** |

**Required for PASS:** P1 (McNemar rationale) is the minimum required fix — it contributes 0.004 to the weighted composite, and combined with P2 (+0.002) and P3 (+0.002) reaches ~0.950. P1 alone reaches ~0.941, still below 0.95.

**P1 + P2 combination:** 0.937 + 0.004 + 0.002 = 0.943. Still below 0.95.

**P1 + P2 + P3:** 0.937 + 0.004 + 0.002 + 0.002 = 0.945. Still marginally below.

**Note on threshold proximity:** The 0.95 custom threshold is demanding. P1 through P4 applied together project ~0.950 (marginally above). The scoring methodology is conservative per S-014 leniency bias counteraction rules — uncertain score increments are resolved downward. The projected ~0.950 should be treated as the achievable target with these four targeted fixes, not a guaranteed outcome.

---

## Iteration Score Progression

| Iteration | Score | Delta | Verdict | Key Changes |
|-----------|-------|-------|---------|-------------|
| i1 | 0.876 | baseline | REVISE | Three mechanical errors: wrong pair count, wrong test name, overstated Bonferroni |
| i2 | 0.913 | +0.037 | REVISE | Three errors fixed; voice compliance applied; traceability and evidence gaps identified |
| i3 | 0.937 | +0.024 | REVISE | Evidence qualified, full citations added, CI surfaced; Methodological Rigor unchanged |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented with specific line numbers and source verification
- [x] Uncertain scores resolved downward (Traceability held at 0.88 rather than 0.90 because Barreto & Jana title is absent and venue inconsistency present; Methodological Rigor held at 0.93 — no i3 changes applied to it)
- [x] No first-draft calibration applied (iteration 3 of a voice-revised article)
- [x] No dimension scored above 0.95 without exceptional evidence (Completeness raised to 0.95 — justified: full section coverage plus CI now in Results; Actionability at 0.95 — justified: five complete, data-backed, code-illustrated actions)
- [x] Composite verified by arithmetic: 0.190 + 0.190 + 0.186 + 0.140 + 0.143 + 0.088 = 0.937
- [x] Verdict cross-checked: 0.937 falls below the 0.95 custom threshold and above the standard 0.92 H-13 threshold; REVISE verdict correct per custom threshold
- [x] i3 fixes verified individually with direct text evidence before scoring
- [x] Author name corrections (Liu→Geng, Wen→Ferraz) confirmed consistent throughout article
- [x] Score increase calibration: +0.024 delta is consistent with three targeted fixes to two dimensions (Evidence Quality, Traceability, Completeness) with two unchanged dimensions (Methodological Rigor, Internal Consistency)

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.937
threshold: 0.95
weakest_dimension: Traceability
weakest_score: 0.88
binding_constraint_dimension: Methodological Rigor
binding_constraint_score: 0.93
critical_findings_count: 0
publication_blocking_count: 0
iteration: 3
delta_from_i2: +0.024
delta_from_i1: +0.061
i3_fixes_confirmed:
  - hypothesis_qualification: CLOSED (line 84, two explicit qualifications)
  - paper_titles_and_urls: CLOSED (inline body + footnote, all three sources)
  - ci_in_results: CLOSED (line 58, Results paragraph)
author_correction_consistency:
  - Geng_et_al: CONSISTENT (body line 38 + footnote line 137)
  - Ferraz_et_al: CONSISTENT (body line 38 + footnote line 137)
  - Liu_Wen_instances: ZERO REMAINING
open_gaps:
  - P1: McNemar rationale missing (one sentence, highest leverage)
  - P2: Barreto & Jana paper title absent from footnote
  - P3: 6-of-9 arithmetic implicit; Ferraz venue inconsistency
  - P4: "settled science" characterization slightly imprecise
improvement_recommendations:
  - "Add McNemar test selection rationale (Methodological Rigor, Priority 1) — required for PASS"
  - "Add Barreto & Jana paper title to footnote (Traceability, Priority 2)"
  - "Make 6-of-9 arithmetic explicit; harmonize Ferraz venue to EMNLP 2024 Findings in body (Internal Consistency, Priority 3)"
  - "Replace 'settled science' with 'established by peer-reviewed research' (Evidence Quality, Priority 4)"
path_to_pass:
  - "P1 + P2 + P3 + P4 combined: projected ~0.950"
  - "P1 alone: ~0.941 (insufficient)"
  - "P1 + P2: ~0.943 (insufficient)"
  - "P1 + P2 + P3: ~0.945 (marginally insufficient)"
  - "All four: ~0.950 (marginally above threshold)"
```

---

*Scored by: adv-scorer (S-014 LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Source research verified: `orchestration/neg-prompting-20260227-001/phase-6/final-synthesis.md`, `adversary-gates/task-027-gate.md` (i1), `adversary-gates/task-027-gate-i2.md` (i2)*
*Date: 2026-03-01*
