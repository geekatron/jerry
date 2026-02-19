# External Prompt Engineering Survey

> Research survey of external prompt engineering documentation, academic sources,
> and industry best practices. Produced by ps-researcher as part of
> PROJ-006-jerry-prompt / prompt-research-20260218-001 / Phase 1 Discovery.

**Date**: 2026-02-18
**Author**: ps-researcher (problem-solving skill agent)
**Sources**: 5 distinct sources surveyed (Note: Source 5 is indirect via DAIR.AI)
**Revision**: v1.1.0 — 2026-02-18 (ps-critic revision: Source 5 reclassified; Section 8 added)
**Status**: Complete

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level synthesis of key findings for stakeholders |
| [L1: Detailed Findings](#l1-detailed-findings) | Organized findings by research focus area |
| [L2: Source Evidence](#l2-source-evidence) | Full citations, quotes, and URLs for all sources |
| [Research Gaps and Limitations](#research-gaps-and-limitations) | Known gaps, limitations, and indirect sources |

---

## L0: Executive Summary

Prompt engineering is the discipline of designing inputs to language models to produce reliably high-quality outputs. Across five surveyed sources spanning official documentation from Anthropic and independent research guides, a consistent set of structural principles emerge. Effective prompts share four core qualities: they are **specific and contextual** (not vague), **structurally organized** (using XML tags, numbered steps, or role definitions), **grounded in examples** (few-shot or multishot), and **scaffolded for reasoning** (chain-of-thought invocations). These principles are not merely stylistic; controlled comparisons across sources show measurable, sometimes dramatic improvements in output quality when clear structure replaces ambiguous instruction.

For complex, multi-step agentic workflows, the evidence converges on a complementary set of practices: decompose tasks into sequential subtasks (prompt chaining), give agents high-level goals with enough freedom to reason, describe tools precisely so agents select them correctly, and build in feedback loops so agents can self-verify before completing. The ReAct (Reasoning + Acting) framework from academic research formalizes this interleaving of reasoning and tool invocation, and it has demonstrated superior performance over either pure chain-of-thought or pure action-based approaches on complex multi-step tasks. Anti-patterns — vague instructions, negative framing, attempting to jam all complexity into one monolithic prompt, and catching exceptions too broadly — are consistently identified as root causes of degraded output quality.

---

## L1: Detailed Findings

### 1. Prompt Structure Patterns

**Core finding**: Prompts with explicit structural elements — role definition, context, numbered instructions, and clear output format — consistently outperform vague prompts across all evaluated scenarios.

#### 1.1 Role Definition (System Prompts)

Assigning a specific role to the AI model is "the most powerful way to use system prompts." Role prompting adjusts not just domain knowledge but also tone, focus, and communication style. The improvement is not marginal: in the legal contract example, role prompting turned a generic summary into a critical professional analysis that identified multi-million-dollar liability risks that the no-role version missed entirely.

Anthropic recommends:
- Use the `system` parameter for the role definition
- Keep task-specific instructions in the user turn
- Experiment with specificity: "data scientist specializing in customer insight analysis for Fortune 500 companies" yields different results than simply "data scientist"

**Example (from Anthropic documentation):**
```
System: You are the General Counsel of a Fortune 500 tech company.
User: Analyze this software licensing agreement for potential risks...
```

#### 1.2 Context and Specificity

The "golden rule of clear prompting" from Anthropic: "Show your prompt to a colleague, ideally someone who has minimal context on the task, and ask them to follow the instructions. If they're confused, Claude will likely be too."

Specific elements that improve performance:
- **Task purpose**: What the results will be used for
- **Audience**: Who the output is intended for
- **Workflow position**: Where this task sits in a larger process
- **Success criteria**: What a completed task looks like
- **Output format**: Exactly what the response should contain and how it should be structured

**Contrast (from Anthropic documentation):**

Vague: `"Please remove all personally identifiable information from these customer feedback messages."`

Specific: Numbered step-by-step rules for each PII category, output format specification, and edge case handling.

The specific version produced perfect output. The vague version left customer names in the output.

#### 1.3 XML Tag Structure

XML tags for prompt organization are "a game-changer" when prompts involve multiple components. Benefits:
- **Clarity**: Separates instructions, context, and examples cleanly
- **Accuracy**: Reduces misinterpretation when variables are substituted into prompts (prevents Claude from confusing where one injected section ends and another begins)
- **Flexibility**: Allows targeted modification of individual sections
- **Parseability**: Makes structured output extraction reliable

Recommended tags: `<instructions>`, `<example>`, `<formatting>`, `<document>`, `<thinking>`, `<answer>`, `<findings>`, `<recommendations>`

Best practices: be consistent with tag names, nest tags for hierarchical content, and combine with other techniques (e.g., `<examples>` wrapping multishot examples).

#### 1.4 Instruction Format

From the DAIR.AI Prompting Guide: Use action verbs ("Write," "Classify," "Summarize") and place instructions at the beginning of the prompt. Use separators (`###` or `---`) to demarcate instructions from content. Provide instructions sequentially with numbered lists rather than prose.

### 2. Directive vs. Conversational Styles

**Core finding**: Directive style (explicit instructions with clear structure) consistently outperforms conversational style for technical and production tasks. Conversational style is appropriate for exploratory tasks or when requirements are genuinely open-ended.

The Anthropic documentation introduces an important nuance for extended thinking mode: **high-level directive instructions outperform step-by-step prescriptive guidance** when the model is given space to reason. Instead of prescribing each step, instruct the model to "think deeply" and "consider multiple approaches." This is specific to contexts where the model's internal reasoning process is not constrained — it does not apply to simple task instructions.

From the DAIR.AI guide on when to be directive:
- Be direct, not clever
- Specify what you want, not what to avoid ("use 2-3 sentences" rather than "don't be too long")
- Replace vague constraints with concrete specifications

### 3. Multi-Step/Compositional Prompting

**Core finding**: Prompt chaining — breaking complex tasks into discrete, sequential prompts — dramatically improves accuracy, clarity, and debuggability compared to monolithic single prompts.

#### 3.1 Prompt Chaining

Rationale for chaining:
1. Each subtask receives the model's full attention
2. Simpler subtasks yield clearer instructions and outputs
3. Individual links can be debugged and refined independently
4. State can be passed between prompts via XML-tagged output blocks

Common chained workflow patterns (from Anthropic):
- **Multi-step analysis**: Analyze → Draft → Review
- **Content creation pipelines**: Research → Outline → Draft → Edit → Format
- **Data processing**: Extract → Transform → Analyze → Visualize
- **Decision-making**: Gather info → List options → Analyze each → Recommend
- **Verification loops**: Generate content → Review → Refine → Re-review

**Key technique**: Have Claude output results in `<section>` XML tags, then pass those tags as input to subsequent prompts. This creates clean handoffs between steps.

**Self-correction chains**: A particularly powerful pattern — chain prompts to have Claude review its own work before considering a task complete. This "catches errors and refines outputs, especially for high-stakes tasks."

**Parallelization**: For subtasks that are independent, run them as separate prompts in parallel rather than sequentially, then synthesize.

#### 3.2 Agent Skill Authoring (Anthropic Agent Skills)

For agentic contexts where skills (reusable prompt bundles) are loaded on demand, additional principles apply:

- **Conciseness is critical**: Context window is shared with conversation history and other skills. Only include context the model does not already have.
- **Progressive disclosure**: Keep the main skill file under 500 lines; split detailed content into separate files that are loaded on demand.
- **Degrees of freedom matching**: Match instruction specificity to task fragility. High-freedom instructions for tasks with many valid approaches; low-freedom (exact scripts) for fragile operations like database migrations.
- **Table of contents for long reference files**: For files exceeding 100 lines, include a table of contents so the model can identify and jump to relevant sections.
- **Gerund naming**: Name skills with gerund form ("processing-pdfs") for clarity about what the skill does.
- **Third-person descriptions**: Skill descriptions are injected into system prompts; inconsistent point-of-view degrades discovery reliability.

### 4. Chain-of-Thought and Reasoning

**Core finding**: Chain-of-thought (CoT) prompting reliably improves performance on complex reasoning tasks (math, logic, multi-factor analysis) with minimal downside for latency-tolerant use cases. The improvement is measurable and the technique has been validated through both academic research and production documentation.

#### 4.1 Evidence of Effectiveness

Wei et al. (2022) introduced CoT prompting, demonstrating that "enabling complex reasoning capabilities through intermediate reasoning steps" allows models to solve arithmetic, logic, and commonsense reasoning tasks they fail at without reasoning scaffolding. A concrete example from research: without CoT, a model answered an apple-counting problem with 11 (incorrect); with "Let's think step by step," the same model reached 10 (correct).

Anthropic's documentation shows this in financial analysis: without CoT, Claude provided a reasonable-sounding but shallow recommendation. With CoT, Claude computed exact figures for both investment scenarios, evaluated historical market volatility, and produced a rigorously justified recommendation.

#### 4.2 CoT Technique Progression (Least to Most Complex)

1. **Basic**: Append "Think step-by-step" — simple, but provides no guidance on *how* to think
2. **Guided**: Outline specific reasoning steps to follow in prose
3. **Structured**: Use XML tags (`<thinking>`, `<answer>`) to separate reasoning from final output — enables post-processing and stripping of thinking

**Power user tip from Anthropic**: Combine structured CoT with XML tags and multishot examples for "super-structured, high-performance prompts."

#### 4.3 Zero-Shot CoT

Simply appending "Let's think step by step" to a prompt — without any examples — "significantly improves performance" on complex reasoning tasks. This is the most accessible form of CoT with near-zero prompt overhead.

#### 4.4 When Not to Use CoT

- Simple, well-defined tasks (adds latency without benefit)
- Latency-critical applications where response time matters more than accuracy
- Tasks that humans would not need to think through step-by-step

#### 4.5 Extended Thinking Mode (Anthropic-specific)

For models with extended thinking capability, different prompting strategy applies:
- Start with **high-level, general instructions** rather than prescriptive step-by-step guidance
- "The model's creativity in approaching problems may exceed a human's ability to prescribe the optimal thinking process"
- Increased thinking budget improves performance on complex STEM problems, constraint optimization, and tasks requiring multiple analytical frameworks
- Ask the model to verify its own work before declaring complete

### 5. Agent/Tool Orchestration Prompting

**Core finding**: Effective tool orchestration requires precise tool descriptions for discovery, clear sequencing signals for dependent operations, parallel dispatch for independent operations, and explicit chain-of-thought to prevent premature tool invocations with inferred parameters.

#### 5.1 Tool Description Quality

Tool descriptions are the primary mechanism by which an agent selects the right tool. Best practices from Anthropic:
- Include what the tool does AND when to use it: "Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."
- Use specific trigger keywords in descriptions
- Write descriptions in third person (they are injected into system prompts)
- Use fully qualified tool names when multiple MCP servers are present (`ServerName:tool_name`)

#### 5.2 ReAct Framework (Reasoning + Acting)

Research by Yao et al. (2022) — the ReAct framework — formalizes interleaved reasoning and tool invocation. The model alternates between:
- **Thought**: Free-form reasoning to decompose questions or decide next action
- **Action**: Specific tool call with parameters
- **Observation**: Tool result that informs next reasoning step

Key advantages over CoT alone:
- Grounds reasoning in real data (reduces hallucination)
- Enables adaptive planning when observations reveal unexpected results
- Best results combine ReAct with CoT and self-consistency methods

Performance: ReAct outperforms action-only approaches on knowledge tasks (HotpotQA, Fever) and decision-making tasks (ALFWorld, WebShop).

#### 5.3 Sequential vs. Parallel Tool Use

- **Sequential**: When Tool B requires Tool A's output as input. The model should call tools one at a time; do not ask for parallel execution of dependent calls, as the model will infer (and likely hallucinate) missing parameters.
- **Parallel**: When tools are independent. Claude can output multiple `tool_use` blocks in one response. The caller must return all results in a single user message.

#### 5.4 Chain-of-Thought for Tool Selection

For models that may invoke tools prematurely (Claude Sonnet and Haiku more so than Opus), a specific CoT prefix improves behavior:

> "Before calling a tool, do some analysis. First, think about which of the provided tools is the relevant tool to answer the user's request. Second, go through each of the required parameters of the relevant tool and determine if the user has directly provided or given enough information to infer a value... If one of the values for a required parameter is missing, DO NOT invoke the function... and instead, ask the user to provide the missing parameters."

#### 5.5 Validation and Feedback Loops

For agentic skill authoring, implement feedback loops where the agent:
1. Generates an intermediate artifact (plan, mapping, draft)
2. Validates that artifact with a deterministic script or checklist
3. Fixes issues before proceeding to execution

The "plan-validate-execute" pattern catches errors before destructive or irreversible operations. Validation scripts should emit specific error messages to help the agent fix issues autonomously.

### 6. Quality Thresholds and Evaluation

**Core finding**: Quality should be specified explicitly in prompts as success criteria, and prompts should be evaluated empirically against defined rubrics — not subjectively.

#### 6.1 Specifying Quality in Prompts

Anthropic recommends establishing success criteria before prompt engineering: "A clear definition of the success criteria for your use case" and "some ways to empirically test against those criteria." This shifts quality from a vague aspiration to a testable criterion.

In multi-step chained workflows, quality can be enforced at each step via self-review prompts. Example from Anthropic: after generating a research summary, a second prompt grades it on accuracy, clarity, and completeness (A–F scale), and a third prompt refines it using the feedback. This produces objectively improved output at the cost of additional inference calls.

For agent skills, the recommended approach is **evaluation-driven development**:
1. Run Claude on representative tasks without a skill → document specific failures
2. Create evaluations testing those failures
3. Write minimal instructions to pass evaluations
4. Iterate based on observed behavior, not assumptions

#### 6.2 Output Format as Quality Signal

Specifying exact output format prevents superfluous text and forces the model to commit to a structure. Examples from Anthropic:
- "Output only the processed messages, separated by '---'"
- "List only: 1) Cause 2) Duration 3) Impacted services..."
- "Produce findings in `<findings>` tags and recommendations in `<recommendations>` tags"

Structured output in XML or JSON also enables programmatic post-processing and validation.

### 7. Anti-Patterns

**Core finding**: A consistent set of anti-patterns degrades output quality across all sources. These are failures of specificity, structure, and scope management.

| Anti-Pattern | Description | Correct Practice |
|-------------|-------------|-----------------|
| **Negative framing** | Instructing what not to do ("don't be too long") | Specify what you want ("use 2-3 sentences") |
| **Vague parameters** | Unclear constraints ("keep it short", "be professional") | Concrete specifications ("under 50 characters", "tone: direct and assertive") |
| **Monolithic prompts** | All complexity in one prompt for multi-step tasks | Chain prompts; one subtask goal per prompt |
| **Over-specification in reasoning** | Prescribing each reasoning step for extended thinking | High-level "think deeply" instruction; let the model reason freely |
| **Inconsistent terminology** | Mixing "endpoint", "URL", "route", "path" for the same concept | Choose one term and use it throughout |
| **Too many options** | Presenting multiple valid libraries/approaches | Provide a recommended default with an escape hatch for edge cases |
| **Time-sensitive content** | Including version-specific or date-dependent instructions | Use "current method" and "old patterns" sections |
| **Missing examples** | Zero-shot for structured output tasks | 3-5 diverse examples in `<examples>` tags |
| **Shallow few-shot** | Examples with incorrect or irrelevant labels | Relevant, diverse, clearly structured examples; label distribution matters |
| **Catching all exceptions** | Over-broad error handling that masks bugs | Specific exception types with targeted handling |
| **Deeply nested references** | Skill docs that chain through multiple files | Keep all references one level deep from the entry point |
| **Broad indemnification in tool descriptions** | Vague descriptions that match too many situations | Include specific trigger keywords for when to use each tool |

### 8. Prompt Calibration by Model Tier

**Core finding**: External prompt engineering literature largely treats models as a single undifferentiated target for prompts. This is a significant gap for multi-model systems like Jerry, where different agents are explicitly routed to different model tiers with meaningfully different reasoning capabilities.

#### 8.1 Model-Tier Routing in Jerry (Internal Evidence)

Jerry's agent YAML specifications (`c:/AI/jerry/skills/problem-solving/agents/`) explicitly route agents to different Claude model tiers based on task complexity:

| Agent | Model | Rationale |
|-------|-------|-----------|
| ps-researcher | opus | Complex, open-ended research requiring broad exploration |
| ps-analyst | sonnet | Balanced analysis: complex enough for Sonnet, structured enough to not require Opus |
| ps-synthesizer | sonnet | Cross-document pattern synthesis: moderate complexity |
| ps-critic | sonnet | Evaluation tasks: structured rubrics reduce reasoning demand |
| ps-reviewer | sonnet | Quality review with specific standards to apply |
| ps-architect | opus | Architectural decisions require complex multi-factor reasoning |
| ps-validator | haiku | Binary constraint verification: fast, low complexity |
| ps-reporter | haiku | Status reporting: structured data aggregation, low reasoning demand |
| ps-investigator | sonnet | Convergent root-cause drilling: structured but complex |

(Source: YAML frontmatter `model:` field in each agent spec file, e.g., `ps-architect.md` line 5: `model: opus  # Architecture requires complex reasoning`; `ps-reporter.md` line 6: `model: haiku  # Fast reporting tasks`)

#### 8.2 Implied Prompt Calibration Principles

The model-tier routing pattern implies that prompts should be calibrated differently for each tier, even when the structural patterns (XML tags, YAML frontmatter, Triple-Lens output) remain consistent:

**Opus-tier agents (ps-researcher, ps-architect)**:
- Receive high-level goal directives rather than step-by-step scripts
- Are given broader "degrees of freedom" matching (per Anthropic agent skills guidance: match instruction specificity to task fragility)
- Benefit from "think deeply" and "consider multiple approaches" language (Anthropic, "Extended Thinking Tips")
- The agent spec language reflects this: ps-architect's identity says "Evaluate options, make decisions, and document rationale with long-term implications in mind"

**Sonnet-tier agents (ps-analyst, ps-synthesizer, ps-critic, ps-reviewer, ps-investigator)**:
- Receive structured evaluation criteria and frameworks (5 Whys, FMEA, Braun & Clarke phases)
- Have more prescriptive output schemas (state schema with specific field types)
- Benefit from the CoT prefix for tool selection noted in Anthropic's tool use docs: "think about which of the provided tools is the relevant tool" — the Sonnet-tier agents are noted in Anthropic's documentation as more prone to premature tool invocation than Opus

**Haiku-tier agents (ps-validator, ps-reporter)**:
- Receive the most constrained and explicit instructions
- Have tightly defined output formats (metrics tables, health indicators, pass/fail status)
- Are not given extended thinking space; instructions are maximally concrete
- The ps-reporter model choice note (`# Fast reporting tasks`) confirms speed-over-depth prioritization

#### 8.3 Gap in External Literature

This multi-model prompt calibration strategy is a **gap in the surveyed external literature**. All five sources surveyed treat prompt engineering as targeting a single model. None of the sources discuss:
- How to calibrate instruction specificity for different model capability tiers
- Whether structural patterns (XML tags, CoT) need to scale differently for weaker vs. stronger models
- How to maintain prompt consistency across agents while varying depth of instruction

The only adjacent guidance found is Anthropic's note that Claude Sonnet and Haiku are "more likely to infer or guess" missing parameters than Opus (Source 3, Tool Use documentation, also cited in Section 5.4 of this survey), which suggests that Haiku-tier agents need more prescriptive parameter specification in their tool invocation prompts. But this is a narrow observation rather than a systematic multi-tier calibration framework.

**Research implication**: A multi-model prompt engineering framework that codifies tier-appropriate instruction patterns is not present in the external literature and may represent an original contribution opportunity for Jerry.

---

## L2: Source Evidence

### Source 1: Anthropic Prompt Engineering Documentation

**URL**: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/
**Type**: Official vendor documentation
**Sub-pages surveyed**:
- Overview: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/overview
- Be Clear and Direct: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct
- Multishot Prompting: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/multishot-prompting
- Chain of Thought: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/chain-of-thought
- XML Tags: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/use-xml-tags
- System Prompts: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/system-prompts
- Chain Prompts: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/chain-prompts
- Long Context Tips: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/long-context-tips
- Extended Thinking Tips: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips

**Key quotes**:

> "Think of it as a brilliant but very new employee (with amnesia) who needs explicit instructions. Like any new employee, Claude does not have context on your norms, styles, guidelines, or preferred ways of working. The more precisely you explain what you want, the better Claude's response will be."
> — Anthropic, "Be Clear and Direct"

> "When faced with complex tasks like research, analysis, or problem-solving, giving Claude space to think can dramatically improve its performance... Stepping through problems reduces errors, especially in math, logic, analysis, or generally complex tasks."
> — Anthropic, "Let Claude Think (Chain of Thought)"

> "XML tags can be a game-changer. They help Claude parse your prompts more accurately, leading to higher-quality outputs."
> — Anthropic, "Use XML Tags"

> "Each link in the chain gets Claude's full attention!"
> — Anthropic, "Chain Complex Prompts"

> "Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs."
> — Anthropic, "Long Context Tips" (note: this quantified improvement applies to long-context scenarios where documents are placed first and the query follows)

> "Claude often performs better with high level instructions to just think deeply about a task rather than step-by-step prescriptive guidance. The model's creativity in approaching problems may exceed a human's ability to prescribe the optimal thinking process."
> — Anthropic, "Extended Thinking Tips"

> "Always have Claude output its thinking. Without outputting its thought process, no thinking occurs!"
> — Anthropic, "Let Claude Think"

### Source 2: Anthropic Agent Skills Best Practices

**URL**: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
**Type**: Official vendor documentation (agent-specific)

**Key quotes**:

> "The context window is a public good. Your Skill shares the context window with everything else Claude needs to know, including the system prompt, conversation history, other Skills' metadata, and your actual request."
> — Anthropic, "Skill Authoring Best Practices"

> "For reference files that exceed 100 lines, it's important to include a table of contents at the top. This structure helps Claude understand the full scope of information available... A table of contents allows Claude to efficiently navigate and jump to specific sections as required."
> — Anthropic, "Skill Authoring Best Practices"

> "Create evaluations BEFORE writing extensive documentation. This ensures your Skill solves real problems rather than documenting imagined ones."
> — Anthropic, "Skill Authoring Best Practices"

> "Claude A helps you design and refine instructions, while Claude B tests them in real tasks. This works because Claude models understand both how to write effective agent instructions and what information agents need."
> — Anthropic, "Skill Authoring Best Practices" (on iterative skill development using two Claude instances)

> "Use pdfplumber for text extraction. [vs.] PDF (Portable Document Format) files are a common file format..." [concise wins]
> — Anthropic, "Skill Authoring Best Practices" (demonstrating that concise, assumption-respecting instructions outperform verbose explanations)

### Source 3: Anthropic Tool Use Documentation

**URL**: https://platform.claude.com/docs/en/docs/build-with-claude/tool-use/overview
**Type**: Official vendor documentation (tool use specific)

**Key quotes**:

> "Answer the user's request using relevant tools (if they are available). Before calling a tool, do some analysis. First, think about which of the provided tools is the relevant tool to answer the user's request. Second, go through each of the required parameters of the relevant tool and determine if the user has directly provided or given enough information to infer a value... If one of the values for a required parameter is missing, DO NOT invoke the function (not even with fillers for the missing params) and instead, ask the user to provide the missing parameters."
> — Anthropic, "Tool Use: Chain of Thought Prompt" (recommended CoT prefix for tool selection)

> "When Claude makes parallel tool calls, you must return all tool results in a single user message, with each result in its own tool_result block."
> — Anthropic, "Tool Use Overview"

### Source 4: DAIR.AI Prompting Guide (promptingguide.ai)

**URL base**: https://www.promptingguide.ai
**Sub-pages surveyed**:
- Chain-of-Thought: https://www.promptingguide.ai/techniques/cot
- Few-Shot Prompting: https://www.promptingguide.ai/techniques/fewshot
- General Tips: https://www.promptingguide.ai/introduction/tips
- ReAct: https://www.promptingguide.ai/techniques/react

**Type**: Independent research and documentation aggregator

**Key quotes**:

> "Chain-of-Thought (CoT) prompting enables complex reasoning capabilities through intermediate reasoning steps."
> — DAIR.AI, citing Wei et al. (2022)

> "Simply adding 'Let's think step by step' to prompts significantly improves performance, even without examples."
> — DAIR.AI, on Zero-Shot CoT

> "The label space and the distribution of the input text specified by the demonstrations are both important."
> — DAIR.AI, citing Min et al. (2022) on few-shot prompting

> "Few-shot prompting fails reliably on complex reasoning tasks requiring multiple logical steps."
> — DAIR.AI, identifying the primary limitation of few-shot without CoT

> "ReAct allows models to generate both reasoning traces and task-specific actions in an interleaved manner. Generating reasoning traces allow the model to induce, track, and update action plans, and even handle exceptions. The action step allows to interface with and gather information from external sources."
> — DAIR.AI, summarizing Yao et al. (2022) on ReAct

> "ReAct outperforms several baselines on knowledge tasks (HotpotQA, Fever) and decision-making (ALFWorld, WebShop). Best results combine ReAct with CoT and self-consistency methods."
> — DAIR.AI, on ReAct performance evidence

> "Don't instruct what NOT to do; frame requirements positively."
> — DAIR.AI, General Tips

> "The more descriptive and detailed the prompt is, the better the results."
> — DAIR.AI, General Tips

**Primary academic references cited by DAIR.AI**:
- Wei, J., et al. (2022). "Chain-of-thought prompting elicits reasoning in large language models." NeurIPS 2022.
- Min, S., et al. (2022). "Rethinking the role of demonstrations: What makes in-context learning work?" EMNLP 2022.
- Zhang, Z., et al. (2022). "Automatic Chain of Thought Prompting in Large Language Models." ICLR 2023.
- Yao, S., et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models." ICLR 2023.
- Kaplan, J., et al. (2020). "Scaling Laws for Neural Language Models." arXiv:2001.08361.

### Source 5: OpenAI Best Practices for Prompt Engineering

**URL**: https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api
**Type**: Indirect via DAIR.AI (not official vendor documentation accessed directly)
**Note**: Direct HTTP fetch was blocked (403); this source was not accessed directly. Findings attributed to OpenAI in this survey are mediated through DAIR.AI's documentation of their published guidance. The DAIR.AI Prompting Guide (Source 4) extensively cross-references and summarizes OpenAI's publicly available best practices; that intermediary is the actual source of these findings. Any citation of OpenAI principles in this document should be understood as "OpenAI as documented by DAIR.AI," not as a direct primary source read.

**Key principles documented by OpenAI (as referenced through DAIR.AI, not directly from OpenAI)**:
- Use the latest models when possible
- Put instructions at the beginning of the prompt; use `###` or `"""` to separate instruction from context
- Be specific, descriptive, and as detailed as possible about desired context, outcome, length, format, and style
- Articulate the desired output format via examples
- Start with zero-shot, then few-shot, then fine-tune — only escalate to fine-tuning if simpler approaches fail
- Reduce "fluffy" and imprecise descriptions
- Say what to do instead of what not to do

---

## Research Gaps and Limitations

1. **No direct OpenAI documentation fetch (Source 5 is indirect)**: The OpenAI guide at help.openai.com returned 403. Source 5 is therefore classified as "indirect via DAIR.AI" — not official vendor documentation. The OpenAI principles cited in this survey are mediated through DAIR.AI's documentation of OpenAI's published guidance, and should be treated as secondary-source characterizations. They are corroborated by cross-consistency with Anthropic's guidance, but direct verification was not possible.

2. **Model-specific variation**: Several findings note model-dependent behavior. Claude Opus is more likely to ask for missing parameters before tool invocation; Claude Sonnet and Haiku are more likely to infer or guess. Strategies that work optimally for one model tier may need adjustment for others.

3. **Academic vs. applied gap**: Academic CoT research (Wei et al., Min et al.) was conducted on earlier model generations. The specific magnitude of improvement may differ on current frontier models, though the direction of effect (CoT helps for complex reasoning) is consistent across all sources.

4. **Context window economics**: The trade-off between prompt thoroughness and token cost is not quantified in most sources. The Anthropic agent skills documentation provides qualitative guidance (concise is better) but no empirical benchmarks on optimal prompt length for a given task type.

---

*Survey completed: 2026-02-18*
*Revised: 2026-02-18 (v1.1.0 — ps-critic revision actions: Source 5 reclassified as indirect via DAIR.AI; Section 8 Prompt Calibration by Model Tier added)*
*Sources: 5 distinct sources (Anthropic Prompt Engineering Docs, Anthropic Agent Skills Best Practices, Anthropic Tool Use Docs, DAIR.AI Prompting Guide, OpenAI Prompt Engineering Guide [indirect via DAIR.AI])*
