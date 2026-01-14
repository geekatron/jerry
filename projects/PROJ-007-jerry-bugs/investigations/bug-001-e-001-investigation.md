# Investigation Report: BUG-001 - Lock File Accumulation

**Bug ID:** BUG-001
**Entry ID:** e-001
**Investigator:** ps-investigator agent v2.1.0
**Date:** 2026-01-14
**Severity:** MEDIUM
**Status:** INVESTIGATION COMPLETE

---

## L0: Executive Summary (ELI5)

### What Happened

Every time Jerry starts a session, it creates small "lock files" to prevent two processes from editing the same file simultaneously. These lock files are created in `.jerry/local/locks/` but are **never deleted** after use.

### Impact

- **97+ lock files** have accumulated (all 0 bytes each)
- Slight performance degradation during directory operations
- Disk space waste (negligible but growing)
- Potential for confusion during debugging
- Risk of filesystem inode exhaustion on long-running systems

### Root Cause (One Sentence)

The `AtomicFileAdapter` was designed to create lock files for safety but the cleanup mechanism mentioned in ADR-006 was **never implemented**.

### Recommended Fix

Add a `cleanup_lock_file()` method to `AtomicFileAdapter` that removes lock files after the lock is released, or implement periodic garbage collection for stale locks.

---

## L1: Technical Analysis

### Evidence Chain

| Evidence ID | Source | Finding |
|-------------|--------|---------|
| E-001.1 | `.jerry/local/locks/` | 97 lock files (all 0 bytes) |
| E-001.2 | `atomic_file_adapter.py:72-76` | Lock files created via `_get_lock_path()` |
| E-001.3 | `atomic_file_adapter.py:94-95` | `lock_path.touch(exist_ok=True)` creates file |
| E-001.4 | `atomic_file_adapter.py:103-104` | Lock released but file NOT deleted |
| E-001.5 | `ADR-006:195-196` | "Lock file cleanup needed" acknowledged |
| E-001.6 | `session_start.py:110-111` | Every session calls `AtomicFileAdapter()` |

### 5 Whys Analysis

#### Why 1: Why are lock files accumulating?

**Answer:** The `AtomicFileAdapter.read_with_lock()` method creates lock files but never removes them after releasing the lock.

**Evidence:**
```python
# atomic_file_adapter.py:94-104
def read_with_lock(self, path: Path) -> str:
    lock_path = self._get_lock_path(path)
    lock_path.touch(exist_ok=True)  # Creates lock file

    with open(lock_path, "r+") as lock_file:
        fcntl.lockf(lock_file.fileno(), fcntl.LOCK_SH)
        try:
            # ... read operation ...
        finally:
            fcntl.lockf(lock_file.fileno(), fcntl.LOCK_UN)  # Releases lock
            # NOTE: Lock FILE is NOT deleted here
```

#### Why 2: Why doesn't the adapter delete lock files after releasing?

**Answer:** The implementation followed a deliberate design choice from ADR-006 to NOT auto-remove lock files, deferring cleanup to a separate mechanism that was never built.

**Evidence from ADR-006:302-306:**
```python
# Do NOT auto-remove; may still be valid
```

**Decision rationale:** The team was concerned about race conditions where one process might delete a lock file while another process was about to acquire it.

#### Why 3: Why was the cleanup mechanism never implemented?

**Answer:** ADR-006 acknowledged the need ("Lock file cleanup needed" at line 195-196) but listed it as a "Negative Consequence" to be addressed later. The work item was never created or prioritized.

**Evidence from ADR-006:194-196:**
```markdown
**Negative**:
- Write operations serialized per file (intentional trade-off)
- Lock file cleanup needed for crashed processes
```

#### Why 4: Why wasn't this caught earlier?

**Answer:** Three contributing factors:
1. Lock files are 0 bytes, so they don't trigger disk space alerts
2. No monitoring/metrics were set up for lock file count
3. The `.jerry/local/` directory is typically ignored during code review

**Evidence:** The lock directory grew to 97+ files without triggering any automated alerts.

#### Why 5: Why is there no garbage collection for stale locks?

**Answer:** The architecture deferred this responsibility to a "CLI command for administrators" that was documented but never implemented.

**Evidence from ADR-006:303-307:**
```markdown
1. **Detection**: Lock file older than 5 minutes without modification
2. **Warning**: Log warning but do NOT auto-remove
3. **Manual cleanup**: Provide CLI command for administrators
4. **Prevention**: Use `atexit` handler to release locks on clean exit
```

### Root Cause Statement

**Technical Root Cause:** The `AtomicFileAdapter` class creates lock files in `_get_lock_path()` (line 72-76) and touches them in `read_with_lock()` (line 95) and `write_atomic()` (line 126), but contains no mechanism to delete these files after the POSIX lock is released.

**Process Root Cause:** ADR-006 correctly identified the need for lock file cleanup as a "Negative Consequence" but:
1. No work item was created to track implementation
2. No acceptance criteria required cleanup functionality
3. No automated test verified lock file count stayed bounded

---

## L2: Systemic Analysis

### Ishikawa (Fishbone) Diagram

```
                                LOCK FILE ACCUMULATION
                                         |
        +-----------+-----------+-----------+-----------+-----------+
        |           |           |           |           |           |
     METHOD      MACHINE     MATERIAL       MAN     MEASUREMENT  ENVIRONMENT
        |           |           |           |           |           |
        |           |           |           |           |           |
   +----+----+  +---+---+   +---+---+   +---+---+   +---+---+   +---+---+
   |         |  |       |   |       |   |       |   |       |   |       |
   |No delete|  |POSIX  |   |Empty  |   |ADR-006|   |No lock|   |Long   |
   |in unlock|  |lock   |   |lock   |   |deferred|  |file   |   |running|
   |flow     |  |semantics| |files  |   |cleanup|   |count  |   |sessions|
   |         |  |       |   |       |   |       |   |metrics|   |       |
   |Atomic   |  |File   |   |SHA256 |   |No WI  |   |No disk|   |Git    |
   |ops only |  |based  |   |hash   |   |created|   |usage  |   |worktree|
   |focus    |  |locks  |   |naming |   |for fix|   |alert  |   |isolation|
   +---------+  +-------+   +-------+   +-------+   +-------+   +-------+
```

#### Category Analysis

**METHOD (Design/Process)**
- Primary Cause: No cleanup step in the lock/unlock flow
- The adapter focuses on atomic operations but not lifecycle management
- Lock acquisition and release are decoupled from file lifecycle

**MACHINE (Technology/Infrastructure)**
- POSIX `fcntl.lockf` locks are advisory and don't manage file existence
- Lock files are separate from data files by design
- File-based locking requires external file management

**MATERIAL (Data/Resources)**
- Lock files are 0 bytes (invisible to disk usage monitoring)
- SHA256 hash naming makes files unrecognizable
- No metadata indicating when lock was last used

**MAN (Human Factors)**
- ADR-006 authors acknowledged need but deferred implementation
- No work item created to track the technical debt
- Code reviewers didn't catch missing cleanup

**MEASUREMENT (Metrics/Monitoring)**
- No metrics on lock file count
- No alerting on directory size/file count
- No automated tests for lock lifecycle

**ENVIRONMENT (External Factors)**
- Long-running sessions accumulate more locks
- Git worktree isolation means locks don't get cleaned by other processes
- Multiple Claude instances create overlapping lock files

### FMEA (Failure Mode and Effects Analysis)

| Failure Mode | Severity (1-10) | Occurrence (1-10) | Detection (1-10) | RPN | Recommended Action |
|--------------|-----------------|-------------------|------------------|-----|-------------------|
| Lock file exhausts inodes | 7 | 2 | 5 | 70 | Implement periodic garbage collection |
| Directory listing slow | 4 | 6 | 7 | 168 | Clean up locks on adapter disposal |
| Stale lock blocks operation | 8 | 3 | 4 | 96 | Add stale lock detection + CLI cleanup |
| Hash collision creates wrong lock | 9 | 1 | 3 | 27 | Extend hash to 32 chars (currently 16) |
| Lock file permissions block access | 6 | 2 | 6 | 72 | Ensure consistent umask on creation |
| Concurrent cleanup deletes active lock | 8 | 2 | 4 | 64 | Use atomic rename for cleanup marker |

**Risk Priority Number (RPN) = Severity x Occurrence x Detection**
- RPN > 100: Requires immediate attention
- RPN 50-100: Schedule for next release
- RPN < 50: Monitor and address if occurrence increases

**Highest Priority (RPN > 100):**
- Directory listing slow (RPN 168): Users may experience delay when accessing `.jerry/local/`

### Related Code Paths

The following code paths create lock files without cleanup:

1. **session_start.py:110-111** (per session)
   ```python
   file_adapter = AtomicFileAdapter()
   content = file_adapter.read_with_lock(path)
   ```

2. **AtomicFileAdapter.read_with_lock()** (every read)
   - Creates lock at line 94-95
   - Never deletes

3. **AtomicFileAdapter.write_atomic()** (every write)
   - Creates lock at line 124-126
   - Never deletes

4. **AtomicFileAdapter.delete_with_lock()** (every delete)
   - Creates lock at line 177-178
   - Never deletes

---

## Corrective Actions

### Immediate (0-24 hours)

**CA-001: Manual Cleanup Command**
```bash
# Safe cleanup of lock files older than 5 minutes
find .jerry/local/locks -name "*.lock" -mmin +5 -delete
```

**Risk:** Low - lock files older than 5 minutes are almost certainly stale
**Owner:** Operations/User
**Verification:** `ls .jerry/local/locks | wc -l` should show significantly fewer files

### Short-Term (1-2 weeks)

**CA-002: Add Lock File Cleanup to AtomicFileAdapter**

Add a cleanup method that removes lock files after lock release:

```python
def _cleanup_lock_file(self, lock_path: Path) -> None:
    """Remove lock file if no other process is using it.

    Uses non-blocking lock attempt to verify file is unused.
    """
    try:
        with open(lock_path, "r+") as lock_file:
            # Try non-blocking exclusive lock
            fcntl.lockf(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            try:
                # We got the lock, safe to delete
                lock_path.unlink(missing_ok=True)
            finally:
                fcntl.lockf(lock_file.fileno(), fcntl.LOCK_UN)
    except (BlockingIOError, OSError):
        # Another process has the lock, don't delete
        pass
```

**Work Item:** Create WI-XXX: Implement lock file cleanup in AtomicFileAdapter
**Acceptance Criteria:**
- [ ] Lock files are removed after successful operation
- [ ] Concurrent processes don't delete each other's locks
- [ ] Unit tests verify cleanup behavior
- [ ] Integration test confirms no lock accumulation over 100 operations

### Long-Term (1-3 months)

**CA-003: Implement Garbage Collection Service**

Create a background/startup garbage collector:

```python
class LockFileGarbageCollector:
    """Periodic cleanup of stale lock files."""

    def __init__(self, lock_dir: Path, max_age_seconds: int = 300):
        self.lock_dir = lock_dir
        self.max_age = max_age_seconds

    def collect(self) -> int:
        """Remove stale lock files. Returns count of files removed."""
        removed = 0
        cutoff = time.time() - self.max_age

        for lock_file in self.lock_dir.glob("*.lock"):
            if lock_file.stat().st_mtime < cutoff:
                # Verify not in use before deleting
                if self._is_stale(lock_file):
                    lock_file.unlink(missing_ok=True)
                    removed += 1

        return removed
```

**Work Item:** Create WI-XXX: Lock file garbage collection service
**Integration Points:**
- Run on session start (non-blocking)
- Expose as CLI command: `jerry maintenance cleanup-locks`
- Add metrics: `jerry.locks.total`, `jerry.locks.stale_removed`

**CA-004: Add Monitoring and Alerting**

- Add metric for lock file count
- Alert when count exceeds threshold (e.g., 500)
- Log warning when lock file is older than 5 minutes

---

## Appendix A: Complete Evidence Listing

### A.1 Lock File Directory Listing (Partial)

```
$ ls -la .jerry/local/locks/
total 0
drwxr-xr-x  99 adam.nowak  staff  3168 Jan 14 07:56 .
drwxr-xr-x   3 adam.nowak  staff    96 Jan 14 07:56 ..
-rw-r--r--   1 adam.nowak  staff     0 Jan 14 07:56 005ca7d9071b1885.lock
-rw-r--r--   1 adam.nowak  staff     0 Jan 14 07:56 0081aff5156f4b6d.lock
-rw-r--r--   1 adam.nowak  staff     0 Jan 14 07:56 0281abc1de6d3d0d.lock
... (97 files total)
```

### A.2 Code Paths Creating Lock Files

| File | Line | Method | Creates Lock |
|------|------|--------|--------------|
| atomic_file_adapter.py | 94-95 | read_with_lock | Yes |
| atomic_file_adapter.py | 124-126 | write_atomic | Yes |
| atomic_file_adapter.py | 177-178 | delete_with_lock | Yes |
| session_start.py | 110-111 | load_local_context | Via read_with_lock |

### A.3 ADR-006 Relevant Excerpts

**Line 195-196 (Negative Consequences):**
> Lock file cleanup needed for crashed processes

**Line 303-307 (Stale Lock Cleanup):**
> 1. Detection: Lock file older than 5 minutes without modification
> 2. Warning: Log warning but do NOT auto-remove
> 3. Manual cleanup: Provide CLI command for administrators
> 4. Prevention: Use `atexit` handler to release locks on clean exit

---

## Appendix B: References

### Internal Documents

| Document | Location | Relevance |
|----------|----------|-----------|
| ADR-006 | `projects/PROJ-001-plugin-cleanup/design/ADR-006-file-locking-strategy.md` | Design decisions for locking |
| AtomicFileAdapter | `src/infrastructure/adapters/persistence/atomic_file_adapter.py` | Implementation code |
| session_start.py | `src/interface/cli/session_start.py` | Usage context |

### External References

| Reference | URL | Relevance |
|-----------|-----|-----------|
| py-filelock | https://github.com/tox-dev/py-filelock | Alternative locking library |
| POSIX fcntl | https://man7.org/linux/man-pages/man2/fcntl.2.html | Lock semantics |
| Atomic writes | https://rcrowley.org/2010/01/06/things-unix-can-do-atomically.html | Pattern background |

---

## Sign-Off

| Role | Name | Date | Status |
|------|------|------|--------|
| Investigator | ps-investigator v2.1.0 | 2026-01-14 | COMPLETE |
| Reviewer | (pending) | - | PENDING |
| Approver | (pending) | - | PENDING |

---

*Investigation completed: 2026-01-14*
*Generated by ps-investigator agent v2.1.0*
