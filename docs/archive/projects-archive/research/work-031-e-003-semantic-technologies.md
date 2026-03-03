# Semantic Presentation Technologies Research

> **Research Date:** 2026-01-08
> **Status:** DECISION-GRADE
> **PS ID:** work-031
> **Entry ID:** e-003
> **Purpose:** Research technologies for semantic presentation and knowledge graph tooling
> **Extends:** `docs/research/GRAPH_DATA_MODEL_ANALYSIS.md`

---

## L0: Executive Summary (Plain Language)

This research extends the existing graph data model analysis by surveying the ecosystem of tools and technologies for building, storing, querying, and visualizing knowledge graphs and semantic data.

### Key Findings

1. **Triple Stores**: Oxigraph emerges as the best embedded option for Jerry (pure Rust, Python bindings, zero Java dependencies), while Apache Jena/Fuseki leads for server-based deployments.

2. **Graph Databases**: Neo4j dominates for property graphs, but Amazon Neptune offers best cloud-native TinkerPop/Gremlin support. ArangoDB provides unique multi-model flexibility.

3. **Python Libraries**: kglab provides an abstraction layer across paradigms, owlready2 excels at OWL ontology work, and pyoxigraph delivers embedded RDF storage.

4. **Visualization**: Gephi for desktop analysis, Cytoscape.js for web interactivity, NetworkX for Python integration.

5. **Embedded vs Server**: Embedded databases (Oxigraph, SQLite) align with Jerry's zero-dependency philosophy; server-based solutions (Jena Fuseki, Neo4j) offer better scalability but require infrastructure.

### Strategic Recommendation for Jerry

**Phase 1 (Current)**: Continue with property graph abstraction layer + file-based JSON storage
**Phase 2**: Add pyoxigraph as embedded RDF triple store adapter
**Phase 3**: Expose SPARQL endpoint via Python (SPARQLWrapper + Flask)
**Phase 4**: Visualization via NetworkX + Cytoscape.js for web presentation

---

## L1: Technical Details

### 1. Triple Stores (RDF Storage)

Triple stores persist RDF data (subject-predicate-object triples) and provide SPARQL query capabilities.

#### 1.1 Apache Jena / Fuseki

**What**: Java-based semantic web framework with TDB2 native triple store and Fuseki SPARQL server
**Who Maintains**: Apache Software Foundation
**Why Use**: Industry standard, mature, handles millions of triples efficiently
**When**: Server-based deployments requiring SPARQL endpoints
**Where**: Powers DBpedia and many enterprise knowledge graphs
**How (Python)**: HTTP/SPARQL via SPARQLWrapper, no direct API

**Key Features**:
- TDB2: High-performance native triple store supporting full Jena APIs
- Fuseki: REST-style SPARQL endpoint over HTTP
- Parallel loading: Import millions of triples in minutes using tdb2_tdbloader
- OWL/RDFS reasoning support
- Named graph support (dataset-level organization)

**Performance**: Can combine Fuseki's persistent TDB2 stores with parallel loading to handle millions of triples with named graphs in minutes.

**Python Integration**:
```python
from SPARQLWrapper import SPARQLWrapper, JSON
sparql = SPARQLWrapper("http://localhost:3030/dataset/sparql")
sparql.setQuery("SELECT * WHERE { ?s ?p ?o } LIMIT 10")
sparql.setReturnFormat(JSON)
results = sparql.queryAndConvert()
```

**Citations**: [Apache Jena](https://jena.apache.org/), [Accelerated Parallel RDF Loading](https://medium.com/@deepakpatwal/accelerated-parallel-rdf-loading-import-millions-of-triples-from-multiple-datasets-using-the-c49a3a6eba37)

---

#### 1.2 Virtuoso Universal Server

**What**: Multi-model relational database with linked data component (RDF + SQL)
**Who Maintains**: OpenLink Software (commercial + open-source editions)
**Why Use**: Extremely fast query performance (3x faster than competitors for deep queries)
**When**: Large-scale deployments (DBpedia uses Virtuoso 7)
**Where**: DBpedia, life sciences knowledge graphs
**How (Python)**: HTTP SPARQL endpoints via SPARQLWrapper

**Key Features**:
- Hybrid architecture: RDF layer over relational database
- 95% better query response than Sesame/Blazegraph for most queries
- Deep query performance: 128ms vs Blazegraph's 3+ seconds
- Commercial version offers high availability clustering
- Supports both SPARQL and SQL queries

**Performance**: Virtuoso and AnzoGraph are significantly faster (almost 3 times faster than Stardog) than other triplestores across diverse queries.

**Tradeoffs**:
- **Pro**: Exceptional performance, proven at scale (DBpedia)
- **Con**: Confusing admin interface, C code compilation issues reported, not always returning correct triples in some edge cases
- **Con**: Stricter requirements for geographical data than Blazegraph

**Citations**: [Comparing Linked Data Triplestores](https://medium.com/wallscope/comparing-linked-data-triplestores-ebfac8c3ad4f), [Wikimedia Virtuoso Evaluation](https://phabricator.wikimedia.org/T206561)

---

#### 1.3 Blazegraph

**What**: Pure Java high-performance triple store (now part of Amazon Neptune)
**Who Maintains**: Originally Systap LLC, now Amazon (used in Neptune backend)
**Why Use**: Powers Wikidata Query Service, strong SPARQL 1.1 support
**When**: Java-based environments, Wikidata-style use cases
**Where**: Wikidata Query Service
**How (Python)**: HTTP SPARQL endpoints via SPARQLWrapper

**Key Features**:
- Syntax highlighting in query editor
- Server-side pagination
- Query performance logging
- Fast RDF/XML loading (2x faster than average)
- Pure Java (easy deployment via JAR)

**Performance**:
- **Strengths**: Fast loading, good for shallow queries
- **Weaknesses**: Trails behind on deep queries (3+ seconds vs Virtuoso's 128ms)

**Tradeoffs**:
- **Pro**: Pure Java, easy to configure, battle-tested (Wikidata)
- **Con**: Slower on deep graph traversals, development slowed after Amazon acquisition

**Citations**: [Comparing Triple Stores](https://utecht.github.io/rdf/triple%20stores/comparing-triplestores/), [Blazegraph vs Virtuoso](https://db-engines.com/en/system/Blazegraph%3BVirtuoso)

---

#### 1.4 Oxigraph ⭐ (Jerry Recommended for Embedded Use)

**What**: Pure Rust SPARQL graph database with Python bindings (pyoxigraph)
**Who Maintains**: Tpt (Oxigraph GitHub organization)
**Why Use**: Modern, fast, embeddable, zero Java dependencies, active development
**When**: Embedded use cases, Python-first applications
**Where**: NaasAI platform, research projects
**How (Python)**: Native Python API via pyoxigraph

**Key Features**:
- **Embedded storage**: In-memory or RocksDB-backed disk storage
- **SPARQL 1.1 support**: Full query, update, federation
- **RDF 1.2 / SPARQL 1.2**: W3C working draft support (enabled by default in Python)
- **RDF* support**: Triple terms for meta-properties
- **Multiple serialization formats**: Turtle, TriG, N-Triples, N-Quads, RDF/XML, JSON-LD 1.0
- **PyO3-based Python bindings**: Native performance, no JVM
- **rdflib integration**: oxrdflib provides drop-in replacement for rdflib stores

**Architecture**:
- RocksDB backend with 11 key-value tables
- 1 table (id2str) for string IDs
- 9 tables for different quad orders (SPO, POS, OSP, etc.)
- 1 table for named graph registry

**Python Integration**:
```python
from pyoxigraph import Store

# In-memory store
store = Store()

# Disk-based store
store = Store(path="/path/to/data")

# Load triples
store.load("data.ttl", format="ttl")

# SPARQL query
results = store.query("SELECT * WHERE { ?s ?p ?o } LIMIT 10")
for result in results:
    print(result)
```

**Integration with rdflib**:
```python
from rdflib import Graph
g = Graph(store="Oxigraph")  # Drop-in replacement
g.parse("data.ttl")
results = g.query("SELECT * WHERE { ?s ?p ?o }")
```

**Recent Updates (2025)**:
- RDF 1.2 and SPARQL 1.2 support
- Custom aggregate functions in Rust and Python API
- oxrdflib updated November 2025 with RocksDB-based storage

**Jerry Alignment**:
- ✅ **Zero Java dependency**: Pure Rust + Python
- ✅ **Embeddable**: No separate server process required
- ✅ **Pre-installed potential**: Could be added to Jerry's stdlib-only core if distribution allows
- ✅ **Modern standards**: RDF 1.2, SPARQL 1.2, RDF*
- ✅ **Active development**: Regular updates in 2025

**Citations**: [Oxigraph GitHub](https://github.com/oxigraph/oxigraph), [pyoxigraph PyPI](https://pypi.org/project/pyoxigraph/), [pyoxigraph Documentation](https://pyoxigraph.readthedocs.io/), [oxrdflib GitHub](https://github.com/oxigraph/oxrdflib)

---

### 2. Graph Databases (Property Graphs)

Property graph databases store vertices (nodes) and edges (relationships) with properties, optimized for traversal queries.

#### 2.1 Neo4j

**What**: Native graph database with Cypher query language
**Who Maintains**: Neo4j, Inc. (commercial + community editions)
**Why Use**: Market leader, mature ecosystem, advanced graph algorithms
**When**: Complex relationship queries, fraud detection, recommendation engines
**Where**: NASA, Walmart, eBay, Airbnb
**How (Python)**: Official neo4j-driver Python library

**Key Features**:
- **Cypher query language**: Declarative, SQL-like syntax for graph patterns
- **Native graph storage**: Index-free adjacency for fast traversals
- **ACID transactions**: Full transaction support
- **Graph algorithms library**: PageRank, community detection, pathfinding
- **Visualization browser**: Built-in graph exploration UI
- **Multi-deployment**: Self-hosted, cloud (Aura), embedded

**Query Example (Cypher)**:
```cypher
MATCH (task:Task)-[:CONTAINS]->(subtask:Subtask)
WHERE task.status = 'IN_PROGRESS'
RETURN task.title, count(subtask) AS subtask_count
```

**Python Integration**:
```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
with driver.session() as session:
    result = session.run("MATCH (n:Task) RETURN n.title LIMIT 10")
    for record in result:
        print(record["n.title"])
```

**Performance**: TigerGraph edges out Neo4j in deep-link traversal benchmarks, but Neo4j performs strongly with Fabric sharding enabled.

**Tradeoffs**:
- **Pro**: Most mature, best developer experience, strong visualization, flexible deployment
- **Con**: Enterprise Edition licensing costs, Cypher not standardized (vs Gremlin)
- **Con**: Not natively TinkerPop-compatible (separate plugin required)

**Citations**: [Neo4j vs Amazon Neptune](https://www.analyticsvidhya.com/blog/2024/08/neo4j-vs-amazon-neptune/), [Best Graph Databases 2025](https://www.getgalaxy.io/learn/data-tools/best-graph-databases-2025)

---

#### 2.2 Amazon Neptune

**What**: Fully managed cloud graph database supporting Gremlin (TinkerPop) and SPARQL
**Who Maintains**: Amazon Web Services
**Why Use**: Cloud-native, dual-model (property graph + RDF), serverless scaling
**When**: AWS-integrated applications, need for both Gremlin and SPARQL
**Where**: AWS cloud deployments
**How (Python)**: gremlinpython or SPARQLWrapper over HTTP

**Key Features**:
- **Dual model**: Property graph (Gremlin) AND RDF (SPARQL) in same database
- **Compute-storage separation**: Storage auto-scales to 128 TiB, compute scales independently
- **Serverless v2**: Auto-provisions compute based on workload
- **15 read replicas**: Low-latency horizontal scaling
- **TinkerPop 3.x compatible**: Portable to other Gremlin databases
- **openCypher support**: Compatible with Neo4j workloads via Bolt/HTTPS

**Consistency Model**:
- Immediate consistency on writer instance
- Eventual consistency on read replicas

**Tradeoffs**:
- **Pro**: Fully managed, dual query language support, cloud-native scalability
- **Con**: AWS lock-in, no built-in visualization (requires SageMaker/Jupyter), costs tied to instance hours
- **Con**: Eventual consistency on replicas (not fully ACID across cluster)

**Jerry Alignment**:
- ✅ **TinkerPop compatibility**: Aligns with Jerry's Gremlin-ready design
- ❌ **Cloud dependency**: Violates Jerry's zero-dependency core principle
- 🟡 **Future migration target**: Good Phase 3 option if cloud deployment needed

**Citations**: [Amazon Neptune vs Neo4j](https://stackshare.io/stackups/amazon-neptune-vs-neo4j), [Neptune vs Neo4j Comparison](https://www.brilworks.com/blog/neptune-vs-neo4j/)

---

#### 2.3 JanusGraph

**What**: Open-source distributed graph database with pluggable storage backends
**Who Maintains**: Linux Foundation (JanusGraph community)
**Why Use**: Flexibility, horizontal scale via Cassandra/HBase/Bigtable
**When**: Need for massive scale, existing Cassandra/HBase infrastructure
**Where**: Organizations with big data infrastructure (Cassandra, Spark)
**How (Python)**: gremlinpython (TinkerPop Gremlin over websocket)

**Key Features**:
- **Pluggable backends**: Cassandra, ScyllaDB, HBase, Google Bigtable
- **Gremlin native**: Full Apache TinkerPop 3.x support
- **Infinite horizontal scale**: Runs atop distributed storage systems
- **Advanced indexing**: Elasticsearch, Solr, Lucene integration
- **Open-source**: Apache 2.0 license, no vendor lock-in

**Architecture**:
- JanusGraph is a layer over proven stores (not a standalone database)
- Brings Gremlin query capabilities to existing distributed systems
- Separates graph logic from storage persistence

**Tradeoffs**:
- **Pro**: True horizontal scaling, open-source, backend flexibility
- **Con**: Complexity of multi-component setup (JanusGraph + Cassandra + Elasticsearch)
- **Con**: Consistency model depends on backend (Cassandra = eventual consistency)
- **Con**: No built-in visualization tools

**Use Case Fit**: Ideal for organizations already using Cassandra/HBase who want graph capabilities without adopting a new storage engine.

**Citations**: [Amazon Neptune vs JanusGraph vs Neo4j](https://db-engines.com/en/system/Amazon+Neptune%3BJanusGraph%3BNeo4j), [Top JanusGraph Alternatives](https://www.puppygraph.com/blog/janusgraph-alternatives)

---

#### 2.4 ArangoDB

**What**: Multi-model database (document, graph, key-value) with AQL query language
**Who Maintains**: ArangoDB GmbH (commercial + open-source)
**Why Use**: Flexibility to mix data models, GraphQL/REST API support
**When**: Applications with diverse data types, microservices architectures
**Where**: Startups, front-end teams using GraphQL
**How (Python)**: python-arango official driver

**Key Features**:
- **Multi-model**: Document, graph, and key-value in one database
- **AQL (ArangoDB Query Language)**: Supports joins, graph traversals, full-text search
- **Foxx microservices**: Build data-centric microservices in the database
- **Full ACID transactions**: Data integrity across models
- **Cluster support**: Horizontal scaling
- **Native JSON**: Document model uses JSON natively

**Python Integration**:
```python
from arango import ArangoClient

client = ArangoClient(hosts='http://localhost:8529')
db = client.db('_system', username='root', password='password')

# Document operations
collection = db.collection('tasks')
collection.insert({'title': 'Task 1', 'status': 'pending'})

# Graph traversal (AQL)
cursor = db.aql.execute("""
    FOR v, e, p IN 1..3 OUTBOUND 'tasks/123' CONTAINS
    RETURN v
""")
```

**Tradeoffs**:
- **Pro**: Multi-model flexibility, good for startups with evolving schemas
- **Con**: Smaller community vs Neo4j, steeper learning curve for AQL
- **Con**: Documentation gaps for advanced features
- **Con**: AQL is not a standard (vendor-specific)

**Jerry Alignment**:
- 🟡 **Multi-model**: Interesting but may add complexity
- ❌ **Non-standard query language**: AQL vs standard Gremlin/SPARQL/Cypher
- 🟡 **Consideration for Phase 3**: If document + graph co-location needed

**Citations**: [ArangoDB GitHub](https://github.com/arangodb/arangodb), [First Steps with ArangoDB and Python](https://cylab.be/blog/299/first-steps-with-a-graph-database-using-python-and-arangodb), [Best Graph Databases 2025](https://www.puppygraph.com/blog/best-graph-databases)

---

### 3. Python Libraries for Knowledge Graphs

#### 3.1 kglab (Knowledge Graph Abstraction Layer) ⭐

**What**: Unified Python API for knowledge graphs across RDF, NetworkX, and Pandas
**Who Maintains**: DerwenAI (Paco Nathan)
**Why Use**: Abstraction across paradigms, integrates semantic web + graph analytics
**When**: Need to support both RDF and property graph workflows
**How**: Wraps RDFLib, NetworkX, SHACL, SPARQL in unified interface

**Key Features**:
- **RDF serialization**: Turtle, RDF/XML, JSON-LD, N-Triples
- **SPARQL execution**: Query local stores or remote endpoints
- **SHACL validation**: Schema validation for RDF graphs
- **NetworkX integration**: Graph algorithms (centrality, clustering, pathfinding)
- **Pandas export**: Convert graph data to DataFrames for analysis
- **Visualization**: Integration with PyVis, Matplotlib

**Python Example**:
```python
import kglab

# Create knowledge graph
kg = kglab.KnowledgeGraph()
kg.load_rdf("data.ttl")

# SPARQL query
sparql = """
SELECT ?s ?p ?o
WHERE { ?s ?p ?o }
LIMIT 10
"""
results = kg.query(sparql)

# Export to NetworkX
nx_graph = kg.build_nx_graph()

# Export to Pandas
df = kg.query_as_df(sparql)
```

**Jerry Alignment**:
- ✅ **Abstraction layer**: Aligns with Jerry's "Model Once, Represent Everywhere" pattern (Netflix UDA)
- ✅ **MIT license**: Open-source, compatible with Jerry
- 🟡 **Dependency tradeoff**: Adds RDFLib, NetworkX as transitive dependencies
- ✅ **Phase 2 candidate**: Could serve as abstraction over pyoxigraph + NetworkX

**Citations**: [kglab GitHub](https://github.com/DerwenAI/kglab)

---

#### 3.2 RDFLib

**What**: Pure Python library for RDF parsing, querying, and serialization
**Who Maintains**: RDFLib team (community-driven)
**Why Use**: Standard Python RDF library, no external dependencies
**When**: Working with RDF/Turtle/JSON-LD files, local SPARQL queries
**How**: Native Python API

**Key Features**:
- **Format support**: Turtle, N-Triples, N-Quads, RDF/XML, JSON-LD, TriG
- **SPARQL 1.1**: Query and update support
- **Triple stores**: In-memory, SQLite, BerkeleyDB backends
- **Namespace management**: Built-in namespace registry
- **Pure Python**: No C extensions required (though plugins can add performance)

**Python Example**:
```python
from rdflib import Graph, Namespace, URIRef, Literal

# Create graph
g = Graph()
g.parse("data.ttl", format="turtle")

# Add triples
JER = Namespace("https://jerry.dev/jer/work-tracker/")
g.add((JER['task-001'], JER['title'], Literal("Implement feature")))

# SPARQL query
results = g.query("""
    SELECT ?task ?title
    WHERE { ?task jer:title ?title }
""")

# Serialize
print(g.serialize(format="json-ld"))
```

**Tradeoffs**:
- **Pro**: Pure Python, extensive format support, SPARQL support
- **Con**: Performance slower than native stores (Oxigraph, Virtuoso)
- **Con**: SPARQL endpoint requires additional setup (Flask + custom code)

**Jerry Alignment**:
- ✅ **Pure Python**: No compilation required
- ✅ **Standard library**: De facto Python RDF standard
- 🟡 **Performance**: Adequate for small-to-medium graphs, may need Oxigraph for large datasets

**Citations**: [RDFLib Documentation](https://rdflib.dev/sparqlwrapper/), [Semantic Web standards and Python](https://www.lassila.org/publications/2025/lassila-omg-challenge-2025.pdf)

---

#### 3.3 owlready2

**What**: Python library for ontology-oriented programming with OWL/RDF support
**Who Maintains**: Jean-Baptiste Lamy (Les Fleurs du Normal)
**Why Use**: Load and manipulate OWL ontologies, reasoning via HermiT/Pellet
**When**: Working with OWL ontologies, medical terminologies (UMLS), reasoning-heavy tasks
**How**: Native Python API with optional Java reasoners

**Key Features**:
- **OWL 2.0 support**: Full ontology manipulation in Python
- **Reasoning**: HermiT and Pellet reasoners (included, requires Java)
- **Quadstore**: Optimized RDF/OWL storage backend
- **ORM capabilities**: Use as object-relational mapper for graph data
- **Medical domain**: Integrated PyMedTermino2 for UMLS
- **RDFLib integration**: Can import/export to RDFLib graphs

**Python Example**:
```python
from owlready2 import *

# Load ontology
onto = get_ontology("http://example.org/work-tracker.owl").load()

# Define classes
class Task(Thing):
    namespace = onto

class hasStatus(Task >> str):
    pass

# Create instances
task1 = Task("task-001")
task1.hasStatus = "pending"

# Reasoning
sync_reasoner_pellet(infer_property_values=True)

# Save
onto.save(file="work-tracker-inferred.owl")
```

**Performance**: Benchmarked to beat Neo4j, MongoDB, SQLObject, and SQLAlchemy as an ORM.

**Tradeoffs**:
- **Pro**: Best Python OWL library, built-in reasoning, fast quadstore
- **Con**: Reasoners require Java (HermiT, Pellet)
- **Con**: No native SPARQL support (requires RDFLib bridge)
- **Con**: LGPL v3 license (copyleft)

**Jerry Alignment**:
- 🟡 **Java dependency for reasoning**: Conflicts with zero-dependency goal
- ✅ **OWL ontology**: Useful if Jerry adopts formal ontology (Phase 3)
- ❌ **LGPL license**: May require careful integration to avoid copyleft issues

**Citations**: [owlready2 PyPI](https://pypi.org/project/owlready2/), [owlready2 Documentation](https://www.lesfleursdunormal.fr/static/informatique/owlready/index_en.html)

---

#### 3.4 PyKEEN (Python Knowledge Embeddings)

**What**: Library for training and evaluating knowledge graph embedding models
**Who Maintains**: PyKEEN team (academic/research-driven)
**Why Use**: Machine learning on knowledge graphs, link prediction, entity alignment
**When**: Research, recommendation systems, graph completion tasks
**How**: PyTorch-based embedding model training

**Key Features**:
- **Embedding models**: TransE, DistMult, ComplEx, RotatE, ConvE, and 30+ others
- **Evaluation**: Ranking metrics (MRR, Hits@K)
- **Hyperparameter optimization**: Integration with Optuna
- **Training pipelines**: End-to-end workflows for KG embeddings
- **Interoperability**: Works with PyG (PyTorch Geometric)

**Use Case Example**:
- **Link prediction**: Given (Task, DEPENDS_ON, ?) predict missing dependencies
- **Entity alignment**: Match entities across different knowledge graphs
- **Recommendation**: Recommend related tasks based on graph structure

**Jerry Alignment**:
- 🟡 **ML/AI future use**: Not immediate need, but could enhance recommendations
- ❌ **PyTorch dependency**: Large dependency footprint
- 🟡 **Phase 4+**: Consider for intelligent task suggestions

**Citations**: [semantic-python-overview](https://github.com/pysemtec/semantic-python-overview)

---

#### 3.5 pyoxigraph (Covered in Section 1.4)

See Triple Stores > Oxigraph for full details.

---

### 4. Visualization Tools

#### 4.1 Gephi (Desktop Application)

**What**: "Photoshop of graph visualization" - desktop app for network analysis
**Who Maintains**: Gephi Consortium (open-source)
**Why Use**: Advanced graph analytics, publication-quality visualizations
**When**: Exploratory data analysis, research, generating static diagrams
**Where**: 10,000+ peer-reviewed publications, academic research

**Key Features**:
- **Real-time manipulation**: Filter, cluster, layout in real-time
- **Algorithms**: Modularity detection, PageRank, betweenness centrality
- **Layouts**: Force-directed (ForceAtlas2), hierarchical, circular
- **Export**: PNG, SVG, PDF
- **Gephi Lite**: Web-based version (2025)

**Python Integration**: Export NetworkX graphs to Gephi format (GEXF)
```python
import networkx as nx
G = nx.DiGraph()
G.add_edge("Task-001", "Subtask-001")
nx.write_gexf(G, "graph.gexf")
# Open graph.gexf in Gephi
```

**Tradeoffs**:
- **Pro**: Powerful desktop tool, excellent for analysis
- **Con**: Desktop application (not embeddable), no web interactivity
- **Con**: Requires manual export/import workflow from Python

**Jerry Alignment**:
- 🟡 **Desktop tool**: Useful for development/debugging, not production
- 🟡 **Workflow**: Export Jerry graph to GEXF for visualization

**Citations**: [Gephi](https://gephi.org/), [Graph Visualization Tools Comparison](https://memgraph.com/blog/you-want-a-fast-easy-to-use-and-popular-graph-visualization-tool)

---

#### 4.2 Graphviz (DOT Language)

**What**: Text-based graph description language with automatic layout
**Who Maintains**: AT&T Research, open-source community
**Why Use**: Simple syntax, reliable layouts, static diagram generation
**When**: Documentation, architecture diagrams, simple visualizations
**Where**: Ubiquitous in software engineering (UML, dependency graphs)

**Key Features**:
- **DOT language**: Plain text graph specification
- **Layout engines**: dot (hierarchical), neato (spring), fdp (force), circo (circular)
- **Output formats**: PNG, SVG, PDF, PostScript
- **Python binding**: graphviz package

**Python Example**:
```python
from graphviz import Digraph

dot = Digraph(comment='Jerry Work Tracker')
dot.node('PLAN-001', 'Plan: Q1 Goals')
dot.node('PHASE-001', 'Phase 1: Setup')
dot.edge('PLAN-001', 'PHASE-001', label='CONTAINS')

dot.render('work-tracker.gv', format='svg', view=True)
```

**Tradeoffs**:
- **Pro**: Simple, reliable, great for static diagrams
- **Con**: No interactivity, limited styling vs modern libraries
- **Con**: DOT syntax learning curve for complex graphs

**Jerry Alignment**:
- ✅ **Documentation**: Good for generating docs/diagrams/ visualizations
- 🟡 **Static output**: Not suitable for interactive web presentations
- ✅ **Lightweight**: Minimal dependencies

**Citations**: [Graphviz](https://graphviz.org/), [External Resources](https://graphviz.org/resources/)

---

#### 4.3 Cytoscape / Cytoscape.js ⭐

**What**: Open-source network visualization platform (desktop + JavaScript library)
**Who Maintains**: Cytoscape Consortium (desktop), Max Franz (Cytoscape.js)
**Why Use**: Interactive web visualizations, bioinformatics standard
**When**: Web applications, scientific visualization, interactive exploration
**Where**: Biology, social networks, knowledge graphs

**Key Features (Cytoscape.js)**:
- **JavaScript library**: Embeddable in web applications
- **Flexible layouts**: Force-directed, hierarchical, circular, grid, custom
- **Event handling**: Click, hover, drag interactions
- **Styling**: CSS-like syntax for node/edge appearance
- **Extensions**: Plugins for additional layouts and features
- **Framework agnostic**: Works with React, Vue, vanilla JS

**Python Integration (Dash Cytoscape)**:
```python
import dash
import dash_cytoscape as cyto

app = dash.Dash(__name__)

elements = [
    {'data': {'id': 'task-001', 'label': 'Implement feature'}},
    {'data': {'id': 'subtask-001', 'label': 'Write tests'}},
    {'data': {'source': 'task-001', 'target': 'subtask-001'}}
]

app.layout = cyto.Cytoscape(
    id='cytoscape',
    elements=elements,
    layout={'name': 'breadthfirst'},
    style={'width': '100%', 'height': '600px'}
)
```

**Tradeoffs**:
- **Pro**: Rich interactivity, web-native, extensive customization
- **Con**: Requires JavaScript for web deployment
- **Con**: Performance limits around 100k nodes (use Cosmos for larger)

**Jerry Alignment**:
- ✅ **Web presentation**: Ideal for Jerry web UI (Phase 3)
- ✅ **Dash integration**: Python backend → Cytoscape.js frontend
- ✅ **Interactive exploration**: Users can navigate knowledge graph visually

**Citations**: [Cytoscape](https://cytoscape.org/), [Dash Cytoscape](https://github.com/pysemtec/semantic-python-overview), [Top 7 Graph Visualization Tools](https://www.marktechpost.com/2024/11/16/top-7-graph-database-visualization-tools/)

---

#### 4.4 NetworkX (Python Graph Algorithms)

**What**: Pure Python library for graph creation, manipulation, and analysis
**Who Maintains**: NetworkX Developers (BSD license)
**Why Use**: Standard Python graph library, extensive algorithm collection
**When**: Graph algorithms, analysis, integration with Python data science stack
**Where**: Academia, data science, network analysis

**Key Features**:
- **Graph types**: Directed, undirected, multigraph, weighted
- **Algorithms**: Shortest path, centrality, community detection, flow
- **I/O**: GEXF, GraphML, JSON, Pickle, Pajek
- **Visualization**: Integration with Matplotlib, PyVis
- **Pure Python**: No compilation required

**Python Example**:
```python
import networkx as nx
import matplotlib.pyplot as plt

# Build graph
G = nx.DiGraph()
G.add_edge("PLAN-001", "PHASE-001", relationship="CONTAINS")
G.add_edge("PHASE-001", "TASK-001", relationship="CONTAINS")

# Algorithms
shortest_path = nx.shortest_path(G, "PLAN-001", "TASK-001")
centrality = nx.betweenness_centrality(G)

# Visualize
nx.draw(G, with_labels=True)
plt.show()
```

**Integration with Jerry**:
- **Convert Jerry graph to NetworkX**: Export vertices/edges to nx.DiGraph
- **Run algorithms**: Centrality (identify critical tasks), path analysis
- **Export to visualization**: GEXF for Gephi, JSON for Cytoscape.js

**Jerry Alignment**:
- ✅ **Pure Python**: No external dependencies
- ✅ **Algorithm library**: Useful for progress calculation, dependency analysis
- ✅ **Integration**: Works with Matplotlib, kglab, Gephi

**Citations**: [Graph Visualization Tools](https://memgraph.com/blog/you-want-a-fast-easy-to-use-and-popular-graph-visualization-tool)

---

### 5. Query Engines and Endpoints

#### 5.1 SPARQL Endpoints (SPARQLWrapper)

**What**: Python wrapper for remote SPARQL query execution
**Who Maintains**: RDFLib team
**Why Use**: Query remote knowledge graphs (DBpedia, Wikidata, custom endpoints)
**When**: Federated queries, accessing public knowledge graphs
**How**: HTTP client wrapper around SPARQL Protocol

**Key Features**:
- **Return formats**: JSON, XML, Turtle, CSV, TSV, JSON-LD
- **Authentication**: HTTP Basic/Digest
- **Update support**: SPARQL UPDATE queries (INSERT, DELETE)
- **Pandas integration**: sparql-dataframe for DataFrame conversion

**Python Example**:
```python
from SPARQLWrapper import SPARQLWrapper, JSON

# Query DBpedia
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)
sparql.setQuery("""
    SELECT ?label
    WHERE { <http://dbpedia.org/resource/Python_(programming_language)>
            rdfs:label ?label }
    FILTER (lang(?label) = 'en')
""")

results = sparql.queryAndConvert()
for result in results["results"]["bindings"]:
    print(result["label"]["value"])
```

**Setting Up Local SPARQL Endpoint (Flask)**:
```python
from flask import Flask, request
from rdflib import Graph

app = Flask(__name__)
g = Graph()
g.parse("data.ttl")

@app.route('/sparql', methods=['GET', 'POST'])
def sparql_endpoint():
    query = request.args.get('query') or request.form.get('query')
    results = g.query(query)
    return results.serialize(format='json')

app.run(port=3030)
```

**Jerry Alignment**:
- ✅ **Phase 3**: Expose Jerry knowledge graph as SPARQL endpoint
- ✅ **Federated queries**: Link Jerry data to external KGs (DBpedia, Wikidata)
- 🟡 **Requires Flask**: Adds web framework dependency

**Citations**: [SPARQLWrapper Documentation](https://sparqlwrapper.readthedocs.io/), [SPARQLWrapper GitHub](https://github.com/RDFLib/sparqlwrapper)

---

#### 5.2 Gremlin Servers (TinkerPop)

**What**: Graph traversal execution engine for Apache TinkerPop
**Who Maintains**: Apache TinkerPop project
**Why Use**: Remote execution of Gremlin queries, multi-language support
**When**: Distributed graph traversals, JVM-based graph databases
**Where**: JanusGraph, Amazon Neptune, Azure Cosmos DB

**Key Features**:
- **WebSocket/HTTP protocols**: Remote query execution
- **gremlinpython**: Python driver for Gremlin Server
- **GraphSON serialization**: JSON-based result format
- **Multi-language support**: Python, JavaScript, Java, .NET, Go

**Python Example (gremlinpython)**:
```python
from gremlin_python.driver import client, serializer

# Connect to Gremlin Server
gremlin_client = client.Client(
    'ws://localhost:8182/gremlin',
    'g',
    message_serializer=serializer.GraphSONSerializersV3d0()
)

# Execute traversal
results = gremlin_client.submit(
    "g.V().has('Task', 'id', 'TASK-001').out('CONTAINS').values('title')"
).all().result()

for result in results:
    print(result)
```

**GraphSON Formats** (covered in Section 6):
- **GraphSON 1.0**: Basic JSON serialization
- **GraphSON 2.0**: Type-aware with @typeId/@value
- **GraphSON 3.0**: Explicit Map/List/Set support (default)
- **GraphSON 4.0**: TinkerPop 4.0 format

**Jerry Alignment**:
- 🟡 **Phase 3+**: If migrating to JanusGraph or Neptune
- ❌ **Requires server**: Adds infrastructure complexity
- 🟡 **TinkerPop compatibility**: Good if targeting Gremlin ecosystem

**Citations**: [TinkerPop](https://tinkerpop.apache.org/), [IO Reference](https://tinkerpop.apache.org/docs/3.4.1/dev/io/)

---

### 6. Serialization Formats

#### 6.1 GraphSON (TinkerPop)

**What**: JSON-based serialization format for property graphs
**Who Maintains**: Apache TinkerPop
**Why Use**: Portable property graph exchange, Gremlin Server communication
**When**: Exporting to TinkerPop-compatible systems (Neptune, JanusGraph)

**Format Evolution**:

**GraphSON 1.0** (TinkerPop 3.0.0):
- Basic JSON with optional type embedding
- `@class` field for Java type information
- Lossy without type embedding (float → double)

**GraphSON 2.0** (TinkerPop 3.2.2):
- `@typeId` and `@value` structure
- Namespace:typename format (e.g., "g:Int64")
- Less Jackson-dependent, more language-agnostic

**GraphSON 3.0** (TinkerPop 3.3.0, default):
- Explicit Map, List, Set types
- Null, Timestamp, UUID support
- Improved Gremlin collection semantics

**GraphSON 4.0** (TinkerPop 4.0.0):
- MIME type: `application/vnd.gremlin-v4.0+json`
- Latest standard for TinkerPop 4.x

**Example (GraphSON 3.0)**:
```json
{
  "@type": "g:Vertex",
  "@value": {
    "id": {"@type": "g:UUID", "@value": "TASK-001"},
    "label": "Task",
    "properties": {
      "title": [{"@type": "g:VertexProperty", "@value": {
        "id": {"@type": "g:UUID", "@value": "prop-001"},
        "value": "Implement feature",
        "label": "title"
      }}]
    }
  }
}
```

**Tradeoffs**:
- **Pro**: Standard format for TinkerPop ecosystem
- **Con**: Verbose compared to RDF Turtle
- **Con**: Not human-friendly for hand editing

**Jerry Alignment**:
- ✅ **Phase 3**: If targeting Neptune/JanusGraph
- 🟡 **Export format**: Good for graph database migration
- ❌ **Primary storage**: Too verbose for Jerry's file-based storage

**Citations**: [GraphSON Reader/Writer](https://github.com/tinkerpop/blueprints/wiki/GraphSON-Reader-and-Writer-Library), [Oracle GraphSON Format](https://docs.oracle.com/en/database/oracle/property-graph/21.1/spgdg/graphson-data-format.html), [TinkerPop IO Reference](https://tinkerpop.apache.org/docs/3.4.1/dev/io/)

---

#### 6.2 RDF Serializations (Turtle, JSON-LD, etc.)

**What**: Standard formats for RDF triple/quad serialization
**Who Maintains**: W3C
**Why Use**: Interoperability with semantic web tools, human-readable (Turtle)
**When**: Working with RDF data, publishing linked data

**Format Comparison**:

| Format | Readability | Compactness | Use Case |
|--------|-------------|-------------|----------|
| **Turtle** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Human editing, documentation |
| **N-Triples** | ⭐⭐⭐ | ⭐⭐⭐ | Machine processing, streaming |
| **RDF/XML** | ⭐⭐ | ⭐⭐ | Legacy systems, XML pipelines |
| **JSON-LD** | ⭐⭐⭐⭐ | ⭐⭐⭐ | Web APIs, JavaScript integration |
| **TriG** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Named graphs (quads), datasets |

**Turtle Example**:
```turtle
@prefix jer: <https://jerry.dev/jer/work-tracker/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

jer:task-001 a jer:Task ;
    jer:title "Implement feature" ;
    jer:status "pending" ;
    jer:contains jer:subtask-001 .

jer:subtask-001 a jer:Subtask ;
    jer:title "Write tests" .
```

**JSON-LD Example**:
```json
{
  "@context": {
    "jer": "https://jerry.dev/jer/work-tracker/",
    "title": "jer:title",
    "status": "jer:status"
  },
  "@id": "jer:task-001",
  "@type": "jer:Task",
  "title": "Implement feature",
  "status": "pending"
}
```

**Jerry Alignment**:
- ✅ **Turtle**: Excellent for human-readable storage (Phase 2)
- ✅ **JSON-LD**: Good for web APIs (Phase 3)
- 🟡 **TriG**: Useful if Jerry adopts named graphs

**Citations**: [RDFLib](https://rdflib.dev/sparqlwrapper/)

---

### 7. Embedded vs Server-Based Tradeoffs

| Criterion | Embedded (Oxigraph, SQLite) | Server-Based (Jena, Neo4j, Neptune) |
|-----------|----------------------------|-------------------------------------|
| **Deployment** | Single-process, no setup | Requires server infrastructure |
| **Latency** | Minimal (direct API) | Network overhead (REST/WebSocket) |
| **Scalability** | Limited to single machine | Horizontal scaling, clustering |
| **Consistency** | ACID (single-writer) | Configurable (ACID or eventual) |
| **Dependencies** | Embeddable library only | Server process + client driver |
| **Use Cases** | Desktop apps, embedded systems, small-to-medium graphs | Web services, multi-user, trillion-scale graphs |
| **Jerry Alignment** | ✅ Phase 1-2 (zero-dependency) | 🟡 Phase 3+ (cloud deployment) |

**Key Insights**:

1. **Embedded for Jerry Core**: Oxigraph (embedded) aligns with Jerry's zero-dependency philosophy and supports Phase 1-2 development without infrastructure.

2. **Server for Scale**: If Jerry needs to support multi-user environments or trillion-scale graphs, server-based solutions (Fuseki, Neptune) become necessary.

3. **Hybrid Strategy**: Start embedded (pyoxigraph), expose SPARQL endpoint (Flask), migrate to Fuseki if scale demands.

4. **Performance vs Simplicity**:
   - Embedded: Lower latency (direct API), simpler deployment
   - Server: Better for distributed workloads, but adds complexity

**Citations**: [Property Graph vs RDF Triple Store](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0144578), [Graph Database vs Triple Store](https://community.openlinksw.com/t/what-are-the-differences-between-a-graph-database-and-a-triple-store/88)

---

## L2: Strategic Implications for Jerry Framework

### 1. Recommended Technology Stack

#### Phase 1: Foundation (Current)
- **Data Model**: Property graph abstractions (Vertex, Edge, VertexProperty)
- **Storage**: File-based JSON (existing TOON format)
- **Query**: Repository pattern with Python traversal
- **Visualization**: NetworkX + Matplotlib (development only)

**Status**: ✅ Complete (per GRAPH_DATA_MODEL_ANALYSIS.md)

---

#### Phase 2: Semantic Layer (Recommended Next)
- **Triple Store**: pyoxigraph (embedded RDF storage)
- **Abstraction**: kglab (unified API across RDF + NetworkX)
- **Serialization**: Turtle (human-readable), JSON-LD (web-ready)
- **Query**: SPARQL via pyoxigraph + RDFLib
- **Visualization**: Export to Gephi (GEXF) for analysis

**Why**:
- **Zero Java**: pyoxigraph is Rust-based, no JVM dependency
- **Embeddable**: No server infrastructure required
- **Standards-aligned**: RDF 1.2, SPARQL 1.2, RDF* (meta-properties)
- **Performance**: RocksDB backend for disk-based storage

**Migration Path**:
```python
# Jerry domain model → RDF (via adapter)
from pyoxigraph import Store
from jerry.domain.entities import Task

store = Store("jerry-data.db")

# Convert Task to RDF triples
task = Task.load("TASK-001")
store.add((
    URIRef("jer:task-001"),
    URIRef("jer:title"),
    Literal(task.title)
))

# SPARQL query
results = store.query("""
    SELECT ?task ?title
    WHERE { ?task jer:title ?title }
""")
```

---

#### Phase 3: Web Presentation
- **SPARQL Endpoint**: Flask + pyoxigraph (expose HTTP API)
- **Visualization**: Cytoscape.js (interactive web graphs)
- **API**: REST API serving GraphSON or JSON-LD
- **Optional**: Gremlin compatibility layer (if targeting Neptune migration)

**Why**:
- **Web-native**: Flask is lightweight, Python-standard
- **Interactive**: Cytoscape.js provides rich user exploration
- **Federated queries**: Link Jerry data to DBpedia, Wikidata via SPARQL

**Architecture**:
```
┌─────────────────────────────────────────────┐
│          Web UI (Cytoscape.js)              │
│  - Interactive graph visualization          │
│  - Node/edge filtering, layout              │
└────────────────┬────────────────────────────┘
                 │ HTTP/JSON-LD
┌────────────────▼────────────────────────────┐
│          Flask REST API                      │
│  - /sparql (SPARQL endpoint)                │
│  - /graph (GraphSON export)                 │
│  - /rdf (Turtle/JSON-LD export)             │
└────────────────┬────────────────────────────┘
                 │ Python API
┌────────────────▼────────────────────────────┐
│       pyoxigraph (Embedded Store)           │
│  - RDF triples persistence                  │
│  - SPARQL query execution                   │
└────────────────┬────────────────────────────┘
                 │ Adapter
┌────────────────▼────────────────────────────┐
│      Jerry Domain Model (Vertices/Edges)    │
│  - Property graph abstractions              │
│  - DDD aggregates, event sourcing           │
└─────────────────────────────────────────────┘
```

---

#### Phase 4: Scale (Optional)
- **Cloud Migration**: Amazon Neptune (if AWS-hosted) or self-hosted Jena Fuseki
- **Graph DB**: Neo4j (if Cypher preferred) or JanusGraph (if Cassandra available)
- **Visualization**: Gephi, Cosmos (for 100k+ nodes)

**Decision Criteria**:
- **Stay embedded** if: Single-user, desktop application, < 10M triples
- **Migrate to server** if: Multi-user, cloud deployment, > 10M triples, need clustering

---

### 2. Alignment with Jerry Principles

#### Hexagonal Architecture
- **Domain Layer**: Vertex/Edge primitives (no external dependencies) ✅
- **Ports**: IGraphRepository, IRDFStore (abstract interfaces) ✅
- **Adapters**:
  - File adapter (JSON/TOON) ✅
  - pyoxigraph adapter (RDF) ⭐ Recommended
  - Fuseki adapter (future, if needed)

#### Zero-Dependency Core
- **Domain**: Pure Python, stdlib only ✅
- **Infrastructure**: pyoxigraph (Rust + Python bindings, pre-compiled wheels)
  - **Tradeoff**: Not stdlib, but pre-installed wheels ≈ zero setup
  - **Alternative**: RDFLib (pure Python, but slower)

#### CQRS Pattern
- **Commands**: Write triples to pyoxigraph (persist domain events)
- **Queries**: SPARQL SELECT for read models
- **Event Sourcing**: CloudEvents as RDF triples (EMITTED edges)

---

### 3. Tradeoff Analysis: Embedded RDF vs Server-Based

| Aspect | Embedded (pyoxigraph + RDFLib) | Server (Jena Fuseki, Neo4j) |
|--------|-------------------------------|------------------------------|
| **Setup** | `pip install pyoxigraph` | Docker/systemd service, config |
| **Performance** | Fast for < 10M triples | Optimized for billions of triples |
| **SPARQL** | Local execution | HTTP endpoint (federated queries) |
| **Dependencies** | Python package only | Server process + monitoring |
| **Scalability** | Single machine | Distributed, clustered |
| **Jerry Fit** | ✅ Phase 1-3 | 🟡 Phase 4+ (if cloud) |

**Recommendation**: Start with pyoxigraph (embedded) for Phase 2, defer server-based decision until user demand validates need for scale.

---

### 4. Netflix UDA Pattern Application

From GRAPH_DATA_MODEL_ANALYSIS.md Section 11 (DISC-064):

> "Model Once, Represent Everywhere" - Single domain model → multiple projections (GraphQL, Avro, SQL, RDF)

**Jerry Implementation**:
1. **Canonical Model**: Domain entities (Task, Phase, Plan) as Vertex/Edge
2. **Representations**:
   - JSON/TOON (file storage)
   - RDF Turtle (semantic web export)
   - JSON-LD (web API)
   - GraphSON (TinkerPop export)
   - Cytoscape.js JSON (visualization)

**Adapter Pattern**:
```python
# src/infrastructure/persistence/rdf_adapter.py

from pyoxigraph import Store, NamedNode, Literal
from jerry.domain.entities import Task

class RDFAdapter:
    def __init__(self, store: Store):
        self.store = store

    def save_task(self, task: Task):
        """Convert Task domain entity to RDF triples."""
        task_uri = NamedNode(f"jer:task:{task.id.value}")

        self.store.add((
            task_uri,
            NamedNode("rdf:type"),
            NamedNode("jer:Task")
        ))

        self.store.add((
            task_uri,
            NamedNode("jer:title"),
            Literal(task.title)
        ))

        self.store.add((
            task_uri,
            NamedNode("jer:status"),
            Literal(task.status.value)
        ))

    def load_task(self, task_id: str) -> Task:
        """Query RDF store and reconstruct Task domain entity."""
        results = self.store.query(f"""
            SELECT ?title ?status
            WHERE {{
                jer:task:{task_id} jer:title ?title ;
                                   jer:status ?status .
            }}
        """)
        # Reconstruct Task from SPARQL results
        return Task(id=task_id, title=..., status=...)
```

---

### 5. Semantic Web Alignment (RDF/OWL)

From GRAPH_DATA_MODEL_ANALYSIS.md Section 11 (AN.Q.2):

| Property Graph | RDF/OWL | Jerry Strategy |
|----------------|---------|----------------|
| Edge properties | Requires RDF* or reification | Use RDF* (pyoxigraph supports it) |
| Schema | Implicit | Define OWL ontology (Phase 3) |
| URIs | Jerry URI scheme (SPEC-001) | Already RDF-compatible ✅ |
| Inference | None | Layer on via owlready2 (Phase 4) |

**Example RDF* for Edge Properties**:
```turtle
# Standard RDF (no edge properties)
jer:task-001 jer:contains jer:subtask-001 .

# RDF* (edge with properties)
<<jer:task-001 jer:contains jer:subtask-001>> jer:sequence 1 .
```

pyoxigraph supports RDF*, so Jerry can model edge properties without reification complexity.

---

### 6. Key Discoveries Informing Jerry Design

| Discovery | Source | Jerry Application |
|-----------|--------|-------------------|
| **Oxigraph as embedded RDF store** | pyoxigraph 2025 | Use for Phase 2 semantic layer |
| **kglab abstraction layer** | DerwenAI | Bridge RDF + NetworkX + Pandas |
| **RDF* for edge properties** | W3C, pyoxigraph | Model CONTAINS(sequence=1) without reification |
| **Gephi for exploration** | 10k+ citations | Export to GEXF for graph analysis |
| **Cytoscape.js for web** | Dash Cytoscape | Interactive web presentation (Phase 3) |
| **SPARQLWrapper for endpoints** | RDFLib team | Expose Jerry as SPARQL service |
| **Netflix UDA pattern** | GRAPH_DATA_MODEL_ANALYSIS | Validates "Model Once, Represent Everywhere" |

---

### 7. Recommended Roadmap

**Q1 2026 (Phase 2 Foundation)**:
1. Install pyoxigraph (`pip install pyoxigraph`)
2. Create RDFAdapter in `src/infrastructure/persistence/rdf_adapter.py`
3. Define Jerry ontology in Turtle (`docs/ontology/jerry-work-tracker.ttl`)
4. Implement domain entity → RDF triple conversion
5. Test SPARQL queries against embedded store

**Q2 2026 (Phase 2 Completion)**:
1. Integrate kglab for abstraction layer
2. Add NetworkX export for graph algorithms
3. Export to Gephi (GEXF) for visualization testing
4. Document RDF export format in `docs/specifications/`

**Q3 2026 (Phase 3 Web)**:
1. Create Flask SPARQL endpoint (`/sparql`)
2. Add JSON-LD API (`/rdf`, `/graph`)
3. Build Cytoscape.js web UI prototype
4. Test federated queries to DBpedia

**Q4 2026 (Phase 3 Refinement)**:
1. Performance testing (how many triples before slow?)
2. Decide: Stay embedded or migrate to Fuseki?
3. If scale needed, evaluate Neptune (cloud) vs Fuseki (self-hosted)
4. Production deployment of web UI

---

## Tool Comparison Matrix

### Triple Stores

| Tool | License | Python Support | Embedding | SPARQL | RDF* | Performance | Jerry Fit |
|------|---------|----------------|-----------|--------|------|-------------|-----------|
| **Oxigraph** | MIT/Apache-2.0 | ✅ pyoxigraph | ✅ Native | ✅ 1.2 | ✅ | Fast (RocksDB) | ⭐⭐⭐⭐⭐ |
| **RDFLib** | BSD-3 | ✅ Native | ✅ Native | ✅ 1.1 | ❌ | Slower | ⭐⭐⭐⭐ |
| **Jena/Fuseki** | Apache-2.0 | 🟡 HTTP/SPARQL | ❌ Server | ✅ 1.1 | 🟡 | Very Fast | ⭐⭐⭐ |
| **Virtuoso** | GPL/Commercial | 🟡 HTTP/SPARQL | ❌ Server | ✅ 1.1 | ❌ | Fastest | ⭐⭐ |
| **Blazegraph** | GPL v2 | 🟡 HTTP/SPARQL | 🟡 Java JAR | ✅ 1.1 | ❌ | Fast | ⭐⭐ |

**Legend**: ✅ Full support | 🟡 Partial/workaround | ❌ Not supported

---

### Graph Databases (Property Graphs)

| Tool | License | Python Support | Embedding | Query Language | ACID | Cloud | Jerry Fit |
|------|---------|----------------|-----------|----------------|------|-------|-----------|
| **Neo4j** | GPL/Commercial | ✅ neo4j-driver | 🟡 Java JAR | Cypher | ✅ | Aura | ⭐⭐⭐ |
| **Neptune** | Proprietary | ✅ gremlinpython | ❌ AWS only | Gremlin/SPARQL | 🟡 Eventual | ✅ | ⭐⭐ |
| **JanusGraph** | Apache-2.0 | ✅ gremlinpython | ❌ Server | Gremlin | 🟡 Backend | 🟡 | ⭐⭐ |
| **ArangoDB** | Apache-2.0 | ✅ python-arango | 🟡 Single mode | AQL | ✅ | 🟡 | ⭐⭐ |

---

### Python Libraries

| Library | Purpose | License | Dependencies | Jerry Phase |
|---------|---------|---------|--------------|-------------|
| **pyoxigraph** | Embedded RDF store | MIT/Apache-2.0 | Rust (pre-compiled) | ⭐ Phase 2 |
| **RDFLib** | RDF parsing/querying | BSD-3 | Pure Python | ⭐ Phase 2 |
| **kglab** | KG abstraction layer | MIT | RDFLib, NetworkX | ⭐ Phase 2 |
| **owlready2** | OWL ontology work | LGPL v3 | Java (reasoning) | 🟡 Phase 3+ |
| **SPARQLWrapper** | SPARQL endpoints | W3C | Pure Python | ⭐ Phase 3 |
| **NetworkX** | Graph algorithms | BSD-3 | Pure Python | ⭐ Phase 1-3 |
| **PyKEEN** | KG embeddings | MIT | PyTorch | 🟡 Phase 4+ |

---

### Visualization Tools

| Tool | Type | Python API | Web Interactive | Best For | Jerry Phase |
|------|------|------------|-----------------|----------|-------------|
| **Gephi** | Desktop | Export only (GEXF) | ❌ | Analysis, publication | 🟡 Dev only |
| **Graphviz** | CLI/Library | ✅ graphviz | ❌ | Static diagrams, docs | ⭐ Phase 1-3 |
| **Cytoscape.js** | JavaScript | ✅ Dash Cytoscape | ✅ | Web applications | ⭐ Phase 3 |
| **NetworkX** | Python | ✅ Native | 🟡 Matplotlib | Python integration | ⭐ Phase 1-2 |
| **PyVis** | Python | ✅ Native | ✅ | Quick web graphs | 🟡 Prototyping |

---

## Sources

### Triple Stores
- [Apache Jena](https://jena.apache.org/)
- [Accelerated Parallel RDF Loading with Jena](https://medium.com/@deepakpatwal/accelerated-parallel-rdf-loading-import-millions-of-triples-from-multiple-datasets-using-the-c49a3a6eba37)
- [Comparing Linked Data Triplestores](https://medium.com/wallscope/comparing-linked-data-triplestores-ebfac8c3ad4f)
- [Wikimedia Virtuoso Evaluation](https://phabricator.wikimedia.org/T206561)
- [Blazegraph vs Virtuoso Comparison](https://db-engines.com/en/system/Blazegraph%3BVirtuoso)
- [Oxigraph GitHub](https://github.com/oxigraph/oxigraph)
- [pyoxigraph PyPI](https://pypi.org/project/pyoxigraph/)
- [pyoxigraph Documentation](https://pyoxigraph.readthedocs.io/)
- [oxrdflib GitHub](https://github.com/oxigraph/oxrdflib)

### Graph Databases
- [Neo4j vs Amazon Neptune](https://www.analyticsvidhya.com/blog/2024/08/neo4j-vs-amazon-neptune/)
- [Best Graph Databases 2025](https://www.getgalaxy.io/learn/data-tools/best-graph-databases-2025)
- [Amazon Neptune vs JanusGraph vs Neo4j](https://db-engines.com/en/system/Amazon+Neptune%3BJanusGraph%3BNeo4j)
- [Neptune vs Neo4j Comparison](https://www.brilworks.com/blog/neptune-vs-neo4j/)
- [Top JanusGraph Alternatives](https://www.puppygraph.com/blog/janusgraph-alternatives)
- [ArangoDB GitHub](https://github.com/arangodb/arangodb)
- [First Steps with ArangoDB and Python](https://cylab.be/blog/299/first-steps-with-a-graph-database-using-python-and-arangodb)

### Python Libraries
- [kglab GitHub](https://github.com/DerwenAI/kglab)
- [RDFLib Documentation](https://rdflib.dev/sparqlwrapper/)
- [owlready2 PyPI](https://pypi.org/project/owlready2/)
- [owlready2 Documentation](https://www.lesfleursdunormal.fr/static/informatique/owlready/index_en.html)
- [Semantic Python Overview](https://github.com/pysemtec/semantic-python-overview)
- [Semantic Web Standards and Python](https://www.lassila.org/publications/2025/lassila-omg-challenge-2025.pdf)

### Visualization
- [Gephi](https://gephi.org/)
- [Graph Visualization Tools Comparison](https://memgraph.com/blog/you-want-a-fast-easy-to-use-and-popular-graph-visualization-tool)
- [Graphviz](https://graphviz.org/)
- [Cytoscape](https://cytoscape.org/)
- [Top 7 Graph Visualization Tools](https://www.marktechpost.com/2024/11/16/top-7-graph-database-visualization-tools/)

### Query Engines & Serialization
- [SPARQLWrapper Documentation](https://sparqlwrapper.readthedocs.io/)
- [SPARQLWrapper GitHub](https://github.com/RDFLib/sparqlwrapper)
- [TinkerPop](https://tinkerpop.apache.org/)
- [GraphSON Reader/Writer](https://github.com/tinkerpop/blueprints/wiki/GraphSON-Reader-and-Writer-Library)
- [Oracle GraphSON Format](https://docs.oracle.com/en/database/oracle/property-graph/21.1/spgdg/graphson-data-format.html)
- [TinkerPop IO Reference](https://tinkerpop.apache.org/docs/3.4.1/dev/io/)

### General
- [Property Graph vs RDF Triple Store](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0144578)
- [Graph Database vs Triple Store](https://community.openlinksw.com/t/what-are-the-differences-between-a-graph-database-and-a-triple-store/88)
- [Knowledge Graph Ecosystem Survey](https://www.kyvosinsights.com/blog/survey-of-the-knowledge-graph-ecosystem/)
- [Semantic Web and AI](https://www.dataversity.net/articles/semantic-web-and-ai-empowering-knowledge-graphs-for-smarter-applications/)

---

## 5W1H Framework Summary

### What
Technologies surveyed: 4 triple stores (Oxigraph ⭐, Jena, Virtuoso, Blazegraph), 4 graph databases (Neo4j, Neptune, JanusGraph, ArangoDB), 7 Python libraries, 5 visualization tools, 2 query engine types, multiple serialization formats.

### Why
To enable Jerry to:
1. Store knowledge graphs efficiently (embedded or server-based)
2. Query semantic data (SPARQL, Gremlin)
3. Visualize relationships interactively (web + desktop)
4. Export to standard formats (RDF, GraphSON)
5. Integrate with semantic web (RDF/OWL alignment)

### Who
- **Maintainers**: Open-source communities (Apache, W3C), commercial vendors (Neo4j, AWS), research groups
- **Jerry Users**: Future use cases include agents querying knowledge graph, web UI exploration, federated queries to external KGs

### When
- **Phase 1** (Complete): Property graph abstractions, file storage
- **Phase 2** (Recommended): Embedded RDF (pyoxigraph), SPARQL queries
- **Phase 3** (Web): SPARQL endpoint, Cytoscape.js visualization
- **Phase 4** (Scale): Server-based migration if needed (Fuseki, Neptune)

### Where
- **Embedded**: pyoxigraph (in-process, RocksDB files)
- **Server**: Jena Fuseki (self-hosted), Neptune (AWS cloud)
- **Visualization**: Gephi (desktop), Cytoscape.js (web browser)

### How
1. **Install**: `pip install pyoxigraph rdflib kglab`
2. **Adapt**: Create RDFAdapter to convert Jerry entities → RDF triples
3. **Query**: Use SPARQL for semantic queries
4. **Visualize**: Export to GEXF (Gephi) or Cytoscape.js JSON
5. **Expose**: Flask endpoint for SPARQL HTTP API

---

## Validation Checklist

| Category | Status |
|----------|--------|
| **5W1H Coverage** | ✅ All questions addressed |
| **L0/L1/L2 Levels** | ✅ Complete |
| **Tool Comparison Matrix** | ✅ 4 matrices provided |
| **Citations with URLs** | ✅ 30+ sources cited |
| **Jerry-Specific Recommendations** | ✅ Phase 1-4 roadmap |
| **Extends Existing Research** | ✅ References GRAPH_DATA_MODEL_ANALYSIS.md |
| **P-001 (Truth & Accuracy)** | ✅ All claims cited |
| **P-002 (File Persistence)** | ✅ Document persisted at docs/research/ |

---

*Document Version: 1.0*
*Created: 2026-01-08*
*Author: Claude (ps-researcher v2.0.0)*
*Extends: docs/research/GRAPH_DATA_MODEL_ANALYSIS.md*

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-08 | Initial research document covering triple stores, graph databases, Python libraries, visualization tools, query engines, serialization formats, and embedded vs server-based tradeoffs |
