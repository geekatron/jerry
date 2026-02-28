# Context7 Library Documentation Survey: Negative Prompting Patterns

> Systematic survey of 6 library/framework documentation sources for negative prompting patterns, guidance, examples, and recommendations.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Key findings, hypothesis verdict, and coverage matrix |
| [Hypothesis Verdict](#hypothesis-verdict) | Primary verdict on PROJ-014 hypothesis |
| [Key Findings](#key-findings) | Six key findings with source attribution |
| [Coverage Matrix](#coverage-matrix) | Per-library coverage summary (bounded to 6 sources) |
| [L1: Library-by-Library Findings](#l1-library-by-library-findings) | Detailed per-library results |
| [L2: Cross-Library Analysis](#l2-cross-library-analysis) | Patterns, gaps, academic evidence, and strategic implications |
| [Pattern Convergence](#pattern-convergence) | Four convergent patterns (NP-001 through NP-004) |
| [Pattern Divergence](#pattern-divergence) | Vendor recommendation vs. practice, OpenAI evolution, DSPy paradigm |
| [Academic Research Findings](#academic-research-findings) | Empirical evidence from Tripathi et al. and Young et al. |
| [Coverage Gaps](#coverage-gaps) | Four identified coverage gaps |
| [Negative Instruction Type Taxonomy (Preliminary)](#negative-instruction-type-taxonomy-preliminary) | Skeleton taxonomy of 5 negative instruction types |
| [Implications for PROJ-014 Hypothesis](#implications-for-proj-014-hypothesis) | Strategic implications and revised hypothesis |
| [Phase 2 Task Mapping](#phase-2-task-mapping) | Actionable Phase 2 task table with experimental design parameters |
| [Methodology](#methodology) | Source selection rationale, tool limitations, query log, and reproducibility |
| [References](#references) | Complete citation list with authority tiers and access dates |
| [PS Integration](#ps-integration) | Problem-solving context and downstream agent guidance |

---

## L0: Executive Summary

This survey systematically examined 6 major library/framework documentation sources for explicit guidance on negative prompting patterns (telling LLMs what NOT to do). The findings directly inform the PROJ-014 hypothesis that "negative unambiguous prompting reduces hallucination by 60% and achieves better results than explicit positive prompting."

### Hypothesis Verdict

**The PROJ-014 hypothesis is NOT SUPPORTED by any surveyed source.** No vendor documentation, framework guide, or academic paper surveyed provides quantitative evidence for a 60% hallucination reduction through negative prompting. On the contrary:

- Both Anthropic and OpenAI explicitly recommend positive framing over negative instructions as the default approach.
- The only empirical research found (Tripathi et al., 2025; Young et al., 2025) measures instruction-following compliance broadly but does not isolate negative-vs-positive framing as a variable or report a 60% improvement for any prompting technique.
- The surveyed evidence suggests that the negative-vs-positive distinction is less important than instruction specificity, pairing prohibitions with positive alternatives, and structural enforcement mechanisms.

A more defensible hypothesis, informed by this survey, would be: "Specific, contextually justified constraints (whether positive or negative) combined with structural enforcement mechanisms reduce hallucination more effectively than unstructured instructions of either framing." This revised hypothesis would be **supported** if: (a) specific, contextually justified constraints show >= 20% higher compliance rates than unstructured instructions across 3+ model families, and (b) the effect is independent of whether the constraint is framed positively or negatively (framing accounts for < 15% of variance in compliance rates). The 15% variance threshold corresponds to Cohen's f-squared of approximately 0.18 (medium effect size per Cohen, 1988), meaning framing would need to explain a practically significant proportion of compliance variance to warrant framework-level changes. Power analysis: detecting this effect size with alpha = 0.05 and power = 0.80 requires approximately 55 observations per framing condition, which the proposed 500-evaluation protocol exceeds. It would be **refuted** if framing (positive vs. negative) accounts for > 15% of variance in compliance rates, indicating that the positive/negative distinction does matter independently of specificity and structural enforcement. This revised hypothesis should serve as the starting point for Phase 2 analysis.

> **Experimental scope note:** The structural enforcement dimension (programmatic constraints via DSPy assertions, LangChain output parsers, etc.) is documented as a complementary approach in the L2 cross-library analysis but is excluded from the experimental protocol in [Phase 2 Task Mapping](#phase-2-task-mapping) because it operates at a different abstraction level than linguistic framing. The experimental design tests *linguistic framing* (negative vs. positive instruction wording) as the independent variable; structural enforcement is a separate research question recommended for future work. The "unstructured instructions" baseline referred to in the success criteria denotes instructions that convey the same intent without explicit constraint language -- e.g., "write a professional response" rather than "never use jargon" (negative) or "use formal language only" (positive).

### Key Findings

> **Important qualifier:** All findings below reflect vendor-published documentation and observed documentation patterns. Production model behavior may differ from documented guidance, and the gap between documented recommendations and observed documentation practice is itself a significant finding (see Key Finding 2). Per-library source-specific limitations are detailed in the L1 coverage assessments.

1. **Both Anthropic and OpenAI explicitly recommend positive framing over negative instructions.** Anthropic's official Claude documentation states: "Tell Claude what to do instead of what not to do" and provides the canonical example: instead of "Do not use markdown in your response," use "Your response should be composed of smoothly flowing prose paragraphs." OpenAI's Prompt Engineering Guide similarly advises (sourced via Ref #15, MEDIUM authority -- promptingguide.ai citing OpenAI; corroborated by GPT-4.1 through GPT-5.2 cookbook guides, Ref #4-#7; primary platform docs returned 403, Ref #3): "avoid saying what not to do but say what to do instead." (Sources: Ref #1, #3, #15)

2. **However, both vendors actively USE negative constraints in their own prompts and documentation.** Anthropic's Claude prompting best practices include numerous "DO NOT" instructions (e.g., `<do_not_act_before_instructions>` XML tags). OpenAI's GPT-5.2 cookbook guide uses explicit prohibitions like "Do NOT invent colors, shadows, tokens, animations, or new UI elements" and "Never fabricate exact figures." This creates a documented tension between the stated recommendation (prefer positive) and actual practice (frequent use of negative constraints). However, this tension may have multiple explanations -- see [Vendor Recommendation vs. Vendor Practice](#1-vendor-recommendation-vs-vendor-practice) in L2 for analysis. (Sources: Ref #1, #2, #7)

3. **No vendor documentation provides quantitative evidence for the 60% hallucination reduction claim.** None of the 6 surveyed sources cite controlled experiments comparing negative vs. positive prompting effectiveness with measurable hallucination metrics. The guidance across all sources is prescriptive, not evidence-based. (Sources: Survey-wide null finding)

4. **Framework libraries (LangChain, LlamaIndex, DSPy) are largely silent on negative vs. positive prompting as a design consideration.** These frameworks provide constraint enforcement mechanisms (output parsers, assertions, guardrails) but do not prescribe whether constraints should be framed negatively or positively. LlamaIndex's own default prompts heavily use negative framing ("Never query for all the columns," "Do NOT fill in the vector values directly"). (Sources: Ref #8, #9, #10, #11, #12)

5. **DSPy establishes a third paradigm: programmatic assertion enforcement renders the negative/positive framing question architecturally moot.** DSPy's `dspy.Assert` and `dspy.Suggest` enforce constraints at the program level rather than through linguistic framing. Notably, DSPy's backtracking mechanism automatically injects negative feedback ("what went wrong" and the failing output) into retry prompts -- demonstrating that negative information is a built-in component of effective constraint enforcement, even within a system that replaces manual prompt engineering. (Sources: Ref #12, #13, #14)

6. **The surveyed evidence converges on a hybrid approach**: use negative constraints for hard safety boundaries and prohibitions, but pair them with positive alternatives that specify desired behavior. This convergence is documented across Anthropic (Ref #1), OpenAI's GPT-5.x guides (Ref #6, #7), and cross-framework prompt engineering guides (Ref #15, #17, #20). Standalone negative instructions without positive alternatives are consistently identified as less effective across all sources that address the topic.

### Coverage Matrix

| Library/Framework | Explicit Negative Prompting Guidance | Recommends Positive Over Negative | Uses Negative Instructions Itself | Quantitative Evidence |
|---|---|---|---|---|
| Anthropic Claude | **Yes** -- direct guidance with examples (Ref #1, #2) | **Yes** | **Yes** (tension documented) | **No** |
| OpenAI GPT | **Partial** -- cookbook guides provide guidance with examples; platform docs returned 403 (Ref #4, #5, #6, #7) | **Yes** | **Yes** (tension documented) | **No** |
| LangChain | **No** -- silent on framing; provides structural constraint mechanisms (Ref #8, #9) | N/A | Indirect (via guardrails -- see L1 for code examples) | **No** |
| LlamaIndex | **No** -- silent on guidance; default prompts use negative framing (Ref #10, #11) | N/A | **Yes** (default prompts) | **No** |
| DSPy | **No** -- transcends the question via programmatic constraints (Ref #12, #13, #14) | N/A | Indirect (backtracking injects negative feedback) | **No** |
| Prompt Engineering Guides | **Yes** -- from OpenAI-derived guidance; authority varies by source (Ref #15 MEDIUM, #16 LOW, #17 LOW, #20 MEDIUM) | **Yes** | Mixed | **No** |

> **Scope caveat:** This matrix reflects only the 6 surveyed sources. The "No" entries under Quantitative Evidence indicate that no quantitative data was found *within these 6 sources* -- not that no quantitative evidence exists globally. Google Gemini, Meta LLaMA, Cohere, and other provider documentation were not surveyed (see [Source Selection Rationale](#source-selection-rationale) in Methodology for exclusion reasoning). The null finding on quantitative evidence is bounded to this survey's scope.

---

## L1: Library-by-Library Findings

### 1. Anthropic Claude Documentation

**Source:** Anthropic official documentation -- [Claude Prompting Best Practices](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) (Accessed: 2026-02-27)

**Source Authority:** HIGH (official vendor documentation)

**Queries Executed:**
- Query 1: "negative prompting patterns and what not to do instructions" -- via WebSearch (Anthropic prompt engineering negative prompting) -> Retrieved full best practices page
- Query 2: "prohibition constraints and avoid instructions in prompts" -- via WebFetch of official documentation page
- Query 3: "hallucination reduction through prompt constraints" -- via WebSearch (Anthropic hallucination reduction constraints)
- Fallback: Context7 MCP tools were configured but not available as callable functions in this session; WebSearch/WebFetch used per MCP error handling protocol (see [Tool Availability and Coverage Risk](#tool-availability-and-coverage-risk)).

**Documented Negative Prompting Patterns:**

Anthropic provides the most explicit guidance of any surveyed source. From the official Claude prompting best practices documentation:

**Pattern 1: Positive Reframing (Primary Recommendation)**

Direct quote from the "Control the format of responses" section:

> "1. Tell Claude what to do instead of what not to do
> - Instead of: 'Do not use markdown in your response'
> - Try: 'Your response should be composed of smoothly flowing prose paragraphs.'"

**Pattern 2: Contextual Negative Instructions (Secondary Pattern)**

Despite recommending positive framing, Anthropic's own documentation uses negative instructions extensively when context justifies them:

> "NEVER use ellipses" is presented as a "Less effective" example. The "More effective" version adds context:
> "Your response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them."

This demonstrates Anthropic's view that negative instructions are more effective when accompanied by a reason (the "why").

**Pattern 3: XML-Wrapped Negative Constraints (Practical Pattern)**

The documentation contains multiple examples of XML-tagged negative constraints used in practice:

```xml
<do_not_act_before_instructions>
Do not jump into implementation or changes files unless clearly instructed
to make changes. When the user's intent is ambiguous, default to providing
information, doing research, and providing recommendations rather than
taking action.
</do_not_act_before_instructions>
```

```xml
<avoid_excessive_markdown_and_bullet_points>
...DO NOT use ordered lists (1. ...) or unordered lists (*) unless:
a) you're presenting truly discrete items where a list format is the
best option, or b) the user explicitly requests a list or ranking...
NEVER output a series of overly short bullet points.
</avoid_excessive_markdown_and_bullet_points>
```

**Pattern 4: Hallucination Prevention via Negative Instruction**

The documentation includes a dedicated anti-hallucination prompt using negative framing:

```xml
<investigate_before_answering>
Never speculate about code you have not opened. If the user references
a specific file, you MUST read the file before answering. Make sure to
investigate and read relevant files BEFORE answering questions about the
codebase. Never make any claims about code before investigating unless
you are certain of the correct answer - give grounded and
hallucination-free answers.
</investigate_before_answering>
```

**Explicit Guidance on Negative vs Positive:**

Anthropic explicitly recommends positive framing as the primary approach, but their own system prompts and recommended patterns demonstrate that negative framing is used extensively in practice -- particularly for:
- Hard safety boundaries
- Behavioral constraints in agentic systems
- Anti-hallucination guardrails
- Formatting prohibitions

**Coverage Assessment:** **Explicit coverage** -- Anthropic provides the most detailed guidance of any surveyed source, including direct comparison examples and recommended reframing patterns. This assessment covers documented guidance and observed usage patterns in official documentation only; production deployment practices may differ.

---

### 2. OpenAI GPT Documentation

**Source:** OpenAI documentation -- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering) (403 on direct fetch; Accessed: 2026-02-27), [GPT-4.1 Prompting Guide](https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide) (Accessed: 2026-02-27), [GPT-5 Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide) (Accessed: 2026-02-27), [GPT-5.1 Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-1_prompting_guide/) (Accessed: 2026-02-27), [GPT-5.2 Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide) (Accessed: 2026-02-27)

**Source Authority:** HIGH (official vendor cookbook guides). **Note:** The primary platform documentation at `platform.openai.com/docs/guides/prompt-engineering` returned HTTP 403 Forbidden on direct fetch. The canonical "say what to do instead of what not to do" recommendation was confirmed via promptingguide.ai (Ref #15, MEDIUM authority), which attributes it to OpenAI. The cookbook guides hosted at `developers.openai.com/cookbook/` are official OpenAI-authored content but represent developer examples rather than the primary platform guidance. This distinction is reflected in the Coverage Matrix marking of "Partial."

**Queries Executed:**
- Query 4: "negative instructions prohibition constraints best practices" -- via WebSearch (OpenAI GPT prompt engineering negative instructions) -> multiple prompting guides retrieved
- Query 5: "positive vs negative framing in prompts" -- via WebFetch of GPT-4.1, GPT-5, GPT-5.1, GPT-5.2 prompting guides
- Query 6: "hallucination reduction through constraints" -- via WebSearch

**Documented Negative Prompting Patterns:**

**Pattern 1: The Canonical Negative-to-Positive Example (attributed to OpenAI via promptingguide.ai)**

OpenAI's foundational Prompt Engineering Guide contains the widely-cited recommendation (sourced via promptingguide.ai, Ref #15, which attributes to OpenAI):

> "Another common tip when designing prompts is to avoid saying what not to do but say what to do instead. This encourages more specificity and focuses on the details that lead to good responses from the model."

The accompanying example shows a movie recommendation agent that was instructed "DO NOT ASK FOR INTERESTS. DO NOT ASK FOR PERSONAL INFORMATION" but proceeded to ask exactly those questions -- demonstrating the failure mode of negative-only instructions.

**Pattern 2: Negative Instructions as Guardrails (GPT-4.1 Cookbook Guide)**

The GPT-4.1 guide documents a critical failure mode with mandatory constraints:

> "Instructing a model to always follow a specific behavior can occasionally induce adverse effects. For instance, if told 'you must call a tool before responding to the user,' models may hallucinate tool inputs or call the tool with null values if they do not have enough information."

The recommended mitigation is a conditional positive alternative:

> "Adding 'if you don't have enough information to call the tool, ask the user for the information you need' should mitigate this."

**Pattern 3: Contradictory Negative Instructions (GPT-5 Cookbook Guide)**

The GPT-5 guide provides an adversarial healthcare scheduling example showing how conflicting negative instructions cause failures:

> "'Never schedule an appointment without explicit patient consent' directly conflicts with 'auto-assign the earliest same-day slot without contacting the patient'"

Resolution: restate instructions positively, e.g., "auto-assign the earliest same-day slot after informing the patient of your actions."

**Pattern 4: Negative Constraints With Positive Alternatives (GPT-5.1/5.2 Cookbook Guides)**

The later guides show evolution toward paired negative-positive patterns:

From GPT-5.1:
> "Do NOT guess a reservation time or name -- ask for whichever detail is missing."

From GPT-5.2:
> "Do NOT invent colors, shadows, tokens, animations, or new UI elements, unless requested or necessary to the requirements."
> "Never fabricate exact figures, line numbers, or external references when uncertain."

The GPT-5.2 guide emphasizes that "GPT-5.2 requires explicit instructions" and that "poorly-constructed prompts containing contradictory or vague instructions can be more damaging to GPT-5.2 than to other models."

**Explicit Guidance on Negative vs Positive:**

OpenAI's guidance has evolved across model generations:
- **Original guide (GPT-3.5/4 era):** Strong recommendation to avoid negative instructions entirely. "Say what to do, not what not to do." (Confirmed via Ref #15; primary platform docs inaccessible)
- **GPT-4.1 cookbook guide:** Acknowledgment that mandatory constraints can backfire; recommends conditional escape clauses.
- **GPT-5/5.1 cookbook guides:** Negative constraints used actively but always paired with positive alternatives.
- **GPT-5.2 cookbook guide:** Explicit negative constraints recommended for scope control ("Do NOT invent..."), but the overall philosophy remains "steerable, instruction-following behavior through clear positive direction."

**Coverage Assessment:** **Partial coverage** -- OpenAI's cookbook guides provide detailed, model-generation-specific guidance with significant evolution from "never use negatives" to "use negatives strategically with positive alternatives." However, the primary platform documentation was inaccessible (403), so this assessment is based on cookbook guides and secondary attribution. This assessment covers documented guidance and observed usage patterns in official documentation only; production deployment practices may differ.

---

### 3. LangChain Framework Documentation

**Source:** [LangChain official documentation](https://docs.langchain.com/) (Accessed: 2026-02-27), [LangChain Reference](https://reference.langchain.com/python/langchain-core/prompts) (Accessed: 2026-02-27), [LangChain Guardrails](https://docs.langchain.com/oss/python/langchain/guardrails) (Accessed: 2026-02-27)

**Source Authority:** HIGH (official framework documentation)

**Queries Executed:**
- Query 7: "negative prompting patterns constraints prohibition" -- via WebSearch (LangChain prompt templates negative prompting) -> no specific coverage found
- Query 8: "system message constraints negative prompting prohibition patterns output parser" -- via WebSearch -> output parser constraint mechanisms found
- Query 9: "guardrails constraint prompt patterns negative instructions" -- via WebSearch -> guardrail patterns found
- Query 10 (Iteration 2): "LangChain LCEL prompt composition negative constraints positive framing guidance 2025 2026" -- via WebSearch -> LCEL documentation found; no negative/positive framing guidance
- Query 11 (Iteration 2): "LangChain guardrails NeMo input validation example code" -- via WebFetch of guardrails documentation page -> code examples extracted
- Fallback: Context7 MCP tools were not available as callable functions (see [Tool Availability and Coverage Risk](#tool-availability-and-coverage-risk)).

**Documented Negative Prompting Patterns:**

LangChain documentation does **not** contain explicit guidance on negative vs. positive prompting as a design philosophy. The framework is agnostic to prompt framing -- it provides templating and constraint enforcement mechanisms without prescribing how constraints should be linguistically framed. Five queries (3 in iteration 1, 2 additional in iteration 2 targeting LCEL prompt composition and guardrails code examples) confirmed this assessment.

**Constraint Enforcement Mechanisms (Structural, Not Linguistic):**

LangChain provides several structural constraint mechanisms that operate independently of negative vs. positive framing:

1. **OutputFixingParser** -- When output violates constraints, it retries with an error message: "check whether completion satisfies constraints given in instructions... retry with an answer that satisfies the constraints." This is a structural pattern that works regardless of whether the constraint was stated negatively or positively.

2. **StructuredOutputParser** -- Forces compliance to a schema. This bypasses the negative/positive framing question entirely by making constraints structural rather than linguistic.

3. **PydanticOutputParser** -- Enforces type constraints via Python type system. Again, structural enforcement that is orthogonal to prompt framing.

4. **Guardrails Integration (Code Examples from LangChain Guardrails Docs)**

LangChain's guardrails documentation demonstrates constraint enforcement through programmatic middleware. These examples illustrate how structural constraints relate to negative/positive framing:

**Negative constraint (blocking):** The `ContentFilterMiddleware` uses keyword blocking -- a purely negative constraint pattern:
```python
class ContentFilterMiddleware(AgentMiddleware):
    def __init__(self, banned_keywords: list[str]):
        self.banned_keywords = [kw.lower() for kw in banned_keywords]

    @hook_config(can_jump_to=["end"])
    def before_agent(self, state: AgentState, runtime: Runtime):
        content = state["messages"][0].content.lower()
        for keyword in self.banned_keywords:
            if keyword in content:
                return {
                    "messages": [{"role": "assistant",
                        "content": "I cannot process requests with inappropriate content."}],
                    "jump_to": "end"
                }
```
This is structurally equivalent to a negative instruction ("do NOT process requests containing these keywords") but enforced programmatically rather than linguistically.

**Positive constraint (transformation):** The `PIIMiddleware` provides positive alternatives to blocking:
```python
PIIMiddleware("email", strategy="redact", apply_to_input=True),
PIIMiddleware("credit_card", strategy="mask", apply_to_input=True),
```
The `strategy` parameter offers `"redact"`, `"mask"`, and `"hash"` -- positive transformations rather than outright prohibition.

**Safety evaluation (binary classification prompt):** The `SafetyGuardrailMiddleware` uses an LLM prompt with constrained output:
```python
safety_prompt = f"""Evaluate if this response is safe.
Respond with only 'SAFE' or 'UNSAFE'. Response: {last_message.content}"""
```
This demonstrates binary classification prompting with a constrained output format -- neither purely positive nor negative, but structurally constrained.

These patterns demonstrate that LangChain's guardrails operate at the structural layer, replacing linguistic framing (positive or negative) with programmatic enforcement. The framework does not prescribe whether the *human-authored* system prompt should use positive or negative framing -- that remains a user decision.

**Explicit Guidance on Negative vs Positive:**

None. LangChain is silent on this topic as a prompt engineering consideration. The `system` role in ChatPromptTemplate is described as setting "the AI's behavior, personality, or constraints" -- but no guidance is provided on whether those constraints should be phrased as prohibitions or as positive directives. The LCEL documentation focuses on chain composition mechanics, not prompt framing philosophy.

**Coverage Assessment:** **Silent on framing guidance, but provides structural alternatives** -- LangChain does not address negative vs. positive prompting. The framework provides structural constraint mechanisms (parsers, guardrails, middleware) that are orthogonal to linguistic framing. Five queries across two iterations confirmed this assessment. This assessment is based on publicly available documentation and default prompt templates; internal development practices are not assessed.

---

### 4. LlamaIndex Documentation

**Source:** [LlamaIndex official documentation](https://developers.llamaindex.ai/) (Accessed: 2026-02-27), [LlamaIndex default prompts source code](https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/prompts/default_prompts.py) (Accessed: 2026-02-27)

**Source Authority:** HIGH (official framework documentation and source code). Note: Reference #11 cites framework source code rather than end-user documentation. Source code is a HIGH-authority indicator of actual framework behavior (what the framework does) but not equivalent to documentation guidance (what the framework recommends users do).

**Queries Executed:**
- Query 12: "negative prompting patterns constraints" -- via WebSearch (LlamaIndex prompt engineering negative prompting) -> no specific coverage found
- Query 13: "system prompt templates constraints negative instructions" -- via WebSearch -> prompt template documentation found
- Query 14: "default prompts source code for negative instructions" -- via WebFetch of GitHub source code -> multiple negative instruction patterns found

**Documented Negative Prompting Patterns:**

LlamaIndex's documentation does **not** contain explicit guidance on negative vs. positive prompting. However, an examination of the framework's own default prompt templates reveals extensive use of negative framing:

**Pattern 1: Query Constraint Prompts (Negative Framing)**

From `DEFAULT_QUERY_PROMPT`:
> "Using only the choices above and not prior knowledge, return the choice..."

The phrase "not prior knowledge" is a negative constraint -- the positive alternative would be "Using exclusively the choices above, return the choice..."

**Pattern 2: SQL Generation Prompts (Multiple Negatives)**

From `DEFAULT_TEXT_TO_SQL`:
> "Never query for all the columns from a specific table"
> "Be careful to not query for columns that do not exist"

These are pure negative instructions without positive alternatives.

**Pattern 3: Vector Search Prompts (Strong Negation)**

From `DEFAULT_TEXT_TO_SQL_PGVECTOR`:
> "Do NOT fill in the vector values directly, but rather specify a `[query_vector]` placeholder"

This is a paired negative-positive pattern (prohibition + alternative).

**Pattern 4: Schema Extraction (Conditional Negative)**

From `DEFAULT_SCHEMA_EXTRACT`:
> "If a field is not present in the text, don't include it in the output."

Conditional negative instruction.

**Pattern 5: Ranking Prompts (Restrictive)**

From `RANKGPT_RERANK_PROMPT`:
> "Only response the ranking results, do not say any word or explain."

Combined positive constraint ("only") with negative prohibition ("do not").

**Explicit Guidance on Negative vs Positive:**

None. LlamaIndex provides no documentation guidance on this topic, but its own default prompts predominantly use negative framing -- suggesting the framework authors did not consider positive reframing as a priority for their internal templates.

**Coverage Assessment:** **Silent on guidance, but active user of negative framing** -- LlamaIndex does not prescribe negative vs. positive patterns, but its own default prompts use negative instructions extensively. This assessment is based on publicly available documentation and default prompt templates; internal development practices are not assessed.

---

### 5. DSPy Documentation

**Source:** [DSPy official documentation](https://dspy.ai/) (Accessed: 2026-02-27), [DSPy Assertions documentation](https://dspy.ai/learn/programming/7-assertions/) (Accessed: 2026-02-27), [DSPy Assertions paper](https://arxiv.org/html/2312.13382v1) (Accessed: 2026-02-27)

**Source Authority:** HIGH (official framework documentation and peer-reviewed paper)

**Queries Executed:**
- Query 15: "prompt optimization constraints negative prompting patterns" -- via WebSearch (DSPy prompt optimization constraints) -> optimizer documentation found
- Query 16: "assertions constraints guardrails dspy.Assert dspy.Suggest" -- via WebSearch (DSPy assertions constraints guardrails) -> assertions documentation found
- Query 17: "constraint-based optimization negative constraints prohibition patterns" -- via WebFetch of DSPy optimizers page -> no negative prompting coverage found
- Query 18: "assertions as computational constraints" -- via WebFetch of DSPy assertions page -> detailed assertion mechanism found
- Query 19 (Iteration 2): "DSPy backtracking assertion example concrete negative feedback" -- via WebSearch + WebFetch -> concrete backtracking examples extracted

**Documented Negative Prompting Patterns:**

DSPy takes a fundamentally different approach to the negative/positive prompting question. Rather than relying on linguistic instructions to the model, DSPy replaces manual prompt engineering with programmatic constraint enforcement.

**Pattern 1: dspy.Assert (Hard Constraints)**

From the DSPy Assertions documentation:
> "Initiates retry upon failure, dynamically adjusting the pipeline's execution."

`dspy.Assert` enforces constraints programmatically. When a constraint fails, the system:
1. Captures the violating output
2. Appends a user-defined feedback message explaining what went wrong
3. Modifies the prompt signature to include the past failure
4. Retries the module

This is architecturally different from prompt-level negative instructions -- the constraint is enforced at the program level, not through linguistic framing in the prompt.

**Pattern 2: dspy.Suggest (Soft Constraints)**

> "A softer alternative offering self-refinement through retries without enforcing hard stops."

`dspy.Suggest` operates like `dspy.Assert` but continues execution after max retries, logging failures rather than halting.

**Pattern 3: Constraint Validation Functions (Code-Level Negation)**

DSPy constraints are expressed as Python validation functions, which naturally use both positive and negative logic:

```python
# Negative constraint (what NOT to produce)
def validate_query_distinction_local(previous_queries, query):
    if dspy.evaluate.answer_exact_match_str(query, previous_queries, frac=0.8):
        return False  # Reject if too similar to previous queries
    return True
```

**Pattern 4: Dynamic Signature Modification (Backtracking with Negative Feedback)**

From the documentation:
> "Dynamic Signature Modification: internally modifying your DSPy program's Signature by adding the following fields: Past Output... [and] Instruction: your user-defined feedback message on what went wrong."

This is a key finding: DSPy's assertion system effectively implements negative prompting at the system level -- when a constraint fails, the system automatically adds "what went wrong" (negative) information to the next prompt iteration. This is structurally equivalent to negative prompting, but implemented programmatically rather than manually.

**Concrete Backtracking Example (from DSPy Assertions documentation):**

When a `dspy.Suggest` assertion fires for query length:

```python
dspy.Suggest(
    len(query) <= 100,
    "Query should be short and less than 100 characters",
    target_module=self.generate_query
)
```

If the generated query exceeds 100 characters, the backtracking mechanism injects negative feedback into the retry prompt:

```
Past Query: [the original output that failed validation]
Instructions: Query should be short and less than 100 characters
```

The LLM then receives both its previous failing output and the corrective instruction, generating a new response more likely to satisfy the constraint. This demonstrates that negative feedback ("this is what you produced, and here is what was wrong with it") is a built-in, automated component of DSPy's self-refinement loop -- not a manually authored prompt pattern.

**Explicit Guidance on Negative vs Positive:**

DSPy's core philosophy is "programming -- not prompting -- language models." The framework intentionally avoids prescribing prompt-level patterns (positive or negative) because it automates prompt generation through optimization. The question of negative vs. positive framing is rendered moot by DSPy's approach of expressing constraints as programmatic assertions.

However, DSPy's backtracking mechanism (Pattern 4) demonstrates that negative feedback (what went wrong) is a built-in component of the system's self-refinement loop -- suggesting the framework implicitly recognizes the value of negative information in prompt optimization.

**Coverage Assessment:** **Architecturally different** -- DSPy transcends the negative vs. positive prompting question by replacing manual prompt engineering with programmatic constraint enforcement. The framework implicitly uses negative feedback in its backtracking mechanism. This assessment is based on publicly available documentation and default prompt templates; internal development practices are not assessed.

---

### 6. Prompt Engineering Guides (Cross-Framework)

**Source:** [Prompt Engineering Guide (promptingguide.ai)](https://www.promptingguide.ai/introduction/tips) (Accessed: 2026-02-27), [Lakera Prompt Engineering Guide](https://www.lakera.ai/blog/prompt-engineering-guide) (Accessed: 2026-02-27), [Pink Elephant Problem analysis](https://eval.16x.engineer/blog/the-pink-elephant-negative-instructions-llms-effectiveness-analysis) (Accessed: 2026-02-27)

**Source Authority:** MIXED -- promptingguide.ai (MEDIUM: community resource citing OpenAI), Lakera (LOW: commercial security company blog), 16x.engineer (LOW: individual analysis post). Authority tier differentiation is noted per-finding below.

**Queries Executed:**
- Query 20: "negative prompting positive prompting comparison hallucination reduction" -- via WebSearch -> multiple framework-agnostic guides found
- Query 21: "promptingguide.ai negative prompting constraints prohibition" -- via WebSearch -> tips page found
- Query 22: "Pink Elephant Problem negative instructions LLMs" -- via WebFetch -> analysis retrieved
- Query 23: "negative prompting comprehensive guide 2025" -- via WebSearch -> Shadecoder guide found (content not extractable)

**Documented Negative Prompting Patterns:**

**Pattern 1: The Canonical Anti-Pattern (promptingguide.ai -- MEDIUM authority, derived from OpenAI)**

From the Prompt Engineering Guide tips page:
> "avoid saying what not to do but say what to do instead."

The guide provides the movie recommendation chatbot example where negative instructions ("DO NOT ASK FOR INTERESTS. DO NOT ASK FOR PERSONAL INFORMATION") failed -- the model asked for interests anyway. The positive reframing provided specific alternative behaviors.

This guidance is attributed to OpenAI's original prompt engineering best practices and has become the most widely-cited recommendation on the topic across the prompt engineering community. Note: promptingguide.ai is a community-maintained resource, not an official OpenAI publication. Its authority derives from accurate attribution to OpenAI's original guidance.

**Pattern 2: The Pink Elephant Problem (16x.engineer -- LOW authority)**

The Pink Elephant Problem analysis draws on ironic process theory from psychology:

> "When you are told 'don't think of a pink elephant,' your brain must first process the concept of a pink elephant to know what to avoid"

The analysis hypothesizes that LLMs, as neural networks trained on human language, may exhibit similar cognitive patterns where suppression attempts paradoxically activate the prohibited behavior.

Key finding from the analysis:
> "these Reddit posts are anecdotal evidence and not controlled experiments"

The article acknowledges that no controlled experimental data exists to validate the pink elephant hypothesis for LLMs. The evidence is anecdotal. This source should be treated as a hypothesis generator, not evidence.

**Pattern 3: Hybrid Approach (Lakera, 2026 -- LOW authority)**

The Lakera prompt engineering guide (2026) recommends:
> "tells it how to think, respond, and decline inappropriate requests"

Rather than pure prohibition, the guide recommends instructing desired behavior as the primary method, with negative constraints reserved for safety boundaries. The pattern: role anchoring (positive instruction) implicitly constrains behavior more effectively than explicit prohibition.

Note: Lakera is a commercial AI security company. This recommendation aligns with vendor guidance (Anthropic, OpenAI) but represents a blog post, not peer-reviewed research.

**Pattern 4: Constraint Scaffolding (Cross-Framework -- MEDIUM authority)**

Multiple guides describe "prompt scaffolding" -- wrapping user inputs in structured, guarded templates that limit model behavior through structure rather than prohibition. This approach represents a third paradigm beyond negative or positive: structural constraint that bypasses the framing question entirely. This aligns with the structural enforcement patterns observed in LangChain (L1 Section 3) and DSPy (L1 Section 5).

**Pattern 5: Practical Recommendations (Cross-Framework -- MEDIUM authority, multiple sources)**

From the Prompt Builder OpenAI Guide (Ref #20, MEDIUM authority) and cross-framework sources:
> "Negative instructions are harder for models to follow than positive ones." (Ref #20)
> "Combining negative prompts with clear positive instructions tends to be more effective than using negative constraints alone." (Ref #20)

From promptingguide.ai (Ref #15, MEDIUM authority):
> "Framing 'what to do' often beats long lists of 'don'ts.' Hard constraints should be saved for safety."

These recommendations represent practitioner guidance with consistent themes across sources, but are not backed by controlled experimental evidence.

**Explicit Guidance on Negative vs Positive:**

The prompt engineering community broadly recommends positive framing as the default, with negative constraints reserved for hard safety boundaries. However, this recommendation is based on practitioner experience and vendor guidance -- not controlled experimental evidence.

**Coverage Assessment:** **Explicit coverage with mixed authority** -- Prompt engineering guides provide the most prescriptive (but least evidence-based) guidance. The convergence on "positive framing > negative framing" is consistent across sources but based on practitioner experience rather than controlled experiments. Source authority ranges from MEDIUM (promptingguide.ai) to LOW (individual blog posts).

---

## L2: Cross-Library Analysis

### Pattern Convergence

The following patterns appear consistently across multiple sources:

**NP-001: "Positive-First, Negative-When-Necessary" (Appears in: Anthropic Ref #1, OpenAI Ref #4-7, Prompt Engineering Guides Ref #15, #17, #20)**

All sources that address the topic explicitly recommend positive framing as the default approach. Negative constraints are reserved for:
- Hard safety boundaries (never reveal system prompts)
- Specific behavioral prohibitions (do not hallucinate tool inputs)
- Scope control (do not invent UI elements)

**NP-002: "Paired Negative-Positive" (Appears in: Anthropic Ref #1, OpenAI Ref #6-7, LlamaIndex Ref #11)**

When negative instructions are used, the most effective pattern pairs the prohibition with a positive alternative:
- "Do NOT guess... -- ask for whichever detail is missing" (OpenAI GPT-5.1, Ref #6)
- "Do NOT fill in the vector values directly, but rather specify a `[query_vector]` placeholder" (LlamaIndex, Ref #11)
- "Never use ellipses since the text-to-speech engine will not know how to pronounce them" (Anthropic -- negative + reason, Ref #1)

**NP-003: "Contextual Justification" (Appears in: Anthropic Ref #1, OpenAI Ref #4)**

Negative instructions are more effective when accompanied by an explanation of why the constraint exists:
- "Your response will be read aloud by a text-to-speech engine, so never use ellipses" (Anthropic, Ref #1)
- "Adding 'if you don't have enough information...' should mitigate this" (OpenAI GPT-4.1, Ref #4)

**NP-004: "Structural Constraint Over Linguistic Constraint" (Appears in: LangChain Ref #8-9, DSPy Ref #12-14, Prompt Engineering Guides Ref #17)**

Multiple sources demonstrate that structural enforcement (output parsers, type systems, programmatic assertions) is more reliable than linguistic constraint (whether positive or negative):
- LangChain's OutputFixingParser, StructuredOutputParser, and guardrail middleware (L1 Section 3 code examples)
- DSPy's dspy.Assert and dspy.Suggest with backtracking (L1 Section 5 code examples)
- Prompt scaffolding patterns in cross-framework guides (Ref #17)

### Pattern Divergence

#### 1. Vendor Recommendation vs. Vendor Practice

The most significant divergence is between what vendors recommend and what they do:
- Anthropic recommends "tell Claude what to do instead of what not to do" -- but their own system prompts use `<do_not_act_before_instructions>` and `NEVER output a series of overly short bullet points` (Ref #1)
- OpenAI recommends "say what to do instead of what not to do" (via Ref #15) -- but their GPT-5.2 cookbook guide uses "Do NOT invent colors" and "Never fabricate" (Ref #7)

This tension admits multiple plausible explanations, and the survey does not have sufficient evidence to determine which explanation is correct:

1. **Intentional context dependency:** Vendors may deliberately use different framing for different use cases -- positive framing for general-purpose prompting, negative framing for safety-critical constraints. The recommendation targets the common case; the practice reflects edge cases.
2. **Temporal lag:** Vendor-authored examples may have been written before the positive-framing recommendation was codified, and have not been updated to reflect current guidance.
3. **Pedagogical vs. production distinction:** Example prompts in documentation may serve pedagogical purposes (showing what is possible) rather than representing production best practices.
4. **Pragmatic recognition:** Vendors may implicitly recognize that some constraints are most clearly expressed as prohibitions, even when the general recommendation favors positive framing.

All four explanations are consistent with the observed evidence. The tension between recommendation and practice is documented but its root cause is uncertain.

#### 2. Evolution of OpenAI's Position

OpenAI's guidance has shifted across model generations (documented via cookbook guides, Ref #4-7):
- **GPT-3.5/4 era:** "Say what to do, not what not to do" (absolute recommendation, via Ref #15)
- **GPT-4.1:** "Mandatory constraints can backfire" (nuanced warning, Ref #4)
- **GPT-5/5.1:** Negative constraints used actively with positive alternatives (Ref #5, #6)
- **GPT-5.2:** "GPT-5.2 requires explicit instructions" -- negative constraints explicitly recommended for scope control (Ref #7)

This evolution suggests that as models have improved at instruction following, the distinction between negative and positive framing has become less important than the clarity and specificity of the instruction.

#### 3. DSPy's Paradigm Rejection

DSPy rejects the negative-vs-positive question entirely by automating prompt generation (Ref #12, #13, #14). This is a fundamentally different approach that makes the debate irrelevant within its framework. However, DSPy's backtracking mechanism (L1 Section 5, Pattern 4) demonstrates that negative feedback -- "what went wrong" injected into the retry prompt -- is a built-in component of effective constraint enforcement.

### Academic Research Findings

Two academic papers were identified that provide empirical (rather than prescriptive) evidence relevant to the PROJ-014 hypothesis. Both are integrated here because they are the only sources in this survey with quantitative data.

> **Preprint disclosure:** Both papers cited below are arXiv preprints that have not undergone peer review as of 2026-02-27. Their findings should be treated as preliminary empirical evidence rather than validated research conclusions. Their authority tier is MEDIUM (arXiv preprint), not HIGH. The peer-reviewed DSPy Assertions paper (Ref #13, arXiv:2312.13382v1) is a separate, higher-authority citation. Quantitative figures cited from these preprints are extracted from WebFetch retrieval of the arXiv HTML pages and abstracts; verbatim quotation from paginated PDF content was not possible via WebFetch.

**"The Instruction Gap" (Tripathi, Allu, & Ahmed, 2025; arXiv:2601.03269) -- arXiv preprint, not peer reviewed**

This study evaluated 13 leading LLMs across 600 enterprise RAG queries, measuring instruction violations, response accuracy, and hallucination rates. Key quantitative findings:

- **Instruction violation counts ranged from 660 (GPT-5 Medium, best) to 1,330 (Gemini 2.0-Flash, worst)** -- a two-fold difference between best and worst performers. Note: "GPT-5 Medium" is the model designation used in the arXiv preprint (Tripathi et al., 2025). This designation cannot be verified against standard OpenAI public model naming conventions and may refer to an internal model variant or a designation that differs in the final published version.
- **Hallucination rates ranged from 0.03 (GPT-5 Medium) to 0.08 (Gemini 2.0-Flash)**, with correct response rates of 0.88 and 0.76 respectively.
- The study identified four violation categories: content scope, format, tone/style, and procedural violations.
- **Relevance to PROJ-014:** The paper demonstrates that instruction-following compliance varies dramatically across models and is measurable, but it does **not** isolate negative vs. positive instruction framing as a variable. The "instruction gap" refers to the general gap between model capability and instruction adherence in enterprise contexts, not specifically to negative instruction compliance. The 60% claim cannot be derived from or validated against this data.

**"When Models Can't Follow" (Young, Gillins, & Matthews, 2025; arXiv:2510.18892) -- arXiv preprint, not peer reviewed**

This study tested 256 LLMs from providers including OpenAI, Anthropic, Google, Meta, and Mistral using 20 carefully designed instruction-following tests. Key quantitative findings:

- **Overall pass rate: 43.7%** across 5,120 individual test evaluations.
- **Pass rates by category:** String manipulation 12.0%, Mathematical operations 44.9%, Data processing 45.5%, Format conversion 57.8%, **Constraint compliance 66.9%** (highest category).
- **Individual test extremes:** Test 5 (Complex String Transformation) had the lowest pass rate at 2.7%; Test 2 (Exact Output Compliance) had the highest at 96.1%.
- The study observed a "binary outcome distribution" in constraint compliance: "successful models appeared to implement robust checking mechanisms, while failing models showed no awareness of the constraint violation... with little middle ground."
- **Relevance to PROJ-014:** The "Constraint compliance" category (66.9% pass rate) is the closest proxy for the type of instruction the PROJ-014 hypothesis addresses, but the study does **not** differentiate between negative and positive constraint framing within this category. The 256-model scale provides a robust methodology template for future research that could isolate framing effects. The binary pass/fail distribution suggests that constraint following may be more about model capability than framing choice.

**Combined Academic Assessment:**

Neither paper directly tests the PROJ-014 hypothesis. Both measure instruction-following compliance broadly without isolating negative vs. positive framing as an independent variable. However, they establish three important findings for Phase 2:
1. Instruction compliance is measurable and varies dramatically across models (2x range).
2. Constraint compliance (66.9%) is the highest-performing instruction category, suggesting models are relatively capable of following constraints regardless of framing.
3. The binary distribution of constraint compliance outcomes suggests that model architecture and training methodology may matter more than linguistic framing.

### Coverage Gaps

**1. No Controlled Experimental Data on Negative vs. Positive Framing**

Zero surveyed sources provide controlled experimental data specifically comparing negative vs. positive prompting effectiveness with matched prompts and measurable hallucination metrics. All prescriptive guidance is based on practitioner experience (anecdotal), vendor recommendation (authoritative but unquantified), and community consensus (broad but uncontrolled). The two academic papers measure instruction compliance broadly but do not isolate framing as a variable.

This is the most critical gap for PROJ-014's hypothesis. The claim of "60% hallucination reduction" through negative prompting cannot be validated or refuted by any documentation surveyed.

**2. No Model-Specific Framing Compliance Data**

No surveyed source provides compliance rate data specifically comparing negative vs. positive instruction framing (e.g., "Claude follows 'do NOT' instructions X% of the time vs. 'please do' instructions Y% of the time"). Tripathi et al. (2025) measure instruction violations but do not categorize by framing type. Young et al. (2025) test constraint compliance but do not differentiate negative from positive constraints.

**3. No Taxonomy of Negative Instruction Types**

No source provides a systematic taxonomy of negative instruction types (prohibitions, exclusions, conditional negations, scope limits, safety boundaries) with differential effectiveness data for each type. The absence of such a taxonomy means Phase 2 analysis cannot systematically compare different types of negative instructions.

### Negative Instruction Type Taxonomy (Preliminary)

> **PRELIMINARY:** This taxonomy skeleton is derived from patterns observed in the survey findings. It is intended as a starting framework for Phase 2 validation and refinement, not as a validated classification system. Phase 2 should test whether these categories are mutually exclusive, collectively exhaustive, and differentially effective.

| Type | Definition | Example from Survey | Source |
|------|-----------|-------------------|--------|
| **Prohibition** | Direct forbiddance of a specific action or output ("Never do X", "Do NOT do X") | "Never fabricate exact figures, line numbers, or external references when uncertain" | OpenAI GPT-5.2 (Ref #7) |
| **Exclusion** | Instruction to omit specific content from output ("Do NOT include X", "Do NOT fill in X") | "Do NOT fill in the vector values directly, but rather specify a `[query_vector]` placeholder" | LlamaIndex (Ref #11) |
| **Conditional negation** | Negation triggered only under specific circumstances ("If X, don't Y") | "if you don't have enough information to call the tool, ask the user for the information you need" | OpenAI GPT-4.1 (Ref #4) |
| **Scope limitation** | Restricting the model to specific inputs or knowledge ("Only X, not Y") | "Using only the choices above and not prior knowledge, return the choice..." | LlamaIndex (Ref #11) |
| **Safety boundary** | Hard constraint preventing disclosure, speculation, or unsafe action ("MUST NOT reveal/share/expose") | `<do_not_act_before_instructions>` -- "Do not jump into implementation or changes files unless clearly instructed" | Anthropic (Ref #1) |

**Observations for Phase 2:**
- **Prohibition** and **Exclusion** are the most common types across all surveyed sources.
- **Conditional negation** is specifically recommended by OpenAI's GPT-4.1 guide as a mitigation for mandatory constraint failures.
- **Safety boundary** type is where vendors most consistently use negative framing despite recommending positive framing as the general default.
- The boundary between Prohibition and Safety boundary may not be clean -- Phase 2 should determine whether these are distinct types or contextual variants of the same pattern.
- No surveyed source provides differential effectiveness data by instruction type. Whether Prohibitions are more or less effective than Scope limitations is an open empirical question.

**4. No Framework-Specific Integration Guidance**

No framework (LangChain, LlamaIndex, DSPy) provides guidance on how to combine structural constraints with linguistic constraints (positive or negative) for optimal results.

### Implications for PROJ-014 Hypothesis

The PROJ-014 hypothesis states: "Negative unambiguous prompting reduces hallucination by 60% and achieves better results than explicit positive prompting."

Based on this survey, the hypothesis faces significant challenges:

1. **The 60% claim is unsupported by any vendor documentation or academic research surveyed.** No source provides quantitative hallucination reduction data for any prompting approach, let alone a specific comparison between negative and positive framing. The claim requires controlled experimental evidence that does not exist in the surveyed landscape.

2. **The "better results" claim contradicts vendor recommendations but aligns partially with vendor practice.** Both Anthropic and OpenAI explicitly recommend positive framing over negative framing. However, the tension between recommendation and practice (see [Pattern Divergence](#1-vendor-recommendation-vs-vendor-practice)) complicates the picture and admits multiple interpretations.

3. **The hypothesis may be asking the wrong question.** The surveyed evidence suggests that the negative-vs-positive distinction is less important than:
   - **Specificity** (vague instructions fail regardless of framing -- OpenAI GPT-5.2 Ref #7)
   - **Pairing** (negative + positive alternative > negative alone -- NP-002 pattern)
   - **Contextual justification** (explaining why the constraint exists -- NP-003 pattern)
   - **Structural enforcement** (programmatic constraints > linguistic constraints -- NP-004 pattern)

4. **The hypothesis needs refinement for Phase 2.** Rather than "negative prompting reduces hallucination by 60%," a more defensible hypothesis informed by this survey would be: "Specific, contextually justified constraints (whether positive or negative) combined with structural enforcement mechanisms reduce hallucination more effectively than unstructured instructions."

5. **What would support the original hypothesis:** Phase 2 would need to produce or locate controlled experimental data comparing matched prompt pairs (identical constraint expressed negatively vs. positively) across multiple models with measurable hallucination rates. The 256-model methodology from Young et al. (2025) provides a scalable evaluation template. To validate the 60% claim specifically, the experiment would need to show a statistically significant 60% reduction in hallucination rate when using negative framing vs. positive framing, with sufficient sample size to control for model variance (which Tripathi et al. 2025 show is a 2x range).

### Phase 2 Task Mapping

| Implication | Phase 2 Task | Artifact |
|---|---|---|
| 60% claim unsupported | Design controlled experiment to test negative vs. positive framing (see Experimental Design Parameters below) | Experimental design document |
| Vendor practice contradicts recommendation | Classify vendor negative instructions by context (safety, formatting, scope) to test context-dependency explanation; use [Negative Instruction Type Taxonomy](#negative-instruction-type-taxonomy-preliminary) as starting framework | Vendor instruction taxonomy |
| Hybrid approach converges across sources | Design paired negative-positive instruction templates for testing; construct framing pairs per methodology below | Instruction pair test suite |
| Structural enforcement > linguistic framing | Evaluate whether PROJ-014 scope should expand to include structural mechanisms | Scope revision proposal |

#### Experimental Design Parameters

The following parameters are derived from the methodologies documented in the two academic papers surveyed. They provide a concrete starting point for Phase 2 experimental design rather than requiring the Phase 2 analyst to re-derive these specifications from scratch.

**Framing pair construction methodology:**
- Each test case consists of a *matched framing pair*: the same semantic constraint expressed once as a negative instruction and once as a positive instruction, applied to the same input.
- Example: Negative -- "Do NOT include information not present in the source document." Positive -- "Include only information that is directly stated in the source document."
- Pairs should be constructed for each type in the [Negative Instruction Type Taxonomy](#negative-instruction-type-taxonomy-preliminary) (Prohibition, Exclusion, Conditional negation, Scope limitation, Safety boundary) to enable per-type effectiveness comparison.
- The GPT-5.2 guide's observation that "poorly-constructed prompts containing contradictory or vague instructions can be more damaging" (Ref #7) suggests that pair construction must control for instruction clarity independently of framing polarity.
- Instruction clarity MUST be controlled as a potential confound. Each framing pair will be rated for clarity on a 5-point Likert scale by the same two raters who validate semantic equivalence; pairs with a mean clarity difference > 1.0 points between positive and negative framings will be revised to equalize clarity before inclusion in the study.
- Framing pair semantic equivalence MUST be validated before use. Validation method: two independent raters classify each pair as "semantically equivalent" or "not equivalent," with Cohen's kappa >= 0.80 required (Landis & Koch, 1977, classify 0.81-1.00 as "almost perfect agreement"; this threshold is standard in inter-rater reliability research); pairs failing the threshold are revised and re-rated.

**Model selection criteria:**
- Minimum 3 model families (e.g., Anthropic Claude, OpenAI GPT, Google Gemini) to control for model-specific instruction-following behavior.
- Tripathi et al.'s finding of a 2x instruction violation range across 13 models (660 to 1,330 violations; Ref #18, MEDIUM authority -- arXiv preprint) demonstrates that model variance is a significant confound that must be controlled.
- Young et al.'s 256-model scale (Ref #19, MEDIUM authority -- arXiv preprint) provides a reference floor; a practical minimum of 5-10 models across 3+ providers would enable within-provider and cross-provider comparison while remaining feasible for a Phase 2 study.

**Metric selection:**
- **Primary metric -- Compliance rate:** Percentage of responses that satisfy the stated constraint. Directly comparable to Young et al.'s pass rate methodology (43.7% overall, 66.9% for constraint compliance; Ref #19).
- **Secondary metric -- Hallucination rate:** Percentage of responses containing fabricated content. Comparable to Tripathi et al.'s hallucination rate range of 0.03-0.08 (Ref #18).
- **Tertiary metric -- Output quality:** Holistic quality assessment of compliant responses to determine whether compliance comes at a quality cost (e.g., a negative instruction that is followed but produces a lower-quality response than the positive alternative).

**Sample size guidance:**
- Tripathi et al.'s 600-query RAG methodology across 13 models (Ref #18) and Young et al.'s 20 test types across 256 models (Ref #19) provide validated sample size references.
- 50 framing pairs (10 per taxonomy type) tested across 5 models, with each pair evaluated under both negative and positive framing conditions, would yield 500 evaluation data points minimum (50 pairs x 5 models x 2 framing conditions = 500), sufficient for per-type and per-model statistical comparison.
- Young et al.'s binary outcome distribution finding (models either implement robust checking or show no awareness of violations, with little middle ground) suggests that power analysis should account for bimodal rather than normal distributions.
- **Experimental validity consideration:** Instruction compliance is often binary (followed/not followed), which may require larger sample sizes for statistical significance than continuous metrics would. A pilot study with 10 framing pairs across 3 models is recommended before committing to the full 500-evaluation protocol, to validate that the proposed metrics produce sufficient distributional variance for meaningful statistical comparison between negative and positive framings.

---

## Methodology

### Source Selection Rationale

Six sources were selected for this survey based on three criteria:

1. **Market representation:** Anthropic and OpenAI are the two largest commercial LLM providers by enterprise adoption. Their prompting guidance is the most widely followed.
2. **Framework coverage:** LangChain, LlamaIndex, and DSPy are the three most widely used Python frameworks for LLM application development (by GitHub stars, PyPI downloads, and community activity as of Q1 2026).
3. **Community guidance:** Cross-framework prompt engineering guides provide the broadest practitioner perspective, independent of any single vendor or framework.

**Excluded sources and rationale:**
- **Google (Gemini):** Excluded due to scope constraints; Gemini's prompting documentation was not surfaced in initial WebSearch queries focused on negative prompting. Future research should include this source.
- **Meta (LLaMA):** LLaMA models are open-weight; Meta's prompting guidance is primarily community-generated rather than vendor-authored. Less relevant for vendor recommendation analysis.
- **Cohere (Command R+):** Smaller market share; excluded to maintain a manageable survey scope.
- **Hugging Face:** Platform rather than model provider; prompt guidance is community-generated and highly variable.

These exclusions mean the survey's findings are most applicable to the commercial LLM vendor + Python framework ecosystem. Guidance from Google, Meta, and other providers may contain different or additional insights not captured here.

### Tool Availability and Coverage Risk

Context7 MCP tools (`mcp__context7__resolve-library-id`, `mcp__context7__query-docs`) were configured in the session settings (`mcp__context7__*` and `mcp__plugin_context7_context7__*`) but were not available as callable functions in the agent runtime. Per the MCP error handling protocol in `mcp-tool-standards.md`, WebSearch and WebFetch were used as systematic fallback. This limitation is documented transparently per P-022 (no deception about capabilities).

**Coverage risk acknowledgment:** WebSearch/WebFetch is NOT equivalent to Context7's curated documentation corpus. Context7 provides structured library documentation lookup with indexed, curated content from official library sources. WebSearch provides general web search results ranked by SEO relevance, which may surface blog posts, tutorials, and community content alongside official documentation. The following specific risks apply:

1. **Documentation depth:** Context7 indexes internal API documentation, code examples, and configuration guides that may not be indexed by search engines or may be behind authentication walls. The OpenAI platform docs 403 error (L1 Section 2) is a direct example of this gap.
2. **Version specificity:** Context7 documentation is versioned and tied to specific library releases. WebSearch results may mix content from different library versions without clear version demarcation.
3. **Structural coverage:** Context7 enables systematic traversal of a library's documentation tree. WebSearch is query-driven and may miss documentation sections not surfaced by keyword matching.

**What may have been missed:** Library-internal documentation on prompt template design patterns, internal style guides for system prompts, version-specific changelog entries discussing framing changes, and API reference documentation not indexed by search engines. The LangChain coverage gap (5 queries returned "silent on framing") may partially reflect this limitation -- LangChain's internal documentation on LCEL prompt composition patterns may contain relevant guidance not surfaced by WebSearch.

### Query Log

| # | Target Library | Method | Query/URL | Result Status | Access Date |
|---|---|---|---|---|---|
| 1 | Anthropic Claude | WebSearch | "Anthropic Claude prompt engineering documentation negative prompting 'do not' 'avoid' constraints best practices 2025 2026" | 10 results found | 2026-02-27 |
| 2 | Anthropic Claude | WebFetch | `https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices` | Full page retrieved (after redirect) | 2026-02-27 |
| 3 | Anthropic Claude | WebSearch | "'tell Claude what to do instead of what not to do' positive framing" | Confirmed canonical recommendation | 2026-02-27 |
| 4 | OpenAI GPT | WebSearch | "OpenAI GPT prompt engineering documentation negative instructions 'do not' prohibition constraints best practices 2025 2026" | 10 results found | 2026-02-27 |
| 5 | OpenAI GPT | WebFetch | `https://platform.openai.com/docs/guides/prompt-engineering` | 403 Forbidden | 2026-02-27 |
| 6 | OpenAI GPT | WebFetch | `https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide` | Retrieved (after redirect) | 2026-02-27 |
| 7 | OpenAI GPT | WebFetch | `https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide` | Retrieved (after redirect) | 2026-02-27 |
| 8 | OpenAI GPT | WebFetch | `https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-1_prompting_guide/` | Retrieved | 2026-02-27 |
| 9 | OpenAI GPT | WebFetch | `https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide` | Retrieved (after redirect) | 2026-02-27 |
| 10 | OpenAI GPT | WebSearch | "OpenAI GPT-5.2 GPT-5.1 prompting guide constraints negative instructions" | 10 results found | 2026-02-27 |
| 11 | LangChain | WebSearch | "LangChain prompt templates negative prompting patterns constraints prohibition 2025 2026" | No specific coverage | 2026-02-27 |
| 12 | LangChain | WebSearch | "LangChain system message constraints negative prompting prohibition patterns output parser 2025" | Output parser mechanisms found | 2026-02-27 |
| 13 | LangChain | WebSearch | "LangChain guardrails constraint prompt patterns negative instructions examples 2025" | Guardrail patterns found | 2026-02-27 |
| 14 | LlamaIndex | WebSearch | "LlamaIndex prompt engineering negative prompting patterns constraints 2025 2026" | No specific coverage | 2026-02-27 |
| 15 | LlamaIndex | WebSearch | "LlamaIndex system prompt templates constraints negative instructions documentation 2025" | Prompt template docs found | 2026-02-27 |
| 16 | LlamaIndex | WebFetch | `https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/prompts/default_prompts.py` | Negative instruction patterns extracted | 2026-02-27 |
| 17 | LlamaIndex | WebFetch | `https://developers.llamaindex.ai/python/framework/module_guides/models/prompts/` | No negative prompting guidance | 2026-02-27 |
| 18 | DSPy | WebSearch | "DSPy prompt optimization constraints negative prompting patterns 2025 2026" | Optimizer documentation found | 2026-02-27 |
| 19 | DSPy | WebSearch | "DSPy assertions constraints guardrails dspy.Assert dspy.Suggest negative prompting 2025" | Assertions documentation found | 2026-02-27 |
| 20 | DSPy | WebFetch | `https://dspy.ai/learn/optimization/optimizers/` | No negative prompting coverage | 2026-02-27 |
| 21 | DSPy | WebFetch | `https://dspy.ai/learn/programming/7-assertions/` | Detailed assertion mechanism found | 2026-02-27 |
| 22 | Prompt Guides | WebSearch | "prompt engineering framework 'negative prompting' 'positive prompting' comparison hallucination reduction 2025" | Multiple guides found | 2026-02-27 |
| 23 | Prompt Guides | WebFetch | `https://www.promptingguide.ai/introduction/tips` | Canonical negative-to-positive example found | 2026-02-27 |
| 24 | Prompt Guides | WebFetch | `https://eval.16x.engineer/blog/the-pink-elephant-negative-instructions-llms-effectiveness-analysis` | Pink Elephant analysis retrieved | 2026-02-27 |
| 25 | Prompt Guides | WebFetch | `https://www.lakera.ai/blog/prompt-engineering-guide` | Constraint scaffolding patterns found | 2026-02-27 |
| 26 | Academic | WebSearch | "research paper LLM negative instruction following compliance rate experimental study 2024 2025" | 10 results found | 2026-02-27 |
| 27 | Academic | WebFetch | `https://arxiv.org/html/2601.03269` | Instruction Gap findings extracted | 2026-02-27 |
| 28 | Academic | WebFetch | `https://arxiv.org/html/2510.18892` | 256 LLM testing methodology found | 2026-02-27 |
| 29 | LangChain (Iter. 2) | WebSearch | "LangChain LCEL prompt composition negative constraints positive framing 2025 2026" | LCEL docs found; no framing guidance | 2026-02-27 |
| 30 | LangChain (Iter. 2) | WebFetch | `https://docs.langchain.com/oss/python/langchain/guardrails` | Guardrails code examples extracted | 2026-02-27 |
| 31 | DSPy (Iter. 2) | WebSearch | "DSPy backtracking assertion example concrete negative feedback retry" | Backtracking examples found | 2026-02-27 |
| 32 | DSPy (Iter. 2) | WebFetch | `https://dspy.ai/learn/programming/7-assertions/` | Concrete backtracking code extracted | 2026-02-27 |
| 33 | Academic (Iter. 2) | WebFetch | `https://arxiv.org/abs/2601.03269` | Authors and key results confirmed | 2026-02-27 |
| 34 | Academic (Iter. 2) | WebFetch | `https://arxiv.org/abs/2510.18892` | Authors and key results confirmed | 2026-02-27 |

**Query Summary:** 34 total queries across 2 iterations. 14 WebSearch queries, 20 WebFetch requests. Queries 1-28 executed in iteration 1; queries 29-34 executed in iteration 2 to address coverage gaps identified by adversarial review (LangChain depth, DSPy examples, academic paper integration).

### Query-to-Library Mapping

| Library Category | Queries | Count |
|---|---|---|
| Anthropic Claude | 1, 2, 3 | 3 |
| OpenAI GPT | 4, 5, 6, 7, 8, 9, 10 | 7 |
| LangChain | 11, 12, 13, 29, 30 | 5 |
| LlamaIndex | 14, 15, 16, 17 | 4 |
| DSPy | 18, 19, 20, 21, 31, 32 | 6 |
| Prompt Engineering Guides | 22, 23, 24, 25 | 4 |
| Academic Papers | 26, 27, 28, 33, 34 | 5 |

### Source Provenance

Every finding in this document is traced to a specific WebSearch query or WebFetch URL as listed in the Query Log above. Direct quotes are used wherever possible; paraphrases are noted when the original source was not fully extractable. The source authority tier (HIGH, MEDIUM, LOW) is annotated per-finding in L1 and in the References section.

### Reproducibility Statement

This survey was executed using WebSearch and WebFetch exclusively as the primary and sole research method. Context7 MCP tools were configured but not available as callable functions in the agent runtime (see [Tool Availability and Coverage Risk](#tool-availability-and-coverage-risk) for details). WebSearch/WebFetch was NOT a fallback -- it was the only tool used for all 34 queries across both iterations.

To reproduce this survey, execute the queries in the Query Log using WebSearch/WebFetch for comparable results. Note that reproduction using Context7 MCP (if available in future sessions) may yield different coverage due to the difference between structured, curated documentation indexing (Context7) and SEO-ranked web search results (WebSearch). The two methods are not equivalent and may surface different content from the same libraries. Vendor documentation is living content -- results may also differ if documentation has been updated after the access dates listed. The arXiv papers (Ref #18, #19) are version-stable and should produce identical results.

---

## References

1. [Anthropic Claude Prompting Best Practices](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) -- **HIGH** -- Key insight: Recommends positive framing but uses negative instructions extensively in practice. Accessed: 2026-02-27. Note: URL path contains "claude-4-best-practices"; Anthropic's public model naming conventions differ from this URL slug. Content describes best practices for Claude prompting generally.
2. [Anthropic Prompt Engineering Blog](https://claude.com/blog/best-practices-for-prompt-engineering) -- **HIGH** -- Key insight: Canonical "tell Claude what to do instead of what not to do" recommendation. Accessed: 2026-02-27.
3. [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering) -- **HIGH** (inaccessible) -- Key insight: Original "say what to do instead of what not to do" recommendation. 403 on direct fetch; content confirmed via Ref #15 (promptingguide.ai, MEDIUM authority). Accessed: 2026-02-27.
4. [OpenAI GPT-4.1 Prompting Guide (Cookbook)](https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide) -- **HIGH** -- Key insight: Mandatory constraints can cause hallucinated tool inputs. Accessed: 2026-02-27.
5. [OpenAI GPT-5 Prompting Guide (Cookbook)](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide) -- **HIGH** -- Key insight: Contradictory negative instructions cause failures; resolve by restating positively. Accessed: 2026-02-27.
6. [OpenAI GPT-5.1 Prompting Guide (Cookbook)](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-1_prompting_guide/) -- **HIGH** -- Key insight: Paired negative-positive patterns; constraint clarity > framing choice. Accessed: 2026-02-27.
7. [OpenAI GPT-5.2 Prompting Guide (Cookbook)](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide) -- **HIGH** -- Key insight: Explicit negative constraints recommended for scope control; model requires explicit instructions. Accessed: 2026-02-27.
8. [LangChain Prompt Templates Reference](https://reference.langchain.com/python/langchain-core/prompts) -- **HIGH** -- Key insight: Silent on negative vs. positive prompting. Accessed: 2026-02-27.
9. [LangChain Guardrails Documentation](https://docs.langchain.com/oss/python/langchain/guardrails) -- **HIGH** -- Key insight: Structural constraint enforcement (middleware, validators) orthogonal to linguistic framing; code examples demonstrate negative blocking and positive transformation strategies. Accessed: 2026-02-27.
10. [LlamaIndex Prompts Documentation](https://developers.llamaindex.ai/python/framework/module_guides/models/prompts/) -- **HIGH** -- Key insight: Silent on guidance but default prompts use negative framing extensively. Accessed: 2026-02-27.
11. [LlamaIndex Default Prompts Source Code](https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/prompts/default_prompts.py) -- **HIGH** (source code) -- Key insight: 6 default prompt templates contain negative instructions ("Never", "Do NOT", "don't"). Source code demonstrates actual framework behavior, not documentation guidance. Accessed: 2026-02-27.
12. [DSPy Assertions Documentation](https://dspy.ai/learn/programming/7-assertions/) -- **HIGH** -- Key insight: Programmatic constraints replace linguistic constraints; backtracking injects negative feedback ("what went wrong") into retry prompts automatically. Accessed: 2026-02-27.
13. [DSPy Assertions Paper (Khattab et al., 2024)](https://arxiv.org/html/2312.13382v1) -- **HIGH** (peer-reviewed) -- Key insight: dspy.Assert and dspy.Suggest provide hard/soft constraint enforcement as computational constraints. Accessed: 2026-02-27.
14. [DSPy Official Site](https://dspy.ai/) -- **HIGH** -- Key insight: "Programming -- not prompting -- language models" philosophy renders framing question moot. Accessed: 2026-02-27.
15. [Prompt Engineering Guide - General Tips (promptingguide.ai)](https://www.promptingguide.ai/introduction/tips) -- **MEDIUM** (community resource citing OpenAI) -- Key insight: Canonical "avoid saying what not to do but say what to do instead" recommendation with movie chatbot example. Accessed: 2026-02-27.
16. [The Pink Elephant Problem (16x.engineer)](https://eval.16x.engineer/blog/the-pink-elephant-negative-instructions-llms-effectiveness-analysis) -- **LOW** (individual analysis post) -- Key insight: Anecdotal evidence only; no controlled experiments; acknowledges limitations. Hypothesis generator, not evidence. Accessed: 2026-02-27.
17. [Lakera Prompt Engineering Guide (2026)](https://www.lakera.ai/blog/prompt-engineering-guide) -- **LOW** (commercial blog) -- Key insight: Instructing desired behavior outperforms prohibition; prompt scaffolding as structural alternative. Accessed: 2026-02-27.
18. [The Instruction Gap (Tripathi, Allu, & Ahmed, 2025; arXiv:2601.03269)](https://arxiv.org/abs/2601.03269) -- **MEDIUM** (arXiv preprint -- not peer reviewed) -- Key insight: 13 LLMs tested across 600 enterprise RAG queries; instruction violations range 660-1,330 (2x); hallucination rates 0.03-0.08; does NOT isolate negative vs. positive framing. Accessed: 2026-02-27.
19. [When Models Can't Follow (Young, Gillins, & Matthews, 2025; arXiv:2510.18892)](https://arxiv.org/abs/2510.18892) -- **MEDIUM** (arXiv preprint -- not peer reviewed) -- Key insight: 256 LLMs tested across 20 instruction types; overall 43.7% pass rate; constraint compliance 66.9% (highest category); does NOT differentiate negative vs. positive constraints. Accessed: 2026-02-27.
20. [Prompt Builder OpenAI Guide](https://promptbuilder.cc/blog/openai-prompt-engineering-guide-best-practices-2026) -- **MEDIUM** (secondary guide) -- Key insight: "Negative instructions are harder for models to follow than positive ones"; recommends hybrid approach. Accessed: 2026-02-27.

---

## PS Integration

- **PS ID:** PROJ-014
- **Entry ID:** TASK-003
- **Artifact Type:** Research Survey (Iteration 5)
- **Confidence:** High (0.80) -- Comprehensive coverage across 6 targets with 34 queries across 2 iterations. Five revision iterations applied with adversarial scoring (I1=0.80, I2=0.87, I3=0.904, I4=0.924). Core structural constraints remain: Context7 unavailability (structural; WebSearch/WebFetch used as sole research method -- see [Coverage Risk](#tool-availability-and-coverage-risk)); OpenAI platform docs inaccessible (structural; 403 on direct fetch, covered via cookbook guides Ref #4-#7 and secondary source Ref #15); arXiv verbatim quotation gap (disclosed). Direct documentation extraction successful for 5 of 6 targets. Two academic papers (arXiv preprints, MEDIUM authority) integrated into L2 analysis. Negative instruction type taxonomy, Phase 2 experimental design parameters, doc-vs-behavior qualifiers, measurable success criteria, and experimental validity considerations added across iterations 3-5.
- **Next Agent Hint:** ps-analyst for cross-library pattern analysis and hypothesis validation. Note: ps-analyst should first determine whether the 60% claim can be tested empirically and identify what data sources would enable that test, before attempting to validate the claim directly. The 256-model methodology from Young et al. (2025) provides a scalable evaluation template for experimental design.
