# E-002: Multi-LLM Agent Framework Analysis

> Stream E: LLM Portability | PROJ-010 Cyber Ops | Phase 1 Research

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level findings and implications |
| [L1: Key Findings](#l1-key-findings) | Structured findings organized by theme |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Per-framework analysis and comparison matrix |
| [Evidence and Citations](#evidence-and-citations) | Dated sources, categorized |
| [Recommendations](#recommendations) | Specific recommendations for PROJ-010 portability |

---

## L0: Executive Summary

The multi-LLM agent framework landscape in 2025-2026 has converged on a common architectural pattern: abstract the model behind a unified interface, define agents as behavioral configurations, and treat tools as typed function schemas. Eight frameworks were analyzed -- LangChain, AutoGen, CrewAI, LiteLLM, Google ADK, Semantic Kernel, Haystack, and DSPy. Each takes a distinct approach to LLM portability, ranging from LiteLLM's pure API translation layer to DSPy's "programming, not prompting" paradigm that compiles model-specific prompts from declarative signatures. The strongest lesson for PROJ-010 is that successful portability requires three layers: (1) a model abstraction interface that normalizes API calls, (2) an agent definition format that captures intent without provider-specific syntax, and (3) a tool schema format based on JSON Schema. No framework achieves perfect portability -- all involve tradeoffs between provider-specific optimization and cross-provider compatibility. The most transferable pattern is the "agent-as-configuration" approach used by CrewAI and LangChain, combined with LiteLLM's provider translation for API normalization.

---

## L1: Key Findings

### Finding 1: Model Abstraction Has Converged on the OpenAI Format as De Facto Standard

LiteLLM, LangChain, CrewAI, Haystack, Google ADK, and AutoGen all use OpenAI's chat completion format (`messages`, `tools`, `response_format`) as the baseline interface, translating to provider-native formats behind the scenes. This convergence means agent systems built against the OpenAI message format gain significant portability. Even Google ADK, which is optimized for Gemini, offers LiteLLM integration for cross-provider support.

**Implication for PROJ-010:** Adopting the OpenAI message schema as the internal canonical format is a pragmatic choice that aligns with the ecosystem consensus.

### Finding 2: Agent Definition Approaches Fall into Three Categories

| Category | Frameworks | Approach |
|----------|-----------|----------|
| **Configuration-driven** | CrewAI, LangChain (LCEL) | YAML/code configs define role, goal, tools, LLM |
| **Conversation-driven** | AutoGen, Microsoft Agent Framework | Agents defined by conversational behavior and message patterns |
| **Declarative/compiled** | DSPy | Agents defined as typed signatures; prompts compiled per model |

Configuration-driven is the most directly applicable to PROJ-010's markdown-based agent definitions. DSPy's compiled approach offers the strongest theoretical portability guarantees but requires a fundamentally different architecture.

### Finding 3: Tool Abstraction Is the Most Solved Problem

Every framework analyzed uses JSON Schema (or a close variant) for tool parameter definitions. The schema is nearly identical across frameworks:

```json
{
  "name": "tool_name",
  "description": "What the tool does",
  "parameters": {
    "type": "object",
    "properties": { ... },
    "required": [ ... ]
  }
}
```

Differences exist only in the envelope (how the schema is registered with the framework) and invocation protocol (how the model's tool call is routed to execution).

**Implication for PROJ-010:** Tool definitions are the most portable element. PROJ-010 can define tools once and expect minimal adaptation across frameworks and providers.

### Finding 4: No Framework Solves the "Optimal Prompt Per Model" Problem

While all frameworks abstract the API layer, none automatically optimize the actual prompt content for a specific model. LiteLLM translates API formats but does not modify prompt text. LangChain provides prompt templates but requires manual per-model variants. CrewAI uses a single prompt format across models. Only DSPy attempts automatic prompt optimization via compilation, but this requires labeled data and training runs.

**Implication for PROJ-010:** Prompt content portability must be handled by PROJ-010's own rendering layer, not delegated to a framework. The E-001 universal patterns research directly addresses this gap.

### Finding 5: Microsoft's Convergence of AutoGen and Semantic Kernel Signals Industry Direction

In October 2025, Microsoft merged AutoGen and Semantic Kernel into the unified "Microsoft Agent Framework." This framework combines AutoGen's simple agent abstractions with Semantic Kernel's enterprise features (session state, type safety, middleware, telemetry) and adds graph-based workflows. It now integrates with the Claude Agent SDK, demonstrating that even vendor-aligned frameworks are embracing cross-provider support.

**Implication for PROJ-010:** The industry is moving toward framework-agnostic agent protocols (MCP, A2A) rather than framework-specific agent definitions. PROJ-010 should align with these emerging standards.

### Finding 6: Haystack's FallbackChatGenerator Pattern Is a Best Practice

Haystack introduced a `FallbackChatGenerator` that runs multiple LLMs sequentially with automatic fallback when one fails. This pattern -- where model selection is a runtime concern, not a design-time decision -- represents the most robust approach to provider portability.

**Implication for PROJ-010:** Agent definitions should support model fallback chains, not just single model assignments.

---

## L2: Detailed Analysis

### Framework Comparison Matrix

| Framework | Model Abstraction | Agent Definition Format | Tool Abstraction | Portability Level | Key Limitation |
|-----------|-------------------|------------------------|-------------------|-------------------|----------------|
| **LangChain** | `BaseChatModel` + `init_chat_model()`; per-provider packages (`langchain-openai`, `langchain-anthropic`) | Code-first with Runnable chains (LCEL); prompt templates; agent factory pattern | `@tool` decorator; Pydantic schemas; `with_structured_output()` | HIGH (API) / MEDIUM (prompts) | Prompt templates require manual per-model tuning; heavy dependency graph |
| **AutoGen** | Provider-agnostic via config; mix models from different providers | `ConversableAgent` class; conversation patterns; message-based behavior | Function registration on agents; JSON Schema params | HIGH (API) / MEDIUM (behavior) | Complex orchestration patterns tightly coupled to framework |
| **CrewAI** | Native SDK integration; `llm` field per agent; supports `provider/model` format | YAML config (`config/agents.yaml`): role, goal, backstory, tools, llm | LangChain/LlamaIndex tool compatibility; `@tool` decorator | HIGH (definition) / HIGH (API) | Limited control over prompt rendering; opinionated workflow |
| **LiteLLM** | OpenAI-format translation to 100+ providers; drop-in replacement for `openai.ChatCompletion` | N/A (API layer, not agent framework) | Translates OpenAI tool calling format to provider-native | VERY HIGH (API) | No agent abstraction; purely API translation |
| **Google ADK** | Optimized for Gemini; LiteLLM integration for other providers | `Agent` class with name, model, instruction, tools; sub-agents for composition | `FunctionDeclaration` with JSON Schema; built-in Google tools | MEDIUM (Gemini-optimized) | Strongest with Google ecosystem; other providers via LiteLLM indirection |
| **Semantic Kernel / MS Agent Framework** | Plugin architecture; connectors for OpenAI, Azure, Anthropic, others | `[KernelFunction]` decorated methods in plugin classes; agent definitions via code | Plugin functions with typed parameters; automatic schema generation | HIGH (API) / HIGH (enterprise) | .NET/C# primary; Python support is secondary |
| **Haystack** | Model-agnostic components; per-provider generators (`OpenAIChatGenerator`, `AnthropicChatGenerator`) | Pipeline graphs with typed components; `FallbackChatGenerator` for multi-model | Pipeline components with typed I/O; tool integration via components | HIGH (pipeline) / HIGH (fallback) | Pipeline abstraction adds complexity; less suited for simple agents |
| **DSPy** | Model-agnostic signatures; compiled prompts; supports any LM via `dspy.LM()` | Declarative signatures (input/output types); modules compose into programs | Native Python functions as tools; typed I/O | VERY HIGH (compiled) | Requires labeled data for optimization; steep learning curve; different paradigm |

### Per-Framework Detailed Analysis

#### LangChain

**Model Abstraction:** LangChain's `BaseChatModel` is the core abstraction. All chat models implement the `Runnable` interface, providing a consistent API for invocation, streaming, batching, and structured output. The `init_chat_model()` function enables runtime model selection by string identifier (e.g., `"openai:gpt-4o"`, `"anthropic:claude-3-opus"`). Each provider requires a separate integration package (`langchain-openai`, `langchain-anthropic`, `langchain-google-genai`).

**Agent Definition:** Agents are defined as chains of `Runnable` components using LangChain Expression Language (LCEL). The agent factory pattern creates agents with middleware support. Prompt templates can include variables and conditional logic but are not automatically adapted per model.

**Tool Integration:** Tools are defined via the `@tool` decorator or Pydantic models. The `with_structured_output()` method enables schema-based output across providers (adapting to each provider's native mechanism).

**Portability Strengths:**
- Widest provider coverage through ecosystem packages
- `init_chat_model()` enables runtime model switching
- `with_structured_output()` abstracts structured output differences

**Portability Limitations:**
- Prompt templates are static; no per-model optimization
- Provider packages must be installed separately
- Complex dependency graph increases integration cost

**Lessons for PROJ-010:** LangChain's `BaseChatModel` interface demonstrates the minimum viable abstraction: `invoke(messages) -> AIMessage`. The `with_structured_output()` pattern of abstracting enforcement mechanism while keeping schema constant is directly applicable.

#### AutoGen / Microsoft Agent Framework

**Model Abstraction:** AutoGen's redesigned v0.4 architecture (January 2025) uses a layered system. The Core API handles message passing and event-driven runtime. The AgentChat API provides higher-level patterns. Model configuration is provider-agnostic via settings that specify model, API key, and endpoint. Different agents in the same system can use different providers.

**Agent Definition:** The `ConversableAgent` class is the primary agent type. Agents are defined by their conversational behavior -- how they respond to messages, when they invoke tools, and how they coordinate with other agents. Custom auto-reply functions enable dynamic behavior.

**Tool Integration:** Functions are registered directly on agents. The framework handles schema generation and invocation routing. Tool schemas follow the OpenAI function calling format.

**Portability Strengths:**
- Event-driven architecture enables cross-process, cross-language agents
- Provider-agnostic configuration
- Microsoft Agent Framework adds enterprise features (session state, telemetry)

**Portability Limitations:**
- Conversation patterns are framework-specific
- Migration from AutoGen to Agent Framework is non-trivial
- Heavy abstraction for simple agent use cases

**Lessons for PROJ-010:** AutoGen's conversation pattern approach (rather than prompt-template approach) is relevant for multi-agent orchestration. The separation of agent behavior from model selection is a strong pattern.

#### CrewAI

**Model Abstraction:** CrewAI integrates with providers through their native SDKs. The `llm` field on each agent accepts a string in `provider/model` format (e.g., `"openai/gpt-4.1-mini"`, `"anthropic/claude-3-7-sonnet-latest"`). Different agents in the same crew can use different models, enabling cost-optimized assignments (e.g., GPT-4.1-mini for planning, Claude Sonnet for implementation).

**Agent Definition:** YAML-based configuration is the recommended approach. Each agent has four standard fields in `config/agents.yaml`:

```yaml
security_analyst:
  role: "Senior Threat Analyst"
  goal: "Identify and classify cybersecurity threats"
  backstory: "You are an experienced security analyst with 15 years..."
  llm: "anthropic/claude-sonnet-4-20250514"
```

**Tool Integration:** Tools are Python functions decorated with `@tool`. CrewAI supports LangChain and LlamaIndex tools via conversion, providing broad tool ecosystem compatibility.

**Portability Strengths:**
- YAML agent definitions are inherently portable and human-readable
- `provider/model` format makes model switching trivial
- Role/goal/backstory pattern is provider-agnostic

**Portability Limitations:**
- Limited control over how the role/goal/backstory are rendered into the actual prompt
- CrewAI generates its own internal prompts around the YAML config
- Workflow patterns (sequential, hierarchical) are framework-specific

**Lessons for PROJ-010:** CrewAI's YAML agent definition format is the closest existing pattern to PROJ-010's markdown-based agent definitions. The `role`/`goal`/`backstory` separation is a proven portable pattern. The `provider/model` string format for model assignment is clean and adoptable.

#### LiteLLM

**Model Abstraction:** LiteLLM is a pure API translation layer. It accepts calls in OpenAI's `completion()` format and translates them to provider-native API calls for 100+ providers. This includes translating message formats, tool calling schemas, structured output requests, and streaming responses. The output is normalized back to OpenAI's response format (`choices[0]["message"]["content"]`).

**Agent Definition:** LiteLLM is not an agent framework. It provides no agent definition format. It is an infrastructure component that other frameworks (Google ADK, CrewAI) use for provider abstraction.

**Tool Integration:** LiteLLM translates OpenAI's tool calling format to each provider's native format. Recent additions include an Agent (A2A) Gateway for routing to LangGraph, Azure AI Foundry, and Bedrock AgentCore agents.

**Portability Strengths:**
- Highest provider coverage (100+ LLM APIs)
- Drop-in replacement for OpenAI SDK
- Handles chat template rendering for open-source models automatically
- Proxy server mode enables centralized gateway with auth, cost tracking, fallbacks

**Portability Limitations:**
- API-level only; does not address prompt content portability
- Some provider-specific features may not translate perfectly
- Proxy server adds operational complexity

**Lessons for PROJ-010:** LiteLLM is the strongest candidate for PROJ-010's API translation layer. It solves the mechanical portability problem (different API formats) and is battle-tested at scale. It should be adopted as infrastructure, not as the agent framework itself. The proxy server's fallback and load-balancing features align well with R-010 portability requirements.

#### Google ADK (Agent Development Kit)

**Model Abstraction:** ADK is optimized for Gemini but explicitly model-agnostic. It integrates with LiteLLM for cross-provider support, enabling agents to use any model LiteLLM supports. This hybrid approach provides first-class Gemini experience with fallback to 100+ other models.

**Agent Definition:** Code-first approach with `Agent` class:

```python
agent = Agent(
    name="threat_analyzer",
    model="gemini-2.0-flash",
    instruction="You are a cybersecurity threat analyst...",
    tools=[search_threats, classify_ioc],
    sub_agents=[detail_agent, report_agent]
)
```

**Tool Integration:** `FunctionDeclaration` with JSON Schema parameters. Built-in tools for Google Search, code execution, and Vertex AI integration. Custom tools via standard Python functions.

**Portability Strengths:**
- Model-agnostic via LiteLLM integration
- Deployment-agnostic (local, container, Cloud Run)
- A2A protocol support for remote agent-to-agent communication
- Available in Python, TypeScript, and Go

**Portability Limitations:**
- Strongest within Google ecosystem; other providers via LiteLLM indirection
- Built-in Google tools (Search, Vertex AI) are not portable
- Instruction format may be Gemini-optimized

**Lessons for PROJ-010:** ADK's pattern of "optimized for one provider, portable via LiteLLM" is a pragmatic middle ground. The sub-agent composition pattern and A2A protocol support are relevant for multi-agent orchestration. The multi-language support (Python, TypeScript, Go) is notable.

#### Semantic Kernel / Microsoft Agent Framework

**Model Abstraction:** Plugin architecture with connectors for multiple providers. The October 2025 Agent Framework merges Semantic Kernel's enterprise features with AutoGen's agent abstractions. Connectors exist for OpenAI, Azure OpenAI, Anthropic (via Claude Agent SDK integration), Google, and others.

**Agent Definition:** Kernel functions decorated with `[KernelFunction]` attributes in plugin classes. The Agent Framework adds graph-based workflows for multi-agent orchestration with explicit state management and middleware.

**Tool Integration:** Plugin functions with typed parameters. The framework generates JSON Schema automatically from type annotations. Supports MCP and A2A protocols for interoperability.

**Portability Strengths:**
- MCP, A2A, and OpenAPI standards support
- Claude Agent SDK integration demonstrates cross-vendor commitment
- Enterprise features (session state, telemetry, middleware)
- Strong type safety

**Portability Limitations:**
- .NET/C# is the primary language; Python is secondary
- Enterprise features tied to Microsoft ecosystem (Azure, M365)
- Migration from pure Semantic Kernel or AutoGen is non-trivial

**Lessons for PROJ-010:** The convergence of AutoGen and Semantic Kernel validates the "agent framework consolidation" trend. The MCP/A2A protocol adoption signals that open standards will be the interoperability mechanism, not framework-specific formats.

#### Haystack (deepset)

**Model Abstraction:** Model-agnostic via typed components. Each provider has a dedicated generator component (`OpenAIChatGenerator`, `AnthropicChatGenerator`, `HuggingFaceLocalChatGenerator`). The `FallbackChatGenerator` wraps multiple generators in priority order, providing automatic failover.

**Agent Definition:** Agents are defined as pipeline graphs connecting typed components. Each component has declared input/output types, enabling compile-time validation of pipeline correctness.

**Tool Integration:** Tools are pipeline components with typed I/O. The pipeline graph allows complex routing, branching, and conditional logic.

**Portability Strengths:**
- `FallbackChatGenerator` for multi-model resilience
- Component-based architecture makes model swapping explicit
- Pipeline validation catches integration errors early
- No hidden prompt manipulation

**Portability Limitations:**
- Pipeline abstraction adds complexity for simple agent tasks
- Less suited for conversational agents (more RAG/pipeline-oriented)
- Smaller ecosystem than LangChain

**Lessons for PROJ-010:** Haystack's `FallbackChatGenerator` pattern is directly applicable -- agent definitions should support model fallback chains. The typed component approach with compile-time validation is a strong engineering pattern.

#### DSPy (Stanford)

**Model Abstraction:** DSPy takes a fundamentally different approach: instead of translating prompts across providers, it eliminates manual prompting entirely. Agents are defined as typed signatures (input/output specifications) and modules. The framework compiles these signatures into model-specific prompts via optimizers.

**Agent Definition:** Declarative signatures specify what the module does, not how:

```python
class ThreatAnalysis(dspy.Signature):
    """Analyze a security event and classify the threat level."""
    event_description: str = dspy.InputField()
    threat_level: str = dspy.OutputField(desc="critical/high/medium/low")
    classification: str = dspy.OutputField(desc="MITRE ATT&CK technique ID")
    confidence: float = dspy.OutputField(desc="0.0 to 1.0")
```

Optimizers (`MIPROv2`, `BootstrapFinetune`) then generate optimal prompts for the target model using training data and metric functions.

**Tool Integration:** Native Python functions serve as tools. Typed I/O ensures interface compatibility.

**Portability Strengths:**
- Theoretically maximum portability: same signature compiles to different prompts per model
- Eliminates prompt engineering as a manual activity
- Empirically-optimized prompts outperform hand-crafted ones
- Model switching requires only recompilation, not prompt rewriting

**Portability Limitations:**
- Requires labeled data and metric functions for optimization
- Compilation adds development overhead
- Paradigm shift from prompt engineering to programming
- Smaller community and less battle-tested in production
- Not suitable for all agent tasks (works best for well-defined I/O tasks)

**Lessons for PROJ-010:** DSPy represents the theoretical ideal of LLM portability -- define intent, compile per model. While adopting DSPy wholesale may be too large a paradigm shift for PROJ-010, the core insight is powerful: **separate the semantic specification from the prompt implementation**. This principle should inform PROJ-010's two-layer architecture even if the compilation is manual rather than automated.

### Cross-Cutting Patterns

#### Pattern: OpenAI Format as Lingua Franca

Every framework uses OpenAI's message format (`system`/`user`/`assistant` roles, `tools` array, `response_format`) as the baseline, either natively or via translation. This is not because OpenAI's format is technically superior, but because it was first to market and has the largest developer ecosystem.

**PROJ-010 implication:** Adopt OpenAI message format as the internal canonical representation. Use LiteLLM for translation to other providers.

#### Pattern: Agent-as-Configuration

CrewAI, LangChain, and Google ADK all define agents as configurations (role, instructions, tools, model) rather than as code. This separation of agent identity from execution logic is the most portable pattern.

**PROJ-010 implication:** PROJ-010's existing markdown agent definitions already follow this pattern. The key addition is formalizing the schema for portable fields vs. provider-specific fields (per E-001 analysis).

#### Pattern: Protocol-Based Interoperability

MCP (Model Context Protocol) and A2A (Agent-to-Agent) are emerging as the standards for tool integration and agent communication respectively. Semantic Kernel, Google ADK, and LiteLLM already support these protocols.

**PROJ-010 implication:** Design for MCP/A2A compatibility from the start. These protocols will likely become the standard mechanism for cross-framework agent interoperability.

#### Pattern: Fallback and Multi-Model Chains

Haystack's `FallbackChatGenerator`, LiteLLM's proxy fallback configuration, and AutoGen's multi-model conversation patterns all address the reality that no single model is always available or optimal.

**PROJ-010 implication:** Agent definitions should support model preference lists, not just single model assignments.

---

## Evidence and Citations

### Framework Official Documentation (2025-2026)

| Source | Date | Content |
|--------|------|---------|
| [LangChain BaseChatModel Reference](https://python.langchain.com/api_reference/core/language_models/langchain_core.language_models.chat_models.BaseChatModel.html) | 2025 | Core model abstraction interface |
| [LangChain init_chat_model](https://api.python.langchain.com/en/latest/chat_models/langchain.chat_models.base.init_chat_model.html) | 2025 | Runtime model initialization |
| [AutoGen Multi-Agent Conversation Framework](https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat/) | 2025 | Conversation patterns and agent architecture |
| [AutoGen GitHub](https://github.com/microsoft/autogen) | 2025 | v0.4 layered architecture redesign |
| [CrewAI LLM Configuration](https://docs.crewai.com/en/concepts/llms) | 2025 | Provider-agnostic model configuration |
| [CrewAI Agent Configuration](https://docs.crewai.com/core-concepts/Agents/) | 2025 | YAML-based agent definition format |
| [LiteLLM Providers](https://docs.litellm.ai/docs/providers) | 2025 | 100+ supported LLM providers |
| [LiteLLM GitHub](https://github.com/BerriAI/litellm) | 2025 | API proxy architecture and features |
| [Google ADK Overview](https://google.github.io/adk-docs/) | 2025 | Agent architecture and model integration |
| [Google ADK Agents Documentation](https://google.github.io/adk-docs/agents/) | 2025 | Agent definition and composition patterns |
| [DSPy Official Site](https://dspy.ai/) | 2025 | Programming-not-prompting paradigm |
| [DSPy GitHub](https://github.com/stanfordnlp/dspy) | 2025 | Signatures, modules, and optimizers |
| [Haystack GitHub](https://github.com/deepset-ai/haystack) | 2025 | Pipeline abstraction and component architecture |
| [Semantic Kernel GitHub](https://github.com/microsoft/semantic-kernel) | 2025 | Plugin architecture and model abstraction |

### Industry Analysis (2025-2026)

| Source | Date | Content |
|--------|------|---------|
| [Microsoft Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview) | Oct 2025 | AutoGen + Semantic Kernel convergence |
| [Semantic Kernel + AutoGen = Microsoft Agent Framework](https://visualstudiomagazine.com/articles/2025/10/01/semantic-kernel-autogen--open-source-microsoft-agent-framework.aspx) | Oct 2025 | Framework consolidation announcement |
| [Google ADK Announcement](https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/) | 2025 | Multi-agent framework launch at Cloud NEXT |
| [Google ADK Architectural Tour](https://thenewstack.io/what-is-googles-agent-development-kit-an-architectural-tour/) | 2025 | Event-driven runtime architecture |
| [Top LLM Gateways 2025](https://agenta.ai/blog/top-llm-gateways) | 2025 | Gateway comparison including LiteLLM |
| [LiteLLM Changelog](https://www.litellm.ai/changelog) | 2026 | Recent features including A2A Gateway |
| [DSPy Hands-on Guide](https://miptgirl.medium.com/programming-not-prompting-a-hands-on-guide-to-dspy-04ea2d966e6d) | 2025 | Practical DSPy implementation patterns |
| [AutoGen Comprehensive Review](https://mgx.dev/insights/259a02509ffd41d8843825f902a4c8d0) | 2025 | Architecture and capabilities analysis |

---

## Recommendations

### R-FW-001: Adopt LiteLLM as the API Translation Layer

Use LiteLLM as the foundational provider abstraction for PROJ-010. It provides the broadest provider coverage (100+ APIs), normalizes the API format, handles chat template rendering for open-source models, and supports tool calling translation.

**Rationale:** LiteLLM is battle-tested, actively maintained, and used as infrastructure by other frameworks (Google ADK, CrewAI). It solves the mechanical API portability problem, freeing PROJ-010 to focus on semantic portability.

**Implementation:** Run LiteLLM as a proxy server for centralized cost tracking, fallback routing, and authentication management.

### R-FW-002: Adopt CrewAI's YAML Agent Definition Pattern

Model PROJ-010's portable agent definition format after CrewAI's `role`/`goal`/`backstory`/`tools`/`llm` structure. This maps naturally to PROJ-010's existing markdown agent definitions and has proven portable across providers.

**Rationale:** CrewAI's YAML format is the most directly analogous to PROJ-010's markdown-based agent definitions. The pattern separates identity (role, goal) from capability (tools, llm) from context (backstory), which maps well to the two-layer architecture recommended in E-001.

**Adaptation:** Extend with PROJ-010-specific fields: `constraints`, `output_schema`, `reasoning_strategy`, `capability_requirements`, `model_preferences` (ordered list for fallback).

### R-FW-003: Design for MCP and A2A Protocol Compatibility

Ensure PROJ-010's agent definitions and tool interfaces are compatible with the Model Context Protocol (MCP) for tool integration and the Agent-to-Agent (A2A) protocol for inter-agent communication.

**Rationale:** MCP and A2A are emerging as industry standards, adopted by Semantic Kernel, Google ADK, LiteLLM, and Anthropic. Designing for these protocols future-proofs PROJ-010 against framework-specific lock-in.

### R-FW-004: Implement Model Fallback Chains per Haystack Pattern

Support ordered model preference lists in agent definitions, with automatic fallback:

```yaml
model_preferences:
  - "anthropic/claude-sonnet-4-20250514"
  - "openai/gpt-4o"
  - "google/gemini-2.0-flash"
  - "ollama/llama3.1:70b"
```

**Rationale:** Haystack's `FallbackChatGenerator` demonstrates that model resilience is an operational requirement. LiteLLM's proxy server supports fallback routing natively.

### R-FW-005: Separate Semantic Intent from Prompt Rendering (DSPy Principle)

Apply DSPy's core insight: define agent behavior as typed specifications (inputs, outputs, constraints) and implement a rendering layer that generates provider-optimized prompts. This need not use DSPy's compilation infrastructure -- manual rendering adapters suffice -- but the separation principle is essential.

**Rationale:** DSPy demonstrates that the same semantic intent compiles to different optimal prompts per model. PROJ-010's two-layer architecture (from E-001) achieves this separation without requiring DSPy's compilation overhead.

### R-FW-006: Use JSON Schema as the Universal Tool Interface

Standardize all tool definitions on JSON Schema for parameters, matching the ecosystem consensus. Implement tools as provider-agnostic typed functions with schema metadata.

**Rationale:** All eight analyzed frameworks use JSON Schema (or a close derivative) for tool definitions. This is the most settled and portable element of the agent ecosystem.

### R-FW-007: Evaluate DSPy for High-Criticality Agent Optimization

For PROJ-010 agents that require maximum accuracy (e.g., threat classification, vulnerability assessment), evaluate DSPy's compiled prompt optimization as an enhancement layer. DSPy can automatically generate model-specific few-shot examples and instructions that outperform hand-crafted prompts.

**Rationale:** DSPy's empirical optimization addresses E-001's finding that few-shot examples and CoT strategies have model-dependent effectiveness. For critical agents where accuracy justifies the compilation overhead, DSPy provides measurable improvements.

**Scope:** This is a MEDIUM-priority enhancement, not a foundational architectural choice. Apply selectively to high-value agents after the base portable architecture is established.
