# BUG-013: SessionStart Hook `uv sync` Runs in Wrong Directory

> **Type:** bug
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-20
> **Parent:** EPIC-001-oss-release
> **Owner:** Claude
> **Found In:** 0.7.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Steps to Reproduce](#steps-to-reproduce) | Schema-required reproduction stub |
| [Reproduction Steps](#reproduction-steps) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Investigation and root cause details |
| [Fix Description](#fix-description) | Solution approach and changes made |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

The SessionStart hook's `uv sync` command on line 10 of `hooks/hooks.json` runs without `--directory ${CLAUDE_PLUGIN_ROOT}`, causing it to search for `pyproject.toml` in the current working directory instead of the Jerry plugin directory. When the CWD is a different repository (e.g., a consumer repo without its own `pyproject.toml`), `uv sync` fails and the `&&` short-circuit prevents the actual hook script from executing.

**Key Details:**
- **Symptom:** `uv sync` fails with `error: No pyproject.toml found in current directory or any parent directory` when CWD is not the Jerry repo. The SessionStart hook script never executes.
- **Frequency:** Always, when Jerry plugin is used from a repository that lacks its own `pyproject.toml` or has an incompatible one.
- **Workaround:** The second matched hook (if present) may succeed independently, masking the failure. Sessions sometimes appear to start normally due to duplicate hook matching.

---

## Steps to Reproduce

See [Reproduction Steps](#reproduction-steps) below for full details.

---

## Reproduction Steps

### Prerequisites

- Jerry plugin installed in Claude Code
- A separate repository (consumer repo) that does not contain a `pyproject.toml` at its root or any parent directory

### Steps to Reproduce

1. Open Claude Code in a consumer repository (e.g., `G.N.A.R/Forge`)
2. Start a new session (triggers SessionStart hook)
3. Observe hook execution output

### Expected Result

`uv sync` resolves `pyproject.toml` from the Jerry plugin directory (`${CLAUDE_PLUGIN_ROOT}`), installs/syncs dependencies, then runs `session_start_hook.py` successfully.

### Actual Result

`uv sync` searches CWD upward for `pyproject.toml`, fails with exit code 1, and the `&&` operator short-circuits — `session_start_hook.py` never executes. The session starts without Jerry framework initialization.

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | macOS (Darwin 24.6.0) |
| **Runtime** | Claude Code CLI |
| **Application Version** | Jerry 0.7.0 |
| **Configuration** | Jerry plugin installed via Claude Code marketplace/plugins |

---

## Root Cause Analysis

### Investigation Summary

Comparison of line 10 with all other hook commands in `hooks/hooks.json` reveals the inconsistency immediately. Lines 21, 33, and 44 all use `uv run --directory ${CLAUDE_PLUGIN_ROOT}`, correctly scoping uv to the plugin's `pyproject.toml`. Line 10 chains two commands:

```
uv sync && uv run --directory ${CLAUDE_PLUGIN_ROOT} ...
```

The second command correctly uses `--directory`, but the first (`uv sync`) does not.

### Root Cause

**Missing `--directory ${CLAUDE_PLUGIN_ROOT}` flag on the `uv sync` command.** The `uv sync` call defaults to searching CWD upward for `pyproject.toml`, which fails when the CWD is not the Jerry plugin directory.

### Contributing Factors

- Shell `&&` semantics: `A && B` only runs B if A exits 0. The `uv sync` failure (exit 1) prevents `session_start_hook.py` from ever executing.
- The bug is partially masked because Claude Code may match multiple hooks for the same event. If a second SessionStart hook exists and succeeds, the session appears to work despite this hook failing.
- No other hook command in the file has a bare `uv sync` — this is the only two-command chain, making it a unique case that was likely overlooked during development.

---

## Fix Description

### Solution Approach

Add `--directory ${CLAUDE_PLUGIN_ROOT}` to the `uv sync` command so it resolves `pyproject.toml` from the plugin root, consistent with all other `uv` invocations in the file.

### Changes Made

- Added `--directory ${CLAUDE_PLUGIN_ROOT}` to the `uv sync` call in the SessionStart hook command

### Code References

| File | Change Description |
|------|-------------------|
| `hooks/hooks.json:10` | `uv sync` → `uv sync --directory ${CLAUDE_PLUGIN_ROOT}` |

**Before:**
```json
"command": "uv sync && uv run --directory ${CLAUDE_PLUGIN_ROOT} ${CLAUDE_PLUGIN_ROOT}/scripts/session_start_hook.py"
```

**After:**
```json
"command": "uv sync --directory ${CLAUDE_PLUGIN_ROOT} && uv run --directory ${CLAUDE_PLUGIN_ROOT} ${CLAUDE_PLUGIN_ROOT}/scripts/session_start_hook.py"
```

---

## Acceptance Criteria

### Fix Verification

- [x] `uv sync --directory ${CLAUDE_PLUGIN_ROOT}` added to SessionStart hook command
- [x] All `uv` invocations in `hooks/hooks.json` now consistently use `--directory ${CLAUDE_PLUGIN_ROOT}`
- [ ] SessionStart hook executes successfully when CWD is a consumer repo without `pyproject.toml`
- [ ] No regression: SessionStart hook still works when CWD is the Jerry repo itself

### Quality Checklist

- [ ] Existing tests still passing
- [ ] No new issues introduced

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-001-oss-release](../EPIC-001-oss-release.md)

### Related Items

- **GitHub Issue:** [geekatron/jerry#46](https://github.com/geekatron/jerry/issues/46)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Initial report. `uv sync` missing `--directory` flag on SessionStart hook. |
| 2026-02-20 | Claude | in_progress | Root cause confirmed. Fix applied to `hooks/hooks.json`. |
