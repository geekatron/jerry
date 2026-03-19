# PROJ-0037-doc-module Implementation: Orchestration Plan

> **Document ID:** PROJ-0037-ORCH-PLAN-002
> **Workflow ID:** impl-20260310-001
> **Date:** 2026-03-10
> **Status:** PLANNED
> **Criticality:** C4 (Critical — architecture-level, irreversible public API surface)
> **Quality Threshold:** >= 0.94

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Workflow Overview](#l0-workflow-overview) | Stakeholder summary |
| [L1: Technical Plan](#l1-technical-plan) | Diagram, phases, agents, barriers |
| [L2: Implementation Details](#l2-implementation-details) | State schema, path configuration, recovery |
| [Quality Gates](#quality-gates) | C4 gate definitions and adversarial strategy assignments |
| [Disclaimer](#disclaimer) | Mandatory P-043 disclaimer |

---

## L0: Workflow Overview

The doc-module implementation workflow takes the completed design artifacts from the prior design phase (doc-module-20260308-001) and builds the production `docs` bounded context in the Jerry framework. The deliverable is a working `jerry docs generate` CLI command backed by a hexagonal-architecture bounded context with Jinja2 templating, YAML-seeded data files, field sanitization, sandboxed rendering, atomic writes, and a pre-commit hook.

This workflow matters because the `docs` module is a public-facing API surface — once merged, users and downstream tooling depend on its CLI flags, template format, and output structure. Getting the security controls and architecture right at first implementation avoids expensive retroactive refactors. The C4 criticality reflects the irreversible nature of a public CLI API and the presence of trust-boundary concerns (Jinja2 rendering, YAML-sourced content, file-system writes).

---

## L1: Technical Plan

### Workflow Diagram (ASCII)

```
IMPL-20260310-001: PROJ-0037-doc-module Implementation Pipeline
================================================================

Input Artifacts (from doc-module-20260308-001)
  ├── specifications/doc-module-spec.md
  ├── security/threat-model-doc-module.md
  └── decisions/ADR-PROJ0037-001-doc-module-design.md

══════════════════════════════════════════════════════════════════
PHASE 1 — FOUNDATION (Fan-Out, Parallel)
══════════════════════════════════════════════════════════════════

  ┌─────────────────────────────┐   ┌─────────────────────────────┐
  │        eng-backend-1        │   │        eng-backend-2        │
  │  src/docs/ bounded context  │   │  templates/ + pre-commit    │
  │  ─────────────────────────  │   │  hook                       │
  │  domain/value_objects/      │   │  ─────────────────────────  │
  │  domain/ports/              │   │  .context/templates/docs/   │
  │  application/commands/      │   │    skills-table.md.jinja2   │
  │  application/handlers/      │   │    features-section.md.     │
  │  application/services/      │   │      jinja2                 │
  │  infrastructure/adapters/   │   │    _macros.jinja2           │
  │  M-1 sanitize, M-2 sandbox  │   │    skill-examples.yaml      │
  │  M-3 atomic write           │   │    features.yaml            │
  │  M-5 schema validation      │   │  scripts/check_docs.py      │
  └──────────────┬──────────────┘   └──────────────┬──────────────┘
                 │                                   │
                 └──────────────┬────────────────────┘
                                │
                                ▼
                    ╔═══════════════════════╗
                    ║      BARRIER 1        ║
                    ║   Foundation Gate     ║
                    ║   /adversary C4       ║
                    ║   All 10 strategies   ║
                    ║   >= 0.94             ║
                    ╚═══════════════════════╝
                    Creator:  eng-backend-1/2
                    Critic:   adv-scorer
                    Revision: eng-backend-1/2
                    Max iter: 10 (C4)
                                │
                                ▼

══════════════════════════════════════════════════════════════════
PHASE 2 — INTEGRATION (Sequential)
══════════════════════════════════════════════════════════════════

                    ┌─────────────────────────┐
                    │       eng-backend-3      │
                    │  CLI + Bootstrap wiring  │
                    │  ──────────────────────  │
                    │  src/interface/cli/      │
                    │    parser.py             │
                    │    _add_docs_namespace   │
                    │    generate subcommand   │
                    │    --check/--write/      │
                    │    --readme flags        │
                    │  src/bootstrap.py        │
                    │    create_docs_generator │
                    │    register command      │
                    └──────────────┬──────────┘
                                   │
                                   ▼
                    ╔═══════════════════════╗
                    ║      BARRIER 2        ║
                    ║  Integration Gate     ║
                    ║   /adversary C4       ║
                    ║   All 10 strategies   ║
                    ║   >= 0.94             ║
                    ╚═══════════════════════╝
                    Creator:  eng-backend-3
                    Critic:   adv-scorer
                    Revision: eng-backend-3
                    Max iter: 10 (C4)
                                │
                                ▼

══════════════════════════════════════════════════════════════════
PHASE 3 — VERIFICATION (Fan-Out, Parallel)
══════════════════════════════════════════════════════════════════

  ┌──────────────┐   ┌──────────────────────┐   ┌──────────────┐
  │   eng-qa     │   │    eng-architect      │   │  red-vuln    │
  │  Test Suite  │   │  Security Review      │   │ Attack Surf. │
  │  ──────────  │   │  ──────────────────   │   │ Analysis     │
  │  10 unit     │   │  M-1 field sanitize   │   │ ──────────── │
  │  4 integ.    │   │  M-2 SandboxedEnv     │   │ YAML inject  │
  │  2 golden    │   │  M-3 atomic writes    │   │ Jinja2 trust │
  │  tests/unit/ │   │  M-4 (review)         │   │ path travers │
  │  tests/      │   │  M-5 schema valid.    │   │ in --readme  │
  │  integration/│   │  hexagonal layers     │   │              │
  │  tests/      │   │  H-07, H-10, H-11     │   │              │
  │  golden/     │   │  compliance           │   │              │
  └──────┬───────┘   └──────────┬───────────┘   └──────┬───────┘
         │                      │                        │
         └──────────────────────┼────────────────────────┘
                                │
                                ▼
                    ╔═══════════════════════╗
                    ║      BARRIER 3        ║
                    ║  Verification Gate    ║
                    ║   /adversary C4       ║
                    ║   All 10 strategies   ║
                    ║   >= 0.94             ║
                    ╚═══════════════════════╝
                    Creator:  eng-qa / eng-architect / red-vuln
                    Critic:   adv-scorer
                    Revision: eng-qa / eng-architect
                    Max iter: 10 (C4)
                                │
                                ▼

══════════════════════════════════════════════════════════════════
PHASE 4 — FINAL GATE (Sequential)
══════════════════════════════════════════════════════════════════

                    ┌─────────────────────────┐
                    │       eng-reviewer       │
                    │  Architecture Compliance │
                    │  ──────────────────────  │
                    │  Hexagonal layer isol.   │
                    │  H-07, H-10, H-11        │
                    │  M-1 through M-5 verify  │
                    │  Test coverage >= 90%    │
                    │  uv run pytest --cov     │
                    └──────────────┬──────────┘
                                   │
                                   ▼
                    ╔═══════════════════════╗
                    ║      BARRIER 4        ║
                    ║   Final Gate          ║
                    ║   /adversary C4       ║
                    ║   All 10 strategies   ║
                    ║   Tournament mode     ║
                    ║   >= 0.94             ║
                    ╚═══════════════════════╝
                    Creator:  eng-reviewer
                    Critic:   adv-scorer (all 10 strategies)
                    Revision: eng-reviewer
                    Max iter: 10 (C4)
                                │
                                ▼
                    ┌─────────────────────────┐
                    │     DEPLOYMENT HELD      │
                    │  Pending human review    │
                    │  and merge approval      │
                    └─────────────────────────┘
```

---

### Pipeline Definitions

| Pipeline | Alias | Phases | Sequential/Parallel |
|----------|-------|--------|---------------------|
| impl | impl | 4 | See per-phase column |

#### Phase Breakdown

| Phase | ID | Pattern | Agents | Trigger |
|-------|----|---------|--------|---------|
| 1 — Foundation | phase-1 | Fan-Out (parallel) | eng-backend-1, eng-backend-2 | Workflow start; design artifacts present |
| 2 — Integration | phase-2 | Sequential | eng-backend-3 | Barrier 1 PASS |
| 3 — Verification | phase-3 | Fan-Out (parallel) | eng-qa, eng-architect, red-vuln | Barrier 2 PASS |
| 4 — Final Gate | phase-4 | Sequential | eng-reviewer | Barrier 3 PASS |

#### Agent Assignments

| Agent | Phase | Deliverable | Tool Tier |
|-------|-------|-------------|-----------|
| eng-backend-1 | 1 | src/docs/ bounded context (domain + application + infrastructure) | T2 |
| eng-backend-2 | 1 | .context/templates/docs/ (Jinja2 templates + YAML data) + scripts/check_docs.py | T2 |
| eng-backend-3 | 2 | CLI namespace registration + bootstrap wiring | T2 |
| eng-qa | 3 | 16 tests (10 unit, 4 integration, 2 golden) | T2 |
| eng-architect | 3 | Security control verification (M-1 through M-5) + hexagonal compliance | T1 |
| red-vuln | 3 | Attack surface analysis (YAML injection, Jinja2 trust boundary, path traversal) | T3 |
| eng-reviewer | 4 | Final architecture compliance + coverage verification | T1 |

---

### Sync Barriers

| Barrier | ID | Waits For | Condition | Quality Gate |
|---------|----|-----------|-----------|--------------|
| Foundation Gate | barrier-1 | eng-backend-1 AND eng-backend-2 | Both Phase 1 agents complete | /adversary C4, >= 0.94 |
| Integration Gate | barrier-2 | eng-backend-3 | Phase 2 agent complete | /adversary C4, >= 0.94 |
| Verification Gate | barrier-3 | eng-qa AND eng-architect AND red-vuln | All three Phase 3 agents complete | /adversary C4, >= 0.94 |
| Final Gate | barrier-4 | eng-reviewer | Phase 4 agent complete | /adversary C4 tournament, >= 0.94 |

---

## L2: Implementation Details

### State Schema (ORCHESTRATION.yaml preview)

See `ORCHESTRATION.yaml` for the full initialised state file.

### Dynamic Path Configuration

All artifact paths use dynamic identifiers derived from the workflow ID `impl-20260310-001` and the single pipeline alias `impl`:

| Path Type | Pattern | Example |
|-----------|---------|---------|
| Base | `orchestration/impl-20260310-001/` | `orchestration/impl-20260310-001/` |
| Phase output | `orchestration/impl-20260310-001/impl/{phase-id}/` | `orchestration/impl-20260310-001/impl/phase-1/` |
| Barrier | `orchestration/impl-20260310-001/cross-pollination/{barrier-id}/{direction}/` | `orchestration/impl-20260310-001/cross-pollination/barrier-1/fanin/` |
| Quality scores | `orchestration/impl-20260310-001/impl/{phase-id}/quality-scores.yaml` | — |

All paths are relative to `projects/PROJ-0037-doc-module/`.

### Input Artifact Registry

| Artifact | Path | Role |
|----------|------|------|
| B4 Spec | `specifications/doc-module-spec.md` | Implementation specification — SSOT for agent work |
| Threat Model | `security/threat-model-doc-module.md` | M-1 through M-5 security control reference |
| ADR | `decisions/ADR-PROJ0037-001-doc-module-design.md` | Architectural decisions for compliance verification |

### Execution Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Agent nesting | Max 1 level (P-003 / H-01) | Constitutional; workers must not spawn sub-workers |
| Python execution | `uv run` only (H-05) | No python/pip/pip3 direct invocation |
| Class-per-file | Enforced (H-10) | All source files in src/docs/ must contain exactly one class |
| Type hints | Required on public functions (H-11) | Standards compliance |
| Test coverage | >= 90% line coverage (H-20) | Testing standards threshold |
| Architecture | Hexagonal isolation (H-07) | Domain layer must not import infrastructure |

### Recovery Strategies

| Failure Mode | Recovery Action |
|-------------|----------------|
| Phase 1 agent partially fails | Halt fan-in; do not advance to Barrier 1; present partial result to user with specific blocker |
| Barrier quality score < 0.94 | Revision cycle (max 10 iterations per C4); after 10 with no convergence, escalate to user |
| Phase 3 red-vuln finds unmitigated CRITICAL | Block Barrier 3 PASS; eng-architect must document remediation before gate passes |
| Circuit breaker fires (> 3 hops) | Log routing history; halt; present best result; ask user per H-31 |
| MCP Memory-Keeper unavailable | Persist context to `work/.mcp-fallback/impl-20260310-001.md`; note failure in worktracker |
| uv test run fails | Agents must NOT proceed past Barrier 3 until `uv run pytest` exits 0 |

---

## Quality Gates

### Criticality Assessment

**Level:** C4 (Critical)

| Factor | Assessment |
|--------|-----------|
| Reversibility | Irreversible — public CLI API surface (`jerry docs generate`), once merged users and CI pipelines depend on flag signatures and output format |
| File scope | Architecture-level — new bounded context (~20+ files), CLI parser, bootstrap wiring, templates, pre-commit hook |
| Impact | Public-facing + security controls — trust boundary in Jinja2 renderer, YAML-sourced content, file system write operations |
| Auto-escalation | AE-001 not triggered; AE-005 applies (security-relevant code: M-1 through M-5 controls) → auto-C3 minimum; manual assessment elevates to C4 |

### Required Adversarial Strategies (C4 — All 10)

| ID | Strategy | Application Point |
|----|----------|-------------------|
| S-014 | LLM-as-Judge | All barriers — primary scoring mechanism |
| S-003 | Steelman Technique | All barriers — applied before devil's advocate (H-16) |
| S-013 | Inversion Technique | Barrier 1, 4 — "What would make this fail?" inversion on security controls |
| S-007 | Constitutional AI Critique | Barrier 4 — constitutional compliance check (H-07, H-10, H-11, P-003) |
| S-002 | Devil's Advocate | All barriers — challenge design assumptions |
| S-004 | Pre-Mortem Analysis | Barrier 2 — "Project failed; what went wrong?" on integration wiring |
| S-010 | Self-Refine | Per agent — self-review before presenting output (H-15) |
| S-012 | FMEA | Barrier 3 — failure mode analysis on security controls and test coverage |
| S-011 | Chain-of-Verification | Barrier 3, 4 — verify each claim in security review and architecture compliance |
| S-001 | Red Team Analysis | Barrier 3 — red-vuln attack surface analysis output feeds this strategy |

### Per-Barrier Quality Gate Definitions

| Barrier | Threshold | Strategies | Creator | Critic | Max Iter |
|---------|-----------|------------|---------|--------|----------|
| Barrier 1 | >= 0.94 | S-014, S-003, S-002, S-010, S-013 | eng-backend-1, eng-backend-2 | adv-scorer | 10 |
| Barrier 2 | >= 0.94 | S-014, S-003, S-002, S-010, S-004 | eng-backend-3 | adv-scorer | 10 |
| Barrier 3 | >= 0.94 | S-014, S-003, S-002, S-010, S-012, S-011, S-001 | eng-qa, eng-architect, red-vuln | adv-scorer | 10 |
| Barrier 4 | >= 0.94 | All 10 (tournament mode) | eng-reviewer | adv-scorer | 10 |

### Operational Score Bands

| Band | Score Range | Workflow Action |
|------|------------|----------------|
| PASS | >= 0.94 | Advance to next phase |
| REVISE | 0.88 – 0.93 | Targeted revision; re-score |
| REJECTED | < 0.88 | Significant rework; escalate if 3 consecutive REJECTED |

---

## Disclaimer

This orchestration plan was generated by the orch-planner agent (v2.2.0) on 2026-03-10 for project PROJ-0037-doc-module. It reflects the implementation pipeline following the completed design phase (doc-module-20260308-001). Human review is recommended before execution. This document is an internal planning artifact and does not constitute official guidance of any external organisation.

All paths in this document are relative to `projects/PROJ-0037-doc-module/` within the Jerry framework worktree unless otherwise stated.
