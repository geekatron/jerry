# Statistical Methodology Research: McNemar's Test for LLM A/B Testing

> Research output for PROJ-014 TASK-025 experimental design validation.
> Agent: ps-researcher | Date: 2026-03-01 | Confidence: HIGH (0.88) | Iteration: 2

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Non-technical overview of findings |
| [L1: Technical Analysis](#l1-technical-analysis) | Detailed statistical methodology |
| [L2: Architectural Implications](#l2-architectural-implications) | Design decisions and trade-offs |
| [Research Questions](#research-questions) | The six questions investigated |
| [Methodology](#methodology) | How this research was conducted |
| [References](#references) | Full citation list |
| [Revision History](#revision-history) | Changes by iteration |

---

## L0: Executive Summary

This research validates the statistical methodology for the PROJ-014 A/B experiment comparing positive vs. negative prompt framing for LLM guardrails. The experiment uses a matched-pairs design where the same test instance is evaluated under both conditions, producing binary COMPLY/VIOLATE outcomes.

**Key finding:** McNemar's test is the correct statistical method for this design. It is specifically designed for paired binary data and focuses on *discordant pairs* -- cases where the two conditions disagree -- which is exactly what the experiment measures. The mlxtend Python library explicitly documents McNemar's test for classifier comparison, validating its use in machine learning contexts. Recent LLM evaluation literature confirms growing adoption of McNemar's test for paired model and prompt comparisons (Kuebler et al., 2025; Vishwanath et al., 2025).

**Sample size concern:** The planned n=270 does not match any standard McNemar sample size formula with the stated parameters (p12=0.20, p21=0.10, alpha=0.05, power=0.80). The Miettinen (1968) formula yields n=234 without continuity correction. The Fleiss continuity correction yields n=253. The n=270 figure appears to incorporate an unstated ~7% inflation factor (possibly for attrition or conservative rounding). **Recommendation: either document the inflation justification or revise to n=253 (Fleiss CC) as the defensible figure.**

**Per-model power warning:** With n=270 split across 3 models, each model has n=90. The per-model power is approximately **41%**, derived step-by-step: delta/sqrt(p_d/n) = 0.10/sqrt(0.30/90) = 1.732; power = Phi(1.732 - 1.96) = Phi(-0.228) = 0.41. This is well below the 80% threshold, making per-model analyses exploratory only.

**Other design elements are sound:** Cohen's kappa >= 0.70 for inter-rater reliability is within the "substantial agreement" range per Landis and Koch (1977). Under the design assumptions, the expected Cohen's g = 0.167 (medium effect per Cohen's conventions). The Bonferroni-corrected alpha for 21 pairwise comparisons is 0.00238 -- consider the less conservative Benjamini-Hochberg FDR procedure as an alternative. The Cochran-Mantel-Haenszel test is appropriate for stratified analysis across models, but with an important caveat: a Breslow-Day test for homogeneity of odds ratios should be run first to verify that combining across model strata is valid.

---

## Research Questions

| # | Question | Verdict |
|---|----------|---------|
| RQ1 | Is McNemar's test correct for this design? | **YES** -- confirmed |
| RQ2 | Is n=270 the correct sample size? | **NO** -- standard formulas yield 234-253; 270 is inflated |
| RQ3 | Is pi_d = (b-c)/n the right effect size? | **PARTIALLY** -- valid but non-standard; odds ratio is preferred |
| RQ4 | Is CMH correct for multi-model stratification? | **YES** -- with Breslow-Day homogeneity prerequisite |
| RQ5 | Is Cohen's kappa >= 0.70 appropriate? | **YES** -- within "substantial" agreement range |
| RQ6 | What is the Bonferroni-corrected alpha for 21 comparisons? | **0.00238** -- but consider BH-FDR as alternative |

---

## Methodology

### Sources Consulted

| Source Type | Count | Examples |
|-------------|-------|---------|
| Primary (official docs, original papers) | 8 | McNemar (1947), Connor (1987), Miettinen (1968), Landis & Koch (1977), Agresti (2002), Dunn (1961) |
| Secondary (review articles, handbooks) | 5 | Fagerland et al. (2013), McHugh (2012), Westfall et al. (2010) |
| Tertiary (calculators, tutorials) | 4 | MedCalc, Vienna Univ. calculator, rcompanion.org, mlxtend docs |
| LLM evaluation papers | 2 | Kuebler et al. (2025), Vishwanath et al. (2025) |
| Computational validation | 1 | Python calculation of 7 formula variants |

### Approach

1. Web search for McNemar methodology, sample size formulas, and LLM evaluation practices
2. Cross-validation of sample size formulas using multiple online calculators and primary sources
3. Independent computational verification using Python (7 formula variants)
4. Synthesis of effect size, stratification, and multiple comparison methods from multiple sources
5. Targeted search for LLM-specific McNemar usage papers (2023-2026) to validate methodological precedent

### LLM-Specific McNemar Search (Iteration 2 Addition)

**Search terms used:**
- "McNemar test LLM evaluation large language model comparison 2023 2024 2025"
- "McNemar test prompt prompting LLM evaluation paired comparison arxiv 2024 2025"
- "McNemar paired binary classifier comparison NLP LLM paper arxiv 2023 2024"

**Results:** Two relevant papers found:

1. **Kuebler et al. (2025)** -- "When LLMs get significantly worse: A statistical approach to detect model degradations" (ICLR 2026). Uses the exact one-sided McNemar test for per-sample degradation detection in LLMs. The paper compares model scores at the sample level rather than aggregated task level, demonstrating that McNemar's test can detect accuracy drops as small as 0.3%. This directly validates our per-instance paired design [18].

2. **Vishwanath et al. (2025)** -- "Generalist Large Language Models Outperform Clinical Tools on Medical Benchmarks." Uses pairwise exact McNemar's tests for statistical significance when comparing model pairs on medical benchmarks [19].

**Null result areas:** No papers found specifically using McNemar's test to compare prompt framing strategies (positive vs. negative) on the same model. The methodology is borrowed from the classifier comparison and model degradation literature, which is structurally identical to our design (two conditions, same test instances, binary outcomes).

---

## L1: Technical Analysis

### RQ1: McNemar's Test for Matched-Pair Binary Outcomes

**Verdict: CONFIRMED -- McNemar's test is the correct choice.**

McNemar's test (1947) is specifically designed for paired nominal (binary) data in 2x2 contingency tables with matched pairs [1]. The test evaluates whether the row and column marginal frequencies are equal (marginal homogeneity).

#### The 2x2 Table for This Experiment

For each test instance evaluated under both positive (P) and negative (N) framing:

```
                    Negative: COMPLY    Negative: VIOLATE
Positive: COMPLY        a                    b
Positive: VIOLATE       c                    d
```

Where:
- **a** = both conditions comply (concordant)
- **d** = both conditions violate (concordant)
- **b** = positive complies, negative violates (discordant) -- corresponds to p21
- **c** = positive violates, negative complies (discordant) -- corresponds to p12

**Key insight:** McNemar's test considers *only* the discordant pairs (b and c). The concordant pairs (a and d) provide no information about which condition is superior [1][2].

#### Test Statistic

Without continuity correction:

```
chi2 = (b - c)^2 / (b + c)
```

With Edwards' continuity correction [3]:

```
chi2_cc = (|b - c| - 1)^2 / (b + c)
```

Under H0 (marginal homogeneity), the test statistic follows a chi-squared distribution with 1 degree of freedom.

#### When to Use Exact vs. Asymptotic

- If b + c >= 25: use the asymptotic chi-squared test (with or without CC) [2]
- If b + c < 25: use the exact binomial test [2][3]
- Fagerland et al. (2013) recommend the mid-p test as performing better than both the exact conditional and asymptotic with CC [4]

#### Applicability to LLM Evaluation

The mlxtend library explicitly implements McNemar's test for classifier comparison, with the exact same 2x2 table structure used for comparing two models on the same test set [3]. Our design is structurally identical: two "classifiers" (prompting strategies) applied to the same test instances.

**LLM evaluation precedent:** Kuebler et al. (2025) demonstrate McNemar's test for per-sample LLM degradation detection at ICLR 2026, comparing model outputs on the same evaluation instances [18]. Vishwanath et al. (2025) use pairwise exact McNemar's tests for comparing generalist LLMs on medical benchmarks [19]. Both papers validate the paired-sample, per-instance design pattern used in this experiment.

**Citation chain:** McNemar (1947) [1] -> Edwards (1948) [3] -> Fagerland et al. (2013) [4] -> mlxtend implementation [3] -> LLM evaluation: Kuebler et al. (2025) [18], Vishwanath et al. (2025) [19].

---

### RQ2: Sample Size Calculation

**Verdict: n=270 is NOT directly reproducible from standard formulas. Recommend revision to n=253 or explicit justification of the inflation factor.**

#### The Standard Formula (Miettinen, 1968)

The canonical sample size formula for McNemar's test is [5][6]:

```
n = [ z_{alpha/2} * sqrt(p_d) + z_{beta} * sqrt(p_d - delta^2) ]^2 / delta^2
```

Where:
- `n` = required number of pairs (each pair = one test instance under both conditions)
- `z_{alpha/2}` = 1.96 for two-sided alpha = 0.05
- `z_{beta}` = 0.8416 for power = 0.80
- `p_d` = p12 + p21 = proportion of discordant pairs = 0.20 + 0.10 = 0.30
- `delta` = p12 - p21 = difference in discordant proportions = 0.10

#### Computational Validation (7 Formula Variants)

| Formula | n (ceiling) | Source | Notes |
|---------|-------------|--------|-------|
| Miettinen (no CC) | **234** | Miettinen (1968) [5] | Standard formula, no continuity correction |
| Connor (multinomial approx.) | **236** | Connor (1987) [6] | Slightly conservative; multinomial-based expression |
| Schoenfeld (simplified) | **236** | Schoenfeld (1980) [20] | Simplified approximation; coincides with Connor |
| Machin CC variant | **243** | Machin et al. (2009) [7] | Continuity correction variant |
| Simple CC (n + 1/delta) | **244** | Common approximation | Standard CC add-on |
| Fleiss CC | **253** | Fleiss et al. (2003) | Most conservative standard CC |
| MedCalc calculator (same params) | **234** | MedCalc [7] -- no CC applied | Validates Miettinen |
| **Design document** | **270** | **Not reproducible from standard formulas** | See analysis below |

**Connor (1987) note:** Connor [6] provides a multinomial-based expression for sample size that yields n=236 for our parameters. This is 2 more than the Miettinen formula (n=234), confirming Connor's observation that Miettinen slightly underestimates required n. Connor's result is included in the table above. The original paper was not directly accessed (cited via Stata documentation [17] and NCSS PASS documentation [16]); the n=236 figure is consistent across these secondary sources.

The MedCalc calculator, using the exact same parameters (p12=0.20, p21=0.10, alpha=0.05, power=0.80), returns n=234 [7]. This matches our Miettinen formula calculation exactly.

#### Where Could n=270 Come From?

Three hypotheses:

1. **Fleiss CC with dropout inflation:** 253 / 0.94 = 269.1 (approximately 270 with 6% dropout assumption). This is the most plausible explanation.
2. **Higher discordant proportion:** p_d = 0.35 (instead of 0.30) produces n = 272 via Miettinen. If the expected discordant proportion is higher, n increases.
3. **Conservative rounding:** Rounding up from 253 to the nearest multiple of some design parameter (e.g., 270 = 90 instances x 3 models, where 90 is a round number per stratum).

**Recommendation:** If n=270 is retained, document the justification (e.g., "Fleiss CC n=253 inflated by 7% for potential scoring attrition"). If no inflation factor was intended, revise to n=253 (Fleiss CC) or n=234 (no CC per MedCalc/Miettinen).

**Power implications:** At n=270 with the stated parameters, power exceeds 0.80, providing a slight safety margin. This is conservative but defensible.

---

### RQ3: Effect Size for McNemar's Test

**Verdict: pi_d = (b-c)/n is a valid but non-standard measure. The odds ratio of discordant pairs is the preferred effect size.**

#### Consolidated Effect Size Table

All effect size measures for McNemar's test, with design assumption values (p12=0.20, p21=0.10) [8]:

| Measure | Formula | Design Value | Interpretation Scale | Convention | Recommended? |
|---------|---------|-------------|---------------------|------------|--------------|
| **Odds Ratio (OR)** | OR = b/c (or equivalently p12/p21) | **2.0** | Small: 1.22-1.86; Medium: 1.86-3.00; Large: >= 3.00 | Medium | **YES -- primary** |
| **Risk Difference (pi_d)** | pi_d = (b-c)/n or equivalently p12 - p21 | **0.10** | Absolute scale, project-specific | N/A (absolute) | YES -- descriptive |
| **Cohen's g** | g = P - 0.5 where P = max(b/(b+c), c/(b+c)) | **0.167** | Small: 0.05-0.15; Medium: 0.15-0.25; Large: >= 0.25 | Medium | YES -- secondary |
| **Discordant proportion (p_d)** | p_d = (b+c)/n = p12 + p21 | **0.30** | Proportion of total disagreements | N/A (design parameter) | YES -- reporting |

#### Expected Cohen's g Calculation (Design Assumptions)

Under the design assumptions (p12=0.20, p21=0.10):

```
P = max(p12, p21) / (p12 + p21) = 0.20 / (0.20 + 0.10) = 0.20 / 0.30 = 0.667
g = P - 0.50 = 0.667 - 0.50 = 0.167
```

Per Cohen's conventions for g: small = 0.05-0.15, medium = 0.15-0.25, large >= 0.25. The expected g = 0.167 falls in the **medium** range, indicating the experiment is designed to detect a medium-sized effect in the McNemar framework.

**Interpretation:** An OR of 2.0 means instances are twice as likely to switch to compliance under negative framing as to switch away from compliance. Cohen's g of 0.167 means that among discordant pairs, 66.7% favor negative framing vs. 33.3% favoring positive framing -- a 2:1 ratio.

#### Analysis of pi_d = (b-c)/n

The measure proposed in the design document, pi_d = (b-c)/n, is equivalent to the difference in marginal proportions (p1+ - p+1). This is:

- **Valid:** It measures the absolute difference in compliance rates between conditions.
- **Interpretable:** A pi_d of 0.10 means positive framing complies 10 percentage points less often than negative framing.
- **Non-standard for McNemar:** The standard effect size literature for McNemar's test uses the odds ratio of discordant pairs, not a raw difference [8].

**Recommendation:** Report all four measures in the results:
1. **Primary:** Odds ratio (OR = 2.0 under design assumptions) with 95% CI. Use profile likelihood CI for the OR of discordant pairs.
2. **Secondary:** Cohen's g = 0.167 (medium) for standardized comparison across studies.
3. **Descriptive:** Risk difference pi_d = (b-c)/n for practical interpretation.
4. **Design parameter:** Discordant proportion p_d for characterizing overall disagreement.

The OR and Cohen's g are mathematically linked: OR = 1 corresponds to g = 0; as OR approaches infinity, g approaches 0.5 [8].

#### Breslow-Day Implementation Note

For testing homogeneity of odds ratios across model strata (prerequisite for CMH pooling):

| Language | Implementation | Usage |
|----------|---------------|-------|
| **Python** | `statsmodels.stats.contingency_tables.StratifiedTable` | `st = StratifiedTable(tables); st.summary()` -- reports "Test constant OR" with statistic and p-value [21] |
| **R** | `DescTools::BreslowDayTest()` | `BreslowDayTest(table_array)` -- takes 2x2xk array [21] |

**Decision threshold:** If Breslow-Day p < 0.10 (conventional threshold for homogeneity tests, which use a liberal alpha to protect against falsely assuming homogeneity), do NOT pool -- report per-model McNemar results instead.

---

### RQ4: Multi-Model Stratification with CMH

**Verdict: CMH is appropriate, but with important prerequisites.**

#### Design Context

The experiment runs across 3 models (haiku, sonnet, opus). For each model, the same test instances produce a paired 2x2 table. The question is how to combine these.

#### Cochran-Mantel-Haenszel (CMH) Test

The CMH test is designed for combining multiple 2x2 tables with a common odds ratio across strata [9][10]. It:

1. Tests whether the association between condition and outcome is consistent across strata
2. Produces a common (pooled) odds ratio estimate
3. Controls for the stratifying variable (model)

**Key relationship:** McNemar's test is a special case of CMH. Specifically, McNemar's test is equivalent to a CMH test with N strata, one for each pair [9][10]. This makes CMH a natural extension for stratifying across models.

#### Prerequisites (CRITICAL)

Before running CMH, the **Breslow-Day test for homogeneity of odds ratios** must be run [10]:

- **H0:** The odds ratios are equal across strata (models)
- **If NOT rejected (p >= 0.10):** CMH is valid; combine strata
- **If rejected (p < 0.10):** The treatment effect differs across models -- do NOT pool. Instead, run separate McNemar tests per model and report model-specific effects.

This is not a formality. If negative framing works for haiku but not for opus, the pooled CMH estimate would be misleading.

#### Alternative: Stratified McNemar

An alternative to CMH is the **stratified McNemar test** (Tang et al., 2014), which extends McNemar's test directly to stratified paired binary data [11]. This tests whether the common risk difference (CRD) is zero while accounting for stratification.

**Recommendation:** Use both:
1. **Breslow-Day test** for homogeneity of odds ratios across models (see implementation note in RQ3 effect size table)
2. **If homogeneous:** CMH for the combined estimate
3. **Regardless:** Report per-model McNemar tests to characterize model-specific effects
4. **Consider:** Stratified McNemar test as a sensitivity analysis

---

### RQ5: Inter-Rater Reliability (Cohen's Kappa >= 0.70)

**Verdict: Adequate, but document the interpretation scale used.**

#### Interpretation Scales

Multiple scales exist for interpreting kappa [12]:

| Scale | 0.61-0.80 Classification | 0.70 Specifically |
|-------|--------------------------|-------------------|
| Landis & Koch (1977) | "Substantial" | Substantial |
| Fleiss (1971) | "Fair to good" (0.40-0.75) | Fair to good |
| McHugh (2012) | "Moderate" (0.60-0.79) | Moderate |
| Cicchetti (1994) | "Good" (0.60-0.74) | Good |

Kappa >= 0.70 falls within the "substantial" range per the most commonly cited Landis and Koch (1977) scale, and within "good" per Cicchetti (1994). McHugh (2012) argues that kappa >= 0.60 should be the minimum for research and recommends >= 0.80 for strong agreement [12].

#### Considerations for Binary Compliance Scoring

For binary COMPLY/VIOLATE scoring with clear rubric criteria:

- **Base rate matters:** If compliance rates are very high (>90%) or very low (<10%), kappa is paradoxically deflated even with high agreement. Report both kappa and percent agreement [12].
- **0.70 is appropriate** for this use case: the scoring rubric is well-defined (constitutional compliance is binary), the raters follow a structured scoring rubric (LLM-as-judge per rubric criteria), and the stakes are research-level (not clinical diagnosis).

**Recommendation:** Retain kappa >= 0.70. Additionally report percent agreement. If kappa is paradoxically low despite high percent agreement, note the base rate effect and rely on percent agreement as the primary measure.

#### Double-Scoring 10% Subset and Kappa CI Estimate at n=27

A 10% subset for inter-rater reliability is standard practice in content analysis research. For n=270, this means 27 instances double-scored.

**Approximate 95% CI width at n=27 with expected kappa=0.70:**

The asymptotic standard error of kappa follows the Fleiss, Cohen, and Everitt (1969) formula [22]. For binary ratings with expected kappa=0.70 and balanced-to-moderate base rates, the approximate standard error is:

```
SE(kappa) ~ 0.10 to 0.14  (at n=27, depending on base rate)
```

This yields a 95% CI of approximately:

```
kappa = 0.70 +/- 1.96 * SE = 0.70 +/- 0.20 to 0.27
Approximate 95% CI: [0.43, 0.97] to [0.56, 0.84]
```

**Interpretation:** At n=27, the 95% CI for kappa is wide (total width ~0.28 to ~0.40). This means:
- If observed kappa = 0.70, the CI could extend below the "substantial" threshold (0.61) into the "moderate" range
- The CI is sufficient to establish that agreement is meaningfully above chance (lower bound well above 0) but not precise enough to distinguish between "moderate" and "substantial" agreement classifications
- Increasing to n=50 double-scored instances would narrow the CI width by approximately 36% (SE scales as 1/sqrt(n)), yielding a CI of approximately +/- 0.15

**Note on small-sample concerns:** At n=27, the kappa sampling distribution may be non-symmetric [22]. Bootstrap CIs or Fisher z-transformation CIs may be more accurate than the asymptotic normal approximation. If feasible, compute both and report the more conservative.

#### Condition Definitions (C1-C7)

The 7 conditions (C1-C7) that generate the 21 pairwise comparisons are defined in the parent experimental design document (TASK-025 design specification). See the experimental conditions matrix in the design document for the full definition of each condition, which maps prompt framing variants to constitutional compliance categories.

---

### RQ6: Bonferroni Correction for 21 Pairwise Comparisons

**Verdict: Corrected alpha = 0.05/21 = 0.00238. Consider BH-FDR as a less conservative alternative.**

#### Calculation

For 7 conditions (C1-C7, defined in the experimental design document -- see RQ5 note), the number of pairwise comparisons is:

```
k = 7 * (7-1) / 2 = 21
```

Bonferroni-corrected significance level [13]:

```
alpha_corrected = 0.05 / 21 = 0.002381
```

This means each individual pairwise McNemar test must achieve p < 0.00238 to be declared significant at the family-wise alpha = 0.05 level.

**Attribution note:** The Bonferroni correction is named after Carlo Emilio Bonferroni (1892-1960) for the underlying inequality, but its practical application to multiple comparisons was first formalized by Dunn (1961) [13]. The method is sometimes called the Bonferroni-Dunn procedure.

#### Power Implications

Bonferroni correction substantially reduces power. For each pairwise test at alpha = 0.00238:

- z_{alpha/2} increases from 1.96 to approximately 3.04
- Required sample size increases proportionally

This means the experiment designed for n=234-270 at alpha=0.05 will have substantially less power for the individual pairwise comparisons under Bonferroni correction.

#### Alternative: Benjamini-Hochberg FDR

The Benjamini-Hochberg (BH) procedure controls the False Discovery Rate rather than the Family-Wise Error Rate [14]:

| Method | Controls | Threshold for 21 tests | Power |
|--------|----------|----------------------|-------|
| Bonferroni | FWER | alpha/21 = 0.00238 | Conservative (low power) |
| Holm (step-down) | FWER | Adaptive (0.00238 to 0.05) | Slightly more powerful |
| BH-FDR | FDR | Adaptive | More powerful |

**Recommendation:** Use Bonferroni as the primary correction (conservative, defensible). Report BH-FDR as a sensitivity analysis. For the multiple McNemar tests specifically, Westfall et al. (2010) recommend a discrete Bonferroni-Holm procedure that leverages the exact binomial nature of McNemar's test to gain power [15].

#### Practical Note

With 7 conditions, not all 21 pairwise comparisons are equally interesting. If the experiment has pre-planned contrasts (e.g., positive vs. each negative variant), the number of planned comparisons may be smaller (e.g., 6 instead of 21), reducing the correction burden:

```
alpha_6 = 0.05 / 6 = 0.00833
```

This is less conservative and may be more appropriate if the design has primary hypotheses.

---

## L2: Architectural Implications

### Design Validation Summary

| Design Element | Status | Risk | Action |
|----------------|--------|------|--------|
| McNemar's test selection | VALID | None | No change needed |
| Sample size n=270 | INFLATED | Low | Document inflation justification or revise to n=253 |
| Effect size pi_d | NON-STANDARD | Medium | Add odds ratio as primary effect size; report all 4 measures |
| CMH for multi-model | VALID | Medium | Add Breslow-Day prerequisite (see implementation note) |
| Cohen's kappa >= 0.70 | ADEQUATE | Low | Add percent agreement co-reporting; note CI width at n=27 |
| Bonferroni for 21 tests | VALID but CONSERVATIVE | Medium | Consider BH-FDR sensitivity analysis |

### Strategic Recommendations

1. **Sample Size Decision:** The difference between n=234 and n=270 is 36 test instances. At ~3 minutes per instance for LLM evaluation, this is ~2 hours of additional compute. The marginal cost is low; if n=270 is already built into the test harness, retain it for the power margin. But document why it differs from the formula.

2. **Effect Size Reporting:** The paper should report four effect sizes (OR, Cohen's g, risk difference, discordant proportion) to maximize comparability with both clinical/epidemiological literature (OR) and applied ML literature (risk difference). See the consolidated effect size table in RQ3.

3. **Multi-Model Analysis Strategy:** The most informative analysis plan is:
   - Per-model McNemar tests (primary: characterize each model's sensitivity to framing)
   - Breslow-Day homogeneity test (prerequisite for pooling; implementation: Python `statsmodels.stats.contingency_tables.StratifiedTable` or R `DescTools::BreslowDayTest()`)
   - CMH pooled estimate (if homogeneous: overall effect)
   - Interaction analysis (if heterogeneous: which models respond to framing?)

4. **Multiple Comparisons Strategy:** Pre-register which comparisons are primary hypotheses vs. exploratory. If only 6 primary contrasts (positive vs. each negative variant), use alpha = 0.05/6 = 0.00833 for primaries and BH-FDR for the remaining 15 exploratory comparisons.

5. **Continuity Correction Decision:** Given the expected discordant pair count (b + c will be in the range of 60-90 for n=234-270 with p_d=0.30), the asymptotic test without continuity correction is appropriate. Fagerland et al. (2013) argue against Edwards' CC, finding the mid-p test superior [4]. Recommendation: report the uncorrected asymptotic test as primary, with mid-p and exact tests as sensitivity checks.

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Breslow-Day rejects homogeneity (models differ) | MEDIUM | HIGH -- cannot pool | Pre-register per-model analysis as primary |
| Low discordant pair count (<25 per cell) | LOW | MEDIUM -- asymptotic invalid | Use exact binomial McNemar |
| Kappa paradox (high agreement, low kappa) | MEDIUM | LOW -- reporting only | Co-report percent agreement |
| Bonferroni too conservative | HIGH | MEDIUM -- miss real effects | Pre-register planned comparisons |
| Sample size insufficient for subgroup (per-model) | MEDIUM | HIGH | n=234-270 spread across 3 models = 78-90 per model; power drops to ~41% per model (see derivation below) |
| Wide kappa CI at n=27 double-scored | MEDIUM | LOW | Report CI alongside point estimate; consider bootstrap CI |

### Critical Warning: Per-Model Power

With n=270 total and 3 models, each model has approximately n=90 instances. At n=90 per model with the same parameters (p12=0.20, p21=0.10), power drops to approximately **41%**. This is well below the 80% threshold.

#### Per-Model Power Derivation (Step-by-Step)

Using the Miettinen (1968) formula rearranged for power at fixed n:

```
Step 1: Compute the noncentrality parameter
  delta = p12 - p21 = 0.20 - 0.10 = 0.10
  p_d = p12 + p21 = 0.30
  n_per_model = 90

Step 2: Compute the standardized effect
  z_effect = delta / sqrt(p_d / n_per_model)
           = 0.10 / sqrt(0.30 / 90)
           = 0.10 / sqrt(0.003333)
           = 0.10 / 0.05774
           = 1.732

Step 3: Compute power
  power = Phi(z_effect - z_{alpha/2})
        = Phi(1.732 - 1.96)
        = Phi(-0.228)
        = 0.4099
        ~ 0.41  (41%)
```

Where Phi() is the standard normal CDF. This confirms that per-model power is approximately 41% -- well below the 80% threshold for adequate power.

**Expected per-model discordant count:** b + c = p_d * n_per_model = 0.30 * 90 = 27. This is **marginally above** the asymptotic validity threshold of 25 discordant pairs. For per-model analyses, the exact binomial McNemar test should be considered alongside the asymptotic test as a sensitivity check.

**Options:**
1. **Accept reduced per-model power** and treat per-model analyses as exploratory
2. **Increase total n to ~702** (234 per model x 3 models) for 80% power per model
3. **Use the pooled CMH estimate** as the primary analysis (requires Breslow-Day non-rejection)

This is the most significant methodological concern in the current design.

---

## References

1. McNemar, Q. (1947). Note on the sampling error of the difference between correlated proportions or percentages. *Psychometrika*, 12(2), 153-157. -- **Key insight:** Original test formulation for paired binary data.

2. [McNemar's Test - Statistics LibreTexts](https://stats.libretexts.org/Bookshelves/Applied_Statistics/Mikes_Biostatistics_Book_(Dohm)/09:_Categorical_Data/9.6:_McNemar's_test) -- **Key insight:** Practical guidance on when to use exact vs. asymptotic.

3. [McNemar's test for classifier comparisons - mlxtend](https://rasbt.github.io/mlxtend/user_guide/evaluate/mcnemar/) -- **Key insight:** ML-specific implementation with exact 2x2 table structure for classifier comparison. Edwards (1948) continuity correction formula.

4. [The McNemar test for binary matched-pairs data: mid-p and asymptotic are better than exact conditional (Fagerland et al., 2013)](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-91) -- **Key insight:** Mid-p test outperforms both exact conditional and asymptotic with CC.

5. Miettinen, O. S. (1968). The matched pairs design in the case of all-or-none responses. *Biometrics*, 339-352. -- **Key insight:** Standard sample size formula for McNemar's test. Referenced by [Vienna University calculator](https://homepage.univie.ac.at/robin.ristl/samplesize.php?test=mcnemar).

6. Connor, R. J. (1987). Sample size for testing differences in proportions for the paired-sample design. *Biometrics*, 43(1), 207-211. -- **Key insight:** Improved multinomial-based approximation over Miettinen; yields n=236 for our parameters (vs. Miettinen's n=234), confirming Miettinen slightly underestimates required n. Referenced by [Stata documentation](https://www.stata.com/manuals/pss-2powerpairedproportions.pdf) and [NCSS PASS documentation](https://www.ncss.com/wp-content/themes/ncss/pdf/Procedures/PASS/Tests_for_Two_Correlated_Proportions-McNemar_Test.pdf). [PubMed](https://pubmed.ncbi.nlm.nih.gov/3567305/).

7. [MedCalc Sample Size: McNemar test](https://www.medcalc.org/en/manual/sample-size-mcnemar-test.php) -- **Key insight:** Online calculator confirms n=234 for p12=0.20, p21=0.10, alpha=0.05, power=0.80. Reference: Machin D, Campbell MJ, Tan SB, Tan SH (2009). *Sample size tables for clinical studies*. 3rd ed. Chichester: Wiley-Blackwell.

8. [McNemar Test and Tests for Paired Nominal Data - R Companion](https://rcompanion.org/handbook/H_05.html) -- **Key insight:** Odds ratio is the standard effect size for McNemar; Cohen's g = P - 0.5 where P is the proportion of discordant pairs in the more frequent direction. Interpretation scale: small OR 1.22-1.86, medium 1.86-3.00, large >= 3.00.

9. [Cochran-Mantel-Haenszel Test - Handbook of Biological Statistics](http://www.biostathandbook.com/cmh.html) -- **Key insight:** CMH combines multiple 2x2 tables with common odds ratio. Breslow-Day test checks homogeneity assumption.

10. Agresti, A. (2002). *Categorical Data Analysis*. 2nd Edition. New York: John Wiley & Sons, pp. 320-332. -- **Key insight:** Authoritative textbook treatment of CMH statistics; CMH is a generalization of McNemar's test (McNemar is CMH with one pair per stratum). Covers Breslow-Day homogeneity test and common odds ratio estimation. [Wiley](https://onlinelibrary.wiley.com/doi/book/10.1002/0471249688).

11. [Testing homogeneity of stratum effects in stratified paired binary data (Tang et al., 2014)](https://pubmed.ncbi.nlm.nih.gov/24697196/) -- **Key insight:** Stratified McNemar test extends to multiple strata; tests for homogeneous stratum effects.

12. [Interrater reliability: the kappa statistic (McHugh, 2012)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3900052/) -- **Key insight:** Landis & Koch scale: 0.61-0.80 = "substantial"; McHugh recommends >= 0.60 minimum, >= 0.80 for strong. Kappa paradox: high percent agreement can coexist with low kappa at extreme base rates. PMCID: PMC3900052.

13. Dunn, O. J. (1961). Multiple comparisons among means. *Journal of the American Statistical Association*, 56(293), 52-64. DOI: [10.1080/01621459.1961.10482090](https://doi.org/10.1080/01621459.1961.10482090). -- **Key insight:** Formalized the practical application of the Bonferroni inequality to multiple comparisons; alpha_corrected = alpha / m = 0.05 / 21 = 0.00238. The foundational paper for what is now called the Bonferroni-Dunn procedure.

14. [Controlling Type I errors: Bonferroni and Benjamini-Hochberg (Statsig)](https://www.statsig.com/blog/controlling-type-i-errors-bonferroni-benjamini-hochberg) -- **Key insight:** BH-FDR controls false discovery rate rather than FWER; more powerful than Bonferroni for large numbers of tests; does not require test independence.

15. Westfall, P. H., Troendle, J. F., & Pennello, G. (2010). Multiple McNemar Tests. *Biometrics*, 66(4), 1185-1191. doi: 10.1111/j.1541-0420.2010.01408.x. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2902578/) -- **Key insight:** Discrete Bonferroni-Holm procedure for multiple McNemar tests leverages exact binomial nature for improved power over standard Bonferroni.

16. [PASS Sample Size Software: Tests for Two Correlated Proportions - McNemar Test](https://www.ncss.com/wp-content/themes/ncss/pdf/Procedures/PASS/Tests_for_Two_Correlated_Proportions-McNemar_Test.pdf) -- **Key insight:** Comprehensive reference for multiple sample size formulas (Miettinen, Connor, Fleiss variants).

17. [Stata: Power analysis for paired proportions test](https://www.stata.com/manuals/pss-2powerpairedproportions.pdf) -- **Key insight:** Stata implementation of McNemar power analysis with multiple formula variants; documents Connor (1987) formula implementation.

18. Kuebler, J., Budhathoki, K., Kleindessner, M., Zhou, X., Yin, J., Khetan, A., & Karypis, G. (2025). When LLMs get significantly worse: A statistical approach to detect model degradations. *ICLR 2026*. [arXiv:2602.10144](https://arxiv.org/abs/2602.10144). -- **Key insight:** Uses exact one-sided McNemar test for per-sample LLM degradation detection; demonstrates that McNemar's test can detect accuracy drops as small as 0.3% by comparing model scores at the instance level rather than aggregated task level. Directly validates our per-instance paired design.

19. Vishwanath, K., Ghosh, M., Alyakin, A., Alber, D. A., Aphinyanaphongs, Y., & Oermann, E. K. (2025). Generalist Large Language Models Outperform Clinical Tools on Medical Benchmarks. [arXiv:2512.01191](https://arxiv.org/abs/2512.01191). -- **Key insight:** Uses pairwise exact McNemar's tests for statistical significance when comparing generalist LLMs versus clinical AI tools on medical benchmarks. Validates McNemar as the standard test for paired LLM comparison.

20. Schoenfeld, D. A. (1980). Statistical considerations for pilot studies. *International Journal of Radiation Oncology, Biology, Physics*, 6(3), 371-374. DOI: [10.1016/0360-3016(80)90153-4](https://doi.org/10.1016/0360-3016(80)90153-4). [PubMed: 7390914](https://pubmed.ncbi.nlm.nih.gov/7390914/). -- **Key insight:** Simplified sample size approximation for paired proportions; yields n=236 for our parameters, consistent with Connor (1987).

21. [Breslow-Day Test implementations] -- Python: `statsmodels.stats.contingency_tables.StratifiedTable` ([statsmodels docs](https://www.statsmodels.org/stable/contingency_tables.html)); R: `DescTools::BreslowDayTest()` ([DescTools docs](https://andrisignorell.github.io/DescTools/reference/BreslowDayTest.html)). -- **Key insight:** Breslow-Day tests whether data are consistent with a common odds ratio across strata. The Python implementation reports this as "Test constant OR" in the `summary()` output.

22. Fleiss, J. L., Cohen, J., & Everitt, B. S. (1969). Large sample standard errors of kappa and weighted kappa. *Psychological Bulletin*, 72(5), 323-327. -- **Key insight:** Foundational formula for the asymptotic standard error of Cohen's kappa, enabling confidence interval construction. At small n (e.g., n=27), bootstrap or Fisher z-transformation CIs may be more accurate than the asymptotic normal approximation. [PsycNet](https://psycnet.apa.org/record/1970-01528-001).

---

## PS Integration

- **PS ID:** PROJ-014
- **Entry ID:** TASK-025
- **Artifact:** `projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/phase-0-design/methodology-research.md`
- **Orchestration:** `projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/ORCHESTRATION_PLAN.md`
- **Confidence:** HIGH (0.88) -- all core claims verified against multiple independent sources; sample size discrepancy identified and characterized; per-model power derivation shown; LLM-specific precedent established
- **Sources count:** 22
- **Iteration:** 2 (revision addressing adversary gate findings)
- **Gaps identified:**
  - Connor (1987) cited via secondary sources (Stata docs, NCSS PASS docs); n=236 figure consistent across these sources but original paper not directly accessed
  - No LLM-specific papers found using McNemar's test specifically for prompt framing comparison -- the closest precedents are model degradation detection (Kuebler et al.) and model comparison on benchmarks (Vishwanath et al.)
  - Kappa CI estimate at n=27 is approximate; exact CI depends on base rate distribution which is unknown pre-experiment

---

## Revision History

### Iteration 2 (2026-03-01)

**Trigger:** Adversary gate score 0.8985 (REVISE) against C4 threshold of 0.95.

**Findings addressed:**

| # | Finding | Resolution |
|---|---------|------------|
| 1 | Schoenfeld (1980) missing from references | Added as reference [20] with full citation: Schoenfeld DA (1980), Int J Radiation Oncology Biol Phys, 6(3), 371-374. PubMed ID and DOI included. |
| 2 | 41% per-model power claim lacks shown derivation | Added full step-by-step derivation in "Per-Model Power Derivation" subsection under Critical Warning. Shows: delta/sqrt(p_d/n) = 0.10/sqrt(0.30/90) = 1.732; power = Phi(1.732-1.96) = Phi(-0.228) = 0.41. Also noted in L0 executive summary. |
| 3 | Two Wikipedia sources (refs 10, 13) | Replaced ref 10 (CMH Wikipedia) with Agresti (2002) Categorical Data Analysis, 2nd ed., pp. 320-332, Wiley. Replaced ref 13 (Bonferroni Wikipedia) with Dunn (1961) JASA, 56(293), 52-64 -- the original formalization of the Bonferroni correction for multiple comparisons. |
| 4 | Connor (1987) is secondhand only | Connor's n=236 was already in the formula comparison table. Added explicit note in RQ2 documenting: (a) n=236 is confirmed across Stata docs [17] and NCSS PASS docs [16], (b) why original paper was not directly accessed (secondhand limitation), (c) the n=236 figure is consistent across secondary sources. Updated reference [6] with expanded key insight including n=236. |
| 5 | Search for LLM-specific McNemar papers | Added "LLM-Specific McNemar Search" subsection in Methodology documenting search terms and results. Found 2 relevant papers: Kuebler et al. (2025) ICLR 2026 [18] and Vishwanath et al. (2025) [19]. Added to references, RQ1 citation chain, and L0 summary. Documented null result for prompt-framing-specific McNemar papers. |
| 6 | Add expected Cohen's g under design assumptions | Added "Expected Cohen's g Calculation" subsection in RQ3 with full derivation: P = 0.20/0.30 = 0.667, g = 0.167 (medium per Cohen's conventions). Added interpretation linking g to the 2:1 discordant pair ratio. Added to L0 summary. |
| 7 | Consolidate effect size formulas into one table | Created "Consolidated Effect Size Table" in RQ3 with OR, risk difference, Cohen's g, and p_d -- all with design values, interpretation scales, and conventions. Added "Breslow-Day Implementation Note" with Python (statsmodels) and R (DescTools) implementations and p < 0.10 decision threshold. Added reference [21]. |
| 8 | Add kappa CI estimate at n=27 | Added CI width estimate in RQ5: SE ~ 0.10-0.14, 95% CI width ~ 0.28-0.40. Noted interpretation implications, bootstrap CI recommendation for small samples, and comparison to n=50 CI width. Added Fleiss, Cohen & Everitt (1969) as reference [22]. Added C1-C7 condition definitions reference pointing to parent design document. |

**Additional changes:**
- Updated source count from 17 to 22
- Updated confidence from 0.85 to 0.88
- Added ORCHESTRATION_PLAN.md reference in PS Integration
- Revised "LLM-as-judge with calibration" to "LLM-as-judge per rubric criteria" in RQ5 for accuracy
- Added expected per-model discordant count (27) and noted asymptotic borderline in Critical Warning
- Added Notes column to sample size formula comparison table
- Updated methodology source table to reflect new LLM evaluation papers category
- Added navigation table entry for Revision History section
