# TD-017-E-002: Bounded Context Organization Patterns

> **Document ID**: td-017-e-002
> **PS ID**: TD-017
> **Entry ID**: e-002
> **Date**: 2026-01-11
> **Author**: ps-researcher agent (Opus 4.5)
> **Topic**: Bounded Context Organization Patterns
> **Status**: COMPLETE
>
> **Sources**:
> - Domain-Driven Hexagon: `/sairyss/domain-driven-hexagon` (Context7)
> - Martin Fowler: [Bounded Context](https://martinfowler.com/bliki/BoundedContext.html)
> - DDD-Crew: [Context Mapping](https://github.com/ddd-crew/context-mapping)
> - Python DDD Example: [pgorecki/python-ddd](https://github.com/pgorecki/python-ddd)
> - Jerry Design Canon: `PROJ-001-e-011-v1-jerry-design-canon.md`
> - Jerry Shared Kernel ADR: `PROJ-001-e-013-v2-adr-shared-kernel.md`

---

## L0: Executive Summary

This research document synthesizes industry best practices for organizing bounded contexts in Domain-Driven Design, specifically addressing directory structures, creation guidelines, inter-context communication, and context mapping patterns.

### Key Findings

| Area | Industry Pattern | Jerry Alignment |
|------|------------------|-----------------|
| **Directory Structure** | Application/Domain/Infrastructure per BC | ALIGNED - Current structure matches |
| **BC Creation** | Minimal viable files with layered structure | NEEDS TEMPLATE |
| **Inter-BC Communication** | Domain Events (internal), Integration Events (external) | ALIGNED - DomainEvent + CloudEvents |
| **Context Mapping** | 9 patterns (Partnership, Shared Kernel, ACL, etc.) | PARTIALLY IMPLEMENTED |
| **Shared Kernel** | Small, jointly-maintained, data structures only | ALIGNED - `src/shared_kernel/` |

### Recommendations

1. **BC Creation Template**: Create a project template/generator for new bounded contexts
2. **Integration Events**: Formalize distinction between domain events and integration events
3. **Context Map Documentation**: Document BC relationships using standard patterns
4. **Anti-Corruption Layer**: Add ACL pattern to pattern catalog for external integrations

---

## L1: Industry Patterns

### 1. Directory Structure per Bounded Context

**Industry Consensus**: Each bounded context should be a self-contained module with its own layered architecture.

#### Pattern: Layered BC Structure (Domain-Driven Hexagon)

```
{bounded_context}/
├── domain/                    # Core business logic
│   ├── aggregates/            # Aggregate roots
│   ├── entities/              # Domain entities
│   ├── value_objects/         # Immutable value objects
│   ├── events/                # Domain events (internal)
│   ├── services/              # Domain services
│   ├── ports/                 # Domain-level ports (IRepository)
│   └── exceptions.py          # Domain exceptions
│
├── application/               # Use cases
│   ├── commands/              # Command definitions
│   ├── queries/               # Query definitions
│   ├── handlers/              # Command/Query handlers
│   │   ├── commands/          # Command handlers
│   │   └── queries/           # Query handlers
│   ├── ports/                 # Application ports
│   │   ├── primary/           # Inbound (ICommandHandler, IQueryHandler)
│   │   └── secondary/         # Outbound (IEventStore, INotifier)
│   ├── services/              # Application services
│   └── dtos/                  # Data transfer objects
│
├── infrastructure/            # Technical adapters
│   ├── adapters/              # Port implementations
│   │   ├── persistence/       # Repository adapters
│   │   ├── messaging/         # Event bus adapters
│   │   └── external/          # External service adapters
│   ├── read_models/           # Materialized views
│   └── acl/                   # Anti-corruption layers
│
└── interface/                 # Primary adapters (optional)
    ├── cli/                   # CLI adapter
    ├── api/                   # HTTP API adapter
    └── events/                # Integration event handlers
```

**Source**: [Domain-Driven Hexagon](https://github.com/sairyss/domain-driven-hexagon) - "Commands directory contains all state changing use cases... Queries directory is structured in the same way as commands but contains data retrieval use cases."

#### Pattern: Module Independence (Domain-Driven Hexagon)

> "Try to make every module independent and keep interactions between modules minimal. Think of each module as a mini application bounded by a single context. Consider module internals private and try to avoid direct imports between modules."

**Key Principles**:
- Each BC is a "mini application"
- Internal imports are private
- External access through public interfaces only
- Loose coupling enables microservice extraction

**Source**: [Domain-Driven Hexagon](https://github.com/sairyss/domain-driven-hexagon)

---

### 2. Bounded Context Creation Guidelines

**Industry Consensus**: A new BC needs minimal viable structure with clear boundaries.

#### Minimal BC Checklist (Synthesized from Multiple Sources)

**Required Files**:

| Layer | Required | Optional |
|-------|----------|----------|
| **Domain** | `__init__.py`, `exceptions.py` | aggregates/, entities/, value_objects/, events/, services/, ports/ |
| **Application** | `__init__.py` | commands/, queries/, handlers/, ports/, services/, dtos/ |
| **Infrastructure** | `__init__.py` | adapters/, read_models/, acl/ |
| **Interface** | (optional) | cli/, api/, events/ |

**Minimal Viable BC**:

```
{new_context}/
├── __init__.py               # Public API exports
├── domain/
│   ├── __init__.py
│   └── exceptions.py         # Context-specific exceptions
├── application/
│   └── __init__.py
└── infrastructure/
    └── __init__.py
```

**Source**: Synthesized from [ddd-for-python](https://pypi.org/project/ddd-for-python/), [python-ddd](https://github.com/pgorecki/python-ddd), [DEV Community DDD File Structure](https://dev.to/stevescruz/domain-driven-design-ddd-file-structure-4pja)

#### BC Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| BC Directory | snake_case | `session_management/` |
| Module `__init__.py` | Explicit exports | `__all__ = [...]` |
| Domain Events | PascalCase past tense | `TaskCompleted` |
| Commands | PascalCase verb+noun | `CreateTaskCommand` |
| Queries | PascalCase verb+noun | `RetrieveTaskQuery` |

**Source**: Jerry Design Canon (aligned with industry patterns)

---

### 3. Inter-BC Communication Patterns

**Industry Consensus**: Bounded contexts should communicate through well-defined integration points, not direct imports.

#### Pattern: Domain Events vs Integration Events

| Aspect | Domain Events | Integration Events |
|--------|---------------|-------------------|
| **Scope** | Within BC | Across BC boundaries |
| **Audience** | Same context components | External contexts/systems |
| **Coupling** | Tight (same vocabulary) | Loose (public contract) |
| **Schema** | Internal format | Versioned public schema (CloudEvents) |
| **Delivery** | In-process dispatcher | Message broker/event bus |

**Source**: [Microsoft DevBlogs - Domain Events vs Integration Events](https://devblogs.microsoft.com/cesardelatorre/domain-events-vs-integration-events-in-domain-driven-design-and-microservices-architectures/)

> "Domain events are bounded context scoped and typically don't cross bounded context boundaries... Integration Events are used for communication between different bounded contexts."

#### Pattern: Event-Driven Communication

```
BC1 (Producer)                  BC2 (Consumer)
    │                               │
    │ DomainEvent                   │
    ▼                               │
[Event Handler] ───────────────────►│
    │                               │
    │ IntegrationEvent              │
    │ (CloudEvents format)          ▼
    └──────────────────────────►[ACL/Adapter]
                                    │
                                    ▼
                              [Internal Command]
```

**Key Rules**:
1. Domain events stay within BC
2. Integration events are published after persistence
3. Integration events use versioned schemas (CloudEvents 1.0)
4. Consuming BC uses ACL to translate to internal model

**Source**: [Cosmic Python - Event-Driven Architecture](https://www.cosmicpython.com/book/chapter_11_external_events.html)

#### Pattern: Shared Kernel Communication

> "A Shared Kernel is a special type of Bounded Context that contains code and data shared across multiple bounded contexts... Both contexts share a common code base which is the kernel."

**What to Include**:
- Identity types (VertexId, etc.)
- Base classes (DomainEvent, AggregateRoot)
- Common protocols (IAuditable, IVersioned)
- Domain exceptions hierarchy

**What NOT to Include**:
- Business logic
- Aggregates
- Application services
- Infrastructure code

**Source**: [DevIQ - Shared Kernel in DDD](https://deviq.com/domain-driven-design/shared-kernel/)

---

### 4. Context Mapping Patterns

**Industry Standard**: 9 patterns for describing BC relationships.

#### Context Map Pattern Catalog

| Pattern | Relationship | Use Case |
|---------|--------------|----------|
| **Partnership** | Mutually dependent | Two teams need joint delivery |
| **Shared Kernel** | Jointly maintained | Common domain objects |
| **Customer-Supplier** | Upstream/Downstream | Producer/consumer relationship |
| **Conformist** | Downstream conforms | Accept upstream model as-is |
| **Anti-Corruption Layer** | Downstream isolates | Translate upstream to internal model |
| **Open Host Service** | Upstream provides API | Well-documented public interface |
| **Published Language** | Shared language | CloudEvents, JSON, Protobuf |
| **Separate Ways** | Independent | No integration needed |
| **Big Ball of Mud** | Demarcated mess | Legacy system boundary |

**Source**: [DDD-Crew Context Mapping](https://github.com/ddd-crew/context-mapping), [Context Mapper](https://contextmapper.org/docs/context-map/)

#### Upstream/Downstream Semantics

> "The upstream/downstream relationship means that the effects of the upstream team are felt by the downstream team. However, changes made by the downstream team do not significantly impact the upstream."

**Upstream Patterns**: Open Host Service (OHS), Published Language (PL)
**Downstream Patterns**: Conformist (CF), Anti-Corruption Layer (ACL)

**Source**: [TechTarget - Using bounded context for effective DDD](https://www.techtarget.com/searchapparchitecture/tip/Using-bounded-context-for-effective-domain-driven-design)

---

## L2: Jerry-Specific Recommendations

### Current Jerry BC Structure

```
src/
├── session_management/        # BC: Project and session handling
│   ├── domain/
│   │   ├── aggregates/
│   │   ├── entities/
│   │   ├── events/
│   │   └── value_objects/
│   ├── application/
│   │   ├── ports/
│   │   └── queries/
│   └── infrastructure/
│
├── work_tracking/             # BC: Task and work item management
│   ├── domain/
│   │   ├── aggregates/
│   │   ├── events/
│   │   ├── ports/
│   │   ├── services/
│   │   └── value_objects/
│   └── infrastructure/
│
├── shared_kernel/             # Cross-context shared code
│   ├── vertex_id.py
│   ├── domain_event.py
│   ├── entity_base.py
│   └── exceptions.py
│
└── application/               # Top-level application (dispatchers, shared handlers)
    ├── dispatchers/
    ├── handlers/
    ├── ports/
    ├── projections/
    └── queries/
```

**Assessment**: Jerry's current structure aligns with industry patterns. Key strengths:
- Clear BC separation
- Shared kernel properly scoped
- Hexagonal layering within each BC

### Recommendation 1: BC Creation Template

Create a template for generating new bounded contexts.

**Proposed Template**: `scripts/create_bounded_context.py`

```python
#!/usr/bin/env python3
"""Generate a new bounded context with standard structure."""

import argparse
from pathlib import Path

STRUCTURE = {
    "domain": {
        "__init__.py": '"""Domain layer for {name}."""\n',
        "exceptions.py": '"""Domain exceptions for {name}."""\n\nfrom src.shared_kernel import DomainError\n',
        "aggregates/__init__.py": "",
        "entities/__init__.py": "",
        "events/__init__.py": "",
        "value_objects/__init__.py": "",
        "ports/__init__.py": "",
        "services/__init__.py": "",
    },
    "application": {
        "__init__.py": '"""Application layer for {name}."""\n',
        "commands/__init__.py": "",
        "queries/__init__.py": "",
        "handlers/__init__.py": "",
        "handlers/commands/__init__.py": "",
        "handlers/queries/__init__.py": "",
        "ports/__init__.py": "",
        "services/__init__.py": "",
        "dtos/__init__.py": "",
    },
    "infrastructure": {
        "__init__.py": '"""Infrastructure layer for {name}."""\n',
        "adapters/__init__.py": "",
        "adapters/persistence/__init__.py": "",
        "adapters/messaging/__init__.py": "",
    },
}

def create_bc(name: str, path: Path) -> None:
    """Create bounded context directory structure."""
    bc_path = path / name
    for layer, files in STRUCTURE.items():
        for file_path, content in files.items():
            full_path = bc_path / layer / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content.format(name=name))

    # Create root __init__.py
    (bc_path / "__init__.py").write_text(f'"""Bounded Context: {name}."""\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="BC name in snake_case")
    parser.add_argument("--path", default="src", help="Base path")
    args = parser.parse_args()
    create_bc(args.name, Path(args.path))
```

### Recommendation 2: Context Map Documentation

Document Jerry's BC relationships using standard patterns.

**Jerry Context Map**:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Jerry Framework                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────┐         ┌───────────────────┐           │
│  │ session_management│         │   work_tracking   │           │
│  │                   │◄───────►│                   │           │
│  │  [Downstream]     │   SK    │    [Downstream]   │           │
│  └─────────┬─────────┘         └─────────┬─────────┘           │
│            │                             │                      │
│            │ SK                          │ SK                   │
│            ▼                             ▼                      │
│  ┌─────────────────────────────────────────────────┐           │
│  │               shared_kernel                      │           │
│  │                                                  │           │
│  │  - VertexId hierarchy    - DomainEvent          │           │
│  │  - IAuditable           - CloudEventEnvelope    │           │
│  │  - IVersioned           - AggregateRoot         │           │
│  │  - EntityBase           - Exceptions            │           │
│  └─────────────────────────────────────────────────┘           │
│                                                                 │
│  ┌───────────────────┐         ┌───────────────────┐           │
│  │ problem_solving   │         │  (future BCs)     │           │
│  │    (future)       │         │                   │           │
│  └───────────────────┘         └───────────────────┘           │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Legend:                                                         │
│   SK = Shared Kernel                                            │
│   ◄──► = Partnership (mutually dependent)                       │
│   ──► = Customer-Supplier (upstream to downstream)              │
│   ACL = Anti-Corruption Layer (for external systems)            │
└─────────────────────────────────────────────────────────────────┘
```

**BC Relationships**:

| Source BC | Target BC | Pattern | Notes |
|-----------|-----------|---------|-------|
| session_management | shared_kernel | Shared Kernel | Uses identity, events, base classes |
| work_tracking | shared_kernel | Shared Kernel | Uses identity, events, aggregates |
| session_management | work_tracking | Partnership | Both need project context |
| work_tracking | External (ADO) | ACL + OHS | CloudEvents for integration |

### Recommendation 3: Integration Event Formalization

Formalize the distinction between domain events and integration events.

**Current State**: Jerry has `DomainEvent` and `CloudEventEnvelope` but doesn't formally distinguish internal vs external events.

**Proposed Enhancement**:

```python
# src/shared_kernel/integration_event.py
"""
IntegrationEvent - Events published across BC boundaries.

Integration events are public contracts that:
1. Use CloudEvents 1.0 format
2. Are versioned (never break consumers)
3. Are published after domain event persistence

References:
    - CNCF CloudEvents: https://cloudevents.io/
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .cloud_events import CloudEventEnvelope
from .domain_event import DomainEvent


@dataclass(frozen=True)
class IntegrationEvent:
    """
    Base class for events published across bounded contexts.

    Usage:
        # In application layer event handler:
        domain_event = task.complete()
        if domain_event:
            integration_event = TaskCompletedIntegration.from_domain(domain_event)
            event_bus.publish(integration_event)
    """

    envelope: CloudEventEnvelope

    @classmethod
    def from_domain_event(cls, event: DomainEvent) -> IntegrationEvent:
        """Convert domain event to integration event."""
        return cls(envelope=event.to_cloud_event())

    def to_dict(self) -> dict[str, Any]:
        """Serialize for transmission."""
        return self.envelope.to_dict()
```

### Recommendation 4: Anti-Corruption Layer Pattern

Add ACL pattern to pattern catalog for external integrations.

**Proposed Pattern**: `PAT-ACL-001`

```python
# src/{bc}/infrastructure/acl/{external_system}_translator.py
"""
Anti-Corruption Layer - Translate external models to internal domain.

The ACL protects the domain from corruption by external system models.
It acts as a translator/adapter between external and internal representations.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TExternal = TypeVar("TExternal")
TInternal = TypeVar("TInternal")


class ITranslator(ABC, Generic[TExternal, TInternal]):
    """Port for translating between external and internal models."""

    @abstractmethod
    def to_internal(self, external: TExternal) -> TInternal:
        """Translate external model to internal domain model."""
        ...

    @abstractmethod
    def to_external(self, internal: TInternal) -> TExternal:
        """Translate internal domain model to external format."""
        ...


# Example: ADO Integration
class AdoWorkItemTranslator(ITranslator[dict, "WorkItem"]):
    """Translate ADO work items to Jerry WorkItems."""

    def to_internal(self, external: dict) -> "WorkItem":
        """Convert ADO JSON to WorkItem aggregate."""
        return WorkItem.create(
            title=external["fields"]["System.Title"],
            work_type=self._map_work_type(external["fields"]["System.WorkItemType"]),
            status=self._map_status(external["fields"]["System.State"]),
        )

    def to_external(self, internal: "WorkItem") -> dict:
        """Convert WorkItem to ADO JSON format."""
        return {
            "op": "add",
            "path": "/fields/System.Title",
            "value": internal.title,
        }
```

---

## L3: BC Creation Checklist

### New Bounded Context Checklist

When creating a new bounded context in Jerry:

#### Phase 1: Structure Creation

- [ ] Create BC directory: `src/{bc_name}/`
- [ ] Create `__init__.py` with public API exports
- [ ] Create domain layer:
  - [ ] `domain/__init__.py`
  - [ ] `domain/exceptions.py` (extends shared_kernel.DomainError)
  - [ ] `domain/aggregates/` (if needed)
  - [ ] `domain/entities/` (if needed)
  - [ ] `domain/value_objects/` (if needed)
  - [ ] `domain/events/` (if needed)
  - [ ] `domain/ports/` (if needed)
- [ ] Create application layer:
  - [ ] `application/__init__.py`
  - [ ] `application/commands/` (if needed)
  - [ ] `application/queries/` (if needed)
  - [ ] `application/handlers/commands/` (if needed)
  - [ ] `application/handlers/queries/` (if needed)
- [ ] Create infrastructure layer:
  - [ ] `infrastructure/__init__.py`
  - [ ] `infrastructure/adapters/` (if needed)

#### Phase 2: Shared Kernel Integration

- [ ] Import identity types from shared_kernel (VertexId subclass if needed)
- [ ] Import base classes (DomainEvent, AggregateRoot)
- [ ] Import protocols (IAuditable, IVersioned)
- [ ] Import exceptions (DomainError hierarchy)

#### Phase 3: Context Map Update

- [ ] Document BC in context map
- [ ] Identify upstream/downstream relationships
- [ ] Determine integration patterns (Partnership, ACL, etc.)
- [ ] Define integration events if cross-BC communication needed

#### Phase 4: Testing

- [ ] Create `tests/unit/{bc_name}/` directory
- [ ] Add domain layer unit tests
- [ ] Add application layer unit tests
- [ ] Add architecture tests for layer boundaries

#### Phase 5: Registration

- [ ] Update `src/bootstrap.py` with BC registrations
- [ ] Update pattern catalog if new patterns introduced
- [ ] Update CLAUDE.md if needed

---

## References

### Primary Sources

| Source | Type | URL/Location |
|--------|------|--------------|
| Domain-Driven Hexagon | Guide | [GitHub](https://github.com/sairyss/domain-driven-hexagon) |
| Context Mapping | Patterns | [GitHub](https://github.com/ddd-crew/context-mapping) |
| Martin Fowler - Bounded Context | Bliki | [martinfowler.com](https://martinfowler.com/bliki/BoundedContext.html) |
| python-ddd | Example | [GitHub](https://github.com/pgorecki/python-ddd) |
| ddd-for-python | Framework | [PyPI](https://pypi.org/project/ddd-for-python/) |

### Industry Articles

| Source | Topic | URL |
|--------|-------|-----|
| Microsoft DevBlogs | Domain vs Integration Events | [devblogs.microsoft.com](https://devblogs.microsoft.com/cesardelatorre/domain-events-vs-integration-events-in-domain-driven-design-and-microservices-architectures/) |
| TechTarget | Bounded Context Best Practices | [techtarget.com](https://www.techtarget.com/searchapparchitecture/tip/Using-bounded-context-for-effective-domain-driven-design) |
| Cosmic Python | External Events | [cosmicpython.com](https://www.cosmicpython.com/book/chapter_11_external_events.html) |
| DevIQ | Shared Kernel | [deviq.com](https://deviq.com/domain-driven-design/shared-kernel/) |
| Context Mapper | Context Map DSL | [contextmapper.org](https://contextmapper.org/docs/context-map/) |
| DEV Community | DDD File Structure | [dev.to](https://dev.to/stevescruz/domain-driven-design-ddd-file-structure-4pja) |

### Jerry Internal Sources

| Document | Location |
|----------|----------|
| Jerry Design Canon | `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-011-v1-jerry-design-canon.md` |
| Shared Kernel ADR v2 | `projects/PROJ-001-plugin-cleanup/decisions/PROJ-001-e-013-v2-adr-shared-kernel.md` |
| Pattern Catalog | `.claude/patterns/PATTERN-CATALOG.md` |
| Architecture Standards | `.claude/rules/architecture-standards.md` |
| File Organization | `.claude/rules/file-organization.md` |

---

*Document created by ps-researcher agent (Opus 4.5)*
*Research completed: 2026-01-11*
*Status: COMPLETE - Ready for synthesis*
