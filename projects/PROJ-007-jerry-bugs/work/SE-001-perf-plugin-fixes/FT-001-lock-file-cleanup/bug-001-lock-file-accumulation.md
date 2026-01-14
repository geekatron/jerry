# BUG-001: Lock File Accumulation

> **Bug ID:** BUG-001
> **Feature:** FT-001 Lock File Cleanup
> **Enabler:** EN-001
> **Status:** INVESTIGATING
> **Severity:** MEDIUM
> **Created:** 2026-01-14
> **Last Updated:** 2026-01-14

---

## Summary

Lock files are accumulating in `.jerry/local/locks/` without any cleanup mechanism, causing potential performance degradation as sessions with Claude using Jerry grow.

---

## Symptoms

1. Claude Code slows down as sessions grow
2. `.jerry/local/locks/` directory contains 97 empty lock files
3. All lock files are 0 bytes (created by `touch()`)

---

## Reproduction Steps

1. Use Jerry Framework with any file operations
2. Observe `.jerry/local/locks/` directory growth
3. Lock files are created but never removed

---

## Technical Details

### Location of Bug

**File:** `src/infrastructure/adapters/persistence/atomic_file_adapter.py`

**Lines:** 72-76, 95

```python
def _get_lock_path(self, path: Path) -> Path:
    self._lock_dir.mkdir(parents=True, exist_ok=True)
    path_hash = hashlib.sha256(str(path.absolute()).encode()).hexdigest()[:16]
    lock_name = f"{path_hash}.lock"
    return self._lock_dir / lock_name
```

**Line 95:** `lock_path.touch(exist_ok=True)` - Creates lock file but never removes it.

### Root Cause

The `AtomicFileAdapter` was designed with lock file creation but:
1. No cleanup mechanism was implemented
2. ADR-006 mentioned "Lock file cleanup needed for crashed processes" but deferred implementation
3. Lock files persist indefinitely

---

## Impact Assessment

| Impact Area | Severity | Description |
|-------------|----------|-------------|
| Performance | MEDIUM | Directory scan overhead grows with file count |
| Storage | LOW | Each file is 0 bytes, but inode usage grows |
| Reliability | LOW | Not causing failures, just slowdowns |

---

## Evidence Chain

| ID | Type | Source | Finding |
|----|------|--------|---------|
| E-001 | Data | `ls -la .jerry/local/locks/ | wc -l` | 97 files + 2 (. and ..) = 100 lines |
| E-002 | Code | `atomic_file_adapter.py:95` | `lock_path.touch(exist_ok=True)` |
| E-003 | Code | Entire file | No `unlink()` or `remove()` calls for lock files |
| E-004 | Doc | ADR-006:195-196 | Acknowledged need for cleanup, not implemented |

---

## Proposed Fix

*To be determined after full investigation (EN-001).*

### Options Under Consideration

1. **Cleanup at session start:** Remove lock files older than threshold
2. **Add TTL to AtomicFileAdapter:** Cleanup as part of normal operations
3. **Use adjacent lock files:** Per ADR-006 original design (e.g., `file.json.lock`)
4. **Periodic cleanup task:** Background cleanup of stale locks

---

## Related Artifacts

| Type | Location | Description |
|------|----------|-------------|
| Enabler | [en-001.md](./en-001.md) | Investigation enabler |
| Feature | [FEATURE-WORKTRACKER.md](./FEATURE-WORKTRACKER.md) | Parent feature |
| ADR | `projects/PROJ-001-plugin-cleanup/design/ADR-006-file-locking-strategy.md` | Original design |
| Source | `src/infrastructure/adapters/persistence/atomic_file_adapter.py` | Bug location |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-14 | BUG-001 documented | Claude |
