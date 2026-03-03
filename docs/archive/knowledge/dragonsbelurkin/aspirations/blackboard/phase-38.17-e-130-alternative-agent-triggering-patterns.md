---
ps: phase-38.17
exploration: e-130
created: 2026-01-04
status: RESEARCH
agent: ps-researcher
title: Alternative Agent Triggering Patterns for Multi-Agent Orchestration
---

# Alternative Agent Triggering Patterns for Multi-Agent Orchestration

> **Research ID:** e-130
> **Phase:** 38.17
> **Agent:** ps-researcher
> **Created:** 2026-01-04
> **Status:** COMPLETE

---

## 1. Executive Summary

This research investigates alternative patterns for triggering AI agents in multi-agent orchestration systems. The investigation focuses on four primary areas: repository-persisted triggers (including blackboard architecture and event sourcing), downstream blocking patterns (futures/promises, polling, callbacks), industry best practices from major frameworks (LangGraph, CrewAI, AutoGen), and alternative orchestration patterns (event-driven, queue-based, state machine, workflow engines).

**Key Findings:**

1. **Blackboard Architecture** has re-emerged as a powerful paradigm for LLM multi-agent systems, enabling 13-57% improvement over baseline approaches by shifting from coordinator-assigned tasks to agent-self-selection based on blackboard content.

2. **Event Sourcing** provides immutable audit trails critical for non-deterministic AI agents, enabling replay, recovery, and full traceability of agent decisions.

3. **LangGraph Supervisor Pattern** offers the most mature hierarchical orchestration with native checkpointing and state persistence through SQLite/PostgreSQL checkpointers.

4. **CrewAI Hierarchical Process** simplifies agent delegation with automatic manager coordination and `@persist` decorators for flow state.

5. **Temporal Workflows** provide industrial-strength durable execution with signals and wait conditions for inter-agent synchronization.

---

## 2. Research Questions

| # | Question | Status | Answer Summary |
|---|----------|--------|----------------|
| 1 | How do frameworks implement file-based or database-persisted signals? | DECIDED | Blackboard (shared memory), Event Stores, SQLite Checkpointers |
| 2 | What patterns exist for downstream agents waiting on upstream results? | DECIDED | Futures/Promises, workflow.wait_condition, @listen decorators |
| 3 | What are industry best practices from major frameworks? | DECIDED | Supervisor hierarchies, Group Chat managers, Hierarchical Crews |
| 4 | What alternative orchestration patterns exist? | DECIDED | Event-driven (Kafka), queue-based (Redis), workflow engines (Temporal) |

---

## 3. Methodology

### 3.1 Research Approach

1. **Context7 MCP Integration:** Used Context7 to query authoritative documentation for LangGraph, CrewAI, and AutoGen
2. **Web Search:** Gathered current (2025-2026) research on blackboard architecture, event sourcing, and agent orchestration
3. **Framework Documentation Analysis:** Deep dive into official documentation for triggering patterns
4. **Pattern Synthesis:** Identified common patterns across frameworks

### 3.2 Sources Consulted

- LangGraph official documentation (langchain-ai/langgraph)
- CrewAI official documentation (crewaiinc/crewai)
- AutoGen official documentation (microsoft/autogen)
- Temporal documentation (temporalio/documentation)
- Academic papers on LLM-based Multi-Agent Systems (LbMAS)
- Industry blog posts from Confluent, Akka, and major AI engineering teams

---

## 4. Findings: W-Dimension Coverage

### 4.1 WHO: Actors and Maintainers

| Actor | Role | Organization |
|-------|------|--------------|
| LangChain/LangGraph Team | Supervisor pattern, StateGraph, Checkpointers | Anthropic ecosystem |
| CrewAI Team | Hierarchical crews, @persist decorators | CrewAI Inc |
| Microsoft AutoGen Team | Group Chat, multi-agent conversations | Microsoft Research |
| Temporal Technologies | Durable workflow execution | Temporal.io |
| Hayes-Roth | Original blackboard architecture (1985) | Stanford |
| LbMAS Researchers | Modern LLM blackboard systems | Academia (ArXiv 2025) |

**Target Users:**
- Enterprise AI teams building production agent systems
- Developers needing fault-tolerant agent orchestration
- Organizations requiring audit trails for AI decisions
- Teams building collaborative multi-agent workflows

### 4.2 WHAT: Specific Mechanisms and Implementations

#### 4.2.1 Blackboard Architecture for LLM Agents

The blackboard architecture has re-emerged as a powerful paradigm for LLM multi-agent systems. Unlike traditional shared-memory where a coordinator assigns tasks, the blackboard approach posts requests that agents independently evaluate.

**Core Components:**
1. **Blackboard (Shared Memory):** Central storage for agent-generated messages, intermediate inferences, and interaction histories
2. **Knowledge Sources (Agents):** Independent modules contributing specific expertise
3. **Control Unit:** Selects which agent acts based on blackboard content

**Key Insight (LbMAS Research):**
> "Rather than assigning subtasks to specific agents, the central agent posts a request on a shared blackboard. Subordinate agents monitoring the blackboard can independently decide whether they possess the capability to contribute."

**Performance Results (ArXiv 2025):**
- 13-57% improvement over master-slave frameworks
- Works across both proprietary and open-source LLMs
- Fewer tokens consumed due to decentralized public memory

```python
# Conceptual Blackboard Pattern
class Blackboard:
    def __init__(self):
        self.public_space = {}  # Shared state
        self.private_spaces = {}  # Per-agent state
        self.message_history = []

    def post_request(self, request: Request):
        """Post task request for any capable agent to claim"""
        self.public_space["current_request"] = request
        self.notify_agents()

    def claim_task(self, agent_id: str, task_id: str):
        """Agent self-selects to handle task"""
        if self._agent_can_handle(agent_id, task_id):
            return True
        return False
```

#### 4.2.2 Event Sourcing for Agent Orchestration

Event sourcing captures every agent decision as an immutable event, enabling:
- **Replay:** Reproduce agent state at any point in time
- **Auditability:** Know why state reached current values
- **Recovery:** Restore from failures by replaying events

**Key Architecture (Akka/KurrentDB):**
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Agent A       │     │   Event Store   │     │   Agent B       │
│   (Producer)    │────▶│   (Immutable)   │◀────│   (Consumer)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │   Replay/Audit  │
                        │   Capability    │
                        └─────────────────┘
```

**Why Event Sourcing for AI Agents (Akka.io):**
> "Since everything that took place in an event sourced system is captured as an immutable event, we can reliably reproduce the state of any agent at any given point in time. Not only do we know and have the ability to regenerate state, we also know why the state is that way."

**Graphite Framework Example:**
> "Graphite employs event sourcing pattern to record every state change. Whenever an Assistant, Node, or Tool is invoked, responds, or fails, a corresponding event is generated and stored in the event store."

#### 4.2.3 LangGraph Supervisor Pattern

LangGraph provides the most mature supervisor pattern for hierarchical agent orchestration.

**Core Mechanism - Command-Based Routing:**
```python
from langgraph.types import Command
from langgraph.graph import StateGraph, MessagesState, START, END

def supervisor(state: MessagesState) -> Command[Literal["agent_1", "agent_2", END]]:
    # LLM determines which agent to route to
    response = model.invoke(...)
    return Command(goto=response["next_agent"])

def agent_1(state: MessagesState) -> Command[Literal["supervisor"]]:
    response = model.invoke(...)
    return Command(
        goto="supervisor",
        update={"messages": [response]},
    )

builder = StateGraph(MessagesState)
builder.add_node(supervisor)
builder.add_node(agent_1)
builder.add_edge(START, "supervisor")
supervisor = builder.compile()
```

**Multi-Level Hierarchical Supervisors:**
```python
from langgraph_supervisor import create_supervisor

# Team-level supervisors
research_team = create_supervisor(
    [research_agent, math_agent],
    model=model,
    supervisor_name="research_supervisor"
).compile(name="research_team")

writing_team = create_supervisor(
    [writing_agent, publishing_agent],
    model=model,
    supervisor_name="writing_supervisor"
).compile(name="writing_team")

# Top-level supervisor managing teams
top_level_supervisor = create_supervisor(
    [research_team, writing_team],
    model=model,
    supervisor_name="top_level_supervisor"
).compile(name="top_level_supervisor")
```

**State Persistence with Checkpointers:**
```python
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver.from_conn_string("checkpoints.db")

graph = builder.compile(checkpointer=checkpointer)

# Execute with thread ID for persistence
config = {"configurable": {"thread_id": "workflow-123"}}
result = graph.invoke({"messages": []}, config)

# Retrieve saved state later
saved_state = graph.get_state(config)
print(f"Next node: {saved_state.next}")

# Get state history for audit
for checkpoint in graph.get_state_history(config):
    print(f"Checkpoint {checkpoint.config['configurable']['checkpoint_id']}")
```

#### 4.2.4 CrewAI Hierarchical Process

CrewAI simplifies agent delegation with automatic manager coordination.

**Hierarchical Crew with Manager LLM:**
```python
from crewai import Agent, Crew, Task, Process

manager = Agent(
    role="Project Manager",
    goal="Coordinate team efforts and ensure project success",
    allow_delegation=True,
    verbose=True
)

researcher = Agent(
    role="Researcher",
    goal="Provide accurate research and analysis",
    allow_delegation=False,  # Specialists don't re-delegate
    verbose=True
)

crew = Crew(
    agents=[manager, researcher, writer],
    tasks=[project_task],
    process=Process.hierarchical,
    manager_llm="gpt-4o",  # Manager coordinates
    verbose=True
)
```

**Flow Persistence with @persist Decorator:**
```python
from crewai.flow.flow import Flow, listen, start
from crewai.flow.persistence import persist
from pydantic import BaseModel

class CounterState(BaseModel):
    value: int = 0

@persist()  # Apply to entire flow class
class PersistentCounterFlow(Flow[CounterState]):
    @start()
    def increment(self):
        self.state.value += 1
        return self.state.value

    @listen(increment)  # Listen for upstream completion
    def double(self, value):
        self.state.value = value * 2
        return self.state.value

# State persists across runs
flow1 = PersistentCounterFlow()
result1 = flow1.kickoff()

flow2 = PersistentCounterFlow()
result2 = flow2.kickoff()  # Resumes from persisted state
```

**Prevention of Delegation Loops:**
```python
# Clear hierarchy prevents infinite delegation
manager = Agent(role="Manager", allow_delegation=True)
specialist1 = Agent(role="Specialist A", allow_delegation=False)
specialist2 = Agent(role="Specialist B", allow_delegation=False)
```

#### 4.2.5 AutoGen Group Chat Pattern

AutoGen implements a group chat pattern where agents share a common message thread.

**GroupChatManager - Central Coordinator:**
```python
class GroupChatManager(RoutedAgent):
    def __init__(self, participant_topic_types, model_client, participant_descriptions):
        super().__init__("Group chat manager")
        self._participant_topic_types = participant_topic_types
        self._model_client = model_client
        self._chat_history = []

    @message_handler
    async def handle_message(self, message: GroupChatMessage, ctx: MessageContext):
        self._chat_history.append(message.body)

        # LLM selects next speaker based on conversation
        history = self._format_history()
        roles = self._format_roles()

        completion = await self._model_client.create([
            SystemMessage(content=f"Select next role from {self._participant_topic_types}")
        ])

        # Publish RequestToSpeak to selected agent
        selected_topic = self._select_from_completion(completion)
        await self.publish_message(
            RequestToSpeak(),
            DefaultTopicId(type=selected_topic)
        )
```

**Agent Waiting for Turn:**
```python
class BaseGroupChatAgent(RoutedAgent):
    @message_handler
    async def handle_request_to_speak(self, message: RequestToSpeak, ctx: MessageContext):
        # Agent only acts when it receives RequestToSpeak
        self._chat_history.append(
            UserMessage(content=f"Transferred to {self.id.type}", source="system")
        )

        completion = await self._model_client.create(
            [self._system_message] + self._chat_history
        )

        # Publish response back to group chat
        await self.publish_message(
            GroupChatMessage(body=UserMessage(content=completion.content)),
            topic_id=DefaultTopicId(type=self._group_chat_topic_type)
        )
```

#### 4.2.6 Temporal Workflows for Durable Execution

Temporal provides industrial-strength workflow orchestration with signals for inter-agent communication.

**Wait Conditions for Synchronization:**
```python
from temporalio import workflow

@workflow.defn
class GreetingWorkflow:
    def __init__(self):
        self.approved_for_release = False
        self.approver_name = None

    @workflow.signal
    def approve(self, input: ApproveInput):
        self.approved_for_release = True
        self.approver_name = input.name

    @workflow.run
    async def run(self):
        # Block until signal received
        await workflow.wait_condition(lambda: self.approved_for_release)
        return f"Approved by {self.approver_name}"
```

**Child Workflows for Agent Hierarchies:**
```python
@workflow.defn
class ParentWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        # Start child and wait for completion
        return await workflow.execute_child_workflow(
            ChildWorkflow.run,
            ComposeInput("Hello", name),
            id="child-workflow-id",
        )
```

**TypeScript - Workflow Handles for Signaling:**
```typescript
import { startChild } from '@temporalio/workflow';

export async function parentWorkflow(names: string[]) {
  const childHandle = await startChild(childWorkflow, { args: [name] });

  // Signal child workflow
  await childHandle.signal('anySignal');

  // Wait for result
  const result = childHandle.result();
}
```

### 4.3 WHERE: Scope and Boundaries

| Pattern | Scope | Best Suited For |
|---------|-------|-----------------|
| Blackboard | In-memory or persisted shared state | Dynamic collaboration, unknown task decomposition |
| Event Sourcing | Database/stream | Auditability, replay, recovery |
| LangGraph Supervisor | Graph execution with checkpoints | Hierarchical control, state persistence |
| CrewAI Hierarchical | Crew-based orchestration | Role-based delegation, team metaphor |
| AutoGen Group Chat | Pub/sub message passing | Multi-agent conversations |
| Temporal | Durable execution platform | Long-running, fault-tolerant workflows |
| Redis Streams | Message queue | Real-time, lightweight pipelines |
| Kafka | Enterprise event streaming | High-throughput, distributed systems |

### 4.4 WHEN: Timeline and Evolution

| Year | Development | Significance |
|------|-------------|--------------|
| 1985 | Hayes-Roth Blackboard Architecture | Original AI problem-solving paradigm |
| 2020 | Event Sourcing for microservices maturity | Foundation for agent systems |
| 2023 | LangGraph 0.x release | Graph-based agent orchestration |
| 2024 | CrewAI emergence | Role-based agent crews |
| 2024 | AutoGen 0.2 | Microsoft multi-agent framework |
| 2025 | LbMAS research (ArXiv) | Blackboard revival for LLMs |
| 2025 | Event-driven agent patterns (Confluent) | Four canonical patterns identified |
| 2025-2026 | Production adoption | Enterprise-grade implementations |

### 4.5 WHY: Problem Solved and Trade-offs

#### 4.5.1 Problems Solved

1. **Blackboard Pattern:**
   - Solves: Rigid coordinator bottleneck
   - Enables: Agent self-selection based on capability
   - Result: 13-57% improvement, fewer tokens

2. **Event Sourcing:**
   - Solves: Non-deterministic agent auditability
   - Enables: Replay, recovery, debugging
   - Result: Full traceability of AI decisions

3. **Supervisor Hierarchies (LangGraph):**
   - Solves: Complex multi-agent coordination
   - Enables: Hierarchical control with state persistence
   - Result: Scalable team-of-teams architecture

4. **Persistence Decorators (CrewAI):**
   - Solves: State loss across sessions
   - Enables: Automatic state persistence
   - Result: Resumable long-running workflows

5. **Wait Conditions (Temporal):**
   - Solves: Blocking on external signals
   - Enables: Durable awaiting of human/agent approval
   - Result: Human-in-the-loop workflows

#### 4.5.2 Trade-offs

| Pattern | Pros | Cons |
|---------|------|------|
| Blackboard | Flexible, self-organizing | Requires agent capability awareness |
| Event Sourcing | Full auditability | Storage overhead, complexity |
| LangGraph | Python-native, checkpointing | Learning curve for graph model |
| CrewAI | Simple role metaphor | Less flexible than raw orchestration |
| AutoGen | Rich conversation model | Microsoft-centric ecosystem |
| Temporal | Production-grade durability | Infrastructure overhead |

### 4.6 HOW: Implementation Details

#### 4.6.1 File-Based Signal Pattern

For repository-persisted triggers in ECW-style systems:

```python
import json
import hashlib
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class AgentSignal:
    source_agent: str
    target_agent: str
    signal_type: str  # READY, COMPLETE, ERROR, REQUEST
    payload: dict
    timestamp: str
    signature: str  # Hash for integrity

class FileBasedSignalBus:
    def __init__(self, signal_dir: Path):
        self.signal_dir = signal_dir
        self.signal_dir.mkdir(parents=True, exist_ok=True)

    def emit(self, signal: AgentSignal) -> Path:
        """Write signal to file for persistence"""
        signal_file = self.signal_dir / f"{signal.source_agent}-to-{signal.target_agent}-{signal.timestamp}.json"
        signal_file.write_text(json.dumps(signal.__dict__, indent=2))
        return signal_file

    def poll(self, target_agent: str) -> list[AgentSignal]:
        """Check for signals addressed to target agent"""
        signals = []
        for signal_file in self.signal_dir.glob(f"*-to-{target_agent}-*.json"):
            data = json.loads(signal_file.read_text())
            signals.append(AgentSignal(**data))
        return signals

    def acknowledge(self, signal_file: Path):
        """Move signal to processed directory"""
        processed_dir = self.signal_dir / "processed"
        processed_dir.mkdir(exist_ok=True)
        signal_file.rename(processed_dir / signal_file.name)
```

#### 4.6.2 Database-Persisted Blackboard

```python
import sqlite3
from datetime import datetime

class SQLiteBlackboard:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS blackboard_entries (
                id INTEGER PRIMARY KEY,
                entry_type TEXT NOT NULL,
                content TEXT NOT NULL,
                posted_by TEXT NOT NULL,
                claimed_by TEXT,
                status TEXT DEFAULT 'OPEN',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def post(self, entry_type: str, content: str, agent_id: str) -> int:
        """Post entry to blackboard for any capable agent to claim"""
        now = datetime.utcnow().isoformat()
        cursor = self.conn.execute(
            "INSERT INTO blackboard_entries (entry_type, content, posted_by, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (entry_type, content, agent_id, now, now)
        )
        self.conn.commit()
        return cursor.lastrowid

    def claim(self, entry_id: int, agent_id: str) -> bool:
        """Agent claims an entry if capable and entry is unclaimed"""
        cursor = self.conn.execute(
            "UPDATE blackboard_entries SET claimed_by = ?, status = 'CLAIMED', updated_at = ? WHERE id = ? AND claimed_by IS NULL",
            (agent_id, datetime.utcnow().isoformat(), entry_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def watch(self, entry_types: list[str]) -> list[dict]:
        """Watch for entries matching agent capabilities"""
        placeholders = ','.join('?' * len(entry_types))
        cursor = self.conn.execute(
            f"SELECT * FROM blackboard_entries WHERE entry_type IN ({placeholders}) AND status = 'OPEN'",
            entry_types
        )
        return [dict(zip([d[0] for d in cursor.description], row)) for row in cursor.fetchall()]
```

#### 4.6.3 Futures/Promises Pattern for Agent Blocking

```python
import asyncio
from dataclasses import dataclass
from typing import TypeVar, Generic, Callable, Awaitable

T = TypeVar('T')

@dataclass
class AgentFuture(Generic[T]):
    """Future representing pending agent result"""
    agent_id: str
    task_id: str
    _result: T | None = None
    _error: Exception | None = None
    _completed: bool = False
    _event: asyncio.Event = None

    def __post_init__(self):
        self._event = asyncio.Event()

    def set_result(self, result: T):
        self._result = result
        self._completed = True
        self._event.set()

    def set_error(self, error: Exception):
        self._error = error
        self._completed = True
        self._event.set()

    async def wait(self, timeout: float | None = None) -> T:
        """Block until result available"""
        await asyncio.wait_for(self._event.wait(), timeout)
        if self._error:
            raise self._error
        return self._result

class AgentOrchestrator:
    def __init__(self):
        self.pending_futures: dict[str, AgentFuture] = {}

    async def dispatch_and_wait(self, upstream_agent: str, task: dict) -> any:
        """Dispatch task to upstream agent and block until complete"""
        task_id = f"{upstream_agent}-{id(task)}"
        future = AgentFuture(agent_id=upstream_agent, task_id=task_id)
        self.pending_futures[task_id] = future

        # Dispatch task (implementation varies)
        await self._dispatch_to_agent(upstream_agent, task, task_id)

        # Block until upstream completes
        return await future.wait(timeout=300.0)

    def complete_task(self, task_id: str, result: any):
        """Called by upstream agent when task completes"""
        if task_id in self.pending_futures:
            self.pending_futures[task_id].set_result(result)
            del self.pending_futures[task_id]
```

#### 4.6.4 Claude Agent SDK Session Management

```python
from claude_sdk import ClaudeSDKClient

# Session creation and resumption
async def session_workflow():
    client = ClaudeSDKClient()

    # Start new session
    session = await client.create_session()
    session_id = session.id

    # First query
    result1 = await session.query("Research topic X")

    # Resume session later (even in different process)
    resumed = await client.resume_session(session_id)

    # Continue from where we left off
    result2 = await resumed.query("Continue with topic X")

    # Fork session for exploration
    forked = await client.fork_session(session_id)
    result3 = await forked.query("Try alternative approach")

# Best practices for state management
class SessionManager:
    def __init__(self, persistence_path: str):
        self.persistence_path = Path(persistence_path)
        self.session_map: dict[str, str] = {}

    def checkpoint(self, workflow_id: str, state: dict):
        """Persist state for session recovery"""
        checkpoint_file = self.persistence_path / f"{workflow_id}.json"
        checkpoint_file.write_text(json.dumps({
            "workflow_id": workflow_id,
            "state": state,
            "timestamp": datetime.utcnow().isoformat()
        }))

    def recover(self, workflow_id: str) -> dict | None:
        """Recover state after crash/restart"""
        checkpoint_file = self.persistence_path / f"{workflow_id}.json"
        if checkpoint_file.exists():
            return json.loads(checkpoint_file.read_text())["state"]
        return None
```

---

## 5. Analysis

### 5.1 Pattern Comparison Matrix

| Pattern | Persistence | Blocking Support | Audit Trail | Complexity | Best For |
|---------|-------------|------------------|-------------|------------|----------|
| Blackboard | Optional (DB/File) | Poll-based | Limited | Medium | Dynamic collaboration |
| Event Sourcing | Required (Event Store) | Event replay | Full | High | Compliance, debugging |
| LangGraph Supervisor | Checkpointer | Command routing | Checkpoint history | Medium | Hierarchical control |
| CrewAI @persist | SQLite default | @listen decorator | Flow state | Low | Simple crews |
| AutoGen Group Chat | Memory | RequestToSpeak | Chat history | Medium | Conversations |
| Temporal | Durable execution | wait_condition | Full workflow | High | Enterprise, long-running |
| Redis Streams | Redis | Consumer groups | Stream replay | Medium | Real-time pipelines |

### 5.2 Applicability to ECW Context

For the ECW (Evolving Claude Workflow) system, the following patterns are most applicable:

1. **File-Based Blackboard:** Aligns with ECW's file-centric approach (CLAUDE.md, proposals, knowledge)
2. **Database-Persisted Signals:** Could use SQLite (already used by PS skill) for agent coordination
3. **Event Sourcing for PS Entities:** PS events could trigger downstream agents
4. **Checkpoint-Based State:** Memory Keeper already provides checkpointing

### 5.3 Recommended Approach for ECW

```
┌─────────────────────────────────────────────────────────────────────┐
│                     ECW AGENT ORCHESTRATION                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────┐    Events    ┌──────────────────┐             │
│  │  PS Skill        │──────────────▶│  Event Store     │             │
│  │  (Producer)      │              │  (SQLite)        │             │
│  └──────────────────┘              └────────┬─────────┘             │
│                                             │                        │
│                           ┌─────────────────┼─────────────────┐     │
│                           ▼                 ▼                 ▼     │
│               ┌──────────────────┐ ┌──────────────────┐ ┌─────────┐│
│               │  ps-researcher   │ │  ps-planner      │ │  ps-... ││
│               │  (Consumer)      │ │  (Consumer)      │ │         ││
│               └──────────────────┘ └──────────────────┘ └─────────┘│
│                                                                      │
│  Signal Bus: File-based (.ecw/signals/) or DB (ps_events table)     │
│  Blocking: Poll + await or workflow.wait_condition                   │
│  Audit: Full event sourcing with replay capability                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 6. Conclusions

1. **Blackboard Architecture** has proven highly effective for LLM multi-agent systems, offering a compelling alternative to rigid coordinator patterns. The shift from assigned tasks to self-selected tasks based on capability reduces bottlenecks and enables more flexible collaboration.

2. **Event Sourcing** is essential for production AI agent systems due to the non-deterministic nature of LLM decisions. The ability to replay, audit, and recover from any point in time is critical for enterprise adoption.

3. **Framework Patterns Converge:** Despite different APIs, LangGraph (Supervisor/Command), CrewAI (Hierarchical/@listen), and AutoGen (GroupChatManager/RequestToSpeak) all implement variations of the same core patterns: central coordination, capability-based routing, and state persistence.

4. **Temporal-Style Signals** provide the most robust blocking mechanism for downstream agents waiting on upstream results, with industrial-strength durability guarantees.

5. **Redis Streams** offer a lightweight alternative to Kafka for agent-to-agent communication in smaller deployments, with built-in persistence and consumer groups.

---

## 7. Recommendations

### 7.1 For ECW PS Agent Portfolio

| Recommendation | Priority | Rationale |
|----------------|----------|-----------|
| R-001: Implement file-based signal bus | HIGH | Aligns with ECW file-centric approach |
| R-002: Add event sourcing to PS skill | HIGH | Enables agent triggering from PS events |
| R-003: Create agent wait/poll primitives | MEDIUM | Enables downstream blocking |
| R-004: Consider LangGraph for complex orchestration | MEDIUM | Production-grade, well-documented |
| R-005: Evaluate Temporal for long-running workflows | LOW | Enterprise-grade but infrastructure overhead |

### 7.2 Implementation Priority

1. **Phase 1:** File-based signal bus (`.ecw/signals/`)
2. **Phase 2:** PS event emission for agent triggers
3. **Phase 3:** Agent wait/poll primitives
4. **Phase 4:** Evaluate orchestration framework adoption

---

## 8. Knowledge Items Generated

### 8.1 Patterns Identified

| ID | Pattern Name | Description |
|----|--------------|-------------|
| PAT-TBD-1 | Blackboard Agent Selection | Agents self-select tasks based on capability rather than coordinator assignment |
| PAT-TBD-2 | Event-Sourced Agent Audit | Immutable event log enables replay and auditability of agent decisions |
| PAT-TBD-3 | File-Based Signal Bus | Repository-persisted signals for agent-to-agent communication |
| PAT-TBD-4 | Hierarchical Supervisor Trees | Multi-level supervisors managing agent teams |
| PAT-TBD-5 | Wait Condition Blocking | Downstream agents block until upstream signals completion |

### 8.2 Lessons Learned

| ID | Lesson | Source |
|----|--------|--------|
| LES-TBD-1 | Blackboard outperforms master-slave by 13-57% for LLM agents | ArXiv LbMAS 2025 |
| LES-TBD-2 | Event sourcing is essential for non-deterministic AI auditability | Akka.io, Confluent |
| LES-TBD-3 | Framework patterns converge despite API differences | LangGraph/CrewAI/AutoGen analysis |

### 8.3 Assumptions Made

| ID | Assumption | Confidence | Impact if Wrong |
|----|------------|------------|-----------------|
| ASM-TBD-1 | ECW agents can access shared filesystem | HIGH | Would need database-based signals |
| ASM-TBD-2 | SQLite sufficient for event store | MEDIUM | May need PostgreSQL for scale |
| ASM-TBD-3 | File-based signals are atomic enough | MEDIUM | May need locking or queue |

---

## 9. PS Integration

### 9.1 Entry Status

| Field | Value |
|-------|-------|
| **Entry ID** | e-130 |
| **Status** | Done |
| **Type** | RESEARCH |
| **Severity** | MEDIUM |
| **Created** | 2026-01-04 |
| **Session** | ps-researcher agent |

### 9.2 Related Entities

- **Questions:** q-TBD (agent triggering patterns)
- **Constraints:** c-009 (artifact persistence), c-010 (artifact linking)
- **Knowledge:** PAT-048 (Three-Tier Enforcement), LES-030 (Evidence-based claims)

---

## 10. Sources with URLs

### 10.1 Primary Sources (Context7 MCP)

1. **LangGraph Official Documentation** - `/llmstxt/langchain-ai_github_io_langgraph_llms-full_txt`
   - Supervisor architecture, Command routing, Checkpointers
   - [LangGraph GitHub](https://github.com/langchain-ai/langgraph)

2. **CrewAI Official Documentation** - `/crewaiinc/crewai`
   - Hierarchical Process, @persist decorator, Agent delegation
   - [CrewAI GitHub](https://github.com/crewaiinc/crewai)

3. **AutoGen Official Documentation** - `/websites/microsoft_github_io_autogen_stable`
   - Group Chat pattern, GroupChatManager, RequestToSpeak
   - [AutoGen GitHub](https://github.com/microsoft/autogen)

4. **Temporal Documentation** - `/temporalio/documentation`
   - Workflow signals, wait_condition, child workflows
   - [Temporal GitHub](https://github.com/temporalio/documentation)

### 10.2 Web Sources

5. **[Exploring Advanced LLM Multi-Agent Systems Based on Blackboard Architecture](https://arxiv.org/html/2507.01701v1)** - ArXiv 2025
   - LbMAS research, blackboard architecture for LLMs

6. **[LLM-based Multi-Agent Blackboard System for Information Discovery](https://arxiv.org/html/2510.01285)** - ArXiv 2025
   - Performance results: 13-57% improvement

7. **[Building Intelligent Multi-Agent Systems with MCPs and the Blackboard Pattern](https://medium.com/@dp2580/building-intelligent-multi-agent-systems-with-mcps-and-the-blackboard-pattern-to-build-systems-a454705d5672)** - Medium 2025
   - MCP integration with blackboard

8. **[Four Design Patterns for Event-Driven Multi-Agent Systems](https://www.confluent.io/blog/event-driven-multi-agent-systems/)** - Confluent 2025
   - Orchestrator-worker, hierarchical, blackboard, market-based

9. **[Event Sourcing: The Backbone of Agentic AI](https://akka.io/blog/event-sourcing-the-backbone-of-agentic-ai)** - Akka.io 2025
   - Why event sourcing for AI agents

10. **[The Future of AI Agents is Event-Driven](https://www.confluent.io/blog/the-future-of-ai-agents-is-event-driven/)** - Confluent 2025
    - EDA for agent systems, immutable log

11. **[Event-Driven Agent Coordination with KurrentDB](https://www.kurrent.io/blog/event-driven-agent-coordination-with-kurrentdb/)** - KurrentDB 2025
    - Database as coordination mechanism

12. **[Open-Source AI Agent Stack 2025: Complete Enterprise Guide](https://futureagi.com/blogs/open-source-stack-ai-agents-2025)** - FutureAGI 2025
    - Redis patterns, orchestration layer

13. **[Claude Agent SDK Best Practices](https://skywork.ai/blog/claude-agent-sdk-best-practices-ai-agents-2025/)** - Skywork.ai 2025
    - Session management, state persistence

14. **[Session Management - Claude Docs](https://platform.claude.com/docs/en/agent-sdk/sessions)** - Anthropic 2025
    - Official session handling documentation

15. **[Blackboard system - Wikipedia](https://en.wikipedia.org/wiki/Blackboard_system)** - Wikipedia
    - Original Hayes-Roth architecture reference

---

## 11. Validation Status (Soft Enforcement)

| Category | Status | Notes |
|----------|--------|-------|
| W-DIMENSION COVERAGE | 6/6 | All dimensions addressed |
| FRAMEWORK APPLICATION | 4/5 | 5W1H, patterns, mechanisms documented |
| EVIDENCE & GAPS | 4/4 | Sources cited, assumptions logged |
| OUTPUT SECTIONS | 4/4 | All sections complete |

**Quality Status:** COMPLETE (18/19 criteria met)

---

## 12. Appendix: Quick Reference

### A. Pattern Selection Guide

| If You Need... | Use This Pattern |
|----------------|------------------|
| Dynamic task assignment | Blackboard |
| Full audit trail | Event Sourcing |
| Hierarchical control | LangGraph Supervisor |
| Simple role-based crews | CrewAI Hierarchical |
| Multi-agent conversations | AutoGen Group Chat |
| Durable long-running workflows | Temporal |
| Lightweight real-time pipelines | Redis Streams |
| Enterprise event streaming | Kafka |

### B. Framework Feature Matrix

| Feature | LangGraph | CrewAI | AutoGen | Temporal |
|---------|-----------|--------|---------|----------|
| State Persistence | Checkpointer | @persist | Memory | Durable |
| Hierarchical | Supervisor | Process.hierarchical | Nested | Child Workflows |
| Blocking Wait | Command routing | @listen | RequestToSpeak | wait_condition |
| Python-native | Yes | Yes | Yes | Yes |
| Production-ready | Yes | Yes | Yes | Yes |
