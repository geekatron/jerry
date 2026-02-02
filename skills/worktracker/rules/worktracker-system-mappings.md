# Worktracker System Mappings

> Rule file for /worktracker skill
> Source: CLAUDE.md lines 131-215 (EN-201 extraction)
> Extracted: 2026-02-01

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [3: System Mapping Summary](#3-system-mapping-summary) | Entity mapping table and complexity overview |
| [4. System Mappings](#4-system-mappings) | Complete entity mapping by system (ADO, SAFe, JIRA) |

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
