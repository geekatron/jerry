# EPIC-001: OSS Release Preparation — Visual Dashboard

> **Generated:** 2026-02-12
> **Agent:** wt-visualizer v1.0.0
> **Root Entity:** EPIC-001
> **Project:** PROJ-001-oss-release
> **Total Entities:** 42

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Hierarchy](#1-hierarchy) | Full parent-child entity tree (flowchart TD) |
| [2. Timeline](#2-timeline) | Project schedule grouped by Feature (gantt) |
| [3. Status Lifecycle](#3-status-lifecycle) | Work item state machine (stateDiagram-v2) |
| [4. Dependencies](#4-dependencies) | Blocking relationships and critical paths (flowchart LR) |
| [5. Progress](#5-progress) | Completion breakdown pie charts |
| [6. Gantt with Dependencies](#6-gantt-with-dependencies) | Detailed schedule with dependency chains and milestones |
| [Legend](#legend) | Color coding and status definitions |
| [Warnings](#warnings) | Data integrity notes |

---

## Legend

| Color | Status | Hex |
|-------|--------|-----|
| Green | done / complete | #90EE90 |
| Gold | in_progress | #FFD700 |
| Light Gray | pending | #D3D3D3 |
| Light Blue | partial | #87CEEB |
| Red | blocked | #FF6B6B |

---

## 1. Hierarchy

> Full EPIC-001 parent-child tree. 42 entities across 3 features, 18 enablers, bugs, decisions, and discoveries.

```mermaid
flowchart TD
    EPIC001["EPIC-001<br/>OSS Release Preparation<br/>35%"]

    %% Features
    FEAT001["FEAT-001<br/>Fix CI Build Failures<br/>85%"]
    FEAT002["FEAT-002<br/>Research & Preparation<br/>10%"]
    FEAT003["FEAT-003<br/>CLAUDE.md Optimization<br/>0%"]

    %% FEAT-001 Enablers
    EN001["EN-001<br/>Fix Plugin Validation"]
    EN002["EN-002<br/>Fix Test Infrastructure"]
    EN003["EN-003<br/>Fix Validation Test Regressions"]
    EN004["EN-004<br/>Fix Pre-commit Hook Coverage"]

    %% FEAT-001 Feature-Level Bugs
    BUG002F1["BUG-002<br/>CLI projects list crash"]
    BUG003F1["BUG-003<br/>Bootstrap test missing dir"]
    BUG007F1["BUG-007<br/>Synthesis content test"]

    %% EN-004 Children
    BUG010["BUG-010<br/>Session hook warning"]
    BUG011["BUG-011<br/>Pytest hook python-only"]
    DEC001E4["DEC-001<br/>Pre-commit install strategy"]
    DEC002E4["DEC-002<br/>Pytest hook file types"]

    %% FEAT-002 Enablers
    EN101["EN-101<br/>OSS Best Practices Research"]
    EN102["EN-102<br/>Claude Code Best Practices"]
    EN103["EN-103<br/>CLAUDE.md Optimization Research"]
    EN104["EN-104<br/>Plugins Research"]
    EN105["EN-105<br/>Skills Research"]
    EN106["EN-106<br/>Decomposition Research"]
    EN107["EN-107<br/>Current State Analysis"]

    %% FEAT-002 Decisions and Discoveries
    DEC001F2["DEC-001<br/>Transcript Decisions"]
    DEC002F2["DEC-002<br/>Orchestration Execution"]
    DEC003F2["DEC-003<br/>Phase 2 Execution Strategy"]
    DISC001F2["DISC-001<br/>Missed Research Scope"]

    %% FEAT-003 Enablers
    EN201["EN-201<br/>Worktracker Skill Extraction"]
    EN202["EN-202<br/>CLAUDE.md Rewrite"]
    EN203["EN-203<br/>TODO Section Migration"]
    EN204["EN-204<br/>Validation & Testing"]
    EN205["EN-205<br/>Documentation Update"]
    EN206["EN-206<br/>Context Distribution Strategy"]
    EN207["EN-207<br/>Worktracker Agent Implementation"]

    %% FEAT-003 Decisions and Discoveries
    DEC001F3["DEC-001<br/>Navigation Table Standard"]
    DISC001F3["DISC-001<br/>Navigation Tables LLM"]

    %% Hierarchy Connections
    EPIC001 --> FEAT001
    EPIC001 --> FEAT002
    EPIC001 --> FEAT003

    FEAT001 --> EN001
    FEAT001 --> EN002
    FEAT001 --> EN003
    FEAT001 --> EN004
    FEAT001 --> BUG002F1
    FEAT001 --> BUG003F1
    FEAT001 --> BUG007F1

    EN004 --> BUG010
    EN004 --> BUG011
    EN004 --> DEC001E4
    EN004 --> DEC002E4

    FEAT002 --> EN101
    FEAT002 --> EN102
    FEAT002 --> EN103
    FEAT002 --> EN104
    FEAT002 --> EN105
    FEAT002 --> EN106
    FEAT002 --> EN107
    FEAT002 --> DEC001F2
    FEAT002 --> DEC002F2
    FEAT002 --> DEC003F2
    FEAT002 --> DISC001F2

    FEAT003 --> EN201
    FEAT003 --> EN202
    FEAT003 --> EN203
    FEAT003 --> EN204
    FEAT003 --> EN205
    FEAT003 --> EN206
    FEAT003 --> EN207
    FEAT003 --> DEC001F3
    FEAT003 --> DISC001F3

    %% Status Color Coding
    style EPIC001 fill:#FFD700,stroke:#333,stroke-width:2px
    style FEAT001 fill:#FFD700,stroke:#333,stroke-width:2px
    style FEAT002 fill:#FFD700,stroke:#333,stroke-width:2px
    style FEAT003 fill:#D3D3D3,stroke:#333,stroke-width:2px

    style EN001 fill:#90EE90,stroke:#333
    style EN002 fill:#FFD700,stroke:#333
    style EN003 fill:#90EE90,stroke:#333
    style EN004 fill:#FFD700,stroke:#333

    style BUG002F1 fill:#90EE90,stroke:#333
    style BUG003F1 fill:#90EE90,stroke:#333
    style BUG007F1 fill:#90EE90,stroke:#333

    style BUG010 fill:#90EE90,stroke:#333
    style BUG011 fill:#D3D3D3,stroke:#333
    style DEC001E4 fill:#90EE90,stroke:#333
    style DEC002E4 fill:#90EE90,stroke:#333

    style EN101 fill:#87CEEB,stroke:#333
    style EN102 fill:#D3D3D3,stroke:#333
    style EN103 fill:#D3D3D3,stroke:#333
    style EN104 fill:#D3D3D3,stroke:#333
    style EN105 fill:#D3D3D3,stroke:#333
    style EN106 fill:#D3D3D3,stroke:#333
    style EN107 fill:#90EE90,stroke:#333

    style DEC001F2 fill:#90EE90,stroke:#333
    style DEC002F2 fill:#90EE90,stroke:#333
    style DEC003F2 fill:#90EE90,stroke:#333
    style DISC001F2 fill:#90EE90,stroke:#333

    style EN201 fill:#D3D3D3,stroke:#333
    style EN202 fill:#D3D3D3,stroke:#333
    style EN203 fill:#D3D3D3,stroke:#333
    style EN204 fill:#D3D3D3,stroke:#333
    style EN205 fill:#D3D3D3,stroke:#333
    style EN206 fill:#D3D3D3,stroke:#333
    style EN207 fill:#D3D3D3,stroke:#333

    style DEC001F3 fill:#90EE90,stroke:#333
    style DISC001F3 fill:#90EE90,stroke:#333


```

---

## 2. Timeline

> Project schedule grouped by Feature. Done/active/future markers. Pending dates are estimates.

```mermaid
gantt
    title EPIC-001: OSS Release Preparation Timeline
    dateFormat YYYY-MM-DD
    axisFormat %m-%d

    section EPIC-001
    OSS Release Preparation           :active, epic001, 2026-02-10, 2026-02-28

    section FEAT-001 CI Fixes
    FEAT-001 Fix CI Build Failures     :active, feat001, 2026-02-10, 2026-02-15
    EN-001 Fix Plugin Validation       :done, en001, 2026-02-10, 2026-02-11
    EN-002 Fix Test Infrastructure     :active, en002, 2026-02-10, 2026-02-14
    EN-003 Fix Validation Regressions  :done, en003, 2026-02-11, 2026-02-11
    EN-004 Fix Pre-commit Hook         :active, en004, 2026-02-11, 2026-02-14
    BUG-002 CLI crash                  :done, bug002, 2026-02-10, 2026-02-10
    BUG-003 Bootstrap test             :done, bug003, 2026-02-10, 2026-02-10
    BUG-007 Synthesis test             :done, bug007, 2026-02-11, 2026-02-11

    section FEAT-002 Research
    FEAT-002 Research & Preparation    :active, feat002, 2026-01-31, 2026-02-20
    EN-101 OSS Best Practices          :done, en101, 2026-01-31, 2026-01-31
    EN-107 Current State Analysis      :done, en107, 2026-01-31, 2026-01-31
    EN-102 Claude Code Best Practices  :en102, 2026-02-13, 2026-02-15
    EN-103 CLAUDE.md Optimization      :en103, 2026-02-13, 2026-02-15
    EN-104 Plugins Research            :en104, 2026-02-15, 2026-02-17
    EN-105 Skills Research             :en105, 2026-02-15, 2026-02-17
    EN-106 Decomposition Research      :en106, 2026-02-17, 2026-02-19

    section FEAT-003 Optimization
    FEAT-003 CLAUDE.md Optimization    :feat003, 2026-02-20, 2026-02-28
    EN-201 Worktracker Extraction      :en201, 2026-02-20, 2026-02-22
    EN-202 CLAUDE.md Rewrite           :en202, 2026-02-22, 2026-02-24
    EN-203 TODO Migration              :en203, 2026-02-22, 2026-02-23
    EN-204 Validation & Testing        :en204, 2026-02-24, 2026-02-25
    EN-205 Documentation Update        :en205, 2026-02-25, 2026-02-26
    EN-206 Context Distribution        :en206, 2026-02-20, 2026-02-26
    EN-207 Worktracker Agents          :en207, 2026-02-20, 2026-02-27

```

---

## 3. Status Lifecycle

> Work item state machine showing all transitions observed in PROJ-001.

```mermaid
stateDiagram-v2
    [*] --> pending : Created

    pending --> in_progress : Work started
    pending --> blocked : Dependency unresolved

    in_progress --> done : All acceptance criteria met
    in_progress --> blocked : Blocker identified
    in_progress --> partial : Partial completion

    blocked --> in_progress : Blocker resolved
    blocked --> pending : Descoped / deferred

    partial --> in_progress : Remaining work resumed
    partial --> done : All criteria met

    done --> in_progress : Reopened (new bug found)

    done --> [*]

    note right of pending
        FEAT-003, EN-201 through EN-207,
        EN-102 through EN-106, BUG-011
    end note

    note right of in_progress
        FEAT-001 (85%), FEAT-002 (10%),
        EN-002, EN-004
    end note

    note right of done
        EN-001, EN-003, EN-107,
        BUG-001 through BUG-007, BUG-010
    end note

    note right of partial
        EN-101 (research 100%, status partial)
    end note

    note right of blocked
        Orchestration phases 1-4.
        FEAT-003 blocked by FEAT-002.
    end note
```

**Transitions observed in PROJ-001:**

| Transition | Count | Examples |
|------------|-------|---------|
| pending -> in_progress | 11+ | FEAT-001, EN-001, EN-002, EN-003, EN-004 |
| in_progress -> done | 10+ | EN-001, EN-003, BUG-001 through BUG-007, BUG-010 |
| done -> in_progress (reopened) | 3 | FEAT-001 (reopened 3x: BUG-007, EN-004, EN-002 PII) |
| in_progress -> partial | 1 | EN-101 |
| pending -> blocked | 3 | Orchestration phases 1-4 |

---

## 4. Dependencies

> Blocking relationships, critical paths, and cross-cutting concerns.

```mermaid
flowchart LR
    %% FEAT-level dependencies
    FEAT001["FEAT-001<br/>Fix CI Build Failures<br/>85%"]
    FEAT002["FEAT-002<br/>Research & Preparation<br/>10%"]
    FEAT003["FEAT-003<br/>CLAUDE.md Optimization<br/>0%"]

    FEAT001 -->|"clean CI baseline<br/>needed"| FEAT002
    FEAT002 -->|"research informs<br/>implementation"| FEAT003

    %% FEAT-001 internal dependencies
    EN001["EN-001<br/>Fix Plugin Validation<br/>DONE"]
    EN003["EN-003<br/>Fix Validation Regressions<br/>DONE"]
    EN002["EN-002<br/>Fix Test Infrastructure<br/>IN PROGRESS"]
    EN004["EN-004<br/>Fix Pre-commit Hook<br/>IN PROGRESS"]

    EN001 -->|"regression from<br/>EN-001/TASK-002"| EN003
    EN004 -->|"blocks FEAT-001<br/>closure"| FEAT001

    BUG011["BUG-011<br/>Pytest hook python-only<br/>PENDING"]
    BUG011 -->|"blocks"| EN004

    %% FEAT-002 internal dependencies
    EN101["EN-101<br/>OSS Best Practices<br/>PARTIAL"]
    EN107["EN-107<br/>Current State Analysis<br/>COMPLETE"]
    EN102["EN-102<br/>Claude Code Best Practices<br/>PENDING"]
    EN103["EN-103<br/>CLAUDE.md Optimization Research<br/>PENDING"]
    EN104["EN-104<br/>Plugins Research<br/>PENDING"]
    EN105["EN-105<br/>Skills Research<br/>PENDING"]
    EN106["EN-106<br/>Decomposition Research<br/>PENDING"]

    EN101 -->|"foundation for"| EN102
    EN101 -->|"foundation for"| EN103
    EN101 -->|"foundation for"| EN104
    EN101 -->|"foundation for"| EN105
    EN101 -->|"foundation for"| EN106

    %% FEAT-003 internal dependencies (critical path)
    EN201["EN-201<br/>Worktracker Extraction<br/>PENDING"]
    EN202["EN-202<br/>CLAUDE.md Rewrite<br/>PENDING"]
    EN203["EN-203<br/>TODO Migration<br/>PENDING"]
    EN204["EN-204<br/>Validation & Testing<br/>PENDING"]
    EN205["EN-205<br/>Documentation Update<br/>PENDING"]
    EN206["EN-206<br/>Context Distribution<br/>PENDING"]
    EN207["EN-207<br/>Worktracker Agents<br/>PENDING"]

    EN201 -->|"critical path"| EN202
    EN201 -->|"enables"| EN203
    EN201 -->|"enables"| EN206
    EN201 -->|"enables"| EN207
    EN202 -->|"critical path"| EN204
    EN203 -->|"feeds into"| EN204
    EN204 -->|"validates"| EN205
    EN206 -->|"informs"| EN205

    %% Status Color Coding
    style FEAT001 fill:#FFD700,stroke:#333,stroke-width:2px
    style FEAT002 fill:#FFD700,stroke:#333,stroke-width:2px
    style FEAT003 fill:#D3D3D3,stroke:#333,stroke-width:2px

    style EN001 fill:#90EE90,stroke:#333
    style EN002 fill:#FFD700,stroke:#333
    style EN003 fill:#90EE90,stroke:#333
    style EN004 fill:#FFD700,stroke:#333
    style BUG011 fill:#D3D3D3,stroke:#333

    style EN101 fill:#87CEEB,stroke:#333
    style EN102 fill:#D3D3D3,stroke:#333
    style EN103 fill:#D3D3D3,stroke:#333
    style EN104 fill:#D3D3D3,stroke:#333
    style EN105 fill:#D3D3D3,stroke:#333
    style EN106 fill:#D3D3D3,stroke:#333
    style EN107 fill:#90EE90,stroke:#333

    style EN201 fill:#D3D3D3,stroke:#333
    style EN202 fill:#D3D3D3,stroke:#333
    style EN203 fill:#D3D3D3,stroke:#333
    style EN204 fill:#D3D3D3,stroke:#333
    style EN205 fill:#D3D3D3,stroke:#333
    style EN206 fill:#D3D3D3,stroke:#333
    style EN207 fill:#D3D3D3,stroke:#333


```

**Critical Paths:**

```
FEAT-001 closure:  BUG-011 -> EN-004 -> FEAT-001 milestone
Full project:      EN-106 -> EN-201 -> EN-202 -> EN-204 -> EN-205 -> EPIC-001 milestone
Parallel path:     EN-201 -> EN-206 (longest parallel path at 7 days)
```


---

## 5. Progress

> Work item completion breakdown across the entire project.

```mermaid
pie title EPIC-001 Work Item Status (All Levels)
    "Done / Complete" : 18
    "In Progress" : 5
    "Pending" : 15
    "Partial" : 1
```

**Status Breakdown:**

| Status | Count | Items |
|--------|-------|-------|
| **Done / Complete** | 18 | EN-001, EN-003, EN-107, BUG-001 through BUG-007, BUG-010, 6 Decisions, DISC-001 (FEAT-002) |
| **In Progress** | 4 | FEAT-001, FEAT-002, EN-002, EN-004 |
| **Pending** | 15 | FEAT-003, EN-102 through EN-106, EN-201 through EN-207, BUG-011 |
| **Partial** | 1 | EN-101 |

```mermaid
pie title Feature Completion (Weighted)
    "FEAT-001 (85%)" : 85
    "FEAT-002 (10%)" : 10
    "FEAT-003 (0%)" : 5
```

```mermaid
pie title Bug Resolution Status
    "Resolved" : 8
    "Pending (FEAT-001)" : 1
    "Pending (FEAT-003)" : 8
```

**By Entity Type:**

| Type | Done | In Progress | Pending | Partial | Total |
|------|------|-------------|---------|---------|-------|
| Features | 0 | 2 | 1 | 0 | 3 |
| Enablers (FEAT-001) | 2 | 2 | 0 | 0 | 4 |
| Enablers (FEAT-002) | 1 | 0 | 5 | 1 | 7 |
| Enablers (FEAT-003) | 0 | 0 | 7 | 0 | 7 |
| Bugs (FEAT-001) | 8 | 0 | 1 | 0 | 9 |
| Bugs (FEAT-003) | 0 | 0 | 8 | 0 | 8 |
| Decisions | 6 | 0 | 0 | 0 | 6 |
| Discoveries | 2 | 0 | 0 | 0 | 2 |

---

## 6. Gantt with Dependencies

> Detailed schedule with dependency chains (`after` keyword), milestones, and today marker.

```mermaid
gantt
    title EPIC-001: OSS Release - Detailed Gantt with Dependencies
    dateFormat YYYY-MM-DD
    axisFormat %m-%d
    todayMarker stroke-width:3px,stroke:#f00,opacity:0.5

    section FEAT-001: CI Fixes (85%)
    EN-001 Fix Plugin Validation         :done, f1en001, 2026-02-10, 1d
    BUG-002 CLI projects list crash      :done, f1bug002, 2026-02-10, 1d
    BUG-003 Bootstrap test missing dir   :done, f1bug003, 2026-02-10, 1d
    EN-003 Fix Validation Regressions    :done, f1en003, after f1en001, 1d
    EN-002 Fix Test Infrastructure       :active, f1en002, 2026-02-10, 4d
    BUG-007 Synthesis content test       :done, f1bug007, 2026-02-11, 1d
    EN-004 Fix Pre-commit Hook           :active, f1en004, 2026-02-11, 3d
    BUG-010 Session hook warning         :done, f1bug010, 2026-02-11, 1d
    BUG-011 Pytest hook python-only      :f1bug011, after f1bug010, 2d

    section FEAT-002: Research (10%)
    EN-101 OSS Best Practices Research   :done, f2en101, 2026-01-31, 1d
    EN-107 Current State Analysis        :done, f2en107, 2026-01-31, 1d
    EN-102 Claude Code Best Practices    :f2en102, 2026-02-13, 3d
    EN-103 CLAUDE.md Optimization Res.   :f2en103, 2026-02-13, 3d
    EN-104 Plugins Research              :f2en104, after f2en102, 2d
    EN-105 Skills Research               :f2en105, after f2en103, 2d
    EN-106 Decomposition Research        :f2en106, after f2en104, 2d

    section FEAT-003: CLAUDE.md Opt. (0%)
    EN-201 Worktracker Extraction        :f3en201, after f2en106, 2d
    EN-202 CLAUDE.md Rewrite             :f3en202, after f3en201, 3d
    EN-203 TODO Section Migration        :f3en203, after f3en201, 2d
    EN-206 Context Distribution          :f3en206, after f3en201, 7d
    EN-207 Worktracker Agents            :f3en207, after f3en201, 7d
    EN-204 Validation & Testing          :f3en204, after f3en202, 2d
    EN-205 Documentation Update          :f3en205, after f3en204, 2d

    section Milestones
    FEAT-001 CI Green                    :milestone, m1, after f1bug011, 0d
    FEAT-002 Research Complete           :milestone, m2, after f2en106, 0d
    FEAT-003 Optimization Complete       :milestone, m3, after f3en205, 0d
    EPIC-001 OSS Ready                   :milestone, m4, after f3en205, 0d
```

**Actual vs Estimated:**

| Item | Start | End | Duration | Basis |
|------|-------|-----|----------|-------|
| EN-001 | 2026-02-10 | 2026-02-11 | 1 day | actual |
| EN-003 | 2026-02-11 | 2026-02-11 | < 1 day | actual |
| BUG-002, BUG-003 | 2026-02-10 | 2026-02-10 | < 1 day | actual |
| BUG-007, BUG-010 | 2026-02-11 | 2026-02-11 | < 1 day | actual |
| EN-101, EN-107 | 2026-01-31 | 2026-01-31 | < 1 day | actual |
| EN-102 through EN-106 | 2026-02-13+ | — | 2-3 days each | estimated (effort pts) |
| EN-201 through EN-207 | 2026-02-20+ | — | 2-7 days each | estimated (effort pts) |

---

## Warnings

All diagrams follow **WORKTRACKER.md as the single source of truth**. State drift was detected:

| Entity | WORKTRACKER.md | Entity File | Delta |
|--------|---------------|-------------|-------|
| FEAT-002 | 10%, 5 EN pending | 100%, all EN complete | Entity file has more current state |
| FEAT-003 | 0%, all EN pending | 49%, 3 EN complete | Entity file has more current state |
| EN-101 | partial | partial (100% research) | Consistent but status vocabulary unclear |

A status reconciliation pass is recommended to align entity files with WORKTRACKER.md.

---

*Generated by wt-visualizer v1.0.0 — Consolidated by main context*
*Source diagrams: hierarchy, timeline, status, dependencies, progress, gantt*
