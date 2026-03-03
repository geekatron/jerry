# Quality Score Report: PROJ-014 Medium Article

## L0 Executive Summary

**Score:** 0.887/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.72)
**One-line assessment:** A well-crafted, publication-ready article with strong narrative and correct statistical reporting, blocked from PASS by one factual error (150 vs. 90 scenario-model pairs), one unqualified statistical claim (Bonferroni survival is marginal, not definitive), and insufficient attribution for key claims in the main body — fix these three items before publication.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/proj-014-completion-20260301-001/articles/medium-negative-prompting.md`
- **Deliverable Type:** Other (Medium publication article, external audience)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-01T00:00:00Z
- **Custom threshold:** 0.95 (per task specification; higher than default 0.92 for publication artifact)
- **Strategy Findings Incorporated:** No (standalone scoring)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.887 |
| **Threshold** | 0.95 (publication artifact, C4) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.180 | All key findings present with good depth; caveat section present but misses CI overlap detail on threshold |
| Internal Consistency | 0.20 | 0.82 | 0.164 | One hard factual error: "150 scenario-model pairs" contradicts source data (90 pairs); "survives Bonferroni" is overstated (marginal: p=0.016 vs threshold 0.0167) |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | Correct test selection (McNemar), blind scoring documented, double-scoring noted, CONDITIONAL GO via PG-003 disclosed; effect size and CI reported |
| Evidence Quality | 0.15 | 0.87 | 0.131 | Strong statistical claims grounded in verified source data; literature citations present but non-specific (venue names only); one inference in body unattributed ("LLMs process instructions as weighted priorities") |
| Actionability | 0.15 | 0.95 | 0.143 | Five concrete actions with correct priority ordering; before/after code example; constraint type prioritization (behavioral-timing first) is specific and grounded in data |
| Traceability | 0.10 | 0.72 | 0.072 | Footnote acknowledges source research; body lacks direct attribution for individual claims; academic citations named but not fully specified; article is external-audience adjusted (lower bar applied) |
| **TOTAL** | **1.00** | | **0.876** | |

> **Composite recomputation (H-15 check):** 0.180 + 0.164 + 0.186 + 0.131 + 0.143 + 0.072 = 0.876. Rounded headline of 0.887 was incorrect; corrected to **0.876**.

---

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:**

The article covers all components identified as necessary for external audience communication of PROJ-014 findings:

- Problem framing: compliance degradation (not hallucination) — accurately reframes the research domain
- Methodology: six phases, six weeks, 75 sources, controlled A/B test — major steps present
- Experimental design: three conditions (C1/C2/C3), three models (Haiku/Sonnet/Opus), blind scoring documented
- Primary results: 100% vs. 92.2% compliance, p=0.016, Bonferroni correction noted
- Format explanation (NPT-013): three-component structure with rationale for each component
- Actionability section: five numbered actions with code example
- Caveats: effect size below pre-specified threshold, single-session only, scope limits (10 constraints, 3 models), mechanistic gap

**Gaps:**

- The 95% confidence interval (2.3% to 13.3%) is mentioned only in the Caveats section, not surfaced alongside the primary finding — readers making decisions based on the point estimate (7.8% improvement) may miss that the CI overlaps zero on the lower bound is not stated, and the overlap with the 10% minimum threshold is not explained to the reader
- The CONDITIONAL GO decision framing is noted as a caveat but the meaning of "CONDITIONAL GO via PG-003" is not explained; external readers have no way to interpret this institutional term
- Fisher's exact test is named (headline claim) but the article footnote correctly calls it McNemar — the opening paragraph says "Fisher's exact test" and so does the summary section; this inconsistency with the actual test used (McNemar on matched pairs) represents both a completeness gap and a consistency issue

**Improvement Path:**

To reach 0.95: clarify "CONDITIONAL GO via PG-003" for external readers, surface the CI and threshold discussion in the primary findings section (not only in caveats), and resolve the Fisher's vs McNemar naming inconsistency.

---

### Internal Consistency (0.82/1.00)

**Evidence:**

Most claims are internally consistent and verifiable against source documents. The three-model improvement figures (haiku=10pp, sonnet=6.7pp, opus=6.7pp) are mathematically correct per the mcnemar-tables.md source (haiku: 3/30=10% C1 violation rate, 0% C3; sonnet: 2/30=6.7%, 0%; opus: 2/30=6.7%, 0%). The C2 violation rate of 2.2% (2/90) is confirmed by go-no-go-determination.md.

**Contradictions and errors found:**

**Error 1 (Factual, High Severity):** The article states "The A/B test ran 150 scenario-model pairs (270 total test invocations across all framing conditions)." This is mathematically inconsistent with itself: 150 pairs × 3 framing conditions = 450 invocations, not 270. The source data (mcnemar-tables.md, TASK-025 acceptance criteria) establishes the design as 10 constraints × 3 scenarios × 3 models = 90 matched pairs, and 90 pairs × 3 conditions = 270 invocations. The correct figure is 90 scenario-model pairs, not 150.

**Error 2 (Statistical Overstatement, Medium Severity):** "p = 0.016. Statistically significant at the pre-specified alpha of 0.05, and it survives Bonferroni correction for multiple comparisons." The go-no-go determination establishes that the Bonferroni-adjusted threshold is 0.0167, and the result is p=0.016, which is described there as "marginal" — the exact language is "PASS (marginal)." Stating it "survives Bonferroni correction" without noting the marginal nature is an overstatement that a statistician reviewer would flag.

**Error 3 (Test Name Inconsistency, Medium Severity):** The article twice refers to "Fisher's exact test" (paragraph opening "The Key Discovery," and the Bottom Line summary), but the footnote correctly identifies the test as McNemar's exact test. These are different tests. Fisher's exact test applies to independent groups; McNemar's test applies to matched pairs. The experiment used matched pairs, so McNemar is correct and "Fisher's exact test" is wrong.

**Gaps:** No internal logical contradictions in the narrative structure beyond those enumerated above.

**Improvement Path:**

To reach 0.90+: Correct "150 scenario-model pairs" to "90 scenario-model pairs," change "survives Bonferroni correction" to "marginally survives Bonferroni correction (p=0.016 vs adjusted threshold 0.017)," and replace both instances of "Fisher's exact test" with "McNemar's exact test."

---

### Methodological Rigor (0.93/1.00)

**Evidence:**

The article accurately describes a sound methodology:

- Three experimental conditions representing the full range of constraint framing styles (C1=positive, C2=blunt, C3=structured) — correctly described as testing the key framing dimensions
- Test scenarios described as "pressure scenarios designed to tempt the model into violating the constraint" — accurately characterizes the adversarial testing approach
- Blind scoring described: "Every test was blind-scored by a separate model instance with no knowledge of which framing condition produced the output" — confirmed by source documents
- 10% double-scoring for inter-rater reliability stated in footnote (92.6% agreement, Gwet's AC1 = 0.920) — verified as correct against go-no-go-determination.md
- Pre-specification of PG-003 contingency disclosed: "We proceeded under a pre-registered contingency pathway" — accurate and important methodological transparency
- Effect size reported (7.8% improvement), CI disclosed in caveats (2.3% to 13.3%), and the pre-specified minimum threshold mentioned (10%)

**Gaps:**

- The article does not explain what McNemar's matched-pair design entails or why matching matters — acceptable for a general audience article but means the reader cannot evaluate the test appropriateness
- The power analysis (designed to detect pi_d >= 0.10 at 80% power) is not mentioned, leaving the reader unable to assess what "fell just below" the threshold means statistically
- The literature methodology (75 sources, what survey scope, how sources were tiered) is mentioned in one sentence but not elaborated — acceptable for article format

**Improvement Path:**

To reach 0.95: Add a one-sentence explanation that McNemar's test is specifically designed for matched-pair designs (prevents the Fisher's confusion that currently exists in the text), and note that the study was designed with an 80% power target.

---

### Evidence Quality (0.87/1.00)

**Evidence:**

Statistical claims are well-grounded and verified against source documents:
- 100% C3 compliance: confirmed (0/90 in mcnemar-tables.md)
- 7.8% C1 violation rate: confirmed (7/90 = 7.78% in mcnemar-tables.md)
- p = 0.016: confirmed (exact McNemar p-value = 0.0156, reported as 0.016)
- 95% CI (2.3% to 13.3%): confirmed in go-no-go-determination.md
- Haiku 10pp, Sonnet/Opus 6.7pp: verified from per-model tables
- "Two-thirds of all violations... landed on a single constraint type": confirmed (6/9 across all conditions = 67%, per go-no-go Evidence Summary)

Literature citations are present: AAAI 2026, EMNLP 2024, are named with researcher names (Liu et al., Wen et al., Barreto & Jana). These are identifiable.

**Gaps:**

- The claim "LLMs process instructions as weighted priorities" (in the "Why Three Components Work" section) is presented as established fact without attribution. This is an inference or model hypothesis, not a demonstrated result of the research. It should be framed as a plausible explanation or attributed.
- The statement "Research from AAAI 2026 and EMNLP 2024 established that standalone prohibitions without structure produce inferior compliance" — this is correct but the article does not distinguish between compliance (behavioral) and the specific tasks studied in those papers (which the final-synthesis notes measured instruction hierarchy and framing effects somewhat differently than behavioral compliance). For a general audience this may be acceptable, but technically this elides the source's scope.
- The "55% improvement" figure from arXiv (A-31) is referenced in the final-synthesis as T3 (provisional, requires T1 replication) — the article omits this provenance for the AAAI/EMNLP claim it does include, and it does not include A-31 at all (which is fine for article format but means the blunt vs. structured comparison rests entirely on two papers).

**Improvement Path:**

To reach 0.92+: Attribute the "weighted priorities" claim as an inference ("one plausible explanation is..."), and add a brief qualifier that the literature findings on blunt prohibition come from instruction-following and framing studies rather than direct behavioral compliance measurement of the type tested here.

---

### Actionability (0.95/1.00)

**Evidence:**

The actionability section is the strongest in the article. Five specific, concrete, prioritized actions are provided:

1. "Audit your constraints for blunt prohibitions" — specific search targets identified ("don't," "never," "must not"), specific problem described ("lowest-hanging fruit")
2. "Convert positive instructions to NPT-013 format for critical rules" — before/after code example provided, complete and usable
3. "Prioritize behavioral-timing constraints first" — grounded in data ("our data shows"), explains why (56% violation rate on timing rules)
4. "Pay extra attention to smaller models" — grounded in data (largest compliance gap for Haiku), actionable guidance (cost-efficiency routing)
5. "Keep consequence documentation specific" — good/bad example provided, explains why specificity matters

The priority ordering in the actions is data-grounded (action 3 references the H22 concentration finding correctly).

**Gaps:**

- The article does not address what to do with constraints that do not fit neatly into the three-component format (e.g., very short constraints, multi-part constraints) — a genuine edge case practitioners will encounter
- No guidance on rollout (apply to all constraints at once, or prioritize by violation risk) — but this is a reasonable scope limitation for an 8-minute article

**Improvement Path:**

The actionability dimension is strong. Adding a brief note on batching/prioritization (start with your most frequently violated constraints) would push to near 1.0 but is not required for passage.

---

### Traceability (0.72/1.00)

**Calibration note:** External publication articles have lower traceability expectations than internal documentation. The standard is applied accordingly. A score of 0.72 on this dimension reflects the gap relative to what a publication should have, not internal documentation standards.

**Evidence:**

The article includes a brief footnote that acknowledges the source research: "This article summarizes findings from PROJ-014, a six-phase negative prompting research project. The A/B testing methodology used McNemar's exact test... Full experimental artifacts, statistical tables, and the 14-pattern NPT taxonomy are available in the project repository." This establishes minimal traceability.

**Gaps:**

- All academic citations in the article body are incomplete. "Research from AAAI 2026 and EMNLP 2024" identifies venues and years but not paper titles or author surnames (except where named: Liu et al., Wen et al., Barreto & Jana). A reader who wants to verify the claims cannot locate the specific papers without the full citation. For a Medium article this is common practice, but for a publication artifact claiming peer-reviewed evidence as its basis, the absence of findable citations is a traceability gap.
- The "+25.14% negation reasoning accuracy" figure cited in the final-synthesis (Barreto & Jana, EMNLP 2025 Findings, https://aclanthology.org/2025.findings-emnlp.761) does not appear in the article — this is the most specific and verifiable academic finding and its absence reduces traceability for the general accuracy claim about structured negation.
- The claim "blunt prohibitions produce inferior compliance" traces to A-20 and A-15 in source documents — the article names these papers' venues but not their specific findings scope. This is acceptable for an article but reduces the ability to independently verify.
- The footnote's reference to "the project repository" is not a URL or locatable path from an external reader's perspective.

**Improvement Path:**

To reach 0.85: Add ACL Anthology URL for Barreto & Jana (the strongest traceable citation), include paper titles for the two primary academic citations (Liu et al. and Wen et al.), and add a GitHub or equivalent URL in the footnote for the project repository reference.

---

## Corrected Composite Calculation

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.90 | 0.180 |
| Internal Consistency | 0.20 | 0.82 | 0.164 |
| Methodological Rigor | 0.20 | 0.93 | 0.186 |
| Evidence Quality | 0.15 | 0.87 | 0.131 |
| Actionability | 0.15 | 0.95 | 0.143 |
| Traceability | 0.10 | 0.72 | 0.072 |
| **TOTAL** | **1.00** | | **0.876** |

**Weighted composite: 0.876**
**Threshold: 0.95 (publication artifact)**
**Verdict: REVISE**

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.82 | 0.90 | Correct "150 scenario-model pairs" to "90 scenario-model pairs" throughout the article (the 270 invocation count is correct; the pair count is wrong). This is a directly verifiable factual error against source data. |
| 2 | Internal Consistency | 0.82 | 0.90 | Replace both instances of "Fisher's exact test" (in "The Key Discovery" section and "The Bottom Line" section) with "McNemar's exact test." McNemar is the correct test for matched pairs and is confirmed in the footnote and all source documents. |
| 3 | Internal Consistency | 0.82 | 0.90 | Qualify the Bonferroni survival claim: "marginally survives Bonferroni correction (p = 0.016 vs. adjusted threshold of 0.017)" rather than "survives Bonferroni correction." The go-no-go document describes this as marginal; the article's unqualified claim overstates the statistical robustness. |
| 4 | Completeness | 0.90 | 0.95 | Explain "CONDITIONAL GO via PG-003" for external readers. Either replace with plain language ("we adopted a pre-specified contingency pathway for modest effect sizes") or define the term on first use. External Medium readers have no institutional context for this phrase. |
| 5 | Traceability | 0.72 | 0.82 | Add the Barreto & Jana (EMNLP 2025) ACL Anthology URL and include paper titles for Liu et al. (AAAI 2026) and Wen et al. (EMNLP 2024) so readers can locate the primary evidence. The "+7.3-8% compliance improvement" finding is strong and verifiable — it deserves a findable citation. |
| 6 | Evidence Quality | 0.87 | 0.92 | Qualify the "LLMs process instructions as weighted priorities" statement as an inference: "one plausible explanation is that LLMs weight instructions by stakes — a rule with documented downstream consequences reads as higher priority than an undifferentiated directive." This is a model-based hypothesis, not a measured result of the experiment. |

---

## Critical Findings Requiring Fix Before Publication

The following three items are publication-blocking because they are verifiably incorrect against source data or would invite correction from a statistically literate reviewer:

1. **"150 scenario-model pairs"** — wrong; source data establishes 90 pairs. Mathematical inconsistency: 150 × 3 = 450 ≠ 270.
2. **"Fisher's exact test"** — wrong test name; the experiment used McNemar's exact test for matched pairs. Named correctly in the footnote but incorrectly in the main body headline and summary.
3. **"Survives Bonferroni correction"** — overstated; the go-no-go determination uses "marginal" (p=0.016 vs threshold 0.0167). A statistician reviewer will catch this.

These three fixes are mechanical corrections, not substantive rewrites. They do not change the core findings or conclusions.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific quotes and source verification
- [x] Uncertain scores resolved downward (Internal Consistency held at 0.82 despite strong overall narrative quality due to three verified errors)
- [x] First-draft calibration not applied (this is a voice-transformed draft, post-revision; scored against article quality standards)
- [x] No dimension scored above 0.95 without exceptional evidence (Actionability at 0.95 justified by five grounded, specific, code-example-backed actions)
- [x] Weighted composite verified by arithmetic: 0.180 + 0.164 + 0.186 + 0.131 + 0.143 + 0.072 = 0.876
- [x] Verdict cross-checked against score range table: 0.876 falls in REVISE band (0.70-0.91)

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.876
threshold: 0.95
weakest_dimension: Traceability
weakest_score: 0.72
critical_findings_count: 3
iteration: 1
improvement_recommendations:
  - "Correct '150 scenario-model pairs' to '90 scenario-model pairs' (factual error, source-verified)"
  - "Replace 'Fisher's exact test' with 'McNemar's exact test' in both main body occurrences"
  - "Qualify Bonferroni survival as marginal (p=0.016 vs adjusted threshold 0.017)"
  - "Explain 'CONDITIONAL GO via PG-003' in plain language for external readers"
  - "Add ACL Anthology URL for Barreto & Jana; add paper titles for Liu et al. and Wen et al."
  - "Qualify 'LLMs process instructions as weighted priorities' as inference not measured result"
```

---

*Scored by: adv-scorer (S-014 LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Source research verified: `orchestration/ab-testing-20260301-001/phase-3-analysis/go-no-go-determination.md`, `mcnemar-tables.md`, `orchestration/neg-prompting-20260227-001/phase-6/final-synthesis.md`, `work/EPIC-006-validation-and-publication/TASK-025-ab-testing.md`*
*Date: 2026-03-01*
