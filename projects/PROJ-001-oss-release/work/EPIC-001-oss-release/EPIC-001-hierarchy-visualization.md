# EPIC-001 Hierarchy Visualization

**Generated:** 2026-02-10
**Root Entity:** EPIC-001
**Diagram Type:** hierarchy
**Entities Included:** 14
**Max Depth Reached:** 5 (EPIC -> FEAT -> EN -> BUG -> TASK)
**Scope:** Full EPIC-001 (OSS Release Preparation)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Hierarchy Diagram](#hierarchy-diagram) | Complete Mermaid flowchart of EPIC-001 entity tree |
| [Legend](#legend) | Color coding and line style explanation |
| [Entity Inventory](#entity-inventory) | Tabular listing of all entities with metadata |
| [Dependency Map](#dependency-map) | Dependency relationships between entities |
| [Key Observations](#key-observations) | Critical path, progress, and blockers |
| [Metadata](#metadata) | Generation details |

---

## Hierarchy Diagram

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
    EN001["EN-001\nFix Plugin Validation\n(in_progress)"]
    EN002["EN-002\nFix Test Infrastructure\n(pending)"]

    %% --- Bug Layer ---
    BUG001["BUG-001\nMarketplace manifest schema error\n(in_progress | major)"]
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
    style EN001 fill:#87CEEB,stroke:#4682B4,color:#000
    style BUG001 fill:#87CEEB,stroke:#4682B4,color:#000

    %% Pending / backlog items: gray (#D3D3D3)
    style EN002 fill:#D3D3D3,stroke:#808080,color:#000
    style BUG004 fill:#D3D3D3,stroke:#808080,color:#000
    style BUG005 fill:#D3D3D3,stroke:#808080,color:#000
    style TASK001 fill:#D3D3D3,stroke:#808080,color:#000
    style TASK002 fill:#D3D3D3,stroke:#808080,color:#000
    style TASK003 fill:#D3D3D3,stroke:#808080,color:#000

    %% Decision: light purple for accepted decisions
    style DEC001 fill:#DDA0DD,stroke:#800080,color:#000
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
| 3 | EN-001 | Enabler | Fix Plugin Validation | in_progress | high | FEAT-001 | Blue |
| 4 | EN-002 | Enabler | Fix Test Infrastructure | pending | medium | FEAT-001 | Gray |
| 5 | BUG-001 | Bug | Marketplace manifest schema error: `keywords` not allowed | in_progress | high | EN-001 | Blue |
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
| Completed | 2 | 15% |
| In Progress | 4 | 31% |
| Pending / Backlog | 7 | 54% |
| **Total** | **13** | **100%** |

(DEC-001 excluded from status distribution as it is a decision artifact, not a deliverable work item.)

---

## Dependency Map

```mermaid
flowchart LR
    %% Critical dependency chain for EN-001
    TASK001["TASK-001\nAdd keywords to schema"] --> TASK002["TASK-002\nAdd validation tests"]
    TASK001 --> TASK003["TASK-003\nSpecify validator class"]
    DEC001["DEC-001\nValidator class decision"] -.->|informs| TASK003

    %% Cross-references
    BUG002["BUG-002\nCLI crash"] -.->|same root cause| BUG003["BUG-003\nBootstrap test"]
    BUG005["BUG-005\nProject validation"] -.->|related| BUG003

    %% Enabler sequencing
    EN001["EN-001\nPlugin Validation"] -.->|suggested before| EN002["EN-002\nTest Infrastructure"]

    style TASK001 fill:#D3D3D3,stroke:#808080,color:#000
    style TASK002 fill:#D3D3D3,stroke:#808080,color:#000
    style TASK003 fill:#D3D3D3,stroke:#808080,color:#000
    style DEC001 fill:#DDA0DD,stroke:#800080,color:#000
    style BUG002 fill:#90EE90,stroke:#228B22,color:#000
    style BUG003 fill:#90EE90,stroke:#228B22,color:#000
    style BUG005 fill:#D3D3D3,stroke:#808080,color:#000
    style EN001 fill:#87CEEB,stroke:#4682B4,color:#000
    style EN002 fill:#D3D3D3,stroke:#808080,color:#000
```

---

## Key Observations

### 1. Critical Path

The critical path to unblocking PR #6 is:

```
TASK-001 (add keywords to schema)
  -> TASK-002 (add validation tests)
  -> TASK-003 (specify validator class)
  -> EN-001 complete
  -> BUG-004 fix (transcript pipeline)
  -> BUG-005 fix (project validation)
  -> EN-002 complete
  -> FEAT-001 complete
  -> EPIC-001 complete
```

**TASK-001 is the single most critical unstarted item.** It is the root cause fix for BUG-001 and blocks both TASK-002 and TASK-003. Completing TASK-001 would unblock the entire EN-001 work stream.

### 2. Progress Assessment

- **Overall Progress:** ~15% (2 of 13 deliverable items completed)
- **Completed:** BUG-002 and BUG-003 (both resolved by committing `projects/` directory to git -- same root cause, single fix)
- **Active Work:** EN-001 / BUG-001 is the current focus area with 3 tasks in backlog
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
- **Status Color Coding:** Enabled (Blue=in_progress, Green=completed, Gray=pending/backlog, Purple=decision)
- **Warnings:** None

---

*Generated by wt-visualizer v1.0.0*
