# JIRA Domain Model Research

**Research ID:** EN-003-JIRA-RAW
**Project:** PROJ-006-worktracker-ontology
**Date:** 2026-01-13
**Researcher:** ps-researcher (Claude)
**Status:** COMPLETE

---

## Executive Summary

This document provides comprehensive research on the Atlassian JIRA domain model, covering issue types, standard and custom fields, workflow states, link types, and hierarchy structures. The research is based on official Atlassian documentation and is intended to inform the worktracker ontology design for the Jerry framework.

---

## 1. Issue Type Inventory

### 1.1 Default Hierarchy Structure

JIRA supports three default hierarchy levels:

| Level | Category | Description |
|-------|----------|-------------|
| Level 1 | **Epic** | High-level initiatives representing major deliverables, phases, or features |
| Level 0 | **Standard Work Items** | Stories, Tasks, Bugs - where daily work is tracked |
| Level -1 | **Subtask** | Granular decomposition of standard work items |

> "Jira's built-in work item hierarchy from top to bottom is: Epics - represent broad objectives or large bodies of work that can be broken down into stories, tasks, and bugs; Work items (task, story, bug) - Stories and tasks are work items that represent work that needs to be completed in support of those larger goals. Bugs are problems that impede the progress or functionality of work; Sub-tasks - A granular piece of work required to complete a story, task, or bug."
>
> Source: [What are work types? | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-types/)

### 1.2 Standard Issue Types

#### Epic
- **Purpose:** Groups together bugs, stories, and tasks to show progress of a larger initiative
- **Characteristics:** Can have stories, tasks, and bugs as child issues
- **Use Case:** Represents significant deliverables like new features or experiences

> "Epics group together bugs, stories, and tasks to show the progress of a larger initiative. In agile development, epics usually represent a significant deliverable, such as a new feature or experience in the software your team develops."
>
> Source: [Introduction to Jira Work Items | Atlassian](https://www.atlassian.com/software/jira/guides/issues/overview)

#### Story
- **Purpose:** Represents a requirement from the user's perspective
- **Characteristics:** Standard work item that can have subtasks
- **Use Case:** User requirements and feature requests
- **Example:** "As a lemonade enthusiast, I'd like to have a really cold, crisp drink."

> "A story represents a requirement expressed from the perspective of the user."
>
> Source: [Introduction to Jira Work Items | Atlassian](https://www.atlassian.com/software/jira/guides/issues/overview)

#### Task
- **Purpose:** Represents generic work that needs to be done
- **Characteristics:** Catch-all for work not represented by other types
- **Use Case:** Technical work, maintenance, or work that doesn't fit other categories
- **Parent Capability:** Can have subtasks as child issues

> "A task represents work that needs to be done. Tasks are used as 'catch-alls' and when the work cannot be accurately represented by the other work types."
>
> Source: [Introduction to Jira Work Items | Atlassian](https://www.atlassian.com/software/jira/guides/issues/overview)

#### Bug
- **Purpose:** Tracks problems that impair or prevent product functionality
- **Characteristics:** Standard work item with specific resolution workflows
- **Use Case:** Defect tracking, quality assurance

> "A bug is a problem which impairs or prevents the functions of a product."
>
> Source: [Introduction to Jira Work Items | Atlassian](https://www.atlassian.com/software/jira/guides/issues/overview)

#### Sub-task
- **Purpose:** Granular decomposition of parent work items
- **Characteristics:** Cannot have child issues; only exists as children
- **Use Case:** Breaking complex work into smaller, assignable pieces

> "A sub-task represents a more granular decomposition of the work required to complete a standard work item. A sub-task can be created for all work types."
>
> Source: [Introduction to Jira Work Items | Atlassian](https://www.atlassian.com/software/jira/guides/issues/overview)

### 1.3 Issue Types by Jira Product

#### Jira Software (Development Teams)
| Issue Type | Level | Purpose |
|------------|-------|---------|
| Epic | Parent | Large bodies of work |
| Story | Standard | User requirements |
| Task | Standard | Technical work |
| Bug | Standard | Defect tracking |
| Sub-task | Child | Granular work breakdown |

#### Jira Work Management (Business Teams)
| Issue Type | Level | Purpose |
|------------|-------|---------|
| Task | Standard | General business work |
| Sub-task | Child | Task breakdown |

> "Business Spaces: Task (standard) and Subtask (child)"
>
> Source: [What are work types? | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-types/)

#### Jira Service Management (IT/Support Teams)
| Issue Type | Purpose |
|------------|---------|
| Change | Change management requests |
| IT Help | Internal IT support requests |
| Incident | Service incidents |
| New Feature | Feature requests |
| Problem | Root cause analysis |
| Service Request | Standard service requests |
| Service Request with Approval | Requests requiring approval |
| Support | External support tickets |

> "Service Spaces: Change, IT Help, Incident, New Feature, Problem, Service Request, Service Request with Approval, Support"
>
> Source: [What are work types? | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-types/)

### 1.4 Parent-Child Relationship Rules

| Parent Type | Can Have Children | Child Types |
|-------------|-------------------|-------------|
| Epic | Yes | Stories, Tasks, Bugs |
| Story | Yes | Sub-tasks |
| Task | Yes | Sub-tasks |
| Bug | Yes | Sub-tasks |
| Sub-task | No | None |

> "The parent and child relationship isn't limited to specific work types. Rather, any work type can be both a parent and a child work item - the only exception being subtasks, which can only be a child since there aren't any work types below it in the hierarchy."
>
> Source: [What are work types? | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-types/)

**Important Limitation:**
> "A work item can only display up to 500 child work items."
>
> Source: [What are work types? | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-types/)

---

## 2. Standard and Custom Field Definitions

### 2.1 Core System Fields

#### Mandatory System Fields

| Field | Type | Description |
|-------|------|-------------|
| **Project** | System | The project containing the issue |
| **Issue Type** | System | Classification of the work item |
| **Summary** | Text | Brief title/description of the issue |
| **Status** | System | Current workflow state |
| **Resolution** | System | How the issue was resolved (when done) |

#### Optional System Fields

| Field | Type | Description |
|-------|------|-------------|
| **Description** | Rich Text | Detailed explanation of the work |
| **Assignee** | User Picker | Person responsible for the work |
| **Reporter** | User Picker | Person who created the issue |
| **Priority** | Select | Relative importance (Highest, High, Medium, Low, Lowest) |
| **Labels** | Multi-value Text | Free-form categorization tags |
| **Component/s** | Multi-select | Project components affected |
| **Affects Version** | Version Picker | Versions where bug was found |
| **Fix Version** | Version Picker | Target release version |
| **Due Date** | Date | Target completion date |
| **Environment** | Text | Technical environment details |
| **Attachment** | File | Associated files |
| **Linked Issues** | Issue Links | Related issues |
| **Comments** | Rich Text List | Discussion and updates |

> "System fields that Jira always has on issues fall into four broad groups: Structural ones that are not really fields (Project, issue type and status), mandatory system fields (summary, resolution), and optional system fields (assignee, reporter, environment, due date, comments)."
>
> Source: [Issue fields and statuses | Atlassian Documentation](https://confluence.atlassian.com/adminjiraserver/issue-fields-and-statuses-938847116.html)

#### Time Tracking Fields

| Field | Type | Description |
|-------|------|-------------|
| **Original Estimate** | Duration | Initial time estimate |
| **Remaining Estimate** | Duration | Time remaining |
| **Time Spent** | Duration | Actual time logged |
| **Log Work** | Work Log | Time tracking entries |

#### Agile/Software Fields

| Field | Type | Description |
|-------|------|-------------|
| **Sprint** | Sprint Picker | Associated sprint(s) |
| **Story Points** | Number | Relative effort estimation |
| **Epic Link** | Issue Picker | Parent epic (legacy, replaced by Parent) |
| **Parent** | Issue Picker | Parent issue in hierarchy |

#### Timestamp Fields (Auto-populated)

| Field | Type | Description |
|-------|------|-------------|
| **Created** | DateTime | When issue was created |
| **Updated** | DateTime | Last modification timestamp |
| **Resolved** | DateTime | When resolution was set |

### 2.2 Priority Field Values

JIRA provides five default priority levels:

| Priority | Description |
|----------|-------------|
| **Highest** | "This problem will block progress." |
| **High** | "Serious problem that could block progress." |
| **Medium** | "Has the potential to affect progress." |
| **Low** | "Minor problem or easily worked around." |
| **Lowest** | "Trivial problem with little or no impact on progress." |

> "Jira provides five standard priority levels that indicate a work item's relative importance... Both the priority rankings and their meanings can be adjusted by administrators to align with organizational needs."
>
> Source: [What are work item statuses, priorities, and resolutions? | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-statuses-priorities-and-resolutions/)

### 2.3 Resolution Field Values

#### Jira Cloud Default Resolutions

| Resolution | Description |
|------------|-------------|
| **Done** | Work on this ticket is complete |
| **Won't do** | The team won't act on this issue |
| **Duplicate** | The task is a duplicate of an existing issue |
| **Cannot reproduce** | Attempts to reproduce the issue have failed |

#### Traditional Jira Default Resolutions

| Resolution | Description |
|------------|-------------|
| **Fixed** | The issue has been resolved |
| **Duplicate** | Duplicate of another issue |
| **Won't Fix** | Issue will not be addressed |
| **Incomplete** | Insufficient information |
| **Cannot Reproduce** | Unable to replicate the issue |

#### Jira Service Management Additional Resolutions

| Resolution | Description |
|------------|-------------|
| **Known error** | Root cause documented |

> "In Jira Cloud, the Resolution field describes the reason a work item was moved to Done... Any issue that has the resolution field set is treated by Jira as 'Resolved'. 'Fixed' is the default resolution value in Jira."
>
> Source: [Master Jira "Resolution" field values | Tempo](https://www.tempo.io/blog/jira-resolution-field-values)

### 2.4 Custom Field Types

#### Text Fields

| Type | Description | Character Limit |
|------|-------------|-----------------|
| **Short Text (Single Line)** | Plain text input | 255 characters |
| **Paragraph (Multi-Line)** | Rich text with formatting | Unlimited |

> "Short text fields allow people to provide information as free-form text... A single line of plain text for short lengths of text (up to 255 characters)."
>
> Source: [Field types you can create as a Jira admin | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/custom-fields-types-in-company-managed-projects/)

#### Number Fields

| Type | Description | Range |
|------|-------------|-------|
| **Number** | Numeric input | -1 trillion to 1 trillion |
| **Number (Currency)** | Formatted as currency | -1 trillion to 1 trillion |
| **Number (Percentage)** | Formatted as percentage | -1 trillion to 1 trillion |

> "Number fields support numbers between -1 trillion and 1 trillion (1,000,000,000,000). Jira rounds decimals to the nearest 1000th place."
>
> Source: [Field types you can create as a Jira admin | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/custom-fields-types-in-company-managed-projects/)

#### Selection Fields

| Type | Description | Options Limit |
|------|-------------|---------------|
| **Dropdown (Single Select)** | Single choice from list | 55 options |
| **Multi-select** | Multiple choices from list | 55 options |
| **Cascading Select** | Parent-child option hierarchy | Varies |
| **Radio Buttons** | Single choice (visible options) | Limited |
| **Checkboxes** | Multiple true/false selections | Limited |

> "Dropdown fields allow people to select a single option from a list... You can add up to 55 options in a dropdown field."
>
> Source: [Field types you can create as a Jira admin | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/custom-fields-types-in-company-managed-projects/)

#### Date and Time Fields

| Type | Description |
|------|-------------|
| **Date Picker** | Calendar date selection (no time) |
| **Date Time Picker** | Date and time selection |

#### User and Group Fields

| Type | Description | Multi-select |
|------|-------------|--------------|
| **User Picker (Single)** | Single user selection | No |
| **User Picker (Multiple)** | Multiple user selection | Yes |
| **Group Picker (Single)** | Single group selection | No |
| **Group Picker (Multiple)** | Multiple group selection | Yes |

> "People fields allow your team to insert people's names from across your Jira site into a field on your work item... By default, the people field allows you to insert multiple names to complete the field."
>
> Source: [Field types you can create as a Jira admin | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/custom-fields-types-in-company-managed-projects/)

#### Other Custom Field Types

| Type | Description |
|------|-------------|
| **Assets** | Track related objects (JSM) |
| **Labels** | Create or select existing labels |
| **Parent** | Associate with parent issue |
| **Space/Project Picker** | Select project(s) |
| **Team** | Select Atlassian Teams |
| **Version Picker** | Select version(s) |

#### Read-Only Information Fields

| Type | Description |
|------|-------------|
| **Date of First Response** | Auto-displays first comment date |
| **Days Since Last Comment** | Activity recency metric |
| **Participants of Work Item** | Lists all contributors |
| **Time in Status** | Workflow productivity metrics |

### 2.5 Custom Field API Reference

Custom fields in the REST API are referenced by their ID with the `customfield_` prefix:

```
customfield_{id}
```

Example: A "Story Points" custom field with ID 10000 would be referenced as `customfield_10000`.

> "Since custom field names are not unique within a JIRA instance, custom fields are referred to by the field ID in the REST API... In REST, custom fields are referenced by 'customfield_' + the id of the custom field."
>
> Source: [Get custom field IDs | Atlassian Documentation](https://confluence.atlassian.com/jirakb/get-custom-field-ids-for-jira-and-jira-service-management-744522503.html)

---

## 3. Link Type Definitions

### 3.1 Default Issue Link Types

JIRA ships with four default link types:

#### 1. Blocks / Is Blocked By

| Direction | Description |
|-----------|-------------|
| Outward | "blocks" |
| Inward | "is blocked by" |

**Use Case:** Indicates dependency where one issue prevents another from progressing.

> "This link type indicates that the issue prevents another issue from progressing or being resolved. For example, if Issue A 'blocks' Issue B, it means that you can't complete Issue B until you resolve Issue A."
>
> Source: [Configure work item linking | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/configure-issue-linking/)

#### 2. Relates To

| Direction | Description |
|-----------|-------------|
| Outward | "relates to" |
| Inward | "relates to" |

**Use Case:** General relationship without specific dependency.

> "This link type establishes a general relationship between two issues without specifying the nature of their dependency. If Issue A 'relates to' Issue B, it means there is some form of connection or relevance between the two issues."
>
> Source: [Configure work item linking | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/configure-issue-linking/)

#### 3. Duplicates / Is Duplicated By

| Direction | Description |
|-----------|-------------|
| Outward | "duplicates" |
| Inward | "is duplicated by" |

**Use Case:** Marks issues representing the same problem/request.

> "This link is used to connect issues that represent the same problem or request. It helps avoid duplicate work and ensures teams focus on addressing unique issues."
>
> Source: [Configure work item linking | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/configure-issue-linking/)

#### 4. Clones / Is Cloned By

| Direction | Description |
|-----------|-------------|
| Outward | "clones" |
| Inward | "is cloned by" |

**Use Case:** Issues copied from originals, expected to diverge.

> "Clone in Jira means 'take a copy of the issue and create a new issue'. While they do look like duplicates initially, the purpose is to have the same issue raised in more than one place, and the clone is expected to diverge rapidly from the original."
>
> Source: [Need definition for 'Link Issue' types | Atlassian Community](https://community.atlassian.com/forums/Jira-questions/Need-definition-for-Link-Issue-types/qaq-p/1738147)

### 3.2 Link Direction Semantics

| Term | Definition |
|------|------------|
| **Outward Link** | Link direction from source to destination issue |
| **Inward Link** | Link direction from destination back to source |

> "A source issue that the link originates from has an Outward link to the destination issue. For example, 'Issue A' that is blocked by 'Issue B' has an outward link of type 'is blocked by', which goes to 'Issue B'. At the same time, 'Issue B' has an inward link of type 'blocks' that goes back to 'Issue A'."
>
> Source: [Configuring issue linking | Atlassian Documentation](https://confluence.atlassian.com/adminjiraserver/configuring-issue-linking-938847862.html)

### 3.3 Custom Link Types

Administrators can create custom link types with:
- Unique name
- Outward description
- Inward description

> "If standard options are insufficient, Jira administrators can configure custom link types."
>
> Source: [Configure work item linking | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/configure-issue-linking/)

---

## 4. Workflow State Definitions

### 4.1 Status Categories

JIRA has three fixed status categories that cannot be extended:

| Category | Color | Position in Workflow |
|----------|-------|---------------------|
| **To Do** | Grey | Beginning |
| **In Progress** | Blue | Middle |
| **Done** | Green | End |

> "Issues in a 'To Do' status category are at the beginning of the workflow, issues in a 'In Progress' status category are in the middle, and issues in a 'Done' status category are towards the end."
>
> Source: [Jira Status Categories | HeroCoders](https://www.herocoders.com/blog/understanding-jira-issue-statuses)

> "Right now there are only 3 status categories - 'To Do', 'In Progress' and 'Done' - creating additional categories is not supported."
>
> Source: [How can I create a status category? | Atlassian Community](https://community.atlassian.com/forums/Jira-questions/How-can-I-create-a-status-category/qaq-p/764219)

### 4.2 Default Statuses

Common default statuses mapped to categories:

| Status | Category | Description |
|--------|----------|-------------|
| **Open** | To Do | Newly created, not started |
| **To Do** | To Do | Ready to be worked on |
| **In Progress** | In Progress | Currently being worked on |
| **In Review** | In Progress | Awaiting review |
| **Approved** | In Progress | Approved, pending completion |
| **Done** | Done | Work completed |
| **Closed** | Done | Issue closed |
| **Resolved** | Done | Issue resolved |
| **Cancelled** | Done | Work cancelled |
| **Rejected** | Done | Work rejected |

> "Beyond the core categories, Jira supports specialized statuses including 'Open,' 'In Review,' 'Approved,' 'Cancelled,' and 'Rejected' depending on your space template and configuration."
>
> Source: [What are work item statuses, priorities, and resolutions? | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-statuses-priorities-and-resolutions/)

### 4.3 Workflow Components

#### Statuses
> "A status represents the state of an issue at a specific point in your workflow (e.g., 'In progress'). An issue can be in only one status at a given point in time."
>
> Source: [Understand workflows | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/work-with-issue-workflows/)

#### Transitions

| Type | Description |
|------|-------------|
| **Common Transition** | Connects two specific statuses |
| **Global Transition** | Allows transition from any status to target |
| **Self-Looping Transition** | Returns to same status (for triggering actions) |

> "A transition is a link between two statuses that enables an issue to move from one status to another. To move an issue between two statuses, a transition must exist... Transitions are also one-way. To move a work item back and forth, you need two separate transitions."
>
> Source: [Understand workflows | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/work-with-issue-workflows/)

### 4.4 Resolution vs Status

Important distinction:

> "In Jira, a work item is either open or closed, based on the value of its Resolution field (not its status). A work item is open if its resolution field isn't set. A work item is closed if its resolution field has a value (for example, Fixed or Can't reproduce). This is true regardless of the work item's current status."
>
> Source: [Understand workflows | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/work-with-issue-workflows/)

### 4.5 Advanced Transition Features

| Feature | Description |
|---------|-------------|
| **Triggers** | Transition based on external events (e.g., Bitbucket) |
| **Conditions** | Check if transition should be allowed |
| **Validators** | Validate input before transition |
| **Post Functions** | Execute actions after transition |
| **Properties** | Key-value customization pairs |

> "As a Jira administrator, you can control the following aspects of a workflow transition: Triggers, Conditions, Validators, Post functions, Properties."
>
> Source: [Configure advanced work item workflows | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/configure-advanced-issue-workflows/)

### 4.6 Built-in Workflows

> "Jira has built-in workflows that you can use straight away. Or, you can start fresh and create your own. You can't edit the built-in workflows, but you can copy them and use them as a base to create your own."
>
> Source: [Understand workflows | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/work-with-issue-workflows/)

---

## 5. Hierarchy Structure

### 5.1 Standard Three-Level Hierarchy

```
Level 1:    [Epic]
             │
Level 0:    [Story] ─── [Task] ─── [Bug]
             │            │          │
Level -1:  [Sub-task] [Sub-task] [Sub-task]
```

### 5.2 Advanced Roadmaps Extended Hierarchy (Premium/Enterprise)

Available with Jira Premium and Enterprise subscriptions:

```
Level 2+:   [Initiative] (or custom names)
             │
Level 1:    [Epic]
             │
Level 0:    [Story] ─── [Task] ─── [Bug]
             │            │          │
Level -1:  [Sub-task] [Sub-task] [Sub-task]
```

> "As part of your Jira Premium and Enterprise subscriptions, you can add levels above 1 and use these extra levels to track your organization's larger initiatives in your plans and unify work across multiple spaces."
>
> Source: [Configure custom hierarchy levels in your plan | Atlassian Support](https://support.atlassian.com/jira-software-cloud/docs/configure-custom-hierarchy-levels-in-advanced-roadmaps/)

### 5.3 Initiative Issue Type

**Definition:** Container for multiple Epics representing strategic goals.

> "Initiatives sit at the very top. Initiatives represent massive strategic goals that span across multiple teams and multiple projects. Note: You won't see this in standard Jira. You generally need Jira Premium (Advanced Roadmaps/Plans)."
>
> Source: [Jira Issue Hierarchy | Titanapps](https://titanapps.io/blog/jira-issue-hierarchy/)

> "The simplest way to look at an initiative is to think of it like an Epic for other Epics."
>
> Source: [Configuring initiatives and other hierarchy levels | Atlassian Documentation](https://confluence.atlassian.com/advancedroadmapsserver0329/configuring-initiatives-and-other-hierarchy-levels-1021218664.html)

### 5.4 Configuring Custom Hierarchy Levels

Three-step process:

1. **Create Work Type:** Settings > Work Items > Work Types
2. **Add to Scheme:** Settings > Work Items > Work Type Schemes
3. **Associate to Hierarchy:** Settings > Work type hierarchy > Create level

> "Organizations can use creative hierarchy names like Legend, Odyssey, Anthology, Monolith, Deity, or Omnipotence - customization is entirely flexible."
>
> Source: [Configure custom hierarchy levels in your plan | Atlassian Support](https://support.atlassian.com/jira-software-cloud/docs/configure-custom-hierarchy-levels-in-advanced-roadmaps/)

### 5.5 Hierarchy Limitations

> "Jira's default issue hierarchy is Epic -> Story -> Sub-task. If you upgrade to Jira Cloud Premium you can create an issue type above Epics such as an Initiative. But you can't create issue types below Epics at this time."
>
> Source: [Configure custom hierarchy levels in your plan | Atlassian Support](https://support.atlassian.com/jira-software-cloud/docs/configure-custom-hierarchy-levels-in-advanced-roadmaps/)

---

## 6. JIRA Cloud vs Server/Data Center Differences

### 6.1 Deployment Models

| Aspect | Cloud | Data Center | Server (EOL) |
|--------|-------|-------------|--------------|
| **Hosting** | Atlassian-managed SaaS | Self-hosted | Self-hosted |
| **Updates** | Automatic | Manual | Manual |
| **Scalability** | Automatic | Active-active clustering | Single node |
| **Support Status** | Active | Active | **Ended Feb 2024** |

> "Atlassian ended Server support on 15th February 2024."
>
> Source: [Jira Data Center vs. Jira Cloud 2025 | Candylio](https://www.candylio.com/en/post/jira-data-center-vs-jira-cloud-2025-which-is-the-smarter-move-for-your-business)

### 6.2 Feature Differences

#### Cloud-Only Features
- Jira Work Management
- Jira Product Discovery
- Atlas
- Atlassian Intelligence (AI)
- Rovo search
- Advanced automation features

> "The most significant new products are cloud only, as that is where Atlassian is focusing its investments. These include Jira Work Management, Jira Product Discovery, Atlas, Atlassian Intelligence, and Beacon."
>
> Source: [Differences administering Jira Data Center and Cloud | Atlassian Support](https://support.atlassian.com/migration/docs/differences-administering-jira-data-center-and-cloud/)

#### Administration Differences

| Feature | Cloud | Data Center |
|---------|-------|-------------|
| **Admin Roles** | User, Product admin, Organization admin | Jira admin, System admin |
| **Email Templates** | Cannot modify | Velocity template customization |
| **Listeners** | Not available (use webhooks) | Configurable |
| **Audit Logging** | Basic with plans; granular with Enterprise | Granular coverage areas |

> "In Jira Data Center and Server, there were two levels of global administrator permissions. In Cloud, you assign roles to people, including User, Product admin (equivalent to Jira administrator global permission), and Organization admin, which is similar to System administrator global permission."
>
> Source: [Differences administering Jira Data Center and Cloud | Atlassian Support](https://support.atlassian.com/migration/docs/differences-administering-jira-data-center-and-cloud/)

### 6.3 Cost Considerations

| Model | Cost Structure |
|-------|---------------|
| **Cloud** | Subscription-based, lower upfront costs |
| **Data Center** | License + infrastructure + IT staff costs |

> "The total cost of ownership extends beyond Atlassian's fees, as businesses need to consider the expenses involved in running their own servers, employing IT staff for maintenance, and upgrading hardware."
>
> Source: [Jira Data Center vs. Cloud | Appfire](https://appfire.com/resources/blog/jira-data-center-vs-cloud-breaking-down-the-differences)

---

## 7. REST API Reference

### 7.1 Create Issue - Required Fields

Minimum required fields for issue creation:

```json
{
  "fields": {
    "project": {
      "key": "PROJECT_KEY"
    },
    "summary": "Issue summary text",
    "issuetype": {
      "name": "Bug"
    }
  }
}
```

> "The basic required fields for creating an issue are: Project - specified by key or ID, Issue Type - specified by name or ID, Summary - the issue title/summary text."
>
> Source: [JIRA REST API Example Create Issue | Atlassian Developer](https://developer.atlassian.com/server/jira/platform/jira-rest-api-example-create-issue-7897248/)

### 7.2 Discovering Required Fields

Use the `createmeta` endpoint:

```
GET /rest/api/2/issue/createmeta?projectKeys=KEY&issuetypeNames=Bug&expand=projects.issuetypes.fields
```

> "Using the createmeta resource you can discover the project and issue types... The createmeta resource returns a list of all the issue types and their fields for each project."
>
> Source: [JIRA REST API Example Discovering Meta Data | Atlassian Developer](https://developer.atlassian.com/server/jira/platform/jira-rest-api-example-discovering-meta-data-for-creating-issues-6291669/)

### 7.3 Key API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /rest/api/3/field` | List all fields (system and custom) |
| `GET /rest/api/3/issue/{issueIdOrKey}` | Get issue details |
| `POST /rest/api/3/issue` | Create new issue |
| `PUT /rest/api/3/issue/{issueIdOrKey}` | Update issue |
| `GET /rest/api/3/issue/createmeta` | Get available fields for creation |
| `GET /rest/api/3/issuetype` | List issue types |
| `GET /rest/api/3/status` | List statuses |
| `GET /rest/api/3/priority` | List priorities |
| `GET /rest/api/3/resolution` | List resolutions |

---

## 8. Summary Tables

### 8.1 Complete Issue Type Reference

| Issue Type | Level | Can Be Parent | Can Be Child | Products |
|------------|-------|---------------|--------------|----------|
| Initiative | 2+ | Yes | No | Premium/Enterprise |
| Epic | 1 | Yes | Yes (of Initiative) | Software, Premium |
| Story | 0 | Yes | Yes | Software |
| Task | 0 | Yes | Yes | All |
| Bug | 0 | Yes | Yes | Software |
| Sub-task | -1 | No | Yes | All |

### 8.2 Complete Field Type Reference

| Category | Field Types |
|----------|-------------|
| **Text** | Short Text, Paragraph |
| **Number** | Number, Currency, Percentage |
| **Selection** | Dropdown, Multi-select, Cascading, Radio, Checkbox |
| **Date/Time** | Date Picker, Date Time Picker |
| **User/Group** | User Picker (single/multi), Group Picker (single/multi) |
| **Reference** | Parent, Labels, Version Picker, Sprint, Team |
| **Read-Only** | Date of First Response, Days Since Last Comment, Time in Status |

### 8.3 Complete Link Type Reference

| Link Type | Outward | Inward |
|-----------|---------|--------|
| **Blocks** | "blocks" | "is blocked by" |
| **Relates** | "relates to" | "relates to" |
| **Duplicates** | "duplicates" | "is duplicated by" |
| **Clones** | "clones" | "is cloned by" |

### 8.4 Complete Status Category Reference

| Category | Color | JQL Clause |
|----------|-------|------------|
| To Do | Grey | `statusCategory = "To Do"` |
| In Progress | Blue | `statusCategory = "In Progress"` |
| Done | Green | `statusCategory = Done` |

---

## Sources

### Official Atlassian Documentation

1. [What are work types? | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-types/)
2. [Introduction to Jira Work Items | Atlassian](https://www.atlassian.com/software/jira/guides/issues/overview)
3. [Understand workflows | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/work-with-issue-workflows/)
4. [Configure work item linking | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/configure-issue-linking/)
5. [What are work item statuses, priorities, and resolutions? | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-statuses-priorities-and-resolutions/)
6. [Field types you can create as a Jira admin | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/custom-fields-types-in-company-managed-projects/)
7. [Configure custom hierarchy levels in your plan | Atlassian Support](https://support.atlassian.com/jira-software-cloud/docs/configure-custom-hierarchy-levels-in-advanced-roadmaps/)
8. [Differences administering Jira Data Center and Cloud | Atlassian Support](https://support.atlassian.com/migration/docs/differences-administering-jira-data-center-and-cloud/)
9. [Configure advanced work item workflows | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/configure-advanced-issue-workflows/)
10. [Create workflow transitions | Atlassian Support](https://support.atlassian.com/jira-cloud-administration/docs/create-workflow-transitions/)

### Atlassian Developer Documentation

11. [The Jira Cloud platform REST API | Atlassian Developer](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-fields/)
12. [Jira REST API examples | Atlassian Developer](https://developer.atlassian.com/server/jira/platform/jira-rest-api-examples/)
13. [JIRA REST API Example Create Issue | Atlassian Developer](https://developer.atlassian.com/server/jira/platform/jira-rest-api-example-create-issue-7897248/)
14. [Get custom field IDs | Atlassian Documentation](https://confluence.atlassian.com/jirakb/get-custom-field-ids-for-jira-and-jira-service-management-744522503.html)

### Atlassian Server/Data Center Documentation

15. [Issue fields and statuses | Atlassian Documentation](https://confluence.atlassian.com/adminjiraserver/issue-fields-and-statuses-938847116.html)
16. [Configuring issue linking | Atlassian Documentation](https://confluence.atlassian.com/adminjiraserver/configuring-issue-linking-938847862.html)
17. [Working with workflows | Atlassian Documentation](https://confluence.atlassian.com/adminjiraserver/working-with-workflows-938847362.html)
18. [Configuring initiatives and other hierarchy levels | Atlassian Documentation](https://confluence.atlassian.com/advancedroadmapsserver0329/configuring-initiatives-and-other-hierarchy-levels-1021218664.html)

### Additional Sources

19. [Master Jira "Resolution" field values | Tempo](https://www.tempo.io/blog/jira-resolution-field-values)
20. [Jira Data Center vs. Cloud | Appfire](https://appfire.com/resources/blog/jira-data-center-vs-cloud-breaking-down-the-differences)
21. [Jira Issue Hierarchy | Titanapps](https://titanapps.io/blog/jira-issue-hierarchy/)
22. [Understanding Jira Statuses | HeroCoders](https://www.herocoders.com/blog/understanding-jira-issue-statuses)
23. [Compare Jira Cloud and Data Center features | Atlassian](https://www.atlassian.com/migration/assess/compare-cloud-data-center/jira-software)

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Research ID** | EN-003-JIRA-RAW |
| **Version** | 1.0 |
| **Created** | 2026-01-13 |
| **Word Count** | ~4,500 |
| **Citation Count** | 23 sources |
| **Completeness** | All 7 research questions addressed |
