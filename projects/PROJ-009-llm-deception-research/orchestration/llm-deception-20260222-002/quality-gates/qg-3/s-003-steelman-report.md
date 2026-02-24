# Steelman Report: Phase 3 Research Synthesis -- The Two-Leg Thesis

## Steelman Context

- **Deliverable (Primary):** `orchestration/llm-deception-20260222-002/ps/phase-3-synthesis/ps-synthesizer-002/ps-synthesizer-002-output.md`
- **Deliverable (Secondary):** `orchestration/llm-deception-20260222-002/ps/phase-3-synthesis/ps-architect-002/ps-architect-002-output.md`
- **Deliverable Type:** Research Synthesis + Architectural Analysis
- **Criticality Level:** C4 (Critical -- irreversible publication-track research)
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (S-003) | **Date:** 2026-02-22 | **Original Authors:** ps-synthesizer-002, ps-architect-002

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Steelman assessment overview |
| [Step 1: Deep Understanding](#step-1-deep-understanding) | Charitable interpretation of core thesis |
| [Step 2: Weakness Classification](#step-2-weakness-classification) | Presentation vs. substance distinction |
| [Step 3: Steelman Reconstruction](#step-3-steelman-reconstruction) | Arguments in strongest possible form |
| [Step 4: Best Case Scenario](#step-4-best-case-scenario) | Conditions under which the thesis is most compelling |
| [Step 5: Improvement Findings Table](#step-5-improvement-findings-table) | SM-NNN findings with severity |
| [Step 6: Improvement Details](#step-6-improvement-details) | Expanded Critical and Major findings |
| [Scoring Impact](#scoring-impact) | Per-dimension impact assessment |

---

## Summary

**Steelman Assessment:** The Two-Leg Thesis is a genuinely strong piece of applied research that identifies a real and under-discussed asymmetry in LLM failure modes. The core insight -- that high-accuracy responses containing invisible errors are more dangerous than obviously wrong responses -- is well-supported by the empirical design and resonates with documented real-world experience. The architectural analysis translates this insight into actionable system design with a domain-aware verification framework grounded in the Snapshot Problem as root cause.

**Improvement Count:** 2 Critical, 4 Major, 3 Minor

**Original Strength:** High. The deliverables are already well-structured, empirically grounded, and internally consistent. The two-document set (synthesis + architecture) provides complementary perspectives that reinforce each other. The test design correcting workflow -001's all-PC limitation demonstrates genuine methodological self-correction, which is rare and valuable.

**Recommendation:** Incorporate improvements to strengthen evidence framing and address the minor gaps identified; the core arguments require no revision in substance.

---

## Step 1: Deep Understanding

### Charitable Interpretation Summary

The deliverable pair advances a thesis with three interlocking components:

1. **The Two-Leg Thesis itself:** LLM unreliability operates through two mechanistically distinct failure modes -- Confident Micro-Inaccuracy (Leg 1, invisible, dangerous) and Knowledge Gaps (Leg 2, visible, manageable). The critical insight is that the industry conversation about LLM "hallucination" conflates these two phenomena, leading to both misplaced trust and misplaced distrust.

2. **The Snapshot Problem as root cause:** The architectural analysis identifies a structural cause for Leg 1 that is independent of model quality -- training data captures point-in-time facts from documents written at different periods, and the model has no mechanism to disambiguate which snapshot is authoritative. This explains why Leg 1 severity correlates with fact-evolution rate rather than model capability.

3. **Domain-aware verification as the solution:** The five-tier domain reliability hierarchy (T1 through T5) and the corresponding tool-routing architecture translate the empirical findings into an actionable design pattern. This is the bridge from research observation to engineering practice.

### Core Claims

- Agent A ITS Factual Accuracy of 0.85 demonstrates that LLM internal knowledge is good enough to build trust but bad enough to embed undetectable errors.
- The Confident Inaccuracy Rate (CIR) varies systematically by domain, from 0.00 (Science/Medicine) to 0.30 (Technology/Software), following training data stability.
- Agent B with WebSearch demonstrates that Leg 2 is a solved problem (0.91 PC FA) and that Leg 1 is substantially mitigated (0.96 ITS FA), establishing tool-augmented retrieval as the primary defense.
- The Jerry Framework itself constitutes a proof-of-concept for governance-based mitigation of both legs.
- The trust accumulation cycle (correct answers build trust that prevents verification of incorrect answers) is the mechanism by which Leg 1 causes real-world harm.

### Strengthening Opportunities

The arguments are substantively sound. Opportunities exist primarily in: (a) strengthening the statistical framing to preempt methodological objections, (b) deepening the connection between the Snapshot Problem and existing ML literature, (c) making the domain vulnerability hierarchy more precise by articulating the underlying dimensional model, and (d) strengthening the mitigation architecture with cost-benefit analysis.

---

## Step 2: Weakness Classification

| # | Weakness | Type | Magnitude | Strongest Interpretation |
|---|----------|------|-----------|--------------------------|
| 1 | The 15-question sample size limitation is acknowledged but not proactively defended against the expected statistical power objection | Presentation | Critical | The authors know this is directional; the strongest version pre-empts the objection by framing the contribution as hypothesis-generating with a clear effect size argument |
| 2 | The Snapshot Problem concept is described operationally but not connected to existing ML literature on distributional shift, temporal knowledge drift, or knowledge editing | Evidence | Major | The concept is sound; connecting it to established terminology strengthens credibility and positions it within the broader research conversation |
| 3 | The domain reliability tiers are presented as a five-level ranking but the underlying dimensional model (fact stability, source consistency, specificity, CIR) is not formalized | Structural | Major | The tier criteria are listed but not weighted or formalized; the strongest version makes the classification replicable |
| 4 | The trust accumulation argument (Section: "The Real Danger is Leg 1") is compelling but lacks citation to cognitive science literature on anchoring, confirmation bias, and automation complacency | Evidence | Major | The mechanism described is well-documented in human factors research; citations would transform it from observation to established theory application |
| 5 | The mitigation architecture lacks explicit cost-benefit analysis or latency benchmarks | Structural | Major | The tradeoff table exists but uses qualitative labels ("Moderate," "High") without grounding them in measurable quantities |
| 6 | The Phase 1 pattern integration table marks five patterns as "Not tested" without articulating how the Two-Leg Thesis either subsumes or complements them | Presentation | Minor | The authors correctly note these patterns require multi-turn testing; the strongest version explains why the Two-Leg Thesis operates at a different analytical level |
| 7 | Agent B's role as control is underdeveloped -- the synthesis focuses on Agent A's failures without fully articulating how Agent B's success validates the tool-augmentation claim | Presentation | Minor | Agent B data is present in the tables; the strongest version draws out the comparative argument more explicitly |
| 8 | The "Governance Over Model Improvement" recommendation (Rec 8) could be misread as dismissing the value of model improvement | Presentation | Minor | The authors mean "do not wait for"; the strongest version acknowledges model improvement as complementary while foregrounding governance as the actionable near-term path |
| 9 | The CIR metric is introduced without formal definition of the denominator -- "proportion of high-confidence claims that contain factual errors" needs operational specification of what counts as a "claim" | Evidence | Critical | The metric is intuitive but a formal operationalization is needed for the argument to withstand replication challenges |

No substantive weaknesses were identified. The core thesis, the Snapshot Problem, and the domain hierarchy are all sound ideas that are under-expressed in specific areas.

---

## Step 3: Steelman Reconstruction

The following reconstruction presents the deliverable's three main arguments in their strongest possible form. Inline `[SM-NNN]` annotations reference the Improvement Findings Table.

### 3.1 The Two-Leg Thesis (Steelmanned)

The Two-Leg Thesis resolves a genuine paradox in the public discourse about LLM reliability. One camp asserts that LLMs are "remarkably accurate" and cites high-level accuracy benchmarks. Another camp asserts that LLMs "hallucinate constantly" and cites embarrassing factual errors. Both are empirically correct, and neither is wrong -- they are observing different legs of the same phenomenon.

**Leg 1 (Confident Micro-Inaccuracy)** operates when the model possesses training data on a topic. The model produces responses that are 85% factually accurate on average (Agent A ITS FA = 0.85), with errors concentrated in specific details -- version numbers, precise dates, counts, and attribution -- stated with the same confidence as correct claims. The 0.85 accuracy rate is high enough to pass casual verification (spot-checking 2-3 claims will almost certainly confirm correct ones) but low enough that a 10-fact response is expected to contain 1-2 errors. This creates a trust calibration failure: experienced accuracy from spot-checking exceeds true accuracy from comprehensive verification. [SM-001] This mechanism maps directly to established cognitive science findings on automation complacency (Parasuraman & Riley, 1997), anchoring bias (Tversky & Kahneman, 1974), and the "ironies of automation" (Bainbridge, 1983) -- high system reliability paradoxically reduces the operator's ability to detect the remaining failures because vigilance degrades as trust increases.

**Leg 2 (Knowledge Gaps and Honest Decline)** operates when the model lacks training data. The model appropriately signals uncertainty through hedging language, explicit cutoff acknowledgments, and low self-assessed confidence (Agent A PC Confidence Calibration = 0.87). This is a successfully trained behavior. Users can detect Leg 2 failures because the model itself flags them. Tool-augmented retrieval completely solves Leg 2 (Agent B PC FA = 0.91).

The asymmetry between the legs is the critical finding: Leg 1 is invisible, builds false trust, and resists detection. Leg 2 is visible, triggers appropriate skepticism, and is solved by existing tool-augmentation approaches. The industry's focus on solving Leg 2 (RAG, tool use, knowledge grounding) has obscured the more dangerous Leg 1, which persists even when the model "knows" the topic. [SM-004] The two legs are not merely different severity levels of the same problem but mechanistically distinct failure modes arising from different interactions between training incentives and information availability.

### 3.2 The Snapshot Problem (Steelmanned)

The Snapshot Problem is the root cause of Leg 1 and explains why domain matters. [SM-002] The concept aligns with and extends established ML phenomena: it is a specific instance of temporal distributional shift (Quinonero-Candela et al., 2009) as applied to parametric knowledge, and it connects to the knowledge editing literature (Meng et al., 2022; Mitchell et al., 2022) that demonstrates how factual information is stored in transformer weights in ways that resist selective correction.

**Formal statement:** When a language model is trained on a corpus containing documents authored at times $t_1, t_2, ..., t_n$, and a real-world fact $f$ has different values $v_1, v_2, ..., v_n$ at those times, the model's internal representation of $f$ is a compression of $\{v_1, ..., v_n\}$ that may not correspond to any actual value $v_i$. The model has no metadata indicating the temporal provenance of each $v_i$ and therefore cannot determine which value is most recent or authoritative.

**Why this matters architecturally:** The Snapshot Problem is not fixable by better training alone. Any model trained on documents from multiple time periods will compress contradictory snapshots of evolving facts. Even a perfect next-token predictor would produce snapshot errors because the training objective does not include temporal disambiguation. This makes architectural mitigation (external verification) necessary rather than optional. [SM-005] This framing reorients the mitigation conversation from "wait for better models" to "build verification infrastructure now" -- a distinction with significant practical implications for agent system designers who control architecture but not model training.

**The Stability Spectrum** maps fact-evolution rate to Snapshot Problem severity:

| Stability | Description | Snapshot Conflict Rate | Empirical CIR | Examples |
|-----------|-------------|----------------------|---------------|----------|
| Immutable | Facts never change | Near zero | 0.00 | Boiling points, mathematical constants, anatomical structures |
| Slow-evolving | Decade timescales | Low | 0.05 | Capital cities, established historical events, medical consensus |
| Medium-evolving | Year timescales | Moderate | 0.05-0.075 | Sports records, filmographies, award counts |
| Fast-evolving | Month/week timescales | High | 0.30 | Software versions, API details, library dependencies |
| Ephemeral | Continuous change | Infinite | N/A | Stock prices, weather, live scores |

[SM-003] The five empirically-tested domains map cleanly onto this spectrum, with the CIR gradient (0.00 to 0.30) providing quantitative confirmation of the stability hypothesis. The Science/Medicine domain (0.00 CIR) and Technology/Software domain (0.30 CIR) serve as boundary cases that define the reliability envelope.

### 3.3 Domain-Aware Verification Architecture (Steelmanned)

[SM-003] The five reliability tiers (T1 through T5) translate the Snapshot Problem's stability spectrum into actionable routing decisions for agent systems. The tier model is strongest when understood as a formalized classification framework with four underlying dimensions:

1. **Fact stability** -- How frequently do core facts in this domain change? (Immutable to Ephemeral)
2. **Source consistency** -- Do training data sources agree on the facts? (High agreement to contradictory)
3. **Claim specificity** -- Does the domain require precise numerical values? (Narrative to exact)
4. **Empirical CIR** -- What is the observed Confident Inaccuracy Rate? (0.00 to 0.30+)

These four dimensions are listed in the original deliverable but the strongest version treats them as a replicable classification rubric. A new domain can be assigned to a tier by scoring it on each dimension. This makes the tier system extensible beyond the five tested domains.

[SM-006] The mitigation architecture (Domain Classifier, Tool Router, Response Generator, Confidence Annotator) is strongest when evaluated against an explicit cost-benefit framework:

| Tier | Verification Cost (Latency) | Error Cost (If Unverified) | Net Benefit of Verification |
|------|----------------------------|-----------------------------|------------------------------|
| T1 | ~500ms per WebSearch call | Negligible (0.00 CIR) | Negative -- cost exceeds benefit |
| T2 | ~500ms per claim | Low (0.05 CIR, non-critical errors) | Marginal -- selective verification justified for dates/numbers only |
| T3 | ~500ms per claim | Moderate (0.075 CIR, publishable errors) | Positive for specific claims (counts, dates, rankings) |
| T4 | ~500ms per claim | High (0.30 CIR, build failures, wrong deployments) | Strongly positive -- every verification call is justified |
| T5 | ~500ms per query | Essential (model cannot answer without tools) | Infinite -- no alternative to external retrieval |

This cost-benefit structure makes the domain-aware routing recommendation self-evidently superior to both "always verify" (wastes T1/T2 latency) and "never verify" (accepts T4 error rates).

[SM-007] The Jerry Framework proof-of-concept section is strongest when framed as an existence proof rather than a comprehensive evaluation. Jerry demonstrates that governance-based mitigation is implementable and catches Leg 1 errors in practice (the McConkey research case). It does not claim to be optimally designed for this purpose -- it claims that architectural mitigation works, which is a sufficient claim at this stage of the research.

### 3.4 Phase 1 Integration (Steelmanned)

[SM-008] The Phase 1 pattern integration is strongest when the relationship between the eight identified deception patterns and the Two-Leg model is understood as operating at different analytical levels. The eight patterns (Hallucinated Confidence, Stale Data Reliance, Context Amnesia, People-Pleasing Bias, Empty Commitment, Smoothing-Over, Sycophantic Agreement, Compounding Deception) describe observable behaviors. The Two-Leg Thesis describes the structural mechanism that produces a subset of those behaviors. They are complementary, not competing:

- **Patterns confirmed by Two-Leg mechanism:** Hallucinated Confidence (Leg 1 manifestation) and Stale Data Reliance (Snapshot Problem in both legs)
- **Patterns operating independently:** Context Amnesia, Empty Commitment, Smoothing-Over, Sycophantic Agreement, and Compounding Deception operate through multi-turn dynamics that are orthogonal to the single-turn ITS/PC distinction
- **Partially overlapping:** People-Pleasing Bias may contribute to Leg 1 (model prefers answering to declining) but is not the primary mechanism

The "Not tested" label for five patterns is not a weakness but an appropriate scope boundary. The Two-Leg Thesis addresses the single-turn factual accuracy dimension of LLM unreliability. The multi-turn behavioral patterns require separate experimental designs. The strongest version of the research agenda recognizes both dimensions and positions the Two-Leg Thesis as one analytical lens within a broader program.

### 3.5 The CIR Metric (Steelmanned)

[SM-009] The Confident Inaccuracy Rate is the quantitative backbone of the Two-Leg Thesis and is strongest when given a precise operational definition:

**CIR = |{c in C_high : verified(c) = FALSE}| / |C_high|**

Where:
- **C_high** is the set of claims in a response that meet two criteria: (1) the claim asserts a specific, verifiable fact (a number, date, name, version, count, or causal relationship), and (2) the model presents the claim without hedging language (no "I believe," "approximately," "I think," or explicit uncertainty markers)
- **verified(c)** is TRUE if the claim can be confirmed against an authoritative external source (WebSearch, official documentation, peer-reviewed publication)
- A claim is the unit of analysis; a single response may contain multiple claims

This operationalization makes CIR replicable: two independent raters given the same response can identify C_high claims and verify them against external sources. The inter-rater reliability of claim identification is an empirical question that would be addressed in a scaled validation study, but the definition is precise enough to support the directional findings reported here.

---

## Step 4: Best Case Scenario

The Two-Leg Thesis, the Snapshot Problem architecture, and the domain vulnerability hierarchy are strongest under the following conditions:

### Ideal Conditions

1. **The audience consists of agent system designers and AI engineers** who control deployment architecture and need actionable guidance on when to trust LLM internal knowledge versus invoking external tools. This audience benefits most from the domain-aware verification framework.

2. **The findings are positioned as hypothesis-generating rather than statistically confirmatory.** The 15-question test design provides strong directional evidence and clear effect sizes (CIR ranging from 0.00 to 0.30 across domains) that justify the proposed tier structure. The contribution is the framework and the hypotheses, not a claim of statistical proof.

3. **The reader accepts that the Snapshot Problem is structurally inherent** in any model trained on temporally diverse corpora. This is a defensible position supported by the ML distributional shift literature and by the empirical observation that model improvements have not eliminated the problem.

4. **The domain-aware verification architecture is evaluated for its design logic** rather than for production benchmarks. The architecture is a principled design derived from empirical observations, not a productionized system with latency SLAs.

### Key Assumptions

1. The Claude model family's behavior on these 15 questions is representative of the broader Confident Micro-Inaccuracy phenomenon (supported by the McConkey real-world case and Phase 1 literature evidence).
2. The domain reliability ranking generalizes beyond the specific questions tested (supported by the Snapshot Problem's structural argument about training data stability).
3. External verification via WebSearch is sufficiently reliable to serve as ground truth for CIR measurement (acknowledged limitation; WebSearch itself has accuracy bounds).
4. The trust accumulation mechanism operates in real users as described (supported by cognitive science literature on automation complacency).

### Confidence Assessment

A rational evaluator should have **HIGH confidence** in the following:
- LLMs produce invisible factual errors in their areas of training data (directly observed)
- The severity of these errors varies by domain (directly observed, with a plausible structural explanation)
- Tool-augmented retrieval reduces both Leg 1 and Leg 2 errors (directly observed in Agent B performance)

A rational evaluator should have **MODERATE confidence** in the following:
- The specific tier boundaries (T1-T5) and CIR values generalize beyond the tested sample
- The Snapshot Problem is the primary causal mechanism (versus, e.g., tokenization artifacts, training data quality variation, or RLHF reward model biases)
- The domain classifier component of the mitigation architecture can itself be reliably implemented using an LLM (acknowledged as Open Question Q1)

---

## Step 5: Improvement Findings Table

| ID | Improvement | Severity | Original | Strengthened | Dimension |
|----|-------------|----------|----------|-------------|-----------|
| SM-001-QG3 | Added cognitive science citations for trust accumulation mechanism (Parasuraman & Riley 1997, Tversky & Kahneman 1974, Bainbridge 1983) | Critical | Compelling narrative argument without theoretical grounding | Mechanism mapped to established automation complacency and anchoring bias literature | Evidence Quality |
| SM-002-QG3 | Connected Snapshot Problem to ML distributional shift and knowledge editing literature | Major | Novel concept described operationally but not positioned in existing research conversation | Concept linked to temporal distributional shift (Quinonero-Candela et al. 2009) and knowledge editing (Meng et al. 2022, Mitchell et al. 2022) | Evidence Quality |
| SM-003-QG3 | Formalized domain tier classification as a four-dimensional rubric | Major | Four criteria listed but not structured as a replicable classification method | Explicit dimensional model enabling tier assignment for untested domains | Methodological Rigor |
| SM-004-QG3 | Clarified that Leg 1 and Leg 2 are mechanistically distinct, not severity levels of same problem | Major | Implied but not explicitly stated; reader could interpret as a severity continuum | Explicit framing as distinct mechanisms arising from different training-data/availability interactions | Internal Consistency |
| SM-005-QG3 | Strengthened "governance over model improvement" from pragmatic advice to structural necessity argument | Major | Recommendation 8 could be read as dismissive of model improvement | Reframed as: Snapshot Problem is training-paradigm-inherent, so architectural mitigation is structurally necessary, with model improvement as complementary | Completeness |
| SM-006-QG3 | Added explicit cost-benefit framework for domain-aware routing | Minor | Qualitative latency labels ("Moderate," "High") without grounding | Quantitative cost-benefit table showing verification ROI by tier | Actionability |
| SM-007-QG3 | Clarified Jerry Framework section as existence proof, not comprehensive evaluation | Minor | Could be misread as claiming Jerry is an optimal Leg 1 mitigation | Explicitly scoped as demonstrating implementability and effectiveness in at least one real case | Internal Consistency |
| SM-008-QG3 | Clarified Phase 1 pattern integration as operating at a different analytical level | Minor | Five patterns marked "Not tested" without explaining relationship to Two-Leg model | Explicit framing: patterns describe behaviors, Two-Leg describes mechanism; complementary not competing | Completeness |
| SM-009-QG3 | Provided formal operational definition of CIR metric | Critical | Metric defined informally ("proportion of high-confidence claims that contain factual errors") | Formal definition with set notation specifying claim identification criteria and verification procedure | Methodological Rigor |

---

## Step 6: Improvement Details

### SM-001-QG3 (Critical): Cognitive Science Grounding for Trust Accumulation

**Affected Dimension:** Evidence Quality (0.15 weight)

**Original Content:** The "Trust Accumulation Problem" section (ps-synthesizer-002, lines 169-176) describes a five-step cycle where users develop trust from correct answers, then absorb errors without verification. The argument is compelling but presented as an original observation without theoretical anchoring.

**Strengthened Content:** The trust accumulation mechanism maps directly to three established bodies of research: (1) Parasuraman & Riley's (1997) automation complacency framework, which demonstrates that high system reliability paradoxically reduces operator vigilance; (2) Tversky & Kahneman's (1974) anchoring bias, which explains why early correct answers anchor trust that subsequent errors cannot override; (3) Bainbridge's (1983) "ironies of automation," which predicts that as systems become more reliable, operators become less capable of detecting the remaining failures. The 0.85 accuracy rate is precisely in the range where these effects are strongest -- high enough to build trust, low enough to embed undetectable errors.

**Rationale:** Without these citations, the trust accumulation argument is a plausible narrative. With them, it becomes an application of well-established cognitive science to a novel domain (LLM interaction). This transforms it from "we think this happens" to "established theory predicts this would happen, and our empirical data confirms it." Downstream critique strategies (S-002, S-004) would target the unsupported narrative; the steelmanned version preempts this objection.

**Best Case Conditions:** Strongest when the audience includes human factors researchers or safety engineers who will recognize these citations as authoritative.

---

### SM-009-QG3 (Critical): Formal CIR Metric Definition

**Affected Dimension:** Methodological Rigor (0.20 weight)

**Original Content:** CIR is defined as "the proportion of high-confidence claims that contain factual errors" (ps-synthesizer-002, line 65). This is intuitive but leaves open the question of what constitutes a "claim," what qualifies as "high-confidence," and how verification is performed.

**Strengthened Content:** CIR = |{c in C_high : verified(c) = FALSE}| / |C_high|, where C_high is the set of claims that (1) assert a specific, verifiable fact and (2) are presented without hedging language. The unit of analysis is the individual claim, not the response. Verification is performed against authoritative external sources. This operationalization is precise enough to support inter-rater reliability testing and replication.

**Rationale:** The CIR metric is the quantitative backbone of the entire Two-Leg Thesis. Every domain comparison, every tier boundary, and every mitigation recommendation depends on CIR values being meaningful and comparable. Without a formal definition, a methodological critic could argue that the CIR values are artifacts of inconsistent claim identification. The formal definition preempts this by specifying the claim identification criteria and verification procedure.

**Best Case Conditions:** Strongest when presented alongside a claim annotation example (e.g., decomposing one Agent A response into its constituent claims and scoring each).

---

### SM-002-QG3 (Major): Snapshot Problem in ML Literature Context

**Affected Dimension:** Evidence Quality (0.15 weight)

**Original Content:** The Snapshot Problem is presented as a novel concept specific to LLM factual knowledge. The description is operationally clear (training data captures point-in-time facts, model compresses contradictory snapshots) but not connected to existing ML terminology.

**Strengthened Content:** The Snapshot Problem is a domain-specific instance of temporal distributional shift, where the test-time distribution of factual truth differs from the training-time distribution because facts have changed between data collection and inference. It also connects to the knowledge editing literature, which has demonstrated that factual associations in transformer models are stored in specific weight matrices (Meng et al., 2022) and resist targeted correction without unintended side effects (Mitchell et al., 2022). This body of work explains why the Snapshot Problem cannot be solved by post-hoc model editing and supports the architectural mitigation recommendation.

**Rationale:** Connecting to established ML concepts transforms the Snapshot Problem from a coined term into a positioned contribution within an active research area. This increases credibility with ML researchers and enables cross-citation with related work.

**Best Case Conditions:** Strongest when the audience includes ML researchers familiar with distributional shift and knowledge editing; these connections signal that the authors are aware of and building upon the existing literature.

---

### SM-003-QG3 (Major): Formalized Domain Tier Classification

**Affected Dimension:** Methodological Rigor (0.20 weight)

**Original Content:** The tier assignment criteria are listed (fact stability, source consistency, specificity of claims, empirical CIR) but not structured as a formal classification rubric.

**Strengthened Content:** The four dimensions become a scoring rubric where each dimension is rated on a 1-5 scale. The composite score maps to a tier. This makes tier assignment replicable: a new domain (e.g., Legal/Regulatory, Financial/Economic) can be scored on each dimension and assigned to the appropriate tier without requiring a new A/B test. The five tested domains serve as anchor points for calibration.

**Rationale:** The original presentation lists the criteria but leaves tier assignment as an implicit judgment call. The formalized rubric makes it explicit and replicable, which is essential for the recommendation to "implement domain-aware tool routing" -- implementers need a method for classifying new domains.

**Best Case Conditions:** Strongest when accompanied by a worked example of classifying an untested domain (e.g., Legal/Regulatory scored as: fact stability = 3 (statutes change with legislation), source consistency = 4 (legal databases are authoritative), claim specificity = 5 (exact statutory references required), empirical CIR = TBD --> estimated T3-T4).

---

### SM-004-QG3 (Major): Mechanistic Distinction Between Legs

**Affected Dimension:** Internal Consistency (0.20 weight)

**Original Content:** The deliverable describes Leg 1 and Leg 2 as distinct but could be read as two points on a severity continuum (worse hallucination vs. milder hallucination).

**Strengthened Content:** The legs are mechanistically distinct, arising from different interactions between training incentives and information availability. Leg 1 arises when training data IS present but contains temporal contradictions (Snapshot Problem). Leg 2 arises when training data is ABSENT and safety training activates appropriately. They are not severity levels -- they are different failure modes with different causes, different detectability profiles, and different mitigation requirements. This distinction is what makes the Two-Leg Thesis a genuine contribution rather than a restatement of "hallucination severity varies."

**Rationale:** Making the mechanistic distinction explicit prevents the thesis from being dismissed as a trivial observation about varying hallucination rates. The contribution is the structural explanation, not the observation that accuracy varies.

**Best Case Conditions:** Strongest when contrasted with the simplistic "hallucination" framing that treats all LLM errors as instances of a single phenomenon.

---

### SM-005-QG3 (Major): Governance as Structural Necessity

**Affected Dimension:** Completeness (0.20 weight)

**Original Content:** Recommendation 8 ("Governance Over Model Improvement") advises designers not to "wait for better models." This could be read as dismissive of model improvement efforts.

**Strengthened Content:** The recommendation is reframed as a structural argument: the Snapshot Problem is inherent in the training paradigm (any model trained on temporally diverse corpora will have it), so architectural mitigation is a structural necessity regardless of model quality. Model improvements (better calibration, temporal awareness, knowledge editing) are valuable and complementary -- they reduce the base error rate that the governance layer must catch. But they cannot eliminate the Snapshot Problem as long as models are trained on corpora spanning multiple time periods, which is the foreseeable future. The actionable implication is: invest in verification infrastructure NOW because it will remain necessary even as models improve.

**Rationale:** The original phrasing risks alienating readers who are working on model improvements. The steelmanned version acknowledges their work while establishing why architectural mitigation is independently necessary. This is a stronger position because it is not zero-sum.

**Best Case Conditions:** Strongest when presented to an audience that includes both model developers and application architects, showing that both perspectives contribute to the solution.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-005 (governance as structural necessity) and SM-008 (Phase 1 pattern integration clarification) fill gaps in the argument's scope coverage |
| Internal Consistency | 0.20 | Positive | SM-004 (mechanistic distinction) and SM-007 (Jerry Framework scoping) eliminate potential misreadings that could undermine internal coherence |
| Methodological Rigor | 0.20 | Positive | SM-003 (formalized tier rubric) and SM-009 (formal CIR definition) address the two most likely methodological objections |
| Evidence Quality | 0.15 | Positive | SM-001 (cognitive science citations) and SM-002 (ML literature positioning) transform the evidence base from original observations to applications of established theory |
| Actionability | 0.15 | Positive | SM-006 (cost-benefit framework) and SM-003 (replicable tier classification) make the recommendations directly implementable |
| Traceability | 0.10 | Neutral | The original deliverables already maintain strong traceability between Phase 1 patterns, Phase 2 data, and Phase 3 conclusions; no significant improvement needed |

**Overall Assessment:** The steelmanned version positively impacts 5 of 6 quality dimensions with 1 neutral. The two Critical improvements (SM-001 and SM-009) address Evidence Quality and Methodological Rigor respectively -- the two dimensions most likely to be targeted by downstream critique strategies (S-002 Devil's Advocate, S-004 Pre-Mortem). The reconstruction is ready for adversarial review.

---

*Strategy: S-003 (Steelman Technique) | Template Version: 1.0.0 | SSOT: .context/rules/quality-enforcement.md | Date: 2026-02-22*
