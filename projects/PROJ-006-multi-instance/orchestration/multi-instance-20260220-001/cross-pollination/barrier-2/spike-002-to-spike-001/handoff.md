# Barrier 2 Handoff: SPIKE-002 → SPIKE-001

> **Direction:** spike-002 (Worktree Lifecycle) → spike-001 (SDK vs CLI)
> **Barrier:** barrier-2 (Phase 2 Cross-Pollination)
> **Date:** 2026-02-20
> **Source:** agent-b-002-analysis.md

---

## Purpose

Provide the convergent Phase 3 ADR synthesis with the session lifecycle feasibility assessment, confirming what works, what's brittle, and what needs human intervention — so the architect can validate the approach recommendation against real lifecycle constraints.

---

## Lifecycle Feasibility Summary

### State Machine: 9 States, 14 Transitions — Fully Specified

| State | Agent SDK Feasibility | CLI Feasibility | Notes |
|-------|:----:|:----:|-------|
| PROVISIONING | Full | Full | Pure git + uv operations; approach-agnostic |
| READY | Full | Full | Approach-agnostic |
| DISPATCHED | Full (`ClaudeAgentOptions.cwd + env`) | Full (subprocess `cwd` + `env`) | Both bind cleanly |
| RUNNING | Full (async generator streaming) | Full (`stream-json` or polling) | SDK has typed events; CLI requires JSON parse |
| COMPLETED | Full (typed return) | Full (`--output-format json`) | SDK returns Python objects; CLI returns JSON string |
| FAILED | Full (typed exceptions: `ProcessError`, etc.) | Partial (exit codes + stderr) | SDK has richer error classification |
| MERGING | Full | Full | Pure git operations; approach-agnostic |
| MERGED | Full | Full | Approach-agnostic |
| CLEANUP | Full | Full | Approach-agnostic |

**Conclusion:** Both Agent SDK and CLI fully support all 9 lifecycle states. The Agent SDK has advantages in RUNNING (streaming async generator), COMPLETED (typed return), and FAILED (typed exceptions).

### Dispatch Mechanism Comparison (14 Dimensions)

| Capability | Agent SDK | CLI | Winner |
|-----------|:---------:|:---:|:------:|
| Working directory binding | `cwd` option | Process `cwd` | Tie |
| Environment isolation | `env` dict | Subprocess `env` | Tie |
| Progress monitoring | Async generator (native) | `stream-json` (requires parse) | **Agent SDK** |
| Output structure | Typed Python objects | JSON string parse | **Agent SDK** |
| Session resume | `resume="<id>"` | `--resume <id>` | Tie |
| Session fork | `fork_session=True` | `--fork-session` | Tie |
| Cost capping | Not directly supported | `--max-budget-usd` | **CLI** |
| Hooks/gating | In-process (`PreToolUse`) | File-based only | **Agent SDK** |
| Custom tools | In-process MCP servers | External MCP servers | **Agent SDK** |
| Error types | Typed exceptions | Exit codes + stderr | **Agent SDK** |
| Parallelism | `anyio` task groups | `asyncio.gather` | Tie |
| Process overhead | 1 subprocess per `query()` | 1 subprocess per instance | Tie |
| Maturity | Newer (203 open issues) | Battle-tested | **CLI** |
| Budget enforcement | `max_turns` + hooks | `--max-budget-usd` | **CLI** |

**Score: Agent SDK 5, CLI 2, Tie 7.** Agent SDK wins on quality-of-life dimensions; CLI wins on cost control and maturity.

### Gap Analysis Results

- **12 gaps identified** between manual 10-step workflow and automated equivalent
- **11 of 12 fully addressable** by the designed automation
- **1 partially automated:** Merge conflict resolution (detection is automated via `git merge-tree`; semantic resolution requires human judgment)
- **Key gap:** No existing parallel instance management (G-04, Critical) — this is the core value proposition

### Risk Assessment (FMEA, Top 5 by RPN)

| Risk | RPN | Mitigation |
|------|:---:|------------|
| API rate limiting across N instances | 72 | Staggered dispatch, configurable concurrency limit |
| Orphaned worktrees after failure | 60 | `jerry worktree prune`, periodic cleanup |
| Coordinator crash mid-orchestration | 48 | ORCHESTRATION.yaml as checkpoint file |
| Cost overrun per instance | 42 | CLI `--max-budget-usd` or SDK `max_turns` + hooks |
| Missing artifacts after completion | 42 | Artifact verification before state transition |

**All RPN scores below 100** (acceptable threshold). No showstopper risks identified.

### Coordinator-Owned State Pattern Validation

The pattern is **validated and recommended**:
- Coordinator is sole writer of ORCHESTRATION.yaml
- Instances write only to their own `agent-{id}/` directories
- Cross-instance communication via coordinator-mediated handoff files only
- Session IDs recorded at dispatch time (T4), enabling resume/fork
- Atomic ORCHESTRATION.yaml writes recommended (write .tmp, rename over)

### Implementation Priority Recommendation

| Phase | Scope | Effort |
|-------|-------|--------|
| MVP | PROVISIONING → COMPLETED states, CLI subprocess dispatch | 3-5 days |
| Enhanced | Agent SDK primary dispatch, hooks, MERGING/MERGED states | 3-5 days |
| Production | Session resume/fork, cost capping, FMEA retry policies, full `jerry worktree` CLI | 5-8 days |

### Hexagonal Architecture Integration

The lifecycle maps to Jerry's hexagonal architecture:

```
domain/
    worktree.py          -> Worktree entity, WorktreeState enum
    session_binding.py   -> SessionBinding value object
    merge_check.py       -> MergeCheck value object

infrastructure/
    git_subprocess_adapter.py    -> GitPort (worktree operations)
    claude_sdk_adapter.py        -> ClaudeDispatchPort (Agent SDK)
    claude_cli_adapter.py        -> ClaudeDispatchPort (CLI fallback)

application/
    commands/  -> create_worktree, dispatch_work, merge_branch, cleanup_worktree
    queries/   -> worktree_status, worktree_list
```

---

## What Phase 3 Should Do With This

1. **Validate Agent SDK recommendation against lifecycle feasibility** — confirmed: all 9 states fully supported by Agent SDK
2. **Include the state machine in the ADR** as the session management architecture
3. **Address the cost-capping gap** — CLI fallback adapter for strict budget scenarios, or `max_turns` + hooks for SDK
4. **Adopt the implementation priority** — MVP with CLI, then upgrade to Agent SDK (this de-risks the SDK maturity concern)
5. **Use the FMEA table** in the ADR's risk assessment section
6. **Adopt the hexagonal architecture mapping** for the integration architecture

---

*Source: agent-b-002-analysis.md (SPIKE-002 Phase 2)*
*Generated: 2026-02-20*
