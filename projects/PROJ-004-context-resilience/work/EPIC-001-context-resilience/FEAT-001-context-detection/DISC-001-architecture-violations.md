# FEAT-001:DISC-001: Hook-CLI Architecture Violations and Enforcement Tech Debt

> **Type:** discovery
> **Status:** documented
> **Priority:** critical
> **Impact:** critical
> **Created:** 2026-02-19
> **Completed:** 2026-02-19
> **Parent:** FEAT-001
> **Owner:** --
> **Source:** SPIKE-002 user review + codebase audit

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Core findings |
| [Context](#context) | What prompted this discovery |
| [Finding](#finding) | Detailed architectural violations |
| [Evidence](#evidence) | Source file references |
| [Implications](#implications) | Impact on FEAT-001 and project |
| [Recommendations](#recommendations) | Actions required |
| [Document History](#document-history) | Change log |

---

## Summary

The Jerry Framework has two incompatible execution paths: hooks that properly call the CLI via subprocess, and hooks that bypass the CLI by directly importing infrastructure modules. The `src/infrastructure/internal/enforcement/` folder is a flat dumping ground with no domain layer, no ports, no adapters -- violating the hexagonal architecture used everywhere else. SPIKE-002's ADR-SPIKE002-001 proposed adding MORE code to this broken pattern. Context monitoring must not repeat these mistakes.

**Key Findings:**
- 3 of 4 hooks bypass the CLI by directly importing from `src/infrastructure/internal/enforcement/`
- Only `session_start_hook.py` partially uses the CLI (`jerry --json projects context`), but also directly imports `SessionQualityContextGenerator`
- The `scripts/` folder contains hook implementations that should be thin CLI wrappers
- ADR-SPIKE002-001 rejected "New CLI Module" (Alternative 3) using invalid reasoning

**Validation:** User review of ADR-SPIKE002-001 and codebase audit of hooks/, scripts/, and src/infrastructure/internal/enforcement/

---

## Context

### Background

During SPIKE-002, an ADR was produced (ADR-SPIKE002-001) proposing to place context resilience engines in `src/infrastructure/internal/enforcement/` alongside existing enforcement engines. The user reviewed the ADR and identified that:

1. The ADR rejected the clean architecture option (Alternative 3: New CLI Module) using reasoning that contradicts the work plan (CWI-00 fixes the InMemorySessionRepository limitation that was used to reject Alternative 3)
2. The enforcement folder is tech debt, not a pattern to follow
3. Hooks should call the CLI, not import internal modules directly

### Research Question

What is the actual state of hook-CLI integration, and does it support or contradict the ADR's architectural decisions?

### Investigation Approach

1. Audited `hooks.json` for all registered hooks and their entry points
2. Traced each hook script for CLI subprocess calls vs direct module imports
3. Mapped the CLI command surface vs what hooks actually use
4. Compared `src/infrastructure/internal/enforcement/` against proper bounded contexts (`src/session_management/`, `src/work_tracking/`)

---

## Finding

### F1: Two Incompatible Execution Paths

The codebase has two execution paths that should be one:

| Hook | Entry Point | CLI Used? | Import Pattern |
|------|-------------|-----------|----------------|
| SessionStart | `scripts/session_start_hook.py` | Partially | Calls `jerry --json projects context` AND imports `SessionQualityContextGenerator` directly |
| UserPromptSubmit | `hooks/user-prompt-submit.py` | No | Imports `PromptReinforcementEngine` directly |
| PreToolUse | `scripts/pre_tool_use.py` | No | Imports `PreToolEnforcementEngine` directly |
| SubagentStop | `scripts/subagent_stop.py` | No | Local functions only |

The `session_start_hook.py` proves the CLI-first pattern works (it calls `jerry --json projects context` within the 10s timeout). But the same file also bypasses the CLI for quality context generation.

### F2: Enforcement Folder is Architectural Tech Debt

Comparing the enforcement folder against proper bounded contexts:

| Aspect | `session_management/` | `work_tracking/` | `infrastructure/internal/enforcement/` |
|--------|----------------------|-------------------|---------------------------------------|
| Domain layer | Yes (aggregates, events, value objects) | Yes (aggregates, events, value objects, services) | **No** |
| Application layer | Yes (commands, queries, handlers, ports) | Yes (commands, queries, handlers, ports) | **No** |
| Infrastructure layer | Yes (adapters) | Yes (adapters, persistence) | **Everything is here** |
| Ports/Adapters | Yes | Yes | **No** |
| Testable via CLI | Yes (`jerry session ...`) | Yes (`jerry items ...`) | **No** (imported directly) |
| Composition root wiring | Yes (via `bootstrap.py`) | Yes (via `bootstrap.py`) | **No** (instantiated ad-hoc in hook scripts) |

The enforcement folder contains 7 files in a flat structure with no architectural boundaries. Every module is directly imported by hook scripts, bypassing the CLI adapter, dispatchers, and composition root.

### F3: ADR-SPIKE002-001 Rejection of Alternative 3 Uses Invalid Reasoning

The ADR rejected "New CLI Module" for two reasons:

1. **"Subprocess overhead per prompt is prohibitive within 5000ms timeout"** -- This conflates having a bounded context with calling it via subprocess. A single CLI command per hook (`jerry hooks prompt-submit`) consolidates all logic into one subprocess call. The `session_start_hook.py` already demonstrates this works.

2. **"InMemorySessionRepository limitation means the CLI module cannot offer state benefits"** -- CWI-00 in the same work plan fixes this by creating `FileSystemSessionRepository`. The ADR rejects an option based on a constraint the work plan eliminates.

### F4: scripts/ vs hooks/ Split Creates Confusion

Hook implementations are split across two directories with no clear rationale:

- `hooks/user-prompt-submit.py` -- in hooks/
- `scripts/session_start_hook.py` -- in scripts/
- `scripts/pre_tool_use.py` -- in scripts/
- `scripts/subagent_stop.py` -- in scripts/

The `scripts/` folder also contains 11 utility/validation scripts unrelated to hooks.

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Code | `session_start_hook.py` calls CLI via subprocess (line 270) | `scripts/session_start_hook.py` | 2026-02-19 |
| E-002 | Code | `session_start_hook.py` also imports `SessionQualityContextGenerator` directly (line 314) | `scripts/session_start_hook.py` | 2026-02-19 |
| E-003 | Code | `user-prompt-submit.py` imports `PromptReinforcementEngine` directly (line 53) | `hooks/user-prompt-submit.py` | 2026-02-19 |
| E-004 | Code | `pre_tool_use.py` imports `PreToolEnforcementEngine` directly (line 354) | `scripts/pre_tool_use.py` | 2026-02-19 |
| E-005 | Code | `hooks.json` registers 4 hooks with 5000ms/10000ms timeouts | `hooks/hooks.json` | 2026-02-19 |
| E-006 | Architecture | `src/infrastructure/internal/enforcement/` has 7 files, flat structure, no domain/application layers | Directory listing | 2026-02-19 |
| E-007 | Architecture | `session_management/` has proper hexagonal layers (domain/application/infrastructure) | Directory listing | 2026-02-19 |
| E-008 | Architecture | `work_tracking/` has proper hexagonal layers with event sourcing | Directory listing | 2026-02-19 |
| E-009 | ADR | ADR-SPIKE002-001 rejects Alternative 3 citing InMemorySessionRepository limitation | ADR-SPIKE002-001 lines 150-155 | 2026-02-19 |
| E-010 | Work Plan | CWI-00 creates FileSystemSessionRepository, invalidating ADR rejection reasoning | Revised work items CWI-00 | 2026-02-19 |

---

## Implications

### Impact on Project

1. **ADR-SPIKE002-001 must be revised.** The chosen alternative (infrastructure placement) perpetuates the architectural violations. Alternative 3 (proper bounded context) should be the chosen approach, updated to reflect CWI-00 eliminating the InMemorySessionRepository constraint.

2. **Revised work items (CWI-00 through CWI-09) need architectural redesign.** CWI-02, CWI-03, CWI-06, CWI-07 all reference placing engines in `enforcement/`. They must be redesigned to use a proper `context_monitoring` bounded context.

3. **Existing enforcement tech debt should be tracked.** The flat enforcement folder is pre-existing tech debt that FEAT-001 should not make worse.

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Adding more code to enforcement/ deepens tech debt | HIGH | Redesign to use proper bounded context |
| ADR-SPIKE002-001 if accepted locks in bad architecture | HIGH | Revise before acceptance |
| Enforcement tech debt remediation is out of FEAT-001 scope | MEDIUM | Track as separate enabler, don't block FEAT-001 |

### Opportunities Created

- CLI-first hook design creates a unified execution path
- Proper bounded context for context monitoring sets the right precedent
- `jerry hooks <event>` commands make hook behavior inspectable and testable via CLI

---

## Recommendations

### Immediate Actions

1. **Supersede ADR-SPIKE002-001** with a revised ADR that chooses proper bounded context architecture
2. **Revise work items** to build `src/context_monitoring/` with domain/application/infrastructure layers
3. **Design `jerry hooks` CLI commands** so hooks become thin wrappers

### Long-term Considerations

- Track enforcement folder tech debt as a separate enabler (not blocking FEAT-001)
- Establish a pattern for future hook-CLI integration: hooks always call CLI, never import directly
- Consider whether enforcement engines should eventually become their own bounded context

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-19 | Claude | Created discovery documenting hook-CLI architecture violations found during ADR review |

---

## Metadata

```yaml
id: "FEAT-001:DISC-001"
parent_id: "FEAT-001"
work_type: DISCOVERY
title: "Hook-CLI Architecture Violations and Enforcement Tech Debt"
status: DOCUMENTED
priority: CRITICAL
impact: CRITICAL
created_by: "Claude"
created_at: "2026-02-19"
updated_at: "2026-02-19"
completed_at: "2026-02-19"
tags: ["architecture", "tech-debt", "clean-architecture", "hooks"]
source: "SPIKE-002 user review + codebase audit"
finding_type: GAP
confidence_level: HIGH
validated: true
```
