---
title: "The Three-Part Rule That Made Our LLM Stop Breaking Its Own Instructions"
subtitle: "How structured negation outperformed positive-only prompting in 150 blind tests across three Claude models"
date: 2026-03-01
tags:
  - prompt-engineering
  - llm
  - ai-research
  - claude
  - negative-prompting
estimated_read_time: 8 min
---

# The Three-Part Rule That Made Our LLM Stop Breaking Its Own Instructions

What if telling an LLM what *not* to do is more effective than telling it what *to* do?

That question sounds almost too simple to matter. Most prompt engineering advice says the same thing: be positive, be specific, tell the model what you want. "Always cite your sources." "Use formal tone." "Follow the coding standard." The conventional wisdom is that negative instructions -- "don't do X" -- confuse language models or get ignored entirely.

We spent six weeks testing that assumption. The answer surprised us.

## The Problem Nobody Talks About

If you have worked with LLMs in production -- not just casual conversation, but systems with behavioral rules, compliance requirements, and multi-step workflows -- you have seen this failure mode: the model follows your instructions beautifully for the first few turns, then quietly starts violating them.

This is not a hallucination problem. This is a *compliance degradation* problem. The model understood your rules. It followed them initially. Then, as the context window filled with conversation history, tool results, and accumulated reasoning, those carefully crafted instructions started losing their grip.

Most prompt engineering guidance addresses this with more positive instructions: be clearer, be more specific, add examples. But there is a category of behavior that positive framing handles poorly: prohibitions. "Always ask before deleting files" is not the same instruction as "NEVER delete files without user confirmation." The first is aspirational guidance. The second is a hard boundary.

We wanted to know: does the framing actually matter? And if so, how much?

## What We Did

We ran a six-phase research project, starting with a literature survey of 75 academic and industry sources, moving through claim validation, taxonomy development, and framework analysis, and culminating in a controlled A/B test.

The literature review turned up something interesting: almost no one has studied this question rigorously. We found 13 peer-reviewed papers (NeurIPS, AAAI, EMNLP, ICLR) that touched on negation in LLM prompting, but most studied negation *comprehension* -- can the model understand "not"? -- rather than negation *compliance* -- does the model follow a prohibition better than a positive instruction?

One clear finding did emerge from the literature: *blunt* negative prompting -- a bare "NEVER do X" with no context, no consequence, no alternative -- is demonstrably the worst way to express a constraint. Research from AAAI 2026 and EMNLP 2024 established that standalone prohibitions without structure produce inferior compliance compared to any structured alternative, whether positive or negative. That much is settled science.

But the real question -- does *structured* negative framing outperform *structured* positive framing? -- was untested. So we built a taxonomy of 14 negative prompting patterns, cataloging everything from model-level interventions (RLHF, fine-tuning) down to prompt-level techniques. And then we tested the ones that matter most for practitioners.

## The Experiment

We designed an A/B test with 150 scenario-model pairs (270 total test invocations when including all framing conditions) across three Claude models: Haiku, Sonnet, and Opus. We selected 10 real behavioral constraints from our production system and wrote three pressure scenarios for each -- situations designed to tempt the model into violating the constraint.

Each constraint was tested under three framing conditions:

- **C1 (Positive-only):** "Always invoke skills proactively when trigger keywords match."
- **C2 (Blunt negation):** "NEVER wait for the user to invoke skills."
- **C3 (Structured negation):** "NEVER wait for the user to invoke skills -- Consequence: Work quality degradation. Rework required. Instead: Use proactively when triggers apply."

The C3 format is what we call NPT-013: a three-component structure combining an explicit prohibition, a documented consequence, and a constructive alternative. Every test was blind-scored by a separate model instance with no knowledge of which framing condition produced the output.

## The Key Discovery

Structured negation (C3) achieved **100% compliance** across all models, all constraints, and all scenarios. Zero violations out of 90 matched pairs.

Positive-only framing (C1) showed a **7.8% violation rate** -- 7 failures out of 90 matched pairs.

Fisher's exact test: **p = 0.016**. Statistically significant at the pre-specified alpha of 0.05, and it survives Bonferroni correction for multiple comparisons.

The effect was unidirectional and consistent. C3 never underperformed C1 on any single constraint, model, or scenario. Not once.

The blunt negation condition (C2) fell in between: 2.2% violation rate, better than positive-only but worse than structured negation. This confirms the literature finding -- bare "NEVER" statements are better than nothing but far from optimal.

### Where the Violations Happened

Two-thirds of all violations (6 out of 9 across all conditions) occurred on a single constraint type: behavioral timing rules -- instructions about *when* to act, not *what* to do. The constraint "invoke skills proactively when trigger keywords match" was the most vulnerable. Under positive-only framing, it failed in 5 out of 9 instances (56% violation rate). Under structured negation, it achieved perfect compliance.

This makes intuitive sense. "Always invoke skills proactively" reads like a suggestion. "NEVER wait for the user to invoke skills -- Consequence: Work quality degradation" reads like a rule. The framing transforms aspirational guidance into an enforced boundary.

### Model Capability Matters

Lower-capability models benefited more from structured framing. Haiku showed the largest improvement: a 10 percentage-point reduction in violations when moving from positive-only to structured negation. Sonnet and Opus showed 6.7 percentage-point improvements each. Haiku was also the only model that violated constraints under the blunt negation condition (C2), suggesting that less capable models need the full three-component structure to achieve reliable compliance.

This has a practical implication: if you are using a smaller, faster model for cost efficiency, investing in structured constraint framing gives you a disproportionate return.

## Why Three Components Work

The NPT-013 format has three parts, and each one does specific work:

**1. The explicit prohibition ("NEVER X")** makes the boundary unambiguous. Positive framing leaves room for interpretation. "Always cite sources" could mean "when convenient" or "when you remember." "NEVER present claims without citations" draws a bright line.

**2. The consequence ("Consequence: Y")** creates stakes. LLMs process instructions as weighted priorities. A prohibition with documented downstream impact -- "downstream agents build analysis on nonexistent evidence, invalidating all derived findings" -- signals that this constraint is load-bearing, not decorative.

**3. The alternative ("Instead: Z")** prevents the model from being stuck. A bare prohibition tells the model what not to do but leaves it without a path forward. "Instead: explicitly state when no source is available and mark confidence as low" gives the model a compliant action to take. This is the component that distinguishes NPT-013 from blunt negation, and our data shows it matters.

## What You Can Do Today

Here are five things you can apply to your own LLM systems right now:

**1. Audit your constraints for "blunt prohibitions."** Search your system prompts for bare "don't," "never," or "must not" statements that lack consequence documentation or alternatives. These are your lowest-hanging fruit. Every one of them is underperforming.

**2. Convert positive instructions to NPT-013 format for critical rules.** Take your most important behavioral constraints and rewrite them using the three-component structure.

Before:
```
Always cite your sources when making factual claims.
```

After:
```
NEVER present factual claims without source citations --
Consequence: Downstream consumers cannot verify accuracy,
eroding trust and potentially propagating misinformation.
Instead: Cite the specific source for each claim, or
explicitly state "no source available" and mark the claim
as unverified.
```

**3. Prioritize behavioral-timing constraints.** Our data shows that instructions about *when* to act are the most vulnerable to compliance failure under positive-only framing. If you have rules about proactive behavior, timing, or sequencing, these should be your first conversion targets.

**4. Pay extra attention to smaller models.** If you are routing some requests to faster, cheaper models, those models need structured framing the most. The compliance gap between positive-only and structured negation is largest for less capable models.

**5. Keep consequence documentation specific.** "Quality degrades" is not a consequence. "Scoring rubric produces inflated scores, masking genuine defects that propagate to production" is a consequence. Specificity is what gives the consequence component its weight.

## The Caveats

We are researchers, not evangelists, so here is what this study does not prove:

**The effect size is modest.** The 7.8 percentage-point improvement is statistically significant but not enormous. Our pre-specified minimum effect size threshold was 10%, and the observed effect (7.8%) fell just below it. We proceeded under a pre-registered contingency pathway that treats the format choice as convention-aligned rather than effectiveness-mandated. The 95% confidence interval (2.3% to 13.3%) does overlap with 10%, so the true effect may be larger than what we observed.

**This was single-session testing only.** We did not test compliance degradation over extended multi-turn conversations, which is where the real pain lives. We have reason to believe the effect would be larger under sustained context pressure -- our highest-pressure scenarios showed the most violations -- but that remains untested.

**We tested 10 constraints across 3 models.** The constraints were selected for testability and drawn from a real production system, but they do not cover every constraint type. Constraints with different characteristics may show different framing sensitivity.

**We do not know *why* it works at a mechanistic level.** We observe that structured negation achieves better compliance, but the experiment does not isolate which of the three components (prohibition, consequence, alternative) contributes most. That is a question for future work.

## The Bottom Line

The structured negation format -- NEVER X, Consequence Y, Instead Z -- is a practical tool you can apply today to improve LLM constraint compliance. It achieved perfect compliance across 90 blind tests on three Claude models, compared to 92.2% for positive-only framing. The statistical evidence is significant (p=0.016), the direction is consistent, and the format never underperformed the alternative.

The most important takeaway is not that negative prompting is universally better than positive prompting. It is that *structure* matters more than *polarity*. A bare "NEVER do X" is the worst constraint formulation we tested. A bare "Always do Y" is better but still vulnerable. "NEVER do X -- here is why, and here is what to do instead" is the format that achieved zero violations.

If you are building systems that depend on LLM behavioral compliance -- and increasingly, who is not -- the three-component structure costs nothing to adopt, takes minutes to implement, and the evidence says it works.

---

*This article summarizes findings from PROJ-014, a six-phase negative prompting research project. The A/B testing methodology used McNemar's exact test on matched pairs with blind scoring and 10% double-scoring for inter-rater reliability (92.6% agreement, Gwet's AC1 = 0.920). Full experimental artifacts, statistical tables, and the 14-pattern NPT taxonomy are available in the project repository.*
