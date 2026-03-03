# Platform Portability Issue Drafts

**Source:** PORT-001 Portability Analysis
**Date:** 2026-02-26
**For Human Review Before Filing**

---

## Issue 1: PORT-001 — Hardcoded `python3` command in status line configuration

### Title
`bug: statusLine command uses python3 which fails on Windows`

### Labels
`bug`, `portability`, `windows`

### Body

## Summary

The `.claude/settings.json` status line configuration uses `python3` as the command, which is not available on Windows systems where Python is typically invoked via `python`, `py`, or `py -3`.

## Environment

- **Affected Platforms:** Windows 10/11
- **File:** `.claude/settings.json`
- **Line:** 25

## Current Behavior

```json
"statusLine": {
  "type": "command",
  "command": "python3 .claude/statusline.py",
  "padding": 0
}
```

When Jerry is used on Windows, the status line fails to execute because `python3` is not recognized as a command.

## Expected Behavior

The status line should work on Windows without requiring users to manually create aliases or modify PATH.

## Reproduction Steps

1. Install Jerry on Windows 10/11
2. Ensure Python is installed via official installer (which registers `python` not `python3`)
3. Run Claude Code with Jerry
4. Observe status line failure

## Proposed Solution

Change the command to use `python` which works on both Unix (symlink) and Windows:

```json
"command": "python .claude/statusline.py"
```

Or use a platform-aware wrapper that detects the correct Python command.

## Impact

- **Severity:** Major
- **User Impact:** Windows users cannot use the status line feature
- **Workaround:** Users can manually create `python3` alias or modify settings.json

## Acceptance Criteria

- [ ] Status line works on Windows 10/11 with standard Python installation
- [ ] Status line continues to work on macOS and Linux
- [ ] CI includes Windows runner to prevent regression

---

## Issue 2: PORT-003 — Migration scripts require bash with no Windows alternative

### Title
`enhancement: Add PowerShell equivalents for migration scripts`

### Labels
`enhancement`, `portability`, `windows`, `documentation`

### Body

## Summary

The migration scripts (`scripts/migration/verify-platform.sh`, `scripts/migration/verify-symlinks.sh`) use bash-specific syntax and features with no Windows-native alternatives provided.

## Environment

- **Affected Platforms:** Windows 10/11 (without WSL)
- **Files:**
  - `scripts/migration/verify-platform.sh`
  - `scripts/migration/verify-symlinks.sh`

## Current Behavior

The scripts use:
- `#!/bin/bash` shebang
- Bash arrays (`EXCLUDED_DIRS=(...)`)
- Bash-specific test syntax (`[[ ]]`)
- Process substitution and pipefail

Windows users without WSL, Git Bash, or Cygwin cannot run these scripts.

## Expected Behavior

Migration verification should be possible on Windows systems using native tools.

## Proposed Solutions

**Option A (Recommended):** Provide PowerShell equivalents
- `scripts/migration/Verify-Platform.ps1`
- `scripts/migration/Verify-Symlinks.ps1`

**Option B:** Convert to Python scripts for cross-platform compatibility
- `scripts/migration/verify_platform.py`
- `scripts/migration/verify_symlinks.py`

**Option C:** Document WSL requirement clearly

## Impact

- **Severity:** Major
- **User Impact:** Windows users cannot verify migration success
- **Workaround:** Install WSL or Git Bash

## Acceptance Criteria

- [ ] Windows users can verify platform setup without WSL
- [ ] Script functionality is equivalent across platforms
- [ ] README documents platform-specific instructions

---

## Issue 3: PORT-004 — Repository symlinks require elevated privileges on Windows

### Title
`docs: Document Windows symlink requirements for .claude directory`

### Labels
`documentation`, `portability`, `windows`

### Body

## Summary

The `.claude/` directory contains symbolic links (`patterns -> ../.context/patterns`, `rules -> ../.context/rules`) that require special handling on Windows.

## Environment

- **Affected Platforms:** Windows 10/11
- **Directory:** `.claude/`
- **Symlinks:**
  - `patterns -> ../.context/patterns`
  - `rules -> ../.context/rules`

## Current Behavior

On Windows, creating or cloning repositories with symlinks requires either:
- Administrator privileges
- Developer Mode enabled
- Git configured with `core.symlinks=true`

Without these, symlinks may be cloned as text files containing the target path, breaking the Jerry configuration.

## Expected Behavior

Clear documentation should guide Windows users through symlink setup, with fallback options for environments where symlinks cannot be used.

## Proposed Solutions

1. **Documentation:** Add Windows symlink setup instructions to README
2. **Git Configuration:** Add `.gitattributes` entry for symlink handling
3. **Setup Script:** Provide a setup script that detects Windows and creates directory junctions if needed
4. **Alternative Architecture:** Consider using file copies or imports instead of symlinks for critical paths

## Verification

```bash
# Check if symlinks are working
ls -la .claude/
# Should show actual symlinks, not text files

# On Windows, verify with:
git config core.symlinks
# Should return 'true'
```

## Impact

- **Severity:** Major
- **User Impact:** Windows users may have non-functional Jerry configuration
- **Workaround:** Enable Developer Mode or run `git config core.symlinks true` before clone

## Acceptance Criteria

- [ ] README includes Windows symlink setup instructions
- [ ] Repository includes `.gitattributes` with symlink handling
- [ ] (Optional) Setup script provides automatic symlink/junction creation
- [ ] Documentation explains how to verify symlinks are working

---

## Issue 4: PORT-005 — Missing .gitattributes for line ending consistency

### Title
`enhancement: Add .gitattributes for cross-platform line ending consistency`

### Labels
`enhancement`, `portability`, `developer-experience`

### Body

## Summary

The repository lacks a `.gitattributes` file to enforce line ending normalization, which can cause issues when contributors work on different platforms.

**Source:** PORT-001 Portability Analysis (2026-02-26)

## Environment

- **Affected Platforms:** All (Windows, macOS, Linux)
- **Missing File:** `.gitattributes`
- **Reference:** [Git Attributes Documentation](https://git-scm.com/docs/gitattributes)

## Current Behavior

Without `.gitattributes`, Git uses default line ending behavior which may:
- Produce spurious diffs when switching between platforms
- Cause shell scripts to fail if checked out with CRLF on Unix
- Create inconsistent file checksums across platforms

**Evidence:**
```bash
$ ls .gitattributes
ls: .gitattributes: No such file or directory
```

## Expected Behavior

Line endings should be normalized consistently regardless of contributor's platform:
- Repository stores files with LF (Unix standard)
- Working copy converts as appropriate for platform
- Shell scripts always LF (to prevent execution failures)

## Proposed Solution

Add `.gitattributes` to repository root per [Git Attributes specification](https://git-scm.com/docs/gitattributes):

```gitattributes
# Auto-detect text files and normalize to LF
* text=auto

# Force specific file types to LF (Unix style)
*.py text eol=lf
*.sh text eol=lf
*.json text eol=lf
*.md text eol=lf
*.yaml text eol=lf
*.yml text eol=lf
*.toml text eol=lf

# Force Windows-native scripts to CRLF
*.bat text eol=crlf
*.ps1 text eol=crlf

# Binary files
*.png binary
*.jpg binary
*.gif binary
```

## Migration for Existing Files

After adding `.gitattributes`, normalize existing files:
```bash
# Stage all files
git add --renormalize .

# Commit the line ending fixes
git commit -m "chore: normalize line endings"
```

## Verification

After adding `.gitattributes`:
```bash
git check-attr -a -- *.py *.sh
# Should show eol: lf
```

## Impact

- **Severity:** Minor
- **User Impact:** Potential for confusing diffs and script failures
- **Workaround:** Manual git config per clone

## Acceptance Criteria

- [ ] `.gitattributes` file added to repository root
- [ ] Python, shell, and config files use LF endings
- [ ] Windows scripts (if any) use CRLF endings
- [ ] CI includes `git diff --check` step to verify no mixed line endings on PR
- [ ] Fresh clone on Windows produces CRLF in `.ps1` files and LF in `.sh` files (verify with `file` command or hex editor)
- [ ] Fresh clone on macOS/Linux produces LF for all text files (verify with `file` command)
- [ ] Existing repository files normalized via `git add --renormalize .`

---

## Issue 5: PORT-006 — Hardcoded path separator in file repository

### Title
`bug: file_repository.py uses hardcoded forward slash instead of pathlib`

### Labels
`bug`, `portability`, `code-quality`

### Body

## Summary

The `_get_file_path` method in `file_repository.py` uses a hardcoded forward slash for path construction instead of `os.path.join` or `pathlib.Path`.

## Environment

- **Affected Platforms:** Potentially Windows
- **File:** `src/infrastructure/adapters/file_repository.py`
- **Line:** 95

## Current Behavior

```python
def _get_file_path(self, aggregate_id: TId) -> str:
    safe_id = self._sanitize_id(str(aggregate_id))
    return f"{self._base_path}/{safe_id}.json"
```

While Python's `Path` class often handles mixed separators, this pattern is inconsistent with best practices and could cause issues in edge cases.

## Expected Behavior

Path construction should use platform-aware methods.

## Proposed Solution

```python
def _get_file_path(self, aggregate_id: TId) -> str:
    safe_id = self._sanitize_id(str(aggregate_id))
    return str(Path(self._base_path) / f"{safe_id}.json")
```

## Impact

- **Severity:** Minor
- **User Impact:** Potential for path-related issues on Windows
- **Workaround:** None needed currently (Python handles mixed separators)

## Acceptance Criteria

- [ ] Path construction uses `pathlib.Path` or `os.path.join`
- [ ] Existing tests pass on all platforms
- [ ] Unit test added to verify Windows path handling

---

## Issue 6: PORT-013 — macOS symlink resolution falls back to python3 without alternatives

### Title
`bug: verify-symlinks.sh macOS fallback assumes python3 in PATH`

### Labels
`bug`, `portability`, `macos`

### Body

## Summary

The `verify-symlinks.sh` script uses a Python fallback for `readlink -f` on macOS (since BSD readlink doesn't support `-f`), but doesn't check for `greadlink` (GNU readlink from Homebrew) first.

## Environment

- **Affected Platforms:** macOS
- **File:** `scripts/migration/verify-symlinks.sh`
- **Lines:** 168-178

## Current Behavior

```bash
if [[ "$(uname)" == "Darwin" ]]; then
    target=$(python3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$symlink" 2>/dev/null) || true
else
    target=$(readlink -f "$symlink" 2>/dev/null) || true
fi
```

If `python3` is not in PATH (e.g., only `python` available, or using pyenv with different naming), the script fails silently.

## Expected Behavior

The script should try multiple fallback options:
1. `greadlink -f` (if Homebrew coreutils installed)
2. `python3`
3. `python`

## Proposed Solution

```bash
if [[ "$(uname)" == "Darwin" ]]; then
    if command -v greadlink &>/dev/null; then
        target=$(greadlink -f "$symlink" 2>/dev/null)
    elif command -v python3 &>/dev/null; then
        target=$(python3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$symlink" 2>/dev/null)
    elif command -v python &>/dev/null; then
        target=$(python -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$symlink" 2>/dev/null)
    fi
else
    target=$(readlink -f "$symlink" 2>/dev/null) || true
fi
```

## Impact

- **Severity:** Major
- **User Impact:** macOS users without `python3` command cannot run verification
- **Workaround:** Ensure `python3` is in PATH

## Acceptance Criteria

- [ ] Script checks for `greadlink` before falling back to Python
- [ ] Script tries both `python3` and `python`
- [ ] Script provides helpful error message if no method works

---

## Issue 7: PORT-002 — Docstring examples use hardcoded /tmp paths

### Title
`docs: Replace /tmp with tempfile.gettempdir() in docstring examples`

### Labels
`documentation`, `portability`, `code-quality`

### Body

## Summary

Several docstring examples use `/tmp` which does not exist on Windows systems.

## Environment

- **Affected Platforms:** Windows (documentation issue)
- **Files:**
  - `src/session_management/infrastructure/adapters/event_sourced_session_repository.py:335`
  - `src/work_tracking/infrastructure/persistence/filesystem_event_store.py:367`
  - `src/work_tracking/infrastructure/adapters/event_sourced_work_item_repository.py:428`
  - `src/infrastructure/internal/file_store.py:82-83`

## Current Behavior

```python
# From file_store.py
>>> store.write("/tmp/data.json", b'{"key": "value"}')
>>> data = store.read("/tmp/data.json")
```

## Expected Behavior

Examples should use cross-platform temp directory:

```python
>>> import tempfile
>>> from pathlib import Path
>>> temp_path = Path(tempfile.gettempdir()) / "data.json"
>>> store.write(str(temp_path), b'{"key": "value"}')
```

## Impact

- **Severity:** Minor
- **User Impact:** Documentation examples are incorrect for Windows users
- **Workaround:** Users can mentally substitute appropriate temp path

## Acceptance Criteria

- [ ] All `/tmp` references in docstrings replaced with platform-aware examples
- [ ] Doctest examples work on all platforms

---

*Issue drafts generated from PORT-001 analysis. Pending adversarial quality review.*
