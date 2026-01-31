# EN-006 Research Synthesis: Context Injection Design

<!--
TEMPLATE: Research Synthesis
SOURCE: ps-researcher + nse-explorer cross-pollinated threads
VERSION: 1.0.0
TASK: TASK-030 Deep Research & Exploration
PHASE: 0
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "en006-research-synthesis"
work_type: RESEARCH
parent_id: "TASK-030"

# === METADATA ===
title: "Context Injection Research Synthesis"
description: |
  Cross-pollinated synthesis of ps-researcher and nse-explorer threads
  investigating context injection patterns across industry frameworks and
  NASA SE stakeholder analysis.

# === AUTHORSHIP ===
created_by: "ps-researcher + nse-explorer"
created_at: "2026-01-26"
updated_at: "2026-01-26"

# === TRACEABILITY ===
requirements_traced:
  - STK-009  # Jerry framework integration
  - IR-004   # SKILL.md interface
  - IR-005   # Hexagonal architecture
  - SK-001   # SKILL.md structure
  - SK-004   # Progressive disclosure
  - MA-001   # Provider-independent design
  - MA-002   # Avoid provider-specific features
```

---

## L0: Executive Summary (ELI5)

**What is Context Injection?**

Imagine you're teaching someone to analyze legal documents. Instead of explaining everything from scratch each time, you give them a "cheat sheet" with legal terms, important patterns, and what to look for. Context injection is like giving AI agents that cheat sheet - domain-specific knowledge that makes them smarter for particular tasks.

**Key Finding:**

Industry leaders (Anthropic, Microsoft, LangChain, CrewAI) all agree: **intelligence is not the bottleneck - context is**. The best AI agents aren't the smartest; they're the ones with the best "cheat sheets" loaded at the right time.

**What We Learned:**

1. **Load context "just-in-time"** - Don't overwhelm with everything upfront
2. **Use structured formats** - YAML, JSON schemas make context machine-readable
3. **Keep it at the "right altitude"** - Not too specific, not too vague
4. **Memory matters** - Agents need short-term, long-term, and entity memory
5. **Standards are emerging** - Model Context Protocol (MCP) is becoming universal

---

## L1: Technical Summary (Software Engineer)

### 1. Research Scope

This synthesis covers context injection patterns from:

| Source | Focus Area | Citation |
|--------|------------|----------|
| LangChain/LangGraph | Middleware patterns, state management | [LangGraph Docs](https://langchain-ai.github.io/langgraph/) |
| CrewAI | Task context, agent memory | [CrewAI Collaboration](https://github.com/crewaiinc/crewai/blob/main/docs/en/concepts/collaboration.mdx) |
| Semantic Kernel | KernelArguments, prompt templates | [Microsoft Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/) |
| Model Context Protocol | Open standard for AI-data integration | [MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25) |
| Anthropic | Context engineering best practices | [Anthropic Engineering Blog](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) |
| NASA SE | Stakeholder expectations (NPR 7123.1D) | [NASA NODIS](https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7123_001D_) |

### 2. Framework Comparison Matrix

| Framework | Context Passing | Memory | State Persistence | Schema |
|-----------|-----------------|--------|-------------------|--------|
| **LangChain/LangGraph** | Middleware decorator | Graph state | Checkpointing | TypedDict |
| **CrewAI** | Task `context=[]` | Short/Long/Entity | Crew-level | YAML |
| **Semantic Kernel** | KernelArguments | AgentThread | Thread-based | PromptTemplate |
| **MCP** | JSON-RPC | Server-managed | Stateful connections | JSON Schema |
| **Claude Code** | CLAUDE.md + skills | Compaction | File system | Markdown + YAML |

### 3. Key Patterns Discovered

#### 3.1 LangChain Middleware Pattern

```python
from langchain.agents.middleware.types import modify_model_request, AgentState, ModelRequest
from langgraph.runtime import Runtime

class Context(TypedDict):
    """Schema defining expected context structure"""
    user_role: str
    domain: str

@modify_model_request
def inject_domain_context(
    request: ModelRequest,
    state: AgentState,
    runtime: Runtime[Context]
) -> ModelRequest:
    """Middleware that injects domain-specific context into prompts"""
    domain = runtime.context.get("domain", "general")

    # Domain-specific prompt modification
    if domain == "legal":
        request.system_prompt += "\n\nLegal analysis guidelines: ..."

    return request

# Agent creation with middleware
agent = create_agent(
    model="openai:gpt-4o",
    tools=[...],
    middleware=[inject_domain_context],
    context_schema=Context  # Type-safe context
)
```

**Key Insight**: LangChain uses decorators to intercept and modify requests, with TypedDict providing type-safe context schemas.

#### 3.2 CrewAI Task Context Pattern

```python
from crewai import Agent, Task, Crew

# Research task produces context
research_task = Task(
    description="Research legal precedents for contract disputes",
    expected_output="Detailed findings with case citations",
    agent=researcher
)

# Writing task consumes context
writing_task = Task(
    description="Draft analysis based on research",
    expected_output="Professional legal analysis",
    agent=writer,
    context=[research_task]  # Explicit dependency injection
)

# Agent with memory for cross-interaction context
analyst = Agent(
    role="Legal Analyst",
    goal="Provide thorough legal analysis",
    memory=True,  # Enables short-term, long-term, entity memory
    verbose=True
)
```

**Key Insight**: CrewAI uses explicit task dependencies and agent-level memory, making context flow visible and traceable.

#### 3.3 Semantic Kernel Arguments Pattern

```python
from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments
from semantic_kernel.prompt_template import PromptTemplateConfig, InputVariable

# Define prompt template with variables
prompt = """
{{$system_context}}

Analyze the following transcript for {{$domain}} patterns:
{{$transcript}}

Focus on: {{$extraction_rules}}
"""

# Configure with typed input variables
template_config = PromptTemplateConfig(
    template=prompt,
    name="domain_analysis",
    template_format="semantic-kernel",
    input_variables=[
        InputVariable(name="system_context", is_required=True),
        InputVariable(name="domain", is_required=True),
        InputVariable(name="transcript", is_required=True),
        InputVariable(name="extraction_rules", is_required=True),
    ]
)

# Pass context via KernelArguments
arguments = KernelArguments(
    system_context="You are a legal document analyst...",
    domain="legal",
    transcript="[transcript content]",
    extraction_rules="Identify parties, obligations, dates..."
)

result = await kernel.invoke(function, arguments)
```

**Key Insight**: Semantic Kernel provides declarative templates with `{{$variable}}` syntax and explicit InputVariable definitions.

#### 3.4 Model Context Protocol (MCP) Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                        MCP Architecture                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────┐         ┌──────────┐         ┌──────────┐   │
│   │   HOST   │◄───────►│  CLIENT  │◄───────►│  SERVER  │   │
│   │ (Claude) │         │(Connector)│         │(Context) │   │
│   └──────────┘         └──────────┘         └──────────┘   │
│                                                              │
│   Server Features:                                           │
│   • Resources: Context and data                              │
│   • Prompts: Templated messages                              │
│   • Tools: Functions to execute                              │
│                                                              │
│   Client Features:                                           │
│   • Sampling: LLM interactions                               │
│   • Roots: Filesystem boundaries                             │
│   • Elicitation: User information requests                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key Insight**: MCP standardizes AI-data integration with JSON-RPC, separating Resources (context), Prompts (templates), and Tools (actions).

### 4. Anthropic Context Engineering Principles

From [Anthropic's Engineering Blog](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents):

#### 4.1 The "Right Altitude" Principle

```
TOO SPECIFIC (Brittle)          RIGHT ALTITUDE           TOO VAGUE (Ineffective)
─────────────────────────────────────────────────────────────────────────────────
"If date format is            "Parse dates using         "Handle dates
 MM/DD/YYYY, use strptime      standard patterns.         appropriately."
 with '%m/%d/%Y'. If           Prefer ISO 8601 when
 DD-MM-YYYY, use..."           output format is
                               unspecified."
```

**Principle**: Instructions should be specific enough to guide behavior but flexible enough to handle variation.

#### 4.2 Just-in-Time Retrieval Strategy

```
┌─────────────────────────────────────────────────────────────┐
│            UPFRONT LOADING          vs    JUST-IN-TIME      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ❌ Load all documents         ✅ Maintain identifiers      │
│   ❌ Pre-fill entire context    ✅ Load data via tools       │
│   ❌ Static, stale data         ✅ Fresh, relevant data      │
│                                                              │
│   Hybrid Approach (Claude Code):                             │
│   • Upfront: CLAUDE.md files (stable context)                │
│   • Runtime: grep/glob exploration (dynamic context)         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 4.3 Context Compaction Strategy

```python
# Compaction preserves critical details while discarding redundancy
compaction_strategy = {
    "preserve": [
        "architectural_decisions",
        "unresolved_bugs",
        "implementation_details",
        "key_findings"
    ],
    "discard": [
        "redundant_tool_outputs",
        "verbose_intermediate_steps",
        "duplicate_file_contents"
    ],
    "compress": [
        "message_history → summary",
        "large_files → key_sections"
    ]
}
```

### 5. Relevant EN-003 Requirements

| Requirement | Description | Context Injection Impact |
|-------------|-------------|-------------------------|
| STK-009 | Jerry framework integration | Must integrate with existing Jerry patterns |
| IR-004 | SKILL.md interface | Context defined in skill files |
| IR-005 | Hexagonal architecture | Context injection as adapter layer |
| SK-001 | SKILL.md structure | YAML frontmatter for context schema |
| SK-004 | Progressive disclosure (<500 lines) | Load context in stages |
| MA-001 | Provider-independent design | Context format must be model-agnostic |
| MA-002 | Avoid provider-specific features | Use standard patterns, not vendor-specific |

---

## L2: Strategic Analysis (Principal Architect)

### 1. Architectural Trade-offs

#### 1.1 Static vs Dynamic Context Loading

| Approach | Pros | Cons | When to Use |
|----------|------|------|-------------|
| **Static** (CLAUDE.md) | Fast, predictable, low latency | Stale, large context overhead | Stable domain knowledge |
| **Dynamic** (tools) | Fresh, targeted, efficient | Latency, complexity | Changing data, user-specific |
| **Hybrid** | Best of both | Implementation complexity | Production systems |

**Recommendation**: Adopt hybrid approach with CLAUDE.md-style static context + tool-based dynamic retrieval.

#### 1.2 Schema Strictness Spectrum

```
LOOSE                                                          STRICT
───────────────────────────────────────────────────────────────────────
  Markdown      YAML       TypedDict    JSON Schema    Protocol Buffers

  ✓ Human-     ✓ Balance   ✓ Type-safe  ✓ Validation   ✓ Binary
    friendly     of both     Python       + IDE          efficient
  ✗ No          ✗ Limited   ✗ Python-    ✗ Complex     ✗ Not human
    validation    typing      only                        readable
```

**Recommendation**: Use YAML for human-editable context files, JSON Schema for validation, TypedDict/Pydantic for runtime.

### 2. One-Way Door Decisions

| Decision | Reversibility | Impact | Recommendation |
|----------|---------------|--------|----------------|
| Context format (YAML vs JSON) | Easy | Medium | YAML (human-friendly) |
| Schema validation approach | Medium | High | JSON Schema + runtime Pydantic |
| Memory persistence strategy | Hard | High | File-based (aligned with Jerry P-002) |
| MCP adoption | Medium | High | Adopt for future-proofing |

### 3. NASA SE Stakeholder Analysis (Process 1)

#### 3.1 Stakeholder Identification

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CONTEXT INJECTION STAKEHOLDERS                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  PRIMARY (End Users)              SECONDARY (Support)                │
│  ─────────────────────            ───────────────────                │
│  • Legal analysts                 • QA teams                         │
│  • Sales managers                 • Operations/SRE                   │
│  • Engineering leads              • Security teams                   │
│  • Domain experts                 • Product managers                 │
│                                                                      │
│  SYSTEM (Developers)              GOVERNANCE                         │
│  ───────────────────              ──────────────                     │
│  • Skill developers               • Compliance officers              │
│  • Agent developers               • Data privacy officers            │
│  • Integration engineers          • Architecture review board        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### 3.2 Stakeholder Expectations to Requirements

| Stakeholder | Expectation | MOE | Derived Requirement |
|-------------|-------------|-----|---------------------|
| Legal analyst | Accurate legal term extraction | 95% precision | REQ: Schema for legal entities |
| Skill developer | Easy domain configuration | <30 min setup time | REQ: YAML-based context files |
| QA team | Testable context injection | 100% deterministic tests | REQ: Mock context provider |
| Security | No sensitive data leakage | Zero incidents | REQ: Context sanitization |
| Operations | Observable context loading | Full traceability | REQ: Context audit logging |

#### 3.3 Measures of Effectiveness (MOEs)

Per NASA SE Process 1, MOEs for context injection:

| MOE | Measurement | Target |
|-----|-------------|--------|
| **Accuracy** | Domain entity extraction F1 score | >= 0.90 |
| **Latency** | Context loading time | < 500ms |
| **Configurability** | Time to create new domain context | < 2 hours |
| **Testability** | Context injection test coverage | >= 95% |
| **Observability** | Context audit trail completeness | 100% |

### 4. Emerging Industry Standards

#### 4.1 Model Context Protocol (MCP) Adoption Timeline

```
Nov 2024    Mar 2025    May 2025    Nov 2025    Dec 2025    Q1 2026
    │           │           │           │           │           │
    ▼           ▼           ▼           ▼           ▼           ▼
  Launch     OpenAI     Microsoft    Major       Linux       General
  by         adopts     joins       spec        Foundation  availability
  Anthropic             steering    update      donation
```

**Strategic Implication**: MCP is becoming the de-facto standard. Design context injection to be MCP-compatible.

#### 4.2 Microsoft Agent Framework Convergence

AutoGen + Semantic Kernel → Microsoft Agent Framework (GA Q1 2026)

**Implication**: Our Semantic Kernel patterns research remains valid; the unified framework will maintain backward compatibility.

### 5. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| MCP becomes incompatible | Low | High | Use adapter pattern, abstract protocol layer |
| Context bloat degrades performance | Medium | Medium | Implement compaction strategy |
| Domain context becomes stale | Medium | Medium | Version context, implement refresh mechanism |
| Security vulnerabilities (prompt injection) | Medium | High | Input sanitization, context boundaries |

---

## Cross-Pollination Synthesis

### ps-researcher Findings

1. **Industry converging on structured context** - All major frameworks use typed schemas
2. **Memory types are standardizing** - Short-term, long-term, entity patterns emerge
3. **Middleware/decorator pattern dominant** - Intercept and modify vs replace
4. **MCP as universal standard** - Cross-vendor adoption accelerating

### nse-explorer Findings

1. **Stakeholder expectations must drive design** - Not technology-first
2. **MOEs provide validation criteria** - Testable, measurable outcomes
3. **Traceability required** - From expectation → requirement → implementation
4. **Quality attributes matter** - Not just functionality (security, observability, testability)

### Synthesis: Design Principles for EN-006

Based on cross-pollinated analysis:

1. **Schema-First Design**: Define context schema before implementation
2. **Hybrid Loading**: Static CLAUDE.md + dynamic tool-based retrieval
3. **MCP Compatibility**: Design for future MCP integration
4. **Stakeholder-Driven MOEs**: Use NASA SE Process 1 measures
5. **Progressive Disclosure**: Load context in stages (<500 lines per stage)
6. **Provider Agnostic**: No vendor-specific features in context format
7. **Auditable Context**: Full traceability of context loading

---

## References

### Primary Sources

1. Anthropic. (2025). *Effective Context Engineering for AI Agents*. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

2. Model Context Protocol. (2025). *MCP Specification 2025-11-25*. https://modelcontextprotocol.io/specification/2025-11-25

3. NASA. (2024). *NASA Systems Engineering Processes and Requirements (NPR 7123.1D)*. https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7123_001D_

4. Microsoft. (2025). *Semantic Kernel Agent Framework Documentation*. https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/

5. LangChain. (2025). *LangGraph Documentation*. https://langchain-ai.github.io/langgraph/

6. CrewAI. (2025). *Agent Collaboration Documentation*. https://github.com/crewaiinc/crewai/blob/main/docs/en/concepts/collaboration.mdx

### Secondary Sources

7. Anthropic. (2025). *Donating MCP to the Agentic AI Foundation*. https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation

8. Microsoft DevBlogs. (2025). *Microsoft's Agentic Frameworks: AutoGen and Semantic Kernel*. https://devblogs.microsoft.com/autogen/microsofts-agentic-frameworks-autogen-and-semantic-kernel/

9. Wikipedia. (2025). *Model Context Protocol*. https://en.wikipedia.org/wiki/Model_Context_Protocol

### Internal References

10. EN-003 Requirements Specification. `REQUIREMENTS-SPECIFICATION.md`

11. EN-003 Requirements Addendum. `REQUIREMENTS-ADDENDUM-001-SKILL-ARCHITECTURE.md`

12. Claude Code Skill Architecture Research. `CLAUDE-CODE-SKILL-ARCHITECTURE-RESEARCH.md`

---

## History

| Date | Version | Author | Notes |
|------|---------|--------|-------|
| 2026-01-26 | 1.0.0 | ps-researcher + nse-explorer | Initial synthesis |

---

*Document ID: en006-research-synthesis*
*Task: TASK-030*
*Phase: 0 (Deep Research & Exploration)*
*Workflow: en006-ctxinj-20260126-001*
