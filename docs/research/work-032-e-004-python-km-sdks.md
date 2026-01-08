# Python Knowledge Management SDKs and Libraries

> **Research ID:** WORK-032-E-004
> **Research Date:** 2026-01-08
> **Researcher:** ps-researcher agent (v2.0.0)
> **Status:** DECISION-GRADE
> **Purpose:** Research Python libraries for Knowledge Management implementation

---

## Context

This research supports the Knowledge Architecture initiative (WORK-032) by cataloging Python libraries across six critical categories for Knowledge Management:

1. Graph Libraries (data structures & algorithms)
2. RDF/Semantic Web (standards-based KGs)
3. Knowledge Graph Construction (NLP-driven extraction)
4. Vector/Embedding Storage (semantic search)
5. Ontology/Taxonomy (formal knowledge representation)
6. Document Processing (knowledge extraction)

This document provides:
- Comprehensive library catalog with PyPI/GitHub links
- Capability analysis for each library
- Jerry compatibility assessment (stdlib preference, dependency analysis)
- Code examples and usage patterns
- Architecture fit for hexagonal design and zero-dependency core

---

## L0: Executive Summary (Plain Language)

### Key Findings

#### 1. **No Pure Stdlib Solution Exists**

The Python standard library alone cannot support modern Knowledge Management requirements. All serious KM implementations require external dependencies. This is a fundamental architectural reality, not a gap we can fill.

**Why**: Knowledge Management requires:
- Graph algorithms (no stdlib implementation)
- Semantic web standards (RDF, OWL, SPARQL)
- Neural embeddings (deep learning models)
- High-performance vector search (C++/Rust backends)
- NLP pipelines (trained models, tokenizers)

#### 2. **Three-Tier Dependency Strategy**

Libraries naturally fall into three tiers by dependency weight:

**Tier 1: Lightweight (Acceptable for Infrastructure Layer)**
- NetworkX (pure Python, minimal deps: only decorator libs)
- RDFLib (pure Python, stdlib + XML/parsing)
- Small, well-scoped tools with minimal transitive dependencies

**Tier 2: Moderate (Infrastructure Layer with Caution)**
- FAISS (C++ core, Python bindings, no deep learning framework required)
- Owlready2 (Python + SQLite, self-contained)
- spaCy (modular, use only needed pipelines)

**Tier 3: Heavy (Interface Layer Only)**
- PyTorch Geometric, DGL (full deep learning stacks)
- ChromaDB, Weaviate, Qdrant (full database systems)
- LangChain, LlamaIndex (large framework ecosystems)

#### 3. **Graph Library Landscape**

| Library | Best For | Performance | Jerry Fit |
|---------|----------|-------------|-----------|
| **NetworkX** | Prototyping, small graphs (<10K nodes) | Slow (pure Python) | ✓ Infrastructure |
| **igraph** | Medium graphs, balance speed/usability | Fast (C core) | ✓ Infrastructure |
| **graph-tool** | Large-scale analytics, parallel processing | Fastest (C++) | ⚠ Complex install |
| **PyTorch Geometric** | GNN research, GPU-accelerated | High (GPU) | ✗ Interface only |
| **DGL** | Production GNNs, multi-framework | High (GPU) | ✗ Interface only |

**Recommendation**: Start with **NetworkX** in infrastructure layer (hexagonal ports). Swap to igraph/graph-tool if performance demands it. Keep GNN libraries (PyG, DGL) in interface layer only.

#### 4. **Semantic Web: RDFLib is the Foundation**

For standards-based knowledge graphs (RDF, OWL, SPARQL), **RDFLib** is the de facto Python standard:
- Pure Python (good Jerry fit)
- 14M+ weekly downloads (ecosystem standard)
- Supports all major RDF serializations (Turtle, JSON-LD, RDF/XML)
- Integrates with Owlready2 for OWL ontologies

**Alternative**: pyoxigraph (Rust-based, faster, but heavier dependency)

#### 5. **Vector Search: FAISS for Embeddings, ChromaDB for RAG**

**FAISS** (Facebook AI Similarity Search):
- Industry standard for vector similarity search
- C++ core with Python bindings
- No deep learning framework required (just NumPy)
- Handles billions of vectors
- **Best fit for Jerry infrastructure layer**

**ChromaDB**:
- Open-source embedding database
- Built for LLM/RAG workflows
- 6K+ GitHub stars, rapid adoption
- Good for prototyping, smaller scale
- **Use in interface layer for LLM integration**

**Pinecone, Weaviate, Qdrant**: Production vector databases, but require external services (not Jerry-compatible for core).

#### 6. **Knowledge Graph Construction: spaCy + Transformers**

**spaCy**:
- Industrial-strength NLP (NER, dependency parsing)
- Modular pipeline design (load only what you need)
- Can extract entities and relationships without LLMs
- **Acceptable for infrastructure layer** with careful pipeline selection

**Hugging Face Transformers**:
- State-of-the-art NLP models (REBEL for relation extraction)
- Large dependency footprint (PyTorch/TensorFlow)
- **Use in interface layer** or separate extraction service

**LangChain/LlamaIndex**:
- High-level RAG frameworks
- Heavy dependencies, rapid API changes
- **Interface layer only**, prefer thin adapters

#### 7. **Document Processing: Docling (IBM) Leading the Pack**

**Docling** (2025-2026 leader):
- IBM's open-source framework (LF AI & Data Foundation project)
- Handles PDF, DOCX, PPTX, HTML, images
- Unified DoclingDocument format
- Export to Markdown, HTML, JSON
- **Best choice for production document processing**

**Marker-PDF**:
- Fast PDF → Markdown conversion
- Excellent layout preservation
- Heavy first-run (1GB model download)
- **Use for PDF-specific workflows**

**Unstructured**:
- Multi-format support (PDF, HTML, Word, images)
- Good for RAG systems (semantic chunking)
- **Use for diverse document types**

### Top Recommendations for Jerry

#### Immediate Actions (WORK-032 Implementation)

1. **Adopt NetworkX for Core Graph Operations**
   - Pure Python, minimal dependencies
   - Place in `src/infrastructure/graph/networkx_adapter.py`
   - Define port in `src/domain/ports/graph_port.py`
   - Easy to swap for igraph/graph-tool if needed

2. **Use RDFLib for Semantic Knowledge Graphs**
   - Place in `src/infrastructure/knowledge/rdflib_adapter.py`
   - Supports future ontology integration
   - Standards-compliant (interoperable)

3. **Integrate FAISS for Vector Search**
   - Lightweight enough for infrastructure layer
   - Place in `src/infrastructure/embeddings/faiss_adapter.py`
   - No framework lock-in (just NumPy arrays)

4. **Document Processing: Start with Docling**
   - Place in `src/infrastructure/documents/docling_adapter.py`
   - Unified interface for multiple formats
   - Export to structured formats (JSON, Markdown)

5. **NLP: Careful spaCy Integration**
   - Use minimal pipeline (`en_core_web_sm` for prototyping)
   - Place in `src/infrastructure/nlp/spacy_adapter.py`
   - Consider separate extraction service if models grow large

#### Architectural Strategy

**Hexagonal Ports Pattern:**

```python
# Domain Layer (src/domain/ports/)
class GraphPort(ABC):
    """Port for graph operations (dependency-free)."""
    @abstractmethod
    def add_node(self, node_id: str, properties: dict) -> None: ...

    @abstractmethod
    def add_edge(self, source: str, target: str, edge_type: str) -> None: ...

    @abstractmethod
    def traverse(self, start: str, pattern: TraversalPattern) -> List[Node]: ...

# Infrastructure Layer (src/infrastructure/graph/)
class NetworkXAdapter(GraphPort):
    """NetworkX implementation of graph port."""
    def __init__(self):
        import networkx as nx  # Import isolated to adapter
        self._graph = nx.MultiDiGraph()

    def add_node(self, node_id: str, properties: dict) -> None:
        self._graph.add_node(node_id, **properties)
    # ... implement other methods
```

**Dependency Isolation:**
- Domain layer: Zero external dependencies
- Infrastructure layer: Lightweight dependencies (NetworkX, RDFLib, FAISS)
- Interface layer: Heavy frameworks (LangChain, ChromaDB, transformers)

**Migration Path:**
- Start: NetworkX (prototyping)
- Scale: igraph (performance)
- Advanced: graph-tool (large-scale analytics)
- Swap adapters, domain layer unchanged

---

## L1: Library Catalog with Code Examples

### 1. Graph Libraries

#### 1.1 NetworkX

**PyPI Package**: `networkx`
**GitHub**: https://github.com/networkx/networkx (16,295 stars)
**Current Version**: 3.6.1 (January 2026)
**Weekly Downloads**: 14.9M
**Maintenance**: Sustainable (active development)

**Key Capabilities:**
- Pure Python implementation (easy install, no compilation)
- Directed, undirected, and multigraphs
- 100+ graph algorithms (shortest path, centrality, clustering)
- Graph generators (random, classic, social networks)
- Drawing/visualization integration (matplotlib, graphviz)

**Jerry Compatibility**: ✓ **Excellent**
- Pure Python (no C dependencies)
- Minimal dependencies (only decorator libs)
- Stdlib-friendly design
- Easy to isolate in adapter

**Performance Characteristics:**
- Small graphs (<10K nodes): Acceptable
- Medium graphs (10K-100K nodes): Slow
- Large graphs (>100K nodes): Not recommended
- 40-250x slower than graph-tool for complex algorithms

**Example Usage:**

```python
import networkx as nx

# Create directed graph
G = nx.DiGraph()

# Add nodes with properties
G.add_node("task-001", type="task", status="active", title="Implement KG")
G.add_node("phase-001", type="phase", name="Development")
G.add_node("plan-001", type="plan", name="WORK-032")

# Add edges with properties
G.add_edge("task-001", "phase-001", edge_type="BELONGS_TO", created_at="2026-01-08")
G.add_edge("phase-001", "plan-001", edge_type="PART_OF")

# Query by property
tasks = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'task']

# Traverse relationships
phase = list(G.successors("task-001"))[0]
print(f"Task belongs to: {G.nodes[phase]['name']}")

# Find all tasks in a plan
tasks_in_plan = []
for phase in G.successors("plan-001"):
    for task in G.predecessors(phase):
        if G.nodes[task]['type'] == 'task':
            tasks_in_plan.append(task)

# Export to various formats
nx.write_graphml(G, "knowledge_graph.graphml")
nx.write_gexf(G, "knowledge_graph.gexf")

# Algorithms
# Shortest path
path = nx.shortest_path(G, "task-001", "plan-001")

# PageRank (for importance scoring)
ranks = nx.pagerank(G)
important_nodes = sorted(ranks.items(), key=lambda x: x[1], reverse=True)[:5]

# Community detection
communities = nx.community.greedy_modularity_communities(G.to_undirected())
```

**Jerry Adapter Pattern:**

```python
# src/infrastructure/graph/networkx_adapter.py
from typing import List, Dict, Any, Optional
import networkx as nx

from src.domain.ports.graph_port import GraphPort, Node, Edge, TraversalPattern

class NetworkXGraphAdapter(GraphPort):
    """NetworkX implementation of graph storage."""

    def __init__(self):
        self._graph = nx.MultiDiGraph()

    def add_node(self, node_id: str, label: str, properties: Dict[str, Any]) -> None:
        """Add a node to the graph."""
        self._graph.add_node(node_id, label=label, **properties)

    def add_edge(
        self,
        source: str,
        target: str,
        edge_type: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add an edge to the graph."""
        props = properties or {}
        self._graph.add_edge(source, target, key=edge_type, edge_type=edge_type, **props)

    def get_node(self, node_id: str) -> Optional[Node]:
        """Retrieve a node by ID."""
        if not self._graph.has_node(node_id):
            return None
        attrs = self._graph.nodes[node_id]
        return Node(
            id=node_id,
            label=attrs.get('label', 'unknown'),
            properties=dict(attrs)
        )

    def traverse_out(self, node_id: str, edge_type: Optional[str] = None) -> List[Node]:
        """Traverse outgoing edges from a node."""
        if not self._graph.has_node(node_id):
            return []

        result = []
        for successor in self._graph.successors(node_id):
            # Filter by edge type if specified
            if edge_type:
                edge_data = self._graph.get_edge_data(node_id, successor)
                if not any(data.get('edge_type') == edge_type for data in edge_data.values()):
                    continue

            node = self.get_node(successor)
            if node:
                result.append(node)

        return result

    def query(self, pattern: TraversalPattern) -> List[Node]:
        """Execute a traversal pattern query."""
        # Pattern matching implementation
        # This is where Gremlin-like queries would be translated
        # For now, simplified implementation
        nodes = []
        for node_id, attrs in self._graph.nodes(data=True):
            if attrs.get('label') == pattern.start_label:
                nodes.append(Node(id=node_id, label=pattern.start_label, properties=dict(attrs)))
        return nodes

    def export_to_dict(self) -> Dict[str, Any]:
        """Export graph to dictionary format."""
        return nx.node_link_data(self._graph)

    def import_from_dict(self, data: Dict[str, Any]) -> None:
        """Import graph from dictionary format."""
        self._graph = nx.node_link_graph(data, multigraph=True, directed=True)
```

**Citations:**
- [NetworkX GitHub Repository](https://github.com/networkx/networkx)
- [NetworkX PyPI Package](https://pypi.org/project/networkx/)
- [NetworkX Documentation](https://networkx.org/documentation/stable/)

---

#### 1.2 igraph

**PyPI Package**: `python-igraph`
**GitHub**: https://github.com/igraph/python-igraph (~3K stars, part of igraph org)
**Current Version**: 0.11.x
**Core**: C/C++ library with Python bindings

**Key Capabilities:**
- High-performance graph algorithms (C/C++ core)
- 8x faster than NetworkX for betweenness centrality
- Support for large graphs (millions of nodes)
- Efficient memory usage
- Cross-platform (R, Python, Mathematica, C/C++)

**Jerry Compatibility**: ✓ **Good**
- Pre-compiled wheels for most platforms
- Smaller dependency footprint than graph-tool
- C extension but well-packaged

**Performance Characteristics:**
- Small graphs: Overkill but works
- Medium graphs (10K-1M nodes): Excellent
- Large graphs (>1M nodes): Very good
- ~8-10x faster than NetworkX

**Example Usage:**

```python
from igraph import Graph

# Create directed graph
g = Graph(directed=True)

# Add vertices with attributes
g.add_vertices(3)
g.vs[0]['name'] = 'task-001'
g.vs[0]['type'] = 'task'
g.vs[1]['name'] = 'phase-001'
g.vs[1]['type'] = 'phase'
g.vs[2]['name'] = 'plan-001'
g.vs[2]['type'] = 'plan'

# Add edges
g.add_edge(0, 1, edge_type='BELONGS_TO')
g.add_edge(1, 2, edge_type='PART_OF')

# Query by attribute
tasks = g.vs.select(type='task')

# Traverse
neighbors = g.neighbors(0, mode='out')

# Algorithms (fast!)
pagerank = g.pagerank(directed=True)
betweenness = g.betweenness(directed=True)

# Community detection
communities = g.community_multilevel()

# Export
g.write_graphml('graph.graphml')
```

**When to Use igraph Over NetworkX:**
- Graph has >10K nodes
- Performance-critical traversals
- Need community detection on large graphs
- Running centrality algorithms repeatedly

**Citations:**
- [igraph Python Package](https://pypi.org/project/python-igraph/)
- [igraph Documentation](https://igraph.org/python/)

---

#### 1.3 graph-tool

**PyPI Package**: `graph-tool` (complex installation, usually via conda)
**Website**: https://graph-tool.skewed.de/
**GitHub**: Part of graph-tool project
**Core**: C++ with Boost Graph Library

**Key Capabilities:**
- Fastest Python graph library (C++ + Boost)
- Parallel processing with OpenMP
- Advanced algorithms (stochastic block models, graph drawing)
- Statistical graph analysis
- Graph filtering without copying

**Jerry Compatibility**: ⚠ **Challenging**
- Complex installation (C++ compilation, Boost dependency)
- Best installed via conda, not pip
- Heavy dependencies
- Not suitable for lightweight deployments

**Performance Characteristics:**
- Fastest of all Python graph libraries
- 40-250x faster than NetworkX
- OpenMP parallel algorithms (PageRank, betweenness)
- Handles billion-node graphs

**When to Use:**
- Large-scale graph analytics (>1M nodes)
- Need maximum performance
- Have controlled deployment environment (conda)
- Running statistical inference on graphs

**Example Usage:**

```python
from graph_tool.all import Graph, graph_draw
import graph_tool.centrality as centrality

# Create graph
g = Graph(directed=True)

# Add vertices
v1 = g.add_vertex()
v2 = g.add_vertex()
v3 = g.add_vertex()

# Properties
vprop_name = g.new_vertex_property("string")
vprop_type = g.new_vertex_property("string")
g.vertex_properties["name"] = vprop_name
g.vertex_properties["type"] = vprop_type

vprop_name[v1] = "task-001"
vprop_type[v1] = "task"

# Add edges
e1 = g.add_edge(v1, v2)
eprop = g.new_edge_property("string")
g.edge_properties["edge_type"] = eprop
eprop[e1] = "BELONGS_TO"

# Fast algorithms
pr = centrality.pagerank(g)
betw = centrality.betweenness(g)

# Visualization
graph_draw(g, vertex_text=vprop_name, output="graph.png")
```

**Jerry Recommendation**: Use only if performance demands it. Start with NetworkX/igraph.

**Citations:**
- [graph-tool Performance Benchmarks](https://graph-tool.skewed.de/performance.html)
- [graph-tool Documentation](https://graph-tool.skewed.de/)

---

#### 1.4 PyTorch Geometric (PyG)

**PyPI Package**: `torch-geometric`
**GitHub**: https://github.com/pyg-team/pytorch_geometric (~20K stars)
**Current Version**: 2.x
**Core**: PyTorch-based Graph Neural Networks

**Key Capabilities:**
- State-of-the-art GNN implementations (GCN, GAT, GraphSAGE)
- GPU-accelerated graph learning
- Message-passing neural networks
- Integration with PyTorch ecosystem
- Large model zoo (100+ implementations)

**Jerry Compatibility**: ✗ **Interface Layer Only**
- Requires full PyTorch stack
- GPU recommended for performance
- Large dependency footprint
- Use only in interface/application layer

**Performance Characteristics:**
- CPU: Slower than traditional graph libraries
- GPU: Excellent for deep learning on graphs
- Best for: Node classification, link prediction, graph classification

**Example Usage:**

```python
import torch
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
import torch.nn.functional as F

# Create graph data
edge_index = torch.tensor([[0, 1, 1, 2],
                           [1, 0, 2, 1]], dtype=torch.long)
x = torch.tensor([[-1], [0], [1]], dtype=torch.float)

data = Data(x=x, edge_index=edge_index)

# Define GNN model
class GCN(torch.nn.Module):
    def __init__(self, num_features, hidden_channels):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(num_features, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        return x

# Train model
model = GCN(num_features=1, hidden_channels=16)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Use for node embeddings
model.eval()
with torch.no_grad():
    embeddings = model(data.x, data.edge_index)
```

**When to Use in Jerry:**
- Need graph embeddings for similarity search
- Building knowledge graph completion models
- Link prediction for suggesting relationships
- **Always isolate in interface layer**

**Citations:**
- [PyTorch Geometric GitHub](https://github.com/pyg-team/pytorch_geometric)
- [PyG vs DGL Comparison](https://www.exxactcorp.com/blog/Deep-Learning/pytorch-geometric-vs-deep-graph-library)

---

#### 1.5 Deep Graph Library (DGL)

**PyPI Package**: `dgl`
**GitHub**: https://github.com/dmlc/dgl (~13K stars)
**Current Version**: 2.x
**Core**: Multi-framework GNN library (PyTorch, TensorFlow, MXNet)

**Key Capabilities:**
- Framework-agnostic (PyTorch/TensorFlow/MXNet backends)
- Lower-level API (more flexible than PyG)
- Support for heterogeneous graphs
- Tree-LSTM and other non-message-passing models
- Used in AlphaFold (SE3-Transformer), RosettaFold

**Jerry Compatibility**: ✗ **Interface Layer Only**
- Requires deep learning framework
- Heavy dependencies
- Production-oriented (good for deployment)

**Example Usage:**

```python
import dgl
import torch

# Create graph
src = torch.tensor([0, 1, 1, 2])
dst = torch.tensor([1, 0, 2, 1])
g = dgl.graph((src, dst))

# Add node features
g.ndata['feat'] = torch.randn(3, 5)

# Add edge features
g.edata['weight'] = torch.randn(4, 1)

# Heterogeneous graph (knowledge graph)
graph_data = {
    ('task', 'belongs_to', 'phase'): (torch.tensor([0, 1]), torch.tensor([0, 0])),
    ('phase', 'part_of', 'plan'): (torch.tensor([0]), torch.tensor([0]))
}
hetero_g = dgl.heterograph(graph_data)

# Message passing
import dgl.function as fn

g.update_all(fn.copy_u('feat', 'm'), fn.mean('m', 'feat_agg'))
```

**When to Use Over PyG:**
- Need multi-framework support
- Building complex, non-standard GNN architectures
- Production deployment with specific framework requirements

**Citations:**
- [DGL GitHub Repository](https://github.com/dmlc/dgl)
- [DGL Documentation](https://docs.dgl.ai/)

---

### 2. RDF/Semantic Web Libraries

#### 2.1 RDFLib

**PyPI Package**: `rdflib`
**GitHub**: https://github.com/RDFLib/rdflib (~2K stars, but de facto standard)
**Current Version**: 7.x (January 2026)
**Weekly Downloads**: 14M+

**Key Capabilities:**
- Pure Python RDF library
- Support for RDF, RDFS, OWL
- Parsers/serializers: RDF/XML, Turtle, N-Triples, JSON-LD, N3
- SPARQL 1.1 query and update
- Triple/quad store with multiple backends
- Graph operations (union, intersection, difference)

**Jerry Compatibility**: ✓ **Excellent**
- Pure Python
- Minimal dependencies (stdlib + XML/parsing libs)
- Industry standard (interoperability)
- Easy to isolate in adapter

**Performance Characteristics:**
- Small graphs (<100K triples): Good
- Medium graphs (100K-1M triples): Acceptable
- Large graphs (>1M triples): Consider triplestore backend

**Example Usage:**

```python
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL

# Create graph
g = Graph()

# Define namespace
JERRY = Namespace("http://jerry.ai/ontology/")
g.bind("jerry", JERRY)

# Add triples (subject, predicate, object)
task_001 = JERRY.Task_001
g.add((task_001, RDF.type, JERRY.Task))
g.add((task_001, JERRY.title, Literal("Implement Knowledge Graph")))
g.add((task_001, JERRY.status, Literal("active")))
g.add((task_001, JERRY.belongsTo, JERRY.Phase_001))

phase_001 = JERRY.Phase_001
g.add((phase_001, RDF.type, JERRY.Phase))
g.add((phase_001, JERRY.name, Literal("Development")))
g.add((phase_001, JERRY.partOf, JERRY.Plan_WORK032))

# SPARQL query
query = """
    PREFIX jerry: <http://jerry.ai/ontology/>

    SELECT ?task ?title ?phase
    WHERE {
        ?task a jerry:Task ;
              jerry:title ?title ;
              jerry:belongsTo ?phase .
        ?phase jerry:partOf jerry:Plan_WORK032 .
    }
"""
results = g.query(query)
for row in results:
    print(f"Task: {row.task}, Title: {row.title}, Phase: {row.phase}")

# Serialize to Turtle (human-readable)
print(g.serialize(format='turtle'))

# Serialize to JSON-LD (LLM-friendly)
print(g.serialize(format='json-ld'))

# Load from file
g.parse("knowledge_graph.ttl", format="turtle")

# Reasoning (simple)
# Add transitivity rule
for s, o in g.subject_objects(JERRY.partOf):
    for s2 in g.subjects(JERRY.belongsTo, s):
        g.add((s2, JERRY.indirectPartOf, o))

# Export to triple store
g.serialize(destination='knowledge_graph.nt', format='nt')
```

**Jerry Adapter Pattern:**

```python
# src/infrastructure/knowledge/rdflib_adapter.py
from typing import List, Dict, Any, Optional
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS

from src.domain.ports.knowledge_port import KnowledgePort, Triple

class RDFLibAdapter(KnowledgePort):
    """RDFLib implementation of knowledge graph storage."""

    def __init__(self, base_uri: str = "http://jerry.ai/ontology/"):
        self._graph = Graph()
        self._namespace = Namespace(base_uri)
        self._graph.bind("jerry", self._namespace)

    def add_triple(self, subject: str, predicate: str, obj: str) -> None:
        """Add a triple to the knowledge graph."""
        s = self._namespace[subject]
        p = self._namespace[predicate]
        o = self._namespace[obj] if not self._is_literal(obj) else Literal(obj)
        self._graph.add((s, p, o))

    def query_sparql(self, query: str) -> List[Dict[str, Any]]:
        """Execute a SPARQL query."""
        results = self._graph.query(query)
        return [dict(row.asdict()) for row in results]

    def export_turtle(self) -> str:
        """Export graph to Turtle format."""
        return self._graph.serialize(format='turtle')

    def export_jsonld(self) -> str:
        """Export graph to JSON-LD format."""
        return self._graph.serialize(format='json-ld')

    def import_turtle(self, data: str) -> None:
        """Import graph from Turtle format."""
        self._graph.parse(data=data, format='turtle')

    def _is_literal(self, value: str) -> bool:
        """Check if value should be a literal."""
        # Simple heuristic: if it doesn't look like an identifier, it's a literal
        return ' ' in value or not value.replace('_', '').replace('-', '').isalnum()
```

**Citations:**
- [RDFLib GitHub Repository](https://github.com/RDFLib/rdflib)
- [RDFLib PyPI Package](https://pypi.org/project/rdflib/)
- [RDFLib Documentation](https://rdflib.readthedocs.io/)

---

#### 2.2 Owlready2

**PyPI Package**: `owlready2`
**GitHub**: https://github.com/pwin/owlready2 (~250 stars)
**Current Version**: 0.49
**Maintenance**: Active

**Key Capabilities:**
- Ontology-oriented programming (load OWL as Python objects)
- Support for OWL 2.0, SWRL
- Reasoning via HermiT (included)
- Optimized quadstore (SQLite3-based)
- Can handle large ontologies
- SPARQL query support (via RDFLib integration)
- ORM-like interface for ontologies

**Jerry Compatibility**: ✓ **Good**
- Pure Python core
- SQLite backend (stdlib)
- Self-contained reasoner
- Moderate dependencies

**Performance Characteristics:**
- Optimized for large ontologies
- Faster reasoning than pure RDFLib
- Quadstore better for versioning/context

**Example Usage:**

```python
from owlready2 import *

# Create ontology
onto = get_ontology("http://jerry.ai/ontology/work_tracker.owl")

# Define classes
with onto:
    class Task(Thing):
        pass

    class Phase(Thing):
        pass

    class Plan(Thing):
        pass

    # Define properties
    class belongsTo(ObjectProperty):
        domain = [Task]
        range = [Phase]

    class partOf(ObjectProperty):
        domain = [Phase]
        range = [Plan]

    class hasTitle(DataProperty):
        domain = [Task]
        range = [str]

    class hasStatus(DataProperty):
        domain = [Task]
        range = [str]

# Create instances
task_001 = Task("task_001")
task_001.hasTitle = ["Implement Knowledge Graph"]
task_001.hasStatus = ["active"]

phase_001 = Phase("phase_001")
task_001.belongsTo = [phase_001]

plan_001 = Plan("plan_WORK032")
phase_001.partOf = [plan_001]

# Reasoning
with onto:
    # Define transitive property
    class indirectPartOf(ObjectProperty, TransitiveProperty):
        pass

    # Add rule: if A belongsTo B and B partOf C, then A indirectPartOf C
    # (This would be done via SWRL or reasoning)

# Run reasoner
sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)

# Query
tasks_in_plan = []
for task in Task.instances():
    for phase in task.belongsTo:
        for plan in phase.partOf:
            if plan == plan_001:
                tasks_in_plan.append(task)

# Save ontology
onto.save(file="work_tracker.owl", format="rdfxml")

# SPARQL via RDFLib integration
graph = default_world.as_rdflib_graph()
results = graph.query("""
    SELECT ?task ?title
    WHERE {
        ?task a <http://jerry.ai/ontology/work_tracker.owl#Task> ;
              <http://jerry.ai/ontology/work_tracker.owl#hasTitle> ?title .
    }
""")
```

**When to Use Over RDFLib:**
- Need formal reasoning (OWL inference)
- Working with complex ontologies
- Want object-oriented interface to RDF
- Need to define SWRL rules

**Known Limitations:**
- Does not support OWL Functional Syntax
- Does not support punned entities
- RDF/XML, OWL/XML, NTriples only (no Turtle parser)

**Citations:**
- [Owlready2 PyPI Package](https://pypi.org/project/owlready2/)
- [Owlready2 Documentation](https://owlready2.readthedocs.io/)

---

#### 2.3 kglab

**PyPI Package**: `kglab`
**GitHub**: https://github.com/DerwenAI/kglab (~500 stars)
**License**: MIT
**Maintenance**: Active (2020-2025)

**Key Capabilities:**
- Abstraction layer over RDFLib, NetworkX, PyVis, morph-kgc
- Integrates multiple KG tools under one API
- Support for Pandas DataFrames ↔ RDF conversion
- Visualization with PyVis
- Inference with OWL-RL and skosify
- Probabilistic Soft Logic (PSL) integration
- Good Jupyter notebook support

**Jerry Compatibility**: ⚠ **Mixed**
- Useful as high-level interface
- Heavy dependencies (pulls in many libraries)
- Better for exploration than production
- Consider cherry-picking patterns, not full dependency

**Example Usage:**

```python
import kglab

# Create knowledge graph
kg = kglab.KnowledgeGraph()

# Load from Turtle
kg.load_rdf("knowledge_graph.ttl", format="ttl")

# Query with SPARQL
sparql = """
    SELECT ?subject ?predicate ?object
    WHERE {
        ?subject ?predicate ?object .
    }
    LIMIT 10
"""
df = kg.query_as_df(sparql)  # Returns Pandas DataFrame

# Add triples from Pandas
import pandas as pd
df = pd.DataFrame({
    'subject': ['task:001', 'task:002'],
    'predicate': ['rdf:type', 'rdf:type'],
    'object': ['jerry:Task', 'jerry:Task']
})
# (Would need custom conversion)

# Visualization
kg.visualize()

# Inference with OWL-RL
kg.infer_owlrl()

# Export
kg.save_rdf("output.ttl", format="ttl")
```

**Jerry Recommendation**: Use for prototyping/exploration, but prefer direct RDFLib for production.

**Citations:**
- [kglab GitHub Repository](https://github.com/DerwenAI/kglab)
- [kglab PyPI Package](https://pypi.org/project/kglab/)

---

### 3. Knowledge Graph Construction (NLP)

#### 3.1 spaCy

**PyPI Package**: `spacy`
**GitHub**: https://github.com/explosion/spacy (~29K stars)
**Current Version**: 3.x
**Maintenance**: Active (Explosion AI)

**Key Capabilities:**
- Industrial-strength NLP pipeline
- Named Entity Recognition (NER)
- Dependency parsing (syntax trees)
- Part-of-speech tagging
- Sentence segmentation
- Custom pipeline components
- Modular design (load only needed components)
- Pre-trained models for 60+ languages
- Fast (Cython core)

**Jerry Compatibility**: ✓ **Acceptable with Caution**
- Core is well-optimized
- Models are large (100MB - 500MB)
- Can use small models (`en_core_web_sm`: ~12MB)
- Modular loading (only load needed pipes)
- **Recommendation**: Place in infrastructure layer, use smallest models

**Performance Characteristics:**
- Fast NER and parsing (Cython core)
- Small model: ~100K words/sec
- Large model: ~50K words/sec
- GPU support available

**Example Usage for Knowledge Graph Construction:**

```python
import spacy

# Load model (use smallest for Jerry)
nlp = spacy.load("en_core_web_sm")

# Process text
text = """
Jerry is a framework for behavior and workflow guardrails.
It uses NetworkX for graph operations and RDFLib for semantic knowledge.
The Work Tracker manages tasks, phases, and plans.
"""

doc = nlp(text)

# Extract entities
entities = []
for ent in doc.ents:
    entities.append({
        'text': ent.text,
        'label': ent.label_,
        'start': ent.start_char,
        'end': ent.end_char
    })
print("Entities:", entities)

# Extract relationships via dependency parsing
triples = []
for sent in doc.sents:
    for token in sent:
        if token.dep_ in ('nsubj', 'nsubjpass'):
            subject = token.text
            predicate = token.head.text

            # Find object
            for child in token.head.children:
                if child.dep_ in ('dobj', 'pobj', 'attr'):
                    obj = child.text
                    triples.append((subject, predicate, obj))

print("Triples:", triples)

# Advanced: Use custom patterns for relation extraction
from spacy.matcher import Matcher

matcher = Matcher(nlp.vocab)

# Pattern: ENTITY uses ENTITY
pattern = [
    {"ENT_TYPE": {"IN": ["ORG", "PRODUCT"]}},
    {"LOWER": "uses"},
    {"ENT_TYPE": {"IN": ["ORG", "PRODUCT"]}}
]
matcher.add("USES_RELATION", [pattern])

matches = matcher(doc)
for match_id, start, end in matches:
    span = doc[start:end]
    print(f"Relation found: {span.text}")

# Build knowledge graph from entities
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF

g = Graph()
JERRY = Namespace("http://jerry.ai/kg/")

for ent in doc.ents:
    entity_uri = JERRY[ent.text.replace(' ', '_')]
    g.add((entity_uri, RDF.type, JERRY[ent.label_]))
    g.add((entity_uri, JERRY.text, Literal(ent.text)))

for subj, pred, obj in triples:
    s_uri = JERRY[subj.replace(' ', '_')]
    p_uri = JERRY[pred.replace(' ', '_')]
    o_uri = JERRY[obj.replace(' ', '_')]
    g.add((s_uri, p_uri, o_uri))

print(g.serialize(format='turtle'))
```

**Jerry Adapter Pattern:**

```python
# src/infrastructure/nlp/spacy_adapter.py
from typing import List, Dict, Any, Tuple
import spacy

from src.domain.ports.nlp_port import NLPPort, Entity, Relation

class SpacyNLPAdapter(NLPPort):
    """spaCy implementation of NLP operations."""

    def __init__(self, model: str = "en_core_web_sm"):
        """Initialize with specified model."""
        # Lazy load to keep adapter lightweight
        self._model_name = model
        self._nlp = None

    def _ensure_loaded(self):
        """Lazy load model on first use."""
        if self._nlp is None:
            self._nlp = spacy.load(self._model_name)

    def extract_entities(self, text: str) -> List[Entity]:
        """Extract named entities from text."""
        self._ensure_loaded()
        doc = self._nlp(text)

        return [
            Entity(
                text=ent.text,
                label=ent.label_,
                start=ent.start_char,
                end=ent.end_char,
                confidence=1.0  # spaCy doesn't provide confidence scores
            )
            for ent in doc.ents
        ]

    def extract_relations(self, text: str) -> List[Relation]:
        """Extract subject-verb-object relations from text."""
        self._ensure_loaded()
        doc = self._nlp(text)

        relations = []
        for sent in doc.sents:
            for token in sent:
                if token.dep_ in ('nsubj', 'nsubjpass'):
                    subject = token.text
                    predicate = token.head.text

                    for child in token.head.children:
                        if child.dep_ in ('dobj', 'pobj', 'attr'):
                            relations.append(
                                Relation(
                                    subject=subject,
                                    predicate=predicate,
                                    object=child.text,
                                    confidence=0.8  # Heuristic score
                                )
                            )

        return relations

    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        self._ensure_loaded()
        doc = self._nlp(text)
        return [token.text for token in doc]

    def sentence_segment(self, text: str) -> List[str]:
        """Segment text into sentences."""
        self._ensure_loaded()
        doc = self._nlp(text)
        return [sent.text for sent in doc.sents]
```

**Model Size Recommendations for Jerry:**

| Model | Size | Use Case |
|-------|------|----------|
| `en_core_web_sm` | 12 MB | Prototyping, lightweight deployment |
| `en_core_web_md` | 40 MB | Better accuracy, word vectors included |
| `en_core_web_lg` | 560 MB | Production quality (consider separate service) |

**Citations:**
- [spaCy GitHub Repository](https://github.com/explosion/spacy)
- [spaCy Knowledge Graph Tutorial](https://www.analyticsvidhya.com/blog/2019/10/how-to-build-knowledge-graph-text-using-spacy/)

---

#### 3.2 Hugging Face Transformers

**PyPI Package**: `transformers`
**GitHub**: https://github.com/huggingface/transformers (~140K stars)
**Current Version**: 4.x
**Maintenance**: Active (Hugging Face)

**Key Capabilities:**
- State-of-the-art transformer models (BERT, GPT, T5, etc.)
- Relation extraction (REBEL model)
- Question answering, summarization, translation
- Named entity recognition (fine-tuned BERT)
- 100K+ pre-trained models on Hugging Face Hub
- PyTorch and TensorFlow backends

**Jerry Compatibility**: ✗ **Interface Layer Only**
- Large models (100MB - several GB)
- Requires PyTorch or TensorFlow
- Heavy computational requirements
- **Use in separate extraction service or interface layer**

**Example Usage for Knowledge Graph Construction:**

```python
from transformers import pipeline

# Relation extraction with REBEL
# (REBEL: Relation Extraction By End-to-end Language generation)
triplet_extractor = pipeline(
    'text2text-generation',
    model='Babelscape/rebel-large',
    tokenizer='Babelscape/rebel-large'
)

text = """
Jerry is a framework for behavior and workflow guardrails developed by the Jerry team.
It uses NetworkX for graph operations and RDFLib for semantic knowledge representation.
The Work Tracker manages tasks, phases, and plans within the framework.
"""

# Extract triplets
extracted_text = triplet_extractor(text, return_tensors=True, return_text=False)[0]['generated_token_ids']
extracted_triplets = triplet_extractor.tokenizer.batch_decode(extracted_text)

# Parse triplets (REBEL format: <subj> <relation> <obj> <subj> <relation> <obj> ...)
def extract_triplets_from_rebel(text):
    triplets = []
    relations = text.split('<triplet>')
    for rel in relations:
        if rel.strip():
            parts = rel.split('<subj>')[1].split('<obj>')
            if len(parts) >= 2:
                subject = parts[0].strip()
                rest = parts[1].split('<relation>')
                if len(rest) >= 2:
                    obj = rest[0].strip()
                    relation = rest[1].strip()
                    triplets.append((subject, relation, obj))
    return triplets

triplets = extract_triplets_from_rebel(extracted_triplets[0])
print("Extracted triplets:", triplets)

# Named entity recognition with BERT
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER")
entities = ner_pipeline(text)
print("Entities:", entities)

# Build knowledge graph
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF

g = Graph()
JERRY = Namespace("http://jerry.ai/kg/")

for subj, rel, obj in triplets:
    s_uri = JERRY[subj.replace(' ', '_')]
    r_uri = JERRY[rel.replace(' ', '_')]
    o_uri = JERRY[obj.replace(' ', '_')]
    g.add((s_uri, r_uri, o_uri))

print(g.serialize(format='turtle'))
```

**When to Use:**
- Need state-of-the-art relation extraction
- Building knowledge graph from unstructured text at scale
- Can afford computational cost (GPU recommended)
- **Recommendation**: Deploy as separate extraction service, not embedded

**Citations:**
- [Hugging Face Transformers GitHub](https://github.com/huggingface/transformers)
- [REBEL for Knowledge Graph Construction](https://medium.com/@sauravjoshi23/building-knowledge-graphs-rebel-llamaindex-and-rebel-llamaindex-8769cf800115)

---

#### 3.3 LangChain

**PyPI Package**: `langchain`
**GitHub**: https://github.com/langchain-ai/langchain (~90K stars)
**Current Version**: 0.x (API changes frequently)
**Maintenance**: Very active

**Key Capabilities:**
- High-level LLM application framework
- Document loaders (PDF, HTML, Markdown, etc.)
- Text splitters (semantic chunking)
- Vector store integrations (FAISS, Chroma, Pinecone)
- Chain composition (sequential, parallel, branching)
- Agents and tools
- Knowledge graph support (Cypher, SPARQL)

**Jerry Compatibility**: ⚠ **Interface Layer with Thin Adapters**
- Large framework with many dependencies
- Rapid API changes (version churn)
- **Recommendation**: Use for prototyping, then extract patterns into Jerry
- Prefer thin adapters over deep integration

**Example Usage:**

```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Load documents
loader = TextLoader("jerry_docs.txt")
documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)

# Create embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Create vector store
vectorstore = FAISS.from_documents(chunks, embeddings)

# Create retrieval chain
llm = OpenAI(temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# Query
result = qa_chain.run("What does Jerry use for graph operations?")
print(result)

# Knowledge graph integration
from langchain.graphs import NetworkxEntityGraph
from langchain.chains import GraphQAChain

graph = NetworkxEntityGraph()
graph_chain = GraphQAChain.from_llm(llm, graph=graph)
```

**Jerry Recommendation:**
- Use for **rapid prototyping** of RAG workflows
- Extract successful patterns into Jerry-native implementations
- Don't let LangChain become core dependency
- Create thin adapters in interface layer

**Citations:**
- [LangChain Documentation](https://python.langchain.com/)
- [LangChain GitHub Repository](https://github.com/langchain-ai/langchain)

---

#### 3.4 LlamaIndex

**PyPI Package**: `llama-index`
**GitHub**: https://github.com/run-llama/llama_index (~30K stars)
**Current Version**: 0.x
**Maintenance**: Very active (LlamaCloud)

**Key Capabilities:**
- Data framework for LLM applications
- Document ingestion and indexing
- Query engines (vector, tree, graph)
- Knowledge graph index type
- Agent framework
- Integration with LLMs (OpenAI, Anthropic, local models)
- Hugging Face model support

**Jerry Compatibility**: ⚠ **Interface Layer Only**
- Enterprise-focused (LlamaCloud)
- Heavy dependencies
- Good for data ingestion pipelines
- **Use in interface layer for document processing**

**Example Usage:**

```python
from llama_index import SimpleDirectoryReader, VectorStoreIndex, ServiceContext
from llama_index.llms import HuggingFaceLLM

# Load documents
documents = SimpleDirectoryReader('docs/').load_data()

# Create index
index = VectorStoreIndex.from_documents(documents)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("What is Jerry's architecture?")
print(response)

# Knowledge graph construction
from llama_index.graph_stores import SimpleGraphStore
from llama_index.indices.knowledge_graph import KnowledgeGraphIndex

graph_store = SimpleGraphStore()
kg_index = KnowledgeGraphIndex.from_documents(
    documents,
    storage_context=graph_store
)

# Query knowledge graph
kg_query_engine = kg_index.as_query_engine()
response = kg_query_engine.query("How are tasks and phases related?")
```

**When to Use Over LangChain:**
- Need structured data extraction
- Building production data pipelines
- Want enterprise support (LlamaCloud)

**Citations:**
- [LlamaIndex Documentation](https://developers.llamaindex.ai/)
- [LlamaIndex Knowledge Graph Examples](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/knowledge_graph2/)

---

### 4. Vector/Embedding Storage Libraries

#### 4.1 FAISS (Facebook AI Similarity Search)

**PyPI Package**: `faiss-cpu` or `faiss-gpu`
**GitHub**: https://github.com/facebookresearch/faiss (~30K stars)
**Maintenance**: Active (Meta FAIR)
**Core**: C++ with Python bindings

**Key Capabilities:**
- Efficient similarity search for dense vectors
- Handles billions of vectors
- Multiple index types (Flat, IVF, HNSW, PQ)
- CPU and GPU support
- Sub-10ms latency for million-scale searches
- Clustering algorithms (k-means)
- Product quantization for compression

**Jerry Compatibility**: ✓ **Good for Infrastructure Layer**
- No deep learning framework required (just NumPy)
- Lightweight Python bindings
- C++ core (high performance)
- Pre-compiled wheels available
- **Recommended for vector search in infrastructure**

**Performance Characteristics:**
- Flat index: Exact search, O(n) time
- IVF index: Approximate search, O(√n) time
- HNSW: Graph-based, fast approximate search
- GPU: 10-100x faster than CPU for large datasets

**Example Usage:**

```python
import numpy as np
import faiss

# Create sample embeddings (e.g., from sentence-transformers)
dimension = 384  # Embedding dimension
num_vectors = 10000

# Random embeddings for demonstration
vectors = np.random.random((num_vectors, dimension)).astype('float32')

# Normalize vectors (for cosine similarity)
faiss.normalize_L2(vectors)

# Create index - Flat (exact search)
index = faiss.IndexFlatL2(dimension)
index.add(vectors)

print(f"Index contains {index.ntotal} vectors")

# Search
query_vector = np.random.random((1, dimension)).astype('float32')
faiss.normalize_L2(query_vector)

k = 5  # Number of nearest neighbors
distances, indices = index.search(query_vector, k)

print(f"Top {k} nearest neighbors:")
print(f"Indices: {indices[0]}")
print(f"Distances: {distances[0]}")

# Advanced: IVF index for large datasets
nlist = 100  # Number of clusters
quantizer = faiss.IndexFlatL2(dimension)
index_ivf = faiss.IndexIVFFlat(quantizer, dimension, nlist)

# Train index (required for IVF)
index_ivf.train(vectors)
index_ivf.add(vectors)

# Search with probe parameter (trade speed/accuracy)
index_ivf.nprobe = 10
distances, indices = index_ivf.search(query_vector, k)

# HNSW index (graph-based, no training required)
M = 32  # Number of connections per layer
index_hnsw = faiss.IndexHNSWFlat(dimension, M)
index_hnsw.add(vectors)
distances, indices = index_hnsw.search(query_vector, k)

# Save/load index
faiss.write_index(index, "vector_index.faiss")
loaded_index = faiss.read_index("vector_index.faiss")
```

**Jerry Adapter Pattern:**

```python
# src/infrastructure/embeddings/faiss_adapter.py
from typing import List, Tuple, Optional
import numpy as np
import faiss

from src.domain.ports.vector_store_port import VectorStorePort, SearchResult

class FAISSVectorStore(VectorStorePort):
    """FAISS implementation of vector storage."""

    def __init__(self, dimension: int, index_type: str = "flat"):
        """
        Initialize FAISS index.

        Args:
            dimension: Embedding dimension
            index_type: "flat", "ivf", or "hnsw"
        """
        self._dimension = dimension
        self._index_type = index_type
        self._index = self._create_index(dimension, index_type)
        self._id_map = []  # Map index position to entity ID

    def _create_index(self, dimension: int, index_type: str):
        """Create FAISS index based on type."""
        if index_type == "flat":
            return faiss.IndexFlatL2(dimension)
        elif index_type == "ivf":
            nlist = 100
            quantizer = faiss.IndexFlatL2(dimension)
            return faiss.IndexIVFFlat(quantizer, dimension, nlist)
        elif index_type == "hnsw":
            M = 32
            return faiss.IndexHNSWFlat(dimension, M)
        else:
            raise ValueError(f"Unknown index type: {index_type}")

    def add_vectors(self, entity_ids: List[str], vectors: np.ndarray) -> None:
        """Add vectors to the index."""
        if vectors.dtype != np.float32:
            vectors = vectors.astype('float32')

        # Normalize for cosine similarity
        faiss.normalize_L2(vectors)

        # Train IVF index if needed
        if self._index_type == "ivf" and not self._index.is_trained:
            self._index.train(vectors)

        # Add to index
        self._index.add(vectors)

        # Update ID mapping
        self._id_map.extend(entity_ids)

    def search(
        self,
        query_vector: np.ndarray,
        k: int = 5
    ) -> List[SearchResult]:
        """Search for nearest neighbors."""
        if query_vector.dtype != np.float32:
            query_vector = query_vector.astype('float32')

        # Ensure 2D array
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)

        # Normalize
        faiss.normalize_L2(query_vector)

        # Search
        distances, indices = self._index.search(query_vector, k)

        # Convert to results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx >= 0 and idx < len(self._id_map):
                results.append(SearchResult(
                    entity_id=self._id_map[idx],
                    distance=float(dist),
                    similarity=1.0 / (1.0 + float(dist))  # Convert distance to similarity
                ))

        return results

    def save(self, path: str) -> None:
        """Save index to disk."""
        faiss.write_index(self._index, path)
        # Save ID mapping separately
        np.save(path + ".ids", np.array(self._id_map))

    def load(self, path: str) -> None:
        """Load index from disk."""
        self._index = faiss.read_index(path)
        self._id_map = list(np.load(path + ".ids", allow_pickle=True))

    def size(self) -> int:
        """Return number of vectors in index."""
        return self._index.ntotal
```

**Index Type Selection Guide:**

| Index | Use Case | Training Required | Speed | Accuracy |
|-------|----------|-------------------|-------|----------|
| Flat | <100K vectors, exact search | No | Slow | 100% |
| IVF | 100K-10M vectors, approximate | Yes | Fast | 95-99% |
| HNSW | Any size, graph-based | No | Very fast | 95-99% |
| PQ | Compression (100M+ vectors) | Yes | Very fast | 90-95% |

**Jerry Recommendation**: Start with Flat for prototyping, switch to HNSW for production.

**Citations:**
- [FAISS GitHub Repository](https://github.com/facebookresearch/faiss)
- [FAISS Documentation](https://faiss.ai/)
- [FAISS Tutorial](https://www.pinecone.io/learn/series/faiss/faiss-tutorial/)

---

#### 4.2 ChromaDB

**PyPI Package**: `chromadb`
**GitHub**: https://github.com/chroma-core/chroma (~6K stars)
**Current Version**: 0.4.x
**Maintenance**: Very active

**Key Capabilities:**
- Open-source embedding database
- Built for LLM applications (RAG)
- Stores embeddings + metadata + documents
- Multiple embedding functions (OpenAI, Sentence Transformers, custom)
- SQL-like query interface
- Persistent storage (SQLite backend)
- Client-server mode available

**Jerry Compatibility**: ⚠ **Interface Layer Preferred**
- Larger dependency footprint than FAISS
- Database-oriented (not just vector index)
- Good for LLM integration
- **Use in interface layer for RAG workflows**

**Performance Characteristics:**
- Small to medium datasets (<1M vectors)
- Good for prototyping and development
- Not as optimized as FAISS for pure vector search
- Better integration with LLM workflows

**Example Usage:**

```python
import chromadb
from chromadb.config import Settings

# Create client
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"
))

# Create or get collection
collection = client.get_or_create_collection(
    name="jerry_knowledge",
    metadata={"description": "Jerry framework knowledge base"}
)

# Add documents with embeddings (automatic embedding)
collection.add(
    documents=[
        "Jerry is a framework for behavior and workflow guardrails.",
        "NetworkX is used for graph operations in Jerry.",
        "RDFLib handles semantic knowledge representation.",
        "The Work Tracker manages tasks, phases, and plans."
    ],
    metadatas=[
        {"source": "readme", "type": "overview"},
        {"source": "architecture", "type": "implementation"},
        {"source": "architecture", "type": "implementation"},
        {"source": "features", "type": "component"}
    ],
    ids=["doc1", "doc2", "doc3", "doc4"]
)

# Query (semantic search)
results = collection.query(
    query_texts=["How does Jerry handle graphs?"],
    n_results=2
)

print("Query results:")
for doc, metadata, distance in zip(
    results['documents'][0],
    results['metadatas'][0],
    results['distances'][0]
):
    print(f"Document: {doc}")
    print(f"Metadata: {metadata}")
    print(f"Distance: {distance}")
    print()

# Query with metadata filtering
results = collection.query(
    query_texts=["Tell me about architecture"],
    n_results=2,
    where={"type": "implementation"}
)

# Add with custom embeddings
import numpy as np

custom_embeddings = [np.random.random(384).tolist() for _ in range(2)]
collection.add(
    embeddings=custom_embeddings,
    documents=["Document 1", "Document 2"],
    ids=["custom1", "custom2"]
)

# Update documents
collection.update(
    ids=["doc1"],
    documents=["Jerry is an advanced framework for AI behavior guardrails."],
    metadatas=[{"source": "readme", "type": "overview", "version": "2.0"}]
)

# Delete documents
collection.delete(ids=["custom1", "custom2"])

# Persist (automatic with persist_directory)
# client.persist()  # Explicit persist if needed
```

**Jerry Integration Example:**

```python
# src/interface/rag/chroma_rag.py
import chromadb
from typing import List, Dict, Any

class ChromaRAGService:
    """RAG service using ChromaDB."""

    def __init__(self, persist_directory: str = "./data/chroma"):
        self._client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory
        ))
        self._collection = self._client.get_or_create_collection("jerry_kb")

    def index_documents(self, documents: List[str], metadata: List[Dict[str, Any]]) -> None:
        """Index documents for retrieval."""
        ids = [f"doc_{i}" for i in range(len(documents))]
        self._collection.add(
            documents=documents,
            metadatas=metadata,
            ids=ids
        )

    def retrieve(self, query: str, k: int = 5, filters: Dict[str, Any] = None) -> List[Dict]:
        """Retrieve relevant documents."""
        results = self._collection.query(
            query_texts=[query],
            n_results=k,
            where=filters
        )

        return [
            {
                'document': doc,
                'metadata': meta,
                'distance': dist
            }
            for doc, meta, dist in zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )
        ]
```

**When to Use ChromaDB:**
- Building RAG applications
- Need document + embedding + metadata together
- Want simple, Pythonic API
- Prototyping LLM applications

**When to Use FAISS Instead:**
- Pure vector search (no document storage)
- Maximum performance requirements
- Handling billions of vectors
- Infrastructure layer implementation

**Citations:**
- [ChromaDB GitHub Repository](https://github.com/chroma-core/chroma)
- [ChromaDB Documentation](https://docs.trychroma.com/)

---

#### 4.3 Qdrant

**PyPI Package**: `qdrant-client`
**GitHub**: https://github.com/qdrant/qdrant (~9K stars)
**Core**: Rust (Python client)
**Maintenance**: Very active

**Key Capabilities:**
- Vector similarity search engine (Rust-based)
- HTTP API with Python client
- Powerful metadata filtering
- ACID-compliant transactions
- Distributed deployment
- Horizontal scaling
- Payload storage with vectors
- Hybrid search (vector + keyword)

**Jerry Compatibility**: ⚠ **Requires External Service**
- Client-server architecture
- Run as separate service (Docker)
- Not embeddable like FAISS
- **Use if building production vector search service**

**Example Usage:**

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Connect to Qdrant (local or cloud)
client = QdrantClient(host="localhost", port=6333)
# Or: client = QdrantClient(":memory:")  # In-memory for testing

# Create collection
client.create_collection(
    collection_name="jerry_knowledge",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Add vectors with payload
import numpy as np

vectors = [np.random.random(384).tolist() for _ in range(5)]
payloads = [
    {"text": "Jerry framework overview", "type": "documentation", "section": "intro"},
    {"text": "Graph operations with NetworkX", "type": "code", "section": "infrastructure"},
    {"text": "RDF knowledge representation", "type": "documentation", "section": "knowledge"},
    {"text": "Work Tracker architecture", "type": "design", "section": "features"},
    {"text": "Hexagonal architecture pattern", "type": "architecture", "section": "design"}
]

client.upsert(
    collection_name="jerry_knowledge",
    points=[
        PointStruct(id=i, vector=vec, payload=pay)
        for i, (vec, pay) in enumerate(zip(vectors, payloads))
    ]
)

# Search
query_vector = np.random.random(384).tolist()

results = client.search(
    collection_name="jerry_knowledge",
    query_vector=query_vector,
    limit=3
)

for result in results:
    print(f"ID: {result.id}, Score: {result.score}")
    print(f"Payload: {result.payload}")

# Search with filtering
results = client.search(
    collection_name="jerry_knowledge",
    query_vector=query_vector,
    query_filter={
        "must": [
            {"key": "type", "match": {"value": "documentation"}}
        ]
    },
    limit=2
)

# Hybrid search (vector + keyword)
from qdrant_client.models import Filter, FieldCondition, MatchValue

results = client.search(
    collection_name="jerry_knowledge",
    query_vector=query_vector,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="section",
                match=MatchValue(value="infrastructure")
            )
        ]
    ),
    limit=3
)
```

**Deployment:**

```bash
# Run Qdrant with Docker
docker run -p 6333:6333 qdrant/qdrant
```

**Jerry Recommendation**: Use if building a dedicated vector search service, otherwise prefer FAISS (embedded) or ChromaDB (simpler).

**Citations:**
- [Qdrant GitHub Repository](https://github.com/qdrant/qdrant)
- [Qdrant Documentation](https://qdrant.tech/documentation/)

---

#### 4.4 Comparison Summary: Vector Databases

| Library | Type | Jerry Fit | Best For | Deployment |
|---------|------|-----------|----------|------------|
| **FAISS** | Index library | ✓ Infrastructure | Pure vector search, billions of vectors | Embedded |
| **ChromaDB** | Embedding DB | ⚠ Interface | RAG, prototyping, small-medium scale | Embedded or server |
| **Qdrant** | Vector DB | ⚠ Service | Production search, metadata filtering | Server (Docker/cloud) |
| **Weaviate** | Vector DB | ⚠ Service | Hybrid search, enterprise features | Server (Docker/cloud) |
| **Pinecone** | Vector DB | ✗ Cloud only | Managed service, zero ops | Cloud SaaS |

**Jerry Strategy:**
1. **Prototyping**: ChromaDB (easy, integrated)
2. **Production (embedded)**: FAISS (fast, lightweight)
3. **Production (service)**: Qdrant (scalable, Rust-based)

---

### 5. Ontology/Taxonomy Libraries

#### 5.1 Owlready2 (Covered in Section 2.2)

**See Section 2.2 for detailed coverage.**

**Key Highlights:**
- Load OWL ontologies as Python objects
- Reasoning with HermiT
- SQLite-based quadstore
- **Best Python library for OWL ontologies**

---

#### 5.2 Pronto

**PyPI Package**: `pronto`
**GitHub**: https://github.com/althonos/pronto (~200 stars)
**Current Version**: 2.x
**Maintenance**: Active

**Key Capabilities:**
- OBO ontology parser (biomedical focus)
- Support for OBO, OBOGraph-JSON, RDF/XML
- Fast parsing with Fastobo (Rust)
- Pythonic API (iterate terms, relationships)
- Export to various formats
- Good for Gene Ontology, biomedical ontologies

**Jerry Compatibility**: ⚠ **Specialized Use Case**
- Best for OBO format (biomedical domain)
- Pure Python with Rust parser
- Not general-purpose (OWL support limited)
- **Use only if working with biomedical ontologies**

**Example Usage:**

```python
import pronto

# Load ontology (e.g., Gene Ontology)
ontology = pronto.Ontology("go-basic.obo")

# Or from URL
# ontology = pronto.Ontology("http://purl.obolibrary.org/obo/go/go-basic.obo")

# Iterate terms
for term in ontology.terms():
    print(f"ID: {term.id}, Name: {term.name}")
    if term.definition:
        print(f"Definition: {term.definition}")

# Get specific term
term = ontology["GO:0008150"]  # Biological process
print(f"Term: {term.name}")

# Traverse relationships
for child in term.subclasses():
    print(f"  Child: {child.name}")

# Find by name
terms = ontology.search("metabolic process")
for term in terms:
    print(f"Found: {term.id} - {term.name}")

# Export
ontology.dump("output.obo", format="obo")
```

**Jerry Recommendation**: Skip unless working with biomedical ontologies. Use Owlready2 for general OWL ontologies.

**Citations:**
- [Pronto GitHub Repository](https://github.com/althonos/pronto)
- [Pronto Documentation](https://pronto.readthedocs.io/)

---

#### 5.3 EMMOntoPy

**PyPI Package**: `EMMOntoPy`
**GitHub**: https://github.com/emmo-repo/EMMOntoPy (~50 stars)
**Maintenance**: Active (European Materials Modelling Ontology project)

**Key Capabilities:**
- Extends Owlready2 with additional features
- Access entities by label (skos:prefLabel)
- Reasoning with FaCT++
- Manchester syntax parsing
- Better OWL ontology support than base Owlready2
- Designed for materials science ontologies

**Jerry Compatibility**: ⚠ **Specialized Extension**
- Builds on Owlready2
- Good if Owlready2 is already used
- Additional features for complex ontologies
- **Consider if Owlready2 is insufficient**

**Example Usage:**

```python
from ontopy import get_ontology

# Load ontology
onto = get_ontology("emmo.owl").load()

# Access by label (instead of IRI)
atom = onto.Atom  # Access by label
print(f"Atom IRI: {atom.iri}")

# Reasoning with FaCT++
onto.sync_reasoner(reasoner="FaCT++")

# Manchester syntax
# (More user-friendly than RDF/XML)
```

**Jerry Recommendation**: Use only if already using Owlready2 and need label-based access or FaCT++ reasoning.

**Citations:**
- [EMMOntoPy GitHub Repository](https://github.com/emmo-repo/EMMOntoPy)
- [EMMOntoPy Documentation](https://emmo-repo.github.io/EMMOntoPy/)

---

#### 5.4 SKOS Libraries

**SKOS (Simple Knowledge Organization System)** is an RDF vocabulary for taxonomies, thesauri, and classification schemes.

**Primary Approach: Use RDFLib with SKOS namespace**

```python
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import SKOS, RDF

g = Graph()

# Define concept scheme
scheme = URIRef("http://jerry.ai/taxonomy/")
g.add((scheme, RDF.type, SKOS.ConceptScheme))
g.add((scheme, SKOS.prefLabel, Literal("Jerry Taxonomy")))

# Define concepts
task_concept = URIRef("http://jerry.ai/taxonomy/Task")
g.add((task_concept, RDF.type, SKOS.Concept))
g.add((task_concept, SKOS.prefLabel, Literal("Task")))
g.add((task_concept, SKOS.inScheme, scheme))

# Define hierarchy
phase_concept = URIRef("http://jerry.ai/taxonomy/Phase")
g.add((phase_concept, RDF.type, SKOS.Concept))
g.add((phase_concept, SKOS.prefLabel, Literal("Phase")))
g.add((task_concept, SKOS.broader, phase_concept))

# Alternative notations
g.add((task_concept, SKOS.altLabel, Literal("Work Item")))

# Related concepts
g.add((task_concept, SKOS.related, URIRef("http://jerry.ai/taxonomy/Issue")))

# Export
print(g.serialize(format='turtle'))
```

**Jerry Recommendation**: Use RDFLib with SKOS namespace. No additional library needed.

---

### 6. Document Processing Libraries

#### 6.1 Docling (IBM)

**PyPI Package**: `docling`
**GitHub**: https://github.com/docling-project/docling (~2K stars, new but rising)
**Maintenance**: Very active (IBM, LF AI & Data Foundation)
**Current Status**: Leading solution for 2025-2026

**Key Capabilities:**
- Parse PDF, DOCX, PPTX, XLSX, HTML, images, audio (WAV, MP3)
- Advanced PDF understanding (layout, tables, figures)
- Unified DoclingDocument format
- Export to Markdown, HTML, DocTags, JSON
- Integration with LangChain, LlamaIndex
- OCR support
- Document classification

**Jerry Compatibility**: ✓ **Good for Infrastructure Layer**
- Well-packaged Python library
- Modular design
- Can be used standalone
- **Recommended for document processing**

**Example Usage:**

```python
from docling.document_converter import DocumentConverter

# Initialize converter
converter = DocumentConverter()

# Convert PDF to Markdown
result = converter.convert("document.pdf")

# Access content
markdown_content = result.document.export_to_markdown()
print(markdown_content)

# Export to JSON (structured)
json_content = result.document.export_to_json()

# Export to HTML
html_content = result.document.export_to_html()

# Access document structure
for element in result.document.elements:
    if element.type == "heading":
        print(f"Heading: {element.text}")
    elif element.type == "paragraph":
        print(f"Paragraph: {element.text}")
    elif element.type == "table":
        print(f"Table with {len(element.rows)} rows")

# Process multiple documents
from pathlib import Path

docs_path = Path("./docs")
for doc_file in docs_path.glob("*.pdf"):
    result = converter.convert(str(doc_file))
    output_file = doc_file.with_suffix(".md")
    with open(output_file, "w") as f:
        f.write(result.document.export_to_markdown())

# Integration with LangChain
from langchain.document_loaders import DoclingLoader

loader = DoclingLoader("document.pdf")
documents = loader.load()
```

**Jerry Adapter Pattern:**

```python
# src/infrastructure/documents/docling_adapter.py
from typing import List, Dict, Any
from pathlib import Path
from docling.document_converter import DocumentConverter

from src.domain.ports.document_port import DocumentPort, Document, DocumentElement

class DoclingAdapter(DocumentPort):
    """Docling implementation of document processing."""

    def __init__(self):
        self._converter = DocumentConverter()

    def extract_text(self, file_path: str) -> str:
        """Extract plain text from document."""
        result = self._converter.convert(file_path)
        return result.document.export_to_markdown()

    def extract_structured(self, file_path: str) -> Document:
        """Extract structured document representation."""
        result = self._converter.convert(file_path)

        elements = []
        for elem in result.document.elements:
            elements.append(DocumentElement(
                type=elem.type,
                text=elem.text,
                metadata=elem.metadata or {}
            ))

        return Document(
            path=file_path,
            title=result.document.metadata.get('title', Path(file_path).name),
            elements=elements,
            metadata=result.document.metadata
        )

    def convert_to_markdown(self, file_path: str, output_path: str) -> None:
        """Convert document to Markdown."""
        result = self._converter.convert(file_path)
        markdown = result.document.export_to_markdown()

        with open(output_path, 'w') as f:
            f.write(markdown)

    def batch_process(self, input_dir: str, output_dir: str) -> None:
        """Batch process documents in directory."""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        for doc_file in input_path.glob("*.*"):
            if doc_file.suffix.lower() in ['.pdf', '.docx', '.pptx', '.html']:
                result = self._converter.convert(str(doc_file))
                out_file = output_path / (doc_file.stem + ".md")

                with open(out_file, 'w') as f:
                    f.write(result.document.export_to_markdown())
```

**Performance:**
- Moderate speed (balances accuracy and performance)
- 1GB+ model download on first run
- CPU-based (no GPU required)
- Good quality output (layout preservation)

**Jerry Recommendation**: **Primary choice for document processing** in infrastructure layer.

**Citations:**
- [Docling GitHub Repository](https://github.com/docling-project/docling)
- [Docling Documentation](https://github.com/docling-project/docling)
- [Docling Tutorial](https://www.codecademy.com/article/docling-ai-a-complete-guide-to-parsing)

---

#### 6.2 Marker-PDF

**PyPI Package**: `marker-pdf`
**GitHub**: https://github.com/VikParuchuri/marker (~10K stars)
**Maintenance**: Active
**Focus**: Fast, high-quality PDF to Markdown

**Key Capabilities:**
- Fast PDF to Markdown conversion
- Excellent layout preservation
- Supports all languages
- Handles tables, forms, math, links, code blocks
- Extracts images
- Removes headers/footers/artifacts
- Customizable formatting
- GPU acceleration available

**Jerry Compatibility**: ⚠ **Specialized for PDFs**
- Large first-run download (1GB model)
- Best for PDF-only workflows
- Good output quality
- **Use for PDF-heavy workflows**

**Example Usage:**

```python
from marker.convert import convert_single_pdf
from marker.models import load_all_models

# Load models (first run downloads ~1GB)
model_list = load_all_models()

# Convert PDF
full_text, images, out_meta = convert_single_pdf(
    "document.pdf",
    model_list
)

print("Markdown content:")
print(full_text)

print(f"\nExtracted {len(images)} images")
print(f"Metadata: {out_meta}")

# Save output
with open("document.md", "w") as f:
    f.write(full_text)

# Save images
for i, img in enumerate(images):
    img.save(f"image_{i}.png")
```

**Performance:**
- Very fast (12 seconds for typical PDF)
- 122 pages/second on H100 GPU
- Excellent quality (layout-perfect)
- Heavy first run (model download)

**Jerry Recommendation**: Use if PDFs are primary document type and quality is critical. Otherwise, use Docling for broader format support.

**Citations:**
- [Marker-PDF PyPI Package](https://pypi.org/project/marker-pdf/)
- [Marker GitHub Repository](https://github.com/VikParuchuri/marker)

---

#### 6.3 Unstructured

**PyPI Package**: `unstructured`
**GitHub**: https://github.com/Unstructured-IO/unstructured (~6K stars)
**Maintenance**: Very active (Unstructured.io)

**Key Capabilities:**
- Multi-format support (PDF, HTML, Word, images, etc.)
- Semantic chunking for RAG
- Element-based parsing (title, text, table, etc.)
- OCR support (Tesseract)
- Partition strategies (fast, hi_res)
- Integration with LangChain, LlamaIndex
- Good for diverse document types

**Jerry Compatibility**: ⚠ **Interface Layer Preferred**
- Many dependencies (Tesseract, poppler, etc.)
- Good for RAG workflows
- Semantic chunking useful for embeddings
- **Use in interface layer for LLM workflows**

**Example Usage:**

```python
from unstructured.partition.auto import partition

# Auto-detect format and parse
elements = partition("document.pdf")

# Iterate elements
for element in elements:
    print(f"Type: {element.category}")
    print(f"Text: {element.text}")
    print()

# Get only specific types
titles = [el.text for el in elements if el.category == "Title"]
tables = [el for el in elements if el.category == "Table"]

# Partition with strategy
elements = partition(
    "document.pdf",
    strategy="hi_res",  # Use OCR for better quality
    languages=["eng"]
)

# Chunk for RAG
from unstructured.chunking.title import chunk_by_title

chunks = chunk_by_title(
    elements,
    max_characters=1000,
    combine_text_under_n_chars=100
)

# Integration with LangChain
from langchain.document_loaders import UnstructuredPDFLoader

loader = UnstructuredPDFLoader("document.pdf")
documents = loader.load()
```

**Performance:**
- Moderate speed (depends on strategy)
- "fast" strategy: Quick but lower quality
- "hi_res" strategy: Slower but better quality (OCR)
- Good semantic chunking

**Jerry Recommendation**: Use for RAG workflows in interface layer when semantic chunking is needed. Prefer Docling for general document processing.

**Citations:**
- [Unstructured GitHub Repository](https://github.com/Unstructured-IO/unstructured)
- [Unstructured Documentation](https://unstructured-io.github.io/unstructured/)

---

#### 6.4 Document Processing Comparison

| Library | Formats | Best For | Performance | Jerry Fit |
|---------|---------|----------|-------------|-----------|
| **Docling** | PDF, DOCX, PPTX, HTML, images | All-in-one solution | Moderate | ✓ Infrastructure |
| **Marker-PDF** | PDF only | High-quality PDF extraction | Fast | ⚠ Specialized |
| **Unstructured** | PDF, HTML, Word, images | RAG workflows, semantic chunking | Moderate | ⚠ Interface |
| **pymupdf4llm** | PDF | Fast, simple PDF parsing | Very fast (0.12s) | ✓ Lightweight |
| **pypdf** | PDF | Basic PDF text extraction | Fast | ✓ Stdlib-friendly |

**Jerry Strategy:**
1. **General use**: Docling (infrastructure layer)
2. **PDF-only, quality critical**: Marker-PDF
3. **RAG with semantic chunking**: Unstructured (interface layer)
4. **Lightweight PDF extraction**: pymupdf or pypdf

---

## L2: Architecture Fit for Jerry

### Hexagonal Architecture Integration

Jerry's architecture follows the **Hexagonal (Ports & Adapters)** pattern with strict dependency rules:

```
┌─────────────────────────────────────────────────┐
│              Interface Layer                     │
│  (CLI, API, Agents, Skills)                     │
│  Heavy frameworks: LangChain, LlamaIndex, PyG   │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│           Application Layer (CQRS)              │
│  Use Cases: Commands & Queries                  │
│  No external dependencies                       │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│         Infrastructure Layer (Adapters)         │
│  Lightweight libs: NetworkX, RDFLib, FAISS      │
│  Implements ports from domain                   │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│         Domain Layer (Business Logic)           │
│  Pure Python, NO external dependencies          │
│  Defines ports (interfaces)                     │
└─────────────────────────────────────────────────┘
```

### Dependency Tier Assignment

**Tier 1: Infrastructure Layer (✓ Acceptable)**
- NetworkX (pure Python, minimal deps)
- RDFLib (pure Python, stdlib-based)
- FAISS (C++ core, Python bindings, no framework)
- Owlready2 (Python + SQLite)
- spaCy (with small models, <50MB)
- Docling (well-packaged, modular)

**Tier 2: Infrastructure with Caution (⚠ Evaluate)**
- igraph (C core, pre-compiled wheels)
- ChromaDB (larger footprint, but useful for RAG)
- Marker-PDF (large models, but excellent quality)

**Tier 3: Interface Layer Only (✗ Never in Core)**
- PyTorch Geometric (full deep learning stack)
- DGL (multi-framework)
- LangChain (heavy framework, rapid changes)
- LlamaIndex (enterprise ecosystem)
- Transformers (large models, PyTorch/TensorFlow)
- Weaviate, Qdrant, Pinecone (external services)

### Port Definitions (Domain Layer)

```python
# src/domain/ports/graph_port.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class Node:
    id: str
    label: str
    properties: Dict[str, Any]

@dataclass
class Edge:
    source: str
    target: str
    edge_type: str
    properties: Dict[str, Any]

class GraphPort(ABC):
    """Port for graph storage and traversal operations."""

    @abstractmethod
    def add_node(self, node_id: str, label: str, properties: Dict[str, Any]) -> None:
        """Add a node to the graph."""
        pass

    @abstractmethod
    def add_edge(
        self,
        source: str,
        target: str,
        edge_type: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add an edge to the graph."""
        pass

    @abstractmethod
    def get_node(self, node_id: str) -> Optional[Node]:
        """Retrieve a node by ID."""
        pass

    @abstractmethod
    def traverse_out(self, node_id: str, edge_type: Optional[str] = None) -> List[Node]:
        """Traverse outgoing edges from a node."""
        pass

    @abstractmethod
    def query(self, pattern: 'TraversalPattern') -> List[Node]:
        """Execute a traversal pattern query."""
        pass
```

```python
# src/domain/ports/knowledge_port.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class KnowledgePort(ABC):
    """Port for semantic knowledge graph operations (RDF/OWL)."""

    @abstractmethod
    def add_triple(self, subject: str, predicate: str, obj: str) -> None:
        """Add a triple to the knowledge graph."""
        pass

    @abstractmethod
    def query_sparql(self, query: str) -> List[Dict[str, Any]]:
        """Execute a SPARQL query."""
        pass

    @abstractmethod
    def export_turtle(self) -> str:
        """Export graph to Turtle format."""
        pass

    @abstractmethod
    def export_jsonld(self) -> str:
        """Export graph to JSON-LD format."""
        pass
```

```python
# src/domain/ports/vector_store_port.py
from abc import ABC, abstractmethod
from typing import List, Tuple
import numpy as np
from dataclasses import dataclass

@dataclass
class SearchResult:
    entity_id: str
    distance: float
    similarity: float

class VectorStorePort(ABC):
    """Port for vector similarity search."""

    @abstractmethod
    def add_vectors(self, entity_ids: List[str], vectors: np.ndarray) -> None:
        """Add vectors to the store."""
        pass

    @abstractmethod
    def search(self, query_vector: np.ndarray, k: int = 5) -> List[SearchResult]:
        """Search for nearest neighbors."""
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        """Persist vectors to disk."""
        pass

    @abstractmethod
    def load(self, path: str) -> None:
        """Load vectors from disk."""
        pass
```

```python
# src/domain/ports/document_port.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class DocumentElement:
    type: str  # "heading", "paragraph", "table", etc.
    text: str
    metadata: Dict[str, Any]

@dataclass
class Document:
    path: str
    title: str
    elements: List[DocumentElement]
    metadata: Dict[str, Any]

class DocumentPort(ABC):
    """Port for document processing operations."""

    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        """Extract plain text from document."""
        pass

    @abstractmethod
    def extract_structured(self, file_path: str) -> Document:
        """Extract structured document representation."""
        pass

    @abstractmethod
    def convert_to_markdown(self, file_path: str, output_path: str) -> None:
        """Convert document to Markdown."""
        pass
```

### Adapter Implementation Strategy

**Directory Structure:**

```
src/infrastructure/
├── graph/
│   ├── networkx_adapter.py      # NetworkX implementation
│   ├── igraph_adapter.py        # igraph implementation (future)
│   └── gremlin_adapter.py       # Gremlin implementation (future)
├── knowledge/
│   ├── rdflib_adapter.py        # RDFLib implementation
│   └── owlready_adapter.py      # Owlready2 implementation (optional)
├── embeddings/
│   ├── faiss_adapter.py         # FAISS implementation
│   └── chroma_adapter.py        # ChromaDB implementation (interface)
├── nlp/
│   └── spacy_adapter.py         # spaCy implementation
└── documents/
    ├── docling_adapter.py       # Docling implementation
    ├── marker_adapter.py        # Marker-PDF implementation (optional)
    └── unstructured_adapter.py  # Unstructured implementation (interface)
```

**Adapter Swapping:**

```python
# src/infrastructure/graph/factory.py
from src.domain.ports.graph_port import GraphPort
from typing import Literal

GraphBackend = Literal["networkx", "igraph", "gremlin"]

def create_graph_adapter(backend: GraphBackend = "networkx") -> GraphPort:
    """Factory to create graph adapter."""
    if backend == "networkx":
        from src.infrastructure.graph.networkx_adapter import NetworkXGraphAdapter
        return NetworkXGraphAdapter()
    elif backend == "igraph":
        from src.infrastructure.graph.igraph_adapter import IGraphAdapter
        return IGraphAdapter()
    elif backend == "gremlin":
        from src.infrastructure.graph.gremlin_adapter import GremlinAdapter
        return GremlinAdapter()
    else:
        raise ValueError(f"Unknown graph backend: {backend}")
```

**Configuration:**

```yaml
# config/infrastructure.yaml
graph:
  backend: networkx  # or igraph, gremlin

knowledge:
  backend: rdflib  # or owlready
  base_uri: "http://jerry.ai/ontology/"

vector_store:
  backend: faiss  # or chroma
  dimension: 384
  index_type: hnsw

nlp:
  backend: spacy
  model: en_core_web_sm

document:
  backend: docling  # or marker, unstructured
```

### Dependency Management

**requirements/base.txt** (Domain + Application):
```txt
# NO external dependencies for domain/application layers
```

**requirements/infrastructure.txt**:
```txt
# Lightweight infrastructure dependencies
networkx>=3.0
rdflib>=7.0
faiss-cpu>=1.7.0
spacy>=3.0
docling>=0.1.0
owlready2>=0.40  # optional
```

**requirements/interface.txt**:
```txt
# Heavy interface dependencies
torch>=2.0
torch-geometric>=2.0  # optional
chromadb>=0.4.0  # optional
langchain>=0.1.0  # optional
transformers>=4.30.0  # optional
```

**Installation Strategy:**

```bash
# Core installation (always)
pip install -r requirements/base.txt
pip install -r requirements/infrastructure.txt

# Optional: Interface layer features
pip install -r requirements/interface.txt

# Minimal installation (no ML/AI)
pip install networkx rdflib
```

### Migration Path

**Phase 1: Prototyping (Current)**
- NetworkX for graph operations
- RDFLib for semantic knowledge
- FAISS for vector search (when needed)
- Docling for document processing

**Phase 2: Scaling (10K-1M nodes)**
- **Swap NetworkX → igraph** (via adapter factory)
- Keep RDFLib (or consider triplestore backend)
- Optimize FAISS index type (Flat → HNSW)

**Phase 3: Large-Scale (>1M nodes)**
- **Swap igraph → graph-tool** (if analytics-heavy)
- **OR: Swap to Gremlin** (distributed graph DB)
- Consider external triplestore (Virtuoso, Stardog)
- Qdrant for vector search (if service-based)

**Key Principle**: Domain layer never changes. Only swap adapters.

---

## L3: Dependency Analysis

### Zero-Dependency Libraries (Domain Layer)

**None.** Modern KM requires external libraries. Focus on **minimal dependencies** instead.

### Minimal Dependency Libraries (Infrastructure Layer)

#### NetworkX
```
networkx==3.6.1
├── no required dependencies (pure Python)
└── optional: numpy, scipy, matplotlib, pandas
```
**Analysis**: Cleanest dependency graph. Ideal for Jerry.

#### RDFLib
```
rdflib==7.0.0
├── pyparsing>=2.1.0  (parsing library)
├── isodate>=0.6.0    (date parsing)
└── optional: html5lib, SPARQLWrapper
```
**Analysis**: Minimal, stdlib-friendly dependencies. Good fit.

#### FAISS
```
faiss-cpu==1.8.0
├── numpy>=1.16  (arrays)
└── no other dependencies (C++ core)
```
**Analysis**: Lightweight for vector search. Excellent fit.

### Moderate Dependency Libraries

#### spaCy (small model)
```
spacy==3.7.0
├── spacy-legacy>=3.0.0
├── spacy-loggers>=1.0.0
├── murmurhash>=0.28.0  (hashing)
├── cymem>=2.0.2  (memory management)
├── preshed>=3.0.2  (hash tables)
├── thinc>=8.2.0  (ML library)
├── wasabi>=0.9.1  (pretty printing)
├── srsly>=2.4.3  (serialization)
├── catalogue>=2.0.6  (registry)
├── weasel>=0.1.0  (CLI)
├── typer>=0.3.0  (CLI)
├── pydantic>=1.7.4  (validation)
├── jinja2  (templating)
├── setuptools  (stdlib)
├── packaging  (stdlib)
└── langcodes>=3.2.0  (language codes)

Model: en_core_web_sm (12 MB)
```
**Analysis**: More dependencies than ideal, but manageable. Core is optimized (Cython). Use smallest model.

#### Owlready2
```
owlready2==0.49
└── no required dependencies (uses stdlib sqlite3)
```
**Analysis**: Surprisingly clean. Self-contained reasoner. Good fit.

#### Docling
```
docling==1.x
├── various parsing libraries
├── pillow (image processing)
├── numpy
└── model dependencies (~1GB first run)
```
**Analysis**: Heavier than ideal, but comprehensive. Well-packaged. Acceptable for infrastructure.

### Heavy Dependency Libraries (Interface Layer Only)

#### PyTorch Geometric
```
torch-geometric==2.x
├── torch>=2.0  (~2GB)
├── torch-scatter
├── torch-sparse
├── torch-cluster
├── torch-spline-conv
└── numpy, scipy, tqdm, etc.
```
**Analysis**: Massive dependency tree. GPU-focused. Interface layer only.

#### LangChain
```
langchain==0.1.x
├── langchain-core
├── langchain-community
├── pydantic>=2.0
├── SQLAlchemy>=1.4
├── requests
├── PyYAML
├── numpy
├── aiohttp
├── tenacity
└── many integration packages
```
**Analysis**: Large framework with many dependencies. Rapid version changes. Use thin adapters only.

#### ChromaDB
```
chromadb==0.4.x
├── requests>=2.28
├── pydantic>=1.9
├── chroma-hnswlib>=0.7
├── fastapi>=0.95.2
├── uvicorn>=0.18.3
├── numpy>=1.21.6
├── posthog>=2.4.0
├── typing_extensions>=4.5.0
├── pulsar-client>=3.1.0
├── onnxruntime>=1.14.1
├── tokenizers>=0.13.2
├── pypika>=0.48.9
├── overrides>=7.3.1
└── importlib-resources  (if Python < 3.9)
```
**Analysis**: Heavy for an "embedding database." Includes server components. Interface layer preferred.

### Transitive Dependency Concerns

**NumPy Conflict**: Many libraries depend on NumPy. Ensure version compatibility:
- FAISS: numpy>=1.16
- spaCy: numpy (via thinc)
- ChromaDB: numpy>=1.21
- PyTorch: includes own numpy-compatible tensors

**PyTorch Conflict**: PyG and DGL both require PyTorch. Consider:
- Use only one GNN library
- Pin PyTorch version
- Test compatibility before upgrading

**Pydantic v1 vs v2**: LangChain moved to Pydantic v2, some libraries still on v1:
- Check compatibility before mixing
- Use pydantic v2 if possible (faster, better typing)

### Installation Size Analysis

| Library | Wheel Size | Installed Size | Models/Data | Total |
|---------|-----------|----------------|-------------|-------|
| networkx | 1.6 MB | 4 MB | 0 | 4 MB |
| rdflib | 500 KB | 3 MB | 0 | 3 MB |
| faiss-cpu | 10 MB | 30 MB | 0 | 30 MB |
| owlready2 | 100 KB | 500 KB | 0 | 500 KB |
| spacy | 7 MB | 20 MB | 12 MB (small) | 32 MB |
| docling | ~50 MB | ~150 MB | ~1 GB (first run) | ~1.2 GB |
| torch | ~800 MB | ~2 GB | varies | 2+ GB |
| transformers | ~4 MB | ~10 MB | 100 MB - 10 GB | varies |

**Jerry Footprint:**

| Configuration | Total Size | Notes |
|---------------|-----------|-------|
| **Minimal** (NetworkX + RDFLib) | ~10 MB | Graph + semantic only |
| **Standard** (+ FAISS + spaCy small) | ~80 MB | + vector search + NLP |
| **Full Infrastructure** (+ Docling) | ~1.3 GB | + document processing |
| **With ML** (+ PyTorch + transformers) | ~3+ GB | Interface layer features |

**Recommendation**: Ship Jerry with **Standard** configuration. Make **Full Infrastructure** and **With ML** optional.

### Dependency Isolation Strategy

**Use Virtual Environments:**

```bash
# Base environment (infrastructure)
python -m venv venv-base
source venv-base/bin/activate
pip install networkx rdflib faiss-cpu spacy docling

# ML environment (interface)
python -m venv venv-ml
source venv-ml/bin/activate
pip install -r requirements/interface.txt
```

**Use Docker Layers:**

```dockerfile
# Base image with infrastructure deps
FROM python:3.11-slim AS base
COPY requirements/infrastructure.txt .
RUN pip install --no-cache-dir -r infrastructure.txt

# ML image extends base
FROM base AS ml
COPY requirements/interface.txt .
RUN pip install --no-cache-dir -r interface.txt
```

**Use Optional Extras:**

```python
# setup.py or pyproject.toml
[project.optional-dependencies]
infrastructure = [
    "networkx>=3.0",
    "rdflib>=7.0",
    "faiss-cpu>=1.7",
]
nlp = [
    "spacy>=3.0",
    "en-core-web-sm @ https://...",
]
documents = [
    "docling>=0.1",
]
ml = [
    "torch>=2.0",
    "transformers>=4.30",
    "langchain>=0.1",
]
all = [
    "jerry[infrastructure,nlp,documents,ml]",
]
```

**Install:**

```bash
# Minimal
pip install jerry

# With infrastructure
pip install jerry[infrastructure]

# Full stack
pip install jerry[all]
```

---

## Recommendations Summary

### Tier 1: Use Now (Infrastructure Layer)

1. **NetworkX** - Primary graph library
   - Pure Python, minimal deps
   - Easy to swap later
   - Good for <10K nodes

2. **RDFLib** - Semantic knowledge graphs
   - Standards-compliant (RDF, OWL, SPARQL)
   - Pure Python
   - Industry standard

3. **FAISS** - Vector similarity search
   - Lightweight (no framework dependency)
   - High performance (C++ core)
   - Scalable to billions of vectors

4. **spaCy** - NLP for entity/relation extraction
   - Use small model (en_core_web_sm)
   - Modular pipelines
   - Good quality/performance balance

5. **Docling** - Document processing
   - Multi-format support
   - Good quality output
   - Well-packaged

### Tier 2: Consider Later (Scaling)

1. **igraph** - When graph performance becomes bottleneck
2. **Owlready2** - If need formal OWL reasoning
3. **ChromaDB** - For RAG prototyping (interface layer)
4. **Marker-PDF** - If PDF quality is critical

### Tier 3: Interface Layer Only

1. **PyTorch Geometric / DGL** - Graph neural networks
2. **Transformers** - State-of-the-art NLP models
3. **LangChain / LlamaIndex** - RAG frameworks (thin adapters)
4. **Qdrant / Weaviate** - Vector databases (if service-based)

### Avoid / Not Recommended

1. **Pinecone** - Cloud-only, vendor lock-in
2. **Heavy GNN libraries in core** - Keep in interface layer
3. **Multiple GNN frameworks** - Pick one (PyG recommended)
4. **LangChain deep integration** - Rapid API changes, use adapters

---

## Citations & References

### Graph Libraries
- [NetworkX GitHub Repository](https://github.com/networkx/networkx)
- [NetworkX PyPI Package](https://pypi.org/project/networkx/)
- [igraph Python Package](https://pypi.org/project/python-igraph/)
- [graph-tool Performance Benchmarks](https://graph-tool.skewed.de/performance.html)
- [PyTorch Geometric GitHub](https://github.com/pyg-team/pytorch_geometric)
- [PyG vs DGL Comparison](https://www.exxactcorp.com/blog/Deep-Learning/pytorch-geometric-vs-deep-graph-library)
- [DGL GitHub Repository](https://github.com/dmlc/dgl)
- [Graph Library Benchmark](https://www.timlrx.com/blog/benchmark-of-popular-graph-network-packages)
- [Graphs with Python Overview](https://towardsdatascience.com/graphs-with-python-overview-and-best-libraries-a92aa485c2f8/)

### RDF/Semantic Web Libraries
- [RDFLib GitHub Repository](https://github.com/RDFLib/rdflib)
- [RDFLib PyPI Package](https://pypi.org/project/rdflib/)
- [RDFLib Documentation](https://rdflib.readthedocs.io/)
- [Owlready2 PyPI Package](https://pypi.org/project/owlready2/)
- [Owlready2 Documentation](https://owlready2.readthedocs.io/)
- [kglab GitHub Repository](https://github.com/DerwenAI/kglab)
- [Semantic Python Overview](https://github.com/pysemtec/semantic-python-overview)

### Knowledge Graph Construction
- [spaCy GitHub Repository](https://github.com/explosion/spacy)
- [spaCy Knowledge Graph Tutorial](https://www.analyticsvidhya.com/blog/2019/10/how-to-build-knowledge-graph-text-using-spacy/)
- [Building KG with spaCy and LLMs](https://medium.com/mantisnlp/constructing-a-knowledge-base-with-spacy-and-spacy-llm-f65b50ea534d)
- [Hugging Face Transformers GitHub](https://github.com/huggingface/transformers)
- [REBEL for Knowledge Graph Construction](https://medium.com/@sauravjoshi23/building-knowledge-graphs-rebel-llamaindex-and-rebel-llamaindex-8769cf800115)
- [LangChain Documentation](https://python.langchain.com/)
- [LangChain GitHub Repository](https://github.com/langchain-ai/langchain)
- [LlamaIndex Documentation](https://developers.llamaindex.ai/)
- [LlamaIndex Knowledge Graph Examples](https://developers.llamaindex.ai/python/examples/index_structs/knowledge_graph/knowledge_graph2/)

### Vector Databases
- [FAISS GitHub Repository](https://github.com/facebookresearch/faiss)
- [FAISS Documentation](https://faiss.ai/)
- [FAISS Tutorial](https://www.pinecone.io/learn/series/faiss/faiss-tutorial/)
- [ChromaDB GitHub Repository](https://github.com/chroma-core/chroma)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Qdrant GitHub Repository](https://github.com/qdrant/qdrant)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Vector Database Comparison 2025](https://liquidmetal.ai/casesAndBlogs/vector-comparison/)
- [Best Vector Databases 2026](https://www.datacamp.com/blog/the-top-5-vector-databases)
- [Vector Database Comparison Guide](https://www.firecrawl.dev/blog/best-vector-databases-2025)

### Ontology/Taxonomy Libraries
- [Pronto GitHub Repository](https://github.com/althonos/pronto)
- [EMMOntoPy GitHub Repository](https://github.com/emmo-repo/EMMOntoPy)
- [Comparing Python Ontology Libraries](https://incenp.org/notes/2025/comparing-python-ontology-libraries.html)

### Document Processing Libraries
- [Docling GitHub Repository](https://github.com/docling-project/docling)
- [Docling Tutorial](https://www.codecademy.com/article/docling-ai-a-complete-guide-to-parsing)
- [Marker-PDF PyPI Package](https://pypi.org/project/marker-pdf/)
- [Unstructured GitHub Repository](https://github.com/Unstructured-IO/unstructured)
- [I Tested 7 Python PDF Extractors](https://dev.to/onlyoneaman/i-tested-7-python-pdf-extractors-so-you-dont-have-to-2025-edition-akm)
- [Best Python PDF to Text Parser Libraries 2026](https://unstract.com/blog/evaluating-python-pdf-to-text-libraries/)

---

## Appendix: Quick Start Examples

### Example 1: Build Simple Knowledge Graph with NetworkX + RDFLib

```python
# Build knowledge graph from Jerry documentation
import networkx as nx
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS

# NetworkX graph (property graph)
pg = nx.DiGraph()
pg.add_node("jerry", type="framework", lang="python")
pg.add_node("networkx", type="library", purpose="graphs")
pg.add_node("rdflib", type="library", purpose="semantic")
pg.add_edge("jerry", "networkx", relationship="uses")
pg.add_edge("jerry", "rdflib", relationship="uses")

# RDF graph (semantic)
kg = Graph()
JERRY = Namespace("http://jerry.ai/")
kg.add((JERRY.Jerry, RDF.type, JERRY.Framework))
kg.add((JERRY.Jerry, JERRY.uses, JERRY.NetworkX))
kg.add((JERRY.Jerry, JERRY.uses, JERRY.RDFLib))

print(kg.serialize(format='turtle'))
```

### Example 2: Vector Search with FAISS

```python
import numpy as np
import faiss

# Create embeddings (use sentence-transformers in production)
vectors = np.random.random((1000, 384)).astype('float32')
faiss.normalize_L2(vectors)

# Build index
index = faiss.IndexHNSWFlat(384, 32)
index.add(vectors)

# Search
query = np.random.random((1, 384)).astype('float32')
faiss.normalize_L2(query)
distances, indices = index.search(query, 5)

print(f"Nearest neighbors: {indices[0]}")
```

### Example 3: Extract Entities with spaCy

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Jerry uses NetworkX for graph operations.")

for ent in doc.ents:
    print(f"Entity: {ent.text}, Type: {ent.label_}")

# Build graph from entities
from rdflib import Graph, Namespace
g = Graph()
JERRY = Namespace("http://jerry.ai/")

for ent in doc.ents:
    g.add((JERRY[ent.text], JERRY.type, JERRY[ent.label_]))

print(g.serialize(format='turtle'))
```

### Example 4: Process Document with Docling

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("document.pdf")

# Export to Markdown
markdown = result.document.export_to_markdown()
with open("output.md", "w") as f:
    f.write(markdown)

# Extract structured data
for element in result.document.elements:
    if element.type == "heading":
        print(f"Heading: {element.text}")
```

---

**END OF RESEARCH DOCUMENT**
