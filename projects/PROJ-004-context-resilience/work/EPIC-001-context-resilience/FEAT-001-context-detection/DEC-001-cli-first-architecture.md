# FEAT-001:DEC-001: CLI-First Hook Architecture & Context Monitoring Bounded Context

> **Type:** decision
> **Status:** pending
> **Priority:** critical
> **Created:** 2026-02-19
> **Parent:** FEAT-001
> **Owner:** --
> **Related:** DISC-001, ADR-SPIKE002-001 (to be superseded)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description of decisions |
| [Decision Context](#decision-context) | Background and constraints |
| [Decisions](#decisions) | D-001 through D-004 |
| [Decision Summary](#decision-summary) | Quick reference table |
| [Related Artifacts](#related-artifacts) | Traceability |
| [Document History](#document-history) | Change log |

---

## Summary

Four architectural decisions arising from DISC-001 findings. These decisions supersede ADR-SPIKE002-001's approach (infrastructure placement) with proper clean architecture (bounded context + CLI-first hooks).

**Decisions Captured:** 4

**Key Outcomes:**
- Hooks become thin wrappers calling CLI commands (single subprocess call per hook event)
- Context monitoring is a proper bounded context (`src/context_monitoring/`) from the start
- CLI gets `jerry hooks <event>` commands for hook-specific operations
- Enforcement tech debt tracked separately, not deepened by FEAT-001

---

## Decision Context

### Background

SPIKE-002 produced ADR-SPIKE002-001, which proposed placing context monitoring engines in `src/infrastructure/internal/enforcement/` alongside existing enforcement engines. User review and DISC-001 audit revealed that:

1. The enforcement folder is a flat dump with no domain/application layers -- it is tech debt, not a pattern to follow
2. 3 of 4 hooks bypass the CLI by directly importing infrastructure modules
3. The ADR rejected "New CLI Module" using reasoning invalidated by the work plan itself (CWI-00 fixes InMemorySessionRepository)
4. The hooks should call the CLI so that scripts are just wrappers, not standalone implementations

### Constraints

- Hooks have timeout budgets: 5000ms (UserPromptSubmit, PreToolUse, PostToolUse), 10000ms (SessionStart, PreCompact)
- Each `uv run jerry ...` subprocess call has startup overhead
- Hooks must be fail-open (errors never block user work)
- Context monitoring has distinct domain concepts validated by 2 spikes of research

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| User (project owner) | Decision authority | Clean architecture, no shortcuts |
| Claude | Implementer | Correct architectural approach |

---

## Decisions

### D-001: Hooks Call CLI, Not Import Modules

**Date:** 2026-02-19
**Participants:** User, Claude

#### Question/Context

Why do hooks directly import Python modules from `src/infrastructure/internal/enforcement/` instead of calling the CLI? We invested in building a CLI with proper CQRS, dispatchers, and a composition root. The `session_start_hook.py` already demonstrates calling `jerry --json projects context` works. Why don't all hooks follow this pattern?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A: Direct imports** (current) | Hooks import infrastructure modules and instantiate engines directly | Avoids subprocess overhead; simple to implement | Bypasses CLI, composition root, dispatchers; two execution paths; no testability via CLI; violates hexagonal architecture |
| **B: CLI-first** (proposed) | Hooks are thin wrappers that call `jerry --json hooks <event>` via subprocess | Single execution path; CLI testable; proper composition root wiring; clean architecture | One subprocess call per hook; must consolidate hook logic into single CLI command per event |

#### Decision

**We decided:** All hooks MUST call the CLI via subprocess. Hook scripts become thin wrappers (~10 lines) that pipe stdin to a CLI command and pipe stdout back. All hook logic lives in the CLI's bounded contexts, wired through the composition root.

#### Rationale

The CLI exists as the single interface layer. When hooks bypass it, they create a parallel execution path that is not testable via `jerry`, not wired through `bootstrap.py`, and not subject to the same architectural constraints. `session_start_hook.py` proves the subprocess pattern works within timeout budgets.

#### Implications

- **Positive:** Single execution path. All logic testable via `jerry --json hooks <event>`.
- **Negative:** Need to create `jerry hooks` command namespace. Each hook event gets one CLI command.
- **Follow-up required:** Design `jerry hooks` commands. Migrate existing enforcement engines to be called through CLI.

---

### D-002: Context Monitoring is a Proper Bounded Context

**Date:** 2026-02-19
**Participants:** User, Claude

#### Question/Context

Where should context monitoring code live? ADR-SPIKE002-001 proposed `src/infrastructure/internal/enforcement/`. The user identified this as a shortcut that deepens tech debt.

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A: Enforcement folder** (ADR-SPIKE002-001) | Place engines in `src/infrastructure/internal/enforcement/` | Follows existing engine pattern; quick to implement | No domain layer; no ports; flat structure; deepens tech debt; violates hexagonal architecture |
| **B: Proper bounded context** (proposed) | Create `src/context_monitoring/` with domain/application/infrastructure layers | Clean architecture; testable via ports; follows session_management and work_tracking patterns; domain concepts get proper home | More initial setup; must define ports and adapters |

#### Decision

**We decided:** Context monitoring MUST be a proper bounded context at `src/context_monitoring/` with domain, application, and infrastructure layers from the start. No "Phase 1 dump it in enforcement, Phase 2 extract later" -- the domain is well-understood after two spikes.

#### Rationale

After SPIKE-001 (7 phases) and SPIKE-002 (4 phases + QG), the domain concepts are validated: ThresholdTier, FillEstimate, ContextState, CheckpointData, CompactionEvent. These are not premature abstractions. `session_management/` and `work_tracking/` demonstrate the pattern. There is no justification for placing domain concepts in an infrastructure flat folder.

#### Implications

- **Positive:** Clean architecture from day one. Testable via ports. Consistent with rest of codebase.
- **Negative:** ADR-SPIKE002-001 must be superseded. Work items CWI-02, CWI-03, CWI-06, CWI-07 need redesign.
- **Follow-up required:** Revise ADR. Redesign work items. Define ports (ITranscriptReader, ICheckpointRepository, IThresholdConfiguration).

---

### D-003: CLI Gets `jerry hooks` Command Namespace

**Date:** 2026-02-19
**Participants:** User, Claude

#### Question/Context

If hooks call the CLI, what CLI commands do they call? We need a single CLI command per hook event that returns everything that hook needs.

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A: Per-concern commands** | Multiple commands per hook: `jerry context monitor`, `jerry context alert`, `jerry quality reinforce` | Fine-grained; reusable commands | Multiple subprocess calls per hook; exceeds timeout budget |
| **B: Per-event commands** | One command per hook event: `jerry hooks prompt-submit`, `jerry hooks session-start` | Single subprocess call; consolidates all hook logic; matches hook lifecycle | Less granular; hook-specific command surface |

#### Decision

**We decided:** The CLI gets a `jerry hooks` namespace with one command per hook event. Each command accepts the hook's stdin payload, executes all relevant logic (context monitoring, quality enforcement, etc.), and returns the complete hook response JSON.

#### Rationale

Each hook invocation has a single timeout budget. Multiple subprocess calls would consume that budget. A single `jerry hooks <event>` command consolidates all logic for that event, keeping the hook script as a trivial wrapper.

#### Implications

- **Positive:** One subprocess call per hook. Clean API surface. All hook behavior inspectable via `jerry --json hooks <event>`.
- **Negative:** The `jerry hooks` commands aggregate concerns (quality + context monitoring). This is acceptable because the hook event is the unit of work.
- **Follow-up required:** Add hook commands to CLI adapter and parser. Wire through composition root.

---

### D-004: Enforcement Tech Debt Tracked Separately

**Date:** 2026-02-19
**Participants:** User, Claude

#### Question/Context

The existing `src/infrastructure/internal/enforcement/` folder is architectural tech debt (flat structure, no domain layer, direct imports from hooks). Should FEAT-001 fix this?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A: Fix in FEAT-001** | Refactor enforcement engines into proper bounded context as part of context resilience work | Clean up tech debt; single effort | Scope creep; FEAT-001 becomes much larger; enforcement is a separate concern from context monitoring |
| **B: Track separately** | Create a separate enabler for enforcement refactoring; FEAT-001 builds context monitoring correctly but doesn't fix pre-existing debt | Focused scope; FEAT-001 delivers clean context monitoring; tech debt tracked and visible | Enforcement remains flat until addressed; two styles coexist temporarily |

#### Decision

**We decided:** Enforcement tech debt is tracked as a separate enabler under EPIC-001, not part of FEAT-001. FEAT-001 builds `context_monitoring` correctly. The `jerry hooks` commands will initially only handle context monitoring and resumption; enforcement hook logic migration happens in the separate enabler.

#### Rationale

FEAT-001's scope is context resilience, not enforcement refactoring. Adding enforcement refactoring would significantly increase scope. However, FEAT-001 MUST NOT make the debt worse -- it creates `context_monitoring` as a clean bounded context and adds `jerry hooks` commands for the new hook events only.

#### Implications

- **Positive:** FEAT-001 stays focused. Tech debt is visible and tracked.
- **Negative:** Two styles coexist temporarily (old hooks import enforcement directly, new hooks call CLI). This is acceptable as long as FEAT-001 hooks use the correct pattern.
- **Follow-up required:** Create enabler for enforcement refactoring.

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | Hooks call CLI via subprocess, not import modules directly | 2026-02-19 | Pending user acceptance |
| D-002 | Context monitoring is a proper bounded context (`src/context_monitoring/`) from the start | 2026-02-19 | Pending user acceptance |
| D-003 | CLI gets `jerry hooks` namespace with one command per hook event | 2026-02-19 | Pending user acceptance |
| D-004 | Enforcement tech debt tracked separately, not fixed in FEAT-001 | 2026-02-19 | Pending user acceptance |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-001](./FEAT-001-context-detection.md) | Parent feature |
| Discovery | [DISC-001](./DISC-001-architecture-violations.md) | Architecture violations that prompted these decisions |
| Supersedes | ADR-SPIKE002-001 | This DEC supersedes the ADR's Alternative 2 (infrastructure placement) decision |
| Related | CWI-00 (FileSystemSessionRepository) | Enables D-001 and D-002 by fixing session persistence |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-19 | Claude | Created decision document with 4 decisions arising from DISC-001 findings and user review |

---

## Metadata

```yaml
id: "FEAT-001:DEC-001"
parent_id: "FEAT-001"
work_type: DECISION
title: "CLI-First Hook Architecture & Context Monitoring Bounded Context"
status: PENDING
priority: CRITICAL
created_by: "Claude"
created_at: "2026-02-19"
updated_at: "2026-02-19"
decided_at: null
participants: ["User", "Claude"]
tags: ["architecture", "clean-architecture", "cli", "hooks", "bounded-context"]
decision_count: 4
superseded_by: null
supersedes: "ADR-SPIKE002-001"
```
