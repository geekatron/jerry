# Quality Score Report: Statistical Methodology Research (McNemar's Test for LLM A/B Testing)

## L0 Executive Summary

**Score:** 0.8985/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.84)
**One-line assessment:** Strong, well-structured research with rigorous multi-formula validation and actionable findings, but falls short of the C4 0.95 threshold due to a missing reference for Schoenfeld (1980), an unsupported 41% per-model power claim, secondhand citation of Connor (1987), and two Wikipedia sources weakening evidence quality.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/phase-0-design/methodology-research.md`
- **Deliverable Type:** Research (statistical methodology validation)
- **Criticality Level:** C4 (Critical) — informs 270-invocation A/B experiment design
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Quality Threshold:** 0.95 (C4 requirement per user specification)
- **Scored:** 2026-03-01T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.8985 |
| **Threshold** | 0.95 (C4, user-specified) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.180 | All 6 RQs answered with depth; minor gaps on kappa CI and consolidated effect size formulas |
| Internal Consistency | 0.20 | 0.95 | 0.190 | No contradictions found; all numbers self-consistent; Schoenfeld (1980) in table but missing from references |
| Methodological Rigor | 0.20 | 0.88 | 0.176 | 7 formula variants computed; peer-reviewed citations; 41% per-model power claim asserted without shown derivation |
| Evidence Quality | 0.15 | 0.84 | 0.126 | 17 sources but Schoenfeld (1980) missing from reference list; Connor (1987) secondhand; two Wikipedia sources; 41% power unverified |
| Actionability | 0.15 | 0.91 | 0.137 | Specific numbers and 4-step plans throughout; all design elements addressed with STATUS/RISK/ACTION; minor formula scattering |
| Traceability | 0.10 | 0.90 | 0.090 | n=270 vs. n=234-253 discrepancy explicitly documented with 3 hypotheses; design parameters traced throughout |
| **TOTAL** | **1.00** | | **0.8985** | |

---

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:**
All 6 research questions are answered with verdicts and specific recommendations. The L0/L1/L2 structure is present. Power analysis is addressed both for the overall design (80% at n=234-270) and the critical per-model scenario (41% at n=90). Multi-model stratification is covered with the CMH/Breslow-Day/stratified McNemar triple recommendation. Effect size covers three measures (OR, Cohen's g, risk difference) with interpretation scales.

**Gaps:**
1. No confidence interval guidance for kappa estimates. The document states "27 instances double-scored" is "sufficient for kappa estimation with reasonable confidence intervals" but provides no CI formula or expected CI width at that sample size. A reviewer designing the double-scoring protocol needs this.
2. No confidence interval guidance for the OR or risk difference effect size estimates. The document recommends reporting these but does not specify whether to use profile likelihood, Wald, or exact CIs for the OR of discordant pairs.
3. The Cohen's g interpretation table is provided (small: 0.05-0.15, medium: 0.15-0.25, large: >= 0.25) but no expected Cohen's g is calculated under the design assumptions (p12=0.20, p21=0.10 implies P=0.20/(0.20+0.10)=0.667, g=0.167, which is "medium" — this calculation would be valuable).

**Improvement Path:**
Add a CI width estimate for kappa at n=27 (e.g., "expected 95% CI ±0.18 at n=27, improving to ±0.10 at n=50"). Add an expected Cohen's g calculation under design assumptions. Add CI method recommendation for OR.

---

### Internal Consistency (0.95/1.00)

**Evidence:**
No contradictions detected across sections. The n=270 discrepancy is the document's primary finding and is consistently flagged throughout (L0, RQ2, L2 risk table, critical warning). The OR of 2.0 under design assumptions (p12/p21 = 0.20/0.10) is arithmetically correct. The per-model n=90 is correctly derived from 270/3. The Bonferroni alpha of 0.00238 is correctly computed as 0.05/21. The CMH-as-McNemar-generalization claim (references 9, 10) is cited and used consistently. The L2 risk table's "MEDIUM/HIGH -- cannot pool" for Breslow-Day rejection is consistent with the RQ4 recommendation to run per-model McNemar tests regardless.

**Gaps:**
1. The sample size table (RQ2) includes "Schoenfeld simplified: n=236" but Schoenfeld (1980) does not appear in the References section. This creates a minor internal inconsistency: the data point is in the table but the citation is absent, making it unverifiable.
2. The document notes in RQ5 that "the raters are trained (LLM-as-judge with calibration)" — this presupposes a calibration step that is not documented in the referenced design. If LLM-as-judge is uncalibrated, this framing is inconsistent with the actual design.

**Improvement Path:**
Add Schoenfeld (1987) or the correct Schoenfeld citation to the reference list with its key insight. Verify that "LLM-as-judge with calibration" accurately describes the planned evaluation approach; if calibration is not planned, revise to "LLM-as-judge per rubric."

---

### Methodological Rigor (0.88/1.00)

**Evidence:**
Seven formula variants are independently computed and compared (Miettinen, Schoenfeld, Machin, Simple CC, Fleiss CC, MedCalc calculator, design document). The McNemar test statistic is stated with both the formula and the chi-squared distribution claim. The asymptotic validity threshold (b + c >= 25) is cited to references [2][3]. Fagerland et al. (2013) [4] is a peer-reviewed BMC paper supporting the mid-p recommendation. Westfall et al. (2010) [15] is a peer-reviewed Biometrics paper supporting the discrete Bonferroni-Holm procedure. Limitations are explicitly documented in the PS Integration section (Connor 1987 not directly accessed, n=270 not reproducible, no LLM-specific McNemar papers found).

**Gaps:**
1. **The 41% per-model power claim is asserted without a shown calculation.** This is the document's "most significant methodological concern" and the critical warning, yet the power derivation is not shown. At n=90 per model with p12=0.20, p21=0.10, alpha=0.05, what is the exact power? The document says "approximately 41%" without showing the formula evaluation. Using Miettinen's formula rearranged for power: delta/sqrt(p_d/n) = 0.10/sqrt(0.30/90) = 0.10/0.0577 = 1.732; power = Phi(1.732 - 1.96) = Phi(-0.228) = 0.41. This calculation exists but is not shown, leaving the most critical finding unsupported by explicit derivation.
2. The asymptotic validity threshold "b + c >= 25" is cited but the expected discordant count at n=90 per model is not computed. With p_d=0.30, expected b+c = 0.30 * 90 = 27 — marginally above 25. This is worth noting explicitly as a borderline case for the per-model analyses.
3. The Connor (1987) reference notes it "showed Miettinen slightly underestimates required n" but the magnitude is not stated. If Connor yields a different n than Miettinen, it should appear in the 7-formula table.

**Improvement Path:**
Show the per-model power formula evaluation step-by-step as a numbered calculation. Add expected per-model discordant count (27) and note the asymptotic borderline. Add Connor (1987) n to the formula table (or note why it was excluded — likely the secondhand access limitation).

---

### Evidence Quality (0.84/1.00)

**Evidence:**
17 sources are consulted across primary papers (McNemar 1947, Miettinen 1968, Westfall et al. 2010, Fagerland et al. 2013), review articles (McHugh 2012, Landis & Koch 1977, Cicchetti 1994), online calculators (MedCalc, Vienna University, rcompanion.org), and software documentation (mlxtend). The mlxtend citation specifically validates the ML-context applicability. The Fagerland et al. (2013) paper's mid-p recommendation is a peer-reviewed, journal-published finding — strong evidence.

**Gaps:**
1. **Schoenfeld (1980) appears in the sample size table (n=236, "Schoenfeld simplified") but has no entry in the References section.** This is the most significant evidence quality gap: a data point used in the primary comparative analysis is uncited. Without a reference, readers cannot verify this n=236 figure.
2. **Connor (1987) is described as "referenced by PubMed" — secondhand citation.** The document did not access the original paper. This is acknowledged as a gap in the PS Integration section but the use of secondhand Connor citation weakens the formula table. Connor's improvement over Miettinen is not quantified.
3. **Two Wikipedia sources (references 10, 13)** are used for the CMH definition and Bonferroni correction. While the facts cited are definitional and low-risk, Wikipedia is a tertiary source. For a C4 research artifact, these should be replaced or supplemented with authoritative secondary sources (e.g., Agresti's Categorical Data Analysis for CMH; Shaffer 1995 for multiple comparisons).
4. **The "41% power" critical warning** — the document's most consequential finding — is not supported by a shown calculation or a cited formula. A reader cannot verify this figure from the document alone.
5. **No LLM evaluation methodology papers are cited.** The document acknowledges "no LLM-specific papers found using McNemar's test for prompt comparison." This gap is noted but not mitigated — a brief search for LLM evaluation methodology papers (e.g., Bai et al. 2022 Constitutional AI, Perez et al. 2022 prompt comparison) may surface relevant precedents or confirm the gap is genuine.

**Improvement Path:**
1. Add Schoenfeld citation (Schoenfeld DA (1980) or identify the correct Schoenfeld reference and add to references list).
2. Replace or supplement Wikipedia references 10 and 13 with textbook citations (Agresti for CMH; any statistics textbook for Bonferroni).
3. Show the per-model power calculation explicitly (this doubles as a Methodological Rigor improvement).
4. Search "McNemar prompt comparison" or "paired binary LLM evaluation" in Google Scholar and add any relevant papers, or document the null result with search terms used.

---

### Actionability (0.91/1.00)

**Evidence:**
The L2 Design Validation Summary table provides STATUS/RISK/ACTION for each of the 6 design elements — this is directly usable by Phase 0 design agents. The Strategic Recommendations section gives 5 numbered, specific recommendations. The per-model power warning gives 3 concrete options with exact numbers: "accept 41% power," "increase to n=702 (234 per model x 3)," or "use CMH as primary." The multiple comparison recommendation includes specific alpha values: alpha=0.00238 (Bonferroni) and alpha=0.00833 (if 6 primary contrasts). The continuity correction recommendation is specific: "uncorrected asymptotic as primary, mid-p and exact as sensitivity."

**Gaps:**
1. The OR/Cohen's g/risk difference formulas are scattered across RQ3 rather than consolidated in one place. Phase 0 agents implementing the analysis plan would need to extract from multiple paragraphs. A consolidated "Effect Size Computation" box with all three formulas and their interpretation scales in one table would improve direct usability.
2. The Breslow-Day prerequisite is stated but the document does not specify which software/library implements it (e.g., scipy has no Breslow-Day; R's mantelhaen.test or the BreslowDayTest package would need to be specified). This is an implementation gap for the experiment execution phase.

**Improvement Path:**
Add a consolidated effect size formula table with OR = b/c, Cohen's g = P - 0.5 (P = max(b,c)/(b+c)), and pi_d = (b-c)/n in one place. Add a note on Breslow-Day implementation (e.g., "Use R's BreslowDayTest package or Python's statsmodels.stats.contingency_tables.StratifiedTable").

---

### Traceability (0.90/1.00)

**Evidence:**
The n=270 vs. n=234-253 discrepancy is the document's primary finding and is explicitly traced: L0 flags it, RQ2 documents three hypotheses for its origin (dropout inflation, higher p_d, conservative rounding), and L2 provides a decision with cost analysis ("36 additional instances = ~2 hours compute"). Design parameters (p12=0.20, p21=0.10, alpha=0.05, power=0.80) are stated in RQ2 and used consistently. The PS Integration section links to TASK-025, PROJ-014, and the artifact path. The L2 risk table maps each risk to a mitigation.

**Gaps:**
1. The document does not trace where the 7 conditions C1-C7 come from. RQ6 states "For 7 conditions (C1-C7)" but does not reference the design document section that defines these conditions. A reader coming only to this research document cannot verify that 21 comparisons is the correct number without accessing the parent design.
2. The design confidence rating (HIGH, 0.85) appears in the metadata but the PS Integration section does not link to the parent ORCHESTRATION_PLAN.md or ORCHESTRATION.yaml, creating a traceability gap for the orchestration context.

**Improvement Path:**
Add a parenthetical "(see design document section X)" when referencing the 7 conditions. Add a reference to the ORCHESTRATION_PLAN.md in the PS Integration section.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.84 | 0.91 | Add Schoenfeld (1980 or correct year) citation to references with formula and key insight; this citation appears in the data table but is absent from the reference list |
| 2 | Methodological Rigor / Evidence Quality | 0.88 / 0.84 | 0.93 / 0.91 | Show the per-model power derivation step-by-step: delta/sqrt(p_d/n) = 0.10/sqrt(0.30/90) = 1.732; power = Phi(1.732 - 1.96) = Phi(-0.228) = 0.41; this is the document's most important finding and must be verifiable |
| 3 | Evidence Quality | 0.84 | 0.91 | Replace Wikipedia references 10 and 13 with authoritative sources: Agresti "Categorical Data Analysis" (2002) for CMH, and a statistics textbook or Shaffer (1995) for Bonferroni; Wikipedia is acceptable for rough orientation but not for C4 research |
| 4 | Internal Consistency | 0.95 | 0.97 | Verify and clarify the "LLM-as-judge with calibration" statement in RQ5: if calibration is planned, document what it consists of; if not planned, revise to "LLM-as-judge per scoring rubric" to avoid overstating the design |
| 5 | Evidence Quality | 0.84 | 0.89 | Document a search for LLM-specific prompt comparison papers using McNemar's test: search terms "McNemar prompt framing LLM evaluation" and "paired binary LLM comparison"; report either found papers or "null result with these search terms" to convert a known gap into documented completeness |
| 6 | Completeness | 0.90 | 0.94 | Add expected Cohen's g under design assumptions: P = 0.20/(0.20+0.10) = 0.667, g = 0.667 - 0.50 = 0.167 (medium effect); this concretizes what effect size the experiment is powered to detect |
| 7 | Actionability | 0.91 | 0.94 | Add a consolidated "Effect Size Computation" table with all three formulas (OR, Cohen's g, risk difference) and their interpretation scales in one location; add Breslow-Day implementation note (R package or Python equivalent) |
| 8 | Completeness / Traceability | 0.90 / 0.90 | 0.93 / 0.94 | Add kappa CI width estimate at n=27 double-scored instances; add reference to C1-C7 condition definitions in the parent design document; add ORCHESTRATION_PLAN.md reference in PS Integration |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific section/claim citations
- [x] Uncertain scores resolved downward (Evidence Quality 0.84 vs. the generous 0.88 initially considered given the 17-source count)
- [x] First-draft calibration considered (this is a research deliverable with 17 sources, computed 7 variants — strong first draft; still below C4 threshold)
- [x] No dimension scored above 0.95 without exceptional evidence (Internal Consistency at 0.95 is justified: zero contradictions found in a numerically dense document with multiple cross-referenced figures)

**Anti-leniency notes:**
- The 17-source count and 7-formula computation were noted as impressive, but dimensional scoring still penalized the missing Schoenfeld reference and unsupported 41% power claim rather than letting the source count inflate Evidence Quality
- The "strong research artifact" impression was resisted: improvement areas were found in every dimension per protocol
- The per-model power claim (41%) is the document's most consequential finding and lacks a shown derivation — this appropriately brings Methodological Rigor and Evidence Quality scores down

---

## Verdict

**REVISE**

Composite score 0.8985 does not meet the C4 threshold of 0.95. The document is strong — all 6 RQs answered, 17 sources, 7 formula variants computed, critical per-model power warning is genuinely valuable. However, four fixable gaps prevent passage at C4:

1. Schoenfeld (1980) appears in the comparative table but has no reference entry — a data point used in the primary analysis is uncitable
2. The 41% per-model power claim — the document's most important finding — lacks a shown formula derivation
3. Two Wikipedia sources in a C4 statistical research document are insufficient authority
4. Connor (1987) is secondhand only

All 4 gaps are correctable in a single revision pass. Expected score after revision: 0.93-0.96.
