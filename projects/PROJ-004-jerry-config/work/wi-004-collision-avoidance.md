# WI-004: Runtime Collision Avoidance Patterns

| Field | Value |
|-------|-------|
| **ID** | WI-004 |
| **Title** | Research runtime collision avoidance patterns |
| **Type** | Research |
| **Status** | COMPLETED |
| **Priority** | CRITICAL |
| **Phase** | PHASE-01 |
| **Assignee** | WT-Main |
| **Created** | 2026-01-12 |
| **Completed** | 2026-01-12 |

---

## Description

Research patterns for preventing runtime file collisions when multiple processes access configuration files.

---

## Acceptance Criteria

- [x] AC-004.1: Document file locking strategies (fcntl, portalocker)
- [x] AC-004.2: Evaluate atomic write patterns (write-rename)
- [x] AC-004.3: Assess lock file approaches
- [x] AC-004.4: Recommend approach for Jerry

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-004.1 | `fcntl.flock()` (BSD), `fcntl.lockf()` (POSIX recommended), `msvcrt` (Windows) documented | PROJ-004-e-002, Section 1.1-1.2 |
| AC-004.2 | Atomic write: `tempfile.mkstemp()` + `os.fsync()` + `os.replace()` pattern documented | PROJ-004-e-002, Section 1.3 |
| AC-004.3 | Lock file pattern with `O_CREAT | O_EXCL` + PID tracking + stale detection | PROJ-004-e-002, Section 1.4, 3.2 |
| AC-004.4 | **Phase 1: stdlib (fcntl.lockf + atomic writes)**, Phase 2: filelock library for Windows | PROJ-004-e-002, L2 Section |

---

## Sub-tasks

- [x] ST-004.1: Research Python fcntl module
- [x] ST-004.2: Research atomic file operations
- [x] ST-004.3: Analyze existing Jerry file operations
- [x] ST-004.4: Create research artifact with findings

---

## Key Findings

1. **Separate lock files** - Never lock data file directly
2. **Combine locking + atomic writes** - Belt and suspenders approach
3. **Use `os.replace()` not `os.rename()`** - Cross-platform atomicity
4. **OS-level locks auto-release** - On process crash, locks are freed
5. **filelock library** - Best for cross-platform if external deps allowed

---

## Progress Log

| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T10:10:00Z | Work item created, ps-researcher agent spawned | Claude |
| 2026-01-12T10:15:00Z | Research completed, 672-line artifact created | ps-researcher |
| 2026-01-12T10:16:00Z | All acceptance criteria verified, WI-004 COMPLETED | Claude |

---

## Dependencies

| Type | Work Item | Relationship |
|------|-----------|--------------|
| Depends On | WI-002 | Tracking must be set up |
| Blocks | WI-007, WI-012 | Plan and adapter need locking strategy |

---

## Related Artifacts

- **Research Artifact**: [PROJ-004-e-002-runtime-collision-avoidance.md](../research/PROJ-004-e-002-runtime-collision-avoidance.md)

---

## Sources

- [Python fcntl Documentation](https://docs.python.org/3/library/fcntl.html)
- [filelock PyPI](https://pypi.org/project/filelock/)
- [portalocker GitHub](https://github.com/wolph/portalocker)
- [Atomic File Writes - Python Atomicwrites](https://python-atomicwrites.readthedocs.io/)
