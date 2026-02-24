# SPIKE-002 Phase 1 Research: Automated Worktree and Session Lifecycle Management

> **Agent:** agent-b-001 (ps-researcher v2.3.0)
> **Pipeline:** spike-002 (Worktree & Session Lifecycle)
> **Phase:** 1 (Research)
> **Workflow ID:** multi-instance-20260220-001
> **PS ID:** phase-1 | **Entry ID:** e-002
> **Date:** 2026-02-20
> **Status:** COMPLETE

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Key findings and automation opportunities |
| [L1: Technical Findings](#l1-technical-findings) | Git API, provisioning, session binding, dispatch, merge, CLI design |
| [L2: Architectural Implications](#l2-architectural-implications) | Coordination challenges, integration with Jerry CLI |
| [References](#references) | All sources with URLs |

---

## L0: Executive Summary

### Overview

The current Jerry multi-instance workflow involves six to nine manual steps per worktree, each requiring operator attention and context-switching. This research establishes that every step in this workflow is automatable, with the primary complexity residing in merge coordination and cross-worktree state consistency rather than in the worktree lifecycle itself.

### Key Findings

1. **Claude Code already supports worktrees natively.** The `claude -w <name>` (or `--worktree`) flag creates an isolated worktree under `.claude/worktrees/<name>`, branching from the default remote branch, and handles cleanup on session exit. This is a critical discovery -- it means the worktree creation, session binding, and cleanup lifecycle already has a first-party solution for simple cases.

2. **Git worktree operations are fully automatable via subprocess.** GitPython has worktree support since v3.0.0 (`Repo.git.worktree("add", ...)`) but its API is a thin wrapper around subprocess calls. Direct `subprocess.run(["git", "worktree", ...])` is the more predictable approach with zero additional dependencies.

3. **The existing manual workflow has six distinct provisioning steps:** worktree creation, branch setup, environment variable configuration (`JERRY_PROJECT`), dependency sync (`uv sync`), pre-commit hook installation, and Claude session launch. Automation can reduce this to a single command.

4. **Merge conflict detection is solvable without touching the working tree.** The `git merge-tree --write-tree` command performs three-way merges in memory, returning exit code 0 for clean merges and 1 for conflicts. The `clash` tool from clash-sh builds on this for real-time cross-worktree conflict monitoring.

5. **The existing Jerry codebase is worktree-aware.** The `session_start_hook.py` already handles worktree detection (checking if `.git` is a file rather than a directory), and `CLAUDE_PROJECT_DIR` provides the right path regardless of worktree location.

6. **Three open-source tools provide reference implementations:** `ccswarm` (Rust, multi-agent orchestration with worktree isolation), `git-worktree-runner` (Bash, automated provisioning with hooks), and `clash` (Rust, conflict detection via `git merge-tree`). These validate the approach and provide design patterns.

### Automation Opportunity Assessment

| Manual Step | Automation Difficulty | Notes |
|-------------|----------------------|-------|
| `git worktree add` | Low | Single subprocess call |
| Branch creation/checkout | Low | Part of worktree add |
| `export JERRY_PROJECT=...` | Low | Set in subprocess environment |
| `uv sync` | Low | Single subprocess call; ~5s cached |
| `uv run pre-commit install` | Low | Single subprocess call; ~2s |
| Launch Claude session | Medium | Depends on SDK vs CLI approach (SPIKE-001) |
| Work/commit/push | N/A | Instance responsibility |
| `git worktree remove` | Low | Single subprocess call |
| Merge back to main | Medium-High | Conflict detection and resolution |

### Barrier 1 Handoff Summary (b-->a)

Key constraints and requirements that SPIKE-001 must account for:

1. **Working directory isolation is mandatory.** Each instance MUST operate from its own worktree path. The SDK/CLI approach must support setting the working directory.
2. **Environment variable isolation is mandatory.** Each instance needs its own `JERRY_PROJECT` value. This rules out shared-process approaches.
3. **Provisioning takes ~10-15 seconds per worktree** (cold) or ~3-5 seconds (warm with cached deps).
4. **Claude Code's `--worktree` flag provides a first-party solution** for simple cases but may not support custom branch naming, `JERRY_PROJECT` setting, or Jerry-specific provisioning steps.
5. **The `.claude/` settings directory is shared** across all worktrees (it lives in the main repo's `.git` area). Each worktree gets its own `.git` file pointing to the shared repo.
6. **`CLAUDE.md` is read from the worktree root**, so each worktree automatically loads the correct context.
7. **Cross-worktree state coordination** (ORCHESTRATION.yaml, WORKTRACKER.md) requires either file-level locking or a coordinator process to prevent race conditions.

---

## L1: Technical Findings

### 1. Current Manual Workflow Documentation

The current Jerry multi-project workflow, as observed in this repository, follows this exact sequence:

**Step 1: Create worktree with branch**
```bash
git worktree add ../jerry-wt/feat/proj-006-multi-instance -b feat/proj-006-multi-instance
```
- **Pain point:** Requires knowing the naming convention and choosing a directory path
- **Error-prone:** Wrong path or duplicate branch name causes failure
- **Automation opportunity:** Generate path from project ID using convention

**Step 2: Navigate to worktree**
```bash
cd ../jerry-wt/feat/proj-006-multi-instance
```
- **Pain point:** Context switch to a new terminal/directory
- **Error-prone:** Forgetting which terminal is which project
- **Automation opportunity:** Automatic working directory binding

**Step 3: Set environment**
```bash
export JERRY_PROJECT=PROJ-006-multi-instance
```
- **Pain point:** Must remember the exact project ID string
- **Error-prone:** Typos, wrong project ID, forgetting to set it
- **Automation opportunity:** Derive from project directory; set in subprocess env

**Step 4: Install dependencies**
```bash
uv sync
```
- **Pain point:** Must wait for dependency resolution (~5s cached, ~30s+ cold)
- **Error-prone:** Rarely fails but blocks work until complete
- **Automation opportunity:** Run automatically; can be parallelized across worktrees

**Step 5: Install pre-commit hooks**
```bash
uv run pre-commit install
```
- **Pain point:** Easy to forget; commits without hooks bypass quality gates
- **Error-prone:** The session_start_hook.py already detects missing hooks and warns
- **Automation opportunity:** Run automatically after uv sync

**Step 6: Launch Claude session**
```bash
claude
```
- **Pain point:** Manual launch; no programmatic control over the session
- **Error-prone:** Session starts without context if JERRY_PROJECT not set
- **Automation opportunity:** Invoke via `-p` flag or SDK; set env vars

**Step 7: Work, commit, push**
- This step is the instance's responsibility and not part of lifecycle automation

**Step 8: Remove worktree**
```bash
git worktree remove ../jerry-wt/feat/proj-006-multi-instance
```
- **Pain point:** Must remember to clean up; orphaned worktrees waste disk space
- **Error-prone:** Removing with uncommitted changes loses work
- **Automation opportunity:** Automatic cleanup after session end; safety check for uncommitted work

**Step 9: Merge branch back to main**
```bash
git checkout main
git merge feat/proj-006-multi-instance
git push
git branch -d feat/proj-006-multi-instance
```
- **Pain point:** Multi-step process; conflict resolution requires manual intervention
- **Error-prone:** Merge conflicts, forgetting to push, leaving stale branches
- **Automation opportunity:** Automated fast-forward merge; conflict detection before merge attempt

**Observed Pattern in This Repository:**

The current repository has the following worktrees active (from `git worktree list`):

```
/Users/anowak/workspace/github/jerry                                      5adece9 [main]
/Users/anowak/workspace/github/jerry-wt/feat/proj-001-oss-documentation   5adece9 [feat/proj-001-oss-documentation]
/Users/anowak/workspace/github/jerry-wt/feat/proj-003-je-ne-sais-quoi     475d333 [feat/proj-003-je-ne-sais-quoi]
/Users/anowak/workspace/github/jerry-wt/feat/proj-004-context-resilience  2bac17c [feat/proj-004-context-resilience]
/Users/anowak/workspace/github/jerry-wt/feat/proj-005-markdown-ast        db6e7bd [feat/proj-005-markdown-ast]
/Users/anowak/workspace/github/jerry-wt/feat/proj-006-multi-instance      5adece9 [feat/proj-006-multi-instance]
```

This confirms the naming convention: `jerry-wt/feat/proj-{NNN}-{slug}` as the worktree directory pattern, with `feat/proj-{NNN}-{slug}` as the branch name pattern. The main worktree is at `jerry/` and all feature worktrees are siblings under `jerry-wt/feat/`.

---

### 2. Git Worktree API Research

#### 2.1 Native Git Commands (subprocess)

The authoritative interface for worktree operations. All commands are well-documented and stable.

| Command | Purpose | Exit Codes | Key Flags |
|---------|---------|------------|-----------|
| `git worktree add <path> [<branch>]` | Create worktree | 0=success, 128=error | `-b <new-branch>`, `--detach`, `--force` |
| `git worktree list` | List all worktrees | 0=success | `--porcelain` (machine-readable) |
| `git worktree remove <path>` | Remove worktree | 0=success, 128=error | `--force` (remove with changes) |
| `git worktree prune` | Clean stale refs | 0=success | `--dry-run`, `--verbose` |
| `git worktree lock <path>` | Prevent pruning | 0=success | `--reason <string>` |
| `git worktree unlock <path>` | Allow pruning | 0=success | -- |
| `git worktree move <src> <dst>` | Move worktree | 0=success | `--force` |
| `git worktree repair [<path>...]` | Fix broken links | 0=success | -- |

**Porcelain output format** (`git worktree list --porcelain`):
```
worktree /path/to/worktree
HEAD abc123def456
branch refs/heads/branch-name
<blank line>
```

This is the recommended format for programmatic parsing -- stable across Git versions, one field per line, blank-line delimited records.

**Concurrency safety:** Multiple worktrees can safely coexist and operate concurrently on the same repository. Git uses file-level locking internally for ref updates. The key constraint is that **each branch can only be checked out in one worktree at a time** -- attempting to check out the same branch in two worktrees will fail.

**Worktree internals:** Each worktree has a `.git` file (not directory) containing `gitdir: /path/to/main/.git/worktrees/<name>`. The main `.git/worktrees/<name>/` directory contains the worktree's HEAD, index, and other per-worktree state. The object store, refs, and config are shared.

Source: [Git Official Documentation - git-worktree](https://git-scm.com/docs/git-worktree)

#### 2.2 GitPython Library

GitPython v3.0.0+ supports worktree operations, but the API is a thin wrapper around git commands.

**Worktree creation:**
```python
from git import Repo
repo = Repo("/path/to/main/repo")
repo.git.worktree("add", "/path/to/worktree", "branch-name")
```

**Worktree listing:**
```python
output = repo.git.worktree("list", "--porcelain")
```

**Known limitations (from GitHub issue #719):**
- Worktree `.git` files (vs directories) caused `Repo()` initialization failures prior to v3.0.0
- `remote.push()` does not work from worktrees -- use `repo.git.push()` instead
- The API surface is identical to calling `git` via subprocess -- no higher-level abstractions
- Not zero-configuration: requires `gitpython` as a dependency

**Recommendation:** Use `subprocess.run(["git", "worktree", ...])` directly. GitPython adds a dependency without adding meaningful abstraction over the CLI for worktree operations. Jerry already has zero external git dependencies and subprocess is the more predictable approach.

Sources:
- [GitPython Issue #719: Support additional worktrees](https://github.com/gitpython-developers/GitPython/issues/719)
- [GitPython API Reference](https://gitpython.readthedocs.io/en/stable/reference.html)

#### 2.3 Branch Management Patterns

**Branch creation with worktree:**
```bash
# Create new branch from current HEAD
git worktree add ../path -b feat/proj-007-new-thing

# Create from a specific base (e.g., main)
git worktree add ../path -b feat/proj-007-new-thing origin/main
```

**Merging main into feature branch (inside worktree):**
```bash
cd /path/to/worktree
git fetch origin
git merge origin/main
```

**Branch naming convention (observed):**
- Pattern: `feat/proj-{NNN}-{slug}`
- Derived from: `JERRY_PROJECT` value (e.g., `PROJ-006-multi-instance` maps to branch `feat/proj-006-multi-instance`)

#### 2.4 Concurrent Worktree Safety

Git worktrees are designed for concurrent use. Key safety properties:

| Property | Status | Details |
|----------|--------|---------|
| Shared object store | Safe | Object writes are atomic; lockfile-based |
| Shared refs | Safe | Ref updates use file-level locks |
| Per-worktree index | Isolated | Each worktree has its own staging area |
| Per-worktree HEAD | Isolated | Each worktree tracks its own branch |
| Branch exclusivity | Enforced | Same branch cannot be checked out twice |
| Concurrent commits | Safe | Different branches commit independently |
| Concurrent pushes | Safe | Push uses remote ref locking |
| Concurrent fetches | Safe | Shared object store; fetch is additive |

**The main risk is not in git operations but in shared file modifications** -- if two worktrees both try to edit `ORCHESTRATION.yaml` or `WORKTRACKER.md` in overlapping ways, git merge will detect conflicts but cannot auto-resolve semantic conflicts (e.g., two worktrees both updating the same status field).

---

### 3. Environment Provisioning Requirements

#### 3.1 Complete Provisioning Checklist

Each worktree needs the following before a Claude instance can work in it:

| Step | Command | Estimated Time | Dependencies | Notes |
|------|---------|---------------|--------------|-------|
| 1. Create worktree | `git worktree add <path> -b <branch>` | <1s | Git repo | Creates directory, checks out files |
| 2. Set `JERRY_PROJECT` | `env={'JERRY_PROJECT': 'PROJ-NNN-slug'}` | 0s | Step 1 | Passed to subprocess environment |
| 3. Sync dependencies | `uv sync` (in worktree dir) | 3-30s | Step 1, uv installed | Cached: ~3-5s. Cold: ~20-30s |
| 4. Install pre-commit hooks | `uv run pre-commit install` (in worktree dir) | 1-2s | Step 3 | Installs hooks to shared `.git/hooks/` |
| 5. Verify provisioning | `uv run jerry --json projects context` | 1-2s | Steps 2-3 | Validates JERRY_PROJECT and project structure |
| 6. Launch Claude session | Depends on SDK/CLI | <1s | Steps 1-5 | Session binding approach TBD (SPIKE-001) |

**Total provisioning time:** ~5-35s per worktree (cached vs cold).

#### 3.2 Provisioning Order and Dependencies

```
Step 1 (worktree) ──> Step 2 (env var) ──> Step 3 (uv sync) ──> Step 4 (hooks) ──> Step 5 (verify) ──> Step 6 (launch)
                                                                       │
                                                                       └──> Step 4 depends on Step 3 (pre-commit needs venv)
```

Steps 2 and 3 could technically run in parallel (env var is just a string, uv sync does not need it), but Step 4 depends on Step 3 (pre-commit needs the virtual environment), and Step 5 depends on both 2 and 3.

#### 3.3 Caching and Pre-baking Opportunities

| Optimization | Approach | Savings |
|-------------|----------|---------|
| **Shared venv symlink** | Symlink `.venv/` from main worktree to avoid re-resolving | ~20-25s (cold) |
| **Cached uv sync** | `uv sync` is already fast with cache; lockfile unchanged = no-op | ~2-3s saved |
| **Pre-commit hook sharing** | Hooks install to shared `.git/hooks/`; only needed once | ~2s saved per worktree after first |
| **Template worktree** | Keep a pre-provisioned worktree as template; copy instead of create | All provisioning time saved |

**Shared venv symlink pattern** (from andreagrandi.it):
```bash
# In new worktree, create symlink to existing venv
ln -s /path/to/main/.venv /path/to/worktree/.venv
```

This avoids `uv sync` entirely but requires that all worktrees use the same dependency set. Since Jerry worktrees are branches of the same project, this is generally safe.

**Pre-commit hook sharing caveat:** Pre-commit hooks install to the git repository's hooks directory, which is shared across worktrees. So `uv run pre-commit install` only needs to run once (in any worktree), and all worktrees inherit the hooks. However, the `session_start_hook.py` already detects this and warns if hooks are missing.

#### 3.4 `.claude/` Settings Directory

The `.claude/settings.json` file is part of the repository and shared across all worktrees automatically (it is tracked in git). Each worktree gets its own copy of the file when the worktree is created.

Claude Code also has user-level settings at `~/.claude/settings.json` and project-level settings in `.claude/settings.local.json` (gitignored). The user-level settings are inherently shared; project-local settings are per-worktree.

**CLAUDE.md loading:** Claude Code reads `CLAUDE.md` from the project root, which is the worktree root. Each worktree has its own copy of `CLAUDE.md` (checked out from the branch), so context loading works correctly per-worktree.

---

### 4. Session Binding Patterns (Approach-Agnostic)

#### 4.1 Working Directory Isolation

Each Claude instance MUST operate in its own worktree directory. This is the foundational isolation boundary.

| Binding Pattern | Mechanism | Isolation Level |
|----------------|-----------|-----------------|
| **subprocess with cwd** | `subprocess.Popen(cmd, cwd=worktree_path)` | Process-level |
| **SDK with working_dir** | SDK constructor/method parameter (TBD) | Client-level |
| **Claude Code `-w`** | `claude -w <name>` creates/uses worktree automatically | Built-in |
| **Manual cd + launch** | `cd worktree && claude` | Terminal-level |

The subprocess approach is the most universal -- it works regardless of whether the instance is SDK-based or CLI-based. The `cwd` parameter to `subprocess.Popen` or `subprocess.run` sets the working directory for the child process.

#### 4.2 Environment Variable Isolation

Each instance needs its own `JERRY_PROJECT` value. This is achieved by passing a custom environment to the subprocess:

```python
import os
import subprocess

env = os.environ.copy()
env["JERRY_PROJECT"] = "PROJ-006-multi-instance"

subprocess.Popen(
    ["claude", "-p", "..."],
    cwd="/path/to/worktree",
    env=env,
)
```

Other environment variables that may need per-instance values:
- `CLAUDE_PROJECT_DIR`: Set automatically by Claude Code to the project root
- `ANTHROPIC_API_KEY`: Shared (same API key for all instances)
- `PATH`: Shared (same tools available)

#### 4.3 File System Isolation: Per-Worktree vs Shared State

| Resource | Per-Worktree | Shared | Notes |
|----------|-------------|--------|-------|
| Source code | Yes | No | Each worktree has its own checkout |
| `.git/` (objects, refs) | No | Yes | Shared git database |
| `.git/worktrees/<name>/` | Yes | No | Per-worktree HEAD, index |
| `.venv/` | Yes (or symlinked) | Optional | Can be symlinked for speed |
| `CLAUDE.md` | Yes | No | Checked out per-branch |
| `.claude/settings.json` | Yes | No | Checked out per-branch |
| `projects/` | Yes | No | Each branch may have different project state |
| `WORKTRACKER.md` | Yes | No | Per-branch work tracking |
| `ORCHESTRATION.yaml` | Yes | No | Per-branch orchestration state |

**Critical implication:** Since `WORKTRACKER.md` and `ORCHESTRATION.yaml` are per-worktree (per-branch), cross-instance coordination requires a merge-based approach. One instance cannot directly read another instance's state files -- it must merge the other branch or use a shared coordination mechanism outside of git (e.g., filesystem locks, a coordinator process, or a shared state file in a known location).

---

### 5. Dispatch and Monitoring Patterns

#### 5.1 Dispatch (Sending Work to an Instance)

| Pattern | Mechanism | Pros | Cons |
|---------|-----------|------|------|
| **CLI -p flag** | `claude -p "prompt" --output-format json` | Simple, stateless, captures output | No interactive tool use unless allowed |
| **CLI -p with tools** | `claude -p "prompt" --allowedTools "Read,Write,Edit,Bash"` | Full tool access, unattended | Must pre-approve tools |
| **CLI -p with --continue** | Capture session_id, use `--resume` | Multi-turn capability | Requires session ID management |
| **SDK client** | Programmatic API call (TBD) | Full control, structured output | Requires SDK integration |
| **File-based dispatch** | Write task to file, instance polls | Decoupled | Polling latency, complexity |

**Recommended for Jerry:** CLI `-p` with `--output-format json` and `--allowedTools` for initial implementation. This provides:
- Full tool access for the instance to work autonomously
- Structured JSON output with session ID, result, and metadata
- No interactive terminal requirement
- Session continuation via `--resume`

**Example dispatch:**
```bash
claude -p "Research git worktree automation patterns. Write findings to spike-002-research.md." \
    --output-format json \
    --allowedTools "Read,Write,Edit,Bash,Glob,Grep,WebSearch,WebFetch" \
    2>/dev/null
```

#### 5.2 Monitoring (Tracking Instance Progress)

| Pattern | Mechanism | Latency | Notes |
|---------|-----------|---------|-------|
| **Process exit monitoring** | `subprocess.Popen.poll()` / `.wait()` | Real-time | Simplest; detects completion/failure |
| **Streaming JSON output** | `--output-format stream-json --verbose` | Real-time | Tokens + events as they occur |
| **File watching** | `inotify`/`kqueue` on output files | Near-real-time | Watch for file changes in worktree |
| **Periodic polling** | Check git status, file timestamps | Configurable | Low overhead but adds latency |
| **Session status check** | `claude --resume <id> --output-format json` | On-demand | Query session state |

**Recommended approach:** Combine process exit monitoring (for completion/failure) with streaming JSON (for progress). The coordinator can:
1. Start each instance as a subprocess with `stream-json` output
2. Read stdout line-by-line for progress events
3. Detect completion via process exit code (0 = success, non-zero = failure)
4. Detect timeouts via `subprocess.Popen` timeout parameter

#### 5.3 Output Capture

Claude Code `-p` with `--output-format json` returns:
```json
{
    "result": "... text output ...",
    "session_id": "...",
    "cost_usd": 0.05,
    "duration_ms": 12345,
    "num_turns": 3,
    "is_error": false
}
```

With `--json-schema`, structured output can be enforced:
```bash
claude -p "..." --output-format json \
    --json-schema '{"type":"object","properties":{"status":{"type":"string"},"findings":{"type":"array"}}}'
```

This allows the coordinator to parse structured results from each instance.

#### 5.4 Timeout and Cancellation

| Mechanism | How | Notes |
|-----------|-----|-------|
| **Process timeout** | `subprocess.Popen.wait(timeout=N)` | Raises `TimeoutExpired`; must then `.kill()` |
| **SIGTERM** | `process.terminate()` | Graceful shutdown signal |
| **SIGKILL** | `process.kill()` | Immediate termination (last resort) |
| **Context budget** | Set `MAX_THINKING_TOKENS` or token budget | Limits per-instance cost |

---

### 6. Merge Coordination

#### 6.1 Merge Strategies

| Strategy | When to Use | Command | Conflict Risk |
|----------|------------|---------|---------------|
| **Fast-forward** | Feature branch is ahead of main, no divergence | `git merge --ff-only feat/branch` | None |
| **3-way merge** | Branches have diverged | `git merge feat/branch` | Medium |
| **Rebase** | Clean linear history desired | `git rebase main` (in feature branch) | Medium |
| **Squash merge** | Compact feature into single commit | `git merge --squash feat/branch` | Low |

**Recommended for Jerry:** Fast-forward when possible (linear workflow), 3-way merge as fallback. Squash merge for spike/research branches where individual commit history is not needed.

#### 6.2 Conflict Detection Before Merge

**`git merge-tree` (the critical tool):**

```bash
git merge-tree --write-tree main feat/proj-006-multi-instance
```

- **Exit code 0:** Clean merge. Output is the resulting tree OID.
- **Exit code 1:** Conflicts detected. Output includes conflicted file info.
- **Exit code 2+:** Error (invalid refs, etc.)

This performs the merge entirely in memory -- no working tree changes, no index changes, no commits. It is safe to run from any directory and does not affect any worktree.

**Conflict detection script pattern:**
```bash
#!/bin/bash
RESULT=$(git merge-tree --write-tree main "$BRANCH" 2>&1)
EXIT=$?

if [ $EXIT -eq 0 ]; then
    echo "CLEAN: No conflicts"
elif [ $EXIT -eq 1 ]; then
    echo "CONFLICT: Merge has conflicts"
    echo "$RESULT"  # Contains conflicted file info
else
    echo "ERROR: Merge failed"
fi
```

**`clash` tool (real-time conflict monitoring):**

The [clash](https://github.com/clash-sh/clash) tool provides continuous conflict monitoring across all worktrees:
- Uses `git merge-tree` via the `gix` library (pure Rust git implementation)
- TUI dashboard showing conflict matrix between all branch pairs
- File-watching via `notify` crate for auto-refresh on changes
- Claude Code plugin integration (`PreToolUse` event hook)
- JSON output for programmatic consumption

Clash is a valuable reference implementation but is a Rust dependency. Jerry could implement the core `git merge-tree` check in Python via subprocess without the full TUI.

Source: [clash-sh/clash on GitHub](https://github.com/clash-sh/clash)

#### 6.3 Conflict Escalation Protocol

| Conflict Type | Auto-Resolution | Escalation |
|---------------|----------------|------------|
| No conflicts (fast-forward) | Merge automatically | None |
| No conflicts (3-way merge) | Merge automatically | None |
| Textual conflicts in non-critical files | Attempt auto-resolution | Operator review if auto-resolution uncertain |
| Conflicts in `WORKTRACKER.md` | Semantic merge (take latest status) | Operator review |
| Conflicts in `ORCHESTRATION.yaml` | Semantic merge (take latest state) | Operator review |
| Conflicts in source code | Never auto-resolve | Operator escalation mandatory |
| Conflicts in `.context/rules/` | Never auto-resolve (AE-002: auto-C3) | Operator escalation mandatory |

#### 6.4 Merge Order

Does the order in which projects merge matter? **Yes, but only when branches conflict.**

If projects work on independent files (the common case with separate `projects/PROJ-NNN-*/` directories), merge order is irrelevant -- all merges will be fast-forward or clean 3-way.

If projects touch shared files (e.g., `CLAUDE.md`, `.context/rules/`, `pyproject.toml`), the first merge succeeds cleanly but subsequent merges may encounter conflicts with the now-updated main branch. The recommendation is:

1. Run `git merge-tree` for all pending branches against main
2. Sort by conflict count (ascending) -- merge cleanest branches first
3. After each merge to main, re-check remaining branches against updated main
4. Escalate any conflicts to operator

---

### 7. Cross-Worktree State Coordination

#### 7.1 State Files That Need Coordination

| File | Shared? | Conflict Risk | Coordination Strategy |
|------|---------|---------------|----------------------|
| `ORCHESTRATION.yaml` | No (per-branch) | High | Coordinator writes; instances read only |
| `WORKTRACKER.md` | No (per-branch) | Medium | Each instance owns its project's tracker |
| `projects/README.md` | No (per-branch) | Low | Updated on merge |
| `CLAUDE.md` | No (per-branch) | Low | Rarely changes during work |
| `.context/rules/*` | No (per-branch) | High (AE-002) | Instances should not modify |

#### 7.2 Coordination Patterns

**Pattern 1: Coordinator-Owned State (Recommended)**

The coordinator process owns `ORCHESTRATION.yaml` and writes to it directly. Instances do not modify orchestration state -- they produce artifacts and signal completion. The coordinator reads artifacts and updates state.

```
Coordinator Process
    |
    |-- Writes ORCHESTRATION.yaml (owns state)
    |-- Reads agent artifacts
    |-- Monitors instance processes
    |
    +-- Instance A (worktree-A)
    |       |-- Reads ORCHESTRATION.yaml (read-only)
    |       |-- Writes agent-a-001-research.md (own artifact)
    |       +-- Commits to feat/branch-a
    |
    +-- Instance B (worktree-B)
            |-- Reads ORCHESTRATION.yaml (read-only)
            |-- Writes agent-b-001-research.md (own artifact)
            +-- Commits to feat/branch-b
```

Advantages: No concurrent writes. No locks needed. Clear ownership.
Disadvantage: Instances cannot update their own status in the tracker.

**Pattern 2: File Locking (Alternative)**

Use `filelock` (already a Jerry dependency) to coordinate writes to shared state:

```python
from filelock import FileLock

lock = FileLock("/path/to/main/repo/.jerry/orchestration.lock")
with lock:
    # Read, modify, write ORCHESTRATION.yaml
    pass
```

Advantage: Any process can update state.
Disadvantage: Lock contention; requires shared filesystem path accessible by all worktrees.

**Pattern 3: Event-Based Coordination (Future)**

Instances write completion events to a shared event log. The coordinator processes events and updates state.

```
Instance A writes: {"event": "phase_complete", "agent": "agent-a-001", "artifact": "..."}
Instance B writes: {"event": "phase_complete", "agent": "agent-b-001", "artifact": "..."}
Coordinator reads log, updates ORCHESTRATION.yaml
```

Advantage: Fully decoupled; append-only log avoids conflicts.
Disadvantage: More complex; requires event schema.

**Recommendation:** Start with Pattern 1 (Coordinator-Owned State) for simplicity. The coordinator is already the orchestrator process that dispatches work -- it naturally owns the state.

#### 7.3 Cross-Worktree File Access

Worktrees on the same machine can read each other's files directly via filesystem paths:

```python
# From coordinator, read Instance A's artifact
artifact_path = Path("/path/to/worktree-a/projects/PROJ-006/orchestration/.../agent-a-001-research.md")
content = artifact_path.read_text()
```

This is simpler than merge-based approaches for reading artifacts. The coordinator can poll for artifact existence, read content, and use it for cross-pollination without any git operations.

---

### 8. Jerry CLI Integration Sketch

#### 8.1 Proposed Command Surface

```
jerry worktree create <project-id> [--base <branch>] [--path <dir>]
jerry worktree provision <path>
jerry worktree dispatch <path> --prompt <text> [--tools <list>] [--timeout <secs>]
jerry worktree status [<path>]
jerry worktree merge <path> [--strategy <ff|merge|squash>] [--dry-run]
jerry worktree cleanup <path> [--force]
jerry worktree list
```

#### 8.2 Command Details

**`jerry worktree create`**
```
jerry worktree create PROJ-006-multi-instance [--base main] [--path ../jerry-wt/feat/proj-006]

Arguments:
  project-id       Jerry project ID (PROJ-NNN-slug)

Options:
  --base <branch>  Base branch (default: main)
  --path <dir>     Worktree directory (default: ../jerry-wt/feat/proj-{nnn}-{slug})

Actions:
  1. git worktree add <path> -b feat/proj-{nnn}-{slug} [base]
  2. Set JERRY_PROJECT in worktree config
  3. Run uv sync in worktree
  4. Run uv run pre-commit install (if not already installed)
  5. Validate with jerry projects context

Output (JSON):
  {
    "worktree_path": "/abs/path/to/worktree",
    "branch": "feat/proj-006-multi-instance",
    "project_id": "PROJ-006-multi-instance",
    "provisioned": true,
    "provisioning_time_ms": 8500
  }
```

**`jerry worktree dispatch`**
```
jerry worktree dispatch /path/to/worktree --prompt "Research X" [--tools "Read,Write,Bash"]

Arguments:
  path             Path to provisioned worktree

Options:
  --prompt <text>  Task prompt to send to Claude instance
  --tools <list>   Comma-separated tool allowlist (default: Read,Write,Edit,Bash,Glob,Grep)
  --timeout <secs> Max execution time (default: 3600)
  --output-format  json | stream-json | text (default: json)
  --async          Return immediately with process ID

Actions:
  1. Validate worktree exists and is provisioned
  2. Set env: JERRY_PROJECT from worktree config
  3. Launch: claude -p "<prompt>" --allowedTools "<tools>" --output-format json
  4. If --async: return PID. Otherwise: wait for completion.

Output (JSON):
  {
    "dispatch_id": "dispatch-20260220-001",
    "worktree_path": "/abs/path",
    "pid": 12345,
    "status": "running" | "complete" | "failed",
    "result": "..." (if complete)
  }
```

**`jerry worktree status`**
```
jerry worktree status [/path/to/worktree]

Arguments:
  path             (Optional) Specific worktree to check. If omitted, show all.

Output (JSON):
  [
    {
      "path": "/abs/path",
      "branch": "feat/proj-006-multi-instance",
      "project_id": "PROJ-006-multi-instance",
      "provisioned": true,
      "dispatch_status": "running" | "idle" | "complete" | "failed",
      "pid": 12345,
      "uncommitted_changes": false,
      "merge_conflicts": false
    }
  ]
```

**`jerry worktree merge`**
```
jerry worktree merge /path/to/worktree [--strategy ff|merge|squash] [--dry-run]

Arguments:
  path               Worktree to merge back to base branch

Options:
  --strategy <type>  Merge strategy (default: ff, fallback: merge)
  --dry-run          Check for conflicts without merging

Actions:
  1. Run git merge-tree to detect conflicts
  2. If --dry-run: report and exit
  3. If clean: perform merge to main, push, delete branch
  4. If conflicts: report conflicts and escalate to operator

Output (JSON):
  {
    "worktree_path": "/abs/path",
    "branch": "feat/proj-006",
    "target": "main",
    "strategy": "fast-forward",
    "status": "merged" | "conflicts" | "dry-run-clean" | "dry-run-conflicts",
    "conflicts": []
  }
```

**`jerry worktree cleanup`**
```
jerry worktree cleanup /path/to/worktree [--force]

Arguments:
  path             Worktree to remove

Options:
  --force          Remove even with uncommitted changes

Actions:
  1. Check for uncommitted changes (abort if found unless --force)
  2. git worktree remove <path>
  3. Optionally delete branch if merged
  4. git worktree prune
```

**`jerry worktree list`**
```
jerry worktree list

Output: Table of all worktrees with project, branch, and status.
```

#### 8.3 Integration with Existing Jerry CLI

The worktree namespace would be added alongside existing namespaces (session, items, projects, config, transcript) in `src/interface/cli/parser.py`. The implementation would follow the same hexagonal architecture pattern:

```
parser.py          -> _add_worktree_namespace()
main.py            -> _handle_worktree()
adapter.py         -> cmd_worktree_create(), cmd_worktree_dispatch(), etc.
bootstrap.py       -> create_worktree_service()
domain/            -> Worktree, WorktreeStatus (value objects)
application/       -> CreateWorktreeCommand, DispatchWorkCommand, etc.
infrastructure/    -> GitSubprocessAdapter, ClaudeProcessAdapter
```

---

### 9. Reference Implementations

#### 9.1 ccswarm (nwiizo)

**Repository:** [github.com/nwiizo/ccswarm](https://github.com/nwiizo/ccswarm)

A Rust-based multi-agent orchestration system using Claude Code with git worktree isolation.

| Aspect | Details |
|--------|---------|
| Language | Rust |
| Worktree management | Automatic create, list, remove, prune |
| Session binding | PTY (pseudo-terminal) sessions, native (no tmux) |
| Agent architecture | Master Claude orchestrator + specialized agents |
| Monitoring | TUI with real-time resource tracking |
| Key insight | Session-Persistent Manager claims 93% token reduction |

**Relevance to Jerry:** ccswarm validates the architectural approach of worktree-based isolation with a master orchestrator. However, it is a Rust crate, not a Python library. The PTY session approach is more complex than Claude Code's `-p` flag but provides richer interactive control.

#### 9.2 git-worktree-runner (CodeRabbit)

**Repository:** [github.com/coderabbitai/git-worktree-runner](https://github.com/coderabbitai/git-worktree-runner)

A Bash-based worktree manager focused on developer workflow automation.

| Aspect | Details |
|--------|---------|
| Language | Bash |
| Key commands | `git gtr new`, `git gtr editor`, `git gtr ai`, `git gtr run`, `git gtr rm`, `git gtr clean` |
| Provisioning | Post-create hooks, config file copying, dependency dir copying |
| Cleanup | Manual `rm` + automated `clean --merged` (checks GitHub PRs) |
| Configuration | Three-tier: local git config, `.gtrconfig` (repo), global |
| AI integration | `git gtr ai <branch>` launches AI tools in worktree |

**Relevance to Jerry:** The hooks system (`gtr.hook.postCreate`, `gtr.hook.postCd`) is directly applicable. The `gtr.copy.include` pattern for syncing config files to worktrees is useful for `.env` or local config. The `clean --merged` command that checks GitHub PR status is a good pattern for automated cleanup.

#### 9.3 Claude Code Built-in Worktree Support

**Documentation:** [code.claude.com/docs/en/common-workflows](https://code.claude.com/docs/en/common-workflows)

Claude Code has native worktree support via the `--worktree` / `-w` flag.

| Aspect | Details |
|--------|---------|
| Creation | `claude -w <name>` creates worktree at `.claude/worktrees/<name>/` |
| Branch naming | `worktree-<name>` |
| Base branch | Default remote branch |
| Cleanup | Auto-remove if no changes; prompt if changes exist |
| Session resume | Sessions in worktrees show in `/resume` picker |
| Integration | Works with all other flags (`-p`, `--output-format`, etc.) |

**Relevance to Jerry:** This is the simplest path for basic multi-instance work but has limitations:
- Worktree path is fixed to `.claude/worktrees/<name>/` (inside the repo)
- Branch naming is `worktree-<name>`, not Jerry's `feat/proj-{NNN}-{slug}` convention
- No `JERRY_PROJECT` auto-setting
- No `uv sync` or hook provisioning
- No merge coordination

For Jerry's use case, custom worktree management that wraps git commands directly would provide more control while still leveraging Claude's `-p` flag for dispatch.

---

## L2: Architectural Implications

### 1. Design Decision: Subprocess vs GitPython

**Recommendation: Subprocess (direct `git` CLI calls)**

| Criterion | subprocess | GitPython |
|-----------|-----------|-----------|
| Dependency | None (git is required anyway) | `gitpython` package |
| API surface for worktrees | Full (all git commands) | Thin wrapper only |
| Predictability | High (CLI is stable API) | Medium (library abstractions may lag) |
| Push/pull from worktree | Works natively | `remote.push()` broken; must use `repo.git.push()` |
| Error handling | Parse stderr + exit codes | Exception hierarchy |
| Jerry compatibility | Zero new dependencies (H-06: UV only) | Requires `uv add gitpython` |

Since GitPython's worktree API is just `repo.git.worktree("add", ...)` (which is literally calling subprocess internally), there is no meaningful abstraction gain. Direct subprocess calls are simpler, have zero dependencies, and match Jerry's existing patterns (see `session_start_hook.py` which already uses `subprocess.run`).

### 2. Design Decision: Worktree Path Convention

**Current observed pattern:**
```
~/workspace/github/jerry                          (main worktree)
~/workspace/github/jerry-wt/feat/proj-NNN-slug    (feature worktrees)
```

**Claude Code's pattern:**
```
<repo>/.claude/worktrees/<name>/                  (inside repo)
```

**Recommendation:** Use the current observed pattern (`jerry-wt/feat/...`) as it keeps worktrees outside the main repo directory, avoiding `.gitignore` complexity and making it clear which directory is the main repo vs a worktree. The path should be configurable.

### 3. Design Decision: Provisioning Strategy

**Recommendation: Sequential provisioning with optional venv symlink**

The provisioning sequence is simple and fast enough that parallelization is unnecessary for a single worktree. For bulk creation (N worktrees), the worktree creation can be parallelized but `uv sync` should be sequential (it may contend on the cache).

The venv symlink optimization should be offered as an option (`--share-venv`) but not the default, since it couples all worktrees to the same dependency set and can cause confusion if a branch modifies `pyproject.toml`.

### 4. Integration Risk: Cross-Worktree State

The highest-risk aspect of the entire multi-instance architecture is cross-worktree state coordination. The coordinator-owned state pattern (Pattern 1) mitigates this by keeping state management centralized, but it means instances cannot self-report their status to `WORKTRACKER.md`.

**Mitigation:** Instances write completion artifacts (markdown files) to their branch. The coordinator reads these artifacts and updates `WORKTRACKER.md` centrally. This is exactly how the current orchestration plan (ORCHESTRATION_PLAN.md) is designed -- artifacts are per-agent, tracked by the coordinator.

### 5. Integration Risk: Claude Code `-w` Flag Overlap

Claude Code's built-in `--worktree` flag overlaps with Jerry's proposed `jerry worktree create`. There are two paths:

**Path A: Complement Claude's `-w` flag.** Use `jerry worktree create` for provisioning (env vars, deps, hooks) and then dispatch with `claude -p` in the provisioned worktree. Do not use `claude -w`.

**Path B: Extend Claude's `-w` flag via hooks.** Use Claude's built-in worktree creation and add a `PostWorktreeCreate` hook (if available) to run Jerry provisioning steps.

**Recommendation:** Path A. Jerry needs custom branch naming, path conventions, and `JERRY_PROJECT` setting that Claude's `-w` flag does not support. Using the built-in flag would constrain Jerry's worktree conventions.

### 6. Makefile Integration

The existing `Makefile` already has a `setup` target that runs `uv sync && uv run pre-commit install`. The worktree provisioning should invoke `make setup` (or its constituent commands) to stay aligned with the project's existing setup conventions.

### 7. `.gitignore` Update Required

The current `.gitignore` does not include `.claude/worktrees/`. If Claude's built-in `-w` flag is used (even experimentally), this line should be added:
```
.claude/worktrees/
```

---

## References

### Git Documentation
1. [Git Official - git-worktree](https://git-scm.com/docs/git-worktree) -- Authoritative reference for all worktree commands
2. [Git Official - git-merge-tree](https://git-scm.com/docs/git-merge-tree) -- Dry-run merge conflict detection without working tree changes
3. [Git Official - git-merge](https://git-scm.com/docs/git-merge) -- Merge strategies and conflict resolution

### GitPython
4. [GitPython Issue #719: Worktree Support](https://github.com/gitpython-developers/GitPython/issues/719) -- Worktree support added in v3.0.0; thin wrapper over CLI
5. [GitPython API Reference](https://gitpython.readthedocs.io/en/stable/reference.html) -- API surface documentation

### Reference Implementations
6. [nwiizo/ccswarm](https://github.com/nwiizo/ccswarm) -- Rust multi-agent orchestration with git worktree isolation
7. [coderabbitai/git-worktree-runner](https://github.com/coderabbitai/git-worktree-runner) -- Bash worktree manager with provisioning hooks
8. [clash-sh/clash](https://github.com/clash-sh/clash) -- Rust conflict detection across worktrees using git merge-tree
9. [frankbria/parallel-cc](https://github.com/frankbria/parallel-cc) -- Automated parallel Claude Code management with git worktrees

### Claude Code Documentation
10. [Claude Code - Run Programmatically (Headless Mode)](https://code.claude.com/docs/en/headless) -- CLI `-p` flag, JSON output, session management, tool approval
11. [Claude Code - Common Workflows](https://code.claude.com/docs/en/common-workflows) -- Git worktree workflow, `--worktree` flag, parallel sessions

### Patterns and Best Practices
12. [Andrea Grandi - Git Worktrees with Python Projects](https://www.andreagrandi.it/posts/how-to-use-git-worktree-effectively-with-python-projects/) -- venv symlink pattern for Python worktrees
13. [Git Worktree Best Practices (GitHub Gist)](https://gist.github.com/ChristopherA/4643b2f5e024578606b9cd5d2e6815cc) -- Comprehensive best practices
14. [Steve Kinney - Git Worktrees for Parallel AI Development](https://stevekinney.com/courses/ai-development/git-worktrees) -- AI-specific worktree patterns
15. [Nx Blog - How Git Worktrees Changed My AI Agent Workflow](https://nx.dev/blog/git-worktrees-ai-agents) -- Worktree patterns for AI agents
16. [Upsun Dev Center - Git Worktrees for Parallel AI Coding Agents](https://devcenter.upsun.com/posts/git-worktrees-for-parallel-ai-coding-agents/) -- Production patterns

### Jerry Codebase (Internal)
17. `scripts/session_start_hook.py` -- Existing worktree-aware hook (handles `.git` file detection)
18. `src/interface/cli/main.py` -- Current CLI namespace structure
19. `src/interface/cli/parser.py` -- Argparse configuration for CLI
20. `src/bootstrap.py` -- Composition root with `JERRY_PROJECT` / `CLAUDE_PROJECT_DIR` handling
21. `.pre-commit-config.yaml` -- Full hook configuration (provisioning requirement)
22. `Makefile` -- `make setup` target for worktree provisioning
23. `pyproject.toml` -- Dependency management (`filelock` already present)

---

*Agent: agent-b-001 (ps-researcher v2.3.0)*
*Pipeline: spike-002 (Worktree & Session Lifecycle)*
*Phase: 1 (Research)*
*Workflow: multi-instance-20260220-001*
*S-010 (Self-Refine) applied: Reviewed for completeness, internal consistency, evidence quality, and actionability before finalization.*
