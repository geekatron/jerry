# BUG-002 Hook Schema Validation Fixes: Orchestration Plan

> **Document ID:** PROJ-001-ORCH-PLAN-002
> **Project:** PROJ-001-oss-release
> **Workflow ID:** `bug002-hookfix-20260217-001`
> **Status:** PLANNED
> **Version:** 2.0
> **Created:** 2026-02-17
> **Last Updated:** 2026-02-17

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#1-executive-summary) | High-level summary and workflow identification |
| [L0: Workflow Overview](#l0-workflow-overview) | Stakeholder-level explanation |
| [L1: Technical Plan](#l1-technical-plan) | Workflow diagram, phases, agents, barriers |
| [L2: Implementation Details](#l2-implementation-details) | State schema, path configuration, recovery strategies |
| [Phase Definitions](#3-phase-definitions) | Detailed phase specifications |
| [Sync Barrier Protocol](#4-sync-barrier-protocol) | Barrier transition rules |
| [Agent Registry](#5-agent-registry) | All agents across all phases |
| [Adversarial Critique Protocol](#6-adversarial-critique-protocol) | C4 tournament review protocol |
| [Execution Constraints](#execution-constraints) | Constitutional and soft constraints |
| [Success Criteria](#success-criteria) | Phase exit and workflow completion criteria |
| [Risk Mitigations](#risk-mitigations) | Risk analysis and mitigations |
| [Resumption Context](#resumption-context) | Current state and next actions |

---

## 1. Executive Summary

This orchestration plan coordinates the resolution of BUG-002 (Hook JSON Schema Validation Failures), a **critical** bug that has rendered L2 per-prompt quality reinforcement completely non-functional since EN-705 implementation. All Jerry Framework hook scripts except `session_start_hook.py` produce JSON output that fails Claude Code's schema validation, meaning security guardrails (PreToolUse) and quality enforcement (UserPromptSubmit) have been silently failing.

The workflow implements a **Sequential Pipeline with Fan-Out and C4 Tournament Review** pattern across 5 phases:
1. Research & schema foundation with C3 adversarial review (TASK-006)
2. Parallel hook fixes (TASK-001, TASK-002, TASK-003+TASK-004)
3. Schema validation tests (TASK-005)
4. C4 adversarial tournament review (all 10 strategies)
5. Revision & closure

**Current State:** Workflow not started. All 6 tasks PENDING.

**Orchestration Pattern:** Sequential + Fan-Out + C4 Tournament Review

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `bug002-hookfix-20260217-001` | auto |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `orchestration/bug002-hookfix-20260217-001/` | Dynamic |

**Artifact Output Locations:**
- Pipeline: `orchestration/bug002-hookfix-20260217-001/fix/`
- Phase 1: `orchestration/bug002-hookfix-20260217-001/fix/phase-1-schema-foundation/`
- Phase 2: `orchestration/bug002-hookfix-20260217-001/fix/phase-2-parallel-hook-fixes/`
- Phase 3: `orchestration/bug002-hookfix-20260217-001/fix/phase-3-schema-tests/`
- Phase 4: `orchestration/bug002-hookfix-20260217-001/fix/phase-4-c4-tournament/`
- Phase 5: `orchestration/bug002-hookfix-20260217-001/fix/phase-5-revision-closure/`
- Barriers: `orchestration/bug002-hookfix-20260217-001/barriers/`

---

## L0: Workflow Overview

The Jerry Framework uses Claude Code hooks to enforce quality and security at runtime. Four hook scripts intercept different events (session start, prompt submission, tool use, subagent stop) and inject guardrails into Claude's context. A discovery (DISC-002) found that 3 of 4 hooks produce JSON output that fails Claude Code's internal schema validation. The consequence:

- **L2 quality reinforcement is completely broken** -- the UserPromptSubmit hook's `additionalContext` never reaches Claude because the output is missing the required `hookEventName` field
- **Security guardrails are on a deprecated API** -- PreToolUse uses `decision`/`approve`/`block` instead of `hookSpecificOutput.permissionDecision`/`allow`/`deny`
- **Subagent handoff never fires** -- SubagentStop is registered under the wrong event type (`Stop`) which doesn't support the matcher pattern used

This workflow fixes all 7 root causes across 4 files, creates JSON Schema definitions for all hook output types, adds automated schema validation tests to prevent regression, and subjects the entire fix set to a C4 tournament review (all 10 adversarial strategies) before closure.

**Impact:** Until BUG-002 is resolved, the 5-layer enforcement architecture (ADR-EPIC002-002) is operating with Layer 2 disabled. This is a critical gap in the quality framework.

---

## L1: Technical Plan

### 2.1 Pipeline Diagram

```
PIPELINE: fix (bug-fix)
============================================================================

PHASE 1: Schema Foundation (TASK-006) -- Sequential
----------------------------------------------------------------------------

 +-------------------------------+
 | fix-researcher-task006        |  STEP 1: RESEARCH
 | Research Claude Code repo for |  Check for existing schema files
 | existing JSON Schema files.   |  (Context7, WebSearch, source code)
 | Generate from official docs.  |
 +---------------+---------------+
                 |
                 v
 +-------------------------------+
 | fix-creator-task006           |  STEP 2: CREATE
 | Create JSON Schema files at   |  Draft 2020-12 format
 | schemas/hooks/*.schema.json   |
 +---------------+---------------+
                 |
                 v
 +-------------------------------+
 | fix-validator-task006         |  STEP 3: VALIDATE
 | Validate schemas against      |  Known-good (session_start_hook.py)
 | known-good and known-bad      |  and known-bad (user-prompt-submit.py)
 | outputs                       |  outputs
 +---------------+---------------+
                 |
                 v
 +-------------------------------+
 | adv-executor-p1               |  STEP 4: C3 ADVERSARIAL REVIEW
 | Execute C3 strategies:        |  S-010, S-003, S-002, S-007,
 | S-010, S-003, S-002, S-007,  |  S-014, S-013, S-011
 | S-014, S-013, S-011          |  (7 strategies per C3)
 +---------------+---------------+
                 |
                 v
 +-------------------------------+
 | adv-scorer-p1                 |  STEP 5: SCORE
 | Score schema deliverable      |  Threshold: >= 0.92
 | with S-014 rubric             |
 +---------------+---------------+
                 |
                 v
         [Score >= 0.92?]
           |           |
          YES          NO
           |           |
           |           v
           |   +-------------------------------+
           |   | fix-reviser-p1                |  STEP 5b: REVISE (conditional)
           |   | Revise schemas based on       |  If score < 0.92, revise and
           |   | adversarial feedback           |  re-run adv-executor-p1
           |   +---------------+---------------+
           |                   |
           +-------------------+
                 |
                 v
+=========================================================================+
||                        SYNC BARRIER 1                                 ||
||  Condition: JSON Schema files exist and validated                     ||
||  Gate: schemas/hooks/*.schema.json files valid and tested             ||
||  STATUS: PENDING                                                      ||
+=========================================================================+
                 |
                 v

PHASE 2: Parallel Hook Fixes (TASK-001 + TASK-002 + TASK-003/004) -- Fan-Out
----------------------------------------------------------------------------

 +---------------------------+  +---------------------------+  +-----------------------------+
 | TASK-001: UserPromptSubmit|  | TASK-002: PreToolUse      |  | TASK-003+004: SubagentStop  |
 | (CRITICAL priority)       |  | (HIGH priority)           |  | + hooks.json (HIGH)         |
 |                           |  |                           |  |                             |
 | fix-creator-task001       |  | fix-creator-task002       |  | fix-creator-task003         |
 | Add hookEventName to      |  | Migrate to                |  | Move to SubagentStop event  |
 | hookSpecificOutput        |  | hookSpecificOutput API    |  | Fix output format + config  |
 |             |             |  |             |             |  |               |             |
 |             v             |  |             v             |  |               v             |
 | fix-validator-task001     |  | fix-validator-task002     |  | fix-validator-task003       |
 | Validate against schema   |  | Validate against schema   |  | Validate against schema     |
 +---------------------------+  +---------------------------+  +-----------------------------+
              |                              |                              |
              +------------------------------+------------------------------+
                                             |
                                             v
+=========================================================================+
||                        SYNC BARRIER 2                                 ||
||  Condition: All 4 hook files fixed, all pass schema validation        ||
||  Gate: Each hook output validates against Phase 1 schemas             ||
||  STATUS: PENDING                                                      ||
+=========================================================================+
                                             |
                                             v

PHASE 3: Schema Validation Tests (TASK-005) -- Sequential
----------------------------------------------------------------------------

 +-------------------------------+
 | fix-creator-task005           |  CREATE test file
 | tests/test_hook_schema_       |  Validate all 4 hooks against
 | compliance.py                 |  Phase 1 JSON Schemas
 +---------------+---------------+
                 |
                 v
 +-------------------------------+
 | fix-validator-task005         |  VALIDATE
 | uv run pytest tests/          |  All tests pass, no regressions
 | test_hook_schema_compliance.py|
 +---------------+---------------+
                 |
                 v
+=========================================================================+
||                        SYNC BARRIER 3                                 ||
||  Condition: All tests pass, full test suite green                     ||
||  Gate: uv run pytest passes with 0 failures                          ||
||  STATUS: PENDING                                                      ||
+=========================================================================+
                 |
                 v

PHASE 4: C4 Tournament Review (/adversary) -- All 10 Strategies
----------------------------------------------------------------------------

 +-------------------------------+
 | adv-selector                  |  SELECT C4 strategy set
 | Criticality: C4 (Critical)   |  All 10 strategies required
 | All strategies mandatory      |
 +---------------+---------------+
                 |
                 v
 +-------------------------------+
 | adv-executor                  |  EXECUTE tournament
 | Run all 10 strategies:       |
 |  S-014 LLM-as-Judge          |
 |  S-003 Steelman              |
 |  S-013 Inversion             |
 |  S-007 Constitutional AI     |
 |  S-002 Devil's Advocate      |
 |  S-004 Pre-Mortem            |
 |  S-010 Self-Refine           |
 |  S-012 FMEA                  |
 |  S-011 Chain-of-Verification |
 |  S-001 Red Team              |
 +---------------+---------------+
                 |
                 v
 +-------------------------------+
 | adv-scorer                    |  SCORE deliverable
 | 6-dimension rubric            |  Threshold: >= 0.92
 | Weighted composite score      |
 +---------------+---------------+
                 |
                 v
         [Score >= 0.92?]
           |           |
          YES          NO
           |           |
           v           v

PHASE 5: Revision & Closure
----------------------------------------------------------------------------

 (If PASS)                    (If REVISE/REJECTED)
 +-------------------+        +-------------------+
 | BUG-002 Closure   |        | fix-reviser       |
 | Update worktracker|        | Address tournament |
 | Mark complete     |        | feedback, re-run   |
 +-------------------+        | Phase 4            |
                               +-------------------+
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | Phase 1 -> Barrier -> Phase 2 -> Barrier -> Phase 3 -> Barrier -> Phase 4 -> Phase 5 |
| Concurrent (Fan-Out) | Yes | Phase 2: TASK-001, TASK-002, TASK-003/004 in parallel |
| Barrier Sync | Yes | 3 barriers gate phase transitions |
| C4 Tournament Review | Yes | Phase 4: All 10 adversarial strategies applied |
| Hierarchical | Yes | Orchestrator delegates to worker agents (P-003 compliant) |

---

## 3. Phase Definitions

### 3.1 Pipeline: fix (bug-fix)

| Phase | Name | Purpose | Tasks | Agents | Status |
|-------|------|---------|-------|--------|--------|
| 1 | Schema Foundation | Create JSON Schema definitions for hook outputs with C3 adversarial review (TASK-006) | TASK-006 | fix-researcher-task006, fix-creator-task006, fix-validator-task006, adv-executor-p1, adv-scorer-p1, fix-reviser-p1 | PENDING |
| 2 | Parallel Hook Fixes | Fix all 3 broken hook scripts + config (TASK-001, 002, 003, 004) | TASK-001, TASK-002, TASK-003, TASK-004 | fix-creator-task001/002/003, fix-validator-task001/002/003 | BLOCKED |
| 3 | Schema Tests | Add automated schema validation tests (TASK-005) | TASK-005 | fix-creator-task005, fix-validator-task005 | BLOCKED |
| 4 | C4 Tournament | Adversarial review of complete fix set with all 10 strategies | -- | adv-selector, adv-executor, adv-scorer | BLOCKED |
| 5 | Revision & Closure | Address tournament feedback (if any), close BUG-002 | -- | fix-reviser (conditional) | BLOCKED |

---

## 4. Sync Barrier Protocol

### 4.1 Barrier Transition Rules

```
BARRIER 1 (After Phase 1):
  PRE-BARRIER:
  [ ] fix-validator-task006 reports VALIDATED
  [ ] schemas/hooks/*.schema.json files exist
  [ ] Schemas validated against session_start_hook.py known-good output
  [ ] Schemas reject known-bad user-prompt-submit.py output
  [ ] C3 adversarial review score >= 0.92 (adv-scorer-p1 output)
  POST-BARRIER:
  [ ] Phase 2 agents unblocked
  [ ] Hook fix agents can reference schemas for validation

BARRIER 2 (After Phase 2):
  PRE-BARRIER:
  [ ] fix-validator-task001 reports VALIDATED (UserPromptSubmit fixed)
  [ ] fix-validator-task002 reports VALIDATED (PreToolUse fixed)
  [ ] fix-validator-task003 reports VALIDATED (SubagentStop + hooks.json fixed)
  [ ] All hook outputs pass schema validation against Phase 1 schemas
  POST-BARRIER:
  [ ] Phase 3 agents unblocked
  [ ] Test creation can begin with confidence all hooks are fixed

BARRIER 3 (After Phase 3):
  PRE-BARRIER:
  [ ] fix-validator-task005 reports VALIDATED
  [ ] tests/test_hook_schema_compliance.py exists
  [ ] uv run pytest tests/test_hook_schema_compliance.py passes
  [ ] Full test suite (uv run pytest) passes with 0 failures
  POST-BARRIER:
  [ ] Phase 4 (C4 Tournament) unblocked
  [ ] Complete deliverable package ready for adversarial review
```

### 4.2 Barrier Definitions

| Barrier | After Phase | Condition | Status |
|---------|-------------|-----------|--------|
| barrier-1 | Phase 1 | Schema files created and validated | PENDING |
| barrier-2 | Phase 2 | All hooks fixed and pass schema validation | PENDING |
| barrier-3 | Phase 3 | All tests pass, full suite green | PENDING |

---

## 5. Agent Registry

### 5.1 Phase 1 Agents (TASK-006: Schema Foundation)

| Agent ID | Role | Input Artifacts | Output Artifact | Status |
|----------|------|-----------------|-----------------|--------|
| fix-researcher-task006 | Research: Find existing schemas | Context7, Claude Code docs, WebSearch | `fix/phase-1-schema-foundation/fix-researcher-task006/fix-researcher-task006-research.md` | PENDING |
| fix-creator-task006 | Create: Generate JSON Schema files | Research output, official docs | `schemas/hooks/*.schema.json` + `fix/phase-1-schema-foundation/fix-creator-task006/fix-creator-task006-implementation.md` | PENDING |
| fix-validator-task006 | Validate: Test schemas against known outputs | Schema files, session_start_hook.py output, broken hook outputs | `fix/phase-1-schema-foundation/fix-validator-task006/fix-validator-task006-validation.md` | PENDING |
| adv-executor-p1 | Execute C3 strategies against schema deliverable | Schema files, strategy templates | `fix/phase-1-schema-foundation/adv-executor-p1/adv-executor-p1-review.md` | PENDING |
| adv-scorer-p1 | Score schema deliverable with S-014 rubric | Review results | `fix/phase-1-schema-foundation/adv-scorer-p1/adv-scorer-p1-score.md` | PENDING |
| fix-reviser-p1 | Revise schemas based on adversarial feedback (conditional) | Scorer feedback | `fix/phase-1-schema-foundation/fix-reviser-p1/fix-reviser-p1-revision.md` | PENDING |

### 5.2 Phase 2 Agents (TASK-001, 002, 003/004: Hook Fixes)

| Agent ID | Role | Task(s) | Input Artifacts | Output Artifact | Status |
|----------|------|---------|-----------------|-----------------|--------|
| fix-creator-task001 | Fix UserPromptSubmit | TASK-001 | TASK-001.md, user-prompt-submit.py, schemas | `fix/phase-2-parallel-hook-fixes/fix-creator-task001/fix-creator-task001-implementation.md` | BLOCKED |
| fix-validator-task001 | Validate TASK-001 | TASK-001 | Fixed hook output, schema | `fix/phase-2-parallel-hook-fixes/fix-validator-task001/fix-validator-task001-validation.md` | BLOCKED |
| fix-creator-task002 | Fix PreToolUse | TASK-002 | TASK-002.md, pre_tool_use.py, schemas | `fix/phase-2-parallel-hook-fixes/fix-creator-task002/fix-creator-task002-implementation.md` | BLOCKED |
| fix-validator-task002 | Validate TASK-002 | TASK-002 | Fixed hook output, schema | `fix/phase-2-parallel-hook-fixes/fix-validator-task002/fix-validator-task002-validation.md` | BLOCKED |
| fix-creator-task003 | Fix SubagentStop + hooks.json | TASK-003, TASK-004 | TASK-003.md, TASK-004.md, subagent_stop.py, hooks.json, schemas | `fix/phase-2-parallel-hook-fixes/fix-creator-task003/fix-creator-task003-implementation.md` | BLOCKED |
| fix-validator-task003 | Validate TASK-003/004 | TASK-003, TASK-004 | Fixed files, schema | `fix/phase-2-parallel-hook-fixes/fix-validator-task003/fix-validator-task003-validation.md` | BLOCKED |

### 5.3 Phase 3 Agents (TASK-005: Schema Tests)

| Agent ID | Role | Input Artifacts | Output Artifact | Status |
|----------|------|-----------------|-----------------|--------|
| fix-creator-task005 | Create test file | TASK-005.md, schema files, all fixed hooks | `fix/phase-3-schema-tests/fix-creator-task005/fix-creator-task005-implementation.md` | BLOCKED |
| fix-validator-task005 | Validate tests pass | Test file, pytest output | `fix/phase-3-schema-tests/fix-validator-task005/fix-validator-task005-validation.md` | BLOCKED |

### 5.4 Phase 4 Agents (C4 Tournament Review)

| Agent ID | Role | Input Artifacts | Output Artifact | Status |
|----------|------|-----------------|-----------------|--------|
| adv-selector | Select C4 strategy set | quality-enforcement.md, BUG-002.md | `fix/phase-4-c4-tournament/adv-selector/adv-selector-strategy-selection.md` | BLOCKED |
| adv-executor | Execute all 10 strategies | All fix artifacts, strategy templates | `fix/phase-4-c4-tournament/adv-executor/adv-executor-tournament-results.md` | BLOCKED |
| adv-scorer | Score with S-014 rubric | Tournament results, quality-enforcement.md | `fix/phase-4-c4-tournament/adv-scorer/adv-scorer-quality-score.md` | BLOCKED |

### 5.5 Phase 5 Agents (Conditional)

| Agent ID | Role | Input Artifacts | Output Artifact | Status |
|----------|------|-----------------|-----------------|--------|
| fix-reviser | Revise based on tournament feedback | Tournament results, scorer feedback | `fix/phase-5-revision-closure/fix-reviser/fix-reviser-revision.md` | BLOCKED |

---

## 6. Adversarial Critique Protocol

### 6.1 C4 Tournament Review Definition

BUG-002 is classified as **C4 (Critical)** because:
- L2 enforcement layer is completely disabled (quality framework integrity)
- Security guardrails (PreToolUse) are on deprecated API (security-relevant: AE-005 -> auto-C3+)
- Affects hook infrastructure used by all Jerry sessions (high blast radius)
- User explicitly requested C4 tournament review

**C4 requires ALL 10 strategies** (no optional strategies at C4).

### 6.2 Strategy Execution Order

Per H-16: Steelman (S-003) MUST be applied before Devil's Advocate (S-002).

| Order | Strategy | ID | Focus Area |
|-------|----------|----|------------|
| 1 | Self-Refine | S-010 | Self-review of complete fix set |
| 2 | Steelman | S-003 | Strengthen the fix approach before critique |
| 3 | Devil's Advocate | S-002 | Challenge assumptions about schema compliance |
| 4 | Constitutional AI | S-007 | Verify fixes comply with Jerry Constitution |
| 5 | LLM-as-Judge | S-014 | Score against 6-dimension rubric |
| 6 | Pre-Mortem | S-004 | "Imagine these fixes failed -- why?" |
| 7 | Inversion | S-013 | "How could these fixes still break?" |
| 8 | FMEA | S-012 | Systematic failure mode enumeration |
| 9 | Chain-of-Verification | S-011 | Verify factual claims (schema fields, exit codes) |
| 10 | Red Team | S-001 | Adversary simulation: bypass hook guardrails |

### 6.3 Scoring Dimensions (S-014)

| Dimension | Weight | BUG-002 Application |
|-----------|--------|---------------------|
| Completeness | 0.20 | All 7 root causes addressed across all 4 files |
| Internal Consistency | 0.20 | All hooks follow same pattern as session_start_hook.py reference |
| Methodological Rigor | 0.20 | Fixes derived from authoritative Claude Code docs, not guesswork |
| Evidence Quality | 0.15 | Schema validation tests prove compliance |
| Actionability | 0.15 | Fixes are directly applicable, no ambiguity |
| Traceability | 0.10 | Each fix traces to specific root cause (RC-1 through RC-7) |

### 6.4 Quality Gate

| Parameter | Value |
|-----------|-------|
| Threshold | >= 0.92 weighted composite (H-13) |
| Max iterations | 3 (per H-14: minimum 3 creator-critic-revision) |
| Escalation | After 3 failed iterations, human escalation (AE-006) |

**Score Bands:**
- PASS (>= 0.92): Proceed to BUG-002 closure
- REVISE (0.85 - 0.91): Targeted revision, re-run tournament
- REJECTED (< 0.85): Significant rework, re-run from Phase 2

---

## L2: Implementation Details

### 7.1 Dynamic Path Configuration

```
orchestration/bug002-hookfix-20260217-001/              # Base path
+-- fix/                                                 # Pipeline alias
|   +-- phase-1-schema-foundation/
|   |   +-- fix-researcher-task006/
|   |   |   +-- fix-researcher-task006-research.md
|   |   +-- fix-creator-task006/
|   |   |   +-- fix-creator-task006-implementation.md
|   |   +-- fix-validator-task006/
|   |   |   +-- fix-validator-task006-validation.md
|   |   +-- adv-executor-p1/
|   |   |   +-- adv-executor-p1-review.md
|   |   +-- adv-scorer-p1/
|   |   |   +-- adv-scorer-p1-score.md
|   |   +-- fix-reviser-p1/
|   |       +-- fix-reviser-p1-revision.md (conditional)
|   +-- phase-2-parallel-hook-fixes/
|   |   +-- fix-creator-task001/
|   |   |   +-- fix-creator-task001-implementation.md
|   |   +-- fix-validator-task001/
|   |   |   +-- fix-validator-task001-validation.md
|   |   +-- fix-creator-task002/
|   |   |   +-- fix-creator-task002-implementation.md
|   |   +-- fix-validator-task002/
|   |   |   +-- fix-validator-task002-validation.md
|   |   +-- fix-creator-task003/
|   |   |   +-- fix-creator-task003-implementation.md
|   |   +-- fix-validator-task003/
|   |       +-- fix-validator-task003-validation.md
|   +-- phase-3-schema-tests/
|   |   +-- fix-creator-task005/
|   |   |   +-- fix-creator-task005-implementation.md
|   |   +-- fix-validator-task005/
|   |       +-- fix-validator-task005-validation.md
|   +-- phase-4-c4-tournament/
|   |   +-- adv-selector/
|   |   |   +-- adv-selector-strategy-selection.md
|   |   +-- adv-executor/
|   |   |   +-- adv-executor-tournament-results.md
|   |   +-- adv-scorer/
|   |       +-- adv-scorer-quality-score.md
|   +-- phase-5-revision-closure/
|       +-- fix-reviser/
|           +-- fix-reviser-revision.md (conditional)
+-- barriers/
|   +-- barrier-1/
|   |   +-- barrier-1-gate-check.md
|   +-- barrier-2/
|   |   +-- barrier-2-gate-check.md
|   +-- barrier-3/
|       +-- barrier-3-gate-check.md
+-- ORCHESTRATION_PLAN.md
+-- ORCHESTRATION.yaml
+-- ORCHESTRATION_WORKTRACKER.md
```

### 7.2 Recovery Strategies

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| Schema generation fails | fix-validator-task006 FAILED | Re-run research with alternative sources |
| Hook fix introduces new bug | fix-validator-task00N FAILED | Roll back specific hook, fix, re-validate |
| Tests fail on fixed hooks | fix-validator-task005 FAILED | Debug test vs implementation mismatch |
| Tournament score < 0.92 | adv-scorer output | Revise based on feedback, re-run tournament |
| Full test suite regression | pytest non-zero exit | Investigate regression, fix without changing hook behavior |

### 7.3 Checkpoint Strategy

| Trigger | When | Purpose |
|---------|------|---------|
| CP-001 | After Phase 1 (schemas created) | Schema rollback point |
| CP-002 | After Phase 2 (all hooks fixed) | Pre-test state |
| CP-003 | After Phase 3 (tests pass) | Pre-tournament state |
| CP-004 | After Phase 4 (tournament scored) | Quality gate decision point |
| CP-005 | After Phase 5 (BUG-002 closed) | Final state snapshot |

---

## Execution Constraints

### Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator -> Worker only. No agent spawns sub-agents. |
| File persistence | P-002 | All state and artifacts to filesystem |
| No deception | P-022 | Transparent reasoning. Issues not hidden. |
| User authority | P-020 | User approves escalations and gates. |
| UV only | H-05/H-06 | All Python via `uv run`. All deps via `uv add`. |

### Worktracker Entity Templates

> **WTI-007:** Entity files created during orchestration MUST use canonical templates from `.context/templates/worktracker/`.

### Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | 3 | Phase 2 fan-out: 3 parallel fix streams |
| Max tournament iterations | 3 | H-14 minimum, circuit breaker after 3 |
| Checkpoint frequency | PHASE | Recovery at phase boundaries |
| Quality threshold | >= 0.92 | H-13 for C2+ criticality |
| Phase 1 criticality | C3 (Significant) | 7 strategies: S-010, S-003, S-002, S-007, S-014, S-013, S-011 |
| Phase 4 criticality | C4 (Critical) | All 10 strategies (no optional at C4) |

---

## Success Criteria

### Phase 1 Exit Criteria

| Criterion | Validation |
|-----------|------------|
| JSON Schema files exist for all hook event types | `ls schemas/hooks/*.schema.json` |
| Schemas use JSON Schema draft 2020-12 | Check `$schema` field |
| Schemas validate session_start_hook.py output (known-good) | jsonschema validates successfully |
| Schemas reject current user-prompt-submit.py output (known-bad) | jsonschema validation fails as expected |

### Phase 2 Exit Criteria

| Criterion | Validation |
|-----------|------------|
| `user-prompt-submit.py` includes `hookEventName: "UserPromptSubmit"` | Grep hook output JSON |
| `pre_tool_use.py` uses `hookSpecificOutput.permissionDecision` | Grep for `permissionDecision` |
| `pre_tool_use.py` uses `"allow"`/`"deny"` (not `"approve"`/`"block"`) | Grep for `allow`/`deny` |
| `pre_tool_use.py` exits 0 on errors (fail-open) | Check exit code logic |
| `subagent_stop.py` registered under `SubagentStop` in hooks.json | Grep hooks.json |
| `subagent_stop.py` outputs schema-compliant JSON | Validate against schema |
| `hooks.json` has no matchers on events that don't support them | Review config |
| All hooks pass schema validation | Run against Phase 1 schemas |

### Phase 3 Exit Criteria

| Criterion | Validation |
|-----------|------------|
| `tests/test_hook_schema_compliance.py` exists | File exists |
| All 4 hook scripts have schema validation tests | Test count >= 4 hook types |
| `uv run pytest tests/test_hook_schema_compliance.py` passes | Zero failures |
| Full suite `uv run pytest` passes | Zero failures, no regressions |

### Phase 4 Exit Criteria

| Criterion | Validation |
|-----------|------------|
| All 10 strategies executed | adv-executor output covers all 10 |
| Quality score >= 0.92 | adv-scorer weighted composite |
| No critical findings unaddressed | Tournament results reviewed |

### Workflow Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All phases complete | All phase status = COMPLETE in YAML |
| All barriers passed | barrier-1, barrier-2, barrier-3 = COMPLETE |
| Tournament score >= 0.92 | adv-scorer output |
| BUG-002 marked complete | WORKTRACKER.md updated |
| L2 reinforcement confirmed working | Debug log shows additionalContext injected |

---

## Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Claude Code schema changes between research and fix | Low | High | Pin to fetched doc version; add schema version to files |
| PreToolUse fix breaks existing security guardrails | Medium | High | Phase 2 validator checks all decision paths; Phase 3 tests cover edge cases |
| SubagentStop event type doesn't fire | Low | Medium | Test with actual subagent invocation; verify hooks.json registration |
| hooks.json config change breaks other hooks | Low | High | TASK-004 coordinated with TASK-003; Phase 2 validates all hooks together |
| Tournament finds fundamental design flaw | Low | High | Phase 5 revision cycle; user escalation per AE-006 |
| Test suite regression from hook changes | Medium | Medium | Full pytest run at barrier-3; checkpoint CP-002 enables rollback |

---

## Resumption Context

### Current Execution State

```
WORKFLOW STATUS AS OF 2026-02-17
=================================

Pipeline: fix
  Phase 1 (Schema Foundation):       PENDING
  Phase 2 (Parallel Hook Fixes):     BLOCKED (by barrier-1)
  Phase 3 (Schema Tests):            BLOCKED (by barrier-2)
  Phase 4 (C4 Tournament):           BLOCKED (by barrier-3)
  Phase 5 (Revision & Closure):      BLOCKED (by Phase 4)

Barriers:
  Barrier 1: PENDING
  Barrier 2: PENDING
  Barrier 3: PENDING

Overall Progress: 0%
```

### Next Actions

1. Execute fix-researcher-task006: Research Claude Code for existing hook output JSON Schema files
2. Execute fix-creator-task006: Create JSON Schema definitions from official docs
3. Execute fix-validator-task006: Validate schemas against known-good and known-bad outputs
4. Execute adv-executor-p1: Run C3 adversarial review (7 strategies) against schema deliverable
5. Execute adv-scorer-p1: Score schema deliverable against S-014 rubric (threshold >= 0.92)
6. Execute fix-reviser-p1: Revise schemas if score < 0.92 (conditional)
7. Check barrier-1 gate: Schema files created, validated, and C3 review score >= 0.92
8. Fan-out to Phase 2: TASK-001, TASK-002, TASK-003/004 in parallel
9. Check barrier-2 gate: All hooks fixed and validated
10. Execute Phase 3: TASK-005 test creation
11. Check barrier-3 gate: All tests pass
12. Execute Phase 4: C4 tournament review (all 10 strategies)
13. Phase 5: Revision if needed, then BUG-002 closure

---

*Document ID: PROJ-001-ORCH-PLAN-002*
*Workflow ID: bug002-hookfix-20260217-001*
*Version: 2.0*
*Cross-Session Portable: All paths are repository-relative*
