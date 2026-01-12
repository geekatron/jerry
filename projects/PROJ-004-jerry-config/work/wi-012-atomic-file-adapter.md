# WI-012: Atomic File Adapter

| Field | Value |
|-------|-------|
| **ID** | WI-012 |
| **Title** | Atomic File Adapter |
| **Type** | Task |
| **Status** | PENDING |
| **Priority** | CRITICAL |
| **Phase** | PHASE-04 |
| **Assignee** | WT-Infra |
| **Created** | 2026-01-12 |
| **Completed** | - |

---

## Description

Implement an atomic file adapter that provides safe concurrent file access using file locking (`fcntl.lockf`) and atomic writes (`tempfile + os.replace`). This is critical infrastructure for preventing data corruption.

---

## Acceptance Criteria

- [ ] AC-012.1: `read_with_lock()` acquires shared lock before reading
- [ ] AC-012.2: `write_atomic()` uses exclusive lock + temp file + os.replace
- [ ] AC-012.3: Lock files are in `.jerry/local/locks/` (gitignored)
- [ ] AC-012.4: Locks auto-release on process crash (OS-level)
- [ ] AC-012.5: Handles missing directories gracefully
- [ ] AC-012.6: Integration tests with concurrent access simulation

---

## Sub-tasks

- [ ] ST-012.1: Create `src/infrastructure/adapters/persistence/atomic_file_adapter.py`
- [ ] ST-012.2: Implement shared lock for reads
- [ ] ST-012.3: Implement exclusive lock + atomic write pattern
- [ ] ST-012.4: Create lock file directory management
- [ ] ST-012.5: Write integration tests with multiprocessing

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-012.1 | - | - |
| AC-012.2 | - | - |
| AC-012.3 | - | - |
| AC-012.4 | - | - |
| AC-012.5 | - | - |
| AC-012.6 | - | - |

---

## Implementation Notes

```python
# src/infrastructure/adapters/persistence/atomic_file_adapter.py
import fcntl
import os
import tempfile
from pathlib import Path


class AtomicFileAdapter:
    """Adapter for atomic file operations with locking."""

    def __init__(self, lock_dir: Path | None = None) -> None:
        self._lock_dir = lock_dir or Path(".jerry/local/locks")

    def _get_lock_path(self, path: Path) -> Path:
        """Get lock file path for a data file."""
        self._lock_dir.mkdir(parents=True, exist_ok=True)
        # Use hash of path to create unique lock file
        lock_name = f"{hash(str(path.absolute())) & 0xFFFFFFFF:08x}.lock"
        return self._lock_dir / lock_name

    def read_with_lock(self, path: Path) -> str:
        """Read file content with shared lock."""
        lock_path = self._get_lock_path(path)
        lock_path.touch(exist_ok=True)

        with open(lock_path, "r+") as lock_file:
            fcntl.lockf(lock_file.fileno(), fcntl.LOCK_SH)
            try:
                if path.exists():
                    return path.read_text()
                return ""
            finally:
                fcntl.lockf(lock_file.fileno(), fcntl.LOCK_UN)

    def write_atomic(self, path: Path, content: str) -> None:
        """Write content atomically with exclusive lock."""
        lock_path = self._get_lock_path(path)
        lock_path.touch(exist_ok=True)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(lock_path, "r+") as lock_file:
            fcntl.lockf(lock_file.fileno(), fcntl.LOCK_EX)
            try:
                fd, temp_path = tempfile.mkstemp(
                    dir=path.parent,
                    prefix=f".{path.name}.",
                    suffix=".tmp"
                )
                try:
                    with os.fdopen(fd, "w") as f:
                        f.write(content)
                        f.flush()
                        os.fsync(f.fileno())
                    os.replace(temp_path, path)
                except Exception:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                    raise
            finally:
                fcntl.lockf(lock_file.fileno(), fcntl.LOCK_UN)
```

---

## Progress Log

| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T11:00:00Z | Work item created | Claude |

---

## Dependencies

| Type | Work Item | Relationship |
|------|-----------|--------------|
| Depends On | WI-008 | Domain model design provides port interface |
| Blocks | WI-014 | Layered config needs atomic file adapter |
| Blocks | WI-015 | CLI integration needs file I/O |

---

## Related Artifacts

- **Research**: [PROJ-004-e-002](../research/PROJ-004-e-002-runtime-collision-avoidance.md)
- **Pattern**: [Persistence Adapter](../../../../.claude/patterns/adapter/persistence-adapter.md)
