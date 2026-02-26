# SAFe Domain Model Analysis

> **Document ID:** PROJ-006-SAFE-MODEL
> **Date:** 2026-01-13
> **Author:** ps-analyst (EN-002 Phase 2)
> **Project:** PROJ-006-worktracker-ontology
> **Input:** PROJ-006-SAFE-RAW.md (Research Document)
> **Status:** COMPLETE

---

## Executive Summary

This document presents a structured domain model extracted from SAFe (Scaled Agile Framework) research.
It catalogs entities, properties, behaviors, relationships, and Kanban state machines across all four
SAFe hierarchy levels. This model serves as the foundation for the Jerry worktracker ontology design.

---

## 1. Hierarchy Overview

```
SAFe Framework Hierarchy
========================

Portfolio Level (Strategic)
├── Epic (Business | Enabler)
│   ├── Strategic Theme
│   ├── Investment Theme
│   └── Lean Business Case
│
Large Solution Level (Coordination) [Optional]
├── Capability (Business | Enabler)
│   └── Solution Vision
│
Program/ART Level (Execution)
├── Feature (Business | Enabler)
│   ├── PI Objectives
│   └── Vision
│
Team Level (Delivery)
├── Story (User | Enabler)
│   ├── Exploration (Spike)
│   ├── Architecture
│   ├── Infrastructure
│   └── Compliance
└── Task
```

### Configuration Variants

| Configuration | Levels Active | Use Case |
|---------------|---------------|----------|
| Essential SAFe | Team + Program | Single ART, basic building block |
| Large Solution SAFe | Team + Program + Solution | Multiple ARTs, complex solutions |
| Portfolio SAFe | Team + Program + Portfolio | Strategy and investment governance |
| Full SAFe | All Four Levels | Largest enterprises |

---

## 2. Entity Catalog by Level

### 2.1 Portfolio Level

| Entity | Description | Type | Subtypes |
|--------|-------------|------|----------|
| **Epic** | Significant solution development initiative requiring portfolio-level oversight | Work Item | Business Epic, Enabler Epic |
| **Strategic Theme** | Business objectives connecting portfolio to enterprise strategy | Planning Artifact | - |
| **Investment Theme** | Funding categories directing budget allocation | Planning Artifact | - |
| **Lean Business Case** | Analysis document supporting Go/No-Go decisions for Epics | Document | - |
| **Portfolio Backlog** | Prioritized list of Epics awaiting implementation | Container | - |
| **Portfolio Kanban** | Visual management system for Epic flow | Workflow | - |

#### Epic Subtypes by Scope

| Subtype | Scope | Decision Criteria |
|---------|-------|-------------------|
| Programme Epic | Single ART, multiple PIs | Below portfolio threshold |
| Solution Epic | Single Solution Train, multiple PIs | Below portfolio threshold |
| Portfolio Epic | Multiple Solution Trains or exceeds threshold | Above portfolio threshold |

### 2.2 Large Solution Level

| Entity | Description | Type | Subtypes |
|--------|-------------|------|----------|
| **Capability** | Large solution functionality spanning multiple ARTs, sized to deliver within a PI | Work Item | Business Capability, Enabler Capability |
| **Solution Vision** | Description of the future state of the solution | Planning Artifact | - |
| **Solution Roadmap** | Timeline of capability delivery | Planning Artifact | - |
| **Solution Backlog** | Prioritized list of Capabilities | Container | - |
| **Solution Kanban** | Visual management system for Capability flow | Workflow | - |

### 2.3 Program/ART Level

| Entity | Description | Type | Subtypes |
|--------|-------------|------|----------|
| **Feature** | Product/solution functionality delivering business value within a PI | Work Item | Business Feature, Enabler Feature |
| **PI Objective** | Business/technical goals for a Program Increment | Planning Artifact | Committed, Uncommitted |
| **Vision** | Description of the future state of the solution for the ART | Planning Artifact | - |
| **Program Roadmap** | Timeline of feature delivery | Planning Artifact | - |
| **ART Backlog** | Prioritized list of Features | Container | - |
| **ART Kanban** | Visual management system for Feature flow | Workflow | - |
| **Program Increment (PI)** | 8-12 week timebox for value delivery | Timebox | - |

### 2.4 Team Level

| Entity | Description | Type | Subtypes |
|--------|-------------|------|----------|
| **Story** | Small piece of desired functionality from user perspective | Work Item | User Story, Enabler Story |
| **Task** | Smallest unit of work, decomposed from Stories | Work Item | - |
| **Iteration Goal** | Objectives for the 2-week sprint | Planning Artifact | - |
| **Team Backlog** | Prioritized list of Stories and Tasks | Container | - |
| **Team Kanban** | Visual management system for Story/Task flow | Workflow | - |
| **Iteration** | 2-week timebox for sprint execution | Timebox | - |

#### Enabler Story Subtypes

| Subtype | Description | Purpose |
|---------|-------------|---------|
| **Exploration (Spike)** | Research to understand options | Reduce uncertainty |
| **Architecture** | Design components and relationships | Build architectural runway |
| **Infrastructure** | Work on solution infrastructure | Enable delivery |
| **Compliance** | Regulatory and audit requirements | Meet compliance needs |

---

## 3. Entity Properties

### 3.1 Epic Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Unique identifier |
| `name` | string | Yes | Brief phrase description |
| `epic_owner` | string | Yes | Accountable individual who shepherds the epic |
| `type` | enum(Business, Enabler) | Yes | Classification for business value vs technical enablement |
| `subtype` | enum(Programme, Solution, Portfolio) | No | Scope classification |
| `description` | text | Yes | High-level overview of organizational need |
| `business_outcome_hypothesis` | text | Yes | Testable assertion about expected outcomes |
| `leading_indicators` | list[string] | Yes | Early signals tracking epic progress |
| `nfrs` | list[NFR] | No | Non-functional requirements |
| `mvp_definition` | text | Yes* | Minimum Viable Product scope (*required for Analyzing) |
| `lean_business_case` | LeanBusinessCase | Yes* | Cost, value, duration, risk evaluation (*required for Go) |
| `wsjf_score` | number | Yes | Weighted Shortest Job First priority score |
| `cost_estimate_mvp` | number | Yes | Preliminary MVP cost estimate |
| `cost_estimate_full` | number | No | Full implementation cost estimate |
| `state` | PortfolioKanbanState | Yes | Current state in Portfolio Kanban |
| `strategic_theme` | string | No | Aligned strategic theme |
| `investment_theme` | string | No | Budget allocation theme |

#### Lean Business Case Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `epic_brief` | text | Yes | Overview including key stakeholders and hypothesis |
| `scope_and_mvp` | text | Yes | In/out of scope, MVP features |
| `analysis_summary` | text | Yes | Go/No-Go decision summary |
| `analysis_of_solution` | text | Yes | Impact analysis on clients and departments |
| `cost_estimates` | CostEstimates | Yes | Preliminary and updated estimates |
| `development_approach` | text | Yes | In-house vs outsourced, dependencies |

### 3.2 Capability Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Unique identifier |
| `name` | string | Yes | Brief phrase description |
| `type` | enum(Business, Enabler) | Yes | Classification |
| `description` | text | Yes | Detailed description |
| `benefit_hypothesis` | text | Yes | Validatable statement of expected benefit |
| `acceptance_criteria` | list[string] | Yes | Criteria for determining completion |
| `parent_epic_id` | string | No | Reference to parent Epic |
| `nfrs` | list[NFR] | No | Non-functional requirements constraints |
| `wsjf_score` | number | Yes | Priority score |
| `state` | SolutionKanbanState | Yes | Current state in Solution Kanban |
| `target_pi` | string | No | Target Program Increment for delivery |

### 3.3 Feature Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Unique identifier |
| `name` | string | Yes | Brief phrase description |
| `type` | enum(Business, Enabler) | Yes | Classification |
| `description` | text | Yes | Detailed description |
| `benefit_hypothesis` | text | Yes | Validatable statement of expected benefit |
| `acceptance_criteria` | list[string] | Yes | Completion criteria including NFRs |
| `parent_capability_id` | string | No | Reference to parent Capability |
| `parent_epic_id` | string | No | Reference to parent Epic (if no Capability) |
| `nfrs` | list[NFR] | No | Non-functional requirements |
| `wsjf_score` | number | Yes | Priority score |
| `state` | ARTKanbanState | Yes | Current state in ART Kanban |
| `target_pi` | string | No | Target Program Increment |
| `mmf` | text | No | Minimum Marketable Feature scope |

### 3.4 Story Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Unique identifier |
| `title` | string | Yes | Brief description |
| `type` | enum(User, Enabler) | Yes | Story classification |
| `enabler_subtype` | enum(Exploration, Architecture, Infrastructure, Compliance) | If Enabler | Enabler classification |
| `description` | text | Yes | Full story description |
| `acceptance_criteria` | list[string] | Yes | Testable criteria for completion |
| `story_points` | number | Yes | Relative effort estimate |
| `parent_feature_id` | string | Yes | Reference to parent Feature |
| `state` | TeamKanbanState | Yes | Current workflow state |
| `iteration` | string | No | Target iteration |
| `team` | string | Yes | Assigned team |
| `product_owner` | string | Yes | PO responsible for acceptance |

### 3.5 Task Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Unique identifier |
| `title` | string | Yes | Brief description |
| `description` | text | No | Detailed description |
| `parent_story_id` | string | Yes | Reference to parent Story |
| `assignee` | string | Yes | Assigned team member |
| `estimated_hours` | number | No | Time estimate in hours |
| `remaining_hours` | number | No | Remaining work in hours |
| `state` | enum(NotStarted, InProgress, Done) | Yes | Current state |

### 3.6 Non-Functional Requirement (NFR) Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Unique identifier |
| `category` | enum(FURPS+) | Yes | Functionality, Usability, Reliability, Performance, Supportability, Plus |
| `description` | text | Yes | NFR description |
| `measure` | text | No | How to measure compliance |
| `threshold` | text | No | Acceptance threshold |

---

## 4. Entity Behaviors

### 4.1 Epic Behaviors

| Behavior | Description | Preconditions | Postconditions |
|----------|-------------|---------------|----------------|
| `create` | Create new Epic in Funnel state | Valid name, owner, type | Epic in FUNNEL state |
| `advance_to_reviewing` | Move Epic to Reviewing state | In FUNNEL, basic hypothesis | Epic in REVIEWING state |
| `advance_to_analyzing` | Move Epic to Analyzing state | In REVIEWING, WSJF calculated | Epic in ANALYZING state |
| `advance_to_ready` | Move Epic to Ready state | In ANALYZING, MVP defined, LBC complete | Epic in READY state |
| `start_mvp` | Begin MVP implementation | In READY, capacity available | Epic in IMPLEMENTING_MVP state |
| `persevere` | Continue past MVP | In IMPLEMENTING_MVP, hypothesis validated | Epic in IMPLEMENTING_PERSEVERE state |
| `complete` | Mark Epic as done | In IMPLEMENTING, all children done | Epic in DONE state |
| `reject` | Abandon Epic (No-Go decision) | In REVIEWING or ANALYZING | Epic in DONE state (No-Go) |
| `pivot` | Change direction based on learnings | In IMPLEMENTING_MVP, hypothesis disproven | Epic reassessed |
| `calculate_wsjf` | Calculate priority score | CoD components and job size available | WSJF score set |
| `decompose` | Split into Capabilities or Features | In ANALYZING or later | Child items created |

### 4.2 Capability Behaviors

| Behavior | Description | Preconditions | Postconditions |
|----------|-------------|---------------|----------------|
| `create` | Create new Capability | Valid name, type, parent Epic (optional) | Capability in FUNNEL state |
| `advance_to_analyzing` | Move to Analyzing state | In FUNNEL, basic definition | Capability in ANALYZING state |
| `advance_to_backlog` | Move to Solution Backlog | In ANALYZING, fully defined | Capability in SOLUTION_BACKLOG state |
| `start_implementation` | Begin implementation | In SOLUTION_BACKLOG, PI planned | Capability in IMPLEMENTING state |
| `complete` | Mark as done | In IMPLEMENTING, all Features done | Capability in DONE state |
| `decompose` | Split into Features | In ANALYZING or later | Child Features created |
| `calculate_wsjf` | Calculate priority score | CoD components and job size available | WSJF score set |

### 4.3 Feature Behaviors

| Behavior | Description | Preconditions | Postconditions |
|----------|-------------|---------------|----------------|
| `create` | Create new Feature | Valid name, type, parent (optional) | Feature in FUNNEL state |
| `advance_to_review` | Move to Business Review | In FUNNEL, basic definition | Feature in BUSINESS_REVIEW state |
| `advance_to_backlog` | Move to ART Backlog | In BUSINESS_REVIEW, approved | Feature in ART_BACKLOG state |
| `reject` | Reject from Business Review | In BUSINESS_REVIEW, not approved | Feature removed or archived |
| `start_implementation` | Begin implementation | In ART_BACKLOG, PI planned | Feature in IMPLEMENTING state |
| `complete` | Mark as done | In IMPLEMENTING, all Stories done | Feature in DONE state |
| `decompose` | Split into Stories | In BUSINESS_REVIEW or later | Child Stories created |
| `calculate_wsjf` | Calculate priority score | CoD components and job size available | WSJF score set |

### 4.4 Story Behaviors

| Behavior | Description | Preconditions | Postconditions |
|----------|-------------|---------------|----------------|
| `create` | Create new Story | Valid title, type, parent Feature | Story in BACKLOG state |
| `refine` | Move to Ready state | In BACKLOG, acceptance criteria defined | Story in READY state |
| `start` | Begin work on Story | In READY, pulled into iteration | Story in IN_PROGRESS state |
| `submit_for_review` | Move to Review state | In IN_PROGRESS, implementation complete | Story in REVIEW state |
| `complete` | Mark as Done | In REVIEW, passes DoD | Story in DONE state |
| `accept` | PO acceptance | In DONE, PO verified | Story in ACCEPTED state |
| `reject` | Reject back to In Progress | In REVIEW, issues found | Story in IN_PROGRESS state |
| `rollover` | Move to next iteration | Incomplete at iteration end | Story remains in backlog |
| `cancel` | Cancel Story | Any state, no longer needed | Story cancelled |
| `decompose` | Split into Tasks | After creation | Child Tasks created |
| `estimate` | Set story points | After refinement | Story points assigned |

### 4.5 Task Behaviors

| Behavior | Description | Preconditions | Postconditions |
|----------|-------------|---------------|----------------|
| `create` | Create new Task | Valid title, parent Story | Task in NOT_STARTED state |
| `start` | Begin work | In NOT_STARTED, assignee available | Task in IN_PROGRESS state |
| `complete` | Mark as done | In IN_PROGRESS, work complete | Task in DONE state |
| `reassign` | Change assignee | Any active state | Assignee updated |
| `update_estimate` | Update remaining hours | Any state | Remaining hours updated |

---

## 5. Relationships

### 5.1 Containment Relationships (Parent-Child Decomposition)

| From | Relationship | To | Cardinality | Cross-Level | Description |
|------|--------------|----|-----------:|-------------|-------------|
| Epic | `contains` | Capability | 1:N | Yes (Portfolio -> Solution) | Epic decomposes into Capabilities |
| Epic | `contains` | Feature | 1:N | Yes (Portfolio -> Program) | Epic directly decomposes into Features (no Solution level) |
| Capability | `contains` | Feature | 1:N | Yes (Solution -> Program) | Capability decomposes into Features |
| Feature | `contains` | Story | 1:N | Yes (Program -> Team) | Feature decomposes into Stories |
| Story | `contains` | Task | 1:N | No (Team) | Story decomposes into Tasks |

### 5.2 Realization Relationships (Bottom-Up Value Delivery)

| From | Relationship | To | Cardinality | Cross-Level | Description |
|------|--------------|----|-----------:|-------------|-------------|
| Capability | `realizes` | Epic | N:1 | Yes (Solution -> Portfolio) | Capability contributes to Epic realization |
| Feature | `realizes` | Capability | N:1 | Yes (Program -> Solution) | Feature contributes to Capability realization |
| Feature | `realizes` | Epic | N:1 | Yes (Program -> Portfolio) | Feature directly realizes Epic (no Solution level) |
| Story | `realizes` | Feature | N:1 | Yes (Team -> Program) | Story contributes to Feature realization |

### 5.3 Dependency Relationships

| From | Relationship | To | Cardinality | Cross-Level | Description |
|------|--------------|----|-----------:|-------------|-------------|
| Any | `depends_on` | Any | N:M | Yes | Item requires another to be completed first |
| Any | `blocked_by` | Any | N:M | Yes | Item cannot proceed until blocker resolved |
| Any | `related_to` | Any | N:M | Yes | Items share context or affect each other |

### 5.4 Assignment Relationships

| From | Relationship | To | Cardinality | Description |
|------|--------------|----|-----------:|-------------|
| Epic | `owned_by` | Epic Owner | N:1 | Epic accountability |
| Story | `owned_by` | Product Owner | N:1 | Story acceptance responsibility |
| Story | `assigned_to` | Team | N:1 | Team responsible for delivery |
| Task | `assigned_to` | Team Member | N:1 | Individual work assignment |

### 5.5 Temporal Relationships

| From | Relationship | To | Cardinality | Description |
|------|--------------|----|-----------:|-------------|
| Capability | `targets` | PI | N:1 | Target Program Increment |
| Feature | `targets` | PI | N:1 | Target Program Increment |
| Story | `scheduled_in` | Iteration | N:1 | Iteration assignment |

### 5.6 Relationship Matrix

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          RELATIONSHIP MATRIX                                 │
├─────────────┬───────────┬────────────┬─────────┬─────────┬──────────────────┤
│             │   Epic    │ Capability │ Feature │  Story  │      Task        │
├─────────────┼───────────┼────────────┼─────────┼─────────┼──────────────────┤
│ Epic        │     -     │  contains  │contains │    -    │        -         │
│             │           │ realized_by│realized_│         │                  │
├─────────────┼───────────┼────────────┼─────────┼─────────┼──────────────────┤
│ Capability  │  realizes │     -      │contains │    -    │        -         │
│             │ child_of  │            │realized_│         │                  │
├─────────────┼───────────┼────────────┼─────────┼─────────┼──────────────────┤
│ Feature     │  realizes │  realizes  │    -    │contains │        -         │
│             │ child_of  │  child_of  │         │realized_│                  │
├─────────────┼───────────┼────────────┼─────────┼─────────┼──────────────────┤
│ Story       │     -     │     -      │realizes │    -    │    contains      │
│             │           │            │child_of │         │                  │
├─────────────┼───────────┼────────────┼─────────┼─────────┼──────────────────┤
│ Task        │     -     │     -      │    -    │child_of │        -         │
└─────────────┴───────────┴────────────┴─────────┴─────────┴──────────────────┘

Cross-cutting relationships (any-to-any):
- depends_on, blocked_by, related_to
```

---

## 6. Kanban State Machines

### 6.1 Portfolio Kanban (Epic States)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           PORTFOLIO KANBAN                                       │
│                                                                                  │
│  ┌────────┐   ┌───────────┐   ┌───────────┐   ┌───────┐   ┌──────────────────┐ │
│  │ FUNNEL │──►│ REVIEWING │──►│ ANALYZING │──►│ READY │──►│ IMPLEMENTING_MVP │ │
│  └────────┘   └─────┬─────┘   └─────┬─────┘   └───────┘   └────────┬─────────┘ │
│       │             │               │                              │            │
│       │             ▼               ▼                              ▼            │
│       │        ┌────────┐      ┌────────┐                 ┌────────────────────┐│
│       │        │ DONE   │      │ DONE   │                 │IMPLEMENTING_PERSEV.││
│       │        │(No-Go) │      │(No-Go) │                 └─────────┬──────────┘│
│       │        └────────┘      └────────┘                           │           │
│       │                                                             ▼           │
│       └─────────────────────────────────────────────────────►┌────────┐        │
│                                                               │  DONE  │        │
│                                                               └────────┘        │
└─────────────────────────────────────────────────────────────────────────────────┘

State Enumeration:
- FUNNEL: Initial intake for significant ideas (no WIP limit)
- REVIEWING: Evaluate and refine investments (explicit WIP limit)
- ANALYZING: In-depth viability evaluation (explicit WIP limit)
- READY: Prioritized, waiting for capacity (explicit WIP limit)
- IMPLEMENTING_MVP: Active MVP development (implicit WIP - capacity)
- IMPLEMENTING_PERSEVERE: Continue post-validation (implicit WIP)
- DONE: No longer requires portfolio governance

Transitions:
- FUNNEL → REVIEWING: Epic Hypothesis Statement developed
- REVIEWING → ANALYZING: WSJF calculated, passes initial review
- REVIEWING → DONE: No-Go decision (not worth analyzing)
- ANALYZING → READY: MVP defined, Lean Business Case approved
- ANALYZING → DONE: No-Go decision (not viable)
- READY → IMPLEMENTING_MVP: Capacity available, prioritized
- IMPLEMENTING_MVP → IMPLEMENTING_PERSEVERE: Hypothesis validated
- IMPLEMENTING_MVP → DONE: Hypothesis disproven (pivot/stop)
- IMPLEMENTING_PERSEVERE → DONE: Full implementation complete
```

### 6.2 Solution Kanban (Capability States)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SOLUTION KANBAN                                     │
│                                                                              │
│  ┌────────┐   ┌───────────┐   ┌──────────────────┐   ┌──────────────┐      │
│  │ FUNNEL │──►│ ANALYZING │──►│ SOLUTION_BACKLOG │──►│ IMPLEMENTING │      │
│  └────────┘   └───────────┘   └──────────────────┘   └──────┬───────┘      │
│                                                              │              │
│                                                              ▼              │
│                                                         ┌────────┐         │
│                                                         │  DONE  │         │
│                                                         └────────┘         │
└─────────────────────────────────────────────────────────────────────────────┘

State Enumeration:
- FUNNEL: Initial ideas for capabilities
- ANALYZING: Evaluation and refinement
- SOLUTION_BACKLOG: Prioritized, ready for PI Planning
- IMPLEMENTING: Active development across ARTs
- DONE: Capability delivered

Transitions:
- FUNNEL → ANALYZING: Capability concept defined
- ANALYZING → SOLUTION_BACKLOG: Benefit hypothesis and acceptance criteria complete
- SOLUTION_BACKLOG → IMPLEMENTING: Scheduled into PI, decomposed into Features
- IMPLEMENTING → DONE: All Features complete
```

### 6.3 ART/Program Kanban (Feature States)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ART KANBAN                                         │
│                                                                              │
│  ┌────────┐   ┌─────────────────┐   ┌─────────────┐   ┌──────────────┐     │
│  │ FUNNEL │──►│ BUSINESS_REVIEW │──►│ ART_BACKLOG │──►│ IMPLEMENTING │     │
│  └────────┘   └────────┬────────┘   └─────────────┘   └──────┬───────┘     │
│                        │                                      │             │
│                        ▼                                      ▼             │
│                   ┌──────────┐                           ┌────────┐        │
│                   │ REJECTED │                           │  DONE  │        │
│                   └──────────┘                           └────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘

State Enumeration:
- FUNNEL: Initial placeholder for proposed features
- BUSINESS_REVIEW: Review for alignment with strategy
- REJECTED: Not approved in business review
- ART_BACKLOG: Ready for PI Planning, ranked by WSJF
- IMPLEMENTING: In active development, decomposed into Stories
- DONE: Feature delivered and accepted by Product Management

Transitions:
- FUNNEL → BUSINESS_REVIEW: Feature formally defined
- BUSINESS_REVIEW → ART_BACKLOG: Approved, fully defined with acceptance criteria
- BUSINESS_REVIEW → REJECTED: Not aligned with strategy
- ART_BACKLOG → IMPLEMENTING: Scheduled into PI
- IMPLEMENTING → DONE: All Stories complete, accepted
```

### 6.4 Team Kanban (Story States)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           TEAM KANBAN                                        │
│                                                                              │
│  ┌─────────┐   ┌───────┐   ┌─────────────┐   ┌────────┐   ┌──────┐        │
│  │ BACKLOG │──►│ READY │──►│ IN_PROGRESS │──►│ REVIEW │──►│ DONE │        │
│  └─────────┘   └───────┘   └──────┬──────┘   └───┬────┘   └──┬───┘        │
│                                   │              │           │             │
│                                   │              │           ▼             │
│                                   │              │      ┌──────────┐      │
│                                   │              │      │ ACCEPTED │      │
│                                   │              │      └──────────┘      │
│                                   │              │                        │
│                                   │◄─────────────┘                        │
│                                   │ (rejected back)                       │
│                                                                           │
│  Side states:                                                             │
│  ┌────────────┐   ┌───────────┐                                          │
│  │ INCOMPLETE │   │ CANCELLED │                                          │
│  └────────────┘   └───────────┘                                          │
└─────────────────────────────────────────────────────────────────────────────┘

State Enumeration:
- BACKLOG: Stories waiting to be pulled
- READY: Stories refined with acceptance criteria, ready for work
- IN_PROGRESS: Actively being worked on
- REVIEW: Under review or testing
- DONE: Completed, meets Definition of Done
- ACCEPTED: Product Owner accepted, ready for deployment
- INCOMPLETE: Doesn't meet DoD (rolled to next iteration)
- CANCELLED: No longer required

Transitions:
- BACKLOG → READY: Refinement complete, acceptance criteria defined
- READY → IN_PROGRESS: Pulled into iteration, work started
- IN_PROGRESS → REVIEW: Implementation complete, submitted for review
- REVIEW → DONE: Passes review, meets DoD
- REVIEW → IN_PROGRESS: Issues found, returned for rework
- DONE → ACCEPTED: PO acceptance verified
- IN_PROGRESS → INCOMPLETE: Iteration ends, work not complete
- Any → CANCELLED: Story no longer needed
```

### 6.5 Task States (Simple)

```
┌─────────────────────────────────────────────────────┐
│                    TASK STATES                       │
│                                                      │
│  ┌─────────────┐   ┌─────────────┐   ┌──────┐      │
│  │ NOT_STARTED │──►│ IN_PROGRESS │──►│ DONE │      │
│  └─────────────┘   └─────────────┘   └──────┘      │
└─────────────────────────────────────────────────────┘

State Enumeration:
- NOT_STARTED: Task created but work not begun
- IN_PROGRESS: Actively being worked on
- DONE: Task complete
```

---

## 7. WSJF (Weighted Shortest Job First) Model

### 7.1 Formula

```
WSJF = Cost of Delay / Job Size (Duration)
```

### 7.2 Cost of Delay Components

| Component | Description | Scale |
|-----------|-------------|-------|
| **User/Business Value** | Relative worth to stakeholders | 1, 2, 3, 5, 8, 13, 20 (Fibonacci) |
| **Time Criticality** | Sensitivity to timing delays | 1, 2, 3, 5, 8, 13, 20 |
| **Risk Reduction / Opportunity Enablement** | Strategic value from mitigating risks or enabling future capabilities | 1, 2, 3, 5, 8, 13, 20 |

### 7.3 WSJF Application

```
Cost of Delay = User/Business Value + Time Criticality + Risk Reduction/Opportunity Enablement

WSJF = Cost of Delay / Job Size
```

| Level | Items Prioritized |
|-------|-------------------|
| Portfolio | Epics |
| Solution | Capabilities |
| Program/ART | Features |

---

## 8. Enabler Classification

### 8.1 Enabler Types Across Levels

| Enabler Type | Description | Portfolio | Solution | Program | Team |
|--------------|-------------|-----------|----------|---------|------|
| **Exploration** | Research, prototyping, customer understanding | Enabler Epic | Enabler Capability | Enabler Feature | Spike Story |
| **Architecture** | Construct Architectural Runway | Enabler Epic | Enabler Capability | Enabler Feature | Architecture Story |
| **Infrastructure** | Build/enhance dev and runtime environments | Enabler Epic | Enabler Capability | Enabler Feature | Infrastructure Story |
| **Compliance** | Regulatory requirements, verification, audits | Enabler Epic | Enabler Capability | Enabler Feature | Compliance Story |

---

## 9. NFR Categories (FURPS+)

| Category | Code | Description | Examples |
|----------|------|-------------|----------|
| **Functionality** | F | Feature set, capabilities, security | Authentication, authorization |
| **Usability** | U | Ease of use, aesthetics, documentation | UI design, help system |
| **Reliability** | R | Availability, accuracy, recoverability | 99.9% uptime, data backup |
| **Performance** | P | Response time, throughput, resource usage | < 200ms response, 1000 TPS |
| **Supportability** | S | Testability, maintainability, configurability | Logging, configuration management |
| **Plus (+)** | + | Design constraints, implementation requirements, interface requirements | Technology stack, API standards |

---

## 10. SAFe Cadences and Timeboxes

### 10.1 Program Increment (PI)

| Property | Value |
|----------|-------|
| Duration | 8-12 weeks (shorter preferred) |
| Structure | 4-5 development iterations + 1 Innovation & Planning (IP) iteration |
| Events | PI Planning, Development Iterations, System Demo, IP Iteration, Inspect & Adapt |

### 10.2 Iteration

| Property | Value |
|----------|-------|
| Duration | 2 weeks (typical) |
| Events | Sprint Planning, Daily Standup, Sprint Review, Sprint Retrospective |
| Content | Stories and Tasks from Team Backlog |

---

## Appendix A: State Enumerations (Code-Ready)

### A.1 PortfolioKanbanState

```
enum PortfolioKanbanState {
    FUNNEL,
    REVIEWING,
    ANALYZING,
    READY,
    IMPLEMENTING_MVP,
    IMPLEMENTING_PERSEVERE,
    DONE
}
```

### A.2 SolutionKanbanState

```
enum SolutionKanbanState {
    FUNNEL,
    ANALYZING,
    SOLUTION_BACKLOG,
    IMPLEMENTING,
    DONE
}
```

### A.3 ARTKanbanState

```
enum ARTKanbanState {
    FUNNEL,
    BUSINESS_REVIEW,
    REJECTED,
    ART_BACKLOG,
    IMPLEMENTING,
    DONE
}
```

### A.4 TeamKanbanState (Story)

```
enum TeamKanbanState {
    BACKLOG,
    READY,
    IN_PROGRESS,
    REVIEW,
    DONE,
    ACCEPTED,
    INCOMPLETE,
    CANCELLED
}
```

### A.5 TaskState

```
enum TaskState {
    NOT_STARTED,
    IN_PROGRESS,
    DONE
}
```

### A.6 WorkItemType

```
enum WorkItemType {
    EPIC,
    CAPABILITY,
    FEATURE,
    STORY,
    TASK
}
```

### A.7 EpicType / CapabilityType / FeatureType

```
enum BusinessEnablerType {
    BUSINESS,
    ENABLER
}
```

### A.8 StoryType

```
enum StoryType {
    USER,
    ENABLER
}
```

### A.9 EnablerSubtype

```
enum EnablerSubtype {
    EXPLORATION,
    ARCHITECTURE,
    INFRASTRUCTURE,
    COMPLIANCE
}
```

### A.10 NFRCategory

```
enum NFRCategory {
    FUNCTIONALITY,
    USABILITY,
    RELIABILITY,
    PERFORMANCE,
    SUPPORTABILITY,
    PLUS
}
```

---

## Appendix B: Entity Templates

### B.1 Epic Hypothesis Statement Template

```
For [target audience]
Who [needs/problem]
The [solution name]
IS A [category/type]
THAT [key benefits]
UNLIKE [current state/competitors]
OUR SOLUTION [differentiation]
```

### B.2 Benefit Hypothesis Template (Feature/Capability)

```
We believe this [business outcome] will be achieved if [these users] successfully
achieve [this user outcome] with [this feature].
```

### B.3 User Story Template (3 Cs)

**Card:**
```
As a [user role],
I want [function/capability],
So that [purpose/benefit].
```

**Conversation:** Collaborative clarification discussions (not stored)

**Confirmation:** Acceptance criteria list

### B.4 Enabler Story Template

```
[Technical statement describing the enabler work]

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
```

---

*End of Domain Model Analysis*
