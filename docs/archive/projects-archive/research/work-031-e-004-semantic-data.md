# Enabling Semantics in Data: JSON-LD, Linked Data, and Semantic Annotations

> **Research Date:** 2026-01-08
> **PS ID:** work-031
> **Entry ID:** e-004
> **Status:** DECISION-GRADE
> **Purpose:** Research semantic data techniques for Jerry framework integration
> **Extends:** `GRAPH_DATA_MODEL_ANALYSIS.md` (Jerry URI scheme, CloudEvents)

---

## L0: Executive Summary (Plain Language Findings)

This research investigates how to add **semantic meaning** to data so that machines can understand relationships, context, and intent—not just syntax. Think of it as the difference between a computer reading "2026-01-08" as a string versus understanding it as a date that comes after January 7th and before January 9th.

### What We Found

**JSON-LD (JSON for Linking Data)** is the clear winner for adding semantics to JSON data:
- **70% of websites** with structured data now use JSON-LD (2024 data)
- **W3C standard** with active community support
- **Works with existing JSON** by adding a `@context` section
- **Schema.org integration** provides 800+ ready-to-use vocabulary terms
- **Google recommends it** for SEO and knowledge graph integration

### Key Recommendations for Jerry

1. **Adopt JSON-LD** as the semantic layer for Jerry entities (Task, Phase, Plan)
2. **Reuse Jerry URI scheme** (SPEC-001) which is already RDF-compatible
3. **Extend CloudEvents** with JSON-LD contexts for semantic event streams
4. **Reference Schema.org** where possible, create Jerry-specific terms for domain concepts
5. **Enable content negotiation** so Jerry URIs can return JSON-LD or plain JSON

### Tim Berners-Lee's 5-Star Linked Data Model

Jerry's current state and target:

| Stars | Level | Jerry Status |
|-------|-------|--------------|
| ★ | Open license data on web | ✅ **CURRENT** (MIT license, file-based) |
| ★★ | Structured data | ✅ **CURRENT** (JSON, YAML) |
| ★★★ | Non-proprietary format | ✅ **CURRENT** (JSON, not Excel) |
| ★★★★ | URIs to denote things | ✅ **CURRENT** (Jerry URI scheme SPEC-001) |
| ★★★★★ | Link data to other data | 🎯 **TARGET** (JSON-LD integration) |

---

## L1: Technical Details (JSON-LD Patterns & Examples)

### 1. JSON-LD Core Concepts

#### 1.1 The `@context` - Vocabulary Mapping

The `@context` establishes a mapping from short keys to full URIs:

```json
{
  "@context": {
    "name": "http://schema.org/name",
    "homepage": {
      "@id": "http://schema.org/url",
      "@type": "@id"
    },
    "created": {
      "@id": "http://purl.org/dc/terms/created",
      "@type": "http://www.w3.org/2001/XMLSchema#dateTime"
    }
  },
  "name": "Manu Sporny",
  "homepage": "https://manu.sporny.org/",
  "created": "2026-01-08T10:30:00Z"
}
```

**W3C Best Practice:** Cache remote contexts with HTTP cache-control headers to avoid processing delays.

#### 1.2 The `@type` - Entity Classification

The `@type` keyword specifies what kind of thing the JSON object represents:

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Ada Lovelace",
  "jobTitle": "Mathematician"
}
```

**Multiple types are supported:**

```json
{
  "@context": "https://schema.org",
  "@type": ["Person", "Author"],
  "name": "Isaac Asimov"
}
```

#### 1.3 The `@id` - Unique Identifiers (URIs)

The `@id` keyword assigns a globally unique identifier to an entity:

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://jerry.dev/org/acme",
  "name": "Acme Corporation"
}
```

**Jerry Integration:**

```json
{
  "@context": "https://jerry.dev/contexts/worktracker.jsonld",
  "@type": "Task",
  "@id": "jer:jer:work-tracker:task:TASK-042+abc123",
  "title": "Implement JSON-LD support",
  "status": "IN_PROGRESS"
}
```

### 2. JSON-LD Patterns for Jerry Entities

#### 2.1 Task Entity with JSON-LD

```json
{
  "@context": {
    "@vocab": "https://jerry.dev/vocab/",
    "schema": "https://schema.org/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "task": "https://jerry.dev/vocab/Task",
    "title": "schema:name",
    "description": "schema:description",
    "status": {
      "@id": "https://jerry.dev/vocab/status",
      "@type": "@vocab"
    },
    "created": {
      "@id": "schema:dateCreated",
      "@type": "xsd:dateTime"
    },
    "modified": {
      "@id": "schema:dateModified",
      "@type": "xsd:dateTime"
    },
    "belongsToPhase": {
      "@id": "https://jerry.dev/vocab/belongsToPhase",
      "@type": "@id"
    },
    "subtasks": {
      "@id": "https://jerry.dev/vocab/subtasks",
      "@container": "@list"
    }
  },
  "@id": "jer:jer:work-tracker:task:TASK-042+abc123",
  "@type": "task",
  "title": "Implement JSON-LD support",
  "description": "Add semantic annotations to Jerry entities",
  "status": "IN_PROGRESS",
  "created": "2026-01-08T10:00:00Z",
  "modified": "2026-01-08T14:30:00Z",
  "belongsToPhase": "jer:jer:work-tracker:phase:PHASE-003+def456",
  "subtasks": [
    {
      "@type": "Subtask",
      "title": "Research JSON-LD patterns",
      "checked": true
    },
    {
      "@type": "Subtask",
      "title": "Create Jerry context file",
      "checked": false
    }
  ]
}
```

#### 2.2 CloudEvents with JSON-LD Semantics

**Standard CloudEvents (current):**

```json
{
  "specversion": "1.0",
  "type": "jer:jer:work-tracker:facts/TaskCompleted",
  "source": "jer:jer:work-tracker:task:TASK-042",
  "id": "EVT-a1b2c3d4",
  "time": "2026-01-08T15:00:00Z",
  "datacontenttype": "application/json",
  "data": {
    "task_id": "TASK-042",
    "completed_by": "claude"
  }
}
```

**CloudEvents with JSON-LD (enhanced):**

```json
{
  "@context": [
    "https://cloudevents.io/context.jsonld",
    "https://jerry.dev/contexts/worktracker.jsonld"
  ],
  "@type": "CloudEvent",
  "specversion": "1.0",
  "type": {
    "@id": "jer:jer:work-tracker:facts/TaskCompleted",
    "@type": "EventType"
  },
  "source": {
    "@id": "jer:jer:work-tracker:task:TASK-042",
    "@type": "Task"
  },
  "id": "EVT-a1b2c3d4",
  "time": {
    "@value": "2026-01-08T15:00:00Z",
    "@type": "xsd:dateTime"
  },
  "datacontenttype": "application/ld+json",
  "data": {
    "@context": "https://jerry.dev/contexts/worktracker.jsonld",
    "@type": "TaskCompletedEvent",
    "task": {
      "@id": "jer:jer:work-tracker:task:TASK-042"
    },
    "completedBy": {
      "@id": "jer:jer:work-tracker:actor:claude",
      "@type": "Actor"
    }
  }
}
```

**Key Enhancement:** The `data` field now contains semantically rich linked data with explicit types and relationships.

#### 2.3 Phase Aggregate with Contained Tasks

```json
{
  "@context": "https://jerry.dev/contexts/worktracker.jsonld",
  "@id": "jer:jer:work-tracker:phase:PHASE-003+def456",
  "@type": "Phase",
  "displayNumber": 1,
  "title": "Research & Design",
  "status": "IN_PROGRESS",
  "targetDate": "2026-02-01",
  "contains": [
    {
      "@id": "jer:jer:work-tracker:task:TASK-042+abc123",
      "@type": "Task"
    },
    {
      "@id": "jer:jer:work-tracker:task:TASK-043+xyz789",
      "@type": "Task"
    }
  ]
}
```

### 3. Schema.org Vocabulary Integration

#### 3.1 Mapping Jerry Concepts to Schema.org

| Jerry Concept | Schema.org Type | Rationale |
|---------------|-----------------|-----------|
| **Task** | `schema:Action` or custom | Action represents something to be done |
| **Phase** | `schema:Project` | Project is a collection of tasks |
| **Plan** | `schema:PlanAction` | High-level plan encompassing phases |
| **Actor (Human)** | `schema:Person` | Direct mapping |
| **Actor (Claude)** | `schema:SoftwareApplication` | AI agent as software |
| **Evidence** | `schema:CreativeWork` | Documents, artifacts |
| **Event** | `schema:Event` | Domain events |

#### 3.2 Example: Task as Schema.org Action

```json
{
  "@context": "https://schema.org",
  "@type": "Action",
  "@id": "jer:jer:work-tracker:task:TASK-042",
  "name": "Implement JSON-LD support",
  "description": "Add semantic annotations to Jerry entities",
  "actionStatus": "ActiveActionStatus",
  "startTime": "2026-01-08T10:00:00Z",
  "agent": {
    "@type": "SoftwareApplication",
    "@id": "jer:jer:work-tracker:actor:claude",
    "name": "Claude",
    "applicationCategory": "AI Assistant"
  },
  "object": {
    "@type": "SoftwareSourceCode",
    "name": "Jerry Framework"
  }
}
```

### 4. Content Negotiation for Jerry URIs

**Concept:** A single Jerry URI can return different representations based on the HTTP `Accept` header.

#### 4.1 Request/Response Examples

**Request JSON:**
```http
GET /jer/work-tracker/task/TASK-042 HTTP/1.1
Host: jerry.dev
Accept: application/json
```

**Response:**
```json
{
  "id": "TASK-042",
  "title": "Implement JSON-LD support",
  "status": "IN_PROGRESS"
}
```

**Request JSON-LD:**
```http
GET /jer/work-tracker/task/TASK-042 HTTP/1.1
Host: jerry.dev
Accept: application/ld+json
```

**Response:**
```json
{
  "@context": "https://jerry.dev/contexts/worktracker.jsonld",
  "@id": "jer:jer:work-tracker:task:TASK-042+abc123",
  "@type": "Task",
  "title": "Implement JSON-LD support",
  "status": "IN_PROGRESS",
  "created": "2026-01-08T10:00:00Z"
}
```

**Request HTML (human-readable):**
```http
GET /jer/work-tracker/task/TASK-042 HTTP/1.1
Host: jerry.dev
Accept: text/html
```

**Response:**
```html
<!DOCTYPE html>
<html>
<head>
  <title>Task TASK-042 - Jerry Framework</title>
  <script type="application/ld+json">
  {
    "@context": "https://jerry.dev/contexts/worktracker.jsonld",
    "@id": "jer:jer:work-tracker:task:TASK-042",
    "@type": "Task",
    "title": "Implement JSON-LD support"
  }
  </script>
</head>
<body>
  <h1>Implement JSON-LD support</h1>
  <dl>
    <dt>Status:</dt><dd>IN_PROGRESS</dd>
    <dt>Created:</dt><dd>2026-01-08 10:00:00 UTC</dd>
  </dl>
</body>
</html>
```

### 5. RDFa and Microdata (Alternative Approaches)

#### 5.1 Adoption Trends (2024)

| Format | Adoption | Use Case | Jerry Applicability |
|--------|----------|----------|---------------------|
| **JSON-LD** | 70% | APIs, data files, SEO | ⭐⭐⭐⭐⭐ **PRIMARY** |
| **Microdata** | 46% | HTML annotations | ⭐⭐⭐ Optional for web UI |
| **RDFa** | 3% | Complex semantic HTML | ⭐ Low priority |
| **Microformats** | 23% | Simple HTML (hCard) | ⭐ Legacy support |

**Source:** Web Data Commons 2024 dataset (1.3 billion HTML pages analyzed)

#### 5.2 JSON-LD vs RDFa Example

**JSON-LD (recommended for Jerry):**
```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Ada Lovelace",
  "jobTitle": "Mathematician"
}
```

**RDFa (HTML embedding):**
```html
<div vocab="https://schema.org/" typeof="Person">
  <span property="name">Ada Lovelace</span>
  <span property="jobTitle">Mathematician</span>
</div>
```

**Verdict:** JSON-LD wins for Jerry because:
- ✅ Separates data from presentation
- ✅ Works with file-based storage (no HTML required)
- ✅ API-friendly
- ✅ Easier maintenance

### 6. Linked Data Principles (Berners-Lee 2006)

#### 6.1 Four Principles

1. **Use URIs to name things**
   - Jerry: ✅ SPEC-001 Jerry URI scheme (`jer:jer:work-tracker:task:TASK-042`)

2. **Use HTTP URIs for dereferencing**
   - Jerry: 🎯 **Future** - Convert `jer:` to `https://jerry.dev/` via resolver

3. **Provide useful information via RDF/SPARQL**
   - Jerry: 🎯 **This research** - JSON-LD provides RDF serialization

4. **Link to other things via their URIs**
   - Jerry: 🎯 **Target** - Cross-reference Schema.org, external ontologies

#### 6.2 5-Star Deployment Scheme

| Level | Requirement | Jerry Example |
|-------|-------------|---------------|
| ★ | Open data on web under open license | MIT license, file-based storage |
| ★★ | Structured data | JSON/YAML files |
| ★★★ | Non-proprietary format | JSON (not Excel) |
| ★★★★ | Use URIs to denote things | Jerry URI scheme |
| ★★★★★ | Link your data to other data | **JSON-LD with Schema.org** 🎯 |

**Jerry's Path to 5 Stars:**

```json
{
  "@context": [
    "https://schema.org",
    "https://jerry.dev/contexts/worktracker.jsonld"
  ],
  "@id": "jer:jer:work-tracker:task:TASK-042",
  "@type": ["Action", "Task"],
  "name": "Implement JSON-LD support",
  "partOf": {
    "@id": "jer:jer:work-tracker:phase:PHASE-003",
    "@type": "Project"
  },
  "agent": {
    "@id": "https://www.anthropic.com/claude",
    "@type": "SoftwareApplication",
    "name": "Claude"
  },
  "instrument": {
    "@id": "https://python.org/",
    "@type": "ProgrammingLanguage",
    "name": "Python"
  }
}
```

**Note:** This links to external entities (Anthropic, Python.org) achieving ★★★★★.

### 7. When to Embed vs Reference External Ontologies

#### 7.1 Decision Matrix

| Scenario | Strategy | Example |
|----------|----------|---------|
| **Common concepts** (people, dates, organizations) | 🔗 **Reference** Schema.org, Dublin Core | `"name": "schema:name"` |
| **Domain-specific** (Jerry's Task, Phase, Plan) | 🏠 **Create** Jerry vocabulary | `"status": "jerry:TaskStatus"` |
| **Well-established standards** (CloudEvents, PROV-O) | 🔗 **Reference** W3C specs | `"@type": "prov:Activity"` |
| **Experimental concepts** | 🏠 **Embed** temporarily, formalize later | Custom JSON-LD inline |

#### 7.2 Jerry Vocabulary Design

**Jerry Context File** (`https://jerry.dev/contexts/worktracker.jsonld`):

```json
{
  "@context": {
    "@version": 1.1,
    "@vocab": "https://jerry.dev/vocab/",

    "schema": "https://schema.org/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "prov": "http://www.w3.org/ns/prov#",
    "ce": "https://cloudevents.io/vocab/",

    "Task": {
      "@id": "jerry:Task",
      "@type": "@id"
    },
    "Phase": {
      "@id": "jerry:Phase",
      "@type": "@id"
    },
    "Plan": {
      "@id": "jerry:Plan",
      "@type": "@id"
    },
    "Subtask": {
      "@id": "jerry:Subtask",
      "@type": "@id"
    },

    "title": "schema:name",
    "description": "schema:description",
    "created": {
      "@id": "schema:dateCreated",
      "@type": "xsd:dateTime"
    },
    "modified": {
      "@id": "schema:dateModified",
      "@type": "xsd:dateTime"
    },

    "status": {
      "@id": "jerry:status",
      "@type": "@vocab"
    },
    "displayNumber": {
      "@id": "jerry:displayNumber",
      "@type": "xsd:integer"
    },
    "verification": "jerry:verification",
    "blockingReason": "jerry:blockingReason",

    "belongsToPhase": {
      "@id": "jerry:belongsToPhase",
      "@type": "@id"
    },
    "belongsToPlan": {
      "@id": "jerry:belongsToPlan",
      "@type": "@id"
    },
    "contains": {
      "@id": "jerry:contains",
      "@type": "@id",
      "@container": "@set"
    },
    "dependsOn": {
      "@id": "jerry:dependsOn",
      "@type": "@id",
      "@container": "@set"
    },

    "Actor": "prov:Agent",
    "performedBy": {
      "@id": "prov:wasAssociatedWith",
      "@type": "@id"
    },
    "emittedEvent": {
      "@id": "prov:generated",
      "@type": "@id"
    }
  }
}
```

**Rationale:**
- ✅ Reuses `schema:name`, `schema:description` (common concepts)
- ✅ Reuses `prov:Agent`, `prov:wasAssociatedWith` (provenance)
- ✅ Defines `jerry:status`, `jerry:displayNumber` (domain-specific)
- ✅ Maps Jerry edges (`belongsToPhase`, `contains`) to custom vocabulary

### 8. Linked Data Success Stories at Scale

#### 8.1 DBpedia Knowledge Graph

**Scale:** 3.4 million concepts, 1 billion triples
**Technology:** RDF, SPARQL, Linked Data
**Use Case:** Extract structured data from Wikipedia
**Impact:** 600,000+ file downloads/year, backbone of Linked Open Data cloud

**Relevance to Jerry:** Demonstrates that file-based RDF can scale to billions of triples. Jerry could adopt similar architecture for work tracker knowledge graph.

#### 8.2 Wikidata

**Scale:** Collaborative linked dataset, Wikimedia Foundation
**Technology:** RDF, SPARQL, content negotiation
**Use Case:** Central structured data repository for Wikipedia projects
**Impact:** Foundation for archival linked data, GLAM sector initiatives

**Relevance to Jerry:** Shows how URIs with content negotiation enable both human and machine access to the same data.

#### 8.3 Schema.org Deployment

**Scale:** 45+ million websites, 450+ billion Schema.org objects (2024)
**Technology:** JSON-LD, Microdata, RDFa
**Use Case:** SEO, knowledge graphs, search engine optimization
**Impact:** 51.25% of web pages now have structured data (up from 5.7% in 2010)

**Relevance to Jerry:** Validates JSON-LD as the dominant semantic data format. Jerry should align with this ecosystem.

#### 8.4 Netflix Knowledge Graph (2025)

**Architecture:** "Conceptual RDF, Flexible Physical"
**Pattern:** "Model Once, Represent Everywhere"
**Technology:** RDF ontology → GraphQL, Avro, SQL projections
**Impact:** Unified data architecture across Netflix domains

**Relevance to Jerry:** Aligns with `GRAPH_DATA_MODEL_ANALYSIS.md` (DISC-064). Jerry can adopt same pattern: EntityBase → JSON, JSON-LD, Graph, RDF.

### 9. AsyncAPI + CloudEvents + JSON-LD Integration

#### 9.1 Current State

**AsyncAPI** focuses on the application and channels; **CloudEvents** focuses on the message format. They are complementary, not competitive.

**Current Challenge:** Limited guidance on adding semantic annotations to event-driven APIs.

#### 9.2 Proposed Pattern for Jerry

**AsyncAPI Definition** (semantic enhancement):

```yaml
asyncapi: 3.0.0
info:
  title: Jerry Work Tracker Event API
  version: 1.0.0

channels:
  task.events:
    messages:
      taskCompleted:
        contentType: application/cloudevents+json; charset=utf-8; profile=ld
        payload:
          $ref: '#/components/schemas/TaskCompletedEvent'

components:
  schemas:
    TaskCompletedEvent:
      type: object
      properties:
        "@context":
          type: array
          items:
            type: string
          example:
            - "https://cloudevents.io/context.jsonld"
            - "https://jerry.dev/contexts/worktracker.jsonld"
        "@type":
          type: string
          example: "CloudEvent"
        specversion:
          type: string
          example: "1.0"
        type:
          type: object
          properties:
            "@id":
              type: string
              example: "jer:jer:work-tracker:facts/TaskCompleted"
        data:
          $ref: '#/components/schemas/TaskCompletedData'

    TaskCompletedData:
      type: object
      properties:
        "@context":
          type: string
          example: "https://jerry.dev/contexts/worktracker.jsonld"
        "@type":
          type: string
          example: "TaskCompletedEvent"
        task:
          type: object
          properties:
            "@id":
              type: string
              example: "jer:jer:work-tracker:task:TASK-042"
```

**Benefits:**
- ✅ AsyncAPI describes the message structure
- ✅ CloudEvents provides event envelope
- ✅ JSON-LD adds semantic richness to event data
- ✅ Maintains backward compatibility (optional `@context`)

---

## L2: Strategic Implications (For Jerry Framework)

### 1. Integration Roadmap

#### Phase 1: Foundation (Q1 2026)
- ✅ Jerry URI scheme already RDF-compatible (SPEC-001)
- 🎯 Create Jerry JSON-LD context at `https://jerry.dev/contexts/worktracker.jsonld`
- 🎯 Add optional `@context`, `@type`, `@id` to entity serialization
- 🎯 Maintain backward compatibility (plain JSON still works)

#### Phase 2: Semantic Events (Q2 2026)
- 🎯 Extend CloudEvents with JSON-LD contexts
- 🎯 Enable RDF export from event streams
- 🎯 Add SPARQL query capability (via RDFLib)

#### Phase 3: Linked Data (Q3 2026)
- 🎯 Implement content negotiation (Accept: application/ld+json)
- 🎯 URI dereferencing via HTTP server
- 🎯 Link Jerry entities to Schema.org, external ontologies
- 🎯 Achieve 5-star Linked Open Data status

#### Phase 4: Knowledge Graph (Q4 2026)
- 🎯 RDF triple store integration (kglab, RDFLib)
- 🎯 SHACL validation for data quality
- 🎯 OWL ontology formalization
- 🎯 Inference and reasoning capabilities

### 2. Architectural Decisions

#### AD-001: JSON-LD as Optional Extension Layer

**Decision:** Add JSON-LD support as an **optional extension** to existing JSON serialization, not a replacement.

**Rationale:**
- ✅ Maintains backward compatibility
- ✅ Low barrier to adoption (gradual enhancement)
- ✅ Follows "Jerry is JSON-LD-ready, not JSON-LD-required" principle

**Implementation:**
```python
# src/domain/serialization/json_ld.py

from typing import Dict, Any, Optional
from ..entities.task import Task

class JsonLdSerializer:
    def __init__(self, context_url: str = "https://jerry.dev/contexts/worktracker.jsonld"):
        self.context_url = context_url

    def serialize(self, entity: Task, include_context: bool = True) -> Dict[str, Any]:
        """Serialize entity to JSON-LD format."""
        base_json = entity.to_dict()  # Existing JSON serialization

        if not include_context:
            return base_json

        json_ld = {
            "@context": self.context_url,
            "@id": entity.uri.to_string(),  # Jerry URI
            "@type": self._get_type(entity),
            **base_json
        }

        return json_ld

    def _get_type(self, entity) -> str:
        return entity.__class__.__name__  # "Task", "Phase", "Plan"
```

#### AD-002: Reuse Schema.org Where Possible

**Decision:** Map Jerry entities to Schema.org types where semantically appropriate, extend with Jerry-specific vocabulary only when necessary.

**Mapping:**
- `Task` → `schema:Action` (base) + `jerry:Task` (extension)
- `Phase` → `schema:Project`
- `Plan` → `schema:PlanAction`
- `Actor` → `schema:Person` or `schema:SoftwareApplication`
- `Evidence` → `schema:CreativeWork`

**Benefits:**
- ✅ Interoperability with existing tools (Google Knowledge Graph, etc.)
- ✅ Reduced vocabulary maintenance burden
- ✅ Leverages 800+ Schema.org terms

#### AD-003: CloudEvents as Semantic Event Stream

**Decision:** Extend CloudEvents `data` field with JSON-LD contexts for semantic event sourcing.

**Rationale:**
- ✅ CloudEvents provides standardized envelope (specversion, type, source)
- ✅ JSON-LD in `data` field adds semantic richness
- ✅ Enables RDF export of entire event history
- ✅ Supports temporal queries (SPARQL with time filters)

**Example Event Reconstruction:**

```sparql
# SPARQL query to reconstruct task state from events

PREFIX jerry: <https://jerry.dev/vocab/>
PREFIX prov: <http://www.w3.org/ns/prov#>

SELECT ?event ?time ?eventType ?data
WHERE {
  ?task a jerry:Task ;
        jerry:id "TASK-042" ;
        prov:generated ?event .

  ?event a <https://cloudevents.io/vocab/CloudEvent> ;
         <https://cloudevents.io/vocab/time> ?time ;
         <https://cloudevents.io/vocab/type> ?eventType ;
         <https://cloudevents.io/vocab/data> ?data .
}
ORDER BY ?time
```

#### AD-004: Content Negotiation for Jerry URIs

**Decision:** Implement HTTP-based content negotiation so Jerry URIs return different formats based on `Accept` header.

**Supported Formats:**
| Accept Header | Response | Use Case |
|--------------|----------|----------|
| `application/json` | Plain JSON | APIs, tools |
| `application/ld+json` | JSON-LD | Semantic web |
| `text/turtle` | RDF Turtle | Triple stores |
| `text/html` | HTML + embedded JSON-LD | Human browsing |
| `application/rdf+xml` | RDF/XML | Legacy systems |

**Implementation Sketch:**

```python
# src/interface/http/uri_resolver.py

from flask import Flask, request, jsonify
from ..serialization.json_ld import JsonLdSerializer
from ..serialization.turtle import TurtleSerializer

app = Flask(__name__)

@app.route('/jer/work-tracker/task/<task_id>')
def resolve_task_uri(task_id: str):
    task = repository.find_by_id(task_id)

    accept = request.headers.get('Accept', 'application/json')

    if 'application/ld+json' in accept:
        serializer = JsonLdSerializer()
        return jsonify(serializer.serialize(task)), 200, {'Content-Type': 'application/ld+json'}

    elif 'text/turtle' in accept:
        serializer = TurtleSerializer()
        return serializer.serialize(task), 200, {'Content-Type': 'text/turtle'}

    elif 'text/html' in accept:
        return render_template('task.html', task=task), 200

    else:
        return jsonify(task.to_dict()), 200
```

### 3. Knowledge Graph Alignment (Netflix UDA Pattern)

**From `GRAPH_DATA_MODEL_ANALYSIS.md` (DISC-064):**

> Netflix UDA "Model Once, Represent Everywhere" - Single domain model with multiple projections (GraphQL, Avro, SQL, RDF)

**Jerry Adoption:**

```
┌─────────────────────────────────────────────────────────────┐
│                   JERRY SEMANTIC DATA MODEL                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────────────────────────────────────┐          │
│   │        DOMAIN MODEL (EntityBase)             │          │
│   │  - Task, Phase, Plan (Aggregate Roots)       │          │
│   │  - Jerry URI scheme (SPEC-001)               │          │
│   │  - CloudEvents (event sourcing)              │          │
│   └──────────────┬───────────────────────────────┘          │
│                  │                                           │
│                  │ Serialization Adapters                    │
│                  │                                           │
│   ┌──────────────┼───────────────────────────────┐          │
│   │              │                               │          │
│   ▼              ▼                               ▼          │
│ JSON          JSON-LD                         RDF Turtle    │
│ (current)     (semantic)                      (triple store)│
│   │              │                               │          │
│   │              │                               │          │
│   ▼              ▼                               ▼          │
│ Files         HTTP API                       SPARQL Endpoint│
│ (storage)     (content negotiation)          (queries)      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key Insight:** Jerry's existing `EntityBase` and repository pattern already support this. Adding JSON-LD is just another serialization adapter.

### 4. Data Quality & Validation (SHACL)

**Challenge:** As Jerry knowledge graph grows, how do we ensure data quality?

**Solution:** SHACL (Shapes Constraint Language) for RDF validation.

**Example SHACL Shape for Task:**

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix jerry: <https://jerry.dev/vocab/> .
@prefix schema: <https://schema.org/> .

jerry:TaskShape
  a sh:NodeShape ;
  sh:targetClass jerry:Task ;

  sh:property [
    sh:path schema:name ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:string ;
    sh:minLength 1 ;
    sh:maxLength 200 ;
  ] ;

  sh:property [
    sh:path jerry:status ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:in ( "PENDING" "IN_PROGRESS" "BLOCKED" "COMPLETED" "CANCELLED" ) ;
  ] ;

  sh:property [
    sh:path jerry:belongsToPhase ;
    sh:maxCount 1 ;
    sh:class jerry:Phase ;
  ] ;

  sh:property [
    sh:path schema:dateCreated ;
    sh:minCount 1 ;
    sh:maxCount 1 ;
    sh:datatype xsd:dateTime ;
  ] .
```

**Benefits:**
- ✅ Machine-readable validation rules
- ✅ Detects data quality issues early
- ✅ Documents constraints as code
- ✅ Integrates with RDF tooling (pySHACL)

**Integration with Jerry:**

```python
# src/domain/validation/shacl_validator.py

from pyshacl import validate
from rdflib import Graph

class ShaclValidator:
    def __init__(self, shapes_file: str):
        self.shapes = Graph().parse(shapes_file, format="turtle")

    def validate_task(self, task_rdf: str) -> tuple[bool, Graph, str]:
        """Validate task RDF against SHACL shapes."""
        data_graph = Graph().parse(data=task_rdf, format="json-ld")

        conforms, results_graph, results_text = validate(
            data_graph,
            shacl_graph=self.shapes,
            inference='rdfs',
            abort_on_first=False
        )

        return conforms, results_graph, results_text
```

### 5. AI & LLM Integration (2025 Trends)

**From Research:** "The growing interplay between semantic technologies and large language models is creating a new layer of enterprise AI, where structured knowledge graphs enhance model accuracy, traceability, and domain adaptation."

**Jerry + LLM Integration Scenarios:**

#### 5.1 LLM-Enhanced Knowledge Graph Construction

**Use Case:** Claude analyzes unstructured task descriptions and infers semantic relationships.

**Example:**

```python
# LLM extracts entities and relationships from natural language

task_description = """
Implement JSON-LD support for Jerry entities. This depends on the
Jerry URI specification (SPEC-001) and should follow W3C best practices.
Claude will be the primary contributor.
"""

# LLM output (structured)
{
  "@context": "https://jerry.dev/contexts/worktracker.jsonld",
  "@type": "Task",
  "title": "Implement JSON-LD support",
  "dependsOn": [
    {
      "@id": "jer:jer:specifications:SPEC-001",
      "@type": "Specification"
    }
  ],
  "conformsTo": {
    "@id": "https://www.w3.org/TR/json-ld11/",
    "@type": "TechnicalSpecification"
  },
  "contributor": {
    "@id": "jer:jer:work-tracker:actor:claude",
    "@type": "SoftwareApplication"
  }
}
```

#### 5.2 Semantic Query Enhancement

**Use Case:** User asks natural language question, LLM converts to SPARQL, executes against Jerry knowledge graph.

**Example:**

```
User: "What tasks has Claude completed in the last week?"

LLM → SPARQL:
PREFIX jerry: <https://jerry.dev/vocab/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?task ?title ?completedTime
WHERE {
  ?task a jerry:Task ;
        jerry:status "COMPLETED" ;
        schema:name ?title ;
        prov:wasAssociatedWith ?actor ;
        schema:dateModified ?completedTime .

  ?actor schema:name "Claude" .

  FILTER (?completedTime >= "2026-01-01T00:00:00Z"^^xsd:dateTime)
}
ORDER BY DESC(?completedTime)
```

#### 5.3 Knowledge Graph Validation via LLM

**Use Case:** LLM reviews Jerry knowledge graph for inconsistencies, suggests fixes.

**Example:**

```
LLM Analysis:
"Task TASK-042 has status 'COMPLETED' but no 'dateCompleted' property.
Recommendation: Add schema:endTime property with completion timestamp."

Suggested Fix (JSON-LD):
{
  "@id": "jer:jer:work-tracker:task:TASK-042",
  "schema:endTime": {
    "@value": "2026-01-08T15:30:00Z",
    "@type": "xsd:dateTime"
  }
}
```

### 6. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Complexity Creep** | JSON-LD adds cognitive overhead | Make it optional; provide simple defaults |
| **Context File Maintenance** | Stale context breaks parsing | Version contexts (v1.0, v1.1); cache with HTTP headers |
| **Performance Overhead** | JSON-LD processing is slower than plain JSON | Lazy evaluation; cache expanded forms |
| **Vocabulary Proliferation** | Too many custom Jerry terms | Reuse Schema.org; limit Jerry vocab to essentials |
| **RDF Tooling Immaturity** | Python RDF tools less mature than JSON tools | Use battle-tested RDFLib; contribute upstream |

### 7. Success Metrics

**How do we know JSON-LD integration is successful?**

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Adoption** | 50% of Jerry entities serialized with JSON-LD | Count `@context` in output files |
| **Interoperability** | Jerry data consumable by 3+ external tools | Test with Google Structured Data Testing Tool, RDF validators |
| **Query Capability** | 10+ useful SPARQL queries documented | Query library in `docs/knowledge/` |
| **Performance** | JSON-LD serialization < 2x plain JSON | Benchmark suite |
| **Data Quality** | SHACL validation passing for 95%+ entities | Automated SHACL tests |

### 8. Related Work & Prior Art

**From `GRAPH_DATA_MODEL_ANALYSIS.md` (Section 11):**

| Library | Purpose | Jerry Applicability |
|---------|---------|---------------------|
| **kglab** | Unified KG abstraction (RDF, NetworkX, Pandas) | ⭐⭐⭐⭐⭐ HIGH - Bridges paradigms |
| **RDFLib** | Pure Python RDF processing | ⭐⭐⭐⭐⭐ HIGH - Semantic Web foundation |
| **rdf2gremlin** | RDF → TinkerPop transformation | ⭐⭐⭐⭐ HIGH - Bridges RDF to property graph |

**Recommendation:** Use **RDFLib** for JSON-LD processing, **kglab** if Jerry needs to support both RDF and property graph paradigms.

---

## Recommendations for Jerry Framework

### Immediate Actions (Week 1)

1. ✅ **Create Jerry JSON-LD Context**
   - File: `contexts/worktracker.jsonld`
   - Host at: `https://jerry.dev/contexts/worktracker.jsonld` (future)
   - Include mappings to Schema.org, Dublin Core, PROV-O

2. ✅ **Add JSON-LD Serializer**
   - Module: `src/domain/serialization/json_ld.py`
   - Make `@context` optional (backward compatibility)
   - Add `@id`, `@type` to Task/Phase/Plan entities

3. ✅ **Document Pattern**
   - Create `docs/design/JSON_LD_INTEGRATION.md`
   - Include examples for each entity type
   - Reference this research document

### Short-term Actions (Month 1)

4. 🎯 **Extend CloudEvents with JSON-LD**
   - Add `@context` to CloudEvents `data` field
   - Create `contexts/cloudevents.jsonld` extension

5. 🎯 **Add RDFLib Dependency**
   - Update `requirements.txt`: `rdflib>=7.0.0`
   - Create RDF export utility for knowledge graph

6. 🎯 **Create SHACL Validation Shapes**
   - File: `schemas/shacl/task-shape.ttl`
   - Integrate with CI/CD for data quality checks

### Medium-term Actions (Quarter 1)

7. 🎯 **Implement Content Negotiation**
   - HTTP server for Jerry URI dereferencing
   - Support: `application/json`, `application/ld+json`, `text/turtle`, `text/html`

8. 🎯 **Create SPARQL Query Library**
   - `docs/knowledge/sparql-queries.md`
   - Document common traversals (task dependencies, progress aggregation)

9. 🎯 **Link to External Ontologies**
   - Map Jerry entities to Schema.org types
   - Reference W3C PROV-O for provenance
   - Link to CloudEvents vocabulary

### Long-term Vision (2026)

10. 🎯 **5-Star Linked Open Data**
    - Publish Jerry knowledge graph as Linked Open Data
    - Enable external tools to query Jerry data
    - Contribute Jerry vocabulary to community

11. 🎯 **Knowledge Graph Analytics**
    - SPARQL endpoint for complex queries
    - OWL reasoning for inferred relationships
    - Graph algorithms via NetworkX/kglab

12. 🎯 **LLM + Knowledge Graph Integration**
    - LLM-enhanced entity extraction from natural language
    - Semantic query interface (natural language → SPARQL)
    - Knowledge graph validation via LLM analysis

---

## Sources

| Source | Title | URL |
|--------|-------|-----|
| **W3C-001** | JSON-LD Best Practices | https://w3c.github.io/json-ld-bp/ |
| **W3C-002** | JSON-LD 1.1 Specification | https://www.w3.org/TR/json-ld11/ |
| **W3C-003** | Content Negotiation by Profile | https://www.w3.org/TR/dx-prof-conneg/ |
| **W3C-004** | SHACL Shapes Constraint Language | https://www.w3.org/TR/shacl/ |
| **W3C-005** | RDF 1.1 Primer | https://www.w3.org/TR/rdf11-primer/ |
| **W3C-006** | SPARQL 1.1 Query Language | https://www.w3.org/TR/sparql11-query/ |
| **JSONLD-001** | JSON-LD Official Site | https://json-ld.org/ |
| **JSONLD-002** | JSON-LD Primer | https://json-ld.org/primer/latest/ |
| **SCHEMA-001** | Schema.org Developers Guide | https://schema.org/docs/developers.html |
| **SCHEMA-002** | Schema.org JSON-LD Context | https://schema.org/docs/jsonldcontext.json |
| **BERNERS-LEE-001** | Linked Data Principles (2006) | https://www.w3.org/DesignIssues/LinkedData.html |
| **5STAR-001** | 5-Star Open Data | https://5stardata.info/en/ |
| **WDC-001** | Web Data Commons 2024 Corpus | https://webdatacommons.org/structureddata/ |
| **WDC-002** | RDFa, Microdata, JSON-LD Dataset | https://www.uni-mannheim.de/dws/news/wdc-json-ld-microdata-rdfa-data-corpus-2024-published/ |
| **DBPEDIA-001** | DBpedia Association | https://www.dbpedia.org/ |
| **WIKIDATA-001** | Wikidata Linked Open Data Workflow | https://www.wikidata.org/wiki/Wikidata:Linked_open_data_workflow |
| **ASYNC-001** | AsyncAPI and CloudEvents | https://www.asyncapi.com/blog/asyncapi-cloud-events |
| **CLOUDEVENTS-001** | CloudEvents Specification | https://cloudevents.io/ |
| **ONTOTEXT-001** | Five-Star Linked Open Data | https://www.ontotext.com/knowledgehub/fundamentals/five-star-linked-open-data/ |
| **SEMANTIC-ARTS-001** | Year of the Knowledge Graph (2025) | https://www.semanticarts.com/the-year-of-the-knowledge-graph-2025/ |
| **MARKETS-001** | Semantic Web Market 2025-2030 | https://www.marketsandmarkets.com/PressReleases/semantic-web.asp |
| **NETFLIX-001** | Netflix Knowledge Graph | https://netflixtechblog.medium.com/unlocking-entertainment-intelligence-with-knowledge-graph-da4b22090141 |
| **NETFLIX-002** | Netflix UDA Architecture | https://netflixtechblog.com/uda-unified-data-architecture-6a6aee261d8d |
| **RDFLIB-001** | RDFLib Python Library | https://github.com/RDFLib/rdflib |
| **KGLAB-001** | kglab - Graph Data Science | https://github.com/DerwenAI/kglab |
| **SHACL-PERF-001** | UpSHACL: Targeted Validation | https://link.springer.com/chapter/10.1007/978-3-032-09527-5_7 |
| **W3C-CNEG-001** | Content Negotiation (2006) | https://www.w3.org/blog/2006/content-negotiation/ |
| **TPXIMPACT-001** | Linked Data Principles Walkthrough | https://www.tpximpact.com/knowledge-hub/blogs/tech/linked-data-principles |

---

## Appendix A: Jerry JSON-LD Context (Draft)

**File:** `contexts/worktracker.jsonld`

```json
{
  "@context": {
    "@version": 1.1,
    "@vocab": "https://jerry.dev/vocab/",

    "schema": "https://schema.org/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "prov": "http://www.w3.org/ns/prov#",
    "dc": "http://purl.org/dc/terms/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "ce": "https://cloudevents.io/vocab/",

    "Task": {
      "@id": "jerry:Task",
      "@type": "@id"
    },
    "Phase": {
      "@id": "jerry:Phase",
      "@type": "@id"
    },
    "Plan": {
      "@id": "jerry:Plan",
      "@type": "@id"
    },
    "Subtask": {
      "@id": "jerry:Subtask",
      "@type": "@id"
    },
    "Actor": {
      "@id": "prov:Agent",
      "@type": "@id"
    },
    "Evidence": {
      "@id": "schema:CreativeWork",
      "@type": "@id"
    },

    "title": "schema:name",
    "description": "schema:description",
    "created": {
      "@id": "schema:dateCreated",
      "@type": "xsd:dateTime"
    },
    "modified": {
      "@id": "schema:dateModified",
      "@type": "xsd:dateTime"
    },
    "createdBy": {
      "@id": "prov:wasAttributedTo",
      "@type": "@id"
    },

    "status": {
      "@id": "jerry:status",
      "@type": "@vocab"
    },
    "displayNumber": {
      "@id": "jerry:displayNumber",
      "@type": "xsd:integer"
    },
    "verification": "jerry:verification",
    "blockingReason": "jerry:blockingReason",
    "targetDate": {
      "@id": "schema:targetDate",
      "@type": "xsd:date"
    },

    "belongsToPhase": {
      "@id": "jerry:belongsToPhase",
      "@type": "@id"
    },
    "belongsToPlan": {
      "@id": "jerry:belongsToPlan",
      "@type": "@id"
    },
    "contains": {
      "@id": "schema:hasPart",
      "@type": "@id",
      "@container": "@set"
    },
    "dependsOn": {
      "@id": "jerry:dependsOn",
      "@type": "@id",
      "@container": "@set"
    },
    "blocks": {
      "@id": "jerry:blocks",
      "@type": "@id",
      "@container": "@set"
    },

    "checked": {
      "@id": "jerry:checked",
      "@type": "xsd:boolean"
    },
    "checkedAt": {
      "@id": "jerry:checkedAt",
      "@type": "xsd:dateTime"
    },
    "checkedBy": {
      "@id": "jerry:checkedBy",
      "@type": "@id"
    },

    "performedBy": {
      "@id": "prov:wasAssociatedWith",
      "@type": "@id"
    },
    "emittedEvent": {
      "@id": "prov:generated",
      "@type": "@id"
    },
    "evidencedBy": {
      "@id": "jerry:evidencedBy",
      "@type": "@id",
      "@container": "@set"
    }
  }
}
```

---

## Appendix B: 5W1H Research Summary

| Question | Answer |
|----------|--------|
| **What** techniques enable semantic meaning? | JSON-LD (primary), RDFa, Microdata, RDF/XML. JSON-LD is the clear winner (70% adoption). |
| **Why** is linked data valuable? | Enables machine understanding, interoperability, knowledge graph construction, and AI/LLM integration. |
| **Who** are authoritative sources? | Tim Berners-Lee (Linked Data principles), W3C (JSON-LD spec), Manu Sporny (JSON-LD co-creator), Schema.org (vocabulary). |
| **When** to embed vs reference? | Reference Schema.org/Dublin Core for common concepts; create Jerry vocabulary for domain-specific concepts. |
| **Where** is it deployed at scale? | DBpedia (1B triples), Wikidata (collaborative LD), Schema.org (45M+ websites), Netflix KG (conceptual RDF). |
| **How** to add semantics to JSON? | Add `@context` (vocabulary), `@type` (entity class), `@id` (URI identifier). Use Schema.org context or create custom. |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-08 | Initial research document (ps-researcher agent v2.0.0) |

---

*Document Version: 1.0*
*Created: 2026-01-08*
*Author: Claude (ps-researcher agent)*
*Research Framework: 5W1H*
*Output Levels: L0 (Executive), L1 (Technical), L2 (Strategic)*
*Constitution Compliance: P-001 (Truth & Accuracy), P-002 (File Persistence)*
