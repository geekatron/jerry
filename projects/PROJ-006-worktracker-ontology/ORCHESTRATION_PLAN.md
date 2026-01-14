# PROJ-006: Work Tracker Ontology - Orchestration Plan

> **Project ID:** PROJ-006-worktracker-ontology
> **Status:** AWAITING APPROVAL
> **Created:** 2026-01-13
> **Approval Required:** YES - Do not execute until user approves

---

## Executive Summary

This orchestration plan defines a multi-phase research and design effort to reverse-engineer a unified **Work Tracker Ontology** from three major project management domains: **ADO Scrum**, **SAFe**, and **JIRA**.

### End Goal

Create a **parent ontology** with:
1. Domain entities (properties and behaviors)
2. Relationships between entities
3. State transitions (workflow state machines)
4. Markdown templates for a Claude Code Skill

---

## Solution Epic: SE-001 - Work Tracker Domain Understanding

### Problem Statement

Work tracking systems (ADO, JIRA, SAFe implementations) have overlapping but inconsistent domain models. To build a universal Claude Code skill for work tracking, we need a **canonical ontology** that:
- Abstracts common patterns across systems
- Maps to system-specific implementations
- Provides templates for AI-assisted work management

### Success Criteria

- [ ] Complete domain models for ADO Scrum, SAFe, and JIRA
- [ ] Identified common entities, relationships, and state machines
- [ ] Parent ontology design with mapping rules
- [ ] Markdown templates ready for skill integration
- [ ] All artifacts reviewed and approved

---

## Feature: FT-001 - Domain Discovery

### Enablers

| ID | Name | Dependencies | Agent(s) |
|----|------|--------------|----------|
| EN-001 | ADO Scrum Domain Analysis | None | ps-researcher, ps-analyst |
| EN-002 | SAFe Domain Analysis | None | ps-researcher, ps-analyst |
| EN-003 | JIRA Domain Analysis | None | ps-researcher, ps-analyst |
| EN-004 | Cross-Domain Synthesis | EN-001, EN-002, EN-003 | ps-synthesizer |

### Work Items

| ID | Name | Dependencies | Agent(s) |
|----|------|--------------|----------|
| WI-001 | Parent Ontology Design | EN-004 | nse-architecture, ps-architect |
| WI-002 | Markdown Template Generation | WI-001 | ps-synthesizer |
| WI-003 | Design Review & Validation | WI-002 | nse-reviews |

---

## Orchestration Architecture

### Pipeline Visualization

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PHASE 1: PARALLEL RESEARCH                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐                │
│  │  Stream A   │      │  Stream B   │      │  Stream C   │                │
│  │  ADO Scrum  │      │    SAFe     │      │    JIRA     │                │
│  │             │      │             │      │             │                │
│  │ ps-research │      │ ps-research │      │ ps-research │                │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘                │
│         │                    │                    │                        │
│         ▼                    ▼                    ▼                        │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐                │
│  │ ADO-RAW.md  │      │ SAFE-RAW.md │      │ JIRA-RAW.md │                │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘                │
│         │                    │                    │                        │
└─────────┼────────────────────┼────────────────────┼────────────────────────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PHASE 2: PARALLEL ANALYSIS                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐                │
│  │  Stream A   │      │  Stream B   │      │  Stream C   │                │
│  │  ADO Model  │      │  SAFe Model │      │  JIRA Model │                │
│  │             │      │             │      │             │                │
│  │ ps-analyst  │      │ ps-analyst  │      │ ps-analyst  │                │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘                │
│         │                    │                    │                        │
│         ▼                    ▼                    ▼                        │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐                │
│  │ADO-MODEL.md │      │SAFE-MODEL.md│      │JIRA-MODEL.md│                │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘                │
│         │                    │                    │                        │
└─────────┼────────────────────┼────────────────────┼────────────────────────┘
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                    ═══════════╧═══════════
                    ║   SYNC BARRIER 1    ║
                    ║ All 3 models ready  ║
                    ═══════════╤═══════════
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PHASE 3: CROSS-DOMAIN SYNTHESIS                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                         ┌─────────────────┐                                │
│                         │  ps-synthesizer │                                │
│                         │                 │                                │
│                         │ Compare models  │                                │
│                         │ Find patterns   │                                │
│                         │ Abstract terms  │                                │
│                         └────────┬────────┘                                │
│                                  │                                          │
│                                  ▼                                          │
│                         ┌─────────────────┐                                │
│                         │ SYNTHESIS.md    │                                │
│                         │ - Common entities│                               │
│                         │ - Mapping table  │                                │
│                         │ - Patterns found │                                │
│                         └────────┬────────┘                                │
│                                  │                                          │
└──────────────────────────────────┼──────────────────────────────────────────┘
                                   │
                        ═══════════╧═══════════
                        ║   SYNC BARRIER 2    ║
                        ║  Synthesis complete ║
                        ═══════════╤═══════════
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PHASE 4: ONTOLOGY DESIGN                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│         ┌─────────────────┐              ┌─────────────────┐               │
│         │ nse-architecture│              │   ps-architect  │               │
│         │                 │              │                 │               │
│         │ Entity design   │─────────────▶│ Validate design │               │
│         │ Relationships   │              │ Check patterns  │               │
│         │ State machines  │              │                 │               │
│         └────────┬────────┘              └────────┬────────┘               │
│                  │                                │                         │
│                  ▼                                ▼                         │
│         ┌─────────────────┐              ┌─────────────────┐               │
│         │ ONTOLOGY.md     │              │ ADR-001.md      │               │
│         │ - Entities      │              │ Design decisions│               │
│         │ - Properties    │              │                 │               │
│         │ - Behaviors     │              │                 │               │
│         │ - Relationships │              │                 │               │
│         │ - State machines│              │                 │               │
│         └────────┬────────┘              └─────────────────┘               │
│                  │                                                          │
└──────────────────┼──────────────────────────────────────────────────────────┘
                   │
        ═══════════╧═══════════
        ║   SYNC BARRIER 3    ║
        ║  Ontology approved  ║
        ═══════════╤═══════════
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PHASE 5: TEMPLATE GENERATION                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                         ┌─────────────────┐                                │
│                         │  ps-synthesizer │                                │
│                         │                 │                                │
│                         │ Generate MD     │                                │
│                         │ templates       │                                │
│                         └────────┬────────┘                                │
│                                  │                                          │
│                                  ▼                                          │
│         ┌────────────────────────┴────────────────────────┐                │
│         │                   TEMPLATES/                     │                │
│         │  ┌──────────────┐ ┌──────────────┐ ┌──────────┐ │                │
│         │  │ EPIC.md      │ │ FEATURE.md   │ │ STORY.md │ │                │
│         │  └──────────────┘ └──────────────┘ └──────────┘ │                │
│         │  ┌──────────────┐ ┌──────────────┐ ┌──────────┐ │                │
│         │  │ TASK.md      │ │ BUG.md       │ │ SPIKE.md │ │                │
│         │  └──────────────┘ └──────────────┘ └──────────┘ │                │
│         └─────────────────────────────────────────────────┘                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                        ┌─────────────────┐
                        │   nse-reviews   │
                        │                 │
                        │ Final validation│
                        │ Quality gate    │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │    COMPLETE     │
                        └─────────────────┘
```

---

## Detailed Phase Breakdown

### Phase 1: Parallel Research (EN-001, EN-002, EN-003)

**Duration:** Parallel execution
**Agent:** ps-researcher (3 instances)

#### Stream A: ADO Scrum Research (EN-001-T1)

**Research Questions:**
1. What work item types exist in ADO Scrum? (Epic, Feature, User Story, Task, Bug, etc.)
2. What properties does each work item type have?
3. What are the default states and transitions?
4. How are work items related (parent-child, links)?
5. What behaviors/operations are supported?

**Sources to Consult:**
- Microsoft Azure DevOps documentation
- ADO REST API reference
- Scrum process template documentation

**Output:** `research/ADO-SCRUM-RAW.md`

#### Stream B: SAFe Research (EN-002-T1)

**Research Questions:**
1. What are the SAFe hierarchy levels? (Portfolio, Program, Team)
2. What work item types exist at each level?
3. What properties are defined for each type?
4. How do items relate across levels?
5. What are the PI (Program Increment) concepts?

**Sources to Consult:**
- Scaled Agile Framework official documentation
- SAFe Big Picture
- SAFe Glossary

**Output:** `research/SAFE-RAW.md`

#### Stream C: JIRA Research (EN-003-T1)

**Research Questions:**
1. What issue types exist in JIRA? (Epic, Story, Task, Bug, Sub-task, etc.)
2. What are the standard and custom fields?
3. What workflow states and transitions exist?
4. How are issues linked (blocks, is blocked by, relates to)?
5. What is the hierarchy (Epic → Story → Sub-task)?

**Sources to Consult:**
- Atlassian JIRA documentation
- JIRA REST API reference
- JIRA Cloud vs Server differences

**Output:** `research/JIRA-RAW.md`

---

### Phase 2: Parallel Analysis (EN-001, EN-002, EN-003)

**Duration:** Parallel execution
**Agent:** ps-analyst (3 instances)

#### Analysis Template (Applied to Each Domain)

For each domain, extract:

```markdown
## Domain Model: {SYSTEM}

### 1. Entity Catalog

| Entity | Description | Level |
|--------|-------------|-------|
| Epic | Large body of work | Portfolio |
| ... | ... | ... |

### 2. Entity Properties

#### {Entity Name}
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| id | string | yes | Unique identifier |
| title | string | yes | Display name |
| ... | ... | ... | ... |

### 3. Entity Behaviors

| Entity | Behavior | Description | Preconditions |
|--------|----------|-------------|---------------|
| Story | create | Create new story | Valid parent |
| Story | transition | Change state | Valid transition |
| ... | ... | ... | ... |

### 4. Relationships

| From | Relationship | To | Cardinality |
|------|--------------|----|-----------:|
| Epic | contains | Feature | 1:N |
| Feature | contains | Story | 1:N |
| ... | ... | ... | ... |

### 5. State Machine

#### {Entity Name} States

```
[New] → [Active] → [Resolved] → [Closed]
         ↓    ↑
       [Blocked]
```

| From State | To State | Trigger | Guards |
|------------|----------|---------|--------|
| New | Active | Start work | Assigned |
| ... | ... | ... | ... |
```

**Outputs:**
- `analysis/ADO-SCRUM-MODEL.md`
- `analysis/SAFE-MODEL.md`
- `analysis/JIRA-MODEL.md`

---

### Phase 3: Cross-Domain Synthesis (EN-004)

**Duration:** Sequential (after Sync Barrier 1)
**Agent:** ps-synthesizer

#### Synthesis Tasks

1. **Entity Alignment Matrix**
   - Map equivalent entities across systems
   - Identify system-specific entities
   - Propose canonical names

2. **Property Alignment Matrix**
   - Map equivalent properties
   - Identify required vs optional
   - Propose canonical property names

3. **Relationship Pattern Analysis**
   - Identify common relationship types
   - Abstract to canonical relationships
   - Document semantic differences

4. **State Machine Comparison**
   - Compare workflow states
   - Identify common transitions
   - Propose canonical state machine

#### Output Structure

```markdown
## Cross-Domain Synthesis Report

### 1. Entity Alignment Matrix

| Canonical | ADO Scrum | SAFe | JIRA | Notes |
|-----------|-----------|------|------|-------|
| Epic | Epic | Epic | Epic | Universal |
| Feature | Feature | Feature | - | Not in JIRA |
| Story | User Story | Story | Story | ADO uses "User Story" |
| Task | Task | Task | Task | Universal |
| Bug | Bug | Defect | Bug | SAFe uses "Defect" |
| ... | ... | ... | ... | ... |

### 2. Property Alignment Matrix

| Canonical | ADO | SAFe | JIRA | Type |
|-----------|-----|------|------|------|
| id | System.Id | id | key | string |
| title | System.Title | name | summary | string |
| description | System.Description | description | description | text |
| status | System.State | status | status | enum |
| priority | Microsoft.VSTS.Common.Priority | priority | priority | enum |
| ... | ... | ... | ... | ... |

### 3. Relationship Types

| Canonical | ADO | SAFe | JIRA |
|-----------|-----|------|------|
| parent-child | Parent/Child | contains | Epic Link |
| blocks | Successor | blocks | Blocks |
| relates-to | Related | relates | Relates |
| ... | ... | ... | ... |

### 4. State Machine Comparison

| Canonical State | ADO | SAFe | JIRA |
|-----------------|-----|------|------|
| backlog | New | Funnel | To Do |
| ready | Approved | Analyzing | Ready |
| in_progress | Active/Committed | Implementing | In Progress |
| blocked | Blocked | Blocked | Blocked |
| review | Resolved | Review | In Review |
| done | Closed | Done | Done |
```

**Output:** `synthesis/CROSS-DOMAIN-SYNTHESIS.md`

---

### Phase 4: Ontology Design (WI-001)

**Duration:** Sequential (after Sync Barrier 2)
**Agents:** nse-architecture, ps-architect

#### Design Tasks

1. **Entity Schema Design**
   - Define canonical entity types
   - Define inheritance hierarchy
   - Define required/optional properties

2. **Relationship Schema Design**
   - Define relationship types
   - Define cardinality rules
   - Define constraint rules

3. **State Machine Design**
   - Define canonical states
   - Define valid transitions
   - Define guard conditions

4. **Mapping Rules Design**
   - Define ADO → Canonical mappings
   - Define SAFe → Canonical mappings
   - Define JIRA → Canonical mappings

#### Output Structure

```markdown
## Work Tracker Ontology v1.0

### 1. Entity Hierarchy

```
WorkItem (abstract)
├── StrategicItem (abstract)
│   ├── Epic
│   ├── Feature
│   └── Capability
├── DeliveryItem (abstract)
│   ├── Story
│   ├── Task
│   └── Spike
└── DefectItem (abstract)
    ├── Bug
    └── Defect
```

### 2. Entity Definitions

#### WorkItem (Abstract Base)

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| id | WorkItemId | yes | auto | Unique identifier |
| title | string(1-500) | yes | - | Display title |
| description | markdown | no | "" | Rich description |
| status | Status | yes | backlog | Current state |
| priority | Priority | no | medium | Urgency level |
| created_at | datetime | yes | now() | Creation timestamp |
| updated_at | datetime | yes | now() | Last update |
| created_by | UserId | yes | current | Creator |
| assigned_to | UserId | no | null | Assignee |
| tags | string[] | no | [] | Labels/tags |
| external_refs | ExternalRef[] | no | [] | System mappings |

### 3. Relationship Types

| Type | From | To | Cardinality | Semantics |
|------|------|----|-----------:|-----------|
| contains | StrategicItem | WorkItem | 1:N | Hierarchical parent |
| blocked_by | WorkItem | WorkItem | N:M | Dependency |
| relates_to | WorkItem | WorkItem | N:M | Association |
| duplicates | WorkItem | WorkItem | N:1 | Duplicate marker |

### 4. State Machine

```
         ┌──────────────────────────────────────────┐
         │                                          │
         ▼                                          │
    ┌─────────┐     ┌─────────┐     ┌─────────┐   │
    │ BACKLOG │────▶│  READY  │────▶│IN_PROGRESS│──┤
    └─────────┘     └─────────┘     └────┬────┘   │
         ▲               ▲               │        │
         │               │               ▼        │
         │               │          ┌─────────┐   │
         │               └──────────│ BLOCKED │   │
         │                          └─────────┘   │
         │                               │        │
         │              ┌────────────────┘        │
         │              ▼                         │
         │         ┌─────────┐     ┌─────────┐   │
         └─────────│ REVIEW  │────▶│  DONE   │◀──┘
                   └─────────┘     └─────────┘
                                        │
                                        ▼
                                   ┌─────────┐
                                   │CANCELLED│
                                   └─────────┘
```

### 5. System Mappings

#### ADO Scrum Mapping
| Canonical | ADO Scrum | Notes |
|-----------|-----------|-------|
| Epic | Epic | Direct |
| Feature | Feature | Direct |
| Story | User Story | Name differs |
| Task | Task | Direct |
| Bug | Bug | Direct |

#### SAFe Mapping
| Canonical | SAFe | Notes |
|-----------|------|-------|
| Epic | Epic | Direct |
| Feature | Feature | Direct |
| Capability | Capability | SAFe-specific |
| Story | Story | Direct |
| Spike | Spike | Direct |
| Bug | Defect | Name differs |

#### JIRA Mapping
| Canonical | JIRA | Notes |
|-----------|------|-------|
| Epic | Epic | Direct |
| Story | Story | Direct |
| Task | Task | Direct |
| Task | Sub-task | Hierarchical |
| Bug | Bug | Direct |
```

**Outputs:**
- `synthesis/ONTOLOGY-v1.md`
- `decisions/ADR-001-ontology-design.md`

---

### Phase 5: Template Generation (WI-002)

**Duration:** Sequential (after Sync Barrier 3)
**Agent:** ps-synthesizer

#### Template Requirements

Each template must include:
1. YAML frontmatter (machine-readable metadata)
2. Human-readable sections
3. Placeholders for dynamic content
4. Relationship references
5. State indicators

#### Template List

| Template | Entity Type | Priority |
|----------|-------------|----------|
| EPIC.md | Epic | P1 |
| FEATURE.md | Feature | P1 |
| STORY.md | Story | P1 |
| TASK.md | Task | P1 |
| BUG.md | Bug | P1 |
| SPIKE.md | Spike | P2 |
| ENABLER.md | Enabler | P2 |

**Output:** `templates/` directory with all templates

---

## Execution Schedule

| Phase | Parallelism | Dependencies | Estimated Steps |
|-------|-------------|--------------|-----------------|
| Phase 1 | 3 parallel | None | 3 research tasks |
| Phase 2 | 3 parallel | Phase 1 complete | 3 analysis tasks |
| Phase 3 | Sequential | Sync Barrier 1 | 1 synthesis task |
| Phase 4 | Sequential | Sync Barrier 2 | 2 design tasks |
| Phase 5 | Sequential | Sync Barrier 3 | 1 generation task |

**Total Estimated Steps:** 10 major tasks

---

## Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Incomplete documentation | High | Medium | Use multiple sources |
| Domain ambiguity | Medium | High | Document assumptions |
| Scope creep | High | Medium | Strict phase gates |
| Template complexity | Medium | Low | Iterative refinement |

---

## Approval Checklist

Before execution, confirm:

- [ ] Solution Epic scope is correct
- [ ] Feature breakdown is appropriate
- [ ] Agent assignments are optimal
- [ ] Sync barriers are well-placed
- [ ] Output formats are acceptable
- [ ] Risk mitigations are adequate

---

## Approval Request

**To proceed with execution, please confirm:**

> "Approved" - Execute the orchestration plan as designed
> "Modify" - Specify changes needed
> "Reject" - Cancel this plan

---

*Plan Version: 1.0*
*Created by: Claude*
*Awaiting Approval*
