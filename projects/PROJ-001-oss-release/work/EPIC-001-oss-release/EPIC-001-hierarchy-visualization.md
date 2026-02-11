# EPIC-001 Hierarchy Visualization

**Generated:** 2026-02-10
**Root Entity:** EPIC-001
**Diagram Types:** hierarchy, dependencies, gantt, state, progress (pie)
**Entities Included:** 14
**Max Depth Reached:** 5 (EPIC -> FEAT -> EN -> BUG -> TASK)
**Scope:** Full EPIC-001 (OSS Release Preparation)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Hierarchy Flowchart](#1-hierarchy-flowchart) | Complete Mermaid flowchart (TD) of EPIC-001 entity tree |
| [2. Dependency Map](#2-dependency-map) | Dependency chains (LR) between entities |
| [3. Gantt Chart](#3-gantt-chart) | Timeline/status view of all work items |
| [4. State Diagram](#4-state-diagram) | State machine showing status progression |
| [5. Pie Chart](#5-pie-chart) | Distribution of items by status |
| [Legend](#legend) | Color coding and line style explanation |
| [Entity Inventory](#entity-inventory) | Tabular listing of all entities with metadata |
| [Key Observations](#key-observations) | Critical path, progress, and blockers |
| [Metadata](#metadata) | Generation details |

---

## 1. Hierarchy Flowchart

Parent-child relationships from EPIC down to leaf tasks.

```mermaid
flowchart TD
    %% ========================================
    %% EPIC-001: OSS Release Preparation
    %% Full hierarchy visualization
    %% ========================================

    %% --- Strategic Layer ---
    EPIC001["EPIC-001\nOSS Release Preparation\n(in_progress)"]

    %% --- Feature Layer ---
    FEAT001["FEAT-001\nFix CI Build Failures\n(in_progress | 40%)"]

    %% --- Enabler Layer ---
    EN001["EN-001\nFix Plugin Validation\n(pending)"]
    EN002["EN-002\nFix Test Infrastructure\n(pending)"]

    %% --- Bug Layer ---
    BUG001["BUG-001\nMarketplace manifest schema error\n(pending | major)"]
    BUG002["BUG-002\nCLI projects list crash\n(completed)"]
    BUG003["BUG-003\nBootstrap test missing projects dir\n(completed)"]
    BUG004["BUG-004\nTranscript pipeline no datasets\n(pending | major)"]
    BUG005["BUG-005\nProject validation missing artifacts\n(pending | major)"]

    %% --- Task Layer ---
    TASK001["TASK-001\nAdd keywords to marketplace schema\n(backlog | HIGH)"]
    TASK002["TASK-002\nAdd validation tests\n(backlog | HIGH)"]
    TASK003["TASK-003\nSpecify Draft202012Validator\n(backlog | MEDIUM)"]

    %% --- Decision Layer ---
    DEC001["DEC-001\nJSON Schema Validator Class\n(ACCEPTED)"]

    %% ========================================
    %% PARENT-CHILD RELATIONSHIPS (solid lines)
    %% ========================================

    %% Epic -> Feature
    EPIC001 --> FEAT001

    %% Feature -> Enablers
    FEAT001 --> EN001
    FEAT001 --> EN002

    %% Feature -> Completed Bugs (direct children)
    FEAT001 --> BUG002
    FEAT001 --> BUG003

    %% Enabler EN-001 -> Children
    EN001 --> BUG001
    EN001 --> TASK001
    EN001 --> TASK002
    EN001 --> TASK003
    EN001 --> DEC001

    %% Enabler EN-002 -> Children
    EN002 --> BUG004
    EN002 --> BUG005

    %% ========================================
    %% DEPENDENCY RELATIONSHIPS (dashed lines)
    %% ========================================

    %% TASK-002 depends on TASK-001
    TASK001 -.->|"must complete before"| TASK002

    %% TASK-003 depends on TASK-001
    TASK001 -.->|"must complete before"| TASK003

    %% BUG-003 related to BUG-002 (same root cause)
    BUG002 -.->|"same root cause"| BUG003

    %% BUG-005 related to BUG-003
    BUG005 -.->|"related"| BUG003

    %% DEC-001 informs TASK-003
    DEC001 -.->|"informs"| TASK003

    %% ========================================
    %% STATUS COLOR CODING
    %% ========================================

    %% Completed items: green (#90EE90)
    style BUG002 fill:#90EE90,stroke:#228B22,color:#000
    style BUG003 fill:#90EE90,stroke:#228B22,color:#000

    %% In-progress items: blue (#87CEEB)
    style EPIC001 fill:#87CEEB,stroke:#4682B4,color:#000
    style FEAT001 fill:#87CEEB,stroke:#4682B4,color:#000

    %% Pending / backlog items: gray (#D3D3D3)
    style EN001 fill:#D3D3D3,stroke:#808080,color:#000
    style EN002 fill:#D3D3D3,stroke:#808080,color:#000
    style BUG001 fill:#D3D3D3,stroke:#808080,color:#000
    style BUG004 fill:#D3D3D3,stroke:#808080,color:#000
    style BUG005 fill:#D3D3D3,stroke:#808080,color:#000
    style TASK001 fill:#D3D3D3,stroke:#808080,color:#000
    style TASK002 fill:#D3D3D3,stroke:#808080,color:#000
    style TASK003 fill:#D3D3D3,stroke:#808080,color:#000

    %% Decision: light purple for accepted decisions
    style DEC001 fill:#DDA0DD,stroke:#800080,color:#000
```

---

## 2. Dependency Map

Dependency chains and blocking relationships between entities.

```mermaid
flowchart LR
    %% ========================================
    %% Critical dependency chain for EN-001
    %% ========================================
    TASK001["TASK-001\nAdd keywords to schema\n(backlog)"] --> TASK002["TASK-002\nAdd validation tests\n(backlog)"]
    TASK001 --> TASK003["TASK-003\nSpecify validator class\n(backlog)"]
    DEC001["DEC-001\nValidator class decision\n(ACCEPTED)"] -.->|informs| TASK003

    %% ========================================
    %% Cross-references between bugs
    %% ========================================
    BUG002["BUG-002\nCLI crash\n(completed)"] -.->|same root cause| BUG003["BUG-003\nBootstrap test\n(completed)"]
    BUG005["BUG-005\nProject validation\n(pending)"] -.->|related| BUG003

    %% ========================================
    %% Enabler sequencing (suggested, not hard)
    %% ========================================
    EN001["EN-001\nPlugin Validation\n(pending)"] -.->|suggested before| EN002["EN-002\nTest Infrastructure\n(pending)"]

    %% ========================================
    %% Enabler -> Feature completion
    %% ========================================
    EN001 -->|"completes"| FEAT001["FEAT-001\nFix CI Build Failures"]
    EN002 -->|"completes"| FEAT001

    %% ========================================
    %% STATUS COLOR CODING
    %% ========================================
    style TASK001 fill:#D3D3D3,stroke:#808080,color:#000
    style TASK002 fill:#D3D3D3,stroke:#808080,color:#000
    style TASK003 fill:#D3D3D3,stroke:#808080,color:#000
    style DEC001 fill:#DDA0DD,stroke:#800080,color:#000
    style BUG002 fill:#90EE90,stroke:#228B22,color:#000
    style BUG003 fill:#90EE90,stroke:#228B22,color:#000
    style BUG005 fill:#D3D3D3,stroke:#808080,color:#000
    style EN001 fill:#D3D3D3,stroke:#808080,color:#000
    style EN002 fill:#D3D3D3,stroke:#808080,color:#000
    style FEAT001 fill:#87CEEB,stroke:#4682B4,color:#000
```

---

## 3. Gantt Chart

Timeline and status view of all work items. Items are grouped by parent and show current status (done, active, or pending).

```mermaid
gantt
    title EPIC-001 OSS Release Preparation - Work Item Status
    dateFormat YYYY-MM-DD

    section FEAT-001 (Completed Bugs)
    BUG-002 CLI crash fix               :done,    bug002, 2026-02-10, 1d
    BUG-003 Bootstrap test fix           :done,    bug003, 2026-02-10, 1d

    section EN-001 Plugin Validation
    BUG-001 Marketplace schema error     :         bug001, 2026-02-11, 2d
    TASK-001 Add keywords to schema      :crit,    task001, 2026-02-11, 1d
    TASK-002 Add validation tests        :         task002, after task001, 1d
    TASK-003 Specify validator class     :         task003, after task001, 1d

    section EN-002 Test Infrastructure
    BUG-004 Transcript pipeline datasets :         bug004, 2026-02-13, 2d
    BUG-005 Project validation fixtures  :         bug005, 2026-02-13, 2d
```

---

## 4. State Diagram

State machine showing the worktracker item status progression. Annotated with current item counts per state.

```mermaid
stateDiagram-v2
    [*] --> pending : create item

    pending --> in_progress : start work
    pending --> backlog : defer

    backlog --> pending : prioritize
    backlog --> in_progress : start work

    in_progress --> blocked : impediment found
    in_progress --> completed : finish work
    in_progress --> cancelled : cancel

    blocked --> in_progress : impediment resolved
    blocked --> cancelled : cancel

    completed --> [*]
    cancelled --> [*]

    note right of pending
        EN-001, EN-002
        BUG-001, BUG-004, BUG-005
        (5 items)
    end note

    note right of in_progress
        EPIC-001, FEAT-001
        (2 items)
    end note

    note right of backlog
        TASK-001, TASK-002, TASK-003
        (3 items)
    end note

    note right of completed
        BUG-002, BUG-003
        (2 items)
    end note
```

---

## 5. Pie Chart

Distribution of deliverable work items by status. DEC-001 excluded (decision artifact, not deliverable).

```mermaid
pie title EPIC-001 Work Item Status Distribution
    "Completed" : 2
    "In Progress" : 2
    "Pending" : 5
    "Backlog" : 3
```

---

## Legend

| Symbol | Meaning |
|--------|---------|
| **Solid arrow** ( `-->` ) | Parent-child relationship |
| **Dashed arrow** ( `-.->` ) | Dependency or cross-reference |
| ![#87CEEB](https://via.placeholder.com/15/87CEEB/87CEEB.png) **Blue (#87CEEB)** | In Progress |
| ![#90EE90](https://via.placeholder.com/15/90EE90/90EE90.png) **Green (#90EE90)** | Completed |
| ![#D3D3D3](https://via.placeholder.com/15/D3D3D3/D3D3D3.png) **Gray (#D3D3D3)** | Pending / Backlog |
| ![#DDA0DD](https://via.placeholder.com/15/DDA0DD/DDA0DD.png) **Purple (#DDA0DD)** | Decision (Accepted) |

---

## Entity Inventory

| # | ID | Type | Title | Status | Priority | Parent | Color |
|---|-----|------|-------|--------|----------|--------|-------|
| 1 | EPIC-001 | Epic | OSS Release Preparation | in_progress | high | -- | Blue |
| 2 | FEAT-001 | Feature | Fix CI Build Failures | in_progress | high | EPIC-001 | Blue |
| 3 | EN-001 | Enabler | Fix Plugin Validation | pending | high | FEAT-001 | Gray |
| 4 | EN-002 | Enabler | Fix Test Infrastructure | pending | medium | FEAT-001 | Gray |
| 5 | BUG-001 | Bug | Marketplace manifest schema error: `keywords` not allowed | pending | high | EN-001 | Gray |
| 6 | BUG-002 | Bug | CLI `projects list` crashes with unhandled exception | completed | high | FEAT-001 | Green |
| 7 | BUG-003 | Bug | Bootstrap test assumes `projects/` directory exists | completed | medium | FEAT-001 | Green |
| 8 | BUG-004 | Bug | Transcript pipeline test finds no datasets | pending | medium | EN-002 | Gray |
| 9 | BUG-005 | Bug | Project validation tests reference non-existent PROJ-001-plugin-cleanup | pending | medium | EN-002 | Gray |
| 10 | TASK-001 | Task | Add `keywords` property to marketplace plugin item schema | backlog | HIGH | BUG-001 / EN-001 | Gray |
| 11 | TASK-002 | Task | Add tests for plugin manifest validation | backlog | HIGH | BUG-001 / EN-001 | Gray |
| 12 | TASK-003 | Task | Specify Draft202012Validator in validation script | backlog | MEDIUM | BUG-001 / EN-001 | Gray |
| 13 | DEC-001 | Decision | JSON Schema Validator Class Selection | ACCEPTED | HIGH | EN-001 | Purple |
| 14 | -- | PR | PR #6: fix Windows CRLF line ending support in VTT validator | blocked (CI failing) | -- | EPIC-001 | -- |

### Status Distribution

| Status | Count | Percentage |
|--------|-------|------------|
| Completed | 2 | 17% |
| In Progress | 2 | 17% |
| Pending | 5 | 41% |
| Backlog | 3 | 25% |
| **Total** | **12** | **100%** |

(DEC-001 excluded from status distribution as it is a decision artifact, not a deliverable work item. EPIC-001 and FEAT-001 counted as in_progress containers.)

---

## Key Observations

### 1. Critical Path

The critical path to unblocking PR #6 is:

```
TASK-001 (add keywords to schema)
  -> TASK-002 (add validation tests)
  -> TASK-003 (specify validator class)
  -> BUG-001 resolved -> EN-001 complete
  -> BUG-004 fix (transcript pipeline)
  -> BUG-005 fix (project validation)
  -> EN-002 complete
  -> FEAT-001 complete
  -> EPIC-001 complete
```

**TASK-001 is the single most critical unstarted item.** It is the root cause fix for BUG-001 and blocks both TASK-002 and TASK-003. Completing TASK-001 would unblock the entire EN-001 work stream.

### 2. Progress Assessment

- **Overall Progress:** ~17% (2 of 12 deliverable items completed)
- **Completed:** BUG-002 and BUG-003 (both resolved by committing `projects/` directory to git -- same root cause, single fix)
- **Active Work:** None currently in_progress at the leaf level. EN-001 and BUG-001 have been corrected to `pending` (no task work has started).
- **Waiting:** EN-002 (BUG-004 + BUG-005) has not started yet

### 3. Blockers and Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| **TASK-001 not started** | HIGH | This is the root cause fix for the Plugin Validation CI failure. Must be started immediately. |
| **EN-002 has no tasks defined** | MEDIUM | BUG-004 and BUG-005 have fix options identified but no tasks created yet. Task decomposition needed before work begins. |
| **BUG-004 test data decision** | MEDIUM | Three options under consideration (skip, dynamic discovery, commit test data). Decision needed before implementation. |
| **Sequential dependency** | LOW | EN-001 and EN-002 are independent and could be worked in parallel to accelerate completion. |

### 4. Parallelization Opportunity

EN-001 (Plugin Validation) and EN-002 (Test Infrastructure) address different CI failure categories and have **no mutual dependencies**. They can be worked concurrently:

- **EN-001 track:** TASK-001 -> TASK-002 -> TASK-003 (fixes Plugin Validation CI check)
- **EN-002 track:** BUG-004 + BUG-005 (fixes Test pip/uv CI jobs)

Working both in parallel could reduce time-to-completion significantly.

### 5. Decision Status

DEC-001 (JSON Schema Validator Class Selection) is **ACCEPTED** but has an important addendum: the decision is valid as a best practice (TASK-003) but is **not** the root cause fix. The root cause fix is TASK-001 (adding `keywords` to the marketplace schema). This distinction was discovered through local verification after the initial analysis.

---

## Metadata

- **Entities Visualized:** EPIC-001, FEAT-001, EN-001, EN-002, BUG-001, BUG-002, BUG-003, BUG-004, BUG-005, TASK-001, TASK-002, TASK-003, DEC-001
- **Relationships Shown:** 11 parent-child, 5 dependency/cross-reference
- **Diagram Types Generated:** 5 (hierarchy flowchart, dependency map, gantt chart, state diagram, pie chart)
- **Status Color Coding:** Enabled (Blue=in_progress, Green=completed, Gray=pending/backlog, Purple=decision)
- **Status Corrections Applied:** EN-001 and BUG-001 corrected from `in_progress` to `pending` per source files
- **Warnings:** None

---

*Generated by wt-visualizer v1.0.0*
