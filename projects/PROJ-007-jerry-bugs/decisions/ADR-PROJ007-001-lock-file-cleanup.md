# ADR-PROJ007-001: Lock File Lifecycle Management

**Status**: Proposed
**Date**: 2026-01-14
**Author**: ps-architect agent
**Related Bug**: BUG-001 (Lock File Accumulation)
**Related ADR**: ADR-006 (File Locking Strategy)

---

## Context

### Problem Statement

The Jerry Framework's `AtomicFileAdapter` creates lock files in `.jerry/local/locks/` to enable safe concurrent file access. These lock files are 0-byte sentinel files used by `fcntl.lockf()` for POSIX file locking.

**The Critical Issue**: Lock files are created but never deleted. This was a deliberate design decision in ADR-006 to avoid race conditions, with cleanup deferred to a "separate mechanism" that was never implemented.

### Current Behavior

The `AtomicFileAdapter` follows this pattern for all operations:

```python
# From atomic_file_adapter.py
lock_path = self._get_lock_path(path)
lock_path.touch(exist_ok=True)  # Creates lock file

with open(lock_path, "r+") as lock_file:
    fcntl.lockf(lock_file.fileno(), fcntl.LOCK_EX)
    try:
        # ... perform operation ...
    finally:
        fcntl.lockf(lock_file.fileno(), fcntl.LOCK_UN)
        # NOTE: lock_path is NOT deleted here
```

### Impact

From the investigation (bug-001-e-001-investigation.md):

| Metric | Value | Concern |
|--------|-------|---------|
| Lock files accumulated | 97+ | Growing indefinitely |
| File size per lock | 0 bytes | Low disk impact |
| Directory listing time | Increasing | Performance degradation |
| Inode consumption | 97+ | Risk of exhaustion on long-running systems |

### Root Cause

1. **Technical**: The `AtomicFileAdapter` class creates lock files in `_get_lock_path()` (line 72-76) and touches them in `read_with_lock()` (line 95) and `write_atomic()` (line 126), but contains no mechanism to delete these files after the POSIX lock is released.

2. **Process**: ADR-006 correctly identified the need for lock file cleanup as a "Negative Consequence" (line 195-196) but:
   - No work item was created to track implementation
   - No acceptance criteria required cleanup functionality
   - No automated test verified lock file count stayed bounded

---

## Decision Drivers

| ID | Driver | Priority | Notes |
|----|--------|----------|-------|
| DD-1 | Must be safe for concurrent access | Critical | Cannot delete a lock file while another process is using it |
| DD-2 | Must handle crashed processes | High | Stale locks from crashes must be recoverable |
| DD-3 | Must be backward compatible | High | No changes to lock file naming or location |
| DD-4 | Should minimize performance impact | Medium | Cleanup overhead should be negligible |
| DD-5 | Should be testable | Medium | Cleanup behavior must be verifiable |
| DD-6 | Must work cross-platform | Medium | macOS, Linux (fcntl-based locking) |

---

## Considered Options

### Option 1: Immediate Cleanup After Lock Release

**Description**: Delete the lock file immediately after releasing the fcntl lock, but only if no other process is using it.

**Implementation**:
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

**Pros**:
- Immediate cleanup - no accumulation
- Simple implementation (~15 lines)
- No background process or scheduler needed
- Self-contained within adapter

**Cons**:
- Slight performance overhead per operation (non-blocking lock attempt)
- Cannot clean up locks from crashed processes
- Race window exists between unlock and cleanup check
- Multiple processes may compete to delete the same file

### Option 2: Periodic Garbage Collection

**Description**: Run garbage collection at session start (or periodically) to remove stale lock files older than a threshold.

**Implementation**:
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

    def _is_stale(self, lock_path: Path) -> bool:
        """Check if lock file is truly stale (not held by another process)."""
        try:
            with open(lock_path, "r+") as f:
                fcntl.lockf(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                fcntl.lockf(f.fileno(), fcntl.LOCK_UN)
                return True
        except (BlockingIOError, OSError):
            return False
```

**Pros**:
- Handles crashed process cleanup (primary ADR-006 concern)
- Batched operation - single overhead per session
- Clear separation of concerns (adapter vs. lifecycle)
- CLI command can be provided for manual cleanup

**Cons**:
- Lock files still accumulate between garbage collection runs
- Requires integration point (session start, cron, etc.)
- Age threshold is arbitrary (5 minutes default)
- Additional component to maintain

### Option 3: Hybrid Approach (Recommended)

**Description**: Combine immediate cleanup after operations with periodic garbage collection for crash recovery.

**Implementation**:
1. **Eager Cleanup**: After each operation, attempt to delete the lock file if unused
2. **Defensive GC**: Run garbage collection at session start for crashed processes
3. **CLI Command**: Provide `jerry maintenance cleanup-locks` for manual intervention

**Rationale**: This approach addresses both concerns:
- Normal operations: Lock files are cleaned up immediately
- Crash recovery: GC catches any orphaned locks on next session

**Pros**:
- Best of both worlds - immediate cleanup + crash recovery
- Bounded accumulation even under heavy load
- Manual override for edge cases
- Follows ADR-006 intent ("CLI command for administrators")

**Cons**:
- Most complex implementation
- Two mechanisms to test and maintain
- Slight redundancy (GC may find nothing to clean if eager works)

---

## Decision Outcome

**Chosen Option**: Option 3 (Hybrid Approach)

### Rationale

1. **Safety First**: The hybrid approach is the safest option because it combines proactive cleanup with defensive garbage collection. If the eager cleanup fails or is skipped, the GC provides a safety net.

2. **ADR-006 Alignment**: The original ADR-006 explicitly mentioned:
   - "Lock file cleanup needed for crashed processes" (line 195-196)
   - "Manual cleanup: Provide CLI command for administrators" (line 306)

   The hybrid approach implements both requirements.

3. **Defense in Depth**: In distributed systems, defense in depth is preferred. Having two complementary cleanup mechanisms ensures robustness.

4. **Testability**: Each mechanism can be tested independently:
   - Eager cleanup: Unit test after single operation
   - GC: Integration test with simulated stale locks
   - CLI: E2E test of manual invocation

### Why Other Options Were Rejected

**Option 1 (Immediate Only)**: Rejected because it cannot handle crashed processes. If a Jerry process crashes while holding a lock, the lock file remains forever. This was the primary concern in ADR-006.

**Option 2 (GC Only)**: Rejected because it allows unbounded accumulation between runs. Under heavy load with many unique files, thousands of lock files could accumulate before the next session start.

---

## Consequences

### Positive

1. **Bounded Lock File Count**: Lock files will no longer accumulate indefinitely
2. **Crash Recovery**: Stale locks from crashed processes are automatically cleaned
3. **Administrator Control**: CLI command provides manual override capability
4. **Performance Maintained**: Per-operation overhead is minimal (single non-blocking syscall)
5. **Backward Compatible**: No changes to lock file naming, location, or format

### Negative

1. **Implementation Complexity**: Two cleanup mechanisms to implement and maintain
2. **Test Surface**: Additional test cases for cleanup behavior
3. **Edge Case Risk**: Theoretical race between cleanup check and file deletion
4. **GC Configuration**: Need to choose appropriate age threshold (5 minutes proposed)

### Neutral

1. **Lock Files Still Created**: The pattern of creating lock files remains unchanged
2. **Directory Structure**: `.jerry/local/locks/` structure unchanged
3. **fcntl Semantics**: POSIX locking behavior unchanged

---

## Implementation Plan

### Phase 1: Eager Cleanup (Priority: High)

**Changes to AtomicFileAdapter**:

1. Add private method `_cleanup_lock_file(self, lock_path: Path) -> None`
2. Call cleanup in `finally` block of each locking operation
3. Handle all exceptions silently (cleanup is best-effort)

**Files to Modify**:
- `src/infrastructure/adapters/persistence/atomic_file_adapter.py`

**Acceptance Criteria**:
- [ ] Lock files are deleted after successful `read_with_lock()`
- [ ] Lock files are deleted after successful `write_atomic()`
- [ ] Lock files are deleted after successful `delete_with_lock()`
- [ ] Cleanup failure does not affect operation success
- [ ] Concurrent processes do not interfere with each other's cleanup

### Phase 2: Garbage Collector (Priority: Medium)

**New Component**:

Create `LockFileGarbageCollector` class in `src/infrastructure/internal/lock_gc.py`

**Integration Points**:
- Call `collect()` in `session_start.py` (non-blocking)
- Expose via CLI: `jerry maintenance cleanup-locks`

**Acceptance Criteria**:
- [ ] GC removes lock files older than 5 minutes
- [ ] GC skips files that are currently locked
- [ ] GC logs count of files removed
- [ ] CLI command returns success/failure status

### Phase 3: Testing (Priority: High)

**Unit Tests** (`tests/unit/infrastructure/test_atomic_file_adapter.py`):
- [ ] Test eager cleanup removes lock file after operation
- [ ] Test cleanup skips file if another process holds lock
- [ ] Test cleanup failure is silent

**Integration Tests** (`tests/integration/test_lock_gc.py`):
- [ ] Test GC removes stale lock files
- [ ] Test GC respects age threshold
- [ ] Test GC skips active locks
- [ ] Test GC handles empty directory
- [ ] Test no lock accumulation over 100+ operations

**E2E Tests** (`tests/e2e/test_lock_lifecycle.py`):
- [ ] Test full session lifecycle with cleanup
- [ ] Test CLI command execution

### Testing Strategy: Simulating Concurrent Access

To safely test the non-blocking lock check:

```python
def test_cleanup_skips_locked_file(tmp_path):
    """Verify cleanup does not delete file held by another process."""
    lock_path = tmp_path / "test.lock"
    lock_path.touch()

    # Simulate another process holding the lock
    lock_holder = open(lock_path, "r+")
    fcntl.lockf(lock_holder.fileno(), fcntl.LOCK_EX)

    try:
        adapter = AtomicFileAdapter(lock_dir=tmp_path)
        # Cleanup should fail silently
        adapter._cleanup_lock_file(lock_path)
        # File should still exist
        assert lock_path.exists()
    finally:
        fcntl.lockf(lock_holder.fileno(), fcntl.LOCK_UN)
        lock_holder.close()
```

---

## Appendix A: Code Locations

| Component | File | Lines |
|-----------|------|-------|
| Lock file creation | `atomic_file_adapter.py` | 72-76, 94-95, 124-126 |
| Lock release (no cleanup) | `atomic_file_adapter.py` | 104, 151, 188 |
| ADR-006 cleanup acknowledgment | `ADR-006-file-locking-strategy.md` | 195-196 |
| ADR-006 cleanup strategy | `ADR-006-file-locking-strategy.md` | 302-307 |

## Appendix B: Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Race condition during cleanup | Low | Medium | Non-blocking lock check before delete |
| Cleanup breaks concurrent access | Very Low | High | fcntl semantics guarantee lock is released before unlink |
| GC deletes active lock | Very Low | High | Non-blocking lock check in `_is_stale()` |
| Performance regression | Low | Low | Cleanup is single syscall; benchmarking in tests |

## Appendix C: References

| Document | Location | Relevance |
|----------|----------|-----------|
| Investigation Report | `investigations/bug-001-e-001-investigation.md` | Root cause analysis |
| ADR-006 | `projects/PROJ-001-plugin-cleanup/design/ADR-006-file-locking-strategy.md` | Original design decisions |
| AtomicFileAdapter | `src/infrastructure/adapters/persistence/atomic_file_adapter.py` | Implementation code |
| POSIX fcntl | https://man7.org/linux/man-pages/man2/fcntl.2.html | Lock semantics |

---

## Sign-Off

| Role | Name | Date | Status |
|------|------|------|--------|
| Author | ps-architect agent | 2026-01-14 | PROPOSED |
| Reviewer | (pending) | - | PENDING |
| Approver | (pending) | - | PENDING |

---

*ADR created: 2026-01-14*
*Generated by ps-architect agent*
