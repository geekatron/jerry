---
ps: phase-38.17
exploration: e-156
created: 2026-01-04
status: RESEARCH
agent: ps-researcher
title: CLI-Blackboard Integration Architecture for Automatic Sub-Agent Dispatch
---

# CLI-Blackboard Integration Architecture for Automatic Sub-Agent Dispatch

> **Research ID:** e-156
> **Phase:** 38.17
> **Agent:** ps-researcher
> **Created:** 2026-01-04
> **Status:** COMPLETE

---

## 1. Executive Summary

This research investigates how to properly wire the PS CLI `add-entry` command to `BlackboardService.post_signal` for automatic sub-agent dispatch. The investigation covers three critical areas: (1) hexagonal architecture boundary integrity between CLI adapters and domain services, (2) hook-based versus direct integration patterns with analysis of process boundary constraints, and (3) MCP context access limitations from CLI subprocesses.

**Key Findings:**

1. **Direct Integration Pattern is Architecturally Sound:** The CLI adapter can invoke `BlackboardService.post_signal` through the existing factory composition root without violating hexagonal boundaries, as both are primary adapters orchestrated by the same composition root.

2. **Hook-Based Integration is Architecturally Infeasible:** Per LES-030, hooks run as subprocesses and cannot access MCP context or in-memory service instances. Any hook-based triggering would require file-based signaling with SessionStart synchronization.

3. **CLI-to-Service Communication Must Be In-Process:** The CLI runs as a subprocess of Claude Code and cannot access the main context's MCP or memory services. However, it CAN create its own service instances through the factory pattern for database-persisted operations.

4. **Event Publishing Enables Decoupled Dispatch:** The existing `IEventPublisher` infrastructure supports synchronous event delivery to registered subscribers, enabling sub-agent dispatch without tight coupling.

**Recommendation:** Implement direct integration through the factory composition root, where CLI creates a `BlackboardService` instance and calls `post_signal` after `add_entry`. Event sourcing persists the signal, and a registered subscriber triggers sub-agent invocation.

---

## 2. Research Questions

| # | Question | Status | Answer Summary |
|---|----------|--------|----------------|
| 1 | How should CLI `add-entry` connect to `BlackboardService.post_signal`? | DECIDED | Factory creates BlackboardService, CLI calls directly |
| 2 | Does hook-based integration respect hexagonal boundaries? | DECIDED | No - hooks lack MCP/service access (LES-030) |
| 3 | Can CLI subprocess access blackboard domain services? | DECIDED | Yes - via factory.py composition root |
| 4 | What triggers sub-agent invocation after signal posted? | DECIDED | IEventPublisher delivers to registered subscriber |

---

## 3. Methodology

### 3.1 Codebase Analysis

Examined the following key files:

| File | Purpose | Relevance |
|------|---------|-----------|
| `.claude/skills/problem-statement/scripts/cli.py` | CLI entry point | Shows current add-entry implementation |
| `.claude/skills/problem-statement/scripts/factory.py` | Composition root | Shows hexagonal wiring pattern |
| `.claude/lib/ecw/domain/blackboard/blackboard_aggregate.py` | Blackboard domain | Shows post_signal signature |
| `.claude/lib/ecw/application/services/blackboard_repository.py` | Repository impl | Shows event persistence |
| `.claude/lib/ecw/application/ports/secondary/event_publisher.py` | Event publisher port | Shows subscriber pattern |
| `sidequests/evolving-claude-workflow/docs/knowledge/hook-mcp-limitation.md` | LES-030 | Critical constraint documentation |

### 3.2 Architecture Documents Reviewed

- Blackboard Agent Orchestration Design (e-140)
- Alternative Agent Triggering Patterns Research (e-130)
- Hook MCP Limitation (LES-030)

### 3.3 Patterns Searched

```bash
# CLI add-entry implementation
grep "add-entry|add_entry" .claude/skills/problem-statement/

# BlackboardService usage
grep "post_signal" .claude/lib/

# Event publisher pattern
grep "IEventPublisher|EventPublisher" .claude/lib/
```

---

## 4. Findings: W-Dimension Coverage

### 4.1 WHO: Actors and Components

| Actor | Role | Process Boundary |
|-------|------|------------------|
| **Claude Main Context** | Orchestrates workflows, has MCP access | Claude Code process |
| **CLI Subprocess** | Executes `python cli.py add-entry ...` | Spawned subprocess |
| **Hook Subprocess** | Runs on lifecycle events | Spawned subprocess |
| **PS Skill** | Manages problem statement operations | Main context |
| **Sub-agents** | ps-researcher, ps-analyst, etc. | Spawned via Task tool |
| **Event Publisher** | Delivers events to subscribers | In-process |

**Process Boundary Diagram:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     CLAUDE CODE PROCESS                                   │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    MAIN CONTEXT                                   │    │
│  │                                                                   │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │    │
│  │  │ MCP Access  │  │ Memory      │  │ Tool Invocation         │  │    │
│  │  │ ✅ Available │  │ Keeper ✅   │  │ (Bash, Read, etc.) ✅   │  │    │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘  │    │
│  │                                                                   │    │
│  │  Can call: context_save(), mcp__* tools, Task tool               │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                      │                                    │
│                                      │ spawns                             │
│                                      ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    CLI SUBPROCESS                                 │    │
│  │                                                                   │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │    │
│  │  │ MCP Access  │  │ Memory      │  │ Factory Access          │  │    │
│  │  │ ❌ NO       │  │ Keeper ❌   │  │ ✅ Can create services  │  │    │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘  │    │
│  │                                                                   │    │
│  │  Can: Read/write files, access SQLite, create own services       │    │
│  │  Cannot: Call MCP tools, access main context memory              │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    HOOK SUBPROCESS (LES-030)                      │    │
│  │                                                                   │    │
│  │  MCP Access: ❌ NO    Memory Keeper: ❌ NO    Services: ✅ Yes    │    │
│  │                                                                   │    │
│  │  Can: Read/write files, execute shell, access databases          │    │
│  │  Cannot: Call MCP tools, access main context, invoke Task tool   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 WHAT: Architectural Mechanisms

#### 4.2.1 Current CLI `add-entry` Flow

The existing `cmd_add_entry` function in `cli.py` (lines 84-135):

```python
def cmd_add_entry(cli, args):
    """Add exploration entry to PS (c-006: MUST be classified at creation)."""
    try:
        kbrefs = args.kbrefs.split(",") if hasattr(args, 'kbrefs') and args.kbrefs else []
        result = cli.add_exploration(args.phase_id, args.text, kbrefs)

        # Extract entry ID from result
        entry_id = None
        if "Added exploration" in result:
            parts = result.split()
            entry_id = parts[-1] if parts else None

        # ... classification logic ...
```

**Key Observation:** The CLI calls `cli.add_exploration()` which is a method on `ProblemStatementCLI`, itself wired to `ProblemStatementService` via factory.

#### 4.2.2 Factory Composition Root Pattern

The `factory.py` (lines 90-104) shows how CLI is wired:

```python
def create_cli(config: Optional[StorageConfig] = None) -> ProblemStatementCLI:
    """Create a configured ProblemStatementCLI adapter."""
    service = create_service(config)
    return ProblemStatementCLI(
        command_handler=service,
        query_handler=service,
    )
```

**Key Insight:** Factory pattern allows CLI to create its own service instances. This same pattern can wire `BlackboardService`.

#### 4.2.3 BlackboardAggregate.post_signal Signature

From `blackboard_aggregate.py` (lines 167-238):

```python
def post_signal(
    self,
    signal_type: SignalType,
    ps_id: str,
    entry_id: str,
    topic: str,
    target_capabilities: List[AgentCapabilityType],
    description: Optional[str] = None,
    timeout_seconds: int = 300,
    context: Optional[Dict[str, Any]] = None,
) -> str:
    """Post a new signal to the blackboard."""
```

**Required Parameters:**
- `signal_type`: Maps from entry type (RESEARCH, ANALYSIS, etc.)
- `ps_id`: Phase ID from CLI args
- `entry_id`: Returned from `add_exploration`
- `topic`: From entry text
- `target_capabilities`: Derived from entry type

#### 4.2.4 Event Publisher for Sub-Agent Dispatch

From `event_publisher.py`:

```python
class IEventPublisher(ABC):
    @abstractmethod
    def register(self, subscriber: IEventSubscriber) -> None:
        """Register a subscriber to receive events."""

    @abstractmethod
    def publish(self, event: CloudEvent) -> None:
        """Publish event to all registered subscribers."""
```

**Dispatch Mechanism:** When `BlackboardRepository.save()` is called, it publishes events to registered subscribers:

```python
# From blackboard_repository.py lines 280-283
if self.event_publisher:
    for cloud_event in cloud_events:
        self.event_publisher.publish(cloud_event)
```

### 4.3 WHERE: Hexagonal Architecture Boundaries

#### 4.3.1 Layer Responsibilities

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       HEXAGONAL ARCHITECTURE                              │
│                    CLI → Blackboard Integration                           │
└─────────────────────────────────────────────────────────────────────────┘

                         PRIMARY ADAPTERS (Driving)
                              ┌──────────────────┐
                              │    PS CLI        │
                              │  (cli.py)        │
                              │                  │
                              │  cmd_add_entry() │◄─── Entry point
                              └────────┬─────────┘
                                       │
                         ┌─────────────┴─────────────┐
                         │                           │
                         ▼                           ▼
              ┌──────────────────┐        ┌──────────────────┐
              │ PSService        │        │ BlackboardService│
              │ (add_exploration)│        │ (post_signal)    │
              └────────┬─────────┘        └────────┬─────────┘
                       │                           │
    ┌──────────────────┼───────────────────────────┼──────────────────────┐
    │                  │                           │                       │
    │                  ▼                           ▼                       │
    │        ┌─────────────────────────────────────────────────┐          │
    │        │                                                  │          │
    │        │               DOMAIN CORE                        │          │
    │        │                                                  │          │
    │        │  ProblemStatementAggregate  BlackboardAggregate  │          │
    │        │  AgentSignal                Domain Events        │          │
    │        │                                                  │          │
    │        └─────────────────────────────────────────────────┘          │
    │                                  │                                   │
    │         ┌────────────────────────┼────────────────────────┐          │
    │         │                        │                        │          │
    │         ▼                        ▼                        ▼          │
    │  ┌────────────────┐     ┌────────────────┐     ┌────────────────┐   │
    │  │ IEventStore    │     │ IBlackboardRepo│     │ IEventPublisher│   │
    │  │ (secondary)    │     │ (secondary)    │     │ (secondary)    │   │
    │  └───────┬────────┘     └───────┬────────┘     └───────┬────────┘   │
    │          │                      │                      │            │
    └──────────┼──────────────────────┼──────────────────────┼────────────┘
               │                      │                      │
               ▼                      ▼                      ▼
    ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐
    │  SQLite3EventStore │  │  BlackboardRepo    │  │  EventPublisher    │
    │  (adapter)         │  │  (adapter)         │  │  (adapter)         │
    └────────────────────┘  └────────────────────┘  └────────────────────┘

                         SECONDARY ADAPTERS (Driven)
```

#### 4.3.2 Boundary Compliance Analysis

| Integration Point | Boundary Crossed? | Compliance | Notes |
|-------------------|-------------------|------------|-------|
| CLI → PSService | Primary → Application | ✅ Valid | Standard adapter pattern |
| CLI → BlackboardService | Primary → Application | ✅ Valid | Same pattern, needs factory wiring |
| PSService → BlackboardService | Application → Application | ⚠️ Careful | Should go through domain events |
| Hook → BlackboardService | Primary → Application | ✅ Valid | But MCP limitation applies (LES-030) |
| EventPublisher → Subscriber | Secondary → Primary | ✅ Valid | Callback inversion pattern |

### 4.4 WHEN: Execution Timeline

#### 4.4.1 Current Flow (Without Blackboard Integration)

```
Timeline: CLI add-entry (no blackboard)
───────────────────────────────────────────────────────────────────────────

User                  Claude               CLI Subprocess      Database
  │                     │                       │                  │
  │ "add-entry phase-38.17 'Research X'"        │                  │
  │────────────────────▶│                       │                  │
  │                     │                       │                  │
  │                     │ Bash: python cli.py   │                  │
  │                     │────────────────────────▶                 │
  │                     │                       │                  │
  │                     │                       │ add_exploration()│
  │                     │                       │─────────────────▶│
  │                     │                       │                  │
  │                     │                       │◀─────────────────│
  │                     │                       │ entry_id: e-156  │
  │                     │                       │                  │
  │                     │◀────────────────────────                 │
  │                     │ "✅ Added exploration e-156"             │
  │                     │                       │                  │
  │◀────────────────────│                       │                  │
  │                     │                       │                  │
  │ END (no sub-agent)  │                       │                  │
```

#### 4.4.2 Proposed Flow (With Blackboard Integration)

```
Timeline: CLI add-entry with blackboard signal
───────────────────────────────────────────────────────────────────────────

User                  Claude               CLI Subprocess      Blackboard       Subscriber
  │                     │                       │                  │                │
  │ "add-entry --type RESEARCH 'Research X'"   │                  │                │
  │────────────────────▶│                       │                  │                │
  │                     │                       │                  │                │
  │                     │ Bash: python cli.py   │                  │                │
  │                     │────────────────────────▶                 │                │
  │                     │                       │                  │                │
  │                     │                       │ add_exploration()│                │
  │                     │                       │─────────────────▶│                │
  │                     │                       │                  │                │
  │                     │                       │◀─────────────────│                │
  │                     │                       │ entry_id: e-156  │                │
  │                     │                       │                  │                │
  │                     │                       │ post_signal()    │                │
  │                     │                       │─────────────────▶│                │
  │                     │                       │                  │                │
  │                     │                       │                  │ publish event  │
  │                     │                       │                  │───────────────▶│
  │                     │                       │                  │                │
  │                     │                       │                  │                │ on_event()
  │                     │                       │                  │                │ (dispatch)
  │                     │                       │                  │◀───────────────│
  │                     │                       │                  │                │
  │                     │                       │◀─────────────────│                │
  │                     │                       │ signal_id: sig-xx│                │
  │                     │                       │                  │                │
  │                     │◀────────────────────────                 │                │
  │                     │ "✅ Added exploration e-156"             │                │
  │                     │ "📢 Posted signal sig-xx"                │                │
  │                     │                       │                  │                │
  │◀────────────────────│                       │                  │                │
```

### 4.5 WHY: Problem Solved and Trade-offs

#### 4.5.1 Problems Addressed

1. **Manual Sub-Agent Invocation:** Currently, sub-agents must be explicitly invoked after entry creation. Automatic dispatch eliminates this manual step.

2. **Decoupled Agent Coordination:** Using events rather than direct calls allows agents to be added/removed without modifying CLI code.

3. **Audit Trail:** Event sourcing captures every signal for replay and debugging.

4. **Capability-Based Selection:** Blackboard pattern enables agent self-selection based on capability matching.

#### 4.5.2 Trade-off Analysis

| Approach | Pros | Cons |
|----------|------|------|
| **Direct Integration (Recommended)** | Simple, in-process, immediate | CLI code grows, must handle errors |
| **Hook-Based Integration** | Decoupled, lifecycle-aware | MCP limitation (LES-030), async complexity |
| **File-Based Signaling** | Works across processes | Polling overhead, eventual consistency |
| **Message Queue (Redis)** | Production-grade, durable | Infrastructure overhead |

### 4.6 HOW: Implementation Approach

#### 4.6.1 Option A: Direct Factory Integration (RECOMMENDED)

**Approach:** Extend `factory.py` to create `BlackboardService`, then call from CLI after entry creation.

**Step 1: Extend factory.py**

```python
# In factory.py
from ecw.application.services.blackboard_repository import BlackboardRepository
from ecw.infrastructure.adapters.secondary.messaging.event_publisher import EventPublisher

def create_blackboard_service(
    config: Optional[StorageConfig] = None
) -> BlackboardService:
    """Create configured BlackboardService with event publishing."""
    event_store, _ = get_configured_stores(config)
    event_publisher = EventPublisher()

    # Register sub-agent dispatcher as subscriber
    dispatcher = SubAgentDispatcher()
    event_publisher.register(dispatcher)

    repository = BlackboardRepository(
        event_store=event_store,
        event_publisher=event_publisher,
        sidequest="ecw"
    )

    return BlackboardService(repository)
```

**Step 2: Modify cmd_add_entry**

```python
# In cli.py cmd_add_entry
def cmd_add_entry(cli, args):
    # ... existing entry creation ...

    # Post signal if entry type warrants agent processing
    if has_type and args.entry_type in AGENT_ENTRY_TYPES:
        from factory import create_blackboard_service

        blackboard = create_blackboard_service()
        signal_id = blackboard.post_signal(
            signal_type=map_entry_type_to_signal(args.entry_type),
            ps_id=args.phase_id,
            entry_id=entry_id,
            topic=args.text,
            target_capabilities=get_capabilities_for_type(args.entry_type),
        )
        print(f"📢 Posted signal {signal_id}")
```

**Step 3: Implement SubAgentDispatcher**

```python
class SubAgentDispatcher(IEventSubscriber):
    """Dispatches sub-agents based on blackboard signals."""

    @property
    def subscriber_id(self) -> str:
        return "sub-agent-dispatcher"

    def on_event(self, event: CloudEvent) -> None:
        if event['type'] == 'ecw.blackboard.AgentSignalPosted':
            # Write signal file for main context to pick up
            signal_data = event.data
            signal_file = Path(f".ecw/signals/pending/{signal_data['signal_id']}.json")
            signal_file.parent.mkdir(parents=True, exist_ok=True)
            signal_file.write_text(json.dumps(signal_data, indent=2))
```

#### 4.6.2 Option B: Hook-Based Integration (NOT RECOMMENDED)

Due to LES-030, hooks cannot:
- Access MCP context
- Call in-memory services directly
- Trigger Task tool

**Workaround (Complex):**
1. Hook writes signal request to `.ecw/signals/pending/`
2. SessionStart reads pending signals
3. Main context invokes Task tool for sub-agent

**Why Not Recommended:** Adds latency (waits for SessionStart), complexity, and loses immediacy.

#### 4.6.3 Option C: File-Based Polling (ALTERNATIVE)

For scenarios where CLI and main context are truly isolated:

```python
# CLI writes signal file
def write_signal_request(signal_data: dict):
    signal_file = Path(f".ecw/signals/requests/{uuid4()}.json")
    signal_file.write_text(json.dumps(signal_data))

# Main context polls for signals (in SessionStart or periodic)
def process_pending_signals():
    for signal_file in Path(".ecw/signals/requests/").glob("*.json"):
        signal = json.loads(signal_file.read_text())
        # Invoke sub-agent via Task tool
        invoke_sub_agent(signal)
        signal_file.rename(signal_file.parent / "processed" / signal_file.name)
```

---

## 5. Analysis

### 5.1 Architectural Boundary Validation

| Question | Answer | Evidence |
|----------|--------|----------|
| Does CLI violate hexagonal boundaries by calling BlackboardService? | NO | CLI is a primary adapter; BlackboardService is application layer. Same pattern as PSService. |
| Can CLI subprocess create BlackboardService instance? | YES | Factory pattern provides composition root. CLI already creates PSService this way. |
| Does event publishing cross boundaries incorrectly? | NO | EventPublisher is a secondary port. Subscriber callback is inversion of control. |
| Is domain logic leaking into CLI? | RISK | Entry-type-to-capability mapping should be in domain or application layer. |

### 5.2 MCP Context Limitation Impact

| Operation | CLI Subprocess | Main Context |
|-----------|---------------|--------------|
| Write to SQLite (events) | ✅ Can do | ✅ Can do |
| Read from SQLite | ✅ Can do | ✅ Can do |
| Call Memory Keeper | ❌ Cannot | ✅ Can do |
| Invoke Task tool | ❌ Cannot | ✅ Can do |
| Write to filesystem | ✅ Can do | ✅ Can do |

**Critical Insight:** CLI can post signals to database (via BlackboardService), but cannot directly invoke sub-agents (which requires Task tool in main context).

### 5.3 Sub-Agent Dispatch Mechanism

**Problem:** CLI cannot call Task tool to spawn sub-agents.

**Solution:** Use file-based signal bridge:

1. CLI posts signal to database (event-sourced)
2. Event publisher writes signal file to `.ecw/signals/pending/`
3. Main context checks pending signals (on next turn or SessionStart)
4. Main context invokes Task tool with signal data

```
┌────────────┐     ┌────────────────┐     ┌──────────────┐     ┌────────────┐
│ CLI        │     │ BlackboardSvc  │     │ Pending File │     │ Main Ctx   │
│ Subprocess │────▶│ post_signal()  │────▶│ .ecw/signals │────▶│ Task tool  │
└────────────┘     └────────────────┘     └──────────────┘     └────────────┘
                         │                                           │
                         │ Event Store                               │
                         ▼                                           ▼
                  ┌────────────────┐                         ┌────────────┐
                  │ SQLite Events  │                         │ Sub-Agent  │
                  │ (Audit Trail)  │                         │ Execution  │
                  └────────────────┘                         └────────────┘
```

---

## 6. Conclusions

### 6.1 Key Insights

1. **Direct Integration is Correct Approach:** The CLI-to-BlackboardService integration follows the same hexagonal pattern as CLI-to-PSService. No architectural violations occur.

2. **LES-030 Constraint is Critical:** Hook-based integration is architecturally infeasible for triggering MCP-dependent operations. File-based bridging is the workaround.

3. **Event Sourcing Provides Foundation:** The existing event store and publisher infrastructure enables decoupled sub-agent dispatch without new infrastructure.

4. **Two-Phase Dispatch Required:** Phase 1 (CLI) posts signal to database; Phase 2 (Main Context) processes pending signals and invokes sub-agents.

5. **Capability Mapping Belongs in Domain:** Entry type → agent capability mapping should be domain logic, not CLI logic.

### 6.2 Implications

- CLI code changes are minimal (add BlackboardService wiring)
- Signal files enable cross-process communication
- Event sourcing provides full audit trail
- Pattern is extensible to new agent types

---

## 7. Recommendations

| Priority | Recommendation | Rationale | Effort |
|----------|---------------|-----------|--------|
| HIGH | R-001: Implement direct factory integration | Follows existing patterns, minimal code changes | Small |
| HIGH | R-002: Use file-based signal bridge for sub-agent dispatch | Works around MCP limitation (LES-030) | Small |
| MEDIUM | R-003: Move capability mapping to domain layer | Maintain hexagonal boundary integrity | Medium |
| MEDIUM | R-004: Add signal processing to SessionStart hook | Enables automatic sub-agent dispatch on session start | Small |
| LOW | R-005: Consider Redis for production signal queue | Better durability and throughput for scale | Large |

### 7.1 Implementation Phases

**Phase 1: Factory Wiring (Immediate)**
- Add `create_blackboard_service()` to factory.py
- Implement entry-type-to-capability mapping
- Wire BlackboardService into CLI

**Phase 2: Signal Bridge (Next)**
- Implement SubAgentDispatcher subscriber
- Write pending signal files on event publish
- Add signal processing to SessionStart

**Phase 3: Main Context Processing (Following)**
- Main context reads pending signals
- Invokes Task tool with signal data
- Marks signals as processed

---

## 8. Knowledge Items Generated

### 8.1 Patterns Identified

| ID | Pattern Name | Description |
|----|--------------|-------------|
| PAT-073 | File-Based Signal Bridge | Use filesystem as IPC mechanism between CLI subprocess and main context |
| PAT-074 | Factory-Wired Cross-Service Integration | Composition root wires multiple services for CLI adapter |
| PAT-075 | Two-Phase Sub-Agent Dispatch | CLI posts signal, main context processes and dispatches |

### 8.2 Lessons Learned

| ID | Lesson | Source |
|----|--------|--------|
| LES-062 | CLI subprocess can create service instances via factory but cannot invoke Task tool | Codebase analysis |
| LES-063 | Event publishing in subprocess writes to database but subscriber callbacks are in-process only | Architecture analysis |

### 8.3 Assumptions Made

| ID | Assumption | Confidence | Impact if Wrong |
|----|------------|------------|-----------------|
| ASM-090 | CLI subprocess and main context share SQLite database access | HIGH | Would need separate database or IPC |
| ASM-091 | File-based signal bridge has acceptable latency for sub-agent dispatch | MEDIUM | May need Redis/queue for real-time |
| ASM-092 | Main context will process pending signals on next turn or SessionStart | MEDIUM | May need explicit polling mechanism |

---

## 9. PS Integration

| Action | Command | Status |
|--------|---------|--------|
| Exploration Entry | `add-entry phase-38.17 "CLI-Blackboard Integration Architecture"` | Done |
| Entry Type | `set-entry-type phase-38.17 e-156 RESEARCH` | Done |
| Artifact Link | `link-artifact phase-38.17 e-156 FILE "docs/research/phase-38.17-e-156-cli-blackboard-integration-architecture.md"` | Pending |
| Knowledge Refs | `add-knowledge phase-38.17 PAT-073,PAT-074,PAT-075` | Pending |

---

## 10. Sources

| # | Source | Type | Relevance | Accessed |
|---|--------|------|-----------|----------|
| 1 | `.claude/skills/problem-statement/scripts/cli.py` | Code | HIGH | 2026-01-04 |
| 2 | `.claude/skills/problem-statement/scripts/factory.py` | Code | HIGH | 2026-01-04 |
| 3 | `.claude/lib/ecw/domain/blackboard/blackboard_aggregate.py` | Code | HIGH | 2026-01-04 |
| 4 | `.claude/lib/ecw/application/services/blackboard_repository.py` | Code | HIGH | 2026-01-04 |
| 5 | `.claude/lib/ecw/application/ports/secondary/event_publisher.py` | Code | HIGH | 2026-01-04 |
| 6 | `.claude/lib/ecw/infrastructure/adapters/secondary/messaging/event_publisher.py` | Code | MEDIUM | 2026-01-04 |
| 7 | `sidequests/evolving-claude-workflow/docs/knowledge/hook-mcp-limitation.md` (LES-030) | Doc | CRITICAL | 2026-01-04 |
| 8 | `sidequests/evolving-claude-workflow/docs/proposals/phase-38/design/phase-38.17/blackboard-agent-orchestration-design.md` (e-140) | Doc | HIGH | 2026-01-04 |
| 9 | `sidequests/evolving-claude-workflow/docs/research/phase-38.17-e-130-alternative-agent-triggering-patterns.md` (e-130) | Doc | HIGH | 2026-01-04 |
| 10 | `.claude/docs/hooks.md` | Doc | MEDIUM | 2026-01-04 |

---

## 11. Validation Status (Soft Enforcement)

| Category | Status | Notes |
|----------|--------|-------|
| W-DIMENSION COVERAGE | 6/6 | WHO, WHAT, WHERE, WHEN, WHY, HOW all addressed |
| FRAMEWORK APPLICATION | 5/5 | 5W1H, architecture analysis, process boundary analysis |
| EVIDENCE & GAPS | 4/4 | Code citations, assumptions logged, unknowns stated |
| OUTPUT SECTIONS | 4/4 | All required sections present |

**Quality Status:** COMPLETE (19/19 criteria met)

---

## 12. Appendix: Quick Reference

### A. Integration Decision Tree

```
CLI add-entry with --type flag
         │
         ▼
    Entry type in AGENT_ENTRY_TYPES?
         │
    ┌────┴────┐
   YES       NO
    │         │
    ▼         ▼
Post signal  Done
to blackboard
    │
    ▼
Event published
    │
    ▼
Signal file written to .ecw/signals/pending/
    │
    ▼
Main context processes (on next turn or SessionStart)
    │
    ▼
Task tool invokes sub-agent
```

### B. Entry Type to Capability Mapping

| Entry Type | Signal Type | Target Capability |
|------------|-------------|-------------------|
| RESEARCH | RESEARCH | RESEARCH |
| ANALYSIS | ANALYSIS | ANALYSIS |
| REVIEW | REVIEW | REVIEW |
| DECISION | DECISION | DECISION |
| INVESTIGATION | INVESTIGATION | INVESTIGATION |
| SYNTHESIS | SYNTHESIS | SYNTHESIS |

### C. File-Based Signal Format

```json
{
  "signal_id": "sig-a1b2c3d4",
  "signal_type": "RESEARCH",
  "ps_id": "phase-38.17",
  "entry_id": "e-156",
  "topic": "CLI-Blackboard Integration Architecture",
  "target_capabilities": ["RESEARCH"],
  "created_at": "2026-01-04T10:30:00Z",
  "status": "PENDING"
}
```

---

**Generated by:** ps-researcher agent
**Template Version:** 1.0 (Phase 38.16.7)
