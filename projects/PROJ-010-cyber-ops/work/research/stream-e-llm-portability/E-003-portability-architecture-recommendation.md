# E-003: Portability Architecture Recommendation

> Stream E: LLM Portability | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Architecture decision and rationale in 3-5 sentences |
| [L1: Key Findings](#l1-key-findings) | Consolidated findings from E-001 and E-002 |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Architecture design, schemas, adapter specs, validation, integration, migration |
| [Recommendations](#recommendations) | Numbered recommendations R-PORT-ARCH-001 through R-PORT-ARCH-012 |
| [Evidence and Citations](#evidence-and-citations) | Rolled up from E-001, E-002, and additional sources |

---

## L0: Executive Summary

PROJ-010's /eng-team and /red-team skills will achieve LLM portability (R-010) through a two-layer architecture that separates **semantic intent** from **provider-specific rendering**, implemented entirely within Jerry's existing markdown-with-YAML-frontmatter agent definition format. The Semantic Layer defines what an agent is and does using provider-agnostic fields (identity, constraints, tool schemas, output schemas) while the Rendering Layer transforms those definitions into provider-optimized prompts at invocation time through declarative transformation rules expressed as YAML configuration -- not compiled adapter code. This architecture draws directly on E-001's finding that the RCCF prompt pattern (Role-Context-Constraints-Format) and JSON Schema tool definitions are universally portable, combined with E-002's finding that the "agent-as-configuration" pattern (CrewAI, LangChain, Google ADK) is the industry-proven approach to portable agent definitions. The design preserves full backward compatibility with Jerry's 37 existing agents by treating the current Anthropic-optimized format as the default rendering target while introducing an optional `portability` frontmatter section that enables multi-provider support.

---

## L1: Key Findings

These findings synthesize E-001 (prompt engineering patterns) and E-002 (framework analysis) into architecture-actionable conclusions.

### Finding 1: The Portable Surface Area Is Larger Than the Non-Portable Surface Area

E-001 identified 10 portable fields, 7 adaptation-required fields, and 4 non-portable fields across the agent definition schema. E-002 confirmed that tool definitions (JSON Schema), agent identity (role/goal/expertise), and behavioral constraints are portable across all eight frameworks analyzed. The non-portable surface -- extended thinking, reasoning effort parameters, grounding APIs, and prompt caching -- consists exclusively of provider-specific performance optimizations, not core agent behavior. This means the majority of an agent definition can be written once and used across providers without modification.

### Finding 2: Prompt Structure Is Portable; Prompt Syntax Is Not

E-001 demonstrated that the RCCF pattern (Role-Context-Constraints-Format) works across all providers. E-002 showed that CrewAI's role/goal/backstory separation is portable across LLMs. However, the specific syntax used to express that structure -- XML tags (Anthropic-optimized), chat template tokens (model-specific), and message role semantics (provider-specific) -- requires adaptation. The architecture must therefore separate structural intent from syntactic expression.

### Finding 3: Structured Output Is the Highest-Value Adaptation Target

E-001 documented fundamentally different enforcement mechanisms: OpenAI's `response_format` (server-side, 100% compliance), Anthropic's tool-call workaround, Google's `response_schema`, and open-source prompt-level-only approaches. E-002 confirmed that no framework automatically resolves this divergence at the prompt level. For PROJ-010's cybersecurity agents -- where structured output reliability directly affects threat classification accuracy and engagement reporting quality -- the structured output adapter has the highest ROI of any adaptation target.

### Finding 4: The Industry Has Converged on Configuration-Driven Agent Definitions

E-002 found that CrewAI (YAML config), LangChain (Runnable chains), and Google ADK (Agent class with name/model/instruction/tools) all define agents as configurations rather than code. Jerry's existing markdown-with-YAML-frontmatter format is already this pattern. The portability layer does not require a new agent definition format -- it extends the existing one with portable metadata.

### Finding 5: Chain-of-Thought and Few-Shot Must Be Model-Adaptive

E-001 cited 2025 research showing that explicit CoT degrades performance on frontier models (GPT-o3, Claude Opus 4, Gemini 2.5 Pro) while remaining beneficial for smaller open-source models. E-001 also cited over-prompting research showing model-dependent sensitivity to few-shot example count. The architecture must make reasoning strategy and example injection configurable per provider-model pair, not hardcoded in agent definitions.

### Finding 6: Open-Source Model Support Requires Infrastructure Delegation

E-001 documented at least five distinct chat template formats across open-source models, with system message support not universal. E-002 identified LiteLLM as the ecosystem-standard solution, used by Google ADK and CrewAI for cross-provider API normalization. The architecture should delegate open-source model template handling to LiteLLM rather than implementing custom template rendering.

### Finding 7: Jerry's Current Agent Format Uses Anthropic-Specific Constructs

Jerry's existing agents use XML-structured bodies (`<agent>`, `<identity>`, `<capabilities>`, `<guardrails>`) which are Anthropic-optimized. E-001 classified XML tag dependence as Anti-Pattern 1 for portability. The portability architecture must define how to transform XML-structured bodies into provider-appropriate formats without requiring agents to abandon their current structure.

---

## L2: Detailed Analysis

### Two-Layer Architecture Design

The portability architecture consists of two layers: a Semantic Layer that captures provider-agnostic agent intent, and a Rendering Layer that transforms semantic definitions into provider-optimized prompts.

#### Semantic Layer (Portable)

The Semantic Layer is the agent definition as it exists in the repository -- the markdown file with YAML frontmatter. Portable fields in this layer express what the agent is, what it does, what constraints it operates under, and what outputs it produces. The Semantic Layer is the single source of truth for agent behavior.

**Semantic Layer responsibilities:**
- Agent identity: role, expertise, cognitive mode
- Behavioral constraints: forbidden actions, guardrails, constitutional compliance
- Tool definitions: name, description, parameters (JSON Schema)
- Output specifications: schema, required fields, format
- Capability requirements: minimum context window, required features (tool use, structured output, vision)
- Reasoning strategy preference: adaptive, explicit_cot, none

**Semantic Layer guarantees:**
- Every field in the Semantic Layer has a defined interpretation regardless of provider
- No field in the Semantic Layer references provider-specific API parameters, message roles, or syntax
- The Semantic Layer alone is sufficient to understand agent behavior (even without a Rendering Layer, the agent definition is human-readable and unambiguous)

#### Rendering Layer (Provider-Specific)

The Rendering Layer is a set of declarative transformation rules expressed as YAML configuration files -- one per provider target. These rules specify how to convert Semantic Layer fields into the prompt format, message structure, and API parameters that a specific provider expects.

**Rendering Layer responsibilities:**
- System prompt assembly: ordering, section delimiters, structural syntax
- Message role mapping: semantic roles to provider-specific roles
- Structured output enforcement: schema to provider-native mechanism
- Tool calling envelope: JSON Schema to provider-specific registration format
- Reasoning strategy injection: model-capability-aware CoT handling
- Context window budgeting: token allocation with provider-specific tokenizer awareness

**Rendering Layer implementation constraint (from PLAN.md R-010):**
The Rendering Layer is NOT compiled adapter code. It is a set of YAML configuration files that describe transformation rules. The actual transformation is performed by the agent invocation infrastructure at runtime. This keeps the portability layer within Jerry's markdown-and-YAML paradigm.

**Rendering Layer file structure:**

```
.context/portability/
  providers/
    anthropic.yaml      # Claude-family rendering rules
    openai.yaml         # GPT-family rendering rules
    google.yaml         # Gemini-family rendering rules
    open-source.yaml    # LiteLLM-mediated open-source rendering rules
  schemas/
    agent-portable.schema.yaml   # Portable agent definition schema
    provider-adapter.schema.yaml # Provider adapter configuration schema
  validation/
    portability-tests.yaml       # Testable portability validation criteria
```

#### Layer Interaction Model

```
Agent Definition File (Semantic Layer)
  skills/{skill}/agents/{agent}.md
  Contains: YAML frontmatter + markdown body
       |
       v
Provider Adapter Config (Rendering Layer)
  .context/portability/providers/{provider}.yaml
  Contains: Transformation rules for prompt assembly
       |
       v
Rendered Prompt (Runtime Output)
  Provider-specific system prompt, message sequence, tool registrations
  Consumed by: LLM API (directly or via LiteLLM proxy)
```

The Semantic Layer is authored by skill developers. The Rendering Layer is authored once per provider by framework maintainers. Skill developers never interact with the Rendering Layer directly -- their agent definitions are portable by default if they use only portable fields.

### Agent Definition Schema

This is the universal agent definition format for all /eng-team and /red-team agents. Each field is classified by portability:

- **portable**: Field value transfers across providers without modification
- **adaptation-required**: Field value is semantically portable but the rendering mechanism differs per provider
- **non-portable**: Field value is meaningful only for a specific provider

#### Identity Fields

| Field | Type | Portability | Description |
|-------|------|-------------|-------------|
| `name` | string | portable | Agent identifier (e.g., `eng-architect`, `red-recon`) |
| `version` | string | portable | Semantic version of the agent definition |
| `description` | string | portable | One-line description of agent purpose and invocation triggers |
| `identity.role` | string | portable | Human-readable role title (e.g., "Solution Architect", "Reconnaissance Specialist") |
| `identity.expertise` | list[string] | portable | Domain expertise areas |
| `identity.cognitive_mode` | enum | portable | `divergent`, `convergent`, `integrative`, `systematic`, `strategic`, `forensic` |
| `persona.tone` | string | portable | Communication tone (e.g., `professional`, `analytical`, `technical`) |
| `persona.communication_style` | string | portable | Interaction style (e.g., `consultative`, `evidence-based`, `direct`) |
| `persona.audience_level` | string | portable | Target audience (e.g., `L0`, `L1`, `L2`, `adaptive`) |

#### Capability Fields

| Field | Type | Portability | Description |
|-------|------|-------------|-------------|
| `capabilities.allowed_tools` | list[string] | adaptation-required | Tool identifiers. Core tools (Read, Write, Edit, Glob, Grep, Bash) are portable. MCP tools (Context7, Memory-Keeper) require provider-specific registration. WebSearch/WebFetch availability varies. |
| `capabilities.output_formats` | list[string] | portable | Supported output formats (markdown, yaml, json) |
| `capabilities.forbidden_actions` | list[string] | portable | Constitutional prohibitions in natural language |
| `capabilities.required_features` | list[string] | adaptation-required | Required provider features: `tool_use`, `structured_output`, `vision`, `streaming`. Adapter maps to provider capability check. |
| `model` | string | adaptation-required | Model preference. Current: `opus`, `sonnet`, `haiku`, `auto`. Portable format: `{provider}/{model}` (e.g., `anthropic/claude-sonnet-4`). Adapter maps preference to available model. |

#### Guardrail Fields

| Field | Type | Portability | Description |
|-------|------|-------------|-------------|
| `guardrails.input_validation` | list[object] | portable | Regex patterns for input validation. Provider-agnostic -- applied before LLM invocation. |
| `guardrails.output_filtering` | list[string] | portable | Output filtering rules in natural language (e.g., `no_secrets_in_output`, `all_claims_must_have_citations`). Applied post-generation. |
| `guardrails.fallback_behavior` | enum | portable | Behavior on failure: `warn_and_retry`, `warn_and_halt`, `escalate_to_user` |
| `guardrails.safety` | object | non-portable | Provider-specific safety API configuration. Anthropic: Constitutional AI parameters. OpenAI: Moderation API config. Google: Safety settings. Defined in provider adapter, not in agent definition. |

#### Tool Schema Fields

| Field | Type | Portability | Description |
|-------|------|-------------|-------------|
| `tools[].name` | string | portable | Tool function name |
| `tools[].description` | string | portable | Natural language description of tool purpose |
| `tools[].parameters` | JSON Schema | portable | Parameter schema using JSON Schema vocabulary. All providers have converged on this format (E-001 Finding 3, E-002 Finding 3). |
| `tools[].required` | list[string] | portable | Required parameter names |
| `tools[].invocation` | object | non-portable | Provider-specific invocation envelope. Defined in provider adapter config, not in agent definition. Anthropic: `tool_choice.type`. OpenAI: `tool_choice`. Google: `function_calling_config.mode`. |

#### Output Schema Fields

| Field | Type | Portability | Description |
|-------|------|-------------|-------------|
| `output.schema` | JSON Schema | portable | Expected output structure defined as JSON Schema. Universal lingua franca per E-001 Finding 2. |
| `output.required` | boolean | portable | Whether structured output is mandatory |
| `output.location` | string | portable | Repository path template for persisted output |
| `output.template` | string | portable | Reference to output template file |
| `output.levels` | list[enum] | portable | Required output levels: `L0`, `L1`, `L2` |
| `output.enforcement` | object | non-portable | Provider-specific enforcement mechanism. Defined in provider adapter config. OpenAI: `response_format`. Anthropic: tool-call pattern. Google: `response_schema`. Open-source: Instructor/Outlines integration. |

#### Portability Configuration Fields (New)

These fields are added to agent definitions that opt into multi-provider support.

| Field | Type | Portability | Description |
|-------|------|-------------|-------------|
| `portability.enabled` | boolean | portable | Whether this agent definition has been validated for multi-provider use. Default: `false` (Anthropic-only, backward-compatible). |
| `portability.minimum_context_window` | integer | portable | Minimum context window required (in tokens). Used for model compatibility checking. |
| `portability.model_preferences` | list[string] | adaptation-required | Ordered model preference list for fallback. Format: `{provider}/{model}`. E.g., `["anthropic/claude-sonnet-4", "openai/gpt-4o", "google/gemini-2.0-flash"]` |
| `portability.reasoning_strategy` | enum | adaptation-required | `adaptive` (renderer decides based on model capability), `explicit_cot` (always include step-by-step), `none` (no reasoning injection). Default: `adaptive`. |
| `portability.few_shot.enabled` | boolean | portable | Whether few-shot examples are used |
| `portability.few_shot.examples_ref` | string | portable | Path to external examples file |
| `portability.few_shot.count_range` | object | adaptation-required | `{min: 1, max: 3}`. Renderer selects optimal count per model. |
| `portability.body_format` | enum | portable | Format of the agent body below the frontmatter. `xml` (current Jerry default, Anthropic-optimized), `markdown` (portable), `rccf` (Role-Context-Constraints-Format, maximally portable). |

#### Portability Classification Summary

| Classification | Count | Percentage | Fields |
|----------------|-------|------------|--------|
| portable | 24 | 63% | identity, persona, guardrails (input/output), tool schemas, output schema, output location/template/levels, few-shot config, body format |
| adaptation-required | 9 | 24% | allowed_tools, required_features, model, model_preferences, reasoning_strategy, few_shot.count_range, output.enforcement (at adapter level), tool invocation (at adapter level) |
| non-portable | 5 | 13% | guardrails.safety, tools[].invocation, output.enforcement, provider-specific extensions (extended_thinking, reasoning_effort, grounding) |

### Provider Adapter Specifications

Each provider adapter is a YAML configuration file that defines transformation rules for rendering portable agent definitions into provider-specific prompts. Adapters do not contain executable code -- they are declarative configurations consumed by the invocation infrastructure.

#### Anthropic (Claude) Adapter

```yaml
# .context/portability/providers/anthropic.yaml
provider:
  name: anthropic
  api_format: anthropic-messages
  models:
    - id: claude-opus-4
      context_window: 200000
      features: [tool_use, structured_output_via_tools, extended_thinking, vision, streaming]
      reasoning: built_in
    - id: claude-sonnet-4
      context_window: 200000
      features: [tool_use, structured_output_via_tools, vision, streaming]
      reasoning: built_in
    - id: claude-haiku-3.5
      context_window: 200000
      features: [tool_use, structured_output_via_tools, vision, streaming]
      reasoning: limited

rendering:
  system_prompt:
    placement: separate_api_parameter  # Not in messages array
    structure: xml_preferred  # Claude trained on XML; use if body_format=xml
    section_delimiters:
      xml: "<{section}>\n{content}\n</{section}>"
      markdown: "## {section}\n{content}"
      rccf: "{LABEL}:\n{content}"
    section_order: [identity, context, constraints, format, tools]

  structured_output:
    mechanism: tool_call_workaround
    description: >
      Define a "tool" whose parameters match the desired output schema.
      Force tool use via tool_choice: {"type": "any"}.
      Extract the tool call arguments as the structured output.
    schema_placement: tools_array
    force_use: 'tool_choice: {"type": "any"}'

  tool_calling:
    format: anthropic_tools
    schema_location: top_level_tools_array
    envelope: |
      {
        "name": "{tool_name}",
        "description": "{tool_description}",
        "input_schema": {json_schema}
      }
    parallel_calling: true
    forced_use: 'tool_choice: {"type": "any"}'

  reasoning:
    strategy_map:
      adaptive: omit  # Claude Opus 4 / Sonnet 4 have built-in reasoning; do not inject CoT
      explicit_cot: inject_step_by_step  # For haiku or when explicitly requested
      none: omit
    extended_thinking:
      available: true
      api_param: "thinking.type = enabled, thinking.budget_tokens = {budget}"
      note: "Provider-exclusive. Omit for portable definitions."

  context_window:
    tokenizer: anthropic_bpe
    budget_strategy: >
      Reserve 20% for output. Allocate remaining 80% as:
      system prompt (15%), tools (10%), conversation history (55%).
    cache_strategy: >
      Use prompt caching for system prompt and tool definitions.
      Cached prefix receives token discount.

  message_roles:
    system: separate_parameter  # Not a message role
    user: "user"
    assistant: "assistant"
    alternation: strict  # API enforces human/assistant alternation
```

#### OpenAI (GPT) Adapter

```yaml
# .context/portability/providers/openai.yaml
provider:
  name: openai
  api_format: openai-chat-completions
  models:
    - id: gpt-4o
      context_window: 128000
      features: [tool_use, structured_output_native, vision, streaming]
      reasoning: built_in
    - id: gpt-4.1
      context_window: 1000000
      features: [tool_use, structured_output_native, vision, streaming]
      reasoning: built_in
    - id: o3
      context_window: 200000
      features: [tool_use, structured_output_native, reasoning_effort]
      reasoning: deep_built_in

rendering:
  system_prompt:
    placement: system_message_role  # system role in messages array
    structure: markdown_preferred  # GPT handles markdown well; XML supported but not optimized
    section_delimiters:
      xml: "<{section}>\n{content}\n</{section}>"  # Functional but not optimized
      markdown: "## {section}\n{content}"
      rccf: "{LABEL}:\n{content}"
    section_order: [identity, context, constraints, format, tools]

  structured_output:
    mechanism: native_response_format
    description: >
      Use response_format with json_schema type for server-side enforcement.
      100% schema compliance guaranteed.
    schema_placement: response_format_parameter
    api_param: |
      response_format: {
        "type": "json_schema",
        "json_schema": {
          "name": "{schema_name}",
          "schema": {json_schema},
          "strict": true
        }
      }

  tool_calling:
    format: openai_functions
    schema_location: top_level_tools_array
    envelope: |
      {
        "type": "function",
        "function": {
          "name": "{tool_name}",
          "description": "{tool_description}",
          "parameters": {json_schema}
        }
      }
    parallel_calling: true
    forced_use: 'tool_choice: "required"'

  reasoning:
    strategy_map:
      adaptive: omit  # GPT-4o / o3 have built-in reasoning
      explicit_cot: inject_step_by_step  # For gpt-4o-mini or when explicitly requested
      none: omit
    reasoning_effort:
      available: true  # o3 series only
      api_param: "reasoning_effort: {low|medium|high}"
      note: "Provider-exclusive. Omit for portable definitions."

  context_window:
    tokenizer: openai_tiktoken
    budget_strategy: >
      Reserve 20% for output. Allocate remaining 80% as:
      system prompt (15%), tools (10%), conversation history (55%).
    cache_strategy: >
      Automatic prompt caching on eligible prefixes.

  message_roles:
    system: "system"
    user: "user"
    assistant: "assistant"
    alternation: flexible  # No strict alternation requirement
```

#### Google (Gemini) Adapter

```yaml
# .context/portability/providers/google.yaml
provider:
  name: google
  api_format: google-generative-ai
  models:
    - id: gemini-2.5-pro
      context_window: 1000000
      features: [tool_use, structured_output_native, vision, grounding, streaming]
      reasoning: built_in_thinking
    - id: gemini-2.0-flash
      context_window: 1000000
      features: [tool_use, structured_output_native, vision, streaming]
      reasoning: built_in

rendering:
  system_prompt:
    placement: system_instruction_config  # system_instruction in generation config
    structure: markdown_preferred
    section_delimiters:
      xml: "<{section}>\n{content}\n</{section}>"  # Supported but not optimized
      markdown: "## {section}\n{content}"
      rccf: "{LABEL}:\n{content}"
    section_order: [identity, context, constraints, format, tools]

  structured_output:
    mechanism: native_response_schema
    description: >
      Use response_schema in generation config for server-side enforcement.
    schema_placement: generation_config_parameter
    api_param: |
      generation_config: {
        "response_mime_type": "application/json",
        "response_schema": {json_schema}
      }

  tool_calling:
    format: google_function_declarations
    schema_location: tools_array
    envelope: |
      {
        "function_declarations": [{
          "name": "{tool_name}",
          "description": "{tool_description}",
          "parameters": {json_schema}
        }]
      }
    parallel_calling: true
    forced_use: 'function_calling_config: {"mode": "ANY"}'

  reasoning:
    strategy_map:
      adaptive: omit  # Gemini 2.5 Pro has built-in thinking
      explicit_cot: inject_step_by_step  # For flash models
      none: omit
    grounding:
      available: true
      note: "Provider-exclusive Google Search grounding. Omit for portable definitions."

  context_window:
    tokenizer: google_sentencepiece
    budget_strategy: >
      Reserve 20% for output. Context caching API available for large prefixes.
    cache_strategy: >
      Use context caching API for system instructions and tool definitions.

  message_roles:
    system: system_instruction  # Separate from message roles
    user: "user"
    assistant: "model"  # Google uses "model" not "assistant"
    alternation: flexible
```

#### Open-Source (Ollama/vLLM) Adapter

```yaml
# .context/portability/providers/open-source.yaml
provider:
  name: open-source
  api_format: openai-compatible-via-litellm
  infrastructure: litellm  # LiteLLM handles chat template rendering
  models:
    - id: llama3.1:70b
      context_window: 128000
      features: [tool_use_via_litellm, streaming]
      reasoning: requires_explicit_cot
      system_message_support: true
    - id: mistral-large
      context_window: 128000
      features: [tool_use_native, streaming]
      reasoning: built_in
      system_message_support: false  # Mistral Instruct lacks native system role
    - id: gemma-2:27b
      context_window: 8192
      features: [streaming]
      reasoning: requires_explicit_cot
      system_message_support: false

rendering:
  system_prompt:
    placement: delegated_to_litellm
    description: >
      LiteLLM automatically detects model family and applies correct chat template.
      System messages are injected as system role where supported, or prepended to
      user message where not supported (Mistral, Gemma).
    structure: rccf_preferred  # Maximally portable plain-text structure
    section_delimiters:
      rccf: "{LABEL}:\n{content}"  # Safest for diverse tokenizers
      markdown: "## {section}\n{content}"  # Supported by most models
    section_order: [identity, constraints, context, format, tools]
    # Note: constraints before context for open-source models due to weaker instruction following

  structured_output:
    mechanism: prompt_level_with_optional_library
    description: >
      Include JSON Schema in prompt text as the baseline.
      Optionally use Instructor or Outlines for constrained generation
      when running against vLLM or compatible inference servers.
    schema_placement: prompt_text
    enforcement: best_effort  # Cannot guarantee 100% compliance without Instructor/Outlines
    fallback: >
      If structured output fails validation, retry with explicit format reminder.
      After 3 failures, return raw output with validation errors noted.

  tool_calling:
    format: openai_compatible_via_litellm
    description: >
      LiteLLM translates OpenAI tool calling format to model-native format.
      Ollama and vLLM support tool calling for compatible models.
    schema_location: delegated_to_litellm
    parallel_calling: model_dependent
    forced_use: not_universally_supported

  reasoning:
    strategy_map:
      adaptive: inject_step_by_step  # Most open-source models benefit from explicit CoT
      explicit_cot: inject_step_by_step
      none: omit
    cot_injection: >
      Append to system prompt: "Think through your response step by step before
      providing your final answer. Show your reasoning."
    note: >
      E-001 Finding 4: CoT remains beneficial for smaller open-source models
      that lack built-in reasoning chains.

  context_window:
    tokenizer: model_specific  # Each model has its own tokenizer
    budget_strategy: >
      Conservative allocation: reserve 30% for output (open-source models
      are less reliable with long outputs). Budget system prompt at 10% max.
      For models with small context (< 32K), prioritize constraints and tools
      over context/examples.
    cache_strategy: >
      Use vLLM prefix caching or SGLang RadixAttention where available.
      Ollama provides no native caching.

  message_roles:
    system: delegated_to_litellm  # LiteLLM handles system message mapping
    user: "user"
    assistant: "assistant"
    alternation: model_dependent
```

### Portability Validation Criteria

These are testable properties that confirm an agent definition is portable. Each criterion becomes a test case for FEAT-043 Portability Validation in Phase 5.

#### Structural Validation (Static Analysis)

These tests can be run against agent definition files without invoking any LLM.

| ID | Criterion | Test Method | Pass Condition |
|----|-----------|-------------|----------------|
| PV-001 | No provider-specific API parameters in frontmatter | Parse YAML frontmatter; check that no field references `response_format`, `tool_choice`, `function_calling_config`, `extended_thinking`, `reasoning_effort`, or `system_instruction` | Zero provider-specific API parameter references |
| PV-002 | All tool definitions use JSON Schema | Parse `tools[].parameters` fields; validate each against JSON Schema metaschema | All tool parameter schemas are valid JSON Schema |
| PV-003 | Output schema is JSON Schema | Parse `output.schema` field; validate against JSON Schema metaschema | Output schema is valid JSON Schema |
| PV-004 | No hardcoded chat template tokens | Grep agent body for `<\|begin_of_text\|>`, `[INST]`, `<start_of_turn>`, `<\|system\|>`, `<\|user\|>` | Zero chat template token matches |
| PV-005 | No hardcoded CoT instructions (when reasoning_strategy != explicit_cot) | Grep agent body for "step by step", "think through", "chain of thought" when `portability.reasoning_strategy` is `adaptive` or `none` | Zero hardcoded CoT instructions |
| PV-006 | Model preference uses portable format | Parse `portability.model_preferences`; validate each entry matches `{provider}/{model}` format | All entries match format |
| PV-007 | Required features are declared | If agent uses tool calling, `capabilities.required_features` includes `tool_use`. If agent requires structured output, list includes `structured_output`. | All implicit feature dependencies explicitly declared |
| PV-008 | Context window requirement is declared | `portability.minimum_context_window` is set and is a positive integer | Field present and valid |
| PV-009 | Body format is declared | `portability.body_format` is set to `xml`, `markdown`, or `rccf` | Field present and valid enum value |
| PV-010 | Portability flag is set | `portability.enabled` is `true` | Field is true |

#### Behavioral Validation (Requires LLM Invocation)

These tests require actually invoking the agent across providers and comparing outputs.

| ID | Criterion | Test Method | Pass Condition |
|----|-----------|-------------|----------------|
| PV-011 | Agent produces valid structured output on all target providers | Invoke agent with identical input on each provider; validate output against `output.schema` | Output validates against schema on all providers |
| PV-012 | Agent uses declared tools correctly on all target providers | Invoke agent with input requiring tool use; verify tool calls match expected schema | Tool call parameters validate against `tools[].parameters` schema on all providers |
| PV-013 | Agent respects constraints on all target providers | Invoke agent with input that should trigger constraint enforcement (forbidden action, guardrail); verify constraint is respected | Constraint enforced on all providers |
| PV-014 | Agent identity is consistent across providers | Invoke agent with identity-probing input; compare role, expertise, and tone across providers | Role and expertise references are semantically equivalent across providers |
| PV-015 | Agent output quality does not degrade significantly across providers | Invoke agent with benchmark input on each provider; score outputs using S-014 LLM-as-Judge dimensions | Weighted composite score >= 0.85 on all providers (allowing 0.07 degradation from primary provider threshold of 0.92) |
| PV-016 | Agent gracefully degrades on capability-limited models | Invoke agent on a model that lacks a declared optional feature (e.g., no tool use); verify agent completes task via fallback path | Agent produces usable output without crashing or producing empty results |

#### Regression Validation (Backward Compatibility)

| ID | Criterion | Test Method | Pass Condition |
|----|-----------|-------------|----------------|
| PV-017 | Existing agents without portability section work unchanged | Invoke existing Jerry agents (no `portability` field) on Anthropic; verify identical behavior | Output matches pre-portability-layer behavior |
| PV-018 | Portability section is optional | Remove `portability` section from a portable agent; invoke on Anthropic; verify it works | Agent functions correctly without portability metadata |

### Jerry Framework Integration

#### Integration with SKILL.md

SKILL.md files define skill-level metadata (description, agents, triggers, routing). The portability layer does not modify SKILL.md structure. Instead, SKILL.md gains an optional `portability` section that declares skill-level portability status:

```yaml
# In SKILL.md frontmatter
portability:
  status: validated  # validated | partial | anthropic-only
  validated_providers: [anthropic, openai, google]
  validation_date: "2026-03-15"
  validation_report: "work/research/stream-e-llm-portability/validation-report-eng-team.md"
```

This allows the `/eng-team` and `/red-team` skills to declare their portability status at the skill level, with per-agent portability tracked in individual agent definition files.

#### Integration with Agent Definition Files

Existing agent definition files gain the optional `portability` section in YAML frontmatter. The agent body (below the frontmatter fence `---`) remains unchanged. The Rendering Layer reads the frontmatter `portability` fields and the `portability.body_format` field to determine how to render the body.

**Example: Portable eng-architect agent frontmatter addition**

```yaml
---
name: eng-architect
version: "1.0.0"
description: "Solution Architect agent for /eng-team"
model: opus

identity:
  role: "Solution Architect"
  expertise:
    - "System design and ADR production"
    - "Threat modeling (STRIDE/DREAD)"
    - "Architecture review"
  cognitive_mode: "strategic"

# ... existing fields (persona, capabilities, guardrails, etc.) ...

# NEW: Portability configuration
portability:
  enabled: true
  minimum_context_window: 128000
  model_preferences:
    - "anthropic/claude-opus-4"
    - "openai/gpt-4o"
    - "google/gemini-2.5-pro"
    - "ollama/llama3.1:70b"
  reasoning_strategy: adaptive
  few_shot:
    enabled: false
  body_format: markdown  # Use portable markdown instead of XML
---
```

#### Integration with AGENTS.md

AGENTS.md gains a portability status column in agent summary tables:

```markdown
| Agent | File | Role | Portability |
|-------|------|------|-------------|
| eng-architect | `skills/eng-team/agents/eng-architect.md` | Solution Architect | validated |
| eng-lead | `skills/eng-team/agents/eng-lead.md` | Technical Lead | validated |
```

#### Integration with Existing Skill Routing

Jerry's skill routing (SKILL.md routing rules) is provider-agnostic -- it routes based on user input keywords and agent capabilities, not on LLM provider. The portability layer adds one new routing consideration: if a specific provider is requested (e.g., via environment variable `JERRY_LLM_PROVIDER=openai`), the routing layer consults the agent's `portability.model_preferences` to select the appropriate model and `portability.enabled` to verify the agent supports that provider.

#### Integration with /adversary Quality Enforcement

The /adversary skill's adv-scorer agent (S-014 LLM-as-Judge) operates on agent outputs, not on agent definitions. The portability layer does not change how /adversary scores deliverables. However, PV-015 (cross-provider quality consistency) uses the same S-014 scoring rubric to validate that an agent's output quality does not degrade when rendered for a different provider.

#### Integration with Provider Adapter Config

The `.context/portability/providers/` directory is loaded by the invocation infrastructure at runtime. Provider adapter configs are NOT loaded into agent context -- they are consumed by the orchestration layer that assembles the final API call. This keeps agent context windows clean of adapter configuration.

### Migration Path

#### Phase 1: Backward-Compatible Foundation (No Existing Agent Changes)

1. Create `.context/portability/` directory structure with provider adapter configs
2. Create `agent-portable.schema.yaml` defining the portable schema
3. All existing agents continue to work unchanged -- `portability.enabled` defaults to `false`, meaning existing agents render exclusively for Anthropic using their current XML body format
4. No changes to any of the 37 existing agents

#### Phase 2: New Agent Authoring (PROJ-010 Agents)

1. Author all /eng-team and /red-team agents with `portability.enabled: true`
2. Use `body_format: markdown` for agent bodies (portable alternative to XML)
3. Use RCCF pattern (Role-Context-Constraints-Format) for system prompt structure
4. Include `portability.model_preferences` with ordered fallback list
5. Define `portability.reasoning_strategy: adaptive` as default
6. Validate each agent against PV-001 through PV-010 (static validation)

#### Phase 3: Cross-Provider Validation (Phase 5 of PROJ-010)

1. Execute PV-011 through PV-016 (behavioral validation) for all /eng-team and /red-team agents
2. Document results in portability validation report
3. Iterate on provider adapter configs based on validation findings
4. Achieve PV-015 threshold (>= 0.85 composite score on all target providers)

#### Phase 4: Existing Agent Migration (Optional, Post-PROJ-010)

For teams that want to migrate existing Jerry agents to portable definitions:

1. Add `portability` section to YAML frontmatter
2. Convert XML body tags to markdown equivalents:
   - `<identity>` content becomes `## Identity` section
   - `<capabilities>` content becomes `## Capabilities` section
   - `<guardrails>` content becomes `## Guardrails` section
   - `<constitutional_compliance>` becomes `## Constitutional Compliance` section
   - All other `<section>` tags follow the same pattern
3. Replace XML structural markers in prompt text (Anti-Pattern 1 from E-001):
   - `<instructions>...</instructions>` becomes `## Instructions\n...\n`
   - `<context>...</context>` becomes `## Context\n...\n`
4. Run PV-001 through PV-010 static validation
5. Run PV-017 regression test to ensure Anthropic behavior is unchanged
6. Optionally run PV-011 through PV-016 behavioral validation on target providers

**Backward Compatibility Guarantees:**

| Guarantee | Mechanism |
|-----------|-----------|
| Existing agents work without modification | `portability.enabled` defaults to `false`; Anthropic rendering is the default |
| Existing XML body format is preserved | `body_format: xml` is explicitly supported; Anthropic adapter renders XML natively |
| No existing SKILL.md changes required | `portability` section in SKILL.md is optional |
| No existing AGENTS.md changes required | Portability column is optional |
| No new dependencies on PROJ-010 code | Provider adapter configs are YAML files, not code |
| Gradual opt-in | Each agent migrates independently; no all-or-nothing cutover |

---

## Recommendations

### R-PORT-ARCH-001: Implement the Two-Layer Architecture

Implement the Semantic Layer (agent definition files) and Rendering Layer (provider adapter YAML configs) as described in the Two-Layer Architecture Design section. The Semantic Layer is the existing agent definition format extended with a `portability` section. The Rendering Layer is a new `.context/portability/providers/` directory containing one YAML config per provider.

**Rationale:** E-001 and E-002 independently converge on the same conclusion: separating semantic intent from provider-specific rendering is the only architecture that achieves portability without sacrificing provider-specific optimization. DSPy proves this principle with compiled prompts; this architecture achieves the same separation with declarative configuration.

### R-PORT-ARCH-002: Use Markdown Body Format as the Portable Default for New Agents

All /eng-team and /red-team agents should use `body_format: markdown` instead of XML tags. Markdown headers (`##`) provide equivalent structural organization to XML tags and are universally supported across all providers (E-001 Anti-Pattern 1, Finding on portable alternatives).

**Rationale:** XML tags are Anthropic-optimized (E-001 evidence). Markdown provides 90%+ of the organizational benefit universally. New agents should start portable; migration of existing agents is optional.

### R-PORT-ARCH-003: Standardize on JSON Schema for All Tool and Output Definitions

All tool parameter schemas and output schemas in /eng-team and /red-team agents must be expressed as JSON Schema. This is the most settled portable element across all providers and all frameworks (E-001 Finding 3, E-002 Finding 3).

**Rationale:** JSON Schema is the universal tool definition format. All eight frameworks analyzed in E-002 use it. All four major providers support it natively for tool calling.

### R-PORT-ARCH-004: Make Reasoning Strategy Adaptive by Default

All /eng-team and /red-team agents should set `portability.reasoning_strategy: adaptive`. The Rendering Layer injects CoT instructions only for models that benefit from them (open-source, smaller models) and omits them for frontier models with built-in reasoning.

**Rationale:** E-001 Finding 4 (2025 research) demonstrates that explicit CoT degrades performance on modern frontier models. A fixed strategy penalizes at least one provider class.

### R-PORT-ARCH-005: Declare Model Preferences as Ordered Fallback Lists

All portable agent definitions should include `portability.model_preferences` with at least two providers. This follows E-002's R-FW-004 (Haystack FallbackChatGenerator pattern) and enables operational resilience.

**Rationale:** No single provider is always available. Fallback chains are an operational requirement documented by Haystack and supported natively by LiteLLM proxy.

### R-PORT-ARCH-006: Delegate Open-Source Chat Template Handling to LiteLLM

Do not implement custom chat template rendering for open-source models. Use LiteLLM as the API translation layer for all open-source model interactions. LiteLLM handles chat template detection and application for 100+ models (E-001 Finding 6, E-002 R-FW-001).

**Rationale:** Chat template fragmentation is the single largest open-source portability barrier. LiteLLM solves it at infrastructure level, proven at scale by Google ADK and CrewAI.

### R-PORT-ARCH-007: Validate Portability as a Testable Property

Implement the 18 Portability Validation Criteria (PV-001 through PV-018) as automated tests in Phase 5. Static validation tests (PV-001 through PV-010) should run in CI. Behavioral validation tests (PV-011 through PV-016) should run as a dedicated validation suite.

**Rationale:** R-010 requires that portability "MUST be validated as a testable property." The PV criteria translate this requirement into concrete, executable test cases.

### R-PORT-ARCH-008: Preserve Backward Compatibility with Existing Agents

The `portability` section must be optional. All 37 existing Jerry agents must continue to function without modification. The default behavior (no `portability` section) must render exclusively for Anthropic using the existing XML body format.

**Rationale:** PROJ-010 introduces portability for new agents. Forcing migration of existing agents would be a disruptive, out-of-scope change that violates the principle of minimal blast radius.

### R-PORT-ARCH-009: Externalize Few-Shot Examples as Configurable Resources

Agent definitions that use few-shot examples should reference an external examples file (`portability.few_shot.examples_ref`) rather than embedding examples in the prompt body. The Rendering Layer selects the optimal example count per model within the declared `count_range`.

**Rationale:** E-001 Finding 5 (over-prompting research, 2025) demonstrates that optimal example count is model-dependent. Fixed embedding prevents per-model optimization.

### R-PORT-ARCH-010: Declare Minimum Capability Requirements per Agent

All portable agents must declare `capabilities.required_features` listing the provider features they depend on (e.g., `tool_use`, `structured_output`, `vision`). The invocation infrastructure checks declared requirements against the selected model's capability profile before invocation.

**Rationale:** An agent that silently fails because a model lacks tool calling is worse than an agent that explicitly refuses to run. Declared requirements enable pre-flight capability checking.

### R-PORT-ARCH-011: Use RCCF Pattern for System Prompt Assembly

Provider adapters should assemble system prompts following the RCCF pattern (Role-Context-Constraints-Format) identified in E-001 as the highest-portability structure. The section ordering may be adjusted per provider (e.g., open-source adapter places constraints before context due to weaker instruction following in smaller models).

**Rationale:** RCCF works across all providers because it leverages universal primacy bias and hierarchical instruction processing (E-001 Pattern 1). Provider adapters can adjust ordering while preserving the same semantic sections.

### R-PORT-ARCH-012: Implement Graceful Degradation for Capability-Limited Models

Agent definitions should distinguish between required and optional capabilities. When invoked on a model that lacks an optional capability (e.g., no structured output enforcement), the agent should degrade gracefully -- using prompt-level schema instructions instead of native enforcement, or skipping vision-dependent steps -- rather than failing entirely.

**Rationale:** Not all target environments will have frontier models. Red team agents may need to run on air-gapped systems with local open-source models. Graceful degradation ensures operational viability across deployment contexts.

---

## Evidence and Citations

### From E-001: Universal Prompt Engineering Patterns

| Finding | Evidence | Source |
|---------|----------|--------|
| RCCF pattern is universally portable | Tested across Anthropic, OpenAI, Google, and open-source models | E-001 Pattern 1; [Lakera Prompt Engineering Guide 2026](https://www.lakera.ai/blog/prompt-engineering-guide) |
| JSON Schema is the universal tool definition format | All major providers support JSON Schema for tool parameters | E-001 Finding 3, Pattern 5; [Structured Output Comparison across LLM Providers](https://medium.com/@rosgluk/structured-output-comparison-across-popular-llm-providers-openai-gemini-anthropic-mistral-and-1a5d42fa612a) |
| XML tags are Anthropic-specific optimization | Claude trained on XML; other providers treat XML as plain text | E-001 Anti-Pattern 1; [Anthropic: XML tags in prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags) |
| Explicit CoT degrades frontier model performance | 2025 benchmarks show CoT not universally beneficial | E-001 Finding 4; [Chain-of-Thought Hub benchmarks](https://github.com/FranxYao/chain-of-thought-hub) (TMLR 2025) |
| Few-shot example count is model-dependent | Over-prompting phenomenon documented in 2025 | E-001 Finding 5; [The Few-shot Dilemma: Over-prompting LLMs](https://arxiv.org/html/2509.13196v1) |
| Chat template fragmentation across open-source models | At least 5 distinct formats; system message support not universal | E-001 Finding 6; [LiteLLM: Prompt Formatting](https://docs.litellm.ai/docs/completion/prompt_formatting); [Hugging Face: Chat Templates](https://huggingface.co/learn/llm-course/chapter11/2) |
| Structured output mechanisms fundamentally differ per provider | OpenAI: `response_format` (server-side); Anthropic: tool-call workaround; Google: `response_schema`; OSS: prompt-level | E-001 Finding 2; [OpenAI: Structured Outputs](https://openai.com/index/introducing-structured-outputs-in-the-api/) |
| System prompt handling differs per provider | Anthropic: separate API param; OpenAI: system message role; Google: system_instruction config; OSS: varies | E-001 Finding 1; Provider documentation |

### From E-002: Multi-LLM Agent Framework Analysis

| Finding | Evidence | Source |
|---------|----------|--------|
| Industry converged on OpenAI format as de facto standard | LiteLLM, LangChain, CrewAI, Haystack, Google ADK, AutoGen all use OpenAI message format | E-002 Finding 1; [LiteLLM Providers](https://docs.litellm.ai/docs/providers) |
| Agent-as-configuration is the dominant portable pattern | CrewAI YAML configs, LangChain Runnables, Google ADK Agent class | E-002 Finding 2, Cross-Cutting Pattern: Agent-as-Configuration |
| No framework solves optimal-prompt-per-model problem | All frameworks abstract API layer but do not optimize prompt content | E-002 Finding 4 |
| DSPy's semantic-intent separation principle is the theoretical ideal | Same signature compiles to different prompts per model | E-002 DSPy Analysis; [DSPy Official Site](https://dspy.ai/) |
| Haystack FallbackChatGenerator is a model resilience best practice | Sequential multi-model fallback with automatic failover | E-002 Finding 6; [Haystack GitHub](https://github.com/deepset-ai/haystack) |
| LiteLLM is the ecosystem-standard API translation layer | 100+ provider support; used by Google ADK and CrewAI | E-002 R-FW-001; [LiteLLM GitHub](https://github.com/BerriAI/litellm) |
| MCP and A2A are emerging interoperability standards | Adopted by Semantic Kernel, Google ADK, LiteLLM | E-002 Cross-Cutting Pattern: Protocol-Based Interoperability |
| CrewAI YAML config is closest to Jerry's agent format | role/goal/backstory/tools/llm in YAML | E-002 CrewAI Analysis; [CrewAI Agent Configuration](https://docs.crewai.com/core-concepts/Agents/) |

### Additional Sources

| Source | Date | Content |
|--------|------|---------|
| Jerry Framework AGENTS.md | 2026-02-20 | Agent definition template and schema; 37 existing agents across 8 skills |
| Jerry Framework PS_AGENT_TEMPLATE.md | 2026-01-11 | Federated core template v1.0 with YAML frontmatter schema |
| Jerry ps-researcher agent definition | 2026-02-14 | Real-world agent definition exemplifying current schema (v2.3.0) |
| Jerry adv-executor agent definition | 2026-02-15 | Real-world agent definition exemplifying current schema (v1.0.0) |
| [PromptBridge: Model-Adaptive Prompt Evolution](https://www.emergentmind.com/topics/prompt-based-llm-framework) | 2025 | Calibrated prompt transfer achieves up to +5pp gain via model-specific adaptation |
| [Inclusive Prompt Engineering Model (IPEM)](https://link.springer.com/article/10.1007/s10462-025-11330-7) | 2025 | Modular framework for adaptable, ethical prompt strategies |
| [Prompt Portability Discussion](https://community.openai.com/t/the-portability-of-a-llm-prompt/311147) | 2024 | Community analysis of prompt transfer challenges |
