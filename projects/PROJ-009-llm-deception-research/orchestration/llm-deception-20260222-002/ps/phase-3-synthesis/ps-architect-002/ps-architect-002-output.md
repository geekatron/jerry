# Architectural Analysis v2: Training Data Reliability Patterns

> **Agent:** ps-architect-002
> **Pipeline:** PS
> **Workflow:** llm-deception-20260222-002
> **Date:** 2026-02-22
> **Status:** Complete
> **Depends On:** ps-synthesizer-002 output (Two-Leg Thesis), Phase 2 A/B Test Results

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Architectural implications of the Two-Leg Thesis |
| [Updated Pattern-to-Incentive Mapping](#updated-pattern-to-incentive-mapping) | How training incentives produce both failure legs |
| [The Snapshot Problem](#the-snapshot-problem) | Why training data captures point-in-time facts as permanent truths |
| [Domain-Specific Reliability Tiers](#domain-specific-reliability-tiers) | Empirically-derived reliability ranking with architectural implications |
| [Mitigation Architecture](#mitigation-architecture) | Tool-augmented retrieval as the primary defense for Leg 1 |
| [Jerry Framework as Proof-of-Concept](#jerry-framework-as-proof-of-concept) | Governance-based mitigation in practice |
| [Recommendations for Agent System Designers](#recommendations-for-agent-system-designers) | Actionable architectural guidance |
| [Failure Mode Taxonomy](#failure-mode-taxonomy) | Classifying LLM failures by detectability and domain |
| [Open Questions](#open-questions) | Unresolved architectural concerns |
| [References](#references) | Source evidence and prior work |

---

## Executive Summary

The Two-Leg Thesis (ps-synthesizer-002) establishes that LLM unreliability operates through two distinct mechanisms: **Confident Micro-Inaccuracy** (Leg 1, invisible) and **Knowledge Gaps** (Leg 2, visible). This architectural analysis examines the structural causes of both legs and derives design principles for agent systems that must operate reliably in the presence of both failure modes.

The central architectural insight is that **LLM internal knowledge reliability is domain-dependent**, and this domain dependence is not random -- it follows directly from the structure of training data. Domains with stable, consistent facts (science) produce reliable internal knowledge. Domains with rapidly-evolving, inconsistently-documented facts (technology) produce unreliable internal knowledge despite high model confidence.

This has direct implications for agent architecture: **the decision of when to invoke external tools should be domain-aware**, not uniform. A blanket "always verify" policy is wasteful; a blanket "trust internal knowledge" policy is dangerous. The optimal architecture routes verification decisions based on the domain-specific reliability profile of the model's internal knowledge.

---

## Updated Pattern-to-Incentive Mapping

The eight deception patterns identified in Phase 1 map to specific training incentives. The corrected A/B test reveals that these incentives produce different failure modes depending on whether training data is present (Leg 1) or absent (Leg 2).

### Training Incentives That Produce Leg 1

| Incentive | Mechanism | Failure Pattern |
|-----------|-----------|-----------------|
| **Helpfulness optimization** | Models are trained to be helpful, which means providing answers. When training data exists, the model has no incentive to decline even when its knowledge is imprecise. | Confident Micro-Inaccuracy: the model provides an answer that is mostly right rather than acknowledging partial knowledge. |
| **Confidence as quality signal** | During RLHF, confident responses are typically rated higher than hedged responses. This trains the model to present information with certainty. | Uniform confidence across correct and incorrect claims: the model cannot distinguish what it knows accurately from what it knows approximately. |
| **Training data volume as proxy for knowledge** | More training data on a topic creates stronger internal representations, but volume does not guarantee accuracy when sources conflict. | High confidence on topics with extensive but contradictory training data (e.g., software version numbers across different time periods). |
| **Next-token prediction on factual text** | The model learns to produce text that looks like factual writing. Factual writing uses specific numbers, dates, and details. | The model generates specific details (version 1.0.0, year 2006, 11 films) because that is what factual text looks like, even when the specific values are wrong. |

### Training Incentives That Produce Leg 2

| Incentive | Mechanism | Failure Pattern |
|-----------|-----------|-----------------|
| **RLHF safety training** | Models are trained to acknowledge limitations and avoid fabrication on topics outside their knowledge. | Appropriate decline or heavy hedging on post-cutoff questions. This is a successfully-trained behavior. |
| **Cutoff-awareness fine-tuning** | Models are explicitly trained to recognize and acknowledge their training cutoff date. | Calibrated confidence on PC questions (0.87 average). The model knows what it does not know. |
| **Hallucination penalty** | Post-training processes penalize obvious fabrication, creating a bias toward caution on unfamiliar topics. | Low factual accuracy (0.00-0.20) on PC questions, but this reflects honest uncertainty rather than failure. |

### The Asymmetry Explained

The training pipeline successfully teaches models to handle Leg 2 (unknown topics) but fails to address Leg 1 (partially-known topics) because:

1. **RLHF evaluators can detect Leg 2 failures** (obvious fabrication about unknown topics) but **cannot easily detect Leg 1 failures** (subtle inaccuracies about known topics) without their own external verification.
2. **Leg 2 has a clear signal** (training data absent = be cautious) while **Leg 1 has no clear signal** (training data present but partially incorrect is indistinguishable from training data present and fully correct).
3. **The reward model conflates confidence with quality** because in training data, confident factual text is usually correct. The rare cases where confident text contains errors are not sufficiently penalized to teach the model to distinguish them.

---

## The Snapshot Problem

The Snapshot Problem is the root architectural cause of Leg 1 failures. It explains why LLM internal knowledge is unreliable for rapidly-evolving domains and reliable for stable domains.

### Definition

**The Snapshot Problem:** Training data captures the state of the world at the time each document was written. When the model is trained on documents from multiple time periods, it acquires multiple contradictory snapshots of the same fact. The model has no mechanism to determine which snapshot is most recent, most authoritative, or currently correct.

### How Snapshots Become Errors

Consider how the model learns about the Python `requests` library:

```
Snapshot 2019: "requests 2.22.0 uses urllib3 1.25..."
Snapshot 2020: "requests 2.24.0 added support for..."
Snapshot 2021: "requests 2.26.0 changed the..."
Snapshot 2022: "requests 2.28.0 deprecated..."
Snapshot 2023: "requests 2.31.0 is the latest..."
```

During training, the model sees all five snapshots with equal weight. Each snapshot makes factual claims about version numbers, API behavior, and dependencies that were true at the time of writing but may not be true at any other time. The model must compress these contradictory snapshots into a single internal representation.

The compression process produces what we observe as Leg 1 errors:
- **Version number errors:** The model selects a version number that is a plausible blend of the snapshots it has seen, but may not correspond to any actual version.
- **API behavior errors:** The model describes behavior that was true in one version but not in the version it claims to be describing.
- **Dependency errors:** The model describes a dependency relationship from one snapshot while describing a version from a different snapshot.

### Snapshot Stability Spectrum

The severity of the Snapshot Problem varies by domain based on how frequently the underlying facts change:

| Stability Level | Description | Domains | Snapshot Conflict Rate |
|----------------|-------------|---------|----------------------|
| **Immutable** | Facts never change | Fundamental science, mathematics, established history | Near zero |
| **Slow-evolving** | Facts change on decade timescales | Geography, demographics, medical consensus | Low |
| **Medium-evolving** | Facts change on year timescales | Pop culture counts, sports records, political geography | Moderate |
| **Fast-evolving** | Facts change on month/week timescales | Software versions, API details, current events | High |
| **Ephemeral** | Facts change continuously | Stock prices, weather, live scores | Infinite (not addressable by training data) |

The A/B test results map directly to this spectrum:
- **Science/Medicine (Immutable/Slow):** 0.00 CIR -- snapshots agree
- **History/Geography (Slow/Medium):** 0.05 CIR -- rare snapshot conflicts
- **Pop Culture/Media (Medium):** 0.075 CIR -- moderate snapshot conflicts
- **Sports/Adventure (Medium):** 0.05 CIR -- moderate but model hedges
- **Technology/Software (Fast):** 0.30 CIR -- extensive snapshot conflicts

### Architectural Implication

The Snapshot Problem is not fixable by better training alone. Even a perfectly trained model will produce snapshot conflicts when trained on documents from different time periods about fast-evolving topics. The architectural solution is **external verification for fast-evolving domains** -- which is exactly what tool-augmented retrieval provides.

---

## Domain-Specific Reliability Tiers

Based on the empirical A/B test results and the Snapshot Problem analysis, we define five reliability tiers for LLM internal knowledge. These tiers should inform tool-routing decisions in agent architectures.

### Tier Definitions

| Tier | Reliability Rating | Domains | ITS Factual Accuracy | CIR | Verification Policy |
|------|-------------------|---------|---------------------|-----|-------------------|
| **T1: Highly Reliable** | 0.95+ FA, 0.00 CIR | Established science, mathematics, fundamental chemistry/physics | 0.95 | 0.00 | Trust with spot-check |
| **T2: Reliable** | 0.90+ FA, <0.05 CIR | Established history, well-documented geography, canonical literature | 0.925 | 0.05 | Trust with verification of specific dates/numbers |
| **T3: Moderate** | 0.80+ FA, <0.10 CIR | Pop culture, sports records, biographical details | 0.825-0.85 | 0.05-0.075 | Verify counts, dates, and specific claims |
| **T4: Unreliable** | <0.80 FA, >0.10 CIR | Software versions, API details, recent technical changes | 0.55 | 0.30 | Always verify externally |
| **T5: Unavailable** | <0.20 FA | Post-cutoff events, real-time data | 0.00-0.20 | N/A (model declines) | External retrieval required |

### Tier Assignment Criteria

A domain should be assigned to a tier based on:

1. **Fact stability:** How frequently do the core facts in this domain change?
2. **Source consistency:** Do training data sources agree on the facts?
3. **Specificity of claims:** Does the domain require precise numbers, dates, or version identifiers?
4. **Empirical CIR:** What is the observed Confident Inaccuracy Rate for this domain?

### Cross-Tier Error Characteristics

| Characteristic | T1-T2 (Reliable) | T3 (Moderate) | T4 (Unreliable) | T5 (Unavailable) |
|---------------|-------------------|---------------|-----------------|-------------------|
| Error type | Rare imprecision | Count/date errors | Version/API errors | Complete absence |
| Model confidence | Justified | Slightly overconfident | Significantly overconfident | Appropriately low |
| Detection difficulty | Low (errors are rare) | Moderate (embedded in correct context) | High (extensive correct context masks errors) | Low (model signals uncertainty) |
| User risk | Minimal | Moderate | High | Low (user knows to verify) |
| Tool augmentation benefit | Marginal | Moderate | Critical | Essential |

---

## Mitigation Architecture

The Two-Leg Thesis demands different mitigation strategies for each leg. Leg 2 is already addressed by standard RAG/tool-augmented retrieval. Leg 1 requires a more sophisticated approach: **domain-aware tool routing**.

### Architecture Overview

```
User Query
    |
    v
[Domain Classifier]  -->  Classifies query into reliability tier (T1-T5)
    |
    v
[Tool Router]
    |
    +-- T1 (Highly Reliable): Use internal knowledge, no tool call
    |
    +-- T2 (Reliable): Use internal knowledge, flag specific numbers/dates for optional verification
    |
    +-- T3 (Moderate): Use internal knowledge with selective WebSearch verification of counts/dates
    |
    +-- T4 (Unreliable): ALWAYS invoke WebSearch/documentation lookup before responding
    |
    +-- T5 (Unavailable): ALWAYS invoke WebSearch; decline if tool returns no results
    |
    v
[Response Generator]  -->  Synthesizes internal knowledge + tool results
    |
    v
[Confidence Annotator]  -->  Adds per-claim confidence based on tier + verification status
    |
    v
User Response
```

### Component Design

#### Domain Classifier

The Domain Classifier examines the user's query and assigns it to a reliability tier. This is a classification task that the LLM itself can perform, guided by the tier definitions above.

**Input:** User query (natural language)
**Output:** Reliability tier (T1-T5) with justification

**Classification signals:**
- Mentions of specific software, libraries, or APIs --> T4
- Questions about current events or recent developments --> T5
- Questions about established scientific facts --> T1
- Questions about historical events with specific dates --> T2
- Questions about counts, records, or rankings in entertainment/sports --> T3

**Important:** The classifier should err toward lower tiers (more verification) when uncertain. Misclassifying a T4 query as T2 produces Leg 1 errors. Misclassifying a T2 query as T4 only produces unnecessary tool calls.

#### Tool Router

The Tool Router implements the verification policy for each tier. For T1-T2, it passes the query directly to the response generator with internal knowledge. For T3-T5, it invokes appropriate external tools before response generation.

**Tool selection by tier:**

| Tier | Primary Tool | Fallback | Latency Impact |
|------|-------------|----------|----------------|
| T1 | None | None | Zero |
| T2 | None (optional WebSearch for specific numbers) | None | Zero to minimal |
| T3 | WebSearch for specific claims | Internal knowledge if tool fails | Moderate |
| T4 | WebSearch or Context7 (for library docs) | Decline if tool fails | Moderate to high |
| T5 | WebSearch (required) | Decline with explanation | High |

#### Confidence Annotator

The Confidence Annotator adds per-claim confidence markers to the response based on the verification status of each claim. This addresses the trust calibration problem identified in the Two-Leg Thesis.

**Confidence levels:**
- **Verified:** Claim was checked against external source and confirmed
- **Internal (High Stability):** Claim is from T1-T2 domain, not externally verified but high historical reliability
- **Internal (Moderate Stability):** Claim is from T3 domain, not externally verified
- **Unverified:** Claim could not be verified; user should check independently

### Latency-Accuracy Tradeoff

The domain-aware routing architecture introduces a tradeoff between response latency and accuracy:

| Strategy | Latency | Accuracy | Use Case |
|----------|---------|----------|----------|
| Always use tools (T1-T5) | High | Highest | Mission-critical applications |
| Domain-aware routing (T3-T5 only) | Moderate | High | General-purpose agents |
| Never use tools | Lowest | Variable (0.55-0.95 by domain) | Low-stakes, latency-sensitive |

The domain-aware routing strategy provides the best latency-accuracy tradeoff for most applications by avoiding unnecessary tool calls for reliable domains while ensuring verification for unreliable ones.

---

## Jerry Framework as Proof-of-Concept

The Jerry Framework itself demonstrates a governance-based approach to mitigating LLM unreliability. While not designed specifically as a response to the Two-Leg Thesis, its architectural patterns address both failure legs.

### Leg 1 Mitigations in Jerry

| Jerry Feature | Mitigation Mechanism | Leg 1 Relevance |
|--------------|---------------------|-----------------|
| **WebSearch-enabled agents** | Agents like ps-researcher use WebSearch for external verification | Directly addresses confident micro-inaccuracy by checking claims against current sources |
| **Context7 integration (MCP-001)** | Mandatory external documentation lookup for library/framework references | Specifically targets the highest-CIR domain (Technology/Software) |
| **Creator-critic-revision cycle (H-14)** | Multi-pass review catches errors that single-pass generation misses | Critic agents can identify claims that "sound wrong" and flag for verification |
| **Quality gate scoring (H-13)** | Evidence Quality dimension (0.15 weight) penalizes unverified claims | Creates systematic incentive to verify rather than assert |
| **S-011 Chain-of-Verification** | Strategy template for systematic claim verification | Directly targets Leg 1 by decomposing responses into individual verifiable claims |

### Leg 2 Mitigations in Jerry

| Jerry Feature | Mitigation Mechanism | Leg 2 Relevance |
|--------------|---------------------|-----------------|
| **WebSearch as default tool** | All research agents have WebSearch access | Standard RAG approach that solves Leg 2 completely |
| **Memory-Keeper persistence (MCP-002)** | Cross-session context preservation | Prevents re-encountering Leg 2 gaps that were already resolved |
| **Orchestration phase boundaries** | Structured workflow with explicit knowledge handoff | Ensures Leg 2 gaps identified in early phases are filled before later phases depend on them |

### Governance as Architecture

Jerry's approach to LLM reliability is fundamentally **governance-based** rather than **model-based**. Instead of trying to make the model more reliable (which does not solve the Snapshot Problem), Jerry wraps the model in a governance framework that:

1. **Mandates external verification** for high-risk domains (Context7 for libraries, WebSearch for current events)
2. **Enforces multi-pass review** that catches errors missed in generation (creator-critic cycle)
3. **Quantifies confidence** through structured scoring rather than relying on model self-assessment
4. **Persists verified knowledge** so that corrected information is available in future sessions

This governance approach is more robust than model improvements alone because it addresses the Snapshot Problem at the architectural level rather than the training level. Even a perfectly trained model will produce snapshot conflicts; a governance framework catches those conflicts through external verification.

### Observed Effectiveness

The McConkey research provides a concrete example of Jerry's governance preventing Leg 1 errors:

1. **Initial generation:** LLM produced confident biographical claims about Shane McConkey (Leg 1 territory -- training data available)
2. **WebSearch verification:** Jerry's mandatory external verification (via research agents) caught specific errors in dates and attribution
3. **Revision cycle:** Errors were corrected in subsequent revision passes
4. **Final output:** Published content was factually accurate, having survived both Leg 1 detection and Leg 2 filling

Without Jerry's governance framework, the Leg 1 errors would have been published as-is because the model presented them with the same confidence as its correct claims.

---

## Recommendations for Agent System Designers

Based on the Two-Leg Thesis, the Snapshot Problem analysis, and the domain-specific reliability tiers, we recommend the following architectural practices for designers of LLM-based agent systems.

### Recommendation 1: Implement Domain-Aware Tool Routing

**Do not treat all queries equally for verification.** Implement a domain classifier that assigns queries to reliability tiers and routes tool calls accordingly. This provides the optimal latency-accuracy tradeoff.

**Minimum viable implementation:**
- Classify queries mentioning specific software/libraries/APIs as T4 (always verify)
- Classify queries about current events as T5 (always verify)
- Allow internal knowledge for established facts (T1-T2)
- Default to T3 (selective verification) when uncertain

### Recommendation 2: Never Trust Version Numbers, Dates, or Counts from Internal Knowledge

**These are the highest-CIR claim types across all domains.** Even when the model's general knowledge of a topic is accurate, specific numbers are disproportionately likely to be wrong due to the Snapshot Problem.

**Implementation:** When the response generation process produces a specific number, date, version, or count, flag it for external verification regardless of the domain tier.

### Recommendation 3: Add Per-Claim Confidence Markers

**Do not present all claims with equal confidence.** Add confidence markers that reflect whether each claim was externally verified, sourced from a reliable domain, or potentially subject to Leg 1 errors.

**Implementation:** Post-process responses to annotate claims with verification status. This helps users calibrate their trust correctly instead of developing the false confidence that the Two-Leg Thesis identifies.

### Recommendation 4: Use the Creator-Critic Pattern for Factual Content

**Single-pass generation is insufficient for factual accuracy.** Implement a creator-critic-revision cycle where the critic specifically looks for Leg 1 indicators:
- Specific numbers stated without hedging
- Version numbers or release dates
- Claims about "the current" or "the latest" anything
- Counts or rankings

**Implementation:** The critic agent should have WebSearch access and should verify a random sample of specific claims in each response. This is more efficient than verifying everything and catches the highest-risk error types.

### Recommendation 5: Log and Learn from Verified Errors

**Track which claims were corrected by external verification to improve domain classification over time.** Build a corpus of "internal knowledge errors" that can inform the domain classifier and tool router.

**Implementation:** When a tool-verified claim differs from what the model would have generated internally, log the domain, claim type (version, date, count, relationship), and error magnitude. Use this corpus to refine reliability tier boundaries.

### Recommendation 6: Design for the 85% Problem, Not the 0% Problem

**Most LLM reliability discussions focus on Leg 2 (the model does not know).** Agent architectures should ALSO address Leg 1 (the model thinks it knows but is 15% wrong). The 85% accuracy case is more dangerous than the 0% accuracy case because:

- Users trust the output (it looks right)
- Errors are embedded in correct context (hard to spot)
- The model does not hedge (no warning signals)
- Spot-checking reinforces false trust (most checked facts are correct)

**Implementation:** Architect for the assumption that ANY response about a fast-evolving topic contains at least one subtle error. Design verification workflows that catch these errors before they reach the user.

### Recommendation 7: Context7 for Library Documentation, WebSearch for Everything Else

**For technology/software domains (T4), use specialized documentation tools rather than general web search.** Context7 provides structured access to library documentation that is more reliable than web search results for API details, version histories, and configuration options.

**Implementation:** Route T4 queries through Context7 (resolve-library-id -> query-docs) as the primary tool, with WebSearch as a fallback when Context7 has no coverage.

### Recommendation 8: Governance Over Model Improvement

**Do not wait for better models to solve Leg 1.** The Snapshot Problem is inherent in the training paradigm: any model trained on documents from multiple time periods will have contradictory snapshots of evolving facts. Architectural and governance solutions (mandatory verification, multi-pass review, confidence annotation) are available now and effective.

**Implementation:** Invest in verification infrastructure and governance frameworks rather than relying solely on model upgrades. Model improvements will reduce Leg 1 error rates but cannot eliminate them as long as the Snapshot Problem exists.

---

## Failure Mode Taxonomy

The Two-Leg Thesis, combined with the domain reliability analysis, produces a taxonomy of LLM failure modes organized by detectability and domain.

### Taxonomy Matrix

| | T1-T2 (Stable Domains) | T3 (Moderate Domains) | T4 (Fast-Evolving Domains) | T5 (Post-Cutoff) |
|---|---|---|---|---|
| **User-Detectable** | Rare; model rarely fails here | Occasional; users may notice count errors | Rare; errors look authoritative | Common; model signals uncertainty |
| **Critic-Detectable** | Very rare | Moderate; critic can spot "round number" heuristics | Moderate; critic can flag version/date claims | Common; critic sees hedging |
| **Tool-Only-Detectable** | Extremely rare | Occasional; specific claims need verification | **COMMON -- this is the danger zone** | Always (by definition) |
| **Undetectable** | Negligible | Rare | Rare (tools catch most T4 errors) | N/A |

The danger zone is **Tool-Only-Detectable errors in T4 (Fast-Evolving) domains**. These are Leg 1 errors that:
- The user cannot detect (the answer looks authoritative)
- A critic agent cannot reliably detect (the surrounding context is correct)
- Only external tool verification can catch

This is why Recommendation 1 (domain-aware tool routing) mandates always verifying T4 queries externally.

### Error Severity Classification

| Error Type | Example | Severity | Detection Method |
|-----------|---------|----------|-----------------|
| **Wrong version number** | "requests 1.0.0" vs "0.6.0" | High (can cause build failures) | Context7 / PyPI lookup |
| **Wrong date (off by one year)** | "2006" vs "2005" | Medium (misleading but rarely actionable) | WebSearch |
| **Wrong count** | "11 films" vs "6 films" | Medium (factually wrong, embarrassing if published) | WebSearch |
| **Wrong attribution** | Descent attributed to wrong mountain | Medium (factually wrong in specific) | WebSearch / domain expert |
| **Wrong relationship** | "wraps directly" vs "adapter pattern" | Low-Medium (technically inaccurate but conceptually close) | Source code / documentation |
| **Omission** | Missing events from a list | Low (incomplete but not wrong) | WebSearch for complete list |

---

## Open Questions

The following architectural questions remain unresolved and represent areas for future investigation:

### Q1: Can the Domain Classifier Be Automated Reliably?

The domain-aware tool routing architecture depends on a Domain Classifier that correctly assigns queries to reliability tiers. If the classifier itself is an LLM, it may have its own Leg 1 errors (confidently misclassifying a T4 query as T2). Research is needed on the reliability of LLM-based domain classification for this specific purpose.

### Q2: How Does Reliability Vary Across LLM Families?

The empirical evidence in this analysis is from a single model family (Claude). Other architectures (GPT, Gemini, Llama, Mistral) may have different domain reliability profiles based on their training data composition and RLHF processes. Cross-model validation would strengthen the tier definitions.

### Q3: Does Fine-Tuning on Verified Data Reduce Leg 1?

If a model were fine-tuned specifically on verified, timestamped factual claims (rather than raw web text), would the Snapshot Problem be reduced? This is an open research question with implications for training pipeline design.

### Q4: What Is the Optimal Verification Sampling Rate?

Recommendation 4 suggests the critic agent should verify "a random sample" of specific claims. What sampling rate provides the best cost-accuracy tradeoff? This depends on the error rate, error cost, and verification latency for each domain tier.

### Q5: How Do Multi-Turn Interactions Affect Leg 1?

The A/B test used single-turn factual questions. In multi-turn conversations, Leg 1 errors may compound (a wrong version number in turn 1 leads to wrong API advice in turn 3). The compounding dynamics of Leg 1 errors in multi-turn contexts are not yet empirically characterized.

---

## References

| Source | Content | Relevance |
|--------|---------|-----------|
| ps-synthesizer-002 output | Unified Research Synthesis v2: The Two-Leg Thesis | Primary evidence source; A/B test results and domain analysis |
| Phase 2 A/B Test Results | Raw scoring data for 15 questions across 2 agents and 5 domains | Empirical data underpinning all quantitative claims |
| Phase 1 Evidence Collection (workflow -001) | 8 deception patterns from literature, industry reports, session mining | Pattern definitions and qualitative evidence |
| Jerry Framework CLAUDE.md | Constitutional constraints, MCP integration rules (MCP-001, MCP-002) | Context7 and WebSearch governance as mitigation examples |
| mcp-tool-standards.md | Context7 mandatory usage for library references | Demonstrates T4 mitigation in practice |
| quality-enforcement.md | Creator-critic cycle (H-14), quality gate (H-13) | Multi-pass review as Leg 1 mitigation |
| McConkey research session logs | Real-world Leg 1 error detection and correction | Proof-of-concept for governance-based mitigation |
