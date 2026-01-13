# WI-005: Worktree-Safe State Patterns

| Field | Value |
|-------|-------|
| **ID** | WI-005 |
| **Title** | Research git worktree-safe state patterns |
| **Type** | Research |
| **Status** | COMPLETED |
| **Priority** | CRITICAL |
| **Phase** | PHASE-01 |
| **Assignee** | WT-Main |
| **Created** | 2026-01-12 |
| **Completed** | 2026-01-12 |

---

## Description

Research how to maintain independent state per git worktree that can be safely merged when branches are merged.

---

## Acceptance Criteria

- [x] AC-005.1: Document worktree file isolation behavior
- [x] AC-005.2: Identify merge conflict patterns for state files
- [x] AC-005.3: Design state structure for safe merging
- [x] AC-005.4: Recommend worktree-aware design

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-005.1 | Worktrees share `.git/` but have independent working trees; each has own HEAD, index | PROJ-004-e-003, Section 1 |
| AC-005.2 | Single JSON files = HIGH conflict risk; One-file-per-entity = LOW risk | PROJ-004-e-003, Section 2 |
| AC-005.3 | `.jerry/local/` (gitignored) for runtime state; `.jerry/data/events/` for committed | PROJ-004-e-003, L2 Section |
| AC-005.4 | Jerry already uses one-file-per-entity with Snowflake IDs - already merge-safe! | PROJ-004-e-003, Appendix |

---

## Sub-tasks

- [x] ST-005.1: Research git worktree documentation
- [x] ST-005.2: Analyze .jerry/ placement in worktrees
- [x] ST-005.3: Design mergeable state file format
- [x] ST-005.4: Create research artifact with findings

---

## Key Findings

1. **Jerry already merge-safe** - Existing one-file-per-entity with Snowflake IDs
2. **Add `.jerry/local/`** - Gitignored directory for worktree-specific runtime state
3. **Separate committed vs local** - `config.toml` (committed), `local/context.toml` (gitignored)
4. **Materialized views are regenerable** - Can rebuild from event streams if conflicts occur

---

## Recommended .jerry/ Structure

```
.jerry/
├── config.toml              # Committed: shared settings
├── data/events/{id}.jsonl   # Committed: event sourcing (merge-safe)
├── data/items/{id}.json     # Committed: materialized views
└── local/                   # GITIGNORED: worktree-local
    ├── context.toml         # Active project, session
    ├── locks/               # File locks
    └── cache/               # Regenerable data
```

---

## Progress Log

| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T10:10:00Z | Work item created, ps-researcher agent spawned | Claude |
| 2026-01-12T10:15:00Z | Research completed, artifact created | ps-researcher |
| 2026-01-12T10:16:00Z | All acceptance criteria verified, WI-005 COMPLETED | Claude |

---

## Dependencies

| Type | Work Item | Relationship |
|------|-----------|--------------|
| Depends On | WI-002 | Tracking must be set up |
| Blocks | WI-007 | Plan needs worktree strategy |

---

## Related Artifacts

- **Research Artifact**: [PROJ-004-e-003-worktree-safe-state.md](../research/PROJ-004-e-003-worktree-safe-state.md)

---

## Sources

- [git-worktree Documentation](https://git-scm.com/docs/git-worktree)
- [How I Use Git Worktrees - matklad](https://matklad.github.io/2024/07/25/git-worktrees.html)
- [CRDT.tech Implementations](https://crdt.tech/implementations)
