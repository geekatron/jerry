# EN-001: Session Start Hook TDD Cleanup

> **Enabler:** Session Start Hook TDD Cleanup
> **Feature:** [FT-001](./FEATURE-WORKTRACKER.md) Session Hook Cleanup
> **Solution Epic:** [SE-004](../SOLUTION-WORKTRACKER.md) CLI and Claude Code Integration
> **Project:** PROJ-007-jerry-bugs
> **Status:** IN PROGRESS
> **Type:** Enabler (Technical Work)
> **Created:** 2026-01-15
> **Last Updated:** 2026-01-20

---

## Problem Statement (Revised via RCA + Discovery)

Root Cause Analysis and subsequent discovery revealed multiple issues:

1. **`cli/session_start.py` shouldn't exist** - It's a rogue entry point that violates hexagonal architecture
2. **Phantom XML syntax** - The `<project-context>` tags and `hookSpecificOutput` structure are not part of Claude Code API
3. **`cli/main.py` is missing functionality** - Features implemented in session_start.py are not in main.py
4. **`session_start_hook.py` should transform CLI output** - Not call a separate entry point

### Related Technical Debt
- [TD-001](./td-001-session-start-violates-hexagonal.md): Hexagonal architecture violation
- [TD-002](./td-002-duplicate-entry-points.md): Duplicate entry points
- [TD-003](./td-003-missing-local-context-support.md): Missing local context support

### Related Discoveries
- [DISC-001](./disc-001-functional-gap-analysis.md): Functional gap analysis
- [DISC-002](./disc-002-architectural-drift-rca.md): Architectural drift RCA
- [DISC-003](./disc-003-phantom-xml-syntax.md): **Phantom XML syntax discovery**

---

## Key Discovery: Phantom XML Syntax

Investigation via Context7 revealed that the XML-like tags and `hookSpecificOutput` structure are **not part of the Claude Code API**:

### Official Claude Code Hook Output

```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Message for Claude"
}
```

### What Jerry Incorrectly Uses

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "<project-context>...</project-context>"
  }
}
```

**Action:** Remove phantom syntax. Use standard `systemMessage` format.

See [DISC-003](./disc-003-phantom-xml-syntax.md) for full investigation.

---

## Acceptance Criteria (Revised)

- [ ] **AC-001**: `jerry projects context --json` outputs clean JSON with project data
- [ ] **AC-002**: `session_start_hook.py` calls CLI and transforms output to standard hook format
- [ ] **AC-003**: Hook output uses `systemMessage` field (not `hookSpecificOutput`)
- [ ] **AC-004**: No XML-like tags in output - use plain text or structured content
- [ ] **AC-005**: Local context reading (`.jerry/local/context.toml`) works via main CLI
- [ ] **AC-006**: `cli/session_start.py` is deleted
- [ ] **AC-007**: `jerry-session-start` entry point removed from pyproject.toml
- [ ] **AC-008**: CLAUDE.md updated to document actual hook output format
- [ ] **AC-009**: All existing E2E and contract tests pass (migrated or updated)

---

## Target Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code Hook System                       │
└───────────────────────────────────┬─────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│              scripts/session_start_hook.py                       │
│  ADAPTER LAYER - Transforms CLI output for Claude                │
│                                                                  │
│  Responsibilities:                                               │
│  - Bootstrap uv environment                                      │
│  - Call: jerry projects context --json                           │
│  - Transform JSON → standard hook output format                  │
│  - Format systemMessage with project info (plain text)           │
│  - Handle errors gracefully                                      │
│                                                                  │
│  Output Format (Standard Claude Code):                           │
│  {                                                               │
│    "continue": true,                                             │
│    "systemMessage": "Jerry Framework initialized.\n\n..."        │
│  }                                                               │
└───────────────────────────────────┬─────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   jerry projects context --json                  │
│  GENERIC CLI - Clean JSON output                                 │
│                                                                  │
│  {                                                               │
│    "project_id": "PROJ-007-jerry-bugs",                         │
│    "project_path": "projects/PROJ-007-jerry-bugs/",             │
│    "validation": {                                               │
│      "is_valid": true,                                           │
│      "messages": []                                              │
│    },                                                            │
│    "available_projects": [...],                                  │
│    "next_number": 8                                              │
│  }                                                               │
└───────────────────────────────────┬─────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                           │
│  RetrieveProjectContextQuery (with local context precedence)     │
│  - Checks JERRY_PROJECT env var                                  │
│  - Falls back to .jerry/local/context.toml                       │
│  - Scans available projects                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tasks (TDD Cycle - Revised)

### Phase 1: RED - Write Failing Tests for CLI JSON Output

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-001 | Write test: `jerry projects context --json` returns valid JSON | PENDING | - |
| T-002 | Write test: JSON includes `project_id` when JERRY_PROJECT set | PENDING | - |
| T-003 | Write test: JSON includes `validation` object | PENDING | - |
| T-004 | Write test: JSON includes `available_projects` array | PENDING | - |
| T-005 | Write test: JSON includes `next_number` for project creation | PENDING | - |

### Phase 2: RED - Write Failing Tests for Local Context Support

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-006 | Write test: CLI reads project from `.jerry/local/context.toml` | PENDING | - |
| T-007 | Write test: env var `JERRY_PROJECT` takes precedence over local context | PENDING | - |
| T-008 | Write test: local context file missing is handled gracefully | PENDING | - |

### Phase 3: RED - Write Failing Tests for Hook Adapter

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-009 | Write test: hook adapter calls `jerry projects context --json` | PENDING | - |
| T-010 | Write test: hook adapter outputs standard format `{"continue": true, "systemMessage": "..."}` | PENDING | - |
| T-011 | Write test: hook adapter formats project info as plain text (no XML tags) | PENDING | - |
| T-012 | Write test: hook adapter handles CLI error gracefully | PENDING | - |
| T-013 | Write test: hook adapter handles CLI timeout | PENDING | - |
| T-014 | Write test: hook adapter handles missing uv | PENDING | - |

### Phase 4: GREEN - Implement/Verify CLI JSON Output

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-015 | Verify `--json` flag exists on `projects context` command | PENDING | - |
| T-016 | Implement/update `cmd_projects_context` to return full context as JSON | PENDING | - |
| T-017 | Ensure JSON output includes all required fields | PENDING | - |

### Phase 5: GREEN - Implement Local Context Support

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-018 | Add local context reading to bootstrap or query handler | PENDING | - |
| T-019 | Implement configuration precedence (env > local > discovery) | PENDING | - |
| T-020 | Update `RetrieveProjectContextQuery` to support precedence | PENDING | - |

### Phase 6: GREEN - Rewrite Hook Adapter

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-021 | Refactor hook adapter for testability (DI for subprocess) | PENDING | - |
| T-022 | Implement CLI call: `jerry projects context --json` | PENDING | - |
| T-023 | Implement JSON transformation to standard hook format | PENDING | - |
| T-024 | Format `systemMessage` with project info (plain text, no XML) | PENDING | - |
| T-025 | Implement error handling with graceful fallback | PENDING | - |

### Phase 7: CLEANUP - Remove Rogue Components

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-026 | Delete `src/interface/cli/session_start.py` | PENDING | - |
| T-027 | Remove `jerry-session-start` from pyproject.toml | PENDING | - |
| T-028 | Migrate relevant tests to proper locations | PENDING | - |
| T-029 | Update CLAUDE.md hook output documentation | PENDING | - |
| T-030 | Remove XML-tag references from all documentation | PENDING | - |

### Phase 8: Validation

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-031 | Run all E2E tests - verify they pass | PENDING | - |
| T-032 | Run all contract tests - verify they pass | PENDING | - |
| T-033 | Run architecture tests - verify no layer violations | PENDING | - |
| T-034 | Manual smoke test: start Claude Code session | PENDING | - |

---

## Hook Output Format (Corrected)

### Before (Phantom Syntax)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Jerry Framework initialized.\n<project-context>\nProjectActive: PROJ-007\n</project-context>"
  }
}
```

### After (Standard Claude Code Format)

```json
{
  "continue": true,
  "systemMessage": "Jerry Framework initialized. See CLAUDE.md for context.\n\nProject: PROJ-007-jerry-bugs\nPath: projects/PROJ-007-jerry-bugs/\nStatus: Valid and configured\n\nReady to proceed with work in the active project context."
}
```

Or when no project is selected:

```json
{
  "continue": true,
  "systemMessage": "Jerry Framework initialized.\n\nNo active project selected.\n\nAvailable Projects:\n- PROJ-001-plugin-cleanup [ACTIVE]\n- PROJ-007-jerry-bugs [ACTIVE]\n\nPlease select a project or create a new one using AskUserQuestion."
}
```

---

## Files to Modify

| File | Action | Changes |
|------|--------|---------|
| `src/interface/cli/adapter.py` | MODIFY | Ensure `cmd_projects_context` supports full JSON output |
| `src/bootstrap.py` | MODIFY | Add local context support if needed |
| `scripts/session_start_hook.py` | REWRITE | Transform CLI JSON → standard hook format |
| `pyproject.toml` | MODIFY | Remove `jerry-session-start` entry |
| `CLAUDE.md` | MODIFY | Update hook output documentation |
| `src/interface/cli/session_start.py` | DELETE | Rogue file |
| Various test files | MODIFY | Migrate and update |

---

## CLAUDE.md Update Required

The "Project Enforcement" section needs to be updated to document the actual hook output format:

**Remove:**
- XML-like tag documentation (`<project-context>`, etc.)
- References to parsing structured tags

**Add:**
- Standard `systemMessage` format
- Plain text project information
- Clear separation between CLI output (JSON) and hook output (systemMessage)

---

## Dependencies

- Python 3.11+
- uv package manager
- pytest for testing
- Context7 research for Claude Code API verification

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Enabler created with 21 TDD tasks | Claude |
| 2026-01-15 | REVISED: Scope updated based on RCA (33 tasks) | Claude |
| 2026-01-20 | **REVISED**: Architecture changed based on DISC-003 (34 tasks) | Claude |
| 2026-01-20 | Removed `--format hook` from CLI - hook adapter handles formatting | Claude |
| 2026-01-20 | Removed XML-like tags - using standard systemMessage format | Claude |
