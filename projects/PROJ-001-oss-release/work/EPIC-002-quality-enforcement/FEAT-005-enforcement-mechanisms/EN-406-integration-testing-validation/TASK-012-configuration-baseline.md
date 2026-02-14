# TASK-012: Configuration Baseline Documentation

<!--
TEMPLATE: Task Deliverable
VERSION: 1.1.0
ENABLER: EN-406
AC: AC-13
CREATED: 2026-02-13 (ps-validator-406)
REVISED: 2026-02-14 (ps-revision-406) -- Iteration 1 critique fixes (F-032, F-033)
PURPOSE: Configuration baseline for all enforcement mechanisms
-->

> **Type:** deliverable
> **Status:** complete
> **Parent:** EN-406-integration-testing-validation
> **AC Mapping:** AC-13 (Configuration baseline documented)
> **Agent:** ps-validator-406
> **Created:** 2026-02-13

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Configuration baseline scope |
| [Token Budget Baselines](#token-budget-baselines) | L1 and L2 token budgets |
| [Hook Configuration Baseline](#hook-configuration-baseline) | Hook entry points and engines |
| [Rule File Baseline](#rule-file-baseline) | Rule file inventory and allocations |
| [HARD Rule Baseline](#hard-rule-baseline) | Complete HARD rule inventory |
| [Preamble Content Baseline](#preamble-content-baseline) | Session preamble configuration |
| [Performance Baselines](#performance-baselines) | Performance targets and budgets |
| [Architecture Baselines](#architecture-baselines) | Architectural configuration |
| [Quality Baselines](#quality-baselines) | Quality thresholds and criteria |
| [Change Control](#change-control) | How to update baselines |
| [References](#references) | Source documents |

---

## Overview

This document establishes the configuration baseline for all enforcement mechanisms in the FEAT-005 enforcement framework. It serves as the single reference for all configurable values, thresholds, inventories, and targets. Any changes to enforcement configuration MUST update this baseline.

### Baseline Version

| Field | Value |
|-------|-------|
| Baseline Version | 1.0.0 |
| Established | 2026-02-13 |
| Architecture | 5-Layer Hybrid Enforcement (ADR-EPIC002-002) |
| Active Layers | L1, L2, L3 (L4, L5 planned) |
| Status | Design Phase Complete |

---

## Token Budget Baselines

### L1 Static Context Budget

| Metric | Value | Source |
|--------|-------|--------|
| Total L1 target budget | 12,476 tokens | ADR-EPIC002-002, EN-404 TASK-003 |
| Current L1 actual (audit) | ~30,160 tokens | EN-404 TASK-002 |
| Target after optimization | ~11,176 tokens | EN-404 TASK-003 |
| Buffer | ~1,300 tokens | EN-404 TASK-003 |
| Measurement method | chars/4 approximation | EN-404 |

### Per-File Token Allocations

| File | Target Tokens | Priority |
|------|---------------|----------|
| `quality-enforcement.md` | ~2,200 | CRITICAL (SSOT) |
| `coding-standards.md` | ~2,100 | HIGH |
| `architecture-standards.md` | ~2,200 | HIGH |
| `testing-standards.md` | ~1,500 | MEDIUM |
| `error-handling-standards.md` | ~1,200 | MEDIUM |
| `file-organization.md` | ~800 | MEDIUM |
| `python-environment.md` | ~600 | HIGH |
| `mandatory-skill-usage.md` | ~576 | MEDIUM |
| **Total** | **~11,176** | |

### L2 Dynamic Injection Budget

| Metric | Value | Source |
|--------|-------|--------|
| L2 per-prompt budget | 600 tokens | EN-403 TASK-002 |
| L2-REINJECT content budget | ~510 tokens | EN-404 TASK-003 |
| L2-REINJECT items | 8 ranked | EN-404 TASK-003 |
| Measurement method | chars/4 | EN-403 |

### Session Preamble Budget

| Metric | Value | Source |
|--------|-------|--------|
| Character count | ~2,096 | EN-405 TASK-006 |
| Conservative tokens (chars/4) | ~524 | EN-405 TASK-006 |
| Calibrated tokens (0.83x) | ~435 | EN-405 TASK-006 |
| XML calibration factor | 0.83 | EN-405 |

### Per-Section Preamble Budget

| Section | Characters | Calibrated Tokens |
|---------|------------|-------------------|
| `<quality-gate>` | ~480 | ~100 |
| `<constitutional-principles>` | ~338 | ~85 |
| `<adversarial-strategies>` | ~696 | ~174 |
| `<decision-criticality>` | ~520 | ~130 |
| **Total** | **~2,096** | **~435** (calibrated) |

---

## Hook Configuration Baseline

### Hook Inventory

| Hook | Layer | Entry Point | Engine Module | Engine Class |
|------|-------|-------------|---------------|--------------|
| UserPromptSubmit | L2 | `hooks/user-prompt-submit.py` | `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py` | `PromptReinforcementEngine` |
| PreToolUse | L3 | `hooks/pre-tool-use.py` | `src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py` | `PreToolEnforcementEngine` |
| SessionStart | L1+ | `scripts/session_start_hook.py` | `src/infrastructure/internal/enforcement/session_quality_context.py` | `SessionQualityContextGenerator` |

### Hook Behavior Configuration

| Hook | Fail Mode | Token Cost | Criticality Detection |
|------|-----------|------------|----------------------|
| UserPromptSubmit | Fail-open | ~600/prompt | Keyword-based (C1-C4) |
| PreToolUse | Fail-open | 0 (deterministic) | Path-based governance escalation |
| SessionStart | Fail-open | ~435 (one-time) | N/A (always injects) |

### Claude Code Settings

```json
{
  "hooks": {
    "UserPromptSubmit": {
      "command": "uv run hooks/user-prompt-submit.py"
    },
    "PreToolUse": {
      "command": "uv run hooks/pre-tool-use.py"
    },
    "SessionStart": {
      "command": "uv run scripts/session_start_hook.py"
    }
  }
}
```

> **Note:** SessionStart is configured separately from UserPromptSubmit/PreToolUse. The SessionStart hook handles both project context injection and quality preamble generation. Quality context availability is controlled by the `QUALITY_CONTEXT_AVAILABLE` flag within the hook code.

---

## Rule File Baseline

### File Inventory

> **Current State vs. Target State:** The table below shows the **current state** (10 files, ~30,160 tokens) as the baseline. The **target state** after EN-404 TASK-002 optimization would consolidate to 8 files at ~11,176 tokens. The planned consolidations are listed separately below. Until optimization is executed, the current state is the operative baseline.

| # | File | Location | Current State | Target State | Tier Mix |
|---|------|----------|---------------|--------------|----------|
| 1 | `coding-standards.md` | `.claude/rules/` (-> `.context/rules/`) | Existing (~6,100 tokens) | Optimized (~2,100 tokens, absorbs error-handling) | HARD + MEDIUM |
| 2 | `architecture-standards.md` | `.claude/rules/` | Existing (~6,200 tokens) | Optimized (~2,200 tokens, absorbs file-org) | HARD dominant |
| 3 | `testing-standards.md` | `.claude/rules/` | Existing (~4,500 tokens) | Optimized (~1,500 tokens, absorbs tool-config) | HARD + MEDIUM |
| 4 | `error-handling-standards.md` | `.claude/rules/` | Existing (~3,200 tokens) | Merged into coding-standards | HARD + MEDIUM |
| 5 | `file-organization.md` | `.claude/rules/` | Existing (~2,800 tokens) | Merged into architecture-standards | MEDIUM dominant |
| 6 | `python-environment.md` | `.claude/rules/` | Existing (~1,500 tokens) | Optimized (~600 tokens) | HARD dominant |
| 7 | `mandatory-skill-usage.md` | `.claude/rules/` | Existing (~1,800 tokens) | Optimized (~576 tokens) | MEDIUM dominant |
| 8 | `quality-enforcement.md` | `.claude/rules/` | NEW (EN-404) | New (~2,200 tokens, SSOT) | HARD dominant (SSOT) |
| 9 | `markdown-navigation-standards.md` | `.claude/rules/` | Existing (~2,500 tokens) | Retained, optimized | HARD + MEDIUM |
| 10 | `project-workflow.md` | `.claude/rules/` | Existing (~1,560 tokens) | Retained, optimized | MEDIUM |
| | **Total** | | **~30,160 tokens (10 files)** | **~11,176 tokens (8 files)** | |

### Planned Consolidations (EN-404 TASK-002)

| Action | Files | Target |
|--------|-------|--------|
| Merge error-handling into coding | `error-handling-standards.md` -> `coding-standards.md` | Reduce file count |
| Merge file-org into architecture | `file-organization.md` -> `architecture-standards.md` | Reduce redundancy |
| Merge tool-config into testing | `tool-configuration.md` -> `testing-standards.md` | Reduce redundancy |
| Create quality-enforcement.md | NEW | SSOT for enforcement constants |

---

## HARD Rule Baseline

### Complete Inventory (24 Rules)

| ID | Rule | Source | File |
|----|------|--------|------|
| H-01 | UV-only Python environment (NEVER use python/pip directly) | python-environment.md | python-environment.md |
| H-02 | Type hints REQUIRED on all public functions | coding-standards.md | coding-standards.md |
| H-03 | Docstrings REQUIRED on all public functions/classes | coding-standards.md | coding-standards.md |
| H-04 | Maximum 100 characters per line | coding-standards.md | coding-standards.md |
| H-05 | Conventional commits format REQUIRED | coding-standards.md | coding-standards.md |
| H-06 | Domain layer NO external imports (hexagonal) | architecture-standards.md | architecture-standards.md |
| H-07 | Application layer NO infrastructure/interface imports | architecture-standards.md | architecture-standards.md |
| H-08 | Infrastructure NO interface imports | architecture-standards.md | architecture-standards.md |
| H-09 | Value objects MUST be immutable (frozen=True) | architecture-standards.md | architecture-standards.md |
| H-10 | Adapters NEVER instantiate own dependencies | architecture-standards.md | architecture-standards.md |
| H-11 | Bootstrap.py is SOLE composition root | architecture-standards.md | architecture-standards.md |
| H-12 | ONE class per file (MANDATORY) | file-organization.md | file-organization.md |
| H-13 | Explicit __init__.py exports REQUIRED | file-organization.md | file-organization.md |
| H-14 | Quality gate >= 0.92 threshold | quality-enforcement.md | quality-enforcement.md |
| H-15 | Self-review REQUIRED before submission | quality-enforcement.md | quality-enforcement.md |
| H-16 | Evidence-based scoring REQUIRED | quality-enforcement.md | quality-enforcement.md |
| H-17 | Context rot awareness REQUIRED | quality-enforcement.md | quality-enforcement.md |
| H-18 | L3 enforcement MUST be deterministic | quality-enforcement.md | quality-enforcement.md |
| H-19 | Fail-open error handling for all hooks | quality-enforcement.md | quality-enforcement.md |
| H-20 | P-003: No Recursive Subagents (max ONE level) | Constitution | quality-enforcement.md |
| H-21 | P-020: User Authority (user decides, never override) | Constitution | quality-enforcement.md |
| H-22 | P-022: No Deception (never deceive about actions) | Constitution | quality-enforcement.md |
| H-23 | L1 token budget MUST NOT exceed 12,476 | ADR-EPIC002-002 | quality-enforcement.md |
| H-24 | HARD rules MUST NOT exceed 25 total | EN-404 TASK-003 | quality-enforcement.md |

### Constraints

| Constraint | Value |
|------------|-------|
| Maximum HARD rules | 25 |
| Current HARD rules | 24 |
| Available slots | 1 |
| Language requirement | MUST, SHALL, NEVER, REQUIRED |
| Consequence requirement | Each HARD rule MUST have stated consequence |

---

## Preamble Content Baseline

### Exact Content Structure

```xml
<quality-gate>
  [Scoring criteria, >= 0.92 threshold, self-review mandate]
  [~480 characters, ~100 calibrated tokens]
</quality-gate>

<constitutional-principles>
  [P-003: No Recursive Subagents]
  [P-020: User Authority]
  [P-022: No Deception]
  [~338 characters, ~85 calibrated tokens]
</constitutional-principles>

<adversarial-strategies>
  [10 strategies from S-001 through S-014 subset]
  [Context rot awareness]
  [SYN #1 pairing guidance]
  [~696 characters, ~174 calibrated tokens]
</adversarial-strategies>

<decision-criticality>
  [C1: Routine, C2: Standard, C3: Significant, C4: Critical]
  [AE-001: governance -> C4]
  [AE-002: rules -> C3]
  [AE-003: architecture -> C3]
  [AE-004: constitutional -> C4]
  [~520 characters, ~130 calibrated tokens]
</decision-criticality>
```

### Degradation Priority

If token budget is tight, degrade in this order:
1. Shorten strategy descriptions
2. Condense C1-C4 descriptions
3. Remove SYN #1 pairing line
4. Minimum viable: ~170 tokens (quality-gate + constitutional only)

---

## Performance Baselines

### Per-Mechanism Performance Targets

| Mechanism | p50 Target | p95 Target | Budget |
|-----------|-----------|-----------|--------|
| PreToolUse (simple file) | < 30ms | < 87ms | 87ms |
| PreToolUse (complex file) | < 50ms | < 87ms | 87ms |
| PreToolUse (non-Python) | < 5ms | < 10ms | 87ms |
| UserPromptSubmit (standard) | < 100ms | < 500ms | 500ms |
| UserPromptSubmit (C4 max) | < 200ms | < 500ms | 500ms |
| SessionStart preamble | < 50ms | < 200ms | 200ms |
| SessionStart full hook | < 500ms | < 1,000ms | 1,000ms |

### Combined Performance Budget

| Metric | Value |
|--------|-------|
| NFC-1 total budget | 2,000ms |
| Worst case per-prompt (L2 + L3) | 587ms |
| Margin | 1,413ms (71%) |
| One-time cost (SessionStart) | ~200ms |

### PreToolUse Phase Breakdown

| Phase | Target | Description |
|-------|--------|-------------|
| P1 (Security) | < 5ms | Existing security checks |
| P2 (Patterns) | < 10ms | Existing pattern checks |
| P3 (AST) | < 50ms | NEW: import boundary + one-class validation |
| P4 (Governance) | < 10ms | NEW: governance file escalation |
| P5 (Approve) | < 2ms | Final approval |
| **Total** | **< 87ms** | |

---

## Architecture Baselines

### Layer Architecture

| Layer | Name | Status | Implementation |
|-------|------|--------|----------------|
| L1 | Static Context | Active | `.claude/rules/*.md` auto-loaded |
| L2 | Dynamic Injection | Active | UserPromptSubmit hook |
| L3 | Active Enforcement | Active | PreToolUse hook |
| L4 | Passive Monitoring | Planned | Future implementation |
| L5 | Post-Hoc Analysis | Planned | Future implementation |

### Module Architecture

| Module | Path | Purpose |
|--------|------|---------|
| PromptReinforcementEngine | `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py` | L2 engine |
| PreToolEnforcementEngine | `src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py` | L3 engine |
| SessionQualityContextGenerator | `src/infrastructure/internal/enforcement/session_quality_context.py` | Session preamble generator |
| EnforcementDecision | `src/infrastructure/internal/enforcement/enforcement_decision.py` | L3 decision dataclass |

### Hexagonal Placement

All enforcement engines reside in `src/infrastructure/internal/enforcement/` per hexagonal architecture standards. They are secondary adapters (driven by the application/hooks).

---

## Quality Baselines

### Quality Gate

| Metric | Baseline |
|--------|----------|
| Quality score threshold | >= 0.920 |
| Creator-critic iterations | Minimum 2 (target 3) |
| Self-review | REQUIRED |
| Evidence-based scoring | REQUIRED |

### Predecessor Quality Scores

| Enabler | Score | Status |
|---------|-------|--------|
| EN-402 | 0.923 | PASS |
| EN-403 | 0.930 | PASS |
| EN-404 | 0.930 | PASS |
| EN-405 | 0.936 | CONDITIONAL PASS |
| EN-406 | 0.937 (self) | TARGET MET |

### Decision Criticality Levels

| Level | Name | Description | Strategies Activated |
|-------|------|-------------|---------------------|
| C1 | Routine | Typos, formatting, minor edits | Baseline only |
| C2 | Standard | Feature development, refactoring | Core strategies |
| C3 | Significant | Rule changes, architecture modifications | Enhanced strategies |
| C4 | Critical | Governance, constitutional changes | All strategies |

### Auto-Escalate Rules

| ID | Trigger | Escalation |
|----|---------|------------|
| AE-001 | `docs/governance/` modifications | -> C4 |
| AE-002 | `.claude/rules/` modifications | -> C3 |
| AE-003 | Architecture boundary changes | -> C3 |
| AE-004 | `JERRY_CONSTITUTION.md` modifications | -> C4 |

---

## Change Control

### Baseline Update Process

1. **Identify** the configuration element to change.
2. **Document** the proposed change with rationale.
3. **Assess** impact on other baselines (e.g., token budget change affects all per-file allocations).
4. **Update** this baseline document.
5. **Update** affected deliverables (rule files, engine configurations, etc.).
6. **Verify** no regressions via test specifications.
7. **Commit** with change log entry.

### Change Categories

| Category | Approval | Examples |
|----------|----------|---------|
| HARD rule addition/removal | C4 (critical) | Adding H-25, removing H-xx |
| Token budget change | C3 (significant) | Adjusting per-file allocations |
| Preamble content change | C3 (significant) | Modifying XML sections |
| Performance target change | C3 (significant) | Adjusting <87ms threshold |
| File consolidation | C2 (standard) | Merging rule files |
| Content optimization | C2 (standard) | Reducing code examples |

### Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-02-13 | ps-validator-406 | Initial baseline established |

---

## References

| Document | Path | Relevance |
|----------|------|-----------|
| FEAT-005 | `../FEAT-005-enforcement-mechanisms.md` | Feature definition, NFCs |
| EN-403 TASK-001 | `../EN-403-hook-based-enforcement/TASK-001-hook-requirements.md` | Hook requirements |
| EN-403 TASK-002 | `../EN-403-hook-based-enforcement/TASK-002-userpromptsubmit-design.md` | L2 engine design |
| EN-403 TASK-003 | `../EN-403-hook-based-enforcement/TASK-003-pretooluse-design.md` | L3 engine design |
| EN-403 TASK-004 | `../EN-403-hook-based-enforcement/TASK-004-sessionstart-design.md` | SessionStart design |
| EN-404 TASK-002 | `../EN-404-rule-based-enforcement/TASK-002-rule-audit.md` | Current state audit |
| EN-404 TASK-003 | `../EN-404-rule-based-enforcement/TASK-003-tiered-enforcement.md` | Tiered enforcement, token budgets |
| EN-405 TASK-006 | `../EN-405-session-context-enforcement/TASK-006-preamble-content.md` | Preamble content |
| ADR-EPIC002-002 | FEAT-004 outputs | 5-Layer architecture |

---

*Generated by ps-validator-406 | 2026-02-13 | EN-406 AC-13*
