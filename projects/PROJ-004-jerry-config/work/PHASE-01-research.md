# PHASE-01: Research & Discovery

| Field | Value |
|-------|-------|
| **Phase ID** | PHASE-01 |
| **Title** | Research & Discovery |
| **Status** | COMPLETED |
| **Parallelizable** | Yes (4 parallel research tasks) |
| **Work Items** | WI-003, WI-004, WI-005, WI-006 |
| **Assignee** | WT-Main |
| **Started** | 2026-01-12 |
| **Completed** | 2026-01-12 |

---

## Objective

Research best practices and patterns for configuration management, file locking, worktree safety, and precedence models. This phase used the `ps-researcher` agents from the problem-solving skill to parallelize research.

---

## Work Items

| ID | Title | Status | File | Research Artifact |
|----|-------|--------|------|-------------------|
| WI-003 | JSON5 Python Support | COMPLETED | [wi-003-json5-research.md](wi-003-json5-research.md) | [PROJ-004-e-001](../research/PROJ-004-e-001-json5-python-support.md) |
| WI-004 | Runtime Collision Avoidance | COMPLETED | [wi-004-collision-avoidance.md](wi-004-collision-avoidance.md) | [PROJ-004-e-002](../research/PROJ-004-e-002-runtime-collision-avoidance.md) |
| WI-005 | Worktree-Safe State Patterns | COMPLETED | [wi-005-worktree-patterns.md](wi-005-worktree-patterns.md) | [PROJ-004-e-003](../research/PROJ-004-e-003-worktree-safe-state.md) |
| WI-006 | Configuration Precedence Model | COMPLETED | [wi-006-config-precedence.md](wi-006-config-precedence.md) | [PROJ-004-e-004](../research/PROJ-004-e-004-config-precedence.md) |

---

## Key Findings

### WI-003: Config Format Decision

**Decision**: Use **TOML** instead of JSON5

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| JSON5 | Comments, trailing commas | No stdlib, pyjson5 is slow | Rejected |
| TOML | Stdlib (tomllib), Pythonic, comments | Write needs tomli-w | **Selected** |
| YAML | Human-friendly | Complex spec, security issues | Rejected |

### WI-004: File Locking Strategy

**Decision**: `fcntl.lockf()` + atomic writes

| Pattern | Description | Recommendation |
|---------|-------------|----------------|
| Advisory locking | `fcntl.lockf(fd, LOCK_EX)` | Use for write operations |
| Atomic writes | `tempfile.mkstemp()` + `os.replace()` | Always use for writes |
| Separate lock files | `.lock` file in local/ | Never lock data file directly |

### WI-005: Worktree Safety

**Discovery**: Jerry already uses merge-safe pattern (one-file-per-entity with Snowflake IDs)

| Component | Location | Git Status |
|-----------|----------|------------|
| Shared config | `.jerry/config.toml` | Committed |
| Event files | `.jerry/data/events/{id}.jsonl` | Committed (merge-safe) |
| Local state | `.jerry/local/` | Gitignored |

### WI-006: Precedence Model

**Decision**: 12-factor app aligned precedence

| Priority | Source | Override Pattern |
|----------|--------|------------------|
| 1 (Highest) | CLI Arguments | `--project=PROJ-001` |
| 2 | Environment Variables | `JERRY_PROJECT=PROJ-001` |
| 3 | Project Config | `projects/PROJ-*/.jerry/config.toml` |
| 4 | Root Config | `.jerry/config.toml` |
| 5 (Lowest) | Code Defaults | `DEFAULT_LOG_LEVEL = "INFO"` |

---

## Research Artifacts

| ID | Topic | Size | Location |
|----|-------|------|----------|
| PROJ-004-e-001 | JSON5 Python Support | 483 lines | [research/](../research/PROJ-004-e-001-json5-python-support.md) |
| PROJ-004-e-002 | Runtime Collision Avoidance | 672 lines | [research/](../research/PROJ-004-e-002-runtime-collision-avoidance.md) |
| PROJ-004-e-003 | Worktree-Safe State | 412 lines | [research/](../research/PROJ-004-e-003-worktree-safe-state.md) |
| PROJ-004-e-004 | Config Precedence | 389 lines | [research/](../research/PROJ-004-e-004-config-precedence.md) |

---

## Phase Summary

All four research tasks completed in parallel using `ps-researcher` agents. The findings were synthesized into PLAN.md during PHASE-02. Key decisions:

1. **TOML over JSON5** - Zero external dependencies
2. **fcntl + atomic writes** - Stdlib-only locking
3. **Jerry is already merge-safe** - No changes needed for event storage
4. **12-factor precedence** - Env vars override config files

---

## Navigation

- **Previous Phase**: [PHASE-00: Project Setup](PHASE-00-project-setup.md)
- **Next Phase**: [PHASE-02: Architecture & Design](PHASE-02-architecture.md)
- **WORKTRACKER**: [../WORKTRACKER.md](../WORKTRACKER.md)
