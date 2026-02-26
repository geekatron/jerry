# JIRA Domain Model

**Analysis ID:** EN-003-JIRA-MODEL
**Project:** PROJ-006-worktracker-ontology
**Date:** 2026-01-13
**Analyst:** ps-analyst (Claude)
**Source:** EN-003-JIRA-RAW.md
**Status:** COMPLETE

---

## 1. Entity Catalog

### 1.1 Issue Type Hierarchy

| Entity | Description | Hierarchy Level | Can Be Parent | Can Be Child | Products |
|--------|-------------|-----------------|---------------|--------------|----------|
| **Initiative** | Strategic goal spanning multiple teams/projects | Level 2+ | Yes | No | Premium/Enterprise only |
| **Epic** | Large body of work, groups Stories/Tasks/Bugs | Level 1 | Yes | Yes (of Initiative) | Software, Premium |
| **Story** | User requirement from user perspective | Level 0 | Yes | Yes (of Epic) | Software |
| **Task** | Generic work item (catch-all) | Level 0 | Yes | Yes (of Epic) | All products |
| **Bug** | Problem impairing product functionality | Level 0 | Yes | Yes (of Epic) | Software |
| **Sub-task** | Granular decomposition of parent work | Level -1 | No | Yes (of Story/Task/Bug) | All products |

### 1.2 Service Management Issue Types (Jira Service Management)

| Entity | Description | Purpose |
|--------|-------------|---------|
| **Change** | Change management request | Controlled change process |
| **Incident** | Service disruption | Incident response |
| **Problem** | Root cause investigation | Root cause analysis |
| **Service Request** | Standard service request | Service fulfillment |
| **Service Request with Approval** | Request requiring authorization | Approval workflows |
| **IT Help** | Internal IT support | Internal support |
| **Support** | External support ticket | Customer support |
| **New Feature** | Feature request | Enhancement tracking |

### 1.3 Hierarchy Visualization

```
STANDARD HIERARCHY (All Products):

Level 2+:   [Initiative]  ← Premium/Enterprise only
                │
Level 1:       [Epic]
                │
Level 0:    ┌───┴───┬───────┐
           [Story] [Task]  [Bug]
             │       │       │
Level -1: [Sub-task] [Sub-task] [Sub-task]


BUSINESS HIERARCHY (Jira Work Management):

Level 0:      [Task]
                │
Level -1:   [Sub-task]
```

### 1.4 Parent-Child Relationship Rules

| Rule | Description |
|------|-------------|
| **Flexible Parenting** | Any work type can be parent or child (except Sub-task) |
| **Sub-task Terminal** | Sub-tasks cannot have children |
| **Child Limit** | Maximum 500 child work items per parent |
| **Cross-Project** | Parent-child relationships can span projects (with Premium) |

---

## 2. Standard Fields

### 2.1 System Fields (Always Present)

| Field | Type | Required | Editable | Description |
|-------|------|----------|----------|-------------|
| **Project** | Reference | Yes | Create-only | Container for the issue |
| **Issue Type** | Enum | Yes | Yes | Classification (Epic, Story, etc.) |
| **Summary** | Text (255) | Yes | Yes | Brief title/description |
| **Status** | Enum | Yes | Via Workflow | Current workflow state |
| **Resolution** | Enum | No | Yes | How issue was resolved |
| **Key** | System | Auto | No | Unique identifier (e.g., PROJ-123) |
| **ID** | System | Auto | No | Internal numeric identifier |

### 2.2 Descriptive Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| **Description** | Rich Text | No | Detailed explanation |
| **Environment** | Text | No | Technical environment details |
| **Labels** | Multi-value Text | No | Free-form categorization tags |
| **Attachment** | File List | No | Associated files |
| **Comment** | Rich Text List | No | Discussion thread |

### 2.3 People Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| **Assignee** | User Picker | No | Person responsible |
| **Reporter** | User Picker | Auto | Person who created issue |
| **Watchers** | User List | No | Users following issue |

### 2.4 Categorization Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| **Priority** | Enum | No | Relative importance |
| **Component/s** | Multi-select | No | Project components affected |
| **Affects Version** | Version Picker | No | Versions where bug found |
| **Fix Version** | Version Picker | No | Target release version |

### 2.5 Time Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| **Due Date** | Date | No | Target completion date |
| **Original Estimate** | Duration | No | Initial time estimate |
| **Remaining Estimate** | Duration | No | Time remaining |
| **Time Spent** | Duration | Auto | Actual time logged |
| **Created** | DateTime | Auto | Creation timestamp |
| **Updated** | DateTime | Auto | Last modification timestamp |
| **Resolved** | DateTime | Auto | Resolution timestamp |

### 2.6 Agile/Software Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| **Sprint** | Sprint Picker | No | Associated sprint(s) |
| **Story Points** | Number | No | Relative effort estimation |
| **Parent** | Issue Picker | No | Parent issue in hierarchy |
| **Epic Link** | Issue Picker | No | Parent epic (legacy field) |

### 2.7 Relationship Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| **Linked Issues** | Issue Links | No | Related issues with link type |
| **Parent** | Issue Picker | No | Hierarchical parent |

---

## 3. Custom Field Types

### 3.1 Text Field Types

| Type | Description | Character Limit | Formatting |
|------|-------------|-----------------|------------|
| **Short Text (Single Line)** | Plain text input | 255 characters | None |
| **Paragraph (Multi-Line)** | Rich text with formatting | Unlimited | Rich text |

### 3.2 Number Field Types

| Type | Description | Range | Precision |
|------|-------------|-------|-----------|
| **Number** | Numeric input | -1T to 1T | 3 decimal places |
| **Number (Currency)** | Currency-formatted | -1T to 1T | 3 decimal places |
| **Number (Percentage)** | Percentage-formatted | -1T to 1T | 3 decimal places |

### 3.3 Selection Field Types

| Type | Description | Options Limit | Multi-select |
|------|-------------|---------------|--------------|
| **Dropdown** | Single choice from list | 55 | No |
| **Multi-select** | Multiple choices from list | 55 | Yes |
| **Cascading Select** | Parent-child option hierarchy | Varies | No |
| **Radio Buttons** | Single choice (visible) | Limited | No |
| **Checkboxes** | Multiple true/false | Limited | Yes |

### 3.4 Date/Time Field Types

| Type | Description | Includes Time |
|------|-------------|---------------|
| **Date Picker** | Calendar date selection | No |
| **Date Time Picker** | Date and time selection | Yes |

### 3.5 Reference Field Types

| Type | Description | Multi-select |
|------|-------------|--------------|
| **User Picker (Single)** | Single user selection | No |
| **User Picker (Multiple)** | Multiple user selection | Yes |
| **Group Picker (Single)** | Single group selection | No |
| **Group Picker (Multiple)** | Multiple group selection | Yes |
| **Version Picker** | Select version(s) | Yes |
| **Sprint** | Select sprint(s) | Yes |
| **Parent** | Associate with parent issue | No |
| **Labels** | Create or select labels | Yes |
| **Team** | Select Atlassian Team | No |

### 3.6 Computed/Read-Only Field Types

| Type | Description | Update Frequency |
|------|-------------|------------------|
| **Date of First Response** | First comment timestamp | Auto |
| **Days Since Last Comment** | Activity recency metric | Auto |
| **Participants of Work Item** | All contributors list | Auto |
| **Time in Status** | Workflow metrics | Auto |

---

## 4. Entity Behaviors

### 4.1 Issue CRUD Operations

| Entity | Behavior | Description | API Endpoint |
|--------|----------|-------------|--------------|
| Issue | **Create** | Create new issue | `POST /rest/api/3/issue` |
| Issue | **Read** | Get issue details | `GET /rest/api/3/issue/{key}` |
| Issue | **Update** | Modify issue fields | `PUT /rest/api/3/issue/{key}` |
| Issue | **Delete** | Remove issue | `DELETE /rest/api/3/issue/{key}` |
| Issue | **Bulk Create** | Create multiple issues | `POST /rest/api/3/issue/bulk` |
| Issue | **Bulk Delete** | Delete multiple issues | `DELETE /rest/api/3/issue` |

### 4.2 Workflow Transitions

| Entity | Behavior | Description | API Endpoint |
|--------|----------|-------------|--------------|
| Issue | **Transition** | Change status | `POST /rest/api/3/issue/{key}/transitions` |
| Issue | **Get Transitions** | List available transitions | `GET /rest/api/3/issue/{key}/transitions` |

### 4.3 Linking Operations

| Entity | Behavior | Description | API Endpoint |
|--------|----------|-------------|--------------|
| Link | **Create Link** | Link two issues | `POST /rest/api/3/issueLink` |
| Link | **Delete Link** | Remove link | `DELETE /rest/api/3/issueLink/{id}` |
| Link | **Get Links** | List issue links | `GET /rest/api/3/issue/{key}?fields=issuelinks` |

### 4.4 Comment Operations

| Entity | Behavior | Description | API Endpoint |
|--------|----------|-------------|--------------|
| Comment | **Add Comment** | Add comment to issue | `POST /rest/api/3/issue/{key}/comment` |
| Comment | **Update Comment** | Modify comment | `PUT /rest/api/3/issue/{key}/comment/{id}` |
| Comment | **Delete Comment** | Remove comment | `DELETE /rest/api/3/issue/{key}/comment/{id}` |

### 4.5 Attachment Operations

| Entity | Behavior | Description | API Endpoint |
|--------|----------|-------------|--------------|
| Attachment | **Add Attachment** | Attach file | `POST /rest/api/3/issue/{key}/attachments` |
| Attachment | **Get Attachment** | Download file | `GET /rest/api/3/attachment/{id}` |
| Attachment | **Delete Attachment** | Remove file | `DELETE /rest/api/3/attachment/{id}` |

### 4.6 Worklog Operations

| Entity | Behavior | Description | API Endpoint |
|--------|----------|-------------|--------------|
| Worklog | **Log Work** | Record time spent | `POST /rest/api/3/issue/{key}/worklog` |
| Worklog | **Update Worklog** | Modify entry | `PUT /rest/api/3/issue/{key}/worklog/{id}` |
| Worklog | **Delete Worklog** | Remove entry | `DELETE /rest/api/3/issue/{key}/worklog/{id}` |

### 4.7 Search Operations

| Entity | Behavior | Description | API Endpoint |
|--------|----------|-------------|--------------|
| Search | **JQL Search** | Query issues | `POST /rest/api/3/search` |
| Search | **Get Field** | List fields | `GET /rest/api/3/field` |
| Search | **Create Meta** | Get creation metadata | `GET /rest/api/3/issue/createmeta` |

---

## 5. Link Types

### 5.1 Default Link Types

| Link Type | Outward Description | Inward Description | Use Case | Symmetrical |
|-----------|--------------------|--------------------|----------|-------------|
| **Blocks** | "blocks" | "is blocked by" | Dependency/blocker | No |
| **Relates** | "relates to" | "relates to" | General relationship | Yes |
| **Duplicates** | "duplicates" | "is duplicated by" | Same problem/request | No |
| **Clones** | "clones" | "is cloned by" | Copied issue | No |

### 5.2 Link Direction Model

```
Source Issue ──[Outward Link]──> Destination Issue
     │                               │
     └────[Inward Link]<─────────────┘

Example:
  PROJ-1 ──[blocks]──> PROJ-2
  PROJ-2 ──[is blocked by]──> PROJ-1
```

### 5.3 Link Type Semantics

| Type | Relationship | Direction Matters | Expected Behavior |
|------|--------------|-------------------|-------------------|
| **Blocks** | Dependency | Yes | Target cannot progress until source resolved |
| **Relates** | Association | No | Informational link only |
| **Duplicates** | Equivalence | Yes | One should be closed as duplicate |
| **Clones** | Copy | Yes | Clone expected to diverge from original |

### 5.4 Custom Link Types

| Attribute | Description | Required |
|-----------|-------------|----------|
| **Name** | Unique link type identifier | Yes |
| **Outward Description** | Text for source → destination | Yes |
| **Inward Description** | Text for destination → source | Yes |

---

## 6. Workflow States

### 6.1 Status Categories (Fixed)

| Category | Color | Position | JQL Clause | Description |
|----------|-------|----------|------------|-------------|
| **To Do** | Grey | Beginning | `statusCategory = "To Do"` | Work not started |
| **In Progress** | Blue | Middle | `statusCategory = "In Progress"` | Work underway |
| **Done** | Green | End | `statusCategory = Done` | Work complete |

> **Constraint:** Only three status categories exist. Custom categories cannot be created.

### 6.2 Default Statuses by Category

| Status | Category | Description |
|--------|----------|-------------|
| **Open** | To Do | Newly created, not started |
| **To Do** | To Do | Ready to be worked on |
| **Backlog** | To Do | In backlog for future |
| **In Progress** | In Progress | Currently being worked on |
| **In Review** | In Progress | Awaiting review |
| **Under Review** | In Progress | Being reviewed |
| **Approved** | In Progress | Approved, pending completion |
| **Done** | Done | Work completed |
| **Closed** | Done | Issue closed |
| **Resolved** | Done | Issue resolved |
| **Cancelled** | Done | Work cancelled |
| **Rejected** | Done | Work rejected |

### 6.3 Default Workflow

```
┌────────────────────────────────────────────────────────────────┐
│                     DEFAULT WORKFLOW                           │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  [TO DO]                                                       │
│  (grey)  ──────────────────┐                                  │
│     │                       │                                  │
│     │ Start Work            │ Cancel                           │
│     ▼                       │                                  │
│  [IN PROGRESS]              │                                  │
│  (blue)  ───────────────────┼──────────────────┐              │
│     │                       │                   │              │
│     │ Complete              │                   │ Block        │
│     ▼                       ▼                   ▼              │
│  [DONE]                [CANCELLED]          [BLOCKED]         │
│  (green)               (green)              (blue)            │
│                                                │              │
│                                                │ Unblock      │
│                                                ▼              │
│                                           [IN PROGRESS]       │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### 6.4 Workflow Transition Types

| Transition Type | Description | Use Case |
|-----------------|-------------|----------|
| **Common** | Connects two specific statuses | Standard flow |
| **Global** | Allows transition from any status | Emergency close/cancel |
| **Self-Looping** | Returns to same status | Trigger actions without state change |

### 6.5 Transition Features

| Feature | Description | Configuration |
|---------|-------------|---------------|
| **Triggers** | External event starts transition | Bitbucket, CI/CD events |
| **Conditions** | Prerequisite checks | User permissions, field values |
| **Validators** | Input validation | Required fields, formats |
| **Post Functions** | Actions after transition | Set fields, send notifications |
| **Properties** | Key-value metadata | Custom automation flags |

### 6.6 Resolution vs Status Model

```
┌─────────────────────────────────────────────────────────────┐
│                  ISSUE STATE MODEL                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Resolution Field:  [Not Set]  →  [Set: Done/Fixed/etc.]   │
│                         │               │                   │
│                         ▼               ▼                   │
│  Issue State:       [OPEN]          [CLOSED]                │
│                                                             │
│  Status:         Any status      Any status                 │
│                  (To Do,        (Done, Resolved,            │
│                   In Progress)   Cancelled, etc.)           │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  KEY INSIGHT: Issue is CLOSED when Resolution is SET,       │
│  regardless of Status value.                                │
└─────────────────────────────────────────────────────────────┘
```

### 6.7 Resolution Values

#### Standard Resolutions

| Resolution | Description | Typical Status |
|------------|-------------|----------------|
| **Done** | Work completed successfully | Done |
| **Fixed** | Issue has been resolved | Resolved |
| **Won't Do** | Team will not act on issue | Closed |
| **Won't Fix** | Issue will not be addressed | Closed |
| **Duplicate** | Duplicate of another issue | Closed |
| **Cannot Reproduce** | Unable to replicate issue | Closed |
| **Incomplete** | Insufficient information | Closed |

#### Service Management Resolutions

| Resolution | Description | Product |
|------------|-------------|---------|
| **Known Error** | Root cause documented | JSM |

---

## 7. Priority Values

### 7.1 Default Priority Levels

| Priority | Numeric Order | Description | Use Case |
|----------|---------------|-------------|----------|
| **Highest** | 1 | "This problem will block progress." | Critical blockers |
| **High** | 2 | "Serious problem that could block progress." | Important issues |
| **Medium** | 3 | "Has the potential to affect progress." | Standard priority |
| **Low** | 4 | "Minor problem or easily worked around." | Low impact issues |
| **Lowest** | 5 | "Trivial problem with little or no impact." | Cosmetic/minor |

### 7.2 Priority Customization

| Aspect | Customizable |
|--------|--------------|
| Priority names | Yes |
| Priority descriptions | Yes |
| Priority icons | Yes |
| Number of priorities | Yes |
| Priority order | Yes |

---

## 8. API Reference Summary

### 8.1 Core Endpoints

| Category | Endpoint | Method | Purpose |
|----------|----------|--------|---------|
| **Issues** | `/rest/api/3/issue` | POST | Create issue |
| **Issues** | `/rest/api/3/issue/{key}` | GET | Get issue |
| **Issues** | `/rest/api/3/issue/{key}` | PUT | Update issue |
| **Issues** | `/rest/api/3/issue/{key}` | DELETE | Delete issue |
| **Search** | `/rest/api/3/search` | POST | JQL search |
| **Transitions** | `/rest/api/3/issue/{key}/transitions` | GET | Get available transitions |
| **Transitions** | `/rest/api/3/issue/{key}/transitions` | POST | Execute transition |
| **Links** | `/rest/api/3/issueLink` | POST | Create link |
| **Links** | `/rest/api/3/issueLink/{id}` | DELETE | Delete link |

### 8.2 Metadata Endpoints

| Category | Endpoint | Method | Purpose |
|----------|----------|--------|---------|
| **Fields** | `/rest/api/3/field` | GET | List all fields |
| **Issue Types** | `/rest/api/3/issuetype` | GET | List issue types |
| **Statuses** | `/rest/api/3/status` | GET | List statuses |
| **Priorities** | `/rest/api/3/priority` | GET | List priorities |
| **Resolutions** | `/rest/api/3/resolution` | GET | List resolutions |
| **Create Meta** | `/rest/api/3/issue/createmeta` | GET | Get creation metadata |

### 8.3 Custom Field Reference Format

```
customfield_{id}

Example: Story Points with ID 10000 → customfield_10000
```

---

## 9. Constraints and Limits

### 9.1 Hierarchy Constraints

| Constraint | Value | Source |
|------------|-------|--------|
| Child items per parent | 500 max | Atlassian docs |
| Hierarchy depth (standard) | 3 levels (-1 to 1) | Default |
| Hierarchy depth (Premium) | Unlimited above Epic | Premium feature |
| Sub-task children | 0 (terminal node) | By design |

### 9.2 Field Constraints

| Constraint | Value |
|------------|-------|
| Short text length | 255 characters |
| Dropdown options | 55 max |
| Number range | -1T to 1T |
| Number precision | 3 decimal places |

### 9.3 Status Category Constraints

| Constraint | Value |
|------------|-------|
| Number of categories | 3 (fixed) |
| Custom categories | Not supported |
| Category names | To Do, In Progress, Done (fixed) |

---

## 10. Domain Model Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        JIRA DOMAIN MODEL                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                         PROJECT                                  │   │
│  │  - key: String                                                   │   │
│  │  - name: String                                                  │   │
│  │  - issueTypes: IssueType[]                                      │   │
│  │  - workflow: Workflow                                           │   │
│  └─────────────────────┬───────────────────────────────────────────┘   │
│                        │ contains                                       │
│                        ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                         ISSUE                                    │   │
│  │  - key: String (PROJ-123)                                       │   │
│  │  - id: Long                                                      │   │
│  │  - summary: String [required]                                   │   │
│  │  - description: RichText                                        │   │
│  │  - issueType: IssueType [required]                              │   │
│  │  - status: Status [required]                                    │   │
│  │  - resolution: Resolution                                       │   │
│  │  - priority: Priority                                           │   │
│  │  - assignee: User                                               │   │
│  │  - reporter: User                                               │   │
│  │  - created: DateTime                                            │   │
│  │  - updated: DateTime                                            │   │
│  │  - dueDate: Date                                                │   │
│  │  - labels: String[]                                             │   │
│  │  - components: Component[]                                      │   │
│  │  - customFields: Map<String, Any>                               │   │
│  └────┬────────────┬────────────┬────────────┬─────────────────────┘   │
│       │            │            │            │                          │
│       │ parent     │ links      │ comments   │ attachments              │
│       ▼            ▼            ▼            ▼                          │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌───────────┐                     │
│  │  ISSUE  │ │  LINK   │ │ COMMENT │ │ATTACHMENT │                     │
│  │ (parent)│ │  TYPE   │ │         │ │           │                     │
│  └─────────┘ └─────────┘ └─────────┘ └───────────┘                     │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                       WORKFLOW                                   │   │
│  │  ┌─────────┐      ┌─────────────┐      ┌─────────┐              │   │
│  │  │ STATUS  │─────►│ TRANSITION  │─────►│ STATUS  │              │   │
│  │  │(To Do)  │      │             │      │(In Prog)│              │   │
│  │  └─────────┘      └─────────────┘      └─────────┘              │   │
│  │       │                 │                   │                    │   │
│  │       ▼                 ▼                   ▼                    │   │
│  │  ┌─────────┐      ┌─────────────┐      ┌─────────┐              │   │
│  │  │CATEGORY │      │  TRIGGERS   │      │CATEGORY │              │   │
│  │  │(grey)   │      │  CONDITIONS │      │(blue)   │              │   │
│  │  └─────────┘      │  VALIDATORS │      └─────────┘              │   │
│  │                   │  POST FUNCS │                               │   │
│  │                   └─────────────┘                               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ISSUE TYPE HIERARCHY:                                                  │
│  ┌──────────────┐                                                       │
│  │  Initiative  │ Level 2+ (Premium)                                    │
│  └──────┬───────┘                                                       │
│         ▼                                                               │
│  ┌──────────────┐                                                       │
│  │     Epic     │ Level 1                                               │
│  └──────┬───────┘                                                       │
│         ▼                                                               │
│  ┌──────┴──────┬──────────┐                                            │
│  │             │          │                                             │
│  ▼             ▼          ▼                                             │
│ [Story]     [Task]      [Bug]  Level 0                                  │
│  │             │          │                                             │
│  ▼             ▼          ▼                                             │
│ [Sub-task] [Sub-task] [Sub-task] Level -1                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 11. Key Insights for Ontology Design

### 11.1 Core Concepts to Model

1. **Work Item** - Central entity with flexible type system
2. **Hierarchy** - Parent-child relationships with level constraints
3. **Workflow** - State machine with transitions and categories
4. **Links** - Directed relationships between work items
5. **Fields** - Extensible field system (system + custom)
6. **Resolution** - Orthogonal to status, determines open/closed

### 11.2 Design Patterns Observed

| Pattern | Description | Jerry Applicability |
|---------|-------------|---------------------|
| **Type Hierarchy** | Issue types form extensible hierarchy | Core concept |
| **State Machine** | Workflows define valid state transitions | Essential |
| **Category Grouping** | Statuses belong to fixed categories | Useful simplification |
| **Directed Links** | Relationships have direction semantics | Important for dependencies |
| **Resolution Orthogonality** | Resolution separate from status | Clean separation of concerns |
| **Flexible Fields** | System + custom field extensibility | Consider for Jerry |

### 11.3 Constraints to Preserve

1. **Three status categories only** - Simple, effective model
2. **Sub-tasks are terminal** - Clear hierarchy boundary
3. **Resolution determines closed state** - Not status
4. **Parent-child limit (500)** - Practical constraint
5. **Custom field limits** - 55 options, 255 char text

### 11.4 Simplifications for Jerry

| JIRA Feature | Jerry Recommendation | Rationale |
|--------------|---------------------|-----------|
| Multiple products | Single model | Jerry is single-purpose |
| Custom issue types | Fixed types | Simplicity for AI agents |
| Complex workflows | Simple state machine | Reduce cognitive load |
| Custom fields | Structured extension point | Allow but don't require |
| Premium hierarchy | Standard 3 levels | Sufficient for most cases |

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Analysis ID** | EN-003-JIRA-MODEL |
| **Version** | 1.0 |
| **Created** | 2026-01-13 |
| **Source Document** | EN-003-JIRA-RAW.md |
| **Tables** | 35 |
| **Diagrams** | 5 |
| **Completeness** | All 6 analysis tasks completed |
