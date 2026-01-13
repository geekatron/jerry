# PROJ-005-e-006: Functional Requirements Investigation

> **Entry ID:** e-006
> **Topic:** Functional Requirements Investigation - What must scripts/session_start.py do?
> **Severity:** HIGH
> **Date:** 2026-01-13
> **Agent:** ps-investigator v2.1.0

---

## L0: Executive Summary

The `scripts/session_start.py` hook must accomplish three core functions:

1. **Scan projects directory** - Discover available projects matching `PROJ-NNN-slug` pattern
2. **Validate active project** - If `JERRY_PROJECT` is set, validate it exists and is properly configured
3. **Output structured XML tags** - Produce one of three tag types (`<project-context>`, `<project-required>`, `<project-error>`) that Claude Code parses to determine next action

The current broken wrapper delegates to the full implementation via subprocess, but fails when the venv/dependencies are unavailable in plugin mode. A minimum viable implementation can be achieved using **Python stdlib only** (~100 lines).

**Key Finding:** All 3 output scenarios and their exact field formats are documented in CLAUDE.md and enforced by contract tests. Exit code must **always be 0**.

---

## L1: Technical Analysis

### 1. Environment Variables Available

| Variable | Source | Purpose | Reference |
|----------|--------|---------|-----------|
| `CLAUDE_PLUGIN_ROOT` | Claude Code | Plugin installation root directory | hooks/hooks.json:10 |
| `CLAUDE_PROJECT_DIR` | Claude Code | Project root where plugin operates | src/interface/cli/session_start.py:22, 60-61 |
| `JERRY_PROJECT` | User | Active project ID to validate | src/interface/cli/session_start.py:276 |

**Evidence from hooks/hooks.json (lines 8-14):**
```json
{
  "type": "command",
  "command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session_start.py",
  "timeout": 10000
}
```

The script is invoked via `python3` with `CLAUDE_PLUGIN_ROOT` expanded to the plugin directory path.

### 2. Output Format Specification

#### 2.1 Project Context Tag (Valid Project Active)

**When:** `JERRY_PROJECT` is set AND project exists AND validation passes

**Format (from CLAUDE.md lines 121-130):**
```
Jerry Framework initialized. See CLAUDE.md for context.
<project-context>
ProjectActive: {project_id}
ProjectPath: projects/{project_id}/
ValidationMessage: Project is properly configured
</project-context>
```

**Alternative with warnings (src/interface/cli/session_start.py lines 189-193):**
```
ValidationWarnings: {semicolon-separated warnings}
```

**Contract Requirements (test_hook_contract.py lines 58-63):**
- Required fields: `ProjectActive:`, `ProjectPath:`
- One of: `ValidationMessage:` OR `ValidationWarnings:`

#### 2.2 Project Required Tag (No Project Selected)

**When:** `JERRY_PROJECT` is not set or empty

**Format (from CLAUDE.md lines 134-150):**
```
Jerry Framework initialized.
<project-required>
ProjectRequired: true
AvailableProjects:
  - PROJ-001-plugin-cleanup [ACTIVE]
  - PROJ-002-example [DRAFT]
NextProjectNumber: 003
ProjectsJson: [{"id": "PROJ-001-plugin-cleanup", "status": "IN_PROGRESS"}]
</project-required>

ACTION REQUIRED: No JERRY_PROJECT environment variable set.
Claude MUST use AskUserQuestion to help the user select an existing project or create a new one.
DO NOT proceed with any work until a project is selected.
```

**Contract Requirements (test_hook_contract.py lines 65-74):**
- Required fields: `ProjectRequired: true`, `AvailableProjects:`, `NextProjectNumber:`, `ProjectsJson:`
- `ACTION REQUIRED` message must appear after tag

**NextProjectNumber Format (test_hook_contract.py lines 294-296):**
- Must be 3-digit zero-padded (e.g., `001`, `042`, `999`)
- Starts at `001` when no projects exist

**ProjectsJson Format (test_hook_contract.py lines 373-406):**
- Valid JSON array
- Each item has `id` (string, `PROJ-NNN-slug` format) and `status` (enum string)
- Valid statuses: `IN_PROGRESS`, `COMPLETED`, `DRAFT`, `ARCHIVED`, `UNKNOWN`

#### 2.3 Project Error Tag (Invalid Project)

**When:** `JERRY_PROJECT` is set but invalid (bad format or doesn't exist)

**Format (from CLAUDE.md lines 154-168):**
```
Jerry Framework initialized with ERROR.
<project-error>
InvalidProject: {jerry_project_value}
Error: {error_message}
AvailableProjects:
  - PROJ-001-plugin-cleanup [ACTIVE]
NextProjectNumber: 002
</project-error>

ACTION REQUIRED: The specified JERRY_PROJECT is invalid.
Claude MUST use AskUserQuestion to help the user select or create a valid project.
```

**Contract Requirements (test_hook_contract.py lines 76-85):**
- Required fields: `InvalidProject:`, `Error:`, `AvailableProjects:`, `NextProjectNumber:`
- `ACTION REQUIRED` message must appear after tag

### 3. Filesystem Operations Required

#### 3.1 Project Discovery (scan_projects)

**Location:** `{CLAUDE_PROJECT_DIR}/projects/` or `{cwd}/projects/`

**Algorithm (from filesystem_project_adapter.py lines 33-90):**
1. Get projects directory path
2. List all items in directory
3. Filter: directories only, not hidden (`.`), not `archive`
4. Match pattern: `^PROJ-\d{3}-[a-z][a-z0-9]*(?:-[a-z0-9]+)*$`
5. Parse each matching directory name as ProjectId
6. Read project info (status from WORKTRACKER.md)
7. Sort by project number ascending

**Project ID Pattern (project_id.py line 58):**
```python
re.compile(r"^PROJ-(\d{3})-([a-z][a-z0-9]*(?:-[a-z0-9]+)*)$")
```

#### 3.2 Project Status Detection

**Location:** `{project_dir}/WORKTRACKER.md`

**Algorithm (from filesystem_project_adapter.py lines 185-216):**
1. If file doesn't exist: return `UNKNOWN`
2. Read first 2KB of file
3. Search (case-insensitive) for status keywords:
   - `COMPLETED` or `DONE` -> `COMPLETED`
   - `IN_PROGRESS` or `IN PROGRESS` -> `IN_PROGRESS`
   - `DRAFT` -> `DRAFT`
   - `ARCHIVED` -> `ARCHIVED`
   - Otherwise -> `UNKNOWN`

#### 3.3 Project Validation

**Location:** `{projects_dir}/{project_id}/`

**Algorithm (from filesystem_project_adapter.py lines 109-145):**
1. Check directory exists
2. Check directory is actually a directory
3. Check `PLAN.md` exists and is not empty
4. Check `WORKTRACKER.md` exists and is not empty
5. Collect warnings for missing/empty files
6. Return success with warnings, or failure if directory doesn't exist

### 4. Essential vs Nice-to-Have Logic

#### Essential (Minimum Viable)

| Function | Required For | Evidence |
|----------|--------------|----------|
| Read `JERRY_PROJECT` env var | All scenarios | session_start.py:276 |
| Read `CLAUDE_PROJECT_DIR` env var | Path resolution | session_start.py:60-61 |
| List directories in `projects/` | Project discovery | filesystem_project_adapter.py:57-79 |
| Match project ID pattern | Filter valid projects | filesystem_project_adapter.py:68 |
| Read WORKTRACKER.md status | Status display | filesystem_project_adapter.py:185-216 |
| Check directory exists | Validation | filesystem_project_adapter.py:122-126 |
| Output structured tags | Claude parsing | All contract tests |

#### Nice-to-Have (Full Implementation)

| Function | Purpose | Can Defer? |
|----------|---------|------------|
| Local context loading (`.jerry/local/context.toml`) | Worktree-specific project | Yes - env var takes precedence |
| LayeredConfigAdapter | Multi-level config | Yes - not needed for output |
| AtomicFileAdapter | Safe concurrent reads | Yes - simple read is sufficient |
| Empty file detection | Validation warnings | Yes - can just check existence |

### 5. Exit Code Contract

**Critical Rule (test_hook_contract.py lines 439-463):**
- Exit code MUST be `0` in ALL cases
- Even on error, exit 0 and report via output tags
- Claude handles error recovery via output parsing

**Evidence:**
```python
# session_start.py line 263
Returns:
    Exit code (always 0 - we want Claude to handle issues)
```

---

## L2: Systemic Analysis

### 1. Dependency Chain Problem

The current broken wrapper (`scripts/session_start.py`) has a fragile dependency chain:

```
hooks/hooks.json
    |
    +-> python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session_start.py
            |
            +-> subprocess: .venv/bin/jerry-session-start
                    |
                    +-> src.interface.cli.session_start (IMPORTS:)
                            |
                            +-> src.infrastructure.adapters.configuration.*
                            +-> src.infrastructure.adapters.persistence.*
                            +-> src.session_management.application.*
                            +-> src.session_management.infrastructure.*
```

**Root Cause:** When installed as a plugin, the `.venv/` directory and installed packages are not available. The subprocess fallback chain fails at every step.

### 2. Minimum Viable Implementation Scope

A stdlib-only implementation needs:

```python
# ~100 lines, stdlib only
import os
import re
import json
from pathlib import Path

# Functions needed:
# 1. get_project_root() -> Path
# 2. scan_projects(projects_dir: Path) -> list[dict]
# 3. validate_project(project_dir: Path) -> tuple[bool, list[str]]
# 4. read_status(tracker_path: Path) -> str
# 5. output_project_context(project_id: str, validation: tuple)
# 6. output_project_required(projects: list, next_num: int)
# 7. output_project_error(project_id: str, error: str, projects: list, next_num: int)
```

### 3. Contract Compliance Checklist

| Requirement | Contract Test | Must Implement |
|-------------|---------------|----------------|
| Exit code always 0 | test_output_exit_code_semantics_match_hook_spec | Yes |
| Exactly one tag type | test_exactly_one_tag_type_per_output | Yes |
| project-context: ProjectActive field | test_project_active_field_format | Yes |
| project-context: ProjectPath field | test_project_path_field_format | Yes |
| project-context: validation field | test_project_context_contains_required_fields | Yes |
| project-required: all fields | test_project_required_contains_required_fields | Yes |
| project-required: ACTION REQUIRED | test_output_action_required_message_present_when_needed | Yes |
| project-required: NextProjectNumber NNN format | test_next_project_number_format | Yes |
| project-error: all fields | test_project_error_contains_required_fields | Yes |
| project-error: ACTION REQUIRED | test_action_required_on_error | Yes |
| ProjectsJson: valid JSON | test_output_json_matches_schema | Yes |
| ProjectsJson: id format | test_json_id_matches_project_id_format | Yes |
| ProjectsJson: valid status | test_json_status_is_valid_enum | Yes |

### 4. Status Icon Mapping

From `session_start.py` lines 164-170:
```python
status_icon = {
    "IN_PROGRESS": "[ACTIVE]",
    "COMPLETED": "[DONE]",
    "DRAFT": "[DRAFT]",
    "ARCHIVED": "[ARCHIVED]",
    "UNKNOWN": "[?]",
}.get(status_name, "[?]")
```

---

## Findings Summary

### Functional Requirements List

1. **FR-001:** Read `JERRY_PROJECT` environment variable
2. **FR-002:** Read `CLAUDE_PROJECT_DIR` environment variable (fallback to cwd)
3. **FR-003:** Scan `projects/` directory for valid project directories
4. **FR-004:** Match project ID pattern `PROJ-NNN-slug`
5. **FR-005:** Read project status from `WORKTRACKER.md`
6. **FR-006:** Validate project directory exists when `JERRY_PROJECT` is set
7. **FR-007:** Calculate next project number (max + 1, capped at 999)
8. **FR-008:** Output `<project-context>` when valid project active
9. **FR-009:** Output `<project-required>` when no project selected
10. **FR-010:** Output `<project-error>` when project invalid
11. **FR-011:** Always exit with code 0
12. **FR-012:** Generate valid ProjectsJson array

### Output Format Specification

See L1 Section 2 for complete format specifications with evidence citations.

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `CLAUDE_PLUGIN_ROOT` | Plugin installation directory | Available (set by Claude Code) |
| `CLAUDE_PROJECT_DIR` | Project root where plugin operates | Optional (fallback to cwd) |
| `JERRY_PROJECT` | Active project ID | Optional (triggers discovery if not set) |

### Minimum Viable Implementation

A stdlib-only implementation (~100 lines) can satisfy all functional requirements using:
- `os.environ.get()` for environment variables
- `pathlib.Path` for filesystem operations
- `re.compile()` and `re.match()` for pattern matching
- `json.dumps()` for ProjectsJson output
- Basic string formatting for structured output

**Key Insight:** The full implementation's complexity comes from hexagonal architecture patterns and configuration layers that are not needed for the hook's core functionality.

---

## References

| File | Lines | Purpose |
|------|-------|---------|
| `src/interface/cli/session_start.py` | 1-341 | Full implementation reference |
| `scripts/session_start.py` | 1-53 | Broken wrapper |
| `hooks/hooks.json` | 1-41 | Hook invocation config |
| `CLAUDE.md` | 117-218 | Output format documentation |
| `tests/session_management/contract/test_hook_contract.py` | 1-487 | Contract test suite |
| `src/session_management/infrastructure/adapters/filesystem_project_adapter.py` | 1-217 | Filesystem operations |
| `src/session_management/domain/value_objects/project_id.py` | 1-225 | Project ID validation |
| `src/session_management/domain/value_objects/project_status.py` | 1-48 | Status enum |
| `src/session_management/domain/value_objects/validation_result.py` | 1-80 | Validation result |

---

*Investigation completed: 2026-01-13*
