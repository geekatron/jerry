# ORCHESTRATION_PLAN.md - EN-202 CLAUDE.md Rewrite

> **Document ID:** EN-202-ORCH-PLAN
> **Project:** PROJ-001-oss-release
> **Workflow ID:** `en202-rewrite-20260201-001`
> **Status:** ACTIVE
> **Version:** 1.0
> **Created:** 2026-02-01
> **Last Updated:** 2026-02-01
> **Protocol:** DISC-002 Adversarial Review
> **Prior Art:** EN-201 Orchestration (FEAT-002/EN-201/orchestration/)

---

## 1. Executive Summary

This orchestration plan coordinates the rewrite of CLAUDE.md from 914 lines to 60-80 lines, using the **DISC-002 Adversarial Review Protocol** established in the FEAT-001 research phase and refined in EN-201.

**Problem:** CLAUDE.md at 914 lines consumes ~10,000 tokens at every session start, contributing to context rot and degraded LLM performance.

**Solution:** Rewrite CLAUDE.md to contain only essential content (~75 lines, ~3,500 tokens):
- Identity section (~10 lines)
- Navigation pointers (~20 lines)
- Active project context (~15 lines)
- Critical constraints (~15 lines)
- Quick reference (~15 lines)

**Prerequisite:** TASK-000 (Navigation tables for templates) must complete first.

**Bug Fixes:** During rewrite, fix 3 source defects discovered in EN-201:
- BUG-001: "relationships to to" typo
- BUG-002: Story folder uses {EnablerId} instead of {StoryId}
- BUG-003: Template path inconsistency

**Orchestration Pattern:** Fan-Out/Fan-In with **DISC-002 Adversarial Review Loops**

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `en202-rewrite-20260201-001` | auto |
| ID Format | `{enabler}-{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `EN-202-claude-md-rewrite/orchestration/` | Enabler-scoped |
| Protocol | **DISC-002** | Adversarial Review Protocol |
| Prior Art | EN-201/orchestration/ | Previous Enabler |

**Pipeline Configuration:**

| Pipeline | Alias | Skill Source | Role |
|----------|-------|--------------|------|
| Pipeline A | `ps` | problem-solving | Content creation, quality review |
| Pipeline B | `nse` | nasa-systems-engineering | Compliance verification |

**Artifact Output Locations:**
- New CLAUDE.md: Repository root
- Backup: `CLAUDE.md.backup`
- Quality gate artifacts: `orchestration/quality-gates/`
- Escalation artifacts: `orchestration/escalations/`

---

## 2. Workflow Architecture

### 2.1 DISC-002 Adversarial Review Protocol

This workflow implements the **DISC-002 Adversarial Review Protocol**:

| Protocol Element | Implementation |
|------------------|----------------|
| **Review Agents** | ps-critic (Quality Evaluator) + nse-qa (NASA SE Compliance) |
| **Quality Threshold** | ≥ 0.92 (per DEC-OSS-001) |
| **Max Iterations** | 3 per artifact (then human escalation per DEC-OSS-004) |
| **Mandatory Findings** | Minimum 3 adversarial findings per review |
| **Versioned Files** | `*-review.md` → `*-review-v2.md` → `*-review-v3.md` |
| **Red Team Framing** | Actively seek weaknesses, blind spots, contradictions |

### 2.2 Pipeline Diagram

```
                     EN-202 ORCHESTRATION WORKFLOW (DISC-002)
                     =========================================
                          Quality Gate: 0.92 | Max Iterations: 3
                          Protocol: DISC-002 Adversarial Review

┌─────────────────────────────────────────────────────────────────────────────┐
│                    PHASE 0: PREREQUISITE (TASK-000)                          │
│                         Navigation Tables for Templates                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                        TASK-000: Navigation Tables                     │  │
│  │  ─────────────────────────────────────────────────────────────────── │  │
│  │  Scope:                                                               │  │
│  │  • 5 worktracker rules (skills/worktracker/rules/*.md)               │  │
│  │  • 10 worktracker templates (.context/templates/worktracker/*.md)    │  │
│  │  • ~8 Claude rules (.claude/rules/*.md)                               │  │
│  │  Total: ~23 files need navigation tables                              │  │
│  │  ─────────────────────────────────────────────────────────────────── │  │
│  │  Execution: Background agent (ps-writer) with ps-critic review       │  │
│  │  Output: All files have NAV-006 compliant navigation tables          │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║                    CHECKPOINT 0: TASK-000 Complete                       ║
    ║     Pre-condition for CLAUDE.md rewrite                                 ║
    ╚═════════════════════════════════════════════════════════════════════════╝
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PHASE 1: SECTION CREATION (Fan-Out)                       │
│                         Execution Mode: PARALLEL                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                │
│  │    TASK-001    │  │    TASK-002    │  │    TASK-003    │                │
│  │    Identity    │  │   Navigation   │  │ Active Project │                │
│  │   (~10 LOC)    │  │    (~20 LOC)   │  │   (~15 LOC)    │                │
│  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘                │
│          │                   │                   │                          │
│  ┌────────────────┐  ┌────────────────┐                                    │
│  │    TASK-004    │  │    TASK-005    │                                    │
│  │   Critical     │  │    Quick       │                                    │
│  │  Constraints   │  │   Reference    │                                    │
│  │   (~15 LOC)    │  │   (~15 LOC)    │                                    │
│  └───────┬────────┘  └───────┬────────┘                                    │
│          │                   │                                              │
│          └───────────────────┴───────────────────────────────────────┐     │
│                                      │                               │     │
│                                      ▼                               │     │
│  ┌─────────────────────────────────────────────────────────────┐    │     │
│  │           BUG FIXES (Applied During Section Creation)        │    │     │
│  │  ────────────────────────────────────────────────────────── │    │     │
│  │  • BUG-001: Fix "relationships to to" typo                   │    │     │
│  │  • BUG-002: Fix Story folder {EnablerId} → {StoryId}         │    │     │
│  │  • BUG-003: Fix template path inconsistency                  │    │     │
│  └─────────────────────────────────────────────────────────────┘    │     │
│                                                                      │     │
│                              ┌───────────────────────────────────────┘     │
│                              │                                             │
│                              ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                  DISC-002 ADVERSARIAL REVIEW LOOP                    │  │
│  │                  (per section until ≥0.92 or escalation)             │  │
│  │  ┌───────────────────────────────────────────────────────────────┐  │  │
│  │  │   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐    │  │  │
│  │  │   │  GENERATE   │────►│  ps-critic  │────►│ Score ≥0.92?│    │  │  │
│  │  │   │  Section    │     │  REVIEW     │     └──────┬──────┘    │  │  │
│  │  │   └─────────────┘     │ C/A/CL/AC/T │            │           │  │  │
│  │  │         ▲             └─────────────┘     YES    │   NO      │  │  │
│  │  │         │                                        ▼           │  │  │
│  │  │         │                                 ┌─────────────┐    │  │  │
│  │  │         │                                 │ Iteration<3?│    │  │  │
│  │  │         │                                 └──────┬──────┘    │  │  │
│  │  │         │             ┌───────────────┐    YES   │   NO      │  │  │
│  │  │         └─────────────│ REVISE (REM-*)│◄─────────┘           │  │  │
│  │  │                       └───────────────┘          │           │  │  │
│  │  │                                                  ▼           │  │  │
│  │  │                       ┌───────────────┐   ┌──────────┐       │  │  │
│  │  │                       │   ESCALATE    │   │  ACCEPT  │       │  │  │
│  │  │                       └───────────────┘   └──────────┘       │  │  │
│  │  └───────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║                    QUALITY GATE 1 (QG-1): SECTION REVIEW                 ║
    ║     DISC-002 Adversarial Review - Both ps-critic AND nse-qa             ║
    ║  ┌───────────────────────────────────────────────────────────────────┐  ║
    ║  │  ┌─────────────────────┐     ┌─────────────────────┐             │  ║
    ║  │  │     ps-critic       │     │      nse-qa         │             │  ║
    ║  │  │  Quality Evaluator  │     │  NASA SE Compliance │             │  ║
    ║  │  │  ──────────────────│     │  ─────────────────── │             │  ║
    ║  │  │  Criteria:          │     │  Criteria:          │             │  ║
    ║  │  │  • Completeness     │     │  • Technical Rigor  │             │  ║
    ║  │  │  • Accuracy         │     │  • Req Traceability │             │  ║
    ║  │  │  • Clarity          │     │  • Verification Evid│             │  ║
    ║  │  │  • Actionability    │     │  • Risk Ident       │             │  ║
    ║  │  │  • Traceability     │     │  • Doc Quality      │             │  ║
    ║  │  └─────────────────────┘     └─────────────────────┘             │  ║
    ║  │                                                                   │  ║
    ║  │  Pass Condition: Both reviews ≥0.92 OR human-approved            │  ║
    ║  │  Location: quality-gates/qg-1/                                   │  ║
    ║  └───────────────────────────────────────────────────────────────────┘  ║
    ║  STATUS: PENDING                                                         ║
    ╚═════════════════════════════════════════════════════════════════════════╝
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     PHASE 2: INTEGRATION & ASSEMBLY                          │
│                         Execution Mode: SEQUENTIAL                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │            nse-qa: Integration Quality Audit (Batch Review)           │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │ Validates assembled CLAUDE.md:                                   │  │  │
│  │  │ • INT-001: Line Count Target (60-80 lines)                       │  │  │
│  │  │ • INT-002: Token Count Target (~3,300-3,500 tokens)              │  │  │
│  │  │ • INT-003: All Navigation Pointers Resolve                       │  │  │
│  │  │ • INT-004: No Duplicated Content                                 │  │  │
│  │  │ • INT-005: All Bug Fixes Applied (BUG-001, 002, 003)            │  │  │
│  │  │ • INT-006: Consistent Formatting                                 │  │  │
│  │  │ • INT-007: Critical Constraints Present (P-003, P-020, P-022)   │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                       │  │
│  │  Output: quality-gates/qg-2/integration-qa-report.md                  │  │
│  │  Quality Threshold: 92% compliance | Max Iterations: 3                │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║                   QUALITY GATE 2 (QG-2): INTEGRATION                     ║
    ║     Final validation of assembled CLAUDE.md                             ║
    ║  ┌───────────────────────────────────────────────────────────────────┐  ║
    ║  │ Pass Condition: Integration review ≥92% OR human-approved         │  ║
    ║  │ No critical findings | High findings ≤3                           │  ║
    ║  │ Line count verified: 60-80 lines                                  │  ║
    ║  │ Location: quality-gates/qg-2/                                     │  ║
    ║  └───────────────────────────────────────────────────────────────────┘  ║
    ║  STATUS: PENDING                                                         ║
    ╚═════════════════════════════════════════════════════════════════════════╝
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PHASE 3: VALIDATION (Sequential)                          │
│                         Execution Mode: SEQUENTIAL                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────┐       ┌──────────────────────────┐           │
│  │       TASK-006           │──────►│       TASK-007           │           │
│  │ Validate All Pointers    │       │ Verify Line Count        │           │
│  │ Resolve Correctly        │       │ Target: 60-80 lines      │           │
│  └──────────────────────────┘       └──────────────────────────┘           │
│                                                                             │
│  DISC-002 review loop for each task (ps-critic + verification)              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                         ┌────────────────────────┐
                         │     EN-202 COMPLETE    │
                         │  All 8 Tasks Done      │
                         │  All QGs Passed        │
                         │  CLAUDE.md: 60-80 LOC  │
                         │  Tokens: ~3,500        │
                         │  Enable EN-204         │
                         └────────────────────────┘
```

### 2.3 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | Phases execute in order (0→1→2→3) |
| Concurrent | Yes | Tasks 001-005 run in parallel within Phase 1 |
| Barrier Sync | Yes | Checkpoints between phases |
| Generator-Critic | Yes | Adversarial review loops per task |
| Fan-Out/Fan-In | Yes | Parallel section creation, integration assembly |

---

## 3. Phase Definitions

### 3.0 Phase 0: Navigation Tables (Prerequisite)

| Task | Name | Scope | Status |
|------|------|-------|--------|
| TASK-000 | Navigation Tables | 23 files (rules + templates) | PENDING |

**Why First:** Navigation tables improve Claude's comprehension of referenced files during rewrite.

### 3.1 Phase 1: Section Creation (Parallel)

| Task | Name | Target LOC | Content Source | Status |
|------|------|------------|----------------|--------|
| TASK-001 | Identity Section | ~10 | Framework purpose, core principle | PENDING |
| TASK-002 | Navigation Section | ~20 | Where to find standards, skills, knowledge | PENDING |
| TASK-003 | Active Project Section | ~15 | JERRY_PROJECT, hook interpretation | PENDING |
| TASK-004 | Critical Constraints | ~15 | P-003, P-020, P-022, Python/UV | PENDING |
| TASK-005 | Quick Reference | ~15 | CLI commands, skill invocation | PENDING |

**Bug Fixes During Section Creation:**

| Bug ID | Description | Applied In |
|--------|-------------|------------|
| BUG-001 | "relationships to to" typo | Any section touching relationships |
| BUG-002 | Story folder {EnablerId} → {StoryId} | Navigation or Quick Reference |
| BUG-003 | Template path inconsistency | Quick Reference (template paths) |

### 3.2 Phase 2: Integration & Assembly

| Agent | Purpose | Input | Output | Status |
|-------|---------|-------|--------|--------|
| nse-qa | Integration audit | 5 sections assembled | QA report | PENDING |

### 3.3 Phase 3: Validation

| Task | Name | Depends On | Status |
|------|------|------------|--------|
| TASK-006 | Validate Pointers | Phase 2 complete | BLOCKED |
| TASK-007 | Verify Line Count | TASK-006 complete | BLOCKED |

---

## 4. Agent Selection Rationale

### 4.1 Background Agent Strategy

Following EN-201 pattern, maximize parallel execution using background agents:

| Phase | Agent Type | Background? | Rationale |
|-------|------------|-------------|-----------|
| Phase 0 | ps-writer | Yes | Navigation tables can run independently |
| Phase 1 | ps-writer (×5) | Yes | All 5 sections can be created in parallel |
| Phase 1 | ps-critic (×5) | Yes | Quality reviews can run after each section |
| Phase 2 | nse-qa | Yes | Integration review after sections complete |
| Phase 3 | Main context | No | Sequential validation requires interaction |

### 4.2 Agent Capability Matrix

| Agent | Quality Score | Iterative Loop | Compliance Check | Best For |
|-------|--------------|----------------|------------------|----------|
| ps-writer | N/A (generator) | N/A | ❌ | Content creation |
| ps-critic | 0.0-1.0 | ✅ Native | ❌ | Per-task quality review |
| nse-qa | % score | ❌ | ✅ Native | Batch validation |

---

## 5. DISC-002 Quality Criteria

### 5.1 ps-critic: Quality Evaluator Criteria

| Criterion | Code | Weight | Description |
|-----------|------|--------|-------------|
| Completeness | C | 0.30 | Section contains all required content |
| Accuracy | A | 0.25 | Information is correct and current |
| Clarity | CL | 0.20 | Clear, concise, well-organized |
| Actionability | AC | 0.15 | Provides actionable guidance |
| Traceability | T | 0.10 | Links to source materials |

**Quality Score Formula:** `Score = (C × 0.30) + (A × 0.25) + (CL × 0.20) + (AC × 0.15) + (T × 0.10)`

### 5.2 nse-qa: Integration Checklist (INT-*)

| Check ID | Criterion | Pass Condition | Verification |
|----------|-----------|----------------|--------------|
| INT-001 | Line Count | 60-80 lines | `wc -l CLAUDE.md` |
| INT-002 | Token Count | 3,300-3,500 tokens | `/context` command |
| INT-003 | Pointers Resolve | All navigation links work | Manual test |
| INT-004 | No Duplication | No content from rules/ | Diff check |
| INT-005 | Bug Fixes | BUG-001,002,003 resolved | Content review |
| INT-006 | Formatting | Consistent markdown style | Style check |
| INT-007 | Constraints | P-003, P-020, P-022 documented | Content check |

---

## 6. Target CLAUDE.md Structure

### 6.1 Section Layout (~75 lines)

```markdown
# CLAUDE.md - Jerry Framework Root Context

> This file provides context to Claude Code at session start.
> It serves as **procedural memory** - loaded once, not maintained in context.

---

## Project Overview (~10 lines)
- Framework purpose
- Core principle (context rot)
- Key solution approach

## Navigation (~20 lines)
- Where to find coding standards
- Where to find skills
- Where to find project context
- Where to find knowledge

## Active Project (~15 lines)
- JERRY_PROJECT variable
- Hook output interpretation
- Project context enforcement

## Critical Constraints (~15 lines)
- P-003: No recursive subagents (HARD)
- P-020: User authority (HARD)
- P-022: No deception (HARD)
- Python 3.11+ / UV only

## Quick Reference (~15 lines)
- CLI command summary
- Skill invocation summary
- Key file locations
```

### 6.2 Content Migration Matrix

| Current Content (914 lines) | New Location | Lines |
|-----------------------------|--------------|-------|
| Worktracker hierarchy | `/worktracker` skill rules | 371 → 0 |
| System mappings | `/worktracker` skill rules | 0 (extracted) |
| Template info | `/worktracker` skill rules | 0 (extracted) |
| Core identity | CLAUDE.md Identity section | ~10 |
| Navigation | CLAUDE.md Navigation section | ~20 |
| Project context | CLAUDE.md Active Project section | ~15 |
| Constraints | CLAUDE.md Constraints section | ~15 |
| Quick ref | CLAUDE.md Quick Reference section | ~15 |

---

## 7. State Files

| File | Purpose | Location |
|------|---------|----------|
| `ORCHESTRATION_PLAN.md` | Strategic context (this file) | `orchestration/` |
| `ORCHESTRATION.yaml` | Machine-readable state (SSOT) | `orchestration/` |
| `ORCHESTRATION_WORKTRACKER.md` | Tactical execution tracking | `orchestration/` |

### 7.1 Artifact Locations

```
EN-202-claude-md-rewrite/
├── orchestration/
│   ├── ORCHESTRATION_PLAN.md          # This file (strategic context)
│   ├── ORCHESTRATION.yaml             # Machine state (SSOT)
│   ├── ORCHESTRATION_WORKTRACKER.md   # Execution tracking (tactical)
│   │
│   ├── quality-gates/                 # DISC-002 Review Artifacts
│   │   ├── qg-1/                      # Quality Gate 1: Section Review
│   │   │   ├── ps-critic-review.md
│   │   │   ├── nse-qa-audit.md
│   │   │   └── remediation-log.md
│   │   │
│   │   └── qg-2/                      # Quality Gate 2: Integration Review
│   │       └── integration-qa-report.md
│   │
│   └── escalations/                   # Human escalation docs (if needed)
│
├── TASK-000-add-navigation-tables.md
├── TASK-001-create-identity-section.md
├── TASK-002-create-navigation-section.md
├── TASK-003-create-active-project-section.md
├── TASK-004-create-critical-constraints-section.md
├── TASK-005-create-quick-reference-section.md
├── TASK-006-validate-pointers.md
├── TASK-007-verify-line-count.md
├── BUG-001-relationships-typo.md
├── BUG-002-story-folder-id-mismatch.md
└── BUG-003-template-path-inconsistency.md
```

---

## 8. Execution Constraints

### 8.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator → Worker only |
| File persistence | P-002 | All state to filesystem |
| No deception | P-022 | Transparent quality scores |
| User authority | P-020 | User approves escalations |

### 8.2 Workflow Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Quality threshold | 0.92 | High bar for CLAUDE.md accuracy |
| Max iterations | 3 | Circuit breaker to prevent loops |
| Max concurrent tasks | 5 | All Phase 1 sections in parallel |
| Target line count | 60-80 | Lean context loading |
| Target tokens | 3,300-3,500 | 91-93% reduction from current |

---

## 9. Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Critical info omitted | Medium | High | nse-qa integration check; ps-critic completeness |
| Pointers broken | Low | Medium | TASK-006 validation; manual test |
| Line count exceeded | Low | Medium | TASK-007 verification; iterative trimming |
| Bug fixes missed | Low | Medium | Explicit checklist in INT-005 |
| Quality loop stuck | Low | Medium | 3-iteration circuit breaker |

---

## 10. Success Criteria

### 10.1 Phase Completion Criteria

| Phase | Criterion | Validation |
|-------|-----------|------------|
| Phase 0 | Navigation tables added | File inspection |
| Phase 1 | All 5 sections ≥ 0.92 | ps-critic quality scores |
| Phase 2 | Integration review ≥ 92% | nse-qa compliance score |
| Phase 3 | Pointers work, line count met | Manual verification |

### 10.2 Workflow Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All 8 tasks complete | Task status = DONE |
| All quality gates passed | QG status = COMPLETE |
| CLAUDE.md 60-80 lines | `wc -l CLAUDE.md` |
| Token count ~3,500 | `/context` command |
| All bugs fixed | BUG-001,002,003 resolved |
| EN-204 unblocked | Dependency resolution |

---

## 11. Resumption Context

### 11.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-02-01
================================

Phase 0 (Navigation Tables):
  TASK-000: PENDING

Phase 1 (Section Creation):
  TASK-001: BLOCKED (waiting TASK-000)
  TASK-002: BLOCKED (waiting TASK-000)
  TASK-003: BLOCKED (waiting TASK-000)
  TASK-004: BLOCKED (waiting TASK-000)
  TASK-005: BLOCKED (waiting TASK-000)

Phase 2 (Integration):
  nse-qa: BLOCKED (waiting Phase 1)

Phase 3 (Validation):
  TASK-006: BLOCKED (waiting Phase 2)
  TASK-007: BLOCKED (waiting TASK-006)

Quality Gates:
  QG-1: PENDING
  QG-2: PENDING

Checkpoints:
  CP-0: PENDING (after TASK-000)
  CP-1: PENDING (after Phase 1)
```

### 11.2 Next Actions

1. **Execute TASK-000** (Navigation tables) as background agent
2. Upon TASK-000 complete: checkpoint CP-0
3. **Execute TASK-001-005** in parallel as background agents
4. For each task: generate → ps-critic → iterate until ≥0.92
5. Upon all Phase 1 complete: QG-1 with ps-critic + nse-qa
6. **Assemble CLAUDE.md** from 5 sections
7. Execute nse-qa integration review
8. Upon QG-2 pass: TASK-006, TASK-007 sequential
9. Workflow complete → EN-204 unblocked

---

*Document ID: EN-202-ORCH-PLAN*
*Workflow ID: en202-rewrite-20260201-001*
*Version: 1.0*
*Cross-Session Portable: All paths are repository-relative*
