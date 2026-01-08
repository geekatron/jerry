# ADR-031: Jerry Knowledge Architecture

## Status
PROPOSED

## Date
2026-01-08

## Context

### The Problem Space

Jerry is a framework for behavior and workflow guardrails that helps solve problems while accruing a body of knowledge, wisdom, and experience. Currently, Jerry operates at **Phase 1** with:
- Property graph abstractions (Vertex, Edge, VertexProperty)
- File-based storage (JSON, TOON)
- Jerry URI scheme (SPEC-001)
- Work Tracker graph model for operational state

However, Jerry faces several architectural challenges:

1. **Context Rot in LLM Agents**: LLM performance degrades as context windows fill, even within technical token limits. Jerry needs persistent knowledge storage beyond ephemeral context.

2. **Knowledge Fragmentation**: Jerry accumulates knowledge across Work Tracker entities (tasks, phases, plans) AND documentation (`docs/` hierarchy), but these exist as isolated silos without semantic connections.

3. **LLM Hallucination**: Claude Code agents operating within Jerry lack grounding mechanisms, leading to factually incorrect responses. Production systems show baseline hallucination rates that impact user trust.

4. **Interoperability Limitations**: Jerry's current property graph uses implicit schemas and Jerry-specific formats, limiting integration with external systems and semantic web standards.

5. **Architectural Evolution**: Jerry needs a knowledge architecture roadmap that scales from current single-user embedded deployment to potential multi-tenant, high-volume scenarios without requiring complete rewrites.

### The Strategic Context

Knowledge architecture is no longer infrastructure—it's **strategic differentiation**. Recent industry evidence shows:

- **GraphRAG achieves 90% hallucination reduction** (FalkorDB case study)
- **63% faster issue resolution** (LinkedIn: 40hrs → 15hrs with knowledge graph grounding)
- **49% → 86% accuracy improvement** (Amazon Finance with GraphRAG)
- **300-320% ROI** from knowledge graph investments in production systems

Additionally, the Semantic Web has undergone a **pragmatic turn in 2024-2025**:
- JSON-LD reached 70% web adoption (vs 3% RDFa, 46% Microdata)
- Modern embedded tooling available (Oxigraph in Rust/Python, not legacy Java)
- 45M+ websites use Schema.org for structured data
- LLM grounding via knowledge graphs has emerged as the "killer app" for semantic technologies

### Jerry's Current Position

Jerry is at **4-star Linked Open Data status** (Tim Berners-Lee's 5-star model):
- ★★★★ **Achieved**: HTTP URIs to denote things (Jerry URI scheme SPEC-001)
- ★★★★★ **Target**: Link data to other data to provide context

The path to 5 stars requires semantic layer capabilities that Jerry currently lacks.

## Decision Drivers

The following factors influenced this architectural decision, in priority order:

### Critical Drivers (Must-Have)

1. **LLM Grounding Effectiveness**: Measurable reduction in hallucinations, improved agent accuracy
2. **Backward Compatibility**: Phase 1 property graph foundation must remain intact
3. **Performance Requirements**: Query latency P95 < 50ms for operational queries
4. **Zero-Dependency Core**: Domain layer maintains Python stdlib-only constraint
5. **Incremental Implementation**: Each phase must deliver independent value

### Important Drivers (Should-Have)

6. **Standards Compliance**: W3C RDF, SPARQL, JSON-LD for interoperability
7. **Implementation Complexity**: Balance between capability and maintainability
8. **Cost Management**: Prefer embedded over server-based through Phase 3
9. **Supernode Prevention**: Avoid catastrophic performance degradation from high-degree vertices
10. **Schema Evolution**: Support for versioning and migrations

### Beneficial Drivers (Nice-to-Have)

11. **Future Extensibility**: Enable advanced capabilities (reasoning, SPARQL) without rewrites
12. **Ecosystem Integration**: Compatibility with Schema.org (45M+ websites)
13. **Visualization**: Graph visualization for debugging and exploration

## Considered Options

### Option 1: Property Graph Only (Gremlin/NetworkX)

**Description:** Extend current Phase 1 property graph with Gremlin queries, maintain file-based JSON/TOON storage, no semantic web capabilities.

**Strengths:**
- Simplest option—builds on existing foundation
- Best performance: O(1) edge traversals, in-memory operations
- Zero infrastructure costs (embedded)
- Low maintenance complexity

**Weaknesses:**
- No standards compliance—Jerry-specific formats only
- No semantic interoperability with external systems
- Implicit schema—risk of drift over time
- Cannot achieve 5-star Linked Open Data status
- Misses LLM grounding improvements from GraphRAG

**Score:** 18/25 (72%)
- Performance: 5/5
- Maintainability: 4/5
- Scalability: 3/5
- Cost: 5/5
- Standards: 1/5

**Verdict:** Strong second place, but strategically limiting.

---

### Option 2: RDF/Semantic Web Only (pyoxigraph)

**Description:** Replace property graph with pure RDF triple store, SPARQL for all queries, OWL ontology for domain model, full semantic web stack.

**Strengths:**
- Full W3C standards compliance (RDF, SPARQL, OWL)
- Maximum interoperability
- Formal reasoning capabilities (OWL-DL)
- Native RDF* support (edge properties without reification)

**Weaknesses:**
- Poorest performance: SPARQL 50-500ms vs Gremlin 5-10ms
- Highest complexity: semantic web learning curve, ontology maintenance
- Requires throwing away Phase 1 property graph work
- Limited Python ecosystem (RDFLib slower than Java-based Jena)
- Breaks backward compatibility

**Score:** 16/25 (64%)
- Performance: 2/5
- Maintainability: 2/5
- Scalability: 4/5
- Cost: 3/5
- Standards: 5/5

**Verdict:** Standards-pure but pragmatically weak.

---

### Option 3: Hybrid Property + RDF (RECOMMENDED)

**Description:** Property graph as primary operational storage with RDF serialization as export/integration layer. Implements Netflix UDA "Model Once, Represent Everywhere" pattern.

**Architecture:**
```
Domain Model (Property Graph)
    ├─ Primary Storage: File-based JSON/TOON
    ├─ Operational Queries: Gremlin traversal (hot path)
    └─ Serialization Adapters (cold path):
        ├─ JSON-LD (web integration)
        ├─ Turtle (human-readable RDF)
        ├─ GraphSON (TinkerPop export)
        └─ RDF* (edge properties without reification)
```

**Strengths:**
- **Best of both worlds**: Fast property graph operations + standards-compliant RDF export
- **Unanimous cross-document support**: 5/5 research documents independently recommend this pattern
- **Netflix UDA validation**: Production-proven pattern at scale
- **Backward compatible**: Phase 1 foundation remains unchanged
- **Incremental risk**: JSON-LD optional, high reversibility in Phase 2
- **Highest decision matrix score**: 22/25 (88%)

**Weaknesses:**
- More complex than property graph alone (multiple serializers)
- Synchronization burden (property graph ↔ RDF consistency)
- Learning curve for semantic web technologies
- Dependency expansion (pyoxigraph, embedding models)

**Score:** 22/25 (88%)
- Performance: 5/5 (property graph primary)
- Maintainability: 3/5 (adapter layer overhead)
- Scalability: 4/5 (embedded → server path)
- Cost: 5/5 (embedded through Phase 3)
- Standards: 5/5 (RDF export)

**Verdict:** Clear winner—pragmatic hybrid approach.

---

### Option 4: Vector DB Only

**Description:** Embed all Jerry knowledge (Work Tracker + docs/) as vectors, use cosine similarity for retrieval, no graph structure.

**Strengths:**
- Fast semantic search (vector similarity)
- Scales horizontally (Pinecone, Weaviate)
- Simple conceptual model (embeddings + distance)

**Weaknesses:**
- **Cannot answer relational queries**: "What blocks this task?" requires graph traversal
- No standards compliance (proprietary vector formats)
- Loses Work Tracker graph structure (tasks, phases, edges)
- Embedding API costs or local model overhead
- 300-token chunk limits break context

**Score:** 16/25 (64%)
- Performance: 4/5
- Maintainability: 3/5
- Scalability: 4/5
- Cost: 3/5
- Standards: 2/5

**Verdict:** Good for semantic search, insufficient for Jerry's relational needs.

---

### Option 5: HybridRAG (Vector + Graph)

**Description:** Combine vector retrieval (docs/ indexing) with graph traversal (Work Tracker), merge results for LLM grounding.

**Strengths:**
- **Best LLM grounding**: 90% hallucination reduction (FalkorDB)
- Semantic similarity + relational reasoning
- Addresses Jerry's core mission (knowledge accumulation + problem solving)

**Weaknesses:**
- **Highest complexity**: Property graph + RDF + vector embeddings + context merger
- Most maintenance burden (multiple systems to coordinate)
- Embedding pipeline management (indexing, updates, dimensions)

**Score:** 18/25 (72%)
- Performance: 4/5
- Maintainability: 2/5
- Scalability: 4/5
- Cost: 4/5
- Standards: 4/5

**Verdict:** Strategic but complex—best deployed as **enhancement layer on top of Option 3** rather than standalone.

## Decision

We will adopt the **Hybrid Property + RDF Architecture (Option 3)** with the following implementation strategy:

### Core Architecture

1. **Primary Storage:** Property graph with file-based JSON/TOON persistence (existing Phase 1)
2. **Operational Queries:** Gremlin traversal for hot-path performance (< 50ms P95)
3. **Semantic Layer:** RDF serialization adapters for cold-path interoperability
4. **Representation Formats:** JSON, TOON, JSON-LD, Turtle, GraphSON (Netflix UDA pattern)
5. **Embedded Databases:** pyoxigraph for RDF storage, zero infrastructure costs through Phase 3
6. **Graph Enhancement (Phase 3):** HybridRAG layer combining vector retrieval (docs/) with graph traversal (Work Tracker)

### Four-Phase Implementation Roadmap

| Phase | Focus | Timeline | Capabilities |
|-------|-------|----------|--------------|
| **Phase 1: Foundation** | Property graph abstractions, file storage | ✅ COMPLETE | Vertex/Edge/VertexProperty, JSON/TOON, Jerry URIs |
| **Phase 2: Semantic Layer** | RDF serialization, JSON-LD, vector RAG | 🎯 Q1 2026 | pyoxigraph, JSON-LD contexts, SHACL, vector search |
| **Phase 3: Advanced Capabilities** | SPARQL endpoint, OWL ontology, GraphRAG | 🔮 Q2-Q3 2026 | Content negotiation, reasoning, grounding verification |
| **Phase 4: Scale (Optional)** | Server-based deployment, cloud migration | 🔮 Q4 2026+ | Neptune/Fuseki evaluation, clustering, > 10M entities |

### Technology Stack

**Phase 2 (Immediate):**
- **RDF Storage:** pyoxigraph (pure Rust, embedded, zero Java)
- **RDF Serialization:** Turtle, JSON-LD, RDF* (via pyoxigraph)
- **Validation:** SHACL shapes for constraint validation
- **Vector Search:** text-embedding-3-small + FAISS/ChromaDB (embedded)
- **Supernode Prevention:** Edge count monitoring with 100/1000 warning/error thresholds

**Phase 3 (Future):**
- **SPARQL Endpoint:** Flask + pyoxigraph with HTTP content negotiation
- **Ontology:** OWL-DL (decidable reasoning) via jerry-ontology.ttl
- **Grounding:** MiniCheck for verification (GPT-4 accuracy at 400x lower cost)
- **Visualization:** Cytoscape.js for graph exploration

**Phase 4 (If Needed):**
- **Trigger Conditions:** Multi-tenant access OR > 10M entities OR clustering/HA required
- **Options:** Apache Jena Fuseki (open-source), AWS Neptune (managed), stay embedded (baseline)

## Rationale

### Evidence from Research

This decision is supported by **unanimous consensus across 5 independent research documents**:

1. **Pattern Support:** PAT-001 (Hybrid Property Graph + RDF) and PAT-002 (Four-Phase Maturity Model) received unanimous support (5/5 documents)
2. **Decision Matrix:** Hybrid architecture scored 22/25 (88%)—highest of all options evaluated
3. **Production Validation:** Netflix UDA pattern deployed at scale, 4/5 documents cite this as architectural ideal
4. **Standards Adoption:** JSON-LD at 70% web adoption, 45M+ Schema.org websites, W3C RDF 1.2 with modern features (RDF*)

### Evidence from Case Studies

5. **FalkorDB:** 90% hallucination reduction with GraphRAG
6. **LinkedIn:** 63% faster ticket resolution (40hrs → 15hrs) with knowledge graph grounding
7. **Amazon Finance:** 49% → 86% accuracy improvement with GraphRAG
8. **ROI Validation:** 300-320% return on investment from knowledge graph initiatives

### Evidence from Jerry's Context

9. **Backward Compatible:** Jerry's existing Phase 1 property graph foundation remains intact—no throwaway work
10. **Jerry URI Scheme:** Already RDF-compatible (SPEC-001), minimal changes needed for semantic web integration
11. **Zero-Dependency Core:** Semantic capabilities live in infrastructure layer (pyoxigraph), domain layer stays pure Python stdlib
12. **Constitutional Alignment:** Supports P-001 (Truth and Accuracy) via grounding verification, P-002 (File Persistence) via multiple serialization formats

### Why Not Property Graph Only?

- Misses 90% hallucination reduction from GraphRAG
- Cannot achieve 5-star Linked Open Data status
- No standards-based interoperability
- Strategically limiting—Jerry's knowledge architecture becomes competitive differentiator

### Why Not RDF Only?

- 10x slower query performance (50-500ms SPARQL vs 5-10ms Gremlin)
- Breaks backward compatibility—throws away Phase 1 work
- Highest learning curve—semantic web stack unfamiliar
- Premature optimization for scale Jerry may never need

### Why Not Vector DB Only?

- Cannot answer relational queries ("What blocks this task?")
- Loses Work Tracker graph structure (tasks → phases → plans)
- No standards compliance (proprietary vector formats)

### Why Hybrid Wins

**Performance:** Hot path uses fast property graph (5-10ms), cold path uses RDF export (no performance impact on operations)

**Standards:** RDF export provides W3C compliance without end-to-end RDF overhead

**Risk:** Incremental phases with clear go/no-go gates—can stop at Phase 2 if advanced features not needed

**Flexibility:** Netflix UDA "Model Once, Represent Everywhere"—single domain model, multiple representations via adapters

**Validation:** Unanimous cross-document support + production case studies + Jerry's existing foundation

## Consequences

### Positive Consequences

1. **Strategic Differentiation via LLM Grounding**
   - 90% hallucination reduction for Claude Code agents (FalkorDB case study)
   - 63% faster issue resolution (LinkedIn case study)
   - Jerry citations via URI scheme enable transparent sourcing
   - Agents can ground responses in accumulated Jerry knowledge

2. **Standards Compliance Without Performance Cost**
   - 5-star Linked Open Data status (Tim Berners-Lee model)
   - W3C RDF, SPARQL, JSON-LD interoperability
   - Integration with Schema.org ecosystem (45M+ websites)
   - Property graph hot path maintains < 50ms P95 latency

3. **Incremental Risk Management**
   - Each phase delivers independent value
   - High reversibility in Phase 2 (JSON-LD optional extension)
   - Can stop at Phase 2 if advanced capabilities not needed
   - Clear go/no-go gates prevent premature optimization

4. **Zero-Dependency Core Preserved**
   - Semantic capabilities in infrastructure layer (pyoxigraph)
   - Domain layer remains pure Python stdlib
   - Embedded databases through Phase 3 ($0 infrastructure)
   - Server-based only if > 10M entities (Phase 4 triggers)

5. **Production-Validated Pattern**
   - Netflix UDA deployed at scale (4/5 documents cite)
   - GraphRAG production case studies (FalkorDB, LinkedIn, Amazon)
   - JSON-LD 70% web adoption (not experimental technology)
   - Modern tooling (Oxigraph in Rust/Python, not legacy Java)

6. **Knowledge as Durable Asset**
   - Accumulated knowledge persists across sessions
   - Graph structure captures relationships (blocks, depends-on, created-by)
   - Multiple serialization formats prevent vendor lock-in
   - Formal validation (SHACL) prevents schema drift

### Negative Consequences

1. **Architectural Complexity Increase**
   - **Issue:** Multiple representation formats (JSON, TOON, JSON-LD, Turtle, GraphSON) require synchronization
   - **Impact:** More code surface area, more potential bugs, testing matrix explosion
   - **Mitigation:** Netflix UDA pattern (serializers as pure functions, no business logic), automated round-trip tests, defer optional serializers to Phase 3

2. **Learning Curve for Semantic Web**
   - **Issue:** SPARQL, SHACL, OWL, RDF concepts unfamiliar to most developers
   - **Impact:** Steeper onboarding for contributors, slower initial development velocity
   - **Mitigation:** Document in `docs/contributing/SERIALIZATION_GUIDE.md`, Phase 2 focuses on JSON-LD (most accessible semantic format), defer SPARQL/OWL to Phase 3

3. **Dependency Expansion**
   - **Issue:** pyoxigraph (RDF storage), embedding models (vector RAG), potentially MiniCheck (grounding)
   - **Impact:** Goes against Jerry's zero-dependency principle (though dependencies in infrastructure layer, not domain)
   - **Mitigation:** All dependencies optional (infrastructure layer only), embedded deployment avoids server dependencies, Phase 2 evaluates pyoxigraph sufficiency before deeper investment

4. **Multi-Layer Validation Overhead**
   - **Issue:** Schema validation + SHACL constraints + supernode detection + grounding verification = latency accumulation
   - **Impact:** Save operations slower, more complex error handling
   - **Mitigation:** Asynchronous validation (non-blocking), performance budgets (P95 < 50ms for hot path), grounding verification optional (Phase 3)

5. **Synchronization Between Property Graph and RDF**
   - **Issue:** Changes to domain model require updates across multiple serializers
   - **Impact:** Risk of format divergence, inconsistent representations
   - **Mitigation:** Netflix UDA pattern (single source of truth = domain model), automated round-trip tests catch divergence, schema versioning (P-030 constitutional requirement)

6. **Risk of Premature Optimization**
   - **Issue:** Building Phase 3-4 capabilities (SPARQL, reasoning, server-based) Jerry may never need
   - **Impact:** Time invested in semantic infrastructure vs domain features, over-engineering
   - **Mitigation:** Phase gates with explicit go/no-go criteria, Phase 3 requires user validation of Phase 2 value, Phase 4 requires quantitative triggers (> 10M entities, multi-tenant, clustering)

### Neutral Consequences (Context-Dependent)

1. **Schema Evolution Requires Governance**
   - Positive: Explicit schema versioning prevents drift
   - Negative: Migration scripts add overhead
   - Constitutional requirement P-030 enforces this

2. **Embedded vs Server-Based Choice Deferred**
   - Positive: No premature infrastructure costs
   - Negative: Phase 4 migration effort if triggers crossed
   - Assumption ASM-001 documents this explicitly

3. **Vector Embeddings Add Storage Overhead**
   - Positive: Enables semantic search for docs/
   - Negative: Embedding generation latency, storage 2-3x growth
   - Can use embedded ChromaDB/FAISS (no cloud costs)

## Risks

### Risk 1: Supernode Performance Degradation (Actor Vertex) — CRITICAL

**Description:** Actor vertex (representing Claude) could accumulate thousands of edges as it creates tasks, leading to catastrophic O(n) traversal performance where n = edge count.

**Probability:** HIGH (synthesis document rates Actor as HIGH supernode risk)

**Impact:** HIGH (performance degradation affects all agents, queries slow from 5-10ms to 500ms+)

**Risk Score:** 9/9 (Critical)

**Mitigations:**
1. **Preventive Monitoring:** Edge count validator with 100 (warn) / 1000 (error) thresholds
2. **Temporal Partitioning:** Use time-based edge labels (`CREATED_BY_2026_01` not generic `CREATED_BY`)
3. **Hierarchical Decomposition:** Create intermediate Actor nodes (`Actor:Claude:Session:2026-01-08`)
4. **Constitutional Enforcement:** P-031 (Supernode Prevention) requires mitigation strategy for HIGH-risk vertices
5. **Quantitative Validation:** Test with 10,000 synthetic tasks to verify mitigation effectiveness

**Residual Risk:** LOW (if mitigations implemented in Phase 2 Week 1-2)

---

### Risk 2: Complexity Overhead Slowing Development Velocity — MODERATE

**Description:** Multi-representation architecture creates maintenance burden (property graph + JSON + TOON + JSON-LD + Turtle + GraphSON), slowing feature development.

**Probability:** MEDIUM (5 serializers confirmed in Phase 2)

**Impact:** MEDIUM (slower velocity, but not catastrophic; estimated 20-30% overhead)

**Risk Score:** 4/9 (Moderate)

**Mitigations:**
1. **Netflix UDA Pattern Enforcement:** Single domain model, serializers as pure functions (no business logic)
2. **Automated Testing:** Parametrized round-trip tests for all serializers, catch divergence early
3. **Defer Optional Serializers:** Phase 2 focuses on JSON + TOON + JSON-LD (essential), defer Turtle + GraphSON to Phase 3
4. **Contributor Documentation:** `docs/contributing/SERIALIZATION_GUIDE.md` with clear examples

**Success Metric:** Time-to-implement new entity type < 2 hours including all serializers

**Residual Risk:** MEDIUM (complexity inherent to multi-representation architecture)

---

### Risk 3: Premature Phase 4 Migration (Server-Based Infrastructure) — LOW-MODERATE

**Description:** Migrating to server-based triple store (Fuseki, Neptune) before necessary, incurring infrastructure costs ($100-1000/month) and operational overhead.

**Probability:** LOW (Phase 4 clearly marked "if scale demands")

**Impact:** HIGH (monthly costs + migration effort measured in weeks + operational complexity)

**Risk Score:** 3/9 (Low-Moderate)

**Mitigations:**
1. **Explicit Trigger Conditions:** Multi-tenant access OR > 10M entities OR clustering/HA required (documented in ASM-001, ASM-002)
2. **Quantitative Monitoring:** Entity count alerts at 8M (80% of 10M threshold), query latency alerts if P95 > 500ms
3. **Phase 4 Evaluation Checklist:** Requires user approval + cost-benefit analysis before migration
4. **Constitutional Gate:** P-032 (Phase Gate Compliance) prevents premature advancement

**Residual Risk:** LOW (clear gates + monitoring prevent premature migration)

---

### Risk 4: Schema Evolution Breaking Graph Traversals — MODERATE-HIGH

**Description:** Changes to graph schema (vertex types, edge labels, property names) break existing Gremlin queries and agent traversal logic.

**Probability:** MEDIUM (Jerry is evolving system, schema changes inevitable)

**Impact:** HIGH (breaks agent functionality, requires code updates across system)

**Risk Score:** 6/9 (Moderate-High)

**Mitigations:**
1. **Schema Versioning:** Semantic versioning (v2.0.0), compatibility validation, major version changes signal breaking changes
2. **Forward Migration Scripts:** Every schema change includes migration script (e.g., `migrations/001_add_blocking_reason.py`)
3. **Rollback Migration Scripts:** Every schema change includes rollback script for reversibility
4. **Schema Changelog:** `docs/specifications/SCHEMA_CHANGELOG.md` documents all changes (constitutional requirement P-030)
5. **Integration Tests:** Traversal test suite runs against schema versions, catches breaking changes before deployment

**Residual Risk:** MEDIUM (can't eliminate schema evolution, but can manage it systematically)

---

### Risk 5: LLM Grounding Verification False Positives — LOW

**Description:** MiniCheck grounding verification incorrectly flags factually correct responses as "not supported," causing agent warnings and user confusion.

**Probability:** MEDIUM (grounding models have error rates; MiniCheck GPT-4-level accuracy but not perfect)

**Impact:** LOW (soft warnings logged, doesn't block functionality; user can review and override)

**Risk Score:** 2/9 (Low)

**Mitigations:**
1. **Confidence Threshold Tuning:** Set threshold at 0.7 (tune based on false positive rate in production)
2. **Soft Warnings (Non-Blocking):** Emit CloudEvent warning, don't block LLM response
3. **Defer to Phase 3:** Grounding verification optional in Phase 2 (simpler Jerry URI citations first), add verification in Phase 3 when models mature
4. **User Feedback Loop:** Allow users to mark false positives, retrain threshold based on feedback

**Success Metric:** False positive rate < 5% on golden dataset

**Residual Risk:** LOW (soft warnings, not hard failures; optional feature)

---

### Risk Summary Table

| Risk ID | Description | Probability | Impact | Score | Residual Risk |
|---------|-------------|-------------|--------|-------|---------------|
| **RISK-1** | Supernode degradation (Actor vertex) | HIGH | HIGH | 9/9 | LOW (strong mitigations) |
| **RISK-2** | Complexity slowing development | MEDIUM | MEDIUM | 4/9 | MEDIUM (inherent tradeoff) |
| **RISK-3** | Premature Phase 4 migration | LOW | HIGH | 3/9 | LOW (clear gates) |
| **RISK-4** | Schema evolution breaking traversals | MEDIUM | HIGH | 6/9 | MEDIUM (systematic management) |
| **RISK-5** | Grounding verification false positives | MEDIUM | LOW | 2/9 | LOW (soft warnings) |

**Overall Risk Profile:** MODERATE (most high-impact risks have strong mitigations; residual risks acceptable)

## Implementation Plan

### Phase 2: Semantic Layer (Q1 2026) — 8 Weeks

#### Week 1-2: Foundation

**Deliverables:**
- Create JSON-LD context: `contexts/worktracker.jsonld`
  - Map Jerry entities to Schema.org (Task → schema:Action, Actor:Human → schema:Person, Actor:Claude → schema:SoftwareApplication)
  - Define custom Jerry vocabulary (`jerry:blockingReason`, `jerry:Phase`, etc.)
  - Reference: Schema.org 803 types, 1,461 properties

- Implement supernode validator (RISK-1 mitigation):
  ```python
  class SupernodeValidator:
      WARN_THRESHOLD = 100
      ERROR_THRESHOLD = 1000

      def validate_vertex_degree(self, vertex_id, edge_label, edge_count):
          if edge_count >= ERROR_THRESHOLD:
              raise SupernodeError(f"Supernode detected: {vertex_id}")
          elif edge_count >= WARN_THRESHOLD:
              log.warning(f"Approaching supernode: {vertex_id} ({edge_count} edges)")
  ```

- Add edge count monitoring to repository save operations
- Document Netflix UDA pattern in `docs/design/MULTI_REPRESENTATION_PATTERN.md`

**Success Criteria:**
- JSON-LD context validates against JSON-LD 1.1 spec
- Supernode validator catches edges >= 100 (warning) and >= 1000 (error)
- Pattern documentation reviewed and approved

---

#### Week 3-4: RDF Serialization

**Deliverables:**
- Install pyoxigraph: `pip install pyoxigraph`
- Create RDF serialization adapter: `src/infrastructure/persistence/rdf_adapter.py`
  - Implement Turtle serialization for Task/Phase/Plan entities
  - Implement JSON-LD serialization using contexts/worktracker.jsonld
  - Implement RDF* for edge properties (no reification overhead)

- Create SHACL validation shapes: `schemas/worktracker-shapes.ttl`
  - Task shape: title (required), status (enum), blocking_reason (optional)
  - Phase shape: name (required), description (optional)
  - Plan shape: goal (required), context (optional)

- Automated round-trip tests (RISK-2 mitigation):
  ```python
  @pytest.mark.parametrize("serializer", [
      JsonSerializer, ToonSerializer, JsonLdSerializer, RdfTurtleSerializer
  ])
  def test_round_trip(serializer):
      task = Task(title="Test", status="IN_PROGRESS")
      serialized = serializer.serialize(task)
      deserialized = serializer.deserialize(serialized)
      assert task == deserialized
  ```

**Success Criteria:**
- All Jerry entities serializable to Turtle and JSON-LD
- SHACL shapes validate against entities (0 constraint violations)
- Round-trip tests pass at 100% success rate

---

#### Week 5-6: Vector RAG (Foundation for HybridRAG)

**Deliverables:**
- Index `docs/` with text-embedding-3-small (OpenAI API or local model)
- Store embeddings in TOON format alongside documents:
  ```toon
  {
    file: "docs/experience/LES-001-hybrid-prevents-lockin.md"
    embedding: [0.023, -0.142, 0.089, ...]  # 1536 dimensions
    chunk_boundaries: [0, 500, 1000, 1500]
    metadata: {indexed_at: 2026-01-08T10:30:00Z}
  }
  ```

- Implement cosine similarity search:
  ```python
  def retrieve_docs(query: str, top_k: int = 5) -> List[Document]:
      query_embedding = embed(query)
      results = []
      for doc in all_docs:
          similarity = cosine_similarity(query_embedding, doc.embedding)
          results.append((doc, similarity))
      return sorted(results, key=lambda x: x[1], reverse=True)[:top_k]
  ```

- Test with Claude Code agent queries: "What tasks block TASK-042?" → retrieve relevant docs + traverse BLOCKS edges

**Success Criteria:**
- docs/ indexed with embeddings (all markdown files covered)
- Vector search returns relevant results (qualitative assessment by user)
- Integration test passes: query returns both docs/ content and Work Tracker relationships

---

#### Week 7-8: Integration & Testing

**Deliverables:**
- Performance benchmarks:
  - Property graph query latency (baseline): Target P95 < 10ms
  - RDF export latency (non-blocking): Target P95 < 100ms
  - Vector search latency: Target P95 < 50ms

- Schema evolution integration tests (RISK-4 mitigation):
  ```python
  def test_schema_migration_backward_compatibility():
      # Create entity with v1 schema
      task_v1 = Task(title="Test", status="TODO")
      task_v1.save()

      # Apply migration to v2 (adds blocking_reason field)
      apply_migration("001_add_blocking_reason")

      # Verify v1 entity still loadable
      loaded_task = Task.load(task_v1.id)
      assert loaded_task.title == "Test"
      assert loaded_task.blocking_reason is None  # Default value
  ```

- Contributor documentation: `docs/contributing/SERIALIZATION_GUIDE.md`
  - How to add new entity types
  - Netflix UDA pattern explanation
  - Serializer implementation checklist

- Constitutional amendments: Add P-030 (Schema Evolution Governance), P-031 (Supernode Prevention), P-032 (Phase Gate Compliance) to `docs/governance/JERRY_CONSTITUTION.md`

**Success Criteria:**
- All performance benchmarks meet targets (P95 < 50ms hot path)
- Schema migration tests pass (100% backward compatibility)
- Contributor guide reviewed and approved by user
- Constitutional amendments integrated

---

### Phase 3: Advanced Capabilities (Q2-Q3 2026) — 12 Weeks

**Conditional on Phase 2 Success:** Proceed ONLY if Phase 2 go/no-go criteria met (see Success Criteria section below).

#### Month 4-5: GraphRAG & Grounding

**Deliverables:**
- Extend Work Tracker entities with embedding properties
- Implement graph traversal retrieval (Gremlin):
  ```python
  def retrieve_blocking_tasks(task_id: str) -> List[Task]:
      return g.V(task_id).out('BLOCKS').toList()
  ```

- Create HybridRAG context merger:
  ```python
  def hybrid_retrieve(query: str) -> GroundingContext:
      # Parallel retrieval
      vector_results = retrieve_docs(query, top_k=5)  # docs/ semantic search
      graph_results = retrieve_related_entities(query)  # Work Tracker traversal

      # Deduplicate and rank
      merged = deduplicate(vector_results + graph_results)
      return GroundingContext(sources=merged, citations=[...])
  ```

- Add Jerry URI citations to LLM responses:
  ```
  Response: "TASK-042 is blocked by TASK-038 due to missing dependency."
  Citations:
  - jer:jer:work-tracker:task:TASK-042
  - jer:jer:work-tracker:task:TASK-038
  - jer:jer:work-tracker:edge:BLOCKS:abc123
  ```

- Integrate MiniCheck model (optional):
  - Evaluate model on golden dataset (false positive rate < 5%)
  - Add verification step to RAG pipeline (non-blocking, soft warnings)
  - Log verification results as CloudEvents

**Success Criteria:**
- Claude Code agents can query Jerry knowledge base (both docs/ and Work Tracker)
- Responses include Jerry URI citations for all factual claims
- Measurable hallucination reduction (baseline vs RAG, user evaluation)

---

#### Month 5-6: SPARQL & Content Negotiation

**Deliverables:**
- SPARQL endpoint (Flask + pyoxigraph):
  ```python
  @app.route('/sparql', methods=['POST'])
  def sparql_query():
      query = request.form.get('query')
      results = oxigraph_store.query(query)
      return jsonify(results), 200
  ```

- Content negotiation for Jerry URIs (PAT-010):
  ```python
  @app.route('/jer/work-tracker/task/<task_id>')
  def resolve_task_uri(task_id: str):
      accept = request.headers.get('Accept', 'application/json')

      if 'application/ld+json' in accept:
          return jsonify(task_as_jsonld), 200
      elif 'text/turtle' in accept:
          return task_as_turtle, 200, {'Content-Type': 'text/turtle'}
      elif 'text/html' in accept:
          return render_template('task.html', task=task), 200
      else:
          return jsonify(task_as_json), 200
  ```

- OWL-DL ontology (decidable reasoning): `ontologies/jerry-ontology.ttl`
  - Define Jerry vocabulary classes (jerry:Task, jerry:Phase, jerry:Plan)
  - Define property restrictions (jerry:blockingReason domain jerry:Task)
  - Map to Schema.org (jerry:Task rdfs:subClassOf schema:Action)

**Success Criteria:**
- SPARQL endpoint responds to queries (test with `SELECT * WHERE { ?s ?p ?o } LIMIT 10`)
- Content negotiation returns correct format based on Accept header
- OWL ontology validates (Protégé or OWL validator)

---

#### Month 6-7: Visualization & Monitoring

**Deliverables:**
- Cytoscape.js graph visualization
- Knowledge architecture health dashboard:
  | Metric | Alert Threshold | Current Value |
  |--------|----------------|---------------|
  | Entity count | 8M (80% of Phase 4 trigger) | 1,234 |
  | Query latency P95 | > 500ms | 12ms |
  | Max vertex degree | > 80 (80% of warning) | 23 (Actor:Claude) |
  | Serialization round-trip time | > 100ms | 45ms |
  | Grounding false positive rate | > 5% | 2.3% |

- CloudEvents integration for monitoring alerts

**Success Criteria:**
- Dashboard deployed and accessible
- Alerts trigger correctly at thresholds
- User reviews dashboard weekly

---

### Phase 4: Scale (Optional — Q4 2026+)

**Trigger Conditions (MUST meet at least one):**
- Multi-tenant SaaS offering required
- > 10M entities in production (currently: thousands)
- P95 query latency > 500ms (currently: < 50ms)
- Clustering/HA required for uptime SLA

**Do NOT proceed to Phase 4 unless one trigger condition met.**

**Evaluation Checklist:**
```markdown
## Phase 4 Migration Checklist

Only proceed if answering YES to one or more:
- [ ] Multi-tenant SaaS offering planned?
- [ ] > 8M entities in production?
- [ ] P95 query latency > 500ms?
- [ ] Clustering/HA required for uptime SLA?

If all NO, remain on embedded Phase 2-3 architecture.
```

**If Triggered, Evaluate:**
- **Option A:** Apache Jena Fuseki (open-source, self-hosted, full SPARQL 1.1)
- **Option B:** AWS Neptune (managed, high availability, $100-1000/month)
- **Option C:** Stay embedded with optimizations (index tuning, caching, query optimization)

**Migration Effort:** Estimated 2-4 weeks (schema export, data migration, testing, deployment)

**Cost Analysis Required:** Cloud costs vs performance gains, user approval mandatory

---

## Success Criteria

### Phase 2 Go/No-Go Gates (Week 8)

Proceed to Phase 3 ONLY if all criteria met:

| Criterion | Metric | Target | Measurement |
|-----------|--------|--------|-------------|
| **Backward Compatibility** | % of existing tests passing | 100% | pytest suite (all Phase 1 tests) |
| **Performance (Hot Path)** | Query latency P95 | < 50ms | Benchmark suite (property graph queries) |
| **Performance (Cold Path)** | RDF export latency P95 | < 100ms | Benchmark suite (Turtle, JSON-LD) |
| **Serialization Correctness** | Round-trip success rate | 100% | Parametrized tests (all serializers) |
| **Supernode Prevention** | Edge count monitoring | Alerts working | Synthetic test (10,000 tasks) |
| **Documentation** | Contributor onboarding time | < 4 hours | User time tracking |

**If any criterion fails:** Pause Phase 3, address issues, re-evaluate.

---

### Phase 3 Go/No-Go Gates (Month 7)

Proceed to Phase 4 evaluation ONLY if:

| Criterion | Evidence Required |
|-----------|------------------|
| ✅ **Phase 2 Success** | All Phase 2 criteria met |
| ✅ **User Validation** | User feedback confirms semantic layer value (surveys, usage metrics) |
| ✅ **Use Case Demand** | SPARQL queries or reasoning required for actual use cases (not theoretical) |
| ✅ **HybridRAG Impact** | Measurable hallucination reduction (baseline vs RAG comparison, user evaluation) |

**Do NOT proceed to Phase 3 if:**
- ❌ Phase 2 increases query latency > 100ms (hot path degraded)
- ❌ Maintenance overhead slows development velocity > 30% (time tracking)
- ❌ No external integration use cases emerge (user feedback)
- ❌ User satisfaction high with Phase 2 capabilities alone (surveys)

---

### Phase 4 Trigger Conditions (Ongoing Monitoring)

Phase 4 migration triggered ONLY if:
- Multi-tenant access required (user requests)
- > 10M entities (dashboard alerts at 8M)
- P95 query latency > 500ms (dashboard monitoring)
- Clustering/HA required (user SLA requirements)

**Monitor quarterly** via Work Tracker.

## Related Decisions

- **SPEC-001: Jerry URI Scheme** — Existing Jerry URI scheme is RDF-compatible, Phase 2 builds on this foundation
- **ADR-XXX: Work Tracker Graph Model** (future) — Will document Phase 1 property graph design
- **ADR-XXX: Constitutional Principles for Knowledge Architecture** (future) — Will formalize P-030, P-031, P-032
- **ASM-001: Jerry Will Remain Single-Tenant Through Phase 3** (future) — Documents assumption that embedded deployment sufficient
- **ASM-002: Property Graph Performance Sufficient for Jerry Scale** (future) — Documents assumption that < 10M entities

## References

### Primary Sources

- **docs/synthesis/work-031-e-006-synthesis.md** — Cross-document synthesis of 5 research reports (1,142 lines)
  - Braun & Clarke thematic analysis
  - 10 architectural patterns (PAT-001 through PAT-010)
  - L0/L1/L2 multi-level synthesis (ELI5, technical, strategic)

- **docs/analysis/work-031-e-007-trade-off-analysis.md** — ATAM-inspired quality attribute trade-off analysis (821 lines)
  - SWOT analysis (6 strengths, 6 weaknesses, 6 opportunities, 6 threats)
  - Quality attribute trade-offs (4 ATAM scenarios)
  - Decision matrix (5 options scored on 5 criteria)
  - Risk analysis (top 5 risks with mitigation strategies)

### Research Evidence (via Synthesis)

**Pattern Support:**
- PAT-001: Hybrid Property Graph + RDF Architecture — **Unanimous support (5/5 documents)**
- PAT-002: Four-Phase Knowledge Architecture Maturity Model — **Unanimous support (5/5 documents)**
- PAT-003: Netflix UDA "Model Once, Represent Everywhere" — **Strong support (4/5 documents)**

**Case Studies:**
- **FalkorDB:** 90% hallucination reduction with GraphRAG
- **LinkedIn:** 63% faster ticket resolution (40hrs → 15hrs) with knowledge graph grounding
- **Amazon Finance:** 49% → 86% accuracy improvement with GraphRAG
- **Netflix UDA:** Production-proven pattern at scale (Unified Data Architecture)

**Standards:**
- **W3C RDF 1.2:** RDF* for edge properties without reification
- **W3C SPARQL 1.2:** Improved query performance
- **W3C JSON-LD 1.1:** 70% web adoption (Web Data Commons 2024)
- **Schema.org:** 45M+ websites, 803 types, 1,461 properties
- **Tim Berners-Lee 5-Star Linked Open Data:** Jerry at 4 stars, targeting 5 stars

**Technologies:**
- **pyoxigraph:** Embedded RDF store in Rust/Python, zero Java dependencies
- **Gremlin/TinkerPop:** Property graph query language, Apache standard
- **MiniCheck:** Grounding verification (GPT-4 accuracy at 400x lower cost, 770M parameters)
- **FAISS/ChromaDB:** Embedded vector databases for semantic search

### Research Methods

- **Braun & Clarke Thematic Analysis:** 6-phase qualitative method for pattern extraction (synthesis document)
- **ATAM (Architecture Tradeoff Analysis Method):** Quality attribute scenario analysis, Carnegie Mellon SEI (analysis document)
- **SWOT Analysis:** Strategic planning framework for identifying strengths, weaknesses, opportunities, threats (analysis document)
- **Decision Matrix:** Multi-criteria decision analysis with weighted scoring (analysis document)
- **Risk Matrix:** Probability × Impact scoring with mitigation strategies (analysis document)

### Industry Prior Art

- **Netflix UDA (Unified Data Architecture):** "Conceptual RDF, Flexible Physical" pattern
- **Microsoft Research GraphRAG:** Knowledge graph-based retrieval for LLM grounding
- **FalkorDB GraphRAG:** Production deployment case study
- **Neo4j Graph Modeling:** Supernode problem and mitigation strategies
- **DataStax Graph Best Practices:** Property graph modeling at scale

### Jerry Documentation

- **CLAUDE.md:** Jerry framework root context, architecture overview
- **docs/governance/JERRY_CONSTITUTION.md:** Constitutional principles for agent governance
- **docs/knowledge/:** Accumulated knowledge hierarchy
- **docs/experience/:** Lessons learned (LES items)
- **docs/wisdom/:** Distilled wisdom (WIS items)

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-08 | ps-architect agent (v2.0.0) | Initial ADR created from synthesis work-031-e-006 and analysis work-031-e-007 |

---

*Decision Record Method: Michael Nygard ADR Format*
*Decision: Hybrid Property + RDF Architecture (22/25, 88%)*
*Top Risk: Supernode degradation (9/9 Critical, strong mitigations)*
*Agent: ps-architect (v2.0.0)*
*Constitution Compliance: P-001 (all claims cited), P-002 (decision persisted to file)*
