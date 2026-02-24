# ADR-PROJ006-001: Multi-Instance Management Approach for Jerry Framework

> **Agent:** agent-c-001 (ps-architect v2.3.0)
> **Pipeline:** convergent (Phase 3 Decision)
> **Workflow ID:** multi-instance-20260220-001
> **PS ID:** convergent | **Entry ID:** phase-3
> **Date:** 2026-02-20
> **Criticality:** C3 (auto-escalated per AE-003 -- new ADR)

## Status

**PROPOSED**

*(Per P-020: User approves final decision. This ADR requires explicit user acceptance before implementation proceeds.)*

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | ELI5 -- what we decided and why |
| [Context](#context) | Problem space and background |
| [Decision Drivers](#decision-drivers) | Weighted criteria |
| [Options Considered](#options-considered) | Four alternatives with steelman cases |
| [Decision](#decision) | Recommended approach with quantitative justification |
| [L1: Technical Implementation](#l1-technical-implementation) | Integration architecture, MVP scope, session lifecycle |
| [L2: Architectural Implications](#l2-architectural-implications) | Hexagonal mapping, long-term consequences, migration paths |
| [Consequences](#consequences) | Positive, negative, neutral |
| [Risks and Mitigations](#risks-and-mitigations) | FMEA, inversion analysis, pre-mortem |
| [Implementation Plan](#implementation-plan) | Phased rollout with effort estimates |
| [C3 Strategy Application Log](#c3-strategy-application-log) | Evidence of S-010, S-003, S-002, S-013, S-004, S-012 application |
| [Related Decisions](#related-decisions) | Dependencies and downstream ADRs |
| [Evidence Traceability](#evidence-traceability) | Source document cross-references |

---

## L0: Executive Summary

Jerry currently requires operators to manually create git worktrees, open terminals, set environment variables, and launch Claude sessions for each parallel work stream. This ADR decides how to automate that.

**We recommend adopting the Claude Agent SDK as the primary dispatch mechanism**, with the Claude Code CLI as a fallback adapter. Both sit behind a port/adapter interface (`ClaudeDispatchPort`) in Jerry's hexagonal architecture, making the choice swappable without architectural change.

The Agent SDK scored 8.70/10 in an 8-dimension weighted trade-off analysis, winning on the three highest-weighted dimensions (Programmatic Control, Tool Surface, Jerry Integration) that together carry 50% of total weight. The CLI scored 7.70 and serves as a proven fallback. The Anthropic Python SDK (4.10) is excluded as a standalone option because it fails mandatory requirements (no CLAUDE.md loading, no `.claude/` settings).

The session lifecycle is a 9-state machine (IDLE through CLEANUP) with 14 transitions, fully specified with triggers, actions, error conditions, and rollback strategies. A coordinator-owned state pattern eliminates concurrent-write hazards. Implementation proceeds in three phases: MVP with CLI dispatch (3-5 days), enhanced with Agent SDK dispatch and merge coordination (3-5 days), and production with full lifecycle features (5-8 days).

**Go decision: YES.** Proceed with implementation per the phased plan. The MVP phase uses CLI subprocess dispatch (proven, lower risk), then upgrades to Agent SDK as the primary mechanism in Phase 2.

---

## Context

### Problem

Jerry's current multi-instance workflow requires 6-9 manual steps per worktree (agent-b-001 research, Section L1.1):

1. `git worktree add` with hand-typed paths and branch names
2. `cd` to the worktree directory
3. `export JERRY_PROJECT=...` (error-prone, easy to forget)
4. `uv sync` (5-30s wait)
5. `uv run pre-commit install` (easy to forget)
6. `claude` (manual launch, no programmatic control)
7. Work, commit, push (instance responsibility)
8. `git worktree remove` (risk of losing uncommitted work)
9. Merge, push, branch delete (conflict-prone)

For N worktrees running in serial, this is N * 25-50s of manual effort plus context-switching overhead plus compounding error risk. There is no parallel execution, no progress monitoring, no automated merge coordination, and no cost tracking.

### Background

PROJ-006 (Automated Multi-Instance Orchestration) was established to investigate and resolve this problem. Two parallel research spikes were conducted:

- **SPIKE-001** (agent-a-001, agent-a-002): Compared four approaches for programmatic Claude instance management -- Anthropic Python SDK, Claude Agent SDK, Claude Code CLI, and a Hybrid. Produced an 8-dimension Kepner-Tregoe weighted trade-off analysis with sensitivity testing.

- **SPIKE-002** (agent-b-001, agent-b-002): Researched and designed the worktree and session lifecycle -- state machine, dispatch patterns, merge coordination, gap analysis (12 gaps), and FMEA (14 failure modes).

Cross-pollination between spikes occurred at two barrier points, ensuring each spike's findings were validated against the other's constraints. This ADR is the convergent synthesis of both spikes.

---

## Decision Drivers

Eight dimensions were identified and weighted based on Jerry's requirements (agent-a-002 analysis, Section L1):

| Rank | Dimension | Weight | Rationale |
|------|-----------|:------:|-----------|
| 1 | Programmatic Control | 0.20 | Core requirement: set `cwd`, `env`, `system_prompt` per instance |
| 2 | Tool Surface | 0.20 | Instances must have full Claude Code tools (Read, Write, Edit, Bash, etc.) |
| 3 | Session Persistence | 0.15 | Resume, fork, and continue sessions across phases |
| 4 | Error Handling | 0.10 | Typed error recovery for automated retry decisions |
| 5 | Developer Experience | 0.10 | Dispatch to N worktrees, capture output, parse results |
| 6 | Cost Efficiency | 0.10 | Per-instance token overhead, cost capping |
| 7 | Jerry Integration | 0.10 | Compatibility with `jerry worktree dispatch`, CLAUDE.md, skills |
| 8 | Scalability | 0.05 | Concurrent instance limits (3-8 expected) |

**Sensitivity analysis** (agent-a-002, Section L1): The ranking is robust across three weight perturbation scenarios. The Agent SDK recommendation holds unless Cost Efficiency is weighted above 0.30 AND Batch API access becomes critical, which is not a current requirement.

---

## Options Considered

### Option 1: Anthropic Python SDK (Direct API)

**What it is:** Direct REST API access to Claude models via the `anthropic` Python package. Maximum control over conversations, tool definitions, and token flow. Requires implementing the entire agent loop from scratch.

#### S-003 Steelman (strongest case for this option)

The Anthropic SDK offers the lowest per-instance token cost (no ~12-15K Claude Code system prompt overhead), exclusive access to the Batch API (50% discount for non-time-sensitive work), and full developer control over prompt caching (cache hits at 10% of base price). For a scenario with 100+ short-lived instances processing files in batch, the SDK would be the clear cost winner. Its in-process architecture (no subprocess per instance) also provides the best scalability ceiling.

#### Why rejected

The SDK **partially fails mandatory requirements**: it does not load CLAUDE.md or `.claude/` settings, which are foundational to Jerry's context system. Without these, instances would lack access to Jerry's rules, skills, governance, and project context. Reimplementing this capability on top of raw API calls is impractical and would create a parallel, divergent context system.

**Composite score: 4.10/10.** Lowest-ranked option. The Tool Surface score (2/10) and Jerry Integration score (2/10) are disqualifying for Jerry's use case.

### Option 2: Claude Agent SDK (Primary Recommendation)

**What it is:** Python wrapper (`claude-agent-sdk`) around the Claude Code CLI subprocess. Provides `ClaudeAgentOptions` with explicit `cwd`, `env`, `system_prompt`, `allowed_tools`, `max_turns`, and `hooks` fields. Full Claude Code tool surface plus in-process MCP servers.

#### S-003 Steelman (strongest case for this option)

The Agent SDK is purpose-built for Jerry's use case: programmatic multi-instance dispatch with per-instance isolation. The `ClaudeAgentOptions` API maps directly to `jerry worktree dispatch` parameters. The async generator pattern (`async for message in query(...)`) provides native streaming progress without polling. Typed exceptions (`ProcessError`, `CLIConnectionError`) enable automated retry decisions. In-process MCP servers allow Jerry-specific custom tools (artifact registration, state reporting) without external server management. The hook system (`PreToolUse`) enables coordinator-level quality gating -- blocking dangerous commands, enforcing worktree boundaries, and monitoring cost.

#### Risks acknowledged

- SDK maturity: 203 open issues on GitHub, renamed once from `claude-code-sdk` (API evolution risk)
- Subprocess overhead: each `query()` spawns a Claude Code process
- No built-in `--max-budget-usd` equivalent (CLI has this)
- Bundled CLI binary (~150MB) creates a tight coupling to Claude Code's release cycle

**Composite score: 8.70/10.** Wins on Programmatic Control (9), Tool Surface (10), Session Persistence (9), Developer Experience (9), and Jerry Integration (9).

### Option 3: Claude Code CLI (Subprocess)

**What it is:** Direct CLI invocation via `claude -p` with `--output-format json`. Session continuity via `--resume`, cost capping via `--max-budget-usd`, tool restriction via `--allowedTools`. Orchestration requires subprocess management code.

#### S-003 Steelman (strongest case for this option)

The CLI is the most battle-tested approach -- it is the primary interface used by thousands of Claude Code users daily. It provides `--max-budget-usd` for strict per-instance cost capping (not available in the Agent SDK). It requires zero additional Python dependencies. Exit codes are well-documented and stable. The `--fallback-model` flag provides automatic availability resilience under API load. For teams already comfortable with CLI automation, this approach has the lowest learning curve and the most community knowledge.

#### Why it is the fallback, not the primary

The CLI requires more orchestration code: subprocess lifecycle management, JSON parsing overhead, manual error classification from exit codes and stderr, and no in-process hook system for quality gating. The Agent SDK wraps the same CLI but adds typed Python objects, structured error handling, and programmatic hooks -- reducing boilerplate by an estimated 40-60% for the orchestration layer.

**Composite score: 7.70/10.** Strong option, viable fallback. Wins on Cost Efficiency (`--max-budget-usd`) and Maturity.

### Option 4: Hybrid (Agent SDK + Anthropic SDK)

**What it is:** Agent SDK for heavy worker dispatch, Anthropic SDK for lightweight coordination tasks (scoring, metadata queries).

#### S-003 Steelman (strongest case for this option)

The Hybrid approach provides the best of both worlds: full Claude Code capabilities for worker instances (via Agent SDK) and low-cost, high-speed coordination for lightweight tasks (via Anthropic SDK). For orchestration patterns that include many short scoring/evaluation calls alongside a few long-running worker instances, the Hybrid approach could save 30-50% on coordination token costs.

#### Why rejected (tiebreak)

The Hybrid tied with Agent SDK at 8.70/10. The tiebreak favors the simpler option: the Agent SDK alone satisfies every mandatory requirement without requiring a second SDK in the dependency graph. The adapter pattern provides the same future flexibility -- if Batch API access or lightweight coordination becomes necessary, an `AnthropicSDKDispatcher` adapter can be added without upfront architectural commitment.

**Composite score: 8.70/10 (tied).** Rejected via tiebreak on complexity.

---

## Decision

**Adopt the Claude Agent SDK as the primary dispatch mechanism for `jerry worktree dispatch`, with the Claude Code CLI as a documented fallback adapter, behind a `ClaudeDispatchPort` abstraction in Jerry's hexagonal architecture.**

### Quantitative Justification

| Dimension | Weight | Agent SDK | CLI | Delta |
|-----------|:------:|:---------:|:---:|:-----:|
| Programmatic Control | 0.20 | 1.80 | 1.60 | +0.20 |
| Tool Surface | 0.20 | 2.00 | 1.80 | +0.20 |
| Session Persistence | 0.15 | 1.35 | 1.35 | 0.00 |
| Error Handling | 0.10 | 0.80 | 0.60 | +0.20 |
| Developer Experience | 0.10 | 0.90 | 0.60 | +0.30 |
| Cost Efficiency | 0.10 | 0.60 | 0.60 | 0.00 |
| Jerry Integration | 0.10 | 0.90 | 0.80 | +0.10 |
| Scalability | 0.05 | 0.35 | 0.35 | 0.00 |
| **TOTAL** | **1.00** | **8.70** | **7.70** | **+1.00** |

The Agent SDK's 1.00-point advantage comes from dimensions that directly impact Jerry's orchestration quality: programmatic control, tool surface, error handling, developer experience, and Jerry integration.

### Key Decision Rationale

1. **Agent SDK wins on the top-3 weighted dimensions** (55% of total weight): Programmatic Control, Tool Surface, and Jerry Integration.
2. **Both approaches fully support all 9 lifecycle states** (agent-b-002 analysis, barrier-2 handoff). No lifecycle feasibility gap exists for either option.
3. **Agent SDK wins on 5 of 14 dispatch dimensions**; CLI wins on 2 (cost cap and maturity); 7 are ties (agent-b-002, Section B.3).
4. **The adapter pattern eliminates lock-in risk.** If the Agent SDK proves unstable, switching to the CLI adapter is a configuration change, not an architectural rewrite.
5. **The phased implementation plan de-risks SDK maturity.** MVP uses CLI (Phase 1), then upgrades to Agent SDK (Phase 2), validating the SDK against real workloads before committing.

---

## L1: Technical Implementation

### 1. Integration Architecture

#### Port/Adapter Pattern

Per Jerry's hexagonal architecture (H-07 through H-09), the dispatch interface is defined as a domain port with infrastructure adapters:

```
domain/
    ports/
        claude_dispatch_port.py     -> ClaudeDispatchPort (Protocol)
    entities/
        worktree.py                 -> Worktree, WorktreeState (enum)
    value_objects/
        session_binding.py          -> SessionBinding (session_id, worktree_path, project_id)
        merge_check.py              -> MergeCheck (branch, target, clean, conflicts)
        instance_result.py          -> InstanceResult (status, session_id, cost_usd, result, artifacts)
        dispatch_options.py         -> DispatchOptions (prompt, tools, timeout, max_turns, system_prompt)

infrastructure/
    adapters/
        claude_sdk_adapter.py       -> AgentSDKDispatcher implements ClaudeDispatchPort
        claude_cli_adapter.py       -> CLISubprocessDispatcher implements ClaudeDispatchPort
        git_subprocess_adapter.py   -> GitSubprocessAdapter implements GitPort
        orchestration_yaml_adapter.py -> OrchestrationStateAdapter implements StatePort

application/
    commands/
        create_worktree_command.py  -> CreateWorktreeCommand + Handler
        dispatch_work_command.py    -> DispatchWorkCommand + Handler
        merge_branch_command.py     -> MergeBranchCommand + Handler
        cleanup_worktree_command.py -> CleanupWorktreeCommand + Handler
    queries/
        worktree_status_query.py    -> WorktreeStatusQuery + Handler
        worktree_list_query.py      -> WorktreeListQuery + Handler

interface/cli/
    parser.py                       -> _add_worktree_namespace()
    main.py                         -> _handle_worktree()
    adapter.py                      -> cmd_worktree_create(), cmd_worktree_dispatch(), etc.
```

#### ClaudeDispatchPort Protocol

```python
from typing import Protocol, AsyncIterator
from domain.value_objects.dispatch_options import DispatchOptions
from domain.value_objects.instance_result import InstanceResult

class ClaudeDispatchPort(Protocol):
    """Port for dispatching work to Claude instances."""

    async def dispatch(
        self,
        worktree_path: str,
        project_id: str,
        options: DispatchOptions,
    ) -> InstanceResult:
        """Dispatch work to a Claude instance in the given worktree."""
        ...

    async def dispatch_streaming(
        self,
        worktree_path: str,
        project_id: str,
        options: DispatchOptions,
    ) -> AsyncIterator[dict]:
        """Dispatch with streaming progress events."""
        ...
```

#### Adapter Selection

| Condition | Adapter | Rationale |
|-----------|---------|-----------|
| Default (Phase 2+) | `AgentSDKDispatcher` | Primary mechanism: typed API, hooks, streaming |
| `--max-budget-usd` required | `CLISubprocessDispatcher` | Only CLI supports strict cost capping |
| Agent SDK unavailable | `CLISubprocessDispatcher` | Graceful fallback |
| Phase 1 (MVP) | `CLISubprocessDispatcher` | De-risk by starting with proven approach |

### 2. Session Lifecycle Architecture

#### State Machine

The session lifecycle follows a 9-state machine with 14 transitions (agent-b-002, Section A):

```
IDLE -> PROVISIONING -> READY -> DISPATCHED -> RUNNING -> COMPLETED -> MERGING -> MERGED -> CLEANUP -> IDLE
                  \                                  |          |                             ^
                   +-> FAILED <-----(instance_failed/timeout)---+                             |
                        |   |                                                                 |
                        |   +-----(retry_dispatch)-> READY                                    |
                        +---------(abandon)-> CLEANUP ----------------------------------------+
                        |
                        +<---(merge_conflict_escalate)--- MERGING
```

**State definitions** (abbreviated):

| State | Description | Key Invariant |
|-------|-------------|---------------|
| IDLE | No worktree exists | No worktree path on disk |
| PROVISIONING | `git worktree add` + `uv sync` + hooks | Worktree directory exists (possibly partial) |
| READY | Fully provisioned, awaiting dispatch | Valid worktree, no active process |
| DISPATCHED | Instance launched, not yet confirmed running | PID/task handle exists |
| RUNNING | Instance actively executing | Active process, monitoring loop active |
| COMPLETED | Instance finished, artifacts written | No active process, artifacts exist |
| FAILED | Error or timeout, recovery needed | Error info captured |
| MERGING | Branch merge in progress | Conflict detection active |
| MERGED | Changes integrated into target branch | Target branch updated |
| CLEANUP | Worktree being removed | Worktree directory being deleted |

**All 14 transitions** are fully specified with trigger events, actions, error conditions, and rollback strategies (see agent-b-002 Section A.3 for the complete table).

**State machine invariants verified** (agent-b-002, Section A.4): no unreachable states, no dead-end states, all error paths terminate, retry is bounded, no concurrent state per worktree, merge conflicts have a resolution path.

#### Coordinator-Owned State Pattern

The coordinator is the **sole writer** of ORCHESTRATION.yaml. This eliminates the entire class of concurrent-write hazards:

- Instances write only to their own `agent-{id}/` artifact directories
- Cross-instance communication occurs exclusively via coordinator-mediated handoff files
- Session IDs are recorded at dispatch time (T4), enabling resume/fork
- Atomic writes recommended (write to `.tmp`, rename over)

#### Dispatch Mechanism

**Primary (Phase 2+): Agent SDK `query()`**

```python
options = ClaudeAgentOptions(
    cwd=worktree_path,
    env={"JERRY_PROJECT": project_id},
    system_prompt="You are a Jerry agent working on an orchestrated task.",
    allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
    max_turns=50,
)

async for message in query(prompt=prompt, options=options):
    # Streaming progress events
    ...
```

**Fallback: CLI subprocess**

```python
cmd = [
    "claude", "-p", prompt,
    "--output-format", "json",
    "--allowedTools", tools,
    "--max-turns", "50",
]
proc = await asyncio.create_subprocess_exec(*cmd, cwd=worktree_path, env=env, ...)
```

**Parallel dispatch** uses `anyio.create_task_group()` (Agent SDK) or `asyncio.gather()` (CLI) with configurable `max_concurrent_instances` (default: 3) using a semaphore pattern.

#### Merge Coordination

1. **Pre-merge conflict detection:** `git merge-tree --write-tree <target> <branch>` (in-memory, no working tree changes)
2. **Sort by conflict count:** Merge cleanest branches first to minimize cascading conflicts
3. **Sequential merge execution:** Fast-forward preferred, 3-way merge as fallback
4. **Re-check after each merge:** Re-run `git merge-tree` for remaining branches against updated target
5. **Conflict escalation:** Source code and `.context/rules/` conflicts always escalate to operator (AE-002)

**Auto-resolvable conflicts:**

| File Pattern | Strategy | Escalation Threshold |
|-------------|----------|---------------------|
| `**/WORKTRACKER.md` | Take latest status fields | Structural conflict |
| `**/agent-*-*.md` | Accept both (non-overlapping directories) | Same file modified by two agents |

**Never auto-resolve:** Source code, `.context/rules/`, `pyproject.toml`, `CLAUDE.md`, `ORCHESTRATION.yaml` (coordinator-owned; conflict = bug).

### 3. MVP Scope Definition

**MVP (Phase 1) delivers:**

1. `jerry worktree create <project-id>` -- automated worktree creation with provisioning (T1, T2)
2. `jerry worktree dispatch <path> --prompt "..."` -- CLI subprocess dispatch with JSON output capture (T4, T5, T6, T7)
3. `jerry worktree status` -- read-only query of worktree and instance state
4. `jerry worktree list` -- list all worktrees with project, branch, status
5. `jerry worktree cleanup <path>` -- worktree removal with safety checks (T11)

**MVP defers:**

- Agent SDK dispatch (Phase 2)
- Merge coordination with conflict detection (Phase 2)
- Session resume/fork (Phase 3)
- Cost capping integration (Phase 3)
- FMEA-informed retry policies (Phase 3)

### 4. Cost Analysis

#### Per-Instance Token Overhead

| Component | Tokens (est.) | Notes |
|-----------|:------------:|-------|
| Claude Code system prompt | 12,000-15,000 | Built-in tool definitions, permissions, etc. |
| CLAUDE.md (Jerry root) | ~2,500 | Jerry's root CLAUDE.md |
| `.claude/rules/` auto-loaded files | ~5,000 | Mandatory rules, quality enforcement, etc. |
| Total system overhead per instance | ~19,500-22,500 | Amortizes over session duration |

**Cost per instance (estimated):**

| Scenario | Model | Input Tokens | Output Tokens | Est. Cost |
|----------|-------|:------------:|:-------------:|:---------:|
| Short task (5 turns) | Sonnet 4.6 | ~50K | ~10K | $0.30 |
| Medium task (20 turns) | Sonnet 4.6 | ~150K | ~40K | $1.05 |
| Long task (50 turns) | Sonnet 4.6 | ~400K | ~100K | $2.70 |

**Orchestration overhead (N=4 instances, medium tasks):** ~$4.20 total, of which ~$0.26 is system prompt overhead (6.2%). The system prompt cost is dominated by the first prompt and amortizes via prompt caching (cache hits at $0.30/MTok vs $3.00/MTok).

#### Cost Control Mechanisms

| Mechanism | Adapter | Description |
|-----------|---------|-------------|
| `--max-budget-usd` | CLI only | Hard per-instance cost cap; instance exits cleanly when reached |
| `max_turns` | Both | Limits conversation turns; proxy for cost |
| `PreToolUse` hook | Agent SDK only | Monitor cumulative token usage, deny tool calls after threshold |
| `anyio.fail_after(timeout)` | Both | Wall-clock limit prevents runaway sessions |
| Coordinator-level budget | Both | Sum `cost_usd` across instances; abort new dispatches when budget exhausted |

---

## L2: Architectural Implications

### 1. Dependency Architecture

Jerry gains a direct dependency on `claude-agent-sdk`, which internally bundles the Claude Code CLI binary. This means:

- **Package size increase:** ~150MB for the bundled Node.js binary. Acceptable for a developer tool.
- **Release coupling:** Jerry's dispatch capability is coupled to Claude Code's release cycle. Mitigated by version pinning.
- **Fallback independence:** The CLI adapter has zero additional dependencies (uses system-installed `claude`), providing an independent fallback path.

### 2. Hexagonal Architecture Compliance

| Constraint | Status | Evidence |
|-----------|--------|----------|
| H-07: Domain layer -- no external imports | COMPLIANT | `ClaudeDispatchPort` is a Protocol; no SDK imports in domain |
| H-08: Application layer -- no infra imports | COMPLIANT | Command handlers depend on ports, not adapters |
| H-09: Composition root exclusivity | COMPLIANT | Adapter selection wired in `bootstrap.py` |
| H-10: One class per file | COMPLIANT | Each entity, value object, adapter in separate file |

### 3. Migration Paths

The adapter pattern ensures migration is a configuration/adapter swap, not an architectural rewrite:

| Trigger | Migration | Effort | Port Change? |
|---------|-----------|--------|:------------:|
| Agent SDK stability issues | Switch to `CLISubprocessDispatcher` | LOW | No |
| Batch API requirement | Add `AnthropicSDKDispatcher` for batch-eligible tasks | MEDIUM | No |
| Agent SDK deprecation | Switch to CLI adapter | LOW | No |
| Cost optimization needed | Use CLI adapter with `--max-budget-usd` | LOW | No |
| TypeScript orchestrator | Implement port with `claude-code-js` | HIGH | Interface only |

### 4. Extensibility

| Extension | Design Support | Changes Needed |
|-----------|---------------|----------------|
| Multiple concurrent workflows | Each workflow has own `workflow_id` and ORCHESTRATION.yaml | Workflow registry in coordinator |
| Cross-project orchestration | Each instance already has own `JERRY_PROJECT` | Different `JERRY_PROJECT` per instance |
| Hierarchical orchestration | State machine is per-instance; coordinator is flat | Sub-coordinator concept (respecting H-01) |
| Remote worktrees | Current design uses local filesystem paths | Replace subprocess `cwd` with container/SSH isolation |
| Persistent coordinator | ORCHESTRATION.yaml is the checkpoint | Read state on restart, reconcile with process state |

### 5. Long-Term Maintainability

**Positive factors:**
- Anthropic actively maintains the SDK (MIT license, ~4.9k GitHub stars, recent releases)
- Python-native with async/await aligns with Jerry's Python stack
- In-process MCP servers reduce external dependency count
- Typed exception hierarchy enables clean error handling patterns
- `ClaudeAgentOptions` is a clean, declarative configuration surface

**Concern factors:**
- Bundled CLI binary creates tight coupling to Claude Code's release cycle
- 203 open issues suggest active development but also instability surface
- No documented SLA or stability guarantees for the SDK
- Session storage location (`~/.claude/`) is shared across all Claude Code usage

**Recommendation:** Adopt with adapter layer. Review SDK stability quarterly. Maintain CLI adapter as tested fallback.

---

## Consequences

### Positive

1. **Single-command multi-instance dispatch.** `jerry worktree dispatch` replaces 6-9 manual steps per worktree, reducing setup time from 25-50s to <1s per instance.
2. **Parallel execution.** N instances run concurrently via async dispatch, replacing serial operator context-switching.
3. **Structured output and cost tracking.** Every instance returns session ID, cost, duration, and result in structured format.
4. **Hook-based quality gating.** Agent SDK `PreToolUse` hooks enable coordinator-level enforcement of Jerry rules (H-05 UV-only, worktree boundary enforcement, dangerous command blocking).
5. **Automated merge coordination.** `git merge-tree` provides conflict detection before merge attempt; dependency-aware ordering minimizes cascading conflicts.
6. **Adapter-based flexibility.** Changing the dispatch mechanism is a configuration change, not a rewrite.
7. **Session continuity.** Resume, fork, and continue sessions across phases and coordinator restarts.

### Negative

1. **New dependency on `claude-agent-sdk`.** Adds ~150MB bundled binary and couples to Claude Code's release cycle. Mitigated by adapter layer and version pinning.
2. **Per-instance token overhead.** ~19,500-22,500 tokens of system prompt per instance. Mitigated by prompt caching (90% cost reduction on cache hits) and amortization over long sessions.
3. **SDK maturity risk.** 203 open issues, one rename already. Mitigated by CLI fallback adapter, version pinning, and quarterly stability review.
4. **No built-in cost cap in Agent SDK.** `--max-budget-usd` is CLI-only. Mitigated by `max_turns`, `PreToolUse` hooks, and external timeout.
5. **Merge conflict resolution remains partially manual.** Source code conflicts require human judgment. Mitigated by conflict detection before merge and directory isolation to minimize conflicts.

### Neutral

1. **Provisioning time unchanged.** Both Agent SDK and CLI approaches have the same worktree provisioning overhead (5-35s per worktree). This is inherent to `git worktree add` + `uv sync`, not to the dispatch mechanism.
2. **API pricing unchanged.** All approaches use the same underlying Anthropic API and token pricing. The cost difference is only in system prompt overhead, which is small relative to task cost.
3. **Git worktree concurrency model unchanged.** Git's built-in concurrency safety (branch exclusivity, lock-based ref updates) applies regardless of dispatch mechanism.

---

## Risks and Mitigations

### Synthesized FMEA Table (S-012)

This table synthesizes failure modes from the lifecycle FMEA (agent-b-002, Section L2.4) with architecture-level failure modes identified during convergent analysis:

| ID | Failure Mode | State/Transition | Sev | Prob | Det | RPN | Mitigation |
|----|-------------|-----------------|:---:|:----:|:---:|:---:|------------|
| FM-13 | API rate limiting across N instances | RUNNING | 6 | 4 | 3 | **72** | Stagger dispatch times. Configurable `max_concurrent_instances` (default: 3). Exponential backoff. |
| FM-11 | Orphaned worktrees after failure | T13 (abandon) | 3 | 5 | 4 | **60** | `jerry worktree list` shows all. `jerry worktree cleanup --force`. Periodic `git worktree prune`. |
| FM-09 | Coordinator crashes mid-orchestration | Any | 8 | 2 | 3 | **48** | ORCHESTRATION.yaml as checkpoint. Atomic writes (`.tmp` + rename). Reconcile with `ps` + `git worktree list` on restart. |
| FM-05 | Instance exceeds cost budget | RUNNING | 7 | 3 | 2 | **42** | CLI: `--max-budget-usd`. SDK: `max_turns` + hooks + external timeout. Coordinator-level budget tracking. |
| FM-06 | Artifacts missing after completion | T6 | 7 | 2 | 3 | **42** | Verify artifact existence before COMPLETED transition. Retry if missing. |
| FM-10 | Two instances modify same file | T9 (merge) | 7 | 3 | 2 | **42** | Directory isolation (`agent-{id}/`). `git merge-tree` detection before merge. `PreToolUse` hook to enforce write boundaries. |
| FM-14 | Disk space exhaustion from N worktrees | T1 | 5 | 2 | 4 | **40** | Pre-check disk space (~200MB/worktree). Venv symlink option. Alert at 80% disk. |
| FM-03 | Instance crashes on startup | T5 | 6 | 3 | 2 | **36** | Capture stderr. Retry with fresh session. Check CLAUDE.md and JERRY_PROJECT validity. |
| FM-02 | `uv sync` fails (network/lockfile) | T2 | 5 | 3 | 2 | **30** | Retry once. Venv symlink fallback. 60s timeout. |
| FM-12 | Session ID lost (cannot resume) | T12 | 5 | 2 | 3 | **30** | Record session ID in ORCHESTRATION.yaml at dispatch time (T4), not completion. CLI `--session-id` for deterministic IDs. |
| FM-07 | Merge conflicts in source code | T14 | 6 | 4 | 1 | **24** | `git merge-tree` pre-detection. Escalate to operator. Preserve both branches. |
| FM-04 | Instance exceeds time limit | T8 | 5 | 4 | 1 | **20** | SIGTERM -> 10s -> SIGKILL. Configurable timeout per dispatch. Capture partial output. |
| FM-08 | Merge conflicts in .context/rules/ | T14 | 8 | 2 | 1 | **16** | AE-002: auto-C3 escalation. Never auto-resolve. Operator review mandatory. |
| FM-01 | Worktree creation fails (branch exists) | T1 | 3 | 4 | 1 | **12** | Check branch existence before `worktree add`. Clear error with suggested fix. |
| FM-15 | Agent SDK breaking API change | Dispatch | 7 | 3 | 2 | **42** | Adapter layer isolates impact. Pin version. CLI fallback. Quarterly review. |
| FM-16 | Agent SDK deprecated by Anthropic | Architecture | 9 | 1 | 4 | **36** | Adapter swap to CLI. No architectural change. Monitor Anthropic announcements. |
| FM-17 | MCP server connection issues (GH-3) | RUNNING | 5 | 2 | 3 | **30** | Use in-process MCP servers (not affected by this bug). Monitor issue resolution. |

**All RPN scores below 100** (acceptable threshold). Top risk (FM-13, RPN 72) is mitigated by configurable concurrency limits and dispatch staggering.

### S-013 Inversion Analysis

**"What if we deliberately chose CLI instead of Agent SDK?"**

| Hidden Trade-off Surfaced | Assessment |
|--------------------------|------------|
| CLI requires ~40-60% more orchestration boilerplate | Jerry would need subprocess management, JSON parsing, exit code interpretation, and manual error classification code that the Agent SDK provides out-of-the-box |
| CLI has `--max-budget-usd` | Genuine advantage. For strict cost capping, CLI is superior. The adapter pattern preserves this advantage: use CLI adapter when cost capping is needed |
| CLI has higher maturity/stability | Genuine advantage. De-risked by the phased plan: MVP uses CLI, then upgrades to Agent SDK after validation |
| CLI is language-agnostic | Irrelevant for Jerry (Python-only stack) |
| CLI avoids ~150MB bundled binary | Minor advantage. Jerry is a developer tool; 150MB is acceptable |
| No hook system in CLI | Significant disadvantage. Jerry needs `PreToolUse` hooks for worktree boundary enforcement and quality gating. CLI has file-based lifecycle hooks only, which are less granular |

**Inversion conclusion:** The CLI is a strong fallback but not the optimal primary mechanism. The Agent SDK's typed API, streaming, and hooks provide meaningful orchestration value that would need to be reimplemented with CLI. The phased plan captures the best of both: CLI stability for MVP, SDK capabilities for production.

### S-002 Devil's Advocate Challenges

**Challenge 1: "What if the Agent SDK is deprecated next year?"**

Response: The adapter pattern makes this a LOW-impact event. Switch the adapter configuration from `AgentSDKDispatcher` to `CLISubprocessDispatcher`. The domain model, application layer, and CLI interface are unaffected. The CLI subprocess approach is fundamental to how Claude Code works and is unlikely to be deprecated alongside the SDK.

**Challenge 2: "What if CLI subprocess is actually simpler long-term?"**

Response: For a single-instance dispatch, CLI is simpler (fewer dependencies, no SDK to learn). But for N-instance orchestration with progress monitoring, error recovery, and quality gating, the Agent SDK's structured API reduces total code complexity. The breakeven point is approximately 3+ concurrent instances with retry logic -- exactly Jerry's use case. If Jerry's needs shrink to single-instance dispatch, the CLI adapter can become the default with zero code change.

**Challenge 3: "What if the 203 open issues indicate fundamental instability?"**

Response: The issue count alone is not diagnostic -- high-traffic open-source projects routinely have 100+ open issues. The critical question is the severity distribution, which was not fully analyzed (identified as a gap in agent-a-002's inversion analysis). Mitigation: pin the SDK version, test each upgrade in CI, maintain the CLI fallback, and establish a quarterly stability review. The phased plan (MVP on CLI) means Jerry does not depend on SDK stability for initial delivery.

**Challenge 4: "What if the per-instance token overhead makes multi-instance uneconomical?"**

Response: The ~19,500-22,500 token system overhead costs approximately $0.06 per instance at Sonnet 4.6 pricing ($3/MTok). For 4 concurrent instances, that is $0.24 of overhead. Prompt caching reduces this by 90% on subsequent turns (cache hits at $0.30/MTok). For tasks that would otherwise require 25-50s of manual operator time per worktree, the automation ROI is strongly positive even with the token overhead.

### S-004 Pre-Mortem Analysis

**"It is August 2026 (6 months later). The multi-instance system is deployed but failing. What went wrong?"**

| Failure Scenario | Root Cause | Prevention (Design Decision) |
|-----------------|------------|------------------------------|
| "Instances keep timing out before completing work." | Default timeout too aggressive for complex tasks. | Configurable timeout per dispatch (default 3600s). Track actual durations to calibrate. |
| "We are burning through API budget with no visibility." | No per-instance cost tracking. Instances run uncapped. | Record `cost_usd` in ORCHESTRATION.yaml per instance. CLI dispatch uses `--max-budget-usd`. Coordinator-level budget enforcement. |
| "Merge conflicts block every orchestration run." | Instances modify shared files (CLAUDE.md, pyproject.toml). | Enforce directory isolation: instances write only to `agent-{id}/` directories. `PreToolUse` hook blocks writes outside worktree artifact directory. |
| "The coordinator lost track of running instances after a crash." | ORCHESTRATION.yaml not updated atomically. | Atomic writes (`.tmp` + rename). On recovery, reconcile with `ps` and `git worktree list`. |
| "Session resume does not work across coordinator restarts." | Session IDs stored in memory, not ORCHESTRATION.yaml. | Session IDs MUST be written to ORCHESTRATION.yaml at dispatch time (T4). |
| "Too many concurrent instances overwhelm the API." | No concurrency limiter. | Configurable `max_concurrent_instances` (default: 3). Semaphore pattern in async dispatch. |
| "Orphaned worktrees accumulate, filling disk." | Cleanup only triggered on happy path. | Periodic `jerry worktree prune` reconciles `git worktree list` with ORCHESTRATION.yaml. |
| "Agent SDK broke after a version upgrade." | Breaking API change in new release. | Pin version. Test upgrades in CI. CLI fallback always available. Quarterly review. |

---

## Implementation Plan

### Phase 1: MVP (CLI Dispatch) -- 3-5 days

| Task | Description | Priority |
|------|-------------|----------|
| Domain entities | `Worktree`, `WorktreeState` enum, `SessionBinding`, `InstanceResult`, `DispatchOptions` | P0 |
| Port definitions | `ClaudeDispatchPort`, `GitPort`, `OrchestrationStatePort` | P0 |
| CLI adapter | `CLISubprocessDispatcher` implementing `ClaudeDispatchPort` | P0 |
| Git adapter | `GitSubprocessAdapter` implementing `GitPort` (worktree add/remove/list/prune) | P0 |
| Create command | `CreateWorktreeCommand` + handler (T1, T2: create + provision) | P0 |
| Dispatch command | `DispatchWorkCommand` + handler (T4, T5, T6, T7: dispatch + monitor) | P0 |
| Status/list queries | `WorktreeStatusQuery`, `WorktreeListQuery` + handlers | P0 |
| Cleanup command | `CleanupWorktreeCommand` + handler (T11: remove + prune) | P0 |
| CLI namespace | `_add_worktree_namespace()` in parser.py | P0 |
| ORCHESTRATION.yaml adapter | Read/write orchestration state | P1 |
| BDD tests | Test-first per H-20 for all commands and queries | P0 |

**Deliverable:** `jerry worktree create`, `dispatch`, `status`, `list`, `cleanup` working with CLI subprocess dispatch.

### Phase 2: Enhanced (Agent SDK + Merge) -- 3-5 days

| Task | Description | Priority |
|------|-------------|----------|
| Agent SDK adapter | `AgentSDKDispatcher` implementing `ClaudeDispatchPort` | P0 |
| Hook system | `PreToolUse` hook for worktree boundary enforcement and dangerous command blocking | P0 |
| Merge command | `MergeBranchCommand` + handler (T9, T10, T14: detect + merge + escalate) | P0 |
| Conflict detection | `git merge-tree --write-tree` integration | P0 |
| Merge ordering | Dependency-aware merge ordering (cleanest first, re-check after each) | P1 |
| Adapter selection | Bootstrap logic to select Agent SDK or CLI adapter based on context | P1 |
| Parallel dispatch | `dispatch_parallel()` with `anyio.create_task_group()` and concurrency limiter | P0 |
| Streaming progress | Real-time progress from Agent SDK async generator | P1 |
| BDD tests | Tests for Agent SDK dispatch, merge coordination, conflict detection | P0 |

**Deliverable:** Agent SDK as primary dispatch, `jerry worktree merge` with conflict detection, parallel multi-instance dispatch.

### Phase 3: Production (Full Lifecycle) -- 5-8 days

| Task | Description | Priority |
|------|-------------|----------|
| Session resume/fork | Resume failed sessions (T12), fork for parallel analysis | P1 |
| Cost capping | CLI adapter with `--max-budget-usd`, SDK adapter with `max_turns` + hooks + timeout | P1 |
| FMEA retry policies | Bounded retry with configurable `max_retries`, exponential backoff, error classification | P1 |
| In-process MCP servers | Jerry-specific custom tools (artifact registration, state reporting) | P2 |
| Coordinator recovery | Reconcile ORCHESTRATION.yaml with actual process/worktree state on restart | P1 |
| Orphan cleanup | `jerry worktree prune` command reconciling `git worktree list` with ORCHESTRATION.yaml | P1 |
| Dashboard/reporting | Aggregate cost, duration, success rate across orchestration runs | P2 |
| Full `jerry worktree` CLI | All 6 commands polished with `--help`, `--json`, error messages | P1 |
| Integration tests | End-to-end orchestration test with 2-3 real instances | P0 |

**Deliverable:** Production-ready multi-instance orchestration with full lifecycle management.

### Total Estimated Effort: 11-18 days

---

## C3 Strategy Application Log

This section documents the application of all six C3-required strategies, providing evidence of compliance with the quality framework.

### S-010 (Self-Refine) -- Applied

Self-review verification before finalization:

| Check | Result | Evidence |
|-------|--------|----------|
| All four alternatives evaluated with quantitative scores | PASS | Options Considered section: 4 approaches, 8 dimensions, 32 score cells |
| Sensitivity analysis cited for robustness | PASS | Decision Drivers section: 3 perturbation scenarios |
| All consequences documented (positive, negative, neutral) | PASS | Consequences section: 7 positive, 5 negative, 3 neutral |
| Evidence traceability for all claims | PASS | Evidence Traceability section: all 6 input documents cited |
| Implementation plan with effort estimates | PASS | Implementation Plan section: 3 phases, 11-18 days |
| Mandatory requirements gate applied | PASS | Option 1 (Anthropic SDK) failure documented |
| MVP scope clearly bounded | PASS | L1 Section 3: what is included and what is deferred |
| FMEA table synthesized from both spikes | PASS | 17 failure modes, top RPN = 72 |

### S-003 (Steelman) -- Applied

Each rejected option received a steelman argument (strongest case) before critique. See Options Considered section:
- Option 1 steelman: lowest token cost, Batch API access, best scalability ceiling
- Option 3 steelman: battle-tested, `--max-budget-usd`, zero additional dependencies
- Option 4 steelman: best of both worlds for mixed workloads

### S-002 (Devil's Advocate) -- Applied

Four challenges posed and addressed (see Risks and Mitigations, S-002 subsection):
1. SDK deprecation risk
2. CLI simplicity argument
3. 203 open issues severity concern
4. Per-instance token overhead economics

### S-013 (Inversion) -- Applied

"What if we deliberately chose CLI?" analysis surfaced six hidden trade-offs (see Risks and Mitigations, S-013 subsection). Conclusion: CLI is a strong fallback but not the optimal primary mechanism due to missing hook system and higher orchestration boilerplate.

### S-004 (Pre-Mortem) -- Applied

Eight failure scenarios analyzed for a hypothetical August 2026 deployment failure (see Risks and Mitigations, S-004 subsection). Prevention strategies incorporated into design decisions (configurable timeouts, atomic writes, concurrency limits, version pinning).

### S-012 (FMEA) -- Applied

17 failure modes analyzed with Severity, Probability, and Detection ratings (see Risks and Mitigations, FMEA table). Synthesized from agent-b-002's 14 lifecycle failure modes plus 3 architecture-level failure modes (FM-15 through FM-17). All RPN scores below 100.

---

## Related Decisions

| Decision | Status | Relationship |
|----------|--------|-------------|
| ADR-PROJ006-001 (this) | PROPOSED | Primary -- multi-instance management approach |
| Worktree path convention | DECIDED (in agent-b-001) | Use `jerry-wt/feat/proj-{NNN}-{slug}` pattern |
| Git subprocess vs GitPython | DECIDED (in agent-b-001) | Use subprocess (zero dependencies, better worktree support) |
| Coordinator-owned state vs file locking | DECIDED (in agent-b-002) | Coordinator-owned state (no concurrent-write hazards) |
| Phase 2: Agent SDK version pinning policy | PENDING | Must be decided before Phase 2 implementation |
| Phase 3: Cost capping strategy details | PENDING | Must be decided before Phase 3 implementation |

---

## Evidence Traceability

| Document | Agent | Content | Used In |
|----------|-------|---------|---------|
| agent-a-001-research.md | agent-a-001 | SDK vs CLI capabilities research (3 approaches, tool surface, sessions, cost) | Context, Options Considered, L1 dispatch patterns |
| agent-a-002-analysis.md | agent-a-002 | 8-dimension weighted trade-off scoring, sensitivity analysis, inversion analysis | Decision Drivers, Decision, quantitative justification |
| agent-b-001-research.md | agent-b-001 | Worktree lifecycle research (10-step manual workflow, git API, provisioning, merge) | Context, gap analysis, worktree conventions |
| agent-b-002-analysis.md | agent-b-002 | Session lifecycle state machine (9 states, 14 transitions), dispatch patterns, merge coordination, gap analysis (12 gaps), FMEA (14 failure modes) | L1 lifecycle architecture, merge coordination, FMEA table |
| barrier-2/spike-001-to-spike-002/handoff.md | cross-pollination | Scored recommendation summary, sensitivity analysis, adapter pattern recommendation | Decision, adapter architecture |
| barrier-2/spike-002-to-spike-001/handoff.md | cross-pollination | Lifecycle feasibility confirmation, 14-dimension dispatch comparison, gap analysis summary, top-5 FMEA risks, hexagonal architecture mapping | Decision validation, L1 integration architecture, risk assessment |

---

*Agent: agent-c-001 (ps-architect v2.3.0)*
*Pipeline: convergent (Phase 3 Decision)*
*Workflow: multi-instance-20260220-001*
*Criticality: C3 (AE-003)*
*Date: 2026-02-20*
*Strategies applied: S-010, S-003, S-002, S-013, S-004, S-012*
