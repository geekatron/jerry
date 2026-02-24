# SPIKE-002: Automated Worktree & Session Lifecycle Management

> **Type:** spike
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-20
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Research question, hypothesis, scope |
| [Findings](#findings) | Results (populated after research) |
| [Recommendation](#recommendation) | Decision (populated after research) |
| [Related Items](#related-items) | Hierarchy |
| [History](#history) | Status changes |

---

## Content

### Research Question

**Question:** Can we automate the full worktree + session lifecycle (create worktree, provision branch, bind Claude instance, dispatch work, monitor, merge results, cleanup) as a Jerry CLI command or Python module?

### Hypothesis

We hypothesize that:
1. Git worktree operations (add, remove, list) are fully automatable via `gitpython` or subprocess
2. Branch provisioning (create, merge main, push) follows deterministic patterns already established in this project
3. Claude instance binding design varies by approach (SDK vs CLI) — Phase 1 researches worktree automation independently; Phase 2 incorporates SPIKE-001 findings via cross-pollination
4. A `jerry worktree create|dispatch|merge|cleanup` command set could encapsulate the full lifecycle
5. The main complexity is cross-worktree state coordination — ensuring ORCHESTRATION.yaml and WORKTRACKER.md stay consistent

### Timebox

| Aspect | Value |
|--------|-------|
| Timebox Duration | 8 hours |
| Start Date | TBD |
| Target End Date | TBD |

### Scope

**In Scope:**
- Git worktree automation: create with branch, merge main, push, remove
- Branch naming conventions and conflict avoidance
- Session binding: how to attach a Claude instance (SDK or CLI) to a specific worktree path
- Environment provisioning: `JERRY_PROJECT` env var, `uv sync`, hook installation
- Dispatch patterns: send a prompt/task to a worktree-bound instance
- Monitoring: check instance status, read output, detect completion or failure
- Merge coordination: merge worktree branch back to main, handle conflicts
- Cleanup: remove worktree, delete branch, archive artifacts
- Jerry CLI integration: command design, argument structure

**Out of Scope:**
- SDK vs CLI decision (that's SPIKE-001)
- Full control plane / scheduler design (future feature)
- Cross-machine distributed execution

### Research Approach

1. **Current workflow audit:** Document the exact manual steps performed today (this session is a perfect case study). Identify automation points.
2. **Git worktree API:** Research `gitpython` and subprocess-based worktree management. Prototype create/merge/cleanup.
3. **Environment provisioning:** Define what a worktree needs before a Claude instance can work in it (`JERRY_PROJECT`, `uv sync`, pre-commit hooks, `.claude/` settings).
4. **Session binding design:** Based on SPIKE-001 findings, design how an instance attaches to a worktree. SDK = working directory param. CLI = `cd worktree && claude -p "..."`.
5. **Dispatch and monitoring:** Design the interface for sending work to an instance and monitoring progress. Consider: polling vs event-driven, output capture, error detection.
6. **Merge coordination:** Research automated merge strategies. Handle: fast-forward, 3-way merge, conflict detection and escalation to operator.
7. **CLI command design:** Draft `jerry worktree` subcommands with arguments and help text.

---

## Findings

_To be populated after research._

---

## Recommendation

_To be populated after research._

---

## Execution Structure

**Parallel-with-sync-point:** SPIKE-002 executes in parallel with SPIKE-001 within an orchestrated cross-pollinated pipeline. Phase 1 (worktree research) is approach-agnostic and runs concurrently with SPIKE-001 research. Phase 2 (session lifecycle design) incorporates SPIKE-001 findings via cross-pollination.

| Phase | SPIKE-002 Work | Sync Point |
|-------|---------------|------------|
| Phase 1 (Research) | Current workflow audit, git worktree API, env provisioning | Barrier 1: Send worktree constraints to SPIKE-001; receive instance approaches from SPIKE-001 |
| Phase 2 (Analysis) | Session lifecycle design for both approaches, informed by SDK/CLI capabilities | Barrier 2: Send lifecycle feasibility to SPIKE-001; receive scored recommendation |
| Phase 3 (Decision) | Convergent: ps-architect creates go/no-go ADR from both spikes | — |

See `ORCHESTRATION_PLAN.md` for full workflow diagram.

---

## Related Items

- Parent: [FEAT-001: Multi-Instance Strategy Assessment](./FEAT-001-instance-strategy.md)
- Parallel With: [SPIKE-001: Claude SDK vs CLI Instance Comparison](./SPIKE-001-sdk-vs-cli.md) (cross-pollinated pipeline)
- Related: Current session — manual worktree management is the direct motivation

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-20 | pending | Spike defined. 7-step research approach. Depends on SPIKE-001 for instance binding design. 8h timebox. |
| 2026-02-20 | pending | Restructured: parallel-with-sync-point execution with SPIKE-001. Phase 1 is approach-agnostic. Orchestration plan created. |
