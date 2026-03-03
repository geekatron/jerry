# ADO Scrum Domain Model

> **Analysis Document ID**: EN-001-ADO-SCRUM-MODEL
> **Date**: 2026-01-13
> **Analyst**: ps-analyst (Claude Opus 4.5)
> **Project**: PROJ-006-worktracker-ontology
> **Input**: `research/ADO-SCRUM-RAW.md`
> **Status**: COMPLETE

---

## Executive Summary

This document provides a structured domain model analysis of the Azure DevOps Scrum process template. The analysis extracts entities, properties, behaviors, relationships, and state machines from the raw research document to serve as input for the Jerry worktracker ontology design.

---

## 1. Entity Catalog

### 1.1 Core Entities

| Entity | Description | Level | Backlog Visibility |
|--------|-------------|-------|-------------------|
| **Epic** | Large body of work spanning multiple features or releases | Portfolio L2 | Portfolio Backlog |
| **Feature** | Significant functionality delivering user value | Portfolio L1 | Portfolio Backlog |
| **Product Backlog Item (PBI)** | User stories, requirements, discrete work units | Product | Product Backlog |
| **Task** | Atomic work units supporting PBI completion | Sprint | Sprint Backlog |
| **Bug** | Code defects requiring remediation | Configurable | Product or Sprint Backlog |
| **Impediment** | Blocking issues impeding team progress | N/A | Query-only (no backlog) |

### 1.2 Test Entities (Secondary)

| Entity | Description | Level |
|--------|-------------|-------|
| **Test Case** | Defines test steps and expected results | Testing |
| **Test Plan** | Groups test suites and test cases | Testing |
| **Test Suite** | Organizes test cases | Testing |

### 1.3 Entity Hierarchy (Tree Structure)

```
                    ┌─────────────────────────┐
                    │          Epic           │ ← Portfolio Level 2
                    │  (Strategic Initiative) │
                    └───────────┬─────────────┘
                                │ contains (1:N)
                                ▼
                    ┌─────────────────────────┐
                    │        Feature          │ ← Portfolio Level 1
                    │ (Deliverable Increment) │
                    └───────────┬─────────────┘
                                │ contains (1:N)
                                ▼
            ┌───────────────────┴───────────────────┐
            │                                       │
            ▼                                       ▼
┌─────────────────────────┐         ┌─────────────────────────┐
│ Product Backlog Item    │         │          Bug            │
│    (PBI / Story)        │         │    (Defect/Issue)       │
└───────────┬─────────────┘         └───────────┬─────────────┘
            │ contains (1:N)                    │ contains (1:N)
            ▼                                   ▼
┌─────────────────────────┐         ┌─────────────────────────┐
│         Task            │         │         Task            │
│   (Atomic Work Unit)    │         │   (Atomic Work Unit)    │
└─────────────────────────┘         └─────────────────────────┘

Side Entity (no hierarchy):
┌─────────────────────────┐
│      Impediment         │ ← Standalone blocker tracking
│  (Blocking Issue)       │
└─────────────────────────┘
```

---

## 2. Entity Properties

### 2.1 System Properties (All Entities)

| Property | Reference Name | Type | Required | Description |
|----------|----------------|------|----------|-------------|
| ID | `System.Id` | Integer | Yes (auto) | Unique identifier |
| Title | `System.Title` | String | Yes | Display name |
| Description | `System.Description` | HTML | No | Detailed description |
| State | `System.State` | String | Yes | Current workflow state |
| Reason | `System.Reason` | String | No | State change reason |
| Area Path | `System.AreaPath` | TreePath | Yes | Organizational area |
| Iteration Path | `System.IterationPath` | TreePath | Yes | Sprint assignment |
| Work Item Type | `System.WorkItemType` | String | Yes (auto) | Type discriminator |
| Team Project | `System.TeamProject` | String | Yes (auto) | Project context |
| Assigned To | `System.AssignedTo` | Identity | No | Current owner |
| Created By | `System.CreatedBy` | Identity | Yes (auto) | Creator (read-only) |
| Created Date | `System.CreatedDate` | DateTime | Yes (auto) | Creation timestamp (read-only) |
| Changed By | `System.ChangedBy` | Identity | Yes (auto) | Last modifier (read-only) |
| Changed Date | `System.ChangedDate` | DateTime | Yes (auto) | Modification timestamp (read-only) |
| Closed By | `System.ClosedBy` | Identity | No | Closure identity |
| Closed Date | `System.ClosedDate` | DateTime | No | Closure timestamp |
| Revision | `System.Rev` | Integer | Yes (auto) | Version number (read-only) |
| Tags | `System.Tags` | String | No | Comma-separated tags |

### 2.2 Common Planning Properties

| Property | Reference Name | Type | Description |
|----------|----------------|------|-------------|
| Priority | `Microsoft.VSTS.Common.Priority` | Integer(1-4) | Prioritization (1=highest) |
| Effort | `Microsoft.VSTS.Scheduling.Effort` | Double | Relative size estimate |
| Business Value | `Microsoft.VSTS.Common.BusinessValue` | Integer | Value score |
| Value Area | `Microsoft.VSTS.Common.ValueArea` | Enum | Business vs. Architectural |
| Time Criticality | `Microsoft.VSTS.Common.TimeCriticality` | Double | Time sensitivity decay |
| Stack Rank | `Microsoft.VSTS.Common.StackRank` | Double | Backlog position |
| Backlog Priority | `Microsoft.VSTS.Common.BacklogPriority` | Double | Backlog ordering |

### 2.3 Epic Properties

| Property | Reference Name | Type | Required | Description |
|----------|----------------|------|----------|-------------|
| Title | `System.Title` | String | **Yes** | Epic name |
| Description | `System.Description` | HTML | No | Strategic description |
| Effort | `Microsoft.VSTS.Scheduling.Effort` | Double | No | Size estimate |
| Business Value | `Microsoft.VSTS.Common.BusinessValue` | Integer | No | Value score |
| Value Area | `Microsoft.VSTS.Common.ValueArea` | Enum | No | Business/Architectural |
| Time Criticality | `Microsoft.VSTS.Common.TimeCriticality` | Double | No | Time sensitivity |
| Start Date | `Microsoft.VSTS.Scheduling.StartDate` | DateTime | No | Planned start |
| Target Date | `Microsoft.VSTS.Scheduling.TargetDate` | DateTime | No | Target completion |
| Priority | `Microsoft.VSTS.Common.Priority` | Integer(1-4) | No | Priority |

### 2.4 Feature Properties

| Property | Reference Name | Type | Required | Description |
|----------|----------------|------|----------|-------------|
| Title | `System.Title` | String | **Yes** | Feature name |
| Description | `System.Description` | HTML | No | Feature description |
| Effort | `Microsoft.VSTS.Scheduling.Effort` | Double | No | Size estimate |
| Business Value | `Microsoft.VSTS.Common.BusinessValue` | Integer | No | Value score |
| Value Area | `Microsoft.VSTS.Common.ValueArea` | Enum | No | Business/Architectural |
| Time Criticality | `Microsoft.VSTS.Common.TimeCriticality` | Double | No | Time sensitivity |
| Start Date | `Microsoft.VSTS.Scheduling.StartDate` | DateTime | No | Planned start |
| Target Date | `Microsoft.VSTS.Scheduling.TargetDate` | DateTime | No | Target completion |
| Priority | `Microsoft.VSTS.Common.Priority` | Integer(1-4) | No | Priority |

### 2.5 Product Backlog Item (PBI) Properties

| Property | Reference Name | Type | Required | Description |
|----------|----------------|------|----------|-------------|
| Title | `System.Title` | String | **Yes** | PBI/Story title |
| Description | `System.Description` | HTML | No | Detailed description |
| Acceptance Criteria | `Microsoft.VSTS.Common.AcceptanceCriteria` | HTML | No | Definition of Done criteria |
| Effort | `Microsoft.VSTS.Scheduling.Effort` | Double | No | Story points |
| Business Value | `Microsoft.VSTS.Common.BusinessValue` | Integer | No | Value score |
| Priority | `Microsoft.VSTS.Common.Priority` | Integer(1-4) | No | Priority |
| Backlog Priority | `Microsoft.VSTS.Common.BacklogPriority` | Double | No | Backlog ordering |

### 2.6 Task Properties

| Property | Reference Name | Type | Required | Description |
|----------|----------------|------|----------|-------------|
| Title | `System.Title` | String | **Yes** | Task name |
| Description | `System.Description` | HTML | No | Task details |
| Remaining Work | `Microsoft.VSTS.Scheduling.RemainingWork` | Double | No | Hours remaining |
| Activity | `Microsoft.VSTS.Common.Activity` | String | No | Work type category |
| Priority | `Microsoft.VSTS.Common.Priority` | Integer(1-4) | No | Priority |

**Note**: Tasks track only Remaining Work (no Completed Work in Scrum).

### 2.7 Bug Properties

| Property | Reference Name | Type | Required | Description |
|----------|----------------|------|----------|-------------|
| Title | `System.Title` | String | **Yes** | Bug title |
| Repro Steps | `Microsoft.VSTS.TCM.ReproSteps` | HTML | No | Reproduction steps |
| System Info | `Microsoft.VSTS.TCM.SystemInfo` | String | No | System information |
| Acceptance Criteria | `Microsoft.VSTS.Common.AcceptanceCriteria` | HTML | No | Fix verification criteria |
| Effort | `Microsoft.VSTS.Scheduling.Effort` | Double | No | Size estimate |
| Priority | `Microsoft.VSTS.Common.Priority` | Integer(1-4) | No | Priority |
| Severity | `Microsoft.VSTS.Common.Severity` | Enum | No | Bug severity level |
| Found In Build | `Microsoft.VSTS.Build.FoundIn` | String | No | Build where found |
| Integrated In Build | `Microsoft.VSTS.Build.IntegrationBuild` | String | No | Build where fixed |

### 2.8 Impediment Properties

| Property | Reference Name | Type | Required | Description |
|----------|----------------|------|----------|-------------|
| Title | `System.Title` | String | **Yes** | Impediment title |
| Description | `System.Description` | HTML | No | Details |
| Priority | `Microsoft.VSTS.Common.Priority` | Integer(1-4) | No | Priority |
| Resolution | `Microsoft.VSTS.Common.Resolution` | String | No | Resolution details |

---

## 3. Entity Behaviors

### 3.1 Core CRUD Operations

| Entity | Behavior | HTTP Method | Endpoint Pattern | Description |
|--------|----------|-------------|------------------|-------------|
| All | Create | POST | `/_apis/wit/workitems/${type}` | Create new work item |
| All | Read | GET | `/_apis/wit/workitems/{id}` | Retrieve single item |
| All | Read Batch | POST | `/_apis/wit/workitemsbatch` | Retrieve multiple (max 200) |
| All | Update | PATCH | `/_apis/wit/workitems/{id}` | Update item properties |
| All | Delete | DELETE | `/_apis/wit/workitems/{id}` | Delete to Recycle Bin |
| All | Delete Batch | DELETE | `/_apis/wit/workitems?ids=...` | Delete multiple items |
| All | Get Template | GET | `/_apis/wit/workitems/${type}/template` | Get type template |

### 3.2 State Transition Behaviors

| Entity | Behavior | Preconditions | Postconditions |
|--------|----------|---------------|----------------|
| PBI | Approve | State = New | State = Approved |
| PBI | Commit | State = Approved | State = Committed |
| PBI | Complete | State = Committed, all Tasks Done | State = Done |
| PBI | Remove | Any state | State = Removed |
| Bug | Approve | State = New | State = Approved |
| Bug | Commit | State = Approved | State = Committed |
| Bug | Resolve | State = Committed, fix verified | State = Done |
| Task | Start | State = To Do | State = In Progress |
| Task | Complete | State = In Progress | State = Done |
| Impediment | Close | State = Open | State = Closed |

### 3.3 Link Operations

| Entity | Behavior | Preconditions | Description |
|--------|----------|---------------|-------------|
| All | Add Link | Target exists | Create relationship |
| All | Remove Link | Link exists | Delete relationship |
| All | Add Child | Target not already parented | Create parent-child link |
| All | Set Parent | No existing parent | Assign to parent |

### 3.4 Query Operations

| Behavior | HTTP Method | Endpoint | Description |
|----------|-------------|----------|-------------|
| Execute WIQL | POST | `/_apis/wit/wiql` | Run Work Item Query Language |
| Get Query | GET | `/_apis/wit/queries/{id}` | Retrieve saved query |
| List Queries | GET | `/_apis/wit/queries` | List all queries |

### 3.5 Optional Operation Parameters

| Parameter | Behavior Modification |
|-----------|----------------------|
| `validateOnly` | Dry-run without saving |
| `bypassRules` | Skip workflow validation (elevated permission) |
| `suppressNotifications` | Silent operation |
| `$expand` | Include Relations, Fields, Links, or All |
| `destroy` | Permanent delete (bypass Recycle Bin) |

---

## 4. Relationships

### 4.1 Work Item Link Types

| From | Relationship | To | Cardinality | Topology | Reference Name |
|------|--------------|----|-----------:|----------|----------------|
| Epic | Parent-Child | Feature | 1:N | Tree | `System.LinkTypes.Hierarchy-Forward/Reverse` |
| Feature | Parent-Child | PBI | 1:N | Tree | `System.LinkTypes.Hierarchy-Forward/Reverse` |
| Feature | Parent-Child | Bug | 1:N | Tree | `System.LinkTypes.Hierarchy-Forward/Reverse` |
| PBI | Parent-Child | Task | 1:N | Tree | `System.LinkTypes.Hierarchy-Forward/Reverse` |
| Bug | Parent-Child | Task | 1:N | Tree | `System.LinkTypes.Hierarchy-Forward/Reverse` |
| Any | Related | Any | N:N | Network | `System.LinkTypes.Related` |
| Task | Predecessor-Successor | Task | N:N | Dependency | `System.LinkTypes.Dependency-Forward/Reverse` |
| Bug | Duplicate-Duplicate Of | Bug | 1:N | Tree | `System.LinkTypes.Duplicate-Forward/Reverse` |

### 4.2 Process-Defined Link Types

| From | Relationship | To | Cardinality | Reference Name |
|------|--------------|----|-----------:|----------------|
| PBI/Bug | Tested By | Test Case | 1:N | `Microsoft.VSTS.Common.TestedBy-Forward/Reverse` |
| Test Case | Shared Steps | Shared Steps | N:N | `Microsoft.VSTS.TestCase.SharedStepReferencedBy-Forward/Reverse` |

### 4.3 External Link Types

| From | Relationship | To (Artifact) | Description |
|------|--------------|---------------|-------------|
| Any | Branch | Git Branch | Links to source branch |
| Any | Build | Build | Links to CI/CD build |
| Any | Commit | Git Commit | Links to commit |
| Any | Pull Request | PR | Links to pull request |
| Any | Hyperlink | URL | Links to external URL |
| Any | Wiki | Wiki Page | Links to documentation |

### 4.4 Remote Link Types (Cross-Organization)

| From | Relationship | To | Reference Name |
|------|--------------|-----|----------------|
| Any | Consumes From | Remote Item | `System.LinkTypes.Remote.Dependency-Forward` |
| Any | Produced For | Remote Item | `System.LinkTypes.Remote.Dependency-Reverse` |
| Any | Remote Related | Remote Item | `System.LinkTypes.Remote.Related` |

### 4.5 Link Topology Constraints

| Topology | Characteristics | Circular Reference |
|----------|-----------------|-------------------|
| **Tree** | One parent, multiple children | Not allowed |
| **Network** | Many-to-many, non-directional | N/A |
| **Dependency** | Directional ordering | Not allowed |

---

## 5. State Machines

### 5.1 Product Backlog Item (PBI) State Machine

```
                              ┌──────────────────────┐
                              │                      │
                              │       REMOVED        │ ← Hidden from backlog
                              │                      │
                              └──────────────────────┘
                                         ▲
                                         │ (any state)
        ┌────────────────────────────────┼────────────────────────────────┐
        │                                │                                │
        ▼                                │                                │
┌──────────────┐    approve    ┌──────────────┐    commit    ┌──────────────┐    done    ┌──────────────┐
│              │ ─────────────►│              │─────────────►│              │───────────►│              │
│     NEW      │               │   APPROVED   │              │   COMMITTED  │            │     DONE     │
│              │◄─────────────┐│              │◄────────────┐│              │            │              │
└──────────────┘   revert     └──────────────┘   revert     └──────────────┘            └──────────────┘
   (Proposed)                    (Proposed)                   (In Progress)                (Completed)
```

| From State | To State | Trigger | Reason |
|------------|----------|---------|--------|
| New | Approved | Product Owner approval | "Approved for estimation" |
| Approved | Committed | Sprint planning | "Agreed for sprint inclusion" |
| Committed | Done | All tasks complete | "Acceptance criteria met" |
| Approved | New | Refinement needed | "Needs more detail" |
| Committed | Approved | Sprint scope change | "Removed from sprint" |
| Any | Removed | Stakeholder decision | "Obsolete/Cancelled" |

### 5.2 Bug State Machine

```
                              ┌──────────────────────┐
                              │                      │
                              │       REMOVED        │
                              │                      │
                              └──────────────────────┘
                                         ▲
                                         │ (any state)
        ┌────────────────────────────────┼────────────────────────────────┐
        │                                │                                │
        ▼                                │                                │
┌──────────────┐    triage     ┌──────────────┐    commit    ┌──────────────┐   resolve   ┌──────────────┐
│              │ ─────────────►│              │─────────────►│              │───────────►│              │
│     NEW      │               │   APPROVED   │              │   COMMITTED  │            │     DONE     │
│              │               │              │              │              │            │              │
└──────────────┘               └──────────────┘              └──────────────┘            └──────────────┘
   (Proposed)                    (Proposed)                   (In Progress)                (Completed)
```

| From State | To State | Trigger | Reason |
|------------|----------|---------|--------|
| New | Approved | Bug triage | "Bug validated" |
| Approved | Committed | Sprint assignment | "Fix scheduled" |
| Committed | Done | Fix verified | "Bug resolved" |
| Any | Removed | Duplicate/Invalid | "Won't fix" |

### 5.3 Task State Machine

```
                              ┌──────────────────────┐
                              │                      │
                              │       REMOVED        │
                              │                      │
                              └──────────────────────┘
                                         ▲
                                         │ (any state)
        ┌────────────────────────────────┼───────────────────┐
        │                                │                   │
        ▼                                │                   │
┌──────────────┐     start     ┌──────────────┐   complete  ┌──────────────┐
│              │ ─────────────►│              │────────────►│              │
│    TO DO     │               │ IN PROGRESS  │             │     DONE     │
│              │◄──────────────│              │             │              │
└──────────────┘    pause      └──────────────┘             └──────────────┘
   (Proposed)                   (In Progress)                 (Completed)
```

| From State | To State | Trigger | Reason |
|------------|----------|---------|--------|
| To Do | In Progress | Work started | "Started work" |
| In Progress | Done | Work complete | "Task finished" |
| In Progress | To Do | Blocked/Paused | "Work paused" |
| Any | Removed | Cancellation | "Not needed" |

### 5.4 Epic/Feature State Machine

```
                              ┌──────────────────────┐
                              │                      │
                              │       REMOVED        │
                              │                      │
                              └──────────────────────┘
                                         ▲
                                         │ (any state)
        ┌────────────────────────────────┼───────────────────┐
        │                                │                   │
        ▼                                │                   │
┌──────────────┐     start     ┌──────────────┐   complete  ┌──────────────┐
│              │ ─────────────►│              │────────────►│              │
│     NEW      │               │ IN PROGRESS* │             │     DONE     │
│              │               │              │             │              │
└──────────────┘               └──────────────┘             └──────────────┘
   (Proposed)                   (In Progress)                 (Completed)

* Note: "In Progress" is commonly added as custom state
```

| From State | To State | Trigger | Reason |
|------------|----------|---------|--------|
| New | In Progress | Work started | "Development begun" |
| New | Done | Direct completion | "All children done" |
| In Progress | Done | Completion | "Feature/Epic complete" |
| Any | Removed | Cancellation | "Cancelled" |

### 5.5 Impediment State Machine

```
┌──────────────┐    resolve    ┌──────────────┐
│              │ ─────────────►│              │
│     OPEN     │               │    CLOSED    │
│              │◄──────────────│              │
└──────────────┘    reopen     └──────────────┘
 (In Progress)                   (Completed)
```

| From State | To State | Trigger | Reason |
|------------|----------|---------|--------|
| Open | Closed | Resolution found | "Impediment resolved" |
| Closed | Open | Recurrence | "Issue resurfaced" |

---

## 6. State Categories Mapping

| Category | Purpose | Backlog Display | Board Position |
|----------|---------|-----------------|----------------|
| **Proposed** | Initial/candidate items | Visible | First column |
| **In Progress** | Active work | Visible | Middle columns |
| **Resolved** | Awaiting verification | Visible | Middle columns |
| **Completed** | Finished work | Hidden | Final column |
| **Removed** | Archived/cancelled | Hidden | Not shown |

### Entity-State-Category Mapping

| Entity | State | Category |
|--------|-------|----------|
| PBI | New | Proposed |
| PBI | Approved | Proposed |
| PBI | Committed | In Progress |
| PBI | Done | Completed |
| PBI | Removed | Removed |
| Bug | New | Proposed |
| Bug | Approved | Proposed |
| Bug | Committed | In Progress |
| Bug | Done | Completed |
| Bug | Removed | Removed |
| Task | To Do | Proposed |
| Task | In Progress | In Progress |
| Task | Done | Completed |
| Task | Removed | Removed |
| Epic/Feature | New | Proposed |
| Epic/Feature | In Progress | In Progress |
| Epic/Feature | Done | Completed |
| Epic/Feature | Removed | Removed |
| Impediment | Open | In Progress |
| Impediment | Closed | Completed |

---

## 7. Constraints and Limits

### 7.1 Field Constraints

| Constraint | Limit |
|------------|-------|
| Max fields per work item type | 64 |
| Max fields per process | 512 |
| Max custom fields per organization | 1,024 |
| Field name max length | 128 Unicode characters |

### 7.2 Workflow Constraints

| Constraint | Limit |
|------------|-------|
| Min workflow states per WIT | 2 |
| Max workflow states per WIT | 32 |

### 7.3 API Constraints

| Constraint | Limit |
|------------|-------|
| Batch read operations | Max 200 items |
| List operations | Max 200 results |

### 7.4 Hierarchy Constraints

| Constraint | Description |
|------------|-------------|
| Parent-Child | One parent per child (tree topology) |
| Circular Reference | Not allowed in tree/dependency topologies |
| Cross-project links | Supported via remote link types |

---

## 8. Customization Model

### 8.1 Inherited Process

| Element | Customizable | Notes |
|---------|-------------|-------|
| Work Item Types | Add new, modify inherited | Cannot delete system types |
| Fields | Add custom, modify existing | Custom prefix: `Custom.{Name}` |
| States | Add custom, hide inherited | Cannot delete inherited states |
| Rules | Add field rules | Workflow validation |
| Forms | Modify layout | Add/remove/arrange fields |
| Link Types | **No** | System link types are fixed |

### 8.2 System Process Inheritance

```
System Process (Locked)
       │
       ▼
Inherited Process (Customizable)
       │
       ▼
Team Project (Uses Process)
```

---

## 9. Analysis Observations

### 9.1 Key Domain Concepts

1. **Hierarchical Containment**: Epic > Feature > PBI/Bug > Task
2. **State Categories**: Unify heterogeneous state names under common semantics
3. **Configurable Bug Tracking**: Bugs can live at requirement or task level
4. **Impediment as Side Entity**: Not part of main hierarchy, query-driven
5. **Effort vs. Remaining Work**: Different estimation models for different levels

### 9.2 Ontology Design Implications

| Observation | Implication for Jerry |
|-------------|----------------------|
| Tree hierarchy with strict one-parent rule | Enforce parent-child integrity |
| State categories abstract state names | Support custom states with category mapping |
| Configurable bug backlog level | Allow runtime configuration |
| Any-to-any transitions | Minimal transition restrictions |
| Field reference names are namespaced | Adopt similar naming convention |

### 9.3 Gaps Identified

| Gap | Description | Impact |
|-----|-------------|--------|
| No sprint entity | Iteration Path is a field, not an entity | Jerry may need Sprint as first-class entity |
| No explicit release entity | Implied via Target Date | Consider Release entity for planning |
| Limited impediment hierarchy | No parent-child support | Design decision: flat or hierarchical |

---

## Appendix A: Quick Reference

### A.1 Entity-Property Matrix

| Property | Epic | Feature | PBI | Task | Bug | Impediment |
|----------|:----:|:-------:|:---:|:----:|:---:|:----------:|
| Title | R | R | R | R | R | R |
| Description | O | O | O | O | O | O |
| Effort | O | O | O | - | O | - |
| Business Value | O | O | O | - | - | - |
| Priority | O | O | O | O | O | O |
| Acceptance Criteria | - | - | O | - | O | - |
| Remaining Work | - | - | - | O | - | - |
| Repro Steps | - | - | - | - | O | - |
| Severity | - | - | - | - | O | - |
| Resolution | - | - | - | - | - | O |
| Start Date | O | O | - | - | - | - |
| Target Date | O | O | - | - | - | - |

**Legend**: R = Required, O = Optional, - = Not Applicable

### A.2 State-Category Matrix

| Entity | Proposed | In Progress | Resolved | Completed | Removed |
|--------|:--------:|:-----------:|:--------:|:---------:|:-------:|
| Epic | New | In Progress | - | Done | Removed |
| Feature | New | In Progress | - | Done | Removed |
| PBI | New, Approved | Committed | - | Done | Removed |
| Task | To Do | In Progress | - | Done | Removed |
| Bug | New, Approved | Committed | - | Done | Removed |
| Impediment | - | Open | - | Closed | - |

---

**Document End**
