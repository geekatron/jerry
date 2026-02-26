# PROJ-002: Windows Compatibility

> **Status:** in_progress
> **Created:** 2026-02-10
> **Branch:** proj/windows-compat (from main)
> **Owner:** Kevin Horvatin

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this project delivers |
| [Strategy](#strategy) | How we'll approach the work |
| [Research Findings](#research-findings) | Full audit results |
| [Implementation Order](#implementation-order) | Prioritized execution plan |
| [Out of Scope](#out-of-scope) | Items intentionally not addressed |

---

## Summary

Make the Jerry framework fully functional on Windows. The core plugin hooks,
file locking, path handling, encoding, and developer tooling must all work on
Windows without requiring WSL or Git Bash.

**Prior Art:** The `fix/windows-fcntl-to-filelock` branch (8 commits) addressed
the most critical issues. This project starts fresh from `main` to produce a
cleaner history, incorporates those fixes, and addresses newly discovered issues.

---

## Strategy

### Phase 1: Cherry-Pick Critical Fixes
Port the 3 critical commits from `fix/windows-fcntl-to-filelock`:
- fcntl to filelock (f89f7ff)
- UTF-8 statusline encoding (29669f8)
- Cross-platform pre-commit hooks (c75a28e)

### Phase 2: Address New Findings
Fix issues discovered during research that the original branch missed:
- Missing `encoding="utf-8"` on write_text/read_text calls
- 20+ `split("\n")` usages that break on CRLF
- Symlink test gating

### Phase 3: Port Remaining Fixes
Cherry-pick the non-critical commits:
- CI test robustness (afa53aa, 39d837c, 5fc1611)
- Schema fix (387bdce)
- Documentation (5513101)

### Phase 4: Low Priority (Optional)
- Migration script PowerShell equivalents
- Windows CI runner

---

## Research Findings

### Critical (Application Cannot Start)

| Issue | Files | Impact |
|-------|-------|--------|
| `import fcntl` (Unix-only) | atomic_file_adapter.py, filesystem_event_store.py | ImportError on Windows |
| `.venv/bin/` hardcoded in pre-commit | .pre-commit-config.yaml | Pre-commit hooks fail |

### High (Malfunction/Data Corruption)

| Issue | Files | Impact |
|-------|-------|--------|
| `split("\n")` with file data | toon_serializer.py, validate_vtt.py, 6+ scripts | CRLF not handled |
| Missing `encoding="utf-8"` | chunker.py, parse_transcript_command_handler.py | System encoding used |
| Path string assertions | test_config_path.py, test_main.py | Tests fail on backslash |

### Medium (Tests Fail / DX Issues)

| Issue | Files | Impact |
|-------|-------|--------|
| Symlink tests | test_infrastructure.py | PermissionError without admin |
| CI assumes local data | test_bootstrap.py, test_pipeline.py, conftest.py | Tests skip/fail |
| Schema missing keywords | marketplace.schema.json | Validation fails |

### Low (Cosmetic / Optional)

| Issue | Files | Impact |
|-------|-------|--------|
| Shell scripts Unix-only | verify-platform.sh, verify-symlinks.sh | No Windows equivalent |
| No Windows CI runner | ci.yml | Issues not caught |

---

## Implementation Order

| Priority | Feature | Tasks | Est. Effort |
|----------|---------|-------|-------------|
| 1 | FEAT-001: File Locking | 3 | Cherry-pick |
| 2 | FEAT-005: Pre-Commit Hooks | 3 | Cherry-pick |
| 3 | FEAT-002: UTF-8 Encoding | 4 | Cherry-pick + new |
| 4 | FEAT-003: split("\n") Audit | 7 | New work |
| 5 | FEAT-004: Path Handling | 2 | Cherry-pick |
| 6 | FEAT-006: CI Test Robustness | 4 | Cherry-pick |
| 7 | FEAT-007: Schema Fix | 1 | Cherry-pick |
| 8 | FEAT-008: Documentation | 2 | Cherry-pick |
| 9 | FEAT-009: Symlink Gating | 1 | New work |
| 10 | FEAT-010: Migration Scripts | 2 | New work (optional) |
| 11 | FEAT-011: Windows CI | 1 | New work (optional) |

---

## Out of Scope

- Rewriting migration shell scripts as PowerShell (optional, tracked as low priority)
- WSL-specific optimizations
- Windows paths with spaces in all edge cases (not Jerry-specific)
- Python shebang removal (harmless when invoked via `uv run`)
