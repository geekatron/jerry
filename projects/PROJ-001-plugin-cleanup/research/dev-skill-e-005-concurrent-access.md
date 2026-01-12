# Concurrent File Access Patterns for Multi-Instance Scenarios

**Document ID:** dev-skill-e-005-concurrent-access
**PS ID:** dev-skill
**Entry ID:** e-005
**Date:** 2026-01-09
**Author:** ps-researcher agent (v2.0.0)
**Topic:** Concurrent file access patterns

---

## L0: Executive Summary (ELI5)

When multiple programs (like several Claude Code instances) try to read and write the same files at the same time, bad things can happen: files can get corrupted, data can be lost, or programs can get stuck waiting forever.

**The solution involves three main strategies:**

1. **Atomic Writes**: Write to a temporary file first, then rename it to the final name. This is like writing a letter on scratch paper, then swapping it with the official document in one quick motion.

2. **File Locking**: Put a "Do Not Disturb" sign on files you're working on, so other programs wait their turn.

3. **Unique IDs Without Coordination**: Use special ID formats (like Snowflake IDs) that guarantee uniqueness even when programs don't talk to each other.

**Key Takeaway:** For Jerry's multi-instance scenarios, use the **temp-file-rename pattern** with **py-filelock** for critical operations, and **Snowflake-style IDs** for generating unique identifiers without coordination.

---

## L1: Technical Findings (Engineer Level)

### 1. Atomic File Writes in Python

#### 1.1 The Temp File + Rename Pattern

The standard pattern for atomic writes involves three steps:

```python
import os
import tempfile

def atomic_write(filepath: str, content: str) -> None:
    """Write content atomically using temp file + rename."""
    # 1. Create temp file in SAME directory (critical for atomicity)
    dir_path = os.path.dirname(filepath) or '.'
    fd, tmp_path = tempfile.mkstemp(dir=dir_path, prefix='.tmp_')

    try:
        # 2. Write and sync to disk
        with os.fdopen(fd, 'w') as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())

        # 3. Atomic rename (POSIX guarantees atomicity on same filesystem)
        os.replace(tmp_path, filepath)

        # 4. Sync directory metadata (for new files)
        dir_fd = os.open(dir_path, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    except:
        # Clean up temp file on failure
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise
```

**Why This Works:**
- `os.replace()` (Python 3.3+) is atomic on all platforms including Windows
- Temp file in same directory ensures same filesystem (cross-filesystem renames are NOT atomic)
- Readers always see either the complete old file or the complete new file, never a partial write

#### 1.2 fsync and Durability

```python
# Durability levels (from weakest to strongest):

# Level 1: Python buffer only
f.write(data)  # Data may be lost on Python crash

# Level 2: OS buffer
f.flush()  # Data may be lost on OS crash

# Level 3: Disk buffer (full durability)
f.flush()
os.fsync(f.fileno())  # Data survives OS crash

# Level 4: Disk + directory metadata (for new files)
os.fsync(f.fileno())
os.fsync(os.open(dir_path, os.O_RDONLY | os.O_DIRECTORY))
```

**Performance Note:** `os.fdatasync()` is faster than `os.fsync()` when you don't need metadata updates (timestamps, ownership).

#### 1.3 atomicwrites Library (Deprecated but Educational)

The [atomicwrites](https://github.com/untitaker/python-atomicwrites) library (now deprecated) provided a clean API:

```python
# Historical example - library is deprecated
from atomicwrites import atomic_write

with atomic_write('foo.txt', overwrite=True) as f:
    f.write('Hello world.')
```

The library handled platform-specific nuances including Windows's `MoveFileEx` and macOS's `F_FULLFSYNC`.

### 2. File Locking Mechanisms

#### 2.1 py-filelock Library

[py-filelock](https://github.com/tox-dev/py-filelock) provides cross-platform file locking:

```python
from filelock import FileLock, Timeout

# Basic usage with context manager
lock = FileLock("high_ground.txt.lock", timeout=10)

with lock:
    # Protected region - only one process can be here
    with open("high_ground.txt", "w") as f:
        f.write("Hello there!")

# Non-blocking attempt
try:
    with lock.acquire(blocking=False):
        # Got the lock immediately
        pass
except Timeout:
    print("Lock is held by another process")

# Timeout with retry
try:
    with lock.acquire(timeout=10):
        # Acquired within 10 seconds
        pass
except Timeout:
    print("Could not acquire lock within 10 seconds")
```

#### 2.2 Pessimistic vs Optimistic Locking

| Aspect | Pessimistic | Optimistic |
|--------|-------------|------------|
| When to Lock | Before reading | Only at commit |
| Contention Handling | Wait/queue | Detect + retry |
| Best For | High contention | Low contention |
| Performance | Lower throughput | Higher throughput |
| Complexity | Lower | Higher (retry logic) |

**Pessimistic Example (py-filelock):**
```python
with FileLock("data.json.lock"):
    data = json.load(open("data.json"))
    data["counter"] += 1
    with open("data.json", "w") as f:
        json.dump(data, f)
```

**Optimistic Example (version-based):**
```python
def optimistic_update(filepath: str, transform_fn, max_retries: int = 3):
    """Update file with optimistic concurrency control."""
    for attempt in range(max_retries):
        # Read current state with version
        with open(filepath) as f:
            data = json.load(f)

        original_version = data.get("_version", 0)

        # Apply transformation
        data = transform_fn(data)
        data["_version"] = original_version + 1

        # Attempt atomic write with version check
        with FileLock(f"{filepath}.lock", timeout=1):
            with open(filepath) as f:
                current = json.load(f)

            if current.get("_version", 0) != original_version:
                # Conflict detected, retry
                continue

            atomic_write(filepath, json.dumps(data))
            return data

    raise ConflictError(f"Failed after {max_retries} retries")
```

#### 2.3 Lock Timeout and Deadlock Prevention

**Timeout Strategies:**
```python
import time
import random

def acquire_with_backoff(lock: FileLock, max_attempts: int = 5):
    """Acquire lock with exponential backoff."""
    for attempt in range(max_attempts):
        try:
            lock.acquire(timeout=1)
            return True
        except Timeout:
            if attempt < max_attempts - 1:
                # Exponential backoff with jitter
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)
    return False
```

**Deadlock Prevention via Lock Ordering:**
```python
def transfer(account_a: str, account_b: str, amount: float):
    """Transfer between accounts with deadlock-free locking."""
    # Always acquire locks in sorted order to prevent deadlock
    locks = sorted([
        FileLock(f"{account_a}.lock"),
        FileLock(f"{account_b}.lock")
    ], key=lambda l: l.lock_file)

    try:
        for lock in locks:
            lock.acquire(timeout=10)

        # Perform transfer
        # ...
    finally:
        for lock in reversed(locks):
            lock.release()
```

### 3. Optimistic Concurrency Control

#### 3.1 Version-Based Conflict Detection

Modeled after etag/version patterns in REST APIs and databases:

```python
from dataclasses import dataclass
from typing import TypeVar, Generic
import hashlib

T = TypeVar('T')

@dataclass
class VersionedData(Generic[T]):
    data: T
    version: str  # Content hash or incrementing version

    @classmethod
    def from_file(cls, filepath: str) -> 'VersionedData':
        with open(filepath, 'rb') as f:
            content = f.read()
        return cls(
            data=json.loads(content),
            version=hashlib.sha256(content).hexdigest()[:16]
        )

    def write_if_unchanged(self, filepath: str, new_data: T) -> bool:
        """Write only if file hasn't changed. Returns success."""
        current = VersionedData.from_file(filepath)
        if current.version != self.version:
            return False  # Conflict

        atomic_write(filepath, json.dumps(new_data))
        return True
```

#### 3.2 Compare-and-Swap Pattern

```python
def compare_and_swap(filepath: str, expected: dict, new_value: dict) -> bool:
    """Atomic compare-and-swap for JSON files."""
    lock = FileLock(f"{filepath}.lock", timeout=5)

    with lock:
        with open(filepath) as f:
            current = json.load(f)

        if current != expected:
            return False  # CAS failed

        atomic_write(filepath, json.dumps(new_value))
        return True
```

### 4. Distributed ID Generation

#### 4.1 Twitter Snowflake Pattern

64-bit IDs with embedded timestamp, worker ID, and sequence:

```python
import time
from threading import Lock

class SnowflakeGenerator:
    """
    Snowflake ID structure (64 bits):
    - 1 bit: sign (always 0)
    - 41 bits: timestamp (milliseconds since epoch)
    - 10 bits: worker ID (0-1023)
    - 12 bits: sequence (0-4095)
    """

    EPOCH = 1704067200000  # 2024-01-01 00:00:00 UTC
    WORKER_BITS = 10
    SEQUENCE_BITS = 12
    MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1

    def __init__(self, worker_id: int):
        if worker_id < 0 or worker_id >= (1 << self.WORKER_BITS):
            raise ValueError(f"Worker ID must be 0-{(1 << self.WORKER_BITS) - 1}")

        self.worker_id = worker_id
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = Lock()

    def generate(self) -> int:
        with self.lock:
            timestamp = int(time.time() * 1000) - self.EPOCH

            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.MAX_SEQUENCE
                if self.sequence == 0:
                    # Wait for next millisecond
                    while timestamp <= self.last_timestamp:
                        timestamp = int(time.time() * 1000) - self.EPOCH
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            return (
                (timestamp << (self.WORKER_BITS + self.SEQUENCE_BITS)) |
                (self.worker_id << self.SEQUENCE_BITS) |
                self.sequence
            )

    @staticmethod
    def parse(snowflake_id: int) -> dict:
        """Extract components from a Snowflake ID."""
        return {
            "timestamp": (snowflake_id >> 22) + SnowflakeGenerator.EPOCH,
            "worker_id": (snowflake_id >> 12) & 0x3FF,
            "sequence": snowflake_id & 0xFFF
        }
```

#### 4.2 UUID vs Snowflake Comparison

| Aspect | UUID (v4) | UUIDv7 | Snowflake |
|--------|-----------|--------|-----------|
| Size | 128 bits | 128 bits | 64 bits |
| Coordination | None | None | Worker ID needed |
| Time-sortable | No | Yes | Yes |
| Index performance | Poor | Good | Best |
| Uniqueness | Statistical | Statistical | Guaranteed (with worker ID) |

#### 4.3 No-Coordination ID Generation

For scenarios without worker ID coordination:

```python
import uuid
import os
import socket
import hashlib

def generate_machine_worker_id() -> int:
    """Derive worker ID from machine characteristics (no coordination)."""
    # Combine hostname, PID, and MAC address
    identity = f"{socket.gethostname()}-{os.getpid()}-{uuid.getnode()}"
    hash_bytes = hashlib.sha256(identity.encode()).digest()

    # Use first 10 bits (0-1023)
    return int.from_bytes(hash_bytes[:2], 'big') & 0x3FF

# Or use UUIDv7 for truly coordination-free IDs
def uuidv7() -> str:
    """Generate UUIDv7 (time-ordered UUID)."""
    import secrets

    timestamp_ms = int(time.time() * 1000)

    # 48 bits timestamp + 4 bits version (7) + 12 bits random
    uuid_int = (timestamp_ms << 16) | 0x7000 | secrets.randbits(12)
    # Add 2 bits variant (10) + 62 bits random
    uuid_int = (uuid_int << 64) | (0x8 << 60) | secrets.randbits(60)

    return str(uuid.UUID(int=uuid_int))
```

### 5. Race Condition Prevention

#### 5.1 Multi-Instance File Access Pattern

For multiple Claude Code instances:

```python
from filelock import FileLock
from contextlib import contextmanager
import json

class ConcurrentFileStore:
    """Thread and multi-process safe file store."""

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.lock_timeout = 30

    @contextmanager
    def locked_read_write(self, filename: str):
        """Context manager for safe read-modify-write operations."""
        filepath = os.path.join(self.data_dir, filename)
        lock = FileLock(f"{filepath}.lock", timeout=self.lock_timeout)

        with lock:
            # Read current data
            if os.path.exists(filepath):
                with open(filepath) as f:
                    data = json.load(f)
            else:
                data = {}

            # Yield for modification
            yield data

            # Write back atomically
            atomic_write(filepath, json.dumps(data, indent=2))

    def create_unique(self, prefix: str, content: dict) -> str:
        """Create file with unique name (no collisions)."""
        generator = SnowflakeGenerator(generate_machine_worker_id())

        unique_id = generator.generate()
        filename = f"{prefix}_{unique_id}.json"
        filepath = os.path.join(self.data_dir, filename)

        # No lock needed - filename is guaranteed unique
        atomic_write(filepath, json.dumps(content))

        return filename
```

#### 5.2 POSIX Guarantees

| Operation | Atomicity Guarantee |
|-----------|---------------------|
| `rename()` | Atomic (same filesystem) |
| `link()` | Atomic |
| `unlink()` | Atomic |
| `write()` | NOT atomic (may be partial) |
| `read()` | NOT atomic (may see partial writes) |
| `open(O_CREAT\|O_EXCL)` | Atomic file creation |

**Safe File Creation Without Lock:**
```python
import os
import errno

def create_exclusive(filepath: str, content: str) -> bool:
    """Create file only if it doesn't exist (atomic)."""
    try:
        fd = os.open(filepath, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        try:
            os.write(fd, content.encode())
            os.fsync(fd)
        finally:
            os.close(fd)
        return True
    except OSError as e:
        if e.errno == errno.EEXIST:
            return False  # File already exists
        raise
```

---

## L2: Strategic Patterns and Trade-offs (Architect Level)

### Pattern PAT-001: Atomic Write with Durability

**Context:** Need to update files without corruption risk.

**Problem:** Direct file writes can leave files in inconsistent state if interrupted.

**Solution:** Temp-file-rename pattern with fsync.

**Trade-offs:**
| Benefit | Cost |
|---------|------|
| Complete atomicity | Double disk space temporarily |
| Crash safety | fsync is slow |
| No partial reads | Slightly more complex |

**When to Use:**
- Configuration files
- Workload state files
- Any file where partial content is catastrophic

**When to Avoid:**
- Large files (>10MB)
- High-frequency writes (>100/sec)
- Append-only logs

### Pattern PAT-002: File-Based Mutual Exclusion

**Context:** Multiple processes accessing shared files.

**Problem:** Concurrent modifications cause data corruption.

**Solution:** Use py-filelock with timeout and retry logic.

**Implementation Guidance:**
```
Lock granularity spectrum:

Coarse (1 lock per directory) ←→ Fine (1 lock per file)
         ↓                              ↓
    Simple, fewer deadlocks       Higher concurrency
    Lower throughput              More complex
```

**Trade-offs:**
| Benefit | Cost |
|---------|------|
| Prevents corruption | Reduces parallelism |
| Simple mental model | Potential for deadlock |
| Cross-process safety | Lock file cleanup needed |

### Pattern PAT-003: Optimistic Concurrency with Retry

**Context:** Low-contention scenario with occasional conflicts.

**Problem:** Pessimistic locking reduces throughput unnecessarily.

**Solution:** Version-based conflict detection with exponential backoff.

**State Diagram:**
```
[Read] → [Modify] → [Validate Version] → [Write]
                          ↓ (conflict)
                    [Backoff] → [Retry] ─┘
```

**Trade-offs:**
| Benefit | Cost |
|---------|------|
| Higher throughput | Wasted work on conflict |
| No waiting | Complex retry logic |
| Scales better | Starvation risk under high contention |

### Pattern PAT-004: Coordination-Free ID Generation

**Context:** Multiple instances generating unique identifiers.

**Problem:** Sequential IDs require coordination; collisions break data integrity.

**Solution:** Snowflake-style IDs or UUIDv7.

**Decision Matrix:**
| Requirement | Solution |
|-------------|----------|
| Time-sortable + compact | Snowflake with derived worker ID |
| Zero coordination + simple | UUIDv7 |
| Database-friendly | UUIDv7 (128-bit, standard format) |
| High throughput (>4096/ms) | Snowflake with larger sequence bits |

**Trade-offs:**
| Benefit | Cost |
|---------|------|
| No coordination needed | Larger than sequential IDs |
| Time-sortable | Clock sync dependency (Snowflake) |
| Horizontal scalability | Worker ID collision risk (Snowflake) |

### Pattern PAT-005: Isolation Through Workspace Separation

**Context:** Multiple Claude Code instances working on same codebase.

**Problem:** Agents modify same files causing merge conflicts.

**Solution:** Git worktrees + file locking for shared state.

**Architecture:**
```
Repository Root/
├── worktree-main/          # Main development
├── worktree-agent-1/       # Agent 1 workspace
├── worktree-agent-2/       # Agent 2 workspace
└── shared-state/           # Locked shared resources
    ├── items/              # Work items (file-locked)
    └── config/             # Configuration (file-locked)
```

**Trade-offs:**
| Benefit | Cost |
|---------|------|
| Full isolation | Disk space overhead |
| No merge conflicts | Coordination via shared state needed |
| Independent commits | Eventual merge required |

### Jerry-Specific Recommendations

For the Jerry framework's multi-instance scenarios:

1. **Work Items Store:** Use PAT-002 (file locking) with PAT-001 (atomic writes)
   - Lock at file level, not directory
   - Use 30-second timeout with exponential backoff
   - Atomic write all item updates

2. **ID Generation:** Use PAT-004 with derived worker ID
   - Hash of (hostname + PID + timestamp) for worker ID
   - Snowflake-style IDs for work items
   - Sortable IDs enable efficient timeline queries

3. **Session Coordination:** Use PAT-003 (optimistic) for session files
   - Sessions are rarely concurrent
   - Version-based conflict detection
   - Last-write-wins with merge on conflict

4. **Plugin Operations:** Use PAT-005 (workspace separation)
   - Each plugin gets isolated workspace
   - Shared state through locked common store
   - Events/messages for coordination

---

## Citations and References

### Primary Sources

1. **py-filelock Library**
   - GitHub: https://github.com/tox-dev/py-filelock
   - Documentation: Context7 library ID `/tox-dev/py-filelock`

2. **atomicwrites Library** (deprecated)
   - Documentation: https://python-atomicwrites.readthedocs.io/
   - GitHub: https://github.com/untitaker/python-atomicwrites
   - PyPI: https://pypi.org/project/atomicwrites/

3. **Twitter Snowflake**
   - Original Announcement: https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake
   - Wikipedia: https://en.wikipedia.org/wiki/Snowflake_ID

4. **Sony Sonyflake**
   - GitHub: https://github.com/sony/sonyflake

### Academic and Technical References

5. **Optimistic Concurrency Control**
   - Original Paper (Kung & Robinson, 1981): https://dl.acm.org/doi/10.1145/319566.319567
   - Wikipedia: https://en.wikipedia.org/wiki/Optimistic_concurrency_control

6. **POSIX File Operations**
   - "POSIX write() is not atomic": https://utcc.utoronto.ca/~cks/space/blog/unix/WriteNotVeryAtomic
   - "Things UNIX can do atomically": https://rcrowley.org/2010/01/06/things-unix-can-do-atomically.html
   - LWN "A way to do atomic writes": https://lwn.net/Articles/789600/

7. **Stateless Snowflake (2025)**
   - arXiv paper: https://arxiv.org/html/2512.11643

### Python-Specific Resources

8. **Python os.fsync**
   - ZetCode Guide: https://zetcode.com/python/os-fsync/
   - GeeksforGeeks: https://www.geeksforgeeks.org/python/python-os-fsync-method/

9. **Reliable File Updates with Python**
   - gocept blog: https://blog.gocept.com/2013/07/15/reliable-file-updates-with-python/

10. **Python stdlib Discussion on atomicwrite**
    - https://discuss.python.org/t/adding-atomicwrite-in-stdlib/11899

### Race Condition and Threading

11. **Python Threading Lock Tutorial**
    - https://www.pythontutorial.net/python-concurrency/python-threading-lock/

12. **Multiprocessing Race Conditions**
    - Super Fast Python: https://superfastpython.com/multiprocessing-race-condition-python/

13. **File Conflicts in Multithreaded Python**
    - Medium article: https://medium.com/@aman.deep291098/avoiding-file-conflicts-in-multithreaded-python-programs-34f2888f4521

### Distributed Systems

14. **UUID vs Sequential ID**
    - Baeldung: https://www.baeldung.com/uuid-vs-sequential-id-as-primary-key
    - System Design Handbook: https://www.systemdesignhandbook.com/guides/design-a-unique-id-generator-in-distributed-systems/

15. **Leader Election**
    - etcd leader election: https://akazuko.medium.com/leader-election-using-etcd-10301473843c
    - ZooKeeper recipes: https://zookeeper.apache.org/doc/r3.9.3/recipes.html

16. **Deadlock Prevention**
    - Jenkov tutorial: https://jenkov.com/tutorials/java-concurrency/deadlock-prevention.html
    - GeeksforGeeks: https://www.geeksforgeeks.org/operating-systems/deadlock-prevention/

### Multi-Agent Development

17. **Multi-Agent Claude Code**
    - DEV.to orchestration guide: https://dev.to/bredmond1019/multi-agent-orchestration-running-10-claude-instances-in-parallel-part-3-29da
    - Claude Code Docs on Subagents: https://code.claude.com/docs/en/sub-agents
    - claude-squad GitHub: https://github.com/smtg-ai/claude-squad

18. **Parallel Coding Agents**
    - Simon Willison's blog: https://simonwillison.net/2025/Oct/5/parallel-coding-agents/

---

## Extracted Patterns Summary

| Pattern ID | Name | Use Case |
|------------|------|----------|
| PAT-001 | Atomic Write with Durability | Crash-safe file updates |
| PAT-002 | File-Based Mutual Exclusion | Multi-process file access |
| PAT-003 | Optimistic Concurrency with Retry | Low-contention updates |
| PAT-004 | Coordination-Free ID Generation | Distributed unique IDs |
| PAT-005 | Isolation Through Workspace Separation | Multi-agent development |

---

*Research completed: 2026-01-09*
*Agent: ps-researcher v2.0.0*
