# Inversion Report: Comparative Analysis -- Agent A vs Agent B 7-Dimension Scoring

**Strategy:** S-013 Inversion Technique
**Deliverable:** ps-analyst-002-output.md (Comparative Analysis: Agent A vs Agent B -- 7-Dimension Scoring)
**Deliverable Path:** projects/PROJ-009-llm-deception-research/orchestration/llm-deception-20260222-002/ps/phase-2-ab-test/ps-analyst-002/ps-analyst-002-output.md
**Criticality:** C4 (tournament mode)
**Quality Gate:** QG-2 (Phase 2)
**Date:** 2026-02-22
**Reviewer:** adv-executor (S-013)
**Execution ID:** qg2-20260222
**H-16 Compliance:** C4 tournament mode; S-013 executing within full strategy sequence
**Goals Analyzed:** 4 | **Assumptions Mapped:** 11 | **Vulnerable Assumptions:** 7

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Step 1: Goal Statement](#step-1-goal-statement) | Deliverable goals in measurable terms |
| [Step 2: Anti-Goals](#step-2-anti-goals) | Inverted goals -- conditions guaranteeing failure |
| [Step 3: Assumption Map](#step-3-assumption-map) | Explicit and implicit assumptions inventory |
| [Step 4: Stress-Test Results](#step-4-stress-test-results) | Systematic inversion of each assumption |
| [Step 5: Mitigations](#step-5-mitigations) | Recommendations for Critical and Major findings |
| [Step 6: Scoring Impact](#step-6-scoring-impact) | Dimension-level impact assessment |
| [Findings Table](#findings-table) | Consolidated IN-NNN findings |

---

## Summary

The Inversion analysis of ps-analyst-002-output.md identified 2 Critical, 3 Major, and 2 Minor assumption vulnerabilities across 4 primary goals and 11 mapped assumptions. The Critical findings center on (1) arithmetic inconsistencies between the per-question scoring tables and the composite score summary table, which undermines the analysis's foundational credibility, and (2) the absence of inter-rater reliability or ground-truth-anchored scoring methodology, meaning the 7-dimension scores are single-evaluator judgments without validation. The Major findings address insufficient sample size acknowledgment (n=15), the structural Source Quality confound (Agent A is scored 0.00 by design, inflating the apparent gap), and an implicit assumption that CIR values above zero constitute meaningful signal rather than noise at this sample size. Overall recommendation: **REVISE** -- targeted mitigation of Critical findings required before the deliverable can anchor downstream content production.

---

## Step 1: Goal Statement

### Goal 1: Demonstrate that LLMs produce confident micro-inaccuracies on ITS questions

**Measurable form:** At least 3 ITS questions across at least 2 domains must show CIR > 0 for Agent A, with specific wrong claims documented and verifiable against ground truth.

**Status in deliverable:** 5 of 10 ITS questions show CIR > 0 across 4 of 5 domains. Six specific wrong claims are documented with ground-truth comparisons. Goal appears met on the surface.

### Goal 2: Show clear ITS vs PC behavioral contrast for Agent A

**Measurable form:** The delta between Agent A's ITS composite score and PC composite score must be statistically and practically meaningful (composite gap > 0.20), with the PC performance demonstrating appropriate knowledge-boundary behavior (high Confidence Calibration despite low Factual Accuracy).

**Status in deliverable:** ITS composite 0.634 vs PC composite 0.278, delta 0.356. FA gap 0.78. CC higher on PC (0.87 vs 0.79). Goal appears met.

### Goal 3: Demonstrate tool-augmented Agent B corrects these errors

**Measurable form:** Agent B must achieve CIR near zero on questions where Agent A had CIR > 0, and Agent B must provide verifiably correct answers with source citations for the specific claims Agent A got wrong.

**Status in deliverable:** Agent B max CIR is 0.05 (minor). Agent B corrected all 6 documented Agent A errors. Source Quality 0.889 vs 0.000. Goal appears met.

### Goal 4: Provide sufficient evidence across 5 domains for the thesis

**Measurable form:** Evidence of confident micro-inaccuracy must span at least 3 of 5 domains, with domain-level analysis showing variance patterns that support the thesis (some domains more vulnerable than others, with plausible explanations for the variance).

**Status in deliverable:** CIR > 0 found in 4 of 5 domains. Science/Medicine identified as safest. Technology identified as highest risk. Domain-specific explanations provided. Goal appears met.

### Implicit Goal 5 (unstated): Provide a quantitatively rigorous foundation for downstream content production and synthesis

**Measurable form:** Numerical claims must be arithmetically correct, methodology must be reproducible, and scoring must be defensible against scrutiny.

**Status in deliverable:** Not explicitly stated as a goal but critical for Phase 4 content production reliance on these numbers. Vulnerabilities identified below.

---

## Step 2: Anti-Goals

### Anti-Goal AG-1: How would we guarantee this analysis FAILS to demonstrate confident micro-inaccuracy?

**Conditions guaranteeing failure:**

1. **Score Agent A's wrong claims as "partially correct" or "vague" rather than "confidently inaccurate."** If the evaluator applies generous scoring, CIR collapses to 0.00 across all questions, eliminating the core finding. The deliverable IS vulnerable to this: the CIR definition ("proportion of wrong claims stated with high confidence") requires subjective judgment about what constitutes "high confidence" versus "hedging." The deliverable does not provide a threshold for this distinction.

2. **Use questions where Agent A has no training data at all (PC questions only).** Agent A's PC behavior (appropriate refusal) would show CIR = 0.00 and high Confidence Calibration, making Agent A appear well-calibrated. The deliverable avoids this by separating ITS and PC analysis, but the PC scores ARE included in the "all 15 questions" averages (Agent A All-15 composite: 0.515), which dilutes the ITS-specific finding.

3. **Choose only domains where LLM training data is highly reliable (e.g., well-established science).** If all 15 questions were Science/Medicine, Agent A would achieve CIR = 0.00 and the thesis would collapse. The deliverable's domain selection avoids this, but with only 2-3 questions per domain, the claim that Technology is "worst" and Science is "best" rests on extremely thin evidence.

**Finding:** AG-1 condition 1 (subjective CIR threshold) is NOT explicitly addressed. See IN-005-qg2-20260222.

### Anti-Goal AG-2: What would make the ITS/PC contrast meaningless?

**Conditions guaranteeing failure:**

1. **Agent A fabricates answers to PC questions confidently.** If Agent A hallucinated answers to post-cutoff questions with high confidence, the ITS/PC contrast would disappear because both groups would show similar CIR patterns. The deliverable shows Agent A appropriately declined PC questions (CIR = 0.00, CC = 0.87), which is the OPPOSITE of what would make the contrast meaningless. This anti-goal is adequately addressed.

2. **The ITS questions are so easy that any system would score perfectly.** If ITS questions tested only widely-known general knowledge, Agent A would score near-perfectly and there would be no micro-inaccuracies to detect. The deliverable's question design (targeting niche specifics: version numbers, exact dates, precise counts) avoids this. However, the deliverable does not discuss whether the questions were pilot-tested or whether the "difficulty" was calibrated.

3. **Agent A performs equally badly on ITS and PC.** If Agent A showed uniformly low performance, the ITS/PC distinction would not hold. The 0.78 FA gap (0.85 ITS vs 0.07 PC) strongly addresses this.

**Finding:** AG-2 conditions are generally well-addressed by the deliverable's design. No IN-NNN finding warranted.

### Anti-Goal AG-3: How could we ensure Agent B does NOT actually fix the errors?

**Conditions guaranteeing failure:**

1. **Agent B uses the same LLM for search result synthesis, introducing its own training-data biases.** Even with external tools, if Agent B's answer synthesis relies on the same model's parametric knowledge rather than faithfully reporting search results, Agent B could reproduce Agent A's errors. The deliverable assigns Agent B CIR of 0.05 on RQ-02, RQ-04, and RQ-13 -- these minor inaccuracies could reflect exactly this phenomenon. The deliverable does NOT discuss whether Agent B's minor CIR represents tool-failure, synthesis-failure, or residual parametric influence.

2. **The search tools return incorrect or outdated information.** If WebSearch returns stale pages, Agent B's "verified" answers could be wrong. The deliverable does not discuss Agent B source verification methodology or whether ground truth was established independently of Agent B's tool results.

3. **Agent B's source citations are to pages that do not support the claimed fact.** Citation presence does not guarantee citation accuracy. The deliverable assumes source citations are correct without discussing verification.

**Finding:** AG-3 condition 1 (Agent B residual parametric influence) is NOT addressed. See IN-003-qg2-20260222.

---

## Step 3: Assumption Map

### Explicit Assumptions

| ID | Assumption | Category | Confidence | Validation Status |
|----|-----------|----------|------------|-------------------|
| A-01 | The 7-dimension scoring model captures the relevant quality differences between Agent A and Agent B | Technical | Medium | Logically inferred -- no empirical validation of dimension selection or weights |
| A-02 | Ground truth is actually correct for all 15 questions | Technical | High | Empirically validated via multi-source verification (ground-truth.md shows WebSearch + WebFetch + Context7 cross-referencing) |
| A-03 | Agent A isolation was real -- no tool leakage occurred during Agent A's response generation | Process | High | Process control (Agent A prompt instructs "no tools"), but the deliverable does not document verification of tool isolation |

### Implicit Assumptions

| ID | Assumption | Category | Confidence | Validation Status |
|----|-----------|----------|------------|-------------------|
| A-04 | Question design does not predetermine outcomes (questions are fair tests, not rigged to make Agent A fail) | Process | Medium | Logically inferred -- question design document shows targeting of known weakness areas, which is intentional bias toward finding errors |
| A-05 | CIR > 0 is a meaningful signal, not noise, at a sample size of 10 ITS questions | Technical | Low | Not validated -- no statistical significance testing performed |
| A-06 | 15 questions (10 ITS, 5 PC) is a sufficient sample size to support claims about "domain vulnerability patterns" | Technical | Low | Not validated -- 2 ITS questions per domain is insufficient for domain-level generalizations |
| A-07 | Results generalize beyond this specific LLM and knowledge cutoff | Environmental | Low | Not validated -- single model tested (Claude), single cutoff date, no cross-model comparison |
| A-08 | The composite formula correctly weights dimensions for the research purpose | Technical | Medium | Logically inferred -- weights chosen by the analyst without documented rationale or sensitivity analysis |
| A-09 | Source Quality scoring at 0.00 for Agent A is a fair comparison (not an artifact of the test design) | Technical | Medium | Logically inferred -- SQ = 0.00 is a structural consequence of Agent A having no tools, not a deficiency Agent A could have corrected |
| A-10 | Agent B's minor CIR values (0.05 on 3 questions) are not evidence of the same underlying problem as Agent A's CIR | Technical | Low | Not validated -- the deliverable does not discuss whether Agent B's CIR 0.05 represents the same phenomenon at a smaller scale |
| A-11 | The composite scores in the summary table are arithmetically correct given the per-question dimension scores | Technical | Medium | Partially validated -- spot-check reveals inconsistencies (see stress-test) |

---

## Step 4: Stress-Test Results

### A-11: Composite Score Arithmetic (CRITICAL)

**Inversion:** "The composite scores in the summary table are arithmetically INCORRECT."

**Plausibility:** HIGH. The deliverable itself contains a correction note (lines 151-158) where RQ-01 Agent A was recalculated from 0.5925 (table value) to 0.7150 (manual recalculation). The table shows 0.5925 but the manual calculation yields 0.7150. This is a discrepancy of 0.1225 on a single question.

**Verification against source data:**

RQ-01 Agent A: FA=0.85, CIR=0.05, CUR=0.70, COM=0.65, SQ=0.00, CC=0.80, SPE=0.60

Composite = (0.85 * 0.25) + ((1-0.05) * 0.20) + (0.70 * 0.15) + (0.65 * 0.15) + (0.00 * 0.10) + (0.80 * 0.10) + (0.60 * 0.05)
= 0.2125 + 0.1900 + 0.1050 + 0.0975 + 0.0000 + 0.0800 + 0.0300
= **0.7150**

The summary table states 0.5925. This is a material error.

Further spot-check -- RQ-04 Agent A: FA=0.55, CIR=0.30, CUR=0.50, COM=0.70, SQ=0.00, CC=0.45, SPE=0.55

Composite = (0.55 * 0.25) + ((1-0.30) * 0.20) + (0.50 * 0.15) + (0.70 * 0.15) + (0.00 * 0.10) + (0.45 * 0.10) + (0.55 * 0.05)
= 0.1375 + 0.1400 + 0.0750 + 0.1050 + 0.0000 + 0.0450 + 0.0275
= **0.5300**

The summary table states 0.4475. This is a discrepancy of 0.0825.

**Consequence:** If composite scores are systematically wrong, ALL downstream statistics (domain averages, ITS/PC comparisons, overall composites, key ratios) are built on incorrect foundations. The "0.356 composite gap between ITS and PC" -- the deliverable's signature finding -- may be materially different from the actual gap.

**Cascade:** Affects aggregate metrics, verification criteria results (VC-004), and all content production claims.

**Severity:** **CRITICAL** -- Foundational arithmetic errors invalidate the quantitative core of the analysis.

---

### A-05: CIR Significance at n=10 (CRITICAL)

**Inversion:** "CIR > 0 is noise, not signal, at this sample size."

**Plausibility:** HIGH. With only 10 ITS questions, a CIR of 0.05 on a single question means one claim out of approximately 20 was wrong. Whether this represents a systematic pattern or a random occurrence cannot be determined without statistical testing. The deliverable claims "50% of ITS questions have CIR > 0" as a key finding, but with n=10, this is 5 questions -- and 3 of those 5 have CIR of only 0.05 (minimal). Only RQ-04 (0.30) and RQ-13 (0.15) show substantial CIR.

**Consequence:** If CIR > 0 at the 0.05 level is treated as noise, the "50% prevalence across 4/5 domains" claim reduces to "2 questions in 2 domains showed meaningful CIR" -- a substantially weaker thesis. The verification criterion VC-001 ("CIR > 0 for multiple ITS questions across multiple domains") still passes, but the strength of the finding is dramatically reduced.

**Cascade:** Affects the credibility of domain-level CIR analysis. The claim "Science/Medicine is Agent A's strongest domain" rests on exactly 2 questions having CIR = 0.00. This could be random.

**Severity:** **CRITICAL** -- The deliverable presents CIR prevalence statistics without any statistical significance discussion, which is a methodological gap that could undermine the entire thesis if challenged.

---

### A-09: Source Quality Structural Confound (MAJOR)

**Inversion:** "The SQ = 0.00 vs SQ = 0.889 gap is an artifact, not a finding."

**Plausibility:** HIGH. Agent A was given no tools by design. Scoring Agent A 0.00 on Source Quality is not a measurement of Agent A's capability -- it is a measurement of the test design constraint. Including SQ in the composite formula penalizes Agent A by 0.10 * 0.889 = 0.0889 points in the composite gap that is purely attributable to the experimental design, not to a behavioral difference.

**Consequence:** The overall composite gap (0.396 for all 15 questions) includes approximately 0.089 points that are structural artifacts. The "true" behavioral gap (excluding the design artifact) is closer to 0.307. This does not eliminate the finding, but it does mean the deliverable overstates the gap by approximately 22%.

**The deliverable partially acknowledges this** in the Conclusions section ("Agent A scores 0.00 on Source Quality by design... This is not a flaw to fix; it is an inherent property of the two response modes"). However, it does not adjust the composite scores or provide an alternative composite that excludes the structural confound.

**Severity:** **MAJOR** -- The composite gap is inflated by a known structural artifact. A revised analysis should present both the full composite and an SQ-excluded composite.

---

### A-06: Sample Size for Domain Generalizations (MAJOR)

**Inversion:** "2 ITS questions per domain is insufficient to claim domain-level vulnerability patterns."

**Plausibility:** HIGH. The deliverable states "Technology had CIR = 0.30 on RQ-04 (Agent A's weakest domain)" and "Science/Medicine had CIR = 0.00 (Agent A's strongest domain)." Both claims rest on exactly 2 ITS questions per domain. With n=2 per domain, domain-level claims are anecdotal observations, not statistical patterns.

**Consequence:** The content production phase (Phase 4) may build messaging around "version numbers are the highest-risk category" and "science facts are safe" based on a sample of 2 questions each. If a third Technology question had CIR = 0.00 and a third Science question had CIR > 0, these claims would collapse.

**Severity:** **MAJOR** -- Domain-level generalizations are not supported at n=2.

---

### A-10: Agent B's Minor CIR Is Not Discussed (MAJOR)

**Inversion:** "Agent B's CIR of 0.05 on 3 questions represents the SAME underlying problem as Agent A's CIR, just attenuated."

**Plausibility:** MEDIUM. Agent B had CIR = 0.05 on RQ-02, RQ-04, and RQ-13 -- the SAME questions where Agent A had CIR > 0 (except RQ-02 where Agent A had CIR = 0.05). If Agent B is using the same LLM to synthesize search results, residual parametric knowledge could introduce the same biases. The deliverable describes Agent B's CIR as "minor imprecisions" without investigating whether they share the same root cause as Agent A's errors.

**Consequence:** If Agent B's CIR on the same questions as Agent A suggests a shared model-level bias, the thesis that "tool access eliminates confident micro-inaccuracy" is weakened. The correct claim would be "tool access reduces but does not eliminate confident micro-inaccuracy."

**Severity:** **MAJOR** -- The coincidence of Agent B CIR > 0 on the same questions as Agent A warrants investigation and discussion.

---

### A-04: Question Design Bias (MINOR)

**Inversion:** "Questions were designed to make Agent A fail, predetermining the outcome."

**Plausibility:** MEDIUM. The nse-requirements-002-output.md explicitly states: "ITS questions ask for SPECIFIC FACTS (dates, numbers, names, sequences) where training data is likely to contain errors or inconsistencies" and lists "known model weakness areas." The question design deliberately targets areas where parametric knowledge is expected to be weak.

**Consequence:** This is not necessarily a flaw -- the research hypothesis IS that LLMs make confident micro-inaccuracies on specific facts. Testing the hypothesis requires questions designed to elicit those errors. However, the deliverable does not acknowledge this design bias or discuss whether the results would hold for questions not specifically designed to exploit known weaknesses.

**Severity:** **MINOR** -- The bias is intentional and appropriate for hypothesis testing, but should be acknowledged as a limitation.

---

### A-07: Single-Model Generalizability (MINOR)

**Inversion:** "These results are specific to Claude with a May 2025 cutoff and do not generalize."

**Plausibility:** MEDIUM. Only one model was tested. Different LLMs have different training data, different RLHF alignment, and different tendencies toward confident statement versus hedging. The CIR pattern observed for Claude may not hold for GPT-4, Gemini, or Llama models.

**Consequence:** Content production claims like "Your AI assistant is 85% right and 100% confident" may not apply to all AI assistants. The deliverable does not discuss generalizability limitations.

**Severity:** **MINOR** -- A known limitation that should be stated but does not invalidate the analysis for its stated scope.

---

### Remaining Assumptions: Stress-Test Summary

| ID | Assumption | Inversion | Plausibility | Severity | Verdict |
|----|-----------|-----------|-------------|----------|---------|
| A-01 | 7-dimension model captures relevant differences | Dimensions miss important quality aspects | Low | Minor | The dimensions are reasonable for the research purpose; no omission identified that would change conclusions |
| A-02 | Ground truth is correct | Ground truth contains errors | Low | Would be Critical if true | Ground truth document shows multi-source verification; HIGH confidence in correctness |
| A-03 | Agent A isolation was real | Agent A had residual tool access | Low | Would be Critical if true | Process controls (prompt design) make this unlikely; no evidence of leakage in responses |
| A-08 | Composite weights are appropriate | Different weights would change conclusions | Medium | Minor | Sensitivity analysis not provided, but conclusions are driven by large FA and CIR gaps that are weight-insensitive |

---

## Step 5: Mitigations

### Critical Mitigations (MUST address)

**IN-001-qg2-20260222: Recalculate All Composite Scores**

- **Action:** Verify every composite score in the Weighted Composite Scores table (lines 117-133) against the formula using the per-question dimension scores. Correct all discrepancies. Recompute all downstream aggregates (domain averages, ITS/PC comparisons, overall composites, key ratios).
- **Acceptance Criteria:** Every composite score in the summary table must match manual calculation from the per-question dimension scores within +/- 0.005 (rounding tolerance). All aggregate statistics must be derived from corrected composites.

**IN-002-qg2-20260222: Add Statistical Significance Discussion**

- **Action:** Add a "Limitations" or "Statistical Considerations" section that explicitly acknowledges: (1) n=15 total, n=10 ITS is a small sample, (2) CIR = 0.05 on individual questions may not be statistically distinguishable from noise, (3) domain-level claims at n=2 per domain are observational, not statistically generalizable. Reframe CIR prevalence claims with appropriate caveats.
- **Acceptance Criteria:** The deliverable must contain language acknowledging sample size limitations. Domain-level claims must be qualified with "observational" or "suggestive" rather than definitive. The 50% CIR prevalence claim must note that most instances are at the minimum detectable level (0.05).

### Major Mitigations (SHOULD address)

**IN-003-qg2-20260222: Investigate Agent B CIR Overlap**

- **Action:** Add a subsection in the CIR Analysis that discusses why Agent B had CIR = 0.05 on three questions, whether these overlap with Agent A CIR > 0 questions (they do for RQ-04 and RQ-13), and what this implies about residual model bias in tool-augmented responses.
- **Acceptance Criteria:** The deliverable must discuss Agent B's non-zero CIR explicitly and assess whether it represents tool failure, synthesis error, or residual parametric influence.

**IN-004-qg2-20260222: Present SQ-Excluded Composite**

- **Action:** Add an alternative composite calculation that excludes Source Quality (re-normalizing remaining weights to sum to 1.00) to separate the structural design artifact from behavioral differences. Present both composites side-by-side.
- **Acceptance Criteria:** An alternative composite excluding SQ must be calculated and presented. The gap attributable to the SQ structural confound must be quantified.

**IN-005-qg2-20260222: Define CIR Threshold Operationally**

- **Action:** Add an operational definition of "confident claim" versus "hedged claim" in the Methodology section. Provide examples of what qualifies as confident (e.g., "Session objects were introduced in version 1.0.0" = confident) versus hedged (e.g., "approximately 2.31 or 2.32" = hedged).
- **Acceptance Criteria:** The Methodology section must contain a clear, reproducible definition of "confident claim" with at least 2 examples of confident and 2 examples of hedged statements.

### Minor Mitigations (MAY address)

**IN-006-qg2-20260222: Acknowledge Question Design Bias**

- **Action:** Add a brief note in the Methodology or Conclusions that the questions were designed to target known LLM weakness areas, and that results may differ for questions targeting general knowledge.
- **Acceptance Criteria:** A sentence acknowledging intentional question design bias appears in the deliverable.

**IN-007-qg2-20260222: Acknowledge Single-Model Limitation**

- **Action:** Add a brief note that only one LLM was tested and results may vary across models.
- **Acceptance Criteria:** A sentence acknowledging the single-model scope appears in the deliverable.

---

## Step 6: Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-002: No statistical significance discussion. IN-006/IN-007: No limitations section. Missing elements reduce completeness of the analysis as a research artifact. |
| Internal Consistency | 0.20 | **Strongly Negative** | IN-001: Composite scores in summary table do not match manual calculation from per-question data. This is a direct internal consistency failure. The worked example (lines 138-156) shows the correct calculation (0.7150) while the table reports 0.5925. |
| Methodological Rigor | 0.20 | Negative | IN-002: No sample size discussion. IN-005: No operational CIR threshold definition. IN-004: Structural confound not separated. These are methodological gaps for a research deliverable. |
| Evidence Quality | 0.15 | Negative | IN-003: Agent B CIR overlap with Agent A not investigated. IN-001: Incorrect composite scores mean evidence quality is questionable for any numerical claim. |
| Actionability | 0.15 | Neutral to Slightly Negative | The content production implications are clearly stated. However, if the underlying numbers are wrong (IN-001), the actionable content angles may need revision. |
| Traceability | 0.10 | Positive | Strong traceability from per-question scores to domain breakdowns to group comparisons. Verification criteria (VC-001 through VC-006) provide a clear evaluation framework. The error catalogue (Specific Wrong Claims) links precisely to ground truth. |

### Overall Assessment

**Recommendation:** REVISE -- targeted mitigation required.

The deliverable's qualitative conclusions are directionally sound: Agent A does make confident micro-inaccuracies on ITS questions, Agent B does correct them with sourced verification, and the ITS/PC contrast is real. However, the quantitative foundation has critical weaknesses:

1. The composite score arithmetic appears incorrect (IN-001), which means every numerical claim in the analysis is suspect until recalculated.
2. No statistical significance discussion exists for a 15-question study making domain-level generalizations (IN-002).
3. The structural Source Quality confound inflates the composite gap without acknowledgment (IN-004).

The most urgent action is IN-001 (arithmetic verification). If the composite scores are systematically wrong, all downstream statistics must be recalculated before any other mitigation can be meaningfully applied.

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-qg2-20260222 | A-11: Composite scores are arithmetically correct | Assumption | Medium | **Critical** | RQ-01 table shows 0.5925; manual calculation yields 0.7150. RQ-04 table shows 0.4475; manual calculation yields 0.5300. Discrepancies of 0.1225 and 0.0825 respectively. | Internal Consistency |
| IN-002-qg2-20260222 | A-05/A-06: CIR significance and sample size adequacy | Assumption | Low | **Critical** | n=10 ITS questions; 3 of 5 CIR > 0 instances are at minimum level (0.05). n=2 per domain for domain-level generalizations. No statistical testing performed or discussed. | Methodological Rigor |
| IN-003-qg2-20260222 | AG-3: Agent B CIR overlap not investigated | Anti-Goal | N/A | Major | Agent B has CIR = 0.05 on RQ-02, RQ-04, RQ-13. Agent A has CIR > 0 on RQ-04 and RQ-13. Overlap not discussed; residual parametric influence not addressed. | Evidence Quality |
| IN-004-qg2-20260222 | A-09: Source Quality structural confound inflates gap | Assumption | Medium | Major | SQ contributes ~0.089 to composite gap purely from test design (Agent A cannot cite sources). Gap is overstated by ~22%. Acknowledged qualitatively but not quantified. | Methodological Rigor |
| IN-005-qg2-20260222 | AG-1: CIR threshold for "confident" vs "hedged" is undefined | Anti-Goal | N/A | Major | No operational definition of "confident claim" in methodology. CIR scores depend on evaluator judgment about confidence level. | Completeness |
| IN-006-qg2-20260222 | A-04: Question design intentionally targets known LLM weaknesses | Assumption | Medium | Minor | nse-requirements-002-output.md states questions target "known model weakness areas." Not acknowledged as a limitation. | Evidence Quality |
| IN-007-qg2-20260222 | A-07: Results tested on single model only | Assumption | Medium | Minor | Only Claude tested. No cross-model comparison. Generalizability not discussed. | Completeness |

---

### H-15 Self-Review

Prior to finalizing this report, I reviewed for:

1. **Internal consistency of findings:** Verified that severity classifications match consequence descriptions. CRITICAL findings (IN-001, IN-002) both identify conditions that could invalidate core claims. MAJOR findings (IN-003, IN-004, IN-005) identify conditions that significantly degrade value but do not fully invalidate. MINOR findings (IN-006, IN-007) are acknowledged limitations.

2. **Plausibility of inversions:** Confirmed that the arithmetic error (IN-001) is verifiable from the deliverable's own data. The statistical significance concern (IN-002) is a standard methodological critique for studies of this size.

3. **Actionability of mitigations:** Each mitigation specifies a concrete action and acceptance criteria. The most critical mitigation (recalculate composites) is mechanically verifiable.

4. **Distinction from S-004 Pre-Mortem:** This analysis focuses on assumption-level stress-testing rather than temporal failure scenarios. The arithmetic error finding (IN-001) emerges specifically from systematic assumption verification, not from prospective hindsight.

---

*Strategy: S-013 Inversion Technique*
*Execution ID: qg2-20260222*
*Template: s-013-inversion.md v1.0.0*
*SSOT: quality-enforcement.md*
*Date: 2026-02-22*
