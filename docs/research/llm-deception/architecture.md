# Architecture & Recommendations

> Why LLM reliability is domain-dependent, how to classify domains by risk, and what builders should do about it.

---

## Key Findings

- **The Snapshot Problem** is the root cause of confident inaccuracy — LLMs compress contradictory training snapshots from different time periods into a single representation, producing subtle errors in fast-evolving domains
- Domain reliability follows a **five-tier spectrum** (T1-T5) from highly reliable (established science) to unavailable (post-cutoff events), each demanding a different verification policy
- The optimal architecture is **domain-aware tool routing** — verify aggressively in fast-evolving domains, trust internal knowledge in stable ones
- Governance-based mitigation (mandatory verification, multi-pass review, confidence annotation) is available now and does not depend on model improvements

---

## The Snapshot Problem

The Snapshot Problem is the structural explanation for why LLMs are "85% right and 100% confident." It is not a bug in any particular model — it is an inherent consequence of how all current LLMs are trained.

**Definition:** Training data captures the state of the world at the time each document was written. When a model trains on documents from multiple time periods, it acquires multiple contradictory snapshots of the same fact. The model has no mechanism to determine which snapshot is most recent, most authoritative, or currently correct.

??? note "How Snapshots Become Errors"
    Consider how a model learns about the Python `requests` library:

    ```
    Snapshot 2019: "requests 2.22.0 uses urllib3 1.25..."
    Snapshot 2020: "requests 2.24.0 added support for..."
    Snapshot 2021: "requests 2.26.0 changed the..."
    Snapshot 2022: "requests 2.28.0 deprecated..."
    Snapshot 2023: "requests 2.31.0 is the latest..."
    ```

    The model sees all five snapshots with equal weight. Each makes factual claims that were true at the time of writing but may not be true at any other time. The model compresses these contradictory snapshots into a single internal representation — and the compression produces characteristic errors:

    - **Version number errors:** The model selects a plausible blend of the snapshots, but it may not correspond to any actual version
    - **API behavior errors:** The model describes behavior from one version while claiming to describe a different version
    - **Dependency errors:** The model describes a dependency relationship from one snapshot while referencing a version from another

The severity of the Snapshot Problem varies by how frequently the underlying facts change:

| Stability | Description | Domains | Snapshot Conflict Rate |
|-----------|-------------|---------|------------------------|
| **Immutable** | Facts never change | Fundamental science, mathematics, established history | Near zero |
| **Slow-evolving** | Facts change on decade timescales | Geography, demographics, medical consensus | Low |
| **Medium-evolving** | Facts change on year timescales | Pop culture counts, sports records, political geography | Moderate |
| **Fast-evolving** | Facts change on month/week timescales | Software versions, API details, current events | High |
| **Ephemeral** | Facts change continuously | Stock prices, weather, live scores | Not addressable by training data |

**The critical insight:** The Snapshot Problem is not fixable by better training alone. Even a perfectly trained model will produce snapshot conflicts when trained on documents from different time periods about fast-evolving topics. The solution is architectural — external verification for domains where snapshots conflict.

---

## Domain Reliability Tiers

Based on empirical testing and the Snapshot Problem analysis, LLM internal knowledge falls into five reliability tiers. These tiers should drive verification decisions in any system built on LLMs.

??? abstract "Tier Definitions (T1 through T5)"
    | Tier | Rating | Domains | Expected Accuracy | Confident Inaccuracy Rate | Verification Policy |
    |------|--------|---------|-------------------|---------------------------|---------------------|
    | **T1: Highly Reliable** | 0.95+ accuracy, 0.00 CIR | Established science, mathematics, fundamental physics/chemistry | 0.95 | 0.00 | Trust with spot-check |
    | **T2: Reliable** | 0.90+ accuracy, <0.05 CIR | Established history, well-documented geography, canonical literature | 0.925 | 0.05 | Trust; verify specific dates and numbers |
    | **T3: Moderate** | 0.80+ accuracy, <0.10 CIR | Pop culture, sports records, biographical details | 0.825-0.85 | 0.05-0.075 | Verify counts, dates, and specific claims |
    | **T4: Unreliable** | <0.80 accuracy, >0.10 CIR | Software versions, API details, recent technical changes | 0.70 | 0.175 | Always verify externally |
    | **T5: Unavailable** | <0.20 accuracy | Post-cutoff events, real-time data | 0.00-0.20 | N/A (model declines) | External retrieval required |

??? abstract "Cross-Tier Error Characteristics"
    | Characteristic | T1-T2 (Reliable) | T3 (Moderate) | T4 (Unreliable) | T5 (Unavailable) |
    |----------------|-------------------|---------------|------------------|-------------------|
    | Error type | Rare imprecision | Count/date errors | Version/API errors | Complete absence |
    | Model confidence | Justified | Slightly overconfident | Significantly overconfident | Appropriately low |
    | Detection difficulty | Low (errors are rare) | Moderate (embedded in correct context) | High (correct context masks errors) | Low (model signals uncertainty) |
    | User risk | Minimal | Moderate | **High** | Low (user knows to verify) |
    | Tool augmentation benefit | Marginal | Moderate | **Critical** | Essential |

### The Danger Zone

The most dangerous combination is **T4 (fast-evolving domains) with tool-only-detectable errors**. These are errors that:

- The user cannot detect — the answer looks authoritative and is mostly correct
- A reviewer cannot reliably detect — the surrounding context is accurate
- Only external tool verification can catch

This is why T4 queries must always be verified externally. The model's confidence provides no signal — it is equally confident about its correct and incorrect claims in this tier.

---

## Recommendations for Builders

Practical guidance for developers building systems on LLMs, derived from the Snapshot Problem analysis and domain reliability tiers.

### 1. Implement Domain-Aware Tool Routing

Do not treat all queries equally for verification. Classify queries by reliability tier and route tool calls accordingly.

**Minimum viable implementation:**

- Queries mentioning specific software, libraries, or APIs: **T4** (always verify)
- Queries about current events or recent developments: **T5** (always verify)
- Queries about established scientific or mathematical facts: **T1** (trust)
- When uncertain, default to **T3** (selective verification)

??? note "Latency-Accuracy Tradeoff"
    | Strategy | Latency | Accuracy | Use Case |
    |----------|---------|----------|----------|
    | Always use tools (T1-T5) | High | Highest | Mission-critical applications |
    | Domain-aware routing (T3-T5 only) | Moderate | High | General-purpose agents |
    | Never use tools | Lowest | Variable (0.70-0.95 by domain) | Low-stakes, latency-sensitive |

    Domain-aware routing provides the best tradeoff for most applications by avoiding unnecessary tool calls for reliable domains while ensuring verification for unreliable ones.

### 2. Never Trust Specific Numbers from Internal Knowledge

Version numbers, dates, counts, and rankings are the highest-risk claim types across all domains. Even when the model's general knowledge of a topic is accurate, specific numbers are disproportionately likely to be wrong due to snapshot compression.

**Rule of thumb:** When the model produces a specific number, date, version, or count, flag it for external verification regardless of the domain tier.

### 3. Add Per-Claim Confidence Markers

Do not present all claims with equal confidence. Post-process responses to annotate claims with verification status:

- **Verified** — checked against an external source and confirmed
- **Internal (High Stability)** — from a T1-T2 domain, not externally verified but historically reliable
- **Internal (Moderate Stability)** — from a T3 domain, not externally verified
- **Unverified** — could not be verified; user should check independently

This helps users calibrate trust correctly instead of developing the false confidence that the 85% accuracy rate encourages.

### 4. Use Creator-Critic Patterns for Factual Content

Single-pass generation is insufficient for factual accuracy. Implement a creator-critic-revision cycle where the critic specifically targets high-risk claim types:

- Specific numbers stated without hedging
- Version numbers or release dates
- Claims about "the current" or "the latest" anything
- Counts, rankings, or record claims

The critic should have external tool access and should verify a sample of specific claims in each response. This is more efficient than verifying everything and catches the highest-risk error types.

### 5. Design for 85% Accuracy, Not 0%

Most LLM reliability discussions focus on the case where the model does not know (knowledge gaps, post-cutoff questions). Agent architectures must also address the case where the model thinks it knows but is partially wrong. The 85% accuracy case is more dangerous because:

- Users trust the output (it looks right)
- Errors are embedded in correct context (hard to spot)
- The model does not hedge (no warning signals)
- Spot-checking reinforces false trust (most checked facts are correct)

**Design assumption:** Any response about a fast-evolving topic contains at least one subtle error. Build verification workflows that catch these errors before they reach the user.

### 6. Use Specialized Tools for Technical Domains

For technology and software domains (T4), use structured documentation tools rather than general web search. Documentation-specific APIs provide more reliable results for API details, version histories, and configuration than general search results.

Route T4 queries through documentation tools as the primary source, with web search as a fallback when specialized tools have no coverage.

### 7. Invest in Governance, Not Just Better Models

The Snapshot Problem is inherent in the training paradigm. Any model trained on documents from multiple time periods will have contradictory snapshots of evolving facts. Do not wait for better models to solve this.

Governance-based solutions are available now:

- **Mandatory verification** for high-risk domains
- **Multi-pass review** that catches errors missed in generation
- **Structured confidence scoring** rather than relying on model self-assessment
- **Verified knowledge persistence** so that corrected information is available in future sessions

Model improvements will reduce error rates but cannot eliminate them as long as the Snapshot Problem exists. Governance catches what training cannot.

### 8. Log and Learn from Corrections

Track which claims were corrected by external verification to improve domain classification over time. When a verified claim differs from what the model would have generated internally, log:

- The domain and topic
- The claim type (version, date, count, relationship)
- The error magnitude

Use this corpus to refine reliability tier boundaries and tool routing decisions.

---

## Related Pages

- [LLM Deception Research Overview](index.md) — research goals, scope, and navigation
- [The 85% Problem](the-85-problem.md) — the core finding: confident partial inaccuracy
- [Methodology](methodology.md) — experimental design and evidence collection approach
