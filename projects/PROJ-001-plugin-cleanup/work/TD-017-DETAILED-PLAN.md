# TD-017: Comprehensive Design Canon Implementation Plan

> **Status**: 🔄 IN PROGRESS
> **Priority**: HIGH
> **Created**: 2026-01-11
> **Purpose**: Detailed implementation plan for capturing ALL patterns and rules in Jerry repository

---

## Executive Summary

This document provides a DETAILED PLAN for TD-017 based on comprehensive repository exploration.
The plan captures ALL 40+ patterns and rules that need to be documented in `.claude/rules/` and `.claude/patterns/`.

---

## Part 1: Complete Pattern Inventory

Based on thorough repository exploration, here are ALL patterns identified:

### 1.1 Identity Patterns (4 patterns)

| Pattern ID | Name | Status | Location | Description |
|------------|------|--------|----------|-------------|
| PAT-ID-001 | VertexId | MANDATORY | `src/shared_kernel/vertex_id.py` | Graph-ready base class for all entity IDs |
| PAT-ID-002 | Domain-Specific IDs | MANDATORY | `src/shared_kernel/vertex_id.py` | TaskId, PhaseId, PlanId, SubtaskId, etc. |
| PAT-ID-003 | JerryUri | RECOMMENDED | Future | `jerry://entity_type/id` format |
| PAT-ID-004 | Snowflake ID Generator | MANDATORY | `src/shared_kernel/snowflake_id.py` | Twitter Snowflake algorithm |

### 1.2 Entity Patterns (5 patterns)

| Pattern ID | Name | Status | Location | Description |
|------------|------|--------|----------|-------------|
| PAT-ENT-001 | IAuditable | MANDATORY | `src/shared_kernel/auditable.py` | created_by, created_at, updated_by, updated_at |
| PAT-ENT-002 | IVersioned | MANDATORY | `src/shared_kernel/versioned.py` | Optimistic concurrency control |
| PAT-ENT-003 | AggregateRoot | MANDATORY | `src/work_tracking/domain/aggregates/base.py` | Event-sourced aggregate base |
| PAT-ENT-004 | EntityBase | RECOMMENDED | `src/shared_kernel/entity_base.py` | Combined VertexId + Auditable + Versioned |
| PAT-ENT-005 | Vertex/Edge | RECOMMENDED | Future | Graph-ready entities |

### 1.3 Aggregate Patterns (4 patterns)

| Pattern ID | Name | Status | Location | Description |
|------------|------|--------|----------|-------------|
| PAT-AGG-001 | WorkItem | MANDATORY | `src/work_tracking/domain/aggregates/work_item.py` | Primary aggregate root |
| PAT-AGG-002 | Event Collection | MANDATORY | AggregateRoot base | `_raise_event()`, `collect_events()` |
| PAT-AGG-003 | History Replay | MANDATORY | AggregateRoot base | `load_from_history()` for reconstitution |
| PAT-AGG-004 | Invariant Enforcement | MANDATORY | Aggregate methods | Self-validating aggregate rules |

### 1.4 Event Patterns (4 patterns)

| Pattern ID | Name | Status | Location | Description |
|------------|------|--------|----------|-------------|
| PAT-EVT-001 | DomainEvent | MANDATORY | `src/shared_kernel/domain_event.py` | Base class for all domain events |
| PAT-EVT-002 | CloudEvents | MANDATORY | External interface | CNCF standard for integration events |
| PAT-EVT-003 | Work Item Events | MANDATORY | `src/work_tracking/domain/events/` | WorkItemCreated, StatusChanged, etc. |
| PAT-EVT-004 | Event Registry | MANDATORY | `src/shared_kernel/domain_event.py` | Polymorphic deserialization |

### 1.5 CQRS Patterns (4 patterns)

| Pattern ID | Name | Status | Location | Description |
|------------|------|--------|----------|-------------|
| PAT-CQRS-001 | Command Pattern | MANDATORY | `src/application/commands/` | Immutable command DTOs |
| PAT-CQRS-002 | Query Pattern | MANDATORY | `src/application/queries/` | Immutable query DTOs |
| PAT-CQRS-003 | Dispatcher Pattern | MANDATORY | `src/application/dispatchers/` | Route handlers without coupling |
| PAT-CQRS-004 | Projection Pattern | RECOMMENDED | `src/application/projections/` | Materialized views |

### 1.6 Repository Patterns (3 patterns)

| Pattern ID | Name | Status | Location | Description |
|------------|------|--------|----------|-------------|
| PAT-REPO-001 | Generic Repository | MANDATORY | `src/work_tracking/domain/ports/repository.py` | `IRepository[T, TId]` port |
| PAT-REPO-002 | Event Store | MANDATORY | `src/work_tracking/domain/ports/event_store.py` | `IEventStore` port |
| PAT-REPO-003 | Snapshot Store | RECOMMENDED | Future | Aggregate snapshot persistence |

### 1.7 Value Object Patterns (3 patterns)

| Pattern ID | Name | Status | Location | Description |
|------------|------|--------|----------|-------------|
| PAT-VO-001 | Immutable Value Objects | MANDATORY | All VOs | `@dataclass(frozen=True)` |
| PAT-VO-002 | State Machine VO | MANDATORY | `WorkItemStatus` | `can_transition_to()`, validation |
| PAT-VO-003 | Factory Methods | MANDATORY | All VOs | `from_string()`, `from_int()` |

### 1.8 Domain Service Patterns (2 patterns)

| Pattern ID | Name | Status | Location | Description |
|------------|------|--------|----------|-------------|
| PAT-SVC-001 | Quality Gate Validator | MANDATORY | `src/work_tracking/domain/services/` | Stateless validation service |
| PAT-SVC-002 | ID Generator Service | MANDATORY | `src/work_tracking/domain/services/` | Domain-aware ID generation |

### 1.9 Architecture Patterns (5 patterns)

| Pattern ID | Name | Status | Location | Description |
|------------|------|--------|----------|-------------|
| PAT-ARCH-001 | Hexagonal Architecture | MANDATORY | All of src/ | Ports & Adapters structure |
| PAT-ARCH-002 | Primary/Secondary Ports | MANDATORY | `src/application/ports/` | Inbound/outbound contracts |
| PAT-ARCH-003 | Bounded Contexts | MANDATORY | `session_management/`, `work_tracking/` | BC structure |
| PAT-ARCH-004 | One-Class-Per-File | MANDATORY | All Python files | LLM optimization |
| PAT-ARCH-005 | Composition Root | MANDATORY | `src/bootstrap.py` | DI wiring |

### 1.10 Adapter Patterns (3 patterns)

| Pattern ID | Name | Status | Location | Description |
|------------|------|--------|----------|-------------|
| PAT-ADAPT-001 | Secondary Adapter | MANDATORY | `infrastructure/adapters/` | Implements outbound ports |
| PAT-ADAPT-002 | Primary Adapter (CLI) | MANDATORY | `src/interface/cli/adapter.py` | Inbound port implementation |
| PAT-ADAPT-003 | In-Memory Adapter | RECOMMENDED | Testing adapters | Test doubles for ports |

### 1.11 Testing Patterns (3 patterns)

| Pattern ID | Name | Status | Location | Description |
|------------|------|--------|----------|-------------|
| PAT-TEST-001 | BDD Red/Green/Refactor | MANDATORY | All tests | TDD cycle |
| PAT-TEST-002 | Test Pyramid | MANDATORY | `tests/` structure | 60% unit, 15% integration, etc. |
| PAT-TEST-003 | Architecture Tests | MANDATORY | `tests/architecture/` | Layer boundary enforcement |

---

## Part 2: Complete Rules Inventory

### 2.1 Existing Rules (to enhance)

| File | Current Coverage | Gaps |
|------|-----------------|------|
| `coding-standards.md` | 85% | Module docstrings, `__post_init__` validation, logging |
| `architecture-standards.md` | 90% | BC mapping patterns, snapshot strategy, versioning |
| `file-organization.md` | 95% | URI specification reference |
| `testing-standards.md` | 92% | Snapshot testing, property-based testing |

### 2.2 New Rules to Create

| File | Purpose | Priority |
|------|---------|----------|
| `error-handling-standards.md` | Exception hierarchy, context storage, when to use each | HIGH |
| `tool-configuration.md` | Python, Ruff, Mypy, Pytest, Editor settings | MEDIUM |

### 2.3 Rules Gaps to Address

| Gap ID | Category | Current | Required |
|--------|----------|---------|----------|
| GAP-R-001 | Module Docstrings | Brief mention | Full pattern with lifecycle |
| GAP-R-002 | Value Object Validation | Frozen dataclass only | Include `__post_init__` |
| GAP-R-003 | Logging Standards | Not documented | Create new section |
| GAP-R-004 | Exception Context | Mentioned | Formalize pattern |
| GAP-R-005 | Event Versioning | Implicit | Document explicitly |
| GAP-R-006 | Snapshot Frequency | Canon mentions 10 events | Add to rules |
| GAP-R-007 | Query Verb Selection | Pattern catalog only | Add to architecture rules |
| GAP-R-008 | BC Mapping Patterns | Partially documented | Add 9 industry patterns |
| GAP-R-009 | Tool Configuration | Scattered in configs | Unified documentation |

---

## Part 3: Implementation Plan

### Phase 1: Pattern Files Creation (40 files)

#### 1.1 Identity Patterns (`patterns/identity/`)

| File | Pattern ID | Status |
|------|------------|--------|
| `vertex-id.md` | PAT-ID-001 | TODO |
| `domain-specific-ids.md` | PAT-ID-002 | TODO |
| `jerry-uri.md` | PAT-ID-003 | TODO |
| `snowflake-id.md` | PAT-ID-004 | TODO |

#### 1.2 Entity Patterns (`patterns/entity/`)

| File | Pattern ID | Status |
|------|------------|--------|
| `iauditable.md` | PAT-ENT-001 | TODO |
| `iversioned.md` | PAT-ENT-002 | TODO |
| `aggregate-root.md` | PAT-ENT-003 | TODO |
| `entity-base.md` | PAT-ENT-004 | TODO |
| `vertex-edge.md` | PAT-ENT-005 | TODO |

#### 1.3 Aggregate Patterns (`patterns/aggregate/`)

| File | Pattern ID | Status |
|------|------------|--------|
| `work-item.md` | PAT-AGG-001 | TODO |
| `event-collection.md` | PAT-AGG-002 | TODO |
| `history-replay.md` | PAT-AGG-003 | TODO |
| `invariant-enforcement.md` | PAT-AGG-004 | TODO |

#### 1.4 Event Patterns (`patterns/event/`)

| File | Pattern ID | Status |
|------|------------|--------|
| `domain-event.md` | PAT-EVT-001 | TODO |
| `cloud-events.md` | PAT-EVT-002 | TODO |
| `work-item-events.md` | PAT-EVT-003 | TODO |
| `event-registry.md` | PAT-EVT-004 | TODO |

#### 1.5 CQRS Patterns (`patterns/cqrs/`)

| File | Pattern ID | Status |
|------|------------|--------|
| `command-pattern.md` | PAT-CQRS-001 | TODO |
| `query-pattern.md` | PAT-CQRS-002 | TODO |
| `dispatcher-pattern.md` | PAT-CQRS-003 | TODO |
| `projection-pattern.md` | PAT-CQRS-004 | TODO |

#### 1.6 Repository Patterns (`patterns/repository/`)

| File | Pattern ID | Status |
|------|------------|--------|
| `generic-repository.md` | PAT-REPO-001 | TODO |
| `event-store.md` | PAT-REPO-002 | TODO |
| `snapshot-store.md` | PAT-REPO-003 | TODO |

#### 1.7 Value Object Patterns (`patterns/value-object/`)

| File | Pattern ID | Status |
|------|------------|--------|
| `immutable-value-object.md` | PAT-VO-001 | TODO |
| `state-machine-vo.md` | PAT-VO-002 | TODO |
| `factory-methods.md` | PAT-VO-003 | TODO |

#### 1.8 Domain Service Patterns (`patterns/domain-service/`)

| File | Pattern ID | Status |
|------|------------|--------|
| `quality-gate-validator.md` | PAT-SVC-001 | TODO |
| `id-generator-service.md` | PAT-SVC-002 | TODO |

#### 1.9 Architecture Patterns (`patterns/architecture/`)

| File | Pattern ID | Status |
|------|------------|--------|
| `hexagonal-architecture.md` | PAT-ARCH-001 | TODO |
| `ports-adapters.md` | PAT-ARCH-002 | TODO |
| `bounded-contexts.md` | PAT-ARCH-003 | TODO |
| `one-class-per-file.md` | PAT-ARCH-004 | TODO |
| `composition-root.md` | PAT-ARCH-005 | TODO |

#### 1.10 Adapter Patterns (`patterns/adapter/`)

| File | Pattern ID | Status |
|------|------------|--------|
| `secondary-adapter.md` | PAT-ADAPT-001 | TODO |
| `primary-adapter.md` | PAT-ADAPT-002 | TODO |
| `in-memory-adapter.md` | PAT-ADAPT-003 | TODO |

#### 1.11 Testing Patterns (`patterns/testing/`)

| File | Pattern ID | Status |
|------|------------|--------|
| `bdd-cycle.md` | PAT-TEST-001 | TODO |
| `test-pyramid.md` | PAT-TEST-002 | TODO |
| `architecture-tests.md` | PAT-TEST-003 | TODO |

### Phase 2: Rules Files (6 files)

#### 2.1 New Files to Create

| File | Purpose | Priority |
|------|---------|----------|
| `error-handling-standards.md` | Exception patterns | HIGH |
| `tool-configuration.md` | Tool settings documentation | MEDIUM |

#### 2.2 Files to Enhance

| File | Enhancements | Priority |
|------|--------------|----------|
| `architecture-standards.md` | BC mapping, Event Sourcing specifics, snapshot strategy | HIGH |
| `coding-standards.md` | Module docstrings, logging, `__post_init__` validation | HIGH |
| `file-organization.md` | URI specification reference | LOW |
| `testing-standards.md` | Property-based testing section | LOW |

### Phase 3: Pattern Catalog Update

Update `PATTERN-CATALOG.md` with:
- All 40+ patterns organized by category
- Links to individual pattern files
- Status indicators (MANDATORY/RECOMMENDED)
- Quick reference table

### Phase 4: Validation

- Run architecture tests to verify standards
- Create fresh agent test to verify reproducibility

---

## Part 4: Industry Citations

Each pattern file MUST include authoritative citations:

### 4.1 Authoritative Sources

| Source | Expertise | URL |
|--------|-----------|-----|
| Martin Fowler | Enterprise Patterns, CQRS, Event Sourcing | martinfowler.com |
| Eric Evans | Domain-Driven Design | domainlanguage.com |
| Alistair Cockburn | Hexagonal Architecture | alistair.cockburn.us |
| Vaughn Vernon | Implementing DDD, Aggregates | vaughnvernon.com |
| Greg Young | Event Sourcing, CQRS | goodenoughsoftware.net |
| Robert C. Martin | Clean Architecture | cleancoder.com |
| Alberto Brandolini | Event Storming | eventstorming.com |

### 4.2 Tool Documentation

| Tool | Documentation |
|------|---------------|
| pytest-archon | Architecture testing for Python |
| PyTestArch | ArchUnit-inspired Python testing |
| Anthropic Claude | Claude Code best practices |

---

## Part 5: Jerry-Specific Opinions

Each pattern file MUST include Jerry-specific decisions marked as:

```markdown
> **Jerry Decision**: [Description of our specific choice and rationale]
```

### 5.1 Documented Jerry Decisions

| Decision | Jerry Choice | Generic Alternative |
|----------|--------------|---------------------|
| File Organization | One-class-per-file | Python's "one idea per file" |
| DI Framework | Factory functions in bootstrap.py | DI containers (injector, dependency-injector) |
| Internal Events | DomainEvent base class | CloudEvents for all |
| BC Naming | Functional names | Metaphorical names |
| Query Verb | Retrieve for single, List for collection | Get for all |
| Snapshot Frequency | Every 10 events | Not specified |

---

## Part 6: Execution Order

### Priority 1: Foundation (Day 1)

1. Create directory structure: `patterns/{category}/`
2. Create `error-handling-standards.md`
3. Create core architecture patterns: PAT-ARCH-001, PAT-ARCH-005

### Priority 2: Core Patterns (Day 1-2)

4. Create CQRS patterns: PAT-CQRS-001 to PAT-CQRS-004
5. Create entity patterns: PAT-ENT-001 to PAT-ENT-003
6. Create event patterns: PAT-EVT-001 to PAT-EVT-004

### Priority 3: Domain Patterns (Day 2)

7. Create identity patterns: PAT-ID-001 to PAT-ID-004
8. Create aggregate patterns: PAT-AGG-001 to PAT-AGG-004
9. Create repository patterns: PAT-REPO-001 to PAT-REPO-003

### Priority 4: Supporting Patterns (Day 2-3)

10. Create value object patterns: PAT-VO-001 to PAT-VO-003
11. Create domain service patterns: PAT-SVC-001, PAT-SVC-002
12. Create adapter patterns: PAT-ADAPT-001 to PAT-ADAPT-003
13. Create testing patterns: PAT-TEST-001 to PAT-TEST-003

### Priority 5: Rules Enhancement (Day 3)

14. Enhance `architecture-standards.md`
15. Enhance `coding-standards.md`
16. Create `tool-configuration.md`

### Priority 6: Finalization (Day 3)

17. Update `PATTERN-CATALOG.md` with all links
18. Validate with architecture tests
19. Create fresh agent reproducibility test

---

## Part 7: Acceptance Criteria

| ID | Criterion | Evidence |
|----|-----------|----------|
| AC-01 | All 40+ patterns documented | Pattern file count = 40 |
| AC-02 | All patterns have industry citations | Each pattern has References section |
| AC-03 | All patterns have Jerry decisions | Each pattern has Jerry Decision callout |
| AC-04 | All patterns have code examples | Each pattern has Implementation section |
| AC-05 | All rules gaps addressed | GAP-R-001 to GAP-R-009 resolved |
| AC-06 | Pattern catalog links work | All links verified |
| AC-07 | Architecture tests pass | pytest architecture/ passes |
| AC-08 | Fresh agent follows rules | Reproducibility test passes |

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-11 | Claude Opus 4.5 | Created comprehensive detailed plan based on repository exploration |
