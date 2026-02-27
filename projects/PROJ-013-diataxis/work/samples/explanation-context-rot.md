# About Jerry's Context Rot Problem

> This explanation covers the concept of context rot in LLM-based development tools and why Jerry's architecture uses the filesystem as infinite memory to solve it.

> **Scope:** This document explains the context rot phenomenon and Jerry's mitigation strategy. It does not cover Jerry's enforcement architecture (L1-L5 layers), specific quality gate thresholds, or individual agent implementations.

<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 (E-01 through E-07) -->
<!-- Anti-patterns to avoid: EAP-01 (instructional creep), EAP-05 (unbounded scope) -->
<!-- Voice: Thoughtful, discursive, contextual. No imperative instructions. See Section 5. -->

## Context

Every LLM-powered coding assistant operates within a context window -- a fixed-size buffer of tokens that represents everything the model "knows" during a session. As conversations progress, this window fills with prior messages, tool results, code snippets, and reasoning chains. The model's ability to follow instructions, maintain consistency, and produce high-quality output degrades as the window fills. This degradation is what Jerry calls "context rot."

The problem is not theoretical. In practice, a 200K-token context window sounds generous until you consider that a single large file read can consume 10,000 tokens, an agent definition might take 5,000, and the accumulated conversation history grows with every exchange. By the time a complex multi-phase task reaches its later stages, the model's performance on early-loaded rules and constraints has measurably declined.

## The Finite Memory Trap

Traditional approaches to LLM tool-building treat the context window as the primary workspace. Everything the model needs -- instructions, prior results, current state, quality criteria -- must fit in this single buffer. This creates what might be called the "finite memory trap": the more capable you make the system (more rules, more agents, more quality checks), the faster you fill the window, and the sooner performance degrades.

The trap is particularly insidious because degradation is not obvious. The model does not report "I can no longer reliably follow rule H-13." Instead, it silently begins omitting steps, loosening criteria, or producing subtly inconsistent output. The failure mode is not a crash but a gradual erosion of quality -- exactly the kind of failure that is hardest to detect and most expensive to correct.

This connects to a broader challenge in software systems: the tension between capability and resource constraints. Adding features to a traditional application increases its memory footprint; adding rules to an LLM system increases its context consumption. In both cases, the system eventually reaches a point where adding more degrades overall performance rather than improving it.

## Filesystem as Infinite Memory

Jerry's core architectural insight is to treat the filesystem as an extension of the model's memory. Rather than loading everything into the context window at session start and hoping it survives, Jerry persists state, rules, findings, and decisions to files and loads them selectively when needed.

This approach works because file storage is effectively unlimited while context windows are fixed. A Jerry project might contain hundreds of files totaling millions of tokens -- far more than any context window could hold. The model reads only what it needs for the current task, keeps its context window lean, and writes results back to files for future sessions to consume.

The filesystem-as-memory pattern also provides durability that in-memory context cannot. When a conversation ends or context is compressed, in-memory state vanishes. File-persisted state survives across sessions, across model versions, and across context window sizes. A decision recorded in an ADR file today remains accessible next month regardless of what happens to the conversation that produced it.

## Why Not Just Use a Larger Context Window?

Larger context windows help, but they do not eliminate the problem. Empirical observation shows that instruction-following reliability degrades with context fill regardless of absolute window size. A model with a 200K-token window at 80% fill shows similar degradation patterns to a model with a 100K-token window at 80% fill. The issue is proportional, not absolute.

There is also an economic dimension. Larger context windows cost more per request. A system that routinely fills a 200K-token window consumes significantly more compute than one that keeps usage lean through selective loading. Jerry's approach of loading only what is needed is not just more reliable -- it is also more cost-effective.

However, it would be misleading to suggest that filesystem-based persistence is without trade-offs. File I/O adds latency compared to in-context access. The model must decide what to read, which introduces a routing problem. And the filesystem itself can become cluttered if persistence is undisciplined -- trading context rot for "file rot." Jerry addresses these trade-offs through structured conventions (project directories, naming patterns, entity hierarchies) and selective loading protocols (progressive disclosure tiers).

## Connections

This topic connects to:
- **Progressive Disclosure:** Jerry's three-tier loading strategy (metadata, core, supplementary) is a direct application of the filesystem-as-memory principle. Tier 1 stays in context; Tier 2 loads on demand; Tier 3 loads selectively during execution. The tiers exist specifically because loading everything would trigger context rot.
- **Quality Enforcement Architecture:** The L2 enforcement layer (per-prompt re-injection of critical rules) exists because L1 rules loaded at session start are vulnerable to context rot. L2 markers are immune because they are re-injected fresh with every prompt, bypassing the degradation that affects L1 content as the context fills.

## Alternative Perspectives

<!-- EAP-01 guard: This section discusses alternatives discursively. Do NOT use imperative verbs to instruct the reader to try alternatives. -->

Not all LLM tool builders agree that context rot is a primary concern. Some argue that model improvements will eventually make context windows large enough and robust enough that selective loading becomes unnecessary overhead. The rapid expansion from 4K to 200K to 1M+ token windows supports this view -- each generation handles more context with less degradation.

Others advocate for retrieval-augmented generation (RAG) rather than filesystem persistence. In this approach, a vector database indexes all knowledge, and a retrieval step fetches relevant context for each request. RAG has the advantage of semantic search -- finding relevant content by meaning rather than file path -- but the disadvantage of introducing probabilistic retrieval into what should be deterministic rule enforcement. Jerry's approach favors deterministic file paths over probabilistic retrieval for critical governance content, while remaining compatible with RAG for supplementary knowledge.

A third perspective holds that the real solution is better prompt engineering rather than architectural mitigation. By crafting more concise, structured prompts, the argument goes, you can fit more capability into less context. Jerry embraces this view partially -- the L2 re-injection markers are precisely engineered for minimal token cost (~850 tokens total) -- but rejects it as a complete solution because prompt engineering cannot overcome the fundamental proportional degradation of context fill.

## Related

- **Tutorial:** [Learn to create a Jerry skill](tutorial-create-jerry-skill.md) -- Hands-on introduction to skill development
- **How-To Guide:** [How to register a skill](howto-register-skill.md) -- Practical registration steps
- **Reference:** [Diataxis Quality Criteria Reference](reference-diataxis-criteria.md) -- Technical specification of quality criteria
