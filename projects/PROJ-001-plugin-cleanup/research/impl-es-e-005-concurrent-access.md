# Research: Concurrent File Access for Event Stores

| Metadata | Value |
|----------|-------|
| **PS ID** | impl-es |
| **Entry ID** | e-005 |
| **Topic** | Concurrent File Access Patterns |
| **Author** | ps-researcher agent (v2.0.0) |
| **Date** | 2026-01-09 |
| **Status** | Complete |

---

## Executive Summary

This research explores concurrent file access patterns for filesystem-based event stores, examining file locking strategies, optimistic concurrency control, and atomic append operations. The findings provide actionable guidance for implementing a robust, cross-platform event store in Python.

---

## L0: Quick Reference (TL;DR)

### Recommended Approach

```python
# Production recommendation: filelock + version-based optimistic concurrency
from filelock import FileLock
import json
from pathlib import Path

class EventStore:
    def append_event(self, stream_id: str, event: dict, expected_version: int) -> None:
        lock_path = self.base_path / f"{stream_id}.lock"
        stream_path = self.base_path / f"{stream_id}.jsonl"

        with FileLock(lock_path):
            current_version = self._get_current_version(stream_path)
            if current_version != expected_version:
                raise ConcurrencyConflictError(
                    f"Expected version {expected_version}, found {current_version}"
                )

            # Atomic append with fsync
            with open(stream_path, 'a') as f:
                event['version'] = current_version + 1
                f.write(json.dumps(event) + '\n')
                f.flush()
                os.fsync(f.fileno())
```

### Key Decisions

| Aspect | Recommendation | Rationale |
|--------|---------------|-----------|
| Locking Library | `filelock` | Cross-platform, actively maintained |
| Lock Type | Separate `.lock` files | Don't lock the data file directly |
| Concurrency Model | Optimistic with versioning | Scales better, detects conflicts |
| Retry Strategy | Exponential backoff + jitter | Prevents thundering herd |
| Durability | fsync after write | Ensures persistence to disk |

---

## L1: Detailed Analysis

### 1. File Locking Strategies

#### 1.1 Python fcntl (POSIX Only)

The `fcntl` module provides POSIX file locking through `flock()` and `lockf()` functions.

**Key Characteristics:**
- `flock()` locks entire files, supports shared (LOCK_SH) and exclusive (LOCK_EX) locks
- `lockf()` is the recommended wrapper around fcntl() locking calls
- Advisory locks by default (processes can ignore them)
- Python 3.14+ releases GIL during system calls and auto-retries EINTR

**Lock Types:**
```python
import fcntl

# Shared lock (multiple readers)
fcntl.flock(fd, fcntl.LOCK_SH)

# Exclusive lock (single writer)
fcntl.flock(fd, fcntl.LOCK_EX)

# Non-blocking (returns immediately if can't acquire)
fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

# Unlock
fcntl.flock(fd, fcntl.LOCK_UN)
```

**Caveats:**
- Advisory locks require all processes to cooperate
- Mandatory locking requires `mount -o mand` (not recommended)
- Not portable to Windows

**Source:** [Python fcntl documentation](https://docs.python.org/3/library/fcntl.html)

#### 1.2 Cross-Platform Libraries

##### filelock (Recommended)

```python
from filelock import FileLock, Timeout

lock = FileLock("myfile.lock", timeout=10)

with lock:
    # Protected section
    pass
```

**Key Features:**
- Platform independent (uses native OS locking)
- `FileLock` for platform-specific, `SoftFileLock` for existence-based
- Recommended: Create separate `.lock` file, don't lock the data file

**Best Practice:**
> "Don't use a FileLock to lock the file you want to write to, instead create a separate .lock file. A FileLock is used to indicate another process of your application that a resource or working directory is currently used."

**Source:** [filelock documentation](https://py-filelock.readthedocs.io/)

##### portalocker

```python
import portalocker

with portalocker.Lock('file.txt', 'r+', timeout=120) as f:
    f.write('protected content')
```

**Key Features:**
- Works on Windows, Linux, BSD, Unix
- Supports distributed locking via Redis
- Provides `BoundedSemaphore` for cross-process semaphores
- Python 3.9+ only (as of 2025)

**Source:** [portalocker GitHub](https://github.com/wolph/portalocker)

#### 1.3 Advisory vs. Mandatory Locks

| Aspect | Advisory Locks | Mandatory Locks |
|--------|---------------|-----------------|
| Enforcement | Cooperative (honor system) | Kernel enforced |
| Performance | Better | Worse |
| Portability | Standard POSIX | Linux-specific, mount flags |
| Recommendation | **Preferred** | Avoid |

**Rationale for Advisory Locks:**
- All event store processes are controlled by the same application
- Mandatory locks have significant overhead
- Better portability across systems

---

### 2. Optimistic Concurrency Control

#### 2.1 Version-Based Conflict Detection

The standard pattern for event stores uses stream version numbers:

```python
class OptimisticEventStore:
    def append(self, stream_id: str, events: list[dict], expected_version: int) -> int:
        with self._get_lock(stream_id):
            current_version = self._read_version(stream_id)

            # Optimistic concurrency check
            if current_version != expected_version:
                raise ConcurrencyConflictError(
                    stream_id=stream_id,
                    expected=expected_version,
                    actual=current_version
                )

            # Append events with sequential versions
            new_version = current_version
            for event in events:
                new_version += 1
                event['stream_version'] = new_version
                self._append_event(stream_id, event)

            return new_version
```

**How it Works:**
1. Client reads current version when loading aggregate
2. Client passes expected version with commit request
3. Server compares expected vs. current version
4. If match: proceed; if mismatch: reject

**Benefits:**
- No long-held locks during business logic processing
- Conflicts detected at commit time
- Scales well with low contention workloads

**Source:** [Event-Driven.io - Optimistic Concurrency](https://event-driven.io/en/optimistic_concurrency_for_pessimistic_times/)

#### 2.2 Conflict Resolution Strategies

When a conflict occurs, applications have options:

| Strategy | When to Use |
|----------|-------------|
| **Fail Fast** | When conflict indicates business logic error |
| **Retry with Reload** | Idempotent operations, low contention |
| **Merge** | Commutative operations (counters, sets) |
| **User Resolution** | Interactive applications |

**Retry Implementation:**

```python
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=0.1, max=2.0),
    retry=retry_if_exception_type(ConcurrencyConflictError)
)
def execute_command(aggregate_id: str, command: Command) -> list[Event]:
    # Load aggregate (gets current version)
    aggregate = repository.load(aggregate_id)

    # Execute business logic
    events = aggregate.handle(command)

    # Attempt to save (may raise ConcurrencyConflictError)
    repository.save(aggregate, events)

    return events
```

**Source:** [Python eventsourcing documentation](https://eventsourcing.readthedocs.io/)

#### 2.3 Compare-and-Swap Pattern

While CAS is typically a hardware instruction, the concept applies to event stores:

```python
def compare_and_append(stream_id: str, event: dict, expected_version: int) -> bool:
    """
    Atomic compare-and-append operation.
    Returns True if successful, False if version mismatch.
    """
    lock_path = f"{stream_id}.lock"

    with FileLock(lock_path):
        current = read_stream_metadata(stream_id)

        # Compare
        if current.version != expected_version:
            return False

        # Swap (append new event)
        append_event(stream_id, event, current.version + 1)
        return True
```

**Handling the ABA Problem:**
In event stores, the ABA problem is naturally avoided because:
- Versions are monotonically increasing
- Events are immutable and append-only
- No "swap back" is possible

**Source:** [Wikipedia - Compare-and-swap](https://en.wikipedia.org/wiki/Compare-and-swap)

---

### 3. Event Append Patterns

#### 3.1 Atomic Append Operations

POSIX guarantees atomic appends up to certain limits:

| Platform | Max Atomic Append Size |
|----------|----------------------|
| Linux | 4KB (tested reliable) |
| Windows (Cygwin) | 1KB |
| Cross-platform safe | 1KB |

**Implementation:**

```python
import os

def atomic_append(path: str, data: bytes) -> None:
    """Append data atomically (within size limits)."""
    # O_APPEND ensures atomic positioning
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT)
    try:
        os.write(fd, data)
        os.fsync(fd)  # Durability guarantee
    finally:
        os.close(fd)
```

**Caveats:**
- Python's file buffering can interfere (use `buffering=0` or `os.open`)
- For larger events, use file locking instead of relying on atomic appends

**Source:** [Not The Wizard - Are File Appends Really Atomic?](https://www.notthewizard.com/2014/06/17/are-files-appends-really-atomic/)

#### 3.2 Write-Replace Pattern (Full Rewrites)

For small streams or when atomic append isn't sufficient:

```python
from atomicwrites import atomic_write
import os

def safe_stream_update(path: str, events: list[dict]) -> None:
    """Write entire stream atomically using temp file + rename."""
    with atomic_write(path, overwrite=True) as f:
        for event in events:
            f.write(json.dumps(event) + '\n')

    # fsync the directory for full durability
    dir_fd = os.open(os.path.dirname(path), os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)
```

**How atomicwrites Works:**
1. Write to temporary file in same directory
2. fsync the temporary file
3. Atomic rename (POSIX) or MoveFileEx (Windows)
4. fsync the directory

**Source:** [atomicwrites documentation](https://python-atomicwrites.readthedocs.io/)

#### 3.3 Write-Ahead Logging (WAL)

WAL provides durability by logging changes before applying them:

```python
class WALEventStore:
    def __init__(self, wal_path: str, data_path: str):
        self.wal_path = wal_path
        self.data_path = data_path

    def append(self, stream_id: str, event: dict) -> None:
        # 1. Write to WAL first
        wal_entry = {
            'stream_id': stream_id,
            'event': event,
            'timestamp': time.time()
        }
        self._append_to_wal(wal_entry)

        # 2. Apply to main store
        self._append_to_stream(stream_id, event)

        # 3. Mark WAL entry as applied (or truncate periodically)

    def recover(self) -> None:
        """Replay unapplied WAL entries after crash."""
        for entry in self._read_wal():
            if not self._is_applied(entry):
                self._append_to_stream(entry['stream_id'], entry['event'])
```

**WAL vs. Event Sourcing:**
- WAL: Temporary, purged after changes applied (command sourcing)
- Event Store: Permanent record of facts (event sourcing)

**Source:** [Wikipedia - Write-ahead logging](https://en.wikipedia.org/wiki/Write-ahead_logging)

#### 3.4 fsync and Durability

Proper durability requires both file and directory sync:

```python
def durable_write(path: str, content: str) -> None:
    """Write with full durability guarantee."""
    # Write and sync file
    with open(path, 'w') as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())

    # Sync directory (for rename/create durability)
    dir_path = os.path.dirname(path) or '.'
    dir_fd = os.open(dir_path, os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)
```

**Why Directory fsync?**
> "If the application needs a guarantee that the new version of the file will be present after a crash, it's necessary to fsync the containing directory."

**Caveats:**
- fsync doesn't guarantee disk controller behavior
- Some filesystems (ext3/4 with certain options) may still lose data
- macOS requires `fcntl(F_FULLFSYNC)` for true durability

**Source:** [Gocept - Reliable file updates with Python](https://blog.gocept.com/2013/07/15/reliable-file-updates-with-python/)

---

### 4. Retry Strategies

#### 4.1 Exponential Backoff with Jitter

Essential for preventing thundering herd in concurrent systems:

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential_jitter,
    retry_if_exception_type
)

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential_jitter(
        initial=0.1,  # Start at 100ms
        max=10.0,     # Cap at 10 seconds
        jitter=1.0    # Add up to 1s random jitter
    ),
    retry=retry_if_exception_type(ConcurrencyConflictError)
)
def save_with_retry(stream_id: str, events: list, expected_version: int):
    return event_store.append(stream_id, events, expected_version)
```

**Full Jitter Formula:**
```
sleep_time = random(0, min(cap, base * 2^attempt))
```

**Why Jitter?**
> "When multiple processes are in contention for a shared resource, exponentially increasing jitter helps minimize collisions."

**Source:** [Tenacity documentation](https://tenacity.readthedocs.io/)

#### 4.2 Retry Libraries Comparison

| Library | Features | Use Case |
|---------|----------|----------|
| **tenacity** | Full-featured, async support | Production systems |
| **backoff** | Lightweight, AWS-style jitter | Simple retry needs |
| **urllib3.Retry** | HTTP-specific | Network requests |

---

## L2: Implementation Recommendations

### Complete Event Store Implementation

```python
"""
Concurrent-safe filesystem event store implementation.
Combines file locking, optimistic concurrency, and retry strategies.
"""
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from filelock import FileLock, Timeout
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential_jitter,
    retry_if_exception_type
)


@dataclass(frozen=True)
class StreamVersion:
    """Immutable stream version information."""
    version: int
    last_modified: float


class ConcurrencyConflictError(Exception):
    """Raised when optimistic concurrency check fails."""
    def __init__(self, stream_id: str, expected: int, actual: int):
        self.stream_id = stream_id
        self.expected_version = expected
        self.actual_version = actual
        super().__init__(
            f"Concurrency conflict on stream '{stream_id}': "
            f"expected version {expected}, found {actual}"
        )


class FileSystemEventStore:
    """
    Thread-safe, process-safe event store using filesystem.

    Features:
    - Optimistic concurrency with version checking
    - File-based locking for process safety
    - fsync for durability
    - Retry with exponential backoff
    """

    def __init__(self, base_path: Path, lock_timeout: float = 30.0):
        self.base_path = Path(base_path)
        self.lock_timeout = lock_timeout
        self.base_path.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for organization
        self.streams_path = self.base_path / "streams"
        self.locks_path = self.base_path / "locks"
        self.streams_path.mkdir(exist_ok=True)
        self.locks_path.mkdir(exist_ok=True)

    def _stream_path(self, stream_id: str) -> Path:
        """Get path to stream file."""
        return self.streams_path / f"{stream_id}.jsonl"

    def _lock_path(self, stream_id: str) -> Path:
        """Get path to lock file (separate from data)."""
        return self.locks_path / f"{stream_id}.lock"

    def _get_lock(self, stream_id: str) -> FileLock:
        """Get lock object for stream."""
        return FileLock(self._lock_path(stream_id), timeout=self.lock_timeout)

    def get_version(self, stream_id: str) -> StreamVersion:
        """Get current version of a stream."""
        stream_path = self._stream_path(stream_id)

        if not stream_path.exists():
            return StreamVersion(version=0, last_modified=0)

        version = 0
        with open(stream_path, 'r') as f:
            for line in f:
                if line.strip():
                    event = json.loads(line)
                    version = event.get('stream_version', version + 1)

        return StreamVersion(
            version=version,
            last_modified=stream_path.stat().st_mtime
        )

    def read_stream(self, stream_id: str, from_version: int = 0) -> Iterator[dict]:
        """Read events from stream, optionally from a specific version."""
        stream_path = self._stream_path(stream_id)

        if not stream_path.exists():
            return

        with open(stream_path, 'r') as f:
            for line in f:
                if line.strip():
                    event = json.loads(line)
                    if event.get('stream_version', 0) > from_version:
                        yield event

    def append(
        self,
        stream_id: str,
        events: list[dict],
        expected_version: int
    ) -> int:
        """
        Append events to stream with optimistic concurrency check.

        Args:
            stream_id: Unique identifier for the event stream
            events: List of events to append
            expected_version: Expected current version (for concurrency check)

        Returns:
            New version number after append

        Raises:
            ConcurrencyConflictError: If expected_version doesn't match current
            Timeout: If lock cannot be acquired
        """
        with self._get_lock(stream_id):
            current = self.get_version(stream_id)

            # Optimistic concurrency check
            if current.version != expected_version:
                raise ConcurrencyConflictError(
                    stream_id=stream_id,
                    expected=expected_version,
                    actual=current.version
                )

            # Append events with versioning
            stream_path = self._stream_path(stream_id)
            new_version = current.version

            with open(stream_path, 'a') as f:
                for event in events:
                    new_version += 1
                    event['stream_version'] = new_version
                    event['timestamp'] = time.time()
                    f.write(json.dumps(event) + '\n')

                # Ensure durability
                f.flush()
                os.fsync(f.fileno())

            return new_version

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential_jitter(initial=0.1, max=2.0),
        retry=retry_if_exception_type(ConcurrencyConflictError)
    )
    def append_with_retry(
        self,
        stream_id: str,
        events: list[dict],
        expected_version: int
    ) -> int:
        """
        Append with automatic retry on concurrency conflicts.

        Uses exponential backoff with jitter to prevent thundering herd.
        """
        return self.append(stream_id, events, expected_version)


# Usage example
if __name__ == "__main__":
    store = FileSystemEventStore(Path("./event_store"))

    # Initial append (version 0 = empty stream)
    events = [
        {"type": "UserCreated", "data": {"name": "Alice"}},
        {"type": "EmailVerified", "data": {"email": "alice@example.com"}}
    ]
    new_version = store.append("user-123", events, expected_version=0)
    print(f"Appended 2 events, new version: {new_version}")

    # Read back
    for event in store.read_stream("user-123"):
        print(f"  Event: {event['type']} (v{event['stream_version']})")
```

---

## Quality Checklist (P-001, P-004)

### Source Citations

1. **File Locking:**
   - [Python fcntl documentation](https://docs.python.org/3/library/fcntl.html)
   - [filelock documentation](https://py-filelock.readthedocs.io/)
   - [portalocker GitHub](https://github.com/wolph/portalocker)
   - [GeeksforGeeks - File Locking in Python](https://www.geeksforgeeks.org/python/file-locking-in-python/)

2. **Optimistic Concurrency:**
   - [Event-Driven.io - Optimistic Concurrency](https://event-driven.io/en/optimistic_concurrency_for_pessimistic_times/)
   - [Python eventsourcing library](https://eventsourcing.readthedocs.io/)
   - [Jef Claes - Event Store with Optimistic Concurrency](https://jefclaes.be/2013/11/an-event-store-with-optimistic.html)

3. **Atomic Operations:**
   - [atomicwrites documentation](https://python-atomicwrites.readthedocs.io/)
   - [Not The Wizard - Are File Appends Really Atomic?](https://www.notthewizard.com/2014/06/17/are-files-appends-really-atomic/)
   - [Gocept - Reliable file updates with Python](https://blog.gocept.com/2013/07/15/reliable-file-updates-with-python/)

4. **Write-Ahead Logging:**
   - [Wikipedia - Write-ahead logging](https://en.wikipedia.org/wiki/Write-ahead_logging)
   - [GitHub - lrwx00t/wal](https://github.com/lrwx00t/wal)

5. **Retry Strategies:**
   - [Tenacity documentation](https://tenacity.readthedocs.io/)
   - [backoff PyPI](https://pypi.org/project/backoff/)

6. **Durability:**
   - [LWN.net - Atomicity vs durability](https://lwn.net/Articles/323360/)
   - [Everything about fsync](https://blog.httrack.com/blog/2013/11/15/everything-you-always-wanted-to-know-about-fsync/)

### Reasoning Documented (P-004)

This research was conducted to inform the implementation of a filesystem-based event store for the Jerry framework. The recommendations prioritize:

1. **Cross-platform compatibility** - Using `filelock` over `fcntl` for Windows support
2. **Correctness over performance** - Using optimistic concurrency with explicit version checking
3. **Durability guarantees** - Proper use of fsync for crash recovery
4. **Production readiness** - Including retry strategies for high-contention scenarios

---

## Related Documents

- `impl-es-infrastructure-5W1H.md` - Infrastructure layer design
- `PROJ-001-e-003-revised-architecture-foundation.md` - Architecture context
- `dev-skill-e-005-concurrent-access.md` - Earlier concurrent access research

---

*Document generated by ps-researcher agent (v2.0.0) per P-002 persistence mandate.*
