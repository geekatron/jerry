# Industry Best Practices: AI Agent Skills Standards

**Document ID:** init-wt-skills-e-002
**PS ID:** init-wt-skills
**Entry ID:** e-002
**Date:** 2026-01-11
**Author:** ps-researcher agent (v2.0.0)
**Topic:** Industry Best Practices - AI Agent Skills Standards

---

## L0: Executive Summary (ELI5)

The AI agent industry in late 2025 has converged on a shared vision: **modular, composable agents with persistent skills and state management**. Three major players have emerged with complementary approaches.

**Anthropic** has established the Agent Skills standard (released December 2025), which treats skills as "procedural memory" - folders containing instructions, examples, and optional scripts that teach AI agents specialized capabilities. They donated the Model Context Protocol (MCP) to the Linux Foundation's Agentic AI Foundation, co-founded with OpenAI and Block. MCP provides the "plumbing" for tool access, while Skills provide the "brain" for using those tools effectively.

**Google** released the Agent Development Kit (ADK) with explicit workflow orchestration patterns: SequentialAgent (pipeline-style), ParallelAgent (fan-out), and LoopAgent (iterative refinement). Their TypeScript SDK (December 2025) brings these patterns to JavaScript developers. Google emphasizes that context management in multi-agent systems is critical - without scoped context, agents suffer from "context explosion."

**OpenAI** published comprehensive agent best practices emphasizing tool calling patterns, handoffs between agents, and the importance of guardrails at every stage. Their Agents SDK (Python and TypeScript) is provider-agnostic with built-in tracing.

The consensus pattern emerging is **hybrid architectures**: workflow orchestration for coordination combined with injected skills for domain expertise. Monolithic agents remain useful for simple tasks, but the industry has moved toward specialized, composable systems for production workloads.

---

## L1: Technical Analysis (Software Engineer)

### 1. Anthropic Agent Skills Standard

**Release Date:** December 18, 2025
**Specification:** https://agentskills.io/specification
**Repository:** https://github.com/anthropics/skills

#### Core Concept

A Skill is a modular knowledge package: a folder containing a `SKILL.md` file that combines:
- **YAML frontmatter**: Structured metadata (name, description, optional fields)
- **Markdown body**: Natural language instructions for the agent

#### SKILL.md Format Specification

**Required Fields:**
```yaml
---
name: skill-name          # Max 64 chars, lowercase, hyphens only
description: What this skill does and when to use it.  # Max 1024 chars
---
```

**Optional Fields:**
```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files.
license: Apache-2.0
compatibility: Designed for Claude Code
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash(git:*) Bash(jq:*) Read
---
```

**Directory Structure:**
```
skill-name/
├── SKILL.md          # Required entry point
├── scripts/          # Executable Python/Bash/JavaScript
├── references/       # Additional documentation
└── assets/           # Templates, images, data files
```

#### Progressive Disclosure Pattern

Skills are loaded in three tiers to minimize context usage:

1. **Metadata (~100 tokens)**: `name` and `description` loaded at startup
2. **Instructions (<5000 tokens)**: Full `SKILL.md` when skill is activated
3. **Resources (on-demand)**: Files in `scripts/`, `references/`, `assets/`

This pattern is critical for addressing **context rot** - the phenomenon where LLM performance degrades as context window fills.

#### Relationship to MCP

**MCP (Model Context Protocol)** and **Agent Skills** are complementary layers:

| Layer | Purpose | Provides |
|-------|---------|----------|
| MCP | Infrastructure | Secure connectivity to external software and data |
| Skills | Knowledge | Procedural knowledge for using those tools effectively |

As Simon Willison noted: "MCP provides the 'plumbing' for tool access, while agent skills provide the 'brain' or procedural memory."

#### Launch Partners

Skills launched with support from: Atlassian, Figma, Canva, Stripe, Notion, and Zapier.

---

### 2. Google ADK Multi-Agent Patterns

**Release Date:** Cloud NEXT 2025 (Python), December 2025 (TypeScript)
**Documentation:** https://google.github.io/adk-docs/

#### Agent Categories

ADK provides three agent types:

| Type | Role | Use Case |
|------|------|----------|
| **LLM Agents** | "Brains" | Reasoning, decision-making via Gemini |
| **Workflow Agents** | "Managers" | Orchestration without execution |
| **Custom Agents** | "Specialists" | Full Python control via BaseAgent |

#### Workflow Orchestration Patterns

**SequentialAgent (Pipeline)**
```python
# Assembly line: fetch -> clean -> analyze -> summarize
SequentialAgent(sub_agents=[
    fetch_agent,
    clean_agent,
    analyze_agent,
    summarize_agent
])
```
Uses `output_key` to write to shared `session.state` for next agent.

**ParallelAgent (Fan-Out)**
```python
# Concurrent execution for independent tasks
ParallelAgent(sub_agents=[
    api_agent_1,
    api_agent_2,
    api_agent_3
])
```

**LoopAgent (Iteration)**
```python
# Quality gate with exit condition
LoopAgent(
    sub_agents=[generator_agent, critic_agent],
    max_iterations=5
)
```

#### Key Patterns

**Coordinator/Specialist Pattern:**
A central LlmAgent manages several specialized sub_agents, routing requests to appropriate specialists.

**Generator-Critic Pattern:**
Separates content creation from validation. A SequentialAgent manages draft-and-review, while a parent LoopAgent enforces quality gates.

#### Context Management

ADK addresses context explosion through:

1. **Scoped Context Passing**: Explicitly define what callees see
2. **Context Compaction**: LLM-based summarization when thresholds are reached
3. **Shared State via `session.state`**: Controlled communication between agents

---

### 3. OpenAI Agent Patterns

**Documentation:** https://developers.openai.com/tracks/building-agents/
**SDK:** https://cookbook.openai.com/topic/agents

#### Core Principles

> "Agents are systems that independently accomplish tasks on your behalf. They use an LLM to execute instructions and make decisions, with access to tools to gather context and take actions, operating within clearly defined guardrails."

#### Tool Use Patterns

**Tool Calling Flow:**
1. LLM understands user intent
2. Model compares request with registered tool descriptions
3. Tool selection/routing based on semantic match
4. Tool execution with structured parameters
5. Result integration into response

**Best Practices:**
- Request thorough tool-calling preambles
- Disambiguate tool instructions maximally
- Insert agentic persistence reminders
- Handle irrelevant/malicious tool outputs carefully

#### Orchestration Approaches

**Manager Pattern (Hub-and-Spoke):**
```
           [Manager Agent]
          /       |       \
     [Agent A] [Agent B] [Agent C]
```
Edges represent tool calls from manager to workers.

**Decentralized Pattern (Handoffs):**
```
[Agent A] <--> [Agent B] <--> [Agent C]
```
Edges represent intelligent handoffs between peer agents.

**Agent-as-Tool Pattern:**
Expose one agent as a callable tool for another, sharing memory keyed by `conversation_id`.

#### Built-in Tracing

The Agents SDK provides automatic tracing: which tools were called, which agents were used, which guardrails were triggered. Enables rapid iteration without additional instrumentation code.

---

### 4. Composable vs Monolithic Agents

#### Industry Trend

By late 2025, **hybrids are prevailing**: orchestrated workflows with injected skills for domain expertise.

| Approach | Best For | Trade-offs |
|----------|----------|------------|
| **Monolithic** | Simple Q&A, RAG, rapid prototyping | Faster, cheaper, easier to debug |
| **Composable** | Multi-step workflows, production systems | 37% shorter time-to-market, better resilience |
| **Hybrid** | Enterprise production | Orchestration + specialization |

#### Benefits of Composable Agents

1. **Flexibility**: New tools/models as modules without retraining
2. **Cost Efficiency**: Pay for what you need; specialized models vs. GPT-4 for everything
3. **Speed**: 30% higher ROI, weekly feature releases
4. **Resilience**: Module failure isolation
5. **Quality**: Best model per task

#### Challenges of Composable Agents

1. **Complexity**: Sophisticated orchestration required
2. **Latency Overhead**: Network/processing per module
3. **Security**: Multiple attack surfaces
4. **Higher Initial Investment**: Planning, infrastructure, training
5. **Dependency Management**: Version compatibility across modules

#### Guidance

- Use composable patterns when coordination, delegation, or reasoning across tools becomes unavoidable
- Products with clearly separable domains (ERP, CRM, workflow automation) benefit most
- Real-time systems (medical devices, trading) may need monolithic cores for stability

---

### 5. Work Tracking in AI Systems

#### The Context Rot Problem

**Definition:** Performance degradation when LLMs process increasingly long input contexts.

**Research (Chroma, July 2025):**
- 18 models tested including GPT-4.1, Claude 4, Gemini 2.5
- Performance drops 20-50% from 10k to 100k+ tokens in NIAH tasks
- "Lost-in-the-middle" problem: models struggle with buried information
- Low-similarity queries degrade faster

#### Anthropic's Solutions

1. **Compaction**: Summarize conversation, preserve architectural decisions, discard redundant tool outputs
2. **Structured Note-Taking**: Persist notes outside context window, retrieve later for continuity
3. **Multi-Agent Architecture**: Sub-agents with clean contexts return condensed summaries (1,000-2,000 tokens)

**Example:** Claude playing Pokemon maintains tallies across thousands of steps via persistent notes: "for the last 1,234 steps I've been training my Pokemon in Route 1."

#### LangGraph State Persistence

**Checkpointing Approach:**
```python
# State saved at every superstep
graph.compile(checkpointer=PostgresSaver(...))
```

**Key Features:**
- Fault-tolerance: Restart from last successful step
- Partial success preservation: Pending checkpoint writes stored
- Cross-thread state: Store interface for shared user preferences

**Available Checkpointers:**
- `InMemorySaver`: Experimentation
- `SqliteSaver`: Local workflows
- `PostgresSaver`: Production (used by LangSmith)
- `langgraph-checkpoint-aws`: AWS Bedrock + ElastiCache

#### Industry Pattern for Persistent Work Tracking

1. **Session-based state**: Short-term memory for interaction context
2. **Long-term storage**: User preferences, historical data
3. **Checkpoint-based recovery**: Resume workflows after failures
4. **Multi-agent memory sharing**: Conversation ID keyed memory

---

## L2: Architectural Implications (Principal Architect)

### Industry Consensus Patterns

**Pattern 1: Three-Layer Agent Stack**
```
┌─────────────────────────────────────┐
│          Skills Layer               │ <- Procedural Knowledge
├─────────────────────────────────────┤
│          Tools Layer (MCP)          │ <- External Connectivity
├─────────────────────────────────────┤
│          Model Layer (LLM)          │ <- Reasoning Engine
└─────────────────────────────────────┘
```

**Pattern 2: Progressive Context Loading**
- Load metadata always (~100 tokens)
- Load instructions on activation (<5000 tokens)
- Load resources on-demand
- Employ compaction at thresholds

**Pattern 3: Hybrid Orchestration**
- Workflow agents for coordination (Sequential, Parallel, Loop)
- LLM agents for reasoning
- Skills for domain expertise
- Checkpointing for state persistence

### Divergent Approaches and Trade-offs

| Provider | Primary Pattern | Strength | Weakness |
|----------|-----------------|----------|----------|
| **Anthropic** | Skills as procedural memory | Clean file-based interface, portable | Less structured orchestration |
| **Google ADK** | Explicit workflow primitives | Strong orchestration patterns | More complex to adopt |
| **OpenAI** | Tool-centric with handoffs | Flexible, tracing built-in | Less opinionated structure |
| **LangChain** | Composable chains/graphs | Maximum flexibility | Steeper learning curve |

### Recommendations for Jerry Framework Alignment

1. **Adopt SKILL.md Format**
   - Jerry's existing `skills/*/SKILL.md` structure aligns with Anthropic's open standard
   - Validate compliance with https://agentskills.io/specification
   - Consider adding optional fields: `license`, `compatibility`, `metadata`

2. **Implement Progressive Disclosure**
   - Load skill metadata at session start (already done via CLAUDE.md references)
   - Full skill loading only when activated
   - Resources loaded on-demand from `references/` directories

3. **Address Context Rot Explicitly**
   - Jerry's Work Tracker already externalizes state to filesystem
   - Consider adding compaction triggers based on token thresholds
   - Implement structured note-taking pattern for multi-session continuity

4. **Adopt Workflow Patterns from Google ADK**
   - `SequentialAgent` pattern for multi-step workflows
   - `LoopAgent` pattern for quality gates (Generator-Critic)
   - Consider explicit orchestration primitives in AGENTS.md

5. **State Persistence Strategy**
   - Leverage existing filesystem-based persistence
   - Consider checkpoint-style snapshots for workflow recovery
   - Implement cross-session state for user preferences

### Future-Proofing Considerations

1. **MCP Compatibility**
   - As MCP evolves under Linux Foundation governance, ensure Jerry's tool integrations remain compatible
   - Monitor https://modelcontextprotocol.io/specification for updates

2. **Multi-Provider Support**
   - OpenAI Agents SDK is provider-agnostic
   - Jerry should support multiple LLM backends
   - Skills should be model-independent

3. **Observability**
   - OpenAI's built-in tracing is becoming table stakes
   - Consider adding trace/span instrumentation to Jerry's agent orchestration
   - Enable workflow debugging without manual log analysis

4. **Security Model**
   - Composable agents have multiple attack surfaces
   - Each skill should have explicit `allowed-tools` declarations
   - Implement guardrails at input, tool use, and output stages

5. **Context Engineering as Discipline**
   - Treat context as a finite resource with diminishing returns
   - Implement "attention budget" awareness in agent design
   - Build compaction and note-taking into core workflow

---

## References

### Anthropic Agent Skills
- [Agent Skills: Anthropic's Next Bid to Define AI Standards](https://thenewstack.io/agent-skills-anthropics-next-bid-to-define-ai-standards/) - The New Stack
- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) - Anthropic Engineering
- [Agent Skills Open Standard](https://agentskills.io/home) - Official Specification
- [SKILL.md Format Specification](https://deepwiki.com/anthropics/skills/2.2-skill.md-format-specification) - DeepWiki
- [GitHub: anthropics/skills](https://github.com/anthropics/skills) - Official Repository
- [Anthropic makes agent Skills an open standard](https://siliconangle.com/2025/12/18/anthropic-makes-agent-skills-open-standard/) - SiliconANGLE
- [Anthropic launches enterprise Agent Skills](https://venturebeat.com/technology/anthropic-launches-enterprise-agent-skills-and-opens-the-standard) - VentureBeat

### Model Context Protocol (MCP)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25) - Official Spec
- [Donating MCP to Agentic AI Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation) - Anthropic
- [MCP and Agent Skills: Empowering AI Agents](https://bytebridge.medium.com/model-context-protocol-mcp-and-agent-skills-empowering-ai-agents-with-tools-and-expertise-bd4dbe3f2f00) - ByteBridge

### Google ADK
- [Developer's guide to multi-agent patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) - Google Developers Blog
- [Building Collaborative AI with ADK](https://cloud.google.com/blog/topics/developers-practitioners/building-collaborative-ai-a-developers-guide-to-multi-agent-systems-with-adk) - Google Cloud
- [Multi-Agent Systems in ADK](https://google.github.io/adk-docs/agents/multi-agents/) - Official Documentation
- [Architecting efficient context-aware multi-agent framework](https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/) - Google Developers
- [ADK for TypeScript](https://developers.googleblog.com/introducing-agent-development-kit-for-typescript-build-ai-agents-with-the-power-of-a-code-first-approach/) - Google Developers

### OpenAI Agent Patterns
- [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) - OpenAI PDF
- [Building agents](https://developers.openai.com/tracks/building-agents/) - OpenAI Developers
- [OpenAI Cookbook: Agents](https://cookbook.openai.com/topic/agents) - Official Cookbook
- [Model Spec (2025/12/18)](https://model-spec.openai.com/2025-12-18.html) - OpenAI

### Composable vs Monolithic Architecture
- [How Composable Agents Are Rewiring AI Architecture in 2025](https://www.tribe.ai/applied-ai/inside-the-machine-how-composable-agents-are-rewiring-ai-architecture-in-2025) - Tribe AI
- [Composable Software in 2025: Why Modular Architectures Are Winning](https://jetsoftpro.com/blog/composable-software-modular-architecture-2025/) - JetSoft Pro
- [Comparing Top 5 AI Agent Architectures in 2025](https://www.marktechpost.com/2025/11/15/comparing-the-top-5-ai-agent-architectures-in-2025-hierarchical-swarm-meta-learning-modular-evolutionary/) - MarkTechPost
- [Three AI Agent Architectures Have Emerged](https://cobusgreyling.medium.com/three-ai-agent-architectures-have-emerged-b28c2a1dcc9f) - Cobus Greyling

### Context Management and Preservation
- [Context Rot: How Increasing Input Tokens Impacts LLM Performance](https://research.trychroma.com/context-rot) - Chroma Research
- [Context rot: the emerging challenge](https://www.understandingai.org/p/context-rot-the-emerging-challenge) - Understanding AI
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - Anthropic Engineering
- [Cutting Through the Noise: Smarter Context Management](https://blog.jetbrains.com/research/2025/12/efficient-context-management/) - JetBrains Research

### State Persistence
- [LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) - LangChain Docs
- [Mastering LangGraph State Management in 2025](https://sparkco.ai/blog/mastering-langgraph-state-management-in-2025) - SparkCo
- [Mastering LangGraph Checkpointing: Best Practices for 2025](https://sparkco.ai/blog/mastering-langgraph-checkpointing-best-practices-for-2025) - SparkCo
- [Building LangGraph: Designing an Agent Runtime from first principles](https://blog.langchain.com/building-langgraph/) - LangChain Blog

### Agentic AI Trends
- [Agentic LLMs in 2025](https://datasciencedojo.com/blog/agentic-llm-in-2025/) - Data Science Dojo
- [LLM Agents Explained: Complete Guide in 2025](https://www.getdynamiq.ai/post/llm-agents-explained-complete-guide-in-2025) - Dynamiq
- [Top Agentic AI Tools in 2025](https://www.lasso.security/blog/agentic-ai-tools) - Lasso Security
- [20 Agentic AI Workflow Patterns That Work in 2025](https://skywork.ai/blog/agentic-ai-examples-workflow-patterns-2025/) - Skywork AI

---

## Appendix: Jerry Framework Alignment Checklist

| Standard | Jerry Status | Recommendation |
|----------|--------------|----------------|
| SKILL.md format | Partial | Validate frontmatter compliance |
| Progressive disclosure | Implemented | Document pattern formally |
| MCP compatibility | Not assessed | Audit tool interfaces |
| Workflow orchestration | Implicit | Consider ADK-style primitives |
| State persistence | File-based | Add checkpoint mechanism |
| Context compaction | Not implemented | Add threshold-based triggers |
| Tracing/observability | Not implemented | Consider instrumentation |
| Multi-agent nesting | P-003 enforced | Compliant |

---

*Document generated by ps-researcher agent. All sources verified as of 2026-01-11.*
