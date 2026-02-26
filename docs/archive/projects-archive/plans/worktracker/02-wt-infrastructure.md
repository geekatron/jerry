# Phase 2: Shared Infrastructure (Weeks 9-16)

> **Goal**: Build shared infrastructure components for Event Store, Graph, Semantic Index, and RDF.
> **Reference**: [Index](00-wt-index.md) | [Unified Design](../../design/work-034-e-003-unified-design.md)

**Status**: PENDING
**Duration**: Weeks 9-16
**WORK Items**: WORK-201 to WORK-204
**Dependencies**: Phase 1 complete

---

## Phase 2 Overview

| WORK Item | Name | Duration | Dependencies |
|-----------|------|----------|--------------|
| WORK-201 | Event Store | Weeks 9-10 | Phase 1 |
| WORK-202 | Graph Store (NetworkX) | Weeks 11-12 | WORK-201 |
| WORK-203 | Semantic Index (FAISS) | Weeks 13-14 | WORK-202 |
| WORK-204 | RDF Serialization (RDFLib) | Weeks 15-16 | WORK-202, WORK-203 |

---

## WORK-201: Event Store

**Status**: PENDING
**Duration**: Weeks 9-10
**Artifacts**: Event store port, SQLite adapter, CloudEvents compliance
**Dependencies**: Phase 1

### Sub-task 201.1: Event Store Port

**Files**: `src/domain/ports/event_store.py`
**Tests**: `tests/unit/domain/ports/test_event_store.py`

- [ ] Define `IEventStore` ABC
  - [ ] `append(event: DomainEvent) -> None`
  - [ ] `append_batch(events: list[DomainEvent]) -> None`
  - [ ] `get_events_for_aggregate(aggregate_id: str) -> list[DomainEvent]`
  - [ ] `get_events_by_type(event_type: str) -> list[DomainEvent]`
  - [ ] `get_events_since(timestamp: datetime) -> list[DomainEvent]`
  - [ ] `get_all_events(limit: int, offset: int) -> list[DomainEvent]`

### Sub-task 201.2: CloudEvents Envelope

**Files**: `src/domain/events/cloud_events.py`
**Tests**: `tests/unit/domain/events/test_cloud_events.py`

- [ ] Implement CloudEvents 1.0 compliant envelope
  - [ ] `specversion: "1.0"`
  - [ ] `type: str` (event class name)
  - [ ] `source: str` (Jerry URI)
  - [ ] `id: str` (UUID)
  - [ ] `time: datetime` (ISO 8601)
  - [ ] `data: dict` (event payload)
  - [ ] Jerry extensions: `x-jerry-correlation-id`, `x-jerry-causation-id`

### Sub-task 201.3: SQLite Event Store Adapter

**Files**: `src/infrastructure/event_store/sqlite_event_store.py`
**Tests**: `tests/integration/event_store/test_sqlite_event_store.py`

- [ ] Implement `SQLiteEventStore`
  - [ ] Append-only semantics
  - [ ] Indexed queries by aggregate_id, type, time
  - [ ] Optimistic concurrency with version checking
  - [ ] Migration: `migrations/002_event_store.sql`

### Sub-task 201.4: Event Store Contract Tests

**Files**: `tests/contract/event_store/`

- [ ] Contract test suite for all adapters
- [ ] Work Tracker event integration tests

---

## WORK-202: Graph Store (NetworkX)

**Status**: PENDING
**Duration**: Weeks 11-12
**Artifacts**: Graph store port, NetworkX adapter, projector
**Dependencies**: WORK-201

### Sub-task 202.1: Graph Store Port

**Files**: `src/domain/ports/graph_store.py`
**Tests**: `tests/unit/domain/ports/test_graph_store.py`

- [ ] Define `IGraphStore` ABC
  - [ ] `add_vertex(id: str, properties: dict) -> None`
  - [ ] `add_edge(from_id: str, to_id: str, edge_type: str, properties: dict) -> None`
  - [ ] `get_vertex(id: str) -> dict | None`
  - [ ] `get_edges(id: str, direction: str) -> list[Edge]`
  - [ ] `traverse(start_id: str, max_depth: int) -> list[str]`
  - [ ] `path_between(from_id: str, to_id: str) -> list[str] | None`
  - [ ] `remove_vertex(id: str) -> bool`
  - [ ] `remove_edge(from_id: str, to_id: str, edge_type: str) -> bool`

### Sub-task 202.2: NetworkX Adapter

**Files**: `src/infrastructure/graph/networkx_graph_store.py`
**Tests**: `tests/integration/graph/test_networkx_graph_store.py`

- [ ] Implement `NetworkXGraphStore`
  - [ ] Vertex CRUD operations
  - [ ] Edge CRUD operations
  - [ ] BFS/DFS traversal
  - [ ] Shortest path
  - [ ] Graph persistence (JSON/pickle)

### Sub-task 202.3: Graph Projector

**Files**: `src/application/event_handlers/graph_projector.py`
**Tests**: `tests/integration/application/test_graph_projector.py`

- [ ] Project domain events to graph vertices/edges
  - [ ] `TaskCreated` → Task vertex
  - [ ] `SubTaskCreated` → SubTask vertex + edge to Task
  - [ ] `TaskCompleted` → Update vertex status

### Sub-task 202.4: Supernode Prevention

**Files**: `src/domain/validators/`
**Tests**: `tests/unit/domain/validators/`

- [ ] Edge count validator (alert at 100, warn at 500)
- [ ] Configurable limits

---

## WORK-203: Semantic Index (FAISS)

**Status**: PENDING
**Duration**: Weeks 13-14
**Artifacts**: Semantic index port, FAISS adapter, embedding provider
**Dependencies**: WORK-202

### Sub-task 203.1: Semantic Index Port

**Files**: `src/domain/ports/semantic_index.py`
**Tests**: `tests/unit/domain/ports/test_semantic_index.py`

- [ ] Define `ISemanticIndex` ABC
  - [ ] `add_embedding(id: str, vector: list[float], metadata: dict) -> None`
  - [ ] `search_similar(vector: list[float], k: int, threshold: float) -> list[SearchResult]`
  - [ ] `get_embedding(id: str) -> list[float] | None`
  - [ ] `remove_embedding(id: str) -> bool`
  - [ ] `update_embedding(id: str, vector: list[float]) -> None`

### Sub-task 203.2: Embedding Provider Port

**Files**: `src/domain/ports/embedding_provider.py`
**Tests**: `tests/unit/domain/ports/test_embedding_provider.py`

- [ ] Define `IEmbeddingProvider` ABC
  - [ ] `embed_text(text: str) -> list[float]`
  - [ ] `embed_batch(texts: list[str]) -> list[list[float]]`
  - [ ] `dimension: int` property

### Sub-task 203.3: FAISS Adapter

**Files**: `src/infrastructure/search/faiss_semantic_index.py`
**Tests**: `tests/integration/search/test_faiss_semantic_index.py`

- [ ] Implement `FAISSSemanticIndex`
  - [ ] Index initialization (Flat, IVF)
  - [ ] Embedding CRUD
  - [ ] kNN search with threshold
  - [ ] Index persistence

### Sub-task 203.4: Simple Embedding Provider

**Files**: `src/infrastructure/search/tfidf_embedding_provider.py`
**Tests**: `tests/unit/infrastructure/search/test_tfidf_provider.py`

- [ ] TF-IDF based provider for testing
  - [ ] Deterministic embeddings
  - [ ] Swappable for production embeddings

---

## WORK-204: RDF Serialization (RDFLib)

**Status**: PENDING
**Duration**: Weeks 15-16
**Artifacts**: RDF serializer port, RDFLib adapter, SPARQL support
**Dependencies**: WORK-202, WORK-203

### Sub-task 204.1: RDF Serializer Port

**Files**: `src/domain/ports/rdf_serializer.py`
**Tests**: `tests/unit/domain/ports/test_rdf_serializer.py`

- [ ] Define `IRDFSerializer` ABC
  - [ ] `serialize_entity(entity) -> list[Triple]`
  - [ ] `serialize_graph(entities) -> Graph`
  - [ ] `deserialize(triples) -> list[Entity]`
  - [ ] `export(graph, format: str, path: str) -> None`
  - [ ] `import_file(path: str) -> Graph`

### Sub-task 204.2: Jerry Ontology

**Files**: `src/domain/ontology/jerry.ttl`
**Tests**: `tests/unit/domain/ontology/test_jerry_ontology.py`

- [ ] Define Jerry ontology in Turtle format
  - [ ] Task class
  - [ ] SubTask class
  - [ ] Status enum
  - [ ] Relationships (hasSubTask, belongsTo, etc.)

### Sub-task 204.3: RDFLib Adapter

**Files**: `src/infrastructure/rdf/rdflib_serializer.py`
**Tests**: `tests/integration/rdf/test_rdflib_serializer.py`

- [ ] Implement `RDFLibSerializer`
  - [ ] Entity to triples
  - [ ] Graph building
  - [ ] Export formats: Turtle, JSON-LD, N-Triples
  - [ ] Import and parsing

### Sub-task 204.4: SPARQL Query Support

**Files**: `src/infrastructure/rdf/sparql_executor.py`
**Tests**: `tests/integration/rdf/test_sparql_executor.py`

- [ ] SPARQL query execution
  - [ ] SELECT queries
  - [ ] ASK queries
  - [ ] CONSTRUCT queries
  - [ ] Security constraints (timeout, depth limit)

### Sub-task 204.5: Phase 2 Gate

- [ ] All unit tests pass (95%+ coverage)
- [ ] All integration tests pass
- [ ] All contract tests pass
- [ ] Event Store append < 10ms p95
- [ ] Graph traversal < 50ms p95
- [ ] Semantic search < 100ms p95
- [ ] RDF export < 1s for 1000 entities
- [ ] No memory leaks in stress test

---

## Estimated Test Counts

| Category | Count |
|----------|-------|
| Unit tests | ~120 |
| Integration tests | ~80 |
| Contract tests | ~30 |
| System tests | ~20 |
| **Total** | **~250** |

---

*Phase 2 plan created 2026-01-09*
