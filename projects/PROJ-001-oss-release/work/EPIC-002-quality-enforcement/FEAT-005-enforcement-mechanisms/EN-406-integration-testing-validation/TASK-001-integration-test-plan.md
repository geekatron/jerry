# TASK-001: Comprehensive Integration Test Plan

<!--
TEMPLATE: Task Deliverable
VERSION: 1.0.0
ENABLER: EN-406
AC: AC-1
CREATED: 2026-02-13 (ps-validator-406)
PURPOSE: Master integration test plan for all enforcement mechanisms
-->

> **Type:** deliverable
> **Status:** complete
> **Parent:** EN-406-integration-testing-validation
> **AC Mapping:** AC-1 (Comprehensive integration test plan documented and approved)
> **Agent:** ps-validator-406
> **Created:** 2026-02-13

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Test plan scope and objectives |
| [Architecture Under Test](#architecture-under-test) | 5-Layer enforcement architecture summary |
| [Test Scope](#test-scope) | What is tested and what is excluded |
| [Enforcement Mechanism Inventory](#enforcement-mechanism-inventory) | Complete inventory of mechanisms |
| [Test Categories](#test-categories) | Categories of tests with rationale |
| [Individual Mechanism Test Matrix](#individual-mechanism-test-matrix) | Per-mechanism test scenarios |
| [Interaction Test Matrix](#interaction-test-matrix) | Cross-mechanism interaction tests |
| [Test Prerequisites](#test-prerequisites) | Environment setup and dependencies |
| [Test Environment](#test-environment) | Required environment configuration |
| [Expected Outcomes](#expected-outcomes) | Pass/fail criteria per test |
| [Test Execution Strategy](#test-execution-strategy) | Order, parallelism, and gating |
| [Risk Assessment](#risk-assessment) | Testing risks and mitigations |
| [Traceability Matrix](#traceability-matrix) | Test-to-requirement mapping |
| [References](#references) | Source documents and predecessors |

---

## Overview

This document defines the master integration test plan for EN-406 (Integration Testing & Cross-Platform Validation). It covers all enforcement mechanisms defined in FEAT-005: hook-based enforcement (EN-403), rule-based enforcement (EN-404), and session context enforcement (EN-405). The plan addresses individual mechanism testing, interaction testing, performance benchmarking, platform validation, CI/CD non-regression, QA audit, and NFC verification.

### Objectives

1. Validate that each enforcement mechanism works correctly end-to-end in its designed role.
2. Validate that enforcement mechanisms work together without conflicts, gaps, or unexpected interactions.
3. Validate that the defense-in-depth compensation chain operates correctly (L1 degrades -> L2 re-injects -> L3 blocks deterministically).
4. Validate performance overhead stays within the <2s budget (NFC-1).
5. Validate macOS as the primary platform and assess Windows/Linux portability.
6. Validate that enforcement does not break existing CI/CD pipelines (NFC-3).
7. Verify all FEAT-005 acceptance criteria (AC-1 through AC-19) and non-functional criteria (NFC-1 through NFC-8).
8. Close EN-405 conditional ACs: AC-4 (integration test execution), AC-5 (auto-loading verification), AC-8 (macOS tests).

### Quality Context

| Predecessor | Quality Score | Status |
|-------------|---------------|--------|
| EN-402 (Priority Analysis) | 0.923 | PASS |
| EN-403 (Hook-Based Enforcement) | 0.930 | PASS |
| EN-404 (Rule-Based Enforcement) | 0.930 | PASS |
| EN-405 (Session Context Enforcement) | 0.936 | CONDITIONAL PASS |
| EN-406 Target | >= 0.920 | In Progress |

---

## Architecture Under Test

The 5-Layer Hybrid Enforcement Architecture (ADR-EPIC002-002):

| Layer | Name | Mechanism | Token Cost | Rot Immunity |
|-------|------|-----------|------------|--------------|
| L1 | Static Context | `.claude/rules/` auto-loaded files | ~12,476 tokens (target) | LOW (degrades with context) |
| L2 | Dynamic Injection | UserPromptSubmit hook (V-024) | ~600 tokens/prompt | MEDIUM (refreshed per prompt) |
| L3 | Active Enforcement | PreToolUse hook (V-038, V-041) | 0 tokens (deterministic) | HIGH (context-rot immune) |
| L4 | Passive Monitoring | (Planned - not in scope) | -- | -- |
| L5 | Post-Hoc Analysis | (Planned - not in scope) | -- | -- |

### Defense-in-Depth Compensation Chain

```
L1 (Static Context)
  |-- degrades via context rot -->
L2 (Dynamic Injection)
  |-- re-injects quality context per prompt -->
L3 (Active Enforcement)
  |-- deterministic blocking, zero token cost -->
  OUTCOME: Enforcement maintained regardless of context rot
```

---

## Test Scope

### In Scope

| Category | Items | Source |
|----------|-------|--------|
| Hooks | UserPromptSubmit (L2), PreToolUse (L3), SessionStart (L1 enhancement) | EN-403 |
| Rules | `.claude/rules/` files, HARD/MEDIUM/SOFT tiers, 24 HARD rules | EN-404 |
| Session Context | SessionQualityContextGenerator, 4-section XML preamble, ~435 calibrated tokens | EN-405 |
| Performance | <2s overhead per enforcement path | NFC-1 |
| Platform | macOS primary validation, Windows/Linux assessment | NFC-2 |
| CI/CD | Non-regression testing | NFC-3 |
| Quality Gates | >= 0.92 threshold | FEAT-005 |

### Out of Scope

| Category | Reason |
|----------|--------|
| L4 Passive Monitoring | Planned for future phase |
| L5 Post-Hoc Analysis | Planned for future phase |
| Runtime test execution | These are design-phase test SPECIFICATIONS |
| Adversarial strategy effectiveness | Unverifiable in design phase (RISK-L2-001) |
| Claude behavioral compliance | LLM response verification is non-deterministic |

---

## Enforcement Mechanism Inventory

### Hook-Based Enforcement (EN-403)

| Hook | Layer | Purpose | Entry Point | Engine |
|------|-------|---------|-------------|--------|
| UserPromptSubmit | L2 | Per-prompt quality context reinforcement via V-024 | `hooks/user-prompt-submit.py` | `PromptReinforcementEngine` |
| PreToolUse | L3 | Pre-action gating with AST validation (V-038, V-041) | `hooks/pre-tool-use.py` | `PreToolEnforcementEngine` |
| SessionStart | L1 | One-time quality context injection at session init | `scripts/session_start_hook.py` | `SessionQualityContextGenerator` |

### Rule-Based Enforcement (EN-404)

| File | Target Tokens | Tier Distribution | Key Content |
|------|---------------|-------------------|-------------|
| `quality-enforcement.md` | ~2,200 | HARD dominant | SSOT for enforcement constants |
| `coding-standards.md` | ~2,100 | HARD/MEDIUM mix | Python 3.11+, type hints, CQRS naming |
| `architecture-standards.md` | ~2,200 | HARD dominant | Hexagonal, dependency rules |
| `testing-standards.md` | ~1,500 | HARD/MEDIUM mix | BDD cycle, AAA pattern, 90% coverage |
| `error-handling-standards.md` | ~1,200 | HARD/MEDIUM mix | Exception hierarchy |
| `file-organization.md` | ~800 | MEDIUM dominant | Directory structure |
| `python-environment.md` | ~600 | HARD dominant | UV only, no system Python |
| `mandatory-skill-usage.md` | ~576 | MEDIUM dominant | Proactive skill invocation |
| **Total** | **~11,176** | | Target: 12,476 (1,300 buffer) |

### Session Context Enforcement (EN-405)

| Component | Content | Tokens |
|-----------|---------|--------|
| `<quality-gate>` | Scoring criteria, >= 0.92 threshold, mandatory self-review | ~100 calibrated |
| `<constitutional-principles>` | P-003, P-020, P-022 hard constraints | ~85 calibrated |
| `<adversarial-strategies>` | 10 strategies (S-001 through S-014 subset), context rot awareness | ~174 calibrated |
| `<decision-criticality>` | C1-C4 levels, AUTO-ESCALATE rules AE-001 through AE-004 | ~130 calibrated |
| **Total Preamble** | ~2,096 characters | **~435 calibrated tokens** |

---

## Test Categories

| Category | ID | Description | Deliverable |
|----------|----|-------------|-------------|
| Hook E2E Testing | TC-HOOK | End-to-end test of each hook type individually | TASK-002 |
| Rule E2E Testing | TC-RULE | End-to-end test of rule enforcement tiers | TASK-003 |
| Session Context E2E Testing | TC-SESS | End-to-end test of session context injection | TASK-004 |
| Interaction Testing | TC-IXTN | Cross-mechanism interaction and conflict tests | TASK-005 |
| Performance Benchmarking | TC-PERF | <2s overhead validation | TASK-006 |
| Platform Validation | TC-PLAT | macOS validation + cross-platform assessment | TASK-007, TASK-008 |
| CI/CD Non-Regression | TC-CICD | Pipeline compatibility testing | TASK-008 (cross-ref TASK-009) |
| QA Audit | TC-QA | FEAT-005 AC verification | TASK-009 (cross-ref TASK-010) |
| NFC Verification | TC-NFC | NFC-1 through NFC-8 | TASK-010 (cross-ref TASK-011) |

---

## Individual Mechanism Test Matrix

### TC-HOOK: Hook Enforcement Tests

| Test ID | Hook | Scenario | Input | Expected Outcome | Verification |
|---------|------|----------|-------|-------------------|--------------|
| TC-HOOK-001 | UserPromptSubmit | Nominal prompt injection | Standard user prompt | `<enforcement-context>` XML appended with 7 content blocks | Inspection |
| TC-HOOK-002 | UserPromptSubmit | C1 routine decision | Low-criticality prompt | Minimal reinforcement (~200 tokens) | Inspection |
| TC-HOOK-003 | UserPromptSubmit | C4 critical decision | Governance-related prompt keywords | Full reinforcement (~600 tokens) | Inspection |
| TC-HOOK-004 | UserPromptSubmit | Token budget enforcement | Any prompt | Output <= 600 tokens | Test |
| TC-HOOK-005 | UserPromptSubmit | Error resilience | Malformed prompt | Fail-open, no crash (REQ-403-070) | Test |
| TC-HOOK-006 | PreToolUse | Valid write to allowed path | Write to `src/domain/` | Action: approve | Test |
| TC-HOOK-007 | PreToolUse | Import boundary violation | Write with `from src.infrastructure` in domain file | Action: block, V-038 violation | Test |
| TC-HOOK-008 | PreToolUse | One-class-per-file violation | Write with 2 public classes | Action: block, V-041 violation | Test |
| TC-HOOK-009 | PreToolUse | Governance escalation | Write to JERRY_CONSTITUTION.md | Criticality escalated to C4 | Test |
| TC-HOOK-010 | PreToolUse | Phase execution order | Any tool use | Phases 1-5 execute sequentially | Inspection |
| TC-HOOK-011 | PreToolUse | Performance budget | Any tool use | Total < 87ms | Test |
| TC-HOOK-012 | PreToolUse | Error resilience | Invalid tool input | Fail-open, approve with warning (REQ-403-070) | Test |
| TC-HOOK-013 | SessionStart | Quality preamble injection | Session initialization | 4-section XML preamble appended to hook output | Inspection |
| TC-HOOK-014 | SessionStart | Token budget | Session initialization | Preamble <= 435 calibrated tokens (~524 conservative) | Test |
| TC-HOOK-015 | SessionStart | Graceful degradation | Missing quality module | QUALITY_CONTEXT_AVAILABLE = False, session starts normally | Test |
| TC-HOOK-016 | SessionStart | Integration with existing output | Session with project context | Quality preamble appended after format_hook_output(), before output_json() | Inspection |

### TC-RULE: Rule Enforcement Tests

| Test ID | Aspect | Scenario | Input | Expected Outcome | Verification |
|---------|--------|----------|-------|-------------------|--------------|
| TC-RULE-001 | HARD tier | HARD rule presence | All rule files | 24 HARD rules (H-01 through H-24) present with MUST/SHALL/NEVER language | Inspection |
| TC-RULE-002 | HARD tier | Consequence statements | All HARD rules | Each HARD rule has stated consequence | Inspection |
| TC-RULE-003 | HARD tier | Maximum count | All rule files | <= 25 HARD rules total | Analysis |
| TC-RULE-004 | MEDIUM tier | MEDIUM rule presence | All rule files | SHOULD/RECOMMENDED language used | Inspection |
| TC-RULE-005 | SOFT tier | SOFT rule presence | All rule files | MAY/CONSIDER language used | Inspection |
| TC-RULE-006 | Token budget | Total L1 token count | All `.claude/rules/` files | <= 12,476 tokens | Test |
| TC-RULE-007 | Token budget | Per-file budget | Each rule file | Within allocated budget per EN-404 TASK-003 | Analysis |
| TC-RULE-008 | L2 re-injection | L2-REINJECT tags | Rule files | L2-REINJECT tags present with rank, tokens, content | Inspection |
| TC-RULE-009 | Quality SSOT | quality-enforcement.md | File exists and contains enforcement constants | Inspection | |
| TC-RULE-010 | Auto-loading | `.claude/rules/` loading | Claude Code session | All rule files auto-loaded at session start | Test |
| TC-RULE-011 | Redundancy reduction | Cross-file duplication | All rule files | No redundant content across files | Inspection |

### TC-SESS: Session Context Tests

| Test ID | Aspect | Scenario | Input | Expected Outcome | Verification |
|---------|--------|----------|-------|-------------------|--------------|
| TC-SESS-001 | Preamble generation | Nominal generation | SessionQualityContextGenerator.generate() | 4-section XML output | Test |
| TC-SESS-002 | Quality gate section | Content correctness | Generated preamble | Contains scoring criteria, >= 0.92 threshold, self-review requirement | Inspection |
| TC-SESS-003 | Constitutional section | Content correctness | Generated preamble | Contains P-003, P-020, P-022 | Inspection |
| TC-SESS-004 | Adversarial section | Content correctness | Generated preamble | Contains 10 strategies with context rot awareness | Inspection |
| TC-SESS-005 | Criticality section | Content correctness | Generated preamble | Contains C1-C4 levels, AE-001 through AE-004 auto-escalate rules | Inspection |
| TC-SESS-006 | Token budget | Total preamble tokens | Generated preamble | <= 435 calibrated tokens, ~2,096 characters | Test |
| TC-SESS-007 | Degradation priority | Budget-constrained generation | Reduced token budget | Degrades in priority order: strategy descriptions -> C1-C4 -> pairing line | Test |
| TC-SESS-008 | Error handling | Missing dependencies | Import failure | QUALITY_CONTEXT_AVAILABLE = False, graceful fallback | Test |
| TC-SESS-009 | Integration point | Hook output integration | Session start execution | Preamble after format_hook_output(), before output_json() | Inspection |

---

## Interaction Test Matrix

### Cross-Mechanism Interaction Tests (TC-IXTN)

| Test ID | Mechanisms | Interaction | Potential Conflict | Expected Behavior | Verification |
|---------|-----------|-------------|--------------------|--------------------|--------------|
| TC-IXTN-001 | L1 + L2 | Rule context + prompt reinforcement | Redundant quality guidance | L2 compact reinforcement supplements (not duplicates) L1 comprehensive rules | Inspection |
| TC-IXTN-002 | L1 + L3 | Rule context + PreToolUse blocking | Conflicting enforcement signals | L3 deterministic blocking overrides any L1 ambiguity | Test |
| TC-IXTN-003 | L2 + L3 | Prompt reinforcement + PreToolUse blocking | V-024 reinforces what L3 blocks | L3 blocks regardless of L2 guidance (defense-in-depth) | Test |
| TC-IXTN-004 | L1 + Session | Rules + session preamble | Overlapping constitutional principles | Session preamble provides compact summary; rules provide full detail | Inspection |
| TC-IXTN-005 | L2 + Session | Prompt injection + session preamble | Both inject quality context | L2 per-prompt is additive to L1 session-start preamble | Inspection |
| TC-IXTN-006 | L3 + Session | PreToolUse + session preamble | Session context irrelevant to L3 | L3 operates independently of any injected context (zero token) | Test |
| TC-IXTN-007 | L1 + L2 + L3 | All three layers | Full defense-in-depth chain | Compensation chain: L1 degrades -> L2 re-injects -> L3 blocks | Analysis |
| TC-IXTN-008 | Rules + Hooks | HARD rule H-01 + PreToolUse V-038 | Import boundary enforcement overlap | Both enforce same boundary; no conflict, mutual reinforcement | Inspection |
| TC-IXTN-009 | All | Complete enforcement stack | Nominal session with all mechanisms active | All mechanisms operate without interference or performance degradation | Test |
| TC-IXTN-010 | L1 degraded + L2 + L3 | Context rot simulation | L1 rules degraded after long context | L2 successfully re-injects key principles; L3 still blocks violations | Analysis |

---

## Test Prerequisites

### Environment Requirements

| Requirement | Description | Validation |
|-------------|-------------|------------|
| Python 3.11+ | Runtime for hooks and enforcement engines | `python --version` |
| UV | Python dependency management | `uv --version` |
| Claude Code | Claude Code CLI with hook support | `claude --version` |
| macOS | Primary validation platform | `uname -s` |
| Git | Repository operations | `git --version` |
| Jerry Framework | Full Jerry framework installation | `uv run jerry session status` |

### File Prerequisites

| File/Directory | Purpose | Must Exist |
|----------------|---------|------------|
| `hooks/user-prompt-submit.py` | UserPromptSubmit hook entry point | Yes |
| `hooks/pre-tool-use.py` | PreToolUse hook entry point | Yes (or planned) |
| `scripts/session_start_hook.py` | SessionStart hook | Yes |
| `.claude/rules/*.md` | Auto-loaded rule files | Yes |
| `src/infrastructure/internal/enforcement/` | Enforcement engine modules | Yes (or planned) |
| `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py` | L2 engine | Yes (or planned) |
| `src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py` | L3 engine | Yes (or planned) |
| `src/infrastructure/internal/enforcement/session_quality_context.py` | Session context generator | Yes (or planned) |

### Data Prerequisites

| Data | Description | Source |
|------|-------------|--------|
| 24 HARD rules inventory | Complete list of H-01 through H-24 | EN-404 TASK-003 |
| Token budgets | Per-file and total token allocations | EN-404 TASK-003 |
| Preamble content | Exact XML preamble text | EN-405 TASK-006 |
| Requirements traceability | 44 + 44 + 34 requirements | EN-403/404/405 TASK-001 |

---

## Test Environment

### macOS Primary Environment

| Component | Version/Configuration |
|-----------|----------------------|
| OS | macOS (Darwin 25.x) |
| Python | 3.11+ via UV |
| Shell | zsh |
| Claude Code | Latest with hook support |
| Git | Latest |

### Test Isolation

Each test execution MUST:
1. Start from a clean Jerry session state
2. Not depend on prior test results (unless in a defined sequence)
3. Clean up any temporary files created
4. Log all outputs for post-analysis

---

## Expected Outcomes

### Pass Criteria

| Criterion | Threshold | Measurement |
|-----------|-----------|-------------|
| Hook tests pass rate | 100% of TC-HOOK tests | Count pass/fail |
| Rule tests pass rate | 100% of TC-RULE tests | Count pass/fail |
| Session tests pass rate | 100% of TC-SESS tests | Count pass/fail |
| Interaction tests pass rate | 100% of TC-IXTN tests | Count pass/fail |
| Performance overhead | < 2 seconds per enforcement path | Timing measurement |
| Platform validation | macOS 100% pass | Platform-specific test run |
| CI/CD non-regression | 0 broken pipelines | CI pipeline execution |
| FEAT-005 AC coverage | 19/19 ACs verified | QA audit checklist |
| NFC verification | 8/8 NFCs verified | NFC checklist |

### Fail Criteria

Any of the following constitutes a test plan failure:
1. Any TC-HOOK, TC-RULE, or TC-SESS test fails with no documented exception
2. Any TC-IXTN test reveals an unresolvable conflict
3. Performance exceeds 2s on any enforcement path
4. macOS platform validation fails
5. CI/CD regression detected
6. Any FEAT-005 AC cannot be verified

---

## Test Execution Strategy

### Execution Order

```
Phase 1: Individual Mechanism Testing (parallelizable)
  ├── TC-HOOK (TASK-002)
  ├── TC-RULE (TASK-003)
  └── TC-SESS (TASK-004)

Phase 2: Interaction Testing (depends on Phase 1)
  └── TC-IXTN (TASK-005)

Phase 3: Performance & Platform (depends on Phase 2)
  ├── TC-PERF (TASK-006)
  ├── TC-PLAT macOS (TASK-007)
  └── TC-PLAT cross-platform (TASK-008)

Phase 4: Compliance & Reporting (depends on Phase 3)
  ├── TC-CICD (TASK-009)
  ├── TC-QA (TASK-010)
  ├── TC-NFC (TASK-011)
  ├── Status Report (TASK-012)
  └── Configuration Baseline (TASK-013)
```

### Gating Rules

- Phase 2 cannot begin until all Phase 1 tests pass.
- Phase 3 cannot begin until all Phase 2 tests pass.
- Phase 4 cannot begin until Phases 1-3 are complete.
- Any blocking failure stops forward progress until resolved.

---

## Risk Assessment

| Risk ID | Description | Probability | Impact | Mitigation |
|---------|-------------|-------------|--------|------------|
| RISK-406-001 | Hooks not yet implemented (design-phase only) | HIGH | MEDIUM | Test specifications validate design; implementation tested later |
| RISK-406-002 | Token counting methodology inconsistent | MEDIUM | HIGH | Use chars/4 approximation with 0.83x XML calibration factor consistently |
| RISK-406-003 | Context rot simulation not fully reproducible | MEDIUM | MEDIUM | Document expected degradation behavior; test L2 re-injection in isolation |
| RISK-406-004 | Cross-platform issues discovered late | LOW | HIGH | Assess early in platform validation phase |
| RISK-406-005 | Performance measurement variance | MEDIUM | LOW | Multiple runs, statistical significance |
| RISK-406-006 | EN-405 conditional ACs cannot be fully closed | LOW | HIGH | Prioritize AC-4, AC-5, AC-8 test specifications |

---

## Traceability Matrix

### Test-to-AC Mapping

| Test Category | EN-406 AC | FEAT-005 ACs | EN-405 Conditional ACs |
|---------------|-----------|--------------|------------------------|
| TC-HOOK | AC-2 | AC-3, AC-4, AC-5 | -- |
| TC-RULE | AC-3 | AC-6, AC-7, AC-8, AC-9 | -- |
| TC-SESS | AC-4 | AC-10, AC-11, AC-12 | AC-4, AC-5, AC-8 |
| TC-IXTN | AC-5 | AC-13, AC-14 | -- |
| TC-PERF | AC-6 | AC-15 (NFC-1) | -- |
| TC-PLAT | AC-7, AC-8 | AC-16 (NFC-2) | AC-8 |
| TC-CICD | AC-9 | AC-17 (NFC-3) | -- |
| TC-QA | AC-10 | All ACs | -- |
| TC-NFC | AC-11 | NFC-1 through NFC-8 | -- |

### Test-to-Requirement Mapping Summary

| Source | Requirements | Test Coverage |
|--------|-------------|---------------|
| EN-403 | 44 requirements (REQ-403-010 through REQ-403-096) | TC-HOOK covers all |
| EN-404 | 44 requirements (REQ-404-001 through REQ-404-064) | TC-RULE covers all |
| EN-405 | 34 requirements (FR-405-001 through EH-405-004) | TC-SESS covers all |
| FEAT-005 | 19 ACs + 8 NFCs | TC-QA + TC-NFC cover all |

---

## References

| Document | Path | Relevance |
|----------|------|-----------|
| EN-406 Enabler Definition | `EN-406-integration-testing-validation.md` | Enabler scope and ACs |
| FEAT-005 Feature Definition | `../FEAT-005-enforcement-mechanisms.md` | Feature ACs and NFCs |
| EN-403 TASK-001 Hook Requirements | `../EN-403-hook-based-enforcement/TASK-001-hook-requirements.md` | 44 hook requirements |
| EN-403 TASK-002 UserPromptSubmit Design | `../EN-403-hook-based-enforcement/TASK-002-userpromptsubmit-design.md` | L2 engine design |
| EN-403 TASK-003 PreToolUse Design | `../EN-403-hook-based-enforcement/TASK-003-pretooluse-design.md` | L3 engine design |
| EN-403 TASK-004 SessionStart Design | `../EN-403-hook-based-enforcement/TASK-004-sessionstart-design.md` | L1 enhancement design |
| EN-403 TASK-008 Validation Report | `../EN-403-hook-based-enforcement/TASK-008-validation-report.md` | Combined EN-403/404 validation |
| EN-404 TASK-001 Rule Requirements | `../EN-404-rule-based-enforcement/TASK-001-rule-requirements.md` | 44 rule requirements |
| EN-404 TASK-002 Rule Audit | `../EN-404-rule-based-enforcement/TASK-002-rule-audit.md` | Current state audit |
| EN-404 TASK-003 Tiered Enforcement | `../EN-404-rule-based-enforcement/TASK-003-tiered-enforcement.md` | HARD/MEDIUM/SOFT tiers, token budgets |
| EN-405 TASK-001 Requirements | `../EN-405-session-context-enforcement/TASK-001-requirements.md` | 34 session context requirements |
| EN-405 TASK-006 Preamble Content | `../EN-405-session-context-enforcement/TASK-006-preamble-content.md` | Exact XML preamble content |
| EN-405 TASK-010 Validation Report | `../EN-405-session-context-enforcement/TASK-010-validation-report.md` | EN-405 conditional pass |
| ADR-EPIC002-002 | FEAT-004 outputs | 5-Layer hybrid enforcement architecture |

---

*Generated by ps-validator-406 | 2026-02-13 | EN-406 AC-1*
