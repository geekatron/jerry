# Research: Cross-Platform Sync Strategies for .context/ → .claude/

> **PS ID:** PROJ-001-oss-release
> **Entry ID:** EN-206-SPIKE-001
> **Topic:** Cross-Platform Sync Strategies for .context/ to .claude/rules/ and .claude/patterns/
> **Workflow:** en206-context-distribution-20260202-001
> **Agent:** ps-researcher
> **Date:** 2026-02-02
> **Requested By:** User (EN-206 Context Distribution Strategy)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary-l0---eli5) | Simple explanation of findings |
| [Technical Details](#technical-implementation-details-l1---engineer) | Deep dive into each strategy |
| [Strategic Implications](#strategic-implications-l2---architect) | Trade-offs and architecture decisions |
| [Platform Compatibility Matrix](#platform-compatibility-matrix) | What works where |
| [Recommendation](#recommendation) | Final recommendation with rationale |

---

## Executive Summary (L0 - ELI5)

**Problem:** Jerry's behavioral rules live in `.context/` (canonical source, version-controlled). But Claude Code only loads rules from `.claude/rules/`. We need a way to sync these directories across macOS, Linux, AND Windows - without requiring admin privileges.

**Key Constraint:** Windows symlinks require either Developer Mode or admin rights. Many enterprise users have neither.

**Solution: Hybrid Platform-Aware Strategy**

```
┌─────────────────────────────────────────────────────────────────┐
│                  /bootstrap Skill Decision Tree                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Detect Platform                                                │
│        │                                                         │
│        ├──► macOS/Linux ──► Use Symlinks (native support)       │
│        │                                                         │
│        └──► Windows                                              │
│                 │                                                │
│                 ├──► Developer Mode ON ──► Use Symlinks         │
│                 │                                                │
│                 └──► Developer Mode OFF ──► Use Junction Points │
│                        (for directories, no admin needed)        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Analogy:** Think of it like connecting garden hoses. On macOS/Linux, you use standard couplers (symlinks). On Windows without admin, you use a special adapter (junction points) that does the same job.

---

## Technical Implementation Details (L1 - Engineer)

### Strategy 1: Symbolic Links (Symlinks)

**How It Works:**
A symlink is a file system object that points to another file or directory. It's a "shortcut" at the file system level.

```bash
# macOS/Linux - works natively
ln -s ../.context/rules .claude/rules

# Windows with Developer Mode or admin
mklink /D .claude\rules ..\.context\rules
```

**Platform Support:**

| Platform | Support | Admin Required | Notes |
|----------|---------|----------------|-------|
| macOS | ✅ Native | No | Full support since Mac OS X |
| Linux | ✅ Native | No | Full support in all kernels |
| Windows | ⚠️ Conditional | **Yes** (without Developer Mode) | Requires Developer Mode (Win 10 1703+) OR admin privileges |

**Windows Developer Mode:**
- Enabled via: Settings → Update & Security → For developers → Developer Mode
- Once enabled, symlinks work without admin
- **Problem:** Many enterprise environments disable this setting via Group Policy

**Pros:**
- Universal concept, well-understood
- Preserves directory structure
- Changes in source immediately reflected in target
- No file duplication (saves disk space)

**Cons:**
- Windows requires Developer Mode or admin
- Can break if source moved/deleted
- Some tools don't follow symlinks properly

**Industry Usage:**
- npm `node_modules` handling (uses symlinks for workspaces)
- pnpm package manager (extensive symlink usage)
- GNU Stow (symlink farm manager)

---

### Strategy 2: Junction Points (Windows Only)

**How It Works:**
Junction points are a Windows-specific feature similar to symlinks but ONLY for directories. Critically, they do NOT require admin privileges.

```cmd
# Windows - NO admin required
mklink /J .claude\rules ..\.context\rules
```

**Key Difference from Symlinks:**

| Feature | Symlink (`/D`) | Junction (`/J`) |
|---------|----------------|-----------------|
| Admin Required (no Dev Mode) | Yes | **No** |
| Works for Files | Yes | No (directories only) |
| Works Across Drives | Yes | No (same volume only) |
| Relative Paths | Yes | **No** (requires absolute paths) |
| Network Paths | Limited | No |

**Platform Support:**

| Platform | Support | Admin Required | Notes |
|----------|---------|----------------|-------|
| macOS | ❌ N/A | - | Not applicable |
| Linux | ❌ N/A | - | Not applicable |
| Windows | ✅ Native | **No** | Works since Windows 2000/NTFS |

**Absolute Path Requirement:**
Junction points require absolute paths. The `/bootstrap` skill must resolve paths:

```python
import os
from pathlib import Path

def create_junction(source: Path, target: Path) -> None:
    """Create Windows junction point."""
    # Junction requires absolute paths
    abs_source = source.resolve()
    abs_target = target.resolve()

    # Use mklink /J
    os.system(f'mklink /J "{abs_target}" "{abs_source}"')
```

**Pros:**
- **NO admin privileges required** - This is the key advantage
- Works on all Windows versions with NTFS (since Windows 2000)
- Transparent to applications (looks like a real directory)
- Changes in source immediately reflected in target

**Cons:**
- Windows-only (requires platform detection)
- Directories only (not files)
- Requires absolute paths
- Same volume only (source and target must be on same drive)

**Industry Usage:**
- [symlink-dir](https://www.npmjs.com/package/symlink-dir) npm package automatically uses junctions on Windows
- Many Windows dev tools silently fall back to junctions

---

### Strategy 3: File Copy with Drift Detection

**How It Works:**
Simply copy files from `.context/` to `.claude/`. Detect when source changes and warn user to re-sync.

```python
import shutil
import hashlib
from pathlib import Path

def sync_with_copy(source: Path, target: Path) -> None:
    """Copy files with hash-based drift detection."""
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)

    # Store hash for drift detection
    hash_file = target / ".sync-hash"
    hash_value = compute_directory_hash(source)
    hash_file.write_text(hash_value)

def check_drift(source: Path, target: Path) -> bool:
    """Check if source has changed since last sync."""
    hash_file = target / ".sync-hash"
    if not hash_file.exists():
        return True
    stored_hash = hash_file.read_text()
    current_hash = compute_directory_hash(source)
    return stored_hash != current_hash
```

**Platform Support:**

| Platform | Support | Admin Required | Notes |
|----------|---------|----------------|-------|
| macOS | ✅ Works | No | Native Python/shell |
| Linux | ✅ Works | No | Native Python/shell |
| Windows | ✅ Works | No | Native Python/shell |

**Pros:**
- Works on ALL platforms with no special requirements
- No permissions issues
- Simple to understand and debug
- Files are "real" - no symlink-unaware tool issues

**Cons:**
- **File duplication** - Wastes disk space
- **Drift risk** - Changes don't auto-propagate
- **Manual sync** - User must re-run bootstrap after Jerry updates
- Potential for user modifications to be overwritten

**Drift Detection Approaches:**

| Approach | Complexity | Reliability |
|----------|------------|-------------|
| Hash comparison | Medium | High |
| Modification timestamp | Low | Medium (unreliable across platforms) |
| Git status | Medium | High (if files are tracked) |
| File count/size | Low | Low |

**Industry Usage:**
- chezmoi (dotfiles manager) - uses templated copies with drift detection
- Many build tools (webpack, rollup) copy files to dist/

---

### Strategy 4: Git Submodules

**How It Works:**
Store rules in a separate git repository and include it as a submodule.

```bash
# Add submodule
git submodule add https://github.com/jerry/rules.git .context/rules

# Users clone with submodules
git clone --recurse-submodules https://github.com/project/repo.git
```

**Platform Support:**

| Platform | Support | Admin Required | Notes |
|----------|---------|----------------|-------|
| macOS | ✅ Works | No | Git required |
| Linux | ✅ Works | No | Git required |
| Windows | ✅ Works | No | Git required |

**Pros:**
- Cross-platform (git is universal)
- Version control built-in
- Explicit dependency management
- Users can pin specific rule versions

**Cons:**
- **Complexity** - Submodules are notoriously confusing
- **Extra step** - Users must remember `--recurse-submodules`
- **Still doesn't solve .claude/ syncing** - Submodule lands in `.context/`, still need to sync to `.claude/`
- Harder for non-git users

**Industry Usage:**
- Large monorepos (Google, Facebook) use similar patterns
- Some plugin systems (vim plugins, emacs packages)

**Verdict:** Submodules solve VERSION CONTROL but not the .context/ → .claude/ sync problem. Still need another strategy for the final sync.

---

### Strategy 5: Bootstrap Script with Platform Detection

**How It Works:**
A `/bootstrap` skill that detects the platform and chooses the best strategy automatically.

```python
import platform
import os
from pathlib import Path

def bootstrap_sync(source: Path, target: Path) -> str:
    """Platform-aware sync strategy."""
    system = platform.system()

    if system == "Darwin" or system == "Linux":
        # Use symlinks on macOS/Linux
        return create_symlink(source, target)

    elif system == "Windows":
        # Check if Developer Mode is enabled
        if windows_developer_mode_enabled():
            return create_symlink(source, target)
        else:
            # Fall back to junction points
            return create_junction(source, target)

    else:
        # Unknown platform - use file copy as fallback
        return copy_with_drift_detection(source, target)

def windows_developer_mode_enabled() -> bool:
    """Check if Windows Developer Mode is enabled."""
    import winreg
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock"
        )
        value, _ = winreg.QueryValueEx(key, "AllowDevelopmentWithoutDevLicense")
        return value == 1
    except (FileNotFoundError, OSError):
        return False
```

**Decision Tree:**

```
bootstrap_sync()
    │
    ├── macOS ──────────────► Symlink (ln -s)
    │
    ├── Linux ──────────────► Symlink (ln -s)
    │
    └── Windows
            │
            ├── Developer Mode ON ──► Symlink (mklink /D)
            │
            └── Developer Mode OFF ─► Junction (mklink /J)
```

**Platform Support:**

| Platform | Strategy Used | Admin Required |
|----------|---------------|----------------|
| macOS | Symlink | No |
| Linux | Symlink | No |
| Windows (Dev Mode) | Symlink | No |
| Windows (No Dev Mode) | Junction | **No** |

**Pros:**
- **Works on ALL platforms without admin**
- Best strategy automatically selected
- Single command for users (`/bootstrap`)
- Aligns with Jerry personality (friendly, helpful)

**Cons:**
- More complex implementation
- Must handle edge cases (WSL, Cygwin, etc.)
- Testing required on all platforms

**Industry Usage:**
- npm packages like `symlink-dir` use this exact pattern
- Cross-platform build tools (CMake, Meson) detect platform capabilities

---

## Strategic Implications (L2 - Architect)

### One-Way Door Decisions

1. **Directory Structure Choice:** Choosing `.context/` as canonical source is a one-way door. Once users have projects with `.context/`, changing it breaks compatibility.

2. **Sync Mechanism:** The sync mechanism affects user experience and maintenance burden. Choosing wrong creates tech debt.

### Trade-off Analysis

| Criterion | Symlinks | Junctions | File Copy | Git Submodules | Bootstrap Script |
|-----------|----------|-----------|-----------|----------------|------------------|
| macOS Support | ✅ Native | ❌ N/A | ✅ Works | ✅ Works | ✅ Best of all |
| Linux Support | ✅ Native | ❌ N/A | ✅ Works | ✅ Works | ✅ Best of all |
| Windows (no admin) | ❌ Needs Dev Mode | ✅ **No admin** | ✅ Works | ✅ Works | ✅ **No admin** |
| Auto-propagate changes | ✅ Yes | ✅ Yes | ❌ Manual | ⚠️ Pull required | ✅ Yes |
| Disk space | ✅ Efficient | ✅ Efficient | ❌ Duplicates | ✅ Efficient | ✅ Efficient |
| User complexity | Low | Medium | Low | **High** | **Low** |
| Implementation complexity | Low | Low | Medium | High | **Medium** |
| Cross-platform uniform | ❌ No | ❌ Windows only | ✅ Yes | ✅ Yes | ✅ Yes (abstracted) |

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Windows users can't use symlinks | High | High | Junction points fallback |
| Users modify synced files | Medium | Medium | Drift detection, warnings |
| Users forget to bootstrap | High | Medium | Clear error messages, auto-detect |
| Junction path issues (relative) | Medium | Low | Always use absolute paths |
| WSL/Cygwin edge cases | Low | Low | Document known issues |

### Enterprise Considerations

Many enterprise environments:
- Disable Developer Mode via Group Policy
- Restrict admin access
- Use network drives (junctions don't work across drives)

**Recommendation:** File copy fallback for network drives.

---

## Platform Compatibility Matrix

### Complete Matrix

| Strategy | macOS | Linux | Windows (Dev Mode) | Windows (No Dev Mode) | Windows (Network Drive) |
|----------|-------|-------|-------------------|----------------------|------------------------|
| Symlinks | ✅ | ✅ | ✅ | ❌ | ⚠️ Limited |
| Junctions | ❌ | ❌ | ✅ | ✅ | ❌ |
| File Copy | ✅ | ✅ | ✅ | ✅ | ✅ |
| Git Submodules | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Bootstrap Script** | ✅ | ✅ | ✅ | ✅ | ✅ (copy fallback) |

### Detection Logic

```python
def detect_best_strategy(source: Path, target: Path) -> str:
    """Determine optimal sync strategy."""
    system = platform.system()

    # macOS/Linux: symlinks always work
    if system in ("Darwin", "Linux"):
        return "symlink"

    # Windows: check conditions
    if system == "Windows":
        # Network drive? Use copy
        if is_network_path(source) or is_network_path(target):
            return "copy"

        # Different drives? Use copy (junctions don't work)
        if source.drive != target.drive:
            return "copy"

        # Developer Mode? Use symlinks
        if windows_developer_mode_enabled():
            return "symlink"

        # Default: junctions
        return "junction"

    # Unknown: safe fallback
    return "copy"
```

---

## 5W2H Analysis

### What
Five strategies for syncing `.context/` to `.claude/`:
1. Symbolic Links (macOS/Linux native, Windows with Dev Mode)
2. Junction Points (Windows without admin)
3. File Copy (universal fallback)
4. Git Submodules (version control, not sync)
5. Bootstrap Script (platform-aware abstraction)

### Why
- Claude Code only loads rules from `.claude/rules/`
- Jerry's canonical rules live in `.context/` (version-controlled, distributable)
- Windows symlinks require admin/Dev Mode, which enterprise users lack
- Need cross-platform solution that "just works"

### Who
- **Jerry maintainers:** Implement bootstrap skill
- **Jerry users:** Run `/bootstrap` once per project
- **Enterprise users:** Benefit from no-admin solution

### When
- **Bootstrap:** Run once when starting a Jerry project
- **Re-sync:** Run after Jerry updates (if using file copy)
- **Check:** Validate sync status at session start (optional)

### Where
- **Source:** `.context/rules/`, `.context/patterns/`
- **Target:** `.claude/rules/`, `.claude/patterns/`
- **Bootstrap skill:** `skills/bootstrap/`

### How
Platform-aware `/bootstrap` skill:
1. Detect platform
2. Check capabilities (Dev Mode, drive types)
3. Select optimal strategy
4. Execute sync
5. Verify success
6. Report to user (with Jerry personality)

### How Much
- **Implementation effort:** 3 story points (TASK-002, TASK-003)
- **User effort:** One command (`/bootstrap`)
- **Disk space:** Minimal (symlinks/junctions don't duplicate)
- **Maintenance:** Low (auto-updates with symlinks/junctions)

---

## Industry Best Practices and Prior Art

### npm / pnpm
- npm workspaces use symlinks for local packages
- pnpm uses symlinks extensively for deduplication
- `symlink-dir` package auto-detects platform, uses junctions on Windows

### chezmoi (Dotfiles Manager)
- Cross-platform dotfiles management
- Uses templating + copy approach
- Supports encryption, password manager integration
- Tracks drift via git

### GNU Stow
- "Symlink farm manager"
- Creates symlinks to manage dotfiles
- UNIX-focused, limited Windows support

### VS Code / Cursor / Windsurf
- Use file watchers for configuration sync
- Store settings in platform-specific locations
- Don't rely on symlinks for cross-platform

---

## Recommendation

### Primary Recommendation: Hybrid Bootstrap Script (Strategy 5)

**Implement a `/bootstrap` skill that:**

1. **Detects platform** automatically
2. **Uses optimal strategy** per platform:
   - macOS/Linux → Symlinks
   - Windows + Dev Mode → Symlinks
   - Windows - Dev Mode → Junction Points
   - Network drives → File Copy (with drift detection)
3. **Reports in Jerry voice** ("Fresh tracks await!")
4. **Provides verification** (`/bootstrap --check`)

### Implementation Priority

| Priority | Item | Rationale |
|----------|------|-----------|
| P0 | Symlinks (macOS/Linux) | Covers most developers |
| P0 | Junction Points (Windows) | Covers enterprise Windows users |
| P1 | File Copy fallback | Covers edge cases |
| P2 | Drift detection | Nice-to-have for copy strategy |
| P3 | Git submodules | Out of scope for MVP |

### Decision Criteria Met

| Criterion | Strategy 5 | Notes |
|-----------|------------|-------|
| Works on macOS | ✅ | Via symlinks |
| Works on Linux | ✅ | Via symlinks |
| Works on Windows without admin | ✅ | Via junction points |
| No extra dependencies | ✅ | Python stdlib only |
| User-friendly | ✅ | Single command |
| Aligns with Jerry personality | ✅ | Fun, helpful messaging |

---

## Deliverables

Based on this research, the following work items should proceed:

| Work Item | Status | Next Action |
|-----------|--------|-------------|
| SPIKE-001 | COMPLETE | This document |
| TASK-001 | UNBLOCKED | Move rules/patterns to .context/ |
| TASK-002 | UNBLOCKED | Implement sync mechanism (bootstrap script) |
| TASK-003 | UNBLOCKED | Create /bootstrap skill with Jerry personality |

### Decision Required

**DEC-001: Which sync strategy to implement?**

**Recommendation:** Hybrid Bootstrap Script (Strategy 5) with:
- Symlinks for macOS/Linux
- Junction points for Windows (no admin)
- File copy fallback for network drives

---

## References

### Primary Sources

1. **Windows Symlinks Documentation**
   - Microsoft Docs: [mklink command](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/mklink)
   - Windows 10 1703 Developer Mode: Allows symlinks without admin

2. **Junction Points**
   - Microsoft Docs: [Hard Links and Junctions](https://docs.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
   - No admin required since Windows 2000

3. **symlink-dir npm package**
   - https://www.npmjs.com/package/symlink-dir
   - Uses junctions on Windows automatically

4. **chezmoi**
   - https://www.chezmoi.io/
   - Cross-platform dotfiles management

5. **GNU Stow**
   - https://www.gnu.org/software/stow/
   - Symlink farm manager

### Internal Sources

6. **EN-206 Context Distribution Strategy** - Parent enabler
7. **research-plugin-claude-folder-loading.md** - Establishes need for this research
8. **Jerry Persona Research** - Voice/tone for /bootstrap skill

---

*Research artifact generated by ps-researcher agent for SPIKE-001.*
*Date: 2026-02-02*
*Agent: ps-researcher*
*Constitutional Compliance: P-001 (Truth), P-002 (Persistence), P-004 (Provenance)*
