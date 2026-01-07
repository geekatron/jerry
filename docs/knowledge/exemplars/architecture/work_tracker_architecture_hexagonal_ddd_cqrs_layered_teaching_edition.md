# Work Tracker Reference Architecture

**Hexagonal Architecture + Domain‑Driven Design (DDD) + Command Query Responsibility Segregation (CQRS)**  
**CLI + HTTP API + SQLite / JSON / Markdown Persistence**

> This document is intentionally written as a *single linear narrative* where **every major concept is explained at three levels**:
>
> - 🧸 *Explain it like I’m 5 (ELI5)*
> - 👶 *Junior Software Engineer*
> - 🧠 *Principal / Architect*
>
> ASCII diagrams are first‑class artifacts and safe for terminals, Markdown, Git, and design reviews.

---

## 0. What Problem Are We Solving?

### 🧸 ELI5

We are building a **to‑do list**.

You can:
- Use it by typing commands
- Use it by calling it over the network

No matter *how* you use it, **the rules are the same**.

---

### 👶 Junior Engineer

We are building a **Work Tracker** that:

- Has a **CLI**
- Has an **HTTP API**
- Stores data in **SQLite**, **JSON**, or **Markdown**
- Keeps **business rules in one place**
- Is **easy to test and change**

We explicitly avoid:
- Business logic in the CLI or API
- Database code mixed with commands
- One giant “god service”

---

### 🧠 Architect

We are optimizing for:

- Behavioral clarity
- Use‑case isolation
- Adapter replaceability
- Long‑term maintainability

We apply:

- Hexagonal Architecture (Ports & Adapters)
- Domain‑Driven Design (Evans)
- CQRS (Fowler)
- Dispatcher + Repository patterns

---

## 1. Big Picture Architecture (Zones + Ports)

### 🧸 ELI5

Think of a **castle**:

- There are **different gates** for different people (public users vs admins).
- Guards at each gate check who you are and what you’re allowed to do.
- Inside, the castle runs the same rules.
- Outside suppliers bring food and tools (databases, files).

Different gates can lead to **different allowed actions**, even though they all reach the same castle.

---

### 👶 Junior Engineer

We split the system into **zones** and we are explicit about **ports**:

- **Primary (Driving) Adapters** call into the application.
- They do so via **Primary Ports** (interfaces / entrypoints).
- The application uses **Secondary Ports** (interfaces) to reach infrastructure.
- **Secondary (Driven) Adapters** implement those interfaces.

Key idea:

> **Not all adapters expose all capabilities.**  
> A *Public API* might expose only “end-user” use cases, while a *Private/Admin API* exposes additional administration use cases.

---

### 🧠 Architect

A more precise picture separates **(a) adapters**, **(b) ports**, and **(c) capability surfaces**.

#### 1.1 Zone Map (Drilled In)

```text
                                 (PRIMARY / DRIVING SIDE)

   Internet Clients                 Private Network                Operators
         |                                |                          |
         v                                v                          v
+------------------+             +-------------------+        +-----------------+
| Public HTTP API  |             | Private HTTP API  |        | Admin CLI       |
| (end-user)       |             | (admin + internal)|        | (ops/admin)     |
+--------+---------+             +---------+---------+        +--------+--------+
         |                               |                           |
         | calls via Primary Port(s)     | calls via Primary Port(s) |
         v                               v                           v
   +----------------+            +-------------------+       +-------------------+
   | Public Facade  |            | Admin Facade      |       | Admin Facade      |
   | Primary Port   |            | Primary Port      |       | Primary Port      |
   | (interfaces)   |            | (interfaces)      |       | (interfaces)      |
   +--------+-------+            +---------+---------+       +---------+---------+
            \                         /                               /
             \                       /                               /
              \                     /                               /
               v                   v                               v
+------------------------------------------------------------------------------+
|                         APPLICATION ZONE (CQRS)                               |
|  - Dispatcher (command/query routing)                                         |
|  - Middleware (authn/authz, logging, tracing, transactions, metrics)          |
|  - Use cases organized by capability:                                         |
|       * End-User Use Cases (Public Surface)                                   |
|       * Admin Use Cases (Privileged Surface)                                  |
+-------------------------------------+----------------------------------------+
                                      |
                                      v
+------------------------------------------------------------------------------+
|                                 DOMAIN ZONE                                  |
|  - Bounded Contexts (e.g., Projects, WorkItems, Identity/Access)              |
|  - Multiple Aggregate Roots per context                                       |
|  - Domain Events (immutable facts)                                            |
+-------------------------------------+----------------------------------------+
                                      |
                                      v
+------------------------------------------------------------------------------+
|                         SECONDARY PORTS (Interfaces)                          |
|  Repositories: IProjectRepository, IWorkItemRepository, IIdentityRepository   |
|  Read models: IReadModelStore, IProjectionCheckpointStore                     |
|  Messaging: IEventBus, ICommandQueue                                          |
|  Integration: IAdoGateway (Anti-Corruption Layer port)                        |
+-------------------------+----------------------------+------------------------+
                          |                            |
                          v                            v
      (SECONDARY / DRIVEN SIDE)              (SECONDARY / DRIVEN SIDE)

+------------------------------+        +---------------------------------------+
| Persistence Adapters         |        | Messaging / Integration Adapters      |
|                              |        |                                       |
| +--------------------------+ |        | +--------------------+                |
| | SQLite Adapter           | |        | | In-Memory Bus       |                |
| | (implements repositories)| |        | | (dev/test)          |                |
| +--------------------------+ |        | +--------------------+                |
| +--------------------------+ |        | +--------------------+                |
| | File Repository Adapter  | |        | | Queue Adapter       |                |
| | (implements repositories)| |        | | (async commands)    |                |
| +-----------+--------------+ |        | +--------------------+                |
|             |                |        | +--------------------+                |
|             v                |        | | ADO Connector       |                |
|   +-----------------------+  |        | | (implements IAdo...)|                |
|   | Markdown Adapter      |  |        | +--------------------+                |
|   +-----------------------+  |        +---------------------------------------+
|   +-----------------------+  |
|   | JSON Adapter          |  |
|   +-----------------------+  |
+------------------------------+
```

**Key clarifications (answering your question directly):**

- **Primary ports are capability surfaces**, not “the whole application.”
  - Public API calls the **Public Primary Port** (end-user surface).
  - Private/Admin API and Admin CLI call the **Admin Primary Port** (privileged surface).
- The **same underlying domain** can be exercised by different surfaces, but each surface is intentionally constrained.
- On the secondary side, the chain is explicit: **IRepository ← FileRepository ← Markdown/JSON adapter**.

---

## 2. Hexagonal Architecture (Ports & Adapters)

### 🧸 ELI5

The core logic is in the middle.

Everything else plugs in like USB devices.

---

### 👶 Junior Engineer

- **Ports** = interfaces owned by the core
- **Adapters** = implementations on the outside

Two adapter types:

```text
Primary (Driving):
- CLI
- HTTP API

Secondary (Driven):
- SQLite
- JSON file
- Markdown file
```

---

### 🧠 Architect

```text
+----------------------------------------------------+
|                    APPLICATION                     |
|                                                    |
|  +-----------+        +-------------------------+ |
|  |   CLI     |        |        HTTP API         | |
|  |  Adapter  |        |        Adapter          | |
|  +-----+-----+        +-----------+-------------+ |
|        |                          |               |
+--------|--------------------------|---------------+
         v                          v
+----------------------------------------------------+
|              APPLICATION LAYER (CQRS)              |
|        Use Cases / Commands / Queries               |
+--------------------------+-------------------------+
                           |
                           v
+----------------------------------------------------+
|                   DOMAIN                           |
|         Entities, Value Objects, Rules              |
+--------------------------+-------------------------+
                           |
                           v
+----------------------------------------------------+
|               REPOSITORY PORT                      |
+------------+---------------+----------------------+
             |               |
             v               v
     +-------------+   +-------------+
     |  SQLite     |   | JSON / MD   |
     |  Adapter    |   | Adapter     |
     +-------------+   +-------------+
```

> **Rule:** The domain owns abstractions. Infrastructure owns implementations.

---

## 3. Domain Model (DDD Core)

### 🧸 ELI5

A **Work Item** is a thing you need to do.

It knows when it can change.

---

### 👶 Junior Engineer

Domain concepts:
- `WorkItem` (entity)
- `Status` (value)

Rules live **inside the entity**, not the UI.

---

### 🧠 Architect

```text
WorkItem (Aggregate Root)
|
+-- id
+-- title
+-- status
|
+-- complete()
|     - if already DONE -> error
|
+-- rename()
      - title must not be empty
```

Guarantees:
- One source of truth
- No rule duplication
- Adapter‑agnostic correctness

---

## 4. Application Layer (Use Cases / CQRS)

### 🧸 ELI5

This layer answers:

> “What is the user trying to do?”

---

### 👶 Junior Engineer

Commands (write):
- AddWorkItem
- CompleteWorkItem

Queries (read):
- ListWorkItems
- GetWorkItem

Each use case does **one thing**.

---

### 🧠 Architect

```text
COMMAND FLOW:
Adapter -> Command -> Domain -> Repository

QUERY FLOW:
Adapter -> Query  -> Repository -> DTO
```

With dispatcher:

```text
+-----------+     +-------------+     +---------+
| Adapter   | --> | Dispatcher  | --> | UseCase |
+-----------+     +-------------+     +---------+
                                     |
                                     v
                                  +------+
                                  |Domain|
                                  +------+
```

---

## 5. Dispatcher Pattern

### 🧸 ELI5

The dispatcher is a **traffic cop**.

---

### 👶 Junior Engineer

Both CLI and API go through the dispatcher:

```text
CLI -> Dispatcher -> Use Case
API -> Dispatcher -> Use Case
```

---

### 🧠 Architect

Dispatcher centralizes:
- Logging
- Transactions
- Retries
- Metrics

Without polluting domain logic.

---

## 6. Repository Pattern (Ports, Secondary Adapters, and the File Repository Chain)

### 🧸 ELI5

The app says:

> “Store this safely.”

It does **not** say:

> “Store this in a database.”

It uses a *plug* (a port) so we can swap storage.

---

### 👶 Junior Engineer

A **repository port** is an interface the application uses: 

```text
IProjectRepository
IWorkItemRepository
```

Then we can have multiple implementations:
- SQLite implementation
- File-based implementation

A **File Repository** can itself delegate to a specific file format adapter:
- Markdown
- JSON

---

### 🧠 Architect

#### 6.1 Secondary Ports (Interfaces) — explicit and typed

```text
interface IProjectRepository:
  - add(Project)
  - get(ProjectId)
  - save(Project)

interface IWorkItemRepository:
  - add(WorkItem)
  - get(WorkItemId)
  - save(WorkItem)

interface IReadModelStore:
  - upsert(ViewRow)
  - query(...)
```

#### 6.2 Secondary Adapter Chain (what you asked for)

```text
            (Application / Domain uses)

  IProjectRepository  IWorkItemRepository
          |                 |
          v                 v
+----------------+   +----------------+
| SQLite Adapter |   | SQLite Adapter |
+----------------+   +----------------+

          OR

  IProjectRepository
          |
          v
+------------------------+
| File Repository Adapter |
| (implements IRepository)|
+-----------+------------+
            |
            | chooses format strategy
            v
   +-------------------+     +-------------------+
   | Markdown Adapter  |     | JSON Adapter      |
   | (read/write .md)  |     | (read/write .json)|
   +-------------------+     +-------------------+
```

#### 6.3 Why have a “File Repository” *and* “Markdown Adapter”?

- **File Repository Adapter**: repository semantics (IDs, concurrency rules, atomic writes, indexing strategy)
- **Markdown/JSON Adapter**: encoding/decoding and file format details

This separation prevents the repository from becoming “a pile of parsing.”

---

## 7. CLI Adapter (Primary Adapter calling Primary Ports)

### 🧸 ELI5

CLI is a **remote control**.

It only presses buttons.
It doesn’t contain the rules.

---

### 👶 Junior Engineer

We often need **two CLIs** in real systems:

- **End-user CLI** (safe, limited)
- **Admin CLI** (powerful, privileged)

Both should call the application via a **Primary Port** — not by reaching into use-case classes directly.

---

### 🧠 Architect

#### 7.1 Two CLI surfaces, two primary ports

```text
+------------------+         +------------------+
| User CLI Adapter |         | Admin CLI Adapter|
+--------+---------+         +--------+---------+
         |                            |
         v                            v
+------------------+         +------------------+
| IPublicFacade    |         | IAdminFacade     |
| (Primary Port)   |         | (Primary Port)   |
+--------+---------+         +--------+---------+
         \                            /
          \                          /
           v                        v
              +------------------+
              | Application (CQRS)|
              +------------------+
```

#### 7.2 Why facades as primary ports?

- They define **capability boundaries** (what this surface is allowed to do)
- They keep adapters from "knowing too much" about internal organization
- They allow different authentication/authorization and rate-limits per surface

---

## 8. HTTP API Adapter (Public vs Private Surfaces)

### 🧸 ELI5

We can have:

- A **front door** for normal people
- A **staff door** for employees

Both reach the same building, but staff can go to more rooms.

---

### 👶 Junior Engineer

We usually expose **different APIs** for different audiences:

- **Public API** (internet-facing)
  - safer
  - limited operations
  - strict throttling
- **Private/Admin API** (private network)
  - more operations
  - internal tooling
  - elevated privileges

Both should call the application via **primary ports**.

---

### 🧠 Architect

#### 8.1 Explicit port separation (answering your question)

> **No: it is not the entire application functionality that is exposed by a port.**
> A port is a *designed surface* (a contract) for a particular audience.

```text
Internet Clients
   |
   v
+-------------------+
| Public API Adapter |
+---------+---------+
          |
          v
+-------------------+
| IPublicFacade     |  (Primary Port: end-user capabilities)
+---------+---------+
          |
          v
      Application

Private Network
   |
   v
+--------------------+
| Private API Adapter |
+----------+---------+
           |
           v
+--------------------+
| IAdminFacade       |  (Primary Port: admin + internal capabilities)
+----------+---------+
           |
           v
       Application
```

#### 8.2 Example: capability slicing

```text
IPublicFacade:
  - createProject
  - addWorkItem
  - listMyWork

IAdminFacade:
  - reindexReadModels
  - importFromAdo
  - deleteProjectHard
  - rebuildProjections
  - manageTenants
```

#### 8.3 Cross-cutting policies differ per port

- **Authentication**: public uses tokens; admin may use mutual Transport Layer Security (mTLS)
- **Authorization**: admin requires privileged roles
- **Rate limits**: aggressive on public
- **Auditing**: stricter on admin

These differences are easiest to manage when the **ports are separate**.

---
## 9. Behavior‑Driven Design Alignment

### 🧸 ELI5

We write code that matches stories.

---

### 👶 Junior Engineer

```text
Given a task
When I complete it
Then it is DONE
```

---

### 🧠 Architect

Each use case is:
- Auditable
- Testable
- Replaceable

Living documentation.

---

## 10. Summary

### 🧸 ELI5

Buttons ask.
Rules decide.
Storage remembers.

---

### 👶 Junior Engineer

```text
CLI/API -> Use Case -> Domain -> Repository
```

---

### 🧠 Architect

This architecture:
- Scales cognitively
- Scales organizationally
- Survives change

---

## References & Prior Art

1. Eric Evans – *Domain‑Driven Design* (Addison‑Wesley, 2004)
2. Martin Fowler – *CQRS* (martinfowler.com)
3. Alistair Cockburn – *Hexagonal Architecture* (2005)
4. AWS Prescriptive Guidance – *Hexagonal Architecture Pattern*
5. Vaughn Vernon – *Implementing Domain‑Driven Design*
6. Dan North – *Introducing BDD*
7. Sairyss – *Domain‑Driven Hexagon* (GitHub)

---

\*End of document\.\*

---

# Appendix A — Language-Specific Reference Architectures (Expanded)

> This appendix explicitly answers:
> - Where **materialized views** live
> - Where **schemas** live
> - Where **primary vs secondary ports** live
> - How **adapters map to ports**
> - What **files actually exist** in each folder

---

## A.1 Python Project Layout (DDD + CQRS + Event-Ready)

```text
project-tracker/
├── pyproject.toml
├── README.md
├── docs/
│   ├── architecture.md
│   ├── adr/
│   │   ├── 0001-use-cqrs.md
│   │   ├── 0002-public-vs-admin-ports.md
│   │   └── 0003-event-naming.md
│   ├── schemas/
│   │   ├── commands/
│   │   │   ├── create_work_item.v1.json
│   │   │   └── complete_work_item.v1.json
│   │   ├── events/
│   │   │   ├── work_item_created.v1.json
│   │   │   ├── work_item_completed.v1.json
│   │   ├── queries/
│   │   │   └── project_dashboard.v1.json
│   │   ├── protobuf/
│   │   │   └── work_item_events.v1.proto
│   │   └── README.md
│   └── naming-conventions.md
├── src/
│   └── project_tracker/
│       ├── bootstrap.py
│       ├── domain/
│       │   ├── work_item/
│       │   │   ├── entities.py          # WorkItem aggregate
│       │   │   ├── events.py            # WorkItemCreated, Completed
│       │   │   └── ids.py
│       │   └── project/
│       │       ├── entities.py
│       │       └── events.py
│       ├── application/
│       │   ├── commands/
│       │   │   ├── create_work_item.py  # CreateWorkItem
│       │   │   └── complete_work_item.py
│       │   ├── queries/
│       │   │   └── get_project_dashboard.py
│       │   ├── ports/
│       │   │   ├── primary/
│       │   │   │   ├── public_facade.py   # IPublicFacade
│       │   │   │   └── admin_facade.py    # IAdminFacade
│       │   │   └── secondary/
│       │   │       ├── repositories.py   # IWorkItemRepository
│       │   │       ├── read_models.py    # IReadModelStore
│       │   │       └── event_bus.py
│       │   ├── dispatching/
│       │   │   └── dispatcher.py
│       │   └── projections/
│       │       ├── project_dashboard.py  # Materialized view builder
│       │       └── checkpoints.py
│       ├── infrastructure/
│       │   ├── persistence/
│       │   │   ├── sqlite/
│       │   │   │   ├── work_item_repo.py
│       │   │   ├── file_repository/
│       │   │   │   ├── file_repo.py
│       │   │   │   ├── markdown_adapter.py
│       │   │   │   └── json_adapter.py
│       │   ├── read_models/
│       │   │   ├── sqlite_views.py        # Materialized views storage
│       │   └── messaging/
│       │       └── in_memory_bus.py
│       ├── adapters/
│       │   ├── cli/
│       │   │   └── user_cli.py
│       │   └── http/
│       │       └── public_api.py
│       └── shared/
│           └── logging.py
└── tests/
```

### Where materialized views live

- **Code**: `application/projections/`
- **Storage**: `infrastructure/read_models/`
- **Port**: `application/ports/secondary/read_models.py`

> Materialized views are *not domain models* and must never live in the domain.

---

### Where schemas live (why outside src/)

Schemas are **contracts**, not implementation details.

- Shared across services
- Versioned independently
- Used for validation, codegen, and governance

This aligns with practices from Kafka, AsyncAPI, and OpenAPI ecosystems.

---

## A.2 C# Project Layout (Mirrors Python)

```text
ProjectTracker.Domain/
  WorkItems/WorkItem.cs
  WorkItems/Events/WorkItemCreated.cs

ProjectTracker.Application/
  Commands/CreateWorkItem.cs
  Queries/GetProjectDashboard.cs
  Ports/Primary/IPublicFacade.cs
  Ports/Secondary/IWorkItemRepository.cs
  Projections/ProjectDashboardProjection.cs

ProjectTracker.Infrastructure/
  Persistence/Sqlite/
  Persistence/FileRepository/
  ReadModels/Sqlite/

ProjectTracker.Adapters.Api/
  Controllers/Public/
  Controllers/Admin/
```

---

# Appendix B — Naming Conventions, Commands, Events & Why They Matter

## B.1 Canonical Naming Pattern

```text
Command: CreateWorkItem
Event:   WorkItemCreated

Command: CompleteWorkItem
Event:   WorkItemCompleted
```

### Why this matters (ELI5)

Commands are **requests**.
Events are **facts**.

Requests may fail.
Facts never lie.

---

### Junior Engineer Explanation

- Commands are **imperative** ("Do this")
- Events are **past tense** ("This happened")

This convention allows:
- Clear logs
- Clear audits
- Clear mental models

---

### Architect Explanation

This follows guidance from:
- Martin Fowler (CQRS)
- Greg Young (Event Sourcing)
- Vaughn Vernon (DDD)

> Events represent *something the domain agrees has happened*.

---

## B.2 Why 1:1 Command → Event Matters

### Good

```text
CreateWorkItem → WorkItemCreated
```

### Dangerous

```text
CreateWorkItem → WorkItemCreated + ProjectUpdated + MetricsAdjusted
```

---

### What breaks if you violate 1:1

| Problem | Consequence |
|------|-------------|
| Multiple events per command | Hard to reason about causality |
| Generic events ("ItemChanged") | Loss of semantic meaning |
| Hidden side effects | Impossible auditing |
| Event replay ambiguity | Broken projections |

---

### Industry Prior Art

- Greg Young: *"If you can’t name the event clearly, you don’t understand the behavior"*
- Martin Fowler: Event names should be "business meaningful facts"
- AWS EventBridge best practices: Avoid generic events

---

### Exception (advanced)

Sagas may **react** to events and emit new events — but this is **explicit orchestration**, not a single command doing many things.

---

# Appendix C — Executable Mental Models

## B.1 What Breaks If You Violate the Rules?

| Violation | What Breaks |
|---------|-------------|
| Domain depends on DB | Cannot test business logic without DB |
| CLI contains logic | API and CLI drift apart |
| Use case does multiple things | Tests become brittle |
| No dispatcher | Cross-cutting concerns scatter |
| Shared DB schema across contexts | Accidental coupling |

---

## B.2 Architectural Smells

```text
SMELL: "Just this once" logic in adapters
SMELL: Repository returns ORM entities
SMELL: Cross-aggregate writes in one transaction
SMELL: Queries reusing command models
SMELL: Direct calls between bounded contexts
```

If you smell these, **stop and refactor**.

---

# Appendix C — Team Playbook

## C.1 Do / Don’t Table

| Do | Don’t |
|----|------|
| One use case per command | God services |
| Domain-first modeling | Schema-first design |
| Explicit ports | Hidden dependencies |
| Separate read models | Reuse aggregates for queries |

---

## C.2 PR Review Checklist

```text
[ ] Does this change add or modify a use case?
[ ] Are domain rules enforced in the domain?
[ ] Are adapters thin?
[ ] Are ports/interfaces used?
[ ] Are read models separate?
[ ] Are schemas versioned?
```

---

## C.3 Onboarding Exercises

1. Add a new command without touching adapters
2. Swap SQLite for JSON without code changes
3. Add a projection without modifying domain
4. Introduce a breaking change safely

---

# Appendix D — CQRS + Event-Driven Evolution

## D.1 Async Commands

```text
CLI/API -> Command -> Queue -> Handler
```

Allows:
- Retries
- Backpressure
- Distributed execution

---

## D.2 Event Sourcing Readiness

```text
Command -> Event -> Projection -> Read Model
```

Requirements:
- Immutable events
- Versioned schemas
- Idempotent handlers

---

## D.3 Sagas / Process Managers

```text
ProjectCreated
   -> InitializeBacklog
   -> AllocateResources
   -> NotifyStakeholders
```

Rules:
- No direct cross-aggregate calls
- State machine per workflow

---

# Appendix E — Anti-Corruption Layer (ACL)

```text
External System (ADO)
      |
      v
+--------------------+
|  ACL Translator    |
+--------------------+
      |
      v
Internal Domain Model
```

ACL responsibilities:
- Schema translation
- Semantic mapping
- Version isolation

---

# Appendix F — Schema & Versioning Strategy

- JSON Schema for commands/events
- Protobuf for internal messaging
- Semantic versioning per bounded context
- Never break consumers

---

*Document extended. End of appendices.*

