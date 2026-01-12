---
id: wi-sao-033
title: "Implement Agent Farm Pattern (Git Worktrees + TMUX)"
status: BACKLOG
parent: "_index.md"
initiative: sao-init-004
children: []
depends_on:
  - "wi-sao-012.md"
blocks: []
created: "2026-01-12"
priority: "P3"
estimated_effort: "24h"
entry_id: "sao-033"
source: "User Context - Agent Farm Architecture"
token_estimate: 800
---

# WI-SAO-033: Implement Agent Farm Pattern (Git Worktrees + TMUX)

> **Status:** BACKLOG
> **Priority:** P3 (Future Enhancement)
> **Created:** 2026-01-12
> **Source:** User context from WI-SAO-012 discussion

---

## Description

Implement the "Agent Farm" pattern for true filesystem and process isolation when running parallel agents across multiple Claude Code instances.

While Claude Code's native Task tool provides sufficient parallel execution for a single instance (validated in PS-ORCH-009), production-scale orchestration may require:
- Multiple Claude Code instances running simultaneously
- True filesystem isolation (not just directory isolation)
- Process-level isolation with independent contexts

---

## Architecture: The Agent Farm

### Copy-on-Spawn (Filesystem Isolation)

Use Git Worktrees to create isolated working copies:

```bash
# Create isolated worktree for each agent
git worktree add ../agent-001-worktree feature-branch
git worktree add ../agent-002-worktree feature-branch
```

**Benefits:**
- Shared `.git` history (easy merges)
- Isolated working trees (no file conflicts)
- Agent in `dir_A` cannot read half-written files from `dir_B`

### Process Isolation (TMUX Sessions)

Use TMUX to manage persistent Claude Code sessions:

```bash
# Create named sessions for each agent
tmux new-session -d -s agent-001 "claude --dir ../agent-001-worktree"
tmux new-session -d -s agent-002 "claude --dir ../agent-002-worktree"
```

**Benefits:**
- Each agent has dedicated terminal session
- Sessions persist across disconnections
- Can scale to 20+ parallel agents

### Coordination Layer

Prevent conflicts with a Lock File Registry:

```
/coordination/
├── agent_locks/
│   ├── agent-001.lock
│   └── agent-002.lock
├── task_queue/
│   └── pending.json
└── merge_queue/
    └── ready-to-merge.json
```

**Locking Protocol:**
1. Before starting task, agent writes lock file
2. Other agents check for locks before same task
3. After completion, agent removes lock and signals ready-to-merge

---

## Acceptance Criteria

| AC# | Criterion | Description |
|-----|-----------|-------------|
| AC-033-001 | Worktree setup | Script to create N worktrees from branch |
| AC-033-002 | TMUX orchestration | Script to spawn N Claude sessions |
| AC-033-003 | Lock file registry | Coordination mechanism for shared resources |
| AC-033-004 | Merge coordination | Queue for merging completed work |
| AC-033-005 | 10+ concurrent agents | Validated with at least 10 parallel agents |

---

## Tasks

- [ ] **T-033.1:** Design worktree naming convention
- [ ] **T-033.2:** Create worktree setup script
- [ ] **T-033.3:** Create TMUX session manager script
- [ ] **T-033.4:** Implement lock file registry
- [ ] **T-033.5:** Implement merge queue coordination
- [ ] **T-033.6:** Create orchestrator that manages full lifecycle
- [ ] **T-033.7:** Test with 10+ concurrent agents

---

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| WI-SAO-012 (Native parallel) | COMPLETE | PS-ORCH-009 validates 5 agents |
| Git worktrees | AVAILABLE | Built-in Git feature |
| TMUX | AVAILABLE | Standard Unix tool |

---

## Research Notes

### Native Task vs Agent Farm

| Aspect | Native Task | Agent Farm |
|--------|-------------|------------|
| Max agents | ~5 (recommended) | 20+ |
| Isolation | Directory + filename | Full filesystem |
| Process | Single Claude instance | Multiple instances |
| Complexity | Low | High |
| Use case | Simple workflows | Production-scale |

### When to Use Agent Farm

1. **Scale:** Need 10+ parallel agents
2. **Isolation:** Agents must not see each other's in-progress files
3. **Independence:** Each agent needs full Claude context
4. **Duration:** Long-running tasks that benefit from persistence

---

## References

- User context from WI-SAO-012 discussion (2026-01-12)
- [Git Worktrees Documentation](https://git-scm.com/docs/git-worktree)
- [TMUX Documentation](https://github.com/tmux/tmux/wiki)
- Claude Code "Team Mode" / Task Toolset (native capability)

---

*Work Item Version: 1.0*
*Created: 2026-01-12*
