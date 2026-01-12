# Research: Domain Layer Implementation - 5W1H Analysis

**ID**: IMPL-R-001
**Date**: 2026-01-09
**Author**: Claude (Distinguished Systems Engineer)
**Status**: COMPLETE
**Branch**: cc/task-subtask

---

## Executive Summary

This document provides comprehensive 5W1H analysis for implementing the domain layer of the Jerry Framework development skill. The analysis synthesizes research from authoritative sources including the Domain-Driven Hexagon guide, Cosmic Python, and the Python eventsourcing library documentation.

---

## 1. WHAT - What Are We Building?

### 1.1 Domain Layer Components

Based on ADR-001 through ADR-009 and DDD best practices, we need to implement:

#### Value Objects (Immutable, Equality by Value)
| Component | Purpose | ADR Reference |
|-----------|---------|---------------|
| `SnowflakeId` | Coordination-free unique ID generation | ADR-007 |
| `WorkItemId` | Hybrid ID (Snowflake internal + display) | ADR-007 |
| `SessionId` | Session identifier for event scoping | ADR-009 |
| `QualityLevel` | L0/L1/L2 quality gate level | ADR-008 |
| `RiskProfile` | T1-T4 risk tier classification | ADR-008 |
| `EnforcementLevel` | HARD/SOFT/GATE_ONLY/NONE | ADR-001 |

#### Entities (Identity, Mutable State)
| Component | Purpose | ADR Reference |
|-----------|---------|---------------|
| `WorkItem` | Task/bug/feature tracking entity | ADR-007 |
| `Session` | Agent execution session | ADR-009 |
| `QualityGate` | Quality gate configuration | ADR-008 |

#### Aggregates (Consistency Boundaries)
| Component | Purpose | ADR Reference |
|-----------|---------|---------------|
| `WorkItemAggregate` | Work item with subtasks | ADR-007 |
| `SessionAggregate` | Session with events | ADR-009 |

#### Domain Events (Immutable, Past Tense)
| Event | Trigger | ADR Reference |
|-------|---------|---------------|
| `WorkItemCreated` | New work item | ADR-009 |
| `WorkItemStatusChanged` | Status transition | ADR-009 |
| `SessionStarted` | Session begins | ADR-009 |
| `SessionEnded` | Session completes | ADR-009 |
| `QualityGatePassed` | Gate validation success | ADR-008 |
| `QualityGateFailed` | Gate validation failure | ADR-008 |

#### Domain Services
| Service | Purpose | ADR Reference |
|---------|---------|---------------|
| `SnowflakeIdGenerator` | Generate Snowflake IDs | ADR-007 |
| `QualityGateValidator` | Validate against gates | ADR-008 |
| `EventPublisher` | Publish domain events | ADR-009 |

#### Ports (Interfaces)
| Port | Type | Purpose |
|------|------|---------|
| `IWorkItemRepository` | Secondary | Work item persistence |
| `ISessionRepository` | Secondary | Session persistence |
| `IEventStore` | Secondary | Event storage |
| `IFileLock` | Secondary | File locking mechanism |

### 1.2 What We Are NOT Building (Scope Exclusions)

Per c-011 compliance (ADR-009, e-008):
- ❌ `DeploymentAdapter` - OUT OF SCOPE (post-MVP)
- ❌ `MutationTestAdapter` - PHASE 5 BACKLOG
- ❌ Full event replay capability - Audit-trail level for MVP
- ❌ External message brokers - Session-scoped buffer only

---

## 2. WHY - Why Is This Needed?

### 2.1 Business Justification

| Driver | Rationale | Evidence |
|--------|-----------|----------|
| Context Rot | LLM performance degrades with context fill | [Chroma Research](https://research.trychroma.com/context-rot) |
| Multi-Instance | Multiple Claude instances need coordination-free IDs | R-005 Critical Risk (e-010) |
| Quality Gates | Enforce quality criteria without manual tracking | ADR-008 |
| Audit Trail | Track all state changes for analytics/debugging | ADR-009 |
| Testability | Domain logic must be pure and testable | P-BDD Principle |

### 2.2 Technical Justification

| Pattern | Benefit | Reference |
|---------|---------|-----------|
| DDD Domain Layer | Business logic isolation | [Cosmic Python Ch1](https://www.cosmicpython.com/book/chapter_01_domain_model.html) |
| Value Objects | Immutability, no side effects | [Domain-Driven Hexagon](https://github.com/sairyss/domain-driven-hexagon) |
| Event Sourcing | Complete audit trail, analytics | [eventsourcing library](https://eventsourcing.readthedocs.io/) |
| Hexagonal Architecture | Dependency inversion, testability | ADR-003 |

### 2.3 Why Now?

- ENFORCE-008d (domain refactoring) is PAUSED waiting for this
- Development skill requires domain foundation
- 0% test coverage on session_management domain is unacceptable

---

## 3. WHO - Who Is Affected?

### 3.1 Stakeholders

| Stakeholder | Impact | Concern |
|-------------|--------|---------|
| Claude Agents | Primary | Will use domain entities for work tracking |
| Human Users | Secondary | Will see work item status in WORKTRACKER.md |
| Orchestrator | Primary | Will spawn agents that use domain |
| QA Agent | Primary | Will validate domain behavior |

### 3.2 Components Affected

| Component | Change Type | Risk |
|-----------|-------------|------|
| `src/shared_kernel/` | Extension | Low - Add Snowflake ID |
| `src/session_management/domain/` | Major refactor | Medium - Add events |
| `src/work_tracking/domain/` | New bounded context | Low - Greenfield |
| `tests/` | Major extension | Low - Additive |

---

## 4. WHERE - Where In The Codebase?

### 4.1 Directory Structure

```
src/
├── shared_kernel/                    # Cross-cutting concerns
│   ├── __init__.py
│   ├── vertex_id.py                  # Existing - extend
│   ├── snowflake_id.py               # NEW - ADR-007
│   ├── entity_base.py                # Existing
│   ├── domain_event.py               # NEW - ADR-009
│   └── exceptions.py                 # Existing
│
├── work_tracking/                    # NEW bounded context
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── value_objects/
│   │   │   ├── __init__.py
│   │   │   ├── work_item_id.py       # Hybrid ID (ADR-007)
│   │   │   ├── quality_level.py      # L0/L1/L2 (ADR-008)
│   │   │   ├── risk_profile.py       # T1-T4 (ADR-008)
│   │   │   └── enforcement_level.py  # HARD/SOFT/... (ADR-001)
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── work_item.py          # Work item entity
│   │   │   └── quality_gate.py       # Quality gate entity
│   │   ├── aggregates/
│   │   │   ├── __init__.py
│   │   │   └── work_item_aggregate.py
│   │   ├── events/
│   │   │   ├── __init__.py
│   │   │   ├── work_item_events.py   # WorkItemCreated, etc.
│   │   │   └── quality_gate_events.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── id_generator.py       # SnowflakeIdGenerator
│   │   │   └── quality_validator.py
│   │   └── exceptions.py
│   │
│   ├── application/                  # Use cases (future)
│   │   └── ports/
│   │       ├── __init__.py
│   │       └── work_item_repository.py
│   │
│   └── infrastructure/               # Adapters (future)
│       └── __init__.py
│
└── session_management/               # Existing - extend
    └── domain/
        └── events/
            └── session_events.py     # NEW - SessionStarted, etc.
```

### 4.2 Test Directory Structure

```
tests/
├── shared_kernel/                    # Existing - extend
│   ├── test_snowflake_id.py          # NEW
│   └── test_domain_event.py          # NEW
│
├── work_tracking/                    # NEW
│   ├── unit/
│   │   ├── domain/
│   │   │   ├── test_work_item_id.py
│   │   │   ├── test_work_item.py
│   │   │   ├── test_quality_level.py
│   │   │   └── test_id_generator.py
│   │   └── conftest.py
│   ├── integration/
│   │   └── test_work_item_repository.py
│   ├── contract/
│   │   └── test_repository_interface.py
│   └── architecture/
│       └── test_layer_boundaries.py
│
└── features/                         # BDD feature files
    ├── work_tracking/
    │   ├── work_item_creation.feature
    │   ├── work_item_status.feature
    │   └── quality_gates.feature
    └── shared_kernel/
        └── snowflake_id.feature
```

---

## 5. WHEN - When Can We Start?

### 5.1 Prerequisites (All Met)

| Prerequisite | Status | Evidence |
|--------------|--------|----------|
| pytest-bdd installed | ✅ | `uv pip install` completed |
| pytest-archon installed | ✅ | `uv pip install` completed |
| ADRs complete | ✅ | ADR-001 to ADR-009 |
| Research complete | ✅ | This document |
| Test baseline | ✅ | 58 tests passing (shared_kernel) |

### 5.2 Dependencies

```
shared_kernel/snowflake_id.py
    ↓
work_tracking/domain/value_objects/work_item_id.py
    ↓
work_tracking/domain/entities/work_item.py
    ↓
work_tracking/domain/aggregates/work_item_aggregate.py
    ↓
work_tracking/domain/events/work_item_events.py
```

### 5.3 Implementation Order

| Phase | Component | Tests Required | Est. Tests |
|-------|-----------|----------------|------------|
| 1 | `SnowflakeIdGenerator` | Unit (happy, edge, negative) | 15 |
| 2 | `WorkItemId` | Unit | 10 |
| 3 | Value Objects (Quality, Risk, Enforcement) | Unit | 20 |
| 4 | `WorkItem` entity | Unit | 15 |
| 5 | `QualityGate` entity | Unit | 10 |
| 6 | Domain events | Unit | 15 |
| 7 | `WorkItemAggregate` | Unit + Integration | 20 |
| 8 | Domain services | Unit | 15 |
| 9 | Architecture tests | Architecture | 10 |
| **Total** | | | **~130** |

---

## 6. HOW - How Will We Implement?

### 6.1 BDD Red/Green/Refactor Cycle

For each component:

```
1. WRITE FEATURE FILE (Gherkin)
   └── Define acceptance criteria in business language

2. RED PHASE
   ├── Generate step definitions
   ├── Write unit tests (pytest)
   └── Run tests → ALL FAIL (expected)

3. GREEN PHASE
   ├── Implement minimal code to pass
   ├── Run tests → ALL PASS
   └── Commit checkpoint

4. REFACTOR PHASE
   ├── Improve design without changing behavior
   ├── Run tests → STILL PASS
   └── Commit final
```

### 6.2 Test Pyramid Per Component

```
Component: WorkItemId
├── Feature: work_item_id.feature (acceptance)
├── Unit Tests: test_work_item_id.py
│   ├── Happy path: valid ID creation
│   ├── Edge cases: boundary values
│   ├── Negative: invalid inputs
│   └── Boundary: max/min values
├── Contract Tests: test_value_object_contract.py
│   └── Verify immutability, equality
└── Architecture Tests: test_layer_boundaries.py
    └── Verify no infrastructure imports
```

### 6.3 Implementation Patterns

#### Value Object Pattern (Python)
```python
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class WorkItemId:
    """Hybrid ID combining Snowflake internal + display ID."""
    internal_id: int  # Snowflake
    display_id: str   # WORK-042

    def __post_init__(self) -> None:
        if self.internal_id < 0:
            raise ValueError("Internal ID must be non-negative")
        if not self.display_id.startswith("WORK-"):
            raise ValueError("Display ID must start with WORK-")
```

#### Entity Pattern (Python)
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class WorkItem:
    """Work item entity with identity and mutable state."""
    id: WorkItemId
    title: str
    status: WorkItemStatus = WorkItemStatus.PENDING
    _events: List[DomainEvent] = field(default_factory=list, repr=False)

    def complete(self) -> None:
        if self.status == WorkItemStatus.COMPLETED:
            raise InvalidStateError("Already completed")
        self.status = WorkItemStatus.COMPLETED
        self._events.append(WorkItemStatusChanged(self.id, self.status))
```

#### Domain Event Pattern (Python)
```python
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class DomainEvent:
    """Base class for all domain events."""
    event_id: EventId
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass(frozen=True)
class WorkItemCreated(DomainEvent):
    """Raised when a work item is created."""
    work_item_id: WorkItemId
    title: str
```

### 6.4 Architecture Test Pattern (pytest-archon)

```python
from pytest_archon import archrule

def test_domain_layer_independence():
    """Domain layer must not import from infrastructure."""
    (
        archrule("domain_independence")
        .match("src.work_tracking.domain.*")
        .should_not_import("src.work_tracking.infrastructure.*")
        .should_not_import("src.work_tracking.application.*")
        .check("src")
    )
```

---

## 7. References & Citations

### Primary Sources

1. **Evans, Eric**. *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley, 2003.

2. **Vernon, Vaughn**. *Implementing Domain-Driven Design*. Addison-Wesley, 2013.

3. **Percival, Harry & Gregory, Bob**. [*Architecture Patterns with Python (Cosmic Python)*](https://www.cosmicpython.com/book/chapter_01_domain_model.html). O'Reilly, 2020.

4. **Sairyss**. [Domain-Driven Hexagon](https://github.com/sairyss/domain-driven-hexagon). GitHub, 2024.

### Python-Specific

5. **pyeventsourcing**. [eventsourcing library](https://eventsourcing.readthedocs.io/). v9.5.0, 2025.

6. **pytest-bdd**. [pytest-bdd documentation](https://pytest-bdd.readthedocs.io/). v8.1.0, 2025.

7. **pytest-archon**. [pytest-archon](https://pypi.org/project/pytest-archon/). v0.0.7, 2024.

### Jerry Framework ADRs

8. ADR-001: Test-First Enforcement
9. ADR-006: File Locking Strategy
10. ADR-007: ID Generation Strategy (Snowflake)
11. ADR-008: Quality Gate Configuration
12. ADR-009: Event Storage Mechanism

### Industry Best Practices

13. **Fowler, Martin**. [DDD Aggregate](https://martinfowler.com/bliki/DDD_Aggregate.html). martinfowler.com.

14. **microservices.io**. [Event Sourcing Pattern](https://microservices.io/patterns/data/event-sourcing.html).

15. **IEEE Study (2025)**. "30% of DDD projects fail due to over-modeling—start small."

---

## 8. Self-Critique & Risk Assessment

### What Could Go Wrong?

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Over-engineering domain | Medium | High | Start with minimal viable entities |
| Test coverage gaps | Low | High | Strict 90%+ gate before moving layers |
| Event schema evolution | Medium | Medium | Use versioned events from start |
| Snowflake clock skew | Low | Medium | Wait-for-next-millisecond strategy |

### Assumptions Made

1. **Python 3.11+ available** - Required for modern type hints
2. **No external dependencies in domain** - stdlib only
3. **Filesystem is shared resource** - Multiple instances, same filesystem
4. **Session-scoped events sufficient** - No cross-session replay needed for MVP

### Open Questions (None Blocking)

1. Should we use `dataclasses` or `attrs` for entities? → Decision: `dataclasses` (stdlib)
2. Should events be stored in JSON or MessagePack? → Decision: JSON (human-readable)

---

*Document Version: 1.0*
*Last Updated: 2026-01-09*
