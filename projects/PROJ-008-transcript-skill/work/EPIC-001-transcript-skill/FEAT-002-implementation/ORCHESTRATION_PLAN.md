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
| **Status** | PLANNING |
| **Created** | 2026-01-26 |
| **Gates** | GATE-5, GATE-6, GATE-7 |

---

## L0: Executive Summary (ELI5)

```
FEAT-002: BUILD THE TRANSCRIPT SKILL
====================================

Think of building a FACTORY that processes meeting recordings:

┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   PHASE 5: BUILD THE MACHINES                                              │
│   ─────────────────────────────                                            │
│                                                                            │
│   ┌─────────────┐         ┌─────────────┐                                 │
│   │  MACHINE 1  │         │  MACHINE 2  │                                 │
│   │  ts-parser  │────────▶│ ts-extractor│                                 │
│   │  (reads VTT)│         │ (finds items)│                                 │
│   └─────────────┘         └──────┬──────┘                                 │
│                                  │                                         │
│                          ┌───────┴───────┐                                │
│                          │ ★ QUALITY     │                                │
│                          │   CHECK ★     │                                │
│                          │  (GATE-5)     │                                │
│                          └───────┬───────┘                                │
│                                  │                                         │
│   PHASE 6: BUILD THE PACKAGING LINE                                        │
│   ─────────────────────────────────                                        │
│                                  │                                         │
│   ┌─────────────┐  ┌─────────────┴─────────────┐  ┌─────────────┐        │
│   │  MACHINE 3  │  │       MACHINE 4           │  │  MACHINE 5  │        │
│   │ts-formatter │  │   Context Injection       │  │ Worktracker │        │
│   │(packages)   │  │   (customization)         │  │ Integration │        │
│   └─────────────┘  └───────────────────────────┘  └─────────────┘        │
│          │                     │                         │                │
│          └─────────────────────┴─────────────────────────┘                │
│                                │                                          │
│                        ┌───────┴───────┐                                 │
│                        │ ★ QUALITY     │                                 │
│                        │   CHECK ★     │                                 │
│                        │  (GATE-6)     │                                 │
│                        └───────┬───────┘                                 │
│                                │                                          │
│   PHASE 7: OPTIONAL UPGRADE (CLI)                                         │
│   ───────────────────────────────                                         │
│                                │                                          │
│                        ┌───────┴───────┐                                 │
│                        │  MACHINE 6    │                                 │
│                        │   CLI         │                                 │
│                        │  Interface    │                                 │
│                        └───────┬───────┘                                 │
│                                │                                          │
│                        ┌───────┴───────┐                                 │
│                        │ ★ FINAL CHECK │                                 │
│                        │  (GATE-7)     │                                 │
│                        └───────────────┘                                 │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

"We build each machine, test it, then connect them into a working factory."
```

---

## L1: Implementation Pipeline (Engineer)

```
FEAT-002 IMPLEMENTATION WORKFLOW
================================

PREREQUISITE: FEAT-001 Complete (All 4 Gates Passed ✓)
               DISC-001 Alignment Analysis Complete ✓

╔═══════════════════════════════════════════════════════════════════════════╗
║  PHASE 5: CORE IMPLEMENTATION (EN-007, EN-008)                            ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  ┌───────────────────────────┐      ┌───────────────────────────┐        ║
║  │        EN-007             │      │        EN-008             │        ║
║  │   ts-parser Agent         │─────▶│   ts-extractor Agent      │        ║
║  │   ──────────────────      │      │   ──────────────────      │        ║
║  │   TASK-101..105           │      │   TASK-106..112           │        ║
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
║              │                                    │                       ║
║              └──────────────┬─────────────────────┘                       ║
║                             │                                             ║
║              ╔══════════════╧══════════════╗                              ║
║              ║  ★ GATE-5: Core Review ★    ║                              ║
║              ║  Human Approval Required    ║                              ║
║              ╚══════════════╤══════════════╝                              ║
╚═════════════════════════════╪═════════════════════════════════════════════╝
                              │
                              ▼
╔═══════════════════════════════════════════════════════════════════════════╗
║  PHASE 6: OUTPUT GENERATION (EN-016, EN-009, EN-011, EN-013-015)          ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  ┌───────────────────────────┐      ┌───────────────────────────┐        ║
║  │        EN-016             │      │        EN-009             │        ║
║  │   ts-formatter Agent      │      │   Mind Map Generator      │        ║
║  │   ──────────────────      │      │   ──────────────────      │        ║
║  │   TASK-113..119           │      │   TASK-046..049           │        ║
║  │                           │      │                           │        ║
║  │   Implements:             │      │   Implements:             │        ║
║  │   - 8-file packet (ADR-002)│     │   - Mermaid diagrams      │        ║
║  │   - Token counting        │      │   - ASCII rendering       │        ║
║  │   - File splitting (ADR-004)│    │   - Visual hierarchy      │        ║
║  │   - Anchors (ADR-003)     │      │                           │        ║
║  │   - Backlinks injection   │      │                           │        ║
║  │   *Absorbs EN-010*        │      │                           │        ║
║  └───────────────────────────┘      └───────────────────────────┘        ║
║                                                                           ║
║  ┌───────────────────────────┐                                           ║
║  │        EN-013             │                                           ║
║  │   Context Injection       │                                           ║
║  │   ──────────────────      │                                           ║
║  │   TASK-120..125           │                                           ║
║  │   - SKILL.md context      │                                           ║
║  │   - AGENT.md context      │                                           ║
║  │   - Template variables    │                                           ║
║  └───────────────────────────┘                                           ║
║                                                                           ║
║  ┌───────────────────────────┐      ┌───────────────────────────┐        ║
║  │        EN-014             │      │        EN-015             │        ║
║  │   Domain Context Files    │      │   Validation & Tests      │        ║
║  │   ──────────────────      │      │   ──────────────────      │        ║
║  │   TASK-126..130           │      │   TASK-131..137           │        ║
║  │                           │      │                           │        ║
║  │   Implements:             │      │   Implements:             │        ║
║  │   - general.yaml          │      │   - Golden dataset        │        ║
║  │   - transcript.yaml       │      │   - Edge case transcripts │        ║
║  │   - meeting.yaml          │      │   - Test specifications   │        ║
║  │   - JSON Schema           │      │   - Integration tests     │        ║
║  └───────────────────────────┘      └───────────────────────────┘        ║
║                                                                           ║
║  ┌───────────────────────────┐                                           ║
║  │        EN-011             │                                           ║
║  │   Worktracker Integration │                                           ║
║  │   ──────────────────      │                                           ║
║  │   (Existing - unchanged)  │                                           ║
║  └───────────────────────────┘                                           ║
║              │                                                            ║
║              └──────────────────────────────────────────────────────────▶ ║
║                             │                                             ║
║              ╔══════════════╧══════════════╗                              ║
║              ║  ★ GATE-6: Func. Review ★   ║                              ║
║              ║  Human Approval Required    ║                              ║
║              ╚══════════════╤══════════════╝                              ║
╚═════════════════════════════╪═════════════════════════════════════════════╝
                              │
                              ▼
╔═══════════════════════════════════════════════════════════════════════════╗
║  PHASE 7: CLI INTERFACE (EN-012) - ABOVE AND BEYOND                       ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  ┌───────────────────────────────────────────────────────────────┐       ║
║  │                          EN-012                                │       ║
║  │                   Skill CLI Interface                          │       ║
║  │                   ──────────────────                           │       ║
║  │                   (Optional Enhancement)                       │       ║
║  │                                                                │       ║
║  │   This is LITERALLY LAST - only after all core work complete   │       ║
║  └───────────────────────────────────────────────────────────────┘       ║
║                             │                                             ║
║              ╔══════════════╧══════════════╗                              ║
║              ║  ★ GATE-7: Final Review ★   ║                              ║
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
```

---

## L2: Strategic Considerations (Architect)

### Enabler Restructuring (DISC-001)

The following changes were made per DISC-001 Alignment Analysis:

| Original | New State | Rationale |
|----------|-----------|-----------|
| EN-007 | Revised | Aligned with TDD-ts-parser.md, tasks renumbered TASK-101+ |
| EN-008 | **MAJOR Rewrite** | 6 parallel agents → 1 ts-extractor per TDD |
| EN-009 | **RESTORED** | Mind Map Generator (Mermaid + ASCII), TASK-046..049 |
| EN-010 | **DEPRECATED** | Absorbed into EN-016 per ADR-002 |
| EN-013 | Revised | YAML-only per SPEC Section 3, tasks renumbered |
| EN-014 | **Created** | Domain context files (general, transcript, meeting) |
| EN-015 | **Created** | Validation & test cases |
| EN-016 | **RENUMBERED** | ts-formatter per TDD, absorbs EN-010 (was EN-009 per BUG-001) |

### Task ID Allocation

| Enabler | Task Range | Purpose |
|---------|------------|---------|
| EN-007 | TASK-101..105 | ts-parser agent |
| EN-008 | TASK-106..112 | ts-extractor agent |
| EN-009 | TASK-046..049 | Mind Map Generator (Mermaid + ASCII) |
| EN-013 | TASK-120..125 | Context injection |
| EN-014 | TASK-126..130 | Domain context files |
| EN-015 | TASK-131..137 | Validation & tests |
| EN-016 | TASK-113..119 | ts-formatter agent (renumbered from EN-009) |

### Critical Dependencies

```
EN-007 (ts-parser)
    │
    └──▶ EN-008 (ts-extractor) ──▶ [GATE-5]
              │
              └──▶ EN-016 (ts-formatter) ──▶ EN-009 (mind-map)
                        │
    EN-013 (context) ───┤
                        │
    EN-014 (domains) ───┼──▶ EN-015 (validation) ──▶ [GATE-6]
                        │
    EN-011 (worktracker)┘
                              │
                              └──▶ EN-012 (CLI) ──▶ [GATE-7]
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
| EN-007 | ts-parser Agent Implementation | pending | TASK-101..105 | GATE-5 |
| EN-008 | ts-extractor Agent Implementation | pending | TASK-106..112 | GATE-5 |
| EN-009 | ts-formatter Agent Implementation | pending | TASK-113..119 | GATE-5 |
| EN-011 | Worktracker Integration | pending | (existing) | GATE-6 |
| EN-012 | Skill CLI Interface | pending | (existing) | GATE-7 |
| EN-013 | Context Injection Implementation | pending | TASK-120..125 | GATE-5 |
| EN-014 | Domain Context Files | pending | TASK-126..130 | GATE-6 |
| EN-015 | Validation & Test Cases | pending | TASK-131..137 | GATE-6 |

### Deprecated Enablers

| ID | Title | Absorbed Into | Rationale |
|----|-------|---------------|-----------|
| EN-010 | Artifact Packaging & Deep Linking | EN-009 | ts-formatter handles all packaging per ADR-002 |

---

## Execution Queue

### Group 1: Core Agents (GATE-5)

```yaml
group: 1
mode: SEQUENTIAL
enablers:
  - EN-007  # ts-parser (foundation)
  - EN-008  # ts-extractor (depends on parser output)
gate: GATE-5
```

### Group 2: Context & Formatting (GATE-5)

```yaml
group: 2
mode: PARALLEL
enablers:
  - EN-009  # ts-formatter
  - EN-013  # Context injection
gate: GATE-5
```

### Group 3: Integration & Validation (GATE-6)

```yaml
group: 3
mode: PARALLEL
enablers:
  - EN-011  # Worktracker
  - EN-014  # Domain context files
  - EN-015  # Validation & tests
gate: GATE-6
```

### Group 4: CLI (GATE-7)

```yaml
group: 4
mode: SEQUENTIAL
enablers:
  - EN-012  # CLI interface (LAST)
gate: GATE-7
```

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [FEAT-002-implementation.md](./FEAT-002-implementation.md) | Feature definition |
| [DISC-001](./FEAT-002--DISC-001-enabler-alignment-analysis.md) | Alignment analysis |
| [ORCHESTRATION.yaml](./ORCHESTRATION.yaml) | Machine-readable state |
| [TDD-ts-parser.md](../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md) | Parser design |
| [TDD-ts-extractor.md](../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-extractor.md) | Extractor design |
| [TDD-ts-formatter.md](../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-formatter.md) | Formatter design |
| [SPEC-context-injection.md](../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md) | Context injection spec |

---

## History

| Date | Author | Notes |
|------|--------|-------|
| 2026-01-26 | Claude | Created per DISC-001 restructuring |
