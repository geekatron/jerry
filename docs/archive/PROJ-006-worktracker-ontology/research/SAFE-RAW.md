# SAFe (Scaled Agile Framework) Domain Model Research

> **Document ID:** PROJ-006-SAFE-RAW
> **Date:** 2026-01-13
> **Author:** ps-researcher (EN-002)
> **Project:** PROJ-006-worktracker-ontology
> **Status:** COMPLETE

---

## Executive Summary

This document provides comprehensive research on the Scaled Agile Framework (SAFe) domain model,
covering hierarchy levels, work item types, properties, relationships, and Kanban states.
SAFe provides a scalable approach for enterprises to organize development around value delivery.

---

## 1. SAFe Hierarchy Levels

SAFe organizes work across four distinct levels, each serving a specific organizational purpose:

### 1.1 Portfolio Level (Strategic)

**Purpose:** Establishes organizational strategy, priorities, and investment funding.

> "The Portfolio level is the highest strategic level of SAFe where purpose and objectives
> are specified."
> — [Premier Agile](https://premieragile.com/levels-of-scaled-agile-framework/)

**Characteristics:**
- Manages multiple portfolios in large enterprises
- Handles strategic planning and Lean governance
- Organizes around value streams
- Aligns portfolio execution to enterprise strategy

**Key Roles:**
- Portfolio Managers
- Chief Technical Officer (CTO)
- Chief Product Officers
- Enterprise Architects
- Enterprise Coaches
- Epic Owners

**Key Artifacts:**
- Portfolio Backlog
- Portfolio Kanban
- Business Cases
- Epics (Business and Enabler)
- Product Roadmap
- Strategic Themes
- Investment Themes

---

### 1.2 Large Solution Level (Coordination)

**Purpose:** Coordinates multiple ARTs for complex, large-scale solutions.

> "Large Solution SAFe is used by organizations building large and complex solutions that
> require multiple Agile Release Trains (ARTs) and suppliers."
> — [PM-Partners](https://www.pm-partners.com.au/insights/the-4-levels-of-the-scaled-agile-framework-explained/)

**When Used:**
- Solutions too large for a single ART
- Multi-ART coordination required
- Cyber-physical systems
- System-of-systems initiatives
- Aerospace, defense, government, large enterprise platforms

**Characteristics:**
- Multiple ARTs synchronized and collaborating
- Solution Train coordination
- Cross-ART dependency management
- Quality system development

**Key Roles:**
- Solution Train Engineer (STE)
- Solution Management
- Solution Architect

**Key Artifacts:**
- Solution Backlog
- Solution Kanban
- Capabilities (Business and Enabler)
- Solution Roadmap
- Solution Vision

---

### 1.3 Program/ART Level (Execution)

**Purpose:** Delivers value through coordinated Agile Release Trains.

> "An Agile Release Train is a team of Agile Teams aligned to a set of shared business
> and technology goals. It functions as a long-lived team that incrementally develops,
> delivers, and often operates one or more solutions."
> — [SAFe Official](https://framework.scaledagile.com/agile-release-train/)

**Characteristics:**
- 50-125 people organized as multiple agile teams
- Cross-functional units containing all capabilities
- Works in Program Increments (8-12 weeks)
- Holds regular ART events

**Key Roles:**
- Release Train Engineer (RTE)
- Product Management
- System Architect
- Business Owners

**Key Artifacts:**
- ART Backlog (Program Backlog)
- ART Kanban (Program Kanban)
- Features (Business and Enabler)
- PI Objectives
- Program Roadmap
- Vision

---

### 1.4 Team Level (Delivery)

**Purpose:** Delivers iterative value through sprints/iterations.

> "At the foundation of SAFe are Agile teams. These are cross-functional groups—typically
> 5-11 people—who use Scrum, Kanban, or a hybrid approach."
> — [Agile Hive](https://agile-hive.com/blog/from-team-to-portfolio-understanding-safes-four-levels-with-agile-hive/)

**Characteristics:**
- Small teams (5-11 members)
- 2-week iterations/sprints
- Scrum or Kanban methodology
- Foundation for all SAFe implementation

**Key Roles:**
- Scrum Master / Team Coach
- Product Owner
- Developers
- Testers
- Business Analysts

**Key Artifacts:**
- Team Backlog
- Team Kanban
- Stories (User and Enabler)
- Tasks
- Iteration Goals

---

## 2. Work Item/Artifact Types by Level

### 2.1 Entity Inventory Summary

| Level | Primary Work Items | Backlog | Kanban System |
|-------|-------------------|---------|---------------|
| **Portfolio** | Epics (Business, Enabler) | Portfolio Backlog | Portfolio Kanban |
| **Large Solution** | Capabilities (Business, Enabler) | Solution Backlog | Solution Kanban |
| **Program/ART** | Features (Business, Enabler) | ART Backlog | ART Kanban |
| **Team** | Stories (User, Enabler), Tasks | Team Backlog | Team Kanban |

### 2.2 Hierarchy Decomposition

```
Portfolio Level
└── Epic (Business or Enabler)
    │
    ├── [Large Solution Level - Optional]
    │   └── Capability (Business or Enabler)
    │       │
    │       └── [Program/ART Level]
    │           └── Feature (Business or Enabler)
    │               │
    │               └── [Team Level]
    │                   ├── Story (User or Enabler)
    │                   │   └── Task
    │                   └── Task (standalone)
    │
    └── [Direct to Program/ART Level - No Large Solution]
        └── Feature (Business or Enabler)
            │
            └── [Team Level]
                ├── Story (User or Enabler)
                │   └── Task
                └── Task (standalone)
```

---

## 3. Entity Definitions and Properties

### 3.1 Epic

> "An Epic is a significant solution development initiative requiring portfolio-level
> oversight due to its substantial scope and impact."
> — [SAFe Official](https://framework.scaledagile.com/epic/)

#### Epic Types

| Type | Description |
|------|-------------|
| **Business Epic** | Delivers value directly to customers |
| **Enabler Epic** | Enhances architectural runway to support future needs |

#### Epic Subtypes by Scope

| Subtype | Scope | Threshold |
|---------|-------|-----------|
| **Programme Epic** | Single ART, multiple PIs | Below portfolio threshold |
| **Solution Epic** | Single Solution Train, multiple PIs | Below portfolio threshold |
| **Portfolio Epic** | Multiple Solution Trains or exceeds threshold | Above portfolio threshold |

#### Epic Properties

| Property | Description | Required |
|----------|-------------|----------|
| `id` | Unique identifier | Yes |
| `name` / `title` | Brief phrase describing the epic | Yes |
| `epic_owner` | Accountable individual who shepherds the epic | Yes |
| `type` | Business or Enabler | Yes |
| `description` | High-level overview of organizational need | Yes |
| `business_outcome_hypothesis` | Testable assertion about expected outcomes | Yes |
| `leading_indicators` | Early signals tracking epic progress | Yes |
| `nfrs` | Non-functional requirements | No |
| `mvp_definition` | Minimum Viable Product scope | Yes (for Analyzing) |
| `lean_business_case` | Cost, value, duration, risk evaluation | Yes (for Go decision) |
| `wsjf_score` | Weighted Shortest Job First priority | Yes |
| `cost_estimate_mvp` | Preliminary MVP cost estimate | Yes |
| `cost_estimate_full` | Full implementation cost estimate | No |
| `portfolio_kanban_state` | Current state in Portfolio Kanban | Yes |

#### Epic Hypothesis Statement Template

```
For [target audience]
Who [needs/problem]
The [solution name]
IS A [category/type]
THAT [key benefits]
UNLIKE [current state/competitors]
OUR SOLUTION [differentiation]
```

> "Similar to Geoffrey Moore's Elevator Pitch from 'Crossing The Chasm'"
> — [Agile Rising](https://www.agilerising.com/blog/safe-epic-real-world-example/)

#### Lean Business Case Sections

| Section | Description |
|---------|-------------|
| Epic Brief | Overview including key stakeholders and hypothesis statement |
| Scope and MVP | In/out of scope, MVP features |
| Analysis Summary | Go/No-Go decision summary |
| Analysis of Solution | Impact on internal/external clients, affected departments |
| Cost Estimates | Preliminary and updated estimates for MVP and full |
| Development Approach | In-house vs outsourced, dependencies |

---

### 3.2 Capability

> "A Capability represents large solution functionality whose implementation often spans
> multiple ARTs and is sized to be delivered within a PI."
> — [SAFe Official](https://framework.scaledagile.com/features-and-capabilities/)

#### Capability Types

| Type | Description |
|------|-------------|
| **Business Capability** | Directly benefits the business or customers |
| **Enabler Capability** | Enables subsequent business capabilities/features |

#### Capability Properties

| Property | Description | Required |
|----------|-------------|----------|
| `id` | Unique identifier | Yes |
| `name` / `title` | Brief phrase description | Yes |
| `description` | Detailed description | Yes |
| `benefit_hypothesis` | Validatable statement of expected benefit | Yes |
| `acceptance_criteria` | Criteria for determining completion | Yes |
| `type` | Business or Enabler | Yes |
| `parent_epic_id` | Reference to parent Epic (if applicable) | No |
| `nfrs` | Non-functional requirements constraints | No |
| `wsjf_score` | Priority score | Yes |
| `solution_kanban_state` | Current state in Solution Kanban | Yes |
| `target_pi` | Target Program Increment for delivery | No |

**Format:** Same as Features - brief phrase + benefit hypothesis + acceptance criteria

---

### 3.3 Feature

> "A Feature describes a product or solution functionality that offers business value,
> meets a stakeholder requirement, and can be completed by an Agile Release Train within
> a PI—typically under 2 months of effort."
> — [SAFe Official](https://framework.scaledagile.com/features-and-capabilities/)

#### Feature Types

| Type | Description |
|------|-------------|
| **Business Feature** | Directly benefits the business or customers |
| **Enabler Feature** | Enables subsequent business features |

#### Feature Properties

| Property | Description | Required |
|----------|-------------|----------|
| `id` | Unique identifier | Yes |
| `name` / `title` | Brief phrase description | Yes |
| `description` | Detailed description | Yes |
| `benefit_hypothesis` | Validatable statement of expected benefit | Yes |
| `acceptance_criteria` | Criteria including NFRs for completion | Yes |
| `type` | Business or Enabler | Yes |
| `parent_capability_id` | Reference to parent Capability | No |
| `parent_epic_id` | Reference to parent Epic (if no Capability) | No |
| `nfrs` | Non-functional requirements | No |
| `wsjf_score` | Weighted Shortest Job First priority | Yes |
| `art_kanban_state` | Current state in ART Kanban | Yes |
| `target_pi` | Target Program Increment | No |
| `mmf` | Minimum Marketable Feature scope | No |

#### Benefit Hypothesis Template

```
We believe this [business outcome] will be achieved if [these users] successfully
achieve [this user outcome] with [this feature].
```

> "The benefit hypothesis is the business value that the feature is expected to deliver.
> Similar to a scientific hypothesis, this is a statement that will ultimately be tested."
> — [Agility at Scale](https://agility-at-scale.com/safe/requirements-model/)

---

### 3.4 Story

> "Stories are short descriptions of a small piece of desired functionality written from
> the user's perspective. They serve as the primary tool Agile Teams use to describe
> small, vertical slices of intended system behavior."
> — [SAFe Official](https://framework.scaledagile.com/story/)

#### Story Types

| Type | Description | Format |
|------|-------------|--------|
| **User Story** | Describes value delivered to end users | "As a [user], I want [function], So that [purpose]" |
| **Enabler Story** | Exploration, architecture, infrastructure, compliance | Technical statement with acceptance criteria |

#### Enabler Story Subtypes

| Subtype | Description |
|---------|-------------|
| **Exploration (Spike)** | Research to understand options |
| **Architecture** | Design components and their relationships |
| **Infrastructure** | Work on solution infrastructure |
| **Compliance** | Actions required for compliance |

#### Story Properties

| Property | Description | Required |
|----------|-------------|----------|
| `id` | Unique identifier | Yes |
| `title` | Brief description | Yes |
| `description` | Full story description | Yes |
| `type` | User or Enabler | Yes |
| `enabler_subtype` | Exploration, Architecture, Infrastructure, Compliance | If Enabler |
| `acceptance_criteria` | Testable criteria for completion | Yes |
| `story_points` | Relative effort estimate | Yes |
| `parent_feature_id` | Reference to parent Feature | Yes |
| `state` | Current workflow state | Yes |
| `iteration` | Target iteration | No |
| `team` | Assigned team | Yes |
| `product_owner` | PO responsible for acceptance | Yes |

#### Story Format (The 3 Cs)

| Component | Description |
|-----------|-------------|
| **Card** | 2-3 sentence summary of intent |
| **Conversation** | Collaborative clarification discussions |
| **Confirmation** | Acceptance criteria verification |

> "Stories act as a 'pidgin language,' where both sides (users and developers) can agree
> enough to work together effectively."
> — Bill Wake, co-inventor of Extreme Programming

---

### 3.5 Task

Tasks represent the smallest unit of work in SAFe, typically created by breaking down Stories.

#### Task Properties

| Property | Description | Required |
|----------|-------------|----------|
| `id` | Unique identifier | Yes |
| `title` | Brief description | Yes |
| `description` | Detailed description | No |
| `parent_story_id` | Reference to parent Story | Yes |
| `assignee` | Team member assigned | Yes |
| `estimated_hours` | Time estimate | No |
| `remaining_hours` | Remaining work | No |
| `state` | Current state (Not Started, In Progress, Done) | Yes |

---

### 3.6 Non-Functional Requirements (NFRs)

> "NFRs are system qualities that guide the design of the solution and often serve as
> constraints across the relevant backlogs."
> — [SAFe Official](https://framework.scaledagile.com/nonfunctional-requirements/)

#### NFR Categories (FURPS+)

| Category | Description |
|----------|-------------|
| **Functionality** | Feature set, capabilities, security |
| **Usability** | Ease of use, aesthetics, documentation |
| **Reliability** | Availability, accuracy, recoverability |
| **Performance** | Response time, throughput, resource usage |
| **Supportability** | Testability, maintainability, configurability |
| **+ (Plus)** | Design constraints, implementation requirements, interface requirements |

#### Common NFR Types in SAFe

- Performance
- Scalability
- Security
- Usability
- Maintainability
- Accessibility
- Privacy
- Resilience
- Compliance

**Application:** NFRs constrain features and stories at all backlog levels and are
revisited as part of Definition of Done.

---

## 4. Relationships Across Levels

### 4.1 Containment/Decomposition Relationships

| Relationship | From | To | Description |
|--------------|------|-----|-------------|
| `contains` | Epic | Capability | Epic splits into Capabilities |
| `contains` | Epic | Feature | Epic splits directly into Features (no Large Solution) |
| `contains` | Capability | Feature | Capability splits into Features |
| `contains` | Feature | Story | Feature decomposes into Stories |
| `contains` | Story | Task | Story breaks into Tasks |

### 4.2 Realization Relationships

| Relationship | From | To | Description |
|--------------|------|-----|-------------|
| `realizes` | Capability | Epic | Capability realizes (part of) Epic |
| `realizes` | Feature | Capability | Feature realizes (part of) Capability |
| `realizes` | Feature | Epic | Feature realizes Epic (no Capability) |
| `realizes` | Story | Feature | Story realizes (part of) Feature |

### 4.3 Cross-Level Relationship Matrix

```
┌──────────────┐
│    EPIC      │ Portfolio Level
│  (Business/  │
│   Enabler)   │
└──────┬───────┘
       │ contains / realized_by
       ▼
┌──────────────┐
│  CAPABILITY  │ Large Solution Level (Optional)
│  (Business/  │
│   Enabler)   │
└──────┬───────┘
       │ contains / realized_by
       ▼
┌──────────────┐
│   FEATURE    │ Program/ART Level
│  (Business/  │
│   Enabler)   │
└──────┬───────┘
       │ contains / realized_by
       ▼
┌──────────────┐
│    STORY     │ Team Level
│  (User/      │
│   Enabler)   │
└──────┬───────┘
       │ contains
       ▼
┌──────────────┐
│    TASK      │ Team Level
└──────────────┘
```

### 4.4 Dependency Relationships

| Relationship | Description | Scope |
|--------------|-------------|-------|
| `depends_on` | One item requires another to be completed first | Within or across levels |
| `blocked_by` | Item cannot proceed until blocker resolved | Within or across levels |
| `related_to` | Items share context or affect each other | Any level |

---

## 5. Program Increment (PI) Concepts and Cadences

### 5.1 Program Increment Definition

> "A Planning Interval (PI) is a cadence-based timebox during which Agile Release Trains
> deliver continuous value to customers aligned with PI Objectives."
> — [SAFe Official](https://framework.scaledagile.com/program-increment/)

### 5.2 PI Structure

| Element | Description |
|---------|-------------|
| **Duration** | 8-12 weeks (shorter preferred) |
| **Structure** | 4-5 development iterations + 1 Innovation & Planning (IP) iteration |
| **Cadence** | PI Planning → Development Iterations → IP Iteration → Inspect & Adapt |

### 5.3 PI Events

| Event | Timing | Purpose |
|-------|--------|---------|
| **PI Planning** | Start of PI | Teams plan the next increment of work |
| **Development Iterations** | Middle of PI | Teams execute on planned work |
| **System Demo** | End of each iteration | Demonstrate integrated increment |
| **Innovation & Planning (IP)** | End of PI | Exploration, planning, hackathons |
| **Inspect & Adapt** | End of PI | Retrospective and improvement |

### 5.4 PI Objectives

> "PI Objectives summarize the business and technical goals that teams and trains intend
> to achieve in the upcoming PI and are either committed or uncommitted."
> — [SAFe Official](https://framework.scaledagile.com/pi-objectives/)

| Type | Description |
|------|-------------|
| **Committed** | Goals teams firmly intend to complete |
| **Uncommitted** | Goals teams may pursue if capacity permits |

### 5.5 Iteration Structure

| Element | Description |
|---------|-------------|
| **Duration** | Typically 2 weeks |
| **Content** | Stories and tasks from Team Backlog |
| **Events** | Sprint Planning, Daily Standup, Sprint Review, Sprint Retro |

---

## 6. Kanban States at Each Level

### 6.1 Portfolio Kanban States

> "The Portfolio Kanban system contains states such as funnel, reviewing, analyzing,
> implementing, and done to manage each epic from ideation to completion."
> — [Agility at Scale](https://agility-at-scale.com/safe/portfolio-kanban/)

| State | Description | WIP Limit | Activities |
|-------|-------------|-----------|------------|
| **Funnel** | Initial intake for significant ideas | None | Capture ideas as Epic Hypothesis Statements |
| **Reviewing** | Evaluate and refine significant investments | Explicit | Develop Epic Hypothesis Statement, calculate WSJF |
| **Analyzing** | In-depth evaluation of viability | Explicit | Multiple solution alternatives, define MVP, Lean Business Case |
| **Ready** | Prioritization waiting state | Explicit | Periodic review, WSJF recalculation |
| **Implementing: MVP** | Active MVP development | Implicit (capacity) | Build MVP, test hypothesis |
| **Implementing: Persevere** | Continue development post-validation | Implicit | Implement additional features |
| **Done** | No longer requires portfolio governance | N/A | Epic removed from active management |

#### Portfolio Kanban Flow

```
Funnel → Reviewing → Analyzing → Ready → Implementing:MVP → Implementing:Persevere → Done
                ↓           ↓                    ↓                    ↓
              Done        Done                 Done                 Done
          (No-Go)      (No-Go)            (Disproven)         (Complete)
```

---

### 6.2 Solution Kanban States (Large Solution Level)

The Solution Kanban manages Capabilities similarly to the Portfolio Kanban managing Epics.

| State | Description |
|-------|-------------|
| **Funnel** | Initial ideas for capabilities |
| **Analyzing** | Evaluation and refinement |
| **Solution Backlog** | Prioritized, ready for implementation |
| **Implementing** | Active development across ARTs |
| **Done** | Capability delivered |

---

### 6.3 ART/Program Kanban States

> "The ART Kanban is a visualization method to manage the flow of features and capabilities
> from ideation to evaluation, application, and release."
> — [The Burndown](https://theburndown.com/safe-6-0-the-art-backlog/)

| State | Description | Activities |
|-------|-------------|------------|
| **Funnel** | Initial placeholder for proposed features | Capture from epics or local context |
| **Business Review** | Review for alignment with strategy | Formal definition, benefits, acceptance criteria |
| **ART Backlog** | Ready for PI Planning | Fully defined, ranked by WSJF |
| **Implementing** | In active development | Decomposed into stories, in PI |
| **Done** | Feature delivered | Accepted by Product Management |

#### ART Kanban Flow

```
Funnel → Business Review → ART Backlog → Implementing → Done
              ↓
            Rejected
```

---

### 6.4 Team Kanban States

> "SAFe Team Kanban is a flow-based agile method for teams within an Agile Release Train
> that continuously deliver value using a pull-based system."
> — [SAFe Official](https://framework.scaledagile.com/safe-team-kanban/)

| State | Description |
|-------|-------------|
| **Backlog** | Stories waiting to be pulled |
| **Ready** | Stories refined and ready for work |
| **In Progress** | Actively being worked on |
| **Review / Test** | Under review or testing |
| **Done** | Completed and accepted |

#### Story Lifecycle States

| State | Description |
|-------|-------------|
| **Not Started** | After Sprint Planning, not yet begun |
| **In Progress** | Active development, testing, or design |
| **Done** | All tasks complete, meets Definition of Done |
| **Accepted** | Product Owner accepted, ready for deployment |
| **Incomplete** | Doesn't meet DoD (rolled to next iteration) |
| **Rejected/Cancelled** | No longer required |

---

## 7. SAFe Configurations

SAFe provides four configurations to match organizational complexity:

### 7.1 Configuration Comparison

| Configuration | Levels Included | Use Case |
|---------------|-----------------|----------|
| **Essential SAFe** | Team + Program/ART | Basic building block, single ART |
| **Large Solution SAFe** | Team + Program + Solution | Multiple ARTs, complex solutions |
| **Portfolio SAFe** | Team + Program + Portfolio | Strategy and investment governance |
| **Full SAFe** | All Four Levels | Largest enterprises, full agility |

### 7.2 Essential SAFe

> "Essential SAFe represents the foundational level, described as the minimal elements
> necessary for Agile Release Trains to deliver solutions."
> — [SAFe Official](https://framework.scaledagile.com/essential-safe/)

**Includes:**
- Agile Teams (Team Level)
- Agile Release Train (Program Level)
- Features, Stories, Tasks
- PI Planning, Iterations
- ART and Team Backlogs

**Excludes:**
- Portfolio management
- Large Solution coordination

### 7.3 Large Solution SAFe

**Adds to Essential:**
- Solution Train
- Capabilities
- Solution Backlog
- Solution Kanban
- Cross-ART coordination

### 7.4 Portfolio SAFe

**Adds to Essential:**
- Portfolio Backlog
- Portfolio Kanban
- Epics
- Lean Portfolio Management
- Strategic Themes
- Investment Themes

### 7.5 Full SAFe

**Combines:**
- All elements from Essential, Large Solution, and Portfolio
- Complete business agility across all four levels

---

## 8. WSJF (Weighted Shortest Job First)

> "WSJF is estimated as the relative cost of delay divided by the relative job duration."
> — [SAFe Official](https://framework.scaledagile.com/wsjf/)

### 8.1 Formula

```
WSJF = Cost of Delay / Job Size
```

### 8.2 Cost of Delay Components

| Component | Description |
|-----------|-------------|
| **User/Business Value** | Relative worth to stakeholders |
| **Time Criticality** | Sensitivity to timing delays |
| **Risk Reduction / Opportunity Enablement** | Strategic value from mitigating risks or enabling future capabilities |

### 8.3 Application

- Applied continuously to prioritize backlogs
- Used at Portfolio, Solution, and ART levels
- Automatically ignores sunk costs

---

## 9. Enablers Across Levels

> "Enablers are backlog items that extend the architectural runway of the solution under
> development or improve the performance of the development value stream."
> — [SAFe Official](https://framework.scaledagile.com/enablers/)

### 9.1 Enabler Types

| Type | Description |
|------|-------------|
| **Exploration** | Research, prototyping, understanding customer needs |
| **Architecture** | Construct Architectural Runway |
| **Infrastructure** | Build/enhance development and runtime environments |
| **Compliance** | Regulatory requirements, verification, audits |

### 9.2 Enablers at Each Level

| Level | Enabler Type | Example |
|-------|--------------|---------|
| Portfolio | Enabler Epic | "Implement microservices architecture" |
| Solution | Enabler Capability | "Cross-ART authentication system" |
| Program | Enabler Feature | "API gateway implementation" |
| Team | Enabler Story | "Research caching strategies (spike)" |

---

## 10. Key Quotes and Citations

### On Epics
> "What if we found ourselves building something that nobody wanted?"
> — Eric Ries, *The Lean Startup*

### On Alignment
> "There is more value created with overall alignment than with local excellence."
> — Don Reinertsen

### On Requirements
> "The emphasis should be on why we do a job."
> — SAFe on Backlog Management

### On Commitment
> "Making and meeting small commitments builds trust."
> — SAFe on PI Objectives

### On Innovation
> "Innovation comes from the producer, not the customer."
> — W. Edwards Deming

---

## 11. Sources

### Primary Sources (Official SAFe Documentation)

1. [SAFe Lean-Agile Principles](https://framework.scaledagile.com/safe-lean-agile-principles/)
2. [SAFe Epic](https://framework.scaledagile.com/epic/)
3. [SAFe Features and Capabilities](https://framework.scaledagile.com/features-and-capabilities/)
4. [SAFe Story](https://framework.scaledagile.com/story/)
5. [SAFe Program Increment](https://framework.scaledagile.com/program-increment/)
6. [SAFe Enablers](https://framework.scaledagile.com/enablers/)
7. [SAFe Agile Release Train](https://framework.scaledagile.com/agile-release-train/)
8. [SAFe Solution Train](https://framework.scaledagile.com/solution-train/)
9. [SAFe Portfolio Backlog](https://framework.scaledagile.com/portfolio-backlog/)
10. [SAFe Team Backlog](https://framework.scaledagile.com/team-backlog/)
11. [SAFe WSJF](https://framework.scaledagile.com/wsjf/)
12. [SAFe Essential SAFe](https://framework.scaledagile.com/essential-safe/)
13. [SAFe Nonfunctional Requirements](https://framework.scaledagile.com/nonfunctional-requirements/)
14. [SAFe PI Objectives](https://framework.scaledagile.com/pi-objectives/)
15. [SAFe ART and Solution Train Backlogs](https://framework.scaledagile.com/art-and-solution-train-backlogs)
16. [SAFe Team Kanban](https://framework.scaledagile.com/safe-team-kanban)

### Secondary Sources

17. [Agility at Scale - Portfolio Kanban](https://agility-at-scale.com/safe/portfolio-kanban/)
18. [Agility at Scale - Requirements Model v6](https://agility-at-scale.com/safe/requirements-model/)
19. [Agility.ac - SAFe Work Items](https://agility.ac/frequent-agile-questions/what-are-the-stories-features-capabilities-and-epics-in-safe)
20. [Agile Seekers - Feature vs Capability vs Epic](https://agileseekers.com/blog/popm-guide-to-feature-capability-epic)
21. [Agile Rising - SAFe Epic Example](https://www.agilerising.com/blog/safe-epic-real-world-example/)
22. [Premier Agile - SAFe Levels](https://premieragile.com/levels-of-scaled-agile-framework/)
23. [Premier Agile - User Story Lifecycle](https://premieragile.com/user-story-lifecycle/)
24. [PM-Partners - SAFe Levels](https://www.pm-partners.com.au/insights/the-4-levels-of-the-scaled-agile-framework-explained/)
25. [PM-Partners - SAFe Enablers](https://www.pm-partners.com.au/insights/what-is-the-role-of-enablers-in-the-scaled-agile-framework/)
26. [Enov8 - SAFe Hierarchy](https://www.enov8.com/blog/the-hierarchy-of-safe-scaled-agile-framework-explained/)
27. [The Burndown - ART Backlog](https://theburndown.com/safe-6-0-the-art-backlog/)
28. [Agile Hive - SAFe Four Levels](https://agile-hive.com/blog/from-team-to-portfolio-understanding-safes-four-levels-with-agile-hive/)

---

## Appendix A: Entity Property Summary Tables

### A.1 Epic Properties (Complete)

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| id | string | Yes | Unique identifier |
| name | string | Yes | Brief phrase description |
| epic_owner | string | Yes | Accountable person |
| type | enum | Yes | Business, Enabler |
| subtype | enum | No | Programme, Solution, Portfolio |
| description | text | Yes | High-level overview |
| business_outcome_hypothesis | text | Yes | Testable outcomes |
| leading_indicators | list | Yes | Progress signals |
| nfrs | list | No | Non-functional requirements |
| mvp_definition | text | Yes* | MVP scope (*for Analyzing) |
| lean_business_case | object | Yes* | Full business case (*for Go) |
| wsjf_score | number | Yes | Priority score |
| cost_estimate_mvp | number | Yes | MVP cost |
| cost_estimate_full | number | No | Full implementation cost |
| state | enum | Yes | Kanban state |
| strategic_theme | string | No | Aligned strategic theme |
| investment_theme | string | No | Budget allocation theme |

### A.2 Capability Properties (Complete)

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| id | string | Yes | Unique identifier |
| name | string | Yes | Brief phrase description |
| type | enum | Yes | Business, Enabler |
| description | text | Yes | Detailed description |
| benefit_hypothesis | text | Yes | Expected benefit statement |
| acceptance_criteria | list | Yes | Completion criteria |
| parent_epic_id | string | No | Parent Epic reference |
| nfrs | list | No | NFR constraints |
| wsjf_score | number | Yes | Priority score |
| state | enum | Yes | Solution Kanban state |
| target_pi | string | No | Target PI for delivery |

### A.3 Feature Properties (Complete)

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| id | string | Yes | Unique identifier |
| name | string | Yes | Brief phrase description |
| type | enum | Yes | Business, Enabler |
| description | text | Yes | Detailed description |
| benefit_hypothesis | text | Yes | Expected benefit statement |
| acceptance_criteria | list | Yes | Completion criteria (with NFRs) |
| parent_capability_id | string | No | Parent Capability reference |
| parent_epic_id | string | No | Parent Epic (if no Capability) |
| nfrs | list | No | NFR constraints |
| wsjf_score | number | Yes | Priority score |
| state | enum | Yes | ART Kanban state |
| target_pi | string | No | Target PI for delivery |
| mmf | text | No | Minimum Marketable Feature |

### A.4 Story Properties (Complete)

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| id | string | Yes | Unique identifier |
| title | string | Yes | Brief description |
| type | enum | Yes | User, Enabler |
| enabler_subtype | enum | If Enabler | Exploration, Architecture, Infrastructure, Compliance |
| description | text | Yes | Full story description |
| acceptance_criteria | list | Yes | Testable criteria |
| story_points | number | Yes | Relative effort estimate |
| parent_feature_id | string | Yes | Parent Feature reference |
| state | enum | Yes | Workflow state |
| iteration | string | No | Target iteration |
| team | string | Yes | Assigned team |
| product_owner | string | Yes | Responsible PO |

### A.5 Task Properties (Complete)

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| id | string | Yes | Unique identifier |
| title | string | Yes | Brief description |
| description | text | No | Detailed description |
| parent_story_id | string | Yes | Parent Story reference |
| assignee | string | Yes | Assigned team member |
| estimated_hours | number | No | Time estimate |
| remaining_hours | number | No | Remaining work |
| state | enum | Yes | Not Started, In Progress, Done |

---

## Appendix B: Kanban State Enumerations

### B.1 Portfolio Kanban States

```
FUNNEL
REVIEWING
ANALYZING
READY
IMPLEMENTING_MVP
IMPLEMENTING_PERSEVERE
DONE
```

### B.2 Solution Kanban States

```
FUNNEL
ANALYZING
SOLUTION_BACKLOG
IMPLEMENTING
DONE
```

### B.3 ART/Program Kanban States

```
FUNNEL
BUSINESS_REVIEW
ART_BACKLOG
IMPLEMENTING
DONE
```

### B.4 Team Kanban / Story States

```
BACKLOG
READY
IN_PROGRESS
REVIEW
DONE
ACCEPTED
```

---

*End of Document*
