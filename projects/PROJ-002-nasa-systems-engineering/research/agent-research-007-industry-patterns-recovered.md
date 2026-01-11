# Industry Multi-Agent Patterns Research (Recovered)

> **Source:** WI-SAO-019 Research Agent (a92cbe3)
> **Date:** 2026-01-10
> **Status:** Recovered from ephemeral task output
> **Framework:** 5W1H + Industry Survey

---

## Executive Summary

This document captures industry best practices for multi-agent AI systems (2024-2025), covering orchestration patterns, state management, error handling, and file structure conventions across major frameworks.

---

## 1. Framework Survey

### 1.1 LangGraph (LangChain)

**Architecture:** Graph-based stateful framework

**Orchestration Patterns:**
1. **Scatter-Gather** - Tasks distributed to multiple agents, results consolidated
2. **Pipeline Parallelism** - Different agents handle sequential stages concurrently
3. **Sequential Processing** - Tasks completed one after another
4. **Hierarchical Teams** - Subagents are LangGraph objects themselves

**State Management:**
- Each agent is a node in the graph
- Control flow managed by edges
- Agents communicate by adding to the graph's state
- Built-in statefulness with time-travel debugging

**Key Features:**
- Human-in-the-loop interrupts
- Robust fault tolerance
- Explicit state machines and error handling

**Source:** [LangGraph Multi-Agent Orchestration](https://latenode.com/blog/ai-frameworks-technical-infrastructure/langgraph-multi-agent-orchestration/)

### 1.2 CrewAI

**Architecture:** Dual approach - Crews (autonomous) + Flows (event-driven)

**Orchestration Patterns:**
1. **Coordinator-Worker** - Central coordinator receives tasks, delegates to specialists
2. **Hierarchical** - Clear reporting structure, like human organizations
3. **Sequential/Parallel Execution** - Map-reduce pattern

**Best Practices:**
- Task design is critical for successful execution
- Specialization leads to better outcomes
- Guardrails prevent loops, hallucinations, cost overruns

**Production Considerations:**
- Default process is synchronous and in-memory
- Long tasks need async with external state store (Redis, SQL)
- Integration with LangSmith for observability

**Source:** [CrewAI Orchestration Guide](https://docs.crewai.com/en/guides/agents/crafting-effective-agents)

### 1.3 Microsoft AutoGen

**Architecture:** Actor model for multi-agent orchestration (v0.4)

**Conversation Patterns:**
1. **Two-Agent Chat** - Simplest form, two agents exchange messages
2. **Sequential Chat** - Chained via carryover mechanism
3. **Group Chat** - 3+ agents, managed by GroupChatManager
4. **Nested Chat** - Complex workflows encapsulated in single agent

**Key Features:**
- Dynamic vs static conversations
- Layered architecture (Core → AgentChat)
- AG2 evolution with open governance

**Source:** [AutoGen Conversation Patterns](https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/)

### 1.4 OpenAI Agents SDK

**Core Primitives:**
1. **Agents** - LLMs with instructions and tools
2. **Handoffs** - Task delegation between agents
3. **Guardrails** - Input/output validation
4. **Sessions** - Automatic conversation history

**Design Philosophy:**
- "Few enough primitives to make it quick to learn"
- Works out of the box, customizable when needed
- Built-in tracing for visualization and debugging

**Source:** [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)

### 1.5 Anthropic Claude Agent SDK

**Core Pattern:** Feedback loop architecture
```
gather context → take action → verify work → repeat
```

**Subagent Orchestration:**
- Parallelization AND context management
- Isolated context windows per subagent
- Return only relevant information to orchestrator

**State Management:**
- File system organization as context engineering
- Agentic search via bash commands (grep, tail)
- Automatic context compaction near limits

**Verification Strategies:**
1. Rule-based validation
2. Visual inspection (screenshots)
3. LLM judging (secondary models)

**Source:** [Building Agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)

---

## 2. Common Orchestration Patterns

### 2.1 Pattern Taxonomy

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| **Sequential** | Linear pipeline, clear dependencies | Multistage processes |
| **Concurrent** | Parallel independent analysis | Time-sensitive, diverse perspectives |
| **Handoff** | Dynamic delegation based on assessment | Unknown optimal agent upfront |
| **Group Chat** | Managed conversation, multiple agents | Collaborative decision-making |
| **Magentic** | Manager refines plan with specialists | Open-ended complex problems |

**Source:** [Azure AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)

### 2.2 Anthropic's Workflow Patterns

1. **Prompt Chaining** - Sequential steps, each processing prior outputs
2. **Routing** - Classify inputs, direct to specialized handlers
3. **Parallelization** - Sectioning (independent) or Voting (multiple attempts)
4. **Orchestrator-Workers** - Central LLM dynamically breaks down tasks
5. **Evaluator-Optimizer** - Generate + evaluate in loops

**Key Insight:**
> "Workflows suit well-defined tasks requiring predictability. Agents excel when flexibility and model-driven decision-making are needed at scale."

**Source:** [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)

---

## 3. State Management Patterns

### 3.1 Context Transfer

**Carryover Mechanism (AutoGen):**
- Brings summary of previous chat to next chat context
- Configurable summary methods: `last_msg`, `reflection_with_llm`, custom

**Task Ledger (Azure Magentic):**
- Documents evolving plan with goals, subgoals, task status
- Dynamic refinement as context evolves
- Provides audit trail for post-execution review

**File System State (Claude):**
- Folder organization reflects workflow needs
- Agents search through folders autonomously
- Structure enables agentic search

### 3.2 Handoff Best Practices

> "Reliability lives and dies in the handoffs. Most 'agent failures' are actually orchestration and context-transfer issues."

**Key Recommendations:**
- Make handoffs explicit, structured, and versioned
- Use schemas and validators, not free-form prose
- Avoid infinite handoff loops
- Watch for handoff drift and stale plans

**Source:** [Best Practices for Multi-Agent Orchestration](https://skywork.ai/blog/ai-agent-orchestration-best-practices-handoffs/)

---

## 4. Error Handling Patterns

### 4.1 Fault Tolerance Mechanisms

1. **Redundancy** - Multiple agent instances in parallel
2. **Automated Recovery** - Intelligent retry with exponential backoff
3. **Self-Healing** - Automatic restart/replace failed instances
4. **Circuit Breakers** - Prevent cascading failures

### 4.2 Retry Logic Best Practices (2025)

- **Exponential backoff with jitter** - Prevents thundering herd
- **Explicit failure classification** - Transient vs permanent errors
- **Timeout and retry mechanisms** - Graceful degradation

### 4.3 Verification Strategies

| Strategy | Use Case |
|----------|----------|
| Rule-based | Explicit requirements, clear feedback |
| Visual inspection | Tasks with visual components |
| LLM judging | Fuzzy criteria (tone, appropriateness) |

**Source:** [Error Recovery in AI Agent Development](https://www.gocodeo.com/post/error-recovery-and-fallback-strategies-in-ai-agent-development)

---

## 5. File Structure Conventions

### 5.1 Agents.md Standard

Emerging industry standard (20,000+ GitHub projects):
```
project/
├── AGENTS.md           # Instructions for AI agents
├── .junie/guidelines.md  # JetBrains Junie
├── .aiassistant/rules/   # JetBrains AI Assistant
└── .github/copilot-instructions.md  # GitHub Copilot
```

**Purpose:** "A README for machines" - project-specific instructions for AI coding agents.

**Source:** [Agents.md Specification](https://ai.plainenglish.io/agents-md-a-comprehensive-guide-to-agentic-ai-collaboration-571df0e78ccc)

### 5.2 Claude Skills Structure

```
skill-name/
├── SKILL.md           # Core prompt + frontmatter
├── scripts/           # Executable Python/Bash
├── references/        # Documentation for context
└── assets/            # Templates and binary files
```

**Source:** [Claude Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)

---

## 6. Agent Discovery & Registration

### 6.1 Agent Mesh Architecture

- Agents register capabilities, SLA requirements, compliance constraints
- Mesh automatically routes to optimal agents based on real-time metrics
- Support for dynamic discovery via Consul, Eureka, Kubernetes

### 6.2 Google A2A Protocol

- Agent-to-Agent protocol backed by 50+ partners
- Standardized peer-to-peer framework
- HTTP and JSON-RPC based
- Agent Cards for discovery

**Source:** [Agent Discovery and Naming](https://www.solo.io/blog/agent-discovery-naming-and-resolution---the-missing-pieces-to-a2a)

---

## 7. Key Takeaways for Jerry Framework

### 7.1 Alignment with Industry Patterns

| Jerry Pattern | Industry Equivalent |
|---------------|---------------------|
| P-003 (No recursive nesting) | Hierarchical limit (Azure recommends ≤3 agents) |
| Filesystem state | Claude Agent SDK pattern |
| ORCHESTRATION.yaml | Task Ledger (Azure Magentic) |
| Skill activation keywords | Agent discovery/routing |

### 7.2 Recommendations

1. **State Management:** Continue using filesystem; add structured handoff schemas
2. **Error Handling:** Implement circuit breaker pattern for agent failures
3. **Observability:** Add tracing for agent orchestration
4. **Discovery:** Consider formalizing agent capability registration

---

## Citations

1. [LangGraph Multi-Agent Orchestration](https://latenode.com/blog/ai-frameworks-technical-infrastructure/langgraph-multi-agent-orchestration/)
2. [CrewAI Documentation](https://docs.crewai.com/)
3. [AutoGen Conversation Patterns](https://microsoft.github.io/autogen/0.2/docs/tutorial/conversation-patterns/)
4. [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
5. [Building Agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
6. [Azure AI Agent Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
7. [Building Effective Agents (Anthropic)](https://www.anthropic.com/research/building-effective-agents)
8. [Claude Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
9. [Best Practices for Multi-Agent Orchestration](https://skywork.ai/blog/ai-agent-orchestration-best-practices-handoffs/)
10. [Error Recovery in AI Agent Development](https://www.gocodeo.com/post/error-recovery-and-fallback-strategies-in-ai-agent-development)
11. [Agents.md Specification](https://ai.plainenglish.io/agents-md-a-comprehensive-guide-to-agentic-ai-collaboration-571df0e78ccc)
12. [Agent Discovery (Solo.io)](https://www.solo.io/blog/agent-discovery-naming-and-resolution---the-missing-pieces-to-a2a)

---

*Recovered: 2026-01-10 | Original task: a92cbe3*
