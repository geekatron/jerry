# Multi-Agent Orchestration Patterns: Industry Research

**Document ID:** AGENT-RESEARCH-002
**Date:** 2026-01-09
**Author:** ps-researcher
**Status:** Complete

---

## Executive Summary

This research document provides a comprehensive analysis of multi-agent orchestration patterns from leading AI frameworks including CrewAI, LangGraph, Microsoft AutoGen/Agent Framework, Google ADK, OpenAI Agents SDK, and Anthropic's patterns. The document catalogs orchestration patterns, compares frameworks, provides code examples, and offers recommendations for different use cases.

### Key Findings

1. **Four Primary Orchestration Patterns Emerge:** Sequential, Hierarchical, Network (Peer-to-Peer), and Supervisor patterns dominate across all frameworks.

2. **Handoff Mechanisms Are Universal:** All frameworks implement agent-to-agent handoffs as a core primitive, though implementations vary significantly.

3. **State Management Approaches Differ Significantly:** From graph-based checkpointing (LangGraph) to layered memory (CrewAI) to conversational context (AutoGen).

4. **Industry Consolidation in 2025:** OpenAI replaced Swarm with Agents SDK; Microsoft merged AutoGen with Semantic Kernel into Agent Framework; Anthropic's MCP became the de-facto standard for tool integration.

5. **Trade-offs Are Context-Dependent:** No single framework excels across all dimensions. Choice depends on workflow complexity, team expertise, and production requirements.

---

## Pattern Catalog

### Pattern 1: Sequential Pipeline

The simplest orchestration pattern where agents execute in a predetermined linear order, passing output to the next agent in the chain.

```
+----------+     +----------+     +----------+     +----------+
|  Agent A | --> |  Agent B | --> |  Agent C | --> |  Output  |
| (Research)|    | (Analysis)|    | (Writing)|     |          |
+----------+     +----------+     +----------+     +----------+
     |                |                |
     v                v                v
  [State 1]       [State 2]        [State 3]
```

**Characteristics:**
- Linear, deterministic flow
- Easy to debug and understand
- Each agent receives the complete output of the previous agent
- No parallel execution

**Best For:**
- Data processing pipelines
- Document generation workflows
- Simple multi-step tasks with clear dependencies

**Framework Implementations:**

| Framework | Implementation |
|-----------|---------------|
| CrewAI | `Process.sequential` |
| LangGraph | Linear graph with edges |
| Google ADK | `SequentialAgent` |
| AutoGen | Sequential chat pattern |

---

### Pattern 2: Hierarchical / Supervisor

A central manager/supervisor agent coordinates specialized worker agents, delegating tasks and synthesizing results.

```
                    +----------------+
                    |   Supervisor   |
                    |    (Manager)   |
                    +-------+--------+
                            |
           +----------------+----------------+
           |                |                |
           v                v                v
    +-----------+    +-----------+    +-----------+
    | Worker A  |    | Worker B  |    | Worker C  |
    | (Research)|    |  (Math)   |    | (Writing) |
    +-----------+    +-----------+    +-----------+
           |                |                |
           +----------------+----------------+
                            |
                            v
                    +----------------+
                    |    Results     |
                    |  Aggregation   |
                    +----------------+
```

**Characteristics:**
- Centralized control and decision-making
- Supervisor decides which worker handles each subtask
- Workers can operate in parallel
- Clear accountability and task routing

**Best For:**
- Complex tasks requiring multiple specializations
- Workflows with clear decomposition
- Systems requiring audit trails

**Framework Implementations:**

| Framework | Implementation |
|-----------|---------------|
| CrewAI | `Process.hierarchical` with `manager_llm` |
| LangGraph | Supervisor node with handoff tools |
| Google ADK | Coordinator pattern with `LlmAgent` |
| AutoGen | GroupChat with manager |

---

### Pattern 3: Network (Peer-to-Peer)

Agents communicate directly with each other without a central coordinator. Each agent can hand off to any other agent.

```
    +-----------+
    |  Agent A  |<---------+
    +-----------+          |
         ^   |             |
         |   v             |
    +-----------+    +-----------+
    |  Agent B  |<-->|  Agent C  |
    +-----------+    +-----------+
         ^                 |
         |                 |
         +-----------------+
```

**Characteristics:**
- Decentralized decision-making
- Any agent can route to any other agent
- Flexible for emergent behaviors
- More complex to debug

**Best For:**
- Problems without clear hierarchy
- Exploratory or creative tasks
- Peer-to-peer collaboration scenarios

**Framework Implementations:**

| Framework | Implementation |
|-----------|---------------|
| LangGraph | Graph with multi-directional edges |
| OpenAI Swarm/SDK | Handoff functions between all agents |
| CrewAI | Agents with `allow_delegation=True` |

---

### Pattern 4: Orchestrator-Worker

An orchestrator dynamically decomposes tasks at runtime and spawns/delegates to workers, adapting based on intermediate results.

```
                +------------------+
                |   Orchestrator   |
                | (Dynamic Planner)|
                +--------+---------+
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
   [Subtask 1]      [Subtask 2]      [Subtask N]
        |                |                |
        v                v                v
   +---------+      +---------+      +---------+
   | Worker  |      | Worker  |      | Worker  |
   +---------+      +---------+      +---------+
        |                |                |
        +----------------+----------------+
                         |
                         v
                +------------------+
                |    Orchestrator  |
                | (Observe/Decide) |
                +------------------+
                         |
                         v
              [More Subtasks or Done]
```

**Characteristics:**
- Dynamic task decomposition at runtime
- Iterative refinement based on results
- Orchestrator maintains global plan
- Workers are stateless and focused

**Best For:**
- Research systems with emergent structure
- Complex problem-solving
- Multi-step reasoning tasks

**Framework Implementations:**

| Framework | Implementation |
|-----------|---------------|
| Anthropic | Lead agent with subagent spawning |
| Microsoft Agent Framework | Magentic orchestration |
| LangGraph | StateGraph with dynamic routing |

---

### Pattern 5: Generator-Critic (Evaluator-Optimizer)

Separates content generation from validation. One agent produces output while another evaluates and provides feedback for iteration.

```
    +-----------+         +-----------+
    | Generator |-------->|   Critic  |
    |  (Draft)  |         | (Evaluate)|
    +-----------+         +-----------+
         ^                      |
         |                      |
         |    [Feedback Loop]   |
         +----------------------+
                   |
                   v
            [Pass/Fail Decision]
                   |
         +----+----+----+
         |              |
         v              v
    [Continue]      [Accept]
```

**Characteristics:**
- Self-improving through iteration
- Clear separation of concerns
- Conditional looping
- Quality assurance built-in

**Best For:**
- Content generation with quality requirements
- Code generation and review
- Document drafting

**Framework Implementations:**

| Framework | Implementation |
|-----------|---------------|
| Google ADK | Generator-Critic pattern with `LoopAgent` |
| CrewAI | Flow with `@router` decorator |
| LangGraph | Conditional edges with feedback loops |

---

### Pattern 6: Parallel Execution (Map-Reduce)

Multiple agents work on independent subtasks concurrently, with results aggregated afterward.

```
                +------------------+
                |   Input/Splitter |
                +--------+---------+
                         |
        +-------+--------+--------+-------+
        |       |        |        |       |
        v       v        v        v       v
    +-----+ +-----+  +-----+  +-----+ +-----+
    |Ag 1 | |Ag 2 |  |Ag 3 |  |Ag 4 | |Ag N |
    +-----+ +-----+  +-----+  +-----+ +-----+
        |       |        |        |       |
        +-------+--------+--------+-------+
                         |
                         v
                +------------------+
                |    Aggregator    |
                +------------------+
```

**Characteristics:**
- Concurrent execution
- Significant time savings
- Requires independent subtasks
- Aggregation logic needed

**Best For:**
- Independent data processing
- Multi-source research
- Batch operations

**Framework Implementations:**

| Framework | Implementation |
|-----------|---------------|
| Google ADK | `ParallelAgent` |
| LangGraph | `Send` API for map-reduce |
| CrewAI | Parallel tasks in Flow |

---

### Pattern 7: Human-in-the-Loop

Incorporates human approval or input at critical decision points in the agent workflow.

```
    +-----------+     +-------------+     +-----------+
    |  Agent A  | --> |   Human     | --> |  Agent B  |
    |           |     |  Approval   |     |           |
    +-----------+     +-------------+     +-----------+
                            |
                            v
                    [Approve/Reject/Edit]
```

**Characteristics:**
- Breakpoints for human review
- Supports approval workflows
- Can modify state before continuation
- Critical for high-stakes decisions

**Framework Implementations:**

| Framework | Implementation |
|-----------|---------------|
| LangGraph | `interrupt_before`/`interrupt_after` |
| Google ADK | Built-in HITL support |
| CrewAI | `human_input=True` on tasks |

---

## Framework Comparison Matrix

| Dimension | CrewAI | LangGraph | AutoGen/Agent Framework | Google ADK | OpenAI Agents SDK |
|-----------|--------|-----------|------------------------|------------|-------------------|
| **Design Philosophy** | Role-based | Graph-based | Conversational | Code-first | Minimal abstractions |
| **Primary Pattern** | Hierarchical/Sequential | Any (graph) | Conversational | Workflow Agents | Handoff-based |
| **State Management** | Layered (ChromaDB + SQLite) | Checkpointing (time-travel) | Context variables | Shared state | Session-based |
| **Memory Persistence** | Built-in (short/long-term) | Configurable stores | Developer-managed | Shared state | Session storage |
| **Learning Curve** | Low-Medium | Medium-High | Low | Medium | Low |
| **Production Ready** | Yes | Yes (v1.0 Oct 2025) | Yes (Agent Framework) | Yes | Yes |
| **Parallel Execution** | Via Flows | Native (`Send`) | Native | `ParallelAgent` | Limited |
| **Human-in-the-Loop** | Task-level | Interrupt nodes | Built-in | Built-in | Guardrails |
| **Tool Integration** | Native + LangChain | LangChain tools | Function tools | Google Cloud | Function tools |
| **Debugging** | Verbose mode | LangSmith | OpenTelemetry | Google Cloud tools | Built-in tracing |

---

## Handoff Mechanisms

### CrewAI Delegation

CrewAI uses agent-level delegation through the `allow_delegation` parameter:

```python
from crewai import Agent, Crew, Task, Process

manager = Agent(
    role="Project Manager",
    goal="Coordinate team efforts",
    allow_delegation=True,  # Can delegate to other agents
    verbose=True
)

researcher = Agent(
    role="Researcher",
    goal="Provide accurate research",
    allow_delegation=False,  # Focuses on own expertise
    verbose=True
)

crew = Crew(
    agents=[manager, researcher],
    tasks=[project_task],
    process=Process.hierarchical,
    manager_llm="gpt-4o"
)
```

### LangGraph Command-Based Handoffs

LangGraph uses the `Command` object for explicit handoffs with state updates:

```python
from typing import Annotated
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

def create_handoff_tool(*, agent_name: str, description: str | None = None):
    name = f"transfer_to_{agent_name}"
    description = description or f"Transfer to {agent_name}"

    @tool(name, description=description)
    def handoff_tool(
        state: Annotated[dict, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        tool_message = {
            "role": "tool",
            "content": f"Successfully transferred to {agent_name}",
            "name": name,
            "tool_call_id": tool_call_id,
        }
        return Command(
            goto=agent_name,  # Navigate to target agent
            update={"messages": state["messages"] + [tool_message]},
            graph=Command.PARENT,  # Update parent graph
        )
    return handoff_tool

# Create handoff tools
transfer_to_research = create_handoff_tool(
    agent_name="research_agent",
    description="Transfer to research specialist"
)
transfer_to_writer = create_handoff_tool(
    agent_name="writer_agent",
    description="Transfer to content writer"
)
```

### OpenAI Agents SDK Handoffs

The Agents SDK provides handoffs as a core primitive:

```python
from openai_agents import Agent, handoff

# Define specialized agents
research_agent = Agent(
    name="researcher",
    instructions="You are a research specialist...",
    tools=[search_tool, browse_tool]
)

writer_agent = Agent(
    name="writer",
    instructions="You are a content writer...",
    tools=[format_tool]
)

# Main agent with handoff capabilities
coordinator = Agent(
    name="coordinator",
    instructions="Route requests to specialists...",
    handoffs=[
        handoff(research_agent, "For research tasks"),
        handoff(writer_agent, "For writing tasks")
    ]
)
```

### Google ADK Handoffs

Google ADK uses explicit invocation via `AgentTool`:

```python
from google.adk import LlmAgent, AgentTool, SequentialAgent

# Define specialist agents
researcher = LlmAgent(
    name="researcher",
    model="gemini-pro",
    system_instruction="You are a research specialist..."
)

writer = LlmAgent(
    name="writer",
    model="gemini-pro",
    system_instruction="You are a content writer..."
)

# Wrap as tools for coordinator
researcher_tool = AgentTool(researcher, description="Call for research tasks")
writer_tool = AgentTool(writer, description="Call for writing tasks")

# Coordinator with agent tools
coordinator = LlmAgent(
    name="coordinator",
    model="gemini-pro",
    tools=[researcher_tool, writer_tool],
    system_instruction="Route requests to the appropriate specialist..."
)
```

---

## State Management Across Agent Boundaries

### LangGraph: Checkpointing and Time-Travel

LangGraph provides the most sophisticated state management through checkpointers:

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import StateGraph, MessagesState

# Development: In-memory
checkpointer = InMemorySaver()

# Production: Persistent storage
# checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
# checkpointer = PostgresSaver.from_conn_string("postgresql://...")

# Compile graph with checkpointer
graph = builder.compile(checkpointer=checkpointer)

# Execute with thread isolation
config = {"configurable": {"thread_id": "conversation-1"}}
result = graph.invoke({"messages": [{"role": "user", "content": "Hello"}]}, config)

# Time-travel: Get state history
for checkpoint in graph.get_state_history(config):
    print(f"Checkpoint: {checkpoint.config['configurable']['checkpoint_id']}")
    print(f"State: {checkpoint.values}")

# Resume from specific checkpoint
past_config = {
    "configurable": {
        "thread_id": "conversation-1",
        "checkpoint_id": "specific-checkpoint-id"
    }
}
result = graph.invoke(new_input, config=past_config)
```

### CrewAI: Layered Memory System

CrewAI provides built-in layered memory:

```python
from crewai import Crew, Agent, Task

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True,  # Enable memory system
    verbose=True
)

# Memory layers:
# - Short-term: ChromaDB vector store (conversation context)
# - Recent results: SQLite (task outputs)
# - Long-term: SQLite (persistent knowledge)
# - Entity memory: Vector embeddings
```

### CrewAI Flows: Pydantic State Management

```python
from crewai.flow.flow import Flow, start, listen, router
from pydantic import BaseModel

class WorkflowState(BaseModel):
    research_data: dict = {}
    analysis_complete: bool = False
    confidence: float = 0.0
    recommendations: list = []

class ResearchFlow(Flow[WorkflowState]):

    @start()
    def gather_research(self):
        # State is automatically managed
        self.state.research_data = {"source": "api", "records": 100}
        return self.state.research_data

    @listen(gather_research)
    def analyze_data(self, research_data):
        self.state.confidence = 0.85
        self.state.analysis_complete = True
        return "Analysis complete"

    @router(analyze_data)
    def route_based_on_confidence(self):
        if self.state.confidence > 0.8:
            return "high_confidence"
        return "low_confidence"

    @listen("high_confidence")
    def execute_strategy(self):
        self.state.recommendations.append("Proceed with plan A")
        return self.state.recommendations
```

### Microsoft Agent Framework: Workflow State

```python
from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.contents import ChatMessageContent

# Agents share conversation history automatically
group_chat = AgentGroupChat(
    agents=[researcher, analyst, writer],
    termination_strategy=TerminationStrategy.max_messages(10)
)

# State persisted through workflow abstraction
async with group_chat:
    async for message in group_chat.invoke("Analyze market trends"):
        print(f"{message.author_name}: {message.content}")
```

---

## Trade-offs Analysis

### Complexity vs. Control

| Framework | Complexity | Control Level |
|-----------|------------|---------------|
| CrewAI | Low | Medium |
| LangGraph | High | Very High |
| OpenAI SDK | Low | Medium |
| Google ADK | Medium | High |
| AutoGen | Medium | Medium-High |

**Recommendation:** Choose LangGraph for maximum control over complex workflows. Choose CrewAI or OpenAI SDK for rapid development with sensible defaults.

### Learning Curve vs. Flexibility

```
High Flexibility
     ^
     |     * LangGraph
     |
     |        * Google ADK
     |
     |           * AutoGen/Agent Framework
     |
     |              * CrewAI
     |
     |                 * OpenAI Agents SDK
     +---------------------------------------->
                                    Low Learning Curve
```

### State Management Trade-offs

| Approach | Pros | Cons |
|----------|------|------|
| **Checkpointing (LangGraph)** | Time-travel, fault tolerance, debugging | Storage overhead, complexity |
| **Layered Memory (CrewAI)** | Built-in, semantic search | Less control, vendor lock-in |
| **Session-based (OpenAI)** | Simple, automatic | Limited persistence options |
| **Shared State (ADK)** | Direct access, simple | Careful coordination needed |

### Parallel Execution Trade-offs

| Pattern | Pros | Cons |
|---------|------|------|
| **Native Parallel (ADK, LangGraph)** | True concurrency, time savings | Harder to debug, resource intensive |
| **Sequential with Batching** | Predictable, easy debugging | Slower, no real parallelism |
| **Async Flows (CrewAI)** | Non-blocking, streaming | Complexity in error handling |

---

## Recommended Patterns by Use Case

### Use Case 1: Document Generation Pipeline

**Recommended Pattern:** Sequential Pipeline
**Best Framework:** CrewAI or LangGraph

```python
# CrewAI Implementation
from crewai import Crew, Process, Agent, Task

researcher = Agent(role="Researcher", goal="Gather information")
analyst = Agent(role="Analyst", goal="Analyze findings")
writer = Agent(role="Writer", goal="Draft document")
editor = Agent(role="Editor", goal="Polish content")

crew = Crew(
    agents=[researcher, analyst, writer, editor],
    tasks=[research_task, analysis_task, writing_task, editing_task],
    process=Process.sequential
)
```

### Use Case 2: Customer Support System

**Recommended Pattern:** Network with Handoffs
**Best Framework:** LangGraph Swarm or OpenAI Agents SDK

```python
# LangGraph Swarm Implementation
from langgraph_swarm import create_handoff_tool, create_swarm

transfer_to_billing = create_handoff_tool(
    agent_name="billing_agent",
    description="Transfer for billing inquiries"
)
transfer_to_technical = create_handoff_tool(
    agent_name="technical_agent",
    description="Transfer for technical support"
)

general_agent = create_agent(
    model,
    tools=[transfer_to_billing, transfer_to_technical],
    name="general_agent"
)

swarm = create_swarm([general_agent, billing_agent, technical_agent])
```

### Use Case 3: Research and Analysis System

**Recommended Pattern:** Orchestrator-Worker with Dynamic Decomposition
**Best Framework:** LangGraph or Anthropic's Pattern

```python
# LangGraph with Dynamic Orchestration
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

def orchestrator(state):
    """Dynamically decompose task and spawn workers"""
    subtasks = decompose_task(state["query"])

    return Command(
        goto="worker_pool",
        update={"subtasks": subtasks, "results": []}
    )

def worker_pool(state):
    """Process subtasks in parallel"""
    results = []
    for subtask in state["subtasks"]:
        result = process_subtask(subtask)
        results.append(result)

    return {"results": results}

def synthesizer(state):
    """Aggregate worker results"""
    return {"final_answer": synthesize(state["results"])}

graph = StateGraph(ResearchState)
graph.add_node("orchestrator", orchestrator)
graph.add_node("worker_pool", worker_pool)
graph.add_node("synthesizer", synthesizer)
graph.add_edge(START, "orchestrator")
graph.add_edge("orchestrator", "worker_pool")
graph.add_edge("worker_pool", "synthesizer")
graph.add_edge("synthesizer", END)
```

### Use Case 4: Content Generation with Quality Assurance

**Recommended Pattern:** Generator-Critic Loop
**Best Framework:** Google ADK or CrewAI Flows

```python
# Google ADK Implementation
from google.adk import LlmAgent, LoopAgent, SequentialAgent

generator = LlmAgent(
    name="generator",
    model="gemini-pro",
    system_instruction="Generate content based on requirements..."
)

critic = LlmAgent(
    name="critic",
    model="gemini-pro",
    system_instruction="Evaluate content quality. Return PASS or provide feedback..."
)

# Sequential within loop
gen_crit_sequence = SequentialAgent(
    name="gen_crit_cycle",
    sub_agents=[generator, critic]
)

# Loop until quality passes
quality_loop = LoopAgent(
    name="quality_assurance",
    sub_agent=gen_crit_sequence,
    max_iterations=3,
    exit_condition=lambda state: "PASS" in state.get("critic_output", "")
)
```

### Use Case 5: Enterprise Multi-Team Coordination

**Recommended Pattern:** Hierarchical with Team Supervisors
**Best Framework:** LangGraph or Microsoft Agent Framework

```python
# LangGraph Hierarchical Teams
from langgraph.graph import StateGraph

# Team 1: Research Team
research_supervisor = create_react_agent(
    model,
    tools=[assign_to_web_researcher, assign_to_data_analyst],
    prompt="You supervise the research team..."
)

# Team 2: Content Team
content_supervisor = create_react_agent(
    model,
    tools=[assign_to_writer, assign_to_editor],
    prompt="You supervise the content team..."
)

# Top-level Supervisor
top_supervisor = create_react_agent(
    model,
    tools=[assign_to_research_team, assign_to_content_team],
    prompt="You coordinate between teams..."
)

# Build hierarchical graph
builder = StateGraph(TeamState)
builder.add_node("top_supervisor", top_supervisor)
builder.add_node("research_team", research_graph)
builder.add_node("content_team", content_graph)
```

---

## Industry Landscape (2025-2026)

### Major Framework Updates

| Date | Event |
|------|-------|
| March 2025 | OpenAI Agents SDK replaces experimental Swarm |
| May 2025 | LangGraph Platform reaches GA |
| October 2025 | LangGraph 1.0 stable release |
| October 2025 | Microsoft Agent Framework merges AutoGen + Semantic Kernel |
| November 2025 | MCP specification 2025-11-25 released |
| December 2025 | Anthropic donates MCP to Linux Foundation |

### Adoption Trends

- **LangGraph/LangChain:** Most widely used agentic AI framework
- **AutoGen/Agent Framework:** Growing rapidly, especially in enterprise
- **MCP:** De-facto standard for tool integration (8M+ server downloads)
- **Google ADK:** Strong adoption in Google Cloud ecosystem

### Enterprise Deployments

- **BMW:** Multi-agent systems analyzing terabytes of vehicle telemetry
- **Commerzbank:** Avatar-driven customer support
- **Fujitsu:** Integration services with Agent Framework
- **Citrix, TCS, TeamViewer, Elastic:** Active adopters

---

## Sources

### CrewAI
- [CrewAI Documentation](https://docs.crewai.com/)
- [CrewAI GitHub](https://github.com/crewaiinc/crewai)

### LangGraph
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [LangGraph Multi-Agent Workflows](https://blog.langchain.com/langgraph-multi-agent-workflows/)
- [LangGraph Supervisor Library](https://github.com/langchain-ai/langgraph-supervisor-py)
- [LangGraph Swarm](https://github.com/langchain-ai/langgraph-swarm-py)
- [Complete Guide to Multi-Agent Systems in LangGraph](https://pub.towardsai.net/a-complete-guide-to-multi-agent-systems-in-langgraph-network-to-supervisor-and-hierarchical-models-a0c319cff24b)
- [Hierarchical Agent Teams Tutorial](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/hierarchical_agent_teams/)

### Microsoft AutoGen / Agent Framework
- [Microsoft Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview)
- [AutoGen GitHub](https://github.com/microsoft/autogen)
- [AutoGen Research](https://www.microsoft.com/en-us/research/project/autogen/)
- [Introducing Microsoft Agent Framework](https://azure.microsoft.com/en-us/blog/introducing-microsoft-agent-framework/)
- [Microsoft's Agentic Frameworks: AutoGen and Semantic Kernel](https://devblogs.microsoft.com/autogen/microsofts-agentic-frameworks-autogen-and-semantic-kernel/)
- [Deep Dive into AutoGen Multi-Agent Patterns 2025](https://sparkco.ai/blog/deep-dive-into-autogen-multi-agent-patterns-2025)

### Google ADK
- [Agent Development Kit Documentation](https://google.github.io/adk-docs/)
- [Developer's Guide to Multi-Agent Patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
- [Multi-Agent Systems in ADK](https://google.github.io/adk-docs/agents/multi-agents/)
- [Building Collaborative AI with ADK](https://cloud.google.com/blog/topics/developers-practitioners/building-collaborative-ai-a-developers-guide-to-multi-agent-systems-with-adk)
- [A2A Agent Patterns with ADK](https://medium.com/google-cloud/a2a-agent-patterns-with-the-agent-development-kit-adk-aee3d61c52cf)

### OpenAI
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [Swarm GitHub (Archived)](https://github.com/openai/swarm)
- [Orchestrating Agents: Routines and Handoffs](https://cookbook.openai.com/examples/orchestrating_agents)
- [OpenAI Swarm Framework Guide](https://galileo.ai/blog/openai-swarm-framework-multi-agents)

### Anthropic
- [Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)
- [Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25)
- [Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Claude Agent SDK Best Practices](https://skywork.ai/blog/claude-agent-sdk-best-practices-ai-agents-2025/)

### Comparative Analysis
- [CrewAI vs LangGraph vs AutoGen - DataCamp](https://www.datacamp.com/tutorial/crewai-vs-langgraph-vs-autogen)
- [Top AI Agent Frameworks in 2025 - Codecademy](https://www.codecademy.com/article/top-ai-agent-frameworks-in-2025)
- [Complete Guide to Choosing an AI Agent Framework - Langflow](https://www.langflow.org/blog/the-complete-guide-to-choosing-an-ai-agent-framework-in-2025)
- [Orchestrator-Worker Agents Comparison - Arize AI](https://arize.com/blog/orchestrator-worker-agents-a-practical-comparison-of-common-agent-frameworks/)
- [AI Agent Orchestration Patterns - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [Microsoft Multi-Agent Reference Architecture](https://microsoft.github.io/multi-agent-reference-architecture/docs/context-engineering/Agents-Orchestration.html)

---

## Appendix: Quick Reference Cards

### Pattern Selection Decision Tree

```
Start
  |
  v
Is the task decomposition known upfront?
  |
  +-- YES --> Are tasks independent?
  |             |
  |             +-- YES --> Parallel Pattern
  |             |
  |             +-- NO --> Sequential Pattern
  |
  +-- NO --> Does one entity need central control?
              |
              +-- YES --> Is there a clear hierarchy?
              |             |
              |             +-- YES --> Hierarchical Pattern
              |             |
              |             +-- NO --> Supervisor Pattern
              |
              +-- NO --> Orchestrator-Worker Pattern
```

### Framework Selection Quick Guide

| If you need... | Choose... |
|----------------|-----------|
| Fastest development | CrewAI or OpenAI Agents SDK |
| Maximum flexibility | LangGraph |
| Enterprise features | Microsoft Agent Framework |
| Google Cloud integration | Google ADK |
| Minimal abstractions | OpenAI Agents SDK |
| Time-travel debugging | LangGraph |
| Built-in memory | CrewAI |
| Conversational workflows | AutoGen |

---

*Document generated by ps-researcher subagent*
*Research completed: 2026-01-09*
