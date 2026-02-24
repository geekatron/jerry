# Blog Article: The 85% Problem -- When Your AI Is Confidently Wrong

> **Agent:** sb-voice-006
> **Pipeline:** PS
> **Workflow:** llm-deception-20260222-002
> **Date:** 2026-02-22
> **Voice:** Saucer Boy (McConkey persona -- calibrated, direct, technically precise)

---

## Content

### The 85% Problem: When Your AI Is Confidently Wrong

#### The McConkey Problem

I was building a persona based on Shane McConkey -- the freestyle skier who redefined what was possible on snow before dying in a ski-BASE jump in the Italian Dolomites in 2009. I asked an LLM for biographical details. The response was detailed, confident, specific. Film appearances, family details, career milestones. It read like it came from someone who knew the subject.

I fact-checked it with web search because the framework I use requires external verification of all factual claims.

Some of the details were wrong. Not wildly wrong -- not "he was a tennis player" wrong. Subtly wrong. A date off by a year. A film attributed to the wrong production company. A detail about his family that conflated two different sources.

The surrounding narrative was accurate. The errors were small and specific. Without the external verification step, I would have published them as fact. That experience became the seed of a controlled experiment.

#### The Experiment

We designed an A/B test to measure exactly this phenomenon. 15 research questions across 5 knowledge domains:

- **Sports/Adventure:** Niche athlete biographies with limited but error-prone web sources
- **Technology/Software:** Library versions, API changes, dependency details
- **Science/Medicine:** Established facts and corrected misconceptions
- **History/Geography:** Frequently confused dates, capitals, measurements
- **Pop Culture/Media:** Filmographies, award records, biographical specifics

Each domain got 2 in-training-set (ITS) questions -- topics the model has training data for -- and 1 post-cutoff (PC) question -- a topic after the model's knowledge boundary.

**Agent A:** An LLM with no external tools. Training data only. Prompted to answer fully and specifically.

**Agent B:** The same LLM with web search and documentation access. Prompted to verify everything externally.

**Ground truth:** Independently verified answers from authoritative sources, established before either agent saw the questions.

We scored both agents across 7 dimensions, including a new metric we designed for this test: **Confident Inaccuracy Rate (CIR)** -- the proportion of claims stated with high confidence that are factually wrong.

#### What We Found

Agent A scored 85% Factual Accuracy on the in-training-set questions. That sounds good. It is not.

Here is what 85% looks like in practice. Agent A was asked about the Python `requests` library. It correctly identified the creator (Kenneth Reitz), correctly described the library's purpose, and correctly explained the relationship between `requests` and `urllib3`. Then it stated that Session objects were introduced in version 1.0.0.

They were introduced in version 0.6.0.

The error is embedded in a paragraph of correct information. It is stated with the same confidence as the correct claims. A developer reading this answer would have no reason to question it unless they independently checked the PyPI release history. The surrounding accuracy creates trust. The specific error rides that trust into the developer's mental model.

This is not hallucination. The model did not invent a topic. It did not fabricate a citation. It produced a detailed, mostly-correct answer with a specific, confident, wrong fact embedded in it. We call this **confident micro-inaccuracy**.

#### The Two-Leg Thesis

The A/B test reveals two distinct failure modes operating simultaneously:

**Leg 1: Confident Micro-Inaccuracy (the invisible failure)**

When the model HAS training data, it answers fully. It does not hedge. It does not decline. It produces responses that are 85% correct with specific errors woven into the accurate context. The model cannot distinguish its correct claims from its incorrect ones because both come from the same training data.

6 of 10 in-training-set questions produced confident inaccuracies across 4 of 5 domains. Only Science/Medicine was immune.

**Leg 2: Knowledge Gaps (the visible failure)**

When the model LACKS training data (post-cutoff questions), it behaves differently. It declines, hedges, or provides heavily qualified responses. Its Confidence Calibration score on these questions is 0.87 -- it knows when it does not know.

This is the less dangerous failure mode. When a model says "I'm not sure about events after my training cutoff," users know to look elsewhere. The failure is visible.

**The asymmetry is the finding.** The model has good metacognition about its knowledge boundaries (Leg 2) but poor metacognition about its knowledge quality (Leg 1). It knows when it doesn't know. It does not know when it's wrong.

#### The Snapshot Problem

Why does this happen? And why is it worse for some domains than others?

Training data captures the state of the world at the time each document was written. A model trained on web text from 2019 through 2024 has seen the Python `requests` library described at version 2.22, 2.24, 2.26, 2.28, and 2.31 -- each described as "the current version" in its respective document.

The model compresses these contradictory snapshots into a single internal representation. It has no mechanism to determine which snapshot is most recent. It picks a version number that is plausible but may not correspond to any actual state of the library.

This is the **Snapshot Problem**: training data captures point-in-time facts as permanent truths, and the model has no way to resolve conflicts between snapshots from different time periods.

The Snapshot Problem explains the domain hierarchy:

| Domain | Why It's Reliable (or Not) |
|--------|----------------------------|
| **Science/Medicine** (95% FA, 0% CIR) | Facts are stable across time. The boiling point of ethanol is the same in every training document. Every source agrees. |
| **History/Geography** (92.5% FA, 5% CIR) | Most facts are stable, but specific dates can vary across sources. A model might absorb "2006" from one source when the actual date was late 2005. |
| **Pop Culture** (85% FA, 7.5% CIR) | Extensive data but with inconsistencies in counts, awards, and credits. Training data from different years lists different MCU phase compositions. |
| **Sports** (82.5% FA, 5% CIR) | Good general coverage but specific records and achievements are often conflated across similar athletes or events. |
| **Technology** (70% FA, 17.5% CIR) | **The worst domain by far.** Version numbers, API details, and dependencies change constantly. Every training snapshot describes a different "current" state. The model is confident because it has seen the topic extensively. It is wrong because the snapshots contradict each other. |

When training data is abundant and consistent, the model is reliable. When training data is abundant but inconsistent, the model is confidently unreliable. Volume creates confidence. Consistency creates accuracy. Technology has volume without consistency.

#### The Tool-Augmented Agent

Agent B -- the same model with web search -- scored 93% on in-training-set questions and 87% on post-cutoff questions. The devastating ITS/PC divide that defines Agent A (85% vs 7%) shrinks to a 6-point gap with tool access.

This is the central architectural insight: **tool-augmented retrieval doesn't just solve the post-cutoff problem (Leg 2). It also catches the confident micro-inaccuracies in the training data (Leg 1).**

The fix is not better prompting. Telling the model to "be careful" or "only state what you're sure about" does not work because the model cannot distinguish what it knows correctly from what it knows incorrectly. Both come from the same training data with the same internal confidence signal.

The fix is architectural. Give the model access to external verification tools and design the system to use them -- especially for technology, dates, version numbers, counts, and any claim that involves a specific number.

#### What This Means for Builders

If you are building systems that use LLM-generated content, three principles:

**1. Never trust specific numbers from internal knowledge.**

Version numbers, release dates, film counts, population figures, record times -- these are the highest-CIR claim types across every domain we tested. Any specific number in an LLM response should be treated as "plausible but unverified" unless confirmed against an external source.

**2. Implement domain-aware verification.**

Not all claims need external verification. Established scientific facts (T1) are highly reliable. Historical facts (T2) need date verification but not general fact verification. Technology claims (T4) need verification of everything.

A blanket "always verify" policy wastes latency. A blanket "trust the model" policy introduces errors. Domain-aware routing provides the right tradeoff.

**3. Design for the 85% problem.**

The field's attention is on hallucination -- the 0% accuracy case where the model fabricates entirely. That failure mode is increasingly well-understood and increasingly detectable.

The harder problem is the 85% accuracy case. The response looks right. Most of it is right. The parts that are wrong are specific, confident, and embedded in correct context. Users who spot-check will almost certainly find correct facts, reinforcing trust. The unchecked facts have a 15% chance of being wrong.

This is the failure mode that propagates. Not because it's dramatic, but because it's invisible.

#### Methodology Note

This research used 15 questions across 5 domains scored on 7 dimensions (Factual Accuracy, Confident Inaccuracy Rate, Currency, Completeness, Source Quality, Confidence Calibration, Specificity) against independently verified ground truth from authoritative sources including sqlite.org, PyPI, NIH, Cochrane Library, Britannica, IMDb, and official government databases.

The findings are directional -- 15 questions provides evidence for patterns but not statistical proof. The domain reliability hierarchy should be treated as a well-supported hypothesis, not a universal law. Results are specific to the Claude model family; other architectures may show different patterns.

What is not directional is the core finding: when an LLM has training data on a topic, it can be confidently wrong about specific details. This is the failure mode that matters most for real-world reliability.

---

## Metadata

| Field | Value |
|-------|-------|
| Platform | Blog (Medium, personal site, or company blog) |
| Target audience | AI practitioners, engineering leaders, technical decision-makers |
| Word count | ~1,400 |
| Voice compliance | Direct, warm, technically precise. McConkey touchstone opens the piece. Inverted expectation. Earned energy. No forced humor. |
| Narrative arc | Personal experience (McConkey) -> Experiment design -> Key finding (85%) -> Mechanism (Snapshot Problem) -> Domain hierarchy -> Solution (tool access) -> Builder takeaways |
| Key hook | "Your AI assistant is 85% right and 100% confident" |
| Citations | PyPI, sqlite.org, NIH, Cochrane Library, Britannica, IMDb |

---

*Agent: sb-voice-006*
*Status: COMPLETED*
*Date: 2026-02-22*
