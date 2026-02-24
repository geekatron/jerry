# Barrier 1 Handoff: SPIKE-002 → SPIKE-001

> **Direction:** spike-002 (Worktree Lifecycle) → spike-001 (SDK vs CLI)
> **Barrier:** barrier-1 (Phase 1 Cross-Pollination)
> **Date:** 2026-02-20
> **Source:** agent-b-001-research.md

---

## Purpose

Provide SPIKE-001's Phase 2 analysis (8-dimension trade-off scoring) with worktree constraints and requirements that each instance management approach must satisfy.

---

## Key Constraints for SPIKE-001 Scoring

### Mandatory Requirements (All Approaches Must Support)

1. **Working directory isolation is MANDATORY.** Each instance MUST operate from its own worktree path. Any approach that cannot set `cwd` per instance is disqualified.

2. **Environment variable isolation is MANDATORY.** Each instance needs its own `JERRY_PROJECT` value. Shared-process approaches are ruled out.

3. **CLAUDE.md is read from worktree root.** Each worktree automatically loads the correct context — no special configuration needed for any approach.

4. **`.claude/` settings are per-worktree** (checked out from branch). User-level settings at `~/.claude/` are shared.

### Provisioning Overhead

| Step | Time (cached) | Time (cold) | Notes |
|------|--------------|-------------|-------|
| `git worktree add` | <1s | <1s | Always fast |
| `uv sync` | 3-5s | 20-30s | Main bottleneck |
| `uv run pre-commit install` | 1-2s | 1-2s | Only needed once (shared hooks dir) |
| Total per worktree | ~5s | ~35s | Before instance can start |

**Impact on scoring:** Provisioning time is identical regardless of SDK/CLI approach. It happens BEFORE instance binding. **This dimension should NOT differentiate approaches.**

### Cross-Worktree State Coordination

**The coordinator-owned state pattern is recommended.** Implications for each approach:

- Instances write artifacts to their own directories (per-agent isolation)
- Coordinator reads artifacts and updates ORCHESTRATION.yaml centrally
- Instances should NOT write to shared state files
- This pattern works identically for SDK and CLI approaches

### Merge Coordination Discovery

**`git merge-tree --write-tree` enables conflict detection without touching any working tree.** This is a critical capability for the control plane — it can check all branches for conflicts before attempting any merge. This works the same regardless of instance approach.

### Claude Code `--worktree` Flag Assessment

The built-in `--worktree` / `-w` flag creates worktrees at `.claude/worktrees/<name>/` with branch naming `worktree-<name>`. **This is insufficient for Jerry because:**
- Path convention doesn't match (`jerry-wt/feat/proj-NNN-slug`)
- Branch naming doesn't match (`feat/proj-NNN-slug`)
- No `JERRY_PROJECT` auto-setting
- No `uv sync` or hook provisioning
- No merge coordination

**Conclusion:** Jerry should implement its own worktree management. The `--worktree` flag adds no value for Jerry's use case.

### Session Binding Requirements

For Phase 2 scoring, each approach should be assessed on these session binding dimensions:

| Dimension | Requirement | Weight Suggestion |
|-----------|------------|-------------------|
| Working directory binding | Set `cwd` per instance | High (mandatory) |
| Env var binding | Set `JERRY_PROJECT` per instance | High (mandatory) |
| Session persistence | Resume/continue across process restarts | Medium |
| Session forking | Fork after initial context for parallel work | Medium |
| Output capture | Structured JSON with session ID, cost, result | Medium |
| Progress monitoring | Stream events or poll for completion | Low |
| Cost capping | Per-instance budget limit | Low |

### Reference Implementation Insights

Three open-source tools validate the worktree-based approach:
- **ccswarm** (Rust): Master orchestrator + worktree-isolated agents, PTY sessions
- **git-worktree-runner** (Bash): Provisioning hooks, config copying, cleanup automation
- **clash** (Rust): Real-time conflict detection via `git merge-tree`

All three confirm that the worktree-based isolation pattern is production-viable.

### Proposed Jerry CLI Commands

The worktree lifecycle maps to 6 commands: `create`, `provision`, `dispatch`, `status`, `merge`, `cleanup`. The dispatch and status commands are where the SDK/CLI choice matters most — the rest are pure git operations.

---

## What SPIKE-001 Phase 2 Should Do With This

1. **Programmatic Control (0.20):** Score each approach on how cleanly it sets `cwd` + `env` + `system_prompt` per instance
2. **Tool Surface (0.20):** Already assessed in Phase 1 — carry forward
3. **Session Persistence (0.15):** Score resume/fork/continue capabilities, factoring in that sessions persist per-worktree
4. **Error Handling (0.10):** Score failure detection + recovery when an instance errors in its worktree
5. **Developer Experience (0.10):** Score how easy it is to dispatch to N worktrees, capture output, parse results
6. **Cost Efficiency (0.10):** Factor in that provisioning overhead is identical; only per-instance token cost differs
7. **Jerry Integration (0.10):** Score compatibility with `jerry worktree dispatch` command design and coordinator-owned state pattern
8. **Scalability (0.05):** Score concurrent instance limits (process count, API rate limits, worktree count)

---

*Source: agent-b-001-research.md (SPIKE-002 Phase 1)*
*Generated: 2026-02-20*
