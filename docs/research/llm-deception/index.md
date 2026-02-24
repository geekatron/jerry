# LLM Deception Research

> **"85% right and 100% confident."** That is the failure mode nobody talks about. LLMs do not just hallucinate from ignorance -- they weave subtle errors into otherwise accurate responses, stated with the same confidence as the facts surrounding them.

---

## Key Findings

- LLMs exhibit **two distinct failure modes** (the Two-Leg Thesis): confident micro-inaccuracy on known topics (Leg 1) and honest decline on unknown topics (Leg 2)
- Leg 1 is far more dangerous because it is **invisible to users** -- spot-checking reinforces trust while unverified claims carry a ~15% error rate
- **Technology/Software** is the least reliable domain (0.70 accuracy, 0.175 CIR) due to rapidly-evolving training data snapshots
- **Science/Medicine** is the most reliable domain (0.95 accuracy, 0.00 CIR) due to stable, consistent training data
- Tool-augmented retrieval (WebSearch) raises accuracy from 0.85 to 0.93 on known topics and from 0.07 to 0.87 on unknown topics

---

## Performance Metrics

??? abstract "Agent A vs Agent B: Core Metrics"
    | Metric | Agent A (No Tools) | Agent B (WebSearch) |
    |--------|-------------------|---------------------|
    | Overall ITS Factual Accuracy | 0.850 | 0.930 |
    | Overall PC Factual Accuracy | 0.070 | 0.870 |
    | Confident Inaccuracy Rate (ITS) | 0.070 | 0.015 |
    | Confidence Calibration (PC) | 0.870 | 0.900 |

    **ITS** = In-Training-Set questions (model has training data). **PC** = Post-Cutoff questions (model lacks training data). **CIR** = Confident Inaccuracy Rate (proportion of high-confidence claims that are factually wrong).

??? abstract "Domain Reliability Breakdown"
    | Domain | Agent A ITS Accuracy | Agent A CIR | Agent B ITS Accuracy | Key Error Pattern |
    |--------|---------------------|-------------|---------------------|-------------------|
    | Science/Medicine | 0.950 | 0.000 | 0.950 | No significant errors |
    | History/Geography | 0.925 | 0.050 | 0.950 | Minor date errors |
    | Pop Culture/Media | 0.850 | 0.075 | 0.925 | Count errors, filmography gaps |
    | Sports/Adventure | 0.825 | 0.050 | 0.925 | Missing specifics, vague on records |
    | Technology/Software | 0.700 | 0.175 | 0.900 | Version numbers, dependency details |

---

## Methodology

??? note "Study Design"
    The study uses a controlled A/B test with 15 questions across 5 knowledge domains (Sports/Adventure, Technology/Software, Science/Medicine, History/Geography, Pop Culture/Media). Questions are split into 10 In-Training-Set (ITS) and 5 Post-Cutoff (PC) to isolate the two failure modes. Agent A operates without tools (internal knowledge only); Agent B has WebSearch enabled. Each question-agent pair is scored on Factual Accuracy, Confident Inaccuracy Rate, Confidence Calibration, and Completeness.

    This corrected design addresses a limitation in an earlier test that used only post-cutoff questions -- revealing only Leg 2 (honest decline) while Leg 1 (confident micro-inaccuracy) remained invisible.

---

## Study Pages

<div class="grid cards" markdown>

-   :material-alert-circle-outline:{ .lg .middle } **The 85% Problem**

    ---

    The central finding: when LLMs have training data, they produce answers that are mostly correct but embed subtle factual errors with full confidence. Why this is worse than hallucination.

    [:octicons-arrow-right-24: Read more](the-85-problem.md)

-   :material-flask-outline:{ .lg .middle } **Methodology**

    ---

    A/B test design, ITS/PC question split, 7-dimension scoring rubric, domain selection rationale, and limitations of the 15-question sample.

    [:octicons-arrow-right-24: Read more](methodology.md)

-   :material-sitemap-outline:{ .lg .middle } **Architecture Implications**

    ---

    Domain-aware verification strategies, agent design patterns for tool-augmented retrieval, and the Snapshot Problem in technology domains.

    [:octicons-arrow-right-24: Read more](architecture.md)

</div>

---

## Quality Gate Scores

All deliverables passed the 0.92 threshold (H-13) via C4 adversarial tournament scoring.

| Gate | Phase | R1 Score | R2 Score | Status |
|------|-------|----------|----------|--------|
| QG-1 | Evidence Collection | 0.952 | -- | PASS |
| QG-2 | A/B Test V&V | 0.88 | 0.92 | PASS (R2) |
| QG-3 | Research Synthesis | 0.82 | 0.92 | PASS (R2) |
| QG-4 | Content QA | 0.90 | 0.94 | PASS (R2) |
| QG-5 | Final V&V | 0.93 | -- | PASS |

??? note "Leniency Bias Observation"
    Self-assessed scores were uniformly 0.96 across all phases. C4 adversarial tournament actual scores ranged 0.82--0.93 (delta -0.03 to -0.14). This validates the necessity of independent adversarial tournament scoring per S-014 leniency bias counteraction.
