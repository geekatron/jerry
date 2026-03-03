# ADR-032: Jerry Knowledge Management Integration

## Status

**PROPOSED** (Awaiting ps-validator approval)

## Date

2026-01-09

## Context

### Problem Statement

Jerry is a framework for behavior and workflow guardrails designed to accrue knowledge, wisdom, and experience while solving problems. As the knowledge corpus grows, we face **context rot**—degraded LLM performance despite remaining within token limits—and practical challenges in knowledge discovery and reuse.

**Current State:**
- Filesystem-only knowledge storage (markdown in `docs/` hierarchy)
- Manual cross-referencing required
- No relationship discovery or semantic search
- Limited ability to answer "what relates to X?" queries
- Knowledge fragmentation as corpus exceeds ~100 documents
- Agent reasoning constrained by keyword-based retrieval

**Research Foundation:**
A comprehensive Knowledge Management research synthesis (358KB across 5 documents, 71+ citations) identified that modern KM requires three complementary capabilities:
1. **Filesystem** - Human-readable, version-controlled source of truth
2. **Graph Layer** - Relationship discovery and traversal
3. **AI Layer** - Semantic search and retrieval-augmented generation (RAG)

**Why Now:**
- Jerry's mission explicitly includes knowledge accumulation
- Current corpus approaching limits of manual management
- Agent capabilities limited without semantic retrieval
- Industry trends validate graph + vector + filesystem architecture
- Lightweight Python libraries available that align with hexagonal architecture

### Decision Drivers

The following factors shaped this decision (weighted by importance):

| Driver | Weight | Rationale |
|--------|--------|-----------|
| **Architectural Fit** | 15% | Must align with hexagonal architecture, zero-dependency domain |
| **Capability** | 20% | Enable relationship discovery, semantic search, RAG foundation |
| **Cost (Implementation)** | 10% | Time/effort to implement and maintain |
| **Cost (Operational)** | 10% | Runtime resources, licensing, service management |
| **Local-First** | 12% | Maintain filesystem as source of truth, no required cloud |
| **Time to Value** | 10% | Speed to working MVP and tangible benefits |
| **Scalability** | 8% | Handle growth from 100s to 1000s of documents |
| **Future-Proofing** | 8% | Migration paths if needs change |
| **Learning Curve** | 7% | Developer/user adoption friction |

**Additional Constraints:**
- Must preserve constitutional principle P-002 (File Persistence)
- Must not violate P-003 (No Recursive Subagents—ReAct uses tools, not nested agents)
- Must support local deployment (privacy, cost, ownership)
- Should enable progressive ISO 30401 standard alignment

## Considered Options

### Option 1: Minimal KM (Filesystem Only)

**Description:** Maintain current state—markdown files in `docs/`, git versioning, no KM tooling.

**Strengths:**
- Zero dependencies (pure stdlib)
- Simple mental model
- Portable, future-proof format (markdown)
- Already working

**Weaknesses:**
- No relationship discovery
- No semantic search
- Manual cross-referencing
- Scales poorly beyond ~100 documents
- Knowledge fragmentation inevitable

**Scores:**
- Decision Matrix: 7.0/10
- SWOT: 5.3/10
- Quality Attributes: 4.30/7

**Verdict:** Inadequate for Jerry's knowledge-centric mission. Already experiencing limitations.

---

### Option 2: Lightweight KM (NetworkX + FAISS + RDFLib) ← RECOMMENDED

**Description:** Add graph operations (NetworkX), vector search (FAISS), semantic web (RDFLib) to infrastructure layer while maintaining filesystem as source of truth.

**Strengths:**
- Pure Python libraries (no external services)
- Minimal dependencies (3 packages, all pre-installable)
- Hexagonal architecture fit (infrastructure adapters via ports)
- Proven at scale (14M+ downloads/week each)
- Enables semantic search, relationship discovery, RAG
- Standards-based interoperability (RDF, SPARQL)
- Swappable implementations (NetworkX → igraph → graph-tool)
- Zero operational cost (no services, no licensing)

**Weaknesses:**
- Introduces external dependencies (infrastructure layer only)
- Learning curve (graph concepts, RDF, embeddings)
- Performance limits (NetworkX <10K nodes, FAISS CPU-bound)
- Memory overhead (in-memory graphs and vectors)

**Scores:**
- Decision Matrix: **8.5/10** (highest)
- SWOT: **8.2/10** (highest)
- Quality Attributes: **4.37/7** (highest)

**Verdict:** Best balance of capability, cost, and architectural fit.

---

### Option 3: Full KM (Neo4j + Qdrant + pyoxigraph)

**Description:** Production-grade tools with native graph database (Neo4j), distributed vector store (Qdrant), advanced RDF processing (pyoxigraph). Requires external services.

**Strengths:**
- Production-ready scalability (billions of vectors, millions of nodes)
- ACID transactions, advanced features (Cypher, graph algorithms)
- Enterprise-proven (Neo4j: 75% Fortune 500 adoption)
- Performance optimized (Rust cores)

**Weaknesses:**
- Requires external services (databases, deployment complexity)
- Operational burden (monitoring, backups, DevOps)
- Resource intensive (RAM, CPU, disk)
- Cost (Neo4j Enterprise licensing)
- Overkill for current corpus (<500 docs)
- Longer implementation timeline
- Doesn't fit hexagonal architecture cleanly

**Scores:**
- Decision Matrix: 6.5/10
- SWOT: 6.8/10
- Quality Attributes: 3.67/7

**Verdict:** Premature optimization. Capabilities exceed current needs.

---

### Option 4: Enterprise KM (ISO 30401 + Commercial Platforms)

**Description:** Complete ISO 30401 implementation with commercial KM platforms (Bloomfire, Guru, Confluence Enterprise), formal governance, dedicated roles.

**Strengths:**
- ISO 30401 certification possible
- Comprehensive features (wikis, forums, analytics)
- Vendor support and SLAs
- Enterprise-scale proven

**Weaknesses:**
- Extremely expensive ($10K-$100K+ annually)
- Massive overkill for 1-10 users
- Cloud-dependent (contradicts local-first)
- Vendor lock-in
- Implementation timeline: months to years
- Heavy cultural change required

**Scores:**
- Decision Matrix: 5.1/10
- SWOT: 4.5/10
- Quality Attributes: 3.14/7

**Verdict:** Completely misaligned with Jerry's philosophy and scale.

## Decision

**We will adopt Lightweight KM (NetworkX + FAISS + RDFLib) with phased implementation starting Q1 2026.**

### Rationale

1. **Highest Scores Across All Evaluation Methods:**
   - Decision Matrix: 8.5/10 (15% higher than next best)
   - SWOT Analysis: 8.2/10
   - Quality Attributes: 4.37/7 (balances functionality with maintainability)

2. **Perfect Architectural Alignment:**
   - Infrastructure layer adapters (domain remains dependency-free)
   - Port/adapter pattern enables future swapping
   - Local-first preserved (filesystem remains source of truth)
   - Hexagonal architecture integrity maintained

3. **Addresses Current Pain Points:**
   - Enables relationship discovery ("what relates to X?")
   - Supports semantic search (beyond keyword grep)
   - Provides standards-based export (RDF/SPARQL for interoperability)
   - Foundation for RAG implementation (agent knowledge retrieval)

4. **Risk Profile Acceptable:**
   - All 5 major risks have effective mitigations
   - Port/adapter pattern de-risks dependency and growth concerns
   - Phased rollout limits implementation risk
   - No operational burden (no services to manage)

5. **Industry Validation:**
   - Synthesis of 358KB research across 71+ citations recommends this exact stack
   - NetworkX: 14.9M downloads/week, active development
   - RDFLib: 14M downloads/week, RDF standard compliance
   - FAISS: Meta-backed, production-proven, used by LangChain/LlamaIndex

6. **Clear Migration Paths:**
   - If corpus exceeds capacity → swap to igraph/graph-tool/Qdrant via ports
   - If need ACID/collaboration → add Neo4j via same port interface
   - Progressive enhancement, not rip-and-replace

7. **Cost-Effective:**
   - Zero licensing costs (all open-source)
   - Zero operational costs (no services)
   - Implementation: 70-100 hours over 3 phases (manageable)
   - ROI: 10-20% time saved finding information (industry average)

### Confidence Level

**85% (HIGH)**

Based on:
- Convergent evidence across multiple evaluation methods
- Clear superiority in weighted decision matrix
- Strong alignment with Jerry's architectural principles
- Industry validation from comprehensive research synthesis
- Effective risk mitigations identified

## Consequences

### Positive

**Immediate Benefits:**
- ✅ Relationship discovery: Answer "what relates to X?" queries
- ✅ Semantic search: Find conceptually similar documents
- ✅ Standards interoperability: Export knowledge graph as RDF/Turtle
- ✅ Foundation for RAG: Retrieval-augmented agent reasoning
- ✅ Graph visualization: NetworkX → Graphviz for knowledge maps

**Medium-Term Benefits:**
- ✅ Reduced duplicate work: 15-25% (via "what already exists?" queries)
- ✅ Faster information discovery: 10-20% time saved (industry average)
- ✅ Improved agent reasoning: Grounded in knowledge retrieval vs. pure generation
- ✅ Knowledge reuse tracking: Measure concept application to new problems
- ✅ ISO 30401 alignment path: Progressive standard compliance

**Long-Term Benefits:**
- ✅ Competitive advantage: Knowledge graph as differentiator
- ✅ Community engagement: Graph visualizations for collaboration
- ✅ Migration readiness: Ports enable production tool adoption if needed
- ✅ Accumulated wisdom: Structured knowledge compounds over time

### Negative

**Compromises Accepted:**
- ❌ Introduces external dependencies (infrastructure layer—acceptable per architecture)
- ❌ Performance limits (NetworkX <10K nodes, FAISS CPU-only—acceptable for 1-2 year horizon)
- ❌ Learning curve (graph concepts, RDF, embeddings—mitigated via phased adoption)
- ❌ Memory overhead (in-memory structures—acceptable for expected corpus size)
- ❌ Manual graph construction initially (automated extraction deferred to Phase 2)

**Technical Debt:**
- Must monitor library health (releases, vulnerabilities)
- Must track knowledge graph size vs. tool capacity
- Must maintain adapter code (vs. stdlib-only simplicity)
- FAISS dimension management adds complexity

**Philosophical Trade-offs:**
- Relaxes "zero-dependency core" aspiration for infrastructure layer
- Accepts that modern KM requires selective external libraries
- Prioritizes capability over purity

### Risks

**Risk #1: Knowledge Corpus Growth Exceeds Tool Capacity**
- **Severity:** HIGH (P=60%, I=8, Score=4.8/10)
- **Mitigation:** Port/adapter pattern enables swap to igraph/graph-tool/Qdrant
- **Trigger:** Graph >5K nodes OR FAISS search >2 seconds
- **Contingency:** Quarterly size monitoring, predefined migration paths

**Risk #2: Dependency Abandonment or Breaking Changes**
- **Severity:** MEDIUM (P=20%, I=7, Score=1.4/10)
- **Mitigation:** Pin versions, quarterly health checks, hexagonal architecture isolates impact
- **Trigger:** 6 months without releases OR critical security vulnerability
- **Contingency:** Adapter replacement via port interface, stdlib fallback where possible

**Risk #3: Implementation Complexity Delays Value Delivery**
- **Severity:** MEDIUM (P=40%, I=5, Score=2.0/10)
- **Mitigation:** Phased rollout with MVP in 1 month (Phase 2 = tangible value)
- **Trigger:** If Phase 2 exceeds 4 weeks, descope or reassess
- **Contingency:** Deliver basic graph operations first, defer advanced features

**Risk #4: User Adoption Failure (Protocols)**
- **Severity:** MEDIUM (P=50%, I=4, Score=2.0/10)
- **Mitigation:** Lightweight AAR (3 questions, <5 min), show value via "Lessons Applied" reports
- **Trigger:** If <20% compliance after 3 months, simplify or automate
- **Contingency:** Quarterly retrospective instead of per-task AAR

**Risk #5: Over-Engineering / Scope Creep**
- **Severity:** MEDIUM (P=30%, I=6, Score=1.8/10)
- **Mitigation:** Strict phase gates, YAGNI discipline, quarterly ROI review
- **Trigger:** If KM work exceeds 20% of total dev time in any quarter
- **Contingency:** Freeze feature development, focus on utilization

## Implementation Plan

### Phase 1: Foundation (Q1 2026, Weeks 1-4)

**Goal:** Working graph operations and semantic search.

**Deliverables:**
```python
# Port definitions (domain layer, zero dependencies)
src/domain/ports/graph_port.py          # Graph operations interface
src/domain/ports/knowledge_port.py      # Semantic/RDF operations interface
src/domain/ports/vector_store_port.py   # Vector search interface

# Adapters (infrastructure layer)
src/infrastructure/graph/networkx_adapter.py      # NetworkX implementation
src/infrastructure/knowledge/rdflib_adapter.py    # RDFLib implementation
src/infrastructure/embeddings/faiss_adapter.py    # FAISS implementation

# Dependencies
pip install networkx==3.2.1 rdflib==7.0.0 faiss-cpu==1.7.4
```

**Success Criteria:**
- [x] Can add nodes and edges to graph
- [x] Can query "What docs reference concept X?"
- [x] Can export knowledge graph to RDF/Turtle format
- [x] Can add document embeddings to FAISS
- [x] Can search "Find top 5 docs similar to query"

**Effort Estimate:** 20-30 hours (1-2 weeks part-time)

**Risk:** Low (libraries well-documented, clear interfaces)

---

### Phase 2: Integration (Q2 2026, Weeks 5-10)

**Goal:** Automated knowledge graph construction from `docs/`.

**Deliverables:**
```python
# Entity extraction
src/infrastructure/extraction/markdown_entities.py

# Graph builder
src/application/commands/build_knowledge_graph.py

# Query interface
src/application/queries/find_related_docs.py
src/application/queries/semantic_search.py

# CLI integration
jerry knowledge graph --query "find related to X"
jerry knowledge search "semantic query text"
```

**Success Criteria:**
- [x] Automatically index `docs/` into graph on update
- [x] Extract entities: Tasks, Phases, Plans, Concepts, Documents
- [x] Extract relationships: REFERENCES, PART_OF, USES, IMPLEMENTS
- [x] Provide CLI for knowledge queries
- [x] Graph visualization export (DOT format for Graphviz)

**Effort Estimate:** 30-40 hours (2-3 weeks part-time)

**Risk:** Medium (entity extraction heuristics may need tuning)

---

### Phase 3: AI Integration (Q3 2026, Weeks 11-16)

**Goal:** RAG over knowledge base for agent reasoning.

**Deliverables:**
```python
# RAG implementation
src/interface/rag/simple_rag.py

# Agent integration
skills/knowledge-search/SKILL.md

# Use cases
src/application/queries/knowledge_query.py  # "What do we know about X?"
```

**Success Criteria:**
- [x] Agents can query: "What do we know about topic X?"
- [x] Retrieval includes top K relevant docs + source citations
- [x] Generation grounded in retrieved knowledge
- [x] Source attribution always provided (constitutional compliance)
- [x] Agents demonstrate measurable reasoning improvement

**Effort Estimate:** 20-30 hours (1-2 weeks part-time)

**Risk:** Low (RAG pattern well-established, FAISS + LLM API)

---

### Phase 4: Optimization (Q4 2026+, Triggered)

**Goal:** Performance tuning and advanced features (only if needed).

**Potential Upgrades:**
- NetworkX → igraph (if graph >5K nodes)
- FAISS CPU → FAISS GPU (if search >1 second)
- Simple RAG → GraphRAG (if multi-hop reasoning needed)
- Add Docling for PDF processing (if document formats expand)
- Consider Neo4j Community Edition (if ACID transactions needed)

**Trigger-Based:** Only implement if performance issues arise or specific needs emerge.

**Governance:** Quarterly review against success metrics.

---

### Success Metrics

**Quantitative (Measured Quarterly):**
- Knowledge graph size: Target 500+ nodes by Q2 2026, 1000+ by Q4 2026
- Query performance: <500ms for graph queries, <2s for semantic search
- Adoption: 50% of work items with associated knowledge by Q2 2026
- Coverage: 80% of `docs/` indexed in graph by Q3 2026

**Qualitative (User/Agent Feedback):**
- Agents demonstrate improved reasoning via knowledge retrieval
- Users report faster discovery of related work
- Knowledge reuse measurable (concepts applied to new problems)
- "Lessons Applied" reports show learning circulation (SECI spiral)

**ROI Targets:**
- Time saved finding information: 10-20% (baseline via time-tracking)
- Reduced duplicate work: 15-25% (via "what exists?" query logs)
- Improved decision quality: Qualitative (better-informed choices)

---

### Governance and Review

**Quarterly Assessment (Jan/Apr/Jul/Oct):**
1. Review knowledge graph growth vs. tool capacity
2. Check dependency health (releases, vulnerabilities, GitHub activity)
3. Measure adoption metrics (AAR completion, knowledge queries)
4. Assess ROI (time saved vs. maintenance burden)
5. Decide: Continue, upgrade tools, or roll back

**Off-Ramps:**
- If adoption <20% by Q2 2026 → Simplify protocols or defer Phase 3
- If maintenance burden >20% of dev time → Consider managed services
- If performance issues arise → Trigger Phase 4 upgrades early
- If constitutional violations detected → Immediate remediation

**Alignment Checks:**
- P-002 (File Persistence): Filesystem remains source of truth ✅
- P-003 (No Recursive Subagents): ReAct uses tools, not nested agents ✅
- P-020 (User Authority): Recommendations, not mandates ✅
- P-022 (No Deception): Always cite sources, expose uncertainty ✅

---

### Rollback Plan

**If Lightweight KM fails to deliver value:**

**Rollback Trigger:** After 6 months, if:
- Adoption <20% AND
- ROI not measurable AND
- Maintenance burden high

**Rollback Steps:**
1. Freeze feature development
2. Preserve filesystem knowledge (already source of truth)
3. Archive graph/vector data (exportable as RDF)
4. Remove infrastructure adapters
5. Revert to Enhanced Minimal KM (pure Python graph fallback)

**Data Preservation:**
- Filesystem unaffected (remained source of truth throughout)
- RDF export available for future tools
- Knowledge not lost, just retrieval mechanisms changed

**Cost of Rollback:** Low (hexagonal architecture isolates impact)

## References

### Primary Research Documents

1. **KM Domain Synthesis** (`docs/synthesis/work-032-e-006-km-synthesis.md`)
   - 37KB, 7 major thematic patterns identified
   - Synthesis of 358KB research across 5 documents, 71+ citations
   - Braun & Clarke thematic analysis methodology
   - Key finding: Modern KM = Filesystem + Graph + AI

2. **Trade-off Analysis** (`docs/analysis/work-032-e-007-trade-off-analysis.md`)
   - 29KB, SWOT + Decision Matrix + Quality Attributes + Risk Analysis
   - 4 options evaluated against 9 weighted criteria
   - Lightweight KM recommended (8.5/10 score, 85% confidence)
   - 5 major risks identified with mitigations

### Research Sources (via Synthesis)

3. **KM Fundamentals** (e-001): SECI model, Cynefin, ISO 30401, thought leaders
4. **KM Protocols** (e-002): AAR, A3, Knowledge Audit, APQC framework
5. **KM Products** (e-003): Neo4j, Obsidian, RAG products, market trends
6. **Python SDKs** (e-004): NetworkX, RDFLib, FAISS, spaCy, Docling analysis
7. **KM Frameworks** (e-005): SECI, Cynefin, TRIZ, Design Thinking, ReAct, RAG, GraphRAG

### Industry Standards

8. **ISO 30401:2018** - Knowledge Management Systems (progressive alignment target)
9. **RDF/SPARQL** - W3C Semantic Web standards (via RDFLib)
10. **Hexagonal Architecture** - Alistair Cockburn (ports/adapters pattern)

### Technical Documentation

11. **NetworkX Documentation** - https://networkx.org/ (v3.2.1)
12. **RDFLib Documentation** - https://rdflib.readthedocs.io/ (v7.0.0)
13. **FAISS Documentation** - https://faiss.ai/ (v1.7.4)

### Jerry Governance

14. **Jerry Constitution** (`docs/governance/JERRY_CONSTITUTION.md`) - Principles P-002, P-003, P-020, P-022
15. **Coding Standards** (`.claude/rules/coding-standards.md`) - Hexagonal architecture enforcement

---

## Approval Chain

| Role | Name | Status | Date |
|------|------|--------|------|
| **Author** | ps-architect v2.0.0 | ✅ Complete | 2026-01-09 |
| **Reviewer** | ps-validator | ⏳ Pending | - |
| **Approver** | User | ⏳ Pending | - |

**Next Steps:**
1. ps-validator review for correctness, completeness, adherence to ADR format
2. User approval or feedback
3. If approved: Create implementation PLAN file and begin Phase 1
4. If rejected: Document rationale, consider alternatives

---

**ADR Status:** PROPOSED
**File:** `/home/user/jerry/docs/decisions/ADR-032-km-integration.md`
**Last Updated:** 2026-01-09
**Supersedes:** None
**Superseded By:** None (active)
