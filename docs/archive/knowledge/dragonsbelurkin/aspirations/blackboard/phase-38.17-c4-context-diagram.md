---
ps: phase-38.17
exploration: e-165
created: 2026-01-04
status: DESIGN
type: SOP-DES ARTIFACT
version: 1.0
---

# Phase 38.17 C4 Context Diagram

> **Phase:** 38.17
> **SOP Compliance:** SOP-DES (Diagrams)
> **Related:** blackboard-agent-orchestration-design.md

---

## 1. C4 Model Overview

The C4 model provides four levels of abstraction for software architecture:
1. **Context** - System in its environment (this document)
2. **Container** - High-level technology choices
3. **Component** - Internal components
4. **Code** - Implementation details

---

## 2. System Context Diagram (Level 1)

### ASCII Representation

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SYSTEM CONTEXT                                      │
│                    Blackboard Agent Orchestration System                         │
└─────────────────────────────────────────────────────────────────────────────────┘

                          ┌─────────────────────┐
                          │       User          │
                          │  (Software Engr)    │
                          │                     │
                          └──────────┬──────────┘
                                     │
                          Manages Problem Statements
                          Creates Exploration Entries
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│                     ┌───────────────────────────────────────┐                    │
│                     │     ECW Blackboard Orchestration      │                    │
│                     │                                       │                    │
│                     │  - Problem Statement Management       │                    │
│                     │  - Sub-Agent Orchestration            │                    │
│                     │  - Signal-based Communication         │                    │
│                     │  - Event Sourced Persistence          │                    │
│                     │                                       │                    │
│                     └───────────────┬───────────────────────┘                    │
│                                     │                                            │
│                                     │                                            │
│      ┌──────────────────────────────┼──────────────────────────────┐            │
│      │                              │                              │            │
│      ▼                              ▼                              ▼            │
│ ┌────────────┐               ┌────────────┐               ┌────────────┐        │
│ │Claude Code │               │  File      │               │ Memory     │        │
│ │   CLI      │               │  System    │               │ Keeper MCP │        │
│ │            │               │            │               │            │        │
│ │ Interactive│               │ .ecw/      │               │ Session    │        │
│ │ Terminal   │               │ events.db  │               │ Context    │        │
│ └────────────┘               └────────────┘               └────────────┘        │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

LEGEND:
┌─────────────────────────────────────────────────────────────────────────────────┐
│  ┌─────────┐                                                                    │
│  │ Person  │  User or stakeholder                                               │
│  └─────────┘                                                                    │
│                                                                                  │
│  ┌─────────────────────┐                                                        │
│  │ Software System     │  The system under design                               │
│  └─────────────────────┘                                                        │
│                                                                                  │
│  ┌─────────┐                                                                    │
│  │ External│  External systems that interact                                    │
│  │ System  │                                                                    │
│  └─────────┘                                                                    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Mermaid Representation

```mermaid
C4Context
    title System Context Diagram - ECW Blackboard Orchestration

    Person(user, "Software Engineer", "Creates and manages Problem Statements, reviews agent outputs")

    System(blackboard, "ECW Blackboard Orchestration", "Manages Problem Statements, orchestrates sub-agents via Blackboard pattern, persists events")

    System_Ext(claudecli, "Claude Code CLI", "Interactive terminal for Claude AI")
    System_Ext(filesystem, "File System", "Stores events, signals, and artifacts")
    System_Ext(memorykeeper, "Memory Keeper MCP", "Provides session context persistence")

    Rel(user, blackboard, "Uses", "CLI commands")
    Rel(blackboard, claudecli, "Runs within", "Process context")
    Rel(blackboard, filesystem, "Persists to", "SQLite, JSON files")
    Rel(blackboard, memorykeeper, "Stores context", "MCP protocol")
```

---

## 3. Container Diagram (Level 2)

### ASCII Representation

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CONTAINER DIAGRAM                                   │
│                    Blackboard Agent Orchestration System                         │
└─────────────────────────────────────────────────────────────────────────────────┘

                          ┌─────────────────────┐
                          │       User          │
                          └──────────┬──────────┘
                                     │
                     ┌───────────────┴───────────────┐
                     ▼                               ▼
         ┌─────────────────────┐         ┌─────────────────────┐
         │    PS CLI Skill     │         │   Task Sub-Agents   │
         │                     │         │                     │
         │ [Python Script]     │         │ [Python Scripts]    │
         │                     │         │                     │
         │ - /ps commands      │────────▶│ - ps-researcher     │
         │ - add-entry         │ spawns  │ - ps-analyst        │
         │ - view/history      │         │ - ps-architect      │
         └──────────┬──────────┘         └──────────┬──────────┘
                    │                               │
                    │ writes                        │ reads/writes
                    │                               │
                    ▼                               ▼
         ┌─────────────────────────────────────────────────────────┐
         │                  Application Core                        │
         │                                                          │
         │  ┌─────────────────┐  ┌─────────────────┐               │
         │  │ PS Service      │  │ Blackboard      │               │
         │  │                 │  │ Service         │               │
         │  │ - Commands      │  │                 │               │
         │  │ - Queries       │  │ - Post Signal   │               │
         │  └────────┬────────┘  │ - Claim/Complete│               │
         │           │           └────────┬────────┘               │
         │           │                    │                        │
         │           └────────┬───────────┘                        │
         │                    ▼                                    │
         │           ┌─────────────────┐                           │
         │           │  Repositories   │                           │
         │           │                 │                           │
         │           │ - PS Repository │                           │
         │           │ - BB Repository │                           │
         │           └────────┬────────┘                           │
         └────────────────────┼────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
            ▼                 ▼                 ▼
   ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
   │ SQLite Event    │ │ SQLite          │ │ Signal Files    │
   │ Store           │ │ Projection      │ │                 │
   │                 │ │ Store           │ │ .ecw/signals/   │
   │ .ecw/events.db  │ │ .ecw/           │ │ pending/        │
   │                 │ │ projections.db  │ │ sig-*.json      │
   └─────────────────┘ └─────────────────┘ └─────────────────┘
```

### Mermaid Representation

```mermaid
C4Container
    title Container Diagram - ECW Blackboard Orchestration

    Person(user, "Software Engineer")

    Container_Boundary(system, "ECW Blackboard Orchestration") {
        Container(pscli, "PS CLI Skill", "Python", "Handles /ps commands, add-entry, view")
        Container(subagents, "Task Sub-Agents", "Python Scripts", "ps-researcher, ps-analyst, ps-architect")
        Container(psservice, "PS Service", "Python", "Problem Statement commands and queries")
        Container(bbservice, "Blackboard Service", "Python", "Signal posting, claiming, completion")
        Container(repos, "Repositories", "Python", "Event-sourced aggregate persistence")
    }

    ContainerDb(eventstore, "SQLite Event Store", "SQLite", "Append-only event log")
    ContainerDb(projstore, "SQLite Projection Store", "SQLite", "Denormalized read models")
    Container(signals, "Signal Files", "JSON", "Cross-process communication")

    Rel(user, pscli, "Uses", "CLI")
    Rel(pscli, subagents, "Spawns", "subprocess")
    Rel(pscli, psservice, "Calls")
    Rel(pscli, bbservice, "Calls")
    Rel(psservice, repos, "Uses")
    Rel(bbservice, repos, "Uses")
    Rel(repos, eventstore, "Reads/Writes")
    Rel(repos, projstore, "Reads/Writes")
    Rel(bbservice, signals, "Creates")
    Rel(subagents, signals, "Reads")
```

---

## 4. Component Diagram (Level 3)

### ASCII Representation

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              COMPONENT DIAGRAM                                   │
│                         Application Core Container                               │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            APPLICATION LAYER                                     │
│                                                                                  │
│  ┌──────────────────────────┐    ┌──────────────────────────┐                   │
│  │  ProblemStatementService │    │    BlackboardService     │                   │
│  │                          │    │                          │                   │
│  │  Commands:               │    │  Commands:               │                   │
│  │  - CreatePS              │    │  - PostSignal            │                   │
│  │  - AddConstraint         │    │  - ClaimSignal           │                   │
│  │  - AddQuestion           │    │  - CompleteSignal        │                   │
│  │  - AddExplorationEntry   │    │                          │                   │
│  │  - AnswerQuestion        │    │  Queries:                │                   │
│  │                          │    │  - GetSignals            │                   │
│  │  Queries:                │    │  - GetSignalStatus       │                   │
│  │  - GetPS                 │    │                          │                   │
│  │  - ListConstraints       │    └──────────────┬───────────┘                   │
│  │  - ListQuestions         │                   │                               │
│  │  - ListExplorations      │                   │                               │
│  └──────────────┬───────────┘                   │                               │
│                 │                               │                               │
└─────────────────┼───────────────────────────────┼───────────────────────────────┘
                  │                               │
┌─────────────────┼───────────────────────────────┼───────────────────────────────┐
│                 │         DOMAIN LAYER          │                               │
│                 ▼                               ▼                               │
│  ┌──────────────────────────┐    ┌──────────────────────────┐                   │
│  │ ProblemStatementAggregate│    │   BlackboardAggregate    │                   │
│  │                          │    │                          │                   │
│  │  State:                  │    │  State:                  │                   │
│  │  - constraints[]         │    │  - signals{}             │                   │
│  │  - questions[]           │    │  - ps_id                 │                   │
│  │  - explorations[]        │    │                          │                   │
│  │  - status                │    │  Events:                 │                   │
│  │                          │    │  - BlackboardCreated     │                   │
│  │  Events:                 │    │  - AgentSignalPosted     │                   │
│  │  - PSCreated             │    │  - AgentSignalClaimed    │                   │
│  │  - ConstraintAdded       │    │  - AgentSignalCompleted  │                   │
│  │  - QuestionAdded         │    │                          │                   │
│  │  - ExplorationAdded      │    └──────────────────────────┘                   │
│  │  - QuestionAnswered      │                                                   │
│  └──────────────────────────┘                                                   │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                           INFRASTRUCTURE LAYER                                   │
│                                                                                  │
│  ┌──────────────────────────┐    ┌──────────────────────────┐                   │
│  │   SQLite3EventStore      │    │ SQLite3ProjectionStore   │                   │
│  │                          │    │                          │                   │
│  │  - append(events)        │    │  - save(projection)      │                   │
│  │  - read(stream_id)       │    │  - get(projection_id)    │                   │
│  │  - get_version()         │    │  - list()                │                   │
│  └──────────────────────────┘    └──────────────────────────┘                   │
│                                                                                  │
│  ┌──────────────────────────┐    ┌──────────────────────────┐                   │
│  │   SignalFileBridge       │    │    EventConverter        │                   │
│  │                          │    │                          │                   │
│  │  - write_signal(signal)  │    │  - domain_to_cloudevent  │                   │
│  │  - read_pending()        │    │  - cloudevent_to_domain  │                   │
│  │  - archive_signal()      │    │                          │                   │
│  └──────────────────────────┘    └──────────────────────────┘                   │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Key Relationships

### Domain Relationships

```
┌──────────────────┐       1        ┌──────────────────┐
│ ProblemStatement │───────────────▶│   Blackboard     │
│   Aggregate      │ has exactly 1  │   Aggregate      │
└──────────────────┘                └──────────────────┘
         │                                   │
         │ contains *                        │ contains *
         ▼                                   ▼
┌──────────────────┐                ┌──────────────────┐
│  Exploration     │                │   AgentSignal    │
│     Entry        │                │                  │
└──────────────────┘                └──────────────────┘
         │                                   │
         │ triggers (if RESEARCH/ANALYSIS)   │
         └───────────────────────────────────┘
```

### Data Flow

```
User Input ──▶ CLI ──▶ Service ──▶ Aggregate ──▶ Event Store
                │                      │
                │                      └──▶ Signal File
                │                               │
                └───────────────────────────────┼──▶ Sub-Agent
                                                │
                                         Agent Output ──▶ Artifact
```

---

## 6. Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Presentation | Python CLI | User interface |
| Application | Python Services | Business logic orchestration |
| Domain | Python Aggregates | Business rules, event sourcing |
| Infrastructure | SQLite | Event and projection persistence |
| Communication | JSON Files | Cross-process signaling |

---

## 7. References

- **blackboard-agent-orchestration-design.md** - Core design
- **phase-38.17-deployment-diagram.md** - Physical deployment
- **phase-38.17-disaster-recovery-runbook.md** - Recovery procedures

---

*Generated per SOP-DES.6 - Design Diagrams*
