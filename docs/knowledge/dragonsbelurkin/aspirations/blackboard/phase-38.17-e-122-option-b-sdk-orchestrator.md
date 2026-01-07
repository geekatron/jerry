# Research: Option B - SDK-Based Python Orchestrator for Agent Chaining

> **PS:** phase-38.17
> **Exploration:** e-122
> **Created:** 2026-01-04
> **Status:** COMPLETE
> **Agent:** ps-researcher
> **Session:** cc/phase-38.16

---

## Executive Summary

This research investigates implementing an SDK-Based Python Orchestrator that chains agent invocations (research -> review -> synthesis) using Anthropic's Claude Agent SDK. The analysis reveals that the Claude Agent SDK provides native support for multi-agent orchestration through subagents with the Task tool, session management with context passing, and robust error handling. This approach offers significant advantages over subprocess-based alternatives: the SDK bundles the CLI automatically, handles JSON streaming and message parsing internally, and provides native Python async patterns for agent chaining.

The research also examines prior art from LangGraph, CrewAI, AutoGen, and Microsoft Semantic Kernel, extracting key patterns including supervisor-agent architectures, state-based graph orchestration, and context isolation strategies. Token optimization through sub-agent architectures shows 67% reduction in token usage, with Anthropic's own research demonstrating 90.2% performance improvement using Opus 4 lead agents coordinating Sonnet 4 subagents.

**Key Recommendation:** Implement the orchestrator using Claude Agent SDK's native subagent architecture with AgentDefinition, leveraging the Task tool for delegation. This provides built-in context isolation, error handling, and session management without requiring custom subprocess orchestration.

---

## Research Questions

1. How can the Claude Agent SDK be used to chain multiple agent calls with context passing for multi-agent orchestration?
2. What prior art exists in multi-agent orchestration (LangGraph, CrewAI, AutoGen, Semantic Kernel) and what patterns can be adopted?
3. What technical architecture should be used for an external Python orchestrator, including state management, error handling, and retry patterns?
4. How can token usage be optimized across multi-agent chains while maintaining context fidelity?

---

## Methodology

### Web Research
- **Keywords:** Claude Agent SDK multi-agent, LangGraph orchestration patterns, CrewAI multi-agent, AutoGen conversation patterns, Semantic Kernel agent orchestration, token optimization multi-agent, context window management
- **Sources Consulted:** 25+
- **Date Range:** 2025-2026 (focus on latest patterns)

### Documentation Review
- **Official Docs:** Claude Agent SDK (Python), LangGraph, CrewAI, AutoGen 0.4, Microsoft Agent Framework
- **Community Resources:** GitHub repositories, technical blogs, Anthropic engineering blog

### Context7 MCP Queries
- Claude Agent SDK Python: session management, subagents, error handling
- LangGraph: multi-agent orchestration, supervisor patterns, state management

---

## Findings

### Finding 1: Claude Agent SDK Native Subagent Architecture

**Source:** [Claude Agent SDK Documentation](https://github.com/context7/platform_claude_en_agent-sdk/blob/main/subagents.md)
**Confidence:** HIGH
**Relevance:** Direct solution for agent chaining requirement

The Claude Agent SDK provides native support for multi-agent orchestration through `AgentDefinition` and the `Task` tool. This eliminates the need for custom subprocess management.

**Key Features:**
- **Subagent Definition:** Define specialized agents with custom prompts, tools, and model overrides
- **Task Tool:** Delegates work to subagents with description, prompt, and subagent type
- **Context Isolation:** Each subagent operates with its own context window
- **Model Flexibility:** Override models per subagent (e.g., Opus for lead, Sonnet for workers)

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async def research_review_synthesis_pipeline():
    async for message in query(
        prompt="Research, review, and synthesize findings on topic X",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Task", "WebSearch"],
            agents={
                "ps-researcher": AgentDefinition(
                    description="Research specialist for deep exploration",
                    prompt="You are a research agent. Explore topics thoroughly.",
                    tools=["Read", "Glob", "Grep", "WebSearch"],
                    model="sonnet"
                ),
                "ps-reviewer": AgentDefinition(
                    description="Quality reviewer for research validation",
                    prompt="You are a review agent. Validate research quality.",
                    tools=["Read", "Glob", "Grep"],
                    model="sonnet"
                ),
                "ps-synthesizer": AgentDefinition(
                    description="Synthesis agent for consolidating findings",
                    prompt="You are a synthesis agent. Consolidate research.",
                    tools=["Read", "Write"],
                    model="opus"
                )
            }
        )
    ):
        if hasattr(message, "result"):
            print(message.result)
```

**Task Tool Output:**
```json
{
    "result": "string",           // Final result from subagent
    "usage": {"input_tokens": N, "output_tokens": M},
    "total_cost_usd": 0.001,
    "duration_ms": 500
}
```

### Finding 2: Session Management and Context Passing

**Source:** [Claude Agent SDK Sessions](https://github.com/context7/platform_claude_en_agent-sdk/blob/main/sessions.md)
**Confidence:** HIGH
**Relevance:** Critical for maintaining state across agent chain

The SDK provides robust session management for multi-turn conversations and context passing:

**Session Capture:**
```python
from claude_agent_sdk import query, ClaudeAgentOptions

session_id = None

async for message in query(
    prompt="Research phase: Analyze the codebase",
    options=ClaudeAgentOptions(allowed_tools=["Read", "Glob"])
):
    if hasattr(message, 'subtype') and message.subtype == 'init':
        session_id = message.session_id
        print(f"Session started: {session_id}")
```

**Session Resume:**
```python
# Resume with full context from previous phase
async for message in query(
    prompt="Review phase: Validate the research findings",
    options=ClaudeAgentOptions(resume=session_id)
):
    if hasattr(message, "result"):
        print(message.result)
```

**Session Forking:**
```python
# Fork session to explore alternative approaches
async for message in query(
    prompt="Try alternative synthesis approach",
    options=ClaudeAgentOptions(
        resume=session_id,
        fork_session=True  # Creates new session ID
    )
):
    pass
```

### Finding 3: LangGraph Multi-Agent Orchestration Patterns

**Source:** [LangGraph Multi-Agent Concepts](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/concepts/multi_agent.md)
**Confidence:** HIGH
**Relevance:** Industry-standard patterns applicable to our orchestrator

LangGraph provides several orchestration patterns that can inform our design:

**Supervisor Pattern:**
```python
from langgraph.types import Command
from langgraph.graph import StateGraph, MessagesState, START, END

def supervisor(state: MessagesState) -> Command[Literal["researcher", "reviewer", END]]:
    response = model.invoke(state["messages"])
    return Command(goto=response["next_agent"])

def researcher(state: MessagesState) -> Command[Literal["supervisor"]]:
    response = model.invoke(state["messages"])
    return Command(
        goto="supervisor",
        update={"messages": [response]}
    )

builder = StateGraph(MessagesState)
builder.add_node(supervisor)
builder.add_node(researcher)
builder.add_edge(START, "supervisor")
graph = builder.compile()
```

**Key Patterns:**
1. **Supervisor-Worker:** Central coordinator delegates to specialized agents
2. **Network Architecture:** Agents route dynamically between each other
3. **Sequential Pipeline:** Linear chain with output->input passing
4. **Hierarchical:** Supervisor of supervisors for complex workflows

### Finding 4: CrewAI Crew and Task Patterns

**Source:** [CrewAI Documentation](https://docs.crewai.com/en/concepts/agents)
**Confidence:** HIGH
**Relevance:** Role-based agent architecture patterns

CrewAI implements a flexible coordinator-worker model with:

**Core Components:**
- **Agent:** LLM-powered unit with name, role, goal
- **Task:** Specific job with description and expected output
- **Crew:** Team of agents working together
- **Flow:** Event-driven pipeline for complex orchestration

**Execution Strategies:**
- **Sequential:** Chained subtasks, each dependent on previous
- **Hierarchical:** Manager agent supervises and delegates
- **Parallel:** Independent subtasks run concurrently

**Role Architecture:**
```python
# CrewAI role pattern (conceptual adaptation)
roles = {
    "researcher": {
        "goal": "Gather comprehensive information",
        "backstory": "Expert researcher with analytical skills"
    },
    "reviewer": {
        "goal": "Validate research quality and accuracy",
        "backstory": "Detail-oriented quality specialist"
    },
    "synthesizer": {
        "goal": "Consolidate findings into actionable insights",
        "backstory": "Strategic thinker skilled at synthesis"
    }
}
```

### Finding 5: Microsoft AutoGen and Agent Framework Patterns

**Source:** [Microsoft AutoGen](https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat/)
**Confidence:** HIGH
**Relevance:** Conversation-based multi-agent patterns

**Key Insights:**
- AutoGen 0.4 (January 2025) introduced asynchronous, event-driven architecture
- Microsoft Agent Framework (October 2025) unifies AutoGen + Semantic Kernel
- Agents communicate through asynchronous messages

**Orchestration Patterns:**
1. **Sequential:** Agents process in order
2. **Concurrent:** Parallel processing with aggregation
3. **Hand-off:** Explicit control transfer between agents
4. **Magentic:** Dynamic orchestration based on task requirements

**Agent Abstractions:**
```python
# AutoGen pattern (conceptual)
class ConversableAgent:
    """Foundation for conversational agents"""
    pass

class AssistantAgent(ConversableAgent):
    """LLM-driven assistance"""
    pass

class UserProxyAgent(ConversableAgent):
    """Human proxy with code execution"""
    pass
```

### Finding 6: Token Optimization and Context Management

**Source:** [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
**Confidence:** HIGH
**Relevance:** Critical for multi-agent efficiency

**Sub-Agent Architecture Benefits:**
- Subagents process with isolated context windows
- Each returns condensed summary (1,000-2,000 tokens)
- Lead agent focuses on synthesis
- **67% fewer tokens** due to context isolation

**Anthropic's Multi-Agent Research Results:**
- Opus 4 lead agent + Sonnet 4 subagents
- **90.2% performance improvement** over single-agent Opus 4
- Token usage explains 80% of performance variance

**Context Optimization Strategies:**
1. **Context Isolation:** Fresh context per subagent for discrete tasks
2. **Compaction:** Summarize older events over sliding window
3. **Selective Sharing:** Pass only necessary state between agents
4. **Embedding Compression:** Store as vectors, reconstruct on demand

**Anti-Pattern: Context Pollution**
```
BAD: Every sub-agent shares same context
     -> Massive KV-cache penalty
     -> Model confusion with irrelevant details

GOOD: Spin up fresh sub-agent with specific instruction
      -> Pass only instruction needed to function
      -> Share full memory only when required for trajectory
```

### Finding 7: Error Handling and Retry Patterns

**Source:** [Claude Agent SDK Error Handling](https://github.com/anthropics/claude-agent-sdk-python/blob/main/README.md)
**Confidence:** HIGH
**Relevance:** Production reliability requirement

**SDK Exception Hierarchy:**
```python
from claude_agent_sdk import (
    ClaudeSDKError,      # Base error
    CLINotFoundError,    # Claude Code not installed
    CLIConnectionError,  # Connection issues
    ProcessError,        # Process failed
    CLIJSONDecodeError,  # JSON parsing issues
)

async def robust_query():
    try:
        async for message in query(prompt="Execute task"):
            if isinstance(message, AssistantMessage):
                if message.error:
                    # Detect rate limits, auth errors
                    handle_error(message.error)
    except ProcessError as e:
        print(f"Process failed: {e.exit_code}")
        if e.stderr:
            print(f"Error: {e.stderr}")
    except CLIConnectionError:
        # Retry with backoff
        await asyncio.sleep(exponential_backoff())
        return await robust_query()
```

**PostToolUse Hook for Error Detection:**
```python
async def stop_on_critical_error(input_data, tool_use_id, context):
    tool_response = input_data.get("tool_response", "")
    if "critical" in str(tool_response).lower():
        return {
            "continue_": False,
            "stopReason": "Critical error detected",
            "systemMessage": "Execution stopped for safety"
        }
    return {"continue_": True}
```

### Finding 8: Architecture Comparison

**Source:** [Arize AI Framework Comparison](https://arize.com/blog/orchestrator-worker-agents-a-practical-comparison-of-common-agent-frameworks/)
**Confidence:** MEDIUM
**Relevance:** Framework selection guidance

| Framework | Execution Speed | Token Efficiency | State Management |
|-----------|-----------------|------------------|------------------|
| LangGraph | Fastest | Most efficient (state deltas) | Graph-based checkpoints |
| LangChain | Moderate | Higher (heavy history) | Memory chains |
| AutoGen | Moderate | Predictable | Async event-driven |
| CrewAI | Slower | Variable | Autonomous deliberation |

**LangGraph Advantages:**
- Optimized state transitions
- Durable execution with checkpoints
- Human-in-the-loop support
- Time travel debugging

---

## Conclusions

### Key Insights

1. **Native SDK Support:** Claude Agent SDK provides complete multi-agent orchestration through subagents, eliminating need for custom subprocess management. The `AgentDefinition` + `Task` tool pattern directly addresses the research->review->synthesis chain requirement.

2. **Context Isolation is Critical:** Sub-agent architectures with isolated context windows achieve 67% token reduction and 90.2% performance improvement. This is not just optimization but architectural necessity for production systems.

3. **Session Management Enables Chaining:** SDK session capture/resume/fork capabilities provide the state management backbone. Session forking allows exploration of alternative approaches without losing main context.

4. **Industry Patterns Converge:** LangGraph supervisor pattern, CrewAI crews, and AutoGen group chat all implement variations of coordinator-worker architecture. The pattern is proven across frameworks.

5. **Error Handling Built-In:** SDK provides comprehensive error hierarchy with hooks for custom handling. PostToolUse hooks enable circuit-breaker patterns for critical errors.

### Implications

**For ECW Orchestrator Design:**
- Use Claude Agent SDK's native subagent architecture rather than subprocess orchestration
- Define specialized agents: ps-researcher, ps-reviewer, ps-synthesizer
- Implement supervisor agent (possibly using Opus) coordinating Sonnet subagents
- Leverage session management for context passing between phases
- Apply context isolation to prevent context pollution and optimize tokens

**For Implementation:**
- Start with sequential pipeline (research -> review -> synthesis)
- Add supervisor layer for dynamic routing as needed
- Implement error handling with retry/fallback strategies
- Persist intermediate results to filesystem for traceability

---

## Recommendations

| Priority | Recommendation | Rationale | Effort |
|----------|---------------|-----------|--------|
| HIGH | Use Claude Agent SDK subagent architecture | Native support, bundled CLI, built-in error handling | S |
| HIGH | Implement context isolation per agent | 67% token savings, prevents context pollution | S |
| HIGH | Define three specialized agents (researcher, reviewer, synthesizer) | Maps to existing PS agent requirements | M |
| MEDIUM | Add supervisor agent for dynamic orchestration | Enables adaptive routing based on task | M |
| MEDIUM | Implement session checkpointing | Allows resume on failure, provides audit trail | M |
| LOW | Explore LangGraph for complex workflows | May provide better state management for future needs | L |

---

## Sources

| # | Source | Type | Relevance | Accessed |
|---|--------|------|-----------|----------|
| 1 | [Claude Agent SDK Python](https://github.com/anthropics/claude-agent-sdk-python) | Doc | HIGH | 2026-01-04 |
| 2 | [Claude Agent SDK Subagents](https://github.com/context7/platform_claude_en_agent-sdk/blob/main/subagents.md) | Doc | HIGH | 2026-01-04 |
| 3 | [Claude Agent SDK Sessions](https://github.com/context7/platform_claude_en_agent-sdk/blob/main/sessions.md) | Doc | HIGH | 2026-01-04 |
| 4 | [LangGraph Multi-Agent](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/concepts/multi_agent.md) | Doc | HIGH | 2026-01-04 |
| 5 | [CrewAI Framework](https://docs.crewai.com/en/concepts/agents) | Doc | HIGH | 2026-01-04 |
| 6 | [AutoGen 0.2](https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat/) | Doc | HIGH | 2026-01-04 |
| 7 | [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview) | Doc | MEDIUM | 2026-01-04 |
| 8 | [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Web | HIGH | 2026-01-04 |
| 9 | [Semantic Kernel Agent Orchestration](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/) | Doc | MEDIUM | 2026-01-04 |
| 10 | [LangGraph Swarm](https://github.com/langchain-ai/langgraph-swarm-py) | Doc | MEDIUM | 2026-01-04 |
| 11 | [Claude Code Headless](https://code.claude.com/docs/en/headless) | Doc | HIGH | 2026-01-04 |
| 12 | [Arize Framework Comparison](https://arize.com/blog/orchestrator-worker-agents-a-practical-comparison-of-common-agent-frameworks/) | Web | MEDIUM | 2026-01-04 |
| 13 | [Context Engineering Multi-Agent](https://www.vellum.ai/blog/multi-agent-systems-building-with-context-engineering) | Web | MEDIUM | 2026-01-04 |

---

## Knowledge Items Generated

### Assumptions (ASM)

- **ASM-062:** Claude Agent SDK subagent Task tool provides sufficient delegation capability for research->review->synthesis pipeline
  - Context: SDK documentation shows Task tool with description, prompt, and subagent_type inputs
  - Impact if Wrong: Would require custom subprocess orchestration, significantly more complex
  - Confidence: HIGH (SDK documentation explicit on this capability)

- **ASM-063:** Session resume maintains sufficient context for multi-phase agent chains
  - Context: Session management docs show capture/resume pattern with full context
  - Impact if Wrong: Would need explicit state serialization between phases
  - Confidence: HIGH (Multiple code examples demonstrate this)

- **ASM-064:** Context isolation between subagents is automatic when using Task tool
  - Context: Each subagent gets fresh context per Anthropic's design guidance
  - Impact if Wrong: Token usage would be higher than expected
  - Confidence: MEDIUM (Implied but not explicitly confirmed in SDK docs)

### Lessons Learned (LES)

- **LES-053:** Native SDK orchestration is superior to subprocess management
  - Context: SDK bundles CLI, handles JSON streaming, provides async patterns
  - Prevention: Always check for native SDK capabilities before building custom solutions

- **LES-054:** Context pollution is the primary failure mode in multi-agent systems
  - Context: Sharing full context between all agents causes performance degradation
  - Prevention: Apply context isolation pattern; share only necessary state

### Patterns (PAT)

- **PAT-055:** Supervisor-Worker Multi-Agent Pattern
  - When to Use: Complex tasks requiring specialized agents with central coordination
  - Example: Opus supervisor + Sonnet workers for research tasks

- **PAT-056:** Session-Based Agent Chaining
  - When to Use: Sequential agent pipeline requiring context continuity
  - Example: Capture session_id from init message, resume with same ID for next phase

- **PAT-057:** Context Isolation for Token Optimization
  - When to Use: Multi-agent systems where each agent handles discrete subtask
  - Example: Fresh subagent context per task, return only condensed summary

---

## PS Integration

| Action | Command | Status |
|--------|---------|--------|
| Exploration Entry | `add-entry phase-38.17 "Option B - SDK-Based Orchestrator"` | Done |
| Entry Type | `set-entry-type phase-38.17 e-122 RESEARCH` | Done |
| Artifact Link | `link-artifact phase-38.17 e-122 FILE "docs/research/phase-38.17-e-122-option-b-sdk-orchestrator.md"` | Pending |
| Knowledge Refs | `add-knowledge phase-38.17 ASM-062 ASM-063 ASM-064 LES-053 LES-054 PAT-055 PAT-056 PAT-057` | Pending |

---

## Appendix

### Raw Notes

**SDK Installation:**
```bash
pip install claude-agent-sdk
# CLI is bundled - no separate installation required
```

**Minimal Orchestrator Skeleton:**
```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

AGENTS = {
    "ps-researcher": AgentDefinition(
        description="Research specialist for deep exploration of topics",
        prompt="You are the ps-researcher agent. Research thoroughly and document findings.",
        tools=["Read", "Glob", "Grep", "WebSearch", "WebFetch"],
        model="sonnet"
    ),
    "ps-reviewer": AgentDefinition(
        description="Quality reviewer for research validation",
        prompt="You are the ps-reviewer agent. Validate research quality and completeness.",
        tools=["Read", "Glob", "Grep"],
        model="sonnet"
    ),
    "ps-synthesizer": AgentDefinition(
        description="Synthesis agent for consolidating research into knowledge",
        prompt="You are the ps-synthesizer agent. Consolidate and synthesize findings.",
        tools=["Read", "Write"],
        model="opus"
    )
}

async def orchestrate_research(topic: str, ps_id: str):
    """Three-phase research orchestration pipeline."""

    # Phase 1: Research
    session_id = None
    async for message in query(
        prompt=f"Research: {topic}",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Task", "WebSearch"],
            agents=AGENTS
        )
    ):
        if hasattr(message, 'subtype') and message.subtype == 'init':
            session_id = message.session_id

    # Phase 2: Review (resume session)
    async for message in query(
        prompt="Review the research findings for quality and completeness",
        options=ClaudeAgentOptions(resume=session_id)
    ):
        pass

    # Phase 3: Synthesize (resume session)
    async for message in query(
        prompt="Synthesize the validated research into knowledge items",
        options=ClaudeAgentOptions(resume=session_id)
    ):
        if hasattr(message, "result"):
            return message.result

if __name__ == "__main__":
    result = asyncio.run(orchestrate_research("SDK orchestration patterns", "phase-38.17"))
    print(result)
```

### Related Research

- Phase 38.16 PS Agent Architecture
- Phase 38.17 PS Enhancement Investigation
- ECW Memory-First Architecture (Phase 19A)

---

**Generated by:** ps-researcher agent
**Template Version:** 1.0 (Phase 38.16.7)
**Research Completed:** 2026-01-04
