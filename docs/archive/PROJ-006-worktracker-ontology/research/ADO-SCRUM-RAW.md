# Azure DevOps Scrum Process Template - Domain Model Research

> **Research Document ID**: EN-001-ADO-SCRUM-RAW
> **Date**: 2026-01-13
> **Researcher**: ps-researcher (Claude Opus 4.5)
> **Project**: PROJ-006-worktracker-ontology
> **Status**: COMPLETE

---

## Executive Summary

This document captures comprehensive research on the Azure DevOps (ADO) Scrum process template domain model. The research covers work item types, their properties/fields, workflow states, relationship types, and supported operations. All information is sourced from official Microsoft documentation.

---

## 1. Entity Inventory: Work Item Types

### 1.1 Core Work Item Types in Scrum Process

The Scrum process template includes the following work item types (WITs):

| Work Item Type | Purpose | Backlog Level |
|----------------|---------|---------------|
| **Epic** | Large body of work spanning multiple features/releases | Portfolio Backlog (Level 2) |
| **Feature** | Significant functionality delivering value | Portfolio Backlog (Level 1) |
| **Product Backlog Item (PBI)** | User stories, requirements, work to be done | Product Backlog |
| **Task** | Discrete units of work supporting PBIs | Sprint Backlog |
| **Bug** | Code defects and issues | Product Backlog or Sprint Backlog (configurable) |
| **Impediment** | Blocking issues that impede progress | Not on backlog (tracked via queries) |

> **Citation**: "Scrum is a process tailored for Scrum teams, featuring Epics, Features, Product Backlog Items (PBIs), and Tasks." - [Microsoft Learn: Scrum Process](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/scrum-process?view=azure-devops)

### 1.2 Work Item Hierarchy

```
Epic (Portfolio Level 2)
  └── Feature (Portfolio Level 1)
        └── Product Backlog Item (PBI)
              └── Task
```

> **Citation**: "Epics and features are used to group work under larger scenarios. Product backlog items and Tasks are used to track work. Bugs track code defects." - [Microsoft Learn: Scrum Process](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/scrum-process?view=azure-devops)

### 1.3 Additional Work Item Types

| Work Item Type | Purpose | Notes |
|----------------|---------|-------|
| **Test Case** | Define test steps and expected results | Consistent across all processes |
| **Test Plan** | Group test suites and test cases | Consistent across all processes |
| **Test Suite** | Organize test cases | Consistent across all processes |

---

## 2. Properties and Fields

### 2.1 System Fields (All Work Item Types)

These fields are automatically available for all work item types:

| Field Name | Reference Name | Data Type | Description |
|------------|----------------|-----------|-------------|
| ID | `System.Id` | Integer | Unique work item identifier |
| Title | `System.Title` | String | Work item name/title |
| Description | `System.Description` | HTML | Detailed description |
| State | `System.State` | String | Current workflow state |
| Reason | `System.Reason` | String | Reason for state change |
| Area Path | `System.AreaPath` | TreePath | Organizational area |
| Iteration Path | `System.IterationPath` | TreePath | Sprint/iteration assignment |
| Work Item Type | `System.WorkItemType` | String | Type classification |
| Team Project | `System.TeamProject` | String | Project assignment |
| Assigned To | `System.AssignedTo` | Identity | Current owner |
| Created By | `System.CreatedBy` | Identity | Creator (read-only) |
| Created Date | `System.CreatedDate` | DateTime | Creation timestamp (read-only) |
| Changed By | `System.ChangedBy` | Identity | Last modifier (read-only) |
| Changed Date | `System.ChangedDate` | DateTime | Last modification (read-only) |
| Closed By | `System.ClosedBy` | Identity | Person who closed |
| Closed Date | `System.ClosedDate` | DateTime | Closure timestamp |
| Revision | `System.Rev` | Integer | Revision number (read-only) |
| Tags | `System.Tags` | String | Custom categorization tags |
| External Link Count | `System.ExternalLinkCount` | Integer | Count of external links |
| Hyperlink Count | `System.HyperLinkCount` | Integer | Count of hyperlinks |
| Related Link Count | `System.RelatedLinkCount` | Integer | Count of related links |
| Attached File Count | `System.AttachedFileCount` | Integer | Count of attachments |

> **Citation**: "Core system fields are automatically included for every work item type. System fields are automatically defined for all WITs, even if they aren't included in the WIT definition." - [Microsoft Learn: Work Item Fields](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/work-item-fields?view=azure-devops)

### 2.2 Scrum-Specific Fields

| Field Name | Reference Name | Data Type | Applicable To |
|------------|----------------|-----------|---------------|
| Acceptance Criteria | `Microsoft.VSTS.Common.AcceptanceCriteria` | HTML | PBI, Bug |
| Backlog Priority | `Microsoft.VSTS.Common.BacklogPriority` | Double | All backlog items |
| Resolution | `Microsoft.VSTS.Common.Resolution` | String | Bug |

### 2.3 Common Planning Fields

| Field Name | Reference Name | Data Type | Description |
|------------|----------------|-----------|-------------|
| Priority | `Microsoft.VSTS.Common.Priority` | Integer | Item prioritization (1-4, 1=highest) |
| Effort | `Microsoft.VSTS.Scheduling.Effort` | Double | Relative work estimate |
| Remaining Work | `Microsoft.VSTS.Scheduling.RemainingWork` | Double | Outstanding work (Tasks) |
| Completed Work | `Microsoft.VSTS.Scheduling.CompletedWork` | Double | Work completed (Tasks) |
| Business Value | `Microsoft.VSTS.Common.BusinessValue` | Integer | Relative business value |
| Value Area | `Microsoft.VSTS.Common.ValueArea` | String | Business vs. Architectural |
| Time Criticality | `Microsoft.VSTS.Common.TimeCriticality` | Double | How value decreases over time |
| Stack Rank | `Microsoft.VSTS.Common.StackRank` | Double | Backlog ordering |

> **Citation**: "Effort field allows you to enter a number that indicates a relative rating (size) of the amount of work required. Business Value is a number field that indicates a fixed or relative value of delivering the item." - [Microsoft Learn: Define Features and Epics](https://learn.microsoft.com/en-us/azure/devops/boards/backlogs/define-features-epics?view=azure-devops)

### 2.4 Fields by Work Item Type

#### Epic Fields

| Field Name | Reference Name | Required | Description |
|------------|----------------|----------|-------------|
| Title | `System.Title` | Yes | Epic name |
| Description | `System.Description` | No | Detailed description |
| Effort | `Microsoft.VSTS.Scheduling.Effort` | No | Size estimate |
| Business Value | `Microsoft.VSTS.Common.BusinessValue` | No | Business priority |
| Value Area | `Microsoft.VSTS.Common.ValueArea` | No | Business/Architectural |
| Time Criticality | `Microsoft.VSTS.Common.TimeCriticality` | No | Time sensitivity |
| Start Date | `Microsoft.VSTS.Scheduling.StartDate` | No | Planned start |
| Target Date | `Microsoft.VSTS.Scheduling.TargetDate` | No | Target completion |
| Priority | `Microsoft.VSTS.Common.Priority` | No | Priority (1-4) |

#### Feature Fields

| Field Name | Reference Name | Required | Description |
|------------|----------------|----------|-------------|
| Title | `System.Title` | Yes | Feature name |
| Description | `System.Description` | No | Detailed description |
| Effort | `Microsoft.VSTS.Scheduling.Effort` | No | Size estimate |
| Business Value | `Microsoft.VSTS.Common.BusinessValue` | No | Business priority |
| Value Area | `Microsoft.VSTS.Common.ValueArea` | No | Business/Architectural |
| Time Criticality | `Microsoft.VSTS.Common.TimeCriticality` | No | Time sensitivity |
| Start Date | `Microsoft.VSTS.Scheduling.StartDate` | No | Planned start |
| Target Date | `Microsoft.VSTS.Scheduling.TargetDate` | No | Target completion |
| Priority | `Microsoft.VSTS.Common.Priority` | No | Priority (1-4) |

#### Product Backlog Item (PBI) Fields

| Field Name | Reference Name | Required | Description |
|------------|----------------|----------|-------------|
| Title | `System.Title` | Yes | PBI name |
| Description | `System.Description` | No | Detailed description |
| Acceptance Criteria | `Microsoft.VSTS.Common.AcceptanceCriteria` | No | Done criteria |
| Effort | `Microsoft.VSTS.Scheduling.Effort` | No | Story points |
| Business Value | `Microsoft.VSTS.Common.BusinessValue` | No | Business priority |
| Priority | `Microsoft.VSTS.Common.Priority` | No | Priority (1-4) |
| Backlog Priority | `Microsoft.VSTS.Common.BacklogPriority` | No | Backlog ordering |

#### Task Fields

| Field Name | Reference Name | Required | Description |
|------------|----------------|----------|-------------|
| Title | `System.Title` | Yes | Task name |
| Description | `System.Description` | No | Task details |
| Remaining Work | `Microsoft.VSTS.Scheduling.RemainingWork` | No | Hours remaining |
| Activity | `Microsoft.VSTS.Common.Activity` | No | Type of work |
| Priority | `Microsoft.VSTS.Common.Priority` | No | Priority (1-4) |

> **Citation**: "Tasks support tracking Remaining Work only." - [Microsoft Learn: Scrum Process](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/scrum-process?view=azure-devops)

#### Bug Fields

| Field Name | Reference Name | Required | Description |
|------------|----------------|----------|-------------|
| Title | `System.Title` | Yes | Bug title |
| Repro Steps | `Microsoft.VSTS.TCM.ReproSteps` | No | Steps to reproduce |
| System Info | `Microsoft.VSTS.TCM.SystemInfo` | No | System information |
| Acceptance Criteria | `Microsoft.VSTS.Common.AcceptanceCriteria` | No | Done criteria |
| Effort | `Microsoft.VSTS.Scheduling.Effort` | No | Size estimate |
| Priority | `Microsoft.VSTS.Common.Priority` | No | Priority (1-4) |
| Severity | `Microsoft.VSTS.Common.Severity` | No | Bug severity |
| Found In Build | `Microsoft.VSTS.Build.FoundIn` | No | Build version |
| Integrated In Build | `Microsoft.VSTS.Build.IntegrationBuild` | No | Fixed in build |

#### Impediment Fields

| Field Name | Reference Name | Required | Description |
|------------|----------------|----------|-------------|
| Title | `System.Title` | Yes | Impediment title |
| Description | `System.Description` | No | Details |
| Priority | `Microsoft.VSTS.Common.Priority` | No | Priority (1-4) |
| Resolution | `Microsoft.VSTS.Common.Resolution` | No | How resolved |

> **Citation**: "Impediments and issues represent unplanned activities. Resolving them requires more work beyond what's tracked for actual requirements." - [Microsoft Learn: Manage Issues and Impediments](https://learn.microsoft.com/en-us/azure/devops/boards/backlogs/manage-issues-impediments?view=azure-devops)

---

## 3. Workflow States and Transitions

### 3.1 State Categories

Azure DevOps uses state categories to organize workflow states:

| Category | Purpose | Backlog Display | Board Position |
|----------|---------|-----------------|----------------|
| **Proposed** | Newly created items | Appears | First column |
| **In Progress** | Active work | Appears | Middle columns |
| **Resolved** | Solution implemented, awaiting verification | Appears | Middle columns |
| **Completed** | Finished work | Hidden | Final column |
| **Removed** | Hidden/archived items | Hidden | Not displayed |

> **Citation**: "Azure Boards uses state categories so Agile planning tools and dashboards treat workflow states consistently across backlogs and boards." - [Microsoft Learn: Workflow and State Categories](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/workflow-and-state-categories?view=azure-devops)

### 3.2 Product Backlog Item (PBI) States

| State | Category | Default Reason | Description |
|-------|----------|----------------|-------------|
| **New** | Proposed | "New backlog item" | Initial state, candidate ideas |
| **Approved** | Proposed | - | Described enough for estimation |
| **Committed** | In Progress | - | Agreed for inclusion in sprint |
| **Done** | Completed | - | Meets acceptance criteria |
| **Removed** | Removed | - | Hidden from backlog |

**Workflow Progression**:
```
New → Approved → Committed → Done
         ↑           ↓
         └───────────┘ (regression allowed)
```

> **Citation**: "The product owner moves the item to Approved once described enough for the team to estimate effort. The team sets the status to Committed when they agree to include the item in the sprint. The team moves the item to Done when all associated tasks are complete." - [Microsoft Learn: Scrum Process Workflow](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/scrum-process-workflow?view=azure-devops)

### 3.3 Bug States

| State | Category | Default Reason | Description |
|-------|----------|----------------|-------------|
| **New** | Proposed | "New" | Bug reported |
| **Approved** | Proposed | - | Bug validated/triaged |
| **Committed** | In Progress | - | Fix included in sprint |
| **Done** | Completed | - | Bug fixed and verified |
| **Removed** | Removed | - | Hidden from backlog |

**Workflow Progression**:
```
New → Approved → Committed → Done
```

### 3.4 Task States

| State | Category | Description |
|-------|----------|-------------|
| **To Do** | Proposed | Task created, not started |
| **In Progress** | In Progress | Work begun |
| **Done** | Completed | Task complete |
| **Removed** | Removed | Hidden |

**Workflow Progression**:
```
To Do → In Progress → Done
```

### 3.5 Epic and Feature States

| State | Category | Description |
|-------|----------|-------------|
| **New** | Proposed | Initial state |
| **In Progress** | In Progress | Active work (custom state, commonly added) |
| **Done** | Completed | Feature/Epic complete |
| **Removed** | Removed | Hidden |

> **Citation**: "In the Scrum process, Epics, Features, Bugs, and Product Backlog Items start in the New state. For Epics, Features, Bugs, and Product Backlog Items, the Committed state falls into [In Progress] category." - [Microsoft Learn: Workflow and State Categories](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/workflow-and-state-categories?view=azure-devops)

### 3.6 Impediment States

| State | Category | Description |
|-------|----------|-------------|
| **Open** | In Progress | Impediment active/unresolved |
| **Closed** | Completed | Impediment resolved |

> **Citation**: "For Impediment work items in the Scrum process, the state 'Open' is used, which maps to the 'In Progress' state category." - [Microsoft Learn: Workflow and State Categories](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/workflow-and-state-categories?view=azure-devops)

### 3.7 State Transition Rules

- Most work item types support **any-to-any transitions** (forward and backward)
- Transitions to "Removed" state hide items from backlog and boards
- When adding custom states, system automatically creates transitions to all inherited states (except Removed)
- Minimum: 2 workflow states per work item type
- Maximum: 32 workflow states per work item type

> **Citation**: "Most work item types used by Agile tools, the ones that appear on backlogs and boards, support any-to-any transitions." - [Microsoft Learn: Workflow and State Categories](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/workflow-and-state-categories?view=azure-devops)

---

## 4. Relationship Types (Link Types)

### 4.1 Work Link Types (System-Defined)

| Link Type | Reference Name | Topology | Description |
|-----------|----------------|----------|-------------|
| **Parent-Child** | `System.LinkTypes.Hierarchy-Forward` / `Hierarchy-Reverse` | Tree | Hierarchical relationships; one parent, many children |
| **Related** | `System.LinkTypes.Related` | Network | Non-directional; relates items at same level |
| **Predecessor-Successor** | `System.LinkTypes.Dependency-Forward` / `Dependency-Reverse` | Dependency | Task dependencies; must complete before |
| **Duplicate-Duplicate Of** | `System.LinkTypes.Duplicate-Forward` / `Duplicate-Reverse` | Tree | Track duplicate work items |

> **Citation**: "Parent-child links represent summary tasks and their subordinate tasks. A work item can have only one Parent. A parent work item can have many children." - [Microsoft Learn: Link Type Reference](https://learn.microsoft.com/en-us/azure/devops/boards/queries/link-type-reference?view=azure-devops)

### 4.2 Process-Defined Link Types

| Link Type | Reference Name | Topology | Description |
|-----------|----------------|----------|-------------|
| **Tested By-Tests** | `Microsoft.VSTS.Common.TestedBy-Forward` / `TestedBy-Reverse` | Dependency | Links test cases to work items |
| **Test Case-Shared Steps** | `Microsoft.VSTS.TestCase.SharedStepReferencedBy-Forward` / `SharedStepReferencedBy-Reverse` | Dependency | Links shared steps |
| **Affects-Affected By** | `Microsoft.VSTS.Common.Affects-Forward` / `Affects-Reverse` (CMMI only) | Dependency | Change request links |

### 4.3 External Link Types

| Link Type | Artifact Type | Description |
|-----------|---------------|-------------|
| Branch | Git | Links to Git branch |
| Build / Pipelines | Build | Links to build |
| Changeset | TFVC | Links to TFVC changeset |
| Commit / Fixed in Commit | Git Commit | Links to Git commit |
| Pull Request | Pull Request | Links to pull request |
| Wiki | Wiki | Links to wiki page |
| Hyperlink | URL | Links to any URL |

### 4.4 Remote Link Types (Cross-Organization)

| Link Type | Reference Name | Description |
|-----------|----------------|-------------|
| Consumes From-Produced For | `System.LinkTypes.Remote.Dependency-Forward/Reverse` | Cross-org dependencies |
| Remote Related | `System.LinkTypes.Remote.Related` | Cross-org relationships |

### 4.5 GitHub Link Types

| Link Type | Description |
|-----------|-------------|
| GitHub Commit | Links to GitHub commit |
| GitHub Issue | Links to GitHub issue |
| GitHub Pull Request | Links to GitHub pull request |

### 4.6 Link Type Topology Definitions

| Topology | Characteristics |
|----------|-----------------|
| **Tree** | Hierarchical; one parent, multiple children; no circular references |
| **Network** | Non-directional; many-to-many relationships |
| **Dependency** | Directional; defines order/sequence |

> **Citation**: "The parent-child link type defines two labels (Parent and Child), supports a hierarchical or tree topology, and prevents circular references from being created between work items." - [Microsoft Learn: Link Type Reference](https://learn.microsoft.com/en-us/azure/devops/boards/queries/link-type-reference?view=azure-devops)

---

## 5. Supported Operations/Behaviors

### 5.1 REST API Operations

| Operation | HTTP Method | Endpoint Pattern | Description |
|-----------|-------------|------------------|-------------|
| **Create** | POST | `/_apis/wit/workitems/${type}` | Create single work item |
| **Get Work Item** | GET | `/_apis/wit/workitems/{id}` | Retrieve single work item |
| **Get Work Items Batch** | POST | `/_apis/wit/workitemsbatch` | Retrieve multiple (max 200) |
| **List** | GET | `/_apis/wit/workitems?ids=...` | List work items (max 200) |
| **Update** | PATCH | `/_apis/wit/workitems/{id}` | Update single work item |
| **Delete** | DELETE | `/_apis/wit/workitems/{id}` | Delete (to Recycle Bin) |
| **Delete Work Items** | DELETE | `/_apis/wit/workitems?ids=...` | Delete multiple items |
| **Get Template** | GET | `/_apis/wit/workitems/${type}/template` | Get work item template |

> **Citation**: "The Work Item API is used for listing, creating and updating work items. REST APIs are service endpoints that support sets of HTTP operations (methods), which provide create, retrieve, update, or delete access to the service's resources." - [Microsoft Learn: Work Items REST API](https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items?view=azure-devops-rest-7.1)

### 5.2 Create Operation Example

```http
POST https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Product%20Backlog%20Item?api-version=7.1
Content-Type: application/json-patch+json

[
  {
    "op": "add",
    "path": "/fields/System.Title",
    "value": "Sample PBI"
  },
  {
    "op": "add",
    "path": "/fields/System.Description",
    "value": "Description of the PBI"
  }
]
```

### 5.3 Update Operation Example

```http
PATCH https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.1
Content-Type: application/json-patch+json

[
  {
    "op": "replace",
    "path": "/fields/System.State",
    "value": "Committed"
  }
]
```

### 5.4 Link Operations

```http
PATCH https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.1
Content-Type: application/json-patch+json

[
  {
    "op": "add",
    "path": "/relations/-",
    "value": {
      "rel": "System.LinkTypes.Hierarchy-Forward",
      "url": "https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{childId}"
    }
  }
]
```

### 5.5 State Transition Operation

State transitions are performed via the Update operation by changing the `System.State` field:

```json
[
  {
    "op": "replace",
    "path": "/fields/System.State",
    "value": "Done"
  },
  {
    "op": "add",
    "path": "/fields/System.Reason",
    "value": "Acceptance tests passed"
  }
]
```

### 5.6 Query Operations

| Operation | HTTP Method | Endpoint | Description |
|-----------|-------------|----------|-------------|
| Execute WIQL | POST | `/_apis/wit/wiql` | Execute Work Item Query Language |
| Get Query | GET | `/_apis/wit/queries/{id}` | Get saved query |
| List Queries | GET | `/_apis/wit/queries` | List all queries |

### 5.7 Field Operations

| Operation | HTTP Method | Endpoint | Description |
|-----------|-------------|----------|-------------|
| List Fields | GET | `/_apis/wit/fields` | Get all field definitions |
| Get Field | GET | `/_apis/wit/fields/{fieldName}` | Get single field definition |
| List WIT Fields | GET | `/_apis/wit/workitemtypes/{type}/fields` | Get fields for a work item type |

### 5.8 Optional Operation Parameters

| Parameter | Description |
|-----------|-------------|
| `validateOnly` | Validate without saving |
| `bypassRules` | Skip workflow rules (requires permission) |
| `suppressNotifications` | Don't send notifications |
| `$expand` | Expand related data (Relations, Fields, Links, All) |
| `destroy` | Permanently delete (skip Recycle Bin) |

### 5.9 API Version

Current latest version: **7.1** (as of 2025)

> **Citation**: "Azure DevOps Service is compatible with the most recent REST API version (including preview versions), as well as previous versions. Microsoft highly recommends using the latest release version of the REST API." - [Microsoft Learn: REST API](https://learn.microsoft.com/en-us/rest/api/azure/devops/?view=azure-devops-rest-7.2)

---

## 6. Bug Tracking Configuration

### 6.1 Bug Tracking Options

Teams can configure how bugs appear on backlogs:

| Setting | Behavior |
|---------|----------|
| **Bugs are managed with requirements** | Bugs appear on Product Backlog alongside PBIs |
| **Bugs are managed with tasks** | Bugs appear on Sprint Backlog/Taskboard |
| **Bugs are not managed on backlogs** | Bugs tracked only via queries |

> **Citation**: "Each team can configure how they manage bugs at the same level as product backlog items or Task work items. Use the Working with bugs setting." - [Microsoft Learn: Scrum Process](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/scrum-process?view=azure-devops)

---

## 7. Constraints and Limits

### 7.1 Field Limits

| Constraint | Limit |
|------------|-------|
| Max fields per work item type | 64 |
| Max fields per process | 512 |
| Max custom fields per organization | 1,024 |
| Field name max length | 128 Unicode characters |

### 7.2 Workflow Limits

| Constraint | Limit |
|------------|-------|
| Min workflow states | 2 |
| Max workflow states per WIT | 32 |

### 7.3 API Limits

| Constraint | Limit |
|------------|-------|
| Batch operations | Max 200 items |
| List operations | Max 200 results |

---

## 8. Process Customization

### 8.1 Inherited Process Model

- System processes (Agile, Scrum, CMMI, Basic) are locked
- Create inherited process to customize
- Can add custom fields, states, work item types
- Custom field reference name pattern: `Custom.{FieldName}`

### 8.2 Customization Options

| Element | Can Customize |
|---------|--------------|
| Work item types | Add new, modify inherited |
| Fields | Add custom, modify existing |
| States | Add custom, hide inherited |
| Rules | Add field rules |
| Forms | Modify layout |
| Link types | Cannot customize system types |

> **Citation**: "You can customize the workflow of any work item type (WIT) by hiding inherited states or adding custom states. The system processes Agile, Basic, Scrum, and CMMI are locked, and users can't change them." - [Microsoft Learn: Workflow Customization](https://learn.microsoft.com/en-us/azure/devops/organizations/settings/work/customize-process-workflow?view=azure-devops)

---

## 9. Key Differences: Scrum vs Other Processes

| Aspect | Scrum | Agile | CMMI |
|--------|-------|-------|------|
| Backlog Item | Product Backlog Item | User Story | Requirement |
| Estimation Field | Effort | Story Points | Size |
| Tracking Field | Remaining Work only | Remaining Work, Completed Work | Original Estimate, Remaining Work, Completed Work |
| Blocking Item | Impediment | Issue | Issue |

> **Citation**: "Choose Scrum when your team practices Scrum. This process works great for tracking product backlog items and bugs on the board. Tasks support tracking Remaining Work only." - [Microsoft Learn: Choose Process](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/choose-process?view=azure-devops)

---

## 10. Sources and Citations

### Primary Sources (Official Microsoft Documentation)

1. [Manage Scrum process template objects - Azure Boards](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/scrum-process?view=azure-devops)
2. [Manage Scrum process work items types & workflow - Azure Boards](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/scrum-process-workflow?view=azure-devops)
3. [Work Item Fields For Agile and Scrum Processes - Azure Boards](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/work-item-field?view=azure-devops)
4. [List work item fields and attributes in Azure Boards](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/work-item-fields?view=azure-devops)
5. [How workflow category states are used in Azure Boards](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/workflow-and-state-categories?view=azure-devops)
6. [Link Types Reference Guide - Azure Boards](https://learn.microsoft.com/en-us/azure/devops/boards/queries/link-type-reference?view=azure-devops)
7. [Define features and epics to organize backlog items - Azure Boards](https://learn.microsoft.com/en-us/azure/devops/boards/backlogs/define-features-epics?view=azure-devops)
8. [Manage and resolve issues or impediments in Azure Boards](https://learn.microsoft.com/en-us/azure/devops/boards/backlogs/manage-issues-impediments?view=azure-devops)
9. [Work Items - REST API (Azure DevOps)](https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items?view=azure-devops-rest-7.1)
10. [Default processes and process templates - Azure Boards](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/choose-process?view=azure-devops)

### API Documentation

11. [Work Items - Create - REST API](https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/create?view=azure-devops-rest-7.1)
12. [Work Items - Update - REST API](https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/update?view=azure-devops-rest-7.1)
13. [Work Items - Delete - REST API](https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/delete?view=azure-devops-rest-7.1)
14. [Fields - List - REST API](https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/fields/list?view=azure-devops-rest-7.1)
15. [Work Item Types Field - List - REST API](https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-item-types-field/list?view=azure-devops-rest-7.1)

---

## Appendix A: Quick Reference Tables

### A.1 Work Item Type Summary

| Type | States | Parent | Children |
|------|--------|--------|----------|
| Epic | New, Done, Removed | None | Feature |
| Feature | New, Done, Removed | Epic | PBI |
| PBI | New, Approved, Committed, Done, Removed | Feature | Task |
| Task | To Do, In Progress, Done, Removed | PBI | None |
| Bug | New, Approved, Committed, Done, Removed | Feature/PBI | Task |
| Impediment | Open, Closed | None | None |

### A.2 Key Field Reference Names

| Field | Reference Name |
|-------|----------------|
| Title | `System.Title` |
| State | `System.State` |
| Assigned To | `System.AssignedTo` |
| Iteration Path | `System.IterationPath` |
| Area Path | `System.AreaPath` |
| Effort | `Microsoft.VSTS.Scheduling.Effort` |
| Business Value | `Microsoft.VSTS.Common.BusinessValue` |
| Priority | `Microsoft.VSTS.Common.Priority` |
| Remaining Work | `Microsoft.VSTS.Scheduling.RemainingWork` |
| Acceptance Criteria | `Microsoft.VSTS.Common.AcceptanceCriteria` |

### A.3 Link Type Reference Names

| Link Type | Forward Reference | Reverse Reference |
|-----------|-------------------|-------------------|
| Parent-Child | `System.LinkTypes.Hierarchy-Forward` | `System.LinkTypes.Hierarchy-Reverse` |
| Related | `System.LinkTypes.Related` | `System.LinkTypes.Related` |
| Predecessor-Successor | `System.LinkTypes.Dependency-Forward` | `System.LinkTypes.Dependency-Reverse` |
| Duplicate | `System.LinkTypes.Duplicate-Forward` | `System.LinkTypes.Duplicate-Reverse` |

---

**Document End**
