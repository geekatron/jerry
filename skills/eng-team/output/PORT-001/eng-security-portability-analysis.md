# Platform Portability Security Analysis

**Engagement ID:** PORT-001
**Agent:** eng-security
**Date:** 2026-02-26
**Target Platforms:** Windows 10/11, macOS (Intel/ARM), Linux (Ubuntu, Fedora, Debian, Arch)
**Codebase:** Jerry Framework v0.21.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 - Executive Summary](#l0---executive-summary) | High-level findings for stakeholders |
| [L1 - Technical Findings](#l1---technical-findings) | Detailed findings with evidence and remediation |
| [L2 - Strategic Implications](#l2---strategic-implications) | Systemic patterns and architectural recommendations |

---

## L0 - Executive Summary

### Finding Count by Severity

| Severity | Count |
|----------|-------|
| Critical | 0 |
| Major | 5 |
| Minor | 9 |
| **Total** | 14 |

### Overall Assessment

The Jerry Framework demonstrates **generally good cross-platform awareness** with several key design decisions that support portability:

1. **Positive:** Uses `pathlib.Path` extensively for path handling
2. **Positive:** Uses `filelock` library for cross-platform file locking
3. **Positive:** Has explicit Windows/POSIX handling in `lifecycle_dir_resolver.py`
4. **Positive:** Uses `tempfile.mkstemp()` for atomic file operations
5. **Positive:** Normalizes path separators in critical code paths

### Top 3 Risk Areas

1. **Shell Command Execution:** Status line and settings invoke `python3` directly, which may not resolve correctly on Windows
2. **Hardcoded Unix Paths:** Several docstring examples and type hints use `/tmp` and Unix-style paths
3. **Shell Scripts:** Migration scripts use bash-specific syntax without Windows alternatives

### Recommended Immediate Actions

1. Replace `python3` with `sys.executable` or cross-platform wrapper in settings.json
2. Add `.gitattributes` file to enforce line ending consistency
3. Add Windows CI testing to validate portability claims

---

## L1 - Technical Findings

### PORT-001: Hardcoded `python3` Command in Status Line Configuration

| Attribute | Value |
|-----------|-------|
| **ID** | PORT-001 |
| **Severity** | Major |
| **Category** | Shell Commands |
| **File** | `.claude/settings.json` |
| **Line** | 25 |

**Description:** The status line command uses `python3` which may not be available on Windows systems where Python is typically invoked via `python`, `py`, or `py -3`.

**Platform Impact:** Windows 10/11 - Status line will fail to execute, breaking the user experience.

**Evidence:**
```json
"statusLine": {
  "type": "command",
  "command": "python3 .claude/statusline.py",
  "padding": 0
}
```

**Recommendation:** Use a cross-platform invocation method:
```json
"command": "python .claude/statusline.py"
```
Or use `sys.executable` pattern in a wrapper script that Claude Code can invoke.

**Test Verification:**
1. Run on Windows with Python installed via official installer
2. Verify `python3` command fails but `python` or `py -3` works
3. Test status line functionality after fix

---

### PORT-002: Hardcoded `/tmp` Path in Docstring Examples

| Attribute | Value |
|-----------|-------|
| **ID** | PORT-002 |
| **Severity** | Minor |
| **Category** | Path Handling |
| **Files** | Multiple (see below) |
| **Lines** | Various |

**Description:** Several docstring examples use `/tmp` which does not exist on Windows systems.

**Platform Impact:** Windows - Documentation examples are incorrect; could mislead developers.

**Evidence:**
- `src/session_management/infrastructure/adapters/event_sourced_session_repository.py:335`
- `src/work_tracking/infrastructure/persistence/filesystem_event_store.py:367`
- `src/work_tracking/infrastructure/adapters/event_sourced_work_item_repository.py:428`
- `src/infrastructure/internal/file_store.py:82-83`

```python
# From event_sourced_session_repository.py:335
store: IEventStoreWithUtilities = FileSystemEventStore("/tmp")

# From file_store.py:82-83
>>> store.write("/tmp/data.json", b'{"key": "value"}')
>>> data = store.read("/tmp/data.json")
```

**Recommendation:** Use `tempfile.gettempdir()` in examples:
```python
import tempfile
>>> store = FileSystemEventStore(tempfile.gettempdir())
>>> store.write(Path(tempfile.gettempdir()) / "data.json", b'...')
```

**Test Verification:**
1. Search codebase for `/tmp` literal strings
2. Verify each is either documentation-only or wrapped with platform-aware handling
3. Run doctests on Windows to verify examples work

---

### PORT-003: Bash-Specific Shell Scripts Without Windows Alternative

| Attribute | Value |
|-----------|-------|
| **ID** | PORT-003 |
| **Severity** | Major |
| **Category** | Shell Commands |
| **Files** | `scripts/migration/verify-platform.sh`, `scripts/migration/verify-symlinks.sh` |
| **Lines** | All |

**Description:** Migration scripts use `#!/bin/bash` and bash-specific features (arrays, `[[`, process substitution) with no PowerShell or cross-platform equivalents provided.

**Platform Impact:** Windows - Cannot run migration verification without WSL or Git Bash.

**Evidence:**
```bash
#!/bin/bash
# From verify-platform.sh:27
set -o pipefail

# Bash arrays (line 51-59)
readonly EXCLUDED_DIRS=(
    "projects"
    "transcripts"
    ...
)

# Bash-specific test syntax (line 136)
if ! command -v rsync &> /dev/null; then
```

**Recommendation:**
1. Provide PowerShell equivalents (`verify-platform.ps1`, `verify-symlinks.ps1`)
2. Or use Python scripts for cross-platform compatibility
3. Document WSL requirement for Windows users if bash scripts are maintained

**Test Verification:**
1. Attempt to run scripts on Windows without WSL
2. Verify equivalent functionality in PowerShell versions
3. Document platform requirements in script headers

---

### PORT-004: Symlink Operations May Require Elevated Privileges on Windows

| Attribute | Value |
|-----------|-------|
| **ID** | PORT-004 |
| **Severity** | Major |
| **Category** | File System |
| **Files** | `.claude/` directory (contains symlinks), `scripts/migration/verify-symlinks.sh` |
| **Lines** | N/A |

**Description:** The `.claude/` directory contains symbolic links (`patterns -> ../.context/patterns`, `rules -> ../.context/rules`). Creating or manipulating symlinks on Windows requires either:
- Administrator privileges, or
- Developer Mode enabled, or
- Using junction points instead

**Platform Impact:** Windows - Repository clone may fail or produce broken symlinks; users may not have necessary privileges.

**Evidence:**
```
$ ls -la .claude/
lrwxr-xr-x  1 evorun  staff  20 Feb 20 12:00 patterns -> ../.context/patterns
lrwxr-xr-x  1 evorun  staff  17 Feb 20 12:00 rules -> ../.context/rules
```

**Recommendation:**
1. Document Windows symlink requirements in README
2. Add git config to handle symlinks: `git config core.symlinks true`
3. Provide a setup script that detects Windows and creates junctions if needed
4. Consider using file copies or relative imports instead of symlinks for critical functionality

**Test Verification:**
1. Clone repository on Windows without Developer Mode
2. Verify symlink status with `git status`
3. Test that application still functions with broken symlinks
4. Document recovery steps

---

### PORT-005: Missing `.gitattributes` for Line Ending Consistency

| Attribute | Value |
|-----------|-------|
| **ID** | PORT-005 |
| **Severity** | Minor |
| **Category** | File System |
| **File** | Repository root |
| **Line** | N/A |

**Description:** No `.gitattributes` file exists to enforce line ending normalization. This can cause issues when contributors work on different platforms.

**Platform Impact:** All platforms - Git may produce spurious diffs, shell scripts may fail if checked out with CRLF on Unix.

**Evidence:**
```bash
$ ls .gitattributes
ls: .gitattributes: No such file or directory
```

**Recommendation:** Add `.gitattributes`:
```
* text=auto
*.py text eol=lf
*.sh text eol=lf
*.json text eol=lf
*.md text eol=lf
*.yaml text eol=lf
*.yml text eol=lf
*.bat text eol=crlf
*.ps1 text eol=crlf
```

**Test Verification:**
1. Add `.gitattributes` file
2. Run `git check-attr -a -- *.py *.sh` to verify attributes
3. Cross-platform clone and verify line endings

---

### PORT-006: Path Separator in File Repository `_get_file_path`

| Attribute | Value |
|-----------|-------|
| **ID** | PORT-006 |
| **Severity** | Minor |
| **Category** | Path Handling |
| **File** | `src/infrastructure/adapters/file_repository.py` |
| **Line** | 95 |

**Description:** Uses hardcoded forward slash `/` for path construction instead of `os.path.join` or `pathlib`.

**Platform Impact:** Potentially Windows - Path may be constructed incorrectly, though Python's `Path` class handles this on read.

**Evidence:**
```python
def _get_file_path(self, aggregate_id: TId) -> str:
    # Sanitize ID for filesystem safety
    safe_id = self._sanitize_id(str(aggregate_id))
    return f"{self._base_path}/{safe_id}.json"
```

**Recommendation:** Use `pathlib` or `os.path.join`:
```python
def _get_file_path(self, aggregate_id: TId) -> str:
    safe_id = self._sanitize_id(str(aggregate_id))
    return str(Path(self._base_path) / f"{safe_id}.json")
```

**Test Verification:**
1. Create unit test that verifies path construction on Windows
2. Check that file operations work correctly with backslash paths
3. Verify existing tests pass on Windows CI

---

### PORT-007: Stream ID Sanitization Handles Backslashes

| Attribute | Value |
|-----------|-------|
| **ID** | PORT-007 |
| **Severity** | Minor (Informational - Good Practice) |
| **Category** | Path Handling |
| **File** | `src/work_tracking/infrastructure/persistence/filesystem_event_store.py` |
| **Line** | 113 |

**Description:** The code correctly sanitizes both forward and backslashes in stream IDs, demonstrating good cross-platform awareness.

**Evidence:**
```python
def _stream_file_path(self, stream_id: str) -> Path:
    """Get the file path for a stream."""
    # Sanitize stream_id to be filesystem-safe
    safe_stream_id = stream_id.replace("/", "_").replace("\\", "_")
    return self._events_dir / f"{safe_stream_id}.jsonl"
```

**Status:** Good practice - no action required.

---

### PORT-008: Pre-Tool Enforcement Path Normalization

| Attribute | Value |
|-----------|-------|
| **ID** | PORT-008 |
| **Severity** | Minor (Informational - Good Practice) |
| **Category** | Path Handling |
| **File** | `src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py` |
| **Lines** | 588, 595 |

**Description:** The code normalizes Windows backslashes to forward slashes for consistent pattern matching. This is a good cross-platform practice.

**Evidence:**
```python
# Normalize separators
rel_path = rel_path.replace("\\", "/")

# Check against governance patterns (most specific first)
for pattern, criticality in sorted(...):
    normalized_pattern = pattern.replace("\\", "/")
    if rel_path == normalized_pattern or rel_path.startswith(normalized_pattern):
        return criticality
```

**Status:** Good practice - no action required.

---

### PORT-009: Platform-Aware Lifecycle Directory Resolution

| Attribute | Value |
|-----------|-------|
| **ID** | PORT-009 |
| **Severity** | Minor (Informational - Good Practice) |
| **Category** | Environment |
| **File** | `src/infrastructure/adapters/configuration/lifecycle_dir_resolver.py` |
| **Lines** | 52-62 |

**Description:** Correctly uses platform-specific paths (`%APPDATA%` on Windows, `~/.jerry` on Unix).

**Evidence:**
```python
def _platform_default_lifecycle_dir() -> Path:
    """Return platform-appropriate Jerry lifecycle directory.

    Returns:
        ~/.jerry/local/ on macOS/Linux, %APPDATA%/jerry/local/ on Windows.
    """
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            return Path(appdata) / "jerry" / "local"
    return Path.home() / ".jerry" / "local"
```

**Status:** Good practice - no action required.

---

### PORT-010: Windows Console UTF-8 Configuration

| Attribute | Value |
|-----------|-------|
| **ID** | PORT-010 |
| **Severity** | Minor (Informational - Good Practice) |
| **Category** | Environment |
| **File** | `.claude/statusline.py` |
| **Lines** | 279-292 |

**Description:** Correctly configures Windows console for UTF-8 output with emoji support.

**Evidence:**
```python
def configure_windows_console() -> None:
    """Configure Windows console for UTF-8 output."""
    if sys.platform == "win32":
        try:
            # Reconfigure stdout for UTF-8 with error handling
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            # Python < 3.7 or reconfigure not available
            pass
```

**Status:** Good practice - no action required.

---

### PORT-011: Atomic File Write with Windows Retry Logic

| Attribute | Value |
|-----------|-------|
| **ID** | PORT-011 |
| **Severity** | Minor (Informational - Good Practice) |
| **Category** | File System |
| **File** | `src/infrastructure/adapters/persistence/atomic_file_adapter.py` |
| **Lines** | 140-152 |

**Description:** Correctly handles Windows file locking issues with retry logic for `os.replace()`.

**Evidence:**
```python
# Atomic replace - on Windows, retry briefly if the target
# is held open by antivirus/indexer (WinError 5)
if sys.platform == "win32":
    for attempt in range(5):
        try:
            os.replace(temp_path, path)
            break
        except PermissionError:
            if attempt == 4:
                raise
            time.sleep(0.01 * (attempt + 1))
else:
    os.replace(temp_path, path)
```

**Status:** Good practice - no action required.

---

### PORT-012: Claude Config Directory Cross-Platform Resolution

| Attribute | Value |
|-----------|-------|
| **ID** | PORT-012 |
| **Severity** | Minor (Informational - Good Practice) |
| **Category** | Environment |
| **File** | `.claude/statusline.py` |
| **Lines** | 392-404 |

**Description:** Correctly uses `%APPDATA%/claude` on Windows and `~/.claude` on Unix.

**Evidence:**
```python
def _get_claude_config_dir() -> Path | None:
    """Get the Claude Code configuration directory (cross-platform).

    Returns ~/.claude on macOS/Linux, %APPDATA%/claude on Windows.
    """
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            return Path(appdata) / "claude"
    try:
        return Path.home() / ".claude"
    except (RuntimeError, KeyError, OSError):
        return None
```

**Status:** Good practice - no action required.

---

### PORT-013: macOS Symlink Resolution Fallback

| Attribute | Value |
|-----------|-------|
| **ID** | PORT-013 |
| **Severity** | Major |
| **Category** | File System |
| **File** | `scripts/migration/verify-symlinks.sh` |
| **Lines** | 168-178 |

**Description:** Uses Python fallback for `readlink -f` on macOS, which doesn't support the `-f` flag. However, this approach assumes Python 3 is available.

**Platform Impact:** macOS without Python 3 - Script may fail.

**Evidence:**
```bash
resolve_symlink() {
    local symlink="$1"
    local target

    if command -v readlink &>/dev/null; then
        # macOS/BSD readlink doesn't have -f, use different approach
        if [[ "$(uname)" == "Darwin" ]]; then
            # Use Python for reliable resolution on macOS
            target=$(python3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$symlink" 2>/dev/null) || true
        else
            # GNU readlink
            target=$(readlink -f "$symlink" 2>/dev/null) || true
        fi
    fi
    ...
}
```

**Recommendation:** Also check for `greadlink` (GNU readlink from Homebrew):
```bash
if [[ "$(uname)" == "Darwin" ]]; then
    if command -v greadlink &>/dev/null; then
        target=$(greadlink -f "$symlink" 2>/dev/null)
    else
        target=$(python3 -c "..." "$symlink" 2>/dev/null)
    fi
fi
```

**Test Verification:**
1. Test on macOS without Python 3 in PATH
2. Test with Homebrew coreutils installed
3. Verify fallback chain works correctly

---

### PORT-014: Case Sensitivity Assumptions in Project Directory Matching

| Attribute | Value |
|-----------|-------|
| **ID** | PORT-014 |
| **Severity** | Minor |
| **Category** | File System |
| **File** | `src/session_management/infrastructure/adapters/filesystem_project_adapter.py` |
| **Lines** | 26, 67-68 |

**Description:** The project directory pattern uses lowercase-only matching, but Windows filesystems are case-insensitive. A directory named `PROJ-001-MyProject` would not match the pattern.

**Platform Impact:** Potential issue on all platforms if users create projects with uppercase letters in the slug.

**Evidence:**
```python
# Pattern to match valid project directory names
PROJECT_DIR_PATTERN = re.compile(r"^PROJ-\d{3}-[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")

# Later in scan_projects:
if item.name.lower() == "archive":
    continue
```

**Recommendation:** Consider case-insensitive matching or document the lowercase requirement:
```python
PROJECT_DIR_PATTERN = re.compile(r"^PROJ-\d{3}-[a-z][a-z0-9]*(?:-[a-z0-9]+)*$", re.IGNORECASE)
```
Or enforce lowercase at project creation time.

**Test Verification:**
1. Create project with uppercase slug on Windows
2. Verify project is discovered/not discovered correctly
3. Add validation at creation time if case matters

---

## L2 - Strategic Implications

### Security Posture Assessment

**Overall Rating:** Moderate

The codebase demonstrates **good awareness** of cross-platform concerns in critical areas (atomic file operations, lifecycle directory resolution, path normalization). However, there are **gaps at the shell integration boundaries** where Unix assumptions are embedded.

### Systemic Vulnerability Patterns

1. **Shell Command Assumption Pattern**
   - Multiple files assume `python3` command exists
   - Shell scripts use bash-specific features
   - No Windows-native equivalents provided
   - **Root Cause:** Development primarily on macOS/Linux

2. **Documentation vs. Runtime Divergence**
   - Docstrings use Unix paths for examples
   - Actual runtime code handles cross-platform correctly
   - **Risk:** New contributors may write non-portable code following examples

3. **Test Coverage Gap**
   - No evidence of Windows CI testing
   - Cross-platform behavior untested in automated pipeline
   - **Risk:** Regressions may be introduced unknowingly

### Comparison with Threat Model

The portability issues identified do not represent direct security vulnerabilities but could lead to:

1. **Availability Impact:** Application may not function on Windows
2. **Integrity Impact:** Path handling issues could lead to file operations in wrong locations
3. **Confidentiality Impact:** None identified

### Recommendations for Security Architecture Evolution

1. **Short-term (1-2 weeks)**
   - Add `.gitattributes` for line ending consistency
   - Replace `python3` with platform-aware invocation in settings.json
   - Document Windows symlink requirements

2. **Medium-term (1 month)**
   - Add Windows CI runner to GitHub Actions
   - Create PowerShell equivalents of critical bash scripts
   - Add integration tests that run on Windows

3. **Long-term (Ongoing)**
   - Establish cross-platform testing as part of PR review
   - Add platform-specific test markers in pytest
   - Consider using Python-based tooling instead of shell scripts for better portability

### ASVS Verification Status

| Chapter | Relevance | Status |
|---------|-----------|--------|
| V1 - Architecture | Low | N/A - No security architecture concerns |
| V5 - Validation | Low | Path validation is cross-platform aware |
| V8 - Data Protection | Low | File operations are platform-aware |

### CWE Top 25 Applicability

| CWE ID | Applicability | Status |
|--------|--------------|--------|
| CWE-22 (Path Traversal) | Medium | Code normalizes paths; PORT-006 is low risk |
| CWE-78 (OS Command Injection) | Low | No user input in shell commands |
| CWE-426 (Untrusted Search Path) | Medium | PORT-001 could be affected if malicious `python3` in PATH |

---

## Appendix: Files Reviewed

| File | Review Status |
|------|---------------|
| `.claude/statusline.py` | Full review |
| `.claude/settings.json` | Full review |
| `scripts/migration/verify-platform.sh` | Full review |
| `scripts/migration/verify-symlinks.sh` | Full review |
| `src/infrastructure/adapters/persistence/atomic_file_adapter.py` | Full review |
| `src/infrastructure/adapters/persistence/filesystem_local_context_adapter.py` | Full review |
| `src/infrastructure/adapters/file_repository.py` | Full review |
| `src/infrastructure/adapters/configuration/lifecycle_dir_resolver.py` | Full review |
| `src/infrastructure/internal/file_store.py` | Full review |
| `src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py` | Partial review |
| `src/session_management/infrastructure/adapters/filesystem_project_adapter.py` | Full review |
| `src/session_management/infrastructure/adapters/os_environment_adapter.py` | Full review |
| `src/work_tracking/infrastructure/persistence/filesystem_event_store.py` | Partial review |
| `src/shared_kernel/jerry_uri.py` | Full review |
| `src/interface/cli/ast_commands.py` | Partial review |
| `pyproject.toml` | Full review |

---

*Analysis performed by eng-security agent per SSDF PW.7 (manual code review). All findings classified using CVSS 3.1 severity guidelines.*
