# Quality Score Report: Statistical Methodology Research — McNemar's Test for LLM A/B Testing (Iteration 2)

## L0 Executive Summary

**Score:** 0.9535/1.00 | **Verdict:** PASS | **Weakest Dimension:** Traceability (0.92)
**One-line assessment:** Iteration 2 addresses all 8 findings from the prior gate with specific, verifiable additions; the artifact now meets the C4 threshold of 0.95, with minor residual gaps in C1-C7 section specificity and OR confidence interval guidance.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/phase-0-design/methodology-research.md`
- **Deliverable Type:** Research (statistical methodology validation)
- **Criticality Level:** C4 (Critical) — informs a 270-invocation A/B experiment design
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Quality Threshold:** 0.95 (C4, user-specified)
- **Iteration:** 2 (post-revision from gate score 0.8985)
- **Prior Score Incorporated:** Yes — Iteration 1 gate report used to verify issue resolution
- **Scored:** 2026-03-01T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.9535 |
| **Threshold** | 0.95 (C4, user-specified) |
| **Verdict** | PASS |
| **Strategy Findings Incorporated** | Yes — Iteration 1 gate report (methodology-research-gate.md) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.96 | 0.192 | All 6 RQs answered in full depth; kappa CI, Cohen's g, power derivation, LLM search all added; minor gap: no OR CI method specified |
| Internal Consistency | 0.20 | 0.97 | 0.194 | Zero contradictions; Schoenfeld now in refs; "per rubric criteria" correction made; all numeric cross-checks pass |
| Methodological Rigor | 0.20 | 0.96 | 0.192 | Full step-by-step power derivation shown; asymptotic borderline noted; Connor limitation documented; alternatives (BH, mid-p, stratified McNemar) explicitly compared |
| Evidence Quality | 0.15 | 0.94 | 0.141 | Wikipedia refs replaced with Agresti (2002) and Dunn (1961); Schoenfeld [20] fully cited; Connor secondhand transparently documented; LLM search null result documented; minor gap: one rcompanion.org tertiary source persists |
| Actionability | 0.15 | 0.96 | 0.144 | Consolidated effect size table added; Breslow-Day Python/R implementations specified with decision threshold; all design elements have STATUS/RISK/ACTION |
| Traceability | 0.10 | 0.92 | 0.092 | ORCHESTRATION_PLAN.md reference added; C1-C7 linked to parent design document (no section number specified); source count and confidence updated |
| **TOTAL** | **1.00** | | **0.9535** | |

---

## Detailed Dimension Analysis

### Completeness (0.96/1.00)

**Evidence:**

All 6 research questions are answered with verdicts and specific recommendations. The following additions from Iteration 2 directly address the Iteration 1 completeness gaps:

1. **Kappa CI estimate at n=27** — Added in RQ5: SE ~ 0.10-0.14, 95% CI width approximately 0.28-0.40. Comparison to n=50 (CI width reduction of ~36%) provided. Bootstrap CI recommendation for small samples included. Reference [22] (Fleiss, Cohen & Everitt 1969) added as source for the SE formula.

2. **Expected Cohen's g under design assumptions** — Added in RQ3 with explicit derivation: P = 0.20/0.30 = 0.667, g = 0.667 - 0.50 = 0.167, classified as medium per Cohen's conventions. The 2:1 discordant pair ratio interpretation is provided.

3. **LLM-specific McNemar search** — Added as a dedicated Methodology subsection with 3 search term strings, 2 relevant papers found (Kuebler et al. 2025 [18], Vishwanath et al. 2025 [19]), and an explicit null result statement for prompt-framing-specific papers.

4. **Per-model power derivation** — Full step-by-step derivation added (Steps 1-3 with Phi() evaluated to 0.41). Also added: expected per-model discordant count (27) and asymptotic borderline note (>25 but marginal).

5. **Breslow-Day implementation** — Python (statsmodels.stats.contingency_tables.StratifiedTable) and R (DescTools::BreslowDayTest()) specified with exact API calls and decision threshold (p < 0.10).

6. **C1-C7 condition reference** — Added in RQ5 and RQ6 pointing to the "parent experimental design document."

**Gaps:**

1. **OR confidence interval method not specified.** The document recommends reporting OR with 95% CI (RQ3 recommendation item 1: "Use profile likelihood CI for the OR of discordant pairs") — this recommendation is present but it reads as a parenthetical rather than a dedicated guidance block. A practitioner implementing the analysis plan would benefit from a clearer statement: "Use `mcnemar.test()` plus `oddsratio()` in R or `statsmodels.stats.contingency_tables.mcnemar()` in Python for the OR CI." This is minor and does not prevent execution.

2. **C1-C7 reference lacks section number.** RQ5 and RQ6 reference "the parent experimental design document" and "the experimental conditions matrix in the design document" but do not specify a section name or heading. A scorer reading only this document cannot navigate to the definition without prior knowledge.

**Improvement Path:**

Add a one-sentence OR CI implementation note specifying the Python or R function. Add the section name or heading for C1-C7 in the parent design document.

---

### Internal Consistency (0.97/1.00)

**Evidence:**

No contradictions found after thorough cross-checking:

- **Schoenfeld [20] now fully integrated.** The formula comparison table lists Schoenfeld (n=236) with reference "[20]". Reference [20] appears in the References section with full citation: Schoenfeld DA (1980), Int J Radiation Oncology Biol Phys, 6(3), 371-374, DOI and PubMed ID included. The internal consistency gap from Iteration 1 is resolved.

- **"LLM-as-judge per rubric criteria" correction made.** RQ5 previously read "LLM-as-judge with calibration" (overstating the design). The revision history confirms: "Revised 'LLM-as-judge with calibration' to 'LLM-as-judge per rubric criteria' in RQ5 for accuracy." This is now internally consistent with the experimental design.

- **Numeric cross-checks pass.** OR = p12/p21 = 0.20/0.10 = 2.0 (correct). Per-model n = 270/3 = 90 (correct). Alpha Bonferroni = 0.05/21 = 0.00238 (correct). Per-model discordant count = 0.30 * 90 = 27 (correct). Power = Phi(-0.228) = 0.41 (verified via standard normal CDF). Cohen's g = 0.667 - 0.50 = 0.167 (correct).

- **L0 summary is consistent with L1 detail.** L0 states the 41% per-model power finding with the formula reference: "delta/sqrt(p_d/n) = 0.10/sqrt(0.30/90) = 1.732; power = Phi(1.732 - 1.96) = Phi(-0.228) = 0.41." L2 Critical Warning provides the full step-by-step derivation. No inconsistency.

- **Connor note consistent throughout.** Reference [6] expanded key insight matches the table note: n=236 confirmed across Stata docs [17] and NCSS PASS docs [16]; original paper not directly accessed; limitation explicitly documented.

**Gaps:**

1. **Minor: the formula comparison table labels MedCalc's source as "[7]"** pointing to the Machin et al. (2009) citation. MedCalc is an independent commercial tool; Machin (2009) is the reference used within MedCalc. The cross-reference is technically accurate but could mislead a reader who thinks "[7]" means MedCalc directly implements Machin's formula variant. A parenthetical "(MedCalc implements Miettinen's formula; [7] is Machin et al. cited within MedCalc documentation)" would improve clarity.

**Improvement Path:**

Add clarifying parenthetical to the MedCalc row in the formula comparison table. This is cosmetic — no substantive inconsistency.

---

### Methodological Rigor (0.96/1.00)

**Evidence:**

Iteration 2 closes the primary methodological rigor gap from Iteration 1 (unsupported 41% power claim):

1. **Full step-by-step power derivation shown.** The "Per-Model Power Derivation" subsection provides a 3-step derivation:
   - Step 1: Define delta=0.10, p_d=0.30, n_per_model=90
   - Step 2: z_effect = 0.10 / sqrt(0.30/90) = 0.10 / 0.05774 = 1.732
   - Step 3: power = Phi(1.732 - 1.96) = Phi(-0.228) = 0.4099 ~ 0.41
   - Formula attributed to Miettinen (1968) rearranged for power.

2. **Asymptotic borderline documented.** Expected per-model discordant count = 0.30 * 90 = 27 pairs. The document explicitly notes this is "marginally above the asymptotic validity threshold of 25 discordant pairs" and recommends the exact binomial McNemar test as a sensitivity check. This addresses the Iteration 1 gap about expected discordant count.

3. **Alternative methods compared explicitly.** Benjamini-Hochberg FDR vs. Bonferroni vs. Holm step-down (RQ6 table). Asymptotic vs. exact vs. mid-p (RQ1). CMH vs. stratified McNemar (RQ4). Fagerland et al. (2013) [4] — a peer-reviewed BMC Methods paper — cited for mid-p superiority.

4. **Limitations transparently stated.** PS Integration section documents: Connor (1987) not directly accessed; n=270 not reproducible from standard formulas; no LLM-specific papers for prompt framing comparison found.

5. **Seven formula variants computed and tabulated** with a Notes column added in Iteration 2 explaining Schoenfeld's "simplified approximation" and Connor's "multinomial-based expression."

**Gaps:**

1. **Connor (1987) figure still secondhand.** n=236 is confirmed across secondary sources (Stata docs [17], NCSS PASS [16]) but the original Biometrics paper was not accessed. The document discloses this transparently. The gap is not a methodological error — the figure is consistently reported across independent secondary sources — but it remains a limitation for a C4 artifact.

2. **Power formula approximation not stated.** The per-model power derivation uses the Miettinen formula rearranged for power. This is a standard approximation but the document does not explicitly state it is an approximation (normal approximation to the binomial). The exact binomial power could differ slightly. This is a minor point for methodological completeness.

**Improvement Path:**

Add a note that the power derivation uses the normal approximation to the McNemar test statistic (consistent with Miettinen's original formula). For Connor, the secondhand limitation is now well-documented and acceptable at the current iteration.

---

### Evidence Quality (0.94/1.00)

**Evidence:**

Iteration 2 resolves the four primary evidence quality gaps from Iteration 1:

1. **Wikipedia sources replaced.** Reference [10] (CMH Wikipedia) is now Agresti (2002) *Categorical Data Analysis*, 2nd ed., pp. 320-332 — an authoritative textbook. Reference [13] (Bonferroni Wikipedia) is now Dunn (1961) JASA 56(293), 52-64 — the original journal paper formalizing the Bonferroni correction. Both replacements include DOI and key insights.

2. **Schoenfeld [20] fully cited.** Reference [20] is now Schoenfeld DA (1980), *International Journal of Radiation Oncology, Biology, Physics*, 6(3), 371-374 with DOI: 10.1016/0360-3016(80)90153-4 and PubMed: 7390914. Key insight specifies "Simplified sample size approximation for paired proportions; yields n=236 for our parameters, consistent with Connor (1987)."

3. **LLM-specific McNemar search documented.** Three search term strings are listed. Two relevant papers found: Kuebler et al. (2025) [18] for per-sample LLM degradation detection using exact one-sided McNemar, and Vishwanath et al. (2025) [19] for pairwise exact McNemar comparing LLMs on medical benchmarks. Null result explicitly documented: "No papers found specifically using McNemar's test to compare prompt framing strategies (positive vs. negative) on the same model."

4. **Kappa SE formula sourced.** Fleiss, Cohen & Everitt (1969) [22] — a peer-reviewed *Psychological Bulletin* paper — added as the source for the asymptotic SE formula used in the kappa CI estimate. Bootstrap CI recommendation is grounded: "At n=27, the kappa sampling distribution may be non-symmetric [22]."

**Remaining gaps:**

1. **Reference [8] (rcompanion.org) is a tertiary web source.** This source provides the odds ratio interpretation scale for McNemar (small OR 1.22-1.86, medium 1.86-3.00, large >= 3.00) and the Cohen's g formula. The OR interpretation scale should ideally be cited to Bland & Altman or another peer-reviewed source. rcompanion.org is a reputable statistics tutorial site, but it is a tertiary source in a C4 artifact. The Cohen's g convention scale could also be cited to Cohen (1988) *Statistical Power Analysis for the Behavioral Sciences*.

2. **Reference [2] (LibreTexts) is a secondary web source** used for the b+c >= 25 asymptotic validity threshold. This specific threshold is attributed to LibreTexts (citing Dohm), not to the original McNemar (1947) paper or a peer-reviewed review. For a C4 artifact, this criterion should be cited to a peer-reviewed source (e.g., Fagerland et al. 2013 [4] discusses exact vs. asymptotic boundaries).

3. **Connor (1987) remains secondhand** — confirmed across Stata and NCSS PASS documentation, with the limitation transparently disclosed. The n=236 figure is now explicitly supported in the table with a "Connor (1987) note" paragraph. This is an acceptable residual gap given the disclosure.

**Improvement Path:**

Replace or supplement reference [8] with Cohen (1988) for the g interpretation scale. Check whether Fagerland et al. (2013) [4] provides the b+c >= 25 boundary explicitly; if so, replace the LibreTexts reference. These are refinements that would push Evidence Quality toward 0.97.

---

### Actionability (0.96/1.00)

**Evidence:**

Iteration 2 adds two key actionability improvements that directly address Iteration 1 findings:

1. **Consolidated effect size table** — RQ3 now presents a single table with OR, risk difference (pi_d), Cohen's g, and discordant proportion (p_d), each with formula, design value, interpretation scale, convention classification, and "Recommended?" flag. A Phase 0 design agent implementing the analysis plan can extract all four measures from one table without hunting across paragraphs.

2. **Breslow-Day implementation specified.** RQ3 "Breslow-Day Implementation Note" provides:
   - Python: `statsmodels.stats.contingency_tables.StratifiedTable`; `st = StratifiedTable(tables); st.summary()` — with explicit note that the "Test constant OR" entry in the output is the Breslow-Day result.
   - R: `DescTools::BreslowDayTest()`; `BreslowDayTest(table_array)`.
   - Decision threshold: p < 0.10 (with rationale: "conventional threshold for homogeneity tests, which use a liberal alpha to protect against falsely assuming homogeneity").

3. **Per-model analysis strategy** in L2 now gives a 4-step ordered sequence: (1) per-model McNemar tests, (2) Breslow-Day homogeneity, (3) CMH if homogeneous, (4) interaction analysis if heterogeneous. This is directly implementable.

4. **L2 Design Validation Summary** provides STATUS/RISK/ACTION for all 6 design elements. The risk table adds "Sample size insufficient for subgroup" with the derivation reference.

**Gaps:**

1. **OR CI implementation not specified.** RQ3 recommendation item 1 states "Use profile likelihood CI for the OR of discordant pairs" — naming the CI method but not specifying the software function. A practitioner needs to know: in R, `fisher.test()` or `oddsratio.wald.ci()` from the DescTools package; in Python, there is no direct McNemar OR CI function in statsmodels (would require manual computation). This implementation gap persists from Iteration 1 (though it was not in the original gate findings).

2. **Multiple comparison implementation not specified.** RQ6 recommends "Bonferroni as primary, BH-FDR as sensitivity analysis" and references "discrete Bonferroni-Holm procedure" from Westfall et al. (2010) but does not specify the software function for the discrete Holm procedure. Standard `p.adjust(method="BH")` in R handles BH-FDR; the Westfall discrete method requires the `MultTest` package. This is relevant for implementers.

**Improvement Path:**

Add OR CI implementation: "In R: `oddsratio()` from DescTools, or `fisher.test()` as an approximation; in Python: manual computation from the 2x2 table using SciPy." Add BH-FDR implementation note: "R: `p.adjust(p_values, method='BH')`."

---

### Traceability (0.92/1.00)

**Evidence:**

Iteration 2 adds the following traceability improvements:

1. **ORCHESTRATION_PLAN.md reference added.** PS Integration section now includes: "Orchestration: projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/ORCHESTRATION_PLAN.md." This links the research artifact to the orchestration context.

2. **Revision History table** added (Section: Revision History) with 8 rows corresponding to all 8 gate findings, each documenting: Finding #, Finding description, Resolution. This provides complete traceability from the prior gate score to the current artifact state.

3. **Source count updated** from 17 to 22, and confidence updated from 0.85 to 0.88. These metadata fields are correctly reflected in the PS Integration section.

4. **Design parameters consistently traced.** p12=0.20, p21=0.10, alpha=0.05, power=0.80 are stated in RQ2 and used consistently throughout. The n=270 discrepancy is traced with three hypotheses (dropout inflation at 6%, higher p_d of 0.35, conservative rounding to 270 = 90 x 3) and a cost-benefit analysis (36 additional instances = ~2 hours compute).

**Gaps:**

1. **C1-C7 condition definitions referenced without section specificity.** RQ5 states: "defined in the parent experimental design document (TASK-025 design specification). See the experimental conditions matrix in the design document." RQ6 states: "C1-C7, defined in the experimental design document -- see RQ5 note." Neither reference includes a section name or anchor. A reader following the traceability chain must load the full parent design document to find the conditions matrix. Specifying the heading (e.g., "Section 3: Experimental Conditions Matrix") would complete the traceability chain.

2. **No entry in the Revision History for the Connor explicit note** (Finding #4 in the gate report). The revision history table lists Finding 4 as: "Connor (1987) is secondhand only — Added explicit note in RQ2 documenting: (a) n=236 confirmed across Stata docs [17] and NCSS PASS docs [16], (b) why original paper was not directly accessed, (c) the n=236 figure is consistent across secondary sources." The note is present in the document body; the revision history entry correctly summarizes it. No gap here — this cross-check confirms traceability.

3. **Confidence rating (0.88) is not traced to specific claims.** The PS Integration states "HIGH (0.88)" but does not explain how the confidence was computed or why it increased from 0.85 to 0.88 in Iteration 2. A sentence noting which specific additions raised confidence (e.g., "addition of LLM-specific papers [18][19] and step-by-step power derivation increased confidence from 0.85 to 0.88") would complete the trace.

**Improvement Path:**

Add the section heading for C1-C7 in the parent design document. Add a one-sentence justification for the confidence score increase in the PS Integration section.

---

## Improvement Recommendations (Priority Ordered)

Even at PASS, the following improvements would further strengthen the artifact:

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability | 0.92 | 0.95 | Add section name/heading for C1-C7 conditions in the parent experimental design document reference in RQ5 and RQ6 |
| 2 | Evidence Quality | 0.94 | 0.97 | Replace reference [8] (rcompanion.org tertiary source) with Cohen (1988) for the Cohen's g interpretation scale; check if Fagerland et al. (2013) [4] covers the b+c >= 25 boundary to replace LibreTexts [2] |
| 3 | Actionability | 0.96 | 0.98 | Add OR CI implementation note: "R: oddsratio() from DescTools; Python: manual computation from 2x2 table"; add BH-FDR implementation: "R: p.adjust(p_values, method='BH')" |
| 4 | Internal Consistency | 0.97 | 0.98 | Add clarifying parenthetical to MedCalc row in formula comparison table: MedCalc implements Miettinen's formula, [7] is Machin et al. cited within MedCalc documentation |
| 5 | Methodological Rigor | 0.96 | 0.97 | Add note that the per-model power derivation uses the normal approximation (consistent with Miettinen's formula) and that exact binomial power could differ marginally |
| 6 | Completeness | 0.96 | 0.97 | Add one sentence specifying the OR CI method in the implementation context (not just in the recommendation text) |

---

## Revision History Verification

The Revision History section of the artifact documents 8 findings from the Iteration 1 gate. Each is verified as resolved:

| # | Iteration 1 Finding | Resolution Status |
|---|---------------------|------------------|
| 1 | Schoenfeld (1980) missing from references | RESOLVED — Reference [20] added with full citation, DOI, PubMed ID, key insight |
| 2 | 41% per-model power claim lacks shown derivation | RESOLVED — Full step-by-step derivation shown in "Per-Model Power Derivation" subsection; also added to L0 |
| 3 | Two Wikipedia sources (refs 10, 13) | RESOLVED — Ref [10] replaced with Agresti (2002); Ref [13] replaced with Dunn (1961) JASA |
| 4 | Connor (1987) secondhand only | RESOLVED (acknowledged) — Explicit note in RQ2 documents secondary source basis; consistent across [16][17]; limitation disclosed |
| 5 | Search for LLM-specific McNemar papers | RESOLVED — Dedicated subsection with 3 search terms, 2 papers found [18][19], null result for prompt-framing-specific papers documented |
| 6 | Add expected Cohen's g under design assumptions | RESOLVED — Full derivation: P = 0.20/0.30 = 0.667, g = 0.167, medium per Cohen's conventions |
| 7 | Consolidate effect size formulas into one table | RESOLVED — Consolidated Effect Size Table in RQ3 with OR, pi_d, Cohen's g, p_d with all fields |
| 8 | Add kappa CI estimate at n=27 | RESOLVED — SE ~ 0.10-0.14, 95% CI width ~0.28-0.40; bootstrap CI recommendation; n=50 comparison; source [22] added |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific section/claim citations
- [x] Uncertain scores resolved downward — Evidence Quality held at 0.94 (not 0.96) due to rcompanion.org and LibreTexts tertiary sources; Traceability held at 0.92 (not 0.95) due to missing section specificity for C1-C7
- [x] Calibration anchors applied: 0.92 = Genuinely excellent; 0.95+ = Essentially excellent with only minor refinements needed; scores at 0.96-0.97 reflect dimensions where Iteration 2 additions were comprehensive
- [x] No dimension scored above 0.97 — Internal Consistency at 0.97 is justified: zero substantive contradictions in a numerically dense document, Schoenfeld resolved, calibration language corrected, all numeric cross-checks pass
- [x] PASS verdict verified: weighted composite 0.9535 >= 0.95 threshold

**Anti-leniency applied:**
- Evidence Quality resisted inflation to 0.96+ despite 22 sources: rcompanion.org [8] and LibreTexts [2] remain as genuine tertiary source limitations that are appropriate to penalize at C4 criticality
- Traceability resisted 0.95: C1-C7 reference without section specificity is a genuine traceability gap, not a minor formatting issue — a reader cannot follow the traceability chain without loading the full parent document
- Completeness resisted 1.00: the OR CI implementation gap (profile likelihood vs. Wald vs. exact not implemented in code) is a real actionability gap even if minor
- First-draft calibration note: this is Iteration 2 of a well-structured research artifact; scores in the 0.94-0.97 range reflect genuine quality improvement, not inflation

---

## Session Context Handoff

```yaml
verdict: PASS
composite_score: 0.9535
threshold: 0.95
weakest_dimension: traceability
weakest_score: 0.92
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Add section name/heading for C1-C7 conditions reference in parent design document (RQ5, RQ6)"
  - "Replace rcompanion.org [8] with Cohen (1988) for g interpretation scale; check Fagerland et al. for b+c threshold"
  - "Add OR CI and BH-FDR implementation notes (software functions)"
  - "Add MedCalc formula clarification in formula comparison table"
  - "Add note that per-model power derivation uses normal approximation"
```
