# Research: LLM Instruction-Following Capacity and HARD Rule Enforcement Limits

**PS ID:** ps-researcher-004
**Date:** 2026-02-21
**Agent:** ps-researcher
**Topic:** LLM instruction-following capacity, hard constraint limits, system prompt effectiveness

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Key takeaways for non-technical stakeholders |
| [L1: Instruction Count and Degradation](#l1-instruction-count-and-degradation) | Empirical data on constraint count vs. compliance |
| [L2: Claude-Specific Findings](#l2-claude-specific-findings) | Anthropic documentation and Claude-specific data |
| [L3: System Prompt Length and Effectiveness](#l3-system-prompt-length-and-effectiveness) | Research on prompt length vs. adherence |
| [L4: Attention Dilution Analogies](#l4-attention-dilution-analogies) | Mechanistic analogies to cognitive load |
| [L5: Token Budget Guidance](#l5-token-budget-guidance) | Context window allocation heuristics |
| [L6: Instruction Hierarchy and Priority Conflicts](#l6-instruction-hierarchy-and-priority-conflicts) | What happens when rules conflict |
| [Confidence Calibration](#confidence-calibration) | Well-established vs. speculative findings |
| [Sources](#sources) | All citations |

---

## L0: Executive Summary

Current research establishes a clear picture: LLMs degrade significantly as the number of simultaneous constraints increases, instruction priority hierarchies are unreliable under conflict, and system prompts beyond approximately 500 words show diminishing returns. No study specifies a single magic number for "maximum trackable HARD rules," but the empirical trajectory is consistent -- the more constraints, the lower the compliance rate per constraint, non-linearly.

**Key numbers to remember:**
- At 1 instruction: 80-97% accuracy (MANYIFEVAL, 2025)
- At 5 instructions: drops to 32-72%
- At 10 instructions: falls to 2-39%
- Best model on AGENTIF (avg 11.9 constraints/instruction): fewer than 30% perfect instruction-level compliance
- When system prompt and user prompt conflict: adherence to system prompt drops from ~74-91% (non-conflicting) to 9.6-45.8% (conflicting) across major models
- Claude 3.5 specifically: 29.9% average adherence to priority hierarchy under conflict conditions

---

## L1: Instruction Count and Degradation

### ManyIFEval (2025) -- Quantified Degradation Curve

The most directly relevant study is "When Instructions Multiply: Measuring and Estimating LLM Capabilities of Multiple Instructions Following" (arXiv:2509.21051), which constructed ManyIFEval specifically to isolate the effect of instruction count on compliance.

**Findings:**

| Instruction Count | Accuracy Range (Across Models) |
|-------------------|-------------------------------|
| 1 | 80 - 97% |
| 5 | 32 - 72% |
| 10 | 2 - 39% |

On the StyleMBPP benchmark (code generation with style constraints):

| Instruction Count | Prompt-Level Accuracy Range |
|-------------------|-----------------------------|
| 1 | 65 - 97% |
| 6 | 0.01 - 68% |

The study's key methodological contribution: it controls for task description variation, confirming the degradation is attributable to instruction count, not task complexity. The relationship is continuous degradation rather than a cliff-edge threshold.

**Practical implication:** Even at 5 simultaneous hard constraints, the worst-performing models drop to 32% accuracy. At 10, some models are effectively non-functional at constraint adherence (2%).

### AGENTIF (NeurIPS 2025 Spotlight) -- Real-World Agentic Scenarios

"AGENTIF: Benchmarking Instruction Following of Large Language Models in Agentic Scenarios" (arXiv:2505.16944, Tsinghua KEG Lab).

- 707 instructions across 50 real-world agentic applications
- Average constraints per instruction: **11.9**
- Best model tested (o1-mini): **constraint success rate of 59.8%**
- Best model for perfect instruction-level compliance: **fewer than 30%**

This is the closest analogue to the Jerry Framework's operating environment: long system prompts with multiple hard behavioral rules, tool specifications, and condition constraints. The 30% perfect-compliance ceiling at ~12 constraints is the most direct data point for this research question.

### IFEval Benchmark (Google, 2023) -- Baseline Reference

"Instruction-Following Evaluation for Large Language Models" (arXiv:2311.07911) -- the foundational benchmark. Tests 25 verifiable instruction types across ~500 prompts. Established the baseline measurement methodology. Current frontier models score 80-90%+ on IFEval's single-constraint-per-prompt format, but IFEval is specifically designed to test one constraint type per prompt, making it an optimistic upper bound rather than a real-world estimate.

### The Instruction Gap (2025) -- Enterprise RAG Context

"The Instruction Gap: LLMs get lost in Following Instruction" (arXiv:2601.03269).

- Tested 13 models on 600 enterprise queries
- Best performer (GPT-5 Medium): 660 violations
- Claude 4-Sonnet: 731 violations (second-best among non-reasoning models)
- Worst: Gemini 2.0-Flash at 1,330 violations -- 2x the best model
- Root cause identified: "instructions often compete for attention with lengthy knowledge snippets, potentially causing models to lose focus on critical compliance requirements"

**Notable:** The study attributes failures to attention allocation challenges, not quantifiable instruction count limits. This is a qualitative mechanism, not a threshold.

---

## L2: Claude-Specific Findings

### Anthropic Long-Context Documentation

From `docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips`:

- Claude 3 models support 200K token contexts with stated quality maintenance across the full window.
- **Key positioning recommendation:** "Put longform data at the top" -- place long documents and inputs (~20K+ tokens) near the top, above query, instructions, and examples.
- **Quantified impact:** "Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs."
- **Grounding technique:** Ask Claude to quote relevant parts before answering -- this counteracts "noise" from surrounding content.

Anthropic does not publish a specific recommended maximum instruction count in their public documentation.

### Claude's System Prompt Evolution (PromptLayer Analysis, 2025)

Analysis of 15+ versions of Claude's production system prompts reveals patterns: instruction clarity increased over time, with explicit, crisp directives preferred over ambiguous guidelines. This suggests Anthropic's own internal practice trends toward specificity-per-instruction over instruction count.

### Claude 4.5 Context Awareness Feature

Claude 4.5 introduced explicit context window token budget tracking, enabling the model to monitor remaining context and adjust behavior as context fills. This is an architectural acknowledgment that token consumption of instructions has a measurable performance impact.

### Control Illusion Study -- Claude 3.5 Specific Data

"Control Illusion: The Failure of Instruction Hierarchies in Large Language Models" (arXiv:2502.15851):

| Model | Adherence to System Prompt Priority Under Conflict |
|-------|----------------------------------------------------|
| GPT-4o | 40.8% |
| **Claude 3.5** | **29.9%** |
| Llama-70B | 16.4% |
| Qwen-7B | 9.6% |

Individual constraint success (non-conflicting): 74.8 - 90.8%
Conflicting constraints: 9.6 - 45.8% primary obedience rate

**Critical finding:** "Larger models showed no consistent advantage" -- model size does not reliably improve instruction hierarchy enforcement. Social framing (authority, expertise, consensus signals) achieved *better* adherence (up to 65.8% for some models) than explicit system prompt designation.

### Anthropic Constitutional AI (Published January 2026)

Anthropic's publicly released Model Spec / Claude's Constitution distinguishes between:
- **Hardcoded behaviors** -- absolute prohibitions encoded at training time (e.g., CSAM, bioweapons)
- **Softcoded defaults** -- operator/user adjustable within boundaries

This distinction is architecturally meaningful: genuinely hardcoded constraints (from training, not system prompt) are more reliable than runtime system prompt rules. The Jerry Framework's HARD rules, being delivered via system prompt, are in the "softcoded" category from a technical enforcement perspective.

---

## L3: System Prompt Length and Effectiveness

### Empirical Data on Prompt Length

From PromptLayer / industry analysis (2024-2025):

- **~500 words:** Identified as a diminishing returns inflection point.
- **Beyond 500 words:** Each 100 additional words may reduce comprehension by approximately 12% (industry estimate, not peer-reviewed; treat as SPECULATIVE).
- **Optimal range for moderately complex tasks:** 150-300 words.

**Caveat:** These numbers appear in practitioner literature and have not been rigorously validated in peer-reviewed studies with controlled methodology. The directional claim (longer prompts = diminishing returns) is well-supported; the specific thresholds are not.

### Position Effects -- Lost in the Middle (Stanford/UW, 2023, Published TACL 2024)

"Lost in the Middle: How Language Models Use Long Contexts" (arXiv:2307.03172, Liu et al., Stanford/UW).

**Core finding:** Performance follows a U-shaped curve relative to document position:
- Information at beginning of context: high retrieval accuracy
- Information at end of context: high retrieval accuracy
- Information in the middle: significantly degraded retrieval

**Implication for instruction placement:** System rules placed in the middle of long contexts are at the highest risk of being "lost." Rules placed first (before working content) or last (after working content) are more reliably recalled.

**Note:** Subsequent work (TACL 2024 publication) affirmed the original finding applies even to models with extended context training. Partial mitigation in some newer models, but not eliminated.

### "Effects of Prompt Length on Domain-Specific Tasks" (arXiv, 2025)

"Effects of Prompt Length on Domain-specific Tasks for Large Language Models" (arXiv:2502.14255).

- Domain-specific performance varies with prompt length in task-dependent ways.
- No universal optimal length found; the relationship is task-specific.
- Long prompts that include irrelevant information consistently hurt performance ("models can identify irrelevant details but frequently struggle to ignore them").

---

## L4: Attention Dilution Analogies

### ADOR: Attention Dilution and Overlap Rejection (2024)

A paper on OpenReview titled "ADOR: Attention Dilution and Overlap Rejection" formalizes attention dilution as a recognized failure mode in transformer-based models. Originally characterized in image generation (semantic neglect when too many concepts compete for attention), the mechanism is architecturally general.

**Mechanism:** In transformer attention, each token competes for weight allocation. As context length and instruction count increase, attention weight per instruction decreases. The model's "budget" for attending to any single constraint is diluted by the presence of others. This is mechanistically analogous to working memory capacity limits in humans, though the underlying physics differ.

### Knowledge Dilution Phenomenon

Distinct from but related to attention dilution: "knowledge dilution" describes how an LLM's domain-specific expertise degrades when exposed to large volumes of contextually relevant but domain-irrelevant information. A 47% reduction in security feature implementation was documented in one study. This is a content-layer effect rather than a pure attention mechanism.

**Cognitive load analogy (SPECULATIVE):** The transformer attention mechanism's finite weight distribution across tokens provides a formal analog to human working memory's 7±2 item capacity (Miller, 1956). However, the mechanisms differ fundamentally: human working memory is capacity-limited by neurological constraints; transformer attention is diluted by mathematical normalization (softmax) across all tokens. The analogy is useful for intuition but should not be taken as equivalence.

### Cognitive Workspace Research (2025)

"Cognitive Workspace: Active Memory Management for LLMs" (arXiv:2508.13171) -- proposes explicit working memory management for LLMs as a response to the demonstrated degradation under context load. The fact that this research direction exists is itself evidence of the underlying limitation being recognized as an architectural problem, not merely a training artifact.

---

## L5: Token Budget Guidance

### General Heuristics (Industry, 2024-2025)

No peer-reviewed study establishes a universal token ratio for system prompts vs. working content. The following are industry heuristics:

**Common allocation pattern for production systems:**
- System prompt: 1-5% of total context
- Document/working content: 60-70%
- Conversation history: 15-25%
- Response reserve: 10-15%

**Example for 32K model (practitioner guidance):**
- System prompt: 500 tokens (1.5%)
- Document/code: 20,000 tokens (62.5%)
- Conversation: 7,500 tokens (23.5%)
- Response space: 4,000 tokens (12.5%)

**Scaling to 200K (extrapolated, SPECULATIVE):** Applying the same 1.5% ratio gives ~3,000 tokens for system prompt. However, some practitioners argue that system prompt overhead does not need to scale linearly with context size -- a 3,000-token system prompt that repeats on every API call creates significant cumulative cost.

### Anthropic's Own Practice

The Jerry Framework's `quality-enforcement.md` specifies: "Total enforcement budget: ~15,100 tokens (7.6% of 200K context)." This is above the typical practitioner 1-5% guideline and represents a deliberate design choice to invest more context in behavioral control at the cost of available working space.

**Industry guidance from multiple sources:** Trigger LLM-based summarization of conversation history when approaching 70-80% context capacity.

### Token Budget Feature (Claude 4.5+)

Claude 4.5 introduces explicit `token_budget` support -- Anthropic's acknowledgment that instruction-aware context management is a production concern.

---

## L6: Instruction Hierarchy and Priority Conflicts

### OpenAI Instruction Hierarchy Research (2024)

"The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions" (arXiv:2404.13208, OpenAI).

- Proposes explicit training to enforce system > user > tool output priority.
- Result: "drastically increases robustness -- even for attack types not seen during training -- while imposing minimal degradations on standard capabilities."
- Deployed in GPT-4o mini.
- **Limitation:** This is a training-time intervention. System-prompt-only instruction hierarchy enforcement (without special training) remains weak.

### Control Illusion -- Hierarchy Failure Without Special Training

"Control Illusion: The Failure of Instruction Hierarchies in Large Language Models" (arXiv:2502.15851, 2025).

- Tests models without specialized hierarchy training.
- **Primary finding:** "The widely-adopted system/user prompt separation fails to establish a reliable instruction hierarchy."
- Models exhibit "strong inherent biases toward certain constraint types regardless of their priority designation."
- **Societal framing beats explicit system priority:** Authority/expertise/consensus signals in the *text itself* achieved better adherence than placement in the system prompt.

**Implication for HARD rule enforcement:** Rules that are merely listed in a system prompt and labeled "HARD" or "MUST" gain compliance from the model's training on similar language, not from the system-prompt position itself. The enforcement is semantic, not structural.

### ICLR 2025 -- Safety with Instruction Hierarchies

"Improving LLM Safety with Instruction Hierarchy" (ICLR 2025 Proceedings).

- Identifies that hierarchical priority information is represented in only a few tokens.
- "This signal is likely to diminish when encountering long-context tasks."
- Confirms: the priority-signaling mechanism is fragile under context pressure.

---

## Confidence Calibration

| Finding | Confidence | Evidence Type |
|---------|-----------|---------------|
| Instruction compliance degrades as constraint count increases | WELL-ESTABLISHED | Multiple peer-reviewed benchmarks (ManyIFEval, AGENTIF, IFEval) |
| At 10 simultaneous constraints, some models reach 2% accuracy | WELL-ESTABLISHED | ManyIFEval (arXiv:2509.21051), controlled study |
| Best model at ~12 constraints achieves <30% perfect instruction compliance | WELL-ESTABLISHED | AGENTIF (arXiv:2505.16944, NeurIPS 2025 Spotlight) |
| System/user prompt priority separation is unreliable under conflict | WELL-ESTABLISHED | Control Illusion (arXiv:2502.15851) |
| Claude 3.5 achieves 29.9% priority adherence under conflict | WELL-ESTABLISHED | Control Illusion study, directly measured |
| "Lost in the middle" position degradation | WELL-ESTABLISHED | Liu et al. (arXiv:2307.03172), TACL 2024 |
| Queries at end of long prompt improve quality by up to 30% | WELL-ESTABLISHED (Anthropic documentation, not independently validated) | Anthropic long-context-tips docs |
| 500-word threshold for diminishing returns | SPECULATIVE | Practitioner literature, not peer-reviewed with controlled methodology |
| 12% comprehension reduction per 100 words beyond 500 | SPECULATIVE | Practitioner literature, no peer-reviewed source identified |
| Societal framing beats system-prompt priority designation | EMERGING (single study, 2025) | Control Illusion (arXiv:2502.15851) |
| Knowledge dilution (47% reduction) | EMERGING (single study domain) | Domain-specific, not generalized |
| Attention dilution as formal mechanism | EMERGING | ADOR paper (OpenReview); formally studied in image generation, extrapolated to text |
| HARD rules in system prompt = "softcoded" from Anthropic's perspective | WELL-ESTABLISHED | Anthropic Model Spec / Claude's Constitution (Jan 2026) |

---

## Sources

| Reference | URL | Notes |
|-----------|-----|-------|
| "Lost in the Middle: How Language Models Use Long Contexts" -- Liu et al. (Stanford/UW, TACL 2024) | https://arxiv.org/abs/2307.03172 | Foundational; U-shaped position degradation |
| "The Instruction Gap: LLMs get lost in Following Instruction" (arXiv:2601.03269) | https://arxiv.org/abs/2601.03269 | Enterprise RAG; violation counts per model |
| "When Instructions Multiply" (arXiv:2509.21051) | https://arxiv.org/html/2509.21051 | ManyIFEval; quantified degradation curve |
| "AGENTIF: Benchmarking Instruction Following in Agentic Scenarios" (NeurIPS 2025) | https://arxiv.org/abs/2505.16944 | 11.9 constraints avg; <30% perfect compliance ceiling |
| "Instruction-Following Evaluation for LLMs" -- IFEval (arXiv:2311.07911) | https://arxiv.org/abs/2311.07911 | Foundational IFEval benchmark |
| "Control Illusion: The Failure of Instruction Hierarchies" (arXiv:2502.15851) | https://arxiv.org/html/2502.15851 | Claude 3.5 at 29.9%; priority hierarchy failure |
| "The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions" -- OpenAI (arXiv:2404.13208) | https://arxiv.org/html/2404.13208v1 | Training-time solution to hierarchy enforcement |
| "Improving LLM Safety with Instruction Hierarchy" (ICLR 2025) | https://proceedings.iclr.cc/paper_files/paper/2025/file/ea13534ee239bb3977795b8cc855bacc-Paper-Conference.pdf | Priority signal dilution under long context |
| "Enhancing Multi-Constraint Complex Instruction Following" (EMNLP 2024 Findings) | https://aclanthology.org/2024.findings-emnlp.637.pdf | Multi-constraint complexity research |
| "Effects of Prompt Length on Domain-specific Tasks" (arXiv:2502.14255) | https://arxiv.org/html/2502.14255v1 | Domain-specific prompt length effects |
| Anthropic Long Context Prompting Tips | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips | +30% quality improvement with end-positioned queries |
| Anthropic Prompting Best Practices (Claude 4) | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices | Precise instruction following guidance |
| Claude's Constitution (Anthropic, January 2026) | https://www.anthropic.com/news/claudes-constitution | Hardcoded vs. softcoded distinction |
| "Cognitive Workspace: Active Memory Management for LLMs" (arXiv:2508.13171) | https://arxiv.org/html/2508.13171v1 | Active memory management; context overload problem |
| ADOR: Attention Dilution and Overlap Rejection | https://openreview.net/pdf/ac0134591cc9f5a4c68c319acb279d79d8504141.pdf | Attention dilution formal mechanism |
| "Large Language Model Instruction Following: A Survey" (MIT Press, Computational Linguistics) | https://direct.mit.edu/coli/article/50/3/1053/121669/ | Survey of progress and challenges |
| "Who is In Charge? Dissecting Role Conflicts in LLM Instruction Following" | https://openreview.net/forum?id=RBfRfCXzkA | Role conflict in multi-instruction scenarios |
| "A Closer Look at System Prompt Robustness" (arXiv:2502.12197) | https://arxiv.org/pdf/2502.12197 | System prompt robustness analysis |
| Context Rot (Understanding AI, 2025) | https://www.understandingai.org/p/context-rot-the-emerging-challenge | Context rot named and described |
| PromptLayer: Disadvantage of Long Prompts | https://blog.promptlayer.com/disadvantage-of-long-prompt-for-llm/ | Practitioner analysis; 500-word threshold (SPECULATIVE) |
