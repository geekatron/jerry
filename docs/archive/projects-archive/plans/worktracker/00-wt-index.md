# Jerry Framework - Work Tracker Implementation Plan

> Granular implementation plan derived from ADR-034 unified design.
> **Source**: [ADR-034](../../decisions/ADR-034-unified-wt-km-implementation.md) | [Unified Design](../../design/work-034-e-003-unified-design.md)

**Created**: 2026-01-09
**Revised**: 2026-01-09
**Status**: PROPOSED (awaiting approval)
**Total Duration**: 32 weeks (4 phases)
**Branch**: TBD (implementation branch)

---

## Architecture & Testing Principles

> **MANDATORY**: All implementation MUST adhere to these principles.

### Architecture Pure Best Practices

| Pattern | Enforcement | Validation |
|---------|-------------|------------|
| DDD | Hard | Architecture tests verify bounded contexts |
| Hexagonal Architecture | Hard | No adapter imports in domain |
| Event Sourcing | Hard | Events immutable, append-only |
| CQRS | Hard | Commands return events, queries return DTOs |
| Repository Pattern | Hard | All data access via ports |
| Dispatcher Pattern | Hard | Events dispatched, not directly handled |
| Dependency Injection | Hard | No `new` in domain/application |

### Test Pyramid (Per Feature)

| Level | Count | Focus | Real Data |
|-------|-------|-------|-----------|
| Unit | Many | Single class/function | Mocked dependencies |
| Integration | Medium | Multiple components | Real file system |
| Contract | Few | Port compliance | Interface verification |
| System | Few | Multi-operation workflows | Full stack |
| E2E | Few | CLI to persistence | Real everything |
| Architecture | Always | Layer dependencies | Static analysis |

### BDD Red/Green/Refactor Protocol

```
1. RED: Write failing test with REAL assertions (no placeholders)
2. GREEN: Implement MINIMUM code to pass
3. REFACTOR: Clean up while maintaining GREEN
4. REPEAT: Until acceptance criteria met
```

### Test Coverage Requirements

| Scenario Type | Coverage |
|--------------|----------|
| Happy path | 100% of use cases |
| Edge cases | Boundary conditions, empty/max values |
| Failure scenarios | NotFound, InvalidState, Concurrent |
| Negative tests | Invalid input, malformed data |

---

## Vertical Slice Focus: Task + Sub-Task

This implementation focuses on delivering a **fully integrated vertical slice** of the Task and Sub-Task aggregates with all supporting components:

### Aggregates (Separate, with Reference)

| Aggregate | Description | Relationship |
|-----------|-------------|--------------|
| **Task** | Primary work item with lifecycle | Parent reference for Sub-Tasks |
| **Sub-Task** | Child work item with own lifecycle | References parent Task via `task_id` |

**Design Decision**: Sub-Task is a **separate aggregate** (not embedded) to allow:
- Multiple simultaneous requests on different sub-tasks
- Independent lifecycle management
- Concurrent modification without aggregate-level locking

### Adapters

| Adapter Type | Format | Purpose |
|--------------|--------|---------|
| **JSON Secondary** | `.json` files | Human-readable persistence, debugging |
| **TOON Secondary** | `.toon` files | LLM-optimized (30-60% token reduction) |
| **CLI Primary** | argparse | User interface for CRUD operations |

### Full Stack Components

```
┌─────────────────────────────────────────────────────────────────┐
│                         SKILL.md                                │
│                  (Natural Language Interface)                   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      CLI Primary Adapter                        │
│                    (src/interface/cli/)                         │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                    Application Layer                            │
│              Commands / Queries / Handlers                      │
│                 (src/application/)                              │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      Domain Layer                               │
│      Task Aggregate │ Sub-Task Aggregate │ Events │ Ports       │
│                    (src/domain/)                                │
└─────────────────────────────┬───────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│   JSON File Adapter      │    │   TOON File Adapter      │
│  (src/infrastructure/)   │    │  (src/infrastructure/)   │
│                          │    │                          │
│  - .json file storage    │    │  - .toon file storage    │
│  - Human readable        │    │  - LLM optimized         │
│  - Debug friendly        │    │  - 30-60% token savings  │
└──────────────────────────┘    └──────────────────────────┘
```

---

## Phase Overview

| Phase | File | Status | WORK Items | Focus |
|-------|------|--------|------------|-------|
| **Phase 1** | [01-wt-foundation.md](01-wt-foundation.md) | PENDING | WORK-101 to WORK-104 | Task + Sub-Task vertical slice |
| **Phase 2** | [02-wt-infrastructure.md](02-wt-infrastructure.md) | PENDING | WORK-201 to WORK-204 | Event Store, Graph, Semantic Index, RDF |
| **Phase 3** | [03-wt-km-integration.md](03-wt-km-integration.md) | PENDING | WORK-301 to WORK-304 | Knowledge Management domain |
| **Phase 4** | [04-wt-advanced-features.md](04-wt-advanced-features.md) | PENDING | WORK-401 to WORK-404 | HybridRAG, Pattern Discovery, API |

---

## Quick Status

| Phase | Status | Progress |
|-------|--------|----------|
| Phase 1: Work Tracker Foundation | PENDING | 0% |
| Phase 2: Shared Infrastructure | PENDING | 0% |
| Phase 3: KM Integration | PENDING | 0% |
| Phase 4: Advanced Features | PENDING | 0% |

---

## Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Runtime | Python | 3.11+ | Zero-dependency core |
| Serialization | JSON | stdlib | Human-readable persistence |
| Serialization | TOON | python-toon | LLM-optimized format |
| Graph | NetworkX | 3.2.1 | Property graph (Phase 2+) |
| Vector Search | FAISS | 1.7.4 | Semantic similarity (Phase 2+) |
| RDF | RDFLib | 7.0.0 | Knowledge export (Phase 2+) |
| Testing | pytest | 8.x | All test types |
| BDD | pytest-bdd | 7.x | BDD scenarios |

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Sub-Task as separate aggregate | Yes | Concurrent modification support |
| File-based persistence (Phase 1) | JSON + TOON | Skill integration, no DB dependency |
| Database adapters | Deferred | Add in later phase when needed |
| TOON for LLM context | Yes | 30-60% token reduction |

---

## References

| Document | Purpose |
|----------|---------|
| [ADR-034](../../decisions/ADR-034-unified-wt-km-implementation.md) | Architecture decision |
| [Unified Design](../../design/work-034-e-003-unified-design.md) | Technical specifications |
| [TOON Format Analysis](../../research/TOON_FORMAT_ANALYSIS.md) | TOON serialization research |

---

*Plan created 2026-01-09*
