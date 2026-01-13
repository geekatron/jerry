# Research: Agent/Skill Architecture Patterns

> **PS ID:** proj-003
> **Entry ID:** e-003
> **Topic:** Agent/Skill Architecture Patterns in AI/LLM Systems
> **Date:** 2026-01-12
> **Author:** ps-researcher (v2.0.0)
> **Status:** Complete

---

## L0: Executive Summary

Industry consensus in 2025-2026 favors **centralized agent registries** with **skill-local capability definitions**. The dominant pattern is:

1. **Central orchestration layer** - A registry or catalog of agents with metadata
2. **Modular agent definitions** - Agents defined close to their capabilities
3. **Hierarchical organization** - Parent-child agent relationships with clear delegation

**Key Recommendation for Jerry:** Consider a **hybrid approach**:
- Keep `.claude/agents/` for framework-level orchestration agents (orchestrator, QA, security)
- Move skill-specific agents to `skills/{skill}/agents/` (problem-solving agents)
- Implement an agent registry manifest that indexes all agents

This mirrors the industry pattern where general-purpose coordination agents are centralized while specialized capability agents live with their domains.

---

## L1: Technical Summary

### Industry Framework Comparison

| Framework | Agent Location | Skill/Tool Location | Registry Pattern |
|-----------|---------------|---------------------|------------------|
| Google ADK | Hierarchical tree | Tools list on agents | Parent-child sub_agents |
| LangChain/LangGraph | Node definitions | Tool bindings | Graph-based orchestration |
| Microsoft Agent Framework | Agent Registry | Semantic Kernel plugins | Centralized + distributed |
| OpenAI Agents SDK | Agent definitions | Tools on agents | Handoff patterns |
| CrewAI | `agents.yaml` config | `tools/` directory | Crew-based organization |
| Anthropic Claude | Single-threaded loop | Computer use tools | Subagent delegation |

### Emerging Standards

1. **AGENTS.md Convention** - 60,000+ projects use this for machine-readable project context
2. **Proposed `.agent/` Directory** - Standardization proposal for centralized agent configuration
3. **MCP (Model Context Protocol)** - Industry standard for tool/capability integration

### Key Architectural Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Orchestrator-Worker | Central coordinator delegates to specialists | Complex multi-domain tasks |
| Sequential Pipeline | Linear agent chain | Data processing workflows |
| Skills Pattern | Single agent loads specialized prompts on-demand | Token-efficient generalists |
| Handoffs | Agents transfer control via tool calls | Domain transitions |
| Coordinator | LLM-driven routing to sub-agents | Request classification |

### Token Economics

- Single agent chat: baseline
- Single agent with tools: ~4x tokens
- Multi-agent systems: ~15x tokens

**Implication:** Reserve multi-agent for high-value tasks where cost is justified.

---

## L2: Architectural Deep Dive

### 1. Multi-Agent Patterns Across Frameworks

#### Google ADK (Agent Development Kit)

Google's ADK, released at Cloud NEXT 2025, provides the most comprehensive multi-agent pattern catalog:

**Eight Essential Design Patterns:**

1. **Sequential Pipeline** - Linear agent chain using `SequentialAgent`
2. **Coordinator/Dispatcher** - LLM-driven delegation via `transfer_to_agent()`
3. **Agents as Tools** - Wrapping agents as callable functions via `AgentTool`
4. **Parallel Fan-Out/Gather** - Concurrent execution via `ParallelAgent`
5. **Hierarchical Task Decomposition** - Multi-level agent trees
6. **Generator-Critic** - Review/critique loops
7. **Iterative Refinement** - Loop-based improvement via `LoopAgent`
8. **Human-in-the-Loop** - Policy-based execution pauses

**Key Structural Principle:**
> "You create a tree structure by passing a list of agent instances to the `sub_agents` argument when initializing a parent agent." [1]

**Single Parent Rule:** Each agent can only have one parent - attempting multiple parent assignments raises `ValueError`.

**Communication Mechanisms:**
- Shared Session State: `session.state` dictionary
- LLM-Driven Delegation: `transfer_to_agent()` function
- Explicit Invocation: `AgentTool` wrappers

#### LangChain/LangGraph

LangChain identifies four primary multi-agent patterns:

1. **Subagents Pattern** - Main agent coordinates subagents as tools
2. **Handoffs Pattern** - Agents transfer control to each other
3. **Skills Pattern** - Single agent loads specialized prompts on-demand
4. **Router Pattern** - Input classification to specialized agents

**Skills vs Tools - Critical Distinction:**

> "Skills offer two advantages over traditional tools: The first benefit is token efficiency." [2]

Skills use **progressive disclosure** - only YAML frontmatter loads initially. Full SKILL.md content loads only when needed, preventing context window bloat.

**Deep Agents Architecture (v1.1.0):**
- Planning tool
- Sub-agents for delegation
- File system access
- Detailed prompts

**Performance Data:**
- Handoffs, Skills, Router: 3 calls for single tasks
- Subagents: +1 call overhead (centralized control tradeoff)
- Stateful patterns: 40-50% savings on repeat requests

#### Microsoft Agent Framework (AutoGen + Semantic Kernel Merger)

Released October 2025, Microsoft unified AutoGen and Semantic Kernel:

**Orchestration Patterns:**
1. Sequential - Step-by-step workflows
2. Concurrent - Parallel agent execution
3. Group Chat - Collaborative brainstorming
4. Handoff - Context-aware responsibility transfer
5. Magentic - Manager agent with dynamic task ledger

**Agent Organization Principles:**
- Monitor agent overlap to prevent redundancy
- Group similar agents under shared interfaces
- Introduce supervisors as architecture scales
- Use hierarchical organization (supervisor -> agent group)

**Registry Pattern:**
The Agent Registry maintains:
- Agent metadata and capabilities
- Endpoints and security credentials
- Performance metrics and version history
- Dynamic lifecycle management

#### OpenAI Agents SDK

Evolved from Swarm, the SDK uses four primitives:

1. **Agents** - LLM instances with instructions/tools
2. **Handoffs** - Delegation mechanisms
3. **Guardrails** - Input/output validation
4. **Sessions** - Automatic conversation history

**Design Philosophy:**
> "The framework prioritizes accessibility through 'very few abstractions' while remaining 'production-ready.'" [3]

**AgentKit Platform (October 2025):**
- Visual canvas for workflow composition
- Drag-and-drop node connections
- Preview runs and versioning
- Inline eval configuration

#### CrewAI

CrewAI uses a declarative YAML approach:

**Standard Project Structure:**
```
project-name/
├── .env
├── pyproject.toml
├── knowledge/           # Knowledge files (PDFs, etc.)
└── src/
    └── project_name/
        ├── config/
        │   ├── agents.yaml   # Agent definitions
        │   └── tasks.yaml    # Task definitions
        ├── tools/            # Custom tools
        ├── crew.py           # Crew orchestration
        └── main.py
```

**Two Complementary Paradigms:**
1. **Crews** - Autonomous agent collaboration
2. **Flows** - Event-driven workflows (deterministic backbone)

### 2. Anthropic's Approach

#### Multi-Agent Research System

Anthropic's production system uses **orchestrator-worker pattern**:

> "A lead agent coordinates the process while delegating to specialized subagents that operate in parallel." [4]

**Performance Results:**
- Multi-agent Claude Opus 4 + Sonnet 4 subagents: 90.2% improvement over single Claude Opus 4
- Token usage explains 80% of performance variance

**Agent Hierarchy:**
1. **LeadResearcher** - Strategy and coordination
2. **Subagents** - Parallel research execution
3. **Citation Agent** - Post-processing

**Key Recommendations:**
- Avoid "game of telephone" - store outputs externally vs routing through coordinators
- Clear task boundaries with effort budgets
- Tool selection heuristics: examine tools first, match to intent
- Implement checkpoints for long-running agents

#### Claude Code Architecture

Production implementation uses:

> "Single-threaded master loop enhanced with real-time steering capabilities, comprehensive developer tools, and controlled parallelism through limited sub-agent spawning." [5]

**Subagent Pattern:**
> "A subagent is very useful for handling context window limits... Whenever Claude needs to do research or figure out where a bug is, it will do it in the subagent." [6]

Key insight: Subagents protect the main agent's context window.

#### Building Effective Agents (Anthropic Research)

Six foundational patterns:

1. **Augmented LLM** - Basic building block with retrieval/tools/memory
2. **Prompt Chaining** - Sequential LLM calls
3. **Routing** - Input classification
4. **Parallelization** - Concurrent subtasks
5. **Orchestrator-Workers** - Dynamic delegation
6. **Evaluator-Optimizer** - Iterative refinement

**Core Principle:**
> "Start with optimized single LLM calls with retrieval and context. Only add complexity when simpler solutions demonstrably fail." [7]

### 3. File Structure Conventions

#### Industry Patterns

| Convention | Pattern | Adoption |
|------------|---------|----------|
| Central `agents/` | All agents in one directory | Common (Mastra, general templates) |
| Config-based | YAML files (agents.yaml) | CrewAI, enterprise |
| Skill-local | Agents within skill directories | Emerging (LangChain skills) |
| Hybrid | Central orchestration + local specialists | Recommended |

#### AGENTS.md Standard

> "A simple Markdown file placed in the project to document clear instructions" for AI coding agents. [8]

- 60,000+ open-source projects use it
- Hierarchical support (per-subdirectory AGENTS.md)
- Machine-readable alternative to README.md

#### Proposed `.agent/` Directory Standard

GitHub proposal for centralized agent configuration:

```
├── AGENT.md              # Meta-guide for behavior/standards
└── .agent/
    ├── spec/             # Requirements, design, tasks
    │   ├── requirement.md
    │   ├── design.md
    │   └── tasks.md
    ├── wiki/             # Architecture, domain knowledge
    └── links/            # External resource URIs
```

**Benefits Cited:**
1. Interoperability - Any agent finds context in compliant repos
2. Enhanced capabilities - Code validation against specs
3. Human-agent collaboration - Version-controlled contract
4. Extensibility - Team customization

### 4. Agent Registry Patterns

#### Purpose

> "An AI Agent Registry serves as a centralized (or federated) catalog of running agents and their metadata." [9]

**Key Functions:**
- Capability discovery and orchestration
- Agent metadata storage (capabilities, endpoints, resources)
- Dynamic updates as capabilities change
- Lifecycle management

#### Architecture Options

| Type | Description | Use Case |
|------|-------------|----------|
| Centralized | Single registry for all agents | Monolithic systems |
| Distributed | Per-agent or per-group registries | Microservices, edge |
| Federated | Multiple connected registries | Enterprise multi-domain |

#### Metadata Standards

- **MCP**: Centralized GitHub-based `mcp.json` registry
- **A2A**: Decentralized "Agent Card" JSON files
- **NANDA**: "AgentFacts" schema with cryptographic signing

#### Enterprise Considerations

> "During the registration process, it's recommended to contain a validation step to evaluate the validity of the agent being registered." [10]

### 5. MCP (Model Context Protocol) Integration

Released November 2024, donated to Linux Foundation December 2025:

**Architecture:**
- Host Application (receives requests)
- MCP Client (orchestration logic)
- MCP Server (exposes tools/resources)

**Core Primitives:**
- **Tools** - Actions AI can request
- **Resources** - Structured data sources
- **Prompts** - Predefined templates

**2025 Spec Updates:**
- Tool calling in sampling requests
- Server-side agent loops
- Parallel tool calls
- Better context control

**Adoption:** OpenAI (March 2025), thousands of community servers, all major language SDKs.

---

## Recommendations for Jerry

### Current State Analysis

Jerry currently has:
- `.claude/agents/` - Framework-level agents (orchestrator, QA, security)
- `skills/problem-solving/agents/` - Skill-specific agents (ps-researcher, etc.)

This is already a **hybrid pattern** aligning with industry best practices.

### Recommended Architecture

#### Option A: Formalize Current Hybrid (Recommended)

Keep the current structure but formalize with an agent registry:

```
.claude/
├── agents/
│   ├── REGISTRY.md          # Central agent index
│   ├── orchestrator.md      # Framework orchestrator
│   ├── qa-engineer.md       # Cross-cutting QA
│   └── security-auditor.md  # Cross-cutting security
│
skills/
├── problem-solving/
│   ├── SKILL.md
│   └── agents/              # Skill-local specialists
│       ├── ps-researcher.md
│       ├── ps-analyst.md
│       └── ...
└── worktracker/
    ├── SKILL.md
    └── agents/              # (if needed)
        └── wt-operator.md
```

**REGISTRY.md Content:**
```yaml
# Agent Registry
version: "1.0.0"

framework_agents:
  - id: orchestrator
    path: .claude/agents/orchestrator.md
    role: Conductor (Opus 4.5)
    scope: global

  - id: qa-engineer
    path: .claude/agents/qa-engineer.md
    role: Test specialist
    scope: global

skill_agents:
  problem-solving:
    - id: ps-researcher
      path: skills/problem-solving/agents/ps-researcher.md
      role: Research Specialist
```

#### Option B: Full Centralization

Move all agents to `.claude/agents/`:

```
.claude/
└── agents/
    ├── framework/
    │   ├── orchestrator.md
    │   ├── qa-engineer.md
    │   └── security-auditor.md
    └── skills/
        └── problem-solving/
            ├── ps-researcher.md
            └── ...
```

**Drawback:** Breaks skill encapsulation; agents become disconnected from their skill context.

#### Option C: Full Distribution

Move all agents to skills:

```
skills/
├── framework/
│   └── agents/
│       ├── orchestrator.md
│       └── ...
└── problem-solving/
    └── agents/
        └── ...
```

**Drawback:** Loses framework-level distinction; harder to find orchestration agents.

### Decision Matrix

| Criterion | Option A (Hybrid) | Option B (Central) | Option C (Distributed) |
|-----------|-------------------|--------------------|-----------------------|
| Industry alignment | High | Medium | Medium |
| Skill encapsulation | High | Low | High |
| Discoverability | High (with registry) | High | Low |
| Maintenance | Medium | High | Low |
| Scalability | High | Medium | High |
| **Recommendation** | **Preferred** | Acceptable | Not recommended |

### Implementation Guidance

1. **Create REGISTRY.md** - Index all agents with metadata
2. **Document agent scopes** - Framework vs skill-local
3. **Define handoff protocols** - How orchestrator delegates to skill agents
4. **Add capability declarations** - What each agent can/cannot do

---

## Sources

1. [Google ADK Multi-Agent Documentation](https://google.github.io/adk-docs/agents/multi-agents/)
2. [LangChain: Using Skills with Deep Agents](https://blog.langchain.com/using-skills-with-deep-agents/)
3. [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
4. [Anthropic: How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
5. [Claude Code Agent Architecture: Single-Threaded Master Loop](https://www.zenml.io/llmops-database/claude-code-agent-architecture-single-threaded-master-loop-for-autonomous-coding)
6. [Agent Ready Ep8: Anthropic Architecture Discussion](https://stytch.com/blog/agent-ready-ep8-anthropic-cloudflare-arcade-agent-architecture/)
7. [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
8. [Builder.io: Improve Your AI Code Output with AGENTS.md](https://www.builder.io/blog/agents-md)
9. [TrueFoundry: What is AI Agent Registry](https://www.truefoundry.com/blog/ai-agent-registry)
10. [Microsoft Multi-Agent Reference Architecture](https://microsoft.github.io/multi-agent-reference-architecture/docs/reference-architecture/Reference-Architecture.html)
11. [Google Developers Blog: Developer's Guide to Multi-Agent Patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
12. [Microsoft Agent Framework Introduction](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview)
13. [OpenAI for Developers 2025](https://developers.openai.com/blog/openai-for-developers-2025)
14. [CrewAI: Agents Documentation](https://docs.crewai.com/en/concepts/agents)
15. [Model Context Protocol Specification](https://modelcontextprotocol.io/specification/2025-11-25)
16. [GitHub: Proposal for .agent Directory Standard](https://github.com/openai/agents.md/issues/71)
17. [LangChain Multi-Agent Documentation](https://docs.langchain.com/oss/python/langchain/multi-agent)
18. [Microsoft Agent Registry Documentation](https://microsoft.github.io/multi-agent-reference-architecture/docs/agent-registry/Agent-Registry.html)
19. [Eclipse LMOS Agent Registry](https://eclipse.dev/lmos/docs/multi_agent_system/agent_registry/)
20. [Anthropic: Introducing Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)

---

## Appendix A: Framework Feature Comparison

| Feature | Google ADK | LangChain | MS Agent Framework | OpenAI SDK | CrewAI |
|---------|-----------|-----------|-------------------|------------|--------|
| Agent hierarchy | Tree structure | Graph nodes | Registry-based | Flat + handoffs | Crew-based |
| Workflow agents | Sequential, Parallel, Loop | LangGraph | Semantic Kernel | Agent loop | Flows |
| Tool integration | AgentTool wrapper | Tool bindings | Plugins | Tools list | Tools directory |
| State management | Session state | Graph state | Kernel memory | Sessions | Crew state |
| LLM flexibility | Model-agnostic | Multiple providers | Azure-optimized | OpenAI-first | Multiple |
| Open source | Yes | Yes | Yes | Yes | Yes |

## Appendix B: Terminology Mapping

| Jerry Term | Google ADK | LangChain | Microsoft | OpenAI | CrewAI |
|------------|-----------|-----------|-----------|--------|--------|
| Agent | Agent/LlmAgent | Agent | Agent | Agent | Agent |
| Skill | - | Skill | Plugin | - | - |
| Tool | Tool | Tool | Function | Tool | Tool |
| Orchestrator | Coordinator | Graph | Orchestrator | Runner | Manager |
| Worker | SubAgent | Node | Worker Agent | - | Worker |

## Appendix C: Jerry-Specific Mapping

Current Jerry architecture maps to industry patterns:

| Jerry Component | Industry Pattern | Notes |
|-----------------|------------------|-------|
| `.claude/agents/orchestrator.md` | Coordinator/Dispatcher | Framework-level routing |
| `skills/problem-solving/agents/*` | Specialist Subagents | Domain-specific workers |
| `SKILL.md` | Skill Definition | Progressive disclosure pattern |
| Claude Code invocation | Agent Loop | Single-threaded master loop |
| Subagent spawning | Context protection | Protects main context window |

---

*Research completed per P-001 (Truth and Accuracy) and P-002 (File Persistence) principles.*
