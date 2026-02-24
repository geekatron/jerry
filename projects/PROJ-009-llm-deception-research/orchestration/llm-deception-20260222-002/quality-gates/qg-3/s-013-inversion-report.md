# Inversion Report: Phase 3 Research Synthesis (Two-Leg Thesis + Architectural Analysis)

**Strategy:** S-013 Inversion Technique
**Deliverables:** ps-synthesizer-002-output.md (primary), ps-architect-002-output.md (secondary)
**Criticality:** C4 (tournament mode)
**Date:** 2026-02-22
**Reviewer:** adv-executor (S-013)
**H-16 Compliance:** S-003 Steelman applied as part of C4 tournament sequence (confirmed)
**Goals Analyzed:** 7 | **Assumptions Mapped:** 14 | **Vulnerable Assumptions:** 9

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Step 1: Goal Inventory](#step-1-goal-inventory) | Explicit and implicit goals of the deliverables |
| [Step 2: Anti-Goal Analysis](#step-2-anti-goal-analysis) | Inverted goals -- what would guarantee failure |
| [Step 3: Assumption Map](#step-3-assumption-map) | All explicit and implicit assumptions |
| [Step 4: Stress-Test Results](#step-4-stress-test-results) | Systematic inversion and consequence assessment |
| [Step 5: Mitigations](#step-5-mitigations) | Recommended actions for vulnerable assumptions |
| [Step 6: Scoring Impact](#step-6-scoring-impact) | Mapping to S-014 quality dimensions |
| [Findings Table](#findings-table) | Consolidated findings with severity and dimension |
| [Finding Details](#finding-details) | Expanded Critical and Major findings |
| [Recommendations](#recommendations) | Prioritized mitigation actions |

---

## Summary

Systematic inversion of the Two-Leg Thesis and its architectural analysis exposes 9 vulnerable assumptions out of 14 mapped, with 2 Critical and 5 Major findings. The deliverables present a coherent and well-structured argument, but the inversion reveals that several foundational claims rest on thin empirical ground (15-question sample), that the "Snapshot Problem" diagnosis may be incomplete (omitting model architecture factors), and that the proposed mitigation architecture (domain-aware tool routing) introduces its own failure modes that are not analyzed. The thesis itself may be a simplification that obscures a more complex reliability landscape.

**Recommendation:** ACCEPT with targeted revisions addressing Critical findings IN-001 and IN-002, and acknowledgment of Major findings IN-003 through IN-007 as limitations.

---

## Step 1: Goal Inventory

### Explicit Goals

| ID | Goal | Source | Measurability |
|----|------|--------|---------------|
| G-01 | Demonstrate that LLM unreliability operates on two distinct legs (Confident Micro-Inaccuracy and Knowledge Gaps) | ps-synthesizer-002, Executive Summary | Binary: thesis either supported or not by evidence |
| G-02 | Prove that Leg 1 is more dangerous than Leg 2 through the visibility asymmetry argument | ps-synthesizer-002, "The Real Danger is Leg 1" | Qualitative: assessed via the visibility asymmetry table |
| G-03 | Establish domain-specific reliability tiers with empirical CIR data | ps-synthesizer-002, Domain Analysis; ps-architect-002, Domain-Specific Reliability Tiers | Quantitative: FA and CIR scores per domain |
| G-04 | Diagnose the "Snapshot Problem" as the root architectural cause of Leg 1 | ps-architect-002, The Snapshot Problem | Explanatory: assessed by whether alternative explanations are excluded |
| G-05 | Propose a mitigation architecture (domain-aware tool routing) that addresses both legs | ps-architect-002, Mitigation Architecture | Architectural: assessed by completeness and feasibility |

### Implicit Goals

| ID | Goal | Inferred From | Measurability |
|----|------|---------------|---------------|
| G-06 | Correct workflow -001's methodological flaw (all-PC questions) and establish that the corrected methodology is valid | ps-synthesizer-002, Methodology Notes | Assessed by whether the corrected design actually addresses the flaw |
| G-07 | Position the Jerry Framework as a proof-of-concept for governance-based LLM reliability | ps-architect-002, Jerry Framework as Proof-of-Concept | Assessed by whether the evidence supports this claim without selection bias |

---

## Step 2: Anti-Goal Analysis

### AG-01: How would we guarantee the Two-Leg Thesis is WRONG?

To guarantee the Two-Leg Thesis fails, we would need:

1. **Demonstrate that Leg 1 and Leg 2 are not distinct failure modes but points on a single continuum.** If models show graduated confidence reduction (not binary "confident" vs. "hedging") as topic familiarity decreases, the "two legs" framing is an artificial bifurcation. The deliverable does not analyze intermediate cases -- questions where the model has partial training data and shows partial confidence. The ITS/PC binary split may be hiding a gradient.

2. **Show that confident micro-inaccuracies are NOT unique to LLMs but are standard human expert behavior.** If human subject-matter experts exhibit similar CIR rates (confidently stating 85% accurate answers in fast-evolving domains), then this is not an "LLM deception" problem but a general knowledge-representation problem. The deliverable never compares LLM error rates to human baselines.

3. **Demonstrate that the 0.85 FA score is an artifact of the scoring methodology, not a real phenomenon.** If different human raters score the same responses differently, or if the "ground truth" from WebSearch is itself unreliable, the measured CIR could be methodological noise rather than signal.

**Assessment:** The deliverable does not address anti-goals 1 or 2 at all. Anti-goal 3 is partially addressed in the Limitations section but dismissed as a minor concern. These represent blind spots.

### AG-02: How would we guarantee the Snapshot Problem diagnosis is WRONG?

To guarantee the Snapshot Problem is misdiagnosed, we would need:

1. **Show that model architecture (attention patterns, parameter compression) rather than training data inconsistency causes Leg 1 errors.** If a model trained on a single, perfectly consistent snapshot of all facts still produces micro-inaccuracies, the Snapshot Problem is not the root cause.

2. **Show that Technology/Software's high CIR is due to domain complexity, not snapshot conflicts.** Technology has inherently more complex, interconnected facts (version X introduced feature Y which depends on Z). Errors may arise from relational complexity, not temporal inconsistency.

3. **Show that fine-tuning on timestamped data eliminates Leg 1 errors.** If the Snapshot Problem is truly the root cause, a model trained only on the most recent snapshot of each fact should have zero CIR. If it still has nonzero CIR, other factors are at play.

**Assessment:** The deliverable acknowledges Q3 (fine-tuning on verified data) as an open question but does not explore alternative root causes for Leg 1 beyond the Snapshot Problem. The diagnosis is presented as more certain than the evidence warrants.

### AG-03: How would we guarantee domain-aware tool routing FAILS?

To guarantee the mitigation architecture fails, we would need:

1. **Show that the Domain Classifier itself makes Leg 1 errors** (confidently misclassifying T4 queries as T2). The deliverable acknowledges this in Q1 but does not analyze the severity or frequency of such misclassification.

2. **Show that WebSearch verification introduces its own errors** (retrieving incorrect information from the web, which replaces correct internal knowledge). The deliverable uses WebSearch as ground truth throughout without questioning its reliability.

3. **Demonstrate that the tier boundaries are unstable.** If a domain like "History" can shift between T2 and T3 depending on how recent the history is, the static tier assignment breaks down.

**Assessment:** The deliverable notes Q1 as an open question but treats the mitigation architecture as largely sound. The anti-goals reveal that the architecture has its own Leg 1 analog -- confident misrouting -- that is not analyzed.

---

## Step 3: Assumption Map

| ID | Assumption | Type | Category | Confidence | Validation Status | Consequence of Failure |
|----|-----------|------|----------|------------|-------------------|----------------------|
| A-01 | 15 questions across 5 domains is sufficient to establish domain-level reliability patterns | Implicit | Methodological | Low | Not validated (no power analysis) | Domain reliability tiers have no statistical backing |
| A-02 | The ITS/PC binary classification correctly captures the relevant knowledge boundary | Implicit | Methodological | Medium | Logically inferred but not empirically tested for edge cases | Two-leg model may be an oversimplification |
| A-03 | WebSearch provides reliable ground truth for scoring | Implicit | Methodological | Medium | Assumed, not validated | All FA and CIR scores may be unreliable |
| A-04 | The Snapshot Problem is the primary root cause of Leg 1 errors | Explicit | Technical | Medium | Logically argued but not empirically isolated | Mitigations target wrong root cause |
| A-05 | CIR is domain-dependent and follows training data stability | Explicit | Technical | Medium | Supported by 15-question sample | Tier definitions may not generalize |
| A-06 | Science/Medicine has zero CIR because facts are stable and consistent | Explicit | Technical | Medium | Supported by 2 questions | Generalization from 2 data points is extremely fragile |
| A-07 | LLM confidence calibration is binary (Leg 1: always high, Leg 2: appropriately low) | Implicit | Technical | Low | Not tested for intermediate cases | Two-leg model may miss a continuous spectrum |
| A-08 | Domain-aware tool routing provides optimal latency-accuracy tradeoff | Explicit | Architectural | Low | Not validated (no prototype or benchmark) | Architecture recommendation may be impractical |
| A-09 | The Domain Classifier can reliably assign queries to tiers | Implicit | Architectural | Low | Acknowledged as open question (Q1) | Misclassification produces the same Leg 1 errors the system tries to prevent |
| A-10 | Tool augmentation "completely solves" Leg 2 | Explicit | Technical | Medium | Supported by Agent B scores (0.88-0.95 FA on PC) | Agent B is not perfect (0.88 FA on Q12); "completely" overstates |
| A-11 | The Jerry Framework demonstrates governance-based mitigation effectiveness | Implicit | Environmental | Low | Supported by single anecdotal case (McConkey) | One case study is not a proof-of-concept |
| A-12 | The error patterns observed in Claude generalize to other LLM families | Implicit | Environmental | Low | Acknowledged as open question (Q2) but deliverable uses universal language ("LLMs") | Claims may be Claude-specific |
| A-13 | Single-turn factual questions are a valid proxy for real-world LLM usage patterns | Implicit | Methodological | Low | Not validated | Real-world LLM usage involves multi-turn, open-ended queries where Leg 1 may manifest differently |
| A-14 | The 8 Phase 1 deception patterns are valid and well-established | Explicit | Technical | Medium | Based on literature review and conversation mining from workflow -001 | 5 of 8 patterns are "not testable" in current methodology; only 2 confirmed |

---

## Step 4: Stress-Test Results

| ID | Assumption | Inversion | Plausibility | Severity | Affected Dimension |
|----|-----------|-----------|-------------|----------|-------------------|
| IN-001-QG3 | A-01: 15 questions sufficient for domain-level patterns | 15 questions is NOT sufficient; 2-3 questions per domain per category provides no statistical power for domain-level reliability claims | HIGH -- any statistician would reject n=2 per domain-category cell | Critical | Methodological Rigor |
| IN-002-QG3 | A-07: Confidence calibration is binary (two legs, not a spectrum) | Confidence calibration is NOT binary; there exists a spectrum of partial knowledge that produces intermediate confidence | HIGH -- likely true given how LLMs process graded familiarity from token frequency | Critical | Internal Consistency |
| IN-003-QG3 | A-04: Snapshot Problem is the primary root cause | Snapshot Problem is NOT the primary root cause; model architecture (compression, attention, parameter sharing) produces errors independently of training data inconsistency | MODERATE -- plausible given that even models trained on curated data still hallucinate | Major | Evidence Quality |
| IN-004-QG3 | A-03: WebSearch provides reliable ground truth | WebSearch does NOT provide reliable ground truth; search results may be incorrect, outdated, or contradictory | MODERATE -- WebSearch is imperfect but generally more reliable than unverified LLM output for specific facts | Major | Methodological Rigor |
| IN-005-QG3 | A-09: Domain Classifier can reliably assign tiers | Domain Classifier CANNOT reliably assign tiers because it is itself an LLM subject to Leg 1 errors about domain classification | HIGH -- creates a recursive reliability problem | Major | Actionability |
| IN-006-QG3 | A-10: Tool augmentation "completely solves" Leg 2 | Tool augmentation does NOT completely solve Leg 2; Agent B achieves 0.88 FA on Q12 (not 1.0), and tool availability is not guaranteed | HIGH -- the word "completely" is falsified by the deliverable's own data | Major | Internal Consistency |
| IN-007-QG3 | A-11: Jerry Framework demonstrates governance-based mitigation | Jerry Framework does NOT demonstrate governance-based mitigation because the McConkey case is a single anecdote, not a systematic evaluation | HIGH -- one case study with no control condition is not a proof-of-concept by any standard | Major | Evidence Quality |
| IN-008-QG3 | A-06: Science/Medicine zero CIR generalizes beyond 2 questions | Science/Medicine CIR is NOT zero in general; the 2 questions tested (ethanol boiling point, heart chambers) are among the most stable facts in all of science | MODERATE -- more complex scientific questions (drug interactions, climate data) would likely show nonzero CIR | Minor | Completeness |
| IN-009-QG3 | A-12: Results generalize beyond Claude | Results do NOT generalize to other LLM families; different training data, RLHF processes, and architectures could produce fundamentally different domain reliability profiles | MODERATE -- plausible but the general Snapshot Problem mechanism likely applies across architectures even if magnitudes differ | Minor | Completeness |

---

## Step 5: Mitigations

### Critical Mitigations (MUST address)

**IN-001-QG3: Insufficient sample size for domain-level claims**

- **Mitigation:** Add explicit statistical limitations throughout the deliverable. Reframe domain reliability tiers as "hypothesized tiers based on directional evidence" rather than "empirically-derived tiers." Add a power analysis showing what sample size would be needed for statistically significant domain-level claims (likely 30+ questions per domain-category cell, i.e., 300+ total questions for 5 domains x 2 categories).
- **Acceptance Criteria:** Every domain-level CIR claim includes a caveat about sample size. The tier definitions in ps-architect-002 are labeled as "hypothesized" rather than "established." A target sample size for future validation is stated.

**IN-002-QG3: Binary two-leg framing may obscure a continuous spectrum**

- **Mitigation:** Add a section discussing the possibility that LLM reliability operates on a continuous spectrum rather than two discrete legs. Acknowledge that the ITS/PC split is a methodological convenience, not a verified boundary. Discuss how questions with partial training data coverage (e.g., a topic that existed before cutoff but has evolved significantly) might show intermediate behavior. Consider renaming from "Two-Leg Thesis" to "Two-Pole Model" or similar language that implies endpoints of a spectrum rather than binary categories.
- **Acceptance Criteria:** The deliverable explicitly acknowledges the possibility of a continuous spectrum. At least one paragraph discusses intermediate cases and how they would be classified. The framing language avoids implying a hard boundary between Leg 1 and Leg 2.

### Major Mitigations (SHOULD address)

**IN-003-QG3: Snapshot Problem may not be the sole root cause**

- **Mitigation:** Add alternative explanations for Leg 1 errors: parameter compression artifacts, attention mechanism limitations, RLHF reward hacking, and tokenization effects on numerical precision. Reframe the Snapshot Problem as "a primary contributing factor" rather than "the root architectural cause."
- **Acceptance Criteria:** At least two alternative root causes are discussed alongside the Snapshot Problem. The causal language is modulated to reflect the strength of evidence.

**IN-004-QG3: WebSearch as ground truth is not validated**

- **Mitigation:** Add a section on ground truth methodology. Describe how WebSearch results were verified (were multiple sources consulted? Were official documentation sources preferred?). Acknowledge that some FA scores may have measurement error.
- **Acceptance Criteria:** Ground truth verification methodology is documented. At least one example shows how conflicting WebSearch results were resolved.

**IN-005-QG3: Domain Classifier is itself subject to LLM errors**

- **Mitigation:** Add a subsection in the Mitigation Architecture analyzing Domain Classifier failure modes. Propose a fallback: when the classifier's confidence is below a threshold, default to T4 (always verify). Quantify the cost of misclassification in each direction (over-verification vs. under-verification).
- **Acceptance Criteria:** Classifier failure modes are enumerated. A fallback strategy is specified. The asymmetry between over-verification (cost: latency) and under-verification (cost: accuracy) is analyzed.

**IN-006-QG3: "Completely solves" is falsified by own data**

- **Mitigation:** Replace "Tool augmentation completely solves it" with "Tool augmentation substantially addresses it" or similar language. Note that Agent B's PC accuracy ranges from 0.88 to 0.95, not 1.0. Discuss residual Leg 2 risk even with tool augmentation.
- **Acceptance Criteria:** No claim of "complete" solution for Leg 2. Agent B's actual PC accuracy range is cited alongside the claim.

**IN-007-QG3: Jerry Framework proof-of-concept claim is unsupported**

- **Mitigation:** Reframe the Jerry section from "proof-of-concept" to "illustrative example" or "case study." Acknowledge that a single anecdotal case does not constitute proof. Describe what a proper evaluation of governance-based mitigation would require (controlled experiment comparing governed vs. ungoverned agent outputs across multiple domains and queries).
- **Acceptance Criteria:** The section title no longer claims "proof-of-concept." The McConkey example is framed as "illustrative" rather than "demonstrative." A brief paragraph describes what a rigorous evaluation would entail.

### Minor Mitigations (MAY address)

**IN-008-QG3:** Note that the two Science/Medicine questions tested are among the most stable scientific facts (physical constants, anatomy). Acknowledge that more complex or evolving scientific topics (pharmacology, climate science, emerging diseases) may show nonzero CIR.

**IN-009-QG3:** Already partially addressed via Open Question Q2. Consider adding a sentence noting that domain reliability tiers should be validated across model families before being adopted as general architectural guidance.

---

## Step 6: Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-008-QG3, IN-009-QG3: Domain coverage is shallow (2-3 questions per domain); Science/Medicine zero-CIR claim rests on 2 easiest-possible questions; cross-model generalization not tested |
| Internal Consistency | 0.20 | Negative | IN-002-QG3: Binary two-leg framing contradicts the likely reality of a continuous spectrum; IN-006-QG3: "completely solves" contradicted by own data (Agent B PC range 0.88-0.95) |
| Methodological Rigor | 0.20 | Negative | IN-001-QG3 (Critical): n=2 per domain-category cell provides no statistical power for domain-level reliability claims; IN-004-QG3: ground truth methodology not documented |
| Evidence Quality | 0.15 | Negative | IN-003-QG3: Alternative root causes for Leg 1 not explored; IN-007-QG3: Jerry "proof-of-concept" rests on single anecdote; causal claims exceed evidence strength |
| Actionability | 0.15 | Negative | IN-005-QG3: Proposed Domain Classifier architecture has unanalyzed failure modes that create recursive reliability problems; recommendations may not be implementable as described |
| Traceability | 0.10 | Neutral | Both deliverables maintain strong traceability to Phase 1 and Phase 2 outputs; findings are well-referenced; no traceability gaps identified |

**Overall Assessment:** Targeted revision required. The Two-Leg Thesis is a valuable conceptual framework, but the deliverables present it with more certainty than the evidence supports. The two Critical findings (sample size insufficiency and binary framing) require revision to align claims with evidence strength. The five Major findings require acknowledgment as limitations or modulation of language. The architectural analysis is sound in structure but needs to analyze its own failure modes with the same rigor it applies to LLM failures.

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-QG3 | 15-question sample provides statistical basis for domain-level reliability claims | Assumption | Low | Critical | Methodology Notes: "15 questions is sufficient for directional findings but not for statistical significance" -- yet tiers are presented as established | Methodological Rigor |
| IN-002-QG3 | LLM reliability is binary (two discrete legs) rather than a continuous spectrum | Assumption | Low | Critical | No intermediate cases tested; ITS/PC classification is methodological convenience; LLMs process graded familiarity continuously | Internal Consistency |
| IN-003-QG3 | Snapshot Problem is the sole root cause of Leg 1 errors | Assumption | Medium | Major | Only one causal mechanism explored; model architecture, RLHF effects, and tokenization not considered | Evidence Quality |
| IN-004-QG3 | WebSearch provides reliable ground truth for all factual claims | Assumption | Medium | Major | WebSearch methodology not documented; no discussion of conflicting search results or source quality | Methodological Rigor |
| IN-005-QG3 | Domain Classifier can reliably route queries to correct tiers | Assumption | Low | Major | Acknowledged as open question Q1 but not analyzed as a failure mode of the proposed architecture | Actionability |
| IN-006-QG3 | Tool augmentation "completely solves" Leg 2 | Assumption | Medium | Major | Contradicted by own data: Agent B PC FA ranges 0.88-0.95, not 1.0 | Internal Consistency |
| IN-007-QG3 | Jerry Framework demonstrates governance-based mitigation as proof-of-concept | Assumption | Low | Major | Single anecdotal case (McConkey) with no control condition or systematic evaluation | Evidence Quality |
| IN-008-QG3 | Science/Medicine zero CIR generalizes beyond the 2 simplest possible questions | Assumption | Medium | Minor | Ethanol boiling point and heart chambers are maximally stable facts; complex science topics untested | Completeness |
| IN-009-QG3 | Domain reliability patterns generalize across LLM families | Assumption | Low | Minor | Acknowledged as open question Q2; deliverable uses universal "LLMs" language despite single-model evidence | Completeness |

---

## Finding Details

### IN-001-QG3: Insufficient Sample Size for Domain-Level Claims [CRITICAL]

**Type:** Assumption
**Original Assumption:** 15 questions (10 ITS + 5 PC) across 5 domains provides sufficient empirical basis to establish domain-level reliability tiers with specific CIR values.
**Inversion:** 15 questions is NOT sufficient. With 2 ITS questions per domain, each domain's CIR is estimated from exactly 2 data points. A single different question could shift a domain's CIR by 0.15 or more.
**Plausibility:** HIGH -- this is a basic statistical limitation that is acknowledged in the deliverable's own Limitations section but not reflected in how the findings are presented elsewhere.
**Confidence:** Low
**Consequence:** The entire domain reliability tier system (T1-T5) and the domain-specific verification policies built on it rest on a sample that would not pass peer review. Science/Medicine's "zero CIR" comes from exactly 2 questions about the most stable facts imaginable. Technology/Software's "0.30 CIR" comes from exactly 2 questions. Any domain-level quantitative claim from this sample is noise, not signal.
**Evidence:** ps-synthesizer-002 Methodology Notes: "15 questions is sufficient for directional findings but not for statistical significance." Yet ps-architect-002 builds an entire tier system with specific verification policies on these numbers.
**Dimension:** Methodological Rigor
**Mitigation:** Reframe all domain-level quantitative claims as "directional hypotheses." Label tier definitions as "hypothesized." Add required sample size for validation (30+ per cell = 300+ total).
**Acceptance Criteria:** No domain-level CIR value is presented without a sample-size caveat. Tier definitions are labeled "hypothesized" in both deliverables.

### IN-002-QG3: Binary Two-Leg Framing Obscures Continuous Spectrum [CRITICAL]

**Type:** Assumption
**Original Assumption:** LLM reliability failures fall into two distinct categories (Leg 1: confident inaccuracy when training data exists; Leg 2: honest decline when training data is absent).
**Inversion:** LLM reliability operates on a continuous spectrum. A model's familiarity with a topic is not binary (has/lacks training data) but graded (extensive data, moderate data, sparse data, no data). Questions in the "moderate data" zone -- topics that existed before cutoff but have evolved significantly -- would likely show intermediate confidence behavior that fits neither leg cleanly.
**Plausibility:** HIGH -- LLM token prediction operates on continuous probability distributions; there is no architectural mechanism for a binary knowledge/no-knowledge switch. The ITS/PC classification is a methodological convenience imposed by the researchers, not an intrinsic property of the model.
**Confidence:** Low
**Consequence:** The "Two-Leg Thesis" name implies a dichotomy that may not exist. If the reality is a spectrum, the architectural recommendations (binary routing: trust T1-T2, always verify T4-T5) are oversimplified. The most interesting and dangerous zone -- moderate familiarity where the model has some training data but is unsure which snapshot is correct -- is completely unexplored.
**Evidence:** No questions in the test design target the intermediate zone. All ITS questions are clearly in-training-set; all PC questions are clearly post-cutoff. The deliverable never tests a question like "What were the key features of Python 3.11?" where the model has training data but it may be mixed with 3.10 or 3.12 information.
**Dimension:** Internal Consistency
**Mitigation:** Add a section discussing the spectrum possibility. Acknowledge that "Two-Leg" is a simplification. Discuss how intermediate-familiarity questions would be classified. Consider renaming to "Two-Pole Model" to imply endpoints rather than binary categories.
**Acceptance Criteria:** The deliverable acknowledges the spectrum possibility with at least one paragraph. Intermediate-familiarity questions are identified as an untested category.

### IN-003-QG3: Snapshot Problem as Sole Root Cause is Unvalidated [MAJOR]

**Type:** Assumption
**Original Assumption:** The Snapshot Problem (contradictory temporal snapshots in training data) is "the root architectural cause of Leg 1 failures."
**Inversion:** The Snapshot Problem is NOT the sole root cause. Other mechanisms contribute: parameter compression forces lossy encoding of precise values (a model with 70B parameters cannot losslessly store every version number it has ever seen); attention patterns may blur similar but distinct facts (version 0.6.0 vs 1.0.0 of the same library share context and may interfere); RLHF reward hacking may have trained the model to prefer specific-sounding answers over accurate ones; tokenization of numbers and dates introduces quantization artifacts.
**Plausibility:** MODERATE -- these alternative mechanisms are well-documented in the LLM interpretability literature but their relative contribution to Leg 1 errors is unknown.
**Confidence:** Medium
**Consequence:** If the Snapshot Problem is only one of several contributing factors, the mitigation architecture is incomplete. Domain-aware routing addresses the Snapshot Problem (verify fast-evolving domains) but does not address compression artifacts or attention interference, which could produce errors even in stable domains when facts are sufficiently similar to other facts.
**Evidence:** ps-architect-002 states "The Snapshot Problem is not fixable by better training alone" and "the root architectural cause" without exploring alternatives.
**Dimension:** Evidence Quality
**Mitigation:** Add 2+ alternative root cause mechanisms alongside the Snapshot Problem. Reframe as "a primary contributing factor" rather than "the root cause."
**Acceptance Criteria:** Alternative mechanisms are named and briefly described. Causal language is modulated.

### IN-004-QG3: WebSearch Ground Truth Not Validated [MAJOR]

**Type:** Assumption
**Original Assumption:** WebSearch results provide reliable ground truth for scoring Agent A's factual accuracy.
**Inversion:** WebSearch does NOT reliably provide ground truth. Search results can be outdated (cached pages), incorrect (user-generated content), or contradictory (multiple sources disagree). The deliverable scores Agent A against WebSearch results but never validates whether those WebSearch results are themselves correct.
**Plausibility:** MODERATE -- WebSearch is generally more reliable than unverified LLM output for specific factual claims, but it is not infallible. For the specific questions tested (version numbers, dates, counts), official documentation sources exist that could serve as higher-quality ground truth.
**Confidence:** Medium
**Consequence:** FA and CIR scores may contain measurement error. If WebSearch occasionally returns incorrect information, some of Agent A's "errors" may be correct (false negative) and some of Agent A's "correct" answers may actually be wrong (false positive undetected). This does not invalidate the general direction of the findings but undermines the precision of specific scores.
**Evidence:** ps-synthesizer-002 Limitations section mentions "WebSearch itself has accuracy limitations" but treats WebSearch as ground truth everywhere else. No ground truth verification methodology is described.
**Dimension:** Methodological Rigor
**Mitigation:** Document the ground truth verification methodology. Were multiple sources consulted? Were official documentation sources preferred? How were conflicting results resolved?
**Acceptance Criteria:** Ground truth methodology section added. At least one example of source verification is provided.

### IN-005-QG3: Domain Classifier Creates Recursive Reliability Problem [MAJOR]

**Type:** Assumption
**Original Assumption:** The proposed Domain Classifier can reliably assign queries to reliability tiers (T1-T5).
**Inversion:** The Domain Classifier CANNOT reliably assign tiers because it is itself an LLM subject to the same reliability problems the system is designed to mitigate. A T4 query misclassified as T2 will bypass external verification, producing exactly the Leg 1 errors the architecture aims to prevent. Worse, the misclassification will be made with confidence (Leg 1 behavior in the classifier itself).
**Plausibility:** HIGH -- this is a recursive instance of the very problem the deliverable diagnoses. The deliverable acknowledges this as "Open Question Q1" but does not analyze the severity or propose mitigations.
**Confidence:** Low
**Consequence:** The mitigation architecture may have a significant blind spot. If the Domain Classifier has even a 10% misclassification rate for T4 queries, 10% of the highest-risk queries bypass verification. The deliverable proposes no fallback strategy, no classifier confidence threshold, and no analysis of misclassification cost asymmetry.
**Evidence:** ps-architect-002 Open Questions Q1: "If the classifier itself is an LLM, it may have its own Leg 1 errors."
**Dimension:** Actionability
**Mitigation:** Add classifier failure mode analysis. Propose default-to-verification fallback. Analyze cost asymmetry between over-verification (latency) and under-verification (accuracy).
**Acceptance Criteria:** Classifier failure modes are enumerated with proposed mitigations. Cost asymmetry is analyzed.

### IN-006-QG3: "Completely Solves" Contradicted by Own Data [MAJOR]

**Type:** Assumption
**Original Assumption:** "Tool augmentation completely solves [Leg 2]" (ps-synthesizer-002, Leg 2 section).
**Inversion:** Tool augmentation does NOT completely solve Leg 2. The deliverable's own data shows Agent B PC FA ranging from 0.88 (Q12: Python requests 3.0 changes) to 0.95 (Q15: Oscar nominees), not 1.0. Q12's 0.88 FA means approximately 12% of claims in a tool-augmented response about post-cutoff technical changes are still inaccurate.
**Plausibility:** HIGH -- directly contradicted by the deliverable's own scoring data.
**Confidence:** Medium
**Consequence:** The deliverable overstates tool augmentation effectiveness for Leg 2, which undermines its credibility on the more nuanced Leg 1 claims. If the reader discovers the "completely solves" claim is false (by checking Agent B's actual scores), they may discount the entire analysis.
**Evidence:** ps-synthesizer-002 Leg 2 section: "Tool augmentation completely solves it. Agent B with WebSearch achieves 0.91 Factual Accuracy on PC questions." 0.91 is not 1.0; "completely" is not warranted.
**Dimension:** Internal Consistency
**Mitigation:** Replace "completely solves" with "substantially addresses" or "largely resolves." Cite the actual Agent B PC FA range (0.88-0.95).
**Acceptance Criteria:** No claim of "complete" solution. Actual score range cited.

### IN-007-QG3: Jerry "Proof-of-Concept" Claim Unsupported [MAJOR]

**Type:** Assumption
**Original Assumption:** The Jerry Framework "demonstrates a governance-based approach to mitigating LLM unreliability" as a "proof-of-concept."
**Inversion:** The Jerry Framework does NOT demonstrate this because the evidence is a single anecdotal case (McConkey research) with no control condition, no systematic evaluation, and no measurement of governance overhead or error detection rate.
**Plausibility:** HIGH -- "proof-of-concept" implies systematic evaluation. A single anecdote, however vivid, is an "illustrative example" at best.
**Confidence:** Low
**Consequence:** The claim positions the Jerry Framework as having validated its approach, which it has not. This could mislead readers into adopting governance-based architectures based on anecdotal rather than empirical evidence.
**Evidence:** ps-architect-002 section "Jerry Framework as Proof-of-Concept": the only specific evidence is the McConkey case. No error detection rate, no comparison to ungoverned agent outputs, no measurement of governance cost.
**Dimension:** Evidence Quality
**Mitigation:** Rename section to "Jerry Framework as Illustrative Example." Describe what a proper proof-of-concept evaluation would require.
**Acceptance Criteria:** Section title changed. Evaluation requirements described. McConkey case explicitly framed as anecdotal.

---

## Recommendations

### Critical (MUST mitigate before acceptance)

1. **IN-001-QG3:** Reframe all domain-level quantitative claims as directional hypotheses. Label reliability tiers as "hypothesized." Add target validation sample size. This does not require new data -- only honest framing of existing data's limitations.

2. **IN-002-QG3:** Add a "Limitations of the Two-Leg Framing" section acknowledging the spectrum possibility. Discuss intermediate-familiarity questions as an untested category. Modulate "Two-Leg Thesis" language to suggest poles rather than categories.

### Major (SHOULD mitigate)

3. **IN-003-QG3:** Add 2+ alternative root cause mechanisms for Leg 1 alongside the Snapshot Problem. Reframe causal language.

4. **IN-004-QG3:** Document ground truth verification methodology.

5. **IN-005-QG3:** Add Domain Classifier failure mode analysis with fallback strategy and cost asymmetry analysis.

6. **IN-006-QG3:** Replace "completely solves" with accurate characterization. Cite Agent B's actual PC FA range.

7. **IN-007-QG3:** Rename "Proof-of-Concept" to "Illustrative Example." Describe proper evaluation requirements.

### Minor (MAY mitigate)

8. **IN-008-QG3:** Note that Science/Medicine zero-CIR claim rests on maximally stable facts.

9. **IN-009-QG3:** Add caveat about single-model evidence alongside existing Open Question Q2.

---

*Strategy: S-013 Inversion Technique v1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Date: 2026-02-22*
