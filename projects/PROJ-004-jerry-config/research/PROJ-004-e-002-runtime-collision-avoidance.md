# Runtime Collision Avoidance Patterns

| Attribute | Value |
|-----------|-------|
| **Document ID** | PROJ-004-e-002 |
| **Type** | Research Artifact |
| **Topic** | File Locking and Atomic Write Patterns |
| **Author** | ps-researcher (v2.0.0) |
| **Created** | 2026-01-12 |
| **Status** | Complete |

---

## L0: Executive Summary (ELI5)

When multiple processes try to read or write the same configuration file simultaneously, data corruption can occur. This research examines two complementary strategies: **file locking** (coordinating access so only one process writes at a time) and **atomic writes** (writing to a temporary file first, then renaming it to replace the original). Python's standard library provides sufficient tools for this on Unix systems, but cross-platform support requires third-party libraries like `filelock` or `portalocker`.

---

## L1: Technical Findings (Software Engineer)

### 1. Python Standard Library Mechanisms

#### 1.1 fcntl Module (Unix Only)

The `fcntl` module provides two primary locking functions:

**`fcntl.flock(fd, operation)`** - BSD-style whole-file locking:

```python
import fcntl
from contextlib import contextmanager
from pathlib import Path

@contextmanager
def file_lock(file_path: Path, exclusive: bool = True):
    """Context manager for file locking using flock.

    Args:
        file_path: Path to the file to lock.
        exclusive: If True, acquire exclusive lock; otherwise shared.

    Yields:
        The opened file handle.
    """
    lock_flag = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH

    with open(file_path, "r+") as f:
        try:
            fcntl.flock(f.fileno(), lock_flag)
            yield f
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
```

**`fcntl.lockf(fd, cmd, ...)`** - POSIX-style byte-range locking:

```python
import fcntl

def lock_file_region(fd: int, start: int, length: int) -> None:
    """Lock a specific region of a file.

    Args:
        fd: File descriptor.
        start: Byte offset to start lock.
        length: Number of bytes to lock (0 = to EOF).
    """
    fcntl.lockf(fd, fcntl.LOCK_EX, length, start)
```

**Key Differences:**

| Feature | `flock()` | `lockf()` |
|---------|-----------|-----------|
| Origin | BSD | POSIX (wraps `fcntl()`) |
| Granularity | Whole file | Byte range |
| Fork behavior | Lock shared with child | Lock NOT inherited |
| NFS support | Local only (pre-2.6.12) | Works over NFS |
| Portability | Not POSIX standard | POSIX compliant |

**Recommendation:** Use `fcntl.lockf()` for POSIX compliance and NFS compatibility.

#### 1.2 msvcrt Module (Windows Only)

```python
import msvcrt

def lock_file_windows(fd: int, length: int) -> None:
    """Lock file on Windows.

    Args:
        fd: File descriptor.
        length: Number of bytes to lock.
    """
    msvcrt.locking(fd, msvcrt.LK_NBLCK, length)

def unlock_file_windows(fd: int, length: int) -> None:
    """Unlock file on Windows."""
    msvcrt.locking(fd, msvcrt.LK_UNLCK, length)
```

#### 1.3 Atomic Write Pattern (stdlib)

The atomic write pattern prevents data corruption during writes:

```python
import os
import tempfile
from pathlib import Path

def atomic_write(file_path: Path, content: str) -> None:
    """Atomically write content to a file.

    Pattern: Write to temp file, fsync, rename to target.
    Ensures file is either fully written or unchanged.

    Args:
        file_path: Target file path.
        content: Content to write.
    """
    parent_dir = file_path.parent
    parent_dir.mkdir(parents=True, exist_ok=True)

    # Create temp file in SAME directory (critical for atomicity)
    fd, temp_path = tempfile.mkstemp(
        dir=parent_dir,
        prefix=f".{file_path.name}.",
        suffix=".tmp"
    )

    try:
        with os.fdopen(fd, "w") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())  # Ensure data is on disk

        # Atomic rename (works within same filesystem)
        os.replace(temp_path, file_path)

        # Sync directory metadata
        dir_fd = os.open(parent_dir, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)

    except Exception:
        # Clean up temp file on failure
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise
```

**Why `os.replace()` over `os.rename()`:**
- `os.replace()` is atomic and overwrites existing files
- Works cross-platform (Python 3.3+)
- `os.rename()` may fail on Windows if destination exists

#### 1.4 Lock File Pattern (stdlib)

Using a separate `.lock` file for coordination:

```python
import os
from pathlib import Path
from contextlib import contextmanager

@contextmanager
def lock_file_exclusive(target_path: Path):
    """Acquire exclusive lock using a separate lock file.

    Uses atomic file creation (mode 'x') for cross-platform safety.

    Args:
        target_path: The file we want to protect.

    Yields:
        None when lock is acquired.
    """
    lock_path = target_path.with_suffix(target_path.suffix + ".lock")

    # Attempt atomic creation
    while True:
        try:
            # 'x' mode: create exclusively, fail if exists
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            break
        except FileExistsError:
            # Lock held by another process - implement backoff
            import time
            time.sleep(0.1)

    try:
        yield
    finally:
        os.unlink(lock_path)
```

### 2. Third-Party Libraries

#### 2.1 filelock (Recommended for Simplicity)

**Repository:** [tox-dev/filelock](https://github.com/tox-dev/filelock)
**PyPI:** https://pypi.org/project/filelock/
**Latest Version:** 3.20.3 (January 2026)

```python
from filelock import FileLock, Timeout

lock = FileLock("config.json.lock", timeout=10)

# Context manager usage (recommended)
with lock:
    # Critical section - only one process at a time
    with open("config.json", "r+") as f:
        config = json.load(f)
        config["updated"] = True
        f.seek(0)
        json.dump(config, f)
        f.truncate()

# Non-blocking check
try:
    with lock.acquire(timeout=0):
        # Got the lock immediately
        pass
except Timeout:
    print("Lock is held by another process")
```

**Key Features:**
- Platform-independent (uses `UnixFileLock` or `WindowsFileLock` automatically)
- Uses advisory locks (like all file locking)
- Thread-local by default (configurable via `thread_local=False`)
- Does NOT support asyncio

**Critical Design Note:** Do NOT lock the data file directly. Always use a separate `.lock` file:

```python
# CORRECT: Use separate lock file
lock = FileLock("config.json.lock")

# INCORRECT: Lock the data file itself
lock = FileLock("config.json")  # May cause issues!
```

#### 2.2 portalocker (Feature-Rich)

**Repository:** [wolph/portalocker](https://github.com/wolph/portalocker)
**Documentation:** https://portalocker.readthedocs.io/

```python
import portalocker

# Simple exclusive lock
with portalocker.Lock("config.json", "r+", timeout=10) as f:
    config = json.load(f)
    # ... modify config ...
    f.seek(0)
    json.dump(config, f)
    f.truncate()

# Bounded semaphore (for limiting concurrent access)
from portalocker import BoundedSemaphore

semaphore = BoundedSemaphore(3, name="config-access")
with semaphore:
    # Up to 3 processes can enter this section
    pass
```

**Key Features:**
- Cross-platform (Windows, Linux, BSD, Unix)
- Redis-based distributed locking
- Bounded semaphore support
- Advisory locks (mandatory locking requires mount options)

#### 2.3 fasteners (Reader-Writer Locks)

**Repository:** [harlowja/fasteners](https://github.com/harlowja/fasteners)
**Documentation:** https://fasteners.readthedocs.io/

```python
from fasteners import InterProcessLock, ReaderWriterLock

# Inter-process lock
lock = InterProcessLock("/tmp/config.lock")

with lock:
    # Exclusive access
    pass

# Reader-writer lock (multiple readers OR single writer)
rw_lock = ReaderWriterLock()

with rw_lock.read_lock():
    # Multiple processes can hold read lock
    pass

with rw_lock.write_lock():
    # Exclusive write access
    pass
```

**Key Features:**
- Reader-writer locks for threads AND processes
- Uses `fcntl` on Unix, `msvcrt._locking` on Windows
- Works between independently launched processes

#### 2.4 Library Comparison

| Feature | filelock | portalocker | fasteners |
|---------|----------|-------------|-----------|
| **Simplicity** | High | Medium | Medium |
| **Cross-platform** | Yes | Yes | Yes |
| **Reader-Writer** | No | No | Yes |
| **Distributed (Redis)** | No | Yes | No |
| **Semaphores** | No | Yes | No |
| **Dependencies** | None | None | None |
| **Asyncio** | No | No | No |
| **Thread-local** | Configurable | N/A | N/A |

### 3. Process Crash and Stale Lock Handling

#### 3.1 How Locks Behave on Process Death

| Mechanism | Behavior on Crash |
|-----------|-------------------|
| `fcntl.flock()` | **Auto-released** - OS releases when file descriptor closes |
| `fcntl.lockf()` | **Auto-released** - OS releases when process terminates |
| Lock files (`O_EXCL`) | **Stale lock** - File persists, requires cleanup |
| `filelock` | **Auto-released** - Uses OS mechanisms |
| `portalocker` | **Auto-released** - Uses OS mechanisms |

#### 3.2 Stale Lock Detection Pattern

For lock file approaches where the lock persists after crash:

```python
import os
import time
from pathlib import Path

def is_lock_stale(lock_path: Path, max_age_seconds: float = 60) -> bool:
    """Check if a lock file is stale (orphaned).

    Args:
        lock_path: Path to the lock file.
        max_age_seconds: Maximum age before considering stale.

    Returns:
        True if lock appears stale.
    """
    if not lock_path.exists():
        return False

    try:
        # Check if PID in lock file is still running
        with open(lock_path) as f:
            pid = int(f.read().strip())

        # Check if process exists
        try:
            os.kill(pid, 0)  # Signal 0 = check existence
            # Process exists - check age as fallback
            lock_age = time.time() - lock_path.stat().st_mtime
            return lock_age > max_age_seconds
        except OSError:
            # Process doesn't exist - lock is stale
            return True

    except (ValueError, IOError):
        # Can't read lock file - assume stale
        return True


def acquire_with_stale_detection(
    lock_path: Path,
    max_age: float = 60,
    timeout: float = 10,
) -> bool:
    """Acquire lock with stale lock detection.

    Args:
        lock_path: Path to lock file.
        max_age: Max lock age before considering stale.
        timeout: Time to wait for lock.

    Returns:
        True if lock acquired.
    """
    start = time.time()

    while (time.time() - start) < timeout:
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            return True
        except FileExistsError:
            if is_lock_stale(lock_path, max_age):
                # Remove stale lock and retry
                try:
                    os.unlink(lock_path)
                except OSError:
                    pass
            else:
                time.sleep(0.1)

    return False
```

### 4. Cross-Platform Considerations

| Aspect | macOS | Linux | Windows |
|--------|-------|-------|---------|
| **fcntl available** | Yes | Yes | No |
| **msvcrt available** | No | No | Yes |
| **Lock type** | Advisory | Advisory | Advisory |
| **Mandatory locking** | No | Via mount option | No |
| **NFS locking** | Limited | Yes (2.6.12+) | N/A |
| **os.replace atomicity** | Yes | Yes | Yes |

#### Platform-Agnostic Implementation

```python
import os
import sys
from contextlib import contextmanager
from pathlib import Path

if sys.platform == "win32":
    import msvcrt

    @contextmanager
    def platform_file_lock(file_path: Path):
        """Windows file locking."""
        with open(file_path, "r+b") as f:
            try:
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                yield f
            finally:
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)

else:
    import fcntl

    @contextmanager
    def platform_file_lock(file_path: Path):
        """Unix file locking using lockf."""
        with open(file_path, "r+") as f:
            try:
                fcntl.lockf(f.fileno(), fcntl.LOCK_EX)
                yield f
            finally:
                fcntl.lockf(f.fileno(), fcntl.LOCK_UN)
```

### 5. Combined Pattern: Lock + Atomic Write

The safest approach combines locking with atomic writes:

```python
import fcntl
import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any

@contextmanager
def safe_config_update(config_path: Path):
    """Context manager for safe, concurrent config file updates.

    Combines:
    1. File locking (prevents concurrent access)
    2. Atomic writes (prevents corruption)

    Usage:
        with safe_config_update(Path("config.json")) as update:
            config = update.read()
            config["key"] = "value"
            update.write(config)
    """
    lock_path = config_path.with_suffix(config_path.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    # Create lock file if it doesn't exist
    lock_path.touch(exist_ok=True)

    with open(lock_path, "r+") as lock_file:
        # Acquire exclusive lock
        fcntl.lockf(lock_file.fileno(), fcntl.LOCK_EX)

        try:
            yield ConfigUpdater(config_path)
        finally:
            # Release lock
            fcntl.lockf(lock_file.fileno(), fcntl.LOCK_UN)


class ConfigUpdater:
    """Helper class for reading and atomically writing config."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def read(self) -> dict[str, Any]:
        """Read current config."""
        if self._path.exists():
            with open(self._path) as f:
                return json.load(f)
        return {}

    def write(self, config: dict[str, Any]) -> None:
        """Atomically write config."""
        content = json.dumps(config, indent=2)

        fd, temp_path = tempfile.mkstemp(
            dir=self._path.parent,
            prefix=f".{self._path.name}.",
            suffix=".tmp"
        )

        try:
            with os.fdopen(fd, "w") as f:
                f.write(content)
                f.flush()
                os.fsync(f.fileno())

            os.replace(temp_path, self._path)
        except Exception:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise
```

---

## L2: Strategic Recommendation (Principal Architect)

### Recommended Approach for Jerry

Given Jerry's constraints:
- **Domain layer must be zero-dependency** (stdlib only)
- **Infrastructure adapters may use external libraries**
- **Must work on macOS and Linux** (Windows nice-to-have)

#### Architecture Decision

```
                    +-----------------------+
                    |   Domain Layer        |
                    |   (Zero Dependencies) |
                    +-----------------------+
                              |
                              | Port Interface
                              v
                    +-----------------------+
                    | IConfigRepository     |
                    | (Protocol)            |
                    +-----------------------+
                              ^
                              |
         +--------------------+--------------------+
         |                    |                    |
    +----------+        +----------+        +----------+
    | Stdlib   |        | Filelock |        | In-Memory|
    | Adapter  |        | Adapter  |        | Adapter  |
    | (fcntl)  |        | (library)|        | (tests)  |
    +----------+        +----------+        +----------+
```

#### Option 1: Stdlib-Only (Recommended for Phase 1)

**Use `fcntl.lockf()` + atomic writes in infrastructure adapter.**

**Pros:**
- Zero dependencies
- Works on macOS and Linux
- Sufficient for single-machine scenarios

**Cons:**
- No Windows support
- Must implement stale lock detection manually

**Implementation Location:**
```
src/infrastructure/adapters/persistence/
    atomic_file_adapter.py      # Atomic write implementation
    locking_config_adapter.py   # fcntl-based locking
```

#### Option 2: Filelock Library (Recommended for Phase 2)

**Add `filelock` as infrastructure dependency.**

**Pros:**
- Cross-platform (Windows support)
- Well-maintained (tox-dev organization)
- Simple API
- No additional dependencies

**Cons:**
- External dependency (but infrastructure layer allows this)

**Implementation:**
```python
# src/infrastructure/adapters/persistence/filelock_config_adapter.py
from filelock import FileLock

class FilelockConfigAdapter(IConfigRepository):
    def __init__(self, config_path: Path) -> None:
        self._path = config_path
        self._lock = FileLock(config_path.with_suffix(".lock"))
```

### Recommendation Summary

| Phase | Approach | Platform Support |
|-------|----------|------------------|
| **Phase 1** | stdlib (`fcntl.lockf` + atomic write) | macOS, Linux |
| **Phase 2** | `filelock` library | macOS, Linux, Windows |

### Key Design Principles

1. **Always use separate lock files** - Never lock the data file directly
2. **Combine locking + atomic writes** - Belt and suspenders
3. **Use `os.replace()` not `os.rename()`** - Cross-platform atomicity
4. **Create temp files in same directory** - Ensures atomic rename works
5. **Include `fsync()` for durability** - Data on disk before rename
6. **Implement timeout + retry** - Handle contention gracefully

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Process crash while holding lock | Use OS-level locks (auto-released on crash) |
| Stale lock files | PID-based detection + age timeout |
| Incomplete writes | Atomic write pattern (temp + rename) |
| NFS race conditions | Avoid shared config on NFS; use local paths |

---

## References

### Primary Sources

- [Python fcntl Documentation](https://docs.python.org/3/library/fcntl.html)
- [filelock PyPI](https://pypi.org/project/filelock/)
- [portalocker GitHub](https://github.com/wolph/portalocker)
- [fasteners Documentation](https://fasteners.readthedocs.io/)

### Secondary Sources

- [Everything You Never Wanted to Know About File Locking](https://apenwarr.ca/log/20101213)
- [File Locking in Python - GeeksforGeeks](https://www.geeksforgeeks.org/python/file-locking-in-python/)
- [Atomic File Writes - Python Atomicwrites Docs](https://python-atomicwrites.readthedocs.io/)
- [What happens to a lock when the process is killed? - filelock Discussion](https://github.com/tox-dev/filelock/discussions/116)
- [Flock and fcntl on NFS](https://utcc.utoronto.ca/~cks/space/blog/linux/FlockFcntlAndNFS)

### Code Examples Reviewed

- [File locking using fcntl.flock - GitHub Gist](https://gist.github.com/jirihnidek/430d45c54311661b47fb45a3a7846537)
- [Simple Python file locking context manager - GitHub Gist](https://gist.github.com/lonetwin/7b4ccc93241958ff6967)
- [Safely and Atomically Write to a File - ActiveState](https://code.activestate.com/recipes/579097-safely-and-atomically-write-to-a-file/)
