# Twitter Thread: Confident Micro-Inaccuracy

> **Agent:** sb-voice-005
> **Pipeline:** PS
> **Workflow:** llm-deception-20260222-002
> **Date:** 2026-02-22
> **Voice:** Saucer Boy (McConkey persona -- calibrated, direct, technically precise)

---

## Content

### Tweet 1/10

We asked an LLM 15 factual questions across 5 domains. No tools, just training data.

It didn't hallucinate. It answered confidently. It was 85% right.

The 15% it got wrong is the interesting part.

Thread.

### Tweet 2/10

The wrong answers weren't wild fabrications. They were subtle:

- A version number off by a major release (1.0.0 vs 0.6.0)
- A date wrong by exactly one year (2006 vs 2005)
- A film count that conflated two phases of a franchise
- A dependency relationship described as it was 3 years ago

Each embedded in paragraphs of correct context. Each stated without hedging.

### Tweet 3/10

We call this Confident Micro-Inaccuracy.

The model has training data. It answers fully. 8 out of 10 facts are right. The 2 that are wrong look identical to the 8 that are right.

No hedging. No "I think." No "approximately." Just wrong, confidently.

### Tweet 4/10

We tested 5 domains. The results aren't uniform.

Science/Medicine: 95% accurate, zero confident errors
History/Geography: 92.5%, minor date issues
Pop Culture: 85%, count errors
Sports: 82.5%, vague on specifics
Technology: 55%, 30% confident inaccuracy rate

Technology is broken.

### Tweet 5/10

Why is technology the worst?

The Snapshot Problem.

Training data captures version numbers, API details, and dependencies at the moment each document was written. The model sees "requests 2.22" in one doc and "requests 2.31" in another, both described as "current."

It picks one. It's confident. It's wrong.

### Tweet 6/10

Why is science the best?

The boiling point of ethanol hasn't changed since it was measured. Every source agrees. Every textbook says the same number.

When training data is consistent across time, the model is reliable.
When training data is contradictory across time, the model is confidently unreliable.

### Tweet 7/10

The second agent had web search and documentation access.

Same 15 questions. 93% accurate on in-training topics. 89% on post-cutoff topics.

The gap between "knows about" and "doesn't know about" that cripples the internal-only agent? Disappears with tool access.

### Tweet 8/10

Two failure modes. Two different danger levels.

Leg 1: Model has training data. Answers confidently. Contains subtle errors. You can't tell which facts are wrong without checking each one. INVISIBLE.

Leg 2: Model lacks training data. Declines or hedges. You know it's struggling. VISIBLE.

Leg 1 is the real problem.

### Tweet 9/10

The trust trap:

1. You ask a question. Answer is correct. Trust builds.
2. You ask another. Correct again. Trust deepens.
3. You ask a third. Answer contains a subtle error. You don't check because trust is high.
4. The wrong fact is now in your head, your doc, your codebase.

85% accuracy creates 100% trust.

### Tweet 10/10

Three rules:

1. Never trust version numbers, dates, or counts from LLM internal knowledge
2. Always verify technology claims externally -- it's the worst domain by far
3. The fix is architectural (tool access), not behavioral (better prompting)

The dangerous failure mode isn't "I don't know." It's "here's a precise, confident, wrong answer."

---

## Metadata

| Field | Value |
|-------|-------|
| Platform | Twitter/X |
| Target audience | AI/ML community, developers, tech-curious professionals |
| Thread length | 10 tweets |
| Avg tweet length | ~250 characters |
| Voice compliance | Direct, declarative sentences. No hedging. Technical precision. Earned energy on key findings. |
| Key hook | "85% right. The 15% it got wrong is the interesting part." |
| Narrative arc | Observation -> Evidence -> Mechanism (Snapshot Problem) -> Contrast (science vs tech) -> Solution |

---

*Agent: sb-voice-005*
*Status: COMPLETED*
*Date: 2026-02-22*
