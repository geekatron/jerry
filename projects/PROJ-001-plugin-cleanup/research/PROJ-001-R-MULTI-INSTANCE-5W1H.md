# Research: Multi-Instance Work Tracker Validation - 5W1H Analysis

**Document ID**: PROJ-001-R-MULTI-INSTANCE-5W1H
**Date**: 2026-01-09
**Author**: Claude (Distinguished Systems Engineer)
**Status**: IN PROGRESS

---

## Executive Summary

This document presents a comprehensive 5W1H analysis for validating that the decomposed work tracker will function correctly when accessed by multiple Claude Code instances simultaneously. This is fundamentally a **concurrent file access problem** in a distributed system context.

---

## 1. WHAT - Problem Definition

### 1.1 What is the Problem?

The Jerry Work Tracker stores persistent state in the filesystem:

```
projects/${JERRY_PROJECT}/.jerry/data/
├── items/
│   └── WORK-NNN.json    # Individual work item files
├── index.json           # Quick lookup index
└── sequences.json       # ID sequence tracking
```

When **multiple Claude Code instances** access this shared storage simultaneously:
- **Race Conditions**: Two instances reading/writing the same file
- **Lost Updates**: Instance A reads, Instance B writes, Instance A overwrites with stale data
- **Index Corruption**: Index file being updated by multiple processes
- **Sequence Collisions**: Two instances getting the same WORK-NNN ID

### 1.2 What are the Concurrency Scenarios?

| Scenario | Risk Level | Description |
|----------|------------|-------------|
| Concurrent Reads | LOW | Multiple instances reading same work item |
| Concurrent Writes (Different Files) | MEDIUM | Instances updating different work items |
| Concurrent Writes (Same File) | HIGH | Instances updating same work item |
| Concurrent Index Updates | HIGH | Multiple instances modifying index.json |
| Concurrent Sequence Generation | CRITICAL | ID collision (WORK-001 assigned twice) |

### 1.3 What are the Success Criteria?

1. **No Data Loss**: Updates are never silently lost
2. **No Corruption**: Files remain valid JSON after concurrent access
3. **ID Uniqueness**: WORK-NNN IDs are globally unique across all instances
4. **Consistency**: Index reflects actual work items at all times
5. **Deterministic Behavior**: Conflicts are detected and handled gracefully

---

## 2. WHY - Business/Technical Justification

### 2.1 Why is this Validation Needed?

**Business Justification:**
- Jerry Framework is designed to survive context compaction
- Users may have multiple Claude Code instances in terminals, IDEs, etc.
- Data corruption or loss violates the core promise of persistent work tracking

**Technical Justification:**
- Filesystem access is inherently shared across processes
- No built-in coordination mechanism exists between Claude Code instances
- Without validation, silent failures could occur in production use

### 2.2 Why Now?

- The work tracker implementation is being designed
- Validating concurrency BEFORE implementation prevents costly rework
- Per NASA Systems Engineering practices: "Test early, test often"

---

## 3. WHO - Stakeholders and Components

### 3.1 Who is Affected?

| Stakeholder | Impact |
|-------------|--------|
| Users with multiple terminals | Direct - data integrity |
| Users with IDE + CLI | Direct - shared state |
| Future maintainers | Indirect - complexity |
| CI/CD pipelines | Indirect - parallel test runs |

### 3.2 What Components are Involved?

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Code Instance 1                    │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Work Tracker Skill → Infrastructure Adapter            │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │  Concurrent
                           │  File Access
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Shared Filesystem                         │
│  projects/${JERRY_PROJECT}/.jerry/data/                     │
│  ├── items/WORK-001.json                                    │
│  ├── index.json                                             │
│  └── sequences.json                                         │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │  Concurrent
                           │  File Access
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                    Claude Code Instance 2                    │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Work Tracker Skill → Infrastructure Adapter            │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. WHERE - Location and Scope

### 4.1 Where in the Codebase?

| Component | Location | Concurrency Concern |
|-----------|----------|---------------------|
| Domain Layer | `src/domain/` | None (pure logic) |
| Application Layer | `src/application/` | Transaction boundaries |
| **Infrastructure Layer** | `src/infrastructure/adapters/` | **PRIMARY CONCERN** |
| Storage | `projects/${JERRY_PROJECT}/.jerry/data/` | File access |

### 4.2 Where do Conflicts Occur?

The infrastructure adapter is the single point of coordination:

```python
# Current pattern (UNSAFE)
class FilesystemWorkItemAdapter:
    def save(self, work_item: WorkItem) -> None:
        path = self._get_item_path(work_item.id)
        with open(path, 'w') as f:
            json.dump(work_item.to_dict(), f)  # ← NOT ATOMIC
        self._update_index(work_item)          # ← RACE CONDITION
```

---

## 5. WHEN - Timing and Triggers

### 5.1 When do Conflicts Occur?

| Trigger | Frequency | Severity |
|---------|-----------|----------|
| Session start (reading) | Every session | LOW |
| Creating new work item | Per feature/task | HIGH |
| Updating work item status | Many times per session | HIGH |
| Listing work items | Many times per session | LOW |
| Completing work item | Per feature/task | MEDIUM |

### 5.2 When Should Validation Run?

- **Unit Tests**: On every commit (mock filesystem)
- **Integration Tests**: On every PR (real filesystem, single process)
- **System Tests**: On merge to main (multi-process simulation)
- **E2E Tests**: On release candidate (actual Claude Code instances)

---

## 6. HOW - Implementation Approaches

### 6.1 Industry Best Practices (Research Summary)

#### 6.1.1 File Locking Strategies

| Strategy | Pros | Cons | Best For |
|----------|------|------|----------|
| **Pessimistic (filelock)** | Simple, guaranteed exclusion | Blocking, potential deadlock | High-conflict scenarios |
| **Optimistic (version)** | Non-blocking, high throughput | Requires retry logic | Low-conflict scenarios |
| **Atomic Writes** | No partial writes | Requires temp file + rename | All scenarios |

**Industry Recommendation (2025):**
> "In environments with multiple nodes or services, managing locks can be complex. Optimistic locking simplifies conflict management using version numbers or timestamps."
> — [Medium: Why Distributed Systems Moving to Optimistic Concurrency](https://medium.com/@yashbatra11111/why-are-distributed-systems-moving-from-pessimistic-to-optimistic-concurrency-b5b114722d21)

#### 6.1.2 Sequence Number Generation

| Strategy | Pros | Cons | Best For |
|----------|------|------|----------|
| **Centralized Counter** | Simple, sequential | Single point of failure | Single-node systems |
| **Snowflake IDs** | Decentralized, unique | Larger IDs (64-bit) | Distributed systems |
| **UUID** | Simple, no coordination | Not sequential, large | When order doesn't matter |
| **Range Allocation** | Batch efficiency | Gaps possible | High-throughput |

**Industry Standard:**
> "Twitter Snowflake encodes metadata (time, server ID, sequence) directly into the ID. Each machine can generate IDs independently without requiring coordination."
> — [CalliCoder: Distributed ID Generation](https://www.callicoder.com/distributed-unique-id-sequence-number-generator/)

### 6.2 Recommended Solution Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Work Tracker Adapter                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. ATOMIC WRITES                                            │
│     ┌──────────┐      ┌──────────┐      ┌──────────┐        │
│     │ Write to │  →   │ fsync()  │  →   │ rename() │        │
│     │ temp file│      │          │      │ to final │        │
│     └──────────┘      └──────────┘      └──────────┘        │
│                                                              │
│  2. OPTIMISTIC LOCKING                                       │
│     ┌──────────┐      ┌──────────┐      ┌──────────┐        │
│     │ Read with│  →   │ Modify   │  →   │ Write if │        │
│     │ version  │      │          │      │ version  │        │
│     └──────────┘      └──────────┘      │ matches  │        │
│                                         └──────────┘        │
│  3. SNOWFLAKE IDS                                            │
│     ┌──────────────────────────────────────────────┐        │
│     │ timestamp (41) + instance (10) + seq (12)    │        │
│     └──────────────────────────────────────────────┘        │
│                                                              │
│  4. FALLBACK: FILE LOCK                                      │
│     ┌──────────┐      ┌──────────┐      ┌──────────┐        │
│     │ Acquire  │  →   │ Critical │  →   │ Release  │        │
│     │ .lock    │      │ Section  │      │ .lock    │        │
│     └──────────┘      └──────────┘      └──────────┘        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 6.3 Detailed Implementation Strategy

#### Strategy 1: Atomic Writes (Required)

```python
from pathlib import Path
import tempfile
import os

def atomic_write(path: Path, content: str) -> None:
    """Write content atomically using temp file + rename."""
    dir_path = path.parent
    fd, temp_path = tempfile.mkstemp(dir=str(dir_path), suffix='.tmp')
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.rename(temp_path, str(path))
    except:
        os.unlink(temp_path)
        raise
```

**Citation**: [python-atomicwrites library](https://github.com/untitaker/python-atomicwrites)

#### Strategy 2: Optimistic Locking (Required)

```python
@dataclass
class VersionedWorkItem:
    id: str
    version: int  # Incremented on each save
    # ... other fields

def save_with_optimistic_lock(item: VersionedWorkItem) -> None:
    path = get_path(item.id)

    # Read current version
    if path.exists():
        current = json.loads(path.read_text())
        if current['version'] != item.version:
            raise ConcurrentModificationError(
                f"Item {item.id} was modified by another process"
            )

    # Increment version and save
    item.version += 1
    atomic_write(path, json.dumps(item.to_dict()))
```

**Citation**: [ByteByteGo: Optimistic vs Pessimistic Locking](https://bytebytego.com/guides/pessimistic-vs-optimistic-locking/)

#### Strategy 3: Snowflake-style ID Generation (Required)

```python
import time
import threading

class SnowflakeIdGenerator:
    """Generate unique IDs without coordination.

    ID Structure (simplified for WORK-NNN display):
    - Display: WORK-{sequence_display}
    - Internal: timestamp_ms + instance_id + sequence
    """

    def __init__(self, instance_id: int):
        self.instance_id = instance_id & 0x3FF  # 10 bits
        self.sequence = 0
        self.last_timestamp = 0
        self.lock = threading.Lock()

    def next_id(self) -> str:
        with self.lock:
            timestamp = int(time.time() * 1000)

            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & 0xFFF
                if self.sequence == 0:
                    # Wait for next millisecond
                    while timestamp <= self.last_timestamp:
                        timestamp = int(time.time() * 1000)
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            # Combine into 64-bit ID
            internal_id = (
                (timestamp << 22) |
                (self.instance_id << 12) |
                self.sequence
            )

            # For display, use a shorter hash
            display_num = internal_id % 1000000
            return f"WORK-{display_num:06d}"
```

**Citation**: [Aman's AI Journal: Designing Unique ID Generator](https://aman.ai/sysdes/uniqueIDForDB/)

#### Strategy 4: File Lock Fallback (For Critical Sections)

```python
from filelock import FileLock, Timeout

def with_file_lock(lock_path: Path, timeout: float = 10.0):
    """Decorator for file-lock protected operations."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            lock = FileLock(str(lock_path) + ".lock", timeout=timeout)
            try:
                with lock:
                    return func(*args, **kwargs)
            except Timeout:
                raise ConcurrentAccessError(
                    f"Could not acquire lock within {timeout}s"
                )
        return wrapper
    return decorator

@with_file_lock(Path("sequences.json"))
def allocate_sequence_range(count: int = 100) -> range:
    """Allocate a range of sequence numbers atomically."""
    # ... implementation
```

**Citation**: [filelock documentation](https://github.com/tox-dev/py-filelock)

---

## 7. Test Scenarios (Preview)

### 7.1 Happy Path

| ID | Scenario | Expected Outcome |
|----|----------|------------------|
| HP-001 | Two instances create work items simultaneously | Both items created with unique IDs |
| HP-002 | Instance reads while another writes | Reader gets consistent snapshot |
| HP-003 | Instance updates item not being modified | Update succeeds |

### 7.2 Edge Cases

| ID | Scenario | Expected Outcome |
|----|----------|------------------|
| EC-001 | Two instances update SAME item simultaneously | One succeeds, one gets conflict error |
| EC-002 | Instance crashes mid-write | No partial file, previous version intact |
| EC-003 | Lock held too long (timeout) | Clean timeout error, no deadlock |
| EC-004 | 100 instances create items in burst | All IDs unique |

### 7.3 Failure Scenarios

| ID | Scenario | Expected Outcome |
|----|----------|------------------|
| FS-001 | Disk full during write | Graceful error, no corruption |
| FS-002 | Filesystem permissions denied | Clear error message |
| FS-003 | Network filesystem latency | Timeouts handled gracefully |

---

## 8. Decision: Recommended Approach

Based on industry best practices and the Jerry Framework requirements:

### Primary Strategy: Optimistic Locking + Atomic Writes

1. **All writes use atomic pattern** (temp file + fsync + rename)
2. **All entities have version field** (optimistic concurrency)
3. **IDs use Snowflake pattern** (no coordination needed)
4. **File locks only for sequence range allocation** (pessimistic fallback)

### Rationale

| Factor | Decision Driver |
|--------|-----------------|
| Conflict frequency | LOW - Users rarely have concurrent sessions |
| Performance | Optimistic > Pessimistic for low-conflict |
| Complexity | Atomic writes are stdlib-compatible |
| Reliability | Snowflake IDs are battle-tested (Twitter scale) |

---

## 9. References and Citations

### Academic/Industry Sources

1. [Chroma Research: Context Rot](https://research.trychroma.com/context-rot) - Problem domain
2. [ByteByteGo: Optimistic vs Pessimistic Locking](https://bytebytego.com/guides/pessimistic-vs-optimistic-locking/) - Locking strategies
3. [CalliCoder: Distributed ID Generation](https://www.callicoder.com/distributed-unique-id-sequence-number-generator/) - Snowflake pattern
4. [Wikipedia: Optimistic Concurrency Control](https://en.wikipedia.org/wiki/Optimistic_concurrency_control) - OCC theory

### Library Documentation

5. [filelock (py-filelock)](https://github.com/tox-dev/py-filelock) - File locking library
6. [python-atomicwrites](https://github.com/untitaker/python-atomicwrites) - Atomic write pattern
7. [portalocker](https://github.com/wolph/portalocker) - Distributed locking

### Technical Articles

8. [Medium: FileLock Concurrency](https://medium.com/top-python-libraries/python-concurrency-made-easy-master-filelock-for-seamless-file-locking-6ca26dce7493)
9. [Medium: Optimistic to Pessimistic Migration](https://medium.com/@yashbatra11111/why-are-distributed-systems-moving-from-pessimistic-to-optimistic-concurrency-b5b114722d21)
10. [SuperFastPython: Thread-Safe File Writing](https://superfastpython.com/thread-safe-write-to-file-in-python/)

---

## 10. Next Steps

1. **Design Validation Test Strategy** - Create BDD feature files
2. **Implement Concurrency Tests** - Unit, Integration, System levels
3. **Create Proof-of-Concept** - Validate atomic write + optimistic lock
4. **Document ADR** - Architectural Decision Record for chosen approach

---

*Document Version: 1.0*
*Last Updated: 2026-01-09*
