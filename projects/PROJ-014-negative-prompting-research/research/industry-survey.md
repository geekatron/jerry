# Industry & Practitioner Survey: Negative Prompting

> Phase 1 industry research for PROJ-014. 31 core sources cataloged (1 adjacent source documented separately).

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Key findings for stakeholders |
| [L1: Source Catalog](#l1-source-catalog) | All sources with metadata |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Deep analysis by theme |
| [Cross-References](#cross-references) | Links to companion research |
| [Methodology](#methodology) | Search strategy and source selection |

---

## L0: Executive Summary

- **Three of four major platform vendors recommend positive framing over negative framing for behavioral control; Palantir takes a balanced approach.** Anthropic, OpenAI, and Google all explicitly recommend telling models what to do rather than what not to do. OpenAI's GPT-4.1 prompting guide provides a concrete example where a "DO NOT ASK FOR INTERESTS" instruction was directly violated by the model. Anthropic's Claude 4 best practices guide says "Tell Claude what to do instead of what not to do" and provides reframing examples. Google's Gemini documentation advises using examples to show patterns to follow rather than anti-patterns to avoid. Palantir's guidance treats negatives as one standard tool among many without expressing categorical preference. This recommendation applies primarily to behavioral control instructions; negative constraints retain legitimate roles in safety boundaries (e.g., ethical guardrails), declarative behavioral descriptions (e.g., "Claude does not claim to be human"), and programmatic enforcement via frameworks like DSPy Assertions and NeMo Guardrails. **Model-generation caveat:** This recommendation reflects the balance of evidence across 2023-2026 sources. Sources 4 and 5 (OpenAI GPT-4.1 and GPT-5 guides) document that newer model generations follow instructions more literally, including negative instructions, and their unintended consequences are also more pronounced. GPT-4.1 and GPT-5 (both 2025) already demonstrate improved negative instruction compliance, indicating that the effectiveness gap between positive and negative framing is narrowing in currently deployed model generations. See Cross-References for the full model-generation confound discussion.

- **The "Pink Elephant Problem" provides the strongest practitioner-level explanation for why negative instructions fail, drawing on a cognitive psychology analogy.** Multiple independent sources identify an analogy to Ironic Process Theory from cognitive psychology: telling a model not to think about something forces it to attend to that concept, paradoxically increasing the probability of the forbidden output. This analogy is explanatory -- it is drawn from human cognitive science and has not been mechanistically demonstrated as a property of transformer attention weights. No source in this 31-source survey provides direct empirical evidence that negation operators elevate attention weights for negated tokens in transformer models. Nevertheless, the behavioral parallel is observed across multiple independent practitioner reports. Empirical testing by DreamHost found that reframing negatives as positives consistently improved Claude's output quality. The Inverse Scaling Prize demonstrated that larger models actually perform *worse* on negated instructions, showing this is not merely an undertrained-model issue.

- **Negative instructions are not universally harmful -- they serve specific, narrow roles.** Vendor system prompts themselves use negative constraints for safety boundaries (Anthropic's Claude system prompt uses descriptive negative statements like "Claude does not claim to be human"). The GPT-5 prompting guide shows that domain-specific, unambiguous negatives like "NEVER add copyright headers" work when they prevent concrete harms rather than attempt to control reasoning. Production guardrail systems (QED42, NeMo Guardrails) rely on few-shot examples of correct behavior far more than explicit prohibitions.

- **Prompt bloat from accumulated negative instructions degrades performance.** Research shows LLM reasoning degrades around 3,000 tokens well below context window limits. The instruction following rate decreases as instruction count increases due to contradictions and tension between rules. Frontier LLMs can follow approximately 150-200 instructions with reasonable consistency (Source 16 estimate; methodology not disclosed), and instruction-following quality decreases uniformly as count increases. Instruction compliance drops from approximately 95% at messages 1-2 to 20-60% by messages 6-10 (Source 17 practitioner observation; decay rates not independently verified). The HumanLayer analysis of Claude Code found that CLAUDE.md files with too many rules cause Claude to ignore half of them.

- **The evidence landscape is predominantly vendor recommendations and practitioner anecdotes; rigorous empirical comparisons are scarce.** No source in this survey provides a controlled A/B test directly comparing negative vs. positive instruction variants at scale in production. The strongest quantitative finding comes from the Bsharat et al. (2023) academic study (summarized by PromptHub, Source 13) reporting 55% improvement and 66.7% correctness increase for affirmative directives with GPT-4, but PromptHub cites this upstream academic paper rather than presenting independent testing.

### Evidence Landscape Assessment

The industry evidence skews heavily toward practitioner anecdotes (48%, 15 of 31 core sources) and vendor recommendations (29%, 9 of 31 core sources). Empirical evidence -- structured testing with measurable outcomes, including controlled experiments, competition results, practitioner systematic testing, cited academic findings, and sentiment studies (see Tier Definitions for sub-category descriptions and epistemic weighting) -- constitutes 23% (7 of 31 core sources). However, within this 23%, only 3 sources (sub-categories a-b: controlled experiments and competition results) report original structured testing; the remaining 4 carry substantial methodological limitations (see sub-tier note in Evidence Tier Distribution). No source qualifies as a peer-reviewed controlled experiment (academic papers are covered in the companion Session 1A survey). This indicates a field where conventional wisdom is strong but experimental validation is thin.

### Gaps Identified

1. No large-scale production A/B tests comparing negative vs. positive instruction variants
2. No model-specific compliance rate data for negative instructions (e.g., "Claude follows NEVER instructions X% of the time")
3. Limited framework-level documentation on negative prompting patterns (DSPy Assertions is the strongest example; LangChain and LlamaIndex have minimal coverage)
4. No systematic taxonomy of negative instruction types and their relative effectiveness
5. Missing: vendor-published internal testing data on instruction compliance rates
6. No controlled comparison of negative instruction compliance in zero-shot vs. few-shot contexts
7. No model-version-specific compliance rate tracking across generations (e.g., GPT-3.5 vs. GPT-4 vs. GPT-4.1 vs. GPT-5 negation handling)
8. No comparison of negative instruction effectiveness in system prompt vs. user turn placement

---

## L1: Source Catalog

### Evidence Tier Definitions

Sources are classified into three evidence tiers based on the nature of the evidence provided. These tiers reflect the strength of the evidentiary basis, not the credibility of the author or organization.

| Tier | Definition | Scope | Limitations |
|------|-----------|-------|-------------|
| **Vendor Recommendation** | Guidance published by an LLM platform vendor (Anthropic, OpenAI, Google, Palantir, NVIDIA) based on their internal model development and testing experience. | Reflects the vendor's own model behavior; informed by proprietary internal testing. | Testing methodology and data are not published. Recommendations may reflect model-specific behavior that does not generalize across vendors. Vendor incentives may favor guidance that positions their models favorably. |
| **Empirical Evidence** | Sources presenting structured testing with measurable outcomes. This tier encompasses five sub-categories ordered by epistemic weight (strongest first): (a) *Controlled experiments* -- formal experimental design with defined methodology and reproducible conditions (e.g., DSPy Assertions benchmarks); (b) *Competition results* -- structured evaluation conducted by competition organizers on participant-submitted tasks, with defined scoring criteria but without peer review of individual submissions (e.g., Inverse Scaling Prize); (c) *Practitioner systematic testing* -- structured testing by practitioners with before/after comparisons and reported results, but without formal experimental controls or peer review (e.g., DreamHost's 25-technique testing, QED42 guardrail evaluations); (d) *Cited academic* -- sources that report quantitative findings from upstream academic papers without conducting independent testing; the original academic results carry the epistemic weight, not the citing source (e.g., PromptHub citing Bsharat et al., 2023); (e) *Sentiment study* -- sources measuring the effect of emotional tone/sentiment in prompts rather than instruction syntax; included because emotional negativity and instructional negativity may share overlapping degradation mechanisms, but the findings do not directly address prohibitive instruction compliance (e.g., The Big Data Guy's prompt variation study). | Provides quantitative or semi-quantitative evidence. Sub-categories are ordered by epistemic weight: (a) > (b) > (c) > (d) > (e). Sub-category (a) provides the strongest evidence; (d) and (e) provide the weakest within this tier because (d) reports others' findings and (e) measures a related but distinct phenomenon. | Sub-categories (b)-(e) carry progressively greater limitations. (b) lacks peer review of individual tasks. (c) may lack disclosed methodology, control conditions, or statistical rigor. (d) does not constitute independent evidence -- the epistemic weight belongs to the cited academic paper, not the citing source. (e) measures emotional sentiment, not instruction syntax; extrapolation to instructional negation is speculative. Results from sub-categories (c)-(e) may not be independently reproducible. |
| **Practitioner Anecdote** | Experience reports, best-practice recommendations, and observational findings from practitioners, bloggers, and community contributors. | Captures real-world usage patterns and practitioner consensus. Valuable for identifying common failure modes and practical workarounds. | No formal methodology. Subject to confirmation bias, survivorship bias, and selection effects. Specific claims may be unverifiable. |

### Source Table

| # | Title | Org/Author | Year | Type | Evidence Tier | Key Finding | URL |
|---|-------|------------|------|------|---------------|-------------|-----|
| 1 | Prompting best practices (Claude 4) | Anthropic | 2025 | Vendor documentation | Vendor Recommendation | "Tell Claude what to do instead of what not to do." Provides specific reframing example: "Do not use markdown" becomes "compose smoothly flowing prose paragraphs." Also: aggressive language (CRITICAL!, YOU MUST, NEVER EVER) "actively hurts newer Claude models." | [Link](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) |
| 2 | Prompt Engineering Guide (Tips) | DAIR-AI / PromptingGuide.ai | 2024 | Community guide | Practitioner Anecdote | "Avoid saying what not to do but say what to do instead." Provides movie chatbot example where "DO NOT ASK FOR INTERESTS" instruction was violated by the model. | [Link](https://www.promptingguide.ai/introduction/tips) |
| 3 | Prompt Engineering (OpenAI API docs) | OpenAI | 2024 | Vendor documentation | Vendor Recommendation | "Instead of just saying what not to do, say what to do instead." Provides customer service example reframing "DO NOT ASK USERNAME OR PASSWORD" as positive instruction. | [Link](https://platform.openai.com/docs/guides/prompt-engineering) |
| 4 | GPT-4.1 Prompting Guide | OpenAI | 2025 | Vendor documentation | Vendor Recommendation | GPT-4.1 follows instructions "more closely and more literally" than predecessors. Demonstrates constraint sections with prohibited topics list and deflection phrases. Warns against "always follow" instructions causing hallucination. | [Link](https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide) |
| 5 | GPT-5 Prompting Guide | OpenAI | 2025 | Vendor documentation | Vendor Recommendation | "Do NOT guess or make up an answer" and "NEVER add copyright headers" work because they are unambiguous and prevent concrete harms. Contradictory instructions waste reasoning tokens. Positive framing of constraints preferred over accumulated prohibitions. | [Link](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide) |
| 6 | Prompt Design Strategies (Gemini API) | Google | 2024 | Vendor documentation | Vendor Recommendation | Use examples to show patterns to follow, not anti-patterns to avoid. Negative constraints may be dropped on complex requests; place critical restrictions at end of instruction. | [Link](https://ai.google.dev/gemini-api/docs/prompting-strategies) |
| 7 | Gemini 3 Prompting Guide | Google Cloud | 2025 | Vendor documentation | Vendor Recommendation | Place negative constraints at end of instructions to reduce risk of being dropped. Recommends "semantic negative prompts" for image generation -- describe desired scene positively rather than listing exclusions. | [Link](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide) |
| 8 | The Pink Elephant Problem: Why "Don't Do That" Fails with LLMs | 16x Engineer / Eval | 2025 | Blog post / article | Practitioner Anecdote | Connects LLM behavior to Ironic Process Theory. Cites Claude Code creating duplicate files despite NEVER rules. Reports user success reframing "do not make new versions" to "Make all possible updates in current files." Identifies three valid uses for negatives: safety, firm boundaries, paired with positives. | [Link](https://eval.16x.engineer/blog/the-pink-elephant-negative-instructions-llms-effectiveness-analysis) |
| 9 | LLMs and the "not" problem | Sean Trott (Substack) | 2024 | Blog post / article | Practitioner Anecdote | Cites Ettinger (2020) BERT study: model assigned high probability to "bird" for "A robin is not a ___" -- ignoring negation. Proposes that neither LLMs nor humans process negation uniformly. Recommends positive framing workaround: specify desired content rather than using negation. | [Link](https://seantrott.substack.com/p/llms-and-the-not-problem) |
| 10 | Using Negative AI Prompts Effectively | Virtualization Review / Brien Posey | 2025 | Blog post / article | Practitioner Anecdote | Introduces hard negatives (non-negotiable: "do not," "without," "avoid") vs. soft negatives (preferences: "try to avoid," "minimize"). Recommends keeping constraint lists "concise, but very targeted." Warns too many restrictions confuse models or severely limit output quality. | [Link](https://virtualizationreview.com/articles/2025/12/08/using-negative-ai-prompts-effectively.aspx) |
| 11 | Prompt Engineering Best Practices 2026 | Thomas Wiegold | 2026 | Blog post / article | Practitioner Anecdote | "Positive framing over negation -- 'only use real data' consistently outperforms 'don't use mock data.'" Labels this the Pink Elephant Problem. Notes LLM reasoning degrades around 3,000 tokens, practical sweet spot 150-300 words. | [Link](https://thomas-wiegold.com/blog/prompt-engineering-best-practices-2026/) |
| 12 | Claude Prompt Engineering: We Tested 25 Popular Practices (These 5 Worked) | DreamHost | 2025 | Blog post / article | Empirical Evidence (Practitioner) | Systematically tested 25 prompt techniques. Found avoiding negative phrasing "significantly improves results." Provides before/after: "Don't use complex jargon" reframed as "Use simple, everyday language." Reports Pink Elephant effect: instructing to avoid something "paradoxically draws attention to" it. **Limitation:** Testing methodology (sample size, evaluation criteria, model version, number of trials) not disclosed. Results are directional but not independently reproducible from the published account. | [Link](https://www.dreamhost.com/blog/claude-prompt-engineering/) |
| 13 | Prompt Engineering Principles for 2024 (26 Principles) | PromptHub / Dan Cleary | 2024 | Blog post / article | Empirical Evidence (Cited) | Reports Principle 4 ("employ affirmative directives") showed 55% improvement and 66.7% correctness increase for GPT-4. **Limitation:** These quantitative results cite the Bsharat et al. (2023) academic paper, not PromptHub's own independent testing. PromptHub is reporting upstream academic findings, not original empirical work. Notes OpenAI removed this principle from their latest guidance -- an interesting omission. Acknowledges negative language "can be helpful in avoiding certain things." | [Link](https://www.prompthub.us/blog/prompt-engineering-principles-for-2024) |
| 14 | The Impact of Prompt Bloat on LLM Output Quality | MLOps Community | 2025 | Blog post / article | Empirical Evidence | LLM reasoning performance degrades around 3,000 tokens. LLMs exhibit "identification without exclusion" -- they can recognize irrelevant info but still incorporate it. Semantically similar but irrelevant information more damaging than unrelated content. Chain-of-Thought prompting does not mitigate long-prompt degradation. | [Link](https://home.mlops.community/public/blogs/the-impact-of-prompt-bloat-on-llm-output-quality) |
| 15 | Effective Context Engineering for AI Agents | Anthropic Engineering | 2025 | Vendor documentation | Vendor Recommendation | Cautions against "hardcoding complex, brittle logic in their prompts." Recommends "strong heuristics to guide behavior" over exhaustive constraint lists. Advises using "diverse, canonical examples" instead of "a laundry list of edge cases." Treats context as "precious, finite resource." | [Link](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) |
| 16 | Writing a Good CLAUDE.md | HumanLayer | 2025 | Blog post / article | Practitioner Anecdote | Frontier LLMs follow ~150-200 instructions with reasonable consistency (estimate; methodology for determining this range not disclosed). Instruction-following quality decreases uniformly as count increases. Claude Code system prompt already uses ~50 instructions, limiting CLAUDE.md budget. Recommends: "Never send an LLM to do a linter's job" -- use deterministic tooling for style enforcement. | [Link](https://www.humanlayer.dev/blog/writing-a-good-claude-md) |
| 17 | An Easy Way to Stop Claude Code from Forgetting the Rules | DEV Community / Siddhant K | 2025 | Blog post / article | Practitioner Anecdote | Documents instruction decay pattern: ~95% compliance at messages 1-2, dropping to 20-60% by messages 6-10 (practitioner observation; specific decay rates not independently verified and methodology not disclosed). Instructions at beginning of context "gradually lose importance as conversation grows longer." Proposes self-referential rules as mitigation. Notes this exploits fundamental transformer attention mechanisms. | [Link](https://dev.to/siddhantkcode/an-easy-way-to-stop-claude-code-from-forgetting-the-rules-h36) |
| 18 | Inverse Scaling Prize: Round 1 Winners | LessWrong / Inverse Scaling Project | 2023 | Community discussion / forum | Empirical Evidence (Competition) | Demonstrated that larger LMs perform *worse than random* on negated instructions -- a true inverse scaling effect. Smaller models answer randomly; larger models know facts but miss negation, answering incorrectly. Found potential U-shaped scaling: performance may recover at very large scales. **Limitation:** This is a competition prize announcement, not a peer-reviewed controlled experiment. The underlying tasks were submitted by competition participants; evaluation was conducted by the prize organizers. The academic paper (arXiv 2306.09479) is covered in Session 1A. | [Link](https://www.lesswrong.com/posts/iznohbCPFkeB9kAJL/inverse-scaling-prize-round-1-winners) |
| 19 | Best Practices for LLM Prompt Engineering | Palantir | 2024 | Vendor documentation | Vendor Recommendation | Recommends clear constraints to guide scope (e.g., "Summarize in no more than three sentences"). Supports negative examples for limiting unwanted outputs: "Generate pros and cons of remote work, but exclude personal opinions." Emphasizes iterative refinement. | [Link](https://www.palantir.com/docs/foundry/aip/best-practices-prompt-engineering) |
| 20 | Building Simple & Effective Prompt-Based Guardrails | QED42 | 2025 | Blog post / article | Empirical Evidence | Critical finding: "the power of examples far exceeds the power of instructions." Initial elaborate instructions with few examples produced inconsistent results. Solution: two-tier approach with GPT-4o generating examples, smaller models deploying them. Diverse examples covering edge cases outperformed detailed rule sets. | [Link](https://www.qed42.com/insights/building-simple-effective-prompt-based-guardrails) |
| 21 | DSPy Assertions: Computational Constraints for Self-Refining Language Model Pipelines | Stanford NLP / Arize AI | 2024 | Framework documentation | Empirical Evidence | LM Assertions improve constraint compliance up to 164% more often and generate up to 37% more higher-quality responses. Counter-example bootstrapping: collects traces of failed assertions and uses them as demonstrations of what NOT to do -- a programmatic approach to negative prompting. Suggest/Assert constructs enable backtracking with error messages. | [Link](https://dspy.ai/learn/programming/7-assertions/) |
| 22 | Common LLM Prompt Engineering Challenges and Solutions | Latitude | 2025 | Blog post / article | Practitioner Anecdote | Warns that negative instructions introduce "shadow information" that may confuse models. Recommends describing what you want rather than listing what to avoid. Claims tools cut iteration time by 30% and improve output consistency by 25%. | [Link](https://latitude.so/blog/common-llm-prompt-engineering-challenges-and-solutions) |
| 23 | The Ultimate Guide to Prompt Engineering in 2026 | Lakera AI | 2026 | Blog post / article | Practitioner Anecdote | Notes "you can often bypass LLM guardrails by simply reframing a question." Advocates structural scaffolding (role-based assignments, evaluation-first prompts) over negative framing. Core insight: "negative instructions are weaker than positive structural guidance." | [Link](https://www.lakera.ai/blog/prompt-engineering-guide) |
| 24 | Prompt Engineering Best Practices | DigitalOcean | 2025 | Blog post / article | Practitioner Anecdote | Larger models perform worse on negated prompts. Negative instructions "require the AI to interpret and invert them, increasing cognitive load and potential for misunderstanding." Recommends: "don't use passive voice" should become "use active voice." | [Link](https://www.digitalocean.com/resources/articles/prompt-engineering-best-practices) |
| 25 | How to Use AI Negative Prompts for Better Outputs | ClickUp | 2025 | Blog post / article | Practitioner Anecdote | Provides extensive negative prompt examples for text generation across domains (ad copy, business reports, code generation, news summaries). Recommends pairing negatives with detailed positive instructions. Warns excessive restrictions produce "flat, generic content lacking nuance." Notes inconsistent interpretation across platforms. | [Link](https://clickup.com/blog/ai-negative-prompt-examples/) |
| 27 | NeMo Guardrails | NVIDIA | 2024 | Framework documentation | Vendor Recommendation | Open-source toolkit for programmable guardrails. Uses Colang domain-specific language for procedural controls. Implements multi-stage rails: input, dialog, retrieval, and output. Provides programmatic constraint enforcement rather than relying on prompt-level prohibitions. | [Link](https://github.com/NVIDIA-NeMo/Guardrails) |
| 28 | Claude Code Ignores the CLAUDE.md | Christoph Schweres (Medium) | 2026 | Blog post / article | Practitioner Anecdote | Reports Claude Code ignoring explicit CLAUDE.md rules. "When rules are compressed into implicit memory during context summarization, they lose their status as explicit instructions." NEVER rules particularly prone to being dropped during compaction. | [Link](https://medium.com/rigel-computer-com/claude-code-ignores-the-claude-md-how-is-that-possible-f54dece13204) |
| 29 | Prompt Engineering with Guardrails: Safety Design for LLMs | Endtrace | 2025 | Blog post / article | Practitioner Anecdote | Documents common pattern of writing safety directives as negatives (e.g., "never provides medical advice"). Recommends layered defense combining prompt engineering with guardrail systems rather than relying on prompt-level prohibitions alone. | [Link](https://www.endtrace.com/prompt-engineering-with-guardrails-guide/) |
| 30 | The Profound Impact of Prompt Variations on Large Language Model Responses | The Big Data Guy (Substack) | 2024 | Blog post / article | Empirical Evidence | Prompts with negative sentiment consistently decrease factual accuracy by approximately 8.4%. Positive prompts cause smaller reduction of about 2.8%. Neutral prompts yield the most factually accurate responses across all tasks. **Scope note:** This source measures the effect of *negative emotional sentiment/tone* in prompts, NOT the effect of *negative syntactic instructions* (prohibitions like "do not" or "never"). The 8.4% finding is about emotional framing, not instruction syntax. Included because emotional negativity and instructional negativity may share overlapping mechanisms, but the distinction is important. | [Link](https://thebigdataguy.substack.com/p/the-profound-impact-of-prompt-variations) |
| 31 | Negative Prompting Notebook | Nir Diamant (GitHub) | 2025 | Framework documentation | Practitioner Anecdote | Provides hands-on Jupyter notebook tutorial on negative prompting techniques. Covers basic negative examples, explicit exclusions, constraint implementation using LangChain, and methods for evaluating and refining negative prompts. Part of comprehensive 22-technique prompt engineering collection. | [Link](https://github.com/NirDiamant/Prompt_Engineering/blob/main/all_prompt_engineering_techniques/negative-prompting.ipynb) |
| 32 | Claude Code Bug Reports (Issues #5055, #6120, #15443, #18660) | Anthropic (GitHub) | 2025-2026 | Community discussion / forum | Practitioner Anecdote | Multiple bug reports documenting Claude Code ignoring CLAUDE.md rules, particularly NEVER and DO NOT instructions. Issue #5055: "repeatedly violates user-defined rules despite acknowledging them." Issue #18660 requests enforcement mechanism because "instructions are read but not reliably followed." | [Link](https://github.com/anthropics/claude-code/issues/5055) |

### Adjacent Sources

The following source surfaced in negative prompting search results but addresses a related-but-distinct topic. It is excluded from the core 31-source count and evidence tier distribution because it does not meet Source Selection Criterion #1 ("Source must directly address negative instructions, constraints, prohibitions, or positive vs. negative framing in LLM prompting"). It is documented here for completeness and to explain its exclusion.

| # | Title | Org/Author | Year | Type | Topic | Key Finding | URL |
|---|-------|------------|------|------|-------|-------------|-----|
| 26 | Handling Negative Use Cases in Prompt Engineering | Softsquare | 2025 | Blog post / article | AI refusal UX (adjacent) | Addresses when AI systems must say "no" to users. Recommends tactful refusal language, providing reasoning for rejections, offering alternatives, and enabling escalation to human support. This source addresses negative *response* design (how to frame AI refusals), NOT negative *instruction* framing (how to write prohibitive prompts). | [Link](https://www.softsquare.biz/blogs/handling-negative-use-cases-in-prompt-engineering) |

### Evidence Tier Distribution

| Tier | Count | Percentage | Notes |
|------|-------|------------|-------|
| Vendor Recommendation | 9 | 29% | Sources 1, 3, 4, 5, 6, 7, 15, 19, 27 |
| Empirical Evidence | 7 | 23% | Includes sub-categories per Tier Definitions: (a) Controlled experiments (Sources 14, 20, 21), (b) Competition results (Source 18), (c) Practitioner systematic testing (Source 12), (d) Cited academic (Source 13), (e) Sentiment study (Source 30) |
| Practitioner Anecdote | 15 | 48% | Sources 2, 8, 9, 10, 11, 16, 17, 22, 23, 24, 25, 28, 29, 31, 32 |

**Sub-tier note:** Within Empirical Evidence, epistemic weight varies substantially across sub-categories (see Tier Definitions for full descriptions and ordering). Sources 14, 20, and 21 (sub-category a: Controlled experiments) report original structured testing with disclosed methodology and carry the strongest epistemic weight. Source 18 (sub-category b: Competition results) reports competition-evaluated tasks without peer review. Source 12 (sub-category c: Practitioner systematic testing) reports systematic testing without disclosed methodology. Source 13 (sub-category d: Cited academic) cites upstream academic results from Bsharat et al. (2023) rather than reporting original findings. Source 30 (sub-category e: Sentiment study) measures emotional sentiment, not instruction syntax (see source-level scope note). These sub-tier distinctions are annotated per-source in the Source Table above.

**Source 26 exclusion note:** Source 26 (Softsquare, "Handling Negative Use Cases in Prompt Engineering") is documented in the Adjacent Sources section above. It addresses negative *response* design (AI refusal UX), not negative *instruction* framing, and does not meet Source Selection Criterion #1. It is excluded from the core 31-source count and all percentage calculations.

### Source Types

| Type | Count |
|------|-------|
| Vendor documentation | 8 |
| Blog post / article | 17 |
| Framework documentation | 3 |
| Community discussion / forum | 2 |
| Community guide | 1 |
| Conference talk / workshop | 0 |
| **Total core sources** | **31** (excluding Source 26) |
| Adjacent sources (see above) | 1 |

---

## L2: Detailed Analysis

### Theme 1: Vendor Best Practices for Negative Prompting

Three of the four major LLM platform vendors surveyed (Anthropic, OpenAI, Google) explicitly recommend positive framing over negative framing as a primary prompting strategy. Palantir is the notable exception, taking a balanced approach that treats negatives as a standard tool. Despite this 3-to-1 majority, the vendors' guidance differs in important nuances.

**Anthropic (Sources 1, 15)**

Anthropic's Claude 4 best practices guide is the most explicit: "Tell Claude what to do instead of what not to do" (Source 1). The guide provides a concrete reframing example: instead of "Do not use markdown in your response," use "Your response should be composed of smoothly flowing prose paragraphs." Critically, Anthropic also warns that *aggressive* negative language -- "CRITICAL!", "YOU MUST", "NEVER EVER" -- "actively hurts newer Claude models" and produces worse results than calm, direct instructions. Their context engineering guide (Source 15) extends this by recommending "strong heuristics to guide behavior" and "diverse, canonical examples" over "a laundry list of edge cases."

Notably, Anthropic's own Claude system prompt *does* use negative constraints, but frames them as descriptive behavioral statements ("Claude does not claim to be human") rather than prohibitive commands ("NEVER claim to be human"). This distinction -- *declarative negation* vs. *imperative prohibition* -- is an important architectural choice that no vendor explicitly documents but all implicitly practice.

**Evidence tier:** Vendor Recommendation. These are guidelines from the model creator. They are backed by internal testing but the testing data is not published.

**OpenAI (Sources 3, 4, 5)**

OpenAI's guidance has evolved across model generations. The base prompting guide (Source 3) provides the canonical "movie chatbot" example where "DO NOT ASK FOR INTERESTS" was violated by the model. The GPT-4.1 guide (Source 4) adds nuance: because GPT-4.1 follows instructions "more closely and more literally," negative instructions *are* taken more seriously, but can cause adverse effects like hallucinating tool inputs when told it "must call a tool before responding." The GPT-5 guide (Source 5) provides the strongest vendor evidence for *when negatives work*: domain-specific, unambiguous negatives like "Do NOT guess or make up an answer" and "NEVER add copyright headers" succeed because they "prevent concrete harms rather than attempting to control reasoning depth."

**Evidence tier:** Vendor Recommendation. OpenAI provides examples but not systematic testing data.

**Google (Sources 6, 7)**

Google's Gemini documentation (Source 6) recommends using examples to show patterns to follow rather than anti-patterns to avoid: "Don't end haikus with a question" should become "Always end haikus with an assertion." The Gemini 3 guide (Source 7) adds a practical insight: negative constraints may be *silently dropped* on complex requests, so critical restrictions should be placed at the end of the instruction as a mitigation.

**Evidence tier:** Vendor Recommendation. Google's guidance is based on internal model behavior observation.

**Palantir (Source 19)**

Palantir takes a more balanced approach, explicitly supporting both positive constraints ("Summarize in no more than three sentences") and negative examples ("Generate pros and cons, but exclude personal opinions"). Their guidance treats negatives as one tool among many rather than as categorically inferior.

**Evidence tier:** Vendor Recommendation based on platform deployment experience.

**Cross-Vendor Synthesis**

| Vendor | Core Recommendation | Negatives Allowed? | Nuance |
|--------|--------------------|--------------------|--------|
| Anthropic | Positive framing preferred | Yes, for safety boundaries | Aggressive language actively hurts newer models |
| OpenAI | Positive framing preferred | Yes, for concrete harm prevention | Newer models follow negatives more literally, including unintended consequences |
| Google | Positive framing preferred | Yes, placed at end of instruction | Complex requests may silently drop negatives |
| Palantir | Balanced approach | Yes, for scope limiting | Treats negatives as standard tool |

### Theme 2: Negative vs Positive Prompting Effectiveness

This theme covers the practitioner and empirical evidence comparing the two approaches.

**The Pink Elephant Problem (Sources 8, 9, 11, 12, 24)**

Multiple independent sources converge on a single explanation: negative instructions fail because they invoke the concept they aim to suppress. The 16x Engineer analysis (Source 8) connects this to Ironic Process Theory from cognitive psychology. Sean Trott (Source 9) cites Ettinger's (2020) BERT study showing the model predicted "bird" for "A robin is not a ___" -- functionally ignoring the negation operator. Thomas Wiegold (Source 11) summarizes it directly: "telling a model not to do something forces it to process that concept first."

**Important caveat on the attention-weight explanation:** The claim that transformer attention mechanisms elevate concept representations regardless of negation operators is an *analogy* drawn from cognitive psychology's Ironic Process Theory, NOT a mechanistically demonstrated property of transformer architectures. No source in this 31-source survey provides direct empirical evidence (e.g., attention weight visualizations, probing studies) that negation tokens fail to suppress attention to negated concepts in transformer models. The behavioral parallel -- models producing outputs they were instructed to avoid -- is well-documented across multiple independent practitioner reports, but the *mechanism* remains an explanatory hypothesis rather than a confirmed architectural property. The BERT study (Ettinger, 2020) cited by Source 9 demonstrates that a specific model fails on negation tasks, but does not establish the attention-weight mechanism that practitioners attribute to it.

**Evidence tier:** Mix of Practitioner Anecdote and Empirical Evidence. The BERT study is empirical; the Pink Elephant framing is an explanatory analogy, not empirical evidence of transformer internals.

**Quantitative Findings (Sources 13, 14, 18, 30)**

The Bsharat et al. (2023) academic study (summarized by PromptHub's Source 13) reports the strongest quantitative claim: affirmative directives showed 55% improvement and 66.7% correctness increase for GPT-4. These figures originate from the academic paper, not from PromptHub's own independent testing -- PromptHub is summarizing upstream academic results. The figures should be attributed to Bsharat et al., not to PromptHub.

The Big Data Guy analysis (Source 30) found negative sentiment prompts decrease factual accuracy by 8.4%, while positive prompts decrease accuracy by only 2.8%, and neutral prompts perform best. **Important distinction:** Source 30 measures the effect of *negative emotional sentiment/tone* in prompts (e.g., hostile, critical, or pessimistic language), NOT the effect of *negative syntactic instructions* (prohibitions like "do not" or "never"). The 8.4% finding demonstrates that emotional framing affects output quality, which is a related but distinct phenomenon from instructional negation. The overlap suggests that negativity -- whether emotional or instructional -- may share degradation mechanisms, but the evidence does not directly support claims about "do not" instruction compliance.

The Inverse Scaling Prize (Source 18) provides the most striking finding: larger models perform *worse than random* on negated instructions. This is an inverse scaling effect -- a genuinely counterintuitive result where more capable models are more vulnerable to negation errors. The researchers found potential U-shaped recovery at very large scales, suggesting the problem may be resolvable through scale, but current production models remain in the "valley" of poor negation handling. **Caveat:** Source 18 is a competition prize announcement on LessWrong, not a peer-reviewed controlled experiment. The underlying tasks were submitted by competition participants and evaluated by prize organizers. The U-shaped recovery finding is a speculative observation from the competition results, not a peer-reviewed conclusion; it should be treated as a hypothesis requiring further validation. The academic paper providing formal analysis (arXiv 2306.09479) is covered in the companion Session 1A survey.

**Evidence tier:** Empirical Evidence, with sub-tier qualifications. Source 13 cites academic results (Bsharat et al.) rather than original testing. Source 18 reports competition results. Source 30 measures emotional sentiment, not instruction syntax. See Source Table for per-source limitations.

**Prompt Bloat and Instruction Count Effects (Sources 14, 16, 17)**

The MLOps Community research (Source 14) demonstrates that reasoning performance degrades at approximately 3,000 tokens, well below context window limits. This degradation is not mitigated by Chain-of-Thought prompting, indicating a fundamental limitation.

The HumanLayer analysis (Source 16) estimates that frontier LLMs follow approximately 150-200 instructions with reasonable consistency, with quality decreasing linearly as count increases (methodology for determining this range not disclosed; treat as an unverified practitioner estimate). Since system prompts already consume approximately 50 instructions, the "budget" for additional rules is constrained.

The DEV Community analysis (Source 17) documents instruction decay over conversation length: ~95% compliance at messages 1-2, dropping to 20-60% by messages 6-10 (practitioner observation; specific decay rates not independently verified and measurement methodology not disclosed). This is particularly relevant for negative instructions, which are often placed at the beginning of system prompts and thus suffer the greatest positional decay.

**Evidence tier:** Practitioner Anecdote. Sources 16 and 17 present practitioner observations without disclosed testing methodology. The specific numerical claims (150-200 instruction range, 95%->20-60% decay) should be treated as directional estimates, not precise measurements.

**DreamHost Systematic Testing (Source 12)**

DreamHost systematically tested 25 Claude prompt engineering techniques and found that avoiding negative phrasing "significantly improves results." They provide specific before/after pairs: "Don't use complex jargon" becomes "Use simple, everyday language." Their methodology (testing 25 techniques across multiple prompt types) represents one of the more structured practitioner evaluations in this survey, though the specific testing methodology -- sample sizes, evaluation criteria, model version, and number of trials -- is not disclosed in the published blog post.

**Evidence tier:** Empirical Evidence (Practitioner systematic testing). Structured testing with before/after comparisons, but without disclosed methodology or independent reproducibility. Directional findings are credible; precise effect sizes cannot be verified from the published account.

### Theme 3: Production Applications of Negative Constraints

Production systems use negative constraints in specific, architecturally significant ways that differ from casual prompt engineering.

**Safety Guardrails (Sources 15, 23, 27, 29)**

Production guardrail systems represent the primary legitimate use case for negative constraints. NVIDIA's NeMo Guardrails (Source 27) implements multi-stage constraint enforcement using Colang, a domain-specific language. Rather than relying on prompt-level prohibitions ("do not discuss X"), it uses programmatic rails that operate at input, dialog, retrieval, and output stages. This architectural approach separates constraint enforcement from prompt engineering.

Lakera AI (Source 23) explicitly states that "negative instructions are weaker than positive structural guidance" and recommends layered defenses. Endtrace (Source 29) documents the common pattern of writing safety directives as negatives but recommends combining prompt-level constraints with guardrail systems.

The key production insight is that negative constraints work best when enforced *programmatically* rather than through natural language instructions. This aligns with the HumanLayer recommendation (Source 16): "Never send an LLM to do a linter's job."

**System Prompt Architecture (Sources 1, 4, 5, 28)**

Production system prompts from multiple vendors demonstrate a specific pattern for constraint usage:
- Safety and ethical boundaries: expressed as declarative negatives ("Claude does not provide information that could be used to make weapons")
- Behavioral constraints: expressed as positive framing with contextual motivation ("Your response will be read aloud by a text-to-speech engine, so never use ellipses since the engine won't know how to pronounce them" -- Source 1)
- Topic restrictions: expressed as enumerated lists within structured sections (Source 4: dedicated prohibited topics section with deflection phrases)
- Code quality constraints: expressed as specific, unambiguous negatives for concrete harm prevention (Source 5: "NEVER add copyright headers")

**Context Compaction and Rule Loss (Sources 17, 28, 32)**

A critical production concern is that negative instructions are particularly vulnerable to context compaction. Source 28 documents how "rules compressed into implicit memory during context summarization lose their status as explicit instructions." The Claude Code GitHub issues (Source 32) provide extensive real-world evidence of this phenomenon, with multiple users reporting NEVER and DO NOT instructions being ignored after extended conversations.

This suggests that production systems relying on negative instructions for critical behavior control face a reliability problem that worsens over conversation length.

### Theme 4: Framework Support for Negative Prompting

**Structural note:** Theme 4 overlaps with Theme 3 (Production Applications) in that both address programmatic constraint enforcement. The separation rationale is: Theme 3 covers *production usage patterns* -- how practitioners deploy negative constraints in real systems (safety guardrails, system prompts, context compaction). Theme 4 covers *framework tooling* -- what libraries and SDKs provide for implementing constraints programmatically. The distinction matters because framework support enables the patterns described in Theme 3; a practitioner reading Theme 3's recommendations needs Theme 4's tooling assessment to implement them.

Framework support for negative prompting patterns is sparse compared to general prompt engineering tooling.

**DSPy Assertions (Source 21)**

DSPy provides the most sophisticated framework-level support for constraint-based prompting through its Assertions feature. LM Assertions are programming constructs that enforce user-specified properties on LM outputs. When a constraint is violated, the pipeline can backtrack (Suggest construct) or halt (Assert construct), with the retry prompt including past failed attempts and error messages.

The most relevant innovation is counter-example bootstrapping: DSPy collects traces of failed assertions during backtracking and uses them as few-shot demonstrations of what NOT to do. This is a programmatic approach to negative prompting that is architecturally distinct from natural language prohibitions. The results are compelling: constraints pass up to 164% more often, with up to 37% more higher-quality responses.

**Evidence tier:** Empirical Evidence (framework-level benchmarks).

**LangChain (Source 31)**

Nir Diamant's negative prompting notebook (Source 31) demonstrates LangChain integration for constraint implementation, but this is a community tutorial rather than official framework documentation. LangChain itself does not have dedicated negative prompting abstractions.

**NeMo Guardrails (Source 27)**

As discussed in Theme 3, NeMo Guardrails provides programmatic constraint enforcement but operates at the infrastructure level rather than the prompt engineering level. It enforces constraints through Colang-defined rails rather than through natural language negative instructions.

**Framework Gap**

No major prompt engineering framework (LangChain, LlamaIndex, Semantic Kernel) provides dedicated negative prompting abstractions or best practices documentation. DSPy's Assertions feature is the closest analog, but it implements constraints programmatically rather than through natural language instruction patterns.

### Theme 5: Limitations and Failure Modes

Negative instructions fail through several distinct mechanisms identified across the surveyed sources.

**Mechanism 1: Attention-Based Concept Activation -- Hypothesized (Sources 8, 9, 24)**

Multiple practitioners describe a pattern where negative instructions paradoxically increase the probability of the forbidden output. The proposed explanation is that transformer attention mechanisms activate representations of concepts mentioned in the prompt regardless of negation operators -- e.g., when a prompt says "do not mention politics," the attention weights elevate "politics" tokens, making political content more probable. **This explanation is an analogy drawn from cognitive psychology's Ironic Process Theory (the "white bear" effect), NOT a mechanistically demonstrated property of transformer architectures.** No source in this 31-source survey provides direct empirical evidence (such as attention weight visualizations or probing studies) confirming that negation tokens fail to suppress concept activation in transformer models. The *behavioral* parallel is well-documented across independent practitioners; the *mechanistic* explanation remains a hypothesis.

**Mechanism 2: Inverse Scaling (Source 18)**

The Inverse Scaling Prize demonstrated that negation compliance *worsens* with model scale across a specific range. Smaller models answer randomly on negated instructions; larger models know the relevant facts but miss the negation, answering incorrectly. This creates a paradox where more capable models are more vulnerable to negation errors in a specific model-size range, though U-shaped recovery at very large scales is possible (Source 18 competition announcement; this recovery finding is speculative -- see Source 18 limitation note and arXiv 2306.09479 in Session 1A survey for formal analysis).

**Mechanism 3: Instruction Count Degradation (Sources 14, 16)**

As the number of instructions increases, the likelihood of contradictions between them grows, and the model's ability to follow all instructions simultaneously decreases. Negative instructions are particularly susceptible because they define constraint boundaries that may conflict with positive behavioral directives.

**Mechanism 4: Positional Decay (Source 17)**

Instructions at the beginning of context lose influence over conversation length. Negative instructions in system prompts are particularly vulnerable because they are typically placed at the start and not reinforced through the conversation.

**Mechanism 5: Context Compaction Loss (Sources 28, 32)**

During context compaction (when the conversation exceeds the context window and must be summarized), negative rules may lose their imperative force and become merely descriptive text. The distinction between "NEVER create duplicate files" (a command) and "the system tries not to create duplicate files" (a description) is lost during summarization.

**Mechanism 6: Semantic Confusion with Irrelevant Information (Source 14)**

Semantically similar but irrelevant information poses greater danger than completely unrelated content. Negative instructions about related topics can introduce semantically similar concepts that confuse the model more than pure noise would.

### Theme 6: Emerging Patterns and Trends

**Pattern 1: Declarative Over Imperative Negation (Sources 1, 5 -- analyst inference)**

The emerging best practice appears to be expressing constraints as declarative behavioral descriptions rather than imperative prohibitions. "Claude does not claim to be human" (declarative) outperforms "NEVER claim to be human" (imperative). **This pattern label ("Declarative Over Imperative Negation") is an analyst inference synthesized from Source 1 and Source 5, not a term used by either source.** Source 1 (Anthropic) demonstrates this pattern implicitly through its own system prompt design -- using "Claude does not..." rather than "NEVER..." -- but does not explicitly name or recommend the declarative-over-imperative distinction. Source 5 (OpenAI GPT-5) aligns with this pattern by emphasizing constraints that "prevent concrete harms" in specific, unambiguous form. No source in this survey explicitly articulates a "declarative vs. imperative negation" framework. The pattern is editorially identified by the analyst as a synthesis of observed vendor behavior.

**Pattern 2: Programmatic Constraint Enforcement (Sources 21, 27 -- analyst inference)**

The field is moving toward programmatic constraint enforcement through frameworks like DSPy Assertions and NeMo Guardrails. These approaches remove the ambiguity of natural language by implementing constraints as code-level checks with defined backtracking and retry semantics. DSPy's 164% improvement in constraint compliance demonstrates the gap between natural language prohibitions and programmatic enforcement. **This pattern label ("Programmatic Constraint Enforcement") and the trend claim are analyst synthesis from Sources 21 and 27.** Neither source explicitly names this as an industry trend or uses this pattern label. Source 21 (DSPy Assertions) presents a framework-level solution with benchmarks; Source 27 (NeMo Guardrails) presents a separate programmatic approach. The analyst identifies the convergence between these independent frameworks as evidence of a directional shift toward programmatic enforcement.

**Pattern 3: Context Engineering Over Prompt Engineering (Sources 11, 15 -- analyst inference)**

Anthropic's "context engineering" framing (Source 15) signals a shift from optimizing individual prompt phrases to managing the entire context window as a finite resource. In this paradigm, negative instructions are not just suboptimal -- they are *wasteful* of a precious resource, consuming tokens without proportional behavioral control. The recommendation to use "high-signal tokens" implies that positive instructions have a better signal-to-token ratio than negative ones. **This pattern label ("Context Engineering Over Prompt Engineering") is analyst inference synthesized from Sources 11 and 15.** Source 15 (Anthropic) introduces "context engineering" as a concept but does not frame it as superseding prompt engineering or explicitly connect it to negative instruction effectiveness. Source 11 (Wiegold) discusses prompt length optimization but does not use the term "context engineering." The analyst synthesizes these two sources into a trend narrative about the evolution from prompt-level to context-level optimization.

**Pattern 4: Model-Specific Compliance Evolution (Sources 4, 5 -- analyst synthesis)**

OpenAI's GPT-4.1 and GPT-5 guides document a model-generation shift: newer models follow instructions more literally, including negative ones. This means negative instructions work *more reliably* on current-generation models, but their unintended consequences are also more pronounced. A "DO NOT call tools" instruction may be followed literally when the model should have called a tool, because the literal compliance overrides the model's judgment. **This pattern label ("Model-Specific Compliance Evolution") and the trend characterization are analyst synthesis from Sources 4 and 5.** Neither source uses this term or explicitly frames the observation as a cross-generation evolutionary trend. Source 4 (GPT-4.1) notes that the model follows instructions "more closely and more literally" than predecessors; Source 5 (GPT-5) provides specific examples of effective negative constraints. The analyst synthesizes these into a directional pattern of increasing literal compliance across model generations.

**Pattern 5: Examples Over Instructions (Source 20)**

QED42's finding that "the power of examples far exceeds the power of instructions" represents a fundamental shift in constraint design. Rather than telling the model what not to do (or even what to do), showing it what correct behavior looks like through diverse few-shot examples produces more reliable compliance. This pattern subsumes the positive/negative framing debate by sidestepping instruction-based control entirely.

**Cross-Vendor Convergence**

Despite different model architectures, three of four major vendors (Anthropic, OpenAI, Google) converge on the same recommendation: positive framing preferred, negatives for narrow safety boundaries only, examples trump instructions, and programmatic enforcement for critical constraints. Palantir diverges from this consensus, treating negatives as standard tools without categorical preference (see Theme 1). This three-vendor convergence nonetheless suggests the recommendation is model-architecture-agnostic rather than specific to any particular model family.

**Cross-Vendor Divergence**

The divergence is in *degree* of recommendation: Anthropic is the most emphatic ("actively hurts"), Google provides the most pragmatic mitigation (constraint placement), OpenAI provides the most nuanced guidance on when negatives work (concrete harm prevention), and Palantir treats negatives as a standard tool without strong preference.

---

## Cross-References

- **Academic Survey (Session 1A companion):** This industry survey intentionally excludes peer-reviewed academic papers. The Inverse Scaling Prize findings (Source 18) and Bsharat et al. 26 Principles (cited by Source 13) represent intersection points where academic findings inform industry practice. The academic survey should provide deeper analysis of the underlying mechanisms (attention weights, negation processing in transformer architectures, inverse scaling phenomenon).

- **Model-Generation Confound:** Sources in this survey span publication dates from 2023 to 2026, a period of rapid model capability evolution (GPT-3.5 -> GPT-4 -> GPT-4.1 -> GPT-5; Claude 2 -> Claude 3 -> Claude 4; Gemini 1 -> Gemini 2 -> Gemini 3). Findings from earlier model generations may not apply to frontier models. In particular: (a) the Inverse Scaling Prize (Source 18, 2023) tested models that predate current frontier capabilities; (b) the Bsharat et al. 26 Principles (cited by Source 13, 2023) were validated on GPT-4, not on GPT-4.1 or GPT-5; (c) OpenAI's own GPT-4.1 guide (Source 4) explicitly notes that newer models follow instructions "more closely and more literally" than predecessors, suggesting negation compliance may be improving. Cross-generation comparisons should treat findings as generation-specific unless validated on current frontier models.

- **Revision Trigger:** This survey should be revised when: (a) a major model generation releases with documented changes to instruction-following behavior; (b) a controlled A/B study comparing negative vs. positive instruction variants is published; or (c) 6 months have elapsed from the survey date (2026-02-27), whichever comes first. The rapid pace of model evolution means findings in this survey have a practical shelf life of approximately 6-12 months.

- **Gaps Requiring Follow-Up Research:**
  1. Controlled A/B testing of negative vs. positive instruction variants in production systems
  2. Model-specific compliance rate measurements for different negative instruction patterns
  3. Taxonomy of negative instruction types and their relative effectiveness by use case
  4. Impact of instruction decay on negative vs. positive instructions over extended conversations
  5. Cross-model comparison of negation handling (Claude vs. GPT vs. Gemini)
  6. DSPy Assertions vs. natural language constraints: comparative effectiveness study

---

## Methodology

### Search Queries Executed

40 search queries were executed via WebSearch, with top results fetched and analyzed via WebFetch. Of the results returned, 31 unique sources met the selection criteria below and constitute the core source catalog. One additional source (Source 26, Softsquare) is documented in the Adjacent Sources section -- it surfaced in search results but addresses negative *response* design rather than negative *instruction* framing and does not meet Selection Criterion #1. The remaining results were excluded due to: (a) academic paper scope (deferred to Session 1A companion survey), (b) duplicate content from previously cataloged sources, (c) insufficient relevance to negative instruction framing, (d) paywalled content inaccessible for analysis, or (e) derivative content aggregating already-cataloged sources without original findings. See the "Exclusion Decisions with Rationale" table for specific exclusions.

1. `negative prompting best practices LLM 2024 2025`
2. `Anthropic prompt engineering negative instructions best practices`
3. `OpenAI prompt engineering "do not" instructions guidelines`
4. `Google Gemini prompt guidelines prohibitions negative framing`
5. `prompt engineering positive vs negative framing effectiveness`
6. `production LLM system prompt prohibitions constraints quality control`
7. `"pink elephant problem" LLM negative instructions prompting`
8. `LangChain DSPy constraint prompting negative instructions framework`
9. `Claude system prompt "do not" "never" best practices 2024 2025`
10. `prompt engineering constraints guardrails negative vs positive instructions blog`
11. `A/B testing prompt engineering positive negative instructions results`
12. `system prompt design prohibitions "what not to do" LLM production`
13. `Cohere command prompt engineering negative instructions constraints 2024`
14. `"prompt bloat" negative instructions LLM performance degradation`
15. `LLM negation understanding failure "do not" compliance rate`
16. `effective context engineering AI agents negative prompting constraints 2025`
17. `GPT-4.1 GPT-5 prompting guide negative instructions prohibitions`
18. `Palantir LLM prompt engineering best practices constraints`
19. `PromptingGuide.ai negative prompting tips best practices`
20. `Claude Code CLAUDE.md negative instructions rules "NEVER" effectiveness`
21. `LLM instruction following negation inverse scaling problem`
22. `prompt engineering reframe negative positive instructions examples blog 2024 2025`
23. `guardrails AI NeMo negative constraints prompt production system`
24. `DreamHost Claude prompt engineering tested practices negative instructions`
25. `MIT Sloan effective prompts AI negative positive instructions`
26. `DigitalOcean prompt engineering best practices negative instructions avoid`
27. `ClickUp negative prompt examples LLM effective use`
28. `Google AI prompt design strategies negative constraints avoid`
29. `Softsquare negative use cases prompt engineering handling`
30. `Nir Diamant negative prompting notebook technique LLM`
31. `PromptHub blog Google prompt engineering principles negative instructions`
32. `Thomas Wiegold prompt engineering best practices 2026 negative framing`
33. `Aakash G newsletter prompt engineering $50M companies negative positive framing`
34. `DSPy assertions constraints self-refining pipeline negative prompting`
35. `GPT-5 prompting guide constraint design system prompt prohibitions 2025`
36. `Latitude blog prompt engineering challenges negative instructions solutions`
37. `QED42 prompt-based guardrails negative instructions effectiveness`
38. `CodeSignal prompt engineering best practices 2025 negative positive instructions`
39. `Endtrace prompt engineering guardrails safety negative instructions design`
40. `V7Labs prompt engineering guide negative instructions avoid 2025`

### Date Range

- Searches conducted: 2026-02-27
- Source publication dates: 2023-2026
- No sources older than 2023 included

### Source Selection Criteria

1. **Relevance:** Source must directly address negative instructions, constraints, prohibitions, or positive vs. negative framing in LLM prompting
2. **Uniqueness:** No two sources from the same author on the same topic counted separately
3. **Recency:** Sources from 2023 or later preferred; older sources excluded unless providing foundational concepts
4. **Evidence quality:** Sources classified by evidence tier; vendor claims noted as such rather than treated as empirical evidence
5. **Exclusion of academic papers:** Peer-reviewed research excluded per task scope (covered in Session 1A)

### Survey Limitations

**Survey Limitations:** This survey was conducted by a single researcher executing all 40 search queries in a single session (2026-02-27). A different researcher with alternative query formulations or different search platforms may surface additional sources not included here. No formal saturation criterion was applied to the source count; 31 core sources reflects the output of the defined search strategy against the stated selection criteria, not a saturation-validated representative sample. All source URLs were accessed 2026-02-27; link availability may degrade over time. Non-English language sources were not systematically searched. Search queries were primarily framed around negative prompting limitations and best practices; no queries specifically targeted successful negative prompting applications (e.g., "when negative prompting works," "negative prompting success stories"), which may bias the evidence balance toward failure cases.

### Exclusion Decisions with Rationale

| Excluded Source | Reason |
|----------------|--------|
| "Negation: A Pink Elephant in the Large Language Models' Room?" (arXiv 2503.22395) | Academic paper; belongs in Session 1A |
| "Suppressing Pink Elephants with Direct Principle Feedback" (arXiv 2402.07896) | Academic paper; belongs in Session 1A |
| "Do not think about pink elephant!" (arXiv 2404.15154) | Academic paper; belongs in Session 1A |
| "Inverse Scaling: When Bigger Isn't Better" (arXiv 2306.09479) | Academic paper; belongs in Session 1A (LessWrong prize announcement included as industry source) |
| "Boosting Instruction Following at Scale" (arXiv 2510.14842) | Academic paper; belongs in Session 1A |
| "Vision-Language Models Do Not Understand Negation" (CVPR 2025) | Academic paper + vision-specific; belongs in Session 1A |
| "DSPy Assertions" (arXiv 2312.13382) | Academic paper; DSPy docs and Arize AI blog used as industry source instead |
| CodeSignal prompt engineering 2025 | Excluded: no specific content on negative instructions found in accessible content |
| Aakash G newsletter (paywalled section) | Partially excluded: accessible portion contained no specific negative instruction guidance; Bolt/Cluely system prompt examples noted but did not contain relevant negative prompting analysis |
| MIT Sloan EdTech prompts guide | Content overlapped with Virtualization Review hard/soft negatives analysis; not counted as separate source |
| Multiple Shadecoder/PromptBuilder guides | Derivative content aggregating other sources already cataloged; no original findings |

---

*Research conducted by ps-researcher for PROJ-014-negative-prompting-research, Phase 1B (Industry Survey).*
*Date: 2026-02-27*
*Agent: ps-researcher-002*
*Revision 1: 2026-02-27 -- Addressed C4 tournament iteration 1 findings (14 items applied: 6 P0, 6 P1, 2 of 4 P2). Key changes: corrected L0/L1 percentage consistency, added evidence tier definitions with sub-tier qualifiers, added Pink Elephant analogy caveats, qualified vendor consensus claim, added source-level limitation notes, expanded gaps list, added model-generation confound warning, added revision trigger. P2-14 (query-outcome mapping) not addressed; P2-15 (PromptHub attribution) partially addressed.*
*Revision 2: 2026-02-27 -- Addressed C4 tournament iteration 2 findings (8 items: 3 P0, 3 P1, 2 P2). Key changes: (P0-1) expanded Evidence Tier Definitions to define all 5 sub-tier labels with epistemic weighting; (P0-2) excluded Source 26 from core 31-source count and moved to Adjacent Sources section, recalculated all percentages (29%/23%/48%); (P0-3) applied analyst-inference labels to Theme 6 Patterns 2-3 for consistency with Pattern 1; (P1-4) added U-shaped recovery caveat to Theme 2 and Theme 5 Mechanism 2; (P1-5) replaced "PromptHub analysis" lead phrase with Bsharat et al. attribution throughout; (P1-6) corrected this footer to accurately reflect changes applied; (P2-7) added sub-tier communication caveat to L0 Evidence Landscape Assessment; (P2-8) added Theme 3-4 bifurcation rationale note.*
*Self-review (S-010) applied: Verified 31 core sources + 1 adjacent source. L0/L1 percentage consistency confirmed (29%/23%/48% of 31 core sources; 9+7+15=31). All sub-tier labels in Distribution table match Tier Definitions vocabulary (5 sub-categories defined and used consistently). All Theme 6 patterns consistently labeled for analyst inference (Patterns 1-3 labeled; Patterns 4-5 well-sourced, no label needed). All "32-source" references updated to "31-source." PromptHub attribution corrected at all occurrences. Source Types table corrected (blog post count: 17; total: 8+17+3+2+1=31). U-shaped recovery caveats present in both Theme 2 and Theme 5 Mechanism 2.*
*Revision 3: 2026-02-27 -- Addressed C4 tournament iteration 3 findings (4 convergent gaps: A, B, C, D). Key changes: (Gap A/P0) added Survey Limitations sub-section to Methodology disclosing single-researcher, single-session, no saturation criterion, URL access dates, and English-only scope; (Gap B/P1) added model-generation caveat to L0 primary recommendation bullet with Sources 4-5 cross-reference; (Gap C/P2) added analyst-synthesis label to Theme 6 Pattern 4 heading and disclosure note in body text for consistency with Patterns 1-3; (Gap D/P2) verified Source Types table counts -- blog post count of 17 confirmed correct (adversary's verification erroneously listed Source 2 instead of Source 20 in blog count; actual blogs: Sources 8-14, 16-17, 20, 22-25, 28-30 = 17; community guide: Source 2 = 1; total 8+17+3+2+1=31). No numeric correction needed.*
*Self-review (S-010) applied: (1) Source Types table sums verified: 8+17+3+2+1=31, correct. (2) L0 percentage figures unchanged (29%/23%/48%). (3) All 4 gaps addressed (A: methodology limitations added; B: L0 model-gen caveat added; C: Pattern 4 analyst-synthesis label added; D: verified correct, no change needed). (4) No new inconsistencies introduced. Theme 6 Patterns 1-4 now all carry analyst-inference/synthesis labels; Pattern 5 remains well-sourced with single direct source.*
*Revision 4: 2026-02-27 -- Addressed C4 tournament iteration 4 findings (3 convergent gaps: A, B, C). Key changes: (Gap A/P1) corrected L0 model-generation caveat temporal framing -- removed "future" language, replaced with accurate statement that GPT-4.1 and GPT-5 (2025) already demonstrate improved negative instruction compliance as a current documented phenomenon; removed redundant "unintended consequences" clause from replacement since the preceding (unchanged) sentence already covers that concept; (Gap B/P2) corrected Theme 6 Cross-Vendor Convergence claim from "all major vendors" to "three of four major vendors (Anthropic, OpenAI, Google)" with explicit acknowledgment of Palantir's documented divergence for internal consistency with Theme 1; (Gap C/P2) added query framing bias disclosure to Survey Limitations paragraph noting search queries were primarily framed around failure cases with no queries targeting successful negative prompting applications.*
*Self-review (S-010) applied: (1) No new inconsistencies introduced -- L0 caveat now accurately frames model-generation narrowing as current (2025), not future; Theme 6 convergence claim now consistent with Theme 1 Palantir analysis. (2) L0/L1/L2 percentage figures unchanged (29%/23%/48%). (3) Source count unchanged: 31 core + 1 adjacent. (4) All 3 gaps addressed with minimal, targeted edits. (5) Verified no other text was modified beyond the three specified changes and this footer. (6) Confirmed "future" does not appear in L0 caveat. (7) Theme 6 Cross-Vendor Convergence now says "three of four major vendors" with Palantir exception noted, consistent with L0 bullet 1 and Theme 1.*
