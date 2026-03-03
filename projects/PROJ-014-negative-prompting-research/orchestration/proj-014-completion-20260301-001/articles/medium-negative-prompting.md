---
title: "The Three-Part Rule That Made Our LLM Stop Breaking Its Own Instructions"
subtitle: "How structured negation outperformed positive-only prompting in 270 blind tests across three Claude models"
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

That question sounds almost too simple to matter. Most prompt engineering advice points the same direction: be positive, be specific, tell the model what you want. "Always cite your sources." "Use formal tone." "Follow the coding standard." The conventional wisdom holds that negative instructions -- "don't do X" -- confuse language models or get ignored entirely.

We spent six weeks testing that assumption, and the answer was not what we expected.

## The Problem Nobody Talks About

If you have worked with LLMs in production -- not just casual conversation, but systems with behavioral rules, compliance requirements, and multi-step workflows -- you have seen this failure mode: the model follows your instructions beautifully for the first few turns, then quietly starts violating them.

The failure mode is *compliance degradation*. The model understood your rules. It followed them initially. Then, as the context window filled with conversation history, tool results, and accumulated reasoning, those carefully crafted instructions started losing their grip.

Most prompt engineering guidance responds with more positive instructions: be clearer, be more specific, add examples. But there is a category of behavior that positive framing handles poorly: prohibitions. "Always ask before deleting files" is not the same instruction as "NEVER delete files without user confirmation." The first is aspirational guidance. The second is a hard boundary.

We wanted to know: does the framing actually matter? And if so, how much?

## Seventy-Five Papers and a Gap in the Literature

The research ran six weeks across six phases: a literature survey of 75 academic and industry sources, followed by claim validation, taxonomy development, and framework analysis, with a controlled A/B test as the final phase.

The literature review turned up something striking: almost no one has studied this question rigorously. We found 13 peer-reviewed papers -- NeurIPS, AAAI, EMNLP, ICLR -- that touched on negation in LLM prompting, but most studied negation *comprehension* (can the model understand "not"?) rather than negation *compliance* (does the model follow a prohibition better than a positive instruction?).

One clear finding emerged from the literature: *blunt* negative prompting -- a bare "NEVER do X" with no context, no consequence, no alternative -- is demonstrably the worst way to express a constraint. Geng et al.'s "Control Illusion: The Failure of Instruction Hierarchies in Large Language Models" (AAAI 2026, [arXiv:2502.15851](https://arxiv.org/abs/2502.15851)) showed that standalone prohibitions fail within instruction hierarchies, and Ferraz et al.'s "LLM Self-Correction with DeCRIM" (EMNLP 2024 Findings, [arXiv:2410.06458](https://arxiv.org/abs/2410.06458)) found that structured constraint decomposition improves compliance by 7-8% over bare prohibitions. That much is established by peer-reviewed research.

The real question -- does *structured* negative framing outperform *structured* positive framing? -- was untested. So we built a taxonomy of 14 negative prompting patterns, cataloging everything from model-level interventions (RLHF, fine-tuning) down to prompt-level techniques, and then we tested the ones that matter most for practitioners.

## The Experiment

The A/B test ran 90 matched pairs (270 total test invocations across all framing conditions) against three Claude models: Haiku, Sonnet, and Opus. We pulled 10 real behavioral constraints from our production system and wrote three pressure scenarios for each -- situations designed to tempt the model into violating the constraint.

Each constraint ran under three framing conditions:

- **C1 (Positive-only):** "Always invoke skills proactively when trigger keywords match."
- **C2 (Blunt negation):** "NEVER wait for the user to invoke skills."
- **C3 (Structured negation):** "NEVER wait for the user to invoke skills -- Consequence: Work quality degradation. Rework required. Instead: Use proactively when triggers apply."

The C3 format is what we call NPT-013: a three-component structure combining an explicit prohibition, a documented consequence, and a constructive alternative. Every test was blind-scored by a separate model instance with no knowledge of which framing condition produced the output.

## Zero Violations Across Ninety Tests

Structured negation (C3) achieved **100% compliance** across all models, all constraints, and all scenarios. Zero violations out of 90 matched pairs.

Positive-only framing (C1) showed a **7.8% violation rate** -- 7 failures out of 90 matched pairs (95% CI: 2.3% to 13.3%).

McNemar's exact test on matched pairs: **p = 0.016**. McNemar's test is designed for matched-pair designs, where each pair controls for constraint-specific difficulty -- an independent-group test like chi-square would misattribute within-pair variation to the framing condition. The result is statistically significant at the pre-specified alpha of 0.05, and it passes Bonferroni correction marginally (p = 0.016 vs. adjusted alpha = 0.0167).

The effect was unidirectional and consistent. C3 never underperformed C1 on any single constraint, model, or scenario. Not once.

Blunt negation (C2) fell in between: 2.2% violation rate, better than positive-only but clearly worse than structured negation. This confirms the literature finding -- bare "NEVER" statements are better than nothing but far from optimal.

### Where the Violations Happened

Of the 9 total violations across all conditions -- 7 in C1, 2 in C2 -- two-thirds (6 of 9, 67%) landed on a single constraint type: behavioral timing rules. Instructions about *when* to act, not *what* to do. The constraint "invoke skills proactively when trigger keywords match" was the most vulnerable. Under positive-only framing, it failed in 5 out of 9 instances (56% violation rate). Under structured negation, it achieved perfect compliance.

That pattern makes sense. "Always invoke skills proactively" reads like a suggestion. "NEVER wait for the user to invoke skills -- Consequence: Work quality degradation" reads like a rule. The framing transforms aspirational guidance into an enforced boundary.

### Model Capability Matters

Lower-capability models benefited more from structured framing. Haiku showed the largest improvement: a 10 percentage-point reduction in violations when moving from positive-only to structured negation. Sonnet and Opus each showed 6.7 percentage-point improvements. Haiku was also the only model that violated constraints under the blunt negation condition (C2) -- suggesting that less capable models need the full three-component structure to achieve reliable compliance.

Practical implication: if you are routing requests to a smaller, faster model for cost efficiency, investing in structured constraint framing gives you a disproportionate return.

## Why Three Components Work

NPT-013 has three parts. Each one does specific work.

**1. The explicit prohibition ("NEVER X")** makes the boundary unambiguous. Positive framing leaves room for interpretation. "Always cite sources" could mean "when convenient" or "when you remember." "NEVER present claims without citations" draws a bright line.

**2. The consequence ("Consequence: Y")** creates stakes. One plausible explanation for the effect we observed: LLMs process instructions as weighted priorities, and a prohibition with documented downstream impact -- "downstream agents build analysis on nonexistent evidence, invalidating all derived findings" -- signals that this constraint is load-bearing, not decorative. We have not isolated this mechanism experimentally, but the pattern is consistent across our data. Isolating which of the three components contributes most to the effect is a question for future work.

**3. The alternative ("Instead: Z")** prevents the model from getting stuck. A bare prohibition tells the model what not to do but leaves it without a path forward. "Instead: explicitly state when no source is available and mark confidence as low" gives the model a compliant action to take. This is the component that separates NPT-013 from blunt negation, and the data shows it matters.

## What You Can Do Today

Five things you can apply to your own LLM systems right now:

**1. Audit your constraints for blunt prohibitions.** Search your system prompts for bare "don't," "never," or "must not" statements that lack consequence documentation or alternatives. These are your lowest-hanging fruit. Every one of them is underperforming.

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

**3. Prioritize behavioral-timing constraints first.** Our data shows that instructions about *when* to act are the most vulnerable to compliance failure under positive-only framing. Rules about proactive behavior, timing, or sequencing -- convert those first.

**4. Pay extra attention to smaller models.** If you are routing some requests to faster, cheaper models, those models need structured framing the most. The compliance gap between positive-only and structured negation is largest for less capable models.

**5. Keep consequence documentation specific.** "Quality degrades" is not a consequence. "Scoring rubric produces inflated scores, masking genuine defects that propagate to production" is a consequence. Specificity is what gives the consequence component its weight.

## The Caveats

**The effect size is modest.** The 7.8 percentage-point improvement is statistically significant but not enormous. Our pre-specified minimum effect size threshold was 10%, and the observed effect fell just below it. Our sample of 90 matched pairs was sized to detect a 10-percentage-point difference with 80% power, and we proceeded under a pre-registered contingency pathway that treats the format choice as convention-aligned rather than effectiveness-mandated. The 95% confidence interval (2.3% to 13.3%) does overlap with 10%, so the true effect may be larger than what we observed, though it may also be as small as 2.3 percentage points.

**This was single-session testing only.** We did not test compliance degradation over extended multi-turn conversations, which is where the real pain lives. Our highest-pressure scenarios showed the most violations, suggesting the effect would be larger under sustained context pressure -- but that remains untested.

**We tested 10 constraints across 3 models.** The constraints were selected for testability and drawn from a real production system, but they do not cover every constraint type. Constraints with different characteristics may show different framing sensitivity.

**We do not know why it works at a mechanistic level.** The experiment does not isolate which of the three components -- prohibition, consequence, alternative -- contributes most. That is a question for future work.

## Structure Beats Polarity

The thing we did not expect going in was that polarity -- positive vs. negative -- would turn out to be the wrong axis entirely. The real variable is structure. Of the three formulations we tested, bare prohibitions performed worst, positive-only was better but still vulnerable, and the three-component format eliminated violations entirely. Whether you phrase a constraint as "always do X" or "never do Y" matters less than whether you give the model a consequence and a path forward.

That changes how we think about prompt engineering for behavioral compliance. The field's emphasis on positive framing is not wrong, but it is incomplete. The constraints that break in production are not breaking because of polarity. They are breaking because they lack stakes and alternatives.

The three-component structure costs nothing to adopt and takes minutes to implement. The harder part is the shift in thinking: treating your system prompt not as a list of aspirations but as a set of load-bearing rules, each one documented with why it matters and what to do instead.

---

*This article summarizes findings from PROJ-014, a six-phase negative prompting research project. The A/B testing methodology used McNemar's exact test on matched pairs with blind scoring and 10% double-scoring for inter-rater reliability (92.6% agreement, Gwet's AC1 = 0.920). Primary academic sources: Geng et al., "Control Illusion: The Failure of Instruction Hierarchies in Large Language Models," AAAI 2026 ([arXiv:2502.15851](https://arxiv.org/abs/2502.15851)); Ferraz et al., "LLM Self-Correction with DeCRIM," EMNLP 2024 Findings ([arXiv:2410.06458](https://arxiv.org/abs/2410.06458)); Barreto & Jana, "This is not a Disimprovement: Improving Negation Reasoning in Large Language Models via Prompt Engineering," EMNLP 2025 Findings ([ACL Anthology](https://aclanthology.org/2025.findings-emnlp.761)). Full experimental artifacts, statistical tables, and the 14-pattern NPT taxonomy are available in the [project repository](https://github.com/geekatron/jerry/tree/main/projects/PROJ-014-negative-prompting-research).*
