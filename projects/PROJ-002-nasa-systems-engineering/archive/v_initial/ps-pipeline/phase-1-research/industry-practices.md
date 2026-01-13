# ps-r-003: Industry Best Practices Research

**Document ID:** ps-r-003
**Date:** 2026-01-09
**Author:** ps-researcher (Claude Opus 4.5)
**Project:** PROJ-002-nasa-systems-engineering
**Phase:** 1 - Research (ps-* Pipeline)
**Status:** Complete

---

## L0: Executive Summary

The Jerry Framework's orchestration patterns are **well-aligned** with Anthropic's official Claude Code best practices but **diverge significantly** from the broader industry landscape dominated by LangGraph, CrewAI, and Google ADK. Our single-level nesting constraint (P-003) is more restrictive than industry standards but aligns with Anthropic's recommendation for subagent architectures. **Critical gaps** include: lack of graph-based state management, no checkpointing/time-travel debugging, missing parallel execution primitives, and absence of formal guardrails/validation hooks. The prompting strategies are strong but would benefit from adopting the WRITE/SELECT/COMPRESS/ISOLATE taxonomy from context engineering literature.

---

## L1: Technical Analysis

### 1. Anthropic/Claude Code Alignment

#### What We're Doing Right

| Jerry Practice | Anthropic Best Practice | Alignment |
|----------------|-------------------------|-----------|
| Single-level nesting (P-003) | "Give each subagent one job, orchestrator coordinates" | **Strong** |
| File-based state persistence (P-002) | "Structured note-taking (NOTES.md, TODO lists) outside context" | **Strong** |
| CLAUDE.md configuration | "Place at repo root, keep concise and human-readable" | **Strong** |
| Agent personas with role/goal/backstory | "Expert prompting with specific domain knowledge" | **Strong** |
| L0/L1/L2 output levels | Progressive disclosure for token efficiency | **Strong** |
| Upstream artifact references | "Just-in-time context loading" with file paths | **Moderate** |
| Session validation (FIX-NEG-008) | "Session mismatch handling with safe defaults" | **Novel** |

**Source:** [Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk), [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

#### What We Could Improve

| Gap | Anthropic Recommendation | Current Jerry State |
|-----|-------------------------|---------------------|
| **Initializer Agent Pattern** | "Specialized prompt for first run to set up environment" | Not implemented |
| **claude-progress.txt** | "Running log for agents to understand state across context windows" | Partially via WORKTRACKER.md |
| **Context Awareness** | "Claude 4.5 can track remaining token budget" | Not leveraged |
| **Compaction Strategy** | "Preserve architectural decisions, discard redundant tool outputs" | Implicit, not documented |
| **Hybrid Context Loading** | "Some data upfront, further exploration at discretion" | Sequential only |
| **Testing Subagents** | "Have one Claude write tests, another write code" | Not formalized |

**Source:** [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

#### Skills System Comparison

Jerry's Skills (`skills/problem-solving/`, `skills/nasa-se/`) align with Anthropic's Agent Skills concept:

| Anthropic Skills Feature | Jerry Implementation |
|--------------------------|---------------------|
| SKILL.md structured metadata | **Present** - YAML frontmatter in SKILL.md |
| Step-by-step instructions | **Present** - Agent prompts |
| Tool access permissions | **Present** - Tool lists in agent specs |
| Trigger conditions | **Present** - Keyword matching |
| Slash command integration | **Partial** - Via orchestrator, not native |

**Source:** [Agent Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)

---

### 2. CrewAI Comparison

#### Framework Overview

CrewAI is a "lean, lightning-fast Python framework" for role-based multi-agent teams with two approaches:
- **Crews**: Autonomous collaborative intelligence
- **Flows**: Production-ready, event-driven workflows with precise control

**Source:** [CrewAI GitHub](https://github.com/crewAIInc/crewAI)

#### Pattern Comparison

| Pattern | CrewAI | Jerry |
|---------|--------|-------|
| Sequential Pipeline | `Process.sequential` | **Supported** - via chaining |
| Hierarchical/Supervisor | `Process.hierarchical` + `manager_llm` | **Partial** - orchestrator only |
| Parallel Execution | Parallel tasks in Flow | **Not Supported** |
| Peer Delegation | `allow_delegation=True` | **Prohibited** (P-003) |
| Router/Conditional | `@router` decorator | **Not Supported** |
| State Management | Pydantic `BaseModel` + ChromaDB | JSON state files |

#### What CrewAI Has That We Don't

1. **Memory Layers**: Short-term (ChromaDB), long-term (SQLite), entity memory (vectors)
2. **Async/Parallel Execution**: True concurrent agent execution
3. **Dynamic Routing**: `@router` decorator for conditional branching
4. **Built-in Cost Monitoring**: Token usage tracking per agent/task
5. **Manager LLM**: Dedicated orchestration model for hierarchical crews

**Source:** [CrewAI Framework Review](https://latenode.com/blog/ai-frameworks-technical-infrastructure/crewai-framework/crewai-framework-2025-complete-review-of-the-open-source-multi-agent-ai-platform)

#### What Jerry Has That CrewAI Lacks

1. **Constitutional Principles**: P-003, P-020, P-022 hard constraints
2. **NASA SE Domain Specialization**: 8 agents mapped to NPR 7123.1D
3. **Session Validation**: FIX-NEG-008 cross-session safety
4. **Explicit Provenance**: Source citation requirements (P-004)
5. **Progressive Disclosure**: L0/L1/L2 output levels

---

### 3. LangGraph Comparison

#### Framework Overview

LangGraph treats workflows as **stateful graphs** with explicit node-based control flow. It's the recommended framework for all new LangChain agent implementations (as of 2025).

**Source:** [LangGraph Multi-Agent Orchestration Guide](https://latenode.com/blog/ai-frameworks-technical-infrastructure/langgraph-multi-agent-orchestration/langgraph-multi-agent-orchestration-complete-framework-guide-architecture-analysis-2025)

#### Pattern Comparison

| Capability | LangGraph | Jerry |
|------------|-----------|-------|
| State Schema | TypedDict + Annotated types + reducers | JSON files |
| Checkpointing | Built-in (memory, SQLite, Postgres) | None |
| Time-Travel Debugging | `get_state_history()` | None |
| Human-in-the-Loop | `interrupt_before`/`interrupt_after` | User approval prompts |
| Conditional Edges | Native graph edges | Keyword matching only |
| Parallel Execution | `Send` API for map-reduce | Not supported |
| Fault Tolerance | Automated retries, per-node timeouts | Basic retry policy |

#### Critical Gaps vs LangGraph

1. **No Graph-Based Orchestration**: Jerry uses linear keyword matching; LangGraph uses explicit graph edges
2. **No Checkpointing**: State history not preserved for replay/debugging
3. **No Time-Travel**: Cannot inspect or rollback to prior states
4. **Limited Conditional Logic**: No programmatic branching based on state
5. **No Native Parallelism**: Cannot fan-out to multiple agents simultaneously

**Source:** [Mastering LangGraph State Management](https://sparkco.ai/blog/mastering-langgraph-state-management-in-2025)

#### LangGraph Insight Worth Adopting

> "Agents make dynamic decisions and are non-deterministic between runs, even with identical prompts. This makes debugging harder. Adding full production tracing lets you diagnose why agents failed and fix issues systematically."

---

### 4. Google ADK Comparison

#### Framework Overview

Google ADK treats agents like **software components** with distinct categories:
- **LlmAgent**: LLM-powered reasoning agents
- **SequentialAgent/ParallelAgent/LoopAgent**: Deterministic workflow agents
- **Custom Agents**: Extend `BaseAgent` for unique logic

**Source:** [Developer's Guide to Multi-Agent Patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)

#### Pattern Comparison

| Pattern | Google ADK | Jerry |
|---------|------------|-------|
| Sequential Pipeline | `SequentialAgent` | Supported |
| Coordinator/Hub-Spoke | LlmAgent + sub_agents + AutoFlow | Partial (orchestrator) |
| Parallel Fan-Out | `ParallelAgent` | **Not Supported** |
| Generator-Critic Loop | `LoopAgent` | **Not Supported** |
| Agent-as-Tool | `AgentTool` wrapper | **Not Supported** |

#### Google ADK Philosophy Worth Adopting

> "The world of software development has already learned this lesson: monolithic applications don't scale... A single agent tasked with too many responsibilities becomes a 'Jack of all trades, master of none.' As the complexity of instructions increases, adherence to specific rules degrades."

**This validates our specialized agent approach** (ps-researcher, ps-analyst, nse-requirements, etc.)

---

### 5. OpenAI Agents SDK Comparison

#### Framework Overview

OpenAI's SDK emphasizes **minimal abstractions** with four core primitives:
- **Agents**: LLMs with instructions and tools
- **Handoffs**: Agent-to-agent delegation
- **Guardrails**: Input/output validation
- **Sessions**: Automatic conversation history

**Source:** [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)

#### Pattern Comparison

| Feature | OpenAI SDK | Jerry |
|---------|------------|-------|
| Handoff Mechanism | First-class `handoff()` primitive | File-based artifact passing |
| Guardrails | Built-in validation hooks | Constitutional principles (soft) |
| Session Memory | Automatic persistence | Manual via WORKTRACKER |
| Agent-as-Tool | Native support | **Not Supported** |
| Python-First | Built-in language orchestration | Prompt-based orchestration |

#### OpenAI Pattern Worth Considering

> "Agent as a Tool: One agent (often a central planner or manager) calls other agents as if they were tools. Sub-agents don't take over the conversation; instead, the main agent invokes them for specific subtasks and incorporates their results."

This differs from our handoff model and may offer more control.

**Source:** [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)

---

### 6. Prompting Strategy Assessment

#### Context Engineering Taxonomy

The industry has moved from "prompt engineering" to **"context engineering"**. Anthropic defines four strategic categories:

| Strategy | Definition | Jerry Implementation |
|----------|------------|---------------------|
| **WRITE** | Persist information for later use | WORKTRACKER.md, artifact files |
| **SELECT** | Filter to most relevant information | Upstream artifact references |
| **COMPRESS** | Reduce tokens while preserving meaning | **Not Explicit** |
| **ISOLATE** | Separate concerns between agents | Agent-specific context windows |

**Source:** [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

#### Prompting Patterns Assessment

| Pattern | Industry Best Practice | Jerry Status |
|---------|----------------------|--------------|
| XML/Markdown Structure | Use for clear section separation | **Implemented** |
| Role-Goal-Backstory | CrewAI's effective persona pattern | **Implemented** |
| Chain-of-Thought | "Let's think step by step" for complex reasoning | **Implicit only** |
| Expert Prompting | Specific domain expertise > generic persona | **Strong** |
| Few-Shot Examples | 2-5 examples for format guidance | **Minimal** |
| Guardrails Section | Dedicated non-negotiable rules | **Partial** (constraints in prompts) |

#### What's Missing

1. **Explicit CoT Triggers**: Should add "Let's think step by step" for analytical agents
2. **Few-Shot Examples**: Agent specs lack concrete input/output examples
3. **Output Verification**: No generator-critic pattern for quality assurance
4. **Temperature/Parameter Guidance**: No model parameter recommendations
5. **Error Recovery Prompting**: Limited guidance on handling failures

---

## L2: Strategic Implications

### Patterns to Adopt (Priority Order)

| Priority | Pattern | Source | Rationale |
|----------|---------|--------|-----------|
| **P1** | Checkpointing/State History | LangGraph | Enables debugging, replay, time-travel |
| **P1** | Parallel Execution Primitive | ADK/CrewAI | Sequential-only is a bottleneck |
| **P1** | Guardrails/Validation Hooks | OpenAI SDK | Constitutional principles need runtime enforcement |
| **P2** | Initializer Agent Pattern | Anthropic | Better cross-session continuity |
| **P2** | Context Compaction Strategy | Anthropic | Explicit guidance for token management |
| **P2** | Generator-Critic Loop | ADK | Quality assurance before output |
| **P3** | Agent-as-Tool Pattern | OpenAI/ADK | More flexible than handoffs |
| **P3** | Memory Layers | CrewAI | Short-term + long-term + entity memory |
| **P3** | Cost/Token Monitoring | CrewAI | Production visibility |

### Gaps vs Industry

| Gap | Impact | Industry Solution | Jerry Remediation |
|-----|--------|-------------------|-------------------|
| No parallel execution | Slow multi-domain workflows | `ParallelAgent`, `Send` API | Add fan-out pattern |
| No checkpointing | Cannot debug failed runs | LangGraph checkpointers | Implement state snapshots |
| No time-travel | Cannot inspect past states | `get_state_history()` | Add checkpoint browsing |
| No guardrail hooks | Constitutional principles not enforced at runtime | OpenAI guardrails | Add validation middleware |
| No graph-based routing | Limited to keyword matching | LangGraph conditional edges | Consider graph model |
| No generator-critic | No automatic quality loop | ADK `LoopAgent` | Add review step |

### Priority Improvements

#### Immediate (This Phase)

1. **Document Context Engineering Strategy**
   - Formalize WRITE/SELECT/COMPRESS/ISOLATE for Jerry agents
   - Add explicit compaction guidance to agent specs

2. **Add Few-Shot Examples to Agent Specs**
   - Each agent should have 2-3 example input/output pairs
   - Reduces ambiguity in output formats

3. **Formalize Testing Subagent Pattern**
   - Per Anthropic: "Have one Claude write tests, another write code"
   - Add `ps-tester` or similar agent

#### Near-Term (Next Phase)

4. **Implement Checkpointing**
   - State snapshots after each agent completes
   - Enable replay from any checkpoint

5. **Add Parallel Execution**
   - Fan-out pattern for independent tasks
   - Aggregation pattern for synthesis

6. **Add Guardrail Hooks**
   - Pre-execution validation
   - Post-execution verification
   - Constitutional principle enforcement

#### Long-Term (Future Phases)

7. **Consider Graph-Based Orchestration**
   - Evaluate if keyword matching scales
   - LangGraph-style explicit edges may be clearer

8. **Memory Layer Architecture**
   - Short-term (current session)
   - Long-term (cross-session knowledge)
   - Entity memory (domain-specific embeddings)

---

## Cross-Pollination Metadata

### Source Agent
- **Agent ID:** ps-r-003
- **Agent Type:** ps-researcher
- **Skill:** problem-solving
- **Session:** Phase 1 Research

### Target Audience
- **nse-requirements** - For formalizing industry patterns as requirements
- **nse-architecture** - For designing checkpointing and parallel execution
- **ps-architect** - For ADR creation on framework improvements

### Key Handoff Items

1. **For nse-requirements:**
   - REQ: Implement checkpointing mechanism for agent state
   - REQ: Support parallel agent execution (fan-out pattern)
   - REQ: Add guardrail validation hooks (pre/post execution)
   - REQ: Formalize context compaction strategy
   - REQ: Support generator-critic quality loops

2. **For nse-architecture:**
   - ARCH: Design state persistence layer (beyond JSON files)
   - ARCH: Design parallel execution runtime
   - ARCH: Design checkpoint storage and retrieval
   - ARCH: Evaluate graph-based vs keyword-based routing

3. **For ps-architect (ADRs):**
   - ADR: Adopt checkpointing pattern from LangGraph
   - ADR: Add ParallelAgent capability inspired by ADK
   - ADR: Implement guardrails middleware
   - ADR: Context engineering strategy documentation

### Gaps for nse-* to Address

| Gap ID | Description | Industry Reference | Formalization Target |
|--------|-------------|-------------------|---------------------|
| GAP-001 | No checkpointing | LangGraph | REQ + ARCH |
| GAP-002 | No parallel execution | ADK ParallelAgent | REQ + ARCH |
| GAP-003 | No guardrail hooks | OpenAI SDK | REQ |
| GAP-004 | No generator-critic | ADK LoopAgent | REQ |
| GAP-005 | No context compaction strategy | Anthropic | DOC |
| GAP-006 | No initializer agent | Anthropic | REQ |
| GAP-007 | No few-shot examples | Industry standard | DOC |
| GAP-008 | No cost/token monitoring | CrewAI | REQ |
| GAP-009 | Limited conditional routing | LangGraph | ARCH |
| GAP-010 | No memory layers | CrewAI | ARCH |

### Validation Criteria

For nse-* to consider gaps addressed:
- [ ] REQ has clear acceptance criteria
- [ ] ARCH has implementation design
- [ ] ADR has rationale and alternatives
- [ ] Test cases defined for verification

---

## Research Sources

### Primary Sources (Anthropic)
- [Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Claude Agent Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)

### Framework Documentation
- [CrewAI GitHub](https://github.com/crewAIInc/crewAI)
- [LangGraph Documentation](https://www.langchain.com/langgraph)
- [Google ADK Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)

### Industry Analysis
- [Agent Orchestration 2026: LangGraph, CrewAI & AutoGen Guide](https://iterathon.tech/blog/ai-agent-orchestration-frameworks-2026)
- [Top 10+ Agentic Orchestration Frameworks & Tools in 2026](https://research.aimultiple.com/agentic-orchestration/)
- [8 Best Multi-Agent AI Frameworks for 2026](https://www.multimodal.dev/post/best-multi-agent-ai-frameworks)
- [AI Agent Orchestration Frameworks Comparison](https://blog.n8n.io/ai-agent-orchestration-frameworks/)

### Context Engineering
- [Context Engineering for Claude Code](https://clune.org/posts/anthropic-context-engineering/)
- [Claude's Context Engineering Playbook](https://01.me/en/2025/12/context-engineering-from-claude/)
- [Mastering LangGraph State Management](https://sparkco.ai/blog/mastering-langgraph-state-management-in-2025)

---

## Appendix A: Framework Comparison Matrix

| Dimension | Jerry | Anthropic/Claude | CrewAI | LangGraph | Google ADK | OpenAI SDK |
|-----------|-------|------------------|--------|-----------|------------|------------|
| **Design Philosophy** | Constitutional | Subagent delegation | Role-based teams | Graph-based | Code-first | Minimal abstractions |
| **Primary Pattern** | Orchestrator-Worker | Orchestrator-Worker | Hierarchical | Any (graph) | Workflow agents | Handoff-based |
| **State Management** | JSON files | claude-progress.txt | ChromaDB + SQLite | Checkpointing | Shared state | Session-based |
| **Parallel Execution** | No | Subagent parallelism | Via Flows | Native (Send) | ParallelAgent | Limited |
| **Human-in-the-Loop** | User prompts | Interrupt nodes | Task-level | interrupt_before | Built-in | Guardrails |
| **Memory Persistence** | WORKTRACKER.md | Artifact files | Built-in layers | Configurable | Shared state | Session storage |
| **Learning Curve** | Medium | Low-Medium | Low | Medium-High | Medium | Low |
| **Production Ready** | In development | Yes | Yes | Yes (v1.0) | Yes | Yes |

---

## Appendix B: Recommendation Summary

### Must Have (P1)
1. Checkpointing mechanism
2. Parallel execution primitive
3. Guardrail validation hooks

### Should Have (P2)
1. Initializer agent pattern
2. Context compaction strategy
3. Generator-critic loops

### Nice to Have (P3)
1. Agent-as-tool pattern
2. Memory layers
3. Cost/token monitoring
4. Graph-based routing

---

*Document generated by ps-r-003 agent*
*Research completed: 2026-01-09*
*Jerry Framework Constitutional Compliance: P-001 (Truth), P-002 (Persistence), P-004 (Provenance)*
