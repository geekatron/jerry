# PROJ-004-e-003: Git Worktree-Safe State Patterns

> **PS ID:** PROJ-004
> **Entry ID:** e-003
> **Topic:** Git Worktree-Safe State Patterns
> **Created:** 2026-01-12
> **Status:** COMPLETED
> **Author:** ps-researcher (Claude Opus 4.5)

---

## L0: Executive Summary (ELI5)

Git worktrees share the `.git` directory but have completely independent working trees (files). When designing `.jerry/` state, we should use **one-file-per-entity** with **immutable append-only event logs** because these naturally merge without conflicts - each worktree creates unique files that don't collide. Shared configuration should use sorted, line-based formats or be treated as "regenerable" artifacts.

---

## L1: Technical Findings (Software Engineer)

### 1. Git Worktree Architecture

#### How Worktrees Work

```
Main Repository (.git/)
├── objects/           # Shared: All commits, blobs, trees
├── refs/              # Shared: Branch references
├── config             # Shared: Repository configuration
├── worktrees/         # Per-worktree metadata
│   ├── worktree-A/
│   │   ├── HEAD       # Per-worktree: Current commit
│   │   ├── index      # Per-worktree: Staging area
│   │   ├── logs/      # Per-worktree: Reflog
│   │   └── gitdir     # Per-worktree: Path back to working tree
│   └── worktree-B/
│       └── ...

Worktree A (working directory)
├── .git              # FILE (not directory) - points to .git/worktrees/worktree-A
├── src/              # Independent: Files from worktree-A's branch
├── projects/         # Independent: Different content per branch
└── .jerry/           # Independent: Different content per branch

Worktree B (working directory)
├── .git              # FILE - points to .git/worktrees/worktree-B
├── src/              # Independent: Files from worktree-B's branch
├── projects/         # Independent: Different content per branch
└── .jerry/           # Independent: Different content per branch
```

**Key Insight**: Each worktree has its own working tree based on its checked-out branch. Files in the working directory are **completely independent** between worktrees.

#### What's Shared vs Per-Worktree

| Shared (in .git/) | Per-Worktree |
|-------------------|--------------|
| Object database | HEAD (current commit) |
| Branch refs | Index (staging area) |
| Tags | Working directory files |
| Configuration (default) | refs/bisect, refs/worktree |
| Hooks | Sparse-checkout (if used) |

**Evidence from Jerry Repo:**
```bash
# Main worktree
$ cat /path/to/jerry-agent-cleanup/.git
gitdir: /Users/.../jerry/.git/worktrees/jerry-agent-cleanup

# Worktree metadata
$ ls .git/worktrees/jerry-agent-cleanup/
HEAD  index  logs/  commondir  gitdir  COMMIT_EDITMSG
```

### 2. The Merge Conflict Problem

When a branch is merged, git performs a 3-way merge:
1. **Base**: Common ancestor
2. **Ours**: Current branch
3. **Theirs**: Branch being merged

#### Conflict Scenarios for State Files

| File Type | Conflict Risk | Example |
|-----------|--------------|---------|
| Single JSON file | HIGH | Both branches modify `state.json` at different keys |
| Single JSONL file | MEDIUM | Both branches append to same file |
| One-file-per-entity | LOW | Each branch creates unique files |
| Line-based sorted | LOW | Git can often auto-merge sorted lines |

#### Example: JSON Merge Conflict

```json
// Base (common ancestor)
{"active_project": "PROJ-001"}

// Ours (worktree A)
{"active_project": "PROJ-002", "last_session": "2026-01-12"}

// Theirs (worktree B)
{"active_project": "PROJ-003", "last_modified": "2026-01-11"}

// Result: CONFLICT!
<<<<<<< HEAD
{"active_project": "PROJ-002", "last_session": "2026-01-12"}
=======
{"active_project": "PROJ-003", "last_modified": "2026-01-11"}
>>>>>>> branch-b
```

### 3. Merge-Friendly Patterns

#### Pattern A: One-File-Per-Entity (Recommended for Events)

Instead of storing all work items in one file, use one file per work item:

```
.jerry/data/events/
├── work_item-269135492818632704.jsonl   # Worktree A creates this
├── work_item-269135492948656128.jsonl   # Worktree A creates this
├── work_item-269158234523029504.jsonl   # Worktree B creates this (different ID)
└── work_item-269158234422366208.jsonl   # Worktree B creates this
```

**Why This Works:**
- Snowflake IDs are globally unique (include timestamp + worker ID)
- Files created in different worktrees have different names
- Git sees these as **new files**, not modifications to existing files
- Merge = union of both sets of files (no conflict)

**Current Jerry Implementation**: Already uses this pattern for events!

```bash
$ ls projects/PROJ-001-plugin-cleanup/.jerry/data/events/ | head -3
work_item-269135492818632704.jsonl
work_item-269135492948656128.jsonl
work_item-269135492998987776.jsonl
```

#### Pattern B: Append-Only JSONL (Good for Logs)

```jsonl
{"event": "SessionStarted", "timestamp": "2026-01-12T10:00:00Z", "worktree": "main"}
{"event": "ProjectActivated", "timestamp": "2026-01-12T10:01:00Z", "project": "PROJ-001"}
```

**Merge Behavior:**
- Git treats JSONL as text lines
- Appends from both branches are preserved
- Only conflicts if same line modified (rare for append-only)
- Timestamps provide natural ordering

#### Pattern C: Sorted Line-Based Format

For configuration that must be shared:

```
# .jerry/config/active_projects.list (sorted)
PROJ-001-plugin-cleanup
PROJ-002-example
PROJ-003-agents-cleanup
PROJ-004-jerry-config
```

**Merge Behavior:**
- Git can auto-merge sorted, unique lines
- Each worktree adds its project to the list
- Result: union of all projects

#### Pattern D: Worktree-Local Files (Gitignored)

Some state should never be committed:

```
.jerry/
├── config.json           # Committed: shared settings
├── data/                 # Committed: event logs
└── local/                # GITIGNORED: worktree-local state
    ├── active_session.json
    ├── cache/
    └── locks/
```

**.gitignore entry:**
```
.jerry/local/
```

### 4. How Other Tools Handle This

#### JetBrains IDEs (.idea/)

```
.idea/
├── .gitignore           # Specifies what NOT to commit
├── encodings.xml        # Committed: shared settings
├── workspace.xml        # Gitignored: per-user/worktree
├── shelf/               # Gitignored: per-user stashes
└── inspectionProfiles/  # Committed: shared code style
```

**Pattern**: Separate committed (shared) from gitignored (local).

#### npm/yarn Lock Files

Lock files use regeneration strategy:
1. Accept one version (theirs or ours)
2. Run `npm install` to regenerate from `package.json`
3. Commit regenerated lock file

**Pattern**: Treat generated files as derivable from source of truth.

#### Git's Own Per-Worktree Config

Git 2.20+ supports `extensions.worktreeConfig`:

```bash
git config extensions.worktreeConfig true
# Creates .git/worktrees/<name>/config.worktree
```

**Pattern**: Explicit separation of shared vs worktree-local config.

### 5. State Classification for Jerry

| State Type | Location | Committed? | Merge Strategy |
|------------|----------|------------|----------------|
| Framework config | `.jerry/config.json` | Yes | Custom merge driver |
| Event streams | `.jerry/data/events/{id}.jsonl` | Yes | One-file-per-entity (no conflict) |
| Work item snapshots | `.jerry/data/items/{id}.json` | Yes | One-file-per-entity |
| Active project | `.jerry/local/context.json` | No | Gitignored |
| Session state | `.jerry/local/session.json` | No | Gitignored |
| File locks | `.jerry/local/locks/` | No | Gitignored |
| Cache | `.jerry/local/cache/` | No | Gitignored |

### 6. Custom Git Merge Driver (Optional Enhancement)

For files that must be single and committed (like `config.json`), a custom merge driver can help:

**.gitattributes:**
```
.jerry/config.json merge=jerry-config
```

**.gitconfig:**
```
[merge "jerry-config"]
    name = Jerry config merge driver
    driver = python scripts/merge_config.py %O %A %B %P
```

**Merge driver logic:**
1. Parse both JSON files
2. Deep merge with "last-writer-wins" for conflicts
3. Sort keys for consistent output
4. Write merged result

---

## L2: Strategic Recommendation (Principal Architect)

### Recommended Architecture for .jerry/

```
.jerry/
├── config.json              # Shared settings (consider TOML for comments)
│
├── data/                    # Committed, merge-safe event sourcing
│   ├── events/              # One JSONL file per aggregate
│   │   └── {aggregate}-{snowflake_id}.jsonl
│   └── items/               # Materialized views (derivable)
│       └── {id}.json
│
├── local/                   # GITIGNORED: worktree-local runtime state
│   ├── context.json         # Active project, session info
│   ├── session.json         # Current session state
│   ├── locks/               # File locks for concurrent access
│   │   └── {resource}.lock
│   └── cache/               # Derived/regenerable data
│       └── project_list.json
│
└── .gitignore               # Ignores local/
```

### Design Decisions

#### D-001: Use One-File-Per-Entity for Events

**Rationale**:
- Eliminates merge conflicts entirely
- Already implemented in Jerry (Snowflake ID per work item)
- Event sourcing pattern naturally supports this
- Each worktree writes to different files

**Trade-off**: More files, but modern filesystems handle this well.

#### D-002: Separate Committed vs Local State

**Rationale**:
- Worktree-local state (active project, session) changes frequently
- Committing it causes unnecessary merge conflicts
- Gitignoring `local/` solves this cleanly

**Implementation**:
```gitignore
# .jerry/.gitignore
local/
*.lock
```

#### D-003: Make Materialized Views Regenerable

**Rationale**:
- `items/{id}.json` files can be derived from event streams
- If conflicts occur, regenerate from events (source of truth)
- Similar to npm's "regenerate lock file" strategy

**Implementation**:
```python
def rebuild_item(item_id: str) -> WorkItem:
    events = event_store.read(f"work_item-{item_id}")
    return WorkItem.reconstitute(events)
```

#### D-004: Custom Merge Driver for config.json (Optional)

**Rationale**:
- Config file is a known merge conflict source
- Custom driver can deep-merge JSON intelligently
- Sorted keys ensure deterministic output

**Priority**: LOW - can be added if conflicts become frequent.

### Implementation Checklist

1. [ ] Add `.jerry/local/` directory structure
2. [ ] Add `.jerry/.gitignore` ignoring `local/`
3. [ ] Move runtime state (active project, session) to `local/`
4. [ ] Ensure Snowflake IDs for all event files (already done)
5. [ ] Add rebuild command for materialized views
6. [ ] (Optional) Implement custom merge driver for config.json

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Worktrees diverge on config | Use defaults, allow local overrides |
| Event IDs collide | Snowflake IDs include machine/process ID |
| Large number of event files | Implement event compaction/archival |
| Lock file conflicts | Gitignore all `.lock` files |

---

## References

### Git Documentation
- [git-worktree Documentation](https://git-scm.com/docs/git-worktree)
- [Ubuntu Manpage: git-worktree](https://manpages.ubuntu.com/manpages/focal/en/man1/git-worktree.1.html)

### Worktree Patterns
- [How I Use Git Worktrees](https://matklad.github.io/2024/07/25/git-worktrees.html) - matklad
- [Git Worktrees for Parallel Development](https://stevekinney.com/courses/ai-development/git-worktrees) - Steve Kinney
- [tree-me: Git Worktrees Made Easy](https://haacked.com/archive/2025/11/21/tree-me/) - Phil Haack

### Merge Strategies
- [git-json-merge](https://github.com/jonatanpedersen/git-json-merge) - JSON merge driver
- [jsonmerge_git_merge_driver](https://github.com/fcostin/jsonmerge_git_merge_driver) - Python JSON merge
- [Custom Git Merge Drivers](https://www.julianburr.de/til/custom-git-merge-drivers) - Julian Burr

### CRDTs and Conflict-Free Data
- [CRDT.tech Implementations](https://crdt.tech/implementations)
- [Automerge](https://github.com/automerge/automerge) - JSON-like CRDT
- [The CRDT Dictionary](https://www.iankduncan.com/engineering/2025-11-27-crdt-dictionary/) - Ian Duncan
- [A Conflict-Free Replicated JSON Datatype](https://martin.kleppmann.com/2017/04/24/json-crdt.html) - Martin Kleppmann

### Event Sourcing
- [Event Sourcing Pattern - Azure](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
- [Event Sourcing Pattern - AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/event-sourcing.html)
- [Git as an Event-Sourced System](https://dev.to/devcorner/git-as-an-event-sourced-system-understanding-event-sourcing-through-git-271p)
- [Merging Disconnected Event Streams](https://groups.google.com/g/dddcqrs/c/LAXHfSXdCUI) - DDD/CQRS Group

### Lock File Handling
- [Lockfile Merge Conflicts - How to Handle](https://dev.to/francecil/lockfile-merge-conflicts-how-to-handle-it-correctly-588b)
- [npm-merge-driver](https://www.npmjs.com/package/npm-merge-driver)
- [Solving Conflicts in package-lock.json](https://tkdodo.eu/blog/solving-conflicts-in-package-lock-json) - TkDodo

---

## Appendix: Verification of Current Jerry State

### Current Event File Pattern (Correct)

```bash
$ ls projects/PROJ-001-plugin-cleanup/.jerry/data/events/ | head -5
work_item-269135492818632704.jsonl
work_item-269135492948656128.jsonl
work_item-269135492998987776.jsonl
work_item-269135493036736512.jsonl
work_item-269135493275811840.jsonl
```

**Assessment**: Jerry already uses one-file-per-entity with Snowflake IDs. This is merge-safe.

### Current Worktree State

```bash
$ git worktree list
/Users/.../jerry                       95a3f00 [PROJ-004-jerry-config]
/Users/.../jerry-agent-cleanup         7f3f65f [cc/clean-up-agents]
/Users/.../jerry/nasa-subagent   b15e745 [cc/proj-nasa-subagent]
```

**Assessment**: Three worktrees active, each on different branches. The one-file-per-entity pattern prevents conflicts when these branches merge.

### Missing: Local State Separation

Currently, there's no `.jerry/local/` directory. Active project state should be moved here to prevent unnecessary commits of worktree-specific state.

---

*Document generated by ps-researcher agent as part of PROJ-004 research phase.*
