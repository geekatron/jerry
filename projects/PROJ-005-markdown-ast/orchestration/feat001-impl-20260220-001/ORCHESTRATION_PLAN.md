# PROJ-005 FEAT-001 Implementation: Orchestration Plan

> **Document ID:** PROJ-005-FEAT001-IMPL-ORCH-PLAN
> **Project:** PROJ-005-markdown-ast
> **Workflow ID:** `feat001-impl-20260220-001`
> **Status:** PLANNED
> **Version:** 1.0
> **Created:** 2026-02-20
> **Last Updated:** 2026-02-20

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#1-executive-summary) | L0 overview of the implementation workflow |
| [Workflow Architecture](#2-workflow-architecture) | Pipeline diagram, fan-out/fan-in pattern, phase topology |
| [Phase Definitions](#3-phase-definitions) | Detailed phase specifications with agents and story mappings |
| [Phase Transition Protocol](#4-phase-transition-protocol) | Quality gates between phases, acceptance criteria |
| [Quality Gate Definitions](#5-quality-gate-definitions) | Per-phase and per-story quality assessment |
| [Agent Registry](#6-agent-registry) | All 10 implementation agents with inputs, outputs, status |
| [State Management](#7-state-management) | State files, path structure, checkpoints |
| [Execution Constraints](#8-execution-constraints) | Constitutional and soft constraints |
| [Success Criteria](#9-success-criteria) | Per-phase and workflow exit criteria |
| [Risk Mitigations](#10-risk-mitigations) | Risk register with mitigations |
| [Recovery Strategies](#11-recovery-strategies) | Failure modes and recovery procedures |
| [Resumption Context](#12-resumption-context) | Current state and next actions |
| [Disclaimer](#disclaimer) | Agent-generated content notice |

---

## 1. Executive Summary

This orchestration plan coordinates the implementation of FEAT-001 (AST Strategy Evaluation & Library Selection) stories ST-001 through ST-010 using a **Sequential Bottleneck -> Fan-Out/Fan-In** pattern. The workflow exploits the dependency graph to maximize parallelism while respecting hard ordering constraints.

The selected stack -- **markdown-it-py v4.0.0 + mdformat v1.0.0 + mdit-py-plugins v0.5.0** -- is already validated by EN-001 (R-01 PoC) and dependencies are already installed. Each story is individually C1 (routine, <3 files, reversible within session) with S-010 self-review sufficient per story. The aggregate workflow is C2 (Standard) requiring phase-level quality gates.

**Orchestration Pattern:** Sequential Bottleneck -> Fan-Out/Fan-In (5 phases, max 4 concurrent agents)

**Criticality:** C2 (Standard) -- new code module, reversible within 1 day per story, module-level impact

**Stack Decision:** markdown-it-py v4.0.0 + mdformat v1.0.0 + mdit-py-plugins v0.5.0 (from spike-eval-20260219-001)

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `feat001-impl-20260220-001` | user |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `orchestration/feat001-impl-20260220-001/` | Dynamic |
| Pipeline Alias | `impl` | implementation pipeline |

**Artifact Output Locations:**
- Implementation artifacts: `orchestration/feat001-impl-20260220-001/impl/`
- Quality gate artifacts: `orchestration/feat001-impl-20260220-001/quality/`
- Phase transition artifacts: `orchestration/feat001-impl-20260220-001/phase-transitions/`

### 1.2 Prerequisites Satisfied

| Prerequisite | Status | Evidence |
|-------------|--------|----------|
| EN-001 (R-01 PoC) | COMPLETE | `work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/EN-001-r01-poc/R01_RESULTS.md` |
| SPIKE-001 (Library Landscape) | COMPLETE | `orchestration/spike-eval-20260219-001/ps/phase-3-synthesis/ps-synthesizer-001/library-recommendation.md` |
| SPIKE-002 (Feasibility) | COMPLETE | `orchestration/spike-eval-20260219-001/ps/phase-6-decision/ps-synthesizer-002/go-nogo-recommendation.md` |
| markdown-it-py v4.0.0 | INSTALLED | `pyproject.toml` |
| mdformat v1.0.0 | INSTALLED | `pyproject.toml` |
| mdit-py-plugins v0.5.0 | INSTALLED | `pyproject.toml` |

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram

```
 ┌──────────────────────────────────────────────────────────────┐
 │  PREREQUISITES (COMPLETE)                                    │
 │  EN-001 (R-01 PoC) COMPLETE                                  │
 │  SPIKE-001 + SPIKE-002 COMPLETE                              │
 │  Selected Stack: markdown-it-py v4 + mdformat v1             │
 └──────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
 ╔══════════════════════════════════════════════════════════════╗
 ║  PHASE 1: Sequential Bottleneck                             ║
 ║  ──────────────────────────────────────────────────────     ║
 ║  impl-st001 (JerryDocument Facade)                          ║
 ║  src/domain/markdown_ast/jerry_document.py (~130 LOC)       ║
 ║  tests/unit/domain/markdown_ast/test_jerry_document.py      ║
 ║  STATUS: PLANNED                                            ║
 ╚══════════════════════════════╦═══════════════════════════════╝
                                │
                ┌───────────────▼────────────────┐
                │    PHASE GATE 1                │
                │    Story QA: S-010 self-review │
                │    90% coverage confirmed      │
                │    All AC checkboxes verified  │
                └───────────────┬────────────────┘
                                │
          ┌─────────────────────┼───────────────────────┐
          │                     │                       │
          ▼                     ▼                       ▼
 ╔══════════════╗     ╔══════════════╗       ╔══════════════╗
 ║ PHASE 2a    ║     ║ PHASE 2b    ║       ║ PHASE 2c    ║
 ║ impl-st002  ║     ║ impl-st003  ║       ║ impl-st004  ║
 ║ Frontmatter ║     ║ Reinject    ║       ║ CLI Commands ║
 ║ Extension   ║     ║ Parser      ║       ║ ~250 LOC    ║
 ║ ~220 LOC    ║     ║ ~120 LOC    ║       ║ STATUS:     ║
 ║ STATUS:     ║     ║ STATUS:     ║       ║ PLANNED     ║
 ║ PLANNED     ║     ║ PLANNED     ║       ╚═══════════╦══╝
 ╚══════╦══════╝     ╚══════╦══════╝                   │
        │                   │                           │
        │         ╔══════════════╗                      │
        │         ║ PHASE 2d    ║                      │
        │         ║ impl-st008  ║                      │
        │         ║ Nav Table   ║                      │
        │         ║ Helpers     ║                      │
        │         ║ ~120 LOC    ║                      │
        │         ║ STATUS:     ║                      │
        │         ║ PLANNED     ║                      │
        │         ╚══════╦══════╝                      │
        │                │                              │
        └──────────┬─────┘                              │
                   │                                    │
        ┌──────────▼────────────────────────────────────┘
        │    PHASE GATE 2                               │
        │    Aggregate QA: S-007 Constitutional        │
        │    S-002 Devil's Advocate, S-014 LLM-Judge   │
        │    Threshold: >= 0.92 (C2 aggregate)         │
        └──────────┬────────────────────────────────────┘
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
 ╔══════════════╗  ╔══════════════════╗
 ║ PHASE 3a    ║  ║ PHASE 3b         ║
 ║ impl-st005  ║  ║ impl-st006       ║
 ║ /ast Skill  ║  ║ Schema Validation ║
 ║ depends on: ║  ║ depends on:       ║
 ║ ST-001+002  ║  ║ ST-001+002        ║
 ║ STATUS:     ║  ║ ~5 SP, medium     ║
 ║ PLANNED     ║  ║ STATUS: PLANNED  ║
 ╚══════╦══════╝  ╚════════╦═════════╝
        │                  │
        └────────┬──────────┘
                 │
        ┌────────▼────────────┐
        │    PHASE GATE 3     │
        │    Story QA: S-010  │
        │    self-review x2   │
        └────────┬────────────┘
                 │
          ┌──────┴──────────────────────────────────────┐
          │                                             │
          ▼                                             ▼
 ╔══════════════════╗                      ╔══════════════════╗
 ║ PHASE 4a        ║                      ║ PHASE 4b         ║
 ║ impl-st007      ║                      ║ impl-st009       ║
 ║ /worktracker    ║                      ║ Pre-commit Hook  ║
 ║ migration       ║                      ║ depends on:      ║
 ║ depends on:     ║                      ║ ST-004+006+008   ║
 ║ ST-005+006      ║                      ║ STATUS: PLANNED  ║
 ║ STATUS: PLANNED ║                      ╚════════╦═════════╝
 ╚════════╦════════╝                               │
          │                                        │
          └──────────────┬─────────────────────────┘
                         │
                ┌────────▼────────┐
                │  PHASE GATE 4   │
                │  Story QA: S-010│
                │  self-review x2 │
                └────────┬────────┘
                         │
                         ▼
 ╔═══════════════════════════════════════════════════════════════╗
 ║  PHASE 5: Sequential Completion                              ║
 ║  ─────────────────────────────────────────────────────────── ║
 ║  impl-st010 (Remaining Skill Migrations)                     ║
 ║  depends on: ST-007 + ST-005                                 ║
 ║  STATUS: PLANNED                                             ║
 ╚═══════════════════════════════╦═══════════════════════════════╝
                                 │
                        ┌────────▼────────────────┐
                        │   PHASE GATE 5 (Final)  │
                        │   S-007 Constitutional  │
                        │   S-002 Devil's Advocate│
                        │   S-014 LLM-as-Judge    │
                        │   Threshold: >= 0.92    │
                        │   Min Iterations: 3     │
                        └────────┬────────────────┘
                                 │
                                 ▼
                        [ WORKFLOW COMPLETE ]
                        FEAT-001 IMPLEMENTED
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential Bottleneck | Yes | Phase 1 (ST-001) must complete before any parallel work begins |
| Fan-Out | Yes | Phase 2: 4 parallel agents; Phase 3: 2 parallel agents; Phase 4: 2 parallel agents |
| Fan-In | Yes | Phase gates collect all wave outputs before advancing |
| Hierarchical | Yes | Main context dispatches agents (P-003 compliant, max 1 nesting level) |
| Quality Gate | Yes | S-010 per-story; S-007+S-002+S-014 at aggregate phase boundaries |

### 2.3 Story-to-Phase Mapping

| Phase | Wave | Stories | Execution Mode | Max Concurrent | SP Total |
|-------|------|---------|----------------|----------------|----------|
| 1 | Sequential | ST-001 | Sequential | 1 | 5 SP |
| 2 | Fan-Out | ST-002, ST-003, ST-004, ST-008 | Parallel | 4 | 16 SP |
| 3 | Fan-Out | ST-005, ST-006 | Parallel | 2 | 8 SP |
| 4 | Fan-Out | ST-007, ST-009 | Parallel | 2 | 5 SP |
| 5 | Sequential | ST-010 | Sequential | 1 | 5 SP |
| **Total** | | **10 stories** | | | **39 SP** |

---

## 3. Phase Definitions

### 3.1 Phase 1: Sequential Bottleneck

**Purpose:** Establish the foundational `JerryDocument` facade. All other stories build on this.

| Field | Value |
|-------|-------|
| Stories | ST-001 |
| Execution | Sequential (1 agent) |
| Model | sonnet |
| Estimated LOC | ~130 LOC |
| Blocked By | EN-001 (COMPLETE) |
| Blocks | All Phase 2 stories |
| Status | PLANNED |

**Story ST-001: JerryDocument Facade**

| Aspect | Specification |
|--------|---------------|
| Agent | impl-st001 |
| Files Created | `src/domain/markdown_ast/__init__.py`, `src/domain/markdown_ast/jerry_document.py` |
| Test Files | `tests/unit/domain/markdown_ast/__init__.py`, `tests/unit/domain/markdown_ast/test_jerry_document.py` |
| Acceptance Criteria | `parse()`, `render()`, `query()`, `transform()` methods; roundtrip; 90% coverage; type hints; docstrings |
| HARD Rules Enforced | H-07 (no external imports in domain), H-10 (one class per file), H-11, H-12, H-20, H-21 |
| Quality | S-010 self-review before phase gate |

### 3.2 Phase 2: Fan-Out Wave 1

**Purpose:** Implement the four parallel extensions that all depend only on ST-001. Run concurrently (max 4 agents).

| Story | Agent | Files | LOC | Dependencies | Status |
|-------|-------|-------|-----|-------------|--------|
| ST-002 | impl-st002 | `src/domain/markdown_ast/frontmatter.py` + tests | ~220 | ST-001 | PLANNED |
| ST-003 | impl-st003 | `src/domain/markdown_ast/reinject.py` + tests | ~120 | ST-001 | PLANNED |
| ST-004 | impl-st004 | `src/interface/cli/ast_commands.py` + tests | ~250 | ST-001 | PLANNED |
| ST-008 | impl-st008 | `src/domain/markdown_ast/nav_table.py` + tests | ~120 | ST-001 | PLANNED |

**Story ST-002: Blockquote Frontmatter Extension**

| Aspect | Specification |
|--------|---------------|
| Agent | impl-st002 |
| Files Created | `src/domain/markdown_ast/frontmatter.py`, `tests/unit/domain/markdown_ast/test_frontmatter.py` |
| Acceptance Criteria | Extract key-value pairs; multiline values; inline markdown; write-back single field; add new field; works on WORKTRACKER/skill/spike entities; 90% coverage |
| HARD Rules Enforced | H-07, H-10, H-11, H-12, H-20, H-21 |

**Story ST-003: L2-REINJECT Parser**

| Aspect | Specification |
|--------|---------------|
| Agent | impl-st003 |
| Files Created | `src/domain/markdown_ast/reinject.py`, `tests/unit/domain/markdown_ast/test_reinject.py` |
| Acceptance Criteria | Parse `<!-- L2-REINJECT: rank=N, tokens=N, content="..." -->` comments; extract all attributes; return typed collection; 90% coverage |
| HARD Rules Enforced | H-07, H-10, H-11, H-12, H-20, H-21 |

**Story ST-004: CLI Commands**

| Aspect | Specification |
|--------|---------------|
| Agent | impl-st004 |
| Files Created | `src/interface/cli/ast_commands.py`, `tests/unit/interface/cli/test_ast_commands.py` |
| Acceptance Criteria | `jerry ast parse|render|validate|query` subcommands; JSON AST output; exit codes 0/1/2; `--help` docs; 90% coverage |
| HARD Rules Enforced | H-08 (no infra imports in interface), H-10, H-11, H-12, H-20, H-21 |

**Story ST-008: Navigation Table Helpers**

| Aspect | Specification |
|--------|---------------|
| Agent | impl-st008 |
| Files Created | `src/domain/markdown_ast/nav_table.py`, `tests/unit/domain/markdown_ast/test_nav_table.py` |
| Acceptance Criteria | Detect navigation table presence; extract section entries; validate anchor links; insert/update nav tables per H-23/H-24 rules; 90% coverage |
| HARD Rules Enforced | H-07, H-10, H-11, H-12, H-20, H-21, H-23, H-24 |

### 3.3 Phase 3: Fan-Out Wave 2

**Purpose:** Implement the skill interface and schema validation, both depending on ST-001 + ST-002.

| Story | Agent | Files | SP | Dependencies | Status |
|-------|-------|-------|----|-------------|--------|
| ST-005 | impl-st005 | `skills/ast/SKILL.md` + supporting files | 3 | ST-001, ST-002 | PLANNED |
| ST-006 | impl-st006 | `src/domain/markdown_ast/schema_validator.py` + tests | 5 | ST-001, ST-002 | PLANNED |

**Story ST-005: /ast Claude Skill**

| Aspect | Specification |
|--------|---------------|
| Agent | impl-st005 |
| Files Created | `skills/ast/SKILL.md`, `skills/ast/agents/` (if needed) |
| Acceptance Criteria | Skill invokable via `/ast`; reads SKILL.md; provides AST operations via domain layer; documents triggers in mandatory-skill-usage.md if H-22 applies |
| HARD Rules Enforced | H-23, H-24 (navigation table in SKILL.md), H-22 (skill trigger map if applicable) |

**Story ST-006: Schema Validation Engine**

| Aspect | Specification |
|--------|---------------|
| Agent | impl-st006 |
| Files Created | `src/domain/markdown_ast/schema_validator.py`, `tests/unit/domain/markdown_ast/test_schema_validator.py` |
| Acceptance Criteria | Entity schema definitions (Story, Task, Feature, Epic, Enabler, Spike); validate frontmatter fields; return structured ValidationResult; report missing/invalid fields; 90% coverage |
| HARD Rules Enforced | H-07, H-10, H-11, H-12, H-20, H-21 |

### 3.4 Phase 4: Fan-Out Wave 3

**Purpose:** Migration and tooling integration -- both parallel, each depending on different Phase 3 outputs.

| Story | Agent | Dependencies | SP | Status |
|-------|-------|-------------|-----|--------|
| ST-007 | impl-st007 | ST-005 + ST-006 | 3 | PLANNED |
| ST-009 | impl-st009 | ST-004 + ST-006 + ST-008 | 2 | PLANNED |

**Story ST-007: /worktracker Migration**

| Aspect | Specification |
|--------|---------------|
| Agent | impl-st007 |
| Files Modified | `/worktracker` skill files to use `JerryDocument` + frontmatter ops instead of regex |
| Acceptance Criteria | /worktracker operations (read/write frontmatter) use new AST layer; existing tests continue to pass; regression-free migration |
| HARD Rules Enforced | H-11, H-12; H-20 (tests must pass before story complete) |

**Story ST-009: Pre-commit Hook**

| Aspect | Specification |
|--------|---------------|
| Agent | impl-st009 |
| Files Modified/Created | `.pre-commit-config.yaml` or hook script; integration with `jerry ast validate` |
| Acceptance Criteria | Hook invokes `jerry ast validate` on staged markdown files; blocks commit on schema violations; passes on valid files; 2 SP |
| HARD Rules Enforced | H-05 (uv run in hook scripts), H-11, H-12 |

### 3.5 Phase 5: Sequential Completion

**Purpose:** Final skill migrations -- depends on both ST-007 and ST-005 being complete.

| Story | Agent | Dependencies | SP | Status |
|-------|-------|-------------|-----|--------|
| ST-010 | impl-st010 | ST-007 + ST-005 | 5 | PLANNED |

**Story ST-010: Remaining Skill Migrations**

| Aspect | Specification |
|--------|---------------|
| Agent | impl-st010 |
| Files Modified | All remaining skills that use regex-based markdown parsing |
| Acceptance Criteria | Skills identified in scope; migrated to AST layer; existing tests pass; no regression |
| HARD Rules Enforced | H-11, H-12; H-20 (green tests before complete) |

---

## 4. Phase Transition Protocol

### 4.1 Phase Gate Criteria

Each phase transition requires a quality gate. Individual stories are C1 (S-010 self-review). Aggregate phase transitions at Phase 2 exit and Phase 5 exit use C2 strategy set.

| Gate | After Phase | Type | Strategies | Threshold | Iterations |
|------|-------------|------|------------|-----------|------------|
| PG-1 | Phase 1 | C1 Story QA | S-010 | Pass/Fail per AC | 1 |
| PG-2 | Phase 2 | C2 Aggregate | S-010, S-007, S-002, S-014 | >= 0.92 | min 3 |
| PG-3 | Phase 3 | C1 Story QA | S-010 x2 | Pass/Fail per AC | 1 each |
| PG-4 | Phase 4 | C1 Story QA | S-010 x2 | Pass/Fail per AC | 1 each |
| PG-5 | Phase 5 | C2 Final | S-010, S-007, S-002, S-014 | >= 0.92 | min 3 |

### 4.2 Phase Gate Checklist

```
PHASE GATE CHECKLIST (per story, C1):
  [ ] All AC checkboxes confirmed passing
  [ ] Tests written BEFORE implementation (H-20)
  [ ] 90%+ line coverage achieved (H-21) -- uv run pytest --cov
  [ ] Type hints on all public methods (H-11)
  [ ] Docstrings on all public methods (H-12)
  [ ] One class per file (H-10)
  [ ] Domain files: no external imports (H-07)
  [ ] S-010 self-review applied by implementing agent
  [ ] Artifact persisted to orchestration path

PHASE GATE CHECKLIST (aggregate, C2):
  [ ] All stories in phase individually passed (C1 above)
  [ ] S-007 Constitutional AI Critique applied
  [ ] S-002 Devil's Advocate applied (after S-003 Steelman per H-16)
  [ ] S-014 LLM-as-Judge scoring >= 0.92
  [ ] Min 3 iterations completed
  [ ] Quality score document persisted to quality/ path
```

### 4.3 Transition Rules

1. A phase does NOT start until ALL stories in the preceding phase have passed their individual C1 gate.
2. For Phase 2 (fan-out), all 4 agents may start as soon as Phase 1 passes PG-1.
3. For Phase 3, both agents may start as soon as Phase 2 passes PG-2.
4. For Phase 4, ST-007 requires ST-005+ST-006; ST-009 requires ST-004+ST-006+ST-008. Both can start when their individual dependencies are met.
5. Phase 5 (ST-010) requires ST-007 AND ST-005 to be complete.

---

## 5. Quality Gate Definitions

### 5.1 Quality Framework Reference

All quality gates reference `.context/rules/quality-enforcement.md` as the SSOT.

| Parameter | Value | Source |
|-----------|-------|--------|
| Individual Story Criticality | C1 (Routine) | <3 files, reversible in session |
| Aggregate Phase Criticality | C2 (Standard) | 3-10 files, reversible in 1 day |
| C1 Threshold | Pass/Fail per AC | quality-enforcement.md |
| C2 Threshold | >= 0.92 weighted composite | H-13 |
| C2 Min Iterations | 3 | H-14 |
| Scoring Mechanism | S-014 (LLM-as-Judge) | SSOT |
| Steelman before Devil's Advocate | Required | H-16 |
| Self-review before presenting | Required | H-15 |

### 5.2 Scoring Dimensions (C2 Gates)

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

### 5.3 Phase Gate 1 (ST-001 Individual)

| Aspect | Specification |
|--------|---------------|
| Scope | ST-001 JerryDocument implementation |
| Type | C1 Story QA |
| Strategies | S-010 (Self-Refine) |
| Checks | AC checklist; 90% coverage via `uv run pytest --cov`; type hints; docstrings |
| Pass Condition | All AC checkboxes met; coverage >= 90% |
| Artifact | `quality/pg1/st001-qa-report.md` |

### 5.4 Phase Gate 2 (Phase 2 Aggregate)

| Aspect | Specification |
|--------|---------------|
| Scope | ST-002 + ST-003 + ST-004 + ST-008 aggregate |
| Type | C2 Aggregate Quality Gate |
| Strategies | S-010, S-003 (Steelman), S-007 (Constitutional), S-002 (Devil's Advocate), S-014 (LLM-as-Judge) |
| Strategy Order | S-010 -> S-003 -> S-007 -> S-002 -> S-014 |
| Threshold | >= 0.92 weighted composite |
| Min Iterations | 3 |
| Circuit Breaker | If no improvement after 2 consecutive iterations: ACCEPT_WITH_CAVEATS or escalate |
| Artifacts | `quality/pg2/iteration-{N}-critique.md`, `quality/pg2/final-score.md` |

### 5.5 Phase Gate 3 (Phase 3 Individual x2)

| Aspect | Specification |
|--------|---------------|
| Scope | ST-005 and ST-006 individually |
| Type | C1 Story QA x2 |
| Strategies | S-010 per story |
| Pass Condition | Both stories pass all AC |
| Artifacts | `quality/pg3/st005-qa-report.md`, `quality/pg3/st006-qa-report.md` |

### 5.6 Phase Gate 4 (Phase 4 Individual x2)

| Aspect | Specification |
|--------|---------------|
| Scope | ST-007 and ST-009 individually |
| Type | C1 Story QA x2 |
| Strategies | S-010 per story |
| Pass Condition | Both stories pass all AC; existing tests still green |
| Artifacts | `quality/pg4/st007-qa-report.md`, `quality/pg4/st009-qa-report.md` |

### 5.7 Phase Gate 5 (Final Aggregate)

| Aspect | Specification |
|--------|---------------|
| Scope | Complete FEAT-001 implementation: all 10 stories |
| Type | C2 Final Quality Gate |
| Strategies | S-010, S-003 (Steelman), S-007 (Constitutional), S-002 (Devil's Advocate), S-014 (LLM-as-Judge) |
| Strategy Order | S-010 -> S-003 -> S-007 -> S-002 -> S-014 |
| Threshold | >= 0.92 weighted composite |
| Min Iterations | 3 |
| Review Scope | Cross-story consistency, H-rules compliance, architecture layer adherence, test coverage aggregate |
| Artifact | `quality/pg5/final-quality-score.md` |

### 5.8 Operational Score Bands

| Band | Score Range | Outcome | Workflow Action |
|------|------------|---------|-----------------|
| PASS | >= 0.92 | Accepted | Phase advances or workflow completes |
| REVISE | 0.85 - 0.91 | Rejected (H-13) | Near threshold -- targeted revision likely sufficient |
| REJECTED | < 0.85 | Rejected (H-13) | Significant rework required |

---

## 6. Agent Registry

### 6.1 Phase 1 Agents

| Agent ID | Story | Role | Model | Files Produced | Status |
|----------|-------|------|-------|----------------|--------|
| impl-st001 | ST-001 | JerryDocument Facade Implementer | sonnet | `src/domain/markdown_ast/jerry_document.py`, test file | PLANNED |

### 6.2 Phase 2 Agents (Parallel Wave 1)

| Agent ID | Story | Role | Model | Files Produced | Status |
|----------|-------|------|-------|----------------|--------|
| impl-st002 | ST-002 | Frontmatter Extension Implementer | sonnet | `src/domain/markdown_ast/frontmatter.py`, test file | PLANNED |
| impl-st003 | ST-003 | Reinject Parser Implementer | sonnet | `src/domain/markdown_ast/reinject.py`, test file | PLANNED |
| impl-st004 | ST-004 | CLI Commands Implementer | sonnet | `src/interface/cli/ast_commands.py`, test file | PLANNED |
| impl-st008 | ST-008 | Nav Table Helpers Implementer | sonnet | `src/domain/markdown_ast/nav_table.py`, test file | PLANNED |

### 6.3 Phase 3 Agents (Parallel Wave 2)

| Agent ID | Story | Role | Model | Files Produced | Status |
|----------|-------|------|-------|----------------|--------|
| impl-st005 | ST-005 | /ast Skill Creator | sonnet | `skills/ast/SKILL.md` + supporting files | PLANNED |
| impl-st006 | ST-006 | Schema Validation Implementer | sonnet | `src/domain/markdown_ast/schema_validator.py`, test file | PLANNED |

### 6.4 Phase 4 Agents (Parallel Wave 3)

| Agent ID | Story | Role | Model | Files Produced | Status |
|----------|-------|------|-------|----------------|--------|
| impl-st007 | ST-007 | /worktracker Migration Agent | sonnet | Modified /worktracker skill files | PLANNED |
| impl-st009 | ST-009 | Pre-commit Hook Implementer | sonnet | Hook config/script files | PLANNED |

### 6.5 Phase 5 Agents

| Agent ID | Story | Role | Model | Files Produced | Status |
|----------|-------|------|-------|----------------|--------|
| impl-st010 | ST-010 | Remaining Migrations Agent | sonnet | Modified skill files | PLANNED |

### 6.6 Agent Input/Output Specification

| Agent | Primary Inputs | Primary Outputs | Story Entity |
|-------|---------------|-----------------|-------------|
| impl-st001 | EN-001 R01 PoC results, go-nogo-recommendation.md | `jerry_document.py` + tests | `work/EPIC-001.../ST-001-jerry-document/ST-001-jerry-document.md` |
| impl-st002 | ST-001 (jerry_document.py), ST-002 entity | `frontmatter.py` + tests | `work/EPIC-001.../ST-002-frontmatter-ext/ST-002-frontmatter-ext.md` |
| impl-st003 | ST-001 (jerry_document.py), ST-003 entity | `reinject.py` + tests | `work/EPIC-001.../ST-003-reinject-parser/ST-003-reinject-parser.md` |
| impl-st004 | ST-001 (jerry_document.py), ST-004 entity | `ast_commands.py` + tests | `work/EPIC-001.../ST-004-cli-commands/ST-004-cli-commands.md` |
| impl-st005 | ST-001 + ST-002 output, ST-005 entity | `skills/ast/SKILL.md` | `work/EPIC-001.../ST-005-ast-skill/ST-005-ast-skill.md` |
| impl-st006 | ST-001 + ST-002 output, ST-006 entity | `schema_validator.py` + tests | `work/EPIC-001.../ST-006-schema-validation/ST-006-schema-validation.md` |
| impl-st007 | ST-005 + ST-006 output, ST-007 entity | Modified worktracker files | `work/EPIC-001.../ST-007-worktracker-migration/ST-007-worktracker-migration.md` |
| impl-st008 | ST-001 (jerry_document.py), ST-008 entity | `nav_table.py` + tests | `work/EPIC-001.../ST-008-nav-table-helpers/ST-008-nav-table-helpers.md` |
| impl-st009 | ST-004 + ST-006 + ST-008 output, ST-009 entity | Pre-commit hook files | `work/EPIC-001.../ST-009-precommit-hook/ST-009-precommit-hook.md` |
| impl-st010 | ST-007 + ST-005 output, ST-010 entity | Modified skill files | `work/EPIC-001.../ST-010-remaining-migrations/ST-010-remaining-migrations.md` |

---

## 7. State Management

### 7.1 State Files

| File | Purpose |
|------|---------|
| `ORCHESTRATION.yaml` | Machine-readable state (SSOT) |
| `ORCHESTRATION_PLAN.md` | This file -- strategic context and L0/L1/L2 documentation |

### 7.2 Artifact Path Structure

All artifacts are stored under the workflow's base path using dynamic identifiers:

```
orchestration/feat001-impl-20260220-001/
├── impl/
│   ├── phase-1-bottleneck/
│   │   └── impl-st001/
│   │       └── st001-completion-report.md
│   ├── phase-2-wave1/
│   │   ├── impl-st002/
│   │   │   └── st002-completion-report.md
│   │   ├── impl-st003/
│   │   │   └── st003-completion-report.md
│   │   ├── impl-st004/
│   │   │   └── st004-completion-report.md
│   │   └── impl-st008/
│   │       └── st008-completion-report.md
│   ├── phase-3-wave2/
│   │   ├── impl-st005/
│   │   │   └── st005-completion-report.md
│   │   └── impl-st006/
│   │       └── st006-completion-report.md
│   ├── phase-4-wave3/
│   │   ├── impl-st007/
│   │   │   └── st007-completion-report.md
│   │   └── impl-st009/
│   │       └── st009-completion-report.md
│   └── phase-5-completion/
│       └── impl-st010/
│           └── st010-completion-report.md
├── quality/
│   ├── pg1/
│   │   └── st001-qa-report.md
│   ├── pg2/
│   │   ├── iteration-1-critique.md
│   │   ├── iteration-2-critique.md
│   │   ├── iteration-3-critique.md
│   │   └── final-score.md
│   ├── pg3/
│   │   ├── st005-qa-report.md
│   │   └── st006-qa-report.md
│   ├── pg4/
│   │   ├── st007-qa-report.md
│   │   └── st009-qa-report.md
│   └── pg5/
│       ├── iteration-1-critique.md
│       ├── iteration-2-critique.md
│       ├── iteration-3-critique.md
│       └── final-quality-score.md
└── phase-transitions/
    ├── pg1-transition.md
    ├── pg2-transition.md
    ├── pg3-transition.md
    ├── pg4-transition.md
    └── pg5-transition.md
```

**Dynamic Path Resolution:**
1. Base path: `orchestration/feat001-impl-20260220-001/`
2. Pipeline alias: `impl` (implementation)
3. All paths use `{base}impl/{phase_id}/{agent_id}/` format

### 7.3 Checkpoint Strategy

| Trigger | When | Purpose |
|---------|------|---------|
| STORY_COMPLETE | After each story passes individual QA | Story-level rollback point |
| PHASE_COMPLETE | After each phase gate passes | Phase-level rollback point |
| QG_COMPLETE | After aggregate quality gates (PG-2, PG-5) | Quality assessment recovery |
| MANUAL | User-triggered | Debug and inspection |

### 7.4 Story Entity State Updates

After each story completes, the agent MUST update the story entity's status field in:
- `work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/{story-dir}/{story-file}.md`

Status transitions: `pending` -> `in_progress` -> `complete`

---

## 8. Execution Constraints

### 8.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator -> Worker only. No recursive subagents. Max concurrent: 4. |
| File persistence | P-002 | All agent outputs persisted to filesystem. Completion reports required. |
| No deception | P-022 | Transparent reasoning; honest quality scores; accurate coverage reporting. |
| User authority | P-020 | User approves quality gates at PG-2 and PG-5. |
| UV only | H-05, H-06 | All Python via `uv run`. Tests via `uv run pytest`. NEVER `python` or `pip`. |
| Domain purity | H-07 | `src/domain/markdown_ast/` MUST NOT import from `infrastructure/`, `interface/`, or external packages not in domain |
| Application purity | H-08 | No infra/interface imports in application layer |
| One class per file | H-10 | Each `.py` file in `src/domain/markdown_ast/` contains exactly one class |
| Type hints | H-11 | All public methods/functions MUST have type hints |
| Docstrings | H-12 | All public methods/functions MUST have docstrings |
| Quality threshold | H-13 | >= 0.92 for C2 aggregate gates (PG-2, PG-5) |
| Min iterations | H-14 | 3 creator-critic-revision iterations for PG-2 and PG-5 |
| Self-review | H-15 | S-010 required before each story is presented |
| Steelman first | H-16 | S-003 before S-002 in aggregate gates |
| BDD test-first | H-20 | Tests written BEFORE implementation code (Red-Green-Refactor) |
| 90% coverage | H-21 | `uv run pytest --cov=src --cov-report=term-missing` must show >= 90% line coverage per new module |
| Nav tables | H-23, H-24 | SKILL.md and all new markdown docs >30 lines MUST have navigation table with anchor links |
| Worktracker templates | WTI-007 | Entity status updates MUST use canonical templates |

### 8.2 Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | 4 | Phase 2 fan-out limit (resource constraint) |
| Max QG iterations | 5 | Circuit breaker for aggregate gates (min 3, max 5 before escalation) |
| LOC budget per file | As specified | Alerts if significantly over budget (design concern) |
| Checkpoint frequency | STORY | Recovery at story completion boundaries |

---

## 9. Success Criteria

### 9.1 Phase 1 Success (ST-001)

| Criterion | Validation |
|-----------|------------|
| `JerryDocument` class created | File exists: `src/domain/markdown_ast/jerry_document.py` |
| `__init__.py` created | File exists: `src/domain/markdown_ast/__init__.py` |
| parse/render/query/transform implemented | Methods present with type hints and docstrings |
| Roundtrip preservation | Test verifies parse-render-parse identity for unmodified content |
| 90% coverage | `uv run pytest --cov` reports >= 90% for new module |
| Domain purity | No external library imports in domain class |
| Tests green | `uv run pytest tests/unit/domain/markdown_ast/test_jerry_document.py` passes |

### 9.2 Phase 2 Success (ST-002, ST-003, ST-004, ST-008)

| Criterion | Validation |
|-----------|------------|
| Frontmatter extraction working | Test extracts all fields from sample Jerry entity |
| Write-back working | Test modifies single field, verifies others unchanged |
| L2-REINJECT parser operational | Test parses known CLAUDE.md reinject comments |
| CLI subcommands registered | `uv run jerry ast --help` shows parse/render/validate/query |
| Nav table helpers functional | Test detects, extracts, validates H-23/H-24 compliance |
| All 4 stories individually at 90%+ coverage | per-module coverage check |
| Aggregate PG-2 passed | >= 0.92 composite score |

### 9.3 Phase 3 Success (ST-005, ST-006)

| Criterion | Validation |
|-----------|------------|
| `/ast` skill invokable | `skills/ast/SKILL.md` exists with navigation table |
| Schema validator operational | Validates WORKTRACKER.md entities against schema |
| ValidationResult typed | Type hints on all public methods |
| Entity schemas defined | Story, Task, Feature, Epic, Enabler, Spike covered |
| Both stories at 90%+ coverage (ST-006) | Coverage check for schema_validator.py |

### 9.4 Phase 4 Success (ST-007, ST-009)

| Criterion | Validation |
|-----------|------------|
| /worktracker migration complete | Worktracker operations use AST layer |
| Existing tests green | `uv run pytest tests/` passes with no regression |
| Pre-commit hook active | Hook triggers on `git commit` with staged .md files |
| Hook validates correctly | Passes on valid files; blocks on schema violations |

### 9.5 Phase 5 Success (ST-010)

| Criterion | Validation |
|-----------|------------|
| All target skills migrated | Skills identified in ST-010 AC migrated to AST layer |
| No regression | `uv run pytest tests/` fully green |
| Final PG-5 passed | >= 0.92 composite score |

### 9.6 Workflow Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All 10 stories complete | All story entities show status: complete |
| All 5 phase gates passed | PG-1 through PG-5 status: COMPLETE |
| Full test suite green | `uv run pytest tests/` all passing |
| Coverage aggregate maintained | Overall project coverage stays >= 90% |
| Domain architecture intact | H-07, H-08, H-09 compliance confirmed |
| FEAT-001 entity updated | FEAT-001-ast-strategy.md status: complete |

---

## 10. Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ST-001 JerryDocument API design inadequate for downstream stories | M | H | Read go-nogo-recommendation.md Component Breakdown before implementation; follow R-01 PoC patterns |
| markdown-it-py internal API changes between v4.0.0 and current | L | M | Pin versions in pyproject.toml (already done); use public API only |
| Blockquote frontmatter regex edge cases undiscovered | M | M | ST-002 must test against actual Jerry entity files (WORKTRACKER.md, SPIKE-001.md); sample-driven TDD |
| Phase 2 parallel agents produce conflicting `__init__.py` or shared module changes | M | M | impl-st001 creates the `__init__.py`; Phase 2 agents only add entries, do not overwrite |
| 90% coverage difficult to achieve for error paths | M | L | Parametrize tests; use pytest fixtures for error injection |
| Context window exhaustion for migration stories (ST-007, ST-010) | M | M | Phase checkpoints; each story is self-contained; agent can resume from story entity |
| Pre-commit hook breaks existing developer workflow | L | H | ST-009 agent must test hook on a clean branch before integrating; provide bypass instructions in docs |
| Phase 2 agents not truly parallel (dispatched sequentially by main context) | H | L | Plan notes max 4 concurrent; actual concurrency depends on Claude Code multi-agent capability |
| ST-003 L2-REINJECT comment structure changed | L | M | Agent must read actual CLAUDE.md reinject comments before implementing parser |

---

## 11. Recovery Strategies

### 11.1 Story-Level Failure Recovery

```
STORY FAILURE RECOVERY:
  1. Identify failure mode:
     a. Tests failing -> Debug and fix implementation
     b. Coverage < 90% -> Add tests for uncovered branches
     c. AC not met -> Complete missing functionality
     d. HARD rule violation -> Refactor to comply

  2. Recovery action:
     - Restart impl-st{N} agent with failure context
     - Agent reads: story entity + existing partial implementation + failure report
     - Agent applies S-010 self-review before re-submitting

  3. Checkpoint:
     - If story fails after 2 attempts, escalate to user (H-02 user authority)
```

### 11.2 Phase Gate Failure Recovery

```
PHASE GATE FAILURE RECOVERY (C1 individual):
  - Re-run failing story with specific AC item callouts
  - Maximum 2 retries before user escalation

PHASE GATE FAILURE RECOVERY (C2 aggregate, PG-2 or PG-5):
  - REVISE band (0.85-0.91): Apply targeted revision to lowest-scoring dimension
  - REJECTED band (<0.85): Full rework of failing stories
  - Max 5 iterations (circuit breaker); if no improvement after 2 consecutive: ACCEPT_WITH_CAVEATS
  - Document all caveats in phase-transitions/{gate}-transition.md
```

### 11.3 Context Exhaustion Recovery

```
CONTEXT EXHAUSTION RECOVERY (AE-006):
  1. If context compaction triggered at C2+ work: MANDATORY human escalation (H-19)
  2. Agent writes current state to ORCHESTRATION.yaml before compaction
  3. Next session reads ORCHESTRATION.yaml resumption section
  4. Story entity files serve as self-contained resumption context
  5. Completed stories need not be re-executed
```

### 11.4 Dependency Failure Propagation

```
DEPENDENCY FAILURE PROPAGATION:
  - If ST-001 (Phase 1) fails: ALL downstream stories blocked; escalate immediately
  - If any Phase 2 story fails: Phase 3 cannot start until ALL Phase 2 stories pass
  - If ST-005 fails: ST-007 and ST-010 blocked; consider path (ST-009 can proceed independently)
  - If ST-006 fails: ST-007, ST-009, ST-010 blocked; escalate immediately (critical path)
```

---

## 12. Resumption Context

### 12.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-02-20
================================

Prerequisites:
  EN-001 (R-01 PoC):             COMPLETE
  SPIKE-001 (Library Landscape):  COMPLETE
  SPIKE-002 (Feasibility):        COMPLETE
  Stack selected:                 markdown-it-py v4 + mdformat v1

Phase 1 (ST-001 Bottleneck):      PLANNED
Phase 2 (ST-002, ST-003, ST-004, ST-008): PLANNED
Phase 3 (ST-005, ST-006):         PLANNED
Phase 4 (ST-007, ST-009):         PLANNED
Phase 5 (ST-010):                 PLANNED

Next Action:                      Dispatch impl-st001
```

### 12.2 Execution Queue (Next Actions)

| Priority | Action | Agent | Unblocked When |
|----------|--------|-------|----------------|
| 1 | Implement ST-001 JerryDocument | impl-st001 | NOW (prerequisites complete) |
| 2 | Phase Gate 1 QA | main context | ST-001 complete |
| 3a | Implement ST-002 Frontmatter | impl-st002 | PG-1 passed |
| 3b | Implement ST-003 Reinject | impl-st003 | PG-1 passed |
| 3c | Implement ST-004 CLI Commands | impl-st004 | PG-1 passed |
| 3d | Implement ST-008 Nav Helpers | impl-st008 | PG-1 passed |
| 4 | Phase Gate 2 Aggregate QA | main context | ST-002+003+004+008 complete |
| 5a | Implement ST-005 /ast Skill | impl-st005 | PG-2 passed |
| 5b | Implement ST-006 Schema Validation | impl-st006 | PG-2 passed |
| 6 | Phase Gate 3 QA | main context | ST-005+006 complete |
| 7a | Implement ST-007 Worktracker Migration | impl-st007 | PG-3 passed |
| 7b | Implement ST-009 Pre-commit Hook | impl-st009 | PG-3 passed |
| 8 | Phase Gate 4 QA | main context | ST-007+009 complete |
| 9 | Implement ST-010 Remaining Migrations | impl-st010 | PG-4 passed |
| 10 | Phase Gate 5 Final QA | main context | ST-010 complete |

### 12.3 Key Reference Files for Agents

All impl agents MUST read these files before beginning implementation:

| File | Purpose |
|------|---------|
| `projects/PROJ-005-markdown-ast/orchestration/spike-eval-20260219-001/ps/phase-6-decision/ps-synthesizer-002/go-nogo-recommendation.md` | Architecture decisions, component breakdown, LOC budgets |
| `projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/EN-001-r01-poc/R01_RESULTS.md` | R-01 PoC results and working patterns |
| `projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/EN-001-r01-poc/r01_poc.py` | Reference implementation |
| `.context/rules/architecture-standards.md` | Hexagonal architecture rules |
| `.context/rules/coding-standards.md` | Type hints, docstrings, exception patterns |
| `.context/rules/testing-standards.md` | BDD Red-Green-Refactor, pytest config |
| Their own story entity file | AC checklist and scope |

---

## Disclaimer

This orchestration plan was generated by orch-planner agent (v2.2.0). Human review recommended before execution. All quality thresholds, strategy IDs, and criticality levels reference `.context/rules/quality-enforcement.md` as the single source of truth. Story scope, LOC estimates, and AC are derived from FEAT-001 story entities and SPIKE-002 go-nogo-recommendation.md. Actual implementation may reveal scope adjustments requiring plan revision.

---

*Document ID: PROJ-005-FEAT001-IMPL-ORCH-PLAN*
*Workflow ID: feat001-impl-20260220-001*
*Version: 1.0*
*Cross-Session Portable: All paths are repository-relative*
