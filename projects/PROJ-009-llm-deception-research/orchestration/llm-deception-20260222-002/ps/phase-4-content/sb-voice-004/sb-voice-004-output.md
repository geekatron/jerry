# LinkedIn Post: The 85% Problem

> **Agent:** sb-voice-004
> **Pipeline:** PS
> **Workflow:** llm-deception-20260222-002
> **Date:** 2026-02-22
> **Voice:** Saucer Boy (McConkey persona -- calibrated, direct, technically precise)

---

## Content

Your AI assistant is 85% right and 100% confident. That's the problem.

We ran an A/B test. 15 research questions across 5 knowledge domains. One LLM agent with no tools -- just training data. One with web search and documentation access. A verified ground truth to score both against.

The agent without tools didn't hallucinate. It didn't fabricate topics or invent citations. It did something worse: it answered with specific, detailed, mostly-correct responses that contained subtle factual errors stated with the same confidence as the correct facts.

Version numbers off by a major release. Dates wrong by exactly one year. Film counts that conflated different phases of a franchise. Each error embedded in paragraphs of accurate context. Each stated without hedging.

We call this the Two-Leg Thesis:

**Leg 1:** When the model HAS training data, it produces answers that are 85% correct with confident micro-inaccuracies woven in. This is the invisible failure mode. You can't catch it without checking every claim against an external source.

**Leg 2:** When the model LACKS training data, it declines or hedges. This is the visible failure mode. You know the model is struggling because it tells you.

The dangerous leg is Leg 1. Not because the errors are large -- they're small, specific, and plausible. But because the surrounding accuracy builds trust. You spot-check two facts, both are correct, and you stop checking. The third fact is wrong and you've already moved on.

The domain matters. We tested five:

- Science/Medicine: 95% accurate, zero confident errors. Stable facts produce reliable training data.
- History/Geography: 92.5% accurate, minor date precision errors.
- Pop Culture: 85% accurate, count errors and filmography gaps.
- Sports: 82.5% accurate, vague on specific records.
- Technology/Software: 55% accurate, 30% confident inaccuracy rate. Version numbers, API details, dependency relationships -- all unreliable.

Technology is the worst domain because training data captures snapshots of rapidly-evolving information. The model has seen "requests 2.22" and "requests 2.31" and "requests 2.32" in different documents, all described as "current." It picks one. It's wrong. It's confident.

The tool-augmented agent? Near-parity across all domains. 93% on in-training questions, 89% on post-cutoff questions. The ITS/PC divide that cripples the internal-only agent disappears with tool access.

The fix is architectural, not behavioral. Better prompting doesn't solve the Snapshot Problem. External verification does.

Three takeaways for anyone building with LLMs:

1. Never trust version numbers, dates, or counts from internal knowledge alone. These are the highest-risk claim types across every domain we tested.
2. Implement domain-aware verification. Always verify technology claims externally. Allow higher trust for established scientific facts. Default to verification when uncertain.
3. Design for the 85% problem, not the 0% problem. The field focuses on hallucination (the model doesn't know). The harder problem is confident micro-inaccuracy (the model thinks it knows).

Full methodology: 15 questions, 7-dimension scoring rubric including Confident Inaccuracy Rate, verified ground truth from authoritative sources. The A/B test was designed to catch exactly this -- not knowledge gaps, but the errors hiding inside otherwise correct answers.

---

## Metadata

| Field | Value |
|-------|-------|
| Platform | LinkedIn |
| Target audience | AI/ML practitioners, engineering leaders, product managers |
| Word count | ~450 |
| Voice compliance | Direct, warm, technically precise. No forced humor. Inverted expectation opening. |
| Key hook | "85% right and 100% confident" |
| CTA | Three actionable takeaways |

---

*Agent: sb-voice-004*
*Status: COMPLETED*
*Date: 2026-02-22*
