# FEAT-002 Orchestration Plan

<!--
DOCUMENT: ORCHESTRATION_PLAN.md
VERSION: 1.0.0
FEATURE: FEAT-002 (Implementation)
CREATED: 2026-01-26 per DISC-001 restructuring
-->

---

## Workflow Overview

| Attribute | Value |
|-----------|-------|
| **Workflow ID** | feat-002-implementation-20260126-001 |
| **Feature** | FEAT-002: Transcript Skill Implementation |
| **Status** | ACTIVE |
| **Created** | 2026-01-26 |
| **Updated** | 2026-01-28 (Group 2 started) |
| **Gates** | GATE-5, GATE-6 (GATE-7/EN-012 moved to FEAT-003 per DISC-002) |

---

## L0: Executive Summary (ELI5)

```
FEAT-002: BUILD THE TRANSCRIPT SKILL (Updated per DEC-003)
==========================================================

Think of building a FACTORY that processes meeting recordings:

┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   GROUP 1: BUILD THE CORE MACHINES (SEQUENTIAL)                            │
│   ─────────────────────────────────────────────                            │
│                                                                            │
│   ┌─────────────┐         ┌─────────────┐                                 │
│   │  MACHINE 1  │         │  MACHINE 2  │                                 │
│   │  ts-parser  │────────▶│ ts-extractor│                                 │
│   │  (reads VTT)│         │ (finds items)│                                 │
│   │   EN-007    │         │   EN-008    │                                 │
│   └─────────────┘         └──────┬──────┘                                 │
│                                  │                                         │
│   GROUP 2: CONTEXT & FORMATTING (PARALLEL)                                 │
│   ────────────────────────────────────────                                 │
│                                  │                                         │
│   ┌─────────────────┐     ┌──────┴──────┐                                 │
│   │  MACHINE 3      │     │  MACHINE 4  │                                 │
│   │  ts-formatter   │     │  Context    │                                 │
│   │  (packages)     │     │  Injection  │                                 │
│   │    EN-016       │     │   EN-013    │                                 │
│   └────────┬────────┘     └─────────────┘                                 │
│            │                                                               │
│   GROUP 3: MIND MAP GENERATION (SEQUENTIAL) ◀── NEW per DEC-003           │
│   ─────────────────────────────────────────                                │
│            │                                                               │
│   ┌────────▼────────┐                                                     │
│   │  MACHINE 5      │  Depends on EN-016 (ts-formatter)                   │
│   │  Mind Map Gen   │                                                     │
│   │  (visualize)    │                                                     │
│   │    EN-009       │                                                     │
│   └────────┬────────┘                                                     │
│            │                                                               │
│   ╔════════╧════════╗                                                     │
│   ║  ★ GATE-5 ★     ║  Core Implementation Review                         │
│   ╚════════╤════════╝                                                     │
│            │                                                               │
│   GROUP 4: INTEGRATION & VALIDATION (PARALLEL)                             │
│   ────────────────────────────────────────────                             │
│            │                                                               │
│   ┌────────┴────────┐  ┌─────────────┐  ┌─────────────┐                  │
│   │  MACHINE 6      │  │  MACHINE 7  │  │  MACHINE 8  │                  │
│   │  Worktracker    │  │  Domain     │  │  Validation │                  │
│   │  Integration    │  │  Contexts   │  │  & Tests    │                  │
│   │    EN-011       │  │   EN-014    │  │   EN-015    │                  │
│   └────────┬────────┘  └──────┬──────┘  └──────┬──────┘                  │
│            └─────────────────┬┴────────────────┘                          │
│                              │                                             │
│   ╔══════════════════════════╧══════════════╗                             │
│   ║  ★ GATE-6 ★  Functionality Review       ║                             │
│   ╚═════════════════════════════════════════╝                             │
│                                                                            │
│   [EN-012 CLI moved to FEAT-003 per DISC-002 - Above and Beyond scope]    │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

"We build each machine, test it, then connect them into a working factory."
```

---

## L1: Implementation Pipeline (Engineer)

```
FEAT-002 IMPLEMENTATION WORKFLOW (Updated per DEC-003)
======================================================

PREREQUISITE: FEAT-001 Complete (All 4 Gates Passed ✓)
               DISC-001 Alignment Analysis Complete ✓
               DEC-003 Execution Order Correction ✓

╔═══════════════════════════════════════════════════════════════════════════╗
║  GROUP 1: CORE AGENTS (SEQUENTIAL)                                        ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  ┌───────────────────────────┐      ┌───────────────────────────┐        ║
║  │        EN-007             │      │        EN-008             │        ║
║  │   ts-parser Agent         │─────▶│   ts-extractor Agent      │        ║
║  │   ──────────────────      │      │   ──────────────────      │        ║
║  │   TASK-101..105           │      │   TASK-106..112           │        ║
║  │   Status: GATE-5 PASSED ✓ │      │   Status: GATE-5 PASSED ✓ │        ║
║  │                           │      │                           │        ║
║  │   Implements:             │      │   Implements:             │        ║
║  │   - VTT processing        │      │   - Action items (FR-006) │        ║
║  │   - SRT processing        │      │   - Decisions (FR-007)    │        ║
║  │   - Plain text            │      │   - Questions (FR-008)    │        ║
║  │   - Format detection      │      │   - Topics (FR-009)       │        ║
║  │   - Timestamp normaliz.   │      │   - Speakers (PAT-003)    │        ║
║  │   - Defensive parsing     │      │   - Tiered extract (PAT-001)│       ║
║  │                           │      │   - Citations (PAT-004)   │        ║
║  └───────────────────────────┘      └───────────────────────────┘        ║
╚═══════════════════════════════════════════════════════════════════════════╝
                              │
                              ▼
╔═══════════════════════════════════════════════════════════════════════════╗
║  GROUP 2: CONTEXT & FORMATTING (PARALLEL)                                 ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  ┌───────────────────────────┐      ┌───────────────────────────┐        ║
║  │        EN-016             │      │        EN-013             │        ║
║  │   ts-formatter Agent      │      │   Context Injection       │        ║
║  │   ──────────────────      │      │   ──────────────────      │        ║
║  │   TASK-113..119           │      │   TASK-120..125           │        ║
║  │   Status: pending         │      │   Status: pending         │        ║
║  │                           │      │                           │        ║
║  │   Implements:             │      │   Implements:             │        ║
║  │   - 8-file packet (ADR-002)│     │   - SKILL.md context      │        ║
║  │   - Token counting        │      │   - AGENT.md context      │        ║
║  │   - File splitting (ADR-004)│    │   - Template variables    │        ║
║  │   - Anchors (ADR-003)     │      │   - YAML-only per DEC-002 │        ║
║  │   - Backlinks injection   │      │                           │        ║
║  │   *Absorbs EN-010*        │      │                           │        ║
║  └─────────────┬─────────────┘      └───────────────────────────┘        ║
╚════════════════╪══════════════════════════════════════════════════════════╝
                 │
                 ▼
╔═══════════════════════════════════════════════════════════════════════════╗
║  GROUP 3: MIND MAP GENERATION (SEQUENTIAL) ◀── NEW per DEC-003            ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  ┌───────────────────────────┐                                           ║
║  │        EN-009             │  Blocked By: EN-016 (ts-formatter)        ║
║  │   Mind Map Generator      │                                           ║
║  │   ──────────────────      │                                           ║
║  │   TASK-001..004*          │  *Enabler-scoped numbering per DEC-003    ║
║  │   Status: pending         │                                           ║
║  │                           │                                           ║
║  │   Implements:             │  Tasks:                                   ║
║  │   - Mermaid diagrams      │  - TASK-001: Mermaid Generator            ║
║  │   - ASCII rendering       │  - TASK-002: ASCII Generator              ║
║  │   - Visual hierarchy      │  - TASK-003: Deep Link Embedding          ║
║  │   - Deep links (ADR-003)  │  - TASK-004: Unit Tests                   ║
║  │                           │                                           ║
║  └───────────────────────────┘                                           ║
║                             │                                             ║
║              ╔══════════════╧══════════════╗                              ║
║              ║  ★ GATE-5: Core Review ★    ║                              ║
║              ║  Human Approval Required    ║                              ║
║              ╚══════════════╤══════════════╝                              ║
╚═════════════════════════════╪═════════════════════════════════════════════╝
                              │
                              ▼
╔═══════════════════════════════════════════════════════════════════════════╗
║  GROUP 4: INTEGRATION & VALIDATION (PARALLEL)                             ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  ┌───────────────────────────┐      ┌───────────────────────────┐        ║
║  │        EN-011             │      │        EN-014             │        ║
║  │   Worktracker Integration │      │   Domain Context Files    │        ║
║  │   ──────────────────      │      │   ──────────────────      │        ║
║  │   (legacy tasks)          │      │   TASK-126..130           │        ║
║  │   Status: pending         │      │   Status: pending         │        ║
║  │                           │      │                           │        ║
║  │   Implements:             │      │   Implements:             │        ║
║  │   - Work item suggestions │      │   - general.yaml          │        ║
║  │   - Task integration      │      │   - transcript.yaml       │        ║
║  │                           │      │   - meeting.yaml          │        ║
║  └───────────────────────────┘      └───────────────────────────┘        ║
║                                                                           ║
║  ┌───────────────────────────┐                                           ║
║  │        EN-015             │                                           ║
║  │   Validation & Tests      │                                           ║
║  │   ──────────────────      │                                           ║
║  │   TASK-131..138           │  (TASK-138 added per DEC-003:D-005)       ║
║  │   Status: pending         │                                           ║
║  │                           │                                           ║
║  │   Implements:             │                                           ║
║  │   - Golden dataset        │                                           ║
║  │   - Edge case transcripts │                                           ║
║  │   - Test specifications   │                                           ║
║  │   - Integration tests     │                                           ║
║  └───────────────────────────┘                                           ║
║                             │                                             ║
║              ╔══════════════╧══════════════╗                              ║
║              ║  ★ GATE-6: Func. Review ★   ║                              ║
║              ║  Human Approval Required    ║                              ║
║              ╚══════════════╤══════════════╝                              ║
╚═════════════════════════════╪═════════════════════════════════════════════╝
                              │
                              ▼
                    ╔═════════════════════════╗
                    ║  TRANSCRIPT SKILL       ║
                    ║  IMPLEMENTATION         ║
                    ║  COMPLETE               ║
                    ╚═════════════════════════╝

[EN-012 CLI Interface moved to FEAT-003 per DISC-002 - Above and Beyond scope]
```

---

## L2: Strategic Considerations (Architect)

### Enabler Restructuring (DISC-001 + DEC-003)

The following changes were made per DISC-001 Alignment Analysis and DEC-003 Execution Order Correction:

| Original | New State | Rationale |
|----------|-----------|-----------|
| EN-007 | Revised → **GATE-5 PASSED** | Aligned with TDD-ts-parser.md, tasks TASK-101..105+105A+106+107 |
| EN-008 | **MAJOR Rewrite** → **GATE-5 PASSED** | 6 parallel agents → 1 ts-extractor per TDD |
| EN-009 | **RESTORED** | Mind Map Generator (Mermaid + ASCII), TASK-001..004 (enabler-scoped per DEC-003) |
| EN-010 | **DEPRECATED** | Absorbed into EN-016 per ADR-002 |
| EN-012 | **MOVED** | → FEAT-003 per DISC-002 (Above and Beyond scope) |
| EN-013 | Revised | YAML-only per SPEC Section 3, tasks renumbered |
| EN-014 | **Created** | Domain context files (general, transcript, meeting) |
| EN-015 | **Created** | Validation & test cases (TASK-138 added per DEC-003:D-005) |
| EN-016 | **RENUMBERED** | ts-formatter per TDD, absorbs EN-010 (was EN-009 per BUG-001) |

### Task ID Allocation

| Enabler | Task Range | Purpose |
|---------|------------|---------|
| EN-007 | TASK-101..105, 105A, 106, 107 | ts-parser agent (8 tasks) |
| EN-008 | TASK-106..112, 112A, 112B | ts-extractor agent (9 tasks) |
| EN-009 | TASK-001..004* | Mind Map Generator (*enabler-scoped per DEC-003) |
| EN-013 | TASK-120..125 | Context injection |
| EN-014 | TASK-126..130 | Domain context files |
| EN-015 | TASK-131..138 | Validation & tests (TASK-138 per DEC-003:D-005) |
| EN-016 | TASK-113..119 | ts-formatter agent |

### Critical Dependencies (Updated per DEC-003)

```
EN-007 (ts-parser) ────────────────┐
    │                              │
    └──▶ EN-008 (ts-extractor)     │
              │                    │  GROUP 1: SEQUENTIAL
              │                    │
╔═════════════╪════════════════════╪═════════════════════════════════════╗
║             ▼                                                          ║
║    EN-016 (ts-formatter) ◄───────────────────┐                        ║
║             │                                │  GROUP 2: PARALLEL      ║
║    EN-013 (context injection) ───────────────┤                        ║
╚═════════════╪════════════════════════════════╪═════════════════════════╝
              │                                │
              ▼                                │
╔═════════════════════════════════════════════╪═════════════════════════╗
║    EN-009 (mind-map) ◄───────────────────────┘  GROUP 3: SEQUENTIAL   ║
║             │          Blocked By: EN-016                              ║
╚═════════════╪═════════════════════════════════════════════════════════╝
              │
              ▼ [GATE-5]
╔═════════════════════════════════════════════════════════════════════╗
║    EN-011 (worktracker) ─────────┬──────────────┐                   ║
║                                  │              │  GROUP 4: PARALLEL ║
║    EN-014 (domains) ─────────────┼──────────────┤                   ║
║                                  │              │                   ║
║    EN-015 (validation) ──────────┴──────────────┘                   ║
╚═════════════════════════════════════════════════════════════════════╝
              │
              ▼ [GATE-6]

[EN-012 (CLI) moved to FEAT-003 per DISC-002]
```

### Risk Areas

| Risk | Mitigation |
|------|------------|
| EN-010 deprecation breaks references | Updated all references to point to EN-009 |
| Task ID conflicts with FEAT-001 | FEAT-002 uses TASK-101+ exclusively |
| YAML-only misunderstanding | DEC-002 and explicit notes in enablers |
| Token limit violations | ts-formatter enforces ADR-002 limits |

---

## Enabler Summary

### Active Enablers

| ID | Title | Status | Tasks | Gate |
|----|-------|--------|-------|------|
| EN-007 | ts-parser Agent Implementation | **gate-5-passed** | TASK-101..107 | GATE-5 ✓ |
| EN-008 | ts-extractor Agent Implementation | **gate-5-passed** ✓ | TASK-106..112B | GATE-5 ✓ |
| EN-009 | Mind Map Generator (Mermaid + ASCII) | pending | TASK-001..004* | GATE-5 |
| EN-011 | Worktracker Integration | pending | (legacy) | GATE-6 |
| EN-013 | Context Injection Implementation | pending | TASK-120..125 | GATE-5 |
| EN-014 | Domain Context Files | pending | TASK-126..130 | GATE-6 |
| EN-015 | Validation & Test Cases | pending | TASK-131..138 | GATE-6 |
| EN-016 | ts-formatter Agent Implementation | pending | TASK-113..119 | GATE-5 |

*EN-009 uses enabler-scoped task numbering per DEC-003:AI-004

### Deprecated/Moved Enablers

| ID | Title | Status | Rationale |
|----|-------|--------|-----------|
| EN-010 | Artifact Packaging & Deep Linking | **DEPRECATED** | Absorbed into EN-016 per ADR-002 |
| EN-012 | Skill CLI Interface | **MOVED** | → FEAT-003 per DISC-002 (Above and Beyond) |

---

## Execution Queue (Updated per DEC-003)

### Group 1: Core Agents (GATE-5)

```yaml
group: 1
mode: SEQUENTIAL
status: COMPLETE ✓
enablers:
  - EN-007  # ts-parser (foundation) - GATE-5 PASSED ✓
  - EN-008  # ts-extractor (depends on parser output) - GATE-5 PASSED ✓
gate: GATE-5
note: "Group 1 (Core Agents) complete. Ready for Group 2."
```

### Group 2: Context & Formatting (GATE-5) ← **ACTIVE**

```yaml
group: 2
mode: PARALLEL
status: in_progress  # Started 2026-01-28
execution_order: [EN-016, EN-013]  # Option A: Sequential within parallel group
enablers:
  - EN-016  # ts-formatter (first - higher effort, establishes output structure)
  - EN-013  # Context injection (second - references established patterns)
gate: GATE-5
note: "Option A execution: EN-016 first → EN-013. User approved 2026-01-28."
```

### Group 3: Mind Map Generation (GATE-5) ← NEW per DEC-003

```yaml
group: 3
mode: SEQUENTIAL
status: pending
enablers:
  - EN-009  # Mind Map Generator (depends on EN-016)
gate: GATE-5
tasks: TASK-001..004  # Enabler-scoped numbering per DEC-003:AI-004
note: "NEW group per DEC-003 - EN-009 must wait for EN-016 ts-formatter output"
```

### Group 4: Integration & Validation (GATE-6) ← Renumbered from Group 3

```yaml
group: 4
mode: PARALLEL
status: pending
enablers:
  - EN-011  # Worktracker
  - EN-014  # Domain context files
  - EN-015  # Validation & tests (TASK-138 added per DEC-003:D-005)
gate: GATE-6
note: "Renumbered from Group 3 per DEC-003"
```

**Note:** Group 4 (CLI/EN-012) moved to FEAT-003 per DISC-002 (Above and Beyond scope)

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [FEAT-002-implementation.md](./FEAT-002-implementation.md) | Feature definition |
| [DISC-001](./FEAT-002--DISC-001-enabler-alignment-analysis.md) | Alignment analysis |
| [DISC-002](./FEAT-002--DISC-002-future-scope-analysis.md) | Future scope (EN-012 → FEAT-003) |
| [DEC-003](./FEAT-002--DEC-003-orchestration-execution-order.md) | Orchestration execution order correction |
| [ORCHESTRATION.yaml](./ORCHESTRATION.yaml) | Machine-readable state (SSOT) |
| [TDD-ts-parser.md](../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md) | Parser design |
| [TDD-ts-extractor.md](../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-extractor.md) | Extractor design |
| [TDD-ts-formatter.md](../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-formatter.md) | Formatter design |
| [SPEC-context-injection.md](../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md) | Context injection spec |

---

## History

| Date | Author | Notes |
|------|--------|-------|
| 2026-01-26 | Claude | Created per DISC-001 restructuring |
| 2026-01-26 | Claude | DISC-002 executed: EN-012 moved to FEAT-003, GATE-7 removed |
| 2026-01-28 | Claude | EN-007 GATE-5 passed, EN-008 gate-5-ready |
| 2026-01-28 | Claude | **DEC-003 AI-003/AI-004 executed:** Group renumbering (Group 2→EN-013+EN-016, NEW Group 3→EN-009, old Group 3→Group 4). EN-009 tasks created with enabler-scoped numbering (TASK-001..004). |
| 2026-01-28 | Claude | **EN-008 GATE-5 PASSED:** Human approval received. Quality evidence: ps-critic (0.91 PASS), nse-qa (0.88 PASS). Group 1 (Core Agents) complete. Ready for Group 2 (EN-016 + EN-013). |
| 2026-01-28 | Claude | **Group 2 Started:** Execution strategy Option A (EN-016 first → EN-013). User approved sequential execution within parallel group. EN-016 in_progress. |
