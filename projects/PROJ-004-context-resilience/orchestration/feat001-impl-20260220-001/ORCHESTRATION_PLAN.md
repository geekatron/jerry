# FEAT-001 Implementation Orchestration Plan

> **Workflow ID:** feat001-impl-20260220-001
> **Criticality:** C3 (implements ADR-SPIKE002-002, creates bounded context)
> **Pattern:** Sequential phases with parallel fan-out per phase
> **Predecessor:** spike002-cli-integration-20260219-001

## Document Sections

| Section | Purpose |
|---------|---------|
| [Workflow Diagram](#workflow-diagram) | Visual execution flow |
| [Phase Definitions](#phase-definitions) | What each phase delivers |
| [Quality Gates](#quality-gates) | Adversarial review points |
| [Agent Assignments](#agent-assignments) | Who does what |
| [Critical Path](#critical-path) | Bottleneck analysis |

---

## Workflow Diagram

```
Phase 1: FOUNDATION (fan-out, 3 parallel)
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  en-001-impl │  │  en-002-impl │  │  st-001-impl │
│  FileSys     │  │  Config      │  │  Resumption  │
│  Session     │  │  Threshold   │  │  Schema      │
│  Repository  │  │  Adapter     │  │  Protocol    │
│  3-4h        │  │  1h          │  │  2-3h        │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       └─────────────────┼─────────────────┘
                         ▼
              ╔════════════════════╗
              ║  QG-1: Foundation  ║  C2: S-007, S-002, S-014
              ║  Review (adv-scorer)║
              ╚════════════════════╝
                         │
            ┌────────────┴────────────┐
            ▼                         ▼
Phase 2: BOUNDED CONTEXT (fan-out, 2 parallel)
┌──────────────┐           ┌──────────────┐
│  en-003-impl │           │  en-005-impl │
│  ctx_monitor │           │  PreToolUse  │
│  Bounded Ctx │           │  Staleness   │
│  Foundation  │           │  Detection   │
│  4-6h        │           │  2-3h        │
└──────┬───────┘           └──────┬───────┘
       │                          │
       ▼                          │
Phase 3: APPLICATION SERVICES     │
┌──────────────┐                  │
│  en-004-impl │                  │
│  FillEstim + │                  │
│  ResumptGen  │                  │
│  3-5h        │                  │
└──────┬───────┘                  │
       └─────────────────┬────────┘
                         ▼
              ╔════════════════════╗
              ║  QG-2: Bounded Ctx ║  C3: S-007,S-002,S-014,
              ║  + Services Review ║      S-004,S-012,S-013
              ╚════════════════════╝
                         │
       ┌─────────────────┼─────────────────┐
       ▼                 ▼                 ▼
Phase 4: CLI + RULES (fan-out, 3 parallel)
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  en-006-impl │  │  st-002-impl │  │ spike-003    │
│  jerry hooks │  │  AE-006      │  │ OQ-9 +       │
│  CLI Cmds    │  │  Sub-Rules   │  │ Method C     │
│  1-1.5h      │  │  1h          │  │ 3h           │
└──────┬───────┘  └──────────────┘  └──────────────┘
       │
       ▼
Phase 5: HOOK INTEGRATION
┌──────────────┐
│  en-007-impl │
│  Hook        │
│  Wrappers +  │
│  hooks.json  │
│  1-2h        │
└──────┬───────┘
       ▼
              ╔════════════════════╗
              ║  QG-3: Integration ║  C3: S-007,S-002,S-014,
              ║  Review            ║      S-004,S-012,S-013
              ╚════════════════════╝
                         │
                         ▼
Phase 6: SYSTEM VALIDATION
┌──────────────┐
│  st-003-exec │
│  Threshold   │
│  Calibration │
│  4h          │
└──────────────┘
```

---

## Phase Definitions

| Phase | Name | Items | Delivers | Criticality |
|-------|------|-------|----------|-------------|
| 1 | Foundation | EN-001, EN-002, ST-001 | Persistent sessions, threshold config, resumption schema | C2 |
| 2 | Bounded Context | EN-003, EN-005 | `src/context_monitoring/` domain+infra, staleness service | C3 |
| 3 | App Services | EN-004 | ContextFillEstimator, ResumptionContextGenerator | C3 |
| 4 | CLI + Rules | EN-006, ST-002, SPIKE-003 | `jerry hooks` commands, AE-006 sub-rules, validation | C2-C3 |
| 5 | Integration | EN-007 | Hook wrappers + hooks.json registration | C2 |
| 6 | Validation | ST-003 | Threshold calibration data + documentation | C2 |

---

## Quality Gates

| Gate | After | Criticality | Strategies | Purpose |
|------|-------|-------------|------------|---------|
| QG-1 | Phase 1 | C2 | S-007, S-002, S-014 | Verify foundation correctness before building on it |
| QG-2 | Phase 3 | C3 | S-007, S-002, S-014, S-004, S-012, S-013 | Verify bounded context architecture before CLI wiring |
| QG-3 | Phase 5 | C3 | S-007, S-002, S-014, S-004, S-012, S-013 | Verify end-to-end integration before validation |

All gates: threshold >= 0.92, minimum 3 iterations (H-14), adv-scorer agent.

---

## Agent Assignments

| Agent ID | Entity | Type | Model | Approach |
|----------|--------|------|-------|----------|
| en-001-impl | EN-001 | general-purpose | sonnet | BDD test-first (H-20), follow EventSourcedWorkItemRepository pattern |
| en-002-impl | EN-002 | general-purpose | sonnet | BDD test-first, follow existing config patterns |
| st-001-impl | ST-001 | general-purpose | sonnet | Schema design + protocol doc, validation tests |
| en-003-impl | EN-003 | general-purpose | sonnet | BDD test-first, hexagonal layers, value objects + events |
| en-005-impl | EN-005 | general-purpose | sonnet | BDD test-first, staleness detection service |
| en-004-impl | EN-004 | general-purpose | sonnet | BDD test-first, application services + ports |
| en-006-impl | EN-006 | general-purpose | sonnet | BDD test-first, CLI adapter + parser + bootstrap |
| st-002-impl | ST-002 | general-purpose | sonnet | Update quality-enforcement.md (AE-002 auto-C3) |
| spike-003-exec | SPIKE-003 | general-purpose | sonnet | ps-researcher: validation research |
| en-007-impl | EN-007 | general-purpose | sonnet | Hook wrapper scripts + hooks.json |
| st-003-exec | ST-003 | general-purpose | sonnet | ps-validator: threshold calibration |
| qg-*-scorer | QG-1/2/3 | general-purpose | sonnet | adv-scorer: S-014 LLM-as-Judge |

---

## Critical Path

```
EN-001 (3-4h) → EN-003 (4-6h) → EN-004 (3-5h) → EN-006 (1-1.5h) → EN-007 (1-2h) → ST-003 (4h)
Total critical path: 16.5-22.5h
+ 3 quality gates: ~2-3h each = 6-9h
Grand total: 22.5-31.5h on critical path
```

**Parallelism savings:** EN-002 (1h) and ST-001 (2-3h) run alongside EN-001. EN-005 (2-3h) runs alongside EN-003. ST-002 (1h) and SPIKE-003 (3h) run alongside EN-006. Total off-critical-path work saved: ~10h wall-clock.

---

## Metadata

```yaml
workflow_id: "feat001-impl-20260220-001"
created_at: "2026-02-20"
created_by: "Claude (orchestrator)"
feature: "FEAT-001"
epic: "EPIC-001"
project: "PROJ-004"
```
