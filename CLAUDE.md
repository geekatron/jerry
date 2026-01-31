# CLAUDE.md - Jerry Framework Root Context

> This file provides context to Claude Code at session start.
> It serves as **procedural memory** - loaded once, not maintained in context.

---

## Project Overview

**Jerry** is a framework for behavior and workflow guardrails that helps solve problems
while accruing a body of knowledge, wisdom, and experience.

### Core Problem: Context Rot

> "Context Rot is the phenomenon where an LLM's performance degrades as the context
> window fills up, even when total token count is well within the technical limit."
> — [Chroma Research](https://research.trychroma.com/context-rot)

Jerry addresses this through:
- **Filesystem as infinite memory** - Offload state to files
- **Work Tracker** - Persistent task state across sessions
- **Skills** - Compressed instruction interfaces
- **Structured knowledge** - `docs/` hierarchy for accumulated wisdom

---

## Worktracker

<worktracker>

## 1: Entity Hierarchy

### 1.1 Complete Hierarchy Tree
```
WorkItem (abstract)
│
├── StrategicItem (abstract) ─────────────────── Long-term planning horizon
│   │
│   ├── Initiative ──────────────────────────── Portfolio-level strategic theme
│   │   └── Contains: Epic[]
│   │
│   ├── Epic ────────────────────────────────── Large initiative (weeks/months)
│   │   └── Contains: Capability[] | Feature[]
│   │
│   ├── Capability [OPTIONAL] ───────────────── SAFe Solution level (large solutions)
│   │   └── Contains: Feature[]
│   │
│   └── Feature ─────────────────────────────── Program-level feature (sprints)
│       └── Contains: Story[]
│
├── DeliveryItem (abstract) ─────────────────── Sprint-level execution
│   │
│   ├── Story ───────────────────────────────── User-valuable increment (days)
│   │   └── Contains: Task[]
│   │
│   ├── Task ────────────────────────────────── Atomic work unit (hours)
│   │   └── Contains: Subtask[]
│   │
│   ├── Subtask ─────────────────────────────── Indivisible work (hours)
│   │   └── Contains: (none - leaf node)
│   │
│   ├── Spike ───────────────────────────────── Timeboxed research/exploration
│   │   └── Contains: (none - leaf node)
│   │
│   └── Enabler ─────────────────────────────── Technical/infrastructure work
│       └── Contains: Task[]
│
├── QualityItem (abstract) ──────────────────── Defect and quality tracking
│   │
│   └── Bug ─────────────────────────────────── Defect requiring fix
│       └── Contains: Task[]
│
└── FlowControlItem (abstract) ──────────────── Workflow impediments
    │
    └── Impediment ──────────────────────────── Blocker requiring resolution
        └── Contains: (none - references blocked items)
```

### 1.2 Hierarchy Levels

| Level | Category  | Entities              | Planning Horizon | Typical Owner     |
|-------|-----------|-----------------------|------------------|-------------------|
| L0    | Portfolio | Initiative            | Quarters/Years   | Portfolio Manager |
| L1    | Strategic | Epic                  | Weeks/Months     | Product Manager   |
| L2    | Solution  | Capability (optional) | PIs              | Solution Manager  |
| L3    | Program   | Feature               | Sprints          | Product Owner     |
| L4    | Delivery  | Story, Enabler        | Days             | Development Team  |
| L5    | Execution | Task, Subtask, Spike  | Hours            | Individual        |
| -     | Quality   | Bug                   | Variable         | QA/Dev            |
| -     | Flow      | Impediment            | Immediate        | Scrum Master      |

---

## 2: Entity Classification and Properties

### 2.1 Classification Matrix

| Entity     | Category  | Level | Container | Atomic | Quality Gates | Optional |
|------------|-----------|-------|-----------|--------|---------------|----------|
| Initiative | Strategic | L0    | Yes       | No     | No            | Yes      |
| Epic       | Strategic | L1    | Yes       | No     | No            | No       |
| Capability | Strategic | L2    | Yes       | No     | No            | Yes      |
| Feature    | Strategic | L3    | Yes       | No     | No            | No       |
| Story      | Delivery  | L4    | Yes       | No     | Yes           | No       |
| Task       | Delivery  | L5    | Yes       | No     | Yes           | No       |
| Subtask    | Delivery  | L5    | No        | Yes    | Yes           | No       |
| Spike      | Delivery  | L5    | No        | Yes    | **No**        | No       |
| Enabler    | Delivery  | L4    | Yes       | No     | Yes           | No       |
| Bug        | Quality   | -     | Yes       | No     | Yes           | No       |
| Impediment | Flow      | -     | No        | Yes    | No            | No       |

### 2.2 Containment Rules Matrix

| Parent Type | Allowed Children            |
|-------------|-----------------------------|
| Initiative  | Epic                        |
| Epic        | Capability, Feature         |
| Capability  | Feature                     |
| Feature     | Story, Enabler              |
| Story       | Task, Subtask               |
| Task        | Subtask                     |
| Subtask     | (none)                      |
| Spike       | (none)                      |
| Enabler     | Task                        |
| Bug         | Task                        |
| Impediment  | (none - uses relationships) |

---

## 3: System Mapping Summary

### 3.1 Entity Mapping Table

| Canonical  | ADO Scrum            | SAFe                        | JIRA                  |
|------------|----------------------|-----------------------------|-----------------------|
| Initiative | (Epic + tag)         | Strategic Theme             | Initiative (Premium)  |
| Epic       | Epic                 | Epic                        | Epic                  |
| Capability | (Feature + tag)      | Capability                  | (Epic or custom)      |
| Feature    | Feature              | Feature                     | Epic (or custom)      |
| Story      | Product Backlog Item | Story                       | Story                 |
| Task       | Task                 | Task                        | Task                  |
| Subtask    | Task (child)         | Task (subtask)              | Sub-task              |
| Spike      | Task + spike tag     | Enabler Story (Exploration) | Task + spike label    |
| Enabler    | PBI (ValueArea=Arch) | Enabler                     | Story + enabler label |
| Bug        | Bug                  | Defect                      | Bug                   |
| Impediment | Impediment           | (blocking links)            | (blocking links)      |

### 3.2 Mapping Complexity

| Direction         | Complexity | Notes                                     |
|-------------------|------------|-------------------------------------------|
| Canonical to ADO  | Medium     | PBI naming; Impediment direct             |
| Canonical to SAFe | High       | 4 Kanban systems; WSJF calculation        |
| Canonical to JIRA | Medium     | Resolution separation; flexible hierarchy |
| ADO to Canonical  | Low        | Direct mapping for most entities          |
| SAFe to Canonical | Medium     | May flatten Capability; preserve WSJF     |
| JIRA to Canonical | Low        | Derive status from Resolution+Status      |

## 4. System Mappings

### 4.1 Complete Entity Mapping

| Canonical Entity | ADO Scrum                     | SAFe                          | JIRA                         |   Native    | Notes                                          |
|------------------|-------------------------------|-------------------------------|------------------------------|:-----------:|------------------------------------------------|
| **Initiative**   | Epic (with tag)               | Strategic Theme               | Initiative (Premium)         |   Partial   | ADO: use Epic with "initiative" tag            |
| **Epic**         | Epic                          | Epic (Portfolio Backlog)      | Epic                         |     Yes     | Universal - direct mapping                     |
| **Capability**   | Feature (with tag)            | Capability (Solution Backlog) | Epic or Feature              |  SAFe-only  | ADO/JIRA: map to Feature with metadata         |
| **Feature**      | Feature                       | Feature (Program Backlog)     | Epic (or custom)             |   Partial   | JIRA: use Epic or create custom type           |
| **Story**        | Product Backlog Item (PBI)    | Story                         | Story                        |     Yes     | ADO uses "PBI" terminology                     |
| **Task**         | Task                          | Task                          | Task, Sub-task               |     Yes     | Universal - direct mapping                     |
| **Subtask**      | Task (child of Task)          | Task (subtask)                | Sub-task                     |     Yes     | Hierarchical placement determines type         |
| **Spike**        | Task (with "spike" tag)       | Enabler Story (Exploration)   | Task (with "spike" label)    |   Labeled   | Use tagging/labeling conventions               |
| **Enabler**      | PBI (ValueArea=Architectural) | Enabler                       | Story (with "enabler" label) | SAFe-native | ADO: use ValueArea field                       |
| **Bug**          | Bug                           | Defect                        | Bug                          |     Yes     | SAFe uses "Defect" terminology                 |
| **Impediment**   | Impediment                    | (blocking links)              | (blocking links)             |  ADO-only   | SAFe/JIRA: synthesize from blocks relationship |

### 4.1. Entity Mapping by System

#### 4.1.1 ADO Scrum Entity Types

| ADO Type             | Canonical Mapping       | Notes                      |
|----------------------|-------------------------|----------------------------|
| Epic                 | Epic or Initiative      | Check for "initiative" tag |
| Feature              | Feature or Capability   | Check for "capability" tag |
| Product Backlog Item | Story or Enabler        | Check ValueArea field      |
| Task                 | Task, Subtask, or Spike | Check parent and tags      |
| Bug                  | Bug                     | Direct mapping             |
| Impediment           | Impediment              | Direct mapping             |

#### 4.1.2 SAFe Entity Types

| SAFe Type                   | Canonical Mapping | Notes                  |
|-----------------------------|-------------------|------------------------|
| Strategic Theme             | Initiative        | Portfolio level        |
| Epic                        | Epic              | Direct mapping         |
| Capability                  | Capability        | Solution level         |
| Feature                     | Feature           | Program level          |
| Story                       | Story             | Team level             |
| Enabler                     | Enabler           | Check enabler_type     |
| Enabler Story (Exploration) | Spike             | Research type          |
| Task                        | Task or Subtask   | Based on parent        |
| Defect                      | Bug               | Terminology difference |

#### 4.1.3 JIRA Entity Types

| JIRA Type  | Canonical Mapping | Notes                    |
|------------|-------------------|--------------------------|
| Initiative | Initiative        | JIRA Premium only        |
| Epic       | Epic or Feature   | Depends on org hierarchy |
| Story      | Story or Enabler  | Check labels             |
| Task       | Task or Spike     | Check labels             |
| Sub-task   | Subtask           | Direct mapping           |
| Bug        | Bug               | Direct mapping           |

---

## Work tracker (worktracker) Behavior
We use the Canonical model for all work items in our project documentation and tracking artifacts. The ADO Scrum, SAFe Terminology and Jira (Standard/Adv. Roadmaps) columns are provided for reference to map our canonical model to common frameworks and tools. If users use terminology from ADO Scrum, SAFe or JIRA, we should map it to our canonical model for consistency.

`WORKTRACKER.md` is the Global Manifest tracking all Initiatives and Epics, Bugs, Decisions, Discoveries and Impediments. It exists in the root of the project folder ({ProjectId} e.g. `PROJ-005-plugin-bugs`). It is a pointer with relationships to to the items it is tracking.

A folder is created for each Epic (`{EpicId}-{slug}`) in the `work/` folder.
Each Epic folder contains its own `{EpicId}-{slug}.md` tracking Features, Enablers, Stories and Tasks (Effort) for that Strategic Theme. This file also acts as a pointer with relationships to all respective artifacts of the Epic.

A folder (`{FeatureId}-{slug}`) is created for each Feature in the `work/{EpicId}-{slug}/` folder.
Each Feature folder contains its own `{FeatureId}-{slug}.md` tracking Unit of Work, Enablers and Tasks (Effort) for that Feature. Each `FEATURE-WORKTRACKER.md` must have and maintain relationships to related artifacts in-order to enable traceability and auditability as well as easier traversal for you - it is a pointer with relationships to all respective artifacts of the Feature.

A folder (`{EnablerId}-{slug}`) is created for each Enabler in the `work/{EpicId}-{slug}/{FeatureId}-{slug}/` folder.
Each Enabler folder contains its own `{EnablerId}-{slug}.md` tracking Tasks, Sub-Tasks, Spikes, Bugs, Impediments and Discoveries for that Enabler. Each `{EnablerId}-{slug}.md` must have and maintain relationships to related artifacts in-order to enable traceability and auditability as well as easier traversal for you - it is a pointer with relationships to all respective artifacts of the Enabler.

A folder (`{EnablerId}-{slug}`) is created for each Story in the `work/{EpicId}-{slug}/{FeatureId}-{slug}/` folder.
Each Story folder contains its own `{Story}-{slug}.md` tracking Tasks, Sub-Tasks, Spikes, Bugs, Impediments and Discoveries for that Story. Each `{Story}-{slug}.md` must have and maintain relationships to related artifacts in-order to enable traceability and auditability as well as easier traversal for you - it is a pointer with relationships to all respective artifacts of the Story.


A file is created for each Task, Sub-Task, Spike, Bug, Impediment and Discovery in the respective `{EnablerId}-{slug}` or `{StoryId}-{slug}` following the scheme outlined in the Directory Structure. Each Task, Sub-Task, Spike, Bug, Impediment and Discovery file must have and maintain relationships to related artifacts in-order to enable traceability and auditability as well as easier traversal for you.
Each Enabler and Story must contain verifiable acceptance criteria.
Each Enabler and Story must be broken down into detailed Tasks with verifiable evidence. Verifiable evidence (citations, references and sources) must be provided to support closing out a Task.

Use MCP Memory-Keeper to help you remember and maintain the structure and relationships of the Worktracker system. You don't have to remember everything, just remember to use MCP Memory-Keeper to help you keep track of everything. Try MCP Memory-Keeper first before searching the repository.

---

## Work Tracker (worktracker) Templates

Description:
- Work tracker (worktracker) templates are stored in the `docs/templates/worktracker/` folder.
- These templates provide a standardized structure for creating various work tracker artifacts such as Bugs, Enablers, Epics, Features, Spikes, Stories, and Tasks.
- Using these templates ensures consistency and completeness across all work tracker items.

Directory Structure:
```
.context/                                                                                                       # Respository level Documents Folder (root)
└── templates/                                                                                              # Repository level Templates Folder
    └── worktracker/                                                                                        # Templates for Worktracker Artifacts
        ├── BUG.md                                                                                          # Template for Bug
        ├── DECISION.md                                                                                     # Template for Decision
        ├── DISCOVERY.md                                                                                    # Template for Discovery
        ├── ENABLER.md                                                                                      # Template for Enabler
        ├── EPIC.md                                                                                         # Template for Epic
        ├── FEATURE.md                                                                                      # Template for Feature
        ├── IMPEDIMENT.md                                                                                   # Template for Impediment
        ├── SPIKE.md                                                                                        # Template for Spike
        ├── STORY.md                                                                                        # Template for Story
        └── TASK.md                                                                                         # Template for Task
```

---

## Work tracker (worktracker) Directory Structure

---

## Templates (MANDATORY)

> **CRITICAL:** You MUST use the repository templates when creating ANY work items or artifacts.
> **DO NOT** make up your own formats. Always check for existing templates first.

### Work Tracker (worktracker) Templates

**Location:** `.context/templates/worktracker/`

Description:
- Work tracker (worktracker) templates are stored in the `docs/templates/worktracker/` folder.
- These templates provide a standardized structure for creating various work tracker artifacts such as Bugs, Enablers, Epics, Features, Spikes, Stories, and Tasks.
- Using these templates ensures consistency and completeness across all work tracker items.

Work tracker templates provide standardized structure for all work item types:

| Template | Use For | Path |
|----------|---------|------|
| `ENABLER.md` | EN-* files | `.context/templates/worktracker/ENABLER.md` |
| `TASK.md` | TASK-* files | `.context/templates/worktracker/TASK.md` |
| `BUG.md` | BUG-* files | `.context/templates/worktracker/BUG.md` |
| `DISCOVERY.md` | DISC-* files | `.context/templates/worktracker/DISCOVERY.md` |
| `DECISION.md` | DEC-* files | `.context/templates/worktracker/DECISION.md` |
| `SPIKE.md` | SPIKE-* files | `.context/templates/worktracker/SPIKE.md` |
| `EPIC.md` | EPIC-* files | `.context/templates/worktracker/EPIC.md` |
| `FEATURE.md` | FEAT-* files | `.context/templates/worktracker/FEATURE.md` |
| `STORY.md` | STORY-* files | `.context/templates/worktracker/STORY.md` |
| `IMPEDIMENT.md` | IMP-* files | `.context/templates/worktracker/IMPEDIMENT.md` |

### Problem-Solving & Knowledge Templates

**Location:** `docs/knowledge/exemplars/templates/`

Templates for problem-solving artifacts and knowledge documents:

| Template | Use For | Path |
|----------|---------|------|
| `adr.md` | Architecture Decision Records | `docs/knowledge/exemplars/templates/adr.md` |
| `research.md` | Research artifacts | `docs/knowledge/exemplars/templates/research.md` |
| `analysis.md` | Analysis artifacts | `docs/knowledge/exemplars/templates/analysis.md` |
| `deep-analysis.md` | Deep analysis | `docs/knowledge/exemplars/templates/deep-analysis.md` |
| `synthesis.md` | Synthesis documents | `docs/knowledge/exemplars/templates/synthesis.md` |
| `review.md` | Review artifacts | `docs/knowledge/exemplars/templates/review.md` |
| `investigation.md` | Investigation reports | `docs/knowledge/exemplars/templates/investigation.md` |
| `jrn.md` | Journal entries | `docs/knowledge/exemplars/templates/jrn.md` |
| `use-case-template.md` | Use case specifications | `docs/knowledge/exemplars/templates/use-case-template.md` |

### Template Usage Rules

1. **ALWAYS** read the template before creating a new file
2. **NEVER** make up your own format - use the existing templates
3. **INCLUDE** all required sections from the template
4. **REFERENCE** the template in the file's HTML comment header
5. **ASK** the user if unsure which template to use

### Directory Structure

```
.context/                                                                      # Repository level context
└── templates/                                                                 # Repository level Templates
    └── worktracker/                                                           # Templates for Worktracker Artifacts
        ├── BUG.md                                                             # Template for Bug
        ├── DECISION.md                                                        # Template for Decision
        ├── DISCOVERY.md                                                       # Template for Discovery
        ├── ENABLER.md                                                         # Template for Enabler
        ├── EPIC.md                                                            # Template for Epic
        ├── FEATURE.md                                                         # Template for Feature
        ├── IMPEDIMENT.md                                                      # Template for Impediment
        ├── SPIKE.md                                                           # Template for Spike
        ├── STORY.md                                                           # Template for Story
        └── TASK.md                                                            # Template for Task

docs/knowledge/exemplars/templates/                                            # Problem-solving templates
├── adr.md                                                                     # ADR (Michael Nygard format)
├── analysis.md                                                                # Analysis artifacts
├── deep-analysis.md                                                           # Deep analysis
├── investigation.md                                                           # Investigation reports
├── jrn.md                                                                     # Journal entries
├── research.md                                                                # Research artifacts
├── review.md                                                                  # Review artifacts
├── synthesis.md                                                               # Synthesis documents
└── use-case-template.md                                                       # Use case specifications
```

---

## Work tracker (worktracker) Directory Structure

```
projects/
└── {ProjectId}/ e.g. PROJ-005-plugin-bugs                                                                      # Project Context Folder
    ├── PLAN.md                                                                                                 # Initial Project Plan and Overview.
    ├── WORKTRACKER.md                                                                                          # Global Manifest tracking all work items. Also a pointer with relationships to all decomposed work items.
    └── work/                                                                                                   # Project Worktracker Decomposition Folder
        └── {EpicId}-{slug}/ e.g. EPIC-001-forge-developer-experience                                           # Epic Folder. Large body of work spanning multiple sprints or months.
            ├── {EpicId}-{slug}.md                                                                              # Epic tracking Features. Also a pointer with relationships to all respective Feature artifacts of the Epic.
            ├── {EpicId}--{BugId}-{slug}.md           e.g. EPIC-001:BUG-001-slugs-too-long.md                    # Bug File documenting identified bugs. Discovered at the Epic Level. Enablers or Story MUST be created to address documented bugs. Contains relationships to related artifacts.
            ├── {EpicId}--{DiscoveryId}-{slug}.md     e.g. EPIC-001:DISC-001-need-claude-md.md                   # Discovery File documenting discoveries made. Discovered at the Epic Level. Discoveries MAY lead to creation of Enablers or Stories. Contains relationships to related artifacts..
            ├── {EpicId}--{ImpedimentId}-{slug}.md    e.g. EPIC-001:IMP-001-missing-claude.md                    # Impediment File documenting identified blockers preventing progress on one or more work items. Discovered at the Epic Level. Valuable for visibility and tracking resolution time. Enablers or Story MUST be created to address documented impediments. Contains relationships to related artifacts.
            ├── {EpicId}--{DecisionId}-{slug}.md    e.g. EPIC-001:DEC-001-worktracker-planning.md                # Decision File documenting decisions between the User and Claude. Discovered at the Epic Level. Captures decisions when Claude asks for clarification. Must provide enough context regarding the questions and decision tree. Contains relationships to related artifacts.
            ├── plans/                                                                                          # Folder for plans that we generate while working in the Epic. As we work through the project and enouncter complexity we generate plans to help us navigate the complexity.
            │   └── PLAN-{PlanId}-{slug}.md e.g. PLAN-001-holy-lazer-cats.md                                    # Plan that we generate anytime we have to do something complicated. References the respective Strategic Theme, Initiative, Solution Epic, Feature, Unit of Work, Enabler and/or Task. Also referenced by the respective Strategic Theme, Initiative, Solution Epic, Feature, Unit of Work, Enabler and/or Task to easily and effectively traverse.
            └── {FeatureId}-{slug}/         e.g. FEAT-001-worktracker                                           # Feature Folder. Program-level functionality deliverable within 1-3 sprints. Primary decomposition target for Stories.
                ├── {FeatureId}-{slug}.md                                                                       # Feature tracking Stories, Enablers, Tasks, Sub-Tasks, Spikes, Bugs, Impediments and Discoveries. Also a pointer with relationships to all respective artifacts of the Feature.
                ├── {FeatureId}--{BugId}-{slug}.md           e.g. FEAT-001:BUG-001-id-bad-casing.md              # Bug File documenting identified bugs. Discovered at the Feature Level. Enablers or Story MUST be created to address documented bugs. Contains relationships to related artifacts.
                ├── {FeatureId}--{DiscoveryId}-{slug}.md     e.g. FEAT-001:DISC-001-missing-templates.md         # Discovery File documenting discoveries made. Discovered at the Feature Level. Discoveries MAY lead to creation of Enablers or Stories. Contains relationships to related artifacts.
                ├── {FeatureId}--{ImpedimentId}-{slug}.md    e.g. FEAT-001:IMP-001-need-impediment-template.md   # Impediment File documenting identified blockers preventing progress on one or more work items. Discovered at the Feature Level. Valuable for visibility and tracking resolution time. Enablers or Story MUST be created to address documented impediments. Contains relationships to related artifacts.
                ├── {FeatureId}--{DecisionId}-{slug}.md    e.g. FEAT-001:DEC-001-id-scheme.md                    # Decision File documenting decisions between the User and Claude. Discovered at the Feature Level. Captures decisions when Claude asks for clarification. Must provide enough context regarding the questions and decision tree. Contains relationships to related artifacts.
                ├── {EnablerId}-{slug}/     e.g. EN-001-claude-md-debt-fixes                                    # Enabler Folder - Technical/infrastructure work that enables future value delivery. SAFe concept for architectural runway, tech debt, etc.
                │   ├── {EnablerId}-{slug}.md                                                                   # Enabler tracking Tasks, Sub-Tasks, Spikes, Bugs, Impediments and Discoveries. Also a pointer with relationships to all respective artifacts of the Enabler.
                │   ├── {TaskId}-{slug}.md          e.g. TASK-001-tests-for-session-hooks.md                    # Task file. Must have verifiable evidence before Task can be Closed. Contains relationships to related artifacts.
                │   ├── {BugId}-{slug}.md           e.g. BUG-001-session-hook-failure.md                        # Bug File documenting identified bugs. Discovered at the Enabler level. Enablers or Story MUST be created to address documented bugs. Contains relationships to related artifacts.
                │   ├── {DiscoveryId}-{slug}.md     e.g. DISC-001-insufficient-coverage.md                      # Discovery File documenting discoveries made. Discovered at the Enabler level. Discoveries MAY lead to creation of Enablers or Stories. Contains relationships to related artifacts.
                │   ├── {ImpedimentId}-{slug}.md    e.g. IMP-001-missing-cli-implementation.md                  # Impediment File documenting identified blockers preventing progress on one or more work items. Discovered at the Enabler Level. Valuable for visibility and tracking resolution time. Enablers or Story MUST be created to address documented impediments. Contains relationships to related artifacts.
                │   ├── {DecisionId}-{slug}.md      e.g. DEC-001-cli-hook.md                                    # Decision File documenting decisions between the User and Claude. Discovered at the Enabler Level. Captures decisions when Claude asks for clarification. Must provide enough context regarding the questions and decision tree. Contains relationships to related artifacts.
                │   └── {SpikeId}-{slug}.md         e.g. SPIKE-001-multiple-claude-md-files.md                  # Spike file representing timeboxed research or exploration activity. Does NOT require quality gates (unlike other work types). Outputs knowledge/decisions, not production code. Contains relationships to related artifacts.
                └── {StoryId}-{slug}/       e.g. STORY-001-worktracker-todo-integration                         # Story Folder - User-valuable increment deliverable within a sprint.
                    ├── {StoryId}-{slug}.md                                                                     # Story tracking Tasks, Sub-Tasks, Spikes, Bugs, Impediments and Discoveries. Also a pointer with relationships to all respective artifacts of the Story.
                    ├── {TaskId}-{slug}.md          e.g. TASK-001-tests-for-worktracker.md                      # Task file. Must have verifiable evidence before Task can be Closed. Contains relationships to related artifacts.
                    ├── {BugId}-{slug}.md           e.g. BUG-001-missing-work-items.md                          # Bug File documenting identified bugs. Discovered at the Story level. Enablers or Story MUST be created to address documented bugs. Contains relationships to related artifacts.
                    ├── {DiscoveryId}-{slug}.md     e.g. DISC-001-missing-worktracker-instructions.md           # Discovery File documenting discoveries made. Discovered at the Story level. Discoveries MAY lead to creation of Enablers or Stories. Contains relationships to related artifacts..
                    ├── {ImpedimentId}-{slug}.md    e.g. IMP-001-missing-templates.md                           # Impediment File documenting identified blockers preventing progress on one or more work items. Discovered at the Story Level. Valuable for visibility and tracking resolution time. Enablers or Story MUST be created to address documented impediments. Contains relationships to related artifacts.
                    ├── {DecisionId}-{slug}.md      e.g. DEC-001-template-fidelity.md                           # Decision File documenting decisions between the User and Claude. Discovered at the Story Level. Captures decisions when Claude asks for clarification. Must provide enough context regarding the questions and decision tree. Contains relationships to related artifacts.
                    └── {SpikeId}-{slug}.md         e.g. SPIKE-001-templates-for-work-items.md                  # Spike file representing timeboxed research or exploration activity. Does NOT require quality gates (unlike other work types). Outputs knowledge/decisions, not production code. Contains relationships to related artifacts.
```

</worktracker>

---

<todo>

Use the task management tools (e.g. TaskCreate, TaskUpdate, TaskList, TaskGet) to manage your TODO list effectively.

REQUIRED BEHAVIOR:
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you are in project {JerryProjectId} | Workflow Id: {WorkflowId}
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to update the respective work tracker `*.md` files.
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to capture and update decisions in the respective `*.md` files with detailed updates as YOU and I go through Questions and Answers.
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to update your respective `*.md` files with detailed updates as you are working/progressing through them.
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to document detailed bugs, discoveries and impediments as they are arise in their respective `*.md` files.
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to Keep your TODO list up to date.
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to Keep your TODO list in sync with your respective work tracker `*.md` files.  You MUST keep your TODO in sync with the work-tracker.
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to Keep your TODO list in sync with work tracker. You MUST keep your work tracker entities up to date with detailed updates so they are truthful, accurate and honest representation of the current state.
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to Keep your orchestration artifacts up to date with detailed updates so they are truthful, accurate and honest representation of the current state.


Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: Do NOT take shortcuts. Do NOT use hacks to solve problems. If you are about to take a shortcut or apply a hack, ask yourself is there a better way? If you are about to answer no, try again. If you are truly blocked and want to take a shortcut or apply a hack, ask me first? We are building mission-critical software and quality is king!
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: Ask questions. Push back if something doesn't make sense or is misaligned.
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: Be truthful, accurate, evidence based (citations, sources, references) and honest.

Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: You MUST ALWAYS document your work so that it is understandable by yourself and three different personas: (1) ELI5 <- Explain it to me like I'm Five - i.e. Simple analogy explanations. (2) Engineer - Deep Technical explanation with context (3) 🧠 Architect - Performance implications, tradeoffs, one-way door decisions and design rationale
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: You MUST ALWAYS perform any kind of research and analysis using at minimum the following Problem-Solving frameworks 5W2H + Ishikawa + Pareto Analysis (80/20) + Failure Mode and Effects Analysis (FMEA) + 8D (Eight Disciplines) and NASA Systems Engineering Handbook framework and other before starting any implementation work.
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: You MUST perform research and analysis using Context7 and search the internet for industry best practices, industry standards, innovative work and prior art on the topics you are working through.
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: You MUST make data + evidence driven decisions based on industry best practices and prior art from authoritative sources such as but not limited to Industry Experts, Industry Innovators, Industry Leaders, Community Experts, Community Innovators, Community Leaders and Community experts ensuring you provide citations, references and sources.
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: You MUST persist your detailed analysis, discoveries, explorations, findings, research and synthesis in the repository.
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: You MUST make all decisions in an evidence based process with citations, references and sources using industry best practices from industry leaders, industry experts, community leaders and community experts.
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you: You MUST make ascii art and mermaid diagrams to illustrate your points wherever applicable including activity diagrams, state diagrams, flow charts, sequence diagrams, class diagrams, component diagrams, architecture diagrams, system context diagrams, etc.

You MUST keep your TODO in sync with the work-tracker showing the current Epic, previous Epic and next Epic -> The current Epic must show previous Features, current Feature and next Feature -> the current Feature MUST show all Enablers || Stories -> the current Enabler || Story must show all Tasks. TODO List MUST survive compaction and provide high fidelity.
You MUST keep your TODO in sync with the orchestration plan showing the previous phase, current phase and next phase -> current phase must show all tasks/subagents

You MUST reflect the actions you are taking in the TODO list that are not captured in work tracker entities.

</todo>

---

## Architecture

```
jerry/
├── .claude/                    # Agent Governance Layer
├── .claude-plugin/             # Distribution Layer
├── skills/                     # Interface Layer (Natural Language)
├── scripts/                    # Execution Layer (CLI Shims)
├── src/                        # Hexagonal Core (Python)
│   ├── domain/                 # Pure Business Logic
│   ├── application/            # Use Cases (CQRS)
│   ├── infrastructure/         # Adapters (Persistence, Messaging)
│   └── interface/              # Primary Adapters (CLI, API)
└── docs/                       # Knowledge Repository
```

### Key Design Principles

1. **Hexagonal Architecture** (Ports & Adapters)
   - Domain has no external dependencies
   - Ports define contracts, adapters implement them
   - Dependency inversion: outer depends on inner

2. **Zero-Dependency Core**
   - Python stdlib only in domain/
   - Libraries allowed in infrastructure/ if pre-installed

3. **CQRS Pattern**
   - Commands: Write operations, return events
   - Queries: Read operations, return DTOs

---

## Working with Jerry

### Project-Based Workflow

Jerry uses isolated project workspaces. Each project has its own `PLAN.md` and `WORKTRACKER.md`.

**Active Project Resolution:**
1. Set `JERRY_PROJECT` environment variable (e.g., `export JERRY_PROJECT=PROJ-001-plugin-cleanup`)
2. If not set, Claude will prompt you to specify which project to work on
3. See `projects/README.md` for the project registry

**Project Structure:**
```
projects/PROJ-{nnn}-{slug}/
├── PLAN.md              # Project implementation plan
├── WORKTRACKER.md       # Work tracking document
└── .jerry/data/items/   # Operational state (work items)
```

### Before Starting Work

1. Set `JERRY_PROJECT` environment variable for your target project
2. Check `projects/${JERRY_PROJECT}/PLAN.md` for current plan
3. Review `projects/${JERRY_PROJECT}/WORKTRACKER.md` for task state
4. Read relevant `docs/knowledge/` for domain context

### During Work

1. Use Work Tracker to persist task state to `projects/${JERRY_PROJECT}/WORKTRACKER.md`
2. Update PLAN.md as implementation progresses
3. Document decisions in `docs/design/`

### After Completing Work

1. Update Work Tracker with completion status
2. Capture learnings in `docs/experience/` or `docs/wisdom/`
3. Commit with clear, semantic messages

### Creating a New Project

1. Check `projects/README.md` for next project number
2. Create directory: `mkdir -p projects/PROJ-{nnn}-{slug}/.jerry/data/items`
3. Create `PLAN.md` and `WORKTRACKER.md`
4. Add entry to `projects/README.md`
5. Set `JERRY_PROJECT` environment variable

---

## Project Enforcement (Hard Rule)

> **Enforcement Level:** HARD
> **Principle:** P-030 - Project Context Required
> **See Also:** `docs/design/ADR-002-project-enforcement.md`

Claude **MUST NOT** proceed with any substantial work without an active project context.
This is a hard constraint enforced via the SessionStart hook.

### Hook Output Format

The `scripts/session_start_hook.py` hook produces JSON output with BOTH `systemMessage` (shown to user in terminal) and `additionalContext` (added to Claude's context window):

```json
{
  "systemMessage": "Jerry Framework: Project PROJ-001-plugin-cleanup active",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Jerry Framework initialized. See CLAUDE.md for context.\n<project-context>...\n</project-context>"
  }
}
```

**Key fields:**
- `systemMessage`: User-visible terminal message (what you see at session start)
- `additionalContext`: Claude's context window content (parsed via XML tags)

#### `<project-context>` - Valid Project Active (in additionalContext)

```
Jerry Framework initialized. See CLAUDE.md for context.
<project-context>
ProjectActive: PROJ-001-plugin-cleanup
ProjectPath: projects/PROJ-001-plugin-cleanup/
ValidationMessage: Project is properly configured
</project-context>
```

**systemMessage:** `Jerry Framework: Project PROJ-001-plugin-cleanup active`
**Action:** Proceed with work in the active project context.

#### `<project-required>` - No Project Selected (in additionalContext)

```
Jerry Framework initialized.
<project-required>
ProjectRequired: true
AvailableProjects:
  - PROJ-001-plugin-cleanup [ACTIVE]
  - PROJ-002-example [DRAFT]
NextProjectNumber: 003
ProjectsJson: [{"id": "PROJ-001-plugin-cleanup", "status": "IN_PROGRESS"}]
</project-required>

ACTION REQUIRED: No JERRY_PROJECT environment variable set.
Claude MUST use AskUserQuestion to help the user select an existing project or create a new one.
DO NOT proceed with any work until a project is selected.
```

**systemMessage:** `Jerry Framework: No project set (2 available)`
**Action:** Use `AskUserQuestion` to help user select or create a project.

#### `<project-error>` - Invalid Project Specified (in additionalContext)

```
Jerry Framework initialized with ERROR.
<project-error>
InvalidProject: bad-format
Error: Project ID must match pattern PROJ-NNN-slug
AvailableProjects:
  - PROJ-001-plugin-cleanup [ACTIVE]
NextProjectNumber: 002
</project-error>

ACTION REQUIRED: The specified JERRY_PROJECT is invalid.
Claude MUST use AskUserQuestion to help the user select or create a valid project.
```

**systemMessage:** `Jerry Framework: ERROR - bad-format invalid (Project ID must...)`
**Action:** Use `AskUserQuestion` to help user correct the error.

### Required AskUserQuestion Flow

When `<project-required>` or `<project-error>` is received, Claude **MUST**:

1. **Parse** the available projects from the hook output
2. **Present options** via `AskUserQuestion`:
   - List available projects (from `AvailableProjects`)
   - Offer "Create new project" option
3. **Handle response**:
   - If existing project selected → instruct user to set `JERRY_PROJECT`
   - If new project → guide through creation flow
4. **DO NOT** proceed with unrelated work until resolved

Example AskUserQuestion structure:
```yaml
question: "Which project would you like to work on?"
header: "Project"
options:
  - label: "PROJ-001-plugin-cleanup"
    description: "[ACTIVE] Plugin system cleanup and refactoring"
  - label: "Create new project"
    description: "Start a new project workspace"
```

### Project Creation Flow

When user selects "Create new project":

1. **Get project details** via AskUserQuestion:
   - Slug/name (required): e.g., "api-redesign"
   - Description (optional)

2. **Auto-generate ID** using `NextProjectNumber` from hook:
   - Format: `PROJ-{NNN}-{slug}`
   - Example: `PROJ-003-api-redesign`

3. **Create project structure**:
   ```
   projects/PROJ-003-api-redesign/
   ├── PLAN.md              # Implementation plan template
   ├── WORKTRACKER.md       # Work tracking document
   └── .jerry/data/items/   # Operational state
   ```

4. **Update registry**: Add entry to `projects/README.md`

5. **Instruct user**: Set `JERRY_PROJECT=PROJ-003-api-redesign`

---

## Skills Available

| Skill          | Purpose                            | Location                       |
|----------------|------------------------------------|--------------------------------|
| `worktracker`  | Task/issue management              | `skills/worktracker/SKILL.md`  |
| `architecture` | System design guidance             | `skills/architecture/SKILL.md` |
| `problem-solving` | Domain use case invocation         | `skills/problem-solving/SKILL.md` |
| `nasa-se`      | NASA Systems Engineering processes | `skills/nasa-se/`              |
| `orchestration` | Multi-agent workflow coordination  | `skills/orchestration/SKILL.md` |
| `transcript`   | Transcription skill                | `skills/transcript/SKILL.md`   |

---

## Mandatory Skill Usage (PROACTIVE)

> **CRITICAL:** You MUST use the following skills PROACTIVELY without waiting for the user to prompt you.
> These skills are designed to ensure quality, rigor, and traceability in all work.

### /problem-solving (MANDATORY for Research/Analysis)

**USE AUTOMATICALLY WHEN:**
- Starting ANY research or analysis task
- Investigating bugs, issues, or problems
- Performing root cause analysis
- Synthesizing findings from multiple sources
- Creating architecture decisions (ADRs)

**Provides:**
- 8 specialized agents: researcher, analyst, synthesizer, architect, reviewer, investigator, validator, reporter
- Structured frameworks: 5W2H, Ishikawa, Pareto, FMEA, 8D
- Evidence-based decision making with citations
- Persistent artifact generation

**Trigger Phrases (use skill automatically):**
- "research", "analyze", "investigate", "explore"
- "root cause", "why", "understand"
- "synthesize", "consolidate", "summarize findings"
- "review", "validate", "critique"

### @nasa-se (MANDATORY for Requirements/Design)

**USE AUTOMATICALLY WHEN:**
- Defining or analyzing requirements
- Creating design specifications
- Performing verification & validation
- Conducting technical reviews
- Managing system integration
- Risk management activities

**Provides:**
- NPR 7123.1D process implementation
- 10 specialized agents for systems engineering
- Requirements engineering rigor
- Verification/validation frameworks
- Technical review protocols
- Mission-grade quality practices

**Trigger Phrases (use skill automatically):**
- "requirements", "specification", "shall statements"
- "verification", "validation", "V&V"
- "technical review", "design review"
- "risk management", "FMEA"
- "system integration", "interface"

### @orchestration (MANDATORY for Multi-Step Workflows)

**USE AUTOMATICALLY WHEN:**
- Work involves multiple phases or stages
- Multiple agents need coordination
- Tasks have dependencies requiring sync barriers
- State must be checkpointed for recovery
- Cross-pollinated pipelines are needed

**Provides:**
- ORCHESTRATION_PLAN.md - Strategic workflow context
- ORCHESTRATION_WORKTRACKER.md - Tactical execution tracking
- ORCHESTRATION.yaml - Machine-readable state (SSOT)
- Sync barriers for parallel work coordination
- State checkpointing for resilience

**Trigger Phrases (use skill automatically):**
- "orchestration", "pipeline", "workflow"
- "multi-agent", "parallel", "coordinate"
- "sync barrier", "checkpoint"
- "phases", "stages", "gates"

### Skill Usage Behavior Rules

1. **DO NOT WAIT** for user to invoke skills - use them proactively when triggers apply
2. **COMBINE SKILLS** when appropriate (e.g., /orchestration + /problem-solving + /nasa-se for complex analysis)
3. **INVOKE EARLY** - Use skills at the start of work, not after struggling without them
4. **PERSIST ARTIFACTS** - All skill outputs must be persisted to the repository
5. **REFERENCE IN TODO** - Track skill invocations and outputs in your TODO list

### Example: Starting a New Feature

```
User: "Let's work on EN-004 Architecture Decisions"

Claude's Internal Process:
1. ✅ Invoke /orchestration - This has multiple ADRs requiring coordination
2. ✅ Invoke /problem-solving - Research and analysis needed for each ADR
3. ✅ Invoke /nasa-se - Architecture decisions require SE rigor
4. ✅ Create/update TODO with skill tracking
5. ✅ Proceed with coordinated execution
```

---

### Orchestration Skill Details

For multi-agent workflows requiring cross-pollinated pipelines, sync barriers, or state checkpointing, use the **orchestration** skill. The skill provides:

- **ORCHESTRATION_PLAN.md** - Strategic context with ASCII workflow diagrams
- **ORCHESTRATION_WORKTRACKER.md** - Tactical execution tracking
- **ORCHESTRATION.yaml** - Machine-readable state (SSOT)

Activate with: "orchestration", "multi-agent workflow", "cross-pollinated pipeline", "sync barrier"

See `skills/orchestration/PLAYBOOK.md` for step-by-step workflow guidance.

---

## Agents Available

See `AGENTS.md` for the full registry. Agents are scoped to skills:

| Skill | Agents | Location |
|-------|--------|----------|
| problem-solving | 8 specialists (researcher, analyst, synthesizer, etc.) | `skills/problem-solving/agents/` |

Invoke agents via the `/problem-solving` skill.

---

## Code Standards

See `.claude/rules/coding-standards.md` for enforced rules.

Quick reference:
- Python 3.11+ with type hints
- 100 character line limit
- Domain layer: NO external imports
- All public functions: docstrings required

---

## CLI Commands (v0.1.0)

> **Version**: 0.1.0 (Breaking changes from v0.0.1)
> **Reference**: `ADR-CLI-002-namespace-implementation.md`

Jerry CLI is organized into bounded-context-aligned namespaces:

### Session Namespace

Manage agent sessions for context tracking.

```bash
jerry session start [--name NAME] [--description DESC]  # Start new session
jerry session end [--summary TEXT]                       # End current session
jerry session status                                     # Show session status
jerry session abandon [--reason TEXT]                    # Abandon without summary
```

### Items Namespace

Manage work items (tasks, bugs, stories).

```bash
jerry items list [--status STATUS] [--type TYPE]        # List work items
jerry items show <id>                                    # Show item details
jerry items create <title> [--type TYPE]                # Create item (Phase 4.5)
jerry items start <id>                                   # Start work (Phase 4.5)
jerry items complete <id>                                # Complete item (Phase 4.5)
```

**Note**: `create`, `start`, `complete` commands are deferred to Phase 4.5 (Event Sourcing).

### Projects Namespace

Manage Jerry projects.

```bash
jerry projects context                                   # Show project context
jerry projects list                                      # List all projects
jerry projects validate <project-id>                     # Validate project
```

### Global Options

```bash
jerry --help                                             # Show help
jerry --version                                          # Show version
jerry --json <namespace> <command>                       # JSON output
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (validation failure, not found, etc.) |
| 2 | Invalid usage (bad arguments) |

---

## Agent Governance (Jerry Constitution)

All agents operating within Jerry MUST adhere to the **Jerry Constitution v1.0**.

**Location:** `docs/governance/JERRY_CONSTITUTION.md`

### Core Principles (Quick Reference)

| ID | Principle | Enforcement |
|----|-----------|-------------|
| P-001 | Truth and Accuracy | Soft |
| P-002 | File Persistence | Medium |
| P-003 | No Recursive Subagents | **Hard** |
| P-010 | Task Tracking Integrity | Medium |
| P-020 | User Authority | **Hard** |
| P-022 | No Deception | **Hard** |

### Hard Principles (Cannot Override)

1. **P-003**: Maximum ONE level of agent nesting (orchestrator → worker)
2. **P-020**: User has ultimate authority; never override user decisions
3. **P-022**: Never deceive users about actions, capabilities, or confidence

### Self-Critique Protocol

Before finalizing significant outputs, agents SHOULD self-critique:

```
1. P-001: Is my information accurate and sourced?
2. P-002: Have I persisted significant outputs?
3. P-004: Have I documented my reasoning?
4. P-010: Is WORKTRACKER updated?
5. P-022: Am I being transparent about limitations?
```

### Behavioral Validation

Constitution compliance is validated via `docs/governance/BEHAVIOR_TESTS.md`:
- 18 test scenarios (golden dataset)
- LLM-as-a-Judge evaluation (industry standard per DeepEval, Datadog)
- Happy path, edge case, and adversarial coverage

**Industry Prior Art:**
- [Anthropic Constitutional AI](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
- [OpenAI Model Spec](https://model-spec.openai.com/2025-12-18.html)
- [DeepEval G-Eval](https://deepeval.com/docs/metrics-llm-evals)

---

## References

- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Alistair Cockburn
- [Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - Anthropic
- [Context Rot Research](https://research.trychroma.com/context-rot) - Chroma
