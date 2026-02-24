# ADR-PROJ010-003: LLM Portability Architecture -- Two-Layer Semantic/Rendering Design

<!--
DOCUMENT-ID: ADR-PROJ010-003
AUTHOR: ps-architect agent
DATE: 2026-02-22
STATUS: PROPOSED
PARENT-FEATURE: FEAT-012 (LLM Portability Architecture)
PARENT-EPIC: EPIC-002 (Architecture & Design)
PROJECT: PROJ-010-cyber-ops
ADR-ID: ADR-PROJ010-003
TYPE: Architecture Decision Record
RESEARCH-SOURCES: E-001, E-002, E-003, S-002
-->

> **ADR ID:** ADR-PROJ010-003
> **Version:** 1.0.0
> **Date:** 2026-02-22
> **Author:** ps-architect
> **Status:** PROPOSED
> **Deciders:** User (P-020 authority), ps-architect (recommendation)
> **Quality Target:** >= 0.95
> **Parent Feature:** FEAT-012 (LLM Portability Architecture)
> **Parent Epic:** EPIC-002 (Architecture & Design)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | Current decision lifecycle stage and ratification requirements |
| [Context](#context) | Why this decision is needed, the problem it solves, and governing constraints |
| [Decision](#decision) | The two-layer architecture, 38-field portable schema, 4 provider adapters, RCCF prompt assembly, 18 validation criteria, backward compatibility, adaptive reasoning, and tool/output schema design |
| [Options Considered](#options-considered) | Four architectural approaches evaluated with evidence-based rationale |
| [Consequences](#consequences) | Positive, negative, and neutral outcomes with impact estimates |
| [Evidence Base](#evidence-base) | Consolidated findings from E-001, E-002, E-003, and S-002 |
| [Compliance](#compliance) | Jerry governance compliance assessment |
| [Related Decisions](#related-decisions) | Upstream and downstream decision linkages |
| [Open Questions](#open-questions) | Genuine ambiguities requiring Phase 2 or Phase 5 resolution |
| [References](#references) | Source citations with dates |

---

## Status

**PROPOSED** -- This ADR is ready for adversarial review and user ratification.

**Ratification requirements:**
1. Adversarial review by /adversary (C4 criticality, >= 0.95 quality threshold)
2. User ratification per P-020 (User Authority)

**Downstream dependency:** This ADR is the primary decision for FEAT-012 (LLM Portability Architecture). Downstream work -- Phase 3 and Phase 4 agent authoring, Phase 5 cross-provider validation -- is blocked until this ADR reaches ACCEPTED status.

---

## Context

### Why This Decision Is Needed

PROJ-010 requirement R-010 mandates that all agent definitions be portable across LLM providers: "All agent definitions MUST be portable across LLM providers (OpenAI, Gemini, Anthropic, open-source models). Agent logic MUST NOT depend on provider-specific features. Prompt engineering MUST use universal patterns. Portability MUST be validated as a testable property."

Without a formalized portability architecture, the 21 agents designed for /eng-team and /red-team would be implicitly locked to a single LLM provider. This creates three unacceptable risks for mission-critical cybersecurity tooling: (1) vendor lock-in reduces operational flexibility in sensitive environments, (2) air-gapped deployments may require local open-source models, and (3) provider outages could disable security operations with no fallback.

Jerry's existing 37 agents use Anthropic-specific constructs -- XML-structured bodies (`<agent>`, `<identity>`, `<capabilities>`, `<guardrails>`) that are Anthropic-optimized (E-001 Anti-Pattern 1). R-010 requires that PROJ-010 agents avoid this provider coupling while preserving backward compatibility with the existing agent fleet.

### Background

Phase 1 research produced three stream-E artifacts directly informing this decision:

- **E-001 (Universal Prompt Engineering Patterns):** Analyzed prompt portability across Anthropic, OpenAI, Google, and open-source models. Identified 6 universal patterns (RCCF structure, JSON Schema output, constraint-first ordering, persona via behavioral description, tool definitions via JSON Schema, guardrails via explicit rules) and 6 anti-patterns (XML tag dependence, OpenAI JSON mode assumption, CoT hardcoding, provider-specific role assumptions, tokenization behavior reliance, chat template hardcoding).

- **E-002 (Multi-LLM Agent Framework Analysis):** Analyzed 8 frameworks (LangChain, AutoGen, CrewAI, LiteLLM, Google ADK, Semantic Kernel, Haystack, DSPy). Identified 4 cross-cutting patterns: OpenAI format as lingua franca, agent-as-configuration, protocol-based interoperability (MCP/A2A), and fallback/multi-model chains. Found that no framework solves the "optimal prompt per model" problem -- only DSPy attempts it through compilation.

- **E-003 (Portability Architecture Recommendation):** Synthesized E-001 and E-002 into a concrete architecture: two-layer design with semantic and rendering layers, 38-field portable agent schema with portability classification, 4 provider adapter specifications, 18 portability validation criteria (PV-001 through PV-018), and a 4-phase backward-compatible migration path.

Additionally, **S-002 (Architecture Implications Synthesis)** cataloged AD-003 as a HIGH-confidence decision where independent research streams converged on the same conclusion.

### Constraints

| Constraint | Source | Impact on Architecture |
|------------|--------|------------------------|
| R-010: LLM Portability | PLAN.md | All 21 agents must be portable; portability must be testable |
| R-022: Agent standards compliance | PLAN.md | Agent definitions must follow Jerry agent-development-standards |
| Backward compatibility | 37 existing Jerry agents | Existing agents must work without modification |
| Jerry format paradigm | CLAUDE.md, architecture-standards | Solutions must use YAML frontmatter + markdown, not compiled code |
| P-003: No recursive subagents | Jerry Constitution (HARD) | Rendering layer cannot spawn nested agents |
| Single-model operational default | Jerry current architecture | Anthropic is the default provider; portability extends rather than replaces |
| R-005: Grounded in reality | PLAN.md | No theoretical frameworks that cannot be demonstrated; architecture must be implementable |

---

## Decision

### 1. Two-Layer Architecture

PROJ-010 adopts a two-layer architecture separating **semantic intent** from **provider-specific rendering** for LLM portability.

#### Semantic Layer (Portable -- Agent Definitions)

The Semantic Layer is the agent definition file as it exists in the repository: a markdown file with YAML frontmatter. Portable fields in this layer express what the agent is, what it does, what constraints it operates under, and what outputs it produces. The Semantic Layer is the single source of truth for agent behavior.

**Semantic Layer responsibilities:**
- Agent identity: role, expertise, cognitive mode, persona
- Behavioral constraints: forbidden actions, guardrails, constitutional compliance
- Tool definitions: name, description, parameters (JSON Schema)
- Output specifications: schema, required fields, format
- Capability requirements: minimum context window, required provider features
- Reasoning strategy preference: adaptive, explicit_cot, none

**Semantic Layer guarantees:**
- Every field has a defined interpretation regardless of provider
- No field references provider-specific API parameters, message roles, or syntax
- The Semantic Layer alone is sufficient to understand agent behavior -- even without a Rendering Layer, the agent definition is human-readable and unambiguous

**Authorship:** Skill developers (authors of /eng-team and /red-team agent definitions).

#### Rendering Layer (Provider-Specific -- Adapter Configs)

The Rendering Layer is a set of declarative transformation rules expressed as YAML configuration files -- one per provider target. These rules specify how to convert Semantic Layer fields into the prompt format, message structure, and API parameters that a specific provider expects.

**Rendering Layer responsibilities:**
- System prompt assembly: ordering, section delimiters, structural syntax
- Message role mapping: semantic roles to provider-specific roles
- Structured output enforcement: schema to provider-native mechanism
- Tool calling envelope: JSON Schema to provider-specific registration format
- Reasoning strategy injection: model-capability-aware CoT handling
- Context window budgeting: token allocation with provider-specific tokenizer awareness

**Implementation constraint:** The Rendering Layer is NOT compiled adapter code. It is a set of YAML configuration files that describe transformation rules. The actual transformation is performed by the agent invocation infrastructure at runtime. This keeps the portability layer within Jerry's markdown-and-YAML paradigm, consistent with the framework's design principles.

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

**Authorship:** Framework maintainers (written once per provider, shared across all agents). Skill developers never interact with the Rendering Layer directly.

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

**Rationale:** E-001 and E-002 independently converge on this separation. E-001 demonstrated that prompt structure is portable but prompt syntax is not (Finding 2). E-002 found that DSPy's semantic-intent separation principle is the theoretical ideal for portability, while CrewAI's YAML agent-as-configuration pattern is the most pragmatic implementation. This architecture achieves DSPy's separation principle using Jerry's existing declarative YAML paradigm, without requiring DSPy's compilation infrastructure.

### 2. Portable Agent Definition Schema (38 Fields)

All /eng-team and /red-team agent definitions use a 38-field schema. Each field is classified by portability.

#### Identity Fields (Fully Portable)

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Agent identifier (e.g., `eng-architect`, `red-recon`) |
| `version` | string | Semantic version of the agent definition |
| `description` | string | One-line description of agent purpose and invocation triggers |
| `identity.role` | string | Human-readable role title (e.g., "Solution Architect", "Reconnaissance Specialist") |
| `identity.expertise` | list[string] | Domain expertise areas |
| `identity.cognitive_mode` | enum | `divergent`, `convergent`, `integrative`, `systematic`, `strategic`, `forensic` |
| `persona.tone` | string | Communication tone (e.g., `professional`, `analytical`, `technical`) |
| `persona.communication_style` | string | Interaction style (e.g., `consultative`, `evidence-based`, `direct`) |
| `persona.audience_level` | string | Target audience (e.g., `L0`, `L1`, `L2`, `adaptive`) |

#### Capability Fields (Adaptation-Required)

| Field | Type | Description |
|-------|------|-------------|
| `capabilities.allowed_tools` | list[string] | Tool identifiers. Core tools (Read, Write, Edit, Glob, Grep, Bash) are portable. MCP tools (Context7, Memory-Keeper) require provider-specific registration. |
| `capabilities.output_formats` | list[string] | Supported output formats (markdown, yaml, json) |
| `capabilities.forbidden_actions` | list[string] | Constitutional prohibitions in natural language |
| `capabilities.required_features` | list[string] | Required provider features: `tool_use`, `structured_output`, `vision`, `streaming`. Adapter maps to provider capability check. |
| `model` | string | Model preference. Portable format: `{provider}/{model}` (e.g., `anthropic/claude-sonnet-4`). Adapter maps preference to available model. |

#### Guardrail Fields

| Field | Type | Portability | Description |
|-------|------|-------------|-------------|
| `guardrails.input_validation` | list[object] | portable | Regex patterns for input validation. Provider-agnostic -- applied before LLM invocation. |
| `guardrails.output_filtering` | list[string] | portable | Output filtering rules in natural language (e.g., `no_secrets_in_output`, `all_claims_must_have_citations`). Applied post-generation. |
| `guardrails.fallback_behavior` | enum | portable | Behavior on failure: `warn_and_retry`, `warn_and_halt`, `escalate_to_user` |
| `guardrails.safety` | object | non-portable | Provider-specific safety API configuration. Defined in provider adapter, not in agent definition. |

#### Tool Schema Fields

| Field | Type | Portability | Description |
|-------|------|-------------|-------------|
| `tools[].name` | string | portable | Tool function name |
| `tools[].description` | string | portable | Natural language description of tool purpose |
| `tools[].parameters` | JSON Schema | portable | Parameter schema using JSON Schema vocabulary. All providers have converged on this format (E-001 Finding 3, E-002 Finding 3). |
| `tools[].required` | list[string] | portable | Required parameter names |
| `tools[].invocation` | object | non-portable | Provider-specific invocation envelope. Defined in provider adapter config, not in agent definition. |

#### Output Schema Fields

| Field | Type | Portability | Description |
|-------|------|-------------|-------------|
| `output.schema` | JSON Schema | portable | Expected output structure defined as JSON Schema. |
| `output.required` | boolean | portable | Whether structured output is mandatory |
| `output.location` | string | portable | Repository path template for persisted output |
| `output.template` | string | portable | Reference to output template file |
| `output.levels` | list[enum] | portable | Required output levels: `L0`, `L1`, `L2` |
| `output.enforcement` | object | non-portable | Provider-specific enforcement mechanism. Defined in provider adapter config. |

#### Portability Configuration Fields (New, Optional)

These fields are added to agent definitions that opt into multi-provider support.

| Field | Type | Portability | Description |
|-------|------|-------------|-------------|
| `portability.enabled` | boolean | portable | Whether this agent definition has been validated for multi-provider use. Default: `false` (Anthropic-only, backward-compatible). |
| `portability.minimum_context_window` | integer | portable | Minimum context window required (in tokens). Used for model compatibility checking. |
| `portability.model_preferences` | list[string] | adaptation-required | Ordered model preference list for fallback. Format: `{provider}/{model}`. |
| `portability.reasoning_strategy` | enum | adaptation-required | `adaptive` (renderer decides based on model capability), `explicit_cot` (always include step-by-step), `none` (no reasoning injection). Default: `adaptive`. |
| `portability.few_shot.enabled` | boolean | portable | Whether few-shot examples are used |
| `portability.few_shot.examples_ref` | string | portable | Path to external examples file |
| `portability.few_shot.count_range` | object | adaptation-required | `{min: 1, max: 3}`. Renderer selects optimal count per model. |
| `portability.body_format` | enum | portable | Format of the agent body below the frontmatter. `xml` (current Jerry default, Anthropic-optimized), `markdown` (portable), `rccf` (Role-Context-Constraints-Format, maximally portable). |

#### Portability Classification Summary

| Classification | Count | Percentage | Field Categories |
|----------------|-------|------------|------------------|
| portable | 24 | 63% | Identity, persona, guardrails (input/output), tool schemas, output schema, output location/template/levels, few-shot config, body format |
| adaptation-required | 9 | 24% | allowed_tools, required_features, model, model_preferences, reasoning_strategy, few_shot.count_range, output.enforcement (at adapter level), tool invocation (at adapter level) |
| non-portable | 5 | 13% | guardrails.safety, tools[].invocation, output.enforcement, provider-specific extensions (extended_thinking, reasoning_effort, grounding) |

The 63/24/13 distribution means the majority of an agent definition can be written once and used across providers without modification. The non-portable 13% consists exclusively of provider-specific performance optimizations, not core agent behavior.

### 3. Four Provider Adapter Specifications

Each provider adapter is a YAML configuration file that defines transformation rules for rendering portable agent definitions into provider-specific prompts. Adapters contain no executable code -- they are declarative configurations consumed by the invocation infrastructure.

#### Anthropic (Claude) Adapter

| Aspect | Specification |
|--------|--------------|
| **System prompt placement** | Separate `system` API parameter (not in messages array) |
| **Preferred body structure** | XML-preferred when `body_format=xml`; markdown and RCCF also supported |
| **Structured output** | Tool-call workaround: define a "tool" matching the desired output schema, force via `tool_choice: {"type": "any"}`, extract tool call arguments as structured output |
| **Tool calling** | Anthropic tools array with `input_schema` field for JSON Schema; parallel calling supported |
| **Reasoning strategy** | Adaptive maps to `omit` (Claude Opus 4 / Sonnet 4 have built-in reasoning). Explicit CoT injected only for Haiku or when explicitly requested. Extended thinking available as provider-exclusive feature (omitted from portable definitions). |
| **Message roles** | `user` and `assistant` only (system is separate API parameter); strict human/assistant alternation enforced by API |
| **Context window** | 200K tokens. Budget: 20% output reserve, 15% system prompt, 10% tools, 55% conversation history. Prompt caching for system prompt and tool definitions. |
| **Models** | claude-opus-4 (200K, built-in reasoning, extended thinking), claude-sonnet-4 (200K, built-in reasoning), claude-haiku-3.5 (200K, limited reasoning) |

#### OpenAI (GPT) Adapter

| Aspect | Specification |
|--------|--------------|
| **System prompt placement** | `system` role in messages array |
| **Preferred body structure** | Markdown-preferred; XML functional but not optimized |
| **Structured output** | Native `response_format` with `json_schema` type for server-side enforcement (100% schema compliance guaranteed) |
| **Tool calling** | OpenAI functions format with `parameters` field for JSON Schema; parallel calling supported; forced use via `tool_choice: "required"` |
| **Reasoning strategy** | Adaptive maps to `omit` (GPT-4o / o3 have built-in reasoning). Explicit CoT for gpt-4o-mini or when explicitly requested. `reasoning_effort` parameter available for o3 series as provider-exclusive feature. |
| **Message roles** | `system`, `user`, `assistant`; flexible alternation (no strict alternation requirement) |
| **Context window** | 128K-1M tokens (model dependent). Budget: 20% output reserve. Automatic prompt caching on eligible prefixes. |
| **Models** | gpt-4o (128K, built-in reasoning), gpt-4.1 (1M, built-in reasoning), o3 (200K, deep built-in reasoning) |

#### Google (Gemini) Adapter

| Aspect | Specification |
|--------|--------------|
| **System prompt placement** | `system_instruction` in generation config (separate from message roles) |
| **Preferred body structure** | Markdown-preferred; XML supported but not optimized |
| **Structured output** | Native `response_schema` in generation config with `response_mime_type: "application/json"` |
| **Tool calling** | `function_declarations` format with JSON Schema parameters; parallel calling supported; forced use via `function_calling_config: {mode: "ANY"}` |
| **Reasoning strategy** | Adaptive maps to `omit` (Gemini 2.5 Pro has built-in thinking). Explicit CoT for flash models. Google Search grounding available as provider-exclusive feature. |
| **Message roles** | `user` and `model` (Google uses "model" not "assistant"); `system_instruction` is separate from message roles; flexible alternation |
| **Context window** | 1M tokens. Context caching API available for large prefixes. |
| **Models** | gemini-2.5-pro (1M, built-in thinking, grounding), gemini-2.0-flash (1M, built-in reasoning) |

#### Open-Source (Ollama/vLLM via LiteLLM) Adapter

| Aspect | Specification |
|--------|--------------|
| **System prompt placement** | Delegated to LiteLLM. LiteLLM auto-detects model family and applies correct chat template. System messages injected as system role where supported, or prepended to user message where not (Mistral, Gemma). |
| **Preferred body structure** | RCCF-preferred (maximally portable plain-text structure). Constraints placed before context due to weaker instruction following in smaller models. |
| **Structured output** | Best-effort: JSON Schema included in prompt text as baseline. Optionally use Instructor or Outlines for constrained generation when running against vLLM or compatible inference servers. Retry with explicit format reminder after failure; raw output with validation errors after 3 failures. |
| **Tool calling** | OpenAI-compatible format via LiteLLM translation; model-dependent parallel calling; forced use not universally supported |
| **Reasoning strategy** | Adaptive maps to `inject_step_by_step` (most open-source models benefit from explicit CoT per E-001 Finding 4). Appends: "Think through your response step by step before providing your final answer. Show your reasoning." |
| **Message roles** | Delegated to LiteLLM for model-specific template handling; `user` and `assistant` as defaults; alternation is model-dependent |
| **Context window** | 8K-128K tokens (model dependent). Conservative allocation: 30% output reserve (open-source models less reliable with long outputs). System prompt capped at 10%. For models with small context (<32K), prioritize constraints and tools over context/examples. |
| **Models** | llama3.1:70b (128K, requires explicit CoT), mistral-large (128K, built-in reasoning, no native system role), gemma-2:27b (8K, requires explicit CoT, no native system role) |

**Rationale for LiteLLM delegation:** E-001 Finding 6 documented at least five distinct chat template formats across open-source models (ChatML, Llama, Mistral `[INST]`, Gemma `<start_of_turn>`, Phi `<|system|>`), with system message support not universal. E-002 identified LiteLLM as the ecosystem-standard solution used by Google ADK and CrewAI for cross-provider API normalization, supporting 100+ providers. Building custom template rendering would duplicate LiteLLM's battle-tested infrastructure.

### 4. System Prompt Assembly (RCCF Pattern)

Provider adapters assemble system prompts following the RCCF pattern (Role-Context-Constraints-Format) identified in E-001 as the highest-portability prompt structure.

**RCCF structure:**

```
ROLE: [Agent identity, expertise, cognitive mode]

CONTEXT: [Background information, domain knowledge, engagement scope]

CONSTRAINTS: [Forbidden actions, guardrails, constitutional compliance]

FORMAT: [Expected output structure, schema, required levels]
```

**Why RCCF is maximally portable:** Every LLM processes structured instructions hierarchically. Leading with role establishes the behavioral frame. Following with context, then constraints, then format mirrors how all major providers weight instruction priority (early content receives stronger attention due to primacy bias). This was validated across Anthropic, OpenAI, Google, and open-source models in E-001 Pattern 1.

**Provider-specific ordering adjustments:**
- Anthropic, OpenAI, Google: Identity -> Context -> Constraints -> Format -> Tools (standard RCCF)
- Open-source: Identity -> Constraints -> Context -> Format -> Tools (constraints elevated before context due to weaker instruction following in smaller models)

**Section delimiters per provider:**
- Anthropic (when `body_format=xml`): `<section>\n{content}\n</section>`
- Anthropic (when `body_format=markdown`), OpenAI, Google: `## {section}\n{content}`
- Open-source, RCCF format: `{LABEL}:\n{content}`

**New agents use markdown body format as the portable default** per E-001 Anti-Pattern 1 evidence. Markdown headers (`##`) provide equivalent structural organization to XML tags and are universally supported across all providers. XML remains explicitly supported for existing agents and as an Anthropic-specific optimization when body_format is set to `xml`.

### 5. Portability Validation Criteria (PV-001 through PV-018)

Portability is a testable property per R-010. The 18 validation criteria decompose into three categories.

#### Structural Validation -- Static Analysis (PV-001 through PV-010)

These tests run against agent definition files without invoking any LLM. They are CI-runnable.

| ID | Criterion | Pass Condition |
|----|-----------|----------------|
| PV-001 | No provider-specific API parameters in frontmatter | Zero references to `response_format`, `tool_choice`, `function_calling_config`, `extended_thinking`, `reasoning_effort`, or `system_instruction` |
| PV-002 | All tool definitions use JSON Schema | All `tools[].parameters` fields validate against JSON Schema metaschema |
| PV-003 | Output schema is JSON Schema | `output.schema` field validates against JSON Schema metaschema |
| PV-004 | No hardcoded chat template tokens | Zero matches for `<\|begin_of_text\|>`, `[INST]`, `<start_of_turn>`, `<\|system\|>`, `<\|user\|>` in agent body |
| PV-005 | No hardcoded CoT instructions (when reasoning_strategy != explicit_cot) | Zero matches for "step by step", "think through", "chain of thought" when `portability.reasoning_strategy` is `adaptive` or `none` |
| PV-006 | Model preference uses portable format | All `portability.model_preferences` entries match `{provider}/{model}` format |
| PV-007 | Required features are declared | All implicit feature dependencies (tool calling, structured output) explicitly listed in `capabilities.required_features` |
| PV-008 | Context window requirement is declared | `portability.minimum_context_window` is set and is a positive integer |
| PV-009 | Body format is declared | `portability.body_format` is set to `xml`, `markdown`, or `rccf` |
| PV-010 | Portability flag is set | `portability.enabled` is `true` |

#### Behavioral Validation -- Cross-Provider Invocation (PV-011 through PV-016)

These tests require invoking the agent across providers and comparing outputs. They run as a dedicated validation suite during Phase 5.

| ID | Criterion | Pass Condition |
|----|-----------|----------------|
| PV-011 | Agent produces valid structured output on all target providers | Output validates against `output.schema` on all providers |
| PV-012 | Agent uses declared tools correctly on all target providers | Tool call parameters validate against `tools[].parameters` schema on all providers |
| PV-013 | Agent respects constraints on all target providers | Forbidden actions enforced on all providers |
| PV-014 | Agent identity is consistent across providers | Role and expertise references are semantically equivalent across providers |
| PV-015 | Agent output quality does not degrade significantly across providers | Weighted composite score >= 0.85 on all providers using S-014 LLM-as-Judge dimensions (allowing 0.07 degradation from primary provider threshold of 0.92) |
| PV-016 | Agent gracefully degrades on capability-limited models | Agent produces usable output without crashing when invoked on a model lacking a declared optional feature |

**PV-015 threshold rationale:** The 0.85 cross-provider threshold allows a 0.07-point degradation from the standard 0.92 quality gate. This acknowledges that provider-specific optimizations (XML for Anthropic, response_format for OpenAI) may contribute marginal quality improvements that cannot be fully replicated portably. The 0.07 margin was calibrated against E-003's analysis of portable vs. provider-optimized prompt performance.

#### Regression Validation -- Backward Compatibility (PV-017 through PV-018)

| ID | Criterion | Pass Condition |
|----|-----------|----------------|
| PV-017 | Existing agents without portability section work unchanged | Output matches pre-portability-layer behavior when invoked on Anthropic |
| PV-018 | Portability section is optional | Agent functions correctly without portability metadata when invoked on Anthropic |

### 6. Backward Compatibility

The portability architecture preserves full backward compatibility with Jerry's 37 existing agents.

| Guarantee | Mechanism |
|-----------|-----------|
| Existing agents work without modification | `portability.enabled` defaults to `false`; Anthropic rendering is the default |
| Existing XML body format is preserved | `body_format: xml` is explicitly supported; Anthropic adapter renders XML natively |
| No existing SKILL.md changes required | `portability` section in SKILL.md is optional |
| No existing AGENTS.md changes required | Portability column in agent summary tables is optional |
| No new code dependencies | Provider adapter configs are YAML files, not compiled code |
| Gradual opt-in | Each agent migrates independently; no all-or-nothing cutover |

**4-phase migration path:**

| Phase | Scope | Change to Existing Agents |
|-------|-------|---------------------------|
| Phase 1: Foundation | Create `.context/portability/` directory with provider adapter configs and schema files | None -- all existing agents continue to work unchanged |
| Phase 2: New Agent Authoring | Author all /eng-team and /red-team agents with `portability.enabled: true`, `body_format: markdown`, RCCF pattern, model preferences | None -- this applies only to new PROJ-010 agents |
| Phase 3: Cross-Provider Validation | Execute PV-011 through PV-016 for all PROJ-010 agents; iterate on adapter configs | None -- validation targets new agents only |
| Phase 4: Existing Agent Migration (Optional, Post-PROJ-010) | Add `portability` section to frontmatter; convert XML body to markdown equivalents | Optional per-agent migration at team's discretion |

### 7. Adaptive Reasoning Strategy

Agent definitions default to `portability.reasoning_strategy: adaptive`. The Rendering Layer injects chain-of-thought instructions only for models that benefit from them.

| Model Class | Reasoning Behavior | CoT Injection |
|-------------|-------------------|---------------|
| Frontier (Claude Opus 4, Claude Sonnet 4, GPT-4o, o3, Gemini 2.5 Pro) | Built-in reasoning | Omit explicit CoT -- E-001 Finding 4 and 2025 TMLR benchmarks demonstrate that explicit CoT degrades performance on frontier models |
| Mid-tier (Claude Haiku 3.5, GPT-4o-mini, Gemini 2.0 Flash) | Built-in but limited | Omit by default; inject on explicit request |
| Open-source (Llama 3.1, Mistral, Gemma) | Requires explicit prompting | Inject step-by-step reasoning prompt -- CoT remains beneficial for models without built-in reasoning chains |

**Rationale:** E-001 Finding 4 cited 2025 Chain-of-Thought Hub benchmarks (TMLR 2025) showing that explicit CoT does not yield statistically significant improvements on modern frontier models and can degrade performance. A fixed CoT strategy penalizes at least one provider class. Adaptive reasoning resolves this by making CoT injection a rendering-layer concern, not an agent-definition concern.

### 8. Tool Schema and Structured Output

**Tool definitions:** JSON Schema is the universal tool definition format. All four providers support JSON Schema for tool parameters (E-001 Finding 3, E-002 Finding 3). Agent definitions express tool schemas in JSON Schema; the Rendering Layer handles provider-specific registration:

| Provider | Registration Format | Example |
|----------|-------------------|---------|
| Anthropic | `tools` array with `input_schema` field | `{"name": "...", "description": "...", "input_schema": {json_schema}}` |
| OpenAI | `tools` array with `function.parameters` field | `{"type": "function", "function": {"name": "...", "parameters": {json_schema}}}` |
| Google | `function_declarations` array | `{"function_declarations": [{"name": "...", "parameters": {json_schema}}]}` |
| Open-source | OpenAI-compatible via LiteLLM translation | LiteLLM translates OpenAI format to model-native |

**Structured output:** Agent definitions declare output schemas in JSON Schema. Enforcement mechanism is the Rendering Layer's responsibility:

| Provider | Enforcement Mechanism | Compliance Level |
|----------|----------------------|------------------|
| Anthropic | Tool-call workaround (define "tool" with output schema, force use) | High (workaround is reliable) |
| OpenAI | Native `response_format` with `json_schema` type | Highest (server-side, 100% compliance) |
| Google | Native `response_schema` in generation config | High (server-side enforcement) |
| Open-source | Prompt-level schema instructions; optionally Instructor/Outlines for constrained generation | Best-effort (no server-side guarantee without additional libraries) |

**Rationale:** E-001 Finding 2 documented fundamentally different enforcement mechanisms across providers. E-003 Finding 3 identified structured output as the highest-value adaptation target because PROJ-010's cybersecurity agents require structured output reliability for threat classification accuracy and engagement reporting quality. Abstracting enforcement into the Rendering Layer shields agent authors from these divergences.

---

## Options Considered

### Option 1: Single-Layer Provider-Specific Agents (Fork Per Provider)

**Description:** Write separate agent definitions per provider. Maintain Anthropic versions, OpenAI versions, Google versions, and open-source versions of each agent.

**Pros:**
- Maximum provider-specific optimization -- each version fully exploits provider strengths
- No abstraction layer overhead
- Simple to understand for any single provider

**Cons:**
- 21 agents x 4 providers = 84 agent definition files to maintain
- Behavioral drift between provider versions as they evolve independently
- Every agent change must be replicated 4 times
- Violates R-010's requirement for portable agent definitions ("Agent logic MUST NOT depend on provider-specific features")
- No testable portability property -- each version is independently authored

**Why rejected:** Maintenance burden scales multiplicatively with agents and providers. Behavioral drift between versions is inevitable and untestable. This approach does not satisfy R-010's portability requirement -- it replaces portability with duplication.

### Option 2: Code-Based Abstraction Library (Compiled Adapter Layer)

**Description:** Build a Python abstraction library (similar to LangChain's `BaseChatModel`) that programmatically transforms agent definitions into provider-specific API calls.

**Pros:**
- Full programmatic control over transformation logic
- Can handle complex conditional rendering
- Familiar software engineering pattern (Strategy pattern, Adapter pattern)

**Cons:**
- Introduces compiled code dependency into Jerry's declarative paradigm
- Violates Jerry's design principle of markdown-and-YAML for agent definitions (PLAN.md R-010 specifies portability within agent definitions, not external code)
- Creates a runtime dependency that must be installed, versioned, and tested
- Increases complexity for skill developers who must now understand both YAML definitions and Python rendering code
- Testing requires running Python code, not just validating YAML

**Why rejected:** Jerry's agent definitions are declarative by design. Introducing a compiled abstraction layer changes the framework's fundamental paradigm. The YAML-based Rendering Layer achieves the same separation without introducing code dependencies, keeping the entire portability stack within the markdown-and-YAML paradigm.

### Option 3: Two-Layer Declarative Architecture (CHOSEN)

**Description:** YAML configuration for rendering, markdown for agent definitions. The Semantic Layer (agent definitions) captures provider-agnostic intent. The Rendering Layer (provider adapter YAML configs) describes transformation rules. 63% of fields are fully portable, 24% require adaptation, 13% are non-portable provider-specific optimizations.

**Pros:**
- Preserves Jerry's declarative paradigm -- no compiled code added
- Clean authorship separation: skill developers write Semantic Layer, framework maintainers write Rendering Layer (once per provider)
- Backward compatible: existing 37 agents work unchanged with `portability.enabled` defaulting to false
- Testable: 10 static analysis criteria (PV-001 through PV-010) runnable in CI without LLM invocation
- Industry-validated: CrewAI YAML config pattern, DSPy semantic-intent separation principle, LiteLLM API translation layer
- 18 concrete validation criteria make portability a measurable, enforceable property per R-010

**Cons:**
- YAML transformation rules are less expressive than compiled code for complex conditional rendering
- Provider adapter configs require maintenance as provider APIs evolve
- New providers require authoring a new adapter config (one-time cost per provider)
- The declarative approach may not handle edge cases that a programmatic adapter could

**Why chosen:** This option is the only one that satisfies all constraints simultaneously: R-010 portability, Jerry's declarative paradigm, backward compatibility with 37 existing agents, and testable portability as a measurable property. The cons are manageable: YAML expressiveness is sufficient for the transformation rules documented in E-003's adapter specifications, and new provider adapter authoring is a one-time cost amortized across all agents.

### Option 4: DSPy-Style Compilation (Semantic Signatures to Provider-Specific Prompts)

**Description:** Adopt DSPy's paradigm: define agents as typed signatures (input/output specifications) and compile them into provider-specific prompts using optimizers with labeled data.

**Pros:**
- Theoretically maximum portability: same signature compiles to different optimal prompts per model
- Eliminates prompt engineering as a manual activity
- Empirically-optimized prompts can outperform hand-crafted ones (E-002 DSPy analysis)

**Cons:**
- Requires labeled data and metric functions for each agent -- PROJ-010 has no training datasets for 21 agents
- Compilation adds development overhead and a new infrastructure dependency
- Fundamental paradigm shift from Jerry's markdown-based agent definitions to typed Python signatures
- Smaller community and less battle-tested in production agent systems (E-002 Finding 4)
- Not suitable for all agent tasks -- works best for well-defined I/O tasks, not open-ended advisory agents like eng-architect or red-lead
- Would require rewriting all existing Jerry agents in DSPy's signature format

**Why rejected:** The paradigm shift is too large for PROJ-010's scope, and the infrastructure requirements (labeled datasets, compilation pipeline) exceed what is justified for an agent system where most tasks are advisory rather than narrowly-defined I/O transformations. However, the core insight -- separate semantic specification from prompt implementation -- is directly incorporated into Option 3's two-layer architecture. E-003 recommendation R-FW-007 recommends evaluating DSPy selectively for high-criticality agents (threat classification, vulnerability assessment) as a Phase 5 enhancement after the base architecture is established.

---

## Consequences

### Positive

1. **R-010 compliance achieved.** The two-layer architecture makes LLM portability a structural property of PROJ-010's agent definitions. Portability is testable through 18 concrete validation criteria (10 static, 6 behavioral, 2 regression), satisfying R-010's mandate that portability "MUST be validated as a testable property."

2. **Provider independence for mission-critical operations.** /eng-team and /red-team agents can operate on Anthropic, OpenAI, Google, or open-source models. This enables air-gapped deployments (open-source models for sensitive environments), provider failover (ordered model preference lists per Haystack FallbackChatGenerator pattern), and cost optimization (different models for different agent tiers).

3. **Zero disruption to existing agents.** All 37 existing Jerry agents continue to function without modification. The `portability.enabled` default of `false` ensures the portability layer is purely additive. The 4-phase migration path allows optional, gradual adoption.

4. **Clean authorship separation.** Skill developers author only the Semantic Layer (portable agent definitions). Framework maintainers author the Rendering Layer once per provider. This eliminates the need for skill developers to understand provider-specific API differences.

5. **CI-enforceable static validation.** 10 of the 18 validation criteria (PV-001 through PV-010) are static analysis tests runnable in CI without LLM invocation. This catches portability regressions at commit time, before they reach behavioral testing.

6. **Industry-aligned architecture.** The design draws on proven patterns from the broader ecosystem: CrewAI's YAML agent-as-configuration (E-002), DSPy's semantic-intent separation principle (E-002), LiteLLM's API translation for open-source models (E-001, E-002), and Haystack's FallbackChatGenerator for model resilience (E-002).

7. **Declarative consistency.** The entire portability stack -- agent definitions, provider adapter configs, validation criteria, schemas -- is expressed in YAML and markdown. No compiled code is introduced, preserving Jerry's design principle of filesystem-as-memory with declarative configurations.

### Negative

1. **YAML expressiveness ceiling.** Declarative YAML transformation rules are less expressive than compiled code for complex conditional rendering. If a future provider introduces a fundamentally novel API pattern that cannot be expressed as a YAML transformation rule, the adapter approach may need to be extended.
   - **Impact estimate:** LOW. The four current major provider APIs (Anthropic, OpenAI, Google, open-source via LiteLLM) are well-characterized by E-003's adapter specifications. The YAML transformation model is sufficient for all documented patterns. The risk materializes only if a future provider introduces a qualitatively different invocation paradigm.

2. **Cross-provider quality degradation.** PV-015 allows a 0.07-point quality degradation (from 0.92 to 0.85) on non-primary providers. For security-critical outputs where maximum accuracy matters (threat classification, vulnerability assessment, scope compliance attestation), this degradation may be operationally significant.
   - **Impact estimate:** MEDIUM. The 0.07 margin acknowledges provider-specific optimizations that contribute marginal quality. For the highest-criticality outputs, organizations can mandate a specific provider (e.g., Anthropic with XML optimization) while retaining portability as a fallback capability rather than a mandatory operational mode.

3. **Open-source structured output is best-effort.** The open-source adapter provides prompt-level schema instructions without server-side enforcement. The retry-then-raw-output strategy (3 retries, then raw output with validation errors) may be insufficient for security-critical structured outputs.
   - **Impact estimate:** MEDIUM for open-source deployments specifically. Mitigated by (a) optional Instructor/Outlines integration for constrained generation on vLLM-compatible servers, and (b) the capability declaration mechanism (`required_features: [structured_output]`) which enables pre-flight capability checking before invocation. See Open Question OQ-005.

4. **Provider adapter maintenance.** Provider APIs evolve. Adapter configs must be updated when providers change their API semantics, add new models, or modify structured output mechanisms.
   - **Impact estimate:** LOW. Provider API changes are typically additive (new features, new models) rather than breaking. The adapter update cadence is expected to be quarterly or less, and each update is a YAML config change with no code compilation required.

5. **New provider onboarding cost.** Adding support for a new LLM provider requires authoring a complete adapter YAML config. Based on E-003's adapter specifications, this is approximately 80-120 lines of YAML per provider.
   - **Impact estimate:** LOW. This is a one-time cost per provider, amortized across all 21+ agents. The structured format of existing adapter configs serves as a template for new providers.

### Neutral (Requires Monitoring)

1. **Adaptive reasoning calibration.** The adaptive reasoning strategy (CoT injection for open-source, omission for frontier) is based on E-001's 2025 research findings. As frontier models continue to evolve and open-source models improve, the optimal reasoning strategy per model class may shift. The adapter configs should be reviewed semi-annually against current model benchmarks.

2. **PV-015 threshold adequacy.** The 0.85 cross-provider quality threshold is derived from E-003's analysis but has not been empirically validated against PROJ-010's specific agent outputs. Phase 5 behavioral validation will produce the first empirical data. The threshold may need adjustment based on observed cross-provider quality distributions.

3. **LiteLLM dependency for open-source.** The open-source adapter delegates chat template handling to LiteLLM. This introduces an infrastructure dependency for open-source model support. LiteLLM is actively maintained (used by Google ADK, CrewAI) but is a third-party dependency. Monitor for maintenance status changes.

4. **Few-shot example optimization.** E-001 Finding 5 documented model-dependent sensitivity to few-shot example count (over-prompting phenomenon). The `few_shot.count_range` mechanism enables per-model optimization, but optimal ranges for PROJ-010's specific agents are unknown until Phase 5 validation.

---

## Evidence Base

### E-001: Universal Prompt Engineering Patterns

| Finding | Evidence | Relevance to Decision |
|---------|----------|----------------------|
| RCCF pattern is universally portable | Tested across Anthropic, OpenAI, Google, and open-source models (E-001 Pattern 1; Lakera Prompt Engineering Guide 2026) | Adopted as system prompt assembly pattern for all provider adapters |
| JSON Schema is the universal tool definition format | All major providers support JSON Schema for tool parameters (E-001 Finding 3, Pattern 5; Structured Output Comparison across LLM Providers, Oct 2025) | Standardized as the sole tool schema format in portable agent definitions |
| XML tags are Anthropic-specific optimization | Claude trained on XML; other providers treat XML as plain text (E-001 Anti-Pattern 1; Anthropic XML tags documentation) | New agents use `body_format: markdown` by default; XML preserved as Anthropic-specific optimization |
| Explicit CoT degrades frontier model performance | 2025 TMLR benchmarks show CoT not universally beneficial (E-001 Finding 4; Chain-of-Thought Hub benchmarks) | Adaptive reasoning strategy: omit CoT for frontier models, inject for open-source |
| Few-shot example count is model-dependent | Over-prompting phenomenon documented in 2025 (E-001 Finding 5; The Few-shot Dilemma, arXiv 2509.13196v1) | Externalized few-shot examples with configurable count ranges per model |
| Chat template fragmentation across open-source models | At least 5 distinct formats; system message support not universal (E-001 Finding 6; LiteLLM Prompt Formatting; Hugging Face Chat Templates) | Open-source adapter delegates template handling to LiteLLM |
| Structured output mechanisms fundamentally differ per provider | OpenAI: `response_format` server-side; Anthropic: tool-call workaround; Google: `response_schema`; OSS: prompt-level (E-001 Finding 2; OpenAI Structured Outputs) | Output schema in JSON Schema; enforcement delegated to rendering layer per provider |
| System prompt handling differs per provider | Anthropic: separate API param; OpenAI: system message role; Google: system_instruction; OSS: varies (E-001 Finding 1) | Provider adapters define system prompt placement per provider API |

### E-002: Multi-LLM Agent Framework Analysis

| Finding | Evidence | Relevance to Decision |
|---------|----------|----------------------|
| Industry converged on OpenAI format as de facto standard | LiteLLM, LangChain, CrewAI, Haystack, Google ADK, AutoGen all use OpenAI message format (E-002 Finding 1; LiteLLM Providers) | OpenAI format adopted as internal canonical representation for cross-provider translation |
| Agent-as-configuration is the dominant portable pattern | CrewAI YAML configs, LangChain Runnables, Google ADK Agent class (E-002 Finding 2, Cross-Cutting Pattern) | Validates Jerry's existing YAML frontmatter + markdown as an industry-aligned agent definition format |
| No framework solves optimal-prompt-per-model | All frameworks abstract API layer but do not optimize prompt content (E-002 Finding 4) | Rendering Layer addresses this gap with per-provider transformation rules |
| DSPy's semantic-intent separation is the theoretical ideal | Same signature compiles to different prompts per model (E-002 DSPy Analysis; dspy.ai) | Two-layer architecture implements this principle using declarative YAML instead of compilation |
| Haystack FallbackChatGenerator is a resilience best practice | Sequential multi-model fallback with automatic failover (E-002 Finding 6; Haystack GitHub) | Model preference lists with ordered fallback adopted in `portability.model_preferences` |
| LiteLLM is the ecosystem-standard API translation layer | 100+ provider support; used by Google ADK and CrewAI (E-002 R-FW-001; LiteLLM GitHub) | Adopted as the infrastructure layer for open-source model support |
| CrewAI YAML config closest to Jerry's format | role/goal/backstory/tools/llm in YAML (E-002 CrewAI Analysis; CrewAI Agent Configuration) | Portable agent schema extends Jerry's existing format following CrewAI's proven pattern |

### E-003: Portability Architecture Recommendation

| Finding | Evidence | Relevance to Decision |
|---------|----------|----------------------|
| Portable surface area is larger than non-portable | 63% fully portable, 24% adaptation-required, 13% non-portable (E-003 Finding 1) | Confirms architecture viability -- majority of agent definitions transfer without modification |
| Prompt structure portable, syntax is not | RCCF works across providers; XML/chat templates are syntax-specific (E-003 Finding 2) | Architecture separates structural intent (Semantic Layer) from syntactic expression (Rendering Layer) |
| Structured output is highest-value adaptation target | Fundamentally different enforcement mechanisms across providers (E-003 Finding 3) | Structured output enforcement handled entirely in Rendering Layer per provider |
| Configuration-driven definitions are industry-proven | CrewAI, LangChain, Google ADK all use configuration-driven definitions (E-003 Finding 4) | Two-layer architecture extends Jerry's existing configuration-driven format |
| Backward compatibility achievable through opt-in | `portability.enabled` defaults to false; existing agents unchanged (E-003 Migration Path) | 4-phase migration path with zero mandatory changes to existing agents |

### S-002: Architecture Implications Synthesis

| Finding | Evidence | Relevance to Decision |
|---------|----------|----------------------|
| AD-003 rated HIGH confidence | E-001 and E-002 independently converge; industry settled on configuration-driven definitions; 18 testable validation criteria defined (S-002 AD-003) | Confirms cross-stream convergence supporting this architecture |
| JSON Schema as universal data interchange format | Convergence 5 in S-001: streams C, E, and F independently validate JSON Schema for tool/output definitions (S-002 Cross-Cutting Concerns) | JSON Schema adopted as the sole tool and output schema format |
| Portability layer affects multiple features | FEAT-010 (agent definitions), FEAT-011 (routing), FEAT-012 (portability), FEAT-014 (tool integration) (S-002 Cross-Cutting Concerns: Portability Layer Integration) | Architecture designed for cross-feature integration, not FEAT-012 in isolation |

---

## Compliance

### R-010: LLM Portability

| R-010 Clause | Compliance Mechanism |
|--------------|---------------------|
| "All agent definitions MUST be portable across LLM providers" | 38-field schema with 63% fully portable fields; Rendering Layer transforms to Anthropic, OpenAI, Google, and open-source |
| "Agent logic MUST NOT depend on provider-specific features" | Semantic Layer guarantees: no field references provider-specific API parameters, message roles, or syntax |
| "Prompt engineering MUST use universal patterns" | RCCF pattern for system prompt assembly; JSON Schema for tools and outputs; markdown body format as portable default |
| "Portability MUST be validated as a testable property" | 18 validation criteria (PV-001 through PV-018): 10 static analysis (CI-runnable), 6 behavioral (cross-provider invocation), 2 regression (backward compatibility) |

### P-003: No Recursive Subagents

The Rendering Layer is a declarative YAML configuration consumed by the invocation infrastructure. It does not spawn agents. All transformation logic operates within the single invocation boundary: the orchestrator reads the Semantic Layer, applies the Rendering Layer transformation rules, and invokes the target LLM. No nested agent spawning occurs.

### P-020: User Authority

This ADR is a **recommendation**, not a final decision. Per P-020, the user retains authority to:
- Override any schema field classification (portable, adaptation-required, non-portable)
- Modify the PV-015 cross-provider quality threshold (currently >= 0.85)
- Add or remove target providers from the adapter set
- Adjust the migration path phases or timelines
- Accept or reject the entire architecture

**Ratification status:** PENDING. This ADR requires explicit user ratification before transitioning to ACCEPTED status.

### P-022: No Deception

**Epistemic boundaries of this ADR:**
- The 63/24/13 portability classification is derived from E-003's schema analysis, which analyzed provider API documentation and framework implementations. It has not been empirically validated through cross-provider agent invocation. Phase 5 behavioral validation will produce the first empirical data.
- The 0.85 cross-provider quality threshold (PV-015) is a design target based on E-003's analysis, not an empirically measured degradation bound. Actual degradation may be higher or lower depending on agent complexity and task type.
- The open-source adapter's "best-effort" structured output is an honest acknowledgment that prompt-level enforcement cannot guarantee compliance without server-side mechanisms or additional libraries (Instructor/Outlines).
- The adaptive reasoning strategy is based on 2025 research findings that may not reflect the behavior of models released after this ADR's date.

### R-022: Agent Development Standards

The portable agent definition schema extends Jerry's existing YAML frontmatter format. All mandatory fields from Jerry's agent-development-standards are preserved. The `portability` section is additive and optional. No existing standards are violated or modified.

---

## Related Decisions

### Upstream (Inputs to This ADR)

| Decision / Artifact | Relationship | Status |
|---------------------|-------------|--------|
| **E-001: Universal Prompt Engineering Patterns** | RCCF pattern, JSON Schema convergence, XML anti-pattern, CoT research, chat template fragmentation analysis | Complete |
| **E-002: Multi-LLM Agent Framework Analysis** | Agent-as-configuration pattern, DSPy semantic-intent principle, LiteLLM recommendation, Haystack fallback pattern, CrewAI YAML format | Complete |
| **E-003: Portability Architecture Recommendation** | Primary source: two-layer design, 38-field schema, 4 adapter specifications, 18 validation criteria, migration path | Complete |
| **S-002: Architecture Implications Synthesis** | AD-003 decision details, cross-cutting portability concerns, HIGH confidence rating | Complete |
| **PLAN.md R-010** | Governing requirement for LLM portability | Baselined |

### Downstream (Decisions Informed by This ADR)

| Decision / Work Item | Relationship | Status |
|---------------------|-------------|--------|
| **FEAT-012 detailed design** | This ADR provides the architectural specification for FEAT-012 implementation | Planned (Phase 2) |
| **Phase 3: /eng-team agent authoring** | All 10 eng-team agents will use the portable schema with `portability.enabled: true` and `body_format: markdown` | Blocked on ADR acceptance |
| **Phase 4: /red-team agent authoring** | All 11 red-team agents will use the portable schema | Blocked on ADR acceptance |
| **Phase 5: Cross-provider validation** | PV-011 through PV-016 behavioral validation executed against all PROJ-010 agents | Blocked on Phases 3-4 |
| **AD-005: MCP-Primary Tool Integration** | Tool schema format (JSON Schema) and common adapter interface align with this ADR's tool schema design | Parallel (independent but aligned) |
| **AD-006: SARIF-Based Finding Normalization** | Finding schemas are a subset of the output schema mechanism defined here | Parallel (independent but aligned) |
| **AD-007: YAML-First Configurable Rule Sets** | Rule set configurations use the same YAML paradigm as provider adapter configs | Parallel (independent but aligned) |

### Cross-Cutting Integration Points

This ADR's architecture affects features beyond FEAT-012, as documented in S-002's cross-cutting concerns:

| Feature | Integration Point |
|---------|-------------------|
| FEAT-010 (Agent Team Architecture) | All 21 agent definitions use the portable schema |
| FEAT-011 (Skill Routing & Invocation) | Routing layer consults `portability.model_preferences` when a specific provider is requested |
| FEAT-013 (Configurable Rule Set Architecture) | Rule set configs follow the same YAML paradigm |
| FEAT-014 (Tool Integration Adapter Architecture) | Common adapter interface produces tool definitions in JSON Schema consumed by the Rendering Layer |

---

## Open Questions

### OQ-ADR003-001: Open-Source Structured Output Enforcement for Security-Critical Outputs

**Context:** The open-source adapter provides best-effort structured output enforcement. The retry-then-raw-output strategy (3 retries, then raw output with validation errors) may be insufficient for security-critical structured outputs such as engagement reports, scope compliance attestations, and finding schemas.

**What must be decided:** Whether the 3-retry-then-raw-output strategy is acceptable for security-critical outputs, or whether open-source deployments must mandate Instructor or Outlines for constrained generation, adding infrastructure dependencies.

**When:** Phase 5 (cross-provider validation will produce empirical data on structured output compliance rates).

**Corresponds to:** S-002 OQ-005.

### OQ-ADR003-002: PV-015 Threshold Empirical Validation

**Context:** The 0.85 cross-provider quality threshold is a design target, not an empirically measured degradation bound. Actual cross-provider quality degradation depends on agent complexity, task type, and provider-specific optimizations.

**What must be decided:** Whether 0.85 is the correct threshold, based on empirical quality score distributions from Phase 5 behavioral validation. The threshold may need to be raised (if cross-provider quality is higher than expected) or lowered (if the 0.07 margin is insufficient).

**When:** Phase 5 (after PV-011 through PV-016 produce empirical data).

### OQ-ADR003-003: DSPy Selective Adoption for High-Criticality Agents

**Context:** E-002 recommendation R-FW-007 suggests evaluating DSPy's compiled prompt optimization for high-criticality agents where maximum accuracy justifies compilation overhead (threat classification, vulnerability assessment).

**What must be decided:** Whether any PROJ-010 agents would benefit from DSPy compilation as an enhancement layer atop the two-layer architecture, and if so, which agents and what labeled datasets would be required.

**When:** Post-Phase 5 (after base portable architecture is validated and operational).

### OQ-ADR003-004: Provider Adapter Config Update Cadence

**Context:** Provider APIs evolve. New models are released. Adapter configs must be updated to reflect current model capabilities, context windows, and API changes.

**What must be decided:** The governance process for adapter config updates -- who is responsible, what triggers an update, and how updates are validated against the portability test suite.

**When:** Phase 2 (as part of FEAT-012 detailed design).

---

## References

### Research Artifacts (PROJ-010 Phase 1)

| Artifact | Date | Content |
|----------|------|---------|
| E-001: Universal Prompt Engineering Patterns | 2026-02-22 | Provider comparison, 6 universal patterns, 6 anti-patterns, portable schema analysis |
| E-002: Multi-LLM Agent Framework Analysis | 2026-02-22 | 8-framework analysis, cross-cutting patterns, per-framework detailed analysis |
| E-003: Portability Architecture Recommendation | 2026-02-22 | Two-layer design, 38-field schema, 4 adapter specs, 18 validation criteria, migration path |
| S-002: Architecture Implications Synthesis | 2026-02-22 | AD-003 decision details, cross-cutting concerns, open questions |

### Academic Research (2025)

| Source | Date | Finding |
|--------|------|---------|
| [Chain-of-Thought Hub benchmarks](https://github.com/FranxYao/chain-of-thought-hub) (TMLR 2025) | Dec 2025 | CoT effectiveness varies by model; not universally beneficial for frontier models |
| [The Few-shot Dilemma: Over-prompting LLMs](https://arxiv.org/html/2509.13196v1) | Sep 2025 | Excessive few-shot examples degrade performance in certain LLMs |
| [PromptBridge: Model-Adaptive Prompt Evolution](https://www.emergentmind.com/topics/prompt-based-llm-framework) | 2025 | Calibrated prompt transfer achieves up to +5pp gain via model-specific adaptation |
| [Inclusive Prompt Engineering Model (IPEM)](https://link.springer.com/article/10.1007/s10462-025-11330-7) | 2025 | Modular framework for adaptable, ethical prompt strategies |

### Industry Documentation (2025-2026)

| Source | Date | Content |
|--------|------|---------|
| [Anthropic: XML tags in prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags) | 2025 | Claude trained on XML; XML improves parsing for Claude specifically |
| [OpenAI: Structured Outputs](https://openai.com/index/introducing-structured-outputs-in-the-api/) | 2024-2025 | 100% schema compliance with server-side enforcement |
| [Structured Output Comparison across LLM Providers](https://medium.com/@rosgluk/structured-output-comparison-across-popular-llm-providers-openai-gemini-anthropic-mistral-and-1a5d42fa612a) | Oct 2025 | Side-by-side comparison of structured output approaches |
| [LiteLLM: Prompt Formatting](https://docs.litellm.ai/docs/completion/prompt_formatting) | 2025 | Automatic chat template handling for open-source models |
| [Hugging Face: Chat Templates](https://huggingface.co/learn/llm-course/chapter11/2) | 2025 | Standardized template system for open-source models |
| [Lakera: Prompt Engineering Guide 2026](https://www.lakera.ai/blog/prompt-engineering-guide) | 2026 | Cross-provider prompt engineering best practices |
| [Prompt Portability Discussion](https://community.openai.com/t/the-portability-of-a-llm-prompt/311147) | 2024 | Community analysis of prompt transfer challenges |

### Framework Documentation (2025-2026)

| Source | Date | Content |
|--------|------|---------|
| [LiteLLM Providers](https://docs.litellm.ai/docs/providers) | 2025 | 100+ supported LLM providers |
| [LiteLLM GitHub](https://github.com/BerriAI/litellm) | 2025 | API proxy architecture and features |
| [CrewAI Agent Configuration](https://docs.crewai.com/core-concepts/Agents/) | 2025 | YAML-based agent definition format |
| [Google ADK Agents Documentation](https://google.github.io/adk-docs/agents/) | 2025 | Agent definition and composition patterns |
| [DSPy Official Site](https://dspy.ai/) | 2025 | Programming-not-prompting paradigm |
| [Haystack GitHub](https://github.com/deepset-ai/haystack) | 2025 | Pipeline abstraction and FallbackChatGenerator |

### Jerry Framework References

| Source | Date | Content |
|--------|------|---------|
| Jerry Framework AGENTS.md | 2026-02-20 | Agent definition template and schema; 37 existing agents across 8 skills |
| Jerry Framework PS_AGENT_TEMPLATE.md | 2026-01-11 | Federated core template v1.0 with YAML frontmatter schema |
| Jerry ps-researcher agent definition | 2026-02-14 | Exemplar agent definition (v2.3.0) |
| Jerry adv-executor agent definition | 2026-02-15 | Exemplar agent definition (v1.0.0) |
