---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Risk Register: Adversarial Strategy Adoption Risk Assessment

<!--
DOCUMENT-ID: FEAT-004:EN-302:TASK-002
AUTHOR: nse-risk agent (v2.1.0)
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-302 (Strategy Selection & Decision Framework)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
-->

> **Project:** PROJ-001-oss-release
> **Entry:** EN-302 / TASK-002
> **Date:** 2026-02-13
> **Status:** Active
> **Agent:** nse-risk v2.1.0
> **Input:** TASK-006 revised catalog (v1.1.0) of 15 adversarial strategies

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What are the top risks and what are we doing about them? |
| [Risk Methodology](#risk-methodology) | Scales, categories, and FMEA-style approach used |
| [L1: Risk Register Detail](#l1-risk-register-detail) | Full risk matrix for all 15 strategies across 7 risk categories |
| [Per-Strategy Risk Profiles](#per-strategy-risk-profiles) | Detailed risk analysis per strategy with If-Then statements |
| [L2: Risk Portfolio Analysis](#l2-risk-portfolio-analysis) | Systemic risks, cross-strategy patterns, portfolio view |
| [Risk-Based Recommendations](#risk-based-recommendations) | Adopt/mitigate/reject recommendations per strategy |
| [References](#references) | NASA standards and source citations |

---

## L0: Executive Summary

**Risk Portfolio:** 3 RED | 18 YELLOW | 84 GREEN (across 105 risk assessments: 15 strategies x 7 categories)

This risk assessment evaluates the adoption of 15 adversarial review strategies into Jerry's quality framework. The assessment examines seven risk categories per strategy: False Positive, False Negative, Context Window, Integration, Quality Regression, Platform, and Composability.

**Key findings:**

1. **No strategy has an unacceptable overall risk profile.** All 15 strategies are adoptable with appropriate mitigation. However, three specific strategy-category combinations score RED and require immediate mitigation before deployment.

2. **Context Window risk is the dominant systemic concern.** Three strategies (S-009 Multi-Agent Debate, S-015 Progressive Adversarial Escalation, S-005 Dialectical Inquiry) consume large token budgets that directly contribute to context rot -- Jerry's core problem.

3. **Shared Model Bias is a cross-cutting risk.** Six strategies rely on self-critique (S-007, S-010, S-011, S-013, S-014, S-015), creating correlated failure modes. This is documented as a systemic risk in the catalog (v1.1.0 DA-002) but must be actively managed during adoption.

4. **Lowest-risk strategies** (strong adoption candidates): S-003 Steelman, S-013 Inversion, S-010 Self-Refine, S-002 Devil's Advocate, S-014 LLM-as-Judge.

5. **Highest-risk strategies** (require special mitigation): S-009 Multi-Agent Debate, S-015 Progressive Adversarial Escalation, S-005 Dialectical Inquiry.

**RED RISK ALERTS:**

- **R-009-CW**: S-009 Multi-Agent Debate context window consumption -- Score: 20 -- Requires token budget caps and selective deployment
- **R-015-CW**: S-015 Progressive Adversarial Escalation context window consumption -- Score: 16 -- Requires escalation budget limits and early termination
- **R-005-CW**: S-005 Dialectical Inquiry context window consumption -- Score: 16 -- Requires scope constraints and synthesis length limits

---

## Risk Methodology

### Likelihood Scale (1-5, per NPR 8000.4C)

| Rating | Name | Description | Probability |
|--------|------|-------------|-------------|
| 1 | Rare | Highly unlikely to occur in normal use | <10% |
| 2 | Unlikely | Could occur but not expected in typical workflows | 10-25% |
| 3 | Possible | May occur in some deployment contexts | 25-50% |
| 4 | Likely | Probably will occur in regular use | 50-75% |
| 5 | Almost Certain | Expected to occur in most deployments | >75% |

### Impact Scale (1-5, per NPR 8000.4C)

| Rating | Name | Description |
|--------|------|-------------|
| 1 | Minimal | Negligible effect on quality framework operation |
| 2 | Minor | Slight degradation; easily correctable |
| 3 | Moderate | Noticeable quality impact; requires intervention |
| 4 | Major | Significant quality framework degradation; blocks workflows |
| 5 | Critical | Quality framework failure; incorrect results accepted or correct results rejected |

### Risk Level Thresholds

| Score Range | Level | Response |
|-------------|-------|----------|
| 1-7 | GREEN | Accept and monitor |
| 8-15 | YELLOW | Mitigate and monitor |
| 16-25 | RED | Immediate action required before deployment |

### Risk Categories Evaluated

| Category | Code | Description |
|----------|------|-------------|
| **False Positive** | FP | Strategy identifies issues that are not real problems (over-criticism) |
| **False Negative** | FN | Strategy misses real issues (under-criticism) |
| **Context Window** | CW | Strategy consumes excessive tokens, contributing to context rot |
| **Integration** | INT | Difficulty integrating with Jerry's agent architecture (P-003 compliance) |
| **Quality Regression** | QR | Strategy degrades rather than improves quality |
| **Platform** | PLT | Strategy behavior varies across macOS/Windows/Linux |
| **Composability** | CMP | Strategy conflicts with or undermines other strategies |

### FMEA Alignment

This assessment uses a Risk Matrix analysis (L x I = Risk Score) aligned with NPR 8000.4C, with a supplementary Detection rating for YELLOW and RED risks to support prioritization. This hybrid approach was chosen over full FMEA (S x O x D = RPN) because: (a) the 5x5 L x I matrix aligns directly with NASA risk management practices, (b) full S x O x D scores would introduce false precision for risks that are themselves assessments of strategies not yet deployed, and (c) the Detection dimension is most valuable for differentiating YELLOW/RED risks where detection capability materially affects risk prioritization.

- **Severity** maps to Impact (I, 1-5)
- **Occurrence** maps to Likelihood (L, 1-5)
- **Detection** (Det): For YELLOW and RED risks, a supplementary Detection rating is provided using H/M/L scale:
  - **H (High)** = Risk is readily detectable through existing monitoring, automated tests, or output inspection (e.g., token counting, linter output)
  - **M (Medium)** = Risk is detectable through targeted review or calibration checks but not automatically surfaced (e.g., rubric calibration audits, human spot-checks)
  - **L (Low)** = Risk is difficult to detect because the detecting mechanism shares the same blind spot or the failure mode is subtle (e.g., shared-model-bias correlated false negatives, constitution gaming)
- **Risk Priority** = Likelihood x Impact (simplified from RPN for 5x5 matrix compatibility). Detection supplements prioritization qualitatively: two YELLOW risks with the same L x I should be prioritized differently if one has High detection capability and the other has Low.

### Residual Risk Methodology

Residual risk scores are decomposed into Residual Likelihood (R-L) and Residual Impact (R-I) with a brief note on which mitigations affect which factor. Residual Score = R-L x R-I. This decomposition improves traceability by showing exactly how mitigations reduce risk.

---

## L1: Risk Register Detail

### Master Risk Matrix

| Risk ID | Strategy | Category | Risk Statement | L | I | Score | Level | Det | Mitigation | Residual (R-L x R-I) |
|---------|----------|----------|----------------|---|---|-------|-------|-----|------------|----------------------|
| R-001-FP | S-001 Red Team | False Positive | If Red Team adopts an unrealistic adversary model, then it will flag non-issues as vulnerabilities | 3 | 3 | 9 | YELLOW | M | Define adversary capability constraints; require realism justification | 6 (R-L=2, R-I=3: constraints reduce occurrence; impact unchanged) |
| R-001-FN | S-001 Red Team | False Negative | If the Red Team fails to model the correct adversary, then real vulnerabilities will be missed | 2 | 4 | 8 | YELLOW | M | Use multiple adversary profiles; cross-reference with FMEA (S-012) | 4 (R-L=1, R-I=4: multiple profiles reduce occurrence; impact unchanged) |
| R-001-CW | S-001 Red Team | Context Window | If Red Team generates extensive vulnerability reports, then context window fills rapidly | 3 | 3 | 9 | YELLOW | H | Cap vulnerability report length; summarize findings hierarchically | 4 (R-L=2, R-I=2: caps reduce occurrence and severity) |
| R-001-INT | S-001 Red Team | Integration | If Red Team requires deeply independent agents, then P-003 (no recursive subagents) may be strained | 2 | 3 | 6 | GREEN | -- | Implement as single-level orchestrator-to-worker; no nested spawning | 2 (GREEN) |
| R-001-QR | S-001 Red Team | Quality Regression | If Red Team is applied to early-stage work, then premature adversarial pressure destroys nascent ideas | 3 | 3 | 9 | YELLOW | H | Gate Red Team behind S-015 Level 4; only for mature artifacts | 4 (R-L=2, R-I=2: gating eliminates most occurrences; impact reduced via maturity) |
| R-001-PLT | S-001 Red Team | Platform | If adversary modeling references OS-specific attack vectors, then findings may not generalize cross-platform | 1 | 2 | 2 | GREEN | -- | Specify platform scope in Red Team charter | 1 (GREEN) |
| R-001-CMP | S-001 Red Team | Composability | If Red Team findings conflict with Steelman (S-003) charitable interpretation, then review produces contradictory signals | 2 | 2 | 4 | GREEN | -- | Sequence S-003 before S-001; Steelman ensures fair baseline before adversarial challenge | 2 (GREEN) |
| R-002-FP | S-002 Devil's Advocate | False Positive | If Devil's Advocate challenges become performative, then token dissent generates noise without value | 3 | 2 | 6 | GREEN | -- | Require DA to cite specific evidence for each counterargument | 3 (GREEN) |
| R-002-FN | S-002 Devil's Advocate | False Negative | If DA only challenges the conclusion but not underlying assumptions, then foundational flaws are missed | 2 | 3 | 6 | GREEN | -- | Pair DA with Socratic Method (S-008) which probes assumptions | 3 (GREEN) |
| R-002-CW | S-002 Devil's Advocate | Context Window | If DA countercase is verbose, then context fills with adversarial content | 2 | 2 | 4 | GREEN | -- | Cap countercase to structured summary format | 2 (GREEN) |
| R-002-INT | S-002 Devil's Advocate | Integration | If DA requires a genuinely empowered dissenter role, then LLM compliance training may weaken adversarial stance | 2 | 3 | 6 | GREEN | -- | Use explicit adversarial persona prompt; temperature adjustment | 3 (GREEN) |
| R-002-QR | S-002 Devil's Advocate | Quality Regression | If DA is applied without subsequent reconciliation, then the creator may abandon valid positions | 2 | 2 | 4 | GREEN | -- | Require formal reconciliation step after DA challenge | 2 (GREEN) |
| R-002-PLT | S-002 Devil's Advocate | Platform | If DA references platform-specific patterns, then critique may not be portable | 1 | 1 | 1 | GREEN | -- | N/A -- DA operates at reasoning level, not platform level | 1 (GREEN) |
| R-002-CMP | S-002 Devil's Advocate | Composability | If DA contradicts Steelman (S-003), then review sends mixed signals | 2 | 2 | 4 | GREEN | -- | S-003 runs first (steelman-then-critique protocol) | 2 (GREEN) |
| R-003-FP | S-003 Steelman | False Positive | If steelmanning adds assumptions the author did not intend, then critique targets a fabricated argument | 2 | 2 | 4 | GREEN | -- | Include verification step: confirm steelmanned version with creator | 2 (GREEN) |
| R-003-FN | S-003 Steelman | False Negative | If steelmanning is too charitable, then genuine weaknesses are obscured | 2 | 3 | 6 | GREEN | -- | Always pair Steelman with subsequent critique phase; never standalone | 3 (GREEN) |
| R-003-CW | S-003 Steelman | Context Window | If steelmanning adds ~0.5 agent pass of content, then context window incrementally fills | 1 | 2 | 2 | GREEN | -- | Minimal overhead; no specific mitigation needed | 1 (GREEN) |
| R-003-INT | S-003 Steelman | Integration | If Steelman requires pre-critique prompt insertion, then prompt templates need modification | 1 | 1 | 1 | GREEN | -- | Simple prompt engineering; no architectural change required | 1 (GREEN) |
| R-003-QR | S-003 Steelman | Quality Regression | If over-steelmanning causes reviewers to accept weak arguments, then quality drops | 2 | 2 | 4 | GREEN | -- | Mandate that Steelman is always a precursor to critique, never a substitute | 2 (GREEN) |
| R-003-PLT | S-003 Steelman | Platform | N/A -- purely reasoning-level strategy | 1 | 1 | 1 | GREEN | -- | No mitigation needed | 1 (GREEN) |
| R-003-CMP | S-003 Steelman | Composability | If Steelman delays the critique process, then time-sensitive reviews are slowed | 1 | 2 | 2 | GREEN | -- | Skip Steelman for time-critical reviews (per contraindications) | 1 (GREEN) |
| R-004-FP | S-004 Pre-Mortem | False Positive | If the "has failed" framing triggers availability bias, then recently-observed failure modes dominate over genuinely likely failures | 3 | 2 | 6 | GREEN | -- | Require categorization of failure modes; cross-reference with FMEA (S-012) for completeness | 3 (GREEN) |
| R-004-FN | S-004 Pre-Mortem | False Negative | If the Pre-Mortem relies on imagination rather than systematic enumeration, then non-obvious failures are missed | 3 | 3 | 9 | YELLOW | M | Pair with FMEA (S-012) for systematic coverage; Pre-Mortem excels at creative failure identification, FMEA at systematic coverage | 4 (R-L=2, R-I=2: FMEA pairing catches systematic gaps; scope boundary reduces missed categories) |
| R-004-CW | S-004 Pre-Mortem | Context Window | If failure cause inventory is extensive, then context fills with failure scenarios | 2 | 2 | 4 | GREEN | -- | Cap failure inventory to top 10 most severe; summarize remainder | 2 (GREEN) |
| R-004-INT | S-004 Pre-Mortem | Integration | If temporal reframing ("it has failed") confuses agent prompting, then output quality degrades | 1 | 2 | 2 | GREEN | -- | Use explicit prompt template with clear temporal framing | 1 (GREEN) |
| R-004-QR | S-004 Pre-Mortem | Quality Regression | If Pre-Mortem creates excessive pessimism, then viable plans are abandoned | 2 | 3 | 6 | GREEN | -- | Always follow Pre-Mortem with mitigation planning; balance with Steelman | 3 (GREEN) |
| R-004-PLT | S-004 Pre-Mortem | Platform | N/A -- reasoning-level strategy | 1 | 1 | 1 | GREEN | -- | No mitigation needed | 1 (GREEN) |
| R-004-CMP | S-004 Pre-Mortem | Composability | If Pre-Mortem findings overlap with FMEA output, then redundant analysis wastes tokens | 2 | 2 | 4 | GREEN | -- | Define clear scope boundaries: Pre-Mortem for creative/strategic failures, FMEA for systematic component failures | 2 (GREEN) |
| R-005-FP | S-005 Dialectical Inquiry | False Positive | If assumption negation produces an artificial antithesis, then debate addresses unrealistic alternatives | 3 | 3 | 9 | YELLOW | M | Validate antithesis coherence before debate; reject degenerate inversions | 4 (R-L=2, R-I=2: coherence check reduces occurrence; rejecting degenerate inversions reduces impact) |
| R-005-FN | S-005 Dialectical Inquiry | False Negative | If synthesis prematurely compromises rather than genuinely integrating, then both plans' weaknesses survive | 2 | 3 | 6 | GREEN | -- | Require synthesizer to explicitly justify what is taken from each plan and why | 3 (GREEN) |
| R-005-CW | S-005 Dialectical Inquiry | Context Window | If thesis + antithesis + debate + synthesis generate 3+ full agent passes of content, then context window is severely consumed | 4 | 4 | **16** | **RED** | H | Cap debate to single round; enforce strict word limits on thesis/antithesis; summarize before synthesis | 8 (R-L=2, R-I=4: word limits and single-round cap reduce occurrence from 4 to 2; impact remains major because even capped DI produces substantial output) |
| R-005-INT | S-005 Dialectical Inquiry | Integration | If DI requires 3 agent passes with sync barriers, then orchestration complexity increases | 3 | 2 | 6 | GREEN | -- | Leverage existing /orchestration skill sync barrier support | 3 (GREEN) |
| R-005-QR | S-005 Dialectical Inquiry | Quality Regression | If DI devolves into positional bargaining, then synthesis quality is worse than original thesis | 2 | 3 | 6 | GREEN | -- | Define synthesis quality criteria; verify synthesis genuinely improves on thesis | 3 (GREEN) |
| R-005-PLT | S-005 Dialectical Inquiry | Platform | N/A -- reasoning-level strategy | 1 | 1 | 1 | GREEN | -- | No mitigation needed | 1 (GREEN) |
| R-005-CMP | S-005 Dialectical Inquiry | Composability | If DI thesis/antithesis pattern conflicts with DA's single-countercase approach (S-002), then applying both is wasteful | 2 | 2 | 4 | GREEN | -- | DI subsumes DA; do not apply both to the same artifact | 2 (GREEN) |
| R-006-FP | S-006 ACH | False Positive | If the hypothesis set is poorly constructed, then ACH rejects correct hypotheses due to noise | 2 | 3 | 6 | GREEN | -- | Include at least one "least likely" hypothesis; validate hypothesis set for exhaustiveness | 3 (GREEN) |
| R-006-FN | S-006 ACH | False Negative | If evidence items are not independent, then the matrix produces misleading diagnosticity scores | 3 | 3 | 9 | YELLOW | M | Explicitly check evidence independence; flag correlated evidence pairs | 4 (R-L=2, R-I=2: independence checking reduces occurrence; flagging reduces severity of misleading results) |
| R-006-CW | S-006 ACH | Context Window | If the hypothesis x evidence matrix is large, then matrix representation consumes significant tokens | 3 | 3 | 9 | YELLOW | H | Limit to 5 hypotheses x 10 evidence items maximum; summarize matrix | 4 (R-L=2, R-I=2: size limits cap both occurrence probability and maximum token impact) |
| R-006-INT | S-006 ACH | Integration | If ACH requires multi-agent hypothesis generation, then coordination overhead increases | 2 | 2 | 4 | GREEN | -- | ACH can be single-agent with structured reasoning protocol | 2 (GREEN) |
| R-006-QR | S-006 ACH | Quality Regression | If ACH is applied to subjective/normative questions where "hypotheses" are preferences, then the method degenerates | 2 | 3 | 6 | GREEN | -- | Restrict ACH to diagnostic/investigative contexts per contraindications | 3 (GREEN) |
| R-006-PLT | S-006 ACH | Platform | N/A -- reasoning-level strategy | 1 | 1 | 1 | GREEN | -- | No mitigation needed | 1 (GREEN) |
| R-006-CMP | S-006 ACH | Composability | If ACH hypothesis generation overlaps with DI alternative generation (S-005), then outputs are redundant | 2 | 2 | 4 | GREEN | -- | ACH is diagnostic (explanation); DI is generative (plan). Different use cases; avoid conflation | 2 (GREEN) |
| R-007-FP | S-007 Constitutional AI | False Positive | If constitution principles are overly rigid, then legitimate creative deviations are flagged as violations | 3 | 3 | 9 | YELLOW | M | Include a "deviation with justification" escape hatch in constitution evaluation | 4 (R-L=2, R-I=2: escape hatch reduces occurrence; deviation mechanism reduces severity of false flags) |
| R-007-FN | S-007 Constitutional AI | False Negative | If constitution has missing principles, then uncovered quality dimensions are not evaluated | 3 | 3 | 9 | YELLOW | L | Periodic constitution review; complement with Inversion (S-013) to generate missing principles | 4 (R-L=2, R-I=2: periodic review fills gaps over time; Inversion generates missing criteria proactively) |
| R-007-CW | S-007 Constitutional AI | Context Window | If multi-pass critique (structural/semantic/holistic) produces 3 full critique rounds, then context fills rapidly | 3 | 3 | 9 | YELLOW | H | Consolidate critique output; only persist violations, not passes; limit to 2 passes for routine artifacts | 4 (R-L=2, R-I=2: pass limits reduce occurrence; violation-only output reduces token volume) |
| R-007-INT | S-007 Constitutional AI | Integration | If Jerry's existing rules files are not structured for principle-by-principle evaluation, then adaptation work is required | 2 | 2 | 4 | GREEN | -- | Rules files are already structured with clear headings and tables; minimal adaptation needed | 2 (GREEN) |
| R-007-QR | S-007 Constitutional AI | Quality Regression | If "constitution gaming" occurs (technically satisfying principles while violating intent), then quality appears high but is actually low | 2 | 4 | 8 | YELLOW | L | Add holistic pass that evaluates spirit-of-the-law; human spot-check for gaming detection | 4 (R-L=1, R-I=4: holistic pass and spot-checks reduce occurrence from 2 to 1; impact unchanged because gaming that evades detection remains major) |
| R-007-PLT | S-007 Constitutional AI | Platform | If constitution includes platform-specific rules (e.g., fcntl vs filelock), then evaluation may be platform-dependent | 2 | 2 | 4 | GREEN | -- | Tag platform-specific rules; conditionally apply based on target | 2 (GREEN) |
| R-007-CMP | S-007 Constitutional AI | Composability | If S-007 is the default review and other strategies add competing evaluations, then which evaluation prevails? | 2 | 3 | 6 | GREEN | -- | S-007 is the baseline; other strategies layer on top with clear precedence rules | 3 (GREEN) |
| R-008-FP | S-008 Socratic Method | False Positive | If Socratic questioning probes areas where the creator's reasoning is correct but hard to articulate, then "failures to answer" are flagged incorrectly | 2 | 2 | 4 | GREEN | -- | Distinguish "unable to articulate" from "wrong"; allow creator to provide evidence in response | 2 (GREEN) |
| R-008-FN | S-008 Socratic Method | False Negative | If questioning does not reach sufficient depth, then surface-level answers mask deep flaws | 2 | 3 | 6 | GREEN | -- | Set minimum 3-turn questioning depth; use Paul & Elder's 6 question categories systematically | 3 (GREEN) |
| R-008-CW | S-008 Socratic Method | Context Window | If multi-turn Q&A exchanges accumulate, then context fills with dialogue | 3 | 3 | 9 | YELLOW | H | Cap at 5 question-answer pairs; summarize Q&A transcript before passing to next phase | 4 (R-L=2, R-I=2: Q&A cap reduces occurrence; summarization reduces token volume per exchange) |
| R-008-INT | S-008 Socratic Method | Integration | If Socratic Method requires interactive dialogue (creator responds to questions), then asynchronous workflows need adaptation | 2 | 2 | 4 | GREEN | -- | Implement as simulated dialogue: critic generates questions, then self-simulates creator responses | 2 (GREEN) |
| R-008-QR | S-008 Socratic Method | Quality Regression | If Socratic questioning becomes confrontational, then creator agent becomes defensive and output degrades | 1 | 2 | 2 | GREEN | -- | Frame questions constructively per prompt template; avoid accusatory language | 1 (GREEN) |
| R-008-PLT | S-008 Socratic Method | Platform | N/A -- reasoning-level strategy | 1 | 1 | 1 | GREEN | -- | No mitigation needed | 1 (GREEN) |
| R-008-CMP | S-008 Socratic Method | Composability | If Socratic questions overlap with DA counterarguments (S-002), then review feels repetitive | 2 | 2 | 4 | GREEN | -- | DA challenges conclusions; Socratic probes reasoning. Different mechanisms; sequence Socratic before DA | 2 (GREEN) |
| R-009-FP | S-009 Multi-Agent Debate | False Positive | If debaters converge on a shared wrong answer through rhetoric over truth, then incorrect criticism appears authoritative | 3 | 4 | 12 | YELLOW | L | Require evidence citations in each debate round; judge evaluates evidence quality, not rhetorical skill | 6 (R-L=2, R-I=3: evidence citation requirement reduces occurrence; rhetorical convergence impact partially persists because judge shares same model biases) |
| R-009-FN | S-009 Multi-Agent Debate | False Negative | If identical model instances share blind spots, then debate cannot surface common-mode failures | 3 | 4 | 12 | YELLOW | L | Acknowledge epistemological limitation; pair with external tool verification or human spot-check for critical artifacts | 6 (R-L=2, R-I=3: external checks reduce occurrence of undetected blind spots; impact partially persists because tool coverage is incomplete) |
| R-009-CW | S-009 Multi-Agent Debate | Context Window | If N agents x M rounds generate massive debate transcripts (4-6+ agent passes), then context window is overwhelmed | 5 | 4 | **20** | **RED** | H | Strict 2-agent 2-round limit; compress debate transcript between rounds; set absolute token budget | 9 (R-L=3, R-I=3: agent/round limits reduce occurrence from 5 to 3; compression and budget caps reduce severity from 4 to 3) |
| R-009-INT | S-009 Multi-Agent Debate | Integration | If debate requires 3+ concurrent agent instances, then P-003 (no recursive subagents) must be carefully respected | 3 | 3 | 9 | YELLOW | H | Implement as sequential orchestrator-to-worker calls, not nested agents; use /orchestration sync barriers | 4 (R-L=2, R-I=2: sequential implementation pattern is well-established in Jerry; /orchestration already supports this) |
| R-009-QR | S-009 Multi-Agent Debate | Quality Regression | If debate degrades into adversarial rhetoric without substance, then output quality drops below single-agent review | 2 | 4 | 8 | YELLOW | M | Judge agent enforces evidence-based argumentation rules; terminate debate if quality criteria not met | 4 (R-L=1, R-I=4: evidence-based rules and early termination eliminate most rhetoric-over-truth occurrences; impact unchanged because undetected rhetoric degradation remains major) |
| R-009-PLT | S-009 Multi-Agent Debate | Platform | N/A -- reasoning-level strategy | 1 | 1 | 1 | GREEN | -- | No mitigation needed | 1 (GREEN) |
| R-009-CMP | S-009 Multi-Agent Debate | Composability | If Multi-Agent Debate is applied alongside DA (S-002) or DI (S-005), then three different adversarial dialogue patterns compete | 2 | 3 | 6 | GREEN | -- | MAD is highest-intensity; only deploy at S-015 Level 4; never combine with DA or DI on same artifact | 3 (GREEN) |
| R-010-FP | S-010 Self-Refine | False Positive | If self-feedback is systematically harsh, then model over-corrects and removes valid content | 2 | 2 | 4 | GREEN | -- | Set maximum 3 iterations per contraindications; stop if self-feedback is empty | 2 (GREEN) |
| R-010-FN | S-010 Self-Refine | False Negative | If model has consistent blind spots, then self-refine reinforces rather than corrects errors | 3 | 3 | 9 | YELLOW | L | Never use Self-Refine as sole review for high-stakes artifacts; pair with external critic | 4 (R-L=2, R-I=2: external critic pairing catches errors Self-Refine misses; pairing reduces severity because blind spots are surfaced by complementary strategy) |
| R-010-CW | S-010 Self-Refine | Context Window | If self-refine adds 1 agent pass of overhead, then context is incrementally consumed | 2 | 2 | 4 | GREEN | -- | Minimal overhead; cap at 2 iterations for routine work | 2 (GREEN) |
| R-010-INT | S-010 Self-Refine | Integration | If Self-Refine must be embedded in every creator agent, then prompt templates need standardized self-review section | 1 | 1 | 1 | GREEN | -- | Simple prompt template addition; no architectural change | 1 (GREEN) |
| R-010-QR | S-010 Self-Refine | Quality Regression | If later iterations degrade output (over-refinement), then quality drops below initial generation | 2 | 3 | 6 | GREEN | -- | Cap at 3 iterations; monitor quality score per iteration; stop if score decreases | 3 (GREEN) |
| R-010-PLT | S-010 Self-Refine | Platform | N/A -- reasoning-level strategy | 1 | 1 | 1 | GREEN | -- | No mitigation needed | 1 (GREEN) |
| R-010-CMP | S-010 Self-Refine | Composability | If Self-Refine runs before external critic, then critic sees refined output and cannot assess baseline quality | 1 | 2 | 2 | GREEN | -- | Acceptable trade-off: critic reviews best-effort output; baseline quality assessment is not required | 1 (GREEN) |
| R-011-FP | S-011 CoVe | False Positive | If verification questions target correct claims, then false discrepancies from model uncertainty flag valid content | 2 | 2 | 4 | GREEN | -- | Only flag claims where verification answer directly contradicts original claim | 2 (GREEN) |
| R-011-FN | S-011 CoVe | False Negative | If the model's knowledge is insufficient for the domain, then verification answers are also incorrect, confirming hallucinations | 3 | 4 | 12 | YELLOW | L | Augment with external tool verification (link checkers, search) per CRITIC enhancement; flag low-confidence verifications | 6 (R-L=2, R-I=3: external tools catch some knowledge gaps; impact partially persists because tool coverage does not span all domain claims) |
| R-011-CW | S-011 CoVe | Context Window | If factored variant generates N independent verification queries, then token consumption scales with claim count | 3 | 3 | 9 | YELLOW | H | Limit to top 10 factual claims per artifact; prioritize novel or unusual claims | 4 (R-L=2, R-I=2: claim limit caps occurrence; prioritization reduces severity by focusing verification on highest-value claims) |
| R-011-INT | S-011 CoVe | Integration | If "independent verification" requires context isolation (answering without original response), then prompt engineering must manage context carefully | 2 | 2 | 4 | GREEN | -- | Implement factored variant with explicit context windowing in prompts | 2 (GREEN) |
| R-011-QR | S-011 CoVe | Quality Regression | If CoVe introduces false corrections based on incorrect verification, then factual accuracy degrades | 2 | 4 | 8 | YELLOW | M | Require high confidence for corrections; flag uncertain corrections for human review | 4 (R-L=1, R-I=4: high-confidence threshold and flagging reduce occurrence to rare; impact unchanged because false corrections that pass the threshold remain major) |
| R-011-PLT | S-011 CoVe | Platform | N/A -- reasoning-level strategy | 1 | 1 | 1 | GREEN | -- | No mitigation needed | 1 (GREEN) |
| R-011-CMP | S-011 CoVe | Composability | If CoVe targets only factual claims while other strategies target reasoning, then there is no conflict but also no overlap coverage | 1 | 1 | 1 | GREEN | -- | CoVe is complementary to all reasoning-level strategies; natural scope separation | 1 (GREEN) |
| R-012-FP | S-012 FMEA | False Positive | If FMEA enumerates theoretical failure modes with near-zero probability, then review wastes effort on irrelevant risks | 3 | 2 | 6 | GREEN | -- | Apply RPN scoring; focus remediation on failures with RPN above threshold only | 3 (GREEN) |
| R-012-FN | S-012 FMEA | False Negative | If FMEA fails to identify interaction effects between failure modes, then cascading failures are missed | 3 | 3 | 9 | YELLOW | M | Supplement FMEA with Pre-Mortem (S-004) for emergent/interaction failures; FMEA covers components, Pre-Mortem covers scenarios | 4 (R-L=2, R-I=2: Pre-Mortem pairing catches interaction effects via scenario imagination; scope boundary reduces missed categories) |
| R-012-CW | S-012 FMEA | Context Window | If FMEA table for a complex system has many component-failure-mode pairs, then output is large | 3 | 3 | 9 | YELLOW | H | Limit FMEA scope to key interfaces and critical components; summarize low-RPN entries | 4 (R-L=2, R-I=2: scope limits reduce occurrence; summarization reduces token volume for low-priority entries) |
| R-012-INT | S-012 FMEA | Integration | If FMEA requires domain expertise the model lacks, then failure mode identification is incomplete | 2 | 3 | 6 | GREEN | -- | Provide FMEA prompt templates with domain-specific failure mode categories (e.g., concurrency, boundary, resource) | 3 (GREEN) |
| R-012-QR | S-012 FMEA | Quality Regression | If RPN scoring uses ordinal scales incorrectly (known FMEA limitation), then risk prioritization is misleading | 2 | 3 | 6 | GREEN | -- | Use High/Medium/Low simplification per Jerry applicability guidance; acknowledge ordinal limitation | 3 (GREEN) |
| R-012-PLT | S-012 FMEA | Platform | If failure modes include platform-specific issues (e.g., file locking, path separators), then FMEA must be platform-aware | 2 | 2 | 4 | GREEN | -- | Include platform as a scoping parameter in FMEA charter | 2 (GREEN) |
| R-012-CMP | S-012 FMEA | Composability | If FMEA output overlaps with Pre-Mortem (S-004) failure identification, then redundant analysis occurs | 2 | 2 | 4 | GREEN | -- | Define scope: FMEA for systematic/component failures; Pre-Mortem for strategic/emergent failures | 2 (GREEN) |
| R-013-FP | S-013 Inversion | False Positive | If inversion generates impractical anti-patterns, then the resulting checklist flags non-issues | 2 | 2 | 4 | GREEN | -- | Filter anti-patterns for plausibility before checklist conversion | 2 (GREEN) |
| R-013-FN | S-013 Inversion | False Negative | If inversion misses subtle failure modes that are not the simple opposite of success, then coverage gaps exist | 2 | 3 | 6 | GREEN | -- | Pair with FMEA (S-012) for systematic coverage; Inversion excels at creative anti-patterns, FMEA at systematic ones | 3 (GREEN) |
| R-013-CW | S-013 Inversion | Context Window | If anti-pattern checklist is compact, then context consumption is minimal | 1 | 2 | 2 | GREEN | -- | Naturally low overhead; 1 agent pass | 1 (GREEN) |
| R-013-INT | S-013 Inversion | Integration | If inversion output needs mechanical conversion to positive checklist, then a transformation step is required | 1 | 1 | 1 | GREEN | -- | Simple prompt template handles inversion-to-checklist conversion | 1 (GREEN) |
| R-013-QR | S-013 Inversion | Quality Regression | If inversion becomes frivolous without constraints, then anti-patterns are absurd and waste effort | 2 | 2 | 4 | GREEN | -- | Constrain inversion prompt to "realistic" and "domain-relevant" failure modes | 2 (GREEN) |
| R-013-PLT | S-013 Inversion | Platform | N/A -- reasoning-level strategy | 1 | 1 | 1 | GREEN | -- | No mitigation needed | 1 (GREEN) |
| R-013-CMP | S-013 Inversion | Composability | If inversion-generated checklists feed into Constitutional AI Critique (S-007), then strong positive synergy | 1 | 1 | 1 | GREEN | -- | Designed as a complementary strategy; generates criteria for other strategies to use | 1 (GREEN) |
| R-014-FP | S-014 LLM-as-Judge | False Positive | If rubric is overly strict, then acceptable artifacts score below threshold and require unnecessary revision | 2 | 3 | 6 | GREEN | -- | Calibrate rubric against human-scored reference set; include tolerance band around thresholds | 3 (GREEN) |
| R-014-FN | S-014 LLM-as-Judge | False Negative | If judge exhibits leniency bias or self-enhancement bias, then low-quality artifacts pass quality gates | 3 | 4 | 12 | YELLOW | M | Mutation testing for judges; calibrate against known-bad artifacts; periodic human audit of scores | 6 (R-L=2, R-I=3: mutation testing and known-bad calibration reduce occurrence; impact partially persists because leniency bias is subtle and calibration may drift between audit cycles) |
| R-014-CW | S-014 LLM-as-Judge | Context Window | If judge evaluation is a single pass with rubric, then context consumption is moderate | 2 | 2 | 4 | GREEN | -- | Low overhead; single evaluation pass | 2 (GREEN) |
| R-014-INT | S-014 LLM-as-Judge | Integration | If rubric design requires domain expertise, then rubric creation is a separate non-trivial task | 2 | 2 | 4 | GREEN | -- | Create rubric templates per artifact type; iterate based on calibration results | 2 (GREEN) |
| R-014-QR | S-014 LLM-as-Judge | Quality Regression | If judge scores are taken as absolute truth without calibration, then quality framework becomes unreliable | 2 | 4 | 8 | YELLOW | M | Treat scores as advisory until calibrated; include confidence intervals; human spot-check | 4 (R-L=1, R-I=4: advisory framing and confidence intervals reduce occurrence from 2 to 1; impact unchanged because uncalibrated scores that are mistakenly trusted remain major) |
| R-014-PLT | S-014 LLM-as-Judge | Platform | N/A -- reasoning-level strategy | 1 | 1 | 1 | GREEN | -- | No mitigation needed | 1 (GREEN) |
| R-014-CMP | S-014 LLM-as-Judge | Composability | If S-014 serves as both a strategy and evaluation infrastructure for S-015, then dual-role creates dependency | 2 | 2 | 4 | GREEN | -- | Explicit dual-role documentation (acknowledged in v1.1.0); clear API boundaries between strategy and infrastructure uses | 2 (GREEN) |
| R-015-FP | S-015 PAE | False Positive | If escalation gates are miscalibrated, then low-risk artifacts are escalated unnecessarily, wasting resources | 3 | 3 | 9 | YELLOW | M | Calibrate gates per S-015 Experiment 2 (escalation calibration); allow de-escalation | 4 (R-L=2, R-I=2: calibration reduces miscalibration occurrence; de-escalation mechanism reduces wasted-resource severity) |
| R-015-FN | S-015 PAE | False Negative | If early-level reviews create false confidence, then critical defects in seemingly-simple artifacts are missed | 3 | 4 | 12 | YELLOW | L | Define mandatory escalation rules for high-risk artifact types (governance, security); implement S-015 Experiment 1 | 6 (R-L=2, R-I=3: mandatory escalation rules bypass gate miscalibration for critical types; impact partially persists because novel high-risk artifacts may not match predefined categories) |
| R-015-CW | S-015 PAE | Context Window | If full escalation through Levels 0-4 accumulates outputs from 6+ agent passes, then context window is severely consumed | 4 | 4 | **16** | **RED** | H | Summarize outputs at each level before escalation; discard lower-level details after synthesis; set absolute token budget per review | 8 (R-L=2, R-I=4: summarization and budget caps reduce occurrence from 4 to 2; impact remains major because even summarized multi-level output is substantial) |
| R-015-INT | S-015 PAE | Integration | If PAE orchestration requires complex multi-level workflow management, then /orchestration skill must handle conditional escalation paths | 3 | 3 | 9 | YELLOW | H | Implement as state machine in /orchestration; leverage existing sync barrier infrastructure | 4 (R-L=2, R-I=2: /orchestration already supports state machines and sync barriers; existing infrastructure reduces both occurrence and severity) |
| R-015-QR | S-015 PAE | Quality Regression | If PAE adds latency from multiple review rounds, then throughput drops without proportional quality gain | 3 | 3 | 9 | YELLOW | M | Implement S-015 Experiment 3 (cost-efficiency comparison); short-circuit if quality gate passed at lower level | 4 (R-L=2, R-I=2: short-circuit mechanism reduces unnecessary rounds; experiment data enables calibration of cost-benefit) |
| R-015-PLT | S-015 PAE | Platform | N/A -- meta-strategy operates at reasoning level | 1 | 1 | 1 | GREEN | -- | No mitigation needed | 1 (GREEN) |
| R-015-CMP | S-015 PAE | Composability | If PAE orchestrates all other strategies, then it is a dependency for the entire adversarial framework | 3 | 3 | 9 | YELLOW | M | Define fallback (already in v1.1.0): if PAE gates unreliable, default to Layer 2 for all artifacts | 4 (R-L=2, R-I=2: fallback strategy ensures framework operates even with PAE failure; mandatory minimum eliminates complete dependency) |

---

## Per-Strategy Risk Profiles

### S-001: Red Team Analysis -- Risk Profile

**Overall Risk Level:** YELLOW (Manageable)
**Aggregate Score:** 39/175 (low-moderate)

| Category | Score | Rationale |
|----------|-------|-----------|
| False Positive | 9 | Red Team adversary models may not accurately reflect realistic threats against Jerry artifacts (code, docs, architecture). The "adversary" in Jerry's context is not a human attacker but quality deficiencies, making adversary modeling abstracted. |
| False Negative | 8 | If Red Team scope is too narrow, real vulnerabilities outside the modeled adversary's capability are missed. Mitigated by the defined adversary profile approach. |
| Context Window | 9 | Vulnerability reports can be detailed. Manageable with hierarchical summarization. |
| Integration | 6 | Fits naturally into 2-agent orchestrator-worker pattern. P-003 compliant. |
| Quality Regression | 9 | Premature Red Team on early-stage work is the primary regression risk. Contraindications (added in v1.1.0) address this. |
| Platform | 2 | Minimal platform sensitivity. |
| Composability | 4 | Mild tension with Steelman (S-003) resolved by sequencing. |

**Recommended Mitigations:**
1. Gate Red Team behind S-015 Level 4 (only for mature, high-stakes artifacts)
2. Define adversary profiles per artifact type (security, architecture, code quality)
3. Cap vulnerability report to structured summary format

---

### S-002: Devil's Advocate Analysis -- Risk Profile

**Overall Risk Level:** GREEN (Low)
**Aggregate Score:** 27/175 (low)

| Category | Score | Rationale |
|----------|-------|-----------|
| False Positive | 6 | Performative dissent is a known risk (Nemeth et al., 2001). Mitigated by requiring evidence-backed counterarguments. |
| False Negative | 6 | DA only challenges conclusions, not assumptions. Complementary to Socratic Method. |
| Context Window | 4 | Single countercase document; compact. |
| Integration | 6 | LLM compliance training may weaken adversarial stance. Addressable via prompt engineering. |
| Quality Regression | 4 | Low regression risk with reconciliation step. |
| Platform | 1 | No platform sensitivity. |
| Composability | 4 | Minor overlap with S-003 resolved by ordering. |

**Recommended Mitigations:**
1. Require evidence citations in DA counterarguments
2. Always pair with reconciliation step
3. Sequence after Steelman (S-003)

---

### S-003: Steelman Technique -- Risk Profile

**Overall Risk Level:** GREEN (Very Low)
**Aggregate Score:** 16/175 (very low)

This is the **lowest-risk strategy in the catalog**. Steelman adds minimal overhead (~0.5 agent pass), operates at the reasoning level with no platform sensitivity, is complementary to all other strategies, and its primary risk (over-charity) is easily mitigated by mandating it as a precursor to critique rather than a standalone method.

**Recommended Mitigations:**
1. Always pair with subsequent critique phase (never standalone)
2. Include author verification step where feasible

---

### S-004: Pre-Mortem Analysis -- Risk Profile

**Overall Risk Level:** GREEN-YELLOW (Low-Moderate)
**Aggregate Score:** 28/175 (low)

| Category | Score | Rationale |
|----------|-------|-----------|
| False Positive | 6 | Availability bias may weight recent failures. Categorization mitigates. |
| False Negative | 9 | Imagination-dependent; non-obvious failures may be missed. Pair with FMEA. |
| Context Window | 4 | Manageable output size. |
| Integration | 2 | Simple temporal reframing prompt; easy integration. |
| Quality Regression | 6 | Excessive pessimism risk; mitigated by mitigation planning step. |
| Platform | 1 | No platform sensitivity. |
| Composability | 4 | Complementary to FMEA with clear scope boundaries. |

**Recommended Mitigations:**
1. Always follow Pre-Mortem with mitigation planning
2. Pair with FMEA (S-012) for systematic coverage
3. Cap failure inventory to top 10 most severe

---

### S-005: Dialectical Inquiry -- Risk Profile

**Overall Risk Level:** YELLOW-RED (Moderate-High)
**Aggregate Score:** 42/175 (moderate)

**Contains 1 RED risk (Context Window).** DI's 3-agent, multi-pass pattern generates substantial token volumes. The thesis-antithesis-synthesis pattern inherently produces large outputs.

| Category | Score | Rationale |
|----------|-------|-----------|
| False Positive | 9 | Artificial antithesis from mechanical assumption negation may not represent realistic alternatives. |
| False Negative | 6 | Premature compromise in synthesis may preserve both plans' weaknesses. |
| Context Window | **16 RED** | 3+ agent passes with full plan development is the most token-intensive academic strategy. |
| Integration | 6 | Requires 3-agent coordination with sync barriers. Feasible with /orchestration. |
| Quality Regression | 6 | Positional bargaining risk. |
| Platform | 1 | No platform sensitivity. |
| Composability | 4 | Subsumes DA; avoid applying both. |

**Recommended Mitigations:**
1. **CRITICAL:** Enforce strict word limits on thesis, antithesis, and synthesis outputs
2. Cap debate to single round
3. Reserve for C3/C4 decisions only (per escalation threshold definitions)
4. Validate antithesis coherence before proceeding to debate

---

### S-006: Analysis of Competing Hypotheses -- Risk Profile

**Overall Risk Level:** YELLOW (Manageable)
**Aggregate Score:** 35/175 (low-moderate)

| Category | Score | Rationale |
|----------|-------|-----------|
| False Positive | 6 | Poor hypothesis set construction leads to incorrect rejections. |
| False Negative | 9 | Non-independent evidence items produce misleading diagnosticity. |
| Context Window | 9 | Matrix representation scales with hypothesis x evidence size. |
| Integration | 4 | Can be single-agent with structured protocol. |
| Quality Regression | 6 | Misapplication to subjective questions degrades method. |
| Platform | 1 | No platform sensitivity. |
| Composability | 4 | Complementary to DI with clear scope separation. |

**Recommended Mitigations:**
1. Limit matrix size to 5 hypotheses x 10 evidence items
2. Explicitly check evidence independence
3. Restrict to diagnostic/investigative use cases

---

### S-007: Constitutional AI Critique -- Risk Profile

**Overall Risk Level:** YELLOW (Manageable)
**Aggregate Score:** 45/175 (moderate)

S-007 is Jerry's most naturally integrated strategy (rules files already exist), but its multi-pass structure and constitution gaming risk require attention.

| Category | Score | Rationale |
|----------|-------|-----------|
| False Positive | 9 | Overly rigid principles flag legitimate deviations. Jerry's coding standards are detailed and may be too strict for exploratory work. |
| False Negative | 9 | Missing principles leave quality gaps. The constitution cannot cover everything. |
| Context Window | 9 | Multi-pass (structural/semantic/holistic) generates significant critique output. |
| Integration | 4 | Natural fit with Jerry's existing .claude/rules/ structure. |
| Quality Regression | 8 | Constitution gaming is a subtle but significant risk: agents can learn to satisfy letter of rules while violating spirit. |
| Platform | 4 | Some rules reference platform-specific patterns. |
| Composability | 6 | As default review strategy, must coexist with all others. |

**Recommended Mitigations:**
1. Include "deviation with justification" mechanism
2. Periodic constitution review cycle to fill gaps
3. Consolidate critique output (violations only, not passes)
4. Add holistic spirit-of-the-law evaluation pass

---

### S-008: Socratic Method -- Risk Profile

**Overall Risk Level:** GREEN (Low)
**Aggregate Score:** 26/175 (low)

| Category | Score | Rationale |
|----------|-------|-----------|
| False Positive | 4 | Low risk of false positives; questions expose rather than assert. |
| False Negative | 6 | Insufficient depth may miss deep flaws. Minimum turn count mitigates. |
| Context Window | 9 | Multi-turn Q&A accumulates dialogue. Cap required. |
| Integration | 4 | Simulated dialogue pattern fits agent architecture. |
| Quality Regression | 2 | Minimal regression risk; questions are constructive. |
| Platform | 1 | No platform sensitivity. |
| Composability | 4 | Complementary to DA with clear scope separation. |

**Recommended Mitigations:**
1. Cap at 5 question-answer pairs per session
2. Use Paul & Elder's 6 categories systematically
3. Summarize Q&A before passing to next phase

---

### S-009: Multi-Agent Debate -- Risk Profile

**Overall Risk Level:** RED (High -- Requires Significant Mitigation)
**Aggregate Score:** 48/175 (high)

**Contains 1 RED risk (Context Window) and 3 YELLOW risks.** MAD is the highest-risk strategy in the catalog, primarily due to token consumption and shared model bias.

| Category | Score | Rationale |
|----------|-------|-----------|
| False Positive | 12 | Rhetorical convergence on wrong answer is a documented failure mode. |
| False Negative | 12 | Identical model instances share blind spots. |
| Context Window | **20 RED** | N agents x M rounds generates massive transcripts. Highest context window risk in the catalog. |
| Integration | 9 | 3+ agent instances require careful P-003 compliance. |
| Quality Regression | 8 | Debate can degrade into rhetoric. |
| Platform | 1 | No platform sensitivity. |
| Composability | 6 | Conflicts with DA and DI if combined. |

**Recommended Mitigations:**
1. **CRITICAL:** Strict 2-agent, 2-round limit with absolute token budget
2. **CRITICAL:** Compress debate transcript between rounds (discard verbose reasoning chains)
3. Reserve exclusively for S-015 Level 4 (highest-stakes artifacts only)
4. Require evidence citations in every debate argument
5. Judge enforces evidence-based argumentation rules
6. Consider cross-model verification when architecturally feasible

---

### S-010: Self-Refine -- Risk Profile

**Overall Risk Level:** GREEN (Low)
**Aggregate Score:** 23/175 (low)

Second-lowest risk after Steelman. Very low overhead, simple integration, and the primary risk (blind spot reinforcement) is easily mitigated by never using Self-Refine as sole review for high-stakes artifacts.

| Category | Score | Rationale |
|----------|-------|-----------|
| False Positive | 4 | Self-criticism tends toward mild; low over-correction risk. |
| False Negative | 9 | Systematic blind spots are the primary concern. Never use alone for critical work. |
| Context Window | 4 | Minimal overhead (1 pass). |
| Integration | 1 | Simplest integration of any strategy. |
| Quality Regression | 6 | Over-refinement after iteration 3+ is documented. Cap mitigates. |
| Platform | 1 | No platform sensitivity. |
| Composability | 2 | Excellent composability; serves as pre-critic baseline for all other strategies. |

**Recommended Mitigations:**
1. Cap at 3 iterations maximum
2. Never use as sole review for high-stakes artifacts
3. Monitor quality score per iteration; stop if decreasing

---

### S-011: Chain-of-Verification -- Risk Profile

**Overall Risk Level:** YELLOW (Manageable)
**Aggregate Score:** 31/175 (low-moderate)

| Category | Score | Rationale |
|----------|-------|-----------|
| False Positive | 4 | Low false positive risk with direct contradiction criterion. |
| False Negative | 12 | If model knowledge is insufficient, verification answers are also wrong. Key risk for domain-specific facts. |
| Context Window | 9 | Factored variant generates N verification queries; scales with claim count. |
| Integration | 4 | Context isolation for independent verification requires prompt engineering. |
| Quality Regression | 8 | False corrections from incorrect verification are the primary regression path. |
| Platform | 1 | No platform sensitivity. |
| Composability | 1 | Perfectly complementary; covers factual accuracy while others cover reasoning. |

**Recommended Mitigations:**
1. Augment with external tool verification (search, link checkers)
2. Limit to top 10 factual claims per artifact
3. Require high confidence for corrections; flag uncertain ones

---

### S-012: FMEA -- Risk Profile

**Overall Risk Level:** YELLOW (Manageable)
**Aggregate Score:** 38/175 (low-moderate)

| Category | Score | Rationale |
|----------|-------|-----------|
| False Positive | 6 | May enumerate trivial failure modes. RPN filtering mitigates. |
| False Negative | 9 | Does not capture interaction effects between failure modes. |
| Context Window | 9 | FMEA tables for complex systems can be large. |
| Integration | 6 | Requires domain-specific failure mode categories. |
| Quality Regression | 6 | RPN ordinal scale limitations are well-known. |
| Platform | 4 | Some failure modes are platform-specific. |
| Composability | 4 | Complementary to Pre-Mortem with clear scope boundaries. |

**Recommended Mitigations:**
1. Scope FMEA to critical components and interfaces
2. Use High/Medium/Low simplification instead of 1-10 scales
3. Supplement with Pre-Mortem for emergent failures
4. Include platform as scoping parameter

---

### S-013: Inversion Technique -- Risk Profile

**Overall Risk Level:** GREEN (Very Low)
**Aggregate Score:** 15/175 (very low)

**Joint lowest-risk strategy** (tied with Steelman S-003). Inversion is a low-cost, high-yield, complementary strategy that generates review criteria for other strategies to use. It has no platform sensitivity, minimal context window impact, and strong composability.

**Recommended Mitigations:**
1. Constrain inversion to "realistic and domain-relevant" failure modes
2. Filter anti-patterns for plausibility before checklist conversion

---

### S-014: LLM-as-Judge -- Risk Profile

**Overall Risk Level:** YELLOW (Manageable)
**Aggregate Score:** 31/175 (low-moderate)

S-014's dual role as both strategy and evaluation infrastructure creates a dependency that must be managed, but the strategy itself is low-overhead and well-understood.

| Category | Score | Rationale |
|----------|-------|-----------|
| False Positive | 6 | Strict rubrics may reject acceptable artifacts. Calibration needed. |
| False Negative | 12 | Leniency and self-enhancement biases are documented. Primary concern for quality gates. |
| Context Window | 4 | Single evaluation pass; compact output. |
| Integration | 4 | Rubric creation is a design task but straightforward. |
| Quality Regression | 8 | Uncalibrated scores treated as ground truth is a significant risk. |
| Platform | 1 | No platform sensitivity. |
| Composability | 4 | Dual-role (strategy + infrastructure) requires clear API boundaries. |

**Recommended Mitigations:**
1. Calibrate rubrics against human-scored reference set
2. Implement mutation testing for judges
3. Treat scores as advisory until validated
4. Periodic human audit of score distribution

---

### S-015: Progressive Adversarial Escalation -- Risk Profile

**Overall Risk Level:** YELLOW-RED (Moderate-High)
**Aggregate Score:** 56/175 (moderate-high)

**Contains 1 RED risk (Context Window).** As the meta-strategy orchestrating all others, S-015 accumulates risk from the strategies it composes. Its novel, unvalidated status adds uncertainty.

| Category | Score | Rationale |
|----------|-------|-----------|
| False Positive | 9 | Miscalibrated gates escalate unnecessarily. |
| False Negative | 12 | Early-level false confidence is the most dangerous failure mode: an artifact passes Level 1-2 and is never subjected to deep review despite having critical defects. |
| Context Window | **16 RED** | Full 5-level escalation generates massive cumulative output. Each level adds content. |
| Integration | 9 | Complex multi-level workflow; most integration work of any strategy. |
| Quality Regression | 9 | Latency from multiple review rounds without proportional quality gain. |
| Platform | 1 | No platform sensitivity. |
| Composability | 9 | As the orchestrator of all other strategies, PAE's reliability is a single point of dependency. |

**Recommended Mitigations:**
1. **CRITICAL:** Summarize outputs at each level; discard lower-level details after synthesis
2. **CRITICAL:** Set absolute token budget per review (regardless of escalation level)
3. Complete S-015 validation experiments before production deployment
4. Define mandatory escalation rules for high-risk artifact types
5. Implement fallback strategy (Layer 2 minimum for all) per v1.1.0 guidance
6. Short-circuit escalation when quality gate passed at lower level

---

## L2: Risk Portfolio Analysis

### 5x5 Risk Matrix

```
        IMPACT
        1       2       3       4       5
    5 |       |       |       | R-009 |       |  L=5 (Almost Certain)
      |       |       |       |  -CW  |       |
    4 |       |       |       | R-005 |       |  L=4 (Likely)
      |       |       |       | R-015 |       |
L   3 |       |  x6   | x17   |  x5   |       |  L=3 (Possible)
      |       |       |       |       |       |
    2 |       |  x16  |  x11  |  x4   |       |  L=2 (Unlikely)
      |       |       |       |       |       |
    1 |  x19  |  x8   |       |       |       |  L=1 (Rare)
      |       |       |       |       |       |
        ↑       ↑       ↑       ↑       ↑
      Minimal  Minor  Moderate Major  Critical

GREEN: 1-7 (Accept/Monitor) = 84 risks
YELLOW: 8-15 (Mitigate/Monitor) = 18 risks
RED: 16-25 (Immediate Action Required) = 3 risks
```

### Risk by Category

| Category | RED | YELLOW | GREEN | Total | Dominant Risk |
|----------|-----|--------|-------|-------|---------------|
| False Positive | 0 | 2 | 13 | 15 | S-009 MAD rhetoric convergence (12) |
| False Negative | 0 | 5 | 10 | 15 | S-009 shared blind spots (12), S-014 leniency (12), S-015 false confidence (12), S-011 knowledge gaps (12) |
| Context Window | **3** | **5** | 7 | 15 | **S-009 debate transcripts (20), S-015 cumulative output (16), S-005 thesis/antithesis (16)** |
| Integration | 0 | 2 | 13 | 15 | S-009 multi-agent P-003 (9), S-015 workflow complexity (9) |
| Quality Regression | 0 | 4 | 11 | 15 | S-007 constitution gaming (8), S-009 rhetoric (8), S-011 false corrections (8), S-014 uncalibrated scores (8) |
| Platform | 0 | 0 | 15 | 15 | Negligible across all strategies |
| Composability | 0 | 1 | 14 | 15 | S-015 single point of dependency (9) |
| **Total** | **3** | **18** | **84** | **105** | |

### Systemic Risk Patterns

#### Pattern 1: Context Window Dominance

Context Window is the **only category with RED risks** and has the highest total YELLOW count. This is directly aligned with Jerry's core problem: context rot. The strategies most likely to help quality are also the most likely to consume the context window budget, creating a fundamental tension.

**If** the adversarial framework deploys high-token-consumption strategies (S-009, S-015, S-005) without strict budget controls, **then** the review process itself will contribute to context rot, degrading overall quality rather than improving it.

**Severity:** 4 (Major) | **Likelihood:** 4 (Likely) | **Score:** 16 (RED)

**Systemic Mitigation:**
- Establish per-review token budgets (hard caps)
- Require output summarization at each phase boundary
- Implement "context window health" monitoring that tracks cumulative token consumption per review pipeline
- Reserve high-token strategies for offline/asynchronous review where context window is not shared with active work

#### Pattern 2: Shared Model Bias (Correlated False Negatives)

Six strategies (S-007, S-010, S-011, S-013, S-014, S-015) rely on the same model critiquing itself or evaluating its own kind. The v1.1.0 catalog identifies this as a systemic risk (DA-002). The consequence is **correlated false negatives**: all self-critique strategies will miss the same class of defects.

**If** self-critique strategies share consistent blind spots, **then** defects in those blind spot categories will pass all review levels undetected.

**Severity:** 4 (Major) | **Likelihood:** 3 (Possible) | **Score:** 12 (YELLOW)

**Systemic Mitigation:**
- External tool verification where available (linters, validators, test runners)
- Periodic human spot-check calibration
- Mutation testing injection to verify critic effectiveness
- Cross-model verification when architecturally feasible (future enhancement)

#### Pattern 3: Meta-Strategy Dependency (S-015 as Single Point of Failure)

S-015 Progressive Adversarial Escalation is designed as the orchestration layer for all other strategies. If S-015's escalation gates are unreliable, the entire adversarial framework is compromised.

**If** S-015 escalation calibration fails validation experiments, **then** the adversarial framework has no reliable way to match review intensity to artifact criticality.

**Severity:** 3 (Moderate) | **Likelihood:** 3 (Possible) | **Score:** 9 (YELLOW)

**Systemic Mitigation:**
- S-015 fallback strategy defined in v1.1.0 (default to Layer 2 minimum)
- S-015 validation experiments must complete before production deployment
- Implement S-015 as optional orchestration layer, not mandatory dependency
- Each strategy must remain independently usable without S-015

#### Pattern 4: P-003 Compliance Tension

Jerry's P-003 constraint (no recursive subagents) limits the adversarial framework to one level of orchestrator-to-worker delegation. Strategies requiring multiple interacting agents (S-005 DI, S-009 MAD) must be implemented as sequential orchestrator calls, not nested agent spawning.

**If** multi-agent strategies are implemented with nested agent spawning, **then** P-003 is violated, creating governance non-compliance.

**Severity:** 4 (Major) | **Likelihood:** 2 (Unlikely) | **Score:** 8 (YELLOW)

**Systemic Mitigation:**
- All multi-agent patterns implemented as sequential orchestrator-to-worker calls
- /orchestration skill manages agent sequencing and sync barriers
- Architecture tests verify P-003 compliance

### Risk Trends

This is the initial risk assessment; no trend data is available. The following indicators should be tracked over time:

| Indicator | Measurement | Frequency |
|-----------|-------------|-----------|
| False positive rate | % of flagged issues that are not real problems (per human review) | Monthly |
| False negative rate | % of real issues missed by review (per post-hoc analysis) | Monthly |
| Context window utilization | Tokens consumed per review pipeline | Per review |
| Escalation accuracy | % of artifacts escalated to correct level (per S-015 Experiment 2) | Quarterly |
| Judge calibration drift | Correlation between judge scores and human scores over time | Quarterly |

---

## Risk-Based Recommendations

### Tier 1: Strong Candidates (Favorable Risk Profile -- Adopt)

These strategies have low aggregate risk scores and can be adopted with minimal mitigation:

| Rank | Strategy | Aggregate Score | Key Advantage | Required Mitigation |
|------|----------|-----------------|---------------|---------------------|
| 1 | **S-013 Inversion** | 15 (GREEN) | Lowest risk; generates criteria for other strategies; excellent composability | Constrain to realistic failure modes |
| 2 | **S-003 Steelman** | 16 (GREEN) | Second-lowest risk; improves quality of all subsequent critiques; mandatory precursor | Always pair with critique; never standalone |
| 3 | **S-010 Self-Refine** | 23 (GREEN) | Very low cost (1 pass); universal applicability; improves baseline quality | Cap at 3 iterations; never sole review for high-stakes |
| 4 | **S-008 Socratic Method** | 26 (GREEN) | Low risk; exposes assumptions; complementary to assertion-based strategies | Cap Q&A pairs; summarize before next phase |
| 5 | **S-002 Devil's Advocate** | 27 (GREEN) | Low cost; low risk; well-established; effective groupthink breaker | Require evidence citations; include reconciliation |

### Tier 2: Solid Candidates (Manageable Risk -- Adopt with Mitigation)

These strategies have moderate risk profiles requiring specific mitigations before deployment:

| Rank | Strategy | Aggregate Score | Key Risk | Required Mitigation |
|------|----------|-----------------|----------|---------------------|
| 6 | **S-004 Pre-Mortem** | 28 (GREEN-YELLOW) | Imagination-dependent coverage gaps (FN=9) | Pair with FMEA for systematic coverage |
| 7 | **S-014 LLM-as-Judge** | 31 (YELLOW) | Leniency bias threatens quality gates (FN=12) | Calibrate rubrics; mutation testing; human audit |
| 8 | **S-011 CoVe** | 31 (YELLOW) | Knowledge gap verification failure (FN=12) | External tool augmentation; confidence thresholds |
| 9 | **S-006 ACH** | 35 (YELLOW) | Evidence independence assumption (FN=9) | Limit matrix size; check evidence independence |
| 10 | **S-012 FMEA** | 38 (YELLOW) | Context window from large tables (CW=9) | Scope to critical components; summarize low-RPN |

### Tier 3: Conditional Candidates (Elevated Risk -- Adopt with Significant Mitigation)

These strategies have elevated risk profiles and should only be adopted with the specified mitigations in place:

| Rank | Strategy | Aggregate Score | Key Risk(s) | Required Mitigation |
|------|----------|-----------------|-------------|---------------------|
| 11 | **S-001 Red Team** | 39 (YELLOW) | Premature adversarial pressure (QR=9); unrealistic adversary models (FP=9) | Gate behind S-015 Level 4; define adversary profiles |
| 12 | **S-005 Dialectical Inquiry** | 42 (YELLOW-RED) | **RED: Context window (16)**; artificial antithesis (FP=9) | Strict word limits; single debate round; C3/C4 only |
| 13 | **S-007 Constitutional AI** | 45 (YELLOW) | Constitution gaming (QR=8); rigidity (FP=9); multi-pass output (CW=9) | Deviation mechanism; periodic review; holistic pass |

### Tier 4: High-Risk Candidates (Significant Risk -- Adopt with Caution)

These strategies have high risk profiles and should be adopted only for their highest-value use cases with all mitigations in place:

| Rank | Strategy | Aggregate Score | Key Risk(s) | Required Mitigation |
|------|----------|-----------------|-------------|---------------------|
| 14 | **S-009 Multi-Agent Debate** | 48 (RED) | **RED: Context window (20)**; shared blind spots (FN=12); rhetoric over truth (FP=12) | Strict 2-agent 2-round limit; absolute token budget; evidence-based debate rules; Level 4 only |
| 15 | **S-015 Progressive Adversarial Escalation** | 56 (RED) | **RED: Context window (16)**; false confidence (FN=12); single point of dependency (CMP=9) | Token budgets; output summarization; validation experiments; fallback strategy |

### Strategies Recommended Against Adoption: NONE

No strategy has a risk profile so unfavorable as to recommend against adoption entirely. All 15 strategies provide unique adversarial mechanisms that complement each other. The three RED-category risks (S-009-CW, S-015-CW, S-005-CW) are all in the Context Window category and are all mitigable through output management practices (summarization, token budgets, word limits).

**Important caveat:** S-015 Progressive Adversarial Escalation should NOT be deployed to production until its three validation experiments (defined in v1.1.0 TASK-006) are completed. The fallback strategy (Layer 2 minimum for all artifacts) should be used during the validation period.

---

## Severity Classification Summary (FMEA-aligned)

| Severity Class | Description | Affected Strategies | Count |
|----------------|-------------|---------------------|-------|
| **Catastrophic (S=5)** | Quality framework failure: incorrect results accepted as correct | None | 0 |
| **Critical (S=4)** | Significant quality degradation; requires immediate intervention | S-009 (FP, FN, CW), S-015 (FN, CW), S-005 (CW), S-011 (FN, QR), S-014 (FN, QR) | 9 risks |
| **Major (S=3)** | Noticeable quality impact; addressable with planned mitigation | S-001 (FP, CW, QR), S-004 (FN, QR), S-006 (FN, CW), S-007 (FP, FN, CW, CMP), S-008 (CW), S-012 (FN, CW, INT, QR), S-015 (FP, INT, QR, CMP) | 22 risks |
| **Moderate (S=2)** | Slight degradation; easily correctable | Most remaining risks | 47 risks |
| **Negligible (S=1)** | No meaningful impact | Platform risks (all 15 strategies), integration for simple strategies | 27 risks |

---

## NPR 7123.1D Compliance Notes

This risk assessment follows NASA Technical Risk Management (Process 13) methodology:

1. **Risk Identification:** All 15 strategies evaluated across 7 risk categories (105 risk assessments)
2. **Risk Analysis:** Each risk scored using 5x5 Likelihood x Impact matrix per NPR 8000.4C
3. **Risk Mitigation Planning:** Every YELLOW and RED risk has a defined mitigation strategy
4. **Residual Risk Assessment:** Post-mitigation risk scores provided for all risks
5. **Risk Communication:** RED risks escalated in L0 Executive Summary
6. **Continuous Risk Management:** Trend indicators defined for ongoing monitoring

---

## References

### NASA Standards Applied

- NPR 8000.4C - Agency Risk Management Procedural Requirements
- NPR 7123.1D - Systems Engineering Processes and Requirements, Section 3.4.4 (Process 13)
- NASA Risk Management Handbook (NASA/SP-2011-3422)
- NASA/SP-2016-6105 Rev2 - NASA Systems Engineering Handbook, Chapter 6
- MIL-STD-1629A - Procedures for Performing FMECA
- IEC 60812:2018 - Failure Mode and Effects Analysis

### Input Documents

- TASK-006 Revised Catalog (v1.1.0) - FEAT-004:EN-301:TASK-006
- TASK-004 Unified Catalog (v1.0.0) - FEAT-004:EN-301:TASK-004
- TASK-005 Adversarial Review (v1.0.0) - FEAT-004:EN-301:TASK-005

### Jerry Framework References

- Jerry Constitution v1.1 - docs/governance/JERRY_CONSTITUTION.md
- P-003: No Recursive Subagents
- P-020: User Authority
- P-022: No Deception
- P-042: Risk Transparency
- P-043: Mandatory Disclaimer

---

*Generated by nse-risk agent v2.1.0*
*Document ID: FEAT-004:EN-302:TASK-002*
*Date: 2026-02-13*
*Status: Complete*
