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

## Problem Statement (Revised via DISC-004)

**IMPORTANT**: This enabler was revised based on [DISC-004](./disc-004-hook-format-correction.md) which corrected earlier misunderstandings.

### What We Now Know

1. **Hook output format IS CORRECT** - `hookSpecificOutput.additionalContext` is the official Claude Code Advanced JSON format
2. **XML tags ARE VALID** - Anthropic recommends XML for structuring prompts for Claude
3. **Architecture violation remains** - `cli/session_start.py` still violates hexagonal architecture

### Actual Problems to Fix

1. **`cli/session_start.py` violates hexagonal architecture** - Direct infrastructure imports in interface layer
2. **Duplicate entry points** - Both `jerry` and `jerry-session-start` in pyproject.toml
3. **Missing local context support** - `.jerry/local/context.toml` not read by main CLI
4. **Missing separation of concerns** - CLI should output generic JSON, hook adapter transforms to hook format

### Related Artifacts
- [DISC-001](./disc-001-functional-gap-analysis.md): Functional gap analysis
- [DISC-002](./disc-002-architectural-drift-rca.md): Architectural drift RCA
- [DISC-003](./disc-003-phantom-xml-syntax.md): ~~Phantom XML syntax~~ **SUPERSEDED**
- [DISC-004](./disc-004-hook-format-correction.md): **Hook format correction (authoritative)**
- [DISC-005](./disc-005-combined-hook-output-test.md): **Combined output empirical test (CONFIRMED)**
- [TD-001](./td-001-session-start-violates-hexagonal.md): Hexagonal architecture violation
- [TD-002](./td-002-duplicate-entry-points.md): Duplicate entry points
- [TD-003](./td-003-missing-local-context-support.md): Missing local context support

---

## Correct Hook Output Format

Per official Claude Code documentation and **empirically verified** via [DISC-005](./disc-005-combined-hook-output-test.md):

### SessionStart Combined Format (VERIFIED)

```json
{
  "systemMessage": "Jerry Framework initialized.\n\nProject: PROJ-007-jerry-bugs\nPath: projects/PROJ-007-jerry-bugs/\nStatus: Valid and configured",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Jerry Framework initialized.\n<project-context>\nProjectActive: PROJ-007-jerry-bugs\nProjectPath: projects/PROJ-007-jerry-bugs/\nValidationMessage: Project is properly configured\n</project-context>"
  }
}
```

### Field Definitions (Empirically Verified)

| Field | Type | Purpose | Who Sees It |
|-------|------|---------|-------------|
| `systemMessage` | string | User notification in terminal | **User (terminal)** |
| `additionalContext` | string | Content added to Claude's context | **Claude (LLM)** |

**Verified:** Both fields work together. User requested detailed `systemMessage` for visibility into hook execution.

### XML Tags Inside `additionalContext` (KEEP)

```xml
<project-context>
ProjectActive: PROJ-007-jerry-bugs
ProjectPath: projects/PROJ-007-jerry-bugs/
ValidationMessage: Project is properly configured
</project-context>
```

These are valid per Anthropic's prompt engineering best practices for structuring data for LLMs.

---

## Acceptance Criteria (Revised per DISC-004 + DISC-005)

- [ ] **AC-001**: `jerry projects context --json` outputs clean JSON with project data
- [ ] **AC-002**: `session_start_hook.py` calls CLI and transforms output to combined format
- [ ] **AC-003**: Hook output includes BOTH `systemMessage` (user visibility) AND `hookSpecificOutput.additionalContext` (Claude context) - **verified via DISC-005**
- [ ] **AC-004**: XML tags preserved in `additionalContext` for Claude parsing
- [ ] **AC-005**: Local context reading (`.jerry/local/context.toml`) works via main CLI
- [ ] **AC-006**: `cli/session_start.py` is deleted (architecture violation)
- [ ] **AC-007**: `jerry-session-start` entry point removed from pyproject.toml
- [ ] **AC-008**: CLAUDE.md updated to clarify hook output format with citations
- [ ] **AC-009**: All tests pass: Unit, Integration, System, E2E, Contract, Architecture

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
│  ADAPTER LAYER - Transforms CLI output to Advanced JSON          │
│                                                                  │
│  Responsibilities:                                               │
│  - Bootstrap uv environment                                      │
│  - Call: jerry projects context --json                           │
│  - Transform JSON → hookSpecificOutput.additionalContext         │
│  - Format additionalContext with XML tags for Claude             │
│  - Handle errors gracefully                                      │
│                                                                  │
│  Output Format (Verified Combined - DISC-005):                   │
│  {                                                               │
│    "systemMessage": "Jerry Framework initialized...",            │
│    "hookSpecificOutput": {                                       │
│      "hookEventName": "SessionStart",                            │
│      "additionalContext": "<project-context>...</project-context>"│
│    }                                                             │
│  }                                                               │
└───────────────────────────────────┬─────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   jerry projects context --json                  │
│  GENERIC CLI - Clean JSON output (no hook-specific format)       │
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

## BDD Test Pyramid

Per testing-standards.md, all features require comprehensive test coverage:

```
                    ┌─────────────┐
                    │    E2E      │ ← Full workflow (5%)
                   ┌┴─────────────┴┐
                   │    System     │ ← Component interaction (10%)
                  ┌┴───────────────┴┐
                  │   Integration   │ ← Adapter/port testing (15%)
                 ┌┴─────────────────┴┐
                 │       Unit        │ ← Domain logic (60%)
                ┌┴───────────────────┴┐
                │ Contract+Architecture│ ← Interface compliance (10%)
                └─────────────────────┘
```

---

## Tasks (BDD Red/Green/Refactor)

### Phase 1: UNIT TESTS (60%) - Domain and Application Layer

#### RED: Write Failing Tests

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-001 | Write unit test: ProjectContextDTO contains all required fields | PENDING | - |
| T-002 | Write unit test: RetrieveProjectContextQuery with env var set | PENDING | - |
| T-003 | Write unit test: RetrieveProjectContextQuery with local context | PENDING | - |
| T-004 | Write unit test: RetrieveProjectContextQuery precedence (env > local > discovery) | PENDING | - |
| T-005 | Write unit test: RetrieveProjectContextQuery with no project returns available list | PENDING | - |
| T-006 | Write unit test: RetrieveProjectContextQuery with invalid project returns error | PENDING | - |
| T-007 | Write unit test: LocalContextReader reads .jerry/local/context.toml | PENDING | - |
| T-008 | Write unit test: LocalContextReader handles missing file gracefully | PENDING | - |

#### GREEN: Implement to Pass

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-009 | Implement LocalContextReader port and adapter | PENDING | - |
| T-010 | Update RetrieveProjectContextQueryHandler to use LocalContextReader | PENDING | - |
| T-011 | Implement configuration precedence logic | PENDING | - |
| T-012 | Run unit tests - all pass | PENDING | - |

---

### Phase 2: INTEGRATION TESTS (15%) - Adapter Layer

#### RED: Write Failing Tests

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-013 | Write integration test: FilesystemLocalContextAdapter reads TOML | PENDING | - |
| T-014 | Write integration test: CLIAdapter.cmd_projects_context returns valid JSON | PENDING | - |
| T-015 | Write integration test: CLIAdapter.cmd_projects_context includes all fields | PENDING | - |

#### GREEN: Implement to Pass

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-016 | Implement FilesystemLocalContextAdapter | PENDING | - |
| T-017 | Update CLIAdapter.cmd_projects_context for full JSON output | PENDING | - |
| T-018 | Register adapter in bootstrap.py | PENDING | - |
| T-019 | Run integration tests - all pass | PENDING | - |

---

### Phase 3: CONTRACT TESTS (5%) - Hook Output Compliance

#### RED: Write Failing Tests

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-020 | Write contract test: Hook output is valid JSON | PENDING | - |
| T-021 | Write contract test: Hook output has `hookSpecificOutput` object | PENDING | - |
| T-022 | Write contract test: Hook output has `hookEventName: "SessionStart"` | PENDING | - |
| T-023 | Write contract test: Hook output has `additionalContext` string | PENDING | - |
| T-024 | Write contract test: `additionalContext` contains project XML tags | PENDING | - |

#### GREEN: Verify or Fix

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-025 | Verify current hook output matches contract | PENDING | - |
| T-026 | Run contract tests - all pass | PENDING | - |

---

### Phase 4: ARCHITECTURE TESTS (5%) - Layer Boundaries

#### RED: Write Failing Tests

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-027 | Write arch test: cli/adapter.py has no infrastructure imports | PENDING | - |
| T-028 | Write arch test: session_start_hook.py only imports subprocess/json | PENDING | - |
| T-029 | Write arch test: No duplicate entry points in pyproject.toml | PENDING | - |
| T-030 | Write arch test: cli/session_start.py does not exist | PENDING | - |

#### GREEN: Refactor to Pass

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-031 | Delete cli/session_start.py | PENDING | - |
| T-032 | Remove jerry-session-start from pyproject.toml | PENDING | - |
| T-033 | Refactor session_start_hook.py to call jerry CLI | PENDING | - |
| T-034 | Run architecture tests - all pass | PENDING | - |

---

### Phase 5: SYSTEM TESTS (10%) - Component Interaction

#### RED: Write Failing Tests

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-035 | Write system test: CLI + LocalContext → correct project | PENDING | - |
| T-036 | Write system test: CLI + EnvVar + LocalContext → env var wins | PENDING | - |
| T-037 | Write system test: Hook script calls CLI and transforms output | PENDING | - |

#### GREEN: Implement and Verify

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-038 | Wire all components together | PENDING | - |
| T-039 | Run system tests - all pass | PENDING | - |

---

### Phase 6: E2E TESTS (5%) - Full Workflow

#### RED: Write Failing Tests

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-040 | Write E2E test: Start Claude Code session with JERRY_PROJECT set | PENDING | - |
| T-041 | Write E2E test: Start Claude Code session with local context | PENDING | - |
| T-042 | Write E2E test: Start Claude Code session with no project | PENDING | - |
| T-043 | Write E2E test: Hook output appears in Claude context | PENDING | - |

#### GREEN: Verify Full Stack

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-044 | Run E2E tests - all pass | PENDING | - |
| T-045 | Manual smoke test: start Claude Code session | PENDING | - |

---

### Phase 7: CLEANUP - Documentation and Migration

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-046 | Update CLAUDE.md: Document correct hook format with citations | PENDING | - |
| T-047 | Update testing-standards.md: Fix contract test example | PENDING | - |
| T-048 | Update BEHAVIOR_TESTS.md: Fix XML tag expectations | PENDING | - |
| T-049 | Update runbooks: Fix hook output expectations | PENDING | - |
| T-050 | Migrate existing tests to correct locations | PENDING | - |

---

### Phase 8: VALIDATION - Final Checks

| ID | Task | Status | Evidence |
|----|------|--------|----------|
| T-051 | Run full test suite: pytest --cov=src | PENDING | - |
| T-052 | Verify coverage >= 90% | PENDING | - |
| T-053 | Run ruff check src/ tests/ | PENDING | - |
| T-054 | Run mypy src/ | PENDING | - |
| T-055 | Final manual smoke test | PENDING | - |

---

## Files to Modify

| File | Action | Changes |
|------|--------|---------|
| `src/interface/cli/adapter.py` | MODIFY | Ensure `cmd_projects_context` supports full JSON output |
| `src/application/ports/secondary/` | ADD | `ilocal_context_reader.py` port |
| `src/infrastructure/adapters/persistence/` | ADD | `filesystem_local_context_adapter.py` |
| `src/bootstrap.py` | MODIFY | Wire LocalContextReader |
| `scripts/session_start_hook.py` | REWRITE | Call jerry CLI, transform to Advanced JSON |
| `pyproject.toml` | MODIFY | Remove `jerry-session-start` entry |
| `CLAUDE.md` | MODIFY | Update hook output documentation with citations |
| `.claude/rules/testing-standards.md` | MODIFY | Fix contract test example |
| `docs/governance/BEHAVIOR_TESTS.md` | MODIFY | Fix XML tag scenarios |
| `runbooks/RUNBOOK-001-plugin-regression-playbook.md` | MODIFY | Fix hook output expectations |
| `src/interface/cli/session_start.py` | DELETE | Rogue file violating hexagonal architecture |

---

## Evidence Sources (Citations)

| Source | URL | What It Proves |
|--------|-----|----------------|
| Official Claude Code Docs | https://code.claude.com/docs/en/hooks#advanced:-json-output | `hookSpecificOutput.additionalContext` is official format |
| GitHub Issue #13650 | https://github.com/anthropics/claude-code/issues/13650 | Bug that was fixed in v2.0.76 |
| Anthropic Prompt Engineering | https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching#structuring-your-prompt | XML tags recommended for Claude |

---

## Dependencies

- Python 3.11+
- uv package manager
- pytest for testing
- Claude Code v2.0.76+ (bug fix for SessionStart stdout)

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Enabler created with 21 TDD tasks | Claude |
| 2026-01-15 | REVISED: Scope updated based on RCA (33 tasks) | Claude |
| 2026-01-20 | REVISED: Architecture changed based on DISC-003 (34 tasks) | Claude |
| 2026-01-20 | **MAJOR REVISION**: Corrected per DISC-004 - keep hookSpecificOutput format | Claude |
| 2026-01-20 | Added comprehensive BDD test pyramid (55 tasks across 8 phases) | Claude |
| 2026-01-20 | Added evidence sources with citations | Claude |
| 2026-01-21 | **DISC-005 CONFIRMED**: Combined `systemMessage` + `additionalContext` works | Claude |
| 2026-01-21 | Updated AC-003 and architecture to use combined format | Claude |
