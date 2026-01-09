# PLAN: Jerry Framework Phase 3 - Hexagonal Core Implementation

**Plan ID**: PLAN-20260107-hexagonal-core
**Status**: DRAFT - AWAITING APPROVAL
**Author**: Claude (Distinguished Systems Engineering Persona)
**Created**: 2026-01-07
**Work Items**: WORK-010, WORK-011, WORK-012, WORK-013, WORK-014

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [5W1H Analysis](#2-5w1h-analysis)
3. [Bounded Context Diagram](#3-bounded-context-diagram)
4. [Package Diagram](#4-package-diagram)
5. [Domain Model - Class Diagrams](#5-domain-model---class-diagrams)
6. [Network/DTO Class Diagrams](#6-networkdto-class-diagrams)
7. [Use Case Specifications](#7-use-case-specifications)
8. [Sequence Diagrams](#8-sequence-diagrams)
9. [Activity Diagrams](#9-activity-diagrams)
10. [JSON Schemas](#10-json-schemas)
11. [BDD Test Specifications](#11-bdd-test-specifications)
12. [Implementation Plan](#12-implementation-plan)
13. [Risk Analysis](#13-risk-analysis)
14. [References](#14-references)

---

## 1. Executive Summary

### 1.1 Purpose

This plan defines the comprehensive design for the Jerry Framework's Hexagonal Core - a Python implementation following Domain-Driven Design (DDD), Hexagonal Architecture (Ports & Adapters), CQRS, and Event Sourcing patterns.

### 1.2 Scope

The Work Tracker bounded context - a local Azure DevOps/JIRA alternative that:
- Persists task state across sessions (surviving context rot)
- Implements CQRS with separate read/write models
- Uses domain events for loose coupling
- Follows pure BDD Red/Green/Refactor development

### 1.3 Key Decisions

| Decision | Choice | Rationale | Reference |
|----------|--------|-----------|-----------|
| Architecture | Hexagonal | Testability, framework independence | [Cockburn, 2005](https://alistair.cockburn.us/hexagonal-architecture/) |
| Domain Pattern | DDD Tactical | Rich domain model, aggregates | [Evans, 2003](https://www.domainlanguage.com/ddd/) |
| Data Pattern | CQRS + Events | Separate read/write, audit trail | [Cosmic Python](https://www.cosmicpython.com/book/chapter_12_cqrs.html) |
| Persistence | SQLite + Event Store | Zero deps, event sourcing ready | [Microsoft](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing) |
| Testing | BDD with pytest-bdd | Behavior-focused, collaboration | [pytest-bdd](https://pytest-bdd.readthedocs.io/) |

---

## 2. 5W1H Analysis

### 2.1 WHO (Stakeholders)

| Stakeholder | Role | Needs |
|-------------|------|-------|
| **Claude Code Agent** | Primary User | Track work across sessions, survive compaction |
| **Human Developer** | Supervisor | Review progress, approve changes |
| **QA Agent** | Quality Gate | Verify tests, validate behavior |
| **Security Agent** | Security Gate | Review for vulnerabilities |

### 2.2 WHAT (Deliverables)

| Component | Description | Files |
|-----------|-------------|-------|
| **Domain Layer** | Pure business logic | `src/domain/` |
| **Application Layer** | Use cases (CQRS) | `src/application/` |
| **Infrastructure Layer** | Adapters | `src/infrastructure/` |
| **Interface Layer** | CLI adapter | `src/interface/` |
| **Test Suites** | BDD, Unit, Integration | `tests/` |

### 2.3 WHEN (Timeline)

| Phase | Components | Dependencies |
|-------|------------|--------------|
| 3.1 | Domain Layer | None |
| 3.2 | Application Layer | 3.1 |
| 3.3 | Infrastructure Layer | 3.1, 3.2 |
| 3.4 | Interface Layer | 3.1, 3.2, 3.3 |
| 3.5 | Integration Testing | All above |

### 2.4 WHERE (Location)

```
jerry/
├── src/
│   ├── domain/           # WHERE: Business logic lives
│   ├── application/      # WHERE: Use cases orchestrate
│   ├── infrastructure/   # WHERE: Technical adapters live
│   └── interface/        # WHERE: Entry points exist
├── tests/
│   ├── unit/             # WHERE: Unit tests
│   ├── integration/      # WHERE: Integration tests
│   ├── e2e/              # WHERE: End-to-end tests
│   └── bdd/              # WHERE: BDD feature tests
└── data/
    └── worktracker/      # WHERE: Persistence storage
```

### 2.5 WHY (Justification)

**Problem**: Context rot degrades LLM performance as context fills.

> "The effective context window where models perform optimally is often <256k tokens"
> — [Chroma Research](https://research.trychroma.com/context-rot)

**Solution**: External memory via Work Tracker persists state outside context window.

**Why These Patterns**:
1. **Hexagonal**: Enables testing without infrastructure
2. **DDD**: Rich domain model captures business rules
3. **CQRS**: Optimized read/write paths
4. **Events**: Audit trail, loose coupling

### 2.6 HOW (Approach)

**Development Methodology**: BDD Red/Green/Refactor

```
1. WRITE failing BDD scenario (RED)
2. IMPLEMENT minimum code to pass (GREEN)
3. REFACTOR for quality (REFACTOR)
4. REPEAT
```

**Architecture Approach**: Outside-In

```
1. Define ports (interfaces) first
2. Implement domain entities
3. Create use cases
4. Build adapters
5. Wire together
```

---

## 3. Bounded Context Diagram

### 3.1 Context Map

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           JERRY FRAMEWORK                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                    WORK TRACKER CONTEXT                           │  │
│  │                    (Core Subdomain)                               │  │
│  │                                                                   │  │
│  │  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐        │  │
│  │  │  WorkItem   │────▶│   Project   │     │   Sprint    │        │  │
│  │  │ (Aggregate) │     │ (Aggregate) │     │ (Aggregate) │        │  │
│  │  └─────────────┘     └─────────────┘     └─────────────┘        │  │
│  │         │                   │                   │                │  │
│  │         ▼                   ▼                   ▼                │  │
│  │  ┌─────────────────────────────────────────────────────┐        │  │
│  │  │              Domain Events Bus                       │        │  │
│  │  │  (WorkItemCreated, WorkItemCompleted, etc.)         │        │  │
│  │  └─────────────────────────────────────────────────────┘        │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                   │                                      │
│                                   │ Anti-Corruption Layer                │
│                                   ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                    KNOWLEDGE CONTEXT                              │  │
│  │                    (Supporting Subdomain)                         │  │
│  │                                                                   │  │
│  │  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐        │  │
│  │  │  Document   │     │  Decision   │     │  Learning   │        │  │
│  │  └─────────────┘     └─────────────┘     └─────────────┘        │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                    GOVERNANCE CONTEXT                             │  │
│  │                    (Generic Subdomain)                            │  │
│  │                                                                   │  │
│  │  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐        │  │
│  │  │    Agent    │     │    Hook     │     │    Rule     │        │  │
│  │  └─────────────┘     └─────────────┘     └─────────────┘        │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

Legend:
  ─────▶  Uses/References
  - - -▶  Publishes Events To
```

### 3.2 Context Relationships

| Upstream | Downstream | Relationship | Pattern |
|----------|------------|--------------|---------|
| Work Tracker | Knowledge | Publisher-Subscriber | Domain Events |
| Work Tracker | Governance | Conformist | Shared Kernel |
| Governance | Work Tracker | Open Host Service | REST/CLI |

---

## 4. Package Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              src/                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                        interface/                                │    │
│  │  ┌─────────────┐    ┌─────────────┐                             │    │
│  │  │    cli/     │    │    api/     │   (Primary Adapters)        │    │
│  │  │  main.py    │    │ controllers │                             │    │
│  │  │  formatter  │    │             │                             │    │
│  │  └──────┬──────┘    └──────┬──────┘                             │    │
│  └─────────┼──────────────────┼────────────────────────────────────┘    │
│            │                  │                                          │
│            ▼                  ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                       application/                               │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │                    use_cases/                            │    │    │
│  │  │  ┌──────────────┐         ┌──────────────┐              │    │    │
│  │  │  │  commands/   │         │   queries/   │              │    │    │
│  │  │  │              │         │              │              │    │    │
│  │  │  │ CreateItem   │         │ GetItem      │              │    │    │
│  │  │  │ UpdateItem   │         │ ListItems    │              │    │    │
│  │  │  │ CompleteItem │         │ SearchItems  │              │    │    │
│  │  │  └──────────────┘         └──────────────┘              │    │    │
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │    │
│  │  │    dtos/     │    │ dispatcher/  │    │  services/   │       │    │
│  │  └──────────────┘    └──────────────┘    └──────────────┘       │    │
│  └──────────────────────────────┬──────────────────────────────────┘    │
│                                 │                                        │
│                                 ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                         domain/                                  │    │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │    │
│  │  │ aggregates/  │    │value_objects/│    │   events/    │       │    │
│  │  │              │    │              │    │              │       │    │
│  │  │ WorkItem     │    │ Status       │    │ ItemCreated  │       │    │
│  │  │ Project      │    │ Priority     │    │ ItemCompleted│       │    │
│  │  │              │    │ WorkItemId   │    │ ItemUpdated  │       │    │
│  │  └──────────────┘    └──────────────┘    └──────────────┘       │    │
│  │  ┌──────────────┐    ┌──────────────┐                           │    │
│  │  │   ports/     │    │ exceptions/  │   (NO EXTERNAL DEPS)      │    │
│  │  │              │    │              │                           │    │
│  │  │ IRepository  │    │ DomainError  │                           │    │
│  │  │ IEventStore  │    │ NotFound     │                           │    │
│  │  │ INotifier    │    │ InvalidState │                           │    │
│  │  └──────┬───────┘    └──────────────┘                           │    │
│  └─────────┼───────────────────────────────────────────────────────┘    │
│            │                                                             │
│            │ implements                                                  │
│            ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                      infrastructure/                             │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │                    persistence/                          │    │    │
│  │  │  ┌──────────────┐         ┌──────────────┐              │    │    │
│  │  │  │   sqlite/    │         │     fs/      │              │    │    │
│  │  │  │              │         │              │              │    │    │
│  │  │  │ repository   │         │ md_adapter   │              │    │    │
│  │  │  │ event_store  │         │              │              │    │    │
│  │  │  └──────────────┘         └──────────────┘              │    │    │
│  │  └─────────────────────────────────────────────────────────┘    │    │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │    │
│  │  │  messaging/  │    │   schemas/   │    │ dispatcher/  │       │    │
│  │  └──────────────┘    └──────────────┘    └──────────────┘       │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

Dependency Rules:
  interface/     → application/, infrastructure/, domain/
  application/   → domain/ ONLY
  infrastructure/→ domain/, application/
  domain/        → NOTHING (stdlib only)
```

---

## 5. Domain Model - Class Diagrams

### 5.1 WorkItem Aggregate

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         <<Aggregate Root>>                               │
│                            WorkItem                                      │
├─────────────────────────────────────────────────────────────────────────┤
│ - _id: WorkItemId                                                        │
│ - _title: str                                                            │
│ - _description: str                                                      │
│ - _type: WorkItemType                                                    │
│ - _status: Status                                                        │
│ - _priority: Priority                                                    │
│ - _parent_id: WorkItemId | None                                          │
│ - _created_at: datetime                                                  │
│ - _updated_at: datetime                                                  │
│ - _completed_at: datetime | None                                         │
│ - _notes: list[Note]                                                     │
│ - _tags: list[Tag]                                                       │
│ - _events: list[DomainEvent]                                             │
├─────────────────────────────────────────────────────────────────────────┤
│ <<class methods>>                                                        │
│ + create(title, type, priority, parent_id?) → WorkItem                   │
│ + reconstitute(events: list[DomainEvent]) → WorkItem                     │
├─────────────────────────────────────────────────────────────────────────┤
│ <<properties>>                                                           │
│ + id: WorkItemId {readonly}                                              │
│ + title: str {readonly}                                                  │
│ + status: Status {readonly}                                              │
│ + priority: Priority {readonly}                                          │
│ + is_completed: bool {readonly}                                          │
│ + is_blocked: bool {readonly}                                            │
│ + pending_events: list[DomainEvent] {readonly}                           │
├─────────────────────────────────────────────────────────────────────────┤
│ <<commands>>                                                             │
│ + update_title(new_title: str) → None                                    │
│ + update_description(desc: str) → None                                   │
│ + change_priority(priority: Priority) → None                             │
│ + start() → None                          # pending → in_progress        │
│ + block(reason: str) → None               # → blocked                    │
│ + unblock() → None                        # blocked → in_progress        │
│ + complete(notes: str?) → None            # → completed                  │
│ + reopen() → None                         # completed → pending          │
│ + add_note(content: str) → None                                          │
│ + add_tag(tag: Tag) → None                                               │
│ + remove_tag(tag: Tag) → None                                            │
├─────────────────────────────────────────────────────────────────────────┤
│ <<internal>>                                                             │
│ - _apply(event: DomainEvent) → None                                      │
│ - _raise_event(event: DomainEvent) → None                                │
│ - _validate_state_transition(from: Status, to: Status) → None            │
└─────────────────────────────────────────────────────────────────────────┘
           │
           │ contains
           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           <<Value Object>>                               │
│                               Note                                       │
├─────────────────────────────────────────────────────────────────────────┤
│ + content: str {readonly, frozen}                                        │
│ + created_at: datetime {readonly, frozen}                                │
│ + author: str {readonly, frozen}                                         │
├─────────────────────────────────────────────────────────────────────────┤
│ + __eq__(other: Note) → bool                                             │
│ + __hash__() → int                                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Value Objects

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           <<Value Object>>                               │
│                            WorkItemId                                    │
├─────────────────────────────────────────────────────────────────────────┤
│ + value: str {readonly, frozen}                                          │
│ + prefix: str = "WORK" {class attr}                                      │
├─────────────────────────────────────────────────────────────────────────┤
│ <<class methods>>                                                        │
│ + generate() → WorkItemId                                                │
│ + from_string(value: str) → WorkItemId                                   │
├─────────────────────────────────────────────────────────────────────────┤
│ + __str__() → str                         # "WORK-001"                   │
│ + __eq__(other) → bool                                                   │
│ + __hash__() → int                                                       │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                           <<Value Object>>                               │
│                              Status                                      │
├─────────────────────────────────────────────────────────────────────────┤
│ <<enumeration>>                                                          │
│ PENDING = "pending"                                                      │
│ IN_PROGRESS = "in_progress"                                              │
│ BLOCKED = "blocked"                                                      │
│ COMPLETED = "completed"                                                  │
├─────────────────────────────────────────────────────────────────────────┤
│ + can_transition_to(target: Status) → bool                               │
│ + valid_transitions() → set[Status]                                      │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                           <<Value Object>>                               │
│                             Priority                                     │
├─────────────────────────────────────────────────────────────────────────┤
│ <<enumeration>>                                                          │
│ CRITICAL = 1                                                             │
│ HIGH = 2                                                                 │
│ MEDIUM = 3                                                               │
│ LOW = 4                                                                  │
├─────────────────────────────────────────────────────────────────────────┤
│ + __lt__(other: Priority) → bool          # For sorting                  │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                           <<Value Object>>                               │
│                           WorkItemType                                   │
├─────────────────────────────────────────────────────────────────────────┤
│ <<enumeration>>                                                          │
│ EPIC = "epic"                                                            │
│ FEATURE = "feature"                                                      │
│ TASK = "task"                                                            │
│ BUG = "bug"                                                              │
│ SPIKE = "spike"                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│ + can_have_children() → bool              # epic, feature can            │
│ + allowed_parent_types() → set[WorkItemType]                             │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                           <<Value Object>>                               │
│                               Tag                                        │
├─────────────────────────────────────────────────────────────────────────┤
│ + name: str {readonly, frozen}                                           │
│ + color: str | None {readonly, frozen}                                   │
├─────────────────────────────────────────────────────────────────────────┤
│ + __eq__(other: Tag) → bool                                              │
│ + __hash__() → int                                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Domain Events

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           <<Abstract>>                                   │
│                          DomainEvent                                     │
├─────────────────────────────────────────────────────────────────────────┤
│ + event_id: UUID {readonly}                                              │
│ + event_type: str {readonly}                                             │
│ + aggregate_id: str {readonly}                                           │
│ + aggregate_type: str {readonly}                                         │
│ + occurred_at: datetime {readonly}                                       │
│ + version: int {readonly}                                                │
│ + payload: dict {readonly}                                               │
├─────────────────────────────────────────────────────────────────────────┤
│ + to_dict() → dict                                                       │
│ + from_dict(data: dict) → DomainEvent {class method}                     │
└─────────────────────────────────────────────────────────────────────────┘
           △
           │ extends
           │
     ┌─────┴─────┬─────────────┬──────────────┬──────────────┐
     │           │             │              │              │
┌────┴────┐ ┌────┴────┐ ┌──────┴──────┐ ┌─────┴─────┐ ┌──────┴──────┐
│WorkItem │ │WorkItem │ │  WorkItem   │ │ WorkItem  │ │  WorkItem   │
│Created  │ │Started  │ │  Completed  │ │  Blocked  │ │   Updated   │
├─────────┤ ├─────────┤ ├─────────────┤ ├───────────┤ ├─────────────┤
│+title   │ │         │ │+completed_at│ │+reason    │ │+field       │
│+type    │ │         │ │+notes       │ │           │ │+old_value   │
│+priority│ │         │ │             │ │           │ │+new_value   │
└─────────┘ └─────────┘ └─────────────┘ └───────────┘ └─────────────┘
```

### 5.4 Port Interfaces

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            <<Protocol>>                                  │
│                       IWorkItemRepository                                │
├─────────────────────────────────────────────────────────────────────────┤
│ + save(item: WorkItem) → None                                            │
│ + get(id: WorkItemId) → WorkItem | None                                  │
│ + get_all() → list[WorkItem]                                             │
│ + get_by_status(status: Status) → list[WorkItem]                         │
│ + get_by_parent(parent_id: WorkItemId) → list[WorkItem]                  │
│ + delete(id: WorkItemId) → None                                          │
│ + exists(id: WorkItemId) → bool                                          │
│ + next_id() → WorkItemId                                                 │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                            <<Protocol>>                                  │
│                          IEventStore                                     │
├─────────────────────────────────────────────────────────────────────────┤
│ + append(aggregate_id: str, events: list[DomainEvent]) → None            │
│ + get_events(aggregate_id: str) → list[DomainEvent]                      │
│ + get_events_since(aggregate_id: str, version: int) → list[DomainEvent]  │
│ + get_all_events() → list[DomainEvent]                                   │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                            <<Protocol>>                                  │
│                         IEventDispatcher                                 │
├─────────────────────────────────────────────────────────────────────────┤
│ + dispatch(event: DomainEvent) → None                                    │
│ + dispatch_all(events: list[DomainEvent]) → None                         │
│ + subscribe(event_type: str, handler: Callable) → None                   │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                            <<Protocol>>                                  │
│                            IUnitOfWork                                   │
├─────────────────────────────────────────────────────────────────────────┤
│ + work_items: IWorkItemRepository {readonly}                             │
│ + __enter__() → IUnitOfWork                                              │
│ + __exit__(exc_type, exc_val, exc_tb) → None                             │
│ + commit() → None                                                        │
│ + rollback() → None                                                      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Network/DTO Class Diagrams

### 6.1 Data Transfer Objects (Read Models)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              <<DTO>>                                     │
│                          WorkItemDTO                                     │
├─────────────────────────────────────────────────────────────────────────┤
│ + id: str                                                                │
│ + title: str                                                             │
│ + description: str                                                       │
│ + type: str                                                              │
│ + status: str                                                            │
│ + priority: str                                                          │
│ + parent_id: str | None                                                  │
│ + created_at: str                         # ISO 8601                     │
│ + updated_at: str                         # ISO 8601                     │
│ + completed_at: str | None                # ISO 8601                     │
│ + notes: list[NoteDTO]                                                   │
│ + tags: list[str]                                                        │
│ + children_count: int                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│ + to_dict() → dict                                                       │
│ + from_dict(data: dict) → WorkItemDTO {class method}                     │
│ + from_entity(entity: WorkItem) → WorkItemDTO {class method}             │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                              <<DTO>>                                     │
│                        WorkItemSummaryDTO                                │
├─────────────────────────────────────────────────────────────────────────┤
│ + id: str                                                                │
│ + title: str                                                             │
│ + status: str                                                            │
│ + priority: str                                                          │
│ + type: str                                                              │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                              <<DTO>>                                     │
│                        WorkTrackerStatsDTO                               │
├─────────────────────────────────────────────────────────────────────────┤
│ + total_items: int                                                       │
│ + by_status: dict[str, int]                                              │
│ + by_priority: dict[str, int]                                            │
│ + by_type: dict[str, int]                                                │
│ + completed_today: int                                                   │
│ + created_today: int                                                     │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                              <<DTO>>                                     │
│                             NoteDTO                                      │
├─────────────────────────────────────────────────────────────────────────┤
│ + content: str                                                           │
│ + created_at: str                         # ISO 8601                     │
│ + author: str                                                            │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Command Objects (Write Models)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            <<Command>>                                   │
│                       CreateWorkItemCommand                              │
├─────────────────────────────────────────────────────────────────────────┤
│ + title: str                              # required                     │
│ + description: str = ""                   # optional                     │
│ + type: str = "task"                      # optional                     │
│ + priority: str = "medium"                # optional                     │
│ + parent_id: str | None = None            # optional                     │
│ + tags: list[str] = []                    # optional                     │
├─────────────────────────────────────────────────────────────────────────┤
│ + validate() → None                       # raises ValidationError       │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                            <<Command>>                                   │
│                       UpdateWorkItemCommand                              │
├─────────────────────────────────────────────────────────────────────────┤
│ + id: str                                 # required                     │
│ + title: str | None = None                # optional                     │
│ + description: str | None = None          # optional                     │
│ + priority: str | None = None             # optional                     │
│ + status: str | None = None               # optional                     │
│ + notes: str | None = None                # optional (adds note)         │
├─────────────────────────────────────────────────────────────────────────┤
│ + validate() → None                                                      │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                            <<Command>>                                   │
│                      CompleteWorkItemCommand                             │
├─────────────────────────────────────────────────────────────────────────┤
│ + id: str                                 # required                     │
│ + notes: str | None = None                # optional                     │
├─────────────────────────────────────────────────────────────────────────┤
│ + validate() → None                                                      │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                             <<Query>>                                    │
│                         GetWorkItemQuery                                 │
├─────────────────────────────────────────────────────────────────────────┤
│ + id: str                                 # required                     │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                             <<Query>>                                    │
│                        ListWorkItemsQuery                                │
├─────────────────────────────────────────────────────────────────────────┤
│ + status: list[str] | None = None         # filter                       │
│ + priority: list[str] | None = None       # filter                       │
│ + type: list[str] | None = None           # filter                       │
│ + parent_id: str | None = None            # filter                       │
│ + limit: int = 50                         # pagination                   │
│ + offset: int = 0                         # pagination                   │
│ + sort_by: str = "created_at"             # sorting                      │
│ + sort_order: str = "desc"                # asc/desc                     │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                             <<Query>>                                    │
│                       SearchWorkItemsQuery                               │
├─────────────────────────────────────────────────────────────────────────┤
│ + query: str                              # search text                  │
│ + include_completed: bool = False         # filter                       │
│ + limit: int = 20                         # pagination                   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Use Case Specifications

### 7.1 Commands (Write Operations)

#### UC-CMD-001: Create Work Item

| Attribute | Value |
|-----------|-------|
| **Name** | CreateWorkItem |
| **Actor** | Claude Agent / User |
| **Preconditions** | None |
| **Postconditions** | Work item exists in repository, WorkItemCreated event emitted |
| **Trigger** | `@worktracker create <title>` |

**Main Flow**:
1. Validate command input
2. Generate new WorkItemId
3. Create WorkItem aggregate via factory method
4. Save to repository within Unit of Work
5. Dispatch WorkItemCreated event
6. Return created WorkItemDTO

**Alternative Flows**:
- **A1**: Invalid title (empty) → Raise ValidationError
- **A2**: Invalid parent_id → Raise WorkItemNotFoundError
- **A3**: Invalid type for parent → Raise InvalidHierarchyError

**Business Rules**:
- Title must be non-empty, max 200 characters
- Tasks can only have Features/Epics as parents
- Bugs can only have Features/Epics as parents

---

#### UC-CMD-002: Update Work Item

| Attribute | Value |
|-----------|-------|
| **Name** | UpdateWorkItem |
| **Actor** | Claude Agent / User |
| **Preconditions** | Work item exists |
| **Postconditions** | Work item updated, WorkItemUpdated event(s) emitted |

**Main Flow**:
1. Validate command input
2. Load WorkItem from repository
3. Apply updates to aggregate
4. Save to repository
5. Dispatch events
6. Return updated WorkItemDTO

**Alternative Flows**:
- **A1**: Work item not found → Raise WorkItemNotFoundError
- **A2**: Invalid status transition → Raise InvalidStateTransitionError

---

#### UC-CMD-003: Complete Work Item

| Attribute | Value |
|-----------|-------|
| **Name** | CompleteWorkItem |
| **Actor** | Claude Agent / User |
| **Preconditions** | Work item exists, not already completed |
| **Postconditions** | Status = completed, WorkItemCompleted event emitted |

**Main Flow**:
1. Load WorkItem
2. Call `work_item.complete(notes)`
3. Save and dispatch events

**Business Rules**:
- Cannot complete if already completed
- Cannot complete if blocked (must unblock first)
- Completing parent does NOT auto-complete children

---

### 7.2 Queries (Read Operations)

#### UC-QRY-001: Get Work Item

| Attribute | Value |
|-----------|-------|
| **Name** | GetWorkItem |
| **Input** | id: str |
| **Output** | WorkItemDTO | None |

---

#### UC-QRY-002: List Work Items

| Attribute | Value |
|-----------|-------|
| **Name** | ListWorkItems |
| **Input** | ListWorkItemsQuery |
| **Output** | list[WorkItemSummaryDTO] |

---

#### UC-QRY-003: Search Work Items

| Attribute | Value |
|-----------|-------|
| **Name** | SearchWorkItems |
| **Input** | SearchWorkItemsQuery |
| **Output** | list[WorkItemSummaryDTO] |

**Search Behavior**:
- Searches title, description, and notes
- Case-insensitive
- Supports partial matches

---

#### UC-QRY-004: Get Work Tracker Stats

| Attribute | Value |
|-----------|-------|
| **Name** | GetWorkTrackerStats |
| **Input** | time_range: str (optional) |
| **Output** | WorkTrackerStatsDTO |

---

## 8. Sequence Diagrams

### 8.1 Create Work Item Flow

```
┌─────┐          ┌─────┐          ┌──────────┐          ┌──────────┐          ┌─────────┐
│ CLI │          │ Use │          │ WorkItem │          │Repository│          │ Event   │
│     │          │Case │          │          │          │          │          │Dispatcher│
└──┬──┘          └──┬──┘          └────┬─────┘          └────┬─────┘          └────┬────┘
   │                │                   │                    │                     │
   │ create("title")│                   │                    │                     │
   │───────────────>│                   │                    │                     │
   │                │                   │                    │                     │
   │                │  validate()       │                    │                     │
   │                │──────────────────>│                    │                     │
   │                │                   │                    │                     │
   │                │               next_id()                │                     │
   │                │───────────────────────────────────────>│                     │
   │                │                   │                    │                     │
   │                │                   │<───────────────────│                     │
   │                │                   │    WORK-001        │                     │
   │                │                   │                    │                     │
   │                │ WorkItem.create() │                    │                     │
   │                │──────────────────>│                    │                     │
   │                │                   │                    │                     │
   │                │                   │ ┌─────────────────┐│                     │
   │                │                   │ │_raise_event(    ││                     │
   │                │                   │ │WorkItemCreated) ││                     │
   │                │                   │ └─────────────────┘│                     │
   │                │                   │                    │                     │
   │                │<──────────────────│                    │                     │
   │                │     WorkItem      │                    │                     │
   │                │                   │                    │                     │
   │                │               save(item)               │                     │
   │                │───────────────────────────────────────>│                     │
   │                │                   │                    │                     │
   │                │                   │                    │ dispatch(event)     │
   │                │──────────────────────────────────────────────────────────────>│
   │                │                   │                    │                     │
   │<───────────────│                   │                    │                     │
   │  WorkItemDTO   │                   │                    │                     │
   │                │                   │                    │                     │
```

### 8.2 Complete Work Item Flow (with State Transition)

```
┌─────┐          ┌─────┐          ┌──────────┐          ┌──────────┐
│ CLI │          │ Use │          │ WorkItem │          │Repository│
│     │          │Case │          │          │          │          │
└──┬──┘          └──┬──┘          └────┬─────┘          └────┬─────┘
   │                │                   │                    │
   │complete("WORK-001", notes)         │                    │
   │───────────────>│                   │                    │
   │                │                   │                    │
   │                │              get("WORK-001")           │
   │                │───────────────────────────────────────>│
   │                │                   │                    │
   │                │<───────────────────────────────────────│
   │                │                WorkItem                │
   │                │                   │                    │
   │                │  complete(notes)  │                    │
   │                │──────────────────>│                    │
   │                │                   │                    │
   │                │                   │ ┌─────────────────────────┐
   │                │                   │ │_validate_state_transition│
   │                │                   │ │(in_progress → completed) │
   │                │                   │ └─────────────────────────┘
   │                │                   │                    │
   │                │                   │ ┌─────────────────┐│
   │                │                   │ │_raise_event(    ││
   │                │                   │ │WorkItemCompleted││
   │                │                   │ └─────────────────┘│
   │                │                   │                    │
   │                │<──────────────────│                    │
   │                │       OK          │                    │
   │                │                   │                    │
   │                │               save(item)               │
   │                │───────────────────────────────────────>│
   │                │                   │                    │
   │<───────────────│                   │                    │
   │  WorkItemDTO   │                   │                    │
```

---

## 9. Activity Diagrams

### 9.1 Work Item State Machine

```
                              ┌─────────────┐
                              │   START     │
                              └──────┬──────┘
                                     │
                                     ▼
                              ┌─────────────┐
                        ┌────▶│   PENDING   │◀────┐
                        │     └──────┬──────┘     │
                        │            │            │
                        │     start()│            │reopen()
                        │            ▼            │
                        │     ┌─────────────┐     │
                        │     │ IN_PROGRESS │─────┤
                        │     └──────┬──────┘     │
                        │            │            │
                 unblock()    block()│            │
                        │            ▼            │
                        │     ┌─────────────┐     │
                        └─────│   BLOCKED   │     │
                              └─────────────┘     │
                                     │            │
                                     │complete()  │
                                     ▼            │
                              ┌─────────────┐     │
                              │  COMPLETED  │─────┘
                              └──────┬──────┘
                                     │
                                     ▼
                              ┌─────────────┐
                              │    END      │
                              └─────────────┘

State Transition Rules:
┌──────────────┬────────────────────────────────────────────┐
│ From State   │ Valid Transitions                          │
├──────────────┼────────────────────────────────────────────┤
│ PENDING      │ IN_PROGRESS (start)                        │
│ IN_PROGRESS  │ BLOCKED (block), COMPLETED (complete)      │
│ BLOCKED      │ IN_PROGRESS (unblock)                      │
│ COMPLETED    │ PENDING (reopen)                           │
└──────────────┴────────────────────────────────────────────┘
```

### 9.2 Create Work Item Activity

```
┌─────────────┐
│   START     │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Receive Command     │
└──────────┬──────────┘
           │
           ▼
     ┌───────────┐
     │ Validate  │
     │  Input?   │
     └─────┬─────┘
           │
     ┌─────┴─────┐
     │           │
    YES          NO
     │           │
     ▼           ▼
┌─────────┐  ┌─────────────┐
│Generate │  │ Raise       │
│   ID    │  │ Validation  │
└────┬────┘  │ Error       │
     │       └──────┬──────┘
     ▼              │
┌─────────────┐     │
│ Create      │     │
│ Aggregate   │     │
└──────┬──────┘     │
       │            │
       ▼            │
┌─────────────┐     │
│ Raise       │     │
│ Domain Event│     │
└──────┬──────┘     │
       │            │
       ▼            │
┌─────────────┐     │
│ Save to     │     │
│ Repository  │     │
└──────┬──────┘     │
       │            │
       ▼            │
┌─────────────┐     │
│ Dispatch    │     │
│ Events      │     │
└──────┬──────┘     │
       │            │
       ▼            │
┌─────────────┐     │
│ Return DTO  │     │
└──────┬──────┘     │
       │            │
       ▼            ▼
┌─────────────────────┐
│        END          │
└─────────────────────┘
```

---

## 10. JSON Schemas

### 10.1 Work Item Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.framework/schemas/work-item.json",
  "title": "WorkItem",
  "description": "A work item in the Jerry Work Tracker",
  "type": "object",
  "required": ["id", "title", "type", "status", "priority", "created_at", "updated_at"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^WORK-[0-9]+$",
      "description": "Unique identifier",
      "examples": ["WORK-001", "WORK-123"]
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200,
      "description": "Short description of the work item"
    },
    "description": {
      "type": "string",
      "maxLength": 10000,
      "default": "",
      "description": "Detailed description"
    },
    "type": {
      "type": "string",
      "enum": ["epic", "feature", "task", "bug", "spike"],
      "default": "task"
    },
    "status": {
      "type": "string",
      "enum": ["pending", "in_progress", "blocked", "completed"],
      "default": "pending"
    },
    "priority": {
      "type": "string",
      "enum": ["critical", "high", "medium", "low"],
      "default": "medium"
    },
    "parent_id": {
      "type": ["string", "null"],
      "pattern": "^WORK-[0-9]+$",
      "default": null
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time"
    },
    "completed_at": {
      "type": ["string", "null"],
      "format": "date-time",
      "default": null
    },
    "notes": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/Note"
      },
      "default": []
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 50
      },
      "default": []
    }
  },
  "$defs": {
    "Note": {
      "type": "object",
      "required": ["content", "created_at"],
      "properties": {
        "content": {
          "type": "string",
          "minLength": 1,
          "maxLength": 5000
        },
        "created_at": {
          "type": "string",
          "format": "date-time"
        },
        "author": {
          "type": "string",
          "default": "claude"
        }
      }
    }
  }
}
```

### 10.2 Domain Event Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.framework/schemas/domain-event.json",
  "title": "DomainEvent",
  "description": "Base schema for domain events",
  "type": "object",
  "required": ["event_id", "event_type", "aggregate_id", "aggregate_type", "occurred_at", "version"],
  "properties": {
    "event_id": {
      "type": "string",
      "format": "uuid"
    },
    "event_type": {
      "type": "string",
      "enum": [
        "WorkItemCreated",
        "WorkItemUpdated",
        "WorkItemStarted",
        "WorkItemBlocked",
        "WorkItemUnblocked",
        "WorkItemCompleted",
        "WorkItemReopened",
        "NoteAdded",
        "TagAdded",
        "TagRemoved"
      ]
    },
    "aggregate_id": {
      "type": "string"
    },
    "aggregate_type": {
      "type": "string",
      "enum": ["WorkItem", "Project"]
    },
    "occurred_at": {
      "type": "string",
      "format": "date-time"
    },
    "version": {
      "type": "integer",
      "minimum": 1
    },
    "payload": {
      "type": "object"
    }
  }
}
```

### 10.3 Command Schemas

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.framework/schemas/commands/create-work-item.json",
  "title": "CreateWorkItemCommand",
  "type": "object",
  "required": ["title"],
  "properties": {
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "maxLength": 10000,
      "default": ""
    },
    "type": {
      "type": "string",
      "enum": ["epic", "feature", "task", "bug", "spike"],
      "default": "task"
    },
    "priority": {
      "type": "string",
      "enum": ["critical", "high", "medium", "low"],
      "default": "medium"
    },
    "parent_id": {
      "type": ["string", "null"],
      "pattern": "^WORK-[0-9]+$"
    },
    "tags": {
      "type": "array",
      "items": {"type": "string"},
      "default": []
    }
  }
}
```

---

## 11. BDD Test Specifications

### 11.1 Feature: Create Work Item

```gherkin
Feature: Create Work Item
  As a Claude Code agent
  I want to create work items
  So that I can track tasks across sessions

  Background:
    Given the work tracker is initialized
    And no work items exist

  @unit @happy-path
  Scenario: Create a simple task
    When I create a work item with title "Implement user authentication"
    Then a work item should be created with id "WORK-001"
    And the work item status should be "pending"
    And the work item type should be "task"
    And the work item priority should be "medium"
    And a WorkItemCreated event should be raised

  @unit @happy-path
  Scenario: Create a feature with custom priority
    When I create a work item with:
      | title    | Add caching layer |
      | type     | feature           |
      | priority | high              |
    Then a work item should be created
    And the work item type should be "feature"
    And the work item priority should be "high"

  @unit @edge-case
  Scenario: Create task with parent feature
    Given a work item exists with:
      | id   | WORK-001        |
      | type | feature         |
      | title| Parent Feature  |
    When I create a work item with:
      | title     | Child Task |
      | type      | task       |
      | parent_id | WORK-001   |
    Then the work item should have parent_id "WORK-001"

  @unit @error-case
  Scenario: Fail to create with empty title
    When I attempt to create a work item with title ""
    Then a ValidationError should be raised
    And the error message should contain "title"

  @unit @error-case
  Scenario: Fail to create with invalid parent
    When I attempt to create a work item with:
      | title     | Orphan Task  |
      | parent_id | WORK-999     |
    Then a WorkItemNotFoundError should be raised

  @unit @error-case
  Scenario: Fail to create task under task
    Given a work item exists with:
      | id   | WORK-001 |
      | type | task     |
    When I attempt to create a work item with:
      | title     | Nested Task |
      | type      | task        |
      | parent_id | WORK-001    |
    Then an InvalidHierarchyError should be raised
```

### 11.2 Feature: Work Item State Transitions

```gherkin
Feature: Work Item State Transitions
  As a Claude Code agent
  I want to change work item status
  So that I can track progress accurately

  Background:
    Given a work item exists with:
      | id     | WORK-001           |
      | title  | Test Item          |
      | status | pending            |

  @unit @state-machine
  Scenario: Start a pending work item
    When I start work item "WORK-001"
    Then the work item status should be "in_progress"
    And a WorkItemStarted event should be raised

  @unit @state-machine
  Scenario: Block an in-progress work item
    Given work item "WORK-001" has status "in_progress"
    When I block work item "WORK-001" with reason "Waiting for API access"
    Then the work item status should be "blocked"
    And a WorkItemBlocked event should be raised with reason "Waiting for API access"

  @unit @state-machine
  Scenario: Complete an in-progress work item
    Given work item "WORK-001" has status "in_progress"
    When I complete work item "WORK-001" with notes "All tests passing"
    Then the work item status should be "completed"
    And the work item completed_at should be set
    And a WorkItemCompleted event should be raised

  @unit @state-machine @error-case
  Scenario: Cannot complete a pending work item directly
    When I attempt to complete work item "WORK-001"
    Then an InvalidStateTransitionError should be raised
    And the error message should contain "pending" and "completed"

  @unit @state-machine @error-case
  Scenario: Cannot complete a blocked work item
    Given work item "WORK-001" has status "blocked"
    When I attempt to complete work item "WORK-001"
    Then an InvalidStateTransitionError should be raised

  @unit @state-machine
  Scenario: Reopen a completed work item
    Given work item "WORK-001" has status "completed"
    When I reopen work item "WORK-001"
    Then the work item status should be "pending"
    And the work item completed_at should be null
    And a WorkItemReopened event should be raised
```

### 11.3 Feature: Query Work Items

```gherkin
Feature: Query Work Items
  As a Claude Code agent
  I want to query work items
  So that I can understand current state

  Background:
    Given work items exist:
      | id       | title          | status      | priority | type    |
      | WORK-001 | Task One       | pending     | high     | task    |
      | WORK-002 | Task Two       | in_progress | medium   | task    |
      | WORK-003 | Task Three     | completed   | low      | task    |
      | WORK-004 | Feature One    | in_progress | high     | feature |

  @integration @query
  Scenario: List all pending and in-progress items
    When I list work items with status "pending,in_progress"
    Then I should receive 3 work items
    And the results should include "WORK-001", "WORK-002", "WORK-004"
    And the results should not include "WORK-003"

  @integration @query
  Scenario: List high priority items
    When I list work items with priority "high"
    Then I should receive 2 work items
    And the results should include "WORK-001", "WORK-004"

  @integration @query
  Scenario: Search by title
    When I search work items for "Task"
    Then I should receive 2 work items
    And the results should include "WORK-001", "WORK-002"

  @integration @query
  Scenario: Get work tracker stats
    When I get work tracker stats
    Then the total_items should be 4
    And by_status should show:
      | status      | count |
      | pending     | 1     |
      | in_progress | 2     |
      | completed   | 1     |
```

---

## 12. Implementation Plan

### 12.1 Phase 3.1: Domain Layer (BDD)

| Task | Sub-tasks | Tests |
|------|-----------|-------|
| **WORK-011.1**: WorkItemId VO | Implement, validate | Unit: generation, parsing, equality |
| **WORK-011.2**: Status VO | Implement with transitions | Unit: all transitions, invalid transitions |
| **WORK-011.3**: Priority VO | Implement with ordering | Unit: ordering, comparison |
| **WORK-011.4**: WorkItemType VO | Implement with hierarchy rules | Unit: parent rules |
| **WORK-011.5**: Note VO | Implement immutable | Unit: immutability |
| **WORK-011.6**: Tag VO | Implement immutable | Unit: equality, hash |
| **WORK-011.7**: DomainEvent base | Implement base class | Unit: serialization |
| **WORK-011.8**: WorkItem events | All event types | Unit: payload validation |
| **WORK-011.9**: DomainException | Exception hierarchy | Unit: messages |
| **WORK-011.10**: WorkItem aggregate | Full implementation | BDD: all scenarios above |
| **WORK-011.11**: Port interfaces | Define protocols | Architecture: dependency direction |

### 12.2 Phase 3.2: Application Layer

| Task | Sub-tasks | Tests |
|------|-----------|-------|
| **WORK-012.1**: DTOs | All DTO classes | Unit: serialization |
| **WORK-012.2**: Commands | Command classes | Unit: validation |
| **WORK-012.3**: Queries | Query classes | Unit: defaults |
| **WORK-012.4**: CreateWorkItem handler | Implement | Integration: full flow |
| **WORK-012.5**: UpdateWorkItem handler | Implement | Integration: full flow |
| **WORK-012.6**: CompleteWorkItem handler | Implement | Integration: full flow |
| **WORK-012.7**: GetWorkItem handler | Implement | Integration: full flow |
| **WORK-012.8**: ListWorkItems handler | Implement | Integration: filtering |
| **WORK-012.9**: SearchWorkItems handler | Implement | Integration: search |

### 12.3 Phase 3.3: Infrastructure Layer

| Task | Sub-tasks | Tests |
|------|-----------|-------|
| **WORK-013.1**: SQLite schema | Design and create | Integration: migrations |
| **WORK-013.2**: SQLiteRepository | Implement IRepository | Integration: CRUD |
| **WORK-013.3**: SQLiteEventStore | Implement IEventStore | Integration: append/read |
| **WORK-013.4**: SQLiteUnitOfWork | Implement IUnitOfWork | Integration: transactions |
| **WORK-013.5**: EventDispatcher | Implement dispatcher | Unit: subscription |
| **WORK-013.6**: JSON schemas | Create schema files | Contract: validation |

### 12.4 Phase 3.4: Interface Layer

| Task | Sub-tasks | Tests |
|------|-----------|-------|
| **WORK-014.1**: CLI argument parser | Implement argparse | Unit: parsing |
| **WORK-014.2**: CLI formatters | Table, JSON output | Unit: formatting |
| **WORK-014.3**: CLI commands | All skill commands | E2E: full workflows |
| **WORK-014.4**: Error handling | User-friendly messages | E2E: error cases |

### 12.5 Phase 3.5: Integration & E2E

| Task | Sub-tasks | Tests |
|------|-----------|-------|
| **WORK-015.1**: Dependency wiring | Composition root | Architecture: DI |
| **WORK-015.2**: E2E test suite | Full workflow tests | E2E: happy paths |
| **WORK-015.3**: Edge case suite | Failure scenarios | E2E: edge cases |
| **WORK-015.4**: Performance tests | Load testing | Performance: benchmarks |

---

## 13. Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| SQLite concurrency limits | Medium | Medium | Use WAL mode, single-writer |
| Event replay performance | Low | Medium | Implement snapshots |
| Schema evolution | Medium | High | Version events, migration scripts |
| Test coverage gaps | Medium | High | Mutation testing, coverage gates |
| Context window pressure | Medium | High | Lazy loading, pagination |

---

## 14. References

### Primary Sources

1. Evans, E. (2003). "Domain-Driven Design: Tackling Complexity in the Heart of Software"
2. Vernon, V. (2013). "Implementing Domain-Driven Design"
3. Cockburn, A. (2005). "[Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)"
4. Percival, H. & Gregory, B. "[Architecture Patterns with Python](https://www.cosmicpython.com/)"
5. Microsoft. "[Event Sourcing Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)"
6. Fowler, M. "[Domain Event](https://martinfowler.com/eaaDev/DomainEvent.html)"

### Implementation References

7. "[Cosmic Python - CQRS](https://www.cosmicpython.com/book/chapter_12_cqrs.html)"
8. "[Cosmic Python - Repository Pattern](https://www.cosmicpython.com/book/chapter_02_repository.html)"
9. "[Cosmic Python - Unit of Work](https://www.cosmicpython.com/book/chapter_06_uow.html)"
10. "[pytest-bdd Documentation](https://pytest-bdd.readthedocs.io/)"
11. "[DDD in Python](https://dddinpython.com/)"
12. "[Atlassian JIRA Schema](https://support.atlassian.com/analytics/docs/schema-for-jira-software/)"

---

## Approval

| Role | Name | Status | Date |
|------|------|--------|------|
| **Author** | Claude | SUBMITTED | 2026-01-07 |
| **Reviewer** | User | PENDING | - |
| **Approver** | User | PENDING | - |

---

**Next Steps Upon Approval**:
1. Create detailed sub-task breakdown in WORKTRACKER.md
2. Begin Phase 3.1 with Domain Layer BDD tests
3. Implement WorkItemId value object (first RED test)
