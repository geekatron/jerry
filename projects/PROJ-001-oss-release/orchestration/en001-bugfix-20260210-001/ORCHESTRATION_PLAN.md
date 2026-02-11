# EN-001 Fix Plugin Validation: Orchestration Plan

> **Document ID:** PROJ-001-ORCH-PLAN
> **Project:** PROJ-001-oss-release
> **Workflow ID:** `en001-bugfix-20260210-001`
> **Status:** PLANNED
> **Version:** 2.0
> **Created:** 2026-02-10
> **Last Updated:** 2026-02-10

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Workflow Overview](#l0-workflow-overview) | High-level summary for stakeholders |
| [L1: Technical Plan](#l1-technical-plan) | Workflow diagram, phases, agents, barriers |
| [L2: Implementation Details](#l2-implementation-details) | State schema, path configuration, recovery strategies |
| [Execution Constraints](#execution-constraints) | Constitutional and soft constraints |
| [Success Criteria](#success-criteria) | Phase exit and workflow completion criteria |
| [Risk Mitigations](#risk-mitigations) | Risk analysis and mitigations |
| [Resumption Context](#resumption-context) | Current state and next actions |
| [Disclaimer](#disclaimer) | Agent-generated output notice |

---

## 1. Executive Summary

This orchestration plan coordinates the resolution of BUG-001 (Marketplace manifest schema error: `keywords` not allowed), which blocks the Plugin Validation CI check and prevents PR #6 from merging. The workflow implements a **Sequential Pipeline with Adversarial Critique Loops** pattern to ensure high-quality, thoroughly reviewed code changes across three tasks.

**Current State:** Workflow not started. All 3 tasks in BACKLOG.

**Orchestration Pattern:** Sequential Pipeline + Fan-Out + Adversarial Critique (Generator-Critic-Revision-Validation)

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `en001-bugfix-20260210-001` | user |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `orchestration/en001-bugfix-20260210-001/` | Dynamic |

**Artifact Output Locations:**
- Pipeline: `orchestration/en001-bugfix-20260210-001/ps/`
- Phase 1: `orchestration/en001-bugfix-20260210-001/ps/phase-1-root-cause-fix/`
- Phase 2: `orchestration/en001-bugfix-20260210-001/ps/phase-2-parallel-improvements/`
- Barriers: `orchestration/en001-bugfix-20260210-001/barriers/`

---

## L0: Workflow Overview

This workflow fixes a bug in the Jerry plugin validation CI system. The marketplace manifest file (`marketplace.json`) includes a `keywords` field in plugin items, but the schema that validates it (`marketplace.schema.json`) does not define that field. Because the schema uses `"additionalProperties": false`, the validator correctly rejects `keywords` as unexpected, causing every CI run to fail.

The fix requires three coordinated changes: (1) adding the `keywords` property to the marketplace schema (the root cause fix), (2) adding validation tests to prevent regression, and (3) specifying the correct JSON Schema validator class as a best practice. The root cause fix must be completed first because both the tests and the validator class change depend on it.

To ensure quality, each task goes through an adversarial critique cycle: a creator agent implements the change, a critic agent challenges it using devil's advocate, steelman, red team, and blue team review modes, the creator revises based on feedback, and a validator confirms the final output meets acceptance criteria. This systematic approach reduces the risk of introducing new issues while fixing the existing one.

---

## L1: Technical Plan

### 2.1 Pipeline Diagram

```
PIPELINE: ps (problem-solving)
══════════════════════════════════════════════════════════════════════════════

PHASE 1: Root Cause Fix (TASK-001) — Sequential Critique Loop
────────────────────────────────────────────────────────────────────────────

 ┌───────────────────────────┐
 │ ps-architect-task001      │  STEP 1: CREATE
 │ Create: Add keywords to   │  Implementation of schema change
 │ marketplace.schema.json   │
 └─────────────┬─────────────┘
               │
               ▼
 ┌───────────────────────────┐
 │ ps-critic-task001         │  STEP 2: ADVERSARIAL CRITIQUE
 │ Modes: Devil's Advocate,  │  Challenge assumptions, find weaknesses,
 │ Steelman, Red Team,       │  attack for vulnerabilities, defend and
 │ Blue Team                 │  validate
 └─────────────┬─────────────┘
               │
               ▼
 ┌───────────────────────────┐
 │ ps-architect-task001-rev  │  STEP 3: REVISE
 │ Revise implementation     │  Incorporate critique feedback
 │ based on critique          │
 └─────────────┬─────────────┘
               │
               ▼
 ┌───────────────────────────┐
 │ ps-validator-task001      │  STEP 4: VALIDATE
 │ Verify against TASK-001   │  Binary pass/fail against acceptance
 │ acceptance criteria        │  criteria
 └─────────────┬─────────────┘
               │
               ▼
╔═════════════════════════════════════════════════════════════════════════╗
║                          SYNC BARRIER 1                                ║
║  ┌───────────────────────────────────────────────────────────────────┐ ║
║  │ Condition: TASK-001 validated and complete                        │ ║
║  │ Artifact:  marketplace.schema.json updated with keywords          │ ║
║  │ Gate:      uv run python scripts/validate_plugin_manifests.py     │ ║
║  │            must pass for all 3 manifests                          │ ║
║  └───────────────────────────────────────────────────────────────────┘ ║
║  STATUS: PENDING                                                       ║
╚═════════════════════════════════════════════════════════════════════════╝
               │
               ▼

PHASE 2: Parallel Improvements (TASK-002 + TASK-003) — Fan-Out Critique Loops
────────────────────────────────────────────────────────────────────────────

 ┌─────────────────────────────────┐   ┌─────────────────────────────────┐
 │  TASK-002: Validation Tests     │   │  TASK-003: Validator Class      │
 │  (HIGH priority)                │   │  (MEDIUM priority)              │
 ├─────────────────────────────────┤   ├─────────────────────────────────┤
 │                                 │   │                                 │
 │  ┌───────────────────────┐     │   │  ┌───────────────────────┐     │
 │  │ ps-architect-task002  │     │   │  │ ps-architect-task003  │     │
 │  │ CREATE: Add tests     │     │   │  │ CREATE: Add cls=      │     │
 │  └───────────┬───────────┘     │   │  │ Draft202012Validator  │     │
 │              │                  │   │  └───────────┬───────────┘     │
 │              ▼                  │   │              │                  │
 │  ┌───────────────────────┐     │   │              ▼                  │
 │  │ ps-critic-task002     │     │   │  ┌───────────────────────┐     │
 │  │ CRITIQUE: Devil's     │     │   │  │ ps-critic-task003     │     │
 │  │ Advocate + Red Team   │     │   │  │ CRITIQUE: Devil's     │     │
 │  └───────────┬───────────┘     │   │  │ Advocate + Red Team   │     │
 │              │                  │   │  └───────────┬───────────┘     │
 │              ▼                  │   │              │                  │
 │  ┌───────────────────────┐     │   │              ▼                  │
 │  │ ps-architect-task002  │     │   │  ┌───────────────────────┐     │
 │  │ -rev                  │     │   │  │ ps-architect-task003  │     │
 │  │ REVISE: Fix based on  │     │   │  │ -rev                  │     │
 │  │ critique              │     │   │  │ REVISE: Fix based on  │     │
 │  └───────────┬───────────┘     │   │  │ critique              │     │
 │              │                  │   │  └───────────┬───────────┘     │
 │              ▼                  │   │              │                  │
 │  ┌───────────────────────┐     │   │              ▼                  │
 │  │ ps-validator-task002  │     │   │  ┌───────────────────────┐     │
 │  │ VALIDATE: Tests pass, │     │   │  │ ps-validator-task003  │     │
 │  │ no regressions        │     │   │  │ VALIDATE: All 3 call  │     │
 │  └─────────────────────── │     │   │  │ sites updated         │     │
 │                                 │   │  └───────────────────────┘     │
 └─────────────────────────────────┘   └─────────────────────────────────┘
               │                                     │
               └──────────────┬──────────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │   WORKFLOW COMPLETE  │
                   │   All 3 tasks done   │
                   │   CI should pass     │
                   └─────────────────────┘
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | Phase 1 must complete before Phase 2 |
| Concurrent (Fan-Out) | Yes | TASK-002 and TASK-003 run in parallel in Phase 2 |
| Barrier Sync | Yes | Barrier 1 gates Phase 1 completion before Phase 2 |
| Adversarial Critique | Yes | Each task goes through create-critique-revise-validate |
| Hierarchical | Yes | Orchestrator delegates to worker agents (P-003 compliant) |

---

## 3. Phase Definitions

### 3.1 Pipeline: ps (problem-solving)

| Phase | Name | Purpose | Agents | Status |
|-------|------|---------|--------|--------|
| 1 | Root Cause Fix | Add `keywords` to marketplace schema (TASK-001) | ps-architect-task001, ps-critic-task001, ps-architect-task001-rev, ps-validator-task001 | PENDING |
| 2 | Parallel Improvements | Add tests (TASK-002) + validator class (TASK-003) | ps-architect-task002, ps-critic-task002, ps-architect-task002-rev, ps-validator-task002, ps-architect-task003, ps-critic-task003, ps-architect-task003-rev, ps-validator-task003 | BLOCKED |

---

## 4. Sync Barrier Protocol

### 4.1 Barrier Transition Rules

```
1. PRE-BARRIER CHECK
   [ ] ps-validator-task001 reports VALIDATED status
   [ ] marketplace.schema.json contains keywords property
   [ ] uv run python scripts/validate_plugin_manifests.py passes all 3 manifests
   [ ] No blocking errors or unresolved critique issues

2. BARRIER GATE EXECUTION
   [ ] Verify schema file is syntactically valid JSON
   [ ] Verify validation script produces [PASS] for plugin.json, marketplace.json, hooks.json
   [ ] Confirm TASK-001 acceptance criteria all met

3. POST-BARRIER RELEASE
   [ ] Phase 2 agents unblocked
   [ ] TASK-002 and TASK-003 critique loops may begin
   [ ] Barrier status updated to COMPLETE
```

### 4.2 Barrier Definitions

| Barrier | After Phase | Condition | Status |
|---------|-------------|-----------|--------|
| barrier-1 | Phase 1 | TASK-001 validated, all manifests pass validation | PENDING |

---

## 5. Agent Registry

### 5.1 Phase 1 Agents (TASK-001: Root Cause Fix)

| Agent ID | Role | Input Artifacts | Output Artifact | Status |
|----------|------|-----------------|-----------------|--------|
| ps-architect-task001 | Creator: Schema change | TASK-001.md, marketplace.schema.json, plugin.schema.json | `ps/phase-1-root-cause-fix/ps-architect-task001/ps-architect-task001-implementation.md` | PENDING |
| ps-critic-task001 | Adversarial Critic | ps-architect-task001 output | `ps/phase-1-root-cause-fix/ps-critic-task001/ps-critic-task001-critique.md` | PENDING |
| ps-architect-task001-rev | Revision | ps-architect-task001 output + critique | `ps/phase-1-root-cause-fix/ps-architect-task001-rev/ps-architect-task001-rev-revision.md` | PENDING |
| ps-validator-task001 | Validation | revised output, acceptance criteria | `ps/phase-1-root-cause-fix/ps-validator-task001/ps-validator-task001-validation.md` | PENDING |

### 5.2 Phase 2 Agents (TASK-002: Tests + TASK-003: Validator Class)

| Agent ID | Role | Input Artifacts | Output Artifact | Status |
|----------|------|-----------------|-----------------|--------|
| ps-architect-task002 | Creator: Test implementation | TASK-002.md, updated schema | `ps/phase-2-parallel-improvements/ps-architect-task002/ps-architect-task002-implementation.md` | BLOCKED |
| ps-critic-task002 | Adversarial Critic | ps-architect-task002 output | `ps/phase-2-parallel-improvements/ps-critic-task002/ps-critic-task002-critique.md` | BLOCKED |
| ps-architect-task002-rev | Revision | ps-architect-task002 output + critique | `ps/phase-2-parallel-improvements/ps-architect-task002-rev/ps-architect-task002-rev-revision.md` | BLOCKED |
| ps-validator-task002 | Validation | revised output, acceptance criteria | `ps/phase-2-parallel-improvements/ps-validator-task002/ps-validator-task002-validation.md` | BLOCKED |
| ps-architect-task003 | Creator: Validator class change | TASK-003.md, DEC-001.md | `ps/phase-2-parallel-improvements/ps-architect-task003/ps-architect-task003-implementation.md` | BLOCKED |
| ps-critic-task003 | Adversarial Critic | ps-architect-task003 output | `ps/phase-2-parallel-improvements/ps-critic-task003/ps-critic-task003-critique.md` | BLOCKED |
| ps-architect-task003-rev | Revision | ps-architect-task003 output + critique | `ps/phase-2-parallel-improvements/ps-architect-task003-rev/ps-architect-task003-rev-revision.md` | BLOCKED |
| ps-validator-task003 | Validation | revised output, acceptance criteria | `ps/phase-2-parallel-improvements/ps-validator-task003/ps-validator-task003-validation.md` | BLOCKED |

---

## 6. Adversarial Critique Protocol

### 6.1 Critique Cycle Definition

Each task follows a 4-step adversarial critique loop:

```
STEP 1: CREATE (ps-architect-{task})
  └─ Agent implements the code change and documents rationale

STEP 2: ADVERSARIAL CRITIQUE (ps-critic-{task})
  └─ Devil's Advocate: Challenge assumptions about the change
  └─ Steelman: Find the strongest counter-arguments
  └─ Red Team: Attack the implementation for vulnerabilities
     - Could this break other schemas?
     - Are there edge cases in the keyword format?
     - Could this introduce a security issue?
  └─ Blue Team: Defend and validate the implementation
     - Confirm the fix addresses root cause
     - Verify alignment with existing patterns

STEP 3: REVISE (ps-architect-{task}-rev)
  └─ Creator receives critique feedback
  └─ Addresses each identified issue
  └─ Documents what changed and why

STEP 4: VALIDATE (ps-validator-{task})
  └─ Binary pass/fail against acceptance criteria
  └─ Evidence-based verification (file paths, test output)
  └─ Reports gaps requiring remediation
```

### 6.2 Critique Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Correctness | 0.30 | Does the change correctly address the root cause / task objective? |
| Completeness | 0.25 | Are all acceptance criteria addressed? |
| Consistency | 0.20 | Is the change consistent with existing patterns (plugin.schema.json)? |
| Safety | 0.15 | Does the change introduce any regressions or vulnerabilities? |
| Clarity | 0.10 | Is the implementation clear and maintainable? |

### 6.3 Circuit Breaker

| Parameter | Value |
|-----------|-------|
| Max iterations | 1 (create-critique-revise-validate; no additional loops) |
| Acceptance threshold | 0.85 quality score |
| Escalation | If validator reports FAILED, escalate to user |

**Rationale:** This is a targeted bugfix, not an architectural design. A single critique-revision cycle is sufficient. If the validator fails, the implementation needs fundamental rework and should be escalated rather than iterated.

---

## L2: Implementation Details

### 7.1 State Schema (ORCHESTRATION.yaml)

See companion file: `orchestration/en001-bugfix-20260210-001/ORCHESTRATION.yaml`

The YAML state file is the single source of truth (SSOT) for machine-readable workflow state. It tracks:
- Workflow metadata and status
- Pipeline and phase progression
- Agent execution status and artifact paths
- Barrier conditions and gate checks
- Execution queue ordering
- Checkpoints for recovery

### 7.2 Dynamic Path Configuration

All artifact paths use dynamic identifiers. No hardcoded pipeline names.

```
orchestration/en001-bugfix-20260210-001/          # Base path
├── ps/                                            # Pipeline alias (problem-solving)
│   ├── phase-1-root-cause-fix/                    # Phase 1
│   │   ├── ps-architect-task001/                  # Agent isolation directory
│   │   │   └── ps-architect-task001-implementation.md
│   │   ├── ps-critic-task001/
│   │   │   └── ps-critic-task001-critique.md
│   │   ├── ps-architect-task001-rev/
│   │   │   └── ps-architect-task001-rev-revision.md
│   │   └── ps-validator-task001/
│   │       └── ps-validator-task001-validation.md
│   └── phase-2-parallel-improvements/             # Phase 2
│       ├── ps-architect-task002/
│       │   └── ps-architect-task002-implementation.md
│       ├── ps-critic-task002/
│       │   └── ps-critic-task002-critique.md
│       ├── ps-architect-task002-rev/
│       │   └── ps-architect-task002-rev-revision.md
│       ├── ps-validator-task002/
│       │   └── ps-validator-task002-validation.md
│       ├── ps-architect-task003/
│       │   └── ps-architect-task003-implementation.md
│       ├── ps-critic-task003/
│       │   └── ps-critic-task003-critique.md
│       ├── ps-architect-task003-rev/
│       │   └── ps-architect-task003-rev-revision.md
│       └── ps-validator-task003/
│           └── ps-validator-task003-validation.md
├── barriers/
│   └── barrier-1/
│       └── barrier-1-gate-check.md
├── ORCHESTRATION_PLAN.md                          # This file
├── ORCHESTRATION.yaml                             # Machine-readable state
└── ORCHESTRATION_WORKTRACKER.md                   # Tactical execution tracking
```

**Path Construction Rules:**
- Pipeline alias: `ps` (derived from skill source: `problem-solving`)
- Phase ID: `phase-{N}-{kebab-slug}`
- Agent isolation: `{agent-id}/` subdirectory per agent
- Artifact filename: `{agent-id}-{artifact-type}.md` (defense-in-depth for safe flattening)

### 7.3 Recovery Strategies

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| Agent execution failure | Agent status = FAILED in YAML | Re-run agent from last checkpoint |
| Critique loop deadlock | Iteration >= max_iterations | Accept with caveats or escalate to user |
| Barrier gate failure | Gate check produces FAIL | Debug specific failing condition, re-run Phase 1 validation |
| Schema syntax error | JSON parse failure | Roll back schema file to pre-change state |
| Test regression | pytest returns non-zero | Investigate failing test, revise implementation |

### 7.4 Checkpoint Strategy

| Trigger | When | Purpose |
|---------|------|---------|
| PHASE_COMPLETE | After Phase 1 validated | Phase-level rollback point |
| BARRIER_COMPLETE | After barrier-1 gate passes | Confidence gate before fan-out |
| WORKFLOW_COMPLETE | After all Phase 2 tasks validated | Final state snapshot |

---

## Execution Constraints

### Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator -> Worker only. No agent spawns sub-agents. |
| File persistence | P-002 | All state and artifacts to filesystem |
| No deception | P-022 | Transparent reasoning. Critique issues not hidden. |
| User authority | P-020 | User approves escalations. User can override any gate. |

### Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | 2 | Phase 2 fan-out: TASK-002 and TASK-003 in parallel |
| Max critique iterations | 1 | Single create-critique-revise-validate cycle for bugfix scope |
| Checkpoint frequency | PHASE | Recovery at phase boundaries |
| Quality threshold | 0.85 | Minimum quality score for critique acceptance |

---

## Success Criteria

### Phase 1 Exit Criteria

| Criterion | Validation |
|-----------|------------|
| `keywords` property added to marketplace schema | Grep `schemas/marketplace.schema.json` for `"keywords"` |
| Schema is valid JSON | `uv run python -c "import json; json.load(open('schemas/marketplace.schema.json'))"` |
| All 3 manifests pass validation | `uv run python scripts/validate_plugin_manifests.py` outputs [PASS] x3 |
| Critique quality score >= 0.85 | ps-critic-task001 output |
| Validator reports VALIDATED | ps-validator-task001 output |

### Phase 2 Exit Criteria (TASK-002)

| Criterion | Validation |
|-----------|------------|
| Test verifies keywords accepted | Test function exists and passes |
| Test verifies unknown properties rejected | Test function exists and passes |
| Test verifies all 3 manifests pass | Test function exists and passes |
| `uv run pytest` passes | Zero test failures |

### Phase 2 Exit Criteria (TASK-003)

| Criterion | Validation |
|-----------|------------|
| `validate_plugin_json()` uses `cls=jsonschema.Draft202012Validator` | Grep for `cls=jsonschema.Draft202012Validator` at call site |
| `validate_marketplace_json()` uses `cls=jsonschema.Draft202012Validator` | Grep for `cls=jsonschema.Draft202012Validator` at call site |
| `validate_hooks_json()` uses `cls=jsonschema.Draft202012Validator` | Grep for `cls=jsonschema.Draft202012Validator` at call site |
| Validation script still passes | `uv run python scripts/validate_plugin_manifests.py` outputs [PASS] x3 |

### Workflow Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All phases complete | All phase status = COMPLETE in YAML |
| All barriers synced | barrier-1 status = COMPLETE |
| All tasks validated | ps-validator-task001, -task002, -task003 all report VALIDATED |
| CI passes | Plugin Validation CI check green |

---

## Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Schema change breaks other consumers | Low | High | Critique Red Team specifically attacks for cross-schema impact; validator checks all 3 manifests |
| Keywords format mismatch with plugin.schema.json | Low | Medium | TASK-001 implementation mirrors exact format from plugin.schema.json |
| Test file location wrong | Low | Low | ps-architect-task002 checks existing test conventions before creating |
| Draft202012Validator import fails | Low | Medium | ps-validator-task003 verifies jsonschema package version >= 4.0 |
| Critique loop produces false negatives | Medium | Low | Single iteration + validator binary check; escalation path to user |

---

## Resumption Context

### Current Execution State

```
WORKFLOW STATUS AS OF 2026-02-10
================================

Pipeline: ps
  Phase 1 (Root Cause Fix):  PENDING
  Phase 2 (Parallel):        BLOCKED (by barrier-1)

Barriers:
  Barrier 1: PENDING

Overall Progress: 0%
```

### Next Actions

1. Execute ps-architect-task001: Create implementation for TASK-001 (add `keywords` to marketplace schema)
2. Execute ps-critic-task001: Adversarial critique of TASK-001 implementation
3. Execute ps-architect-task001-rev: Revise based on critique feedback
4. Execute ps-validator-task001: Validate TASK-001 against acceptance criteria
5. Check barrier-1 gate: All manifests pass validation
6. If barrier passes: Fan-out to TASK-002 and TASK-003 critique loops in parallel

---

## Disclaimer

This orchestration plan was generated by the orch-planner agent (v2.1.0) in the Jerry framework. It documents a workflow design for EN-001 (Fix Plugin Validation) with adversarial critique loops. Human review is recommended before execution. All paths are repository-relative and cross-session portable.

---

*Document ID: PROJ-001-ORCH-PLAN*
*Workflow ID: en001-bugfix-20260210-001*
*Version: 2.0*
*Cross-Session Portable: All paths are repository-relative*
