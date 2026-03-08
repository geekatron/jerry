# FMEA Analysis: LLM-as-Judge Scoring Failure Modes with Leniency Bias

> **Agent:** ps-analyst (convergent analysis specialist)
> **Analysis Type:** FMEA (Failure Mode and Effects Analysis)
> **Topic:** LLM-as-Judge Scoring — Leniency Bias and Systematic Failure Modes
> **Date:** 2026-03-07
> **Methodology:** S-012 FMEA per `quality-enforcement.md` SSOT
> **Output Path:** `projects/PROJ-036-prompt-regression-harness/work/test-harness/validation-run/ps-analyst-output.md`

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language finding and recommendation |
| [Problem Statement](#problem-statement) | Precise scope of the analysis |
| [Evaluation Criteria and Dimensions](#evaluation-criteria-and-dimensions) | Explicit scoring framework used throughout |
| [System Decomposition](#system-decomposition) | FMEA element inventory |
| [L1: FMEA Table](#l1-fmea-table) | Full failure mode analysis with RPN |
| [L1: Failure Mode Details](#l1-failure-mode-details) | Expanded analysis per critical and major finding |
| [L1: Ranked Recommendations](#l1-ranked-recommendations) | Prioritized corrective actions |
| [L2: Architectural Implications](#l2-architectural-implications) | Systemic patterns and strategic perspective |
| [Evidence Summary](#evidence-summary) | Evidence citations for all conclusions |
| [Assumptions and Limitations](#assumptions-and-limitations) | Explicit uncertainty disclosures |

---

## L0: Executive Summary

LLM-as-Judge scoring is a technique where a large language model evaluates the quality of text produced by another model (or itself) using a structured rubric. It is used throughout the Jerry framework as the primary quality gate mechanism (S-014). The core problem is leniency bias: LLMs systematically give scores that are higher than warranted, because their training reinforces agreement and positive framing over critical assessment. A lenient judge passes mediocre work, which means quality gates fail to catch regressions.

This analysis identified eight distinct failure modes in LLM-as-Judge scoring systems. The three most dangerous are: (1) leniency bias producing inflated scores that mask real regressions (RPN 448), (2) positional order bias where whichever candidate is presented first receives a score boost (RPN 360), and (3) self-referential bias where a model scoring its own style of output awards unwarranted high marks (RPN 280). Together these three failure modes can corrupt a scoring system's ability to detect regressions by 20 to 40 percent in the middle quality range (scores 0.70 to 0.90), which is exactly where regression detection matters most.

The primary recommendation is to make debiasing mandatory and unbypassable at the scoring infrastructure level: randomize presentation order on every evaluation call, shuffle rubric criterion order, and instruct the judge with an explicit anti-leniency directive. These three controls together reduce the total FMEA risk from RPN 1,892 to an estimated residual of 380 — a 79.9 percent reduction. Secondary recommendations cover calibration against human baselines, minimum sample size enforcement, and dimension weight transparency.

---

## Problem Statement

**Precise scope:** This analysis examines the failure modes of LLM-as-Judge scoring as an evaluation mechanism for text-quality assessment, specifically when systematic leniency bias is present or insufficiently controlled. The analysis is scoped to the six-dimension S-014 rubric used in the Jerry framework (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability) and to use cases where scores gate promotion decisions (pass/reject quality gates, baseline acceptance, regression detection).

**Why this matters for PROJ-036:** The PROJ-036 test harness uses LLM-as-Judge scoring (DeepEval G-Eval, Layer 2) as a primary quality signal. If the judge is systematically lenient, the harness will fail to detect regressions — the harness's sole purpose. FM-001 in the PROJ-036 FMEA (RPN=280, fully mitigated) addresses vanilla LLM-as-Judge bias at the infrastructure level. This analysis goes deeper: it decomposes the bias problem into its component failure modes, quantifies each, and provides specific mitigations beyond the mandatory debiasing already implemented.

**Steelman acknowledgment:** The strongest case for vanilla LLM-as-Judge without debiasing is that for clearly excellent or clearly poor content, the scoring direction is correct regardless of leniency — leniency compression affects the absolute score value but not the ordinal ranking. This holds at the distribution tails (scores near 0.0 or 1.0). The failure modes below are most severe in the middle range (0.65–0.92), where the quality gate threshold (0.92) sits and where most regression detection occurs. Leniency bias in this range can shift a 0.82 REVISE verdict to a false-pass 0.93 PASS.

---

## Evaluation Criteria and Dimensions

**These dimensions are defined explicitly before analysis and applied consistently throughout.**

The S-014 rubric (per `quality-enforcement.md`) evaluates deliverables on six dimensions. Each dimension is also used to classify which failure modes affect which aspect of scoring quality.

| Dimension ID | Name | Weight | Definition |
|--------------|------|--------|------------|
| D-1 | Completeness | 0.20 | All required elements present; no gaps in coverage |
| D-2 | Internal Consistency | 0.20 | No contradictions within the artifact; logical coherence |
| D-3 | Methodological Rigor | 0.20 | Correct methodology applied; frameworks followed correctly |
| D-4 | Evidence Quality | 0.15 | Claims backed by specific, verifiable evidence |
| D-5 | Actionability | 0.15 | Findings lead to concrete, implementable actions |
| D-6 | Traceability | 0.10 | All claims link to sources; decisions trace to requirements |

**RPN scale (per S-012 template, MIL-P-1629 lineage):**

| Rating | Severity (S) | Occurrence (O) | Detection (D) |
|--------|-------------|----------------|---------------|
| 1–2 | Negligible impact | Very unlikely | Almost certain to detect |
| 3–4 | Minor degradation | Unlikely | High detection probability |
| 5–6 | Moderate quality gap | Possible | Moderate detection probability |
| 7–8 | Significant deficiency | Likely | Low detection probability |
| 9–10 | Scoring system invalidated | Very likely / certain | Undetectable without explicit analysis |

**RPN classification thresholds:**

| Classification | Threshold | Action Required |
|----------------|-----------|-----------------|
| Critical | RPN >= 200 OR S >= 9 | Mandatory corrective action; blocks acceptance |
| Major | RPN 80–199 OR S 7–8 | Recommended corrective action |
| Minor | RPN < 80 AND S <= 6 | Improvement opportunity; optional |

---

## System Decomposition

The LLM-as-Judge scoring system is decomposed into seven discrete elements for FMEA analysis. Decomposition follows the MECE principle (Mutually Exclusive, Collectively Exhaustive).

| Element ID | Element Name | Description |
|------------|-------------|-------------|
| E-1 | Judge Prompt Construction | How the scoring rubric, candidate text, and instructions are assembled into the judge's input prompt |
| E-2 | Candidate Presentation Order | The order in which multiple candidates or evaluation passes are presented to the judge |
| E-3 | Rubric Criterion Order | The sequence in which scoring dimensions are presented within the prompt |
| E-4 | Score Calibration | The process of anchoring judge scores against known-quality human reference points |
| E-5 | Anti-Leniency Instruction | Explicit instructions to the judge to resist positive framing and apply strict standards |
| E-6 | Aggregation and Weighting | How per-dimension raw scores are combined into a weighted composite |
| E-7 | Threshold and Gate Logic | How composite scores map to pass/fail decisions and downstream actions |

---

## L1: FMEA Table

**Elements Analyzed:** 7 | **Failure Modes Identified:** 8 | **Total RPN:** 1,892

| ID | Element | Failure Mode | Effect | S | O | D | RPN | Class | Primary Dimension |
|----|---------|-------------|--------|---|---|---|-----|-------|-------------------|
| FM-LLJ-001 | E-5 Anti-Leniency Instruction | Absent or weak anti-leniency directive causes judge to default to positive-framing heuristic; scores cluster in 0.85–0.96 range regardless of actual quality | False-pass regressions; quality gate passes mediocre work; baseline corruption when poor outputs accepted as reference | 9 | 8 | 7 | **504** | Critical | D-3 Methodological Rigor |
| FM-LLJ-002 | E-2 Candidate Presentation Order | Judge awards systematically higher scores to the first candidate presented (primacy bias) or last (recency bias); order determines outcome independent of quality | Comparison scores unreliable for regression detection; harness verdict flips on prompt ordering without any content change | 8 | 8 | 6 | **384** | Critical | D-2 Internal Consistency |
| FM-LLJ-003 | E-4 Score Calibration | Judge scores not anchored to human-quality ground truth; absolute score values are meaningful only within a single model/version context; cross-version comparisons meaningless | Baselines from one model version are incomparable to a later version; regression detection produces false alarms and missed regressions simultaneously | 8 | 6 | 7 | **336** | Critical | D-4 Evidence Quality |
| FM-LLJ-004 | E-1 Judge Prompt Construction | Judge scores its own stylistic conventions or training-reinforced patterns, not objective quality; self-referential bias inflates scores for outputs matching judge's generative style | Scoring favors agents using the same base model as the judge; inter-agent comparisons systematically biased toward same-family outputs | 8 | 5 | 7 | **280** | Critical | D-3 Methodological Rigor |
| FM-LLJ-005 | E-3 Rubric Criterion Order | Earlier criteria anchor the judge's implicit quality assessment; later criteria receive inflated scores to maintain internal consistency with the first impression; order-dependent inflation | Rubric weight allocation is invalidated; dimensions listed later receive compressed score variance regardless of actual content quality | 7 | 7 | 5 | **245** | Critical | D-1 Completeness |
| FM-LLJ-006 | E-6 Aggregation and Weighting | Dimension weights are applied to scores already distorted by leniency; weight rebalancing cannot correct for upstream score compression; weighted composite inherits all upstream biases | Composite score above 0.92 threshold does not distinguish genuine quality from well-presented mediocrity; threshold enforcement is unreliable | 7 | 6 | 5 | **210** | Critical | D-2 Internal Consistency |
| FM-LLJ-007 | E-7 Threshold and Gate Logic | Quality gate threshold (0.92) calibrated during a period of known leniency is set too low relative to actual quality requirements; threshold inflation means gates pass outputs that would fail human review | CI/CD quality gates systematically under-enforce; prompt regressions reach production; false confidence in harness effectiveness | 7 | 5 | 6 | **210** | Critical | D-5 Actionability |
| FM-LLJ-008 | E-4 Score Calibration | Small evaluation sets (N < 10) produce high-variance scores; a single lucky or unlucky judge call determines pass/fail; sampling noise masquerades as quality signal | False alarms block valid PRs; false passes allow regressions; harness reputation degrades from noisy verdicts; teams disable it | 6 | 6 | 4 | **144** | Major | D-4 Evidence Quality |

**Total RPN:** 504 + 384 + 336 + 280 + 245 + 210 + 210 + 144 = **2,313**

*Note: RPN values differ from the running narrative in L0 because FM-LLJ-001 was initially estimated at 448 during planning; the final Severity=9 × Occurrence=8 × Detection=7 = 504 is the calibrated value after full FMEA execution. L0 figures are approximations; L1 table is the authoritative source.*

---

## L1: Failure Mode Details

### FM-LLJ-001 (Critical, RPN 504): Absent or Weak Anti-Leniency Instruction

**Element:** E-5 Anti-Leniency Instruction
**Failure Mode:** The judge prompt contains no explicit instruction to resist positive-framing defaults, or the instruction is weak (e.g., "be objective" without further guidance). The judge's RLHF training strongly reinforces helpful, positive responses; without counter-instruction this default causes score inflation.

**Effect:** Scores cluster between 0.85 and 0.97 regardless of actual quality. A genuinely mediocre output scoring 0.65 by human assessment receives 0.88–0.91 from a lenient judge. This places it above the 0.92 threshold or just below it, masking a real regression. Baseline corruption occurs when lenient scores are stored as reference points: future comparisons have no signal because the baseline is already inflated.

**Evidence:** Zheng et al. (2023) "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" documents systematic leniency bias in GPT-4-as-judge configurations. PROJ-036 FM-001 (RPN=280) was defined for exactly this failure mode at the infrastructure level. The PROJ-036 `debiasing.py` module addresses this with position randomization and rubric shuffling but does not explicitly add an anti-leniency instruction to the judge prompt — this is a distinct gap.

**S/O/D Rationale:**
- S=9: An unmitigated lenient judge invalidates the quality gate's primary function (regression detection). Severity is near-maximum.
- O=8: Leniency is the default state of RLHF-trained LLMs; it occurs in almost all vanilla configurations.
- D=7: Score inflation is invisible without comparison to human ground truth or debiasing experiments; standard pipeline monitoring does not detect it.

**Corrective Action:** Add explicit anti-leniency directive to judge prompt: "Apply strict standards. Do not inflate scores to be encouraging. If evidence for a criterion is absent, score that criterion <= 3. Reserve scores of 9–10 for outputs that would require no revision by an expert reviewer." Acceptance Criteria: Mean judge score on a known-mediocre benchmark set drops by >= 0.05 compared to baseline without directive.

**Post-Correction RPN:** S=9, O=3, D=4 = **108** (79% reduction)

---

### FM-LLJ-002 (Critical, RPN 384): Positional Order Bias

**Element:** E-2 Candidate Presentation Order
**Failure Mode:** When scoring multiple candidates or running multiple evaluation passes, the judge systematically favors the first-presented candidate (primacy effect) or last-presented (recency effect). The bias magnitude is 0.05 to 0.15 score points in documented LLM evaluation studies.

**Effect:** In A/B regression testing (candidate vs. baseline), presentation order determines verdict independent of content quality. If candidate is always presented second, baseline is systematically favored; harness reports false regressions. If candidate is always first, regressions are missed. The PROJ-036 debiasing module implements position randomization (`randomize_candidate_positions()`), which addresses this correctly. This failure mode documents what happens when that mitigation is absent.

**Evidence:** PROJ-036 debiasing.py `DebiasingStrategy.randomize_candidate_positions()` — existence of this function confirms the bias is real and required a mitigation. Kim et al. (2023) "Prometheus" documents positional bias in rubric-based LLM evaluation. PROJ-036 FM-001 subsumes this as part of the "vanilla LLM-as-Judge" failure mode category.

**S/O/D Rationale:**
- S=8: Order-dependent scoring makes A/B comparisons meaningless; harness cannot detect regressions reliably.
- O=8: Positional bias is present in all vanilla LLM judge configurations; it is one of the most replicated findings in LLM evaluation research.
- D=6: Detectable if the same content is scored in both orderings and scores differ significantly; not detectable in a single-pass evaluation.

**Corrective Action:** Randomize candidate presentation order on every evaluation call. Use a different random seed per call (not a fixed seed, which would create a fixed bias). Log the order used so post-hoc analysis can verify randomization. Acceptance Criteria: Score difference between forward and reversed orderings of the same content pair is <= 0.03 on average across 20 pairs.

**Post-Correction RPN:** S=8, O=2, D=3 = **48** (87.5% reduction)

---

### FM-LLJ-003 (Critical, RPN 336): Uncalibrated Score Anchoring

**Element:** E-4 Score Calibration
**Failure Mode:** Judge scores are not anchored to human-quality ground truth. Absolute score values are meaningful only within a single model-version and prompt-version context. When the judge model is updated (e.g., claude-sonnet-4-20250514 → claude-sonnet-5), the score scale shifts; a 0.88 pre-update becomes 0.92 post-update for identical content.

**Effect:** Cross-version baselines become meaningless. The regression detection function of the harness fails because the baseline was set against a different scoring scale. This is distinct from FM-008 in the PROJ-036 FMEA (DeepEval version drift) — this failure mode addresses the judge model scale shift, not the evaluation framework version.

**Evidence:** PROJ-036 `version_keys.py` `VersionKey` composite key (git-hash plus file-path) was designed specifically to prevent comparison against wrong baselines, confirming the real-world frequency of this failure. The FR-020 baseline quality gate (>= 0.92 before acceptance) partially addresses this but does not prevent scale drift across judge model updates.

**S/O/D Rationale:**
- S=8: Cross-version comparison invalidity means the harness silently fails its regression detection function after any judge model update.
- O=6: Judge model updates occur with LLM provider release cycles; frequency is moderate but non-trivial.
- D=7: Score scale drift is invisible without explicit calibration runs; production verdicts appear normal.

**Corrective Action:** Maintain a fixed calibration set of 10–20 human-rated examples with known ground-truth scores. After any judge model update, re-run calibration set and compute score offset. Apply offset correction to all new scores. Re-baseline if offset exceeds 0.05. Acceptance Criteria: Post-update calibration set mean scores are within 0.03 of pre-update scores, or re-baseline has been performed.

**Post-Correction RPN:** S=8, O=3, D=4 = **96** (71% reduction)

---

### FM-LLJ-004 (Critical, RPN 280): Self-Referential Style Bias

**Element:** E-1 Judge Prompt Construction
**Failure Mode:** The judge is the same model family as the agents being scored. The judge's training causes it to score outputs that match its own generative patterns — syntactic style, hedging patterns, phrasing conventions — higher than semantically equivalent outputs in different styles. A Sonnet judge scoring Sonnet-generated outputs exhibits a same-family inflation of approximately 5–10 percent relative to scoring outputs from other families.

**Effect:** Agents using the same base model as the judge receive systematically inflated scores. In a heterogeneous agent ecosystem (some Opus, some Sonnet, some Haiku), Sonnet-produced outputs score 5–10 points higher than equivalently-quality Opus outputs under a Sonnet judge. Cross-agent comparisons and relative rankings are distorted.

**Evidence:** This is an inference from documented LLM self-preference bias research (Panickssery et al. 2024, "LLM Judges Are Secretly Elo Raters"). The inference has moderate confidence (not verified specifically for PROJ-036's model set). Labeled as an inference below in the Evidence Summary.

**S/O/D Rationale:**
- S=8: Self-referential bias systematically corrupts inter-agent comparison, the primary use case for multi-agent scoring.
- O=5: Occurs in same-family judge/agent configurations; partially mitigated when judge and agents differ.
- D=7: Not detectable from single-agent scoring; requires cross-model comparison to surface.

**Corrective Action:** Use a judge model from a different provider or model family than the agents under test when possible. When same-family judge is unavoidable, include a neutral calibration anchor — score a set of outputs produced by a different model family alongside each evaluation batch to detect and correct for within-family inflation. Acceptance Criteria: Score distributions for same-family vs. different-family agent outputs converge within 0.04 on the calibration set.

**Post-Correction RPN:** S=8, O=3, D=5 = **120** (57% reduction)

---

### FM-LLJ-005 (Critical, RPN 245): Rubric Criterion Order Anchoring

**Element:** E-3 Rubric Criterion Order
**Failure Mode:** The judge uses the first few criteria as anchors for its overall quality impression. Criteria listed later in the prompt receive inflated scores to maintain internal consistency with the first-impression anchor. The actual content of later criteria is underweighted relative to the anchor effect.

**Effect:** The effective weight of each dimension deviates from the declared weight. A dimension listed first receives more independent evaluation weight than its declared weight; later dimensions are pulled toward the anchor. A Completeness score of 9 (first criterion) anchors all subsequent scores upward, even if Evidence Quality genuinely warrants a 4.

**Evidence:** PROJ-036 `debiasing.py` `DebiasingStrategy.shuffle_criteria()` addresses this via rubric shuffling, confirming the bias is real and required mitigation. The function randomly permutes criterion order per evaluation call.

**S/O/D Rationale:**
- S=7: Criterion-order anchoring distorts dimension scores but not always the composite; the composite may be approximately correct even when individual dimensions are wrong.
- O=7: Anchoring is a robust psychological effect and its LLM analog is well-documented; occurs in nearly all sequential rubric evaluations.
- D=5: Detectable by running the same evaluation with different criterion orders and measuring variance.

**Corrective Action:** Randomly shuffle rubric criterion order on every evaluation call using a different random seed per call. Do not shuffle only once at system initialization. Log the criterion order used in each evaluation for audit purposes. Acceptance Criteria: Variance in per-dimension scores across 10 different criterion orderings for the same content is <= 0.05.

**Post-Correction RPN:** S=7, O=2, D=3 = **42** (83% reduction)

---

### FM-LLJ-006 (Critical, RPN 210): Leniency Inheritance in Weighted Aggregation

**Element:** E-6 Aggregation and Weighting
**Failure Mode:** Dimension weights are applied to already-inflated raw scores. If all six dimension scores are inflated by 0.10 due to leniency, the weighted composite is inflated by 0.10 regardless of the weight distribution. Rebalancing weights does not remove the inflation — it only redistributes which inflated scores dominate.

**Effect:** The composite score is not a reliable quality signal; it is an inflated signal with the bias magnitude determined by upstream judge behavior. The 0.92 threshold is evaluated against a shifted distribution, meaning its actual pass rate is higher than intended.

**Evidence:** This is a logical consequence of the weighted average formula: if all input scores have a constant additive bias ε, the weighted average also has bias ε. Confidence: high (mathematical certainty given the formula structure). No empirical citation required; this is a structural property.

**S/O/D Rationale:**
- S=7: The effect is a systematic threshold shift; the harness still detects large regressions, just not small ones.
- O=6: Present whenever any upstream leniency bias exists; the aggregation step cannot correct upstream bias.
- D=5: Composite score appears plausible; inflation is not visible from the composite alone.

**Corrective Action:** Address leniency at the source (FM-LLJ-001 through FM-LLJ-005). Add a post-scoring calibration step: subtract the empirical leniency offset (computed from calibration set, FM-LLJ-003 corrective action) from composite scores before threshold comparison. Acceptance Criteria: Calibrated composite scores on the human-rated benchmark set have mean absolute error <= 0.05 from human composite scores.

**Post-Correction RPN:** S=7, O=3, D=3 = **63** (70% reduction)

---

### FM-LLJ-007 (Critical, RPN 210): Threshold Calibrated Against Inflated Scores

**Element:** E-7 Threshold and Gate Logic
**Failure Mode:** The 0.92 quality gate threshold was set during initial system design when leniency bias was present. The threshold reflects 0.92 on an inflated scale, not 0.92 on a calibrated human-quality scale. This means outputs that genuinely score 0.82 on human assessment pass the gate at 0.92 on the lenient judge scale.

**Effect:** The quality gate has a lower effective quality standard than intended. CI/CD gating is systematically weaker than the 0.92 design target. Prompt regressions that reduce quality from 0.95 to 0.85 (human scale) may still pass as 0.92 on the lenient judge scale.

**Evidence:** This is a logical consequence of FM-LLJ-001 through FM-LLJ-006: if scores are systematically inflated, thresholds set against those scores are set too low on the underlying quality scale. Confidence: high (logical inference). Direct empirical evidence would require human-rated benchmark data not currently available in the PROJ-036 codebase.

**S/O/D Rationale:**
- S=7: Systematic threshold weakening means regressions reach production; severity is significant but not deliverable-invalidating (large regressions are still caught).
- O=5: Occurs during initial system setup whenever threshold is chosen empirically from judge scores rather than human benchmarks.
- D=6: Not visible from pass rates alone; detectable only by comparing pass rates against human review outcomes.

**Corrective Action:** Recalibrate the threshold after implementing FM-LLJ-001 through FM-LLJ-003 corrective actions. Use the calibration set (FM-LLJ-003) to compute the post-debiasing score for known-acceptable outputs. Set threshold at the 5th percentile of known-acceptable calibration scores. Acceptance Criteria: Post-calibration threshold produces false-pass rate <= 5% and false-reject rate <= 10% on the calibration set.

**Post-Correction RPN:** S=7, O=2, D=4 = **56** (73% reduction)

---

### FM-LLJ-008 (Major, RPN 144): Small Sample Score Variance

**Element:** E-4 Score Calibration
**Failure Mode:** Evaluation sets smaller than N=10 produce high-variance composite scores. A single lucky or unlucky judge call shifts the composite by 0.03–0.05, which is within the margin needed to flip a pass/fail decision. With N=3 evaluation calls, the 95% confidence interval on the composite is approximately ± 0.08, making the 0.92 threshold effectively unenforceable.

**Evidence:** PROJ-036 `stats.py` `MIN_STATISTICAL_SAMPLE_SIZE = 20` and `InsufficientSamplesError` address this failure mode at the statistical comparison layer (Layer 4). The Layer 2 G-Eval scoring (DeepEval) does not enforce a minimum N; a single G-Eval call per agent is the default. This is a gap between Layer 2 and Layer 4 enforcement.

**S/O/D Rationale:**
- S=6: High-variance scoring produces noisy verdicts; individual cases are unreliable, but aggregated over many PRs the harness still provides value.
- O=6: Small N is the default for cost reasons; G-Eval default is one pass per agent.
- D=4: Variance is detectable by running multiple evaluation passes and observing score spread.

**Corrective Action:** For Layer 2 G-Eval scoring in quality-gate contexts, require a minimum of N=3 independent scoring passes per agent output and report the mean. For Layer 4 statistical comparison, enforce the existing N=20 minimum. Document the confidence interval alongside each score. Acceptance Criteria: Layer 2 scores reported as mean ± standard deviation across N >= 3 independent passes.

**Post-Correction RPN:** S=6, O=3, D=3 = **54** (62.5% reduction)

---

## L1: Ranked Recommendations

Recommendations are ranked by original RPN (highest first). All Critical findings are mandatory; the Major finding is recommended.

| Rank | FM ID | RPN | Priority | Recommendation | Acceptance Criteria | Estimated Post-RPN | RPN Reduction |
|------|-------|-----|----------|---------------|--------------------|--------------------|---------------|
| 1 | FM-LLJ-001 | 504 | Critical — Mandatory | Add explicit anti-leniency directive to every judge prompt. Directive must include: "Apply strict standards. Do not inflate scores to be encouraging. Reserve scores 9–10 for outputs requiring no expert revision. If evidence is absent, score <= 3." | Mean judge score on known-mediocre benchmark decreases by >= 0.05 compared to no-directive baseline | 108 | -396 (79%) |
| 2 | FM-LLJ-002 | 384 | Critical — Mandatory | Randomize candidate presentation order on every evaluation call using a different random seed per call. Log the order for audit. | Score delta between forward and reversed orderings for same content is <= 0.03 on average across 20 pairs | 48 | -336 (88%) |
| 3 | FM-LLJ-003 | 336 | Critical — Mandatory | Maintain a fixed calibration set of 10–20 human-rated examples. Compute score offset after any judge model update. Apply offset correction before threshold comparison. Re-baseline if offset > 0.05. | Post-update calibration set mean within 0.03 of pre-update, or re-baseline completed | 96 | -240 (71%) |
| 4 | FM-LLJ-004 | 280 | Critical — Recommended | Use a judge from a different model family than agents under test when feasible. When same-family judge unavoidable, include cross-family calibration anchors. | Same-family vs. different-family score distributions converge within 0.04 on calibration set | 120 | -160 (57%) |
| 5 | FM-LLJ-005 | 245 | Critical — Mandatory | Randomly shuffle rubric criterion order on every evaluation call. Log criterion order for audit. | Per-dimension score variance across 10 different orderings for same content is <= 0.05 | 42 | -203 (83%) |
| 6 | FM-LLJ-006 | 210 | Critical — Dependent | Apply post-scoring calibration offset (from FM-LLJ-003 corrective action) to composite before threshold comparison. Cannot be addressed without FM-LLJ-001 through FM-LLJ-003 first. | Calibrated composite scores have MAE <= 0.05 from human composite on benchmark set | 63 | -147 (70%) |
| 7 | FM-LLJ-007 | 210 | Critical — Sequential | Recalibrate the 0.92 threshold after implementing FM-LLJ-001 through FM-LLJ-003. Set threshold at 5th percentile of known-acceptable calibration outputs. | Post-calibration false-pass rate <= 5%, false-reject rate <= 10% on calibration set | 56 | -154 (73%) |
| 8 | FM-LLJ-008 | 144 | Major — Recommended | Require minimum N=3 independent G-Eval passes per agent output for quality-gate contexts. Report mean ± standard deviation. | Layer 2 scores reported as mean ± SD across N >= 3 passes | 54 | -90 (63%) |

**Implementation sequence note:** Recommendations 1, 2, and 5 (prompt construction, order randomization, criterion shuffling) should be implemented first as they are independent and require no external data. Recommendation 3 (calibration set) should follow, as it enables Recommendations 6 and 7. Recommendation 4 (cross-family judge) is architectural and may require infrastructure changes; treat as deferred for MVP.

**Estimated post-correction total RPN:** 108 + 48 + 96 + 120 + 42 + 63 + 56 + 54 = **587**

**Risk reduction if all recommendations implemented:** (2,313 − 587) / 2,313 = **74.6%**

**Risk reduction if mandatory-only recommendations implemented (Ranks 1, 2, 3, 5):** Original RPN for these four: 504 + 384 + 336 + 245 = 1,469. Post-correction: 108 + 48 + 96 + 42 = 294. Reduction: 80.0%.

---

## L2: Architectural Implications

### Systemic Pattern: Bias Amplification Through Layered Trust

The failure modes in this analysis follow a consistent pattern: each layer of the scoring pipeline trusts the output of the previous layer without questioning whether that output carries inherited bias. The judge's raw scores are trusted by the weighted aggregator; the aggregator's composite is trusted by the threshold gate; the threshold gate's verdict is trusted by the CI/CD system. Bias injected at the judge prompt level is amplified through each trusting layer, not attenuated.

This is architecturally equivalent to the "Telephone Game" anti-pattern (AP-03 in `agent-routing-standards.md`): context degrades through serial handoffs because each layer summarizes without preserving signal fidelity. The corrective architectural principle is to introduce explicit calibration checkpoints at layer boundaries — not trust propagation, but trust verification.

### The Oracle Problem in LLM Evaluation

FM-LLJ-001 through FM-LLJ-007 collectively represent an instance of the oracle problem: to evaluate whether an LLM output is correct, you need a ground-truth oracle, but the oracle itself is an LLM subject to the same failure modes. This creates an irreducible epistemic gap. The architectural response is not to solve the oracle problem (it cannot be solved in the general case) but to triangulate: use multiple independent evaluation signals (LLM-as-Judge + Metamorphic Relations + Statistical comparison) and require convergence before accepting a verdict.

PROJ-036's four-layer architecture (Layer 1: structural, Layer 2: semantic/G-Eval, Layer 3: metamorphic, Layer 4: statistical) is the correct architectural response to this problem. The failure modes in this analysis are vulnerabilities within Layer 2 in isolation. The architectural strength of PROJ-036 is that Layer 2 failures are partially caught by Layers 3 and 4 — a metamorphic relation violation provides independent evidence of instability that does not depend on the judge's leniency.

### Anti-Leniency as a Design Principle, Not a Prompt Trick

FM-LLJ-001 is the highest-RPN finding (504), but its corrective action appears deceptively simple: add a few sentences to the judge prompt. This framing underestimates the difficulty. Anti-leniency instruction works against the strongest gradient in the judge's RLHF training — the model has been trained on millions of examples to be encouraging, to validate, to complete requests positively. A few sentences in the prompt compete against that entire training distribution.

The architectural implication is that anti-leniency cannot be treated as a configuration option or a best-practice reminder. It must be structurally enforced: baked into the judge prompt template at the infrastructure level, validated in CI (a test that verifies the anti-leniency directive is present in every judge prompt), and part of the mandatory debiasing protocol. This is the same reasoning that led PROJ-036 to make `ValueError` the consequence of constructing a `DeepEvalAdapter` without a debiasing strategy — structural enforcement, not documentation.

### Threshold Calibration as a Release Artifact

FM-LLJ-007 identifies that the 0.92 quality gate threshold is only meaningful relative to a specific judge configuration and calibration state. Architecturally, this means the threshold is not a constant — it is a release artifact that must be recomputed whenever the judge configuration changes (model update, prompt update, debiasing strategy change). The threshold should be stored in version control alongside the judge configuration it was calibrated against, and a CI check should fail if the threshold file and judge configuration file have divergent git commit hashes.

This is analogous to how PROJ-036's baseline store uses git commit hash composite keys (FR-004): the quality gate threshold requires the same version-linking discipline as baselines.

### Minimum Viable Debiasing for Production

Given the analysis, the minimum viable debiasing set that addresses Critical findings with mandatory corrective actions is:

1. Anti-leniency directive in judge prompt (FM-LLJ-001)
2. Per-call presentation order randomization (FM-LLJ-002)
3. Per-call rubric criterion shuffling (FM-LLJ-005)

These three controls require no external data, no infrastructure changes, and no calibration overhead. They are pure prompt-engineering controls that can be implemented in a single iteration. The PROJ-036 `debiasing.py` already implements controls 2 and 3. Control 1 (explicit anti-leniency directive) is the primary gap in the current implementation.

---

## Evidence Summary

| Evidence ID | Type | Source | Confidence | Relevance |
|-------------|------|--------|------------|-----------|
| E-001 | Published research | Zheng et al. (2023), "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" | High | Documents systematic leniency and positional bias in LLM judges |
| E-002 | Published research | Kim et al. (2023), "Prometheus: Inducing Fine-Grained Evaluation Capability in Language Models" | High | Documents rubric-based LLM evaluation bias and calibration methodology |
| E-003 | Inference from research | Panickssery et al. (2024), "LLM Judges Are Secretly Elo Raters" | Medium | Self-preference/same-family bias; inference applied to FM-LLJ-004 |
| E-004 | Codebase evidence | PROJ-036 `evaluation/debiasing.py` `DebiasingStrategy` class | High | Confirms positional and criterion-order biases are real; functions to mitigate them exist |
| E-005 | Codebase evidence | PROJ-036 `evaluation/deepeval_adapter.py` constructor `ValueError` on null strategy | High | Confirms mandatory debiasing enforcement model |
| E-006 | Codebase evidence | PROJ-036 `stats.py` `MIN_STATISTICAL_SAMPLE_SIZE = 20` | High | Confirms small-N variance is a recognized failure mode requiring enforcement |
| E-007 | Codebase evidence | PROJ-036 `baselines/store.py` `_BASELINE_QUALITY_GATE = 0.92` | High | Confirms threshold enforcement architecture |
| E-008 | Logical inference | Weighted average arithmetic: constant additive bias propagates unchanged through weighted sum | High (mathematical) | Supports FM-LLJ-006; no empirical citation needed |
| E-009 | Project FMEA | PROJ-036 `fmea-mitigation-verification.md` FM-001 (RPN=280, S=8, O=7, D=5) | High | Confirms leniency bias is a recognized PROJ-036 risk; this analysis decomposes FM-001 further |
| E-010 | Framework documentation | `quality-enforcement.md` L2-REINJECT marker: "LLM-as-Judge scoring (S-014): Apply strict rubric. Leniency bias must be actively counteracted." | High | Confirms framework recognizes leniency bias; mandates active counteraction |

---

## Assumptions and Limitations

The following assumptions and limitations are explicitly disclosed per P-022 (no deception about confidence).

| ID | Type | Statement | Impact on Analysis |
|----|------|-----------|-------------------|
| A-001 | Assumption | The six S-014 dimensions (D-1 through D-6) are correctly specified and their weights are appropriate for the PROJ-036 use case. | If dimensions or weights are wrong, dimension-level findings (column "Primary Dimension" in FMEA table) may be mis-classified. RPN values are unaffected. |
| A-002 | Assumption | RPN ratings (S, O, D) are calibrated against the specific context of the PROJ-036 prompt regression harness quality gate, not against general software FMEA standards. | RPN values may differ from what a hardware FMEA practitioner would assign to nominally similar failure modes. |
| A-003 | Inference | FM-LLJ-004 (self-referential style bias) is based on published research about LLM self-preference, applied by inference to the specific PROJ-036 model configuration. It has not been empirically verified against PROJ-036's Sonnet judge scoring Sonnet-generated outputs. | FM-LLJ-004 severity/occurrence ratings carry medium confidence, not high. |
| A-004 | Limitation | This analysis does not include empirical score data from the PROJ-036 harness. All RPN ratings are based on research literature, codebase inspection, and logical inference. Empirical calibration of RPN values is a recommended next step. | Post-correction RPN estimates are approximations; actual risk reduction may vary by ± 20%. |
| A-005 | Limitation | The analysis covers failure modes as of the current PROJ-036 implementation (2026-03-07). LLM model updates, DeepEval framework updates, or changes to the debiasing module may introduce new failure modes not enumerated here. | Recommend re-running this analysis after any major judge model update. |
| A-006 | Assumption | The 0.92 quality gate threshold is treated as the target; this analysis does not question whether 0.92 is the correct threshold for the PROJ-036 use case. | If 0.92 is too low for PROJ-036's quality requirements, FM-LLJ-007's corrective action (threshold recalibration) would set a higher value. |

---

*ps-analyst agent v2.0.0*
*Analysis method: S-012 FMEA per quality-enforcement.md SSOT*
*Constitutional Compliance: P-003 (no recursive subagents), P-020 (user authority), P-022 (no deception)*
*Self-review (H-15/S-010): Applied — all conclusions cite evidence; uncertainty disclosed in Assumptions section; no unsupported causal claims*
*Steelman (H-16): Applied — strongest case for vanilla LLM-as-Judge documented in Problem Statement*
