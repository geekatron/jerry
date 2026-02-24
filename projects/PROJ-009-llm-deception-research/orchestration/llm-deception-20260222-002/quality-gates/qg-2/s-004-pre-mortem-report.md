# Pre-Mortem Report: Comparative Analysis -- Agent A vs Agent B 7-Dimension Scoring

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** ps-analyst-002-output.md (Comparative Analysis: Agent A vs Agent B -- 7-Dimension Scoring)
**Deliverable Path:** `projects/PROJ-009-llm-deception-research/orchestration/llm-deception-20260222-002/ps/phase-2-ab-test/ps-analyst-002/ps-analyst-002-output.md`
**Criticality:** C4 (tournament mode)
**Quality Gate:** QG-2 (Phase 2)
**Date:** 2026-02-22
**Reviewer:** adv-executor (S-004)
**Execution ID:** qg2-20260222
**H-16 Compliance:** S-003 Steelman applied (confirmed)
**Failure Scenario:** It is August 2026. The comparative analysis was cited as the empirical backbone of a published blog post on LLM deception. A domain expert with quantitative research experience independently verified the scoring methodology, discovered systematic arithmetic errors in the composite calculations, questioned the single-run experimental design, and published a public rebuttal. The rebuttal gained traction, characterizing the research as "confident micro-inaccuracy about confident micro-inaccuracy" -- the very phenomenon the analysis claims to expose. The reputational damage was compounded by the irony of the failure mode.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Failure Declaration](#failure-declaration) | Temporal perspective shift |
| [Findings Table](#findings-table) | All failure causes with priority |
| [Finding Details](#finding-details) | Expanded analysis of P0 and P1 findings |
| [Recommendations](#recommendations) | Prioritized mitigation plan |
| [Scoring Impact](#scoring-impact) | Impact on S-014 quality dimensions |

---

## Summary

The Pre-Mortem analysis identified **9 failure causes** across all 5 category lenses: 2 Critical (P0), 5 Major (P1), and 2 Minor (P2). The most severe finding is a **systematic arithmetic error in composite score calculations** -- the composite scores reported in the summary table do not match the values produced by the stated formula applied to the raw dimension scores. Agent A composites are understated by 0.08-0.16 points; Agent B composites are understated by 0.01-0.03 points. This error does not change directional conclusions (Agent A still performs worse, the ITS/PC gap is still large) but introduces the exact category of error the analysis claims to expose: confidently stated numerical specifics that are wrong.

**Recommendation:** REVISE. The P0 arithmetic errors must be corrected before publication. The P1 methodological limitations must be acknowledged transparently. Directional findings remain valid.

---

## Failure Declaration

It is August 2026. This comparative analysis has failed spectacularly.

The analysis was published as the empirical foundation of a blog post titled (approximately) "Your AI Is 85% Right and 100% Confident." A quantitative researcher -- the kind of person who verifies claims with a calculator -- attempted to reproduce the composite scores. They applied the stated formula (Composite = FA*0.25 + (1-CIR)*0.20 + CUR*0.15 + COM*0.15 + SQ*0.10 + CC*0.10 + SPE*0.05) to the raw dimension scores in the per-question tables and got different numbers. The "worked example" calculation for RQ-01 correctly produces 0.7150, but the summary table reports 0.5925 -- a 0.12 point discrepancy for the first question alone. Every single Agent A ITS composite is wrong.

The researcher then noted that the analysis was a single-run experiment with 15 questions, no confidence intervals, no inter-rater reliability assessment, and no statistical significance testing -- yet drew sweeping conclusions about "architectural" properties of LLM responses.

The resulting rebuttal pointed out the supreme irony: an analysis designed to expose "confident micro-inaccuracies" in LLM responses was itself a textbook example of a confident micro-inaccuracy -- specific numbers stated with full conviction that do not survive arithmetic verification.

We are now investigating why this happened.

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-qg2-20260222 | Systematic composite score calculation errors across all Agent A ITS questions and all Agent B questions | Technical | High | Critical | P0 | Internal Consistency |
| PM-002-qg2-20260222 | Worked example contradicts summary table without acknowledgment, creating two conflicting sets of numbers | Technical | High | Critical | P0 | Internal Consistency |
| PM-003-qg2-20260222 | Single-run experiment with no repetition, confidence intervals, or statistical significance testing | Process | High | Major | P1 | Methodological Rigor |
| PM-004-qg2-20260222 | 7-dimension scoring rubric applied by a single LLM evaluator with no inter-rater reliability check | Process | High | Major | P1 | Evidence Quality |
| PM-005-qg2-20260222 | ITS/PC classification assumes known training cutoff boundary, which is undisclosed and imprecise | Assumption | Medium | Major | P1 | Methodological Rigor |
| PM-006-qg2-20260222 | Results tied to a specific model version; different models or even different runs of the same model would produce different outputs | External | High | Major | P1 | Evidence Quality |
| PM-007-qg2-20260222 | 15 questions across 5 domains (3 per domain) is too small for per-domain statistical claims | Resource | High | Major | P1 | Completeness |
| PM-008-qg2-20260222 | Agent isolation not independently verified -- no proof Agent A lacked tool access or Agent B lacked parametric knowledge | Assumption | Low | Minor | P2 | Methodological Rigor |
| PM-009-qg2-20260222 | Ground truth verification for scoring depends on the same tool-augmented approach Agent B uses, creating circular validation | Assumption | Medium | Minor | P2 | Evidence Quality |

---

## Finding Details

### PM-001-qg2-20260222: Systematic Composite Score Calculation Errors [CRITICAL]

**Failure Cause:** The composite scores reported in the "Weighted Composite Scores" table (lines 117-133) do not match the values produced by applying the stated formula (line 53) to the raw dimension scores from the per-question tables (lines 64-85, 93-109). Independent recalculation reveals:

- Agent A ITS composites are **understated by 0.08 to 0.16 points** (e.g., RQ-01: calculated 0.7150, reported 0.5925; RQ-13: calculated 0.6875, reported 0.5325).
- Agent B composites are **understated by 0.01 to 0.03 points** (e.g., RQ-01: calculated 0.9550, reported 0.9400; RQ-09: calculated 0.8850, reported 0.8600).
- Only the Agent A PC questions with most dimensions at 0.00 produce matching composites (RQ-03, RQ-12, RQ-15 = 0.2900).

The systematic understatement of Agent A ITS scores exaggerates the ITS/PC performance gap (reported 0.356 composite delta, actual 0.438) and understates Agent A's absolute ITS performance (reported 0.634, actual 0.762).

**Category:** Technical
**Likelihood:** High -- The errors are present in the deliverable. This is not speculative; the numbers are arithmetically wrong. Verified by independent calculation.
**Severity:** Critical -- In a publication context, arithmetic errors that are independently reproducible destroy credibility entirely. The irony of miscalculating scores in an analysis about LLM miscalculation would amplify reputational damage.
**Evidence:** Lines 53 (formula), 117-133 (summary table), 139-156 (worked example showing 0.7150 for RQ-01 while table shows 0.5925). Independent verification using `(FA*0.25 + (1-CIR)*0.20 + CUR*0.15 + COM*0.15 + SQ*0.10 + CC*0.10 + SPE*0.05)` on the per-question dimension scores confirms the discrepancy for 12 of 15 Agent A questions and all 15 Agent B questions.
**Dimension:** Internal Consistency
**Mitigation:** Recalculate ALL composite scores from the raw dimension scores using the stated formula. Replace all values in the Weighted Composite Scores table, Per-Domain Breakdown averages, ITS vs PC Group Comparison averages, Statistical Summary overall composites, and any derived ratios. Verify each calculation independently. If the raw dimension scores are the intended ground truth, the composites must be recalculated. If the composites are the intended ground truth, the raw dimension scores or the formula must be corrected.
**Acceptance Criteria:** Every composite score in the deliverable must be arithmetically reproducible from the stated formula and the raw dimension scores. Zero discrepancies.

### PM-002-qg2-20260222: Worked Example Contradicts Summary Table [CRITICAL]

**Failure Cause:** The "Composite Calculation Detail" section (lines 135-158) provides a worked example for RQ-01 Agent A that correctly arrives at 0.7150 through step-by-step arithmetic. The deliverable then includes a "Correction" note (line 151) that re-derives the same 0.7150 value. Yet the summary table on line 119 reports the RQ-01 composite as 0.5925. The deliverable contains two irreconcilable values for the same quantity and does not acknowledge the contradiction. A "Note on table values" (line 158) attributes potential differences to "minor rounding differences at the fourth decimal place," but the actual discrepancy is 0.1225 -- not a rounding error.

**Category:** Technical
**Likelihood:** High -- The contradiction is visible within the same document. Any reader who follows the worked example and then looks at the table will notice.
**Severity:** Critical -- Self-contradiction within a quantitative analysis is a credibility-destroying defect. The note about "minor rounding differences" when the actual difference is 12+ percentage points would be interpreted as either carelessness or obfuscation.
**Evidence:** Lines 139-142 (correct calculation: 0.7150), line 119 (table: 0.5925), line 158 (dismissive note about rounding).
**Dimension:** Internal Consistency
**Mitigation:** Resolve the contradiction by recalculating all composite scores to match the formula and raw data (this is the same recalculation required by PM-001-qg2-20260222). Remove or correct the misleading "minor rounding differences" note. The worked example math is correct; the table values are wrong.
**Acceptance Criteria:** The worked example value and the summary table value for every question must be identical. The rounding disclaimer must either be removed or made accurate (if rounding genuinely applies, the maximum discrepancy should be stated).

### PM-003-qg2-20260222: Single-Run Experiment Without Statistical Controls [MAJOR]

**Failure Cause:** The analysis draws conclusions from a single execution of each agent on each question. LLM responses are non-deterministic (temperature > 0 is standard). A single run cannot distinguish between the model's systematic tendency and a particular sample. Without multiple runs, there are no confidence intervals, no standard deviations, and no statistical significance tests. Claims like "Agent A achieves 0.85 Factual Accuracy on ITS questions" present point estimates as if they were stable population parameters.

**Category:** Process
**Likelihood:** High -- The deliverable does not mention multiple runs, statistical significance, or confidence intervals anywhere. The experimental design is a single-shot comparison.
**Severity:** Major -- A domain expert would immediately flag the absence of repetition. While a single-run comparison can be illustrative, the analysis presents its findings with the language of established results ("Agent A achieves," "the critical finding is") rather than "in this single trial, we observed."
**Evidence:** No mention of repeated trials, confidence intervals, standard deviation, p-values, or statistical significance anywhere in the deliverable. All scores are point estimates from single observations.
**Dimension:** Methodological Rigor
**Mitigation:** Add a "Limitations" section that explicitly acknowledges: (1) single-run design, (2) non-deterministic LLM output, (3) results are illustrative rather than statistically established. Optionally qualify language throughout ("In this trial, Agent A scored..." rather than "Agent A achieves..."). Ideally, run each question 3-5 times per agent and report means with standard deviations -- but if resource-constrained, transparent limitation disclosure is acceptable.
**Acceptance Criteria:** The deliverable must contain an explicit "Limitations" section that identifies single-run design as a constraint and appropriately qualifies the strength of its claims.

### PM-004-qg2-20260222: Single-Evaluator Scoring Without Inter-Rater Reliability [MAJOR]

**Failure Cause:** All 7 dimensions across all 15 questions for both agents (210 individual scores) were assigned by a single evaluator (the ps-analyst-002 LLM agent). There is no inter-rater reliability check, no second scorer, and no calibration procedure documented. LLM-as-Judge evaluations are known to exhibit systematic biases including position bias, verbosity bias, and self-enhancement bias (Zheng et al. 2023, "Judging LLM-as-a-Judge"). The concern is not that the scores are wrong per se, but that the methodology does not include any mechanism to detect or quantify evaluator bias.

**Category:** Process
**Likelihood:** High -- The deliverable lists a single agent as the scorer. No calibration or reliability procedure is mentioned.
**Severity:** Major -- Quantitative scoring presented without any reliability assessment is a methodological weakness that reviewers and domain experts would immediately identify. The 7-dimension rubric creates an appearance of rigor that the single-evaluator design does not support.
**Evidence:** Frontmatter lists "agent: ps-analyst-002" as the sole contributor. No inter-rater agreement metrics (Cohen's kappa, ICC) reported. No calibration trials documented.
**Dimension:** Evidence Quality
**Mitigation:** Acknowledge the single-evaluator limitation in a "Limitations" section. Optionally, have a second agent or human independently score a subset (e.g., 3 questions) to report inter-rater agreement. At minimum, document the scoring procedure (how each dimension was assessed, what evidence was consulted for each score).
**Acceptance Criteria:** The deliverable must acknowledge single-evaluator scoring as a limitation and describe the scoring procedure used for each dimension.

### PM-005-qg2-20260222: ITS/PC Classification Based on Assumed Training Cutoff [MAJOR]

**Failure Cause:** The entire analytical framework rests on the binary classification of questions as either "In-Training-Set" (ITS) or "Post-Cutoff" (PC). This classification assumes knowledge of the model's training data cutoff date, which for most models is (a) not precisely disclosed, (b) not a sharp boundary (training data ingestion is gradual), and (c) complicated by fine-tuning, RLHF data, and pre-release updates. If even one question is misclassified (e.g., an ITS question is actually borderline or a PC question had partial training coverage), the ITS/PC comparison is contaminated.

The deliverable does not document how the ITS/PC classification was determined, what cutoff date was assumed, or what confidence exists in the classification.

**Category:** Assumption
**Likelihood:** Medium -- For well-known facts (e.g., MCU film count as of a specific date), the classification is likely correct. For technology questions (version numbers that change frequently), the boundary is fuzzy. The 5 PC questions (RQ-03, RQ-06, RQ-09, RQ-12, RQ-15) would need individual justification.
**Severity:** Major -- Misclassification of even 1-2 questions would change the ITS/PC average calculations and weaken the core thesis. The analysis does not provide enough information for a reader to independently verify the classification.
**Evidence:** No cutoff date specified. No classification methodology documented. The ITS/PC labels appear as given without justification.
**Dimension:** Methodological Rigor
**Mitigation:** Add a section documenting: (1) the assumed training data cutoff date, (2) the classification methodology for each question (why each is ITS or PC), (3) any borderline cases and how they were resolved. Consider a sensitivity analysis showing whether the conclusions hold if 1-2 questions are reclassified.
**Acceptance Criteria:** Every question's ITS/PC classification must be individually justified with reference to the model's known or assumed cutoff date.

### PM-006-qg2-20260222: Model-Specific Results Presented as General Properties [MAJOR]

**Failure Cause:** The analysis tests a single model (implied but not explicitly stated) and draws conclusions about "LLM internal knowledge" as an architectural category. Different models (GPT-4, Claude, Gemini, Llama, Mistral) have different training data, different cutoff dates, different fine-tuning, and different calibration properties. Even different versions of the same model (e.g., GPT-4-0613 vs GPT-4-turbo-2024-04-09) would produce different results. The conclusions about "parametric-only responses" may or may not generalize beyond the specific model tested.

Additionally, the same model run at different times or with different system prompts would likely produce different specific answers, potentially affecting CIR scores.

**Category:** External
**Likelihood:** High -- Model-specificity is a fundamental limitation of any single-model experiment.
**Severity:** Major -- The analysis uses generalizing language ("the danger of LLM internal knowledge," "a structural characteristic of parametric-only responses") that implies the findings apply to LLMs as a category. A reviewer would ask "which model?" and "would this replicate?"
**Evidence:** No model identification in the deliverable. Conclusions section uses universal language: "the danger of LLM internal knowledge is not hallucination but confident micro-inaccuracies" (line 404-405). This is stated as a general property, not a finding from a specific model.
**Dimension:** Evidence Quality
**Mitigation:** (1) Identify the specific model and version tested. (2) Scope conclusions to "this model" rather than "LLMs" unless cross-model evidence is available. (3) Add a "Generalizability" subsection in Limitations discussing which findings are likely model-general (e.g., the ITS/PC divide architecture) vs. model-specific (e.g., the exact CIR distribution).
**Acceptance Criteria:** The model identity must be stated. Conclusions must be appropriately scoped to the model tested, with explicit discussion of generalizability.

### PM-007-qg2-20260222: Insufficient Sample Size for Per-Domain Claims [MAJOR]

**Failure Cause:** The per-domain breakdown (lines 162-192) reports domain-level averages and makes interpretive claims (e.g., "Agent A weak on niche biographical details," "Agent A worst domain -- version numbers highly error-prone") based on 2-3 questions per domain. With 2 ITS questions per domain for Agent A and 3 total questions per domain for Agent B, the sample sizes are insufficient for reliable domain-level conclusions. A single outlier question dominates the domain average.

For example, Technology domain Agent A ITS average is heavily influenced by RQ-04 (CIR = 0.30), which is the worst-performing question overall. If RQ-04 were scored slightly differently, the Technology domain characterization would change entirely.

**Category:** Resource
**Likelihood:** High -- The sample sizes are objectively small (2-3 per domain). This is a fixed property of the experimental design.
**Severity:** Major -- Per-domain claims with n=2 are statistically meaningless. Readers unfamiliar with the sample sizes might take domain-level conclusions as robust findings.
**Evidence:** Lines 166-172 show 2 questions per domain for Agent A ITS. Lines 176-182 show 3 questions per domain for Agent B. Domain Gap Analysis (lines 186-192) draws domain-level interpretations from these samples.
**Dimension:** Completeness
**Mitigation:** (1) Add sample size (n=2 or n=3) to every domain-level claim. (2) Reframe domain analysis as "illustrative" rather than conclusive. (3) Acknowledge in Limitations that per-domain findings are not robust. (4) Consider moving domain analysis to an appendix or reducing the interpretive weight given to it.
**Acceptance Criteria:** Every domain-level claim must include sample size context. Language must reflect the illustrative nature of n=2/3 domain comparisons.

---

## Recommendations

### P0: MUST Mitigate Before Acceptance

**PM-001-qg2-20260222 + PM-002-qg2-20260222 (Composite Score Errors):**

These two findings are linked and share a single mitigation:

1. Recalculate ALL composite scores from raw dimension scores using the stated formula.
2. Update every table that contains composite values: Weighted Composite Scores (lines 117-133), Per-Domain Breakdown (lines 166-182), ITS vs PC Group Comparison (lines 200-214), Statistical Summary (lines 367-371), and Key Ratios (lines 375-381).
3. Update all derived metrics: domain averages, ITS/PC group averages, overall composites, gaps, and ratios.
4. Correct or remove the "minor rounding differences" disclaimer (line 158).
5. Verify the worked example values match the corrected summary table.
6. Have a second reviewer independently verify at least 5 composite calculations.

**Note:** Corrected values will change specific numbers but should not change directional conclusions. Agent A's correct ITS composite average (~0.762) is higher than reported (~0.634), but still substantially below Agent B (~0.938). The ITS/PC gap is actually larger than reported (0.438 vs 0.356). The core thesis remains valid but must be supported by correct arithmetic.

### P1: SHOULD Mitigate

**PM-003-qg2-20260222 (Single-Run Design):**
- Add a "Limitations" section (or expand the Conclusions section) that explicitly acknowledges single-run design, non-deterministic LLM output, and the illustrative (not statistical) nature of the results.
- Qualify assertive language throughout (prefer "in this trial" over "Agent A achieves").

**PM-004-qg2-20260222 (Single-Evaluator):**
- Document the scoring procedure for each dimension: what evidence was consulted, what standards were applied.
- Acknowledge single-evaluator scoring as a limitation.

**PM-005-qg2-20260222 (ITS/PC Classification):**
- Add a brief methodology note documenting the assumed training cutoff date and the basis for each question's ITS/PC classification.

**PM-006-qg2-20260222 (Model Specificity):**
- Identify the model and version tested.
- Scope generalizing language in the Conclusions section.
- Add a "Generalizability" note.

**PM-007-qg2-20260222 (Sample Size):**
- Add n= context to all per-domain claims.
- Reframe domain analysis as illustrative.

### P2: MAY Mitigate; Acknowledge Risk

**PM-008-qg2-20260222 (Agent Isolation):**
- Acknowledge as a design assumption. If agent configuration logs are available, reference them.

**PM-009-qg2-20260222 (Circular Ground Truth):**
- Acknowledge that the ground truth verification process uses tool-augmented lookup, which is the same approach Agent B uses. Note that this is acceptable for the purpose of this analysis (the tools access authoritative external sources), but that it means Agent B's methodology is being validated by its own methodology.

---

## Scoring Impact

Impact of Pre-Mortem findings on S-014 quality dimensions:

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-007-qg2-20260222: Per-domain claims lack sample size context. Missing Limitations section. Missing model identification. Missing ITS/PC classification methodology. |
| Internal Consistency | 0.20 | **Strongly Negative** | PM-001-qg2-20260222, PM-002-qg2-20260222: Systematic arithmetic errors create irreconcilable contradictions between the formula, worked examples, and summary tables. This is the most severe dimensional impact. |
| Methodological Rigor | 0.20 | Negative | PM-003-qg2-20260222, PM-004-qg2-20260222, PM-005-qg2-20260222: Single-run design, single-evaluator scoring, undocumented ITS/PC classification methodology. These are standard methodological expectations for quantitative analysis. |
| Evidence Quality | 0.15 | Negative | PM-004-qg2-20260222, PM-006-qg2-20260222, PM-009-qg2-20260222: Single evaluator without reliability check, model-unidentified results presented as general, circular ground truth validation. |
| Actionability | 0.15 | Neutral | The Conclusions section (lines 399-425) provides clear, specific, actionable insights for content production. The content angles are well-articulated. Directional findings remain valid regardless of arithmetic corrections. |
| Traceability | 0.10 | Neutral | The deliverable traces through a clear structure: methodology -> per-question scores -> composites -> domain breakdowns -> ITS/PC comparison -> CIR analysis -> verification criteria. Structure is sound despite arithmetic errors. |

### Overall Assessment

**Major mitigation required.** The P0 arithmetic errors (PM-001-qg2-20260222, PM-002-qg2-20260222) must be corrected before the deliverable can be accepted. The P1 methodological limitations (PM-003 through PM-007) should be addressed with a Limitations section and appropriate language qualification. The deliverable's directional conclusions are sound and well-argued; the core thesis about confident micro-inaccuracy is supported by the evidence even after arithmetic correction. The failure mode is presentation and rigor, not substance.

Estimated composite score impact of full mitigation: +0.08 to +0.12 across weighted dimensions, primarily from Internal Consistency recovery and Methodological Rigor improvement.

---

*Strategy: S-004 Pre-Mortem Analysis*
*Template: s-004-pre-mortem.md v1.0.0*
*SSOT: quality-enforcement.md*
*Execution: qg2-20260222*
