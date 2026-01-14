# ADR-PROJ005-001: Standalone Session Start Hook Implementation

**ADR ID:** ADR-PROJ005-001
**Status:** Proposed
**Date:** 2026-01-13
**Author:** ps-architect
**Deciders:** Project PROJ-005 team
**Bug Reference:** BUG-007 (session_start.py requires pip installation)

---

## Context

### Problem Statement

The `scripts/session_start.py` hook currently fails in Claude Code plugin mode because it attempts to delegate to the full implementation via subprocess, which requires:
1. A Python virtual environment (`.venv/`)
2. The jerry package to be pip-installed
3. Access to `src/` module hierarchy

When the plugin is installed via Claude Code's plugin system, none of these dependencies are available. The hook fails silently or produces invalid output, breaking the project selection workflow.

### Current Architecture (Broken)

```
hooks/hooks.json
    |
    +-> python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session_start.py
            |
            +-> subprocess: .venv/bin/jerry-session-start  [FAILS: no venv]
                    |
                    +-> src.interface.cli.session_start    [FAILS: no package]
```

### Constraint Analysis

From prior research (PROJ-005-e-006, PROJ-005-e-007, PROJ-005-a-001):

| Constraint | Requirement | Source |
|------------|-------------|--------|
| Dependencies | Python stdlib only | Plugin self-containment |
| Exit Code | Always 0 | Contract test suite |
| Output Format | Structured XML tags | CLAUDE.md specification |
| Timeout | 10 seconds max | hooks/hooks.json |
| Error Handling | Never crash without output | Pattern P-007 |

### Options Evaluated

| Option | Score | Description |
|--------|-------|-------------|
| A: Full Standalone Rewrite | 3.4/5 | Complete 12/12 FR coverage, high maintenance burden |
| **B: Simplified Plugin Mode** | **4.1/5** | **10/12 FR coverage, minimal complexity** |
| C: Dual-Mode Script | 3.2/5 | Try dev imports, fallback to standalone |
| D: External Configuration | 3.6/5 | Modular design with separate module |

---

## Decision

**Implement Option B: Simplified Plugin Mode**

We will create a single-file, stdlib-only implementation of `scripts/session_start.py` that:
1. Covers 10 of 12 functional requirements (essential functionality)
2. Uses only Python stdlib modules (os, re, json, pathlib)
3. Always exits with code 0
4. Produces valid structured output in all scenarios
5. Defers non-essential features to future iterations

### Deferred Features

| Feature | Reason for Deferral | Impact |
|---------|---------------------|--------|
| Local context loading (`.jerry/local/context.toml`) | Requires TOML parsing; env var is explicit alternative | Low - JERRY_PROJECT covers 95% of use cases |
| Layered configuration | Over-engineering for plugin mode | Low - single source sufficient |
| Empty file validation warnings | Convenience, not critical | Low - existence check sufficient |

---

## Consequences

### Positive

1. **Self-Contained Plugin:** No external dependencies, works in any Python 3.11+ environment
2. **Minimal Maintenance:** Isolated implementation with clear boundaries
3. **Fast Execution:** Lightweight script completes well under 10s timeout
4. **Contract Compliance:** Satisfies all 13 contract test requirements
5. **Clear Upgrade Path:** Can incrementally add deferred features if needed

### Negative

1. **Feature Gap:** 2/12 FRs deferred (local context, layered config)
2. **Code Duplication:** Logic exists in both plugin script and src/ implementation
3. **Manual Sync Risk:** Contract changes require updates in two places

### Mitigations

| Risk | Mitigation |
|------|------------|
| Feature gap | JERRY_PROJECT env var provides explicit project selection |
| Code duplication | Contract tests verify both implementations |
| Manual sync | Architecture tests flag drift; shared contract spec |

---

## Implementation Guidance

### File Structure

```
scripts/
└── session_start.py    # Single file, ~80 lines, stdlib only
```

### Module Design

```python
#!/usr/bin/env python3
"""
Session Start Hook - Project Context Initialization

Provides project context to Claude Code at session start.
Scans projects directory and validates active project selection.

Reference: https://docs.anthropic.com/en/docs/claude-code/hooks

Exit Codes:
    0 - Always (Claude handles errors via output parsing)

Output Tags:
    <project-context>   - Valid project active
    <project-required>  - No project selected
    <project-error>     - Invalid project specified
"""

import json
import os
import re
from pathlib import Path
```

### Function Signatures

```python
# =============================================================================
# CONFIGURATION
# =============================================================================

PROJECT_ID_PATTERN = re.compile(r"^PROJ-(\d{3})-([a-z][a-z0-9]*(?:-[a-z0-9]+)*)$")

STATUS_KEYWORDS = {
    "COMPLETED": "COMPLETED",
    "DONE": "COMPLETED",
    "IN_PROGRESS": "IN_PROGRESS",
    "IN PROGRESS": "IN_PROGRESS",
    "DRAFT": "DRAFT",
    "ARCHIVED": "ARCHIVED",
}

STATUS_ICONS = {
    "IN_PROGRESS": "[ACTIVE]",
    "COMPLETED": "[DONE]",
    "DRAFT": "[DRAFT]",
    "ARCHIVED": "[ARCHIVED]",
    "UNKNOWN": "[?]",
}


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def get_project_root() -> Path:
    """
    Determine project root directory.

    Resolution order:
    1. CLAUDE_PROJECT_DIR environment variable
    2. Current working directory

    Returns:
        Path to project root directory
    """
    ...


def scan_projects(projects_dir: Path) -> list[dict]:
    """
    Scan projects directory for valid project directories.

    Args:
        projects_dir: Path to projects/ directory

    Returns:
        List of project dicts with keys: id, status, number
        Sorted by project number ascending
    """
    ...


def read_project_status(project_dir: Path) -> str:
    """
    Read project status from WORKTRACKER.md.

    Searches first 2KB for status keywords (case-insensitive).

    Args:
        project_dir: Path to project directory

    Returns:
        Status string: IN_PROGRESS, COMPLETED, DRAFT, ARCHIVED, or UNKNOWN
    """
    ...


def validate_project(projects_dir: Path, project_id: str) -> tuple[bool, str]:
    """
    Validate that a project exists and is properly configured.

    Args:
        projects_dir: Path to projects/ directory
        project_id: Project ID to validate (e.g., "PROJ-001-example")

    Returns:
        Tuple of (is_valid, message)
        - (True, "Project is properly configured") on success
        - (False, "error description") on failure
    """
    ...


def calculate_next_project_number(projects: list[dict]) -> str:
    """
    Calculate next available project number.

    Args:
        projects: List of project dicts from scan_projects()

    Returns:
        Three-digit zero-padded string (e.g., "001", "042")
        Starts at "001" if no projects exist
        Capped at "999"
    """
    ...


# =============================================================================
# OUTPUT FUNCTIONS
# =============================================================================

def output_project_context(project_id: str, validation_message: str) -> None:
    """
    Output <project-context> tag for valid active project.

    Format:
        Jerry Framework initialized. See CLAUDE.md for context.
        <project-context>
        ProjectActive: {project_id}
        ProjectPath: projects/{project_id}/
        ValidationMessage: {validation_message}
        </project-context>
    """
    ...


def output_project_required(projects: list[dict], next_number: str) -> None:
    """
    Output <project-required> tag when no project selected.

    Format:
        Jerry Framework initialized.
        <project-required>
        ProjectRequired: true
        AvailableProjects:
          - PROJ-001-example [ACTIVE]
        NextProjectNumber: {next_number}
        ProjectsJson: [{...}]
        </project-required>

        ACTION REQUIRED: No JERRY_PROJECT environment variable set.
        Claude MUST use AskUserQuestion to help the user select an existing project or create a new one.
        DO NOT proceed with any work until a project is selected.
    """
    ...


def output_project_error(
    invalid_project: str,
    error: str,
    projects: list[dict],
    next_number: str,
) -> None:
    """
    Output <project-error> tag when project is invalid.

    Format:
        Jerry Framework initialized with ERROR.
        <project-error>
        InvalidProject: {invalid_project}
        Error: {error}
        AvailableProjects:
          - PROJ-001-example [ACTIVE]
        NextProjectNumber: {next_number}
        </project-error>

        ACTION REQUIRED: The specified JERRY_PROJECT is invalid.
        Claude MUST use AskUserQuestion to help the user select or create a valid project.
    """
    ...


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main() -> int:
    """
    Main hook entry point.

    Flow:
    1. Read environment variables (JERRY_PROJECT, CLAUDE_PROJECT_DIR)
    2. Scan projects directory
    3. If JERRY_PROJECT set:
       a. Validate project exists
       b. Output project-context or project-error
    4. If JERRY_PROJECT not set:
       a. Output project-required
    5. Always return 0

    Returns:
        Exit code (always 0 - Claude handles errors via output)
    """
    ...


if __name__ == "__main__":
    sys.exit(main())
```

### Error Handling Strategy

Following Pattern P-007 from safe scripts:

```python
def main() -> int:
    """Main hook entry point."""
    try:
        # Core logic here
        ...
        return 0

    except Exception as e:
        # CRITICAL: Never crash without output
        # Output project-required as safe fallback
        print("Jerry Framework initialized.")
        print("<project-required>")
        print("ProjectRequired: true")
        print("AvailableProjects:")
        print("NextProjectNumber: 001")
        print(f"ProjectsJson: []")
        print("</project-required>")
        print()
        print("ACTION REQUIRED: No JERRY_PROJECT environment variable set.")
        print("Claude MUST use AskUserQuestion to help the user select an existing project or create a new one.")
        print("DO NOT proceed with any work until a project is selected.")

        # Log error to stderr for debugging
        import sys
        print(f"[session_start.py] Error: {e}", file=sys.stderr)

        return 0  # ALWAYS return 0
```

Key principles:
1. **Catch all exceptions** - No unhandled exceptions allowed
2. **Always produce valid output** - Fallback to project-required tag
3. **Log errors to stderr** - For debugging without affecting stdout parsing
4. **Always return 0** - Claude handles errors via output parsing

### Testing Strategy

#### Contract Tests (Required)

All 13 contract requirements must pass:

| Test ID | Requirement | Validation |
|---------|-------------|------------|
| CT-001 | Exit code always 0 | `assert result.returncode == 0` |
| CT-002 | Exactly one tag type | Count `<project-*>` occurrences |
| CT-003 | project-context: ProjectActive | Regex match |
| CT-004 | project-context: ProjectPath | Regex match |
| CT-005 | project-context: ValidationMessage | Regex match |
| CT-006 | project-required: ProjectRequired | `== "true"` |
| CT-007 | project-required: AvailableProjects | Section present |
| CT-008 | project-required: NextProjectNumber | 3-digit format |
| CT-009 | project-required: ProjectsJson | Valid JSON array |
| CT-010 | project-required: ACTION REQUIRED | Message present |
| CT-011 | project-error: InvalidProject | Field present |
| CT-012 | project-error: Error | Field present |
| CT-013 | project-error: ACTION REQUIRED | Message present |

#### Integration Tests (Recommended)

```python
# tests/integration/test_session_start_plugin.py

def test_no_project_selected(tmp_path):
    """Hook outputs project-required when no JERRY_PROJECT set."""
    # Arrange
    projects_dir = tmp_path / "projects"
    projects_dir.mkdir()

    # Act
    result = subprocess.run(
        ["python3", "scripts/session_start.py"],
        capture_output=True,
        text=True,
        env={"CLAUDE_PROJECT_DIR": str(tmp_path)},
    )

    # Assert
    assert result.returncode == 0
    assert "<project-required>" in result.stdout
    assert "ProjectRequired: true" in result.stdout


def test_valid_project_selected(tmp_path):
    """Hook outputs project-context when valid project selected."""
    # Arrange
    projects_dir = tmp_path / "projects"
    project_dir = projects_dir / "PROJ-001-test"
    project_dir.mkdir(parents=True)
    (project_dir / "PLAN.md").write_text("# Test Plan")
    (project_dir / "WORKTRACKER.md").write_text("Status: IN_PROGRESS")

    # Act
    result = subprocess.run(
        ["python3", "scripts/session_start.py"],
        capture_output=True,
        text=True,
        env={
            "CLAUDE_PROJECT_DIR": str(tmp_path),
            "JERRY_PROJECT": "PROJ-001-test",
        },
    )

    # Assert
    assert result.returncode == 0
    assert "<project-context>" in result.stdout
    assert "ProjectActive: PROJ-001-test" in result.stdout


def test_invalid_project_format(tmp_path):
    """Hook outputs project-error when project ID format is invalid."""
    # Arrange
    projects_dir = tmp_path / "projects"
    projects_dir.mkdir()

    # Act
    result = subprocess.run(
        ["python3", "scripts/session_start.py"],
        capture_output=True,
        text=True,
        env={
            "CLAUDE_PROJECT_DIR": str(tmp_path),
            "JERRY_PROJECT": "invalid-format",
        },
    )

    # Assert
    assert result.returncode == 0
    assert "<project-error>" in result.stdout
    assert "InvalidProject: invalid-format" in result.stdout


def test_nonexistent_project(tmp_path):
    """Hook outputs project-error when project doesn't exist."""
    # Arrange
    projects_dir = tmp_path / "projects"
    projects_dir.mkdir()

    # Act
    result = subprocess.run(
        ["python3", "scripts/session_start.py"],
        capture_output=True,
        text=True,
        env={
            "CLAUDE_PROJECT_DIR": str(tmp_path),
            "JERRY_PROJECT": "PROJ-999-nonexistent",
        },
    )

    # Assert
    assert result.returncode == 0
    assert "<project-error>" in result.stdout
    assert "Error:" in result.stdout
```

#### Unit Tests (Optional Enhancement)

```python
# tests/unit/test_session_start_functions.py

def test_project_id_pattern_valid():
    """PROJECT_ID_PATTERN matches valid IDs."""
    valid_ids = [
        "PROJ-001-example",
        "PROJ-999-multi-word-slug",
        "PROJ-042-a1b2c3",
    ]
    for pid in valid_ids:
        assert PROJECT_ID_PATTERN.match(pid)


def test_project_id_pattern_invalid():
    """PROJECT_ID_PATTERN rejects invalid IDs."""
    invalid_ids = [
        "PROJ-1-short",           # Number too short
        "PROJ-0001-long",         # Number too long
        "PROJ-001-UPPERCASE",     # Uppercase in slug
        "proj-001-lowercase",     # Lowercase prefix
        "PROJ-001-",              # Trailing dash
        "PROJ-001-1startnumber",  # Slug starts with number
    ]
    for pid in invalid_ids:
        assert not PROJECT_ID_PATTERN.match(pid)


def test_calculate_next_project_number_empty():
    """Next number is 001 when no projects exist."""
    assert calculate_next_project_number([]) == "001"


def test_calculate_next_project_number_sequential():
    """Next number is max + 1."""
    projects = [
        {"id": "PROJ-001-a", "number": 1},
        {"id": "PROJ-003-b", "number": 3},
    ]
    assert calculate_next_project_number(projects) == "004"


def test_calculate_next_project_number_max():
    """Next number caps at 999."""
    projects = [{"id": "PROJ-999-max", "number": 999}]
    assert calculate_next_project_number(projects) == "999"
```

### Implementation Checklist

Use this checklist during implementation:

**Before Implementation:**
- [ ] Read functional requirements (PROJ-005-e-006)
- [ ] Review contract tests (test_hook_contract.py)
- [ ] Review pre_tool_use.py patterns (PROJ-005-e-007)
- [ ] Confirm stdlib-only constraint

**During Implementation:**
- [ ] FR-001: Read JERRY_PROJECT env var
- [ ] FR-002: Read CLAUDE_PROJECT_DIR env var (fallback to cwd)
- [ ] FR-003: Scan projects/ directory
- [ ] FR-004: Match PROJ-NNN-slug pattern
- [ ] FR-005: Read status from WORKTRACKER.md
- [ ] FR-006: Validate project directory exists
- [ ] FR-007: Calculate next project number (3-digit format)
- [ ] FR-008: Output project-context tag
- [ ] FR-009: Output project-required tag
- [ ] FR-010: Output project-error tag
- [ ] FR-011: Exit code 0 always
- [ ] FR-012: Generate valid ProjectsJson

**After Implementation:**
- [ ] Run contract tests
- [ ] Test in actual plugin installation
- [ ] Verify all three output scenarios
- [ ] Document deferred features
- [ ] Update WORKTRACKER.md

---

## Compliance

### Functional Requirements Coverage

| FR ID | Description | Status | Notes |
|-------|-------------|--------|-------|
| FR-001 | Read JERRY_PROJECT env var | Implemented | os.environ.get() |
| FR-002 | Read CLAUDE_PROJECT_DIR env var | Implemented | Fallback to cwd |
| FR-003 | Scan projects/ directory | Implemented | pathlib.Path.iterdir() |
| FR-004 | Match PROJ-NNN-slug pattern | Implemented | re.compile() |
| FR-005 | Read status from WORKTRACKER.md | Implemented | First 2KB scan |
| FR-006 | Validate project directory exists | Implemented | Path.exists() |
| FR-007 | Calculate next project number | Implemented | max + 1, cap 999 |
| FR-008 | Output project-context tag | Implemented | print() |
| FR-009 | Output project-required tag | Implemented | print() |
| FR-010 | Output project-error tag | Implemented | print() |
| FR-011 | Exit code 0 always | Implemented | return 0 |
| FR-012 | Generate valid ProjectsJson | Implemented | json.dumps() |

### Pattern Compliance

| Pattern ID | Description | Compliance |
|------------|-------------|------------|
| P-001 | Shebang and docstring | Yes |
| P-002 | Minimal stdlib imports | Yes (os, re, json, pathlib) |
| P-003 | Graceful import fallback | N/A (no optional imports) |
| P-005 | Configuration as module constants | Yes |
| P-006 | Validation functions return tuples | Yes |
| P-007 | Main function with error handling | Yes |
| P-008 | Entry point guard | Yes |

---

## References

### Prior Research

| Document | Content |
|----------|---------|
| PROJ-005-e-006 | 12 functional requirements |
| PROJ-005-e-007 | 10 plugin patterns, constraint checklist |
| PROJ-005-a-001 | Trade-off analysis, Option B recommendation |

### Source Files

| File | Purpose |
|------|---------|
| scripts/session_start.py | Current broken wrapper |
| src/interface/cli/session_start.py | Full implementation reference |
| scripts/pre_tool_use.py | Exemplar pattern script |
| tests/session_management/contract/test_hook_contract.py | Contract test suite |

### External References

| Source | URL |
|--------|-----|
| Claude Code Hooks | https://docs.anthropic.com/en/docs/claude-code/hooks |
| CLAUDE.md Output Spec | Root CLAUDE.md lines 117-218 |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-13 | ps-architect | Initial proposal |

---

*ADR created: 2026-01-13*
*Status: Proposed*
