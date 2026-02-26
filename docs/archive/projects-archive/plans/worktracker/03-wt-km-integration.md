# Phase 3: Knowledge Management Integration (Weeks 17-24)

> **Goal**: Implement KM domain entities and connect to Work Tracker through events.
> **Reference**: [Index](00-wt-index.md) | [Unified Design](../../design/work-034-e-003-unified-design.md)

**Status**: PENDING
**Duration**: Weeks 17-24
**WORK Items**: WORK-301 to WORK-304
**Dependencies**: Phase 2 complete

---

## Phase 3 Overview

| WORK Item | Name | Duration | Dependencies |
|-----------|------|----------|--------------|
| WORK-301 | KM Domain Layer | Weeks 17-18 | Phase 2 |
| WORK-302 | KM Repository Layer | Weeks 19-20 | WORK-301 |
| WORK-303 | KM CQRS Implementation | Weeks 21-22 | WORK-301, WORK-302 |
| WORK-304 | KM Interface Layer | Weeks 23-24 | WORK-303 |

---

## WORK-301: KM Domain Layer

**Status**: PENDING
**Duration**: Weeks 17-18
**Artifacts**: KM entities, value objects, events
**Dependencies**: Phase 2

### Sub-task 301.1: KM Value Objects

**Files**: `src/domain/value_objects/knowledge/`
**Tests**: `tests/unit/domain/value_objects/knowledge/`

- [ ] `KnowledgeId` value object
  - [ ] Format: PAT-NNN (patterns), LES-NNN (lessons), ASM-NNN (assumptions)
  - [ ] Type inference from prefix

- [ ] `Evidence` value object
  - [ ] `evidence_type: EvidenceType`
  - [ ] `source: JerryUri`
  - [ ] `confidence: float` (0.0-1.0)
  - [ ] `timestamp: datetime`

- [ ] `EvidenceType` enum
  - [ ] TASK_COMPLETION
  - [ ] USER_FEEDBACK
  - [ ] PATTERN_MATCH
  - [ ] SYSTEM_INFERENCE

- [ ] `Confidence` value object
  - [ ] Range validation
  - [ ] `combine()` for aggregation
  - [ ] Decay over time

### Sub-task 301.2: KnowledgeItem Aggregate

**Files**: `src/domain/aggregates/knowledge_item.py`
**Tests**: `tests/unit/domain/aggregates/test_knowledge_item.py`

- [ ] `KnowledgeItem` aggregate root
  - [ ] `id: KnowledgeId`
  - [ ] `content: str`
  - [ ] `item_type: KnowledgeType` (PATTERN, LESSON, ASSUMPTION)
  - [ ] `evidence: list[Evidence]`
  - [ ] `tags: frozenset[Tag]`
  - [ ] `confidence: Confidence` (calculated from evidence)
  - [ ] `links: frozenset[KnowledgeId]`

- [ ] Type-specific behavior
  - [ ] Pattern: requires `example_count > 0`
  - [ ] Lesson: requires `outcome` (POSITIVE, NEGATIVE, NEUTRAL)
  - [ ] Assumption: requires `validation_status`

- [ ] Evidence management
  - [ ] `add_evidence(evidence)` → recalculates confidence
  - [ ] `get_evidence()` → sorted by timestamp
  - [ ] Evidence expiration policy

- [ ] Knowledge linking
  - [ ] `link_to(other_id, relationship)`
  - [ ] Circular link detection
  - [ ] Relationship types: REFERENCES, CONTRADICTS, SUPPORTS, EXTENDS

### Sub-task 301.3: KM Domain Events

**Files**: `src/domain/events/knowledge.py`
**Tests**: `tests/unit/domain/events/test_knowledge_events.py`

- [ ] `KnowledgeItemCreated`
- [ ] `KnowledgeItemUpdated`
- [ ] `EvidenceAdded`
- [ ] `ConfidenceChanged`
- [ ] `KnowledgeLinked`
- [ ] `KnowledgeArchived`

- [ ] Cross-domain events
  - [ ] `TaskCompletedTriggersAAR`
  - [ ] `PatternSuggested`
  - [ ] `LessonExtracted`
  - [ ] `AssumptionValidated`

### Sub-task 301.4: KM Architecture Tests

**Files**: `tests/architecture/test_km_architecture.py`

- [ ] Domain layer isolation
- [ ] WT→KM communication via events only
- [ ] Shared kernel for value objects only

---

## WORK-302: KM Repository Layer

**Status**: PENDING
**Duration**: Weeks 19-20
**Artifacts**: KM repository port, SQLite adapter
**Dependencies**: WORK-301

### Sub-task 302.1: KM Repository Port

**Files**: `src/domain/ports/knowledge_repository.py`
**Tests**: `tests/unit/domain/ports/test_knowledge_repository.py`

- [ ] Define `IKnowledgeRepository` ABC
  - [ ] `get(id: KnowledgeId) -> KnowledgeItem | None`
  - [ ] `save(item: KnowledgeItem) -> None`
  - [ ] `delete(id: KnowledgeId) -> bool`
  - [ ] `list_by_type(item_type: KnowledgeType) -> list[KnowledgeItem]`
  - [ ] `list_by_tag(tag: Tag) -> list[KnowledgeItem]`
  - [ ] `search_by_content(query: str) -> list[KnowledgeItem]`
  - [ ] `get_related(id: KnowledgeId) -> list[KnowledgeItem]`

### Sub-task 302.2: SQLite KM Repository

**Files**: `src/infrastructure/persistence/sqlite_knowledge_repo.py`
**Tests**: `tests/integration/persistence/test_sqlite_knowledge_repo.py`

- [ ] Schema migration: `migrations/003_knowledge_schema.sql`
  - [ ] `knowledge_items` table
  - [ ] `knowledge_evidence` table
  - [ ] `knowledge_tags` junction
  - [ ] `knowledge_links` table
  - [ ] FTS5 index on content

- [ ] Full-text search implementation
- [ ] Link traversal queries

### Sub-task 302.3: KM Repository Contracts

**Files**: `tests/contract/persistence/test_knowledge_repo_contract.py`

- [ ] All port methods
- [ ] Cross-repository integrity (WT ↔ KM via JerryUri)

---

## WORK-303: KM CQRS Implementation

**Status**: PENDING
**Duration**: Weeks 21-22
**Artifacts**: KM commands, queries, handlers, AAR flow
**Dependencies**: WORK-301, WORK-302

### Sub-task 303.1: KM Commands

**Files**: `src/application/commands/km/`
**Tests**: `tests/unit/application/commands/km/`

- [ ] `CreateKnowledgeItemCommand`
- [ ] `UpdateKnowledgeItemCommand`
- [ ] `AddEvidenceCommand`
- [ ] `LinkKnowledgeCommand`
- [ ] `ArchiveKnowledgeCommand`

### Sub-task 303.2: KM Command Handlers

**Files**: `src/application/handlers/commands/km/`
**Tests**: `tests/unit/application/handlers/km/`

- [ ] Create handler
- [ ] Update handler
- [ ] Add evidence handler (recalculates confidence)
- [ ] Link handler (validates both exist)
- [ ] Archive handler

### Sub-task 303.3: KM Queries & Handlers

**Files**: `src/application/queries/km/`, `src/application/handlers/queries/km/`
**Tests**: `tests/unit/application/queries/km/`

- [ ] `GetKnowledgeItemQuery`
- [ ] `ListKnowledgeItemsQuery` (with filters)
- [ ] `SearchKnowledgeQuery`
- [ ] `GetRelatedKnowledgeQuery`
- [ ] `GetKnowledgeGraphQuery`

### Sub-task 303.4: After Action Review (AAR) Flow

**Files**: `src/application/event_handlers/aar_handler.py`
**Tests**: `tests/integration/application/test_aar_flow.py`

- [ ] `AARTriggerHandler`
  - [ ] TaskCompleted → AAR prompt
  - [ ] PhaseCompleted → Summary prompt
  - [ ] Configurable delay
  - [ ] Opt-out support

- [ ] `CaptureAARCommand`
  - [ ] Creates KnowledgeItems from AAR input
  - [ ] Links to source task
  - [ ] Evidence from task completion

- [ ] `SkipAARCommand` / `DeferAARCommand`
  - [ ] Track skip reasons (analytics)
  - [ ] Defer scheduling

### Sub-task 303.5: Cross-Domain Event Handlers

**Files**: `src/application/event_handlers/cross_domain/`
**Tests**: `tests/integration/application/test_cross_domain_handlers.py`

- [ ] WT→KM handlers
  - [ ] TaskCompleted → AARPrompt
  - [ ] PatternDetected → PatternSuggestion

- [ ] KM→WT handlers
  - [ ] PatternMatched → TaskSuggestion
  - [ ] LessonRelevant → TaskAnnotation

---

## WORK-304: KM Interface Layer

**Status**: PENDING
**Duration**: Weeks 23-24
**Artifacts**: KM CLI, SKILL.md, BDD tests
**Dependencies**: WORK-303

### Sub-task 304.1: KM CLI

**Files**: `src/interface/cli/km_cli.py`
**Tests**: `tests/e2e/cli/test_km_cli.py`

- [ ] `km --help`
- [ ] `km create --type pattern "content"`
- [ ] `km list --type lesson`
- [ ] `km show <id>`
- [ ] `km search "query"`
- [ ] `km link <id1> <id2> --rel references`
- [ ] `km aar capture --task <id> --lesson "text"`
- [ ] `km aar pending`
- [ ] `km aar skip <task_id> --reason`
- [ ] `km export --format turtle --output file.ttl`

### Sub-task 304.2: KM SKILL.md

**Files**: `skills/km/SKILL.md`

- [ ] Natural language patterns for KM operations
- [ ] AAR capture patterns
- [ ] Search patterns
- [ ] Integration with WT skill

### Sub-task 304.3: KM BDD Tests

**Files**: `tests/bdd/km/`

- [ ] `features/knowledge.feature`
- [ ] `features/aar.feature`
- [ ] Step definitions (REAL implementations)

### Sub-task 304.4: Phase 3 Gate

- [ ] All tests pass (95%+ coverage)
- [ ] All BDD scenarios pass
- [ ] AAR capture < 200ms p95
- [ ] Knowledge search < 100ms p95
- [ ] Cross-domain events < 50ms propagation
- [ ] AAR adoption tracking in place

---

## Estimated Test Counts

| Category | Count |
|----------|-------|
| Unit tests | ~150 |
| Integration tests | ~80 |
| Contract tests | ~20 |
| BDD scenarios | ~30 |
| E2E tests | ~20 |
| **Total** | **~300** |

---

*Phase 3 plan created 2026-01-09*
