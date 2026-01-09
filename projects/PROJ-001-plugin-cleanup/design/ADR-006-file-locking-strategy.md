# ADR-006: File Locking Strategy

**Status**: Proposed
**Date**: 2026-01-09
**Deciders**: Development Team
**Technical Story**: INIT-DEV-SKILL

---

## Context

The Jerry Framework's Work Tracker component requires concurrent file access from multiple Claude Code instances operating in parallel. This creates several challenges:

1. **Multiple Claude Code instances** may read and write the same work item files simultaneously
2. **Race conditions** can corrupt index files and work item JSON data
3. **Session state files** may be modified by overlapping operations
4. **ID generation** must produce unique identifiers without central coordination

### Research Findings (e-005)

The concurrent access research document (dev-skill-e-005-concurrent-access) identifies these key scenarios:

- **Index corruption**: Multiple instances modifying `.jerry/data/index.json` simultaneously
- **Partial writes**: Interrupted writes leaving files in inconsistent state
- **Lost updates**: Last-write-wins causing data loss when parallel writes overlap
- **ID collisions**: Sequential IDs requiring coordination; risk of duplicates

### Relevant Risks (from e-010)

| Risk ID | Description | Score | Mitigation Focus |
|---------|-------------|-------|------------------|
| R-005 | Snowflake ID worker collisions across instances | 3 (High Impact) | Derived worker ID strategy |
| R-006 | File lock contention under parallel agent load | 4 (Medium) | Per-file locking with backoff |
| R-009 | (Duplicate of R-005 in numbering) | - | - |

---

## Decision Drivers

1. **Multi-instance safety**: Multiple Claude Code instances must safely share filesystem
2. **Data integrity**: No partial writes or corruption permitted
3. **Performance**: Lock contention must not create unacceptable delays
4. **Simplicity**: Solution must work with file-based persistence (no external database)
5. **Cross-platform**: Must work on macOS, Linux, and Windows
6. **Coordination-free**: ID generation should not require central coordinator
7. **Crash recovery**: System must recover gracefully from interrupted operations

---

## Considered Options

### Option 1: Pessimistic Locking (filelock)

Acquire exclusive lock before any read-modify-write operation.

**Implementation**:
```python
from filelock import FileLock, Timeout

def update_work_item(filepath: str, updates: dict) -> None:
    lock = FileLock(f"{filepath}.lock", timeout=30)
    with lock:
        with open(filepath) as f:
            data = json.load(f)
        data.update(updates)
        with open(filepath, 'w') as f:
            json.dump(data, f)
```

**Pros**:
- Simple mental model
- Prevents all concurrent access conflicts
- Well-tested library (py-filelock)
- Cross-platform support

**Cons**:
- Reduces parallelism
- Risk of deadlock with multiple files
- Stale locks if process crashes
- Performance overhead on every operation

### Option 2: Optimistic Locking (version field)

Read with version, validate version unchanged before write.

**Implementation**:
```python
def optimistic_update(filepath: str, transform_fn, max_retries: int = 3):
    for attempt in range(max_retries):
        with open(filepath) as f:
            data = json.load(f)
        original_version = data.get("_version", 0)

        data = transform_fn(data)
        data["_version"] = original_version + 1

        # Brief lock for compare-and-swap
        with FileLock(f"{filepath}.lock", timeout=1):
            with open(filepath) as f:
                current = json.load(f)
            if current.get("_version", 0) != original_version:
                continue  # Retry
            atomic_write(filepath, json.dumps(data))
            return data
    raise ConflictError(f"Failed after {max_retries} retries")
```

**Pros**:
- Higher throughput for low-contention scenarios
- Readers never block
- Natural conflict detection

**Cons**:
- Wasted work on conflict
- Complex retry logic
- Starvation risk under high contention
- Requires version field in all files

### Option 3: Atomic Writes Only (no locking)

Rely solely on atomic rename operations without explicit locking.

**Implementation**:
```python
def atomic_write(filepath: str, content: str) -> None:
    dir_path = os.path.dirname(filepath) or '.'
    fd, tmp_path = tempfile.mkstemp(dir=dir_path, prefix='.tmp_')
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, filepath)
    except:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise
```

**Pros**:
- Maximum parallelism
- No lock contention
- Simple implementation

**Cons**:
- Does NOT prevent read-modify-write race conditions
- Last-write-wins semantics cause data loss
- Insufficient for Work Tracker use case

### Option 4: Hybrid Approach (Recommended)

Combine pessimistic locking for write operations with atomic writes for durability.

**Strategy**:
- **Write operations**: Pessimistic lock with timeout and backoff
- **Read operations**: No lock (eventual consistency acceptable)
- **Atomic writes**: Always use temp-file-rename pattern
- **ID generation**: Coordination-free Snowflake-style IDs

---

## Decision Outcome

**Chosen Option**: Option 4 (Hybrid Approach)

This decision balances data integrity with acceptable performance by:
1. Using pessimistic locking only for write operations (not reads)
2. Implementing atomic writes for crash safety
3. Using per-file granularity to maximize parallelism
4. Employing exponential backoff to handle contention gracefully
5. Generating coordination-free IDs via Snowflake pattern

### Rationale

From the research synthesis (e-007):

> "For Jerry's multi-instance scenarios, use the **temp-file-rename pattern** with **py-filelock** for critical operations, and **Snowflake-style IDs** for generating unique identifiers without coordination."

The hybrid approach directly implements this recommendation by:
- PAT-001-e005 (Atomic Write with Durability): Temp file + rename + fsync
- PAT-002-e005 (File-Based Mutual Exclusion): py-filelock with timeout
- PAT-004-e005 (Coordination-Free ID Generation): Snowflake with derived worker ID

### Consequences

**Positive**:
- Data integrity guaranteed for all write operations
- Crash recovery via atomic writes
- No external dependencies beyond py-filelock
- Scales to multiple parallel Claude Code instances
- Coordination-free ID generation enables horizontal scaling

**Negative**:
- Write operations serialized per file (intentional trade-off)
- Lock file cleanup needed for crashed processes
- Slight complexity increase over pure atomic writes
- 30-second timeout may cause delays under extreme contention

**Neutral**:
- Read operations remain lock-free (eventual consistency)
- Version field optional (only needed if optimistic concurrency desired later)

---

## Implementation

### Lock Granularity

**Decision**: Per-file locking (fine-grained)

| Granularity | Concurrency | Complexity | Deadlock Risk |
|-------------|-------------|------------|---------------|
| Per-directory | Low | Low | Low |
| Per-entity-type | Medium | Medium | Medium |
| **Per-file** | **High** | **Medium** | **Low** |

Per-file locking chosen because:
- Work items are independent; no cross-file transactions required
- Maximizes parallelism for multi-agent scenarios
- Lock files are cheap (empty files)

### Lock File Naming Convention

```
{original_file}.lock

Examples:
  .jerry/data/items/WORK-001.json       -> .jerry/data/items/WORK-001.json.lock
  .jerry/data/index.json                -> .jerry/data/index.json.lock
  sessions/session-12345.json           -> sessions/session-12345.json.lock
```

### Timeout Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Lock timeout | 30 seconds | Allows for slow disk I/O; prevents indefinite waiting |
| Max retries | 5 | Sufficient for transient contention |
| Initial backoff | 1 second | Quick first retry |
| Backoff multiplier | 2x | Exponential growth |
| Backoff jitter | 0-1 second | Prevents thundering herd |

**Maximum wait time**: 1 + 2 + 4 + 8 + 16 + jitter = ~32 seconds

### Retry Strategy

Exponential backoff with jitter:

```python
import time
import random
from filelock import FileLock, Timeout

def acquire_with_backoff(filepath: str, max_attempts: int = 5) -> FileLock:
    """Acquire file lock with exponential backoff."""
    lock = FileLock(f"{filepath}.lock", timeout=30)

    for attempt in range(max_attempts):
        try:
            lock.acquire(timeout=1)
            return lock
        except Timeout:
            if attempt < max_attempts - 1:
                # Exponential backoff with jitter
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)

    raise LockAcquisitionError(
        f"Failed to acquire lock for {filepath} after {max_attempts} attempts. "
        f"Another process may be holding the lock. Check for stale lock files."
    )
```

### Error Handling

#### Lock Acquisition Failure

```python
class LockAcquisitionError(Exception):
    """Raised when file lock cannot be acquired within timeout."""
    pass

def handle_lock_failure(filepath: str, error: LockAcquisitionError) -> None:
    """Handle lock acquisition failure."""
    # Log the failure with context
    logger.error(f"Lock acquisition failed: {error}")

    # Check for stale lock
    lock_path = f"{filepath}.lock"
    if os.path.exists(lock_path):
        lock_age = time.time() - os.path.getmtime(lock_path)
        if lock_age > 300:  # 5 minutes
            logger.warning(f"Stale lock detected ({lock_age:.0f}s old): {lock_path}")
            # Do NOT auto-remove; may still be valid

    # Raise for caller to handle
    raise
```

#### Stale Lock Cleanup

Stale locks occur when a process crashes while holding a lock. Strategy:

1. **Detection**: Lock file older than 5 minutes without modification
2. **Warning**: Log warning but do NOT auto-remove
3. **Manual cleanup**: Provide CLI command for administrators
4. **Prevention**: Use `atexit` handler to release locks on clean exit

```python
import atexit

# Registry of active locks for cleanup
_active_locks: list[FileLock] = []

def register_lock(lock: FileLock) -> None:
    _active_locks.append(lock)

def unregister_lock(lock: FileLock) -> None:
    if lock in _active_locks:
        _active_locks.remove(lock)

@atexit.register
def cleanup_locks():
    """Release all locks on process exit."""
    for lock in _active_locks:
        try:
            if lock.is_locked:
                lock.release()
        except Exception:
            pass  # Best effort
```

### Atomic Write Implementation

```python
import os
import tempfile
import json
from typing import Any

def atomic_write_json(filepath: str, data: Any, indent: int = 2) -> None:
    """Write JSON data atomically using temp file + rename pattern.

    Args:
        filepath: Target file path
        data: JSON-serializable data
        indent: JSON indentation (default 2 for readability)

    Raises:
        OSError: If write or rename fails
        TypeError: If data is not JSON-serializable

    Implementation follows PAT-001-e005 (Atomic Write with Durability):
    1. Write to temp file in same directory
    2. Flush and fsync for durability
    3. Atomic rename to target path
    4. fsync directory metadata (for new files)
    """
    dir_path = os.path.dirname(filepath) or '.'

    # Ensure directory exists
    os.makedirs(dir_path, exist_ok=True)

    # Create temp file in same directory (required for atomic rename)
    fd, tmp_path = tempfile.mkstemp(dir=dir_path, prefix='.tmp_', suffix='.json')

    try:
        # Write content with durability
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
            f.write('\n')  # Trailing newline
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename (POSIX guarantees atomicity on same filesystem)
        os.replace(tmp_path, filepath)

        # Sync directory metadata (for new files)
        try:
            dir_fd = os.open(dir_path, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        except OSError:
            pass  # O_DIRECTORY not supported on all platforms

    except Exception:
        # Clean up temp file on failure
        try:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        except OSError:
            pass
        raise
```

### ID Generation (Snowflake Pattern)

```python
import time
import os
import socket
import hashlib
from threading import Lock
from dataclasses import dataclass

@dataclass
class SnowflakeConfig:
    """Configuration for Snowflake ID generator."""
    epoch: int = 1704067200000  # 2024-01-01 00:00:00 UTC
    worker_bits: int = 10
    sequence_bits: int = 12

class SnowflakeGenerator:
    """Coordination-free unique ID generator.

    64-bit ID structure:
    - 1 bit: sign (always 0)
    - 41 bits: timestamp (milliseconds since epoch)
    - 10 bits: worker ID (0-1023)
    - 12 bits: sequence (0-4095 per millisecond)

    Implements PAT-004-e005 (Coordination-Free ID Generation).
    """

    def __init__(self, worker_id: int | None = None, config: SnowflakeConfig | None = None):
        self.config = config or SnowflakeConfig()
        self.worker_id = worker_id if worker_id is not None else self._derive_worker_id()
        self.sequence = 0
        self.last_timestamp = -1
        self._lock = Lock()

        max_worker = (1 << self.config.worker_bits) - 1
        if self.worker_id < 0 or self.worker_id > max_worker:
            raise ValueError(f"Worker ID must be 0-{max_worker}")

    def _derive_worker_id(self) -> int:
        """Derive worker ID from machine characteristics (no coordination needed).

        Combines hostname, PID, and MAC address to generate deterministic worker ID.
        """
        identity = f"{socket.gethostname()}-{os.getpid()}-{uuid.getnode()}"
        hash_bytes = hashlib.sha256(identity.encode()).digest()
        return int.from_bytes(hash_bytes[:2], 'big') & ((1 << self.config.worker_bits) - 1)

    def generate(self) -> int:
        """Generate a unique Snowflake ID."""
        max_sequence = (1 << self.config.sequence_bits) - 1

        with self._lock:
            timestamp = int(time.time() * 1000) - self.config.epoch

            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & max_sequence
                if self.sequence == 0:
                    # Wait for next millisecond
                    while timestamp <= self.last_timestamp:
                        timestamp = int(time.time() * 1000) - self.config.epoch
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            return (
                (timestamp << (self.config.worker_bits + self.config.sequence_bits)) |
                (self.worker_id << self.config.sequence_bits) |
                self.sequence
            )

    def generate_hex(self) -> str:
        """Generate ID as hexadecimal string."""
        return format(self.generate(), 'x')

    @staticmethod
    def parse(snowflake_id: int, config: SnowflakeConfig | None = None) -> dict:
        """Extract components from a Snowflake ID."""
        config = config or SnowflakeConfig()
        return {
            "timestamp_ms": (snowflake_id >> (config.worker_bits + config.sequence_bits)) + config.epoch,
            "worker_id": (snowflake_id >> config.sequence_bits) & ((1 << config.worker_bits) - 1),
            "sequence": snowflake_id & ((1 << config.sequence_bits) - 1)
        }
```

### Complete ConcurrentFileStore Implementation

```python
from contextlib import contextmanager
from filelock import FileLock, Timeout
from typing import Generator, Any
import json
import os

class ConcurrentFileStore:
    """Thread and multi-process safe file store.

    Implements hybrid locking strategy:
    - Pessimistic locking for writes (PAT-002-e005)
    - Atomic writes for durability (PAT-001-e005)
    - Coordination-free ID generation (PAT-004-e005)
    """

    def __init__(self, data_dir: str, lock_timeout: int = 30):
        self.data_dir = data_dir
        self.lock_timeout = lock_timeout
        self.id_generator = SnowflakeGenerator()
        os.makedirs(data_dir, exist_ok=True)

    @contextmanager
    def locked_read_write(self, filename: str) -> Generator[dict, None, None]:
        """Context manager for safe read-modify-write operations.

        Usage:
            with store.locked_read_write("items/WORK-001.json") as data:
                data["status"] = "completed"
                # Changes are automatically saved on context exit
        """
        filepath = os.path.join(self.data_dir, filename)
        lock = FileLock(f"{filepath}.lock", timeout=self.lock_timeout)

        with lock:
            # Read current data
            if os.path.exists(filepath):
                with open(filepath, encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {}

            # Yield for modification
            yield data

            # Write back atomically
            atomic_write_json(filepath, data)

    def read(self, filename: str) -> dict | None:
        """Read file without locking (eventual consistency).

        Safe for concurrent reads. May see stale data if write
        is in progress, but never partial/corrupt data.
        """
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            return None
        with open(filepath, encoding='utf-8') as f:
            return json.load(f)

    def create_unique(self, prefix: str, content: dict) -> str:
        """Create file with unique name (no collision possible).

        Uses Snowflake ID for coordination-free uniqueness.
        No lock needed because filename is guaranteed unique.
        """
        unique_id = self.id_generator.generate_hex()
        filename = f"{prefix}_{unique_id}.json"
        filepath = os.path.join(self.data_dir, filename)

        atomic_write_json(filepath, content)
        return filename

    def delete(self, filename: str) -> bool:
        """Delete file with locking.

        Returns True if file was deleted, False if it didn't exist.
        """
        filepath = os.path.join(self.data_dir, filename)
        lock = FileLock(f"{filepath}.lock", timeout=self.lock_timeout)

        with lock:
            if os.path.exists(filepath):
                os.unlink(filepath)
                return True
            return False
```

---

## Validation

### Concurrency Tests

Test scenarios derived from e-005 research:

```python
import pytest
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class TestConcurrentFileStore:
    """Concurrency tests for file locking strategy."""

    def test_parallel_writes_no_data_loss(self, tmp_path):
        """Verify parallel writes don't lose data."""
        store = ConcurrentFileStore(str(tmp_path))

        # Create initial file
        with store.locked_read_write("test.json") as data:
            data["counter"] = 0

        # Parallel increments
        num_writers = 10
        increments_per_writer = 100

        def increment():
            for _ in range(increments_per_writer):
                with store.locked_read_write("test.json") as data:
                    data["counter"] += 1

        threads = [threading.Thread(target=increment) for _ in range(num_writers)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Verify no lost updates
        result = store.read("test.json")
        assert result["counter"] == num_writers * increments_per_writer

    def test_unique_id_generation_no_collisions(self, tmp_path):
        """Verify Snowflake IDs are unique across threads."""
        store = ConcurrentFileStore(str(tmp_path))
        num_threads = 10
        ids_per_thread = 1000

        all_ids = []
        lock = threading.Lock()

        def generate_ids():
            local_ids = []
            for _ in range(ids_per_thread):
                local_ids.append(store.id_generator.generate())
            with lock:
                all_ids.extend(local_ids)

        threads = [threading.Thread(target=generate_ids) for _ in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Verify no duplicates
        assert len(all_ids) == len(set(all_ids))

    def test_atomic_write_crash_recovery(self, tmp_path):
        """Verify atomic writes don't corrupt on simulated crash."""
        filepath = tmp_path / "test.json"

        # Write initial valid content
        atomic_write_json(str(filepath), {"status": "initial"})

        # Simulate crash during write (temp file exists but rename didn't happen)
        tmp_file = tmp_path / ".tmp_crash_test.json"
        tmp_file.write_text('{"status": "partial_write"')  # Invalid JSON

        # Original file should still be valid
        with open(filepath) as f:
            data = json.load(f)
        assert data["status"] == "initial"

    def test_lock_timeout_with_backoff(self, tmp_path):
        """Verify lock acquisition with exponential backoff."""
        filepath = tmp_path / "locked.json"
        filepath.write_text('{}')

        lock = FileLock(f"{filepath}.lock", timeout=30)
        lock.acquire()  # Hold lock

        # Attempt to acquire with short timeout should fail
        try:
            second_lock = FileLock(f"{filepath}.lock", timeout=0.1)
            with pytest.raises(Timeout):
                second_lock.acquire(timeout=0.1)
        finally:
            lock.release()

    def test_stale_lock_detection(self, tmp_path):
        """Verify stale locks are detected (not auto-removed)."""
        filepath = tmp_path / "test.json"
        filepath.write_text('{}')

        # Create stale lock file
        lock_path = tmp_path / "test.json.lock"
        lock_path.touch()

        # Set modification time to 10 minutes ago
        old_time = time.time() - 600
        os.utime(lock_path, (old_time, old_time))

        # Lock age should be detectable
        lock_age = time.time() - os.path.getmtime(lock_path)
        assert lock_age > 300  # More than 5 minutes
```

### Performance Benchmarks

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Single write latency | <50ms | Median of 1000 writes |
| Lock acquisition (no contention) | <5ms | Median of 1000 acquisitions |
| Lock acquisition (10 writers) | <500ms | 95th percentile |
| Atomic write overhead | <2x direct write | Compare with non-atomic write |
| ID generation throughput | >10,000/sec | IDs per second single-threaded |
| ID generation (10 threads) | >50,000/sec | Total IDs per second |

### Lock Contention Measurements

```python
def benchmark_lock_contention(store: ConcurrentFileStore, num_writers: int, duration_sec: int = 10):
    """Measure lock contention under load."""
    metrics = {
        "total_operations": 0,
        "lock_wait_times": [],
        "operation_times": [],
        "timeouts": 0
    }
    lock = threading.Lock()
    stop_event = threading.Event()

    def writer():
        while not stop_event.is_set():
            start = time.time()
            try:
                with store.locked_read_write("benchmark.json") as data:
                    lock_acquired = time.time()
                    data["counter"] = data.get("counter", 0) + 1

                end = time.time()

                with lock:
                    metrics["total_operations"] += 1
                    metrics["lock_wait_times"].append(lock_acquired - start)
                    metrics["operation_times"].append(end - start)
            except Timeout:
                with lock:
                    metrics["timeouts"] += 1

    threads = [threading.Thread(target=writer) for _ in range(num_writers)]
    for t in threads:
        t.start()

    time.sleep(duration_sec)
    stop_event.set()

    for t in threads:
        t.join()

    return {
        "total_ops": metrics["total_operations"],
        "ops_per_sec": metrics["total_operations"] / duration_sec,
        "avg_lock_wait_ms": sum(metrics["lock_wait_times"]) / len(metrics["lock_wait_times"]) * 1000,
        "p95_lock_wait_ms": sorted(metrics["lock_wait_times"])[int(len(metrics["lock_wait_times"]) * 0.95)] * 1000,
        "timeouts": metrics["timeouts"]
    }
```

---

## References

### Primary Sources

1. **py-filelock Library**
   - GitHub: https://github.com/tox-dev/py-filelock
   - Cross-platform file locking for Python

2. **atomicwrites Library** (deprecated, educational)
   - Documentation: https://python-atomicwrites.readthedocs.io/
   - PyPI: https://pypi.org/project/atomicwrites/

3. **Twitter Snowflake**
   - Original Announcement: https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake
   - Wikipedia: https://en.wikipedia.org/wiki/Snowflake_ID

### Technical References

4. **Optimistic Concurrency Control** (Kung & Robinson, 1981)
   - ACM: https://dl.acm.org/doi/10.1145/319566.319567
   - Wikipedia: https://en.wikipedia.org/wiki/Optimistic_concurrency_control

5. **POSIX File Operations**
   - "POSIX write() is not atomic": https://utcc.utoronto.ca/~cks/space/blog/unix/WriteNotVeryAtomic
   - "Things UNIX can do atomically": https://rcrowley.org/2010/01/06/things-unix-can-do-atomically.html
   - LWN "A way to do atomic writes": https://lwn.net/Articles/789600/

6. **Reliable File Updates with Python**
   - gocept blog: https://blog.gocept.com/2013/07/15/reliable-file-updates-with-python/

### Multi-Agent Development

7. **Multi-Agent Claude Code**
   - DEV.to: https://dev.to/bredmond1019/multi-agent-orchestration-running-10-claude-instances-in-parallel-part-3-29da
   - Simon Willison's blog: https://simonwillison.net/2025/Oct/5/parallel-coding-agents/

### Research Documents

8. **e-005 Concurrent File Access Patterns**
   - Document: `projects/PROJ-001-plugin-cleanup/research/dev-skill-e-005-concurrent-access.md`
   - Patterns: PAT-001-e005 through PAT-005-e005

9. **e-007 Research Synthesis**
   - Document: `projects/PROJ-001-plugin-cleanup/research/dev-skill-e-007-synthesis.md`
   - Patterns: 37 patterns across 6 research documents

10. **e-008 Architecture Analysis**
    - Document: `projects/PROJ-001-plugin-cleanup/research/dev-skill-e-008-architecture-analysis.md`
    - ADR requirements and component mapping

11. **e-010 Risk Gap Analysis**
    - Document: `projects/PROJ-001-plugin-cleanup/research/dev-skill-e-010-risk-gap-analysis.md`
    - Risks R-005, R-006 addressed by this ADR

---

## Pattern Traceability

| Pattern ID | Pattern Name | Implementation Component |
|------------|--------------|-------------------------|
| PAT-001-e005 | Atomic Write with Durability | `atomic_write_json()` |
| PAT-002-e005 | File-Based Mutual Exclusion | `ConcurrentFileStore.locked_read_write()` |
| PAT-003-e005 | Optimistic Concurrency with Retry | Deferred (available if needed) |
| PAT-004-e005 | Coordination-Free ID Generation | `SnowflakeGenerator` |
| PAT-005-e005 | Isolation Through Workspace Separation | Out of scope (covered by Git worktrees) |

---

*ADR created: 2026-01-09*
*Author: ps-architect agent*
*Technical Story: INIT-DEV-SKILL*
