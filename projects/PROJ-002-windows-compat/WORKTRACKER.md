# PROJ-002: Windows Compatibility - Work Tracker

> **Project:** PROJ-002-windows-compat
> **Status:** completed
> **Created:** 2026-02-10
> **Updated:** 2026-02-26
> **Branch:** proj/windows-compat (rebased on main with PR #4 merged)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Epic Overview](#epic-overview) | High-level epic and feature summary |
| [Completed Items](#completed-items) | Work already merged via PR #4 + PR #7 |
| [Remaining Work](#remaining-work) | Low-priority items still pending |
| [Progress Summary](#progress-summary) | Overall completion status |
| [History](#history) | Change log |

---

## Epic Overview

### EPIC-001: Windows Compatibility

> **Status:** completed
> **Priority:** high
> **Created:** 2026-02-10

Make Jerry fully functional on Windows without requiring WSL or Git Bash.

**Branch:** `proj/windows-compat` (rebased on main - includes all PR #4 fixes)

---

## Completed Items

### PR #4: fix/windows-fcntl-to-filelock (merged to main)

#### FEAT-001: Cross-Platform File Locking (CRITICAL)

> **Status:** completed
> **Completed:** 2026-02-09 (PR #4)

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Replace fcntl with filelock in atomic_file_adapter.py | completed |
| TASK-002 | Replace fcntl with filelock in filesystem_event_store.py | completed |
| TASK-003 | Add Windows retry logic for os.replace() | completed |

#### FEAT-002: UTF-8 Statusline Encoding

> **Status:** completed
> **Completed:** 2026-02-09 (PR #4)

| ID | Title | Status |
|----|-------|--------|
| TASK-004 | Add UTF-8 encoding wrapper in statusline.py | completed |

#### FEAT-003: Cross-Platform Pre-Commit Hooks (CRITICAL)

> **Status:** completed
> **Completed:** 2026-02-09 (PR #4)

| ID | Title | Status |
|----|-------|--------|
| TASK-005 | Replace .venv/bin/pyright with uv run pyright | completed |
| TASK-006 | Replace .venv/bin/pip-audit with uv run pip-audit | completed |
| TASK-007 | Fix session_start_hook.py error message | completed |

#### FEAT-004: Path Handling in Tests

> **Status:** completed
> **Completed:** 2026-02-09 (PR #4)

| ID | Title | Status |
|----|-------|--------|
| TASK-008 | Fix path assertions in test_config_path.py | completed |
| TASK-009 | Fix path assertion in test_main.py | completed |

#### FEAT-005: CI Test Robustness

> **Status:** completed
> **Completed:** 2026-02-09 (PR #4)

| ID | Title | Status |
|----|-------|--------|
| TASK-010 | Use tmp_path for scan projects test | completed |
| TASK-011 | Skip VTT perf test when no golden datasets | completed |
| TASK-012 | Skip project validation when files missing | completed |
| TASK-013 | Ensure projects/ dir for CLI subprocess tests | completed |

#### FEAT-006: Schema Fix

> **Status:** completed
> **Completed:** 2026-02-09 (PR #4)

| ID | Title | Status |
|----|-------|--------|
| TASK-014 | Add keywords property to marketplace schema | completed |

#### FEAT-007: Windows Developer Documentation

> **Status:** completed
> **Completed:** 2026-02-09 (PR #4)

| ID | Title | Status |
|----|-------|--------|
| TASK-015 | Add Windows setup instructions to CONTRIBUTING.md | completed |
| TASK-016 | Update INSTALLATION.md with cross-platform commands | completed |

### PR #7: proj/windows-compat (open)

#### FEAT-008: Missing UTF-8 Encoding on File I/O (HIGH)

> **Status:** completed
> **Completed:** 2026-02-11 (PR #7)

| ID | Title | Status |
|----|-------|--------|
| TASK-017 | Add encoding="utf-8" to chunker.py write_text | completed |
| TASK-018 | Add encoding="utf-8" to parse_transcript_command_handler.py | completed |

#### FEAT-009: split("\n") CRLF Audit (HIGH)

> **Status:** completed
> **Completed:** 2026-02-11 (PR #7)

| ID | Title | Status | Notes |
|----|-------|--------|-------|
| TASK-019 | Fix toon_serializer.py split("\n") (3 usages) | completed | Line 290 kept (in-memory data, allowlisted in arch test) |
| TASK-020 | Fix validate_vtt.py split("\n") | completed | |
| TASK-021 | Fix statusline.py git output split("\n") | completed | |
| TASK-022 | Fix check_agent_conformance.py split("\n") | completed | |
| TASK-023 | Fix compose_agent_template.py split("\n") | completed | |
| TASK-024 | Fix subagent_stop.py split("\n") | completed | |
| TASK-025 | Fix patterns/loader.py split("\n") | completed | |
| TASK-026 | Add cross-platform architecture regression tests | completed | 6 tests in test_cross_platform.py |

#### FEAT-010: Symlink Test Gating

> **Status:** completed
> **Completed:** 2026-02-11 (already in codebase)

| ID | Title | Status | Notes |
|----|-------|--------|-------|
| TASK-027 | Gate symlink tests with os.name == "nt" skip | completed | Already present at test_infrastructure.py:309 |

---

## Completed (PR #7 continued)

### FEAT-011: Migration Script Windows Support

> **Status:** completed
> **Completed:** 2026-02-11 (PR #7)

| ID | Title | Status | Notes |
|----|-------|--------|-------|
| TASK-028 | Add Windows platform guard to verify-platform.sh | completed | Graceful skip with exit 0 on MINGW/MSYS/Cygwin |
| TASK-029 | Add Windows platform guard to verify-symlinks.sh | completed | Graceful skip with exit 0 on MINGW/MSYS/Cygwin |

### FEAT-012: Windows CI Pipeline

> **Status:** completed
> **Completed:** 2026-02-11 (PR #7)

| ID | Title | Status | Notes |
|----|-------|--------|-------|
| TASK-030 | Add windows-latest runner to GitHub Actions | completed | Added to test-uv job matrix (os x python-version) |

---

## Open Bugs

### BUG-001: `uv run jerry transcript parse` fails outside plugin project root

> **Status:** open
> **Priority:** high
> **Reported:** 2026-02-26
> **Affected:** Transcript skill — `uv run jerry transcript parse <file>`

**Description:**

Running `uv run jerry transcript parse <filename>` fails when the working directory
is not the Jerry plugin's project root (i.e. when invoked from a user's own project
or from any directory that does not contain Jerry's `pyproject.toml`).

The correct invocation must include the `--project` flag pointing to the installed
plugin path:

```bash
# BROKEN — only works if CWD contains Jerry's pyproject.toml
uv run jerry transcript parse filename

# CORRECT — works from any directory
uv run --project "~/.claude/plugins/jerry-framework/jerry/0.21.0" jerry transcript parse filename
```

**Root Cause:**

`uv run` resolves the virtual environment and the `jerry` entry point from the
nearest `pyproject.toml` in the current or parent directories. When invoked outside
the plugin install root, UV either errors (no `pyproject.toml` found) or resolves
to the wrong environment.

**Correct plugin path (Windows and Unix):**
```
~/.claude/plugins/cache/jerry-framework/jerry/<version>/
```
Note: `cache/` is part of the path. The `~` tilde expands correctly on both platforms.

**Affected Files Updated:**

| File | Location | Change Made |
|------|----------|-------------|
| `python-environment.md` | `.claude/rules/` | Added `--project` flag guidance + updated Common Commands table |
| `RUNBOOK.md` | `skills/transcript/docs/` | Fixed R-018 §4.6.1 transcript parse command |
| `PLAYBOOK.md` | `skills/transcript/docs/` | Audited — no `uv run jerry` calls found (uses skill invocations) |

**Tasks:**

| ID | Title | Status |
|----|-------|--------|
| TASK-031 | Update python-environment.md with --project flag guidance | completed |
| TASK-032 | Fix RUNBOOK.md R-018 transcript parse example | completed |
| TASK-033 | Audit and fix PLAYBOOK.md transcript parse examples | completed |
| TASK-034 | Verify correct path format for Windows vs Unix plugin installs | completed |

---

## Progress Summary

```
EPIC-001: Windows Compatibility
+------------------------------------------------------------------+
| Features:  [####################] 100% (12/12 completed)         |
| Tasks:     [####################] 100% (34/34 completed)         |
| Bugs:      [####################] 100% (1/1 resolved)            |
+------------------------------------------------------------------+
| Overall:   [####################] 100%                           |
+------------------------------------------------------------------+
```

| Metric | Value |
|--------|-------|
| **Total Features** | 12 |
| **Completed Features** | 12 |
| **In Progress Features** | 0 |
| **Pending Features** | 0 |
| **Total Tasks** | 34 |
| **Completed Tasks** | 34 |
| **Pending Tasks** | 0 |
| **Open Bugs** | 0 |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-10 | Created | Project created; research completed |
| 2026-02-10 | Rebased | PR #4 merged to main; rebased proj/windows-compat; 16 tasks already done |
| 2026-02-11 | PR #7 | FEAT-008, FEAT-009, FEAT-010 completed; 6 arch regression tests added |
| 2026-02-11 | Complete | FEAT-011, FEAT-012 completed; all 12 features and 30 tasks done |
| 2026-02-26 | Reopened | BUG-001 filed: `uv run jerry transcript parse` requires `--project` flag when invoked outside plugin root |
| 2026-02-26 | Complete | BUG-001 resolved: TASK-031–034 done; python-environment.md and RUNBOOK.md updated with correct --project path |
