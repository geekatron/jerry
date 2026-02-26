# Cross-Domain Synthesis Report

> **Document ID:** EN-004-CROSS-DOMAIN-SYNTHESIS
> **Date:** 2026-01-13
> **Analyst:** ps-synthesizer (Claude Opus 4.5)
> **Project:** PROJ-006-worktracker-ontology
> **Inputs:**
>   - `analysis/ADO-SCRUM-MODEL.md`
>   - `analysis/SAFE-MODEL.md`
>   - `analysis/JIRA-MODEL.md`
> **Status:** COMPLETE

---

## 1. Executive Summary

This report synthesizes the domain models from Azure DevOps Scrum, SAFe (Scaled Agile Framework), and JIRA to identify common patterns, propose canonical entity names, and design a unified ontology for the Jerry worktracker skill.

### Key Findings

1. **Universal Core Entities:** All three systems share Epic, Story/PBI, Task, and Bug equivalents
2. **Hierarchy Depth Varies:** SAFe has 5 levels (Epic-Capability-Feature-Story-Task), ADO has 4 (Epic-Feature-PBI-Task), JIRA has 3-4 (Initiative-Epic-Story-Subtask)
3. **State Categories Converge:** All systems map to three fundamental categories: Not Started, In Progress, Done
4. **Relationship Patterns Align:** Parent-child hierarchy, blocking dependencies, and general associations are universal
5. **Property Core is Stable:** ID, title, description, status, priority, and assignee are universal

### System-Specific Divergences

| System | Unique Concept | Impact |
|--------|---------------|--------|
| ADO Scrum | State Reason field | Captures why transitions occurred |
| SAFe | WSJF prioritization | Economic prioritization model |
| SAFe | Capability level | Extra hierarchy layer for large solutions |
| SAFe | Business/Enabler classification | Work type categorization |
| JIRA | Resolution orthogonal to Status | Separate concepts for completion reason |
| JIRA | Flexible parent-child | Any type can parent any type (except subtask) |

---

## 2. Entity Alignment Matrix

### 2.1 Full Entity Mapping

| Canonical Entity | ADO Scrum | SAFe | JIRA | Rationale |
|-----------------|-----------|------|------|-----------|
| **Epic** | Epic | Epic (Portfolio) | Epic | Universal term, all systems use "Epic" for strategic initiatives |
| **Capability** | - | Capability (Solution) | - | SAFe-only; maps to Epic or Feature in other systems |
| **Feature** | Feature | Feature (Program) | - | ADO/SAFe concept; JIRA uses Epic for this level |
| **Story** | Product Backlog Item (PBI) | Story | Story | "Story" chosen as industry standard; ADO's PBI is equivalent |
| **Task** | Task | Task | Task, Sub-task | Universal atomic work unit |
| **Bug** | Bug | Defect* | Bug | "Bug" more common; SAFe often uses "Defect" |
| **Impediment** | Impediment | Blocker* | - | ADO explicit entity; others use blocking links |
| **Spike** | - | Enabler Story (Exploration) | Task (labeled) | Research/discovery work; SAFe has formal type |
| **Initiative** | - | Strategic Theme* | Initiative | JIRA Premium feature; SAFe uses Strategic Themes |

**Citations:**
- ADO-SCRUM-MODEL.md Section 1.1 (Core Entities)
- SAFE-MODEL.md Section 2 (Entity Catalog by Level)
- JIRA-MODEL.md Section 1.1 (Issue Type Hierarchy)

### 2.2 Canonical Name Rationale

| Canonical | Decision Rationale |
|-----------|-------------------|
| **Epic** | Industry standard term used by all three systems. No translation needed. |
| **Feature** | Retained as distinct level; JIRA users can map Epic-to-Epic or Epic-to-Feature based on org size. |
| **Story** | Preferred over "PBI" because: (1) more intuitive, (2) used by 2/3 systems, (3) industry standard from Scrum. |
| **Task** | Universal agreement across all systems. No alternative needed. |
| **Bug** | Preferred over "Defect" because more common in 2/3 systems and developer vernacular. |
| **Spike** | Retained from SAFe for exploration work; can be modeled as Story with type=spike in other systems. |
| **Impediment** | Retained as first-class entity despite JIRA using links; explicit tracking is valuable. |

### 2.3 Gap Analysis: Entity Coverage

| Entity | ADO | SAFe | JIRA | Gap Impact |
|--------|:---:|:----:|:----:|------------|
| Epic | Yes | Yes | Yes | None - universal |
| Capability | No | Yes | No | SAFe-only; can flatten to Feature |
| Feature | Yes | Yes | No* | JIRA uses Epic for this; mapping required |
| Story | Yes (PBI) | Yes | Yes | Naming difference only |
| Task | Yes | Yes | Yes | None - universal |
| Bug | Yes | Yes | Yes | None - universal |
| Impediment | Yes | No* | No | Unique to ADO; valuable addition |
| Spike | No* | Yes | No* | Can be modeled as Story subtype |
| Initiative | No | No* | Yes | Premium feature; optional in ontology |

*No = Not explicit entity, but achievable through configuration/labeling

---

## 3. Property Alignment Matrix

### 3.1 Core Properties (Universal - Present in All Systems)

| Canonical Property | ADO Reference | SAFe Property | JIRA Field | Type | Required |
|-------------------|---------------|---------------|------------|------|----------|
| `id` | `System.Id` | `id` | `key` | identifier | Yes |
| `title` | `System.Title` | `name` | `summary` | string(255) | Yes |
| `description` | `System.Description` | `description` | `description` | richtext | No |
| `status` | `System.State` | `state` | `status` | enum | Yes |
| `priority` | `Microsoft.VSTS.Common.Priority` | `priority` | `priority` | enum | No |
| `assignee` | `System.AssignedTo` | `assignee` | `assignee` | user | No |
| `created_date` | `System.CreatedDate` | `created` | `created` | datetime | Yes (auto) |
| `updated_date` | `System.ChangedDate` | `updated` | `updated` | datetime | Yes (auto) |
| `created_by` | `System.CreatedBy` | `created_by` | `reporter` | user | Yes (auto) |

**Citations:**
- ADO-SCRUM-MODEL.md Section 2.1 (System Properties)
- SAFE-MODEL.md Section 3 (Entity Properties)
- JIRA-MODEL.md Section 2 (Standard Fields)

### 3.2 Extended Properties (Common - Present in 2+ Systems)

| Canonical Property | ADO Reference | SAFe Property | JIRA Field | Type | Notes |
|-------------------|---------------|---------------|------------|------|-------|
| `parent_id` | Parent Link | `parent_*_id` | `parent` | reference | Hierarchy link |
| `effort` | `Microsoft.VSTS.Scheduling.Effort` | `story_points` | `story_points` | number | ADO uses "Effort" |
| `tags` | `System.Tags` | labels | `labels` | string[] | Categorization |
| `due_date` | `Microsoft.VSTS.Scheduling.TargetDate` | `target_pi` | `dueDate` | date | Target completion |
| `remaining_work` | `Microsoft.VSTS.Scheduling.RemainingWork` | `remaining_hours` | `remaining_estimate` | duration | Task-level only |
| `acceptance_criteria` | `Microsoft.VSTS.Common.AcceptanceCriteria` | `acceptance_criteria` | custom | richtext | Story/Bug level |

### 3.3 System-Specific Properties

#### ADO Scrum Only

| Property | Reference | Type | Description |
|----------|-----------|------|-------------|
| `state_reason` | `System.Reason` | string | Why state changed |
| `area_path` | `System.AreaPath` | treepath | Organizational area |
| `iteration_path` | `System.IterationPath` | treepath | Sprint assignment |
| `revision` | `System.Rev` | integer | Version number |
| `value_area` | `Microsoft.VSTS.Common.ValueArea` | enum | Business vs. Architectural |
| `activity` | `Microsoft.VSTS.Common.Activity` | string | Task type (Dev, Test, etc.) |

**Citation:** ADO-SCRUM-MODEL.md Section 2.1-2.8

#### SAFe Only

| Property | Type | Description |
|----------|------|-------------|
| `type` | enum(Business, Enabler) | Classification for value type |
| `wsjf_score` | number | Weighted Shortest Job First priority |
| `cost_of_delay` | number | Economic impact of delay |
| `job_size` | number | Implementation size estimate |
| `business_outcome_hypothesis` | text | Expected outcomes for Epics |
| `benefit_hypothesis` | text | Expected benefits for Features |
| `mvp_definition` | text | Minimum Viable Product scope |
| `lean_business_case` | object | Economic justification (Epics) |
| `nfrs` | list | Non-functional requirements |
| `target_pi` | string | Target Program Increment |

**Citation:** SAFE-MODEL.md Sections 3.1-3.5

#### JIRA Only

| Property | Type | Description |
|----------|------|-------------|
| `resolution` | enum | How issue was resolved (Done, Won't Do, etc.) |
| `components` | reference[] | Project components affected |
| `affects_version` | version[] | Versions where bug found |
| `fix_version` | version[] | Target release version |
| `environment` | text | Technical environment details |
| `time_spent` | duration | Actual time logged |
| `original_estimate` | duration | Initial time estimate |
| `watchers` | user[] | Users following issue |

**Citation:** JIRA-MODEL.md Sections 2.1-2.7

### 3.4 Property Type Mapping

| Canonical Type | ADO Type | SAFe Type | JIRA Type |
|---------------|----------|-----------|-----------|
| `identifier` | Integer | string | string (KEY-123) |
| `string` | String | string | text (255 char) |
| `richtext` | HTML | text | rich text |
| `enum` | String | enum | enum |
| `number` | Double | number | number |
| `date` | DateTime | datetime | date/datetime |
| `user` | Identity | string | user picker |
| `reference` | Link | reference | issue picker |
| `duration` | Double (hours) | number (hours) | duration |

---

## 4. Relationship Types Analysis

### 4.1 Hierarchical Relationships (Containment)

| Canonical | ADO Link Type | SAFe Relationship | JIRA Link Type | Topology |
|-----------|--------------|-------------------|----------------|----------|
| `parent_of` | `System.LinkTypes.Hierarchy-Forward` | `contains` | `Parent` field | Tree |
| `child_of` | `System.LinkTypes.Hierarchy-Reverse` | `child_of` | (implicit) | Tree |

**Characteristics:**
- **Cardinality:** 1:N (one parent, many children)
- **Circular Reference:** Not allowed in any system
- **Cross-Project:** ADO supports via Area Paths; JIRA Premium supports cross-project parenting

**Citations:**
- ADO-SCRUM-MODEL.md Section 4.1 (Work Item Link Types)
- SAFE-MODEL.md Section 5.1 (Containment Relationships)
- JIRA-MODEL.md Section 1.4 (Parent-Child Relationship Rules)

### 4.2 Dependency Relationships (Blocking)

| Canonical | ADO Link Type | SAFe Relationship | JIRA Link Type | Directional |
|-----------|--------------|-------------------|----------------|-------------|
| `blocks` | `System.LinkTypes.Dependency-Forward` | `blocks` | `Blocks` (outward) | Yes |
| `blocked_by` | `System.LinkTypes.Dependency-Reverse` | `blocked_by` | `is blocked by` | Yes |
| `depends_on` | `System.LinkTypes.Dependency-Forward` | `depends_on` | `Blocks` | Yes |

**Characteristics:**
- **Cardinality:** N:M (many-to-many)
- **Circular Reference:** Not allowed (would create deadlock)
- **Cross-Level:** Allowed in all systems

**Semantic Distinction:**
- `blocks`: Source prevents target from proceeding
- `blocked_by`: Target cannot proceed until source resolves
- `depends_on`: Softer dependency; target can proceed but benefits from source completion

### 4.3 Association Relationships (Non-Blocking)

| Canonical | ADO Link Type | SAFe Relationship | JIRA Link Type | Directional |
|-----------|--------------|-------------------|----------------|-------------|
| `relates_to` | `System.LinkTypes.Related` | `related_to` | `Relates` | No (symmetric) |
| `duplicates` | `System.LinkTypes.Duplicate-Forward` | - | `Duplicates` | Yes |
| `duplicated_by` | `System.LinkTypes.Duplicate-Reverse` | - | `is duplicated by` | Yes |
| `clones` | - | - | `Clones` | Yes |
| `realizes` | - | `realizes` | - | Yes (SAFe only) |

**Characteristics:**
- **Cardinality:** N:M (many-to-many)
- **Circular Reference:** Allowed for `relates_to`
- **Purpose:** Informational linkage, no workflow impact

### 4.4 External Relationships (Artifacts)

| Canonical | ADO Link Type | SAFe | JIRA | Target Type |
|-----------|--------------|------|------|-------------|
| `links_to_commit` | Git Commit artifact | - | Development panel | VCS Commit |
| `links_to_branch` | Git Branch artifact | - | Development panel | VCS Branch |
| `links_to_pr` | Pull Request artifact | - | Development panel | Pull Request |
| `links_to_build` | Build artifact | - | CI/CD integration | Build/Pipeline |
| `links_to_wiki` | Wiki Page artifact | - | Confluence | Documentation |
| `links_to_url` | Hyperlink | - | Web Link | External URL |

### 4.5 Relationship Matrix Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CANONICAL RELATIONSHIP TYPES                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  HIERARCHICAL (Tree Topology - No Cycles)                                   │
│  ├── parent_of / child_of                                                   │
│  │   Epic ──► Feature ──► Story ──► Task                                   │
│  │                                                                          │
│  DEPENDENCY (Directed - No Cycles)                                          │
│  ├── blocks / blocked_by                                                    │
│  │   Task A ──[blocks]──► Task B                                           │
│  │                                                                          │
│  ASSOCIATION (Network - Cycles OK)                                          │
│  ├── relates_to (symmetric)                                                 │
│  ├── duplicates / duplicated_by                                             │
│  │                                                                          │
│  EXTERNAL (Artifact Links)                                                  │
│  ├── links_to_commit, links_to_pr, links_to_build, etc.                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. State Machine Comparison

### 5.1 State Mapping by Entity Type

#### Epic/Feature Level

| Canonical State | ADO Scrum | SAFe Portfolio Kanban | JIRA | Category |
|-----------------|-----------|----------------------|------|----------|
| `funnel` | - | FUNNEL | - | Proposed |
| `new` | New | REVIEWING | To Do | Proposed |
| `analyzing` | - | ANALYZING | - | Proposed |
| `ready` | - | READY | Ready | Proposed |
| `in_progress` | In Progress* | IMPLEMENTING_MVP | In Progress | InProgress |
| `implementing` | In Progress | IMPLEMENTING_PERSEVERE | In Progress | InProgress |
| `done` | Done | DONE | Done | Completed |
| `removed` | Removed | - | - | Removed |
| `rejected` | - | DONE (No-Go) | Rejected | Completed |

*ADO Scrum default Epic/Feature states: New, In Progress, Done, Removed

#### Story/PBI Level

| Canonical State | ADO Scrum (PBI) | SAFe Team Kanban | JIRA (Story) | Category |
|-----------------|-----------------|------------------|--------------|----------|
| `new` | New | BACKLOG | To Do | Proposed |
| `approved` | Approved | - | - | Proposed |
| `ready` | - | READY | Ready | Proposed |
| `committed` | Committed | - | - | InProgress |
| `in_progress` | - | IN_PROGRESS | In Progress | InProgress |
| `in_review` | - | REVIEW | In Review | InProgress |
| `done` | Done | DONE | Done | Completed |
| `accepted` | - | ACCEPTED | - | Completed |
| `removed` | Removed | CANCELLED | Cancelled | Removed |

#### Task Level

| Canonical State | ADO Scrum | SAFe | JIRA | Category |
|-----------------|-----------|------|------|----------|
| `todo` | To Do | NOT_STARTED | To Do | Proposed |
| `in_progress` | In Progress | IN_PROGRESS | In Progress | InProgress |
| `done` | Done | DONE | Done | Completed |
| `removed` | Removed | - | - | Removed |

#### Bug Level

| Canonical State | ADO Scrum | SAFe (Defect) | JIRA (Bug) | Category |
|-----------------|-----------|---------------|------------|----------|
| `new` | New | BACKLOG | Open | Proposed |
| `approved` | Approved | - | - | Proposed |
| `committed` | Committed | IN_PROGRESS | In Progress | InProgress |
| `in_review` | - | REVIEW | In Review | InProgress |
| `done` | Done | DONE | Resolved | Completed |
| `removed` | Removed | CANCELLED | Closed (Won't Fix) | Removed |

**Citations:**
- ADO-SCRUM-MODEL.md Section 5 (State Machines)
- SAFE-MODEL.md Section 6 (Kanban State Machines)
- JIRA-MODEL.md Section 6 (Workflow States)

### 5.2 State Category Alignment

All three systems converge on a fundamental three-category model:

| Canonical Category | ADO Category | SAFe | JIRA Category | Color |
|-------------------|--------------|------|---------------|-------|
| **Proposed** | Proposed | Funnel/Analyzing | To Do | Grey |
| **InProgress** | In Progress | Implementing | In Progress | Blue |
| **Completed** | Completed | Done | Done | Green |
| **Removed** | Removed | - | Done (resolution) | - |

**Key Insight:** JIRA's "Removed" state is achieved through Resolution field (Won't Do, Duplicate, etc.) rather than a separate category.

**Citations:**
- ADO-SCRUM-MODEL.md Section 6 (State Categories Mapping)
- JIRA-MODEL.md Section 6.1 (Status Categories)

### 5.3 Proposed Canonical State Machine

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        CANONICAL STATE MACHINE                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│                              [REMOVED]                                           │
│                                  ▲                                               │
│                                  │ (from any state)                              │
│                                  │                                               │
│  ┌─────────┐    refine    ┌─────────┐    start    ┌─────────────┐              │
│  │ BACKLOG │─────────────►│  READY  │────────────►│ IN_PROGRESS │              │
│  │         │              │         │             │             │              │
│  │(Proposed)              │(Proposed)             │(InProgress) │              │
│  └────┬────┘              └────┬────┘             └──────┬──────┘              │
│       │                        │                         │                      │
│       │                        │                         │ complete             │
│       └────────────────────────┴─────────────────────────▼                      │
│                                                    ┌─────────┐                  │
│                                                    │  DONE   │                  │
│                                                    │         │                  │
│                                                    │(Complete)│                  │
│                                                    └─────────┘                  │
│                                                                                  │
│  EXTENDED STATES (Optional):                                                     │
│                                                                                  │
│  ┌─────────────┐                                  ┌─────────────┐              │
│  │   BLOCKED   │ ◄──────── block ──────────────► │ IN_PROGRESS │              │
│  │ (InProgress)│ ────────► unblock ─────────────►│             │              │
│  └─────────────┘                                  └─────────────┘              │
│                                                                                  │
│  ┌─────────────┐                                  ┌─────────────┐              │
│  │  IN_REVIEW  │ ◄──────── submit ──────────────►│ IN_PROGRESS │              │
│  │ (InProgress)│ ────────► approve ─────────────►│    DONE     │              │
│  └─────────────┘ ────────► reject ──────────────►│ IN_PROGRESS │              │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 5.4 Canonical States Definition

| State | Category | Entry Criteria | Exit Criteria | Canonical Meaning |
|-------|----------|----------------|---------------|-------------------|
| `backlog` | Proposed | Created | Refined/Removed | Work captured but not ready |
| `ready` | Proposed | Acceptance criteria defined | Started/Removed | Ready to be worked on |
| `in_progress` | InProgress | Work started | Completed/Blocked/Review | Actively being worked on |
| `blocked` | InProgress | Blocker identified | Blocker resolved | Cannot proceed due to dependency |
| `in_review` | InProgress | Implementation complete | Approved/Rejected | Awaiting review or testing |
| `done` | Completed | Acceptance criteria met | - | Work successfully completed |
| `removed` | Removed | Cancelled/Obsolete | - | Work will not be completed |

### 5.5 Canonical Transitions

| From State | To State | Transition | Preconditions |
|------------|----------|------------|---------------|
| `backlog` | `ready` | `refine` | Acceptance criteria defined |
| `backlog` | `removed` | `cancel` | Decision to not pursue |
| `ready` | `in_progress` | `start` | Capacity available |
| `ready` | `removed` | `cancel` | No longer needed |
| `in_progress` | `blocked` | `block` | Blocker identified |
| `in_progress` | `in_review` | `submit` | Implementation complete |
| `in_progress` | `done` | `complete` | No review required |
| `in_progress` | `removed` | `cancel` | Work abandoned |
| `blocked` | `in_progress` | `unblock` | Blocker resolved |
| `in_review` | `done` | `approve` | Review passed |
| `in_review` | `in_progress` | `reject` | Issues found |

### 5.6 State Machine Mapping Rules

**To ADO Scrum:**
```
backlog     -> New
ready       -> Approved (PBI/Bug) or New (Task)
in_progress -> Committed (PBI/Bug) or In Progress (Task/Epic)
blocked     -> (use Impediment entity)
in_review   -> (custom state if needed)
done        -> Done
removed     -> Removed
```

**To SAFe:**
```
backlog     -> BACKLOG (Team) or FUNNEL (Portfolio)
ready       -> READY
in_progress -> IN_PROGRESS or IMPLEMENTING
blocked     -> (use blocking link)
in_review   -> REVIEW
done        -> DONE or ACCEPTED
removed     -> CANCELLED
```

**To JIRA:**
```
backlog     -> To Do / Open / Backlog
ready       -> Ready (custom) or To Do
in_progress -> In Progress
blocked     -> Blocked (custom status)
in_review   -> In Review / Under Review
done        -> Done (Resolution: Done/Fixed)
removed     -> Closed (Resolution: Won't Do/Duplicate)
```

---

## 6. Recommendations

### 6.1 Ontology Design Recommendations

| Recommendation | Rationale | Priority |
|---------------|-----------|----------|
| **Use 5-level hierarchy** | Epic > Capability > Feature > Story > Task covers all systems | High |
| **Make Capability optional** | Only SAFe uses it; can flatten to Feature for smaller orgs | Medium |
| **Support Business/Enabler typing** | Valuable classification from SAFe; optional for others | Medium |
| **Include Impediment as entity** | Explicit blocker tracking is valuable for visibility | Medium |
| **Model Resolution separately** | JIRA pattern is cleaner; separate completion reason from status | High |
| **Use state categories** | Three categories (Proposed/InProgress/Completed) with extensible states | High |
| **Minimal core, extensible custom** | Keep core properties small; support custom fields | High |

### 6.2 Mapping Complexity Assessment

| Mapping Direction | Complexity | Challenges |
|-------------------|-----------|------------|
| Canonical to ADO | Medium | Need to handle PBI vs Story naming; Impediment is direct |
| Canonical to SAFe | High | Must handle 4 Kanban systems; WSJF calculation |
| Canonical to JIRA | Medium | Need to manage Resolution separately; flexible hierarchy |
| ADO to Canonical | Low | Direct mapping; most concepts have equivalents |
| SAFe to Canonical | Medium | May need to flatten Capability; preserve WSJF data |
| JIRA to Canonical | Low | Need to derive status from Resolution+Status combo |

### 6.3 Implementation Considerations

1. **ID Strategy:** Use compound IDs (system:key) to prevent collisions
2. **State Sync:** Track both canonical state and system-specific state
3. **Property Mapping:** Store unmapped properties in `custom_fields` bucket
4. **Hierarchy Flexibility:** Allow configuration of which levels are active
5. **Link Type Extensibility:** Support custom link types beyond core set
6. **Resolution Handling:** Treat JIRA Resolution as first-class concept
7. **WSJF Support:** Include WSJF fields even if not used by all systems

### 6.4 Gap Mitigation Strategies

| Gap | System | Mitigation |
|-----|--------|------------|
| No Capability level | ADO, JIRA | Map to Feature; preserve original type in metadata |
| No WSJF | ADO, JIRA | Calculate if CoD components available; otherwise use priority |
| No Resolution | ADO, SAFe | Derive from final state reason |
| No Impediment entity | SAFe, JIRA | Create from blocking links; flag as synthetic |
| State mismatch | All | Map to nearest canonical state; preserve original in metadata |

---

## 7. Appendix: Evidence References

### 7.1 Entity Alignment Evidence

| Matrix Cell | Source Document | Section |
|-------------|-----------------|---------|
| Epic mappings | ADO-SCRUM-MODEL.md | Section 1.1 |
| Epic mappings | SAFE-MODEL.md | Section 2.1 |
| Epic mappings | JIRA-MODEL.md | Section 1.1 |
| Capability (SAFe) | SAFE-MODEL.md | Section 2.2 |
| Feature mappings | ADO-SCRUM-MODEL.md | Section 1.1 |
| Feature mappings | SAFE-MODEL.md | Section 2.3 |
| Story/PBI mappings | ADO-SCRUM-MODEL.md | Section 2.5 |
| Story mappings | SAFE-MODEL.md | Section 3.4 |
| Story mappings | JIRA-MODEL.md | Section 1.1 |
| Task mappings | All three models | Entity sections |
| Bug mappings | ADO-SCRUM-MODEL.md | Section 2.7 |
| Bug mappings | JIRA-MODEL.md | Section 1.1 |

### 7.2 Property Alignment Evidence

| Property Group | Source Document | Section |
|----------------|-----------------|---------|
| ADO System Properties | ADO-SCRUM-MODEL.md | Section 2.1 |
| ADO Planning Properties | ADO-SCRUM-MODEL.md | Section 2.2 |
| SAFe Epic Properties | SAFE-MODEL.md | Section 3.1 |
| SAFe Feature Properties | SAFE-MODEL.md | Section 3.3 |
| SAFe Story Properties | SAFE-MODEL.md | Section 3.4 |
| JIRA System Fields | JIRA-MODEL.md | Section 2.1 |
| JIRA Descriptive Fields | JIRA-MODEL.md | Section 2.2 |
| JIRA Time Fields | JIRA-MODEL.md | Section 2.5 |

### 7.3 Relationship Evidence

| Relationship Type | Source Document | Section |
|-------------------|-----------------|---------|
| ADO Link Types | ADO-SCRUM-MODEL.md | Section 4.1-4.4 |
| SAFe Containment | SAFE-MODEL.md | Section 5.1 |
| SAFe Dependencies | SAFE-MODEL.md | Section 5.3 |
| JIRA Link Types | JIRA-MODEL.md | Section 5 |
| JIRA Hierarchy | JIRA-MODEL.md | Section 1.3-1.4 |

### 7.4 State Machine Evidence

| State Machine | Source Document | Section |
|---------------|-----------------|---------|
| ADO PBI States | ADO-SCRUM-MODEL.md | Section 5.1 |
| ADO Bug States | ADO-SCRUM-MODEL.md | Section 5.2 |
| ADO Task States | ADO-SCRUM-MODEL.md | Section 5.3 |
| ADO Epic/Feature States | ADO-SCRUM-MODEL.md | Section 5.4 |
| SAFe Portfolio Kanban | SAFE-MODEL.md | Section 6.1 |
| SAFe Solution Kanban | SAFE-MODEL.md | Section 6.2 |
| SAFe ART Kanban | SAFE-MODEL.md | Section 6.3 |
| SAFe Team Kanban | SAFE-MODEL.md | Section 6.4 |
| JIRA Status Categories | JIRA-MODEL.md | Section 6.1 |
| JIRA Default Workflow | JIRA-MODEL.md | Section 6.3 |
| JIRA Resolution Model | JIRA-MODEL.md | Section 6.6-6.7 |

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Document ID** | EN-004-CROSS-DOMAIN-SYNTHESIS |
| **Version** | 1.0 |
| **Created** | 2026-01-13 |
| **Author** | ps-synthesizer (Claude Opus 4.5) |
| **Inputs** | ADO-SCRUM-MODEL.md, SAFE-MODEL.md, JIRA-MODEL.md |
| **Tables** | 32 |
| **Diagrams** | 2 |
| **Task 1** | Entity Alignment Matrix - COMPLETE |
| **Task 2** | Property Alignment Matrix - COMPLETE |
| **Task 3** | Relationship Pattern Analysis - COMPLETE |
| **Task 4** | State Machine Comparison - COMPLETE |

---

*End of Cross-Domain Synthesis Report*
