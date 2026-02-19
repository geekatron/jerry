# Jerry Prompt Engineering — Executive Summary

> **Document ID:** PROJ-006-RPT-002
> **Agent:** ps-reporter (problem-solving skill)
> **Version:** 1.0.0
> **Date:** 2026-02-18
> **Status:** COMPLETE
> **Audience:** Stakeholders, team leads, and new Jerry users seeking orientation
> **Input:** PROJ-006-SYN-001, PROJ-006-ARCH-001, PROJ-006-ANA-001

---

## What Was Researched and Why

Jerry is a framework that gives Claude a persistent, structured memory system — projects, work items, and specialized agents that survive across sessions. Getting value from Jerry depends heavily on how prompts are written. A vague prompt bypasses the entire framework and produces a plain conversational response. A well-structured prompt activates a multi-agent pipeline with quality gates, adversarial critics, and traceable, filesystem-persisted artifacts.

This research was commissioned to answer: **what makes a Jerry prompt effective, and how can users reliably write better prompts?** Four research and analysis artifacts were produced across three phases, examining both external prompt engineering literature (Anthropic, DAIR.AI, academic CoT and ReAct research) and Jerry's internal architecture in detail.

---

## Key Findings

**1. Five structural elements separate effective prompts from ineffective ones.**
The highest-performing Jerry prompts share a consistent anatomy: explicit skill invocation using `/skill-name` syntax, a named domain and time scope, a named data source, a numeric quality threshold, and a specified output path with format. Each element maps to a specific Jerry mechanism. Missing any element forces Claude to make a structural decision the user should have made — defaulting file paths, lowering quality thresholds, or inferring scope.

**2. The Adversarial Critique Loop (ps-critic) is the single highest-impact quality mechanism — and the most underused.**
When explicitly requested in a prompt, ps-critic applies four adversarial critique modes (Devil's Advocate, Steelman, Red Team, Blue Team) at each phase boundary, with a circuit breaker that blocks progress until the quality threshold is met. Analysis confirmed this pattern has the largest quality uplift of any single prompt element. It is also the pattern most often absent from prompts that would benefit from it. Without an explicit request, no critique loop fires at all — not even at the default threshold of 0.85.

**3. A quality rubric with seven criteria and four tiers can score any Jerry prompt in under five minutes.**
The rubric weights Task Specificity (20%), Skill Routing (18%), Context Provision (15%), Quality Specification (15%), Decomposition (12%), Output Specification (12%), and Positive Framing (8%). A real prompt — the Salesforce privilege control example used throughout the research — scored Tier 3 (Proficient, 76.3/100). Its strengths were exemplary skill routing and quality specification. Its gaps were one incomplete trailing clause and absent output paths. These are one-sentence fixes.

**4. Jerry's architecture already implements most external best practices at the system level.**
Role definition (XML identity in every agent spec), structured output (Triple-Lens L0/L1/L2 format), ReAct-style reasoning loops, and model-tier routing are built into every agent. Users do not need to ask for these. What users must provide — because no system component can supply it — are specificity, numeric quality thresholds, explicit output paths, and the adversarial critique request.

**5. Eight anti-patterns reliably degrade prompt quality.**
The most impactful: vague directives without skill routing (bypasses all architecture), missing quality thresholds (ps-critic uses a generic default), and monolithic prompts without decomposition (prevents multi-agent orchestration). The least obvious: cognitive mode mismatch — using "research" language when root-cause investigation is needed routes to the wrong agent (ps-researcher instead of ps-investigator), producing a broad survey instead of a specific root cause.

---

## Top Recommendation

**For any prompt where being wrong has consequences — architecture decisions, security analysis, research synthesis that informs real decisions — always include this two-line addition:**

```
Include ps-critic adversarial critique after each phase.
Quality threshold: >= 0.90.
```

This activates the Adversarial Critique Loop and overrides the ps-critic default threshold. Without it, no critique fires. With it, every phase output is challenged by four adversarial modes and must meet the stated threshold before the pipeline proceeds. The research found this is the single highest-ROI change a user can make to an existing prompt.

---

## ROI and Value of Following This Guidance

The concrete, measurable benefits of applying this guidance are:

- **Fewer clarification rounds.** Tier 4 prompts (score 90+) complete without clarification requests. Tier 1 prompts require multiple back-and-forth turns. The rubric and templates provide a direct path from Tier 1 to Tier 3 or 4 in a single revision pass.
- **Artifacts at predictable locations.** Specifying output paths means research, analysis, and decision artifacts land where expected — retrievable across sessions without searching.
- **Quality gates that match the task stakes.** Specifying a numeric threshold (0.92 for architecture, 0.85 for research) means ps-critic enforces the right bar, not a generic default.
- **Reproducible workflows.** Orchestrated pipelines with explicit phase names, sync barriers, and output paths can be resumed across sessions. Unstructured prompts produce ephemeral results that cannot be reliably reproduced.

---

## Scope Limitations

This research is grounded in detailed analysis of Jerry's **problem-solving and orchestration skills**. The worktracker, nasa-se, transcript, and architecture skills were not examined in Phase 1. Patterns described here are confirmed for problem-solving and orchestration; they are likely but not confirmed for the other skills. Additionally, only one user prompt (the Salesforce privilege control example) was analyzed as a confirmed effective example — frequency statistics are directional, not statistically significant.

---

*Document Version: 1.0.0*
*Agent: ps-reporter*
*Word count: approximately 780 words (stakeholder sections; annotations excluded)*
*Constitutional Compliance: P-001, P-002, P-003, P-022*
*Created: 2026-02-18*
