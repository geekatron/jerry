---
ps: phase-38.17
exploration: e-140
created: 2026-01-04
status: DESIGN
type: SOP-DES ARTIFACT
version: 1.0
---

# Blackboard Agent Orchestration Design

> **Phase:** 38.17
> **Exploration:** e-140
> **Status:** DESIGN
> **SOP Compliance:** SOP-DES.6 (All Design Artifacts)

---

## 1. Executive Summary

This document defines the detailed design for sub-agent orchestration and communication using Blackboard Architecture integrated with ECW's Event Sourcing infrastructure. The design follows ECW Clean Architecture principles: DDD, Hexagonal Architecture, CQRS, Repository Pattern, and Dispatcher Pattern.

**Key Design Decisions:**
- **q-033:** Separate BlackboardAggregate from ProblemStatementAggregate
- **q-034:** Capability-based agent self-selection (PAT-070)
- **q-035:** Agent capabilities defined in agent .md frontmatter
- **q-036:** Dedicated AgentSignalPosted event (PAT-072)
- **q-037:** Event subscription with IEventSubscriber callback

**Research Foundation:** e-130 Alternative Agent Triggering Patterns (ArXiv LbMAS 2025, Confluent, Akka.io)

---

## 2. Use Cases (SOP-DES.6.a)

### UC-001: Post Agent Signal

**Actor:** PS Skill / Main Claude Context
**Precondition:** Exploration entry created with type requiring agent processing
**Postcondition:** AgentSignal posted to blackboard, matching agents notified

**Main Flow:**
1. PS Skill creates exploration entry (e.g., type=RESEARCH)
2. PS Skill determines agent requirement from entry type
3. PS Skill calls BlackboardService.post_signal(signal)
4. BlackboardAggregate emits AgentSignalPosted event
5. Event dispatcher notifies registered subscribers
6. Matching agents evaluate capability fit

### UC-002: Claim Agent Signal

**Actor:** Agent (ps-researcher, ps-analyst, etc.)
**Precondition:** AgentSignalPosted event received, agent has matching capability
**Postcondition:** Signal claimed by agent, status updated to CLAIMED

**Main Flow:**
1. Agent receives AgentSignalPosted via IEventSubscriber
2. Agent evaluates capability match (capability_score > threshold)
3. Agent calls BlackboardService.claim_signal(signal_id, agent_id)
4. BlackboardAggregate verifies signal unclaimed (optimistic locking)
5. BlackboardAggregate emits AgentSignalClaimed event
6. Agent begins processing task

### UC-003: Complete Agent Task

**Actor:** Agent (ps-researcher, ps-analyst, etc.)
**Precondition:** Signal claimed, agent processing complete
**Postcondition:** Signal marked complete, artifact linked to PS

**Main Flow:**
1. Agent creates artifact (research doc, analysis, etc.)
2. Agent calls link-artifact to connect artifact to PS entry
3. Agent calls BlackboardService.complete_signal(signal_id, result)
4. BlackboardAggregate emits AgentSignalCompleted event
5. Downstream agents notified of completion (blocking release)

### UC-004: Watch for Agent Signals

**Actor:** Agent waiting for upstream completion
**Precondition:** Downstream agent registered for signal type
**Postcondition:** Agent notified when matching signal completes

**Main Flow:**
1. Agent registers interest via BlackboardService.watch(signal_types)
2. When AgentSignalCompleted fires for matching type, agent notified
3. Agent retrieves signal result
4. Agent proceeds with dependent processing

---

## 3. Use Case Diagram (SOP-DES.6.b)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      BLACKBOARD AGENT ORCHESTRATION                          │
│                              Use Case Diagram                                │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────────────────────┐
                    │         <<System>>                  │
                    │    Blackboard Subsystem             │
                    │                                     │
    ┌───────┐       │  ┌─────────────────────────────┐   │       ┌───────────┐
    │       │       │  │                             │   │       │           │
    │  PS   │───────┼──│    UC-001: Post Signal      │   │       │ Agent     │
    │ Skill │       │  │                             │   │       │ (Worker)  │
    │       │       │  └─────────────────────────────┘   │       │           │
    └───────┘       │              │                     │       └─────┬─────┘
                    │              ▼                     │             │
                    │  ┌─────────────────────────────┐   │             │
                    │  │                             │───┼─────────────┘
                    │  │   UC-002: Claim Signal      │   │
                    │  │                             │   │
                    │  └─────────────────────────────┘   │
                    │              │                     │
                    │              ▼                     │
                    │  ┌─────────────────────────────┐   │       ┌───────────┐
                    │  │                             │   │       │           │
                    │  │  UC-003: Complete Task      │───┼───────│ Downstream│
                    │  │                             │   │       │   Agent   │
                    │  └─────────────────────────────┘   │       │           │
                    │              │                     │       └─────┬─────┘
                    │              ▼                     │             │
                    │  ┌─────────────────────────────┐   │             │
                    │  │                             │───┼─────────────┘
                    │  │   UC-004: Watch Signals     │   │
                    │  │                             │   │
                    │  └─────────────────────────────┘   │
                    │                                     │
                    └─────────────────────────────────────┘
```

---

## 4. Class Diagram (SOP-DES.6.c)

### 4.1 Domain Layer

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DOMAIN LAYER                                       │
│                    (No Infrastructure Dependencies)                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│      BlackboardAggregate        │     │       AgentSignal               │
├─────────────────────────────────┤     │       <<Entity>>                │
│ - id: BlackboardId              │     ├─────────────────────────────────┤
│ - signals: List[AgentSignal]    │     │ - signal_id: SignalId           │
│ - version: int                  │     │ - signal_type: SignalType       │
│ - uncommitted_events: List      │     │ - payload: SignalPayload        │
├─────────────────────────────────┤     │ - target_capabilities: List[Cap]│
│ + post_signal(signal)           │     │ - posted_by: AgentId            │
│ + claim_signal(id, agent_id)    │     │ - claimed_by: Optional[AgentId] │
│ + complete_signal(id, result)   │     │ - status: SignalStatus          │
│ + watch(signal_types)           │     │ - created_at: datetime          │
│ + apply(event)                  │     │ - completed_at: Optional[dt]    │
└─────────────────────────────────┘     │ - result: Optional[SignalResult]│
              │                          └─────────────────────────────────┘
              │ emits
              ▼
┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│     AgentSignalPosted           │     │      SignalPayload              │
│     <<Domain Event>>            │     │      <<Value Object>>           │
├─────────────────────────────────┤     ├─────────────────────────────────┤
│ - event_id: str                 │     │ - ps_id: str                    │
│ - aggregate_id: BlackboardId    │     │ - entry_id: str                 │
│ - signal_id: SignalId           │     │ - topic: str                    │
│ - signal_type: SignalType       │     │ - prompt: str                   │
│ - payload: SignalPayload        │     │ - context: dict                 │
│ - target_capabilities: List     │     └─────────────────────────────────┘
│ - timestamp: datetime           │
└─────────────────────────────────┘     ┌─────────────────────────────────┐
                                        │      AgentCapability            │
┌─────────────────────────────────┐     │      <<Value Object>>           │
│     AgentSignalClaimed          │     ├─────────────────────────────────┤
│     <<Domain Event>>            │     │ - capability_type: str          │
├─────────────────────────────────┤     │ - capability_score: float       │
│ - signal_id: SignalId           │     │ + matches(signal_type): bool    │
│ - claimed_by: AgentId           │     │ + score(signal): float          │
│ - claimed_at: datetime          │     └─────────────────────────────────┘
└─────────────────────────────────┘
                                        ┌─────────────────────────────────┐
┌─────────────────────────────────┐     │      SignalStatus               │
│     AgentSignalCompleted        │     │      <<Enumeration>>            │
│     <<Domain Event>>            │     ├─────────────────────────────────┤
├─────────────────────────────────┤     │ POSTED                          │
│ - signal_id: SignalId           │     │ CLAIMED                         │
│ - completed_by: AgentId         │     │ COMPLETED                       │
│ - result: SignalResult          │     │ FAILED                          │
│ - completed_at: datetime        │     │ EXPIRED                         │
└─────────────────────────────────┘     └─────────────────────────────────┘
```

### 4.2 Application Layer (Ports)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         APPLICATION LAYER                                    │
│                    (Use Cases and Port Interfaces)                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│   IBlackboardRepository         │     │   IAgentRegistry                │
│   <<Port - Secondary>>          │     │   <<Port - Secondary>>          │
├─────────────────────────────────┤     ├─────────────────────────────────┤
│ + get(id: BlackboardId)         │     │ + register(agent: AgentDef)     │
│ + save(agg: BlackboardAggregate)│     │ + get_by_capability(cap): List  │
│ + find_by_signal_id(id): Agg    │     │ + get_all(): List[AgentDef]     │
└─────────────────────────────────┘     └─────────────────────────────────┘

┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│   IBlackboardEventPublisher     │     │   BlackboardService             │
│   <<Port - Secondary>>          │     │   <<Application Service>>       │
├─────────────────────────────────┤     ├─────────────────────────────────┤
│ + publish(event: DomainEvent)   │     │ - repository: IBlackboardRepo   │
│ + subscribe(handler)            │     │ - publisher: IEventPublisher    │
└─────────────────────────────────┘     │ - registry: IAgentRegistry      │
                                        ├─────────────────────────────────┤
┌─────────────────────────────────┐     │ + post_signal(request)          │
│   PostSignalUseCase             │     │ + claim_signal(signal_id, agent)│
│   <<Use Case>>                  │     │ + complete_signal(id, result)   │
├─────────────────────────────────┤     │ + watch(signal_types)           │
│ - service: BlackboardService    │     └─────────────────────────────────┘
├─────────────────────────────────┤
│ + execute(request): Result      │
└─────────────────────────────────┘
```

### 4.3 Infrastructure Layer (Adapters)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       INFRASTRUCTURE LAYER                                   │
│                    (Adapter Implementations)                                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│   SQLiteBlackboardRepository    │     │   FileBasedAgentRegistry        │
│   <<Adapter - Secondary>>       │     │   <<Adapter - Secondary>>       │
├─────────────────────────────────┤     ├─────────────────────────────────┤
│ implements IBlackboardRepository│     │ implements IAgentRegistry       │
│                                 │     │                                 │
│ - event_store: IEventStore      │     │ - agents_dir: Path              │
│ - projection: BlackboardProj    │     │ - capability_cache: dict        │
├─────────────────────────────────┤     ├─────────────────────────────────┤
│ + get(id): BlackboardAggregate  │     │ + register(agent): void         │
│ + save(agg): void               │     │ + get_by_capability(cap): List  │
│ + find_by_signal_id(id): Agg    │     │ + _parse_agent_md(path): Def    │
└─────────────────────────────────┘     └─────────────────────────────────┘

┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│   EventStorePublisher           │     │   BlackboardProjection          │
│   <<Adapter - Secondary>>       │     │   <<Projection>>                │
├─────────────────────────────────┤     ├─────────────────────────────────┤
│ implements IEventPublisher      │     │ - conn: sqlite3.Connection      │
│                                 │     ├─────────────────────────────────┤
│ - event_store: IEventStore      │     │ + on_signal_posted(event)       │
│ - subscribers: List[Callable]   │     │ + on_signal_claimed(event)      │
├─────────────────────────────────┤     │ + on_signal_completed(event)    │
│ + publish(event): void          │     │ + get_open_signals(): List      │
│ + subscribe(handler): void      │     │ + get_by_capability(cap): List  │
└─────────────────────────────────┘     └─────────────────────────────────┘
```

---

## 5. Component Diagram (SOP-DES.6.d)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         COMPONENT DIAGRAM                                    │
│               Blackboard Agent Orchestration System                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              <<Component>>                                   │
│                           PS Skill Component                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  SKILL.md                                                           │   │
│  │  - Orchestration instructions                                       │   │
│  │  - Trigger phrase detection                                         │   │
│  │  - Task tool invocation                                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    │ posts signal                            │
│                                    ▼                                         │
└────────────────────────────────────┼─────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              <<Component>>                                   │
│                        Blackboard Domain Component                           │
│  ┌────────────────────────┐    ┌────────────────────────┐                   │
│  │  BlackboardAggregate   │    │  AgentSignal Entity    │                   │
│  │  - Domain logic        │    │  - Signal state        │                   │
│  │  - Event emission      │    │  - Capability matching │                   │
│  └────────────────────────┘    └────────────────────────┘                   │
│                                                                              │
│  ┌────────────────────────┐    ┌────────────────────────┐                   │
│  │  Domain Events         │    │  Value Objects         │                   │
│  │  - AgentSignalPosted   │    │  - SignalPayload       │                   │
│  │  - AgentSignalClaimed  │    │  - AgentCapability     │                   │
│  │  - AgentSignalCompleted│    │  - SignalResult        │                   │
│  └────────────────────────┘    └────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                    ▼                ▼                ▼
┌──────────────────────────┐ ┌──────────────────────────┐ ┌──────────────────┐
│    <<Component>>         │ │    <<Component>>         │ │   <<Component>>  │
│  Application Services    │ │  Ports (Interfaces)      │ │   Use Cases      │
│  ┌────────────────────┐  │ │  ┌────────────────────┐  │ │ ┌──────────────┐ │
│  │ BlackboardService  │  │ │  │IBlackboardRepository│  │ │ │PostSignal   │ │
│  │ - Orchestration    │  │ │  │IAgentRegistry      │  │ │ │ClaimSignal  │ │
│  │ - Coordination     │  │ │  │IEventPublisher     │  │ │ │CompleteTask │ │
│  └────────────────────┘  │ │  └────────────────────┘  │ │ │WatchSignals │ │
└──────────────────────────┘ └──────────────────────────┘ │ └──────────────┘ │
                                     │                     └──────────────────┘
                    ┌────────────────┼────────────────┐
                    │                │                │
                    ▼                ▼                ▼
┌──────────────────────────┐ ┌──────────────────────────┐ ┌──────────────────┐
│    <<Component>>         │ │    <<Component>>         │ │   <<Component>>  │
│  SQLite Adapter          │ │  File-Based Registry     │ │  Event Publisher │
│  ┌────────────────────┐  │ │  ┌────────────────────┐  │ │ ┌──────────────┐ │
│  │ Repository Impl    │  │ │  │ Agent .md Parser   │  │ │ │EventStore   │ │
│  │ Projection         │  │ │  │ Capability Cache   │  │ │ │Integration  │ │
│  └────────────────────┘  │ │  └────────────────────┘  │ │ └──────────────┘ │
└──────────────────────────┘ └──────────────────────────┘ └──────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              <<Component>>                                   │
│                         Agent Worker Components                              │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌──────────────┐  │
│  │ ps-researcher  │ │ ps-analyst     │ │ ps-reviewer    │ │ ps-architect │  │
│  │ - RESEARCH     │ │ - ANALYSIS     │ │ - REVIEW       │ │ - DECISION   │  │
│  │ - Subscribes   │ │ - Subscribes   │ │ - Subscribes   │ │ - Subscribes │  │
│  └────────────────┘ └────────────────┘ └────────────────┘ └──────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Sequence Diagrams (SOP-DES.6.i)

### 6.1 Post and Claim Signal Flow

```
┌──────────┐   ┌──────────────────┐   ┌──────────────────┐   ┌────────────────┐   ┌────────────┐
│ PS Skill │   │ BlackboardService│   │BlackboardAggregate│   │ EventPublisher │   │ ps-researcher│
└────┬─────┘   └────────┬─────────┘   └────────┬─────────┘   └───────┬────────┘   └──────┬─────┘
     │                  │                      │                     │                   │
     │ post_signal(req) │                      │                     │                   │
     │─────────────────>│                      │                     │                   │
     │                  │                      │                     │                   │
     │                  │ post_signal(signal)  │                     │                   │
     │                  │─────────────────────>│                     │                   │
     │                  │                      │                     │                   │
     │                  │                      │ emit AgentSignalPosted                  │
     │                  │                      │────────────────────>│                   │
     │                  │                      │                     │                   │
     │                  │                      │                     │ notify(event)     │
     │                  │                      │                     │──────────────────>│
     │                  │                      │                     │                   │
     │                  │                      │                     │  evaluate         │
     │                  │                      │                     │  capability       │
     │                  │                      │                     │<─ ─ ─ ─ ─ ─ ─ ─ ─│
     │                  │                      │                     │                   │
     │                  │ claim_signal(id, agent)                    │                   │
     │                  │<───────────────────────────────────────────────────────────────│
     │                  │                      │                     │                   │
     │                  │ claim_signal()       │                     │                   │
     │                  │─────────────────────>│                     │                   │
     │                  │                      │                     │                   │
     │                  │                      │ emit AgentSignalClaimed                 │
     │                  │                      │────────────────────>│                   │
     │                  │                      │                     │                   │
     │  Result(claimed) │                      │                     │                   │
     │<─────────────────│                      │                     │                   │
     │                  │                      │                     │                   │
```

### 6.2 Downstream Blocking Flow

```
┌──────────────┐   ┌──────────────────┐   ┌──────────────────┐   ┌────────────────┐
│ps-researcher │   │ BlackboardService│   │ EventPublisher   │   │ ps-reviewer    │
└──────┬───────┘   └────────┬─────────┘   └────────┬─────────┘   └───────┬────────┘
       │                    │                      │                     │
       │                    │                      │  watch([RESEARCH])  │
       │                    │                      │<────────────────────│
       │                    │                      │                     │
       │ ... processing ... │                      │                     │
       │                    │                      │     (blocking)      │
       │                    │                      │                     │
       │ complete_signal()  │                      │                     │
       │───────────────────>│                      │                     │
       │                    │                      │                     │
       │                    │ emit AgentSignalCompleted                  │
       │                    │─────────────────────>│                     │
       │                    │                      │                     │
       │                    │                      │ notify(completed)   │
       │                    │                      │────────────────────>│
       │                    │                      │                     │
       │                    │                      │  unblock            │
       │                    │                      │  get_result()       │
       │                    │                      │<────────────────────│
       │                    │                      │                     │
       │                    │                      │  Result(artifact)   │
       │                    │                      │────────────────────>│
       │                    │                      │                     │
       │                    │                      │  proceed with       │
       │                    │                      │  downstream work    │
       │                    │                      │                     │
```

---

## 7. State Machine Diagram (SOP-DES.6.h)

### 7.1 AgentSignal State Machine

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     AgentSignal State Machine                                │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌───────────────┐
                              │               │
                              │   INITIAL     │
                              │               │
                              └───────┬───────┘
                                      │
                              post_signal()
                                      │
                                      ▼
                              ┌───────────────┐
                         ┌────│               │────┐
                         │    │    POSTED     │    │
                         │    │               │    │
                         │    └───────┬───────┘    │
                         │            │            │
                   timeout()    claim_signal()   no_capable_agent()
                         │            │            │
                         ▼            ▼            ▼
               ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
               │               │ │               │ │               │
               │   EXPIRED     │ │   CLAIMED     │ │   UNCLAIMED   │
               │               │ │               │ │               │
               └───────────────┘ └───────┬───────┘ └───────────────┘
                                         │
                         ┌───────────────┼───────────────┐
                         │               │               │
                   complete_signal()  fail_signal()  timeout()
                         │               │               │
                         ▼               ▼               ▼
               ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
               │               │ │               │ │               │
               │  COMPLETED    │ │    FAILED     │ │   EXPIRED     │
               │               │ │               │ │               │
               └───────────────┘ └───────────────┘ └───────────────┘

Transitions:
- INITIAL → POSTED: post_signal() called
- POSTED → CLAIMED: claim_signal() by capable agent
- POSTED → EXPIRED: No claim within timeout (default 30s)
- POSTED → UNCLAIMED: No capable agent found
- CLAIMED → COMPLETED: Agent completes processing
- CLAIMED → FAILED: Agent encounters error
- CLAIMED → EXPIRED: Agent times out (default 5min)
```

---

## 8. Activity Diagram (SOP-DES.6.g)

### 8.1 Signal Processing Activity

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Signal Processing Activity Diagram                       │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌───────────────┐
                              │    START      │
                              └───────┬───────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │ PS creates    │
                              │ exploration   │
                              │ entry         │
                              └───────┬───────┘
                                      │
                                      ▼
                            ◆─────────────────◆
                           ╱                   ╲
                          ╱  Entry requires     ╲
                         ╱   agent processing?   ╲
                          ╲                     ╱
                           ╲                   ╱
                            ◆────────┬────────◆
                                     │
                         ┌───────────┴───────────┐
                         │                       │
                    [Yes]│                       │[No]
                         ▼                       ▼
              ┌───────────────────┐     ┌───────────────┐
              │ Determine required│     │     END       │
              │ capabilities      │     │ (no agent)    │
              └─────────┬─────────┘     └───────────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Post AgentSignal  │
              │ to blackboard     │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Emit AgentSignal  │
              │ Posted event      │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Notify registered │
              │ agent subscribers │
              └─────────┬─────────┘
                        │
                        ▼
                ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
                │  FOR EACH Agent          │
                │                          │
                │  ┌───────────────────┐   │
                │  │ Evaluate          │   │
                │  │ capability match  │   │
                │  └─────────┬─────────┘   │
                │            │             │
                │            ▼             │
                │  ◆─────────────────◆     │
                │ ╱                   ╲    │
                │╱  capability_score   ╲   │
                │╲  > threshold?       ╱   │
                │ ╲                   ╱    │
                │  ◆────────┬────────◆     │
                │           │              │
                │  ┌────────┴────────┐     │
                │  │                 │     │
                │  │[Yes]            │[No] │
                │  ▼                 ▼     │
                │ ┌─────────┐  ┌─────────┐ │
                │ │ Attempt │  │ Skip    │ │
                │ │ claim   │  │ agent   │ │
                │ └────┬────┘  └─────────┘ │
                │      │                   │
                └ ─ ─ ─│─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
                       │
                       ▼
              ◆─────────────────◆
             ╱                   ╲
            ╱  Claim successful?  ╲
            ╲                     ╱
             ╲                   ╱
              ◆────────┬────────◆
                       │
           ┌───────────┴───────────┐
           │                       │
      [Yes]│                       │[No - already claimed]
           ▼                       ▼
  ┌───────────────────┐   ┌───────────────┐
  │ Agent processes   │   │ Wait for next │
  │ task              │   │ signal        │
  └─────────┬─────────┘   └───────────────┘
            │
            ▼
  ┌───────────────────┐
  │ Create artifact   │
  │ (research doc)    │
  └─────────┬─────────┘
            │
            ▼
  ┌───────────────────┐
  │ Link artifact     │
  │ to PS entry       │
  └─────────┬─────────┘
            │
            ▼
  ┌───────────────────┐
  │ Complete signal   │
  │ with result       │
  └─────────┬─────────┘
            │
            ▼
  ┌───────────────────┐
  │ Emit AgentSignal  │
  │ Completed event   │
  └─────────┬─────────┘
            │
            ▼
  ┌───────────────────┐
  │ Notify downstream │
  │ watchers          │
  └─────────┬─────────┘
            │
            ▼
      ┌───────────────┐
      │     END       │
      └───────────────┘
```

---

## 9. Network Contracts (SOP-DES.6.k)

### 9.1 JSON Schema for AgentSignal

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://ecw.io/schemas/agent-signal.json",
  "title": "AgentSignal",
  "description": "Signal posted to blackboard for agent coordination",
  "type": "object",
  "properties": {
    "signal_id": {
      "type": "string",
      "pattern": "^sig-[0-9a-f]{8}$",
      "description": "Unique signal identifier"
    },
    "signal_type": {
      "type": "string",
      "enum": ["RESEARCH", "ANALYSIS", "REVIEW", "DECISION", "INVESTIGATION", "SYNTHESIS"],
      "description": "Type of agent work requested"
    },
    "payload": {
      "type": "object",
      "properties": {
        "ps_id": {"type": "string"},
        "entry_id": {"type": "string", "pattern": "^e-[0-9]+$"},
        "topic": {"type": "string", "maxLength": 200},
        "prompt": {"type": "string"},
        "context": {"type": "object"}
      },
      "required": ["ps_id", "entry_id", "topic"]
    },
    "target_capabilities": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 1
    },
    "posted_by": {"type": "string"},
    "claimed_by": {"type": ["string", "null"]},
    "status": {
      "type": "string",
      "enum": ["POSTED", "CLAIMED", "COMPLETED", "FAILED", "EXPIRED"]
    },
    "created_at": {"type": "string", "format": "date-time"},
    "completed_at": {"type": ["string", "null"], "format": "date-time"},
    "result": {
      "type": ["object", "null"],
      "properties": {
        "artifact_path": {"type": "string"},
        "knowledge_items": {"type": "array"},
        "error": {"type": ["string", "null"]}
      }
    }
  },
  "required": ["signal_id", "signal_type", "payload", "target_capabilities", "posted_by", "status", "created_at"]
}
```

---

## 10. Hexagonal Architecture Mapping

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      HEXAGONAL ARCHITECTURE                                  │
│                    (Ports and Adapters Pattern)                              │
└─────────────────────────────────────────────────────────────────────────────┘

                         PRIMARY ADAPTERS (Driving)
                              ┌──────────────────┐
                              │    PS Skill      │
                              │  (CLI Adapter)   │
                              └────────┬─────────┘
                                       │
                              ┌────────▼─────────┐
                              │  Primary Port    │
                              │  (Use Cases)     │
                              │                  │
                              │ - PostSignal     │
                              │ - ClaimSignal    │
                              │ - CompleteTask   │
                              │ - WatchSignals   │
                              └────────┬─────────┘
                                       │
    ┌──────────────────────────────────┼──────────────────────────────────┐
    │                                  │                                   │
    │                        ┌─────────▼──────────┐                        │
    │                        │                    │                        │
    │                        │   DOMAIN CORE      │                        │
    │                        │                    │                        │
    │                        │ BlackboardAggregate│                        │
    │                        │ AgentSignal        │                        │
    │                        │ Domain Events      │                        │
    │                        │ Value Objects      │                        │
    │                        │                    │                        │
    │                        └─────────┬──────────┘                        │
    │                                  │                                   │
    │         ┌────────────────────────┼────────────────────────┐          │
    │         │                        │                        │          │
    │         ▼                        ▼                        ▼          │
    │  ┌────────────────┐     ┌────────────────┐     ┌────────────────┐    │
    │  │ Secondary Port │     │ Secondary Port │     │ Secondary Port │    │
    │  │ IBlackboard    │     │ IAgentRegistry │     │ IEventPublisher│    │
    │  │ Repository     │     │                │     │                │    │
    │  └───────┬────────┘     └───────┬────────┘     └───────┬────────┘    │
    │          │                      │                      │             │
    └──────────┼──────────────────────┼──────────────────────┼─────────────┘
               │                      │                      │
               ▼                      ▼                      ▼
    ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐
    │  SQLite Adapter    │  │  File-Based        │  │  EventStore        │
    │  (Repository)      │  │  Registry Adapter  │  │  Publisher Adapter │
    └────────────────────┘  └────────────────────┘  └────────────────────┘

                         SECONDARY ADAPTERS (Driven)
```

---

## 11. Event Sourcing Integration

### 11.1 Event Store Schema

The Blackboard system integrates with existing ECW Event Store:

```sql
-- Uses existing events table structure
-- Adds new event types for blackboard

-- Event types:
-- AgentSignalPosted
-- AgentSignalClaimed
-- AgentSignalCompleted
-- AgentSignalFailed
-- AgentSignalExpired

-- Projection table for read model
CREATE TABLE IF NOT EXISTS blackboard_signals (
    signal_id TEXT PRIMARY KEY,
    signal_type TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    target_capabilities TEXT NOT NULL,  -- JSON array
    posted_by TEXT NOT NULL,
    claimed_by TEXT,
    status TEXT NOT NULL DEFAULT 'POSTED',
    created_at TEXT NOT NULL,
    claimed_at TEXT,
    completed_at TEXT,
    result_json TEXT,
    version INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX idx_signals_status ON blackboard_signals(status);
CREATE INDEX idx_signals_type ON blackboard_signals(signal_type);
CREATE INDEX idx_signals_capabilities ON blackboard_signals(target_capabilities);
```

### 11.2 Event Replay

```python
class BlackboardProjectionRebuilder:
    """Rebuilds blackboard projection from event store."""

    def rebuild(self, event_store: IEventStore) -> None:
        # Clear existing projection
        self._clear_projection()

        # Replay all blackboard events in order
        events = event_store.get_events_by_type([
            "AgentSignalPosted",
            "AgentSignalClaimed",
            "AgentSignalCompleted",
            "AgentSignalFailed",
            "AgentSignalExpired"
        ])

        for event in events:
            self._apply_event(event)
```

---

## 12. CQRS Pattern

### 12.1 Command Side

```python
@dataclass
class PostSignalCommand:
    """Command to post a new agent signal."""
    ps_id: str
    entry_id: str
    signal_type: str
    topic: str
    prompt: str
    target_capabilities: List[str]

@dataclass
class ClaimSignalCommand:
    """Command for agent to claim a signal."""
    signal_id: str
    agent_id: str
    capability_score: float

@dataclass
class CompleteSignalCommand:
    """Command to mark signal as complete."""
    signal_id: str
    agent_id: str
    artifact_path: str
    knowledge_items: List[str]
```

### 12.2 Query Side

```python
@dataclass
class GetOpenSignalsQuery:
    """Query for open signals matching capabilities."""
    capabilities: List[str]
    limit: int = 10

@dataclass
class GetSignalByIdQuery:
    """Query for specific signal."""
    signal_id: str

@dataclass
class WatchSignalsQuery:
    """Query to watch for signal completions."""
    signal_types: List[str]
    since: Optional[datetime] = None
```

---

## 13. Repository Pattern

### 13.1 IBlackboardRepository Interface

```python
from abc import ABC, abstractmethod
from typing import Optional, List

class IBlackboardRepository(ABC):
    """Port interface for blackboard persistence."""

    @abstractmethod
    def get(self, blackboard_id: str) -> Optional[BlackboardAggregate]:
        """Get aggregate by ID."""
        pass

    @abstractmethod
    def save(self, aggregate: BlackboardAggregate) -> None:
        """Save aggregate (append events to event store)."""
        pass

    @abstractmethod
    def find_by_signal_id(self, signal_id: str) -> Optional[BlackboardAggregate]:
        """Find aggregate containing signal."""
        pass

    @abstractmethod
    def get_open_signals(self, capabilities: List[str]) -> List[AgentSignal]:
        """Query open signals matching capabilities (read model)."""
        pass
```

---

## 14. Dispatcher Pattern

### 14.1 Event Dispatcher

```python
class BlackboardEventDispatcher:
    """Dispatches blackboard events to registered handlers."""

    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = defaultdict(list)

    def register(self, event_type: str, handler: Callable) -> None:
        """Register handler for event type."""
        self._handlers[event_type].append(handler)

    def dispatch(self, event: DomainEvent) -> None:
        """Dispatch event to all registered handlers."""
        event_type = type(event).__name__
        for handler in self._handlers[event_type]:
            handler(event)
```

---

## 15. Constraints Compliance Matrix

| Constraint | Design Element | Status |
|------------|----------------|--------|
| c-025 | Uses IEventStore, no new tables except projection | SATISFIED |
| c-026 | Domain defines ports, infrastructure provides adapters | SATISFIED |
| c-027 | Integrates with existing event store | SATISFIED |
| c-028 | Emits AgentSignalPosted, Claimed, Completed events | SATISFIED |
| c-029 | IBlackboardRepository + SQLiteBlackboardRepository | SATISFIED |
| c-015 | Subagents don't spawn subagents (main context orchestrates) | SATISFIED |

---

## 16. Test Strategy

### 16.1 Test Pyramid

| Level | Count | Focus |
|-------|-------|-------|
| Unit | 40+ | Aggregate logic, value objects, events |
| Contract | 15+ | Port interface contracts |
| Integration | 20+ | Repository + EventStore integration |
| Architecture | 10+ | Hexagonal boundary verification |
| E2E | 5+ | Full signal flow with real agents |
| BDD | 25+ | User scenarios per use cases |

### 16.2 BDD Scenarios (Preview)

```gherkin
Feature: Blackboard Agent Orchestration

  Scenario: Post research signal triggers agent
    Given PS skill creates exploration entry with type "RESEARCH"
    When PS skill posts agent signal to blackboard
    Then AgentSignalPosted event should be emitted
    And ps-researcher agent should receive notification

  Scenario: Agent claims matching signal
    Given agent signal posted with capability "RESEARCH"
    And ps-researcher has capability "RESEARCH"
    When ps-researcher evaluates capability match
    Then capability_score should be > 0.8
    And ps-researcher should successfully claim signal
```

---

## 17. PS Integration

| Action | Command | Status |
|--------|---------|--------|
| Design Entry | `add-entry e-140 "DESIGN ARTIFACT..."` | Done |
| Constraints | c-025 through c-029 | Done |
| Questions | q-033 through q-037 | Answered |
| Patterns | PAT-070, PAT-071, PAT-072 | Done |
| Lessons | LES-060, LES-061 | Done |
| Assumptions | ASM-080 | Done |

---

**Generated by:** Claude Opus 4.5 (Distinguished NASA Systems Engineer persona)
**Date:** 2026-01-04
**PS Exploration:** e-140
**Research Foundation:** e-130 (Alternative Agent Triggering Patterns)
