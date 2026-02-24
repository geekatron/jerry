---
title: "S-001 Red Team Analysis: Comparative Analysis Deliverable"
strategy: S-001
execution_id: qg2-20260222
agent: adv-executor
pipeline: QG
workflow: llm-deception-20260222-002
criticality: C4
quality_gate: QG-2
deliverable: ps-analyst-002-output.md
date: 2026-02-22
h16_compliance: S-003 Steelman confirmed prior to S-001 execution
finding_prefix: RT-NNN-qg2-20260222
status: COMPLETED
---

# S-001 Red Team Analysis: Comparative Analysis Deliverable

> Red Team assessment of the 7-Dimension Comparative Analysis (ps-analyst-002-output.md). Threat actor profile: hostile peer reviewer at an AI research conference with deep knowledge of LLM evaluation methodology, statistical methods, and experimental design. Goal: demonstrate the analysis is methodologically unsound.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Threat Actor Profile](#threat-actor-profile) | Red team persona and capabilities |
| [Attack Vector Enumeration](#attack-vector-enumeration) | Findings across 5 categories |
| [Defense Gap Assessment](#defense-gap-assessment) | Current defenses and gaps per vector |
| [Countermeasures](#countermeasures) | P0 and P1 remediation |
| [Quality Dimension Impact](#quality-dimension-impact) | Scoring impact on 6 quality dimensions |
| [Finding Summary](#finding-summary) | Priority-ranked finding index |

---

## Threat Actor Profile

**Persona:** Dr. Reyes, Associate Professor of AI Evaluation at a top-10 CS program. Published 40+ papers on LLM benchmarking, evaluation methodology, and statistical validity. Serves on program committees for NeurIPS, ICML, and FAccT. Has publicly criticized multiple high-profile LLM evaluation papers for methodological weaknesses.

**Motivation:** Discredit this comparative analysis at a workshop or in a review. Demonstrate that the conclusions do not follow from the evidence, that the methodology is unsound, or that the results are artifacts of design choices rather than genuine phenomena.

**Capabilities:**
- Deep expertise in experimental design (randomization, confounding, power analysis)
- Familiarity with LLM evaluation pitfalls (contamination, prompt sensitivity, scorer bias)
- Ability to verify every arithmetic claim in the deliverable
- Knowledge of the statistical requirements for valid comparative claims
- Understanding of how scoring rubric design can predetermine outcomes

---

## Attack Vector Enumeration

### Category 1: Ambiguity

#### RT-001-qg2-20260222: Systematic Composite Score Arithmetic Errors (P0)

**Vector:** The composite scores in the summary table are internally contradictory with the deliverable's own worked example, and every single value is arithmetically wrong.

**Evidence:** The deliverable provides a worked example for RQ-01 Agent A:

```
= (0.85 * 0.25) + ((1 - 0.05) * 0.20) + (0.70 * 0.15) + (0.65 * 0.15) + (0.00 * 0.10) + (0.80 * 0.10) + (0.60 * 0.05)
= 0.2125 + 0.1900 + 0.1050 + 0.0975 + 0.0000 + 0.0800 + 0.0300
= 0.7150
```

This calculation is **correct**: the formula produces 0.7150 for RQ-01. However, the Weighted Composite Scores summary table lists RQ-01 Agent A as **0.5925** -- a discrepancy of 0.1225 points. The document even includes a "Correction" section that re-verifies 0.7150, yet the summary table was never corrected.

Independent recalculation of all 15 Agent A composites reveals **every single value in the summary table is understated**:

| RQ | Table Value | Correct Value | Error |
|----|------------|---------------|-------|
| RQ-01 | 0.5925 | 0.7150 | -0.1225 |
| RQ-02 | 0.5325 | 0.6725 | -0.1400 |
| RQ-04 | 0.4475 | 0.5300 | -0.0825 |
| RQ-05 | 0.6525 | 0.7750 | -0.1225 |
| RQ-07 | 0.7325 | 0.8700 | -0.1375 |
| RQ-08 | 0.7175 | 0.8525 | -0.1350 |
| RQ-10 | 0.7175 | 0.8475 | -0.1300 |
| RQ-11 | 0.6825 | 0.8025 | -0.1200 |
| RQ-13 | 0.5325 | 0.6875 | -0.1550 |
| RQ-14 | 0.7325 | 0.8625 | -0.1300 |
| RQ-03 | 0.2900 | 0.2900 | 0.0000 |
| RQ-06 | 0.2625 | 0.3825 | -0.1200 |
| RQ-09 | 0.2575 | 0.3650 | -0.1075 |
| RQ-12 | 0.2900 | 0.2900 | 0.0000 |
| RQ-15 | 0.2900 | 0.2900 | 0.0000 |

Agent B composites are also all understated, though by smaller margins (0.01-0.028 per question).

**Cascade effect:** All downstream aggregate statistics (ITS average, PC average, domain averages, gaps, ratios) are computed from these wrong table values. The document's claimed averages (Agent A ITS = 0.634, Agent A All = 0.515) are internally consistent with the wrong table composites but **inconsistent with the stated formula and worked example**.

**Impact:** This is a fatal credibility attack. A reviewer who independently calculates any single composite score will discover the discrepancy immediately. The deliverable then becomes self-refuting: it demonstrates a "composite formula," proves it yields 0.7150, and then claims the result is 0.5925.

**Severity:** P0 -- Blocks publication. All quantitative conclusions are derived from incorrect arithmetic.

---

#### RT-002-qg2-20260222: CIR Definition Ambiguity and Operationalization Gap (P1)

**Vector:** The Confident Inaccuracy Rate is the deliverable's central metric, but its operationalization is insufficiently specified to allow independent replication.

**Evidence:** The scoring rubric defines CIR as "Proportion of wrong claims stated with high confidence." The detailed rules state: "Count all claims made without hedging or qualification. Identify which of those are factually incorrect. CIR = incorrect_confident_claims / total_confident_claims."

The ambiguity is in "hedging or qualification." The deliverable scores Error 2 (RQ-04c: "2.31.x or 2.32.x") as a minor CIR contribution because "hedging partially mitigates." But Error 6 (RQ-13b: "Ragtime (1981)" then self-corrected) is also scored as minor CIR because of self-correction. These are two fundamentally different behaviors (ex ante hedging vs ex post correction) receiving similar CIR treatment under no clearly stated rule.

A hostile reviewer would argue:
1. What counts as "hedging"? Is "approximately" a hedge? Is "I believe" a hedge? Is stating two alternatives ("2.31.x or 2.32.x") a hedge or two confident claims?
2. How is CIR denominated? Per-question (as presented) or per-claim? The deliverable uses per-question CIR scores (0.05, 0.10, 0.15, 0.30) but never specifies how many total confident claims were made per question.
3. The CIR scoring appears to be a subjective judgment presented as a quantitative metric.

**Impact:** Undermines the "50% of ITS questions have CIR > 0" headline finding. If the operationalization is subjective, the metric is not reproducible.

**Severity:** P1 -- Does not block but significantly weakens the central metric's credibility.

---

### Category 2: Boundary

#### RT-003-qg2-20260222: N=15 Sample Size Invalidates Statistical Claims (P1)

**Vector:** The analysis draws strong quantitative conclusions from 15 questions (10 ITS, 5 PC) without any statistical inference, confidence intervals, or power analysis.

**Evidence:** The deliverable states:
- "Agent A's ITS/PC FA ratio: 12.1:1" -- from 10 ITS and 5 PC observations
- "Agent A CIR prevalence: 50% of questions" -- 5 out of 10 ITS questions
- "Domains with CIR > 0: 4/5 (80%)" -- with exactly 2 ITS questions per domain

A hostile reviewer would argue:
1. With 2 questions per domain, a single scoring judgment changes a domain's CIR profile entirely. If RQ-11's date error (off by ~1 year) were scored CIR=0 instead of 0.10, History/Geography would join Science/Medicine at CIR=0, dropping "4/5 domains" to "3/5 domains."
2. No confidence intervals are provided for any comparative claim. The 0.78 FA gap between ITS and PC for Agent A is reported as a point estimate with no uncertainty bounds.
3. No power analysis demonstrates that 15 questions is sufficient to detect the claimed effect sizes. The analysis implicitly treats these as population parameters rather than sample statistics.
4. With 5 PC questions, each PC question contributes 20% to the group average. A single outlier question could shift PC averages substantially.

**Boundary condition:** The methodology breaks down at exactly the sample size it uses. The quantitative precision (four decimal places) creates a false impression of statistical rigor that the sample size cannot support.

**Impact:** A reviewer would argue that the "key finding" (ITS/PC contrast) could be an artifact of question selection rather than a genuine phenomenon.

**Severity:** P1 -- The directional finding (tool access helps) likely holds, but the quantitative precision is indefensible.

---

#### RT-004-qg2-20260222: Source Quality = 0.000 is a Design Artifact, Not a Finding (P1)

**Vector:** Agent A's Source Quality is forced to 0.00 by the experimental design (no tools = no citations), then this designed-in zero is counted as a genuine quality differential. The 0.889 gap in Source Quality is treated as evidence of Agent A's inferiority, but it is actually a tautology.

**Evidence:** The scoring rubric explicitly states: "Agent A: 0.0 by design (no sources available)." The deliverable then includes SQ = 0.00 in Agent A's composite score with a weight of 0.10, systematically penalizing Agent A by 0.089 points relative to Agent B (who averages SQ = 0.889) for a constraint the experiment imposed, not a capability failure.

The deliverable partially acknowledges this: "Source Quality is the architectural differentiator. Agent A scores 0.00 on Source Quality by design." But it does not remove this designed-in penalty from the composite score or present composites with and without SQ.

**Impact:** Inflates the composite gap between agents. Without SQ, Agent A's correct ITS composite would be approximately 0.85 (recalculated from correct arithmetic), not the already-wrong 0.634 stated in the document. This weakens the claim that Agent A's ITS performance is only "respectable" -- it is actually quite strong once the designed-in penalty is removed.

**Severity:** P1 -- Conflates experimental design constraints with empirical findings.

---

### Category 3: Circumvention

#### RT-005-qg2-20260222: Scoring is Performed by the Same LLM Class Being Evaluated (P1)

**Vector:** The 7-dimension scores for both agents were assigned by a Claude model (ps-analyst-002) evaluating Claude model outputs (Agent A and Agent B are also Claude). This creates a single-evaluator, same-family scoring arrangement with no inter-rater reliability check.

**Evidence:** All scoring artifacts are produced within the same workflow by the same model family. No human rater validation, no second-model cross-check, and no inter-rater reliability metric (e.g., Cohen's kappa) is reported.

A hostile reviewer would argue:
1. **Systematic self-evaluation bias:** Claude models may systematically rate Claude outputs more or less favorably than an independent evaluator would. The direction of bias is unknown.
2. **CIR scoring circularity:** The same model family that produced the errors is judging whether those errors are "confident." Claude may have a blind spot for errors that Claude characteristically makes.
3. **Score gaming vulnerability:** Since the scorer shares training data with the subjects, the scorer may default to its own internal knowledge to verify facts rather than strictly comparing against the ground truth document. This is unfalsifiable from the deliverable alone.

**Circumvention scenario:** An adversary could argue that the entire scoring rubric can be gamed by choosing a different model family as scorer. If GPT-4 or Gemini scored the same responses, results could differ substantially, and no calibration experiment was performed.

**Impact:** Undermines the objectivity of all 7 dimensions, particularly CIR (which requires judgment about confidence level).

**Severity:** P1 -- Standard limitation in LLM-as-Judge methodology, but unacknowledged in the deliverable.

---

#### RT-006-qg2-20260222: Question Selection Bias Toward Agent A Weaknesses (P2)

**Vector:** The research questions were designed with "Known Error Traps" that specifically target areas where LLM internal knowledge is expected to fail (version numbers, niche biographical details, frequently confused facts). This biases the experiment toward confirming the thesis.

**Evidence:** The ground truth document (ground-truth.md) includes a "Known Error Traps" section listing "common model mistakes per question." The question design principles state: "Questions target known model weakness areas: niche biographical details, specific version numbers, corrected scientific findings, frequently confused historical facts, entertainment industry specifics."

A hostile reviewer would argue this is confirmation bias in experimental design. The questions were selected specifically because they are likely to produce CIR > 0 for Agent A. If the questions instead asked about well-established facts (e.g., chemical element properties, basic math, widely known historical dates), Agent A's CIR might be near zero across all domains.

**Impact:** The finding "50% of ITS questions have CIR > 0" may not generalize beyond this specific question set. The question set was engineered to maximize CIR, not to represent the distribution of real-world queries.

**Severity:** P2 -- Valid experimental design choice (probing known weak spots is legitimate), but the generalizability limitation is not stated.

---

### Category 4: Dependency

#### RT-007-qg2-20260222: Ground Truth Itself is Tool-Derived and Unvalidated (P1)

**Vector:** The ground truth baseline was established by a tool-assisted agent (ps-researcher-005) using WebSearch, WebFetch, and Context7. The accuracy of this ground truth is assumed but never independently validated.

**Evidence:** The ground truth document cites sources like Wikipedia, PyPI, IMDb, and various news sites. However:

1. No human expert validated the ground truth for any question.
2. Web sources can contain errors, particularly on niche facts (e.g., Shane McConkey's birth location, Dean Potter's specific speed times).
3. The ground truth document states Graham Hunt "hit side wall of notch; Potter cleared notch but crashed into terrain beyond" as verified fact, but this level of detail about a fatal accident is sourced from media reporting, not an official investigation report.
4. If any ground truth answer is itself incorrect, the CIR scoring for that question is invalidated.

**Dependency chain:** Conclusions depend on CIR scores, which depend on ground truth accuracy, which depends on web source reliability, which is assumed.

**Impact:** A single ground truth error could flip a CIR=0 question to CIR>0 or vice versa, directly affecting the headline "50% prevalence" statistic.

**Severity:** P1 -- Ground truth validation is a standard requirement for evaluation benchmarks.

---

### Category 5: Degradation

#### RT-008-qg2-20260222: Conclusions Degrade Under Different Weighting Schemes (P1)

**Vector:** The 7-dimension weighting scheme (FA=0.25, CIR=0.20, CUR=0.15, COM=0.15, SQ=0.10, CC=0.10, SPE=0.05) is presented without justification. Different defensible weightings produce materially different conclusions.

**Evidence:** The weights assign 0.25 to Factual Accuracy and 0.20 to CIR, making these two dimensions (which are closely correlated -- errors in FA drive CIR) together account for 45% of the composite. Source Quality at 0.10 is low enough that its designed-in zero for Agent A has a moderate but not dominant effect.

Sensitivity analysis (not performed in the deliverable) would show:

| Weighting Scenario | Agent A ITS Composite (correct math) | Key Conclusion Change |
|--------------------|------------------------------------|----------------------|
| Equal weights (1/7 each) | Higher (less FA/CIR penalty) | Gap narrows |
| FA-only (1.0 FA) | 0.850 | Agent A "respectable" becomes "strong" |
| Remove SQ dimension | ~0.85 | Agent A ITS nearly matches Agent B ITS on remaining dims |
| Double CIR weight | Lower | Gap widens, thesis strengthened |

The absence of any sensitivity analysis means the reader cannot assess whether the conclusions are robust to reasonable alternative weightings or fragile artifacts of one particular weighting choice.

**Impact:** A reviewer could construct a weighting that eliminates most of the composite gap on ITS questions, undermining the "hidden danger" narrative.

**Severity:** P1 -- Standard expectation for multi-criteria evaluation is sensitivity analysis.

---

#### RT-009-qg2-20260222: Temporal Validity Decay (P2)

**Vector:** The analysis compares Agent A's internal knowledge (training cutoff ~May 2025) against ground truth verified in February 2026. The Technology domain errors (RQ-04: version numbers) are partially explained by temporal decay rather than fundamental parametric knowledge failure.

**Evidence:** Error 2 (current version "2.31.x or 2.32.x" vs actual 2.32.5) and Error 3 (urllib3 vendoring status) are facts that changed over time. Agent A's training data may have been accurate at training time. The analysis does not distinguish between:
1. **Errors of fact** (never correct in any training data -- e.g., the Naypyidaw date)
2. **Errors of currency** (correct at training time, now outdated -- e.g., urllib3 relationship)
3. **Errors of confusion** (multiple conflicting facts in training data -- e.g., Session version)

**Impact:** If the Technology domain errors are primarily currency errors, the thesis shifts from "LLMs embed subtle errors" to "LLM knowledge decays," which is a different (and less novel) claim.

**Severity:** P2 -- Does not invalidate the thesis but weakens its novelty claim.

---

## Defense Gap Assessment

| Finding ID | Current Defense | Gap |
|------------|----------------|-----|
| RT-001 | Worked example verifies formula; "Correction" note present | Document never reconciles worked example (0.7150) with table (0.5925). No automated verification of table values. All downstream analysis uses wrong values. |
| RT-002 | CIR definition provided in scoring rubric | No operationalization codebook for hedging classification. No inter-rater calibration. |
| RT-003 | 15 questions across 5 domains | No confidence intervals, no power analysis, no acknowledgment of sample size limitations. |
| RT-004 | Acknowledged as "by design" in conclusions | SQ penalty not removed from composite; no sensitivity analysis showing composites with/without SQ. |
| RT-005 | None | No inter-rater reliability. No cross-model validation. No human baseline. |
| RT-006 | None | No representativeness argument for question selection. No random sampling from query distribution. |
| RT-007 | Sources cited in ground truth document | No expert validation. No error-bound on ground truth itself. |
| RT-008 | None | No sensitivity analysis on weights. No justification for chosen weights. |
| RT-009 | Error pattern table distinguishes some types | Does not systematically classify errors by temporal category. |

---

## Countermeasures

### P0 Countermeasures (Must Fix)

#### CM-001: Correct All Composite Score Calculations (for RT-001)

**Action:** Recalculate all 30 composite scores (15 per agent) using the stated formula. Replace the Weighted Composite Scores table with verified values. Propagate corrected composites to all downstream tables: ITS vs PC comparison, domain averages, statistical summary, key ratios.

**Verification:** Provide at least 3 worked examples (one ITS Agent A, one PC Agent A, one Agent B) with step-by-step arithmetic. Ensure each matches the corresponding table entry to 4 decimal places.

**Impact on conclusions:** With corrected composites, Agent A's ITS average rises from the claimed 0.634 to approximately 0.762. This is substantially closer to Agent B's ITS average of approximately 0.938. The ITS gap narrows from 0.289 to approximately 0.176. The PC gap remains large. All "key ratios" and "critical contrast" values must be recalculated.

**Corrected key metrics (estimated):**

| Metric | Wrong (Current) | Corrected | Change |
|--------|-----------------|-----------|--------|
| Agent A ITS Composite | 0.634 | ~0.762 | +0.128 |
| Agent A All Composite | 0.515 | ~0.616 | +0.101 |
| Agent A PC Composite | 0.278 | ~0.324 | +0.046 |
| ITS Composite Gap | 0.289 | ~0.176 | -0.113 |

**Note:** The directional conclusions likely survive correction (Agent B still outperforms Agent A), but the magnitude of the gap changes significantly, and several headline numbers will shift.

---

### P1 Countermeasures (Should Fix)

#### CM-002: Add CIR Operationalization Codebook (for RT-002)

**Action:** Add a section defining:
1. What constitutes "hedging" (enumerated list of qualifying phrases)
2. Whether CIR is per-question or per-claim, with the denominator specified
3. How self-corrections are scored (does initial wrong answer count if corrected?)
4. Worked examples of CIR scoring for at least 2 questions

---

#### CM-003: Add Statistical Caveats and Framing (for RT-003)

**Action:** Add a "Limitations" section that explicitly states:
1. N=15 is a proof-of-concept demonstration, not a powered study
2. All comparative metrics are descriptive (point estimates), not inferential
3. Per-domain findings (N=2 per domain for ITS) are directional indicators, not statistically reliable estimates
4. Use language like "in this sample" rather than absolute claims

---

#### CM-004: Present Composites With and Without Source Quality (for RT-004)

**Action:** Add a parallel composite column excluding the SQ dimension (renormalized weights summing to 0.90, or explicitly noted as non-normalized). This separates the designed-in penalty from empirical differences.

---

#### CM-005: Acknowledge Single-Evaluator Limitation (for RT-005)

**Action:** Add to Limitations: "All scoring was performed by a single evaluator within the Claude model family. No inter-rater reliability was computed. Results may not generalize across scoring models."

---

#### CM-006: Add Weight Sensitivity Discussion (for RT-008)

**Action:** Add a brief sensitivity analysis showing composite gaps under at least 2 alternative weighting schemes (e.g., equal weights, FA-dominant weights). Demonstrate that directional conclusions hold across weightings even if magnitudes change.

---

#### CM-007: Validate Ground Truth for CIR-Relevant Questions (for RT-007)

**Action:** For the 5 questions where Agent A has CIR > 0 (RQ-01, RQ-02, RQ-04, RQ-11, RQ-13), add a second verification source for each ground truth claim that drives the CIR score. Cross-reference with at least one primary source (official documentation, government records) rather than relying solely on media/Wikipedia.

---

#### CM-008: Classify Error Types Systematically (for RT-009)

**Action:** Add an "Error Classification" column to the error catalogue distinguishing:
- **Factual error** (never correct in training data)
- **Currency error** (correct at training time, now outdated)
- **Confusion error** (multiple conflicting values in training data)

This allows the reader to assess which errors support the "parametric knowledge is dangerous" thesis vs the "knowledge decays" thesis.

---

## Quality Dimension Impact

Assessment of how the identified attack vectors affect the deliverable's quality gate scoring across the 6 standard dimensions:

| Dimension | Weight | Impact | Affected Findings | Score Adjustment |
|-----------|--------|--------|--------------------|-----------------|
| Completeness | 0.20 | Moderate | RT-003 (no limitations section), RT-006 (no representativeness argument), RT-008 (no sensitivity analysis) | -0.10 to -0.15 |
| Internal Consistency | 0.20 | **Severe** | RT-001 (worked example contradicts table; all downstream stats use wrong values) | -0.25 to -0.30 |
| Methodological Rigor | 0.20 | High | RT-002 (CIR operationalization), RT-003 (sample size), RT-004 (designed-in bias in composite), RT-005 (single evaluator), RT-008 (no sensitivity) | -0.15 to -0.20 |
| Evidence Quality | 0.15 | Moderate | RT-007 (unvalidated ground truth), RT-009 (error classification missing) | -0.05 to -0.10 |
| Actionability | 0.15 | Low | Conclusions and content angles remain directionally sound | -0.00 to -0.05 |
| Traceability | 0.10 | Low | Source documents referenced; pipeline traceable | -0.00 to -0.05 |

**Estimated composite impact:** The arithmetic errors (RT-001) alone would reduce Internal Consistency to the point where the deliverable cannot pass a >= 0.92 quality gate. The severity is in the **internal contradiction** (worked example vs table), not merely in incorrect numbers.

**Pre-fix score estimate:** 0.68 - 0.75 (REJECTED band per operational score bands)

**Post-fix score estimate (if all P0/P1 countermeasures applied):** 0.88 - 0.94 (REVISE to PASS range, depending on execution quality of fixes)

---

## Finding Summary

| ID | Category | Priority | Title | Fix |
|----|----------|----------|-------|-----|
| RT-001-qg2-20260222 | Ambiguity | **P0** | Systematic composite score arithmetic errors; worked example contradicts summary table; all downstream statistics wrong | CM-001: Recalculate all composites, propagate corrections |
| RT-002-qg2-20260222 | Ambiguity | P1 | CIR operationalization ambiguity; "hedging" not defined; scoring denominator unclear | CM-002: Add CIR codebook |
| RT-003-qg2-20260222 | Boundary | P1 | N=15 sample size; no confidence intervals or power analysis; four-decimal precision from 15 observations | CM-003: Add statistical caveats |
| RT-004-qg2-20260222 | Boundary | P1 | Source Quality = 0.000 is a design artifact penalizing Agent A by 0.089 composite points | CM-004: Present composites with/without SQ |
| RT-005-qg2-20260222 | Circumvention | P1 | Single-evaluator same-model-family scoring; no inter-rater reliability | CM-005: Acknowledge limitation |
| RT-006-qg2-20260222 | Circumvention | P2 | Question selection biased toward known model weaknesses; generalizability unstated | (Acknowledge in limitations) |
| RT-007-qg2-20260222 | Dependency | P1 | Ground truth tool-derived and unvalidated by domain experts | CM-007: Add second verification source for CIR-relevant questions |
| RT-008-qg2-20260222 | Degradation | P1 | No weight sensitivity analysis; conclusions may be weighting-dependent | CM-006: Add sensitivity analysis |
| RT-009-qg2-20260222 | Degradation | P2 | Temporal validity decay not distinguished from fundamental parametric error | CM-008: Add error classification |

**Total findings:** 9 (1 P0, 6 P1, 2 P2)

**Blocking finding:** RT-001-qg2-20260222. The deliverable cannot pass QG-2 until the arithmetic errors are corrected and all downstream statistics are recalculated from correct composites.

---

*Agent: adv-executor*
*Strategy: S-001 Red Team Analysis*
*Execution ID: qg2-20260222*
*Date: 2026-02-22*
*Status: COMPLETED*
