# Work Tracker Ontology v1.4

> **Document ID:** ONTOLOGY-v1
> **Version:** 1.4
> **Created:** 2026-01-13
> **Author:** nse-architecture (Claude Opus 4.5)
> **Project:** PROJ-006-worktracker-ontology
> **Entry ID:** e-001
> **Task:** WI-001 Task 1 - Entity Hierarchy Design
> **Status:** DRAFT - PENDING HUMAN REVIEW

---

> **DISCLAIMER (P-043):** This document was produced by an AI agent (nse-architecture)
> as part of the Jerry framework's problem-solving workflow. All recommendations,
> designs, and decisions herein are ADVISORY and require human review before
> implementation. The agent has traced findings to source artifacts where possible
> but makes no guarantee of completeness. Human judgment is the final authority.

---

## L0: Executive Summary

This document defines the canonical entity hierarchy for the Jerry Work Tracker Ontology, synthesizing concepts from Azure DevOps Scrum, SAFe, and JIRA into a unified domain model. The design follows a **5-level hierarchy** (Epic > Capability > Feature > Story > Task) with Capability marked as optional for non-SAFe organizations. The ontology introduces three abstract base categories: **StrategicItem** (long-term planning), **DeliveryItem** (sprint-level work), and **QualityItem** (defect tracking), plus **FlowControlItem** (impediments).

Key design decisions include: (1) using "Story" as the canonical term for user-valuable features (aligning with industry standard over ADO's "PBI"), (2) treating Bug as a first-class entity rather than a subtype, (3) modeling Impediment explicitly despite some systems using links, and (4) supporting the SAFe Business/Enabler classification as an optional cross-cutting concern. This ontology is designed for extensibility while maintaining a minimal core that maps cleanly to all three source systems.

---

## L1: Entity Hierarchy

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

| Level | Category | Entities | Planning Horizon | Typical Owner |
|-------|----------|----------|------------------|---------------|
| L0 | Portfolio | Initiative | Quarters/Years | Portfolio Manager |
| L1 | Strategic | Epic | Weeks/Months | Product Manager |
| L2 | Solution | Capability (optional) | PIs | Solution Manager |
| L3 | Program | Feature | Sprints | Product Owner |
| L4 | Delivery | Story, Enabler | Days | Development Team |
| L5 | Execution | Task, Subtask, Spike | Hours | Individual |
| - | Quality | Bug | Variable | QA/Dev |
| - | Flow | Impediment | Immediate | Scrum Master |

**Source Traceability:**
- Hierarchy levels derived from: CROSS-DOMAIN-SYNTHESIS.md Section 2.1 (Entity Alignment Matrix)
- 5-level recommendation from: CROSS-DOMAIN-SYNTHESIS.md Section 6.1 (Recommendation 1)

---

## L2: Detailed Entity Specifications

### 2.1 Abstract Base: WorkItem

```yaml
Entity: WorkItem
type: abstract
description: |
  Base class for all work tracking entities. Provides common
  identity, metadata, and lifecycle management. Cannot be
  instantiated directly.

properties:
  # Identity
  id:
    type: WorkItemId
    required: true
    immutable: true
    description: Unique identifier (system:key format)
    source: [ADO:System.Id, SAFe:id, JIRA:key]

  # Core Metadata
  title:
    type: string
    required: true
    constraints:
      minLength: 1
      maxLength: 500
    source: [ADO:System.Title, SAFe:name, JIRA:summary]

  description:
    type: richtext
    required: false
    source: [ADO:System.Description, SAFe:description, JIRA:description]

  # Classification
  work_type:
    type: WorkType (enum)
    required: true
    immutable: true
    description: Discriminator for concrete type

  classification:
    type: WorkClassification (enum: BUSINESS | ENABLER)
    required: false
    default: BUSINESS
    description: SAFe Business/Enabler typing (optional)
    source: [SAFe:type]

  # State
  status:
    type: WorkItemStatus (enum)
    required: true
    default: BACKLOG
    description: Lifecycle state
    source: [ADO:System.State, SAFe:state, JIRA:status]

  resolution:
    type: Resolution (enum)
    required: false
    description: Completion reason (JIRA pattern)
    source: [JIRA:resolution]

  # Priority
  priority:
    type: Priority (enum)
    required: false
    source: [ADO:Priority, SAFe:priority, JIRA:priority]

  # People
  assignee:
    type: User
    required: false
    source: [ADO:System.AssignedTo, SAFe:assignee, JIRA:assignee]

  created_by:
    type: User
    required: true
    auto: true
    source: [ADO:System.CreatedBy, SAFe:created_by, JIRA:reporter]

  # Timestamps
  created_at:
    type: datetime
    required: true
    auto: true
    immutable: true
    source: [ADO:System.CreatedDate, SAFe:created, JIRA:created]

  updated_at:
    type: datetime
    required: true
    auto: true
    source: [ADO:System.ChangedDate, SAFe:updated, JIRA:updated]

  # Hierarchy
  parent_id:
    type: WorkItemId
    required: false
    description: Parent work item reference
    source: [ADO:Hierarchy-Link, SAFe:parent, JIRA:parent]

  # Tags
  tags:
    type: string[]
    required: false
    source: [ADO:System.Tags, SAFe:labels, JIRA:labels]

behaviors:
  - create
  - update
  - transition (status change)
  - link (relationships)
  - comment
  - watch

invariants:
  - "title cannot be empty"
  - "status must be valid for entity type"
  - "parent must be valid parent type (if set)"
  - "circular hierarchy not allowed"
```

---

### 2.2 StrategicItem Entities

#### 2.2.1 Initiative

```yaml
Entity: Initiative
extends: WorkItem
work_type: INITIATIVE
description: |
  Portfolio-level strategic theme that groups related Epics.
  Represents major business objectives spanning quarters or years.
  OPTIONAL - only present in JIRA Premium and SAFe Strategic Themes.

additional_properties:
  target_date:
    type: date
    required: false
    description: Target completion date
    source: [JIRA:dueDate]

  business_outcome:
    type: richtext
    required: false
    description: Expected business outcomes
    source: [SAFe:business_outcome_hypothesis]

containment:
  allowed_children: [Epic]
  max_depth: 1

system_mapping:
  ADO: (not native - use Epic with tag)
  SAFe: Strategic Theme
  JIRA: Initiative (Premium)

design_rationale: |
  Initiative is included for JIRA Premium compatibility but marked
  as OPTIONAL. Organizations not using JIRA Premium or SAFe Strategic
  Themes can omit this level and use Epics as top-level containers.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.1, Section 2.3 (Gap Analysis)
```

#### 2.2.2 Epic

```yaml
Entity: Epic
extends: WorkItem
work_type: EPIC
description: |
  Large body of work spanning multiple sprints or months.
  Universal concept present in all three source systems.
  Primary container for Features (or Capabilities in SAFe).

additional_properties:
  target_quarter:
    type: string
    required: false
    description: Target fiscal quarter (e.g., "FY25-Q2")

  business_outcome_hypothesis:
    type: richtext
    required: false
    description: Expected outcomes (SAFe)
    source: [SAFe:business_outcome_hypothesis]

  lean_business_case:
    type: object
    required: false
    description: Economic justification
    source: [SAFe:lean_business_case]

  # SAFe WSJF
  wsjf_score:
    type: number
    required: false
    description: Weighted Shortest Job First score
    source: [SAFe:wsjf_score]

  cost_of_delay:
    type: number
    required: false
    description: CoD component for WSJF
    source: [SAFe:cost_of_delay]

  job_size:
    type: number
    required: false
    description: Job size component for WSJF
    source: [SAFe:job_size]

containment:
  allowed_children: [Capability, Feature]
  max_depth: 2 (via Feature)

system_mapping:
  ADO: Epic
  SAFe: Epic (Portfolio Backlog)
  JIRA: Epic

design_rationale: |
  Epic is universal across all systems. The additional WSJF properties
  support SAFe's economic prioritization model but are optional for
  teams not using SAFe.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2 (Canonical Name Rationale)
```

#### 2.2.3 Capability (OPTIONAL)

```yaml
Entity: Capability
extends: WorkItem
work_type: CAPABILITY
description: |
  SAFe Solution-level construct for large solutions with multiple
  ARTs. Bridges Epic and Feature for complex programs.
  OPTIONAL - only relevant for SAFe Large Solution configurations.

additional_properties:
  target_pi:
    type: string
    required: false
    description: Target Program Increment
    source: [SAFe:target_pi]

  benefit_hypothesis:
    type: richtext
    required: false
    description: Expected benefits
    source: [SAFe:benefit_hypothesis]

  enabler_type:
    type: EnablerType (enum)
    required: false
    description: Infrastructure, Exploration, Architecture, Compliance
    source: [SAFe:enabler_type]

containment:
  allowed_children: [Feature]
  allowed_parents: [Epic]

system_mapping:
  ADO: (not native - use Feature with tag)
  SAFe: Capability (Solution Backlog)
  JIRA: (not native - use Epic or Feature)

design_rationale: |
  Capability is SAFe-specific for Large Solution setups. Most
  organizations can flatten this to Feature. Included for SAFe
  compliance but marked OPTIONAL.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 6.1 (Recommendation 2)
```

#### 2.2.4 Feature

```yaml
Entity: Feature
extends: WorkItem
work_type: FEATURE
description: |
  Program-level functionality deliverable within 1-3 sprints.
  Present in ADO and SAFe; JIRA uses Epic for this level.
  Primary decomposition target for Stories.

additional_properties:
  benefit_hypothesis:
    type: richtext
    required: false
    description: Expected benefits
    source: [ADO:Value, SAFe:benefit_hypothesis]

  acceptance_criteria:
    type: richtext
    required: false
    description: Definition of Done criteria
    source: [ADO:AcceptanceCriteria, SAFe:acceptance_criteria]

  target_sprint:
    type: string
    required: false
    description: Target iteration/sprint

  mvp_definition:
    type: richtext
    required: false
    description: Minimum viable product scope
    source: [SAFe:mvp_definition]

containment:
  allowed_children: [Story, Enabler]
  allowed_parents: [Epic, Capability]

system_mapping:
  ADO: Feature
  SAFe: Feature (Program Backlog)
  JIRA: Epic (or custom issue type)

design_rationale: |
  Feature retained as distinct level despite JIRA lacking it natively.
  JIRA users map Epic-to-Feature or create custom issue type.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2, Section 2.3
```

---

### 2.3 DeliveryItem Entities

#### 2.3.1 Story

```yaml
Entity: Story
extends: WorkItem
work_type: STORY
description: |
  User-valuable increment deliverable within a sprint.
  Canonical term chosen over ADO's "Product Backlog Item" (PBI)
  as it is more intuitive and used by 2/3 systems.

additional_properties:
  effort:
    type: number
    required: false
    description: Story points or effort estimate
    source: [ADO:Effort, SAFe:story_points, JIRA:story_points]

  acceptance_criteria:
    type: richtext
    required: false
    description: Conditions for acceptance
    source: [ADO:AcceptanceCriteria, SAFe:acceptance_criteria]

  value_area:
    type: ValueArea (enum: BUSINESS | ARCHITECTURAL)
    required: false
    description: Value classification
    source: [ADO:ValueArea]

containment:
  allowed_children: [Task, Subtask]
  allowed_parents: [Feature]

system_mapping:
  ADO: Product Backlog Item (PBI)
  SAFe: Story
  JIRA: Story

design_rationale: |
  "Story" chosen over "PBI" because: (1) more intuitive for users,
  (2) used by 2/3 systems natively, (3) aligns with Scrum terminology.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2 (Canonical Name Rationale)
```

#### 2.3.2 Task

```yaml
Entity: Task
extends: WorkItem
work_type: TASK
description: |
  Specific work unit typically completed in hours to a day.
  Universal concept with identical semantics across all systems.

additional_properties:
  original_estimate:
    type: duration
    required: false
    description: Initial time estimate
    source: [ADO:OriginalEstimate, JIRA:original_estimate]

  remaining_work:
    type: duration
    required: false
    description: Remaining effort
    source: [ADO:RemainingWork, SAFe:remaining_hours, JIRA:remaining_estimate]

  time_spent:
    type: duration
    required: false
    description: Actual time logged
    source: [JIRA:time_spent]

  activity:
    type: Activity (enum)
    required: false
    description: Task type (Development, Testing, Documentation, etc.)
    source: [ADO:Activity]

containment:
  allowed_children: [Subtask]
  allowed_parents: [Story, Bug, Enabler]

system_mapping:
  ADO: Task
  SAFe: Task
  JIRA: Task, Sub-task

design_rationale: |
  Task is universally agreed across all systems. No translation needed.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.1
```

#### 2.3.3 Subtask

```yaml
Entity: Subtask
extends: WorkItem
work_type: SUBTASK
description: |
  Atomic, indivisible work unit. Leaf node in hierarchy.
  Child of Task only. Typically hours of work.

additional_properties:
  remaining_work:
    type: duration
    required: false

containment:
  allowed_children: [] # Leaf node
  allowed_parents: [Task]

system_mapping:
  ADO: Task (child of Task)
  SAFe: Task (subtask)
  JIRA: Sub-task

design_rationale: |
  Subtask represents the lowest decomposition level. Inherits from
  Task semantically but cannot have children.
  Trace: Existing Jerry WorkType enum (work_type.py)
```

#### 2.3.4 Spike

```yaml
Entity: Spike
extends: WorkItem
work_type: SPIKE
description: |
  Timeboxed research or exploration activity.
  Does NOT require quality gates (unlike other work types).
  Outputs knowledge/decisions, not production code.

additional_properties:
  timebox:
    type: duration
    required: true
    description: Maximum allowed duration
    constraints:
      max: "2 weeks"

  findings:
    type: richtext
    required: false
    description: Research findings/conclusions

  recommendation:
    type: richtext
    required: false
    description: Recommended next steps

containment:
  allowed_children: [] # Leaf node (research output)
  allowed_parents: [Feature, Story]

system_mapping:
  ADO: Task (with "spike" tag)
  SAFe: Enabler Story (Exploration type)
  JIRA: Task (with "spike" label)

design_rationale: |
  Spike modeled as first-class entity because it has distinct
  behavior: no quality gates required. SAFe formalizes this;
  other systems use labeling conventions.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.1 (Spike row)
  Existing Jerry: WorkType.SPIKE does not require quality gates
```

#### 2.3.5 Enabler

```yaml
Entity: Enabler
extends: WorkItem
work_type: ENABLER
description: |
  Technical/infrastructure work that enables future value delivery.
  SAFe concept for architectural runway, tech debt, etc.

additional_properties:
  enabler_type:
    type: EnablerType (enum)
    required: false
    values: [INFRASTRUCTURE, EXPLORATION, ARCHITECTURE, COMPLIANCE]
    source: [SAFe:enabler_type]

  nfrs:
    type: string[]
    required: false
    description: Non-functional requirements addressed
    source: [SAFe:nfrs]

containment:
  allowed_children: [Task]
  allowed_parents: [Feature, Epic]

system_mapping:
  ADO: PBI with ValueArea=Architectural
  SAFe: Enabler (all types)
  JIRA: Story with "enabler" label

design_rationale: |
  Enabler is SAFe's formal construct for non-feature work.
  ADO approximates via ValueArea. JIRA uses labeling.
  Modeled as first-class for SAFe compatibility.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 6.1 (Recommendation 3)
```

---

### 2.4 QualityItem Entities

#### 2.4.1 Bug

```yaml
Entity: Bug
extends: WorkItem
work_type: BUG
description: |
  Defect or problem requiring fix. First-class entity present
  in all three systems. Can exist at any hierarchy level.

additional_properties:
  severity:
    type: Severity (enum)
    required: false
    values: [CRITICAL, MAJOR, MINOR, TRIVIAL]
    source: [ADO:Severity, JIRA:priority]

  reproduction_steps:
    type: richtext
    required: false
    description: Steps to reproduce the issue
    source: [ADO:ReproSteps]

  found_in_version:
    type: string
    required: false
    description: Version where bug was found
    source: [JIRA:affects_version]

  fix_version:
    type: string
    required: false
    description: Target fix version
    source: [JIRA:fix_version]

  environment:
    type: richtext
    required: false
    description: Environment details
    source: [JIRA:environment]

  root_cause:
    type: richtext
    required: false
    description: Root cause analysis

containment:
  allowed_children: [Task]
  allowed_parents: [Feature, Story, Epic]

system_mapping:
  ADO: Bug
  SAFe: Defect (uses "Defect" terminology)
  JIRA: Bug

design_rationale: |
  "Bug" preferred over "Defect" because it is used by 2/3 systems
  and is more common in developer vernacular.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2 (Canonical Name Rationale)
```

---

### 2.5 FlowControlItem Entities

#### 2.5.1 Impediment

```yaml
Entity: Impediment
extends: WorkItem
work_type: IMPEDIMENT
description: |
  Blocker preventing progress on one or more work items.
  Explicit entity in ADO; other systems use blocking links.
  Valuable for visibility and tracking resolution time.

additional_properties:
  blocked_items:
    type: WorkItemId[]
    required: true
    description: Work items blocked by this impediment

  impact:
    type: ImpactLevel (enum)
    required: false
    values: [TEAM, PROGRAM, PORTFOLIO]
    description: Scope of impact

  owner:
    type: User
    required: false
    description: Person responsible for resolution

  resolution_notes:
    type: richtext
    required: false
    description: How the impediment was resolved

containment:
  allowed_children: [] # Impediments don't contain work
  allowed_parents: [] # Standalone entity

relationships:
  blocks: WorkItem[]  # Required relationship

system_mapping:
  ADO: Impediment
  SAFe: (blocking links, not explicit entity)
  JIRA: (blocking links, not explicit entity)

design_rationale: |
  Impediment modeled as first-class entity despite SAFe/JIRA
  using links. Explicit tracking enables better visibility,
  metrics, and resolution workflows. When importing from SAFe/JIRA,
  synthetic Impediments can be created from blocking relationships.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.1, Section 6.4 (Gap Mitigation)
```

---

## 3. Entity Classification and Properties

### 3.1 Classification Matrix

| Entity | Category | Level | Container | Atomic | Quality Gates | Optional |
|--------|----------|-------|-----------|--------|---------------|----------|
| Initiative | Strategic | L0 | Yes | No | No | Yes |
| Epic | Strategic | L1 | Yes | No | No | No |
| Capability | Strategic | L2 | Yes | No | No | Yes |
| Feature | Strategic | L3 | Yes | No | No | No |
| Story | Delivery | L4 | Yes | No | Yes | No |
| Task | Delivery | L5 | Yes | No | Yes | No |
| Subtask | Delivery | L5 | No | Yes | Yes | No |
| Spike | Delivery | L5 | No | Yes | **No** | No |
| Enabler | Delivery | L4 | Yes | No | Yes | No |
| Bug | Quality | - | Yes | No | Yes | No |
| Impediment | Flow | - | No | Yes | No | No |

### 3.2 Containment Rules Matrix

| Parent Type | Allowed Children |
|-------------|------------------|
| Initiative | Epic |
| Epic | Capability, Feature |
| Capability | Feature |
| Feature | Story, Enabler |
| Story | Task, Subtask |
| Task | Subtask |
| Subtask | (none) |
| Spike | (none) |
| Enabler | Task |
| Bug | Task |
| Impediment | (none - uses relationships) |

### 3.3 Cross-Cutting Classifications

#### Business vs. Enabler (SAFe)

```yaml
WorkClassification:
  type: enum
  values:
    - BUSINESS: Delivers direct customer/user value
    - ENABLER: Enables future value delivery (tech debt, architecture)
  applicable_to: [Epic, Feature, Story, Capability]
  source: [SAFe:type]
  default: BUSINESS
```

#### Enabler Types (SAFe)

```yaml
EnablerType:
  type: enum
  values:
    - INFRASTRUCTURE: Build development/deployment environments
    - EXPLORATION: Spikes, prototypes, research
    - ARCHITECTURE: Technical foundation and runway
    - COMPLIANCE: Regulatory, security, audit requirements
  applicable_to: [Capability, Feature, Enabler]
  source: [SAFe:enabler_type]
```

---

## 4. System Mapping Summary

### 4.1 Entity Mapping Table

| Canonical | ADO Scrum | SAFe | JIRA |
|-----------|-----------|------|------|
| Initiative | (Epic + tag) | Strategic Theme | Initiative (Premium) |
| Epic | Epic | Epic | Epic |
| Capability | (Feature + tag) | Capability | (Epic or custom) |
| Feature | Feature | Feature | Epic (or custom) |
| Story | Product Backlog Item | Story | Story |
| Task | Task | Task | Task |
| Subtask | Task (child) | Task (subtask) | Sub-task |
| Spike | Task + spike tag | Enabler Story (Exploration) | Task + spike label |
| Enabler | PBI (ValueArea=Arch) | Enabler | Story + enabler label |
| Bug | Bug | Defect | Bug |
| Impediment | Impediment | (blocking links) | (blocking links) |

### 4.2 Mapping Complexity

| Direction | Complexity | Notes |
|-----------|------------|-------|
| Canonical to ADO | Medium | PBI naming; Impediment direct |
| Canonical to SAFe | High | 4 Kanban systems; WSJF calculation |
| Canonical to JIRA | Medium | Resolution separation; flexible hierarchy |
| ADO to Canonical | Low | Direct mapping for most entities |
| SAFe to Canonical | Medium | May flatten Capability; preserve WSJF |
| JIRA to Canonical | Low | Derive status from Resolution+Status |

**Source:** CROSS-DOMAIN-SYNTHESIS.md Section 6.2 (Mapping Complexity Assessment)

---

## 5. Design Decisions

### 5.1 Decision: Story over PBI

**Decision:** Use "Story" as the canonical name for user-valuable features.

**Rationale:**
1. "Story" is more intuitive and widely understood
2. Used by 2/3 systems (SAFe, JIRA) natively
3. Aligns with Scrum methodology terminology
4. ADO's "PBI" is organization-specific naming

**Trade-off:** ADO users will see a different term in canonical view vs. native view.

**Trace:** CROSS-DOMAIN-SYNTHESIS.md Section 2.2

---

### 5.2 Decision: Bug as First-Class Entity

**Decision:** Model Bug as a concrete entity rather than a Story subtype.

**Rationale:**
1. All three systems treat Bug/Defect as distinct issue type
2. Bugs have unique properties (severity, repro steps, fix version)
3. Bugs can exist at any hierarchy level (Epic, Feature, Story)
4. Quality tracking semantics differ from Stories

**Trade-off:** Additional entity type increases ontology complexity.

**Trace:** CROSS-DOMAIN-SYNTHESIS.md Section 2.1

---

### 5.3 Decision: Explicit Impediment Entity

**Decision:** Model Impediment as a first-class entity despite SAFe/JIRA using links.

**Rationale:**
1. ADO has native Impediment entity
2. Explicit tracking enables better visibility and metrics
3. Resolution workflow is distinct from work item workflow
4. Can synthesize from blocking links when importing

**Trade-off:** Synthetic impediments needed when importing from SAFe/JIRA.

**Trace:** CROSS-DOMAIN-SYNTHESIS.md Section 6.4 (Gap Mitigation)

---

### 5.4 Decision: Optional Capability Level

**Decision:** Include Capability in hierarchy but mark as OPTIONAL.

**Rationale:**
1. Only SAFe uses Capability (Large Solution configurations)
2. Most organizations can flatten to Feature
3. Preserves SAFe compatibility for large enterprises
4. Non-SAFe users can ignore without loss of functionality

**Trade-off:** Hierarchy depth varies by configuration.

**Trace:** CROSS-DOMAIN-SYNTHESIS.md Section 6.1 (Recommendation 2)

---

### 5.5 Decision: Resolution as Separate Concept

**Decision:** Model Resolution separately from Status (following JIRA pattern).

**Rationale:**
1. JIRA's separation is semantically cleaner
2. Allows "Done" status with different resolutions (Fixed, Won't Fix, etc.)
3. Enables better reporting on completion reasons
4. ADO/SAFe can derive Resolution from state_reason

**Trade-off:** Additional property to manage; ADO/SAFe need derivation logic.

**Trace:** CROSS-DOMAIN-SYNTHESIS.md Section 6.1 (Recommendation 5)

---

### 5.6 Decision: Align with Existing Jerry Patterns

**Decision:** Maintain compatibility with existing Jerry domain models.

**Rationale:**
1. Existing WorkType enum has: EPIC, STORY, TASK, SUBTASK, BUG, SPIKE
2. Existing WorkItemStatus has: PENDING, IN_PROGRESS, BLOCKED, DONE, CANCELLED
3. Extensions should add to existing patterns, not replace them
4. Consistency with established codebase reduces cognitive load

**Alignment Actions:**
- Add INITIATIVE, FEATURE, CAPABILITY, ENABLER, IMPEDIMENT to WorkType
- Add BACKLOG, READY, IN_REVIEW to WorkItemStatus
- Extend existing WorkItem aggregate patterns

**Trace:** Existing Jerry codebase (work_item.py, work_type.py, work_item_status.py)

---

## 6. Gaps and Trade-offs

### 6.1 Identified Gaps

| Gap | Impact | Mitigation |
|-----|--------|------------|
| No native Capability in ADO/JIRA | Medium | Use Feature with tag/metadata |
| No WSJF in ADO/JIRA | Low | Calculate if CoD available; else use priority |
| No Resolution in ADO | Low | Derive from StateReason field |
| No explicit Impediment in SAFe/JIRA | Medium | Create synthetic from blocking links |
| Initiative only in JIRA Premium | Low | Optional level; use Epic for others |

### 6.2 Trade-off Summary

| Trade-off | Decision | Justification |
|-----------|----------|---------------|
| 5-level vs. 4-level | 5-level with optional L2 | SAFe compliance while supporting simpler orgs |
| Single WorkItem table vs. per-type | Single with discriminator | Simpler queries, consistent handling |
| Bug in hierarchy vs. standalone | Can be at any level | Matches real-world defect patterns |
| Strict hierarchy vs. flexible | Strict containment rules | Prevents inconsistent data |

---

## 7. Validation Checklist

For human reviewer to verify before approval:

- [ ] Entity hierarchy covers all required use cases
- [ ] Naming conventions align with organization standards
- [ ] System mappings are bidirectionally complete
- [ ] Design decisions have clear rationale
- [ ] Gaps are acceptable or have mitigation plans
- [ ] Compatibility with existing Jerry codebase confirmed
- [ ] No missing entities from source synthesis

---

## Appendix A: Evidence Traceability

| Section | Source Document | Source Section |
|---------|-----------------|----------------|
| 1.1 Hierarchy | CROSS-DOMAIN-SYNTHESIS.md | 2.1 Entity Alignment Matrix |
| 1.2 Levels | CROSS-DOMAIN-SYNTHESIS.md | 6.1 Recommendations |
| 2.2 Epic | CROSS-DOMAIN-SYNTHESIS.md | 2.2 Canonical Name Rationale |
| 2.3.1 Story | CROSS-DOMAIN-SYNTHESIS.md | 2.2 Canonical Name Rationale |
| 2.3.4 Spike | work_type.py | requires_quality_gates property |
| 2.4.1 Bug | CROSS-DOMAIN-SYNTHESIS.md | 2.2 Canonical Name Rationale |
| 2.5.1 Impediment | CROSS-DOMAIN-SYNTHESIS.md | 2.1, 6.4 Gap Mitigation |
| 4.1 Mapping | CROSS-DOMAIN-SYNTHESIS.md | 2.1 Entity Alignment Matrix |
| 4.2 Complexity | CROSS-DOMAIN-SYNTHESIS.md | 6.2 Mapping Complexity |

---

## Appendix B: Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-13 | nse-architecture | Initial draft - Task 1 complete |
| 1.1 | 2026-01-13 | nse-architecture | Added Section 3: Entity Schemas (Task 2) |
| 1.2 | 2026-01-13 | nse-architecture | Added Section 4: Relationship Types (Task 3) |
| 1.3 | 2026-01-13 | nse-architecture | Added Section 5: Canonical State Machine (Task 4) |
| 1.4 | 2026-01-14 | nse-architecture | Added Section 6: System Mappings (Task 5) |

---

## Section 3: Entity Schemas

> **Task:** WI-001 Task 2 - Define entity schemas
> **Author:** nse-architecture (Claude Opus 4.5)
> **Date:** 2026-01-13
> **Status:** DRAFT - PENDING HUMAN REVIEW

---

> **DISCLAIMER (P-043):** This section was produced by an AI agent (nse-architecture)
> as part of the Jerry framework's problem-solving workflow. All schema definitions,
> property constraints, and invariants herein are ADVISORY and require human review
> before implementation. Property mappings are traced to CROSS-DOMAIN-SYNTHESIS.md
> where possible. Human judgment is the final authority.

---

### 3.1 Schema Design Principles

The entity schemas follow these design principles derived from the synthesis:

1. **Property Inheritance:** Child entities inherit all properties from their parent class
2. **Minimal Required Properties:** Only truly essential properties are marked required
3. **Immutable Identity:** ID and work_type are immutable after creation
4. **Auto-Populated Timestamps:** created_at, updated_at, created_by are system-managed
5. **Extensibility:** custom_fields bucket allows system-specific properties
6. **Type Safety:** All properties have explicit types with validation constraints

**Source Traceability:**
- Core properties: CROSS-DOMAIN-SYNTHESIS.md Section 3.1
- Extended properties: CROSS-DOMAIN-SYNTHESIS.md Section 3.2
- Property type mapping: CROSS-DOMAIN-SYNTHESIS.md Section 3.4

---

### 3.2 Abstract Base Schema: WorkItem

```yaml
Entity: WorkItem
type: abstract
extends: null
description: |
  Abstract base class for all work tracking entities. Provides common
  identity, metadata, lifecycle management, and hierarchy support.
  Cannot be instantiated directly - use concrete entity types.

properties:
  inherited: []  # Root entity - no inheritance

  specific:
    # === IDENTITY (Immutable) ===
    id:
      type: WorkItemId
      required: true
      immutable: true
      auto: true
      constraints:
        pattern: "^[A-Z]+-[0-9]+$"  # e.g., JERRY-123, PROJ-456
      description: "Unique identifier in system:key format"
      source: [ADO:System.Id, SAFe:id, JIRA:key]

    work_type:
      type: WorkType (enum)
      required: true
      immutable: true
      values: [INITIATIVE, EPIC, CAPABILITY, FEATURE, STORY, TASK, SUBTASK,
               SPIKE, ENABLER, BUG, IMPEDIMENT]
      description: "Discriminator for concrete entity type"
      source: "Ontology-defined enumeration"

    # === CORE METADATA ===
    title:
      type: string
      required: true
      immutable: false
      constraints:
        minLength: 1
        maxLength: 500
      description: "Human-readable title/summary"
      source: [ADO:System.Title, SAFe:name, JIRA:summary]

    description:
      type: richtext
      required: false
      immutable: false
      constraints:
        maxLength: 50000  # ~50KB
      description: "Detailed description with rich formatting"
      source: [ADO:System.Description, SAFe:description, JIRA:description]

    # === CLASSIFICATION ===
    classification:
      type: WorkClassification (enum)
      required: false
      immutable: false
      values: [BUSINESS, ENABLER]
      default: BUSINESS
      description: "SAFe Business/Enabler typing (optional for non-SAFe)"
      source: [SAFe:type]

    # === LIFECYCLE STATE ===
    status:
      type: WorkItemStatus (enum)
      required: true
      immutable: false
      values: [BACKLOG, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, DONE, REMOVED]
      default: BACKLOG
      description: "Current lifecycle state"
      source: [ADO:System.State, SAFe:state, JIRA:status]
      note: "Extended from existing Jerry WorkItemStatus (PENDING->BACKLOG, added READY/IN_REVIEW/REMOVED)"

    resolution:
      type: Resolution (enum)
      required: false
      immutable: false
      values: [DONE, FIXED, WONT_DO, DUPLICATE, CANNOT_REPRODUCE, OBSOLETE]
      description: "Completion reason (JIRA pattern for richer semantics)"
      source: [JIRA:resolution]
      applicability: "Only set when status is DONE or REMOVED"

    # === PRIORITY ===
    priority:
      type: Priority (enum)
      required: false
      immutable: false
      values: [CRITICAL, HIGH, MEDIUM, LOW]
      default: MEDIUM
      description: "Work priority level"
      source: [ADO:Priority, SAFe:priority, JIRA:priority]

    # === PEOPLE ===
    assignee:
      type: User
      required: false
      immutable: false
      description: "User responsible for this work item"
      source: [ADO:System.AssignedTo, SAFe:assignee, JIRA:assignee]

    created_by:
      type: User
      required: true
      immutable: true
      auto: true
      description: "User who created this work item"
      source: [ADO:System.CreatedBy, SAFe:created_by, JIRA:reporter]

    # === TIMESTAMPS ===
    created_at:
      type: datetime
      required: true
      immutable: true
      auto: true
      description: "UTC timestamp when created"
      source: [ADO:System.CreatedDate, SAFe:created, JIRA:created]

    updated_at:
      type: datetime
      required: true
      immutable: false
      auto: true
      description: "UTC timestamp of last update"
      source: [ADO:System.ChangedDate, SAFe:updated, JIRA:updated]

    # === HIERARCHY ===
    parent_id:
      type: WorkItemId
      required: false
      immutable: false
      constraints:
        valid_parent_type: "Defined by entity type"
        no_circular_reference: true
      description: "Reference to parent work item"
      source: [ADO:Hierarchy-Link, SAFe:parent, JIRA:parent]

    # === CATEGORIZATION ===
    tags:
      type: string[]
      required: false
      immutable: false
      constraints:
        maxItems: 50
        itemMaxLength: 100
      description: "Labels for categorization and filtering"
      source: [ADO:System.Tags, SAFe:labels, JIRA:labels]

    # === EXTENSIBILITY ===
    custom_fields:
      type: object
      required: false
      immutable: false
      description: "Bucket for system-specific unmapped properties"
      constraints:
        maxSize: 100KB

behaviors:
  - create: "Instantiate new work item with required properties"
  - update: "Modify mutable properties"
  - transition: "Change status following state machine rules"
  - link: "Create relationships with other entities"
  - comment: "Add comments/discussion"
  - watch: "Subscribe to change notifications"
  - delete: "Soft delete (transition to REMOVED)"

invariants:
  - "INV-001: title cannot be empty or whitespace-only"
  - "INV-002: status must be valid for entity type's state machine"
  - "INV-003: parent_id must reference valid parent type (if set)"
  - "INV-004: circular hierarchy references are not allowed"
  - "INV-005: resolution is only set when status is terminal (DONE or REMOVED)"
  - "INV-006: work_type cannot change after creation"
  - "INV-007: id cannot change after creation"
  - "INV-008: created_at cannot be in the future"
```

**Jerry Codebase Alignment:**
- Existing `WorkType` enum has: EPIC, STORY, TASK, SUBTASK, BUG, SPIKE
- Extensions needed: INITIATIVE, CAPABILITY, FEATURE, ENABLER, IMPEDIMENT
- Existing `WorkItemStatus` has: PENDING, IN_PROGRESS, BLOCKED, DONE, CANCELLED
- Extensions needed: Map PENDING->BACKLOG, CANCELLED->REMOVED, add READY, IN_REVIEW

---

### 3.3 Abstract Category Schemas

#### 3.3.1 StrategicItem (Abstract)

```yaml
Entity: StrategicItem
type: abstract
extends: WorkItem
description: |
  Abstract base for long-term planning items (Initiative, Epic, Capability, Feature).
  Strategic items represent work planned over weeks to years.

properties:
  inherited:
    - All WorkItem properties

  specific:
    target_date:
      type: date
      required: false
      immutable: false
      description: "Target completion date for strategic planning"
      source: [JIRA:dueDate]

    business_outcome:
      type: richtext
      required: false
      immutable: false
      constraints:
        maxLength: 10000
      description: "Expected business outcomes/hypothesis"
      source: [SAFe:business_outcome_hypothesis]

behaviors:
  - All WorkItem behaviors
  - "decompose: Break down into child items"
  - "roadmap: Include in roadmap/timeline planning"

invariants:
  - All WorkItem invariants
  - "INV-S01: target_date must be in the future when set"
  - "INV-S02: Strategic items should have at least one child when IN_PROGRESS"

applicable_work_types: [INITIATIVE, EPIC, CAPABILITY, FEATURE]
planning_horizon: "Weeks to Years"
```

#### 3.3.2 DeliveryItem (Abstract)

```yaml
Entity: DeliveryItem
type: abstract
extends: WorkItem
description: |
  Abstract base for sprint-level execution items (Story, Task, Subtask, Spike, Enabler).
  Delivery items represent work completed within sprints/iterations.

properties:
  inherited:
    - All WorkItem properties

  specific:
    effort:
      type: number
      required: false
      immutable: false
      constraints:
        min: 0
        max: 100
      description: "Story points or effort estimate"
      source: [ADO:Effort, SAFe:story_points, JIRA:story_points]

    acceptance_criteria:
      type: richtext
      required: false
      immutable: false
      constraints:
        maxLength: 10000
      description: "Conditions that must be met for acceptance"
      source: [ADO:AcceptanceCriteria, SAFe:acceptance_criteria]

    due_date:
      type: date
      required: false
      immutable: false
      description: "Sprint or iteration deadline"
      source: [ADO:TargetDate, JIRA:dueDate]

behaviors:
  - All WorkItem behaviors
  - "estimate: Set/update effort estimate"
  - "accept: Mark as meeting acceptance criteria"

invariants:
  - All WorkItem invariants
  - "INV-D01: effort must be non-negative"
  - "INV-D02: acceptance_criteria should be defined before IN_PROGRESS"

applicable_work_types: [STORY, TASK, SUBTASK, SPIKE, ENABLER]
planning_horizon: "Days to Weeks"
```

#### 3.3.3 QualityItem (Abstract)

```yaml
Entity: QualityItem
type: abstract
extends: WorkItem
description: |
  Abstract base for defect and quality tracking items (Bug).
  Quality items represent issues requiring fixes.

properties:
  inherited:
    - All WorkItem properties

  specific:
    severity:
      type: Severity (enum)
      required: false
      immutable: false
      values: [CRITICAL, MAJOR, MINOR, TRIVIAL]
      default: MAJOR
      description: "Impact severity of the defect"
      source: [ADO:Severity, JIRA:priority]

    found_in_version:
      type: string
      required: false
      immutable: false
      constraints:
        maxLength: 50
      description: "Version where defect was discovered"
      source: [JIRA:affects_version]

    fix_version:
      type: string
      required: false
      immutable: false
      constraints:
        maxLength: 50
      description: "Target version for the fix"
      source: [JIRA:fix_version]

behaviors:
  - All WorkItem behaviors
  - "triage: Assess and categorize severity"
  - "verify: Confirm fix is effective"

invariants:
  - All WorkItem invariants
  - "INV-Q01: CRITICAL severity bugs must have assignee"
  - "INV-Q02: fix_version should be set before DONE"

applicable_work_types: [BUG]
planning_horizon: "Variable (based on severity)"
```

#### 3.3.4 FlowControlItem (Abstract)

```yaml
Entity: FlowControlItem
type: abstract
extends: WorkItem
description: |
  Abstract base for workflow impediments (Impediment).
  Flow control items represent blockers requiring resolution.

properties:
  inherited:
    - All WorkItem properties

  specific:
    blocked_items:
      type: WorkItemId[]
      required: true
      immutable: false
      constraints:
        minItems: 1
        maxItems: 50
      description: "Work items blocked by this impediment"
      source: [ADO:Impediment.BlockedItems]

    impact:
      type: ImpactLevel (enum)
      required: false
      immutable: false
      values: [TEAM, PROGRAM, PORTFOLIO]
      default: TEAM
      description: "Organizational scope of impact"

    resolution_notes:
      type: richtext
      required: false
      immutable: false
      description: "How the impediment was resolved"

behaviors:
  - All WorkItem behaviors
  - "escalate: Raise impact level"
  - "resolve: Mark as resolved and unblock items"

invariants:
  - All WorkItem invariants
  - "INV-F01: blocked_items must contain at least one item"
  - "INV-F02: resolution_notes must be set when status is DONE"
  - "INV-F03: blocked items must be unblocked when impediment is DONE"

applicable_work_types: [IMPEDIMENT]
planning_horizon: "Immediate"
```

---

### 3.4 Concrete Entity Schemas

#### 3.4.1 Initiative

```yaml
Entity: Initiative
type: concrete
extends: StrategicItem
work_type: INITIATIVE
optional: true
description: |
  Portfolio-level strategic theme grouping related Epics.
  Represents major business objectives spanning quarters or years.
  OPTIONAL - only present in JIRA Premium and SAFe Strategic Themes.

properties:
  inherited:
    - id, work_type, title, description (WorkItem)
    - classification, status, resolution, priority (WorkItem)
    - assignee, created_by, created_at, updated_at (WorkItem)
    - parent_id, tags, custom_fields (WorkItem)
    - target_date, business_outcome (StrategicItem)

  specific:
    fiscal_year:
      type: string
      required: false
      immutable: false
      constraints:
        pattern: "^FY[0-9]{2}$"  # e.g., FY25, FY26
      description: "Fiscal year for the initiative"

    strategic_theme:
      type: string
      required: false
      immutable: false
      constraints:
        maxLength: 200
      description: "Strategic theme alignment"
      source: [SAFe:strategic_theme]

containment:
  allowed_children: [Epic]
  allowed_parents: []  # Top-level entity
  max_depth: 1

system_mapping:
  ADO: "(not native - use Epic with tag)"
  SAFe: "Strategic Theme"
  JIRA: "Initiative (Premium)"

state_machine:
  initial: BACKLOG
  valid_states: [BACKLOG, READY, IN_PROGRESS, DONE, REMOVED]
  transitions:
    BACKLOG: [READY, REMOVED]
    READY: [IN_PROGRESS, BACKLOG, REMOVED]
    IN_PROGRESS: [DONE, REMOVED]
    DONE: []
    REMOVED: []

invariants:
  - All StrategicItem invariants
  - "INV-I01: Initiative can only contain Epics"

design_rationale: |
  Initiative is included for JIRA Premium compatibility but marked OPTIONAL.
  Organizations not using JIRA Premium or SAFe Strategic Themes can omit
  this level and use Epics as top-level containers.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.1, Section 2.3 (Gap Analysis)
```

#### 3.4.2 Epic

```yaml
Entity: Epic
type: concrete
extends: StrategicItem
work_type: EPIC
optional: false
description: |
  Large body of work spanning multiple sprints or months.
  Universal concept present in all three source systems.
  Primary container for Features (or Capabilities in SAFe).

properties:
  inherited:
    - id, work_type, title, description (WorkItem)
    - classification, status, resolution, priority (WorkItem)
    - assignee, created_by, created_at, updated_at (WorkItem)
    - parent_id, tags, custom_fields (WorkItem)
    - target_date, business_outcome (StrategicItem)

  specific:
    target_quarter:
      type: string
      required: false
      immutable: false
      constraints:
        pattern: "^FY[0-9]{2}-Q[1-4]$"  # e.g., FY25-Q2
      description: "Target fiscal quarter"

    lean_business_case:
      type: object
      required: false
      immutable: false
      properties:
        problem: string
        solution: string
        cost: number
        benefit: number
        risk: string
      description: "Economic justification (SAFe pattern)"
      source: [SAFe:lean_business_case]

    # SAFe WSJF Components
    wsjf_score:
      type: number
      required: false
      immutable: false
      constraints:
        min: 0
      description: "Weighted Shortest Job First score"
      source: [SAFe:wsjf_score]
      note: "Calculated: (business_value + time_criticality + risk_reduction) / job_size"

    cost_of_delay:
      type: number
      required: false
      immutable: false
      constraints:
        min: 0
      description: "CoD component for WSJF (sum of value components)"
      source: [SAFe:cost_of_delay]

    job_size:
      type: number
      required: false
      immutable: false
      constraints:
        min: 1  # Cannot be zero (division)
      description: "Implementation size estimate (1-13 Fibonacci)"
      source: [SAFe:job_size]

containment:
  allowed_children: [Capability, Feature]
  allowed_parents: [Initiative]  # Or top-level if no Initiative
  max_depth: 2

system_mapping:
  ADO: "Epic"
  SAFe: "Epic (Portfolio Backlog)"
  JIRA: "Epic"

state_machine:
  initial: BACKLOG
  valid_states: [BACKLOG, READY, IN_PROGRESS, DONE, REMOVED]
  transitions:
    BACKLOG: [READY, REMOVED]
    READY: [IN_PROGRESS, BACKLOG, REMOVED]
    IN_PROGRESS: [DONE, BLOCKED, REMOVED]
    BLOCKED: [IN_PROGRESS, REMOVED]
    DONE: [IN_PROGRESS]  # Reopen
    REMOVED: []

invariants:
  - All StrategicItem invariants
  - "INV-E01: Epic can contain Capabilities or Features (not mixed)"
  - "INV-E02: wsjf_score = cost_of_delay / job_size (when both set)"
  - "INV-E03: job_size must be > 0 if set"

design_rationale: |
  Epic is universal across all systems. The additional WSJF properties
  support SAFe's economic prioritization model but are optional for
  teams not using SAFe.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2 (Canonical Name Rationale)
```

#### 3.4.3 Capability (OPTIONAL)

```yaml
Entity: Capability
type: concrete
extends: StrategicItem
work_type: CAPABILITY
optional: true
description: |
  SAFe Solution-level construct for large solutions with multiple ARTs.
  Bridges Epic and Feature for complex programs.
  OPTIONAL - only relevant for SAFe Large Solution configurations.

properties:
  inherited:
    - id, work_type, title, description (WorkItem)
    - classification, status, resolution, priority (WorkItem)
    - assignee, created_by, created_at, updated_at (WorkItem)
    - parent_id, tags, custom_fields (WorkItem)
    - target_date, business_outcome (StrategicItem)

  specific:
    target_pi:
      type: string
      required: false
      immutable: false
      constraints:
        pattern: "^PI[0-9]{1,3}$"  # e.g., PI1, PI12
      description: "Target Program Increment"
      source: [SAFe:target_pi]

    benefit_hypothesis:
      type: richtext
      required: false
      immutable: false
      constraints:
        maxLength: 5000
      description: "Expected benefits statement"
      source: [SAFe:benefit_hypothesis]

    enabler_type:
      type: EnablerType (enum)
      required: false
      immutable: false
      values: [INFRASTRUCTURE, EXPLORATION, ARCHITECTURE, COMPLIANCE]
      description: "Type of enabler capability (if classification=ENABLER)"
      source: [SAFe:enabler_type]
      applicability: "Only when classification=ENABLER"

containment:
  allowed_children: [Feature]
  allowed_parents: [Epic]
  max_depth: 1

system_mapping:
  ADO: "(not native - use Feature with tag)"
  SAFe: "Capability (Solution Backlog)"
  JIRA: "(not native - use Epic or Feature)"

state_machine:
  initial: BACKLOG
  valid_states: [BACKLOG, READY, IN_PROGRESS, DONE, REMOVED]
  transitions:
    BACKLOG: [READY, REMOVED]
    READY: [IN_PROGRESS, BACKLOG, REMOVED]
    IN_PROGRESS: [DONE, BLOCKED, REMOVED]
    BLOCKED: [IN_PROGRESS, REMOVED]
    DONE: []
    REMOVED: []

invariants:
  - All StrategicItem invariants
  - "INV-C01: Capability can only contain Features"
  - "INV-C02: enabler_type is only valid when classification=ENABLER"
  - "INV-C03: Capability must have Epic as parent"

design_rationale: |
  Capability is SAFe-specific for Large Solution setups. Most
  organizations can flatten this to Feature. Included for SAFe
  compliance but marked OPTIONAL.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 6.1 (Recommendation 2)
```

#### 3.4.4 Feature

```yaml
Entity: Feature
type: concrete
extends: StrategicItem
work_type: FEATURE
optional: false
description: |
  Program-level functionality deliverable within 1-3 sprints.
  Present in ADO and SAFe; JIRA uses Epic for this level.
  Primary decomposition target for Stories.

properties:
  inherited:
    - id, work_type, title, description (WorkItem)
    - classification, status, resolution, priority (WorkItem)
    - assignee, created_by, created_at, updated_at (WorkItem)
    - parent_id, tags, custom_fields (WorkItem)
    - target_date, business_outcome (StrategicItem)

  specific:
    benefit_hypothesis:
      type: richtext
      required: false
      immutable: false
      constraints:
        maxLength: 5000
      description: "Expected benefits from this feature"
      source: [ADO:Value, SAFe:benefit_hypothesis]

    acceptance_criteria:
      type: richtext
      required: false
      immutable: false
      constraints:
        maxLength: 10000
      description: "Feature-level definition of done"
      source: [ADO:AcceptanceCriteria, SAFe:acceptance_criteria]

    target_sprint:
      type: string
      required: false
      immutable: false
      constraints:
        maxLength: 50
      description: "Target sprint/iteration"

    mvp_definition:
      type: richtext
      required: false
      immutable: false
      constraints:
        maxLength: 5000
      description: "Minimum viable product scope"
      source: [SAFe:mvp_definition]

    value_area:
      type: ValueArea (enum)
      required: false
      immutable: false
      values: [BUSINESS, ARCHITECTURAL]
      default: BUSINESS
      description: "Value classification (ADO pattern)"
      source: [ADO:ValueArea]

containment:
  allowed_children: [Story, Enabler]
  allowed_parents: [Epic, Capability]
  max_depth: 1

system_mapping:
  ADO: "Feature"
  SAFe: "Feature (Program Backlog)"
  JIRA: "Epic (or custom issue type)"

state_machine:
  initial: BACKLOG
  valid_states: [BACKLOG, READY, IN_PROGRESS, IN_REVIEW, DONE, REMOVED]
  transitions:
    BACKLOG: [READY, REMOVED]
    READY: [IN_PROGRESS, BACKLOG, REMOVED]
    IN_PROGRESS: [IN_REVIEW, DONE, BLOCKED, REMOVED]
    BLOCKED: [IN_PROGRESS, REMOVED]
    IN_REVIEW: [DONE, IN_PROGRESS]
    DONE: [IN_PROGRESS]  # Reopen
    REMOVED: []

invariants:
  - All StrategicItem invariants
  - "INV-FE01: Feature can contain Stories or Enablers"
  - "INV-FE02: acceptance_criteria should be defined before DONE"

design_rationale: |
  Feature retained as distinct level despite JIRA lacking it natively.
  JIRA users map Epic-to-Feature or create custom issue type.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2, Section 2.3
```

#### 3.4.5 Story

```yaml
Entity: Story
type: concrete
extends: DeliveryItem
work_type: STORY
optional: false
description: |
  User-valuable increment deliverable within a sprint.
  Canonical term chosen over ADO's "Product Backlog Item" (PBI)
  as it is more intuitive and used by 2/3 systems.

properties:
  inherited:
    - id, work_type, title, description (WorkItem)
    - classification, status, resolution, priority (WorkItem)
    - assignee, created_by, created_at, updated_at (WorkItem)
    - parent_id, tags, custom_fields (WorkItem)
    - effort, acceptance_criteria, due_date (DeliveryItem)

  specific:
    value_area:
      type: ValueArea (enum)
      required: false
      immutable: false
      values: [BUSINESS, ARCHITECTURAL]
      default: BUSINESS
      description: "Value classification"
      source: [ADO:ValueArea]

    user_role:
      type: string
      required: false
      immutable: false
      constraints:
        maxLength: 100
      description: "As a <user_role>... (user story format)"

    user_goal:
      type: string
      required: false
      immutable: false
      constraints:
        maxLength: 500
      description: "I want <goal>... (user story format)"

    user_benefit:
      type: string
      required: false
      immutable: false
      constraints:
        maxLength: 500
      description: "So that <benefit>... (user story format)"

containment:
  allowed_children: [Task, Subtask]
  allowed_parents: [Feature]
  max_depth: 2

system_mapping:
  ADO: "Product Backlog Item (PBI)"
  SAFe: "Story"
  JIRA: "Story"

state_machine:
  initial: BACKLOG
  valid_states: [BACKLOG, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, DONE, REMOVED]
  transitions:
    BACKLOG: [READY, REMOVED]
    READY: [IN_PROGRESS, BACKLOG, REMOVED]
    IN_PROGRESS: [BLOCKED, IN_REVIEW, DONE, REMOVED]
    BLOCKED: [IN_PROGRESS, REMOVED]
    IN_REVIEW: [DONE, IN_PROGRESS]
    DONE: [IN_PROGRESS]  # Reopen
    REMOVED: []

invariants:
  - All DeliveryItem invariants
  - "INV-ST01: Story must have Feature as parent"
  - "INV-ST02: Story effort is typically 1-13 (Fibonacci)"
  - "INV-ST03: acceptance_criteria must be defined before DONE"

design_rationale: |
  "Story" chosen over "PBI" because: (1) more intuitive for users,
  (2) used by 2/3 systems natively, (3) aligns with Scrum terminology.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2 (Canonical Name Rationale)

jerry_alignment:
  existing_type: "WorkType.STORY"
  changes_needed: "None - already exists"
```

#### 3.4.6 Task

```yaml
Entity: Task
type: concrete
extends: DeliveryItem
work_type: TASK
optional: false
description: |
  Specific work unit typically completed in hours to a day.
  Universal concept with identical semantics across all systems.

properties:
  inherited:
    - id, work_type, title, description (WorkItem)
    - classification, status, resolution, priority (WorkItem)
    - assignee, created_by, created_at, updated_at (WorkItem)
    - parent_id, tags, custom_fields (WorkItem)
    - effort, acceptance_criteria, due_date (DeliveryItem)

  specific:
    original_estimate:
      type: duration
      required: false
      immutable: false
      constraints:
        min: 0
        unit: hours
      description: "Initial time estimate in hours"
      source: [ADO:OriginalEstimate, JIRA:original_estimate]

    remaining_work:
      type: duration
      required: false
      immutable: false
      constraints:
        min: 0
        unit: hours
      description: "Remaining effort in hours"
      source: [ADO:RemainingWork, SAFe:remaining_hours, JIRA:remaining_estimate]

    time_spent:
      type: duration
      required: false
      immutable: false
      constraints:
        min: 0
        unit: hours
      description: "Actual time logged"
      source: [JIRA:time_spent]

    activity:
      type: Activity (enum)
      required: false
      immutable: false
      values: [DEVELOPMENT, TESTING, DOCUMENTATION, DESIGN, DEPLOYMENT, RESEARCH, OTHER]
      description: "Type of task activity"
      source: [ADO:Activity]

containment:
  allowed_children: [Subtask]
  allowed_parents: [Story, Bug, Enabler]
  max_depth: 1

system_mapping:
  ADO: "Task"
  SAFe: "Task"
  JIRA: "Task, Sub-task"

state_machine:
  initial: BACKLOG
  valid_states: [BACKLOG, IN_PROGRESS, BLOCKED, DONE, REMOVED]
  transitions:
    BACKLOG: [IN_PROGRESS, REMOVED]
    IN_PROGRESS: [BLOCKED, DONE, REMOVED]
    BLOCKED: [IN_PROGRESS, REMOVED]
    DONE: [IN_PROGRESS]  # Reopen
    REMOVED: []
  note: "Simplified state machine for Tasks (no READY, no IN_REVIEW)"

invariants:
  - All DeliveryItem invariants
  - "INV-T01: Task can have Story, Bug, or Enabler as parent"
  - "INV-T02: remaining_work <= original_estimate when both set"
  - "INV-T03: time_spent should be updated when DONE"

design_rationale: |
  Task is universally agreed across all systems. No translation needed.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.1

jerry_alignment:
  existing_type: "WorkType.TASK"
  changes_needed: "None - already exists"
```

#### 3.4.7 Subtask

```yaml
Entity: Subtask
type: concrete
extends: DeliveryItem
work_type: SUBTASK
optional: false
description: |
  Atomic, indivisible work unit. Leaf node in hierarchy.
  Child of Task only. Typically hours of work.

properties:
  inherited:
    - id, work_type, title, description (WorkItem)
    - classification, status, resolution, priority (WorkItem)
    - assignee, created_by, created_at, updated_at (WorkItem)
    - parent_id, tags, custom_fields (WorkItem)
    - effort, acceptance_criteria, due_date (DeliveryItem)

  specific:
    remaining_work:
      type: duration
      required: false
      immutable: false
      constraints:
        min: 0
        unit: hours
      description: "Remaining effort in hours"

containment:
  allowed_children: []  # Leaf node
  allowed_parents: [Task]
  max_depth: 0  # Cannot have children

system_mapping:
  ADO: "Task (child of Task)"
  SAFe: "Task (subtask)"
  JIRA: "Sub-task"

state_machine:
  initial: BACKLOG
  valid_states: [BACKLOG, IN_PROGRESS, DONE, REMOVED]
  transitions:
    BACKLOG: [IN_PROGRESS, REMOVED]
    IN_PROGRESS: [DONE, REMOVED]
    DONE: [IN_PROGRESS]  # Reopen
    REMOVED: []
  note: "Minimal state machine for atomic work"

invariants:
  - All DeliveryItem invariants
  - "INV-SUB01: Subtask must have Task as parent"
  - "INV-SUB02: Subtask cannot have children (leaf node)"

design_rationale: |
  Subtask represents the lowest decomposition level. Inherits from
  Task semantically but cannot have children.
  Trace: Existing Jerry WorkType enum (work_type.py)

jerry_alignment:
  existing_type: "WorkType.SUBTASK"
  changes_needed: "None - already exists"
```

#### 3.4.8 Spike

```yaml
Entity: Spike
type: concrete
extends: DeliveryItem
work_type: SPIKE
optional: false
description: |
  Timeboxed research or exploration activity.
  Does NOT require quality gates (unlike other work types).
  Outputs knowledge/decisions, not production code.

properties:
  inherited:
    - id, work_type, title, description (WorkItem)
    - classification, status, resolution, priority (WorkItem)
    - assignee, created_by, created_at, updated_at (WorkItem)
    - parent_id, tags, custom_fields (WorkItem)
    - effort, acceptance_criteria, due_date (DeliveryItem)

  specific:
    timebox:
      type: duration
      required: true
      immutable: false
      constraints:
        min: 1
        max: 336  # 2 weeks in hours
        unit: hours
      description: "Maximum allowed duration"

    findings:
      type: richtext
      required: false
      immutable: false
      constraints:
        maxLength: 20000
      description: "Research findings and conclusions"

    recommendation:
      type: richtext
      required: false
      immutable: false
      constraints:
        maxLength: 10000
      description: "Recommended next steps based on findings"

    research_question:
      type: string
      required: false
      immutable: false
      constraints:
        maxLength: 500
      description: "The question the spike aims to answer"

containment:
  allowed_children: []  # Leaf node (research output)
  allowed_parents: [Feature, Story]
  max_depth: 0

system_mapping:
  ADO: "Task (with 'spike' tag)"
  SAFe: "Enabler Story (Exploration type)"
  JIRA: "Task (with 'spike' label)"

state_machine:
  initial: BACKLOG
  valid_states: [BACKLOG, IN_PROGRESS, DONE, REMOVED]
  transitions:
    BACKLOG: [IN_PROGRESS, REMOVED]
    IN_PROGRESS: [DONE, REMOVED]
    DONE: []  # Cannot reopen - research is done
    REMOVED: []

invariants:
  - "INV-SP01: timebox is required and must be set"
  - "INV-SP02: findings should be documented when DONE"
  - "INV-SP03: Spike cannot have children"
  - "INV-SP04: Spike does NOT require quality gates"

design_rationale: |
  Spike modeled as first-class entity because it has distinct
  behavior: no quality gates required. SAFe formalizes this;
  other systems use labeling conventions.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.1 (Spike row)
  Existing Jerry: WorkType.SPIKE requires_quality_gates = False

jerry_alignment:
  existing_type: "WorkType.SPIKE"
  existing_property: "requires_quality_gates = False"
  changes_needed: "None - already exists with correct semantics"
```

#### 3.4.9 Enabler

```yaml
Entity: Enabler
type: concrete
extends: DeliveryItem
work_type: ENABLER
optional: false
description: |
  Technical/infrastructure work that enables future value delivery.
  SAFe concept for architectural runway, tech debt, etc.

properties:
  inherited:
    - id, work_type, title, description (WorkItem)
    - classification, status, resolution, priority (WorkItem)
    - assignee, created_by, created_at, updated_at (WorkItem)
    - parent_id, tags, custom_fields (WorkItem)
    - effort, acceptance_criteria, due_date (DeliveryItem)

  specific:
    enabler_type:
      type: EnablerType (enum)
      required: true
      immutable: false
      values: [INFRASTRUCTURE, EXPLORATION, ARCHITECTURE, COMPLIANCE]
      description: "Category of enabler work"
      source: [SAFe:enabler_type]

    nfrs:
      type: string[]
      required: false
      immutable: false
      constraints:
        maxItems: 20
        itemMaxLength: 200
      description: "Non-functional requirements addressed"
      source: [SAFe:nfrs]

    technical_debt_category:
      type: string
      required: false
      immutable: false
      constraints:
        maxLength: 100
      description: "Category of tech debt being addressed"

containment:
  allowed_children: [Task]
  allowed_parents: [Feature, Epic]
  max_depth: 1

system_mapping:
  ADO: "PBI with ValueArea=Architectural"
  SAFe: "Enabler (all types)"
  JIRA: "Story with 'enabler' label"

state_machine:
  initial: BACKLOG
  valid_states: [BACKLOG, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, DONE, REMOVED]
  transitions:
    BACKLOG: [READY, REMOVED]
    READY: [IN_PROGRESS, BACKLOG, REMOVED]
    IN_PROGRESS: [BLOCKED, IN_REVIEW, DONE, REMOVED]
    BLOCKED: [IN_PROGRESS, REMOVED]
    IN_REVIEW: [DONE, IN_PROGRESS]
    DONE: [IN_PROGRESS]  # Reopen
    REMOVED: []

invariants:
  - All DeliveryItem invariants
  - "INV-EN01: enabler_type is required"
  - "INV-EN02: classification should be ENABLER"
  - "INV-EN03: Enabler can have Feature or Epic as parent"

design_rationale: |
  Enabler is SAFe's formal construct for non-feature work.
  ADO approximates via ValueArea. JIRA uses labeling.
  Modeled as first-class for SAFe compatibility.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 6.1 (Recommendation 3)

jerry_alignment:
  existing_type: "None"
  changes_needed: "Add ENABLER to WorkType enum"
```

#### 3.4.10 Bug

```yaml
Entity: Bug
type: concrete
extends: QualityItem
work_type: BUG
optional: false
description: |
  Defect or problem requiring fix. First-class entity present
  in all three systems. Can exist at any hierarchy level.

properties:
  inherited:
    - id, work_type, title, description (WorkItem)
    - classification, status, resolution, priority (WorkItem)
    - assignee, created_by, created_at, updated_at (WorkItem)
    - parent_id, tags, custom_fields (WorkItem)
    - severity, found_in_version, fix_version (QualityItem)

  specific:
    reproduction_steps:
      type: richtext
      required: false
      immutable: false
      constraints:
        maxLength: 20000
      description: "Steps to reproduce the issue"
      source: [ADO:ReproSteps]

    environment:
      type: richtext
      required: false
      immutable: false
      constraints:
        maxLength: 5000
      description: "Environment where bug occurs"
      source: [JIRA:environment]

    root_cause:
      type: richtext
      required: false
      immutable: false
      constraints:
        maxLength: 10000
      description: "Root cause analysis"

    effort:
      type: number
      required: false
      immutable: false
      constraints:
        min: 0
        max: 100
      description: "Effort estimate for fix"

    acceptance_criteria:
      type: richtext
      required: false
      immutable: false
      constraints:
        maxLength: 10000
      description: "Conditions for bug to be considered fixed"

containment:
  allowed_children: [Task]
  allowed_parents: [Feature, Story, Epic]
  max_depth: 1

system_mapping:
  ADO: "Bug"
  SAFe: "Defect (uses 'Defect' terminology)"
  JIRA: "Bug"

state_machine:
  initial: BACKLOG
  valid_states: [BACKLOG, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, DONE, REMOVED]
  transitions:
    BACKLOG: [READY, REMOVED]
    READY: [IN_PROGRESS, BACKLOG, REMOVED]
    IN_PROGRESS: [BLOCKED, IN_REVIEW, DONE, REMOVED]
    BLOCKED: [IN_PROGRESS, REMOVED]
    IN_REVIEW: [DONE, IN_PROGRESS]
    DONE: [IN_PROGRESS]  # Reopen (regression)
    REMOVED: []

invariants:
  - All QualityItem invariants
  - "INV-BG01: Bug can have Feature, Story, or Epic as parent"
  - "INV-BG02: reproduction_steps should be provided for non-TRIVIAL severity"
  - "INV-BG03: root_cause should be documented when DONE"

design_rationale: |
  "Bug" preferred over "Defect" because it is used by 2/3 systems
  and is more common in developer vernacular.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.2 (Canonical Name Rationale)

jerry_alignment:
  existing_type: "WorkType.BUG"
  changes_needed: "None - already exists"
```

#### 3.4.11 Impediment

```yaml
Entity: Impediment
type: concrete
extends: FlowControlItem
work_type: IMPEDIMENT
optional: false
description: |
  Blocker preventing progress on one or more work items.
  Explicit entity in ADO; other systems use blocking links.
  Valuable for visibility and tracking resolution time.

properties:
  inherited:
    - id, work_type, title, description (WorkItem)
    - classification, status, resolution, priority (WorkItem)
    - assignee, created_by, created_at, updated_at (WorkItem)
    - parent_id, tags, custom_fields (WorkItem)
    - blocked_items, impact, resolution_notes (FlowControlItem)

  specific:
    owner:
      type: User
      required: false
      immutable: false
      description: "Person responsible for resolution (may differ from assignee)"

    escalation_level:
      type: number
      required: false
      immutable: false
      constraints:
        min: 0
        max: 3
      default: 0
      description: "Escalation level (0=none, 1=manager, 2=director, 3=executive)"

    time_blocked:
      type: duration
      required: false
      immutable: false
      constraints:
        min: 0
        unit: hours
      description: "Total time items have been blocked"
      auto: true  # Calculated from status history

    external_dependency:
      type: string
      required: false
      immutable: false
      constraints:
        maxLength: 500
      description: "External team/vendor dependency if applicable"

containment:
  allowed_children: []  # Impediments don't contain work
  allowed_parents: []   # Standalone entity
  max_depth: 0

relationships:
  blocks:
    type: WorkItemId[]
    required: true
    description: "Work items blocked by this impediment"
    cardinality: "1:N"

system_mapping:
  ADO: "Impediment"
  SAFe: "(blocking links, not explicit entity)"
  JIRA: "(blocking links, not explicit entity)"

state_machine:
  initial: BACKLOG
  valid_states: [BACKLOG, IN_PROGRESS, DONE, REMOVED]
  transitions:
    BACKLOG: [IN_PROGRESS, REMOVED]
    IN_PROGRESS: [DONE, REMOVED]
    DONE: []  # Cannot reopen
    REMOVED: []
  note: "Simplified state machine for impediments"

invariants:
  - All FlowControlItem invariants
  - "INV-IM01: blocked_items must contain at least one item"
  - "INV-IM02: resolution_notes must be set when status is DONE"
  - "INV-IM03: blocked items' BLOCKED status should be cleared when DONE"
  - "INV-IM04: Impediment cannot have parent (standalone)"
  - "INV-IM05: Impediment cannot have children"

design_rationale: |
  Impediment modeled as first-class entity despite SAFe/JIRA
  using links. Explicit tracking enables better visibility,
  metrics, and resolution workflows. When importing from SAFe/JIRA,
  synthetic Impediments can be created from blocking relationships.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 2.1, Section 6.4 (Gap Mitigation)

jerry_alignment:
  existing_type: "None"
  changes_needed: "Add IMPEDIMENT to WorkType enum"
```

---

### 3.5 Enumeration Schemas

#### 3.5.1 WorkType Enum

```yaml
Enumeration: WorkType
description: "Discriminator for concrete work item types"
values:
  # Strategic Items
  - INITIATIVE: "Portfolio-level strategic theme"
  - EPIC: "Large initiative spanning months"
  - CAPABILITY: "SAFe solution-level construct (optional)"
  - FEATURE: "Program-level functionality"

  # Delivery Items
  - STORY: "User-valuable increment"
  - TASK: "Specific work unit"
  - SUBTASK: "Atomic indivisible work"
  - SPIKE: "Timeboxed research"
  - ENABLER: "Technical/infrastructure work"

  # Quality Items
  - BUG: "Defect requiring fix"

  # Flow Control Items
  - IMPEDIMENT: "Blocker requiring resolution"

jerry_alignment:
  existing_values: [EPIC, STORY, TASK, SUBTASK, BUG, SPIKE]
  new_values: [INITIATIVE, CAPABILITY, FEATURE, ENABLER, IMPEDIMENT]
```

#### 3.5.2 WorkItemStatus Enum

```yaml
Enumeration: WorkItemStatus
description: "Work item lifecycle states"
values:
  - BACKLOG: "Created but not ready for work"
  - READY: "Refined and ready to start"
  - IN_PROGRESS: "Actively being worked on"
  - BLOCKED: "Cannot proceed due to impediment"
  - IN_REVIEW: "Awaiting review or verification"
  - DONE: "Successfully completed"
  - REMOVED: "Cancelled or obsolete"

category_mapping:
  Proposed: [BACKLOG, READY]
  InProgress: [IN_PROGRESS, BLOCKED, IN_REVIEW]
  Completed: [DONE]
  Removed: [REMOVED]

jerry_alignment:
  existing_values: [PENDING, IN_PROGRESS, BLOCKED, DONE, CANCELLED]
  mapping:
    PENDING: BACKLOG
    CANCELLED: REMOVED
  new_values: [READY, IN_REVIEW]
```

#### 3.5.3 Other Enumerations

```yaml
Enumeration: WorkClassification
description: "SAFe Business/Enabler classification"
values:
  - BUSINESS: "Delivers direct customer/user value"
  - ENABLER: "Enables future value delivery"
source: [SAFe:type]

---

Enumeration: Priority
description: "Work priority levels"
values:
  - CRITICAL: "Immediate attention required"
  - HIGH: "High priority"
  - MEDIUM: "Normal priority"
  - LOW: "Low priority"

---

Enumeration: Severity
description: "Bug severity levels"
values:
  - CRITICAL: "System unusable, no workaround"
  - MAJOR: "Major functionality affected"
  - MINOR: "Minor functionality affected"
  - TRIVIAL: "Cosmetic or minor issue"
source: [ADO:Severity, JIRA:priority]

---

Enumeration: Resolution
description: "How work item was resolved"
values:
  - DONE: "Work completed successfully"
  - FIXED: "Bug was fixed"
  - WONT_DO: "Decided not to implement"
  - DUPLICATE: "Duplicate of another item"
  - CANNOT_REPRODUCE: "Bug could not be reproduced"
  - OBSOLETE: "No longer relevant"
source: [JIRA:resolution]

---

Enumeration: EnablerType
description: "SAFe enabler categories"
values:
  - INFRASTRUCTURE: "Build development/deployment environments"
  - EXPLORATION: "Spikes, prototypes, research"
  - ARCHITECTURE: "Technical foundation and runway"
  - COMPLIANCE: "Regulatory, security, audit requirements"
source: [SAFe:enabler_type]

---

Enumeration: ImpactLevel
description: "Impediment impact scope"
values:
  - TEAM: "Affects single team"
  - PROGRAM: "Affects multiple teams/ART"
  - PORTFOLIO: "Affects multiple programs"

---

Enumeration: Activity
description: "Task activity types"
values:
  - DEVELOPMENT: "Writing code"
  - TESTING: "Test creation/execution"
  - DOCUMENTATION: "Writing documentation"
  - DESIGN: "Design work"
  - DEPLOYMENT: "Deployment/DevOps"
  - RESEARCH: "Investigation/research"
  - OTHER: "Other activity"
source: [ADO:Activity]

---

Enumeration: ValueArea
description: "ADO value classification"
values:
  - BUSINESS: "Business value delivery"
  - ARCHITECTURAL: "Technical/architectural work"
source: [ADO:ValueArea]
```

---

### 3.6 Schema Validation Summary

#### 3.6.1 Coverage Matrix

| Entity | Extends | Properties Inherited | Properties Specific | State Machine | Invariants |
|--------|---------|---------------------|--------------------|--------------:|------------|
| WorkItem | - | - | 14 | N/A (abstract) | 8 |
| StrategicItem | WorkItem | 14 | 2 | N/A (abstract) | 2 |
| DeliveryItem | WorkItem | 14 | 3 | N/A (abstract) | 2 |
| QualityItem | WorkItem | 14 | 3 | N/A (abstract) | 2 |
| FlowControlItem | WorkItem | 14 | 3 | N/A (abstract) | 3 |
| Initiative | StrategicItem | 16 | 2 | 5 states | 1 |
| Epic | StrategicItem | 16 | 5 | 6 states | 3 |
| Capability | StrategicItem | 16 | 3 | 6 states | 3 |
| Feature | StrategicItem | 16 | 5 | 7 states | 2 |
| Story | DeliveryItem | 17 | 4 | 7 states | 3 |
| Task | DeliveryItem | 17 | 4 | 5 states | 3 |
| Subtask | DeliveryItem | 17 | 1 | 4 states | 2 |
| Spike | DeliveryItem | 17 | 4 | 4 states | 4 |
| Enabler | DeliveryItem | 17 | 3 | 7 states | 3 |
| Bug | QualityItem | 17 | 5 | 7 states | 3 |
| Impediment | FlowControlItem | 17 | 4 | 4 states | 5 |

#### 3.6.2 Gaps for Review

| Gap ID | Description | Impact | Recommendation |
|--------|-------------|--------|----------------|
| GAP-S01 | Version field not modeled | Low | Add if needed for optimistic concurrency |
| GAP-S02 | Comment/history not in schema | Medium | Model as separate entity with relationship |
| GAP-S03 | Attachment support not modeled | Low | Add as extension entity if needed |
| GAP-S04 | Audit trail not explicit | Medium | Consider Event Sourcing pattern |
| GAP-S05 | Sprint/Iteration assignment not explicit | Medium | Add iteration_id to DeliveryItem |

#### 3.6.3 Jerry Codebase Alignment Summary

| Area | Current State | Required Changes |
|------|---------------|------------------|
| WorkType enum | 6 values | Add 5: INITIATIVE, CAPABILITY, FEATURE, ENABLER, IMPEDIMENT |
| WorkItemStatus enum | 5 values | Rename PENDING->BACKLOG, CANCELLED->REMOVED; Add READY, IN_REVIEW |
| WorkItem aggregate | Exists | Extend with new properties |
| Hierarchy enforcement | Partial (valid_parent_types) | Full containment rules per entity |
| State machine | Exists | Extend with entity-specific machines |

---

### 3.7 Validation Checklist (Section 3)

For human reviewer to verify before approval:

- [ ] All entities have complete property definitions
- [ ] Property constraints are appropriate and implementable
- [ ] State machines cover all required transitions
- [ ] Invariants are enforceable in code
- [ ] Inheritance hierarchy is correct
- [ ] Containment rules align with Section 1-2 definitions
- [ ] Jerry codebase alignment is accurate
- [ ] Gaps are documented and acceptable
- [ ] Enumeration values are complete

---

### 3.8 Evidence Traceability (Section 3)

| Schema Element | Source Document | Source Section |
|----------------|-----------------|----------------|
| Core Properties | CROSS-DOMAIN-SYNTHESIS.md | 3.1 Core Properties |
| Extended Properties | CROSS-DOMAIN-SYNTHESIS.md | 3.2 Extended Properties |
| Property Types | CROSS-DOMAIN-SYNTHESIS.md | 3.4 Property Type Mapping |
| Entity Containment | ONTOLOGY-v1.md | Section 2 (from Task 1) |
| State Machines | CROSS-DOMAIN-SYNTHESIS.md | Section 5 State Machine Comparison |
| ADO-specific | CROSS-DOMAIN-SYNTHESIS.md | 3.3 System-Specific (ADO) |
| SAFe-specific | CROSS-DOMAIN-SYNTHESIS.md | 3.3 System-Specific (SAFe) |
| JIRA-specific | CROSS-DOMAIN-SYNTHESIS.md | 3.3 System-Specific (JIRA) |
| Jerry Alignment | work_type.py, work_item_status.py | Existing codebase |

---

*End of Section 3: Entity Schemas*

---

## Section 4: Relationship Types

> **Task:** WI-001 Task 3 - Design relationship types
> **Author:** nse-architecture (Claude Opus 4.5)
> **Date:** 2026-01-13
> **Status:** DRAFT - PENDING HUMAN REVIEW

---

> **DISCLAIMER (P-043):** This section was produced by an AI agent (nse-architecture)
> as part of the Jerry framework's problem-solving workflow. All relationship type
> definitions, constraints, and invariants herein are ADVISORY and require human review
> before implementation. Relationship mappings are traced to CROSS-DOMAIN-SYNTHESIS.md
> Section 4 where possible. Human judgment is the final authority.

---

### 4.1 Relationship Design Principles

The relationship types follow these design principles derived from the cross-domain synthesis:

1. **Semantic Clarity:** Each relationship type has a distinct meaning and use case
2. **Directionality Explicit:** Directional relationships have named forward/reverse variants
3. **Cardinality Constraints:** All relationships define cardinality bounds (1:1, 1:N, N:M)
4. **Cycle Prevention:** Hierarchical and dependency relationships prohibit circular references
5. **Cross-Entity Support:** Relationships can span entity types (Epic to Task, Bug to Story, etc.)
6. **External Artifact Links:** Support for linking to VCS, CI/CD, and documentation systems
7. **Jerry Codebase Alignment:** Extensions build on existing `add_dependency` / `remove_dependency` patterns

**Source Traceability:**
- Relationship categories: CROSS-DOMAIN-SYNTHESIS.md Section 4.1-4.4
- Design principles: CROSS-DOMAIN-SYNTHESIS.md Section 6.1 (Recommendations)
- Jerry alignment: `src/work_tracking/domain/aggregates/work_item.py` (dependency methods)

---

### 4.2 Relationship Type Categories

The ontology defines four categories of relationships:

| Category | Purpose | Topology | Cycles Allowed |
|----------|---------|----------|----------------|
| **Hierarchical** | Parent-child containment | Tree | No |
| **Dependency** | Blocking/sequencing | Directed Graph | No |
| **Association** | Informational linkage | Network | Yes (for symmetric) |
| **External** | Artifact links | Star (entity-centered) | N/A |

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      RELATIONSHIP CATEGORY OVERVIEW                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  HIERARCHICAL (Tree - No Cycles)                                            │
│  ├── parent_of / child_of                                                   │
│  │   Epic ──► Feature ──► Story ──► Task ──► Subtask                       │
│  │                                                                          │
│  DEPENDENCY (Directed Graph - No Cycles)                                    │
│  ├── blocks / blocked_by                                                    │
│  ├── depends_on / dependency_of                                             │
│  │   Story A ──[blocks]──► Story B ──[depends_on]──► Story C               │
│  │                                                                          │
│  ASSOCIATION (Network - Cycles OK for symmetric)                            │
│  ├── relates_to (symmetric)                                                 │
│  ├── duplicates / duplicated_by                                             │
│  ├── clones / cloned_by                                                     │
│  ├── realizes / realized_by                                                 │
│  │                                                                          │
│  EXTERNAL (Star Topology)                                                   │
│  ├── links_to_commit, links_to_branch, links_to_pr                         │
│  ├── links_to_build, links_to_wiki, links_to_url                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 4.3 Hierarchical Relationships Schema

#### 4.3.1 parent_of / child_of

```yaml
Relationship: parent_of
category: hierarchical
direction: forward
inverse: child_of
description: |
  Represents containment hierarchy where a parent work item contains
  or decomposes into child work items. Forms a strict tree structure.

cardinality:
  source: 1  # One parent
  target: N  # Many children
  constraint: "1:N"

cycle_prevention:
  enabled: true
  enforcement: HARD
  violation_error: "CircularHierarchyError"

cross_level_rules:
  allowed: true
  constraints:
    - "Parent must be at a higher hierarchy level than child"
    - "Valid parent types defined per entity schema (containment.allowed_parents)"
    - "Valid child types defined per entity schema (containment.allowed_children)"

cross_project:
  ADO: "Supported via Area Paths"
  SAFe: "Supported within Solution/ART"
  JIRA: "JIRA Premium supports cross-project parenting"
  canonical: "Supported with explicit project reference"

properties:
  source_id:
    type: WorkItemId
    required: true
    description: "Parent work item ID"

  target_id:
    type: WorkItemId
    required: true
    description: "Child work item ID"

  created_at:
    type: datetime
    required: true
    auto: true
    description: "When relationship was established"

  created_by:
    type: User
    required: true
    auto: true
    description: "Who established the relationship"

system_mapping:
  ADO: "System.LinkTypes.Hierarchy-Forward"
  SAFe: "contains"
  JIRA: "Parent field (parent_id property)"

invariants:
  - "INV-R-H01: A work item can have at most one parent"
  - "INV-R-H02: Parent type must be in child's allowed_parents list"
  - "INV-R-H03: Child type must be in parent's allowed_children list"
  - "INV-R-H04: No circular references (A cannot be ancestor of itself)"
  - "INV-R-H05: Parent must exist and not be in REMOVED status"
  - "INV-R-H06: Cross-project links require explicit project reference"

design_rationale: |
  parent_of/child_of forms the backbone of work decomposition. The strict
  tree structure (1 parent max) matches all three source systems. Cross-level
  rules enforce type safety (e.g., Epic cannot be child of Task).
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 4.1 (Hierarchical Relationships)

jerry_alignment:
  existing_property: "parent_id (WorkItem base)"
  existing_method: "None - hierarchy via parent_id property"
  changes_needed: "Add validation for containment rules per entity type"
```

#### 4.3.2 child_of (Inverse)

```yaml
Relationship: child_of
category: hierarchical
direction: reverse
inverse: parent_of
description: |
  Inverse of parent_of. Represents the child's view of the hierarchy.
  Automatically derived from parent_of relationships.

cardinality:
  source: N  # Many children
  target: 1  # One parent
  constraint: "N:1"

note: |
  child_of is typically implicit - set by assigning parent_id on the child.
  Query support should provide both directions for navigation.

system_mapping:
  ADO: "System.LinkTypes.Hierarchy-Reverse"
  SAFe: "child_of"
  JIRA: "(implicit via parent field)"
```

---

### 4.4 Dependency Relationships Schema

#### 4.4.1 blocks / blocked_by

```yaml
Relationship: blocks
category: dependency
direction: forward
inverse: blocked_by
description: |
  Hard dependency where the source work item prevents the target from
  proceeding. The target cannot be completed until the source is resolved.

cardinality:
  source: N  # Many blockers
  target: M  # Many blocked items
  constraint: "N:M"

cycle_prevention:
  enabled: true
  enforcement: HARD
  violation_error: "CircularDependencyError"
  rationale: "Circular blocking would create deadlock"

semantic:
  meaning: "Source prevents target from proceeding"
  workflow_impact: true
  status_effect: "Target should transition to BLOCKED when blocker is active"

cross_level_rules:
  allowed: true
  constraints:
    - "Any work item type can block any other type"
    - "Cross-project blocking supported with explicit reference"

properties:
  source_id:
    type: WorkItemId
    required: true
    description: "Blocking work item ID"

  target_id:
    type: WorkItemId
    required: true
    description: "Blocked work item ID"

  created_at:
    type: datetime
    required: true
    auto: true
    description: "When blocking relationship was established"

  created_by:
    type: User
    required: true
    auto: true
    description: "Who established the blocking relationship"

  reason:
    type: string
    required: false
    constraints:
      maxLength: 500
    description: "Why this item blocks the other"

  blocking_type:
    type: BlockingType (enum)
    required: false
    values: [TECHNICAL, RESOURCE, EXTERNAL, DECISION, OTHER]
    default: TECHNICAL
    description: "Category of blocking reason"

system_mapping:
  ADO: "System.LinkTypes.Dependency-Forward"
  SAFe: "blocks"
  JIRA: "Blocks (outward link)"

invariants:
  - "INV-R-D01: No circular blocking chains (A blocks B blocks A)"
  - "INV-R-D02: Blocking item must exist"
  - "INV-R-D03: Cannot block self"
  - "INV-R-D04: Blocking a REMOVED item has no effect"
  - "INV-R-D05: When blocker completes, blocked items should be notified"

design_rationale: |
  blocks/blocked_by is the core dependency mechanism. All three systems
  support this pattern. Cycle prevention is critical to avoid deadlocks.
  The relationship has workflow impact - blocked items should show BLOCKED status.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 4.2 (Dependency Relationships)

jerry_alignment:
  existing_method: "add_dependency(dependency_id, dependency_type='blocks')"
  existing_property: "_dependencies: list[str]"
  changes_needed: "Extend to support full relationship metadata (reason, blocking_type)"
```

#### 4.4.2 blocked_by (Inverse)

```yaml
Relationship: blocked_by
category: dependency
direction: reverse
inverse: blocks
description: |
  Inverse of blocks. Target cannot proceed until source resolves.
  Represents the blocked item's perspective on the dependency.

cardinality:
  source: M  # Many blocked items
  target: N  # Many blockers
  constraint: "M:N"

system_mapping:
  ADO: "System.LinkTypes.Dependency-Reverse"
  SAFe: "blocked_by"
  JIRA: "is blocked by (inward link)"

note: |
  blocked_by is the reverse query of blocks. When item A blocks item B,
  querying B's blocked_by returns A.
```

#### 4.4.3 depends_on / dependency_of

```yaml
Relationship: depends_on
category: dependency
direction: forward
inverse: dependency_of
description: |
  Soft dependency indicating the target benefits from the source being
  completed first, but can proceed independently if necessary.

cardinality:
  source: N  # Many dependencies
  target: M  # Many dependents
  constraint: "N:M"

cycle_prevention:
  enabled: true
  enforcement: SOFT
  violation_warning: "Circular dependency detected - review recommended"
  rationale: "Soft dependencies may form cycles in complex projects"

semantic:
  meaning: "Target benefits from source completion but can proceed"
  workflow_impact: false
  status_effect: "None - informational only"

distinction_from_blocks: |
  - blocks: Hard stop - target CANNOT proceed
  - depends_on: Soft preference - target SHOULD wait but can proceed

properties:
  source_id:
    type: WorkItemId
    required: true
    description: "Dependency (item being depended on)"

  target_id:
    type: WorkItemId
    required: true
    description: "Dependent (item that depends on source)"

  created_at:
    type: datetime
    required: true
    auto: true

  created_by:
    type: User
    required: true
    auto: true

  strength:
    type: DependencyStrength (enum)
    required: false
    values: [STRONG, MEDIUM, WEAK]
    default: MEDIUM
    description: "How strongly the dependency affects planning"

  notes:
    type: string
    required: false
    constraints:
      maxLength: 500
    description: "Additional context about the dependency"

system_mapping:
  ADO: "System.LinkTypes.Dependency-Forward (with metadata)"
  SAFe: "depends_on"
  JIRA: "Blocks (semantic distinction via metadata)"

invariants:
  - "INV-R-D06: Soft dependency cycles trigger warning, not error"
  - "INV-R-D07: Cannot depend on self"
  - "INV-R-D08: Dependency on REMOVED item should be flagged"

design_rationale: |
  depends_on provides softer sequencing than blocks. It supports planning
  and prioritization without enforcing hard workflow constraints. SAFe
  distinguishes this from blocks; other systems use metadata to differentiate.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 4.2 (Semantic Distinction)

jerry_alignment:
  existing_method: "add_dependency(dependency_id, dependency_type='depends_on')"
  changes_needed: "Add strength property; implement soft cycle detection"
```

#### 4.4.4 dependency_of (Inverse)

```yaml
Relationship: dependency_of
category: dependency
direction: reverse
inverse: depends_on
description: |
  Inverse of depends_on. Shows what items depend on the source.

cardinality:
  source: M
  target: N
  constraint: "M:N"

system_mapping:
  ADO: "System.LinkTypes.Dependency-Reverse"
  SAFe: "dependency_of"
  JIRA: "(reverse query of Blocks)"
```

---

### 4.5 Association Relationships Schema

#### 4.5.1 relates_to (Symmetric)

```yaml
Relationship: relates_to
category: association
direction: bidirectional
inverse: relates_to  # Self-inverse (symmetric)
description: |
  Generic association between related work items without directional
  semantics. Used for cross-referencing and knowledge linking.

cardinality:
  source: N
  target: M
  constraint: "N:M"

cycle_prevention:
  enabled: false
  rationale: "Symmetric association naturally forms networks with cycles"

semantic:
  meaning: "Items are related for reference purposes"
  workflow_impact: false
  status_effect: "None - informational only"

properties:
  source_id:
    type: WorkItemId
    required: true

  target_id:
    type: WorkItemId
    required: true

  created_at:
    type: datetime
    required: true
    auto: true

  created_by:
    type: User
    required: true
    auto: true

  context:
    type: string
    required: false
    constraints:
      maxLength: 500
    description: "Why these items are related"

  relationship_strength:
    type: RelationshipStrength (enum)
    required: false
    values: [STRONG, MODERATE, WEAK]
    default: MODERATE
    description: "How closely related the items are"

system_mapping:
  ADO: "System.LinkTypes.Related"
  SAFe: "related_to"
  JIRA: "Relates (link type)"

invariants:
  - "INV-R-A01: relates_to(A,B) implies relates_to(B,A)"
  - "INV-R-A02: Cannot relate item to itself"
  - "INV-R-A03: Duplicate relates_to links are merged"

design_rationale: |
  relates_to is the catch-all for general associations. It's symmetric
  (bidirectional) and has no workflow impact. All three systems support
  this as a basic link type.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 4.3 (Association Relationships)

jerry_alignment:
  existing_method: "add_dependency(dependency_id, dependency_type='related')"
  changes_needed: "Add symmetric link storage; context property"
```

#### 4.5.2 duplicates / duplicated_by

```yaml
Relationship: duplicates
category: association
direction: forward
inverse: duplicated_by
description: |
  Indicates the source item duplicates the target item.
  The source (duplicate) is typically closed in favor of the target (original).

cardinality:
  source: N  # Many duplicates
  target: 1  # One original (typically)
  constraint: "N:1 (recommended)"

cycle_prevention:
  enabled: true
  enforcement: SOFT
  rationale: "A duplicating B duplicating A would be nonsensical"

semantic:
  meaning: "Source is a duplicate of target (target is the original)"
  workflow_impact: true
  status_effect: "Source typically transitions to REMOVED with resolution=DUPLICATE"

properties:
  source_id:
    type: WorkItemId
    required: true
    description: "The duplicate item"

  target_id:
    type: WorkItemId
    required: true
    description: "The original item"

  created_at:
    type: datetime
    required: true
    auto: true

  created_by:
    type: User
    required: true
    auto: true

  confidence:
    type: DuplicateConfidence (enum)
    required: false
    values: [EXACT, LIKELY, POSSIBLE]
    default: LIKELY
    description: "Confidence that items are true duplicates"

system_mapping:
  ADO: "System.LinkTypes.Duplicate-Forward"
  SAFe: "(not explicit - use relates_to)"
  JIRA: "Duplicates (outward link)"

invariants:
  - "INV-R-A04: Duplicate should be marked REMOVED with resolution=DUPLICATE"
  - "INV-R-A05: Original should not be REMOVED when duplicate links exist"
  - "INV-R-A06: Cannot mark item as duplicate of itself"

design_rationale: |
  duplicates is directional - source is the duplicate, target is the original.
  This matters for resolution workflows where the duplicate gets closed.
  SAFe doesn't formalize this but the pattern is universal.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 4.3

jerry_alignment:
  existing_method: "None"
  changes_needed: "Add duplicates relationship type with workflow integration"
```

#### 4.5.3 duplicated_by (Inverse)

```yaml
Relationship: duplicated_by
category: association
direction: reverse
inverse: duplicates
description: |
  Inverse of duplicates. Shows what items are duplicates of the source.

cardinality:
  source: 1  # One original
  target: N  # Many duplicates
  constraint: "1:N"

system_mapping:
  ADO: "System.LinkTypes.Duplicate-Reverse"
  SAFe: "(not explicit)"
  JIRA: "is duplicated by (inward link)"
```

#### 4.5.4 clones / cloned_by

```yaml
Relationship: clones
category: association
direction: forward
inverse: cloned_by
description: |
  Indicates the source item was cloned from the target item.
  Used for tracking item lineage when copying work items.

cardinality:
  source: 1  # One clone
  target: 1  # One original
  constraint: "1:1"

cycle_prevention:
  enabled: true
  enforcement: HARD
  rationale: "Clone relationships form a directed acyclic graph (lineage)"

semantic:
  meaning: "Source was created by cloning target"
  workflow_impact: false
  status_effect: "None - informational only"

properties:
  source_id:
    type: WorkItemId
    required: true
    description: "The cloned item"

  target_id:
    type: WorkItemId
    required: true
    description: "The original item"

  created_at:
    type: datetime
    required: true
    auto: true

  cloned_fields:
    type: string[]
    required: false
    description: "Which fields were copied during clone"

system_mapping:
  ADO: "(Copy operation - tracked in history)"
  SAFe: "(not explicit)"
  JIRA: "Clones (link type)"

invariants:
  - "INV-R-A07: Clone source must have been created after target"
  - "INV-R-A08: Cannot clone self"

design_rationale: |
  clones is JIRA-specific but useful for tracking item lineage.
  ADO/SAFe don't formalize this but the concept applies when copying items.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 4.3

jerry_alignment:
  existing_method: "None"
  changes_needed: "Add clones relationship type for lineage tracking"
```

#### 4.5.5 cloned_by (Inverse)

```yaml
Relationship: cloned_by
category: association
direction: reverse
inverse: clones
description: |
  Inverse of clones. Shows what items were cloned from the source.

cardinality:
  source: 1
  target: N
  constraint: "1:N"

system_mapping:
  ADO: "(not explicit)"
  SAFe: "(not explicit)"
  JIRA: "is cloned by (inward link)"
```

#### 4.5.6 realizes / realized_by

```yaml
Relationship: realizes
category: association
direction: forward
inverse: realized_by
description: |
  SAFe-specific relationship indicating a lower-level item realizes
  (implements) a higher-level item. Used for traceability from
  Stories to Capabilities/Features.

cardinality:
  source: N  # Many realizing items
  target: M  # Many realized items
  constraint: "N:M"

cycle_prevention:
  enabled: true
  enforcement: SOFT

semantic:
  meaning: "Source implements/realizes the target"
  workflow_impact: false
  status_effect: "None - traceability only"

applicability:
  - "Story realizes Feature"
  - "Feature realizes Capability"
  - "Capability realizes Epic"

properties:
  source_id:
    type: WorkItemId
    required: true
    description: "The realizing (implementing) item"

  target_id:
    type: WorkItemId
    required: true
    description: "The realized (specified) item"

  created_at:
    type: datetime
    required: true
    auto: true

  coverage_percent:
    type: number
    required: false
    constraints:
      min: 0
      max: 100
    description: "Percentage of target realized by source"

system_mapping:
  ADO: "(use parent_of or custom link)"
  SAFe: "realizes"
  JIRA: "(use relates_to or custom link)"

invariants:
  - "INV-R-A09: Source should be at same or lower level than target"
  - "INV-R-A10: Cannot realize self"

design_rationale: |
  realizes is SAFe-specific for requirements traceability. It differs
  from parent_of because it tracks specification-to-implementation
  rather than decomposition. Other systems can use relates_to or
  custom link types.
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 4.3

jerry_alignment:
  existing_method: "None"
  changes_needed: "Add realizes relationship type for SAFe compatibility"
```

#### 4.5.7 realized_by (Inverse)

```yaml
Relationship: realized_by
category: association
direction: reverse
inverse: realizes
description: |
  Inverse of realizes. Shows what items implement/realize the source.

cardinality:
  source: M
  target: N
  constraint: "M:N"

system_mapping:
  ADO: "(not explicit)"
  SAFe: "realized_by"
  JIRA: "(not explicit)"
```

---

### 4.6 External Relationships Schema

#### 4.6.1 links_to_commit

```yaml
Relationship: links_to_commit
category: external
direction: forward
inverse: null  # External - no inverse
description: |
  Links a work item to a VCS commit. Used for tracking which commits
  relate to which work items.

target_type: VCS Commit (external artifact)

cardinality:
  source: N  # Many work items
  target: M  # Many commits
  constraint: "N:M"

properties:
  source_id:
    type: WorkItemId
    required: true
    description: "The work item"

  commit_id:
    type: string
    required: true
    constraints:
      pattern: "^[a-f0-9]{40}$"  # SHA-1 or SHA-256
    description: "Git commit SHA"

  repository:
    type: string
    required: true
    constraints:
      maxLength: 500
    description: "Repository identifier (org/repo or URL)"

  created_at:
    type: datetime
    required: true
    auto: true

  commit_message:
    type: string
    required: false
    constraints:
      maxLength: 1000
    description: "First line of commit message (cached)"

  commit_author:
    type: string
    required: false
    description: "Commit author (cached)"

system_mapping:
  ADO: "Git Commit artifact link"
  SAFe: "(external integration)"
  JIRA: "Development panel - Commits"

invariants:
  - "INV-R-E01: Commit ID must be valid SHA format"
  - "INV-R-E02: Repository must be accessible"

design_rationale: |
  Commit links provide development traceability. All three systems
  support this via different mechanisms (ADO artifacts, JIRA development panel).
  Trace: CROSS-DOMAIN-SYNTHESIS.md Section 4.4

jerry_alignment:
  existing_method: "None"
  changes_needed: "Add external artifact link support"
```

#### 4.6.2 links_to_branch

```yaml
Relationship: links_to_branch
category: external
direction: forward
inverse: null
description: |
  Links a work item to a VCS branch. Used for tracking feature branches.

target_type: VCS Branch (external artifact)

cardinality:
  source: N
  target: M
  constraint: "N:M"

properties:
  source_id:
    type: WorkItemId
    required: true

  branch_name:
    type: string
    required: true
    constraints:
      maxLength: 255
    description: "Branch name (e.g., 'feature/WORK-123-login')"

  repository:
    type: string
    required: true

  created_at:
    type: datetime
    required: true
    auto: true

  branch_status:
    type: BranchStatus (enum)
    required: false
    values: [ACTIVE, MERGED, DELETED]
    default: ACTIVE

system_mapping:
  ADO: "Git Branch artifact link"
  SAFe: "(external integration)"
  JIRA: "Development panel - Branches"

invariants:
  - "INV-R-E03: Branch name should follow naming convention if configured"
```

#### 4.6.3 links_to_pr

```yaml
Relationship: links_to_pr
category: external
direction: forward
inverse: null
description: |
  Links a work item to a pull request / merge request.

target_type: Pull Request (external artifact)

cardinality:
  source: N
  target: M
  constraint: "N:M"

properties:
  source_id:
    type: WorkItemId
    required: true

  pr_id:
    type: string
    required: true
    description: "Pull request ID or number"

  pr_url:
    type: string
    required: true
    constraints:
      format: uri
    description: "Full URL to the pull request"

  repository:
    type: string
    required: true

  created_at:
    type: datetime
    required: true
    auto: true

  pr_status:
    type: PRStatus (enum)
    required: false
    values: [OPEN, MERGED, CLOSED, DRAFT]
    default: OPEN

  pr_title:
    type: string
    required: false
    constraints:
      maxLength: 500
    description: "PR title (cached)"

system_mapping:
  ADO: "Pull Request artifact link"
  SAFe: "(external integration)"
  JIRA: "Development panel - Pull Requests"

invariants:
  - "INV-R-E04: PR URL must be valid URI format"
  - "INV-R-E05: Work item typically transitions when PR merges"
```

#### 4.6.4 links_to_build

```yaml
Relationship: links_to_build
category: external
direction: forward
inverse: null
description: |
  Links a work item to a CI/CD build or pipeline run.

target_type: Build/Pipeline (external artifact)

cardinality:
  source: N
  target: M
  constraint: "N:M"

properties:
  source_id:
    type: WorkItemId
    required: true

  build_id:
    type: string
    required: true
    description: "Build number or pipeline run ID"

  build_url:
    type: string
    required: true
    constraints:
      format: uri
    description: "URL to the build result"

  pipeline_name:
    type: string
    required: false
    constraints:
      maxLength: 200
    description: "Name of the pipeline"

  created_at:
    type: datetime
    required: true
    auto: true

  build_status:
    type: BuildStatus (enum)
    required: false
    values: [RUNNING, SUCCEEDED, FAILED, CANCELLED]

system_mapping:
  ADO: "Build artifact link"
  SAFe: "(external integration)"
  JIRA: "CI/CD integration"

invariants:
  - "INV-R-E06: Build URL must be valid URI format"
```

#### 4.6.5 links_to_wiki

```yaml
Relationship: links_to_wiki
category: external
direction: forward
inverse: null
description: |
  Links a work item to documentation in a wiki or knowledge base.

target_type: Documentation (external artifact)

cardinality:
  source: N
  target: M
  constraint: "N:M"

properties:
  source_id:
    type: WorkItemId
    required: true

  wiki_url:
    type: string
    required: true
    constraints:
      format: uri
    description: "URL to the wiki page"

  wiki_title:
    type: string
    required: false
    constraints:
      maxLength: 500
    description: "Title of the wiki page (cached)"

  wiki_type:
    type: WikiType (enum)
    required: false
    values: [ADO_WIKI, CONFLUENCE, NOTION, GITHUB_WIKI, OTHER]
    default: OTHER

  created_at:
    type: datetime
    required: true
    auto: true

system_mapping:
  ADO: "Wiki Page artifact link"
  SAFe: "(external documentation)"
  JIRA: "Confluence integration"

invariants:
  - "INV-R-E07: Wiki URL must be valid URI format"
```

#### 4.6.6 links_to_url

```yaml
Relationship: links_to_url
category: external
direction: forward
inverse: null
description: |
  Generic hyperlink to any external resource.

target_type: External URL (any)

cardinality:
  source: N
  target: M
  constraint: "N:M"

properties:
  source_id:
    type: WorkItemId
    required: true

  url:
    type: string
    required: true
    constraints:
      format: uri
    description: "External URL"

  title:
    type: string
    required: false
    constraints:
      maxLength: 500
    description: "Display title for the link"

  link_category:
    type: string
    required: false
    constraints:
      maxLength: 100
    description: "Category for grouping links (e.g., 'Design', 'Reference')"

  created_at:
    type: datetime
    required: true
    auto: true

system_mapping:
  ADO: "Hyperlink artifact"
  SAFe: "(external link)"
  JIRA: "Web Link"

invariants:
  - "INV-R-E08: URL must be valid URI format"
```

---

### 4.7 Relationship Constraint Rules

#### 4.7.1 Global Invariants

```yaml
GlobalInvariants:
  description: "Constraints that apply to all relationship types"

  invariants:
    - id: INV-R-G01
      rule: "A relationship cannot reference a non-existent work item"
      enforcement: HARD
      error: "InvalidReferenceError"

    - id: INV-R-G02
      rule: "Relationships to REMOVED items should be flagged or cleaned up"
      enforcement: SOFT
      warning: "RelationshipToRemovedItemWarning"

    - id: INV-R-G03
      rule: "Relationship metadata (created_at, created_by) is immutable"
      enforcement: HARD

    - id: INV-R-G04
      rule: "Only the owner or admin can delete relationships"
      enforcement: HARD

    - id: INV-R-G05
      rule: "Cross-project relationships require appropriate permissions"
      enforcement: HARD
```

#### 4.7.2 Cycle Detection Algorithm

```yaml
CycleDetection:
  description: "Algorithm for detecting cycles in directed relationships"

  applies_to:
    - parent_of / child_of (HARD enforcement)
    - blocks / blocked_by (HARD enforcement)
    - depends_on / dependency_of (SOFT enforcement)
    - duplicates / duplicated_by (SOFT enforcement)
    - clones / cloned_by (HARD enforcement)

  algorithm: |
    1. For HARD enforcement: Use DFS from source, reject if target is reachable
    2. For SOFT enforcement: Use DFS, warn but allow if cycle detected
    3. Cache traversal results for performance

  pseudocode: |
    function detectCycle(source, target, relationshipType):
      visited = Set()
      return dfs(target, source, visited, relationshipType)

    function dfs(current, target, visited, type):
      if current == target:
        return true  # Cycle found
      if current in visited:
        return false  # Already checked this path
      visited.add(current)
      for related in getRelated(current, type):
        if dfs(related, target, visited, type):
          return true
      return false

  enforcement_matrix:
    parent_of: REJECT
    blocks: REJECT
    depends_on: WARN
    duplicates: WARN
    clones: REJECT
    realizes: WARN
    relates_to: ALLOW  # Symmetric - cycles natural
```

#### 4.7.3 Relationship Count Limits

```yaml
RelationshipLimits:
  description: "Soft limits on relationship counts for performance/usability"

  limits:
    parent_of:
      max_children_per_parent: 100
      warning_threshold: 50
      rationale: "Large decompositions become unwieldy"

    blocks:
      max_blockers_per_item: 20
      max_blocked_per_item: 50
      rationale: "Too many blockers indicates scope issues"

    depends_on:
      max_dependencies_per_item: 30
      rationale: "High dependency count suggests poor decomposition"

    relates_to:
      max_per_item: 50
      rationale: "Too many relations dilutes meaning"

    external_links:
      max_per_item: 100
      rationale: "Practical limit for UI display"

  enforcement: SOFT
  action: "Warning to user; does not prevent creation"
```

---

### 4.8 Relationship Mapping Summary

#### 4.8.1 System Mapping Table

| Canonical | ADO Link Type | SAFe Relationship | JIRA Link Type | Direction |
|-----------|---------------|-------------------|----------------|-----------|
| `parent_of` | `System.LinkTypes.Hierarchy-Forward` | `contains` | `Parent` field | Forward |
| `child_of` | `System.LinkTypes.Hierarchy-Reverse` | `child_of` | (implicit) | Reverse |
| `blocks` | `System.LinkTypes.Dependency-Forward` | `blocks` | `Blocks` | Forward |
| `blocked_by` | `System.LinkTypes.Dependency-Reverse` | `blocked_by` | `is blocked by` | Reverse |
| `depends_on` | `System.LinkTypes.Dependency-Forward` | `depends_on` | `Blocks` (metadata) | Forward |
| `dependency_of` | `System.LinkTypes.Dependency-Reverse` | `dependency_of` | (reverse query) | Reverse |
| `relates_to` | `System.LinkTypes.Related` | `related_to` | `Relates` | Bidirectional |
| `duplicates` | `System.LinkTypes.Duplicate-Forward` | (use relates_to) | `Duplicates` | Forward |
| `duplicated_by` | `System.LinkTypes.Duplicate-Reverse` | (use relates_to) | `is duplicated by` | Reverse |
| `clones` | (history tracking) | (not explicit) | `Clones` | Forward |
| `cloned_by` | (history tracking) | (not explicit) | `is cloned by` | Reverse |
| `realizes` | (custom or parent) | `realizes` | (custom link) | Forward |
| `realized_by` | (custom or parent) | `realized_by` | (custom link) | Reverse |
| `links_to_commit` | Git Commit artifact | (external) | Development panel | Forward |
| `links_to_branch` | Git Branch artifact | (external) | Development panel | Forward |
| `links_to_pr` | Pull Request artifact | (external) | Development panel | Forward |
| `links_to_build` | Build artifact | (external) | CI/CD integration | Forward |
| `links_to_wiki` | Wiki Page artifact | (external) | Confluence | Forward |
| `links_to_url` | Hyperlink | (external) | Web Link | Forward |

#### 4.8.2 Mapping Complexity by Direction

| Direction | Complexity | Notes |
|-----------|------------|-------|
| Canonical to ADO | Low | Direct mapping for most types |
| Canonical to SAFe | Medium | realizes needs SAFe-specific handling |
| Canonical to JIRA | Low | Direct mapping; duplicates/clones native |
| ADO to Canonical | Low | Link types map cleanly |
| SAFe to Canonical | Medium | realizes relationship is SAFe-specific |
| JIRA to Canonical | Low | Native link types align well |

**Source:** CROSS-DOMAIN-SYNTHESIS.md Section 4.5, Section 6.2

---

### 4.9 Relationship Enumeration Schemas

#### 4.9.1 Relationship Type Enums

```yaml
Enumeration: RelationshipType
description: "All canonical relationship types"
values:
  # Hierarchical
  - PARENT_OF: "Parent contains child"
  - CHILD_OF: "Child belongs to parent"

  # Dependency
  - BLOCKS: "Source blocks target (hard)"
  - BLOCKED_BY: "Source is blocked by target"
  - DEPENDS_ON: "Source depends on target (soft)"
  - DEPENDENCY_OF: "Source is dependency of target"

  # Association
  - RELATES_TO: "Generic association (symmetric)"
  - DUPLICATES: "Source duplicates target"
  - DUPLICATED_BY: "Source is duplicated by target"
  - CLONES: "Source cloned from target"
  - CLONED_BY: "Source is cloned by target"
  - REALIZES: "Source realizes/implements target"
  - REALIZED_BY: "Source is realized by target"

  # External
  - LINKS_TO_COMMIT: "Link to VCS commit"
  - LINKS_TO_BRANCH: "Link to VCS branch"
  - LINKS_TO_PR: "Link to pull request"
  - LINKS_TO_BUILD: "Link to CI/CD build"
  - LINKS_TO_WIKI: "Link to wiki page"
  - LINKS_TO_URL: "Link to external URL"

---

Enumeration: RelationshipCategory
description: "Categories of relationships"
values:
  - HIERARCHICAL: "Parent-child containment"
  - DEPENDENCY: "Blocking/sequencing"
  - ASSOCIATION: "Informational linkage"
  - EXTERNAL: "Artifact links"

---

Enumeration: BlockingType
description: "Categories of blocking reasons"
values:
  - TECHNICAL: "Technical dependency or blocker"
  - RESOURCE: "Resource availability issue"
  - EXTERNAL: "External dependency (vendor, other team)"
  - DECISION: "Awaiting decision or approval"
  - OTHER: "Other blocking reason"

---

Enumeration: DependencyStrength
description: "Strength of soft dependencies"
values:
  - STRONG: "Should definitely wait"
  - MEDIUM: "Waiting recommended"
  - WEAK: "Minor benefit to waiting"

---

Enumeration: DuplicateConfidence
description: "Confidence level for duplicate detection"
values:
  - EXACT: "Definitely the same issue"
  - LIKELY: "Very probably the same issue"
  - POSSIBLE: "May be related or duplicate"

---

Enumeration: RelationshipStrength
description: "Strength of association relationships"
values:
  - STRONG: "Closely related"
  - MODERATE: "Somewhat related"
  - WEAK: "Loosely related"

---

Enumeration: BranchStatus
description: "Status of linked branches"
values:
  - ACTIVE: "Branch is active"
  - MERGED: "Branch has been merged"
  - DELETED: "Branch has been deleted"

---

Enumeration: PRStatus
description: "Status of linked pull requests"
values:
  - DRAFT: "PR is in draft state"
  - OPEN: "PR is open for review"
  - MERGED: "PR has been merged"
  - CLOSED: "PR was closed without merge"

---

Enumeration: BuildStatus
description: "Status of linked builds"
values:
  - RUNNING: "Build is in progress"
  - SUCCEEDED: "Build completed successfully"
  - FAILED: "Build failed"
  - CANCELLED: "Build was cancelled"

---

Enumeration: WikiType
description: "Types of wiki systems"
values:
  - ADO_WIKI: "Azure DevOps Wiki"
  - CONFLUENCE: "Atlassian Confluence"
  - NOTION: "Notion workspace"
  - GITHUB_WIKI: "GitHub Wiki"
  - OTHER: "Other wiki/documentation system"
```

---

### 4.10 Validation Checklist (Section 4)

For human reviewer to verify before approval:

- [ ] All relationship types from CROSS-DOMAIN-SYNTHESIS.md Section 4 are covered
- [ ] Cardinality constraints are appropriate for each relationship type
- [ ] Cycle prevention rules are clear and enforceable
- [ ] System mappings are bidirectionally complete (ADO, SAFe, JIRA)
- [ ] Invariants are implementable in code
- [ ] External relationship types cover VCS, CI/CD, and documentation
- [ ] Enumeration values are complete
- [ ] Jerry codebase alignment is accurate
- [ ] Semantic distinctions (blocks vs depends_on) are clear

---

### 4.11 Evidence Traceability (Section 4)

| Schema Element | Source Document | Source Section |
|----------------|-----------------|----------------|
| Hierarchical Relationships | CROSS-DOMAIN-SYNTHESIS.md | 4.1 |
| Dependency Relationships | CROSS-DOMAIN-SYNTHESIS.md | 4.2 |
| Association Relationships | CROSS-DOMAIN-SYNTHESIS.md | 4.3 |
| External Relationships | CROSS-DOMAIN-SYNTHESIS.md | 4.4 |
| Relationship Matrix | CROSS-DOMAIN-SYNTHESIS.md | 4.5 |
| ADO Link Types | ADO-SCRUM-MODEL.md | 4.1-4.4 |
| SAFe Relationships | SAFE-MODEL.md | 5.1-5.3 |
| JIRA Link Types | JIRA-MODEL.md | 5 |
| Jerry Alignment | work_item.py | add_dependency method |
| Cycle Prevention | CROSS-DOMAIN-SYNTHESIS.md | 4.1-4.2 (characteristics) |

---

*End of Section 4: Relationship Types*

---

## Section 5: Canonical State Machine

> **Task:** WI-001 Task 4 - Design canonical state machine
> **Author:** nse-architecture (Claude Opus 4.5)
> **Date:** 2026-01-13
> **Status:** DRAFT - PENDING HUMAN REVIEW

---

> **DISCLAIMER (P-043):** This section was produced by an AI agent (nse-architecture)
> as part of the Jerry framework's problem-solving workflow. All state machine definitions,
> transitions, and mappings herein are ADVISORY and require human review before
> implementation. State mappings are traced to CROSS-DOMAIN-SYNTHESIS.md Section 5
> where possible. Human judgment is the final authority.

---

### 5.1 State Machine Design Principles

The canonical state machine follows these design principles derived from the cross-domain synthesis:

1. **Simplicity:** Minimal state count that captures essential workflow stages
2. **Mappability:** All states map cleanly to ADO Scrum, SAFe, and JIRA
3. **Extensibility:** Entity-specific states can extend the core state machine
4. **Category Alignment:** States group into four semantic categories (Proposed, InProgress, Completed, Removed)
5. **Transition Clarity:** Each transition has explicit preconditions and effects
6. **Terminal State Handling:** DONE and REMOVED are terminal (with controlled reopen for DONE)
7. **Blocking Integration:** BLOCKED state integrates with Impediment entity
8. **Review Support:** IN_REVIEW state supports quality gate workflows

**Source Traceability:**
- Principles 1-4: CROSS-DOMAIN-SYNTHESIS.md Section 5.2 (State Category Alignment)
- Principles 5-8: CROSS-DOMAIN-SYNTHESIS.md Section 5.3-5.5 (Canonical State Machine)

---

### 5.2 State Categories

All three source systems converge on a fundamental four-category model for organizing work item states:

| Canonical Category | Purpose | ADO Category | SAFe Category | JIRA Category | Visual Indicator |
|-------------------|---------|--------------|---------------|---------------|------------------|
| **Proposed** | Work captured but not started | Proposed | Funnel/Analyzing | To Do | Grey |
| **InProgress** | Work actively being executed | In Progress | Implementing | In Progress | Blue |
| **Completed** | Work successfully finished | Completed | Done | Done | Green |
| **Removed** | Work will not be completed | Removed | (Resolution) | Done (Won't Do) | Red/Strikethrough |

#### 5.2.1 Category Mapping Table

```yaml
StateCategoryMapping:
  Proposed:
    description: "Work has been captured but is not yet being actively worked on"
    canonical_states: [BACKLOG, READY]
    ADO:
      category: "Proposed"
      states: [New, Approved]
    SAFe:
      category: "Funnel/Analyzing/Ready"
      states: [FUNNEL, REVIEWING, ANALYZING, READY, BACKLOG]
    JIRA:
      category: "To Do"
      states: [To Do, Open, Backlog, Ready]
    workflow_semantics: "Planning and refinement phase"

  InProgress:
    description: "Work is actively being executed by the team"
    canonical_states: [IN_PROGRESS, BLOCKED, IN_REVIEW]
    ADO:
      category: "In Progress"
      states: [Committed, In Progress]
    SAFe:
      category: "Implementing"
      states: [IN_PROGRESS, IMPLEMENTING_MVP, IMPLEMENTING_PERSEVERE, REVIEW]
    JIRA:
      category: "In Progress"
      states: [In Progress, In Review, Under Review, Blocked]
    workflow_semantics: "Execution and verification phase"

  Completed:
    description: "Work has been successfully finished and accepted"
    canonical_states: [DONE]
    ADO:
      category: "Completed"
      states: [Done]
    SAFe:
      category: "Done"
      states: [DONE, ACCEPTED]
    JIRA:
      category: "Done"
      states: [Done, Resolved, Closed (with Done resolution)]
    workflow_semantics: "Value delivered"

  Removed:
    description: "Work will not be completed (cancelled, obsolete, duplicate)"
    canonical_states: [REMOVED]
    ADO:
      category: "Removed"
      states: [Removed]
    SAFe:
      category: "(No explicit category)"
      states: [CANCELLED]
    JIRA:
      category: "Done (with non-Done resolution)"
      states: [Closed (Won't Do), Closed (Duplicate), Cancelled]
    workflow_semantics: "Work intentionally not completed"
    note: "JIRA achieves 'Removed' semantics through Resolution field rather than status category"

source: CROSS-DOMAIN-SYNTHESIS.md Section 5.2
```

**Key Insight:** JIRA's "Removed" state is achieved through the Resolution field (Won't Do, Duplicate, etc.) combined with a Done status, rather than a separate category. This ontology models Resolution as a separate property to capture this semantic distinction.

---

### 5.3 Canonical States

The canonical state machine defines seven states that can represent any work item lifecycle:

```yaml
CanonicalStates:
  description: "The seven canonical states for work item lifecycle"

  states:
    - id: BACKLOG
      category: Proposed
      display_name: "Backlog"
      description: "Work has been captured but is not yet refined or ready to start"
      entry_criteria:
        - "Work item has been created"
        - "Basic information (title, description) provided"
      exit_criteria:
        - "Acceptance criteria defined (for READY transition)"
        - "Decision to not pursue (for REMOVED transition)"
      typical_duration: "Days to weeks"
      source_mapping:
        ADO: "New"
        SAFe: "BACKLOG, FUNNEL"
        JIRA: "To Do, Open, Backlog"
      jerry_alignment: "Maps from existing PENDING status"

    - id: READY
      category: Proposed
      display_name: "Ready"
      description: "Work has been refined and is ready to be started"
      entry_criteria:
        - "Acceptance criteria are defined"
        - "Effort estimate provided (for DeliveryItems)"
        - "Dependencies identified"
        - "Work item is prioritized in backlog"
      exit_criteria:
        - "Work has been started by assignee"
        - "No longer relevant (for REMOVED transition)"
      typical_duration: "Hours to days"
      source_mapping:
        ADO: "Approved (PBI/Bug)"
        SAFe: "READY"
        JIRA: "Ready (custom status)"
      jerry_alignment: "New status - add to WorkItemStatus enum"

    - id: IN_PROGRESS
      category: InProgress
      display_name: "In Progress"
      description: "Work is actively being performed"
      entry_criteria:
        - "Assignee has started work"
        - "Capacity is available"
        - "No blocking impediments"
      exit_criteria:
        - "Implementation complete (for IN_REVIEW or DONE)"
        - "Blocker identified (for BLOCKED)"
        - "Work abandoned (for REMOVED)"
      typical_duration: "Hours to days"
      source_mapping:
        ADO: "Committed (PBI/Bug), In Progress (Task/Epic)"
        SAFe: "IN_PROGRESS, IMPLEMENTING"
        JIRA: "In Progress"
      jerry_alignment: "Maps to existing IN_PROGRESS status"

    - id: BLOCKED
      category: InProgress
      display_name: "Blocked"
      description: "Work cannot proceed due to an impediment or dependency"
      entry_criteria:
        - "Impediment or blocker identified"
        - "Blocking item created or linked (if using Impediment entity)"
      exit_criteria:
        - "Impediment resolved"
        - "Blocker completed"
        - "Decision to cancel (for REMOVED)"
      typical_duration: "Hours to days (should be minimized)"
      source_mapping:
        ADO: "(Use Impediment entity)"
        SAFe: "(Use blocking relationship)"
        JIRA: "Blocked (custom status)"
      workflow_note: "BLOCKED status triggers Scrum Master attention"
      jerry_alignment: "Maps to existing BLOCKED status"

    - id: IN_REVIEW
      category: InProgress
      display_name: "In Review"
      description: "Implementation complete, awaiting review or verification"
      entry_criteria:
        - "Implementation/development work complete"
        - "Ready for peer review, QA, or acceptance testing"
      exit_criteria:
        - "Review passed (for DONE)"
        - "Review found issues (for IN_PROGRESS)"
      typical_duration: "Hours to days"
      source_mapping:
        ADO: "(Custom state or use Committed)"
        SAFe: "REVIEW"
        JIRA: "In Review, Under Review"
      jerry_alignment: "New status - add to WorkItemStatus enum"

    - id: DONE
      category: Completed
      display_name: "Done"
      description: "Work has been successfully completed and accepted"
      entry_criteria:
        - "All acceptance criteria met"
        - "Quality gates passed (where applicable)"
        - "Review approved (if IN_REVIEW was used)"
      exit_criteria:
        - "Reopen due to defect or incomplete work (for IN_PROGRESS)"
        - "Note: Terminal for most flows"
      typical_duration: "Permanent (final state)"
      resolution_values: [DONE, FIXED]
      source_mapping:
        ADO: "Done"
        SAFe: "DONE, ACCEPTED"
        JIRA: "Done, Resolved (resolution=Done/Fixed)"
      jerry_alignment: "Maps to existing DONE status"

    - id: REMOVED
      category: Removed
      display_name: "Removed"
      description: "Work will not be completed (cancelled, obsolete, or duplicate)"
      entry_criteria:
        - "Decision made to not complete the work"
        - "Resolution reason provided"
      exit_criteria:
        - "None - terminal state (no transitions out)"
      typical_duration: "Permanent (terminal state)"
      resolution_values: [WONT_DO, DUPLICATE, OBSOLETE, CANNOT_REPRODUCE]
      source_mapping:
        ADO: "Removed"
        SAFe: "CANCELLED"
        JIRA: "Closed (resolution=Won't Do/Duplicate)"
      jerry_alignment: "Maps from existing CANCELLED status"
      note: "REMOVED is a hard terminal - cannot be reopened"

source: CROSS-DOMAIN-SYNTHESIS.md Section 5.4
```

---

### 5.4 State Machine Diagram

#### 5.4.1 Core State Machine

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        CANONICAL STATE MACHINE (Core)                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│                              ┌──────────┐                                        │
│                              │ REMOVED  │ ◄───────────────────────────────────┐  │
│                              │          │                                     │  │
│                              │(Terminal)│                                     │  │
│                              └──────────┘                                     │  │
│                                  ▲  ▲  ▲                                      │  │
│                     cancel ─────┘  │  └────── cancel ──────┐                  │  │
│                                    │                        │                  │  │
│  ┌──────────┐    refine    ┌──────────┐    start    ┌──────────────┐          │  │
│  │ BACKLOG  │─────────────►│  READY   │────────────►│ IN_PROGRESS  │──────────┘  │
│  │          │              │          │             │              │             │
│  │(Proposed)│              │(Proposed)│             │ (InProgress) │             │
│  └────┬─────┘              └────┬─────┘             └──────┬───────┘             │
│       │                         │                          │                      │
│       │ cancel                  │ demote                   │ complete             │
│       │                         │                          │                      │
│       └─────────────────────────┼──────────────────────────▼                      │
│                                 │                    ┌──────────┐                 │
│                                 │                    │   DONE   │                 │
│                                 │                    │          │                 │
│                                 │                    │(Complete)│                 │
│                                 │                    └────┬─────┘                 │
│                                 │                         │                       │
│                                 └───────── demote ────────┤ reopen                │
│                                                           │                       │
│                                                           ▼                       │
│                                                     (back to IN_PROGRESS)         │
│                                                                                   │
└───────────────────────────────────────────────────────────────────────────────────┘

Legend:
  ────►  Primary forward flow
  ─ ─ ►  Alternative/exception flow
  (Category) indicates state category
```

#### 5.4.2 Extended State Machine (with BLOCKED and IN_REVIEW)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                   CANONICAL STATE MACHINE (Extended)                                 │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   REMOVED (Terminal) ◄── cancel (from any non-terminal state)                       │
│                                                                                      │
│                                                                                      │
│   ┌──────────┐                ┌──────────┐                ┌──────────────┐           │
│   │ BACKLOG  │───refine──────►│  READY   │────start──────►│ IN_PROGRESS  │           │
│   │          │                │          │◄──demote───────│              │           │
│   └──────────┘                └──────────┘                └──────┬───────┘           │
│                                                                  │                   │
│                                                    ┌─────────────┼─────────────┐     │
│                                                    │             │             │     │
│                                                    ▼             ▼             ▼     │
│                                              ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│                                              │ BLOCKED  │  │IN_REVIEW │  │  DONE   │ │
│                                              │          │  │          │  │         │ │
│                                              │(InProg)  │  │(InProg)  │  │(Complete)│ │
│                                              └────┬─────┘  └────┬─────┘  └────┬────┘ │
│                                                   │             │             │      │
│                                     unblock ──────┘   approve───┘   reopen────┘      │
│                                         │               │              │             │
│                                         ▼               ▼              ▼             │
│                                   (IN_PROGRESS)      (DONE)      (IN_PROGRESS)      │
│                                                         │                            │
│                                                   reject ▼                           │
│                                                   (IN_PROGRESS)                      │
│                                                                                      │
│   ┌─────────────────────────────────────────────────────────────────────────────┐   │
│   │ TRANSITION SUMMARY:                                                          │   │
│   │   BACKLOG → READY:        refine                                             │   │
│   │   READY → IN_PROGRESS:    start                                              │   │
│   │   READY → BACKLOG:        demote                                             │   │
│   │   IN_PROGRESS → BLOCKED:  block                                              │   │
│   │   IN_PROGRESS → IN_REVIEW: submit                                            │   │
│   │   IN_PROGRESS → DONE:     complete (no review required)                      │   │
│   │   BLOCKED → IN_PROGRESS:  unblock                                            │   │
│   │   IN_REVIEW → DONE:       approve                                            │   │
│   │   IN_REVIEW → IN_PROGRESS: reject                                            │   │
│   │   DONE → IN_PROGRESS:     reopen (controlled)                                │   │
│   │   ANY (non-terminal) → REMOVED: cancel                                       │   │
│   └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘

source: CROSS-DOMAIN-SYNTHESIS.md Section 5.3
```

---

### 5.5 Transition Definitions Schema

```yaml
TransitionDefinitions:
  description: "Complete transition definitions with preconditions and effects"

  schema:
    Transition:
      from_state:
        type: WorkItemStatus
        required: true
        description: "Source state"
      to_state:
        type: WorkItemStatus
        required: true
        description: "Target state"
      action:
        type: string
        required: true
        description: "Named action triggering the transition"
      preconditions:
        type: Precondition[]
        required: false
        description: "Conditions that must be true for transition"
      effects:
        type: Effect[]
        required: false
        description: "Side effects of the transition"
      available_to:
        type: Role[]
        required: false
        description: "Roles allowed to perform this transition"

  transitions:
    # === BACKLOG Transitions ===
    - from_state: BACKLOG
      to_state: READY
      action: refine
      preconditions:
        - "acceptance_criteria is defined (for DeliveryItems)"
        - "effort estimate provided (recommended for Story/Task)"
      effects:
        - "Work item becomes eligible for sprint planning"
      available_to: [ProductOwner, ScrumMaster, Developer]

    - from_state: BACKLOG
      to_state: REMOVED
      action: cancel
      preconditions:
        - "Decision made to not pursue"
        - "resolution reason provided"
      effects:
        - "resolution set to WONT_DO or OBSOLETE"
        - "Work item removed from backlog"
      available_to: [ProductOwner, ScrumMaster]

    # === READY Transitions ===
    - from_state: READY
      to_state: IN_PROGRESS
      action: start
      preconditions:
        - "Capacity available"
        - "No blocking dependencies"
        - "assignee set (optional but recommended)"
      effects:
        - "Work item enters active sprint"
        - "started_at timestamp set"
      available_to: [Developer, ScrumMaster]

    - from_state: READY
      to_state: BACKLOG
      action: demote
      preconditions:
        - "Work item no longer ready (requirements changed, etc.)"
      effects:
        - "Work item returns to refinement"
      available_to: [ProductOwner, ScrumMaster]

    - from_state: READY
      to_state: REMOVED
      action: cancel
      preconditions:
        - "Decision made to not pursue"
      effects:
        - "resolution set to WONT_DO or OBSOLETE"
      available_to: [ProductOwner, ScrumMaster]

    # === IN_PROGRESS Transitions ===
    - from_state: IN_PROGRESS
      to_state: BLOCKED
      action: block
      preconditions:
        - "Impediment or blocker identified"
      effects:
        - "Blocked timestamp recorded"
        - "Optionally creates/links Impediment entity"
        - "Notifies Scrum Master"
      available_to: [Developer, ScrumMaster]

    - from_state: IN_PROGRESS
      to_state: IN_REVIEW
      action: submit
      preconditions:
        - "Implementation complete"
        - "Ready for review/testing"
      effects:
        - "Review process initiated"
        - "Reviewer notified (if configured)"
      available_to: [Developer]

    - from_state: IN_PROGRESS
      to_state: DONE
      action: complete
      preconditions:
        - "Acceptance criteria met"
        - "Quality gates passed (if applicable)"
        - "No review required OR review already passed"
      effects:
        - "completed_at timestamp set"
        - "resolution set to DONE or FIXED"
        - "Child items should also be DONE"
      available_to: [Developer, ScrumMaster]

    - from_state: IN_PROGRESS
      to_state: REMOVED
      action: cancel
      preconditions:
        - "Decision to abandon work"
      effects:
        - "resolution set to WONT_DO or OBSOLETE"
        - "Work in progress is lost"
      available_to: [ProductOwner, ScrumMaster]

    # === BLOCKED Transitions ===
    - from_state: BLOCKED
      to_state: IN_PROGRESS
      action: unblock
      preconditions:
        - "Impediment resolved"
        - "Blocking item completed (if link exists)"
      effects:
        - "Blocked duration recorded"
        - "Linked Impediment marked DONE"
      available_to: [Developer, ScrumMaster]

    - from_state: BLOCKED
      to_state: REMOVED
      action: cancel
      preconditions:
        - "Decision to cancel blocked work"
      effects:
        - "resolution set to WONT_DO"
      available_to: [ProductOwner, ScrumMaster]

    # === IN_REVIEW Transitions ===
    - from_state: IN_REVIEW
      to_state: DONE
      action: approve
      preconditions:
        - "Review passed"
        - "All review feedback addressed"
        - "Acceptance criteria verified"
      effects:
        - "completed_at timestamp set"
        - "resolution set to DONE or FIXED"
      available_to: [ProductOwner, Reviewer, QA]

    - from_state: IN_REVIEW
      to_state: IN_PROGRESS
      action: reject
      preconditions:
        - "Review found issues"
        - "Rework required"
      effects:
        - "Review feedback recorded"
        - "Returns to active development"
      available_to: [ProductOwner, Reviewer, QA]

    # === DONE Transitions ===
    - from_state: DONE
      to_state: IN_PROGRESS
      action: reopen
      preconditions:
        - "Defect found or work incomplete"
        - "Reopen justification provided"
      effects:
        - "completed_at cleared"
        - "resolution cleared"
        - "Reopen reason recorded in history"
      available_to: [ProductOwner, ScrumMaster, QA]
      note: "Reopen should be rare and controlled"

    # === REMOVED Transitions ===
    # Note: REMOVED is terminal - no transitions out
    - from_state: REMOVED
      to_state: null
      action: null
      preconditions: []
      effects: []
      note: "REMOVED is a terminal state. To resurrect work, create a new item."

source: CROSS-DOMAIN-SYNTHESIS.md Section 5.5
```

---

### 5.6 Entity-Specific State Machine Configurations

Each entity type uses a subset of the canonical states based on its workflow requirements:

```yaml
EntityStateMachineConfigurations:
  description: "Per-entity state machine configurations"

  # === STRATEGIC ITEMS ===

  Initiative:
    category: Strategic
    allowed_states: [BACKLOG, READY, IN_PROGRESS, DONE, REMOVED]
    excluded_states: [BLOCKED, IN_REVIEW]
    initial_state: BACKLOG
    terminal_states: [DONE, REMOVED]
    allowed_transitions:
      BACKLOG: [READY, REMOVED]
      READY: [IN_PROGRESS, BACKLOG, REMOVED]
      IN_PROGRESS: [DONE, REMOVED]
      DONE: []
      REMOVED: []
    rationale: "Initiatives are high-level strategic items - no review or blocking at this level"

  Epic:
    category: Strategic
    allowed_states: [BACKLOG, READY, IN_PROGRESS, BLOCKED, DONE, REMOVED]
    excluded_states: [IN_REVIEW]
    initial_state: BACKLOG
    terminal_states: [DONE, REMOVED]
    allowed_transitions:
      BACKLOG: [READY, REMOVED]
      READY: [IN_PROGRESS, BACKLOG, REMOVED]
      IN_PROGRESS: [BLOCKED, DONE, REMOVED]
      BLOCKED: [IN_PROGRESS, REMOVED]
      DONE: [IN_PROGRESS]  # Reopen
      REMOVED: []
    rationale: "Epics can be blocked by organizational impediments but don't require review"

  Capability:
    category: Strategic
    optional: true
    allowed_states: [BACKLOG, READY, IN_PROGRESS, DONE, REMOVED]
    excluded_states: [BLOCKED, IN_REVIEW]
    initial_state: BACKLOG
    terminal_states: [DONE, REMOVED]
    allowed_transitions:
      BACKLOG: [READY, REMOVED]
      READY: [IN_PROGRESS, BACKLOG, REMOVED]
      IN_PROGRESS: [DONE, BLOCKED, REMOVED]
      BLOCKED: [IN_PROGRESS, REMOVED]
      DONE: []
      REMOVED: []
    rationale: "SAFe-specific; similar to Epic workflow"

  Feature:
    category: Strategic
    allowed_states: [BACKLOG, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, DONE, REMOVED]
    excluded_states: []
    initial_state: BACKLOG
    terminal_states: [DONE, REMOVED]
    allowed_transitions:
      BACKLOG: [READY, REMOVED]
      READY: [IN_PROGRESS, BACKLOG, REMOVED]
      IN_PROGRESS: [BLOCKED, IN_REVIEW, DONE, REMOVED]
      BLOCKED: [IN_PROGRESS, REMOVED]
      IN_REVIEW: [DONE, IN_PROGRESS]
      DONE: [IN_PROGRESS]  # Reopen
      REMOVED: []
    rationale: "Features may require review (demo, acceptance) before Done"

  # === DELIVERY ITEMS ===

  Story:
    category: Delivery
    allowed_states: [BACKLOG, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, DONE, REMOVED]
    excluded_states: []
    initial_state: BACKLOG
    terminal_states: [DONE, REMOVED]
    allowed_transitions:
      BACKLOG: [READY, REMOVED]
      READY: [IN_PROGRESS, BACKLOG, REMOVED]
      IN_PROGRESS: [BLOCKED, IN_REVIEW, DONE, REMOVED]
      BLOCKED: [IN_PROGRESS, REMOVED]
      IN_REVIEW: [DONE, IN_PROGRESS]
      DONE: [IN_PROGRESS]  # Reopen
      REMOVED: []
    quality_gates_required: true
    rationale: "Stories use full state machine with quality gates"

  Task:
    category: Delivery
    allowed_states: [BACKLOG, IN_PROGRESS, BLOCKED, DONE, REMOVED]
    excluded_states: [READY, IN_REVIEW]
    initial_state: BACKLOG
    terminal_states: [DONE, REMOVED]
    allowed_transitions:
      BACKLOG: [IN_PROGRESS, REMOVED]
      IN_PROGRESS: [BLOCKED, DONE, REMOVED]
      BLOCKED: [IN_PROGRESS, REMOVED]
      DONE: [IN_PROGRESS]  # Reopen
      REMOVED: []
    quality_gates_required: true
    rationale: "Tasks are simple - skip READY refinement and IN_REVIEW verification"

  Subtask:
    category: Delivery
    allowed_states: [BACKLOG, IN_PROGRESS, DONE, REMOVED]
    excluded_states: [READY, BLOCKED, IN_REVIEW]
    initial_state: BACKLOG
    terminal_states: [DONE, REMOVED]
    allowed_transitions:
      BACKLOG: [IN_PROGRESS, REMOVED]
      IN_PROGRESS: [DONE, REMOVED]
      DONE: [IN_PROGRESS]  # Reopen
      REMOVED: []
    quality_gates_required: true
    rationale: "Minimal state machine for atomic work units"

  Spike:
    category: Delivery
    allowed_states: [BACKLOG, IN_PROGRESS, DONE, REMOVED]
    excluded_states: [READY, BLOCKED, IN_REVIEW]
    initial_state: BACKLOG
    terminal_states: [DONE, REMOVED]
    allowed_transitions:
      BACKLOG: [IN_PROGRESS, REMOVED]
      IN_PROGRESS: [DONE, REMOVED]
      DONE: []  # Cannot reopen - research is done
      REMOVED: []
    quality_gates_required: false
    rationale: "Spikes are timeboxed research - no quality gates, no reopen"

  Enabler:
    category: Delivery
    allowed_states: [BACKLOG, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, DONE, REMOVED]
    excluded_states: []
    initial_state: BACKLOG
    terminal_states: [DONE, REMOVED]
    allowed_transitions:
      BACKLOG: [READY, REMOVED]
      READY: [IN_PROGRESS, BACKLOG, REMOVED]
      IN_PROGRESS: [BLOCKED, IN_REVIEW, DONE, REMOVED]
      BLOCKED: [IN_PROGRESS, REMOVED]
      IN_REVIEW: [DONE, IN_PROGRESS]
      DONE: [IN_PROGRESS]  # Reopen
      REMOVED: []
    quality_gates_required: true
    rationale: "Enablers follow Story workflow for technical work"

  # === QUALITY ITEMS ===

  Bug:
    category: Quality
    allowed_states: [BACKLOG, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, DONE, REMOVED]
    excluded_states: []
    initial_state: BACKLOG
    terminal_states: [DONE, REMOVED]
    allowed_transitions:
      BACKLOG: [READY, REMOVED]
      READY: [IN_PROGRESS, BACKLOG, REMOVED]
      IN_PROGRESS: [BLOCKED, IN_REVIEW, DONE, REMOVED]
      BLOCKED: [IN_PROGRESS, REMOVED]
      IN_REVIEW: [DONE, IN_PROGRESS]
      DONE: [IN_PROGRESS]  # Reopen (regression)
      REMOVED: []
    quality_gates_required: true
    resolution_on_done: "FIXED"
    rationale: "Bugs use full state machine; DONE resolution is typically FIXED"

  # === FLOW CONTROL ITEMS ===

  Impediment:
    category: FlowControl
    allowed_states: [BACKLOG, IN_PROGRESS, DONE, REMOVED]
    excluded_states: [READY, BLOCKED, IN_REVIEW]
    initial_state: BACKLOG
    terminal_states: [DONE, REMOVED]
    allowed_transitions:
      BACKLOG: [IN_PROGRESS, REMOVED]
      IN_PROGRESS: [DONE, REMOVED]
      DONE: []  # Cannot reopen impediment
      REMOVED: []
    quality_gates_required: false
    rationale: "Simplified workflow - impediments are resolved, not reviewed"
    special_behavior: "When DONE, unblocks all linked work items"

source: "Derived from ONTOLOGY-v1.md Section 3 per-entity state_machine definitions"
```

#### 5.6.1 State Machine Configuration Summary

| Entity | States Used | BLOCKED | IN_REVIEW | Can Reopen | Quality Gates |
|--------|-------------|---------|-----------|------------|---------------|
| Initiative | 5 | No | No | No | No |
| Epic | 6 | Yes | No | Yes | No |
| Capability | 5 | Yes | No | No | No |
| Feature | 7 | Yes | Yes | Yes | No |
| Story | 7 | Yes | Yes | Yes | **Yes** |
| Task | 5 | Yes | No | Yes | **Yes** |
| Subtask | 4 | No | No | Yes | **Yes** |
| Spike | 4 | No | No | **No** | **No** |
| Enabler | 7 | Yes | Yes | Yes | **Yes** |
| Bug | 7 | Yes | Yes | Yes | **Yes** |
| Impediment | 4 | No | No | **No** | **No** |

---

### 5.7 State Machine Mapping Rules

#### 5.7.1 Canonical to ADO Scrum Mapping

```yaml
CanonicalToADO:
  description: "Bidirectional state mapping between Canonical and ADO Scrum"

  # Canonical → ADO
  canonical_to_ado:
    BACKLOG:
      PBI: "New"
      Bug: "New"
      Task: "To Do"
      Epic: "New"
      Feature: "New"
    READY:
      PBI: "Approved"
      Bug: "Approved"
      Task: "(use To Do or custom)"
      Epic: "(no direct mapping - use New)"
      Feature: "(no direct mapping - use New)"
    IN_PROGRESS:
      PBI: "Committed"
      Bug: "Committed"
      Task: "In Progress"
      Epic: "In Progress"
      Feature: "In Progress"
    BLOCKED:
      all: "(Use Impediment entity + blocking link)"
      note: "ADO models blocking via Impediment work item, not status"
    IN_REVIEW:
      all: "(Custom state or use Committed)"
      note: "ADO Scrum doesn't have native review state"
    DONE:
      all: "Done"
    REMOVED:
      all: "Removed"

  # ADO → Canonical
  ado_to_canonical:
    # PBI/Bug states
    New: "BACKLOG"
    Approved: "READY"
    Committed: "IN_PROGRESS"
    Done: "DONE"
    Removed: "REMOVED"

    # Task states
    "To Do": "BACKLOG"
    "In Progress": "IN_PROGRESS"
    # Done and Removed same as above

    # Epic/Feature states
    # New, In Progress, Done, Removed map directly

  # State Reason mapping (ADO-specific)
  state_reason_to_resolution:
    "Moved to backlog": null
    "Acceptance tests pass": "DONE"
    "Work finished": "DONE"
    "Cut": "WONT_DO"
    "Obsolete": "OBSOLETE"
    "Duplicate": "DUPLICATE"

source: CROSS-DOMAIN-SYNTHESIS.md Section 5.6
```

#### 5.7.2 Canonical to SAFe Mapping

```yaml
CanonicalToSAFe:
  description: "Bidirectional state mapping between Canonical and SAFe Kanban states"

  # Canonical → SAFe (by Kanban level)
  canonical_to_safe:
    BACKLOG:
      PortfolioKanban: "FUNNEL"
      SolutionKanban: "BACKLOG"
      ARTKanban: "BACKLOG"
      TeamKanban: "BACKLOG"
    READY:
      PortfolioKanban: "READY"
      SolutionKanban: "READY"
      ARTKanban: "READY"
      TeamKanban: "READY"
    IN_PROGRESS:
      PortfolioKanban: "IMPLEMENTING_MVP"
      SolutionKanban: "IMPLEMENTING"
      ARTKanban: "IN_PROGRESS"
      TeamKanban: "IN_PROGRESS"
    BLOCKED:
      all: "(Use blocking relationship)"
      note: "SAFe uses dependency relationships, not status"
    IN_REVIEW:
      PortfolioKanban: "(part of IMPLEMENTING)"
      SolutionKanban: "REVIEW"
      ARTKanban: "REVIEW"
      TeamKanban: "REVIEW"
    DONE:
      PortfolioKanban: "DONE"
      SolutionKanban: "DONE"
      ARTKanban: "DONE"
      TeamKanban: "DONE, ACCEPTED"
    REMOVED:
      all: "CANCELLED"

  # SAFe → Canonical
  safe_to_canonical:
    # Portfolio Kanban
    FUNNEL: "BACKLOG"
    REVIEWING: "BACKLOG"
    ANALYZING: "BACKLOG"
    READY: "READY"
    IMPLEMENTING_MVP: "IN_PROGRESS"
    IMPLEMENTING_PERSEVERE: "IN_PROGRESS"
    IMPLEMENTING_PIVOT: "IN_PROGRESS"
    "DONE (Go)": "DONE"
    "DONE (No-Go)": "REMOVED"

    # Team Kanban
    BACKLOG: "BACKLOG"
    # READY same
    IN_PROGRESS: "IN_PROGRESS"
    REVIEW: "IN_REVIEW"
    DONE: "DONE"
    ACCEPTED: "DONE"
    CANCELLED: "REMOVED"

source: CROSS-DOMAIN-SYNTHESIS.md Section 5.6
```

#### 5.7.3 Canonical to JIRA Mapping

```yaml
CanonicalToJIRA:
  description: "Bidirectional state mapping between Canonical and JIRA"

  # Canonical → JIRA
  canonical_to_jira:
    BACKLOG:
      status: "To Do"
      alternatives: ["Open", "Backlog"]
      resolution: null
    READY:
      status: "Ready"
      alternatives: ["To Do (with Ready label)"]
      resolution: null
      note: "JIRA default workflow doesn't have Ready; use custom status"
    IN_PROGRESS:
      status: "In Progress"
      resolution: null
    BLOCKED:
      status: "Blocked"
      alternatives: ["In Progress (with Blocked flag)"]
      resolution: null
      note: "Blocked is often a custom status in JIRA"
    IN_REVIEW:
      status: "In Review"
      alternatives: ["Under Review"]
      resolution: null
    DONE:
      status: "Done"
      resolution: "Done"
      resolution_alternatives: ["Fixed"]
    REMOVED:
      status: "Closed"
      resolution: "Won't Do"
      resolution_alternatives: ["Duplicate", "Cannot Reproduce", "Obsolete"]
      note: "JIRA uses Resolution to distinguish completion from removal"

  # JIRA → Canonical
  jira_to_canonical:
    # By status + resolution combination
    "To Do + null": "BACKLOG"
    "Open + null": "BACKLOG"
    "Backlog + null": "BACKLOG"
    "Ready + null": "READY"
    "In Progress + null": "IN_PROGRESS"
    "Blocked + null": "BLOCKED"
    "In Review + null": "IN_REVIEW"
    "Under Review + null": "IN_REVIEW"
    "Done + Done": "DONE"
    "Done + Fixed": "DONE"
    "Resolved + Fixed": "DONE"
    "Closed + Done": "DONE"
    "Closed + Won't Do": "REMOVED"
    "Closed + Won't Fix": "REMOVED"
    "Closed + Duplicate": "REMOVED"
    "Closed + Cannot Reproduce": "REMOVED"
    "Closed + Obsolete": "REMOVED"

  # Resolution mapping
  jira_resolution_to_canonical:
    Done: "DONE"
    Fixed: "FIXED"
    "Won't Do": "WONT_DO"
    "Won't Fix": "WONT_DO"
    Duplicate: "DUPLICATE"
    "Cannot Reproduce": "CANNOT_REPRODUCE"
    Incomplete: "WONT_DO"
    "Not a Bug": "WONT_DO"

source: CROSS-DOMAIN-SYNTHESIS.md Section 5.6
```

---

### 5.8 State Machine Invariants

```yaml
StateMachineInvariants:
  description: "Global invariants for state machine integrity"

  invariants:
    # === Transition Invariants ===
    - id: INV-SM-001
      rule: "No transition to current state (self-transition)"
      enforcement: HARD
      error: "InvalidTransitionError: Cannot transition from {state} to {state}"

    - id: INV-SM-002
      rule: "REMOVED is terminal - no transitions out"
      enforcement: HARD
      error: "TerminalStateError: REMOVED is a terminal state with no outbound transitions"

    - id: INV-SM-003
      rule: "Transitions must follow entity-specific allowed_transitions"
      enforcement: HARD
      error: "InvalidTransitionError: Transition from {from} to {to} not allowed for {entity_type}"

    # === State Consistency Invariants ===
    - id: INV-SM-004
      rule: "Resolution must be set when status is DONE or REMOVED"
      enforcement: SOFT
      warning: "Missing resolution for terminal state"

    - id: INV-SM-005
      rule: "Resolution must be null when status is not terminal"
      enforcement: SOFT
      warning: "Resolution should only be set for DONE or REMOVED states"

    - id: INV-SM-006
      rule: "completed_at timestamp set only when status is DONE"
      enforcement: MEDIUM
      error: "completed_at must be set when transitioning to DONE"

    - id: INV-SM-007
      rule: "started_at timestamp set when first entering IN_PROGRESS"
      enforcement: MEDIUM
      note: "Enables cycle time metrics"

    # === Quality Gate Invariants ===
    - id: INV-SM-008
      rule: "DeliveryItems requiring quality gates cannot transition to DONE without passing"
      enforcement: MEDIUM
      applicable_to: [Story, Task, Subtask, Enabler, Bug]
      exception: "Spike is exempt (quality_gates_required = false)"
      error: "QualityGateError: Cannot complete without passing quality gates"

    - id: INV-SM-009
      rule: "acceptance_criteria must be defined before transitioning to DONE (for DeliveryItems)"
      enforcement: SOFT
      warning: "Completing without acceptance criteria defined"

    # === Hierarchy Consistency Invariants ===
    - id: INV-SM-010
      rule: "Parent cannot be DONE while children are IN_PROGRESS"
      enforcement: SOFT
      warning: "Parent marked DONE with active children"
      note: "Some workflows allow this; soft enforcement"

    - id: INV-SM-011
      rule: "REMOVED parent should cascade REMOVED to children (optional)"
      enforcement: SOFT
      behavior: "When parent is REMOVED, prompt to remove children"

    # === Blocking Invariants ===
    - id: INV-SM-012
      rule: "Item in BLOCKED status should have linked blocker or impediment"
      enforcement: SOFT
      warning: "BLOCKED status without documented blocker"

    - id: INV-SM-013
      rule: "Unblocking should clear BLOCKED status on dependent items"
      enforcement: MEDIUM
      note: "Integration with Impediment entity"

    # === Reopen Invariants ===
    - id: INV-SM-014
      rule: "Reopen from DONE requires justification"
      enforcement: SOFT
      warning: "Reopening DONE item without documented reason"

    - id: INV-SM-015
      rule: "Spikes and Impediments cannot be reopened (DONE is terminal for them)"
      enforcement: HARD
      applicable_to: [Spike, Impediment]
      error: "Cannot reopen {entity_type} - DONE is terminal for this type"

source: "Derived from CROSS-DOMAIN-SYNTHESIS.md Section 5 and entity schemas"
```

---

### 5.9 Validation Checklist (Section 5)

For human reviewer to verify before approval:

- [ ] All 7 canonical states are defined (BACKLOG, READY, IN_PROGRESS, BLOCKED, IN_REVIEW, DONE, REMOVED)
- [ ] State categories align with synthesis (Proposed, InProgress, Completed, Removed)
- [ ] All transitions from synthesis Section 5.5 are included
- [ ] Entity-specific configurations match Section 3 schemas
- [ ] ADO Scrum mapping is bidirectionally complete
- [ ] SAFe mapping covers all 4 Kanban levels
- [ ] JIRA mapping handles Resolution+Status combinations
- [ ] Invariants are implementable in code
- [ ] Quality gate integration is clear
- [ ] Terminal state behavior (DONE, REMOVED) is well-defined
- [ ] Reopen behavior is controlled and documented
- [ ] BLOCKED state integrates with Impediment entity

---

### 5.10 Evidence Traceability (Section 5)

| Section Element | Source Document | Source Section |
|-----------------|-----------------|----------------|
| 5.1 Design Principles | CROSS-DOMAIN-SYNTHESIS.md | 5.2, 5.3 |
| 5.2 State Categories | CROSS-DOMAIN-SYNTHESIS.md | 5.2 State Category Alignment |
| 5.3 Canonical States | CROSS-DOMAIN-SYNTHESIS.md | 5.4 Canonical States Definition |
| 5.4 State Machine Diagram | CROSS-DOMAIN-SYNTHESIS.md | 5.3 Proposed Canonical State Machine |
| 5.5 Transitions | CROSS-DOMAIN-SYNTHESIS.md | 5.5 Canonical Transitions |
| 5.6 Entity Configurations | ONTOLOGY-v1.md | Section 3.4 (per-entity state_machine) |
| 5.7 ADO Mapping | CROSS-DOMAIN-SYNTHESIS.md | 5.6 State Machine Mapping Rules (ADO) |
| 5.7 SAFe Mapping | CROSS-DOMAIN-SYNTHESIS.md | 5.6 State Machine Mapping Rules (SAFe) |
| 5.7 JIRA Mapping | CROSS-DOMAIN-SYNTHESIS.md | 5.6 State Machine Mapping Rules (JIRA) |
| 5.8 Invariants | CROSS-DOMAIN-SYNTHESIS.md | 5.4 Entry/Exit Criteria |
| Jerry Alignment | work_item_status.py | Existing enum values |

---

*End of Section 5: Canonical State Machine*

---

## Section 6: System Mappings

> **Task:** WI-001 Task 5 - Document system mappings
> **Author:** nse-architecture (Claude Opus 4.5)
> **Date:** 2026-01-14
> **Status:** DRAFT - PENDING HUMAN REVIEW

---

> **DISCLAIMER (P-043):** This section was produced by an AI agent (nse-architecture)
> as part of the Jerry framework's problem-solving workflow. All system mapping definitions,
> adapter guidelines, and implementation recommendations herein are ADVISORY and require
> human review before implementation. Mappings are consolidated from Sections 3, 4, and 5
> with source traceability to CROSS-DOMAIN-SYNTHESIS.md. Human judgment is the final authority.

---

### 6.1 System Mapping Overview

#### 6.1.1 Purpose

System mappings define the bidirectional translation between the canonical Jerry Work Tracker ontology and external work management systems. These mappings enable:

1. **Import:** Ingest work items from ADO Scrum, SAFe, or JIRA into canonical format
2. **Export:** Synchronize canonical work items back to external systems
3. **Federation:** Query across multiple systems through a unified ontology
4. **Migration:** Move work items between systems while preserving semantics

#### 6.1.2 Design Principles

| Principle | Description | Impact |
|-----------|-------------|--------|
| **Semantic Preservation** | Mappings preserve meaning, not just data | Use resolution + status for JIRA; use Impediment for ADO blocking |
| **Lossless Round-Trip** | Import then export should not lose data | Store unmapped properties in custom_fields |
| **Graceful Degradation** | Handle unmappable concepts without failure | Map SAFe Capability to Feature with metadata |
| **Explicit Gaps** | Document what cannot be mapped | Initiative not native in ADO |
| **Bidirectional Completeness** | Every canonical concept maps to/from each system | Ensure coverage of all 11 entities |

#### 6.1.3 Supported Systems

| System | Version Baseline | API Reference | Adapter Priority |
|--------|-----------------|---------------|------------------|
| **Azure DevOps (ADO) Scrum** | 2022+ | Azure DevOps REST API v7.0 | High (Primary) |
| **SAFe (Scaled Agile Framework)** | SAFe 6.0 | Rally API / Jira Align API | Medium |
| **JIRA** | Cloud / Server 9.0+ | Jira REST API v3 | High (Primary) |

**Source:** CROSS-DOMAIN-SYNTHESIS.md Section 1 (Executive Summary)

---

### 6.2 Entity Type Mapping Matrix

#### 6.2.1 Complete Entity Mapping

This matrix consolidates the `system_mapping` fields from all 11 concrete entity schemas in Section 3.

| Canonical Entity | ADO Scrum | SAFe | JIRA | Native | Notes |
|------------------|-----------|------|------|:------:|-------|
| **Initiative** | Epic (with tag) | Strategic Theme | Initiative (Premium) | Partial | ADO: use Epic with "initiative" tag |
| **Epic** | Epic | Epic (Portfolio Backlog) | Epic | Yes | Universal - direct mapping |
| **Capability** | Feature (with tag) | Capability (Solution Backlog) | Epic or Feature | SAFe-only | ADO/JIRA: map to Feature with metadata |
| **Feature** | Feature | Feature (Program Backlog) | Epic (or custom) | Partial | JIRA: use Epic or create custom type |
| **Story** | Product Backlog Item (PBI) | Story | Story | Yes | ADO uses "PBI" terminology |
| **Task** | Task | Task | Task, Sub-task | Yes | Universal - direct mapping |
| **Subtask** | Task (child of Task) | Task (subtask) | Sub-task | Yes | Hierarchical placement determines type |
| **Spike** | Task (with "spike" tag) | Enabler Story (Exploration) | Task (with "spike" label) | Labeled | Use tagging/labeling conventions |
| **Enabler** | PBI (ValueArea=Architectural) | Enabler | Story (with "enabler" label) | SAFe-native | ADO: use ValueArea field |
| **Bug** | Bug | Defect | Bug | Yes | SAFe uses "Defect" terminology |
| **Impediment** | Impediment | (blocking links) | (blocking links) | ADO-only | SAFe/JIRA: synthesize from blocks relationship |

**Legend:**
- **Native:** Yes = explicit entity type in system | Partial = achievable via configuration | SAFe-only = only native in SAFe

#### 6.2.2 Entity Mapping by System

##### ADO Scrum Entity Types

| ADO Type | Canonical Mapping | Notes |
|----------|-------------------|-------|
| Epic | Epic or Initiative | Check for "initiative" tag |
| Feature | Feature or Capability | Check for "capability" tag |
| Product Backlog Item | Story or Enabler | Check ValueArea field |
| Task | Task, Subtask, or Spike | Check parent and tags |
| Bug | Bug | Direct mapping |
| Impediment | Impediment | Direct mapping |

##### SAFe Entity Types

| SAFe Type | Canonical Mapping | Notes |
|-----------|-------------------|-------|
| Strategic Theme | Initiative | Portfolio level |
| Epic | Epic | Direct mapping |
| Capability | Capability | Solution level |
| Feature | Feature | Program level |
| Story | Story | Team level |
| Enabler | Enabler | Check enabler_type |
| Enabler Story (Exploration) | Spike | Research type |
| Task | Task or Subtask | Based on parent |
| Defect | Bug | Terminology difference |

##### JIRA Issue Types

| JIRA Type | Canonical Mapping | Notes |
|-----------|-------------------|-------|
| Initiative | Initiative | JIRA Premium only |
| Epic | Epic or Feature | Depends on org hierarchy |
| Story | Story or Enabler | Check labels |
| Task | Task or Spike | Check labels |
| Sub-task | Subtask | Direct mapping |
| Bug | Bug | Direct mapping |

**Source:** CROSS-DOMAIN-SYNTHESIS.md Section 2.1 (Full Entity Mapping)

---

### 6.3 Property Mapping Tables

#### 6.3.1 Core Properties (Universal)

These properties exist in all three systems and map directly.

| Canonical Property | ADO Reference | SAFe Property | JIRA Field | Type | Transformation |
|--------------------|---------------|---------------|------------|------|----------------|
| `id` | `System.Id` | `id` | `key` | identifier | ADO: numeric, JIRA: PROJECT-123 format |
| `title` | `System.Title` | `name` | `summary` | string | Direct copy (max 500 chars) |
| `description` | `System.Description` | `description` | `description` | richtext | HTML to/from format conversion may apply |
| `status` | `System.State` | `state` | `status` | enum | Use Section 5.7 mapping rules |
| `priority` | `Microsoft.VSTS.Common.Priority` | `priority` | `priority` | enum | Normalize to CRITICAL/HIGH/MEDIUM/LOW |
| `assignee` | `System.AssignedTo` | `assignee` | `assignee` | user | User identity resolution required |
| `created_by` | `System.CreatedBy` | `created_by` | `reporter` | user | Immutable after creation |
| `created_at` | `System.CreatedDate` | `created` | `created` | datetime | UTC normalization |
| `updated_at` | `System.ChangedDate` | `updated` | `updated` | datetime | UTC normalization |
| `tags` | `System.Tags` | `labels` | `labels` | string[] | Semicolon-separated in ADO |
| `parent_id` | Hierarchy-Link | `parent` | `parent` | reference | Resolve cross-system IDs |

**Source:** CROSS-DOMAIN-SYNTHESIS.md Section 3.1

#### 6.3.2 Extended Properties by Entity Type

##### Strategic Items (Initiative, Epic, Capability, Feature)

| Canonical Property | ADO Reference | SAFe Property | JIRA Field | Applicable To |
|--------------------|---------------|---------------|------------|---------------|
| `target_date` | `TargetDate` | `target_pi` (convert) | `dueDate` | All strategic |
| `business_outcome` | (custom field) | `business_outcome_hypothesis` | (custom) | Initiative, Epic |
| `target_quarter` | (custom field) | (derive from PI) | (custom) | Epic |
| `lean_business_case` | (custom fields) | `lean_business_case` | (custom) | Epic |
| `wsjf_score` | (custom/extension) | `wsjf_score` | (custom) | Epic |
| `cost_of_delay` | (custom) | `cost_of_delay` | (custom) | Epic |
| `job_size` | (custom) | `job_size` | (custom) | Epic |
| `target_pi` | (custom) | `target_pi` | (custom) | Capability |
| `benefit_hypothesis` | `Value` | `benefit_hypothesis` | (custom) | Capability, Feature |
| `acceptance_criteria` | `AcceptanceCriteria` | `acceptance_criteria` | (custom) | Feature |
| `mvp_definition` | (custom) | `mvp_definition` | (custom) | Feature |
| `enabler_type` | (tag or custom) | `enabler_type` | (label) | Capability, Enabler |

##### Delivery Items (Story, Task, Subtask, Spike, Enabler)

| Canonical Property | ADO Reference | SAFe Property | JIRA Field | Applicable To |
|--------------------|---------------|---------------|------------|---------------|
| `effort` | `Effort` | `story_points` | `storyPoints` | Story, Enabler |
| `acceptance_criteria` | `AcceptanceCriteria` | `acceptance_criteria` | (custom) | Story, Enabler |
| `due_date` | `TargetDate` | (sprint end) | `dueDate` | All delivery |
| `original_estimate` | `OriginalEstimate` | (hours) | `timeoriginalestimate` | Task |
| `remaining_work` | `RemainingWork` | `remaining_hours` | `timeestimate` | Task, Subtask |
| `time_spent` | (work log) | (time tracking) | `timespent` | Task |
| `activity` | `Activity` | (label) | (label) | Task |
| `timebox` | (custom) | (iteration length) | (custom) | Spike |
| `findings` | (custom) | (description) | (custom) | Spike |
| `recommendation` | (custom) | (description) | (custom) | Spike |
| `nfrs` | (custom) | `nfrs` | (labels) | Enabler |

##### Quality Items (Bug)

| Canonical Property | ADO Reference | SAFe Property | JIRA Field |
|--------------------|---------------|---------------|------------|
| `severity` | `Severity` | (priority mapping) | `priority` |
| `reproduction_steps` | `ReproSteps` | (description) | (description field) |
| `found_in_version` | `FoundIn` | (custom) | `versions` |
| `fix_version` | `IntegrationBuild` | (custom) | `fixVersions` |
| `environment` | `Environment` | (custom) | `environment` |
| `root_cause` | (custom) | (custom) | (custom) |

##### Flow Control Items (Impediment)

| Canonical Property | ADO Reference | SAFe Equivalent | JIRA Equivalent |
|--------------------|---------------|-----------------|-----------------|
| `blocked_items` | Linked work items | blocked_by links | blocked_by links |
| `impact` | (custom) | (derive from scope) | (custom) |
| `owner` | `AssignedTo` | N/A | N/A |
| `resolution_notes` | `Resolution` | N/A | N/A |
| `escalation_level` | (custom) | N/A | N/A |

**Source:** CROSS-DOMAIN-SYNTHESIS.md Section 3.2, Section 3.3

#### 6.3.3 Property Type Transformations

| Canonical Type | ADO Type | SAFe Type | JIRA Type | Transformation Notes |
|----------------|----------|-----------|-----------|---------------------|
| `identifier` | Integer | string | string (KEY-123) | ADO: convert to string; JIRA: parse project prefix |
| `string` | String | string | text | Max length constraints may differ |
| `richtext` | HTML | text/markdown | ADF (Atlassian Doc Format) | Format conversion required |
| `enum` | String | enum | option id | Map to/from canonical enum values |
| `number` | Double | number | number | Direct mapping |
| `date` | DateTime | date | date string (YYYY-MM-DD) | Parse/format date only |
| `datetime` | DateTime | ISO 8601 | ISO 8601 | UTC normalization |
| `user` | IdentityRef | string (email) | AccountId | User identity resolution |
| `reference` | Link object | reference | issue key | Cross-system ID mapping |
| `duration` | Double (hours) | number (hours) | seconds | ADO/SAFe: hours; JIRA: seconds |
| `object` | (serialized) | object | (serialized) | JSON serialization |

**Source:** CROSS-DOMAIN-SYNTHESIS.md Section 3.4

---

### 6.4 State Mapping Summary

This section provides quick-reference tables consolidating the detailed mappings from Section 5.7.

#### 6.4.1 ADO Scrum State Mapping

| Canonical State | ADO State (PBI/Bug) | ADO State (Task) | ADO State (Epic/Feature) |
|-----------------|---------------------|------------------|--------------------------|
| **BACKLOG** | New | To Do | New |
| **READY** | Approved | (To Do) | (New) |
| **IN_PROGRESS** | Committed | In Progress | In Progress |
| **BLOCKED** | (Impediment link) | (Impediment link) | (Impediment link) |
| **IN_REVIEW** | (Custom/Committed) | (Custom) | (Custom) |
| **DONE** | Done | Done | Done |
| **REMOVED** | Removed | Removed | Removed |

**ADO to Canonical (Reverse):**

| ADO State | Canonical State | Applicable Types |
|-----------|-----------------|------------------|
| New | BACKLOG | PBI, Bug, Epic, Feature |
| Approved | READY | PBI, Bug |
| To Do | BACKLOG | Task |
| Committed | IN_PROGRESS | PBI, Bug |
| In Progress | IN_PROGRESS | Task, Epic, Feature |
| Done | DONE | All |
| Removed | REMOVED | All |

#### 6.4.2 SAFe State Mapping

| Canonical State | Portfolio Kanban | Solution Kanban | ART Kanban | Team Kanban |
|-----------------|------------------|-----------------|------------|-------------|
| **BACKLOG** | FUNNEL | BACKLOG | BACKLOG | BACKLOG |
| **READY** | READY | READY | READY | READY |
| **IN_PROGRESS** | IMPLEMENTING_MVP | IMPLEMENTING | IN_PROGRESS | IN_PROGRESS |
| **BLOCKED** | (dependency) | (dependency) | (dependency) | (dependency) |
| **IN_REVIEW** | (IMPLEMENTING) | REVIEW | REVIEW | REVIEW |
| **DONE** | DONE | DONE | DONE | DONE/ACCEPTED |
| **REMOVED** | DONE (No-Go) | CANCELLED | CANCELLED | CANCELLED |

**SAFe to Canonical (Reverse):**

| SAFe State | Canonical State |
|------------|-----------------|
| FUNNEL, REVIEWING, ANALYZING | BACKLOG |
| READY | READY |
| IMPLEMENTING_MVP, IMPLEMENTING_PERSEVERE, IN_PROGRESS | IN_PROGRESS |
| REVIEW | IN_REVIEW |
| DONE, ACCEPTED | DONE |
| DONE (No-Go), CANCELLED | REMOVED |

#### 6.4.3 JIRA State Mapping

| Canonical State | JIRA Status | JIRA Resolution | Combined Interpretation |
|-----------------|-------------|-----------------|------------------------|
| **BACKLOG** | To Do, Open, Backlog | null | Not started |
| **READY** | Ready | null | Refined, ready to start |
| **IN_PROGRESS** | In Progress | null | Active work |
| **BLOCKED** | Blocked | null | Waiting on dependency |
| **IN_REVIEW** | In Review, Under Review | null | Awaiting verification |
| **DONE** | Done, Resolved | Done, Fixed | Successfully completed |
| **REMOVED** | Closed | Won't Do, Duplicate, Cannot Reproduce | Not completed |

**JIRA Resolution Mapping:**

| JIRA Resolution | Canonical Resolution |
|-----------------|---------------------|
| Done | DONE |
| Fixed | FIXED |
| Won't Do, Won't Fix | WONT_DO |
| Duplicate | DUPLICATE |
| Cannot Reproduce | CANNOT_REPRODUCE |
| Incomplete, Not a Bug | WONT_DO |
| (null with Done status) | DONE |

**Source:** Section 5.7, CROSS-DOMAIN-SYNTHESIS.md Section 5.6

---

### 6.5 Relationship Mapping Summary

This section consolidates the relationship mappings from Section 4.8.

#### 6.5.1 Complete Relationship Mapping Table

| Canonical Relationship | ADO Link Type | SAFe Relationship | JIRA Link Type | Category |
|------------------------|---------------|-------------------|----------------|----------|
| `parent_of` | `Hierarchy-Forward` | `contains` | Parent field | Hierarchical |
| `child_of` | `Hierarchy-Reverse` | `child_of` | (implicit) | Hierarchical |
| `blocks` | `Dependency-Forward` | `blocks` | `Blocks` (outward) | Dependency |
| `blocked_by` | `Dependency-Reverse` | `blocked_by` | `is blocked by` | Dependency |
| `depends_on` | `Dependency-Forward` | `depends_on` | `Blocks` (metadata) | Dependency |
| `dependency_of` | `Dependency-Reverse` | `dependency_of` | (reverse query) | Dependency |
| `relates_to` | `Related` | `related_to` | `Relates` | Association |
| `duplicates` | `Duplicate-Forward` | (relates_to) | `Duplicates` | Association |
| `duplicated_by` | `Duplicate-Reverse` | (relates_to) | `is duplicated by` | Association |
| `clones` | (history) | (not explicit) | `Clones` | Association |
| `cloned_by` | (history) | (not explicit) | `is cloned by` | Association |
| `realizes` | (custom/parent) | `realizes` | (custom link) | Association |
| `realized_by` | (custom/parent) | `realized_by` | (custom link) | Association |
| `links_to_commit` | Git Commit artifact | (external) | Development panel | External |
| `links_to_branch` | Git Branch artifact | (external) | Development panel | External |
| `links_to_pr` | Pull Request artifact | (external) | Development panel | External |
| `links_to_build` | Build artifact | (external) | CI/CD integration | External |
| `links_to_wiki` | Wiki Page artifact | (external) | Confluence link | External |
| `links_to_url` | Hyperlink | (external) | Web Link | External |

#### 6.5.2 Relationship Support by System

| Relationship Type | ADO Native | SAFe Native | JIRA Native |
|-------------------|:----------:|:-----------:|:-----------:|
| `parent_of` / `child_of` | Yes | Yes | Yes |
| `blocks` / `blocked_by` | Yes | Yes | Yes |
| `depends_on` / `dependency_of` | Yes | Yes | Partial |
| `relates_to` | Yes | Yes | Yes |
| `duplicates` / `duplicated_by` | Yes | No | Yes |
| `clones` / `cloned_by` | No | No | Yes |
| `realizes` / `realized_by` | No | Yes | No |
| External (VCS, CI/CD) | Yes | Partial | Yes |

**Legend:** Yes = native support | Partial = achievable via configuration | No = not supported

**Source:** Section 4.8, CROSS-DOMAIN-SYNTHESIS.md Section 4.5

---

### 6.6 Mapping Complexity Assessment

#### 6.6.1 Complexity Ratings by Direction

| Mapping Direction | Complexity | Key Challenges | Implementation Effort |
|-------------------|------------|----------------|----------------------|
| **Canonical to ADO** | Medium | PBI naming; Impediment entity; ValueArea for Enabler | 3-4 weeks |
| **Canonical to SAFe** | High | 4 Kanban systems; WSJF calculation; Capability level | 5-6 weeks |
| **Canonical to JIRA** | Medium | Resolution separation; flexible hierarchy; custom fields | 3-4 weeks |
| **ADO to Canonical** | Low | Direct mapping for most entities | 2-3 weeks |
| **SAFe to Canonical** | Medium | May flatten Capability; preserve WSJF; Kanban state mapping | 3-4 weeks |
| **JIRA to Canonical** | Low | Derive status from Resolution+Status | 2-3 weeks |

#### 6.6.2 Known Gaps and Workarounds

| Gap | Affected System(s) | Impact | Workaround |
|-----|-------------------|--------|------------|
| No native Capability | ADO, JIRA | Medium | Map to Feature with `capability=true` in custom_fields |
| No native Initiative | ADO | Low | Map to Epic with `initiative=true` tag |
| No WSJF fields | ADO, JIRA | Low | Calculate from custom fields if CoD components available |
| No Resolution field | ADO, SAFe | Low | Derive from StateReason (ADO) or final state |
| No explicit Impediment | SAFe, JIRA | Medium | Synthesize from blocking relationships |
| No realizes relationship | ADO, JIRA | Low | Use parent_of or custom link type |
| No clones relationship | ADO, SAFe | Low | Track in custom_fields or history |
| Different ID formats | All | Low | Use compound IDs: `{system}:{id}` |

#### 6.6.3 Data Loss Risk Assessment

| Scenario | Risk Level | Mitigation |
|----------|------------|------------|
| Import SAFe Epic without WSJF | Low | Preserve in custom_fields; calculate if components available |
| Import JIRA issue without project context | Low | Derive project from key prefix |
| Export Impediment to JIRA | Medium | Create blocking relationships; add comment noting synthetic source |
| Export Capability to ADO | Low | Map to Feature with metadata tag |
| Round-trip through different systems | Medium | Preserve original system data in custom_fields |
| State mapping for custom workflows | Medium | Allow workflow configuration overrides |

**Source:** CROSS-DOMAIN-SYNTHESIS.md Section 6.2, Section 6.4

---

### 6.7 Adapter Implementation Guidelines

#### 6.7.1 Adapter Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ADAPTER ARCHITECTURE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│   ┌───────────────┐        ┌───────────────┐        ┌───────────────┐       │
│   │  ADO Adapter  │        │ SAFe Adapter  │        │ JIRA Adapter  │       │
│   │               │        │               │        │               │       │
│   │  - Client     │        │  - Client     │        │  - Client     │       │
│   │  - Mapper     │        │  - Mapper     │        │  - Mapper     │       │
│   │  - Cache      │        │  - Cache      │        │  - Cache      │       │
│   └───────┬───────┘        └───────┬───────┘        └───────┬───────┘       │
│           │                        │                        │               │
│           └────────────────────────┼────────────────────────┘               │
│                                    │                                         │
│                           ┌────────▼────────┐                               │
│                           │  Adapter Port   │                               │
│                           │  (Interface)    │                               │
│                           └────────┬────────┘                               │
│                                    │                                         │
│                           ┌────────▼────────┐                               │
│                           │   Canonical     │                               │
│                           │   Domain Model  │                               │
│                           └─────────────────┘                               │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 6.7.2 ADO Scrum Adapter Guidelines

```yaml
ADOAdapter:
  name: "AzureDevOpsAdapter"
  api_version: "7.0"
  authentication: ["PAT", "OAuth", "Managed Identity"]

  entity_transformation_rules:
    # Work Item Type Detection
    detect_type:
      - if: "Work Item Type == 'Epic' AND tags contains 'initiative'"
        then: "Initiative"
      - if: "Work Item Type == 'Epic'"
        then: "Epic"
      - if: "Work Item Type == 'Feature' AND tags contains 'capability'"
        then: "Capability"
      - if: "Work Item Type == 'Feature'"
        then: "Feature"
      - if: "Work Item Type == 'Product Backlog Item' AND ValueArea == 'Architectural'"
        then: "Enabler"
      - if: "Work Item Type == 'Product Backlog Item'"
        then: "Story"
      - if: "Work Item Type == 'Task' AND tags contains 'spike'"
        then: "Spike"
      - if: "Work Item Type == 'Task' AND parent is Task"
        then: "Subtask"
      - if: "Work Item Type == 'Task'"
        then: "Task"
      - if: "Work Item Type == 'Bug'"
        then: "Bug"
      - if: "Work Item Type == 'Impediment'"
        then: "Impediment"

  state_transformation_rules:
    # PBI/Bug states
    pbi_bug_mapping:
      "New": "BACKLOG"
      "Approved": "READY"
      "Committed": "IN_PROGRESS"
      "Done": "DONE"
      "Removed": "REMOVED"

    # Task states
    task_mapping:
      "To Do": "BACKLOG"
      "In Progress": "IN_PROGRESS"
      "Done": "DONE"
      "Removed": "REMOVED"

    # Epic/Feature states
    epic_feature_mapping:
      "New": "BACKLOG"
      "In Progress": "IN_PROGRESS"
      "Done": "DONE"
      "Removed": "REMOVED"

  relationship_transformation_rules:
    link_types:
      "System.LinkTypes.Hierarchy-Forward": "parent_of"
      "System.LinkTypes.Hierarchy-Reverse": "child_of"
      "System.LinkTypes.Dependency-Forward": "blocks"  # or depends_on based on metadata
      "System.LinkTypes.Dependency-Reverse": "blocked_by"
      "System.LinkTypes.Related": "relates_to"
      "System.LinkTypes.Duplicate-Forward": "duplicates"
      "System.LinkTypes.Duplicate-Reverse": "duplicated_by"

  error_handling:
    - scenario: "Work item not found"
      action: "Return NotFoundError with ADO ID"
    - scenario: "Link to deleted item"
      action: "Skip link with warning"
    - scenario: "Unknown work item type"
      action: "Map to Story with type preserved in custom_fields"
    - scenario: "Rate limit exceeded"
      action: "Exponential backoff with retry"

  implementation_notes:
    - "Use WIQL for bulk queries"
    - "Batch updates for performance"
    - "Cache Area Path and Iteration Path mappings"
    - "Handle Impediment entity specially - create blocks relationships"
```

#### 6.7.3 SAFe Adapter Guidelines

```yaml
SAFeAdapter:
  name: "ScaledAgileAdapter"
  target_tools: ["Rally", "Jira Align", "SAFe native"]
  api_version: "Rally v2.0 / Jira Align"

  entity_transformation_rules:
    detect_type:
      - if: "Type == 'StrategicTheme' OR Type == 'Theme'"
        then: "Initiative"
      - if: "Type == 'Epic' AND Level == 'Portfolio'"
        then: "Epic"
      - if: "Type == 'Capability' AND Level == 'Solution'"
        then: "Capability"
      - if: "Type == 'Feature' AND Level == 'Program'"
        then: "Feature"
      - if: "Type == 'Story' AND enabler_type != null"
        then: "Enabler"
      - if: "Type == 'Story'"
        then: "Story"
      - if: "Type == 'Enabler' AND enabler_type == 'Exploration'"
        then: "Spike"
      - if: "Type == 'Enabler'"
        then: "Enabler"
      - if: "Type == 'Task'"
        then: "Task"  # or Subtask based on parent
      - if: "Type == 'Defect'"
        then: "Bug"

  state_transformation_rules:
    # Map based on Kanban level
    portfolio_kanban:
      "FUNNEL": "BACKLOG"
      "REVIEWING": "BACKLOG"
      "ANALYZING": "BACKLOG"
      "READY": "READY"
      "IMPLEMENTING_MVP": "IN_PROGRESS"
      "IMPLEMENTING_PERSEVERE": "IN_PROGRESS"
      "IMPLEMENTING_PIVOT": "IN_PROGRESS"
      "DONE": "DONE"

    team_kanban:
      "BACKLOG": "BACKLOG"
      "READY": "READY"
      "IN_PROGRESS": "IN_PROGRESS"
      "REVIEW": "IN_REVIEW"
      "DONE": "DONE"
      "ACCEPTED": "DONE"
      "CANCELLED": "REMOVED"

  wsjf_handling:
    # WSJF = Cost of Delay / Job Size
    import:
      - "Preserve wsjf_score, cost_of_delay, job_size"
      - "Calculate if components provided but score missing"
    export:
      - "If wsjf_score set, include in Epic/Feature"
      - "Calculate components from score if needed"

  capability_handling:
    import:
      - "Import as Capability entity if SAFe Large Solution mode"
      - "Set classification = ENABLER if technical"
    export:
      - "If target doesn't support Capability, export as Feature with tag"

  error_handling:
    - scenario: "Capability not supported in target"
      action: "Map to Feature with capability=true metadata"
    - scenario: "Enabler Story vs Spike ambiguity"
      action: "Check enabler_type; Exploration = Spike"
    - scenario: "Missing WSJF components"
      action: "Leave WSJF fields null; don't calculate partial"

  implementation_notes:
    - "Handle 4 Kanban levels with separate state machines"
    - "Preserve SAFe-specific properties (PI, ART) in custom_fields"
    - "Impediment: synthesize from blocks relationships"
    - "realizes relationship is native - preserve during round-trip"
```

#### 6.7.4 JIRA Adapter Guidelines

```yaml
JIRAAdapter:
  name: "JiraCloudAdapter"
  api_version: "v3"
  authentication: ["API Token", "OAuth 2.0"]

  entity_transformation_rules:
    detect_type:
      - if: "issuetype == 'Initiative'"
        then: "Initiative"
      - if: "issuetype == 'Epic' AND project.hierarchy_level == 3"
        then: "Feature"  # Epic used as Feature in JIRA
      - if: "issuetype == 'Epic'"
        then: "Epic"
      - if: "issuetype == 'Story' AND labels contains 'enabler'"
        then: "Enabler"
      - if: "issuetype == 'Story'"
        then: "Story"
      - if: "issuetype == 'Task' AND labels contains 'spike'"
        then: "Spike"
      - if: "issuetype == 'Task'"
        then: "Task"
      - if: "issuetype == 'Sub-task'"
        then: "Subtask"
      - if: "issuetype == 'Bug'"
        then: "Bug"

  state_transformation_rules:
    # Status + Resolution combination determines canonical state
    status_resolution_mapping:
      "To Do + null": "BACKLOG"
      "Open + null": "BACKLOG"
      "Backlog + null": "BACKLOG"
      "Ready + null": "READY"
      "In Progress + null": "IN_PROGRESS"
      "Blocked + null": "BLOCKED"
      "In Review + null": "IN_REVIEW"
      "Under Review + null": "IN_REVIEW"
      "Done + Done": "DONE"
      "Done + Fixed": "DONE"
      "Resolved + Fixed": "DONE"
      "Resolved + Done": "DONE"
      "Closed + Done": "DONE"
      "Closed + Fixed": "DONE"
      "Closed + Won't Do": "REMOVED"
      "Closed + Won't Fix": "REMOVED"
      "Closed + Duplicate": "REMOVED"
      "Closed + Cannot Reproduce": "REMOVED"
      "Cancelled + null": "REMOVED"

  resolution_handling:
    import:
      - "Extract resolution from JIRA resolution field"
      - "Map to canonical Resolution enum"
      - "null resolution with Done status = DONE resolution"
    export:
      - "Set JIRA resolution based on canonical resolution"
      - "WONT_DO maps to 'Won't Do' or 'Won't Fix'"
      - "DUPLICATE requires linking to duplicate issue"

  hierarchy_handling:
    # JIRA hierarchy is flexible - needs configuration
    default_hierarchy:
      - "Initiative (L0) -> Epic (L1) -> Story (L2) -> Subtask (L3)"
    extended_hierarchy:
      - "Initiative -> Epic (as Feature) -> Story -> Subtask"
    import:
      - "Detect hierarchy from parent relationships"
      - "Map Epic to Feature if used below another Epic"
    export:
      - "If Feature exists, may need to create Epic as container"

  error_handling:
    - scenario: "Unknown status value"
      action: "Map to IN_PROGRESS with warning; preserve original in custom_fields"
    - scenario: "Resolution without Done status"
      action: "Clear resolution or transition to Done"
    - scenario: "Parent in different project"
      action: "Require JIRA Premium; warn if not available"
    - scenario: "Subtask without parent"
      action: "Error - JIRA requires parent for subtasks"

  implementation_notes:
    - "Use JQL for bulk queries"
    - "Handle ADF (Atlassian Document Format) for rich text"
    - "Changelog API for status history"
    - "Development information API for VCS links"
    - "Create Impediment: add blocking links + optionally tag as impediment"
```

#### 6.7.5 Common Adapter Interface

```yaml
AdapterInterface:
  name: "IWorkItemAdapter"
  description: "Port interface for external system adapters"

  methods:
    # Entity Operations
    - name: "get"
      signature: "get(system_id: str) -> CanonicalWorkItem | None"
      description: "Retrieve single work item by system ID"

    - name: "get_batch"
      signature: "get_batch(system_ids: list[str]) -> list[CanonicalWorkItem]"
      description: "Retrieve multiple work items"

    - name: "query"
      signature: "query(filter: WorkItemFilter) -> list[CanonicalWorkItem]"
      description: "Query work items with filter criteria"

    - name: "create"
      signature: "create(work_item: CanonicalWorkItem) -> str"
      description: "Create work item in external system, return system ID"

    - name: "update"
      signature: "update(system_id: str, changes: WorkItemChanges) -> bool"
      description: "Update work item in external system"

    - name: "delete"
      signature: "delete(system_id: str) -> bool"
      description: "Delete/remove work item (soft delete where applicable)"

    # Relationship Operations
    - name: "get_relationships"
      signature: "get_relationships(system_id: str) -> list[Relationship]"
      description: "Get all relationships for a work item"

    - name: "create_relationship"
      signature: "create_relationship(rel: Relationship) -> bool"
      description: "Create relationship between work items"

    - name: "delete_relationship"
      signature: "delete_relationship(rel: Relationship) -> bool"
      description: "Remove relationship between work items"

    # Bulk Operations
    - name: "sync"
      signature: "sync(since: datetime) -> SyncResult"
      description: "Sync changes since timestamp"

    - name: "import_project"
      signature: "import_project(project_id: str) -> ImportResult"
      description: "Import entire project"

  error_types:
    - "AdapterConnectionError"
    - "AuthenticationError"
    - "RateLimitError"
    - "EntityNotFoundError"
    - "MappingError"
    - "ValidationError"
```

---

### 6.8 Validation Checklist (Section 6)

For human reviewer to verify before approval:

- [ ] All 11 concrete entity types are mapped to all 3 systems
- [ ] All 19 relationship types are mapped to all 3 systems
- [ ] Core properties (9) have complete mappings
- [ ] Extended properties have entity-specific mappings
- [ ] State mappings consolidated from Section 5.7 are accurate
- [ ] Relationship mappings consolidated from Section 4.8 are accurate
- [ ] Complexity ratings align with CROSS-DOMAIN-SYNTHESIS.md Section 6.2
- [ ] Known gaps are documented with workarounds
- [ ] Adapter guidelines are actionable for implementation
- [ ] Transformation rules cover edge cases
- [ ] Error handling scenarios are comprehensive
- [ ] Round-trip data preservation strategy is clear

---

### 6.9 Evidence Traceability (Section 6)

| Section Element | Source Document | Source Section |
|-----------------|-----------------|----------------|
| 6.1 Overview Purpose | CROSS-DOMAIN-SYNTHESIS.md | 1 (Executive Summary) |
| 6.2 Entity Mapping | CROSS-DOMAIN-SYNTHESIS.md | 2.1 (Full Entity Mapping) |
| 6.2 Entity Mapping | ONTOLOGY-v1.md Section 3 | system_mapping per entity |
| 6.3 Property Mapping | CROSS-DOMAIN-SYNTHESIS.md | 3.1-3.4 (Property Alignment) |
| 6.4 State Mapping | ONTOLOGY-v1.md Section 5.7 | State Mapping Rules |
| 6.4 State Mapping | CROSS-DOMAIN-SYNTHESIS.md | 5.6 (Mapping Rules) |
| 6.5 Relationship Mapping | ONTOLOGY-v1.md Section 4.8 | Relationship Mapping Summary |
| 6.5 Relationship Mapping | CROSS-DOMAIN-SYNTHESIS.md | 4.5 (Relationship Matrix) |
| 6.6 Complexity Assessment | CROSS-DOMAIN-SYNTHESIS.md | 6.2 (Mapping Complexity) |
| 6.6 Gap Analysis | CROSS-DOMAIN-SYNTHESIS.md | 6.4 (Gap Mitigation Strategies) |
| 6.7 ADO Guidelines | ADO-SCRUM-MODEL.md | Full document |
| 6.7 SAFe Guidelines | SAFE-MODEL.md | Full document |
| 6.7 JIRA Guidelines | JIRA-MODEL.md | Full document |
| 6.7 Adapter Interface | Jerry Architecture Standards | Hexagonal Adapter Pattern |

---

*End of Section 6: System Mappings*
